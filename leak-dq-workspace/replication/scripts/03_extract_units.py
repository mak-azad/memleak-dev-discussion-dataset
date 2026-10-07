"""Step 3 - turn raw threads into coding units with stable keys.

  python scripts/03_extract_units.py            # all passes/sources present under data/raw/

Units (data/units/<pass>_<source>.jsonl):
  Stack Overflow  - memory-related interrogative sentences (asker or responder).
                    unit_key = sha1(post_permalink + US + sentence)[:16]
  GitHub, main    - interrogatives (form Q) and regex-prefiltered diagnostic statements (form S).
                    unit_key = issue_url|comment_id|form|ordinal   (comment_id '-' = issue title/body)
  GitHub, offcwe  - interrogatives and leak-keyword statements (max 4 statements per post).
                    unit_key = issue_url|comment_id|ordinal

The selection rules mirror the Oct-2026 run exactly; see dq/codebook.py.
"""
from __future__ import annotations

import hashlib
import html
import json
from typing import Any, Iterator

from common import RAW, UNITS, log, write_jsonl
from dq.codebook import (GH_KEY_OFF, GH_MEM_Q_MAIN, GH_MEM_Q_OFF, SO_ALLOC_HINT, SO_LANG_TAGS, SO_LEAK_OFF,
                         SO_MEM_MAIN, SO_MEM_OFF, cwe_signatures, dq_prefilter, gh_sentences, so_clean,
                         so_interrogatives)


def skey(link: str, s: str) -> str:
    return hashlib.sha1(f"{link}\x1f{s}".encode()).hexdigest()[:16]


def load(name: str) -> Any:
    p = RAW / name
    return json.loads(p.read_text()) if p.exists() else None


# ------------------------------------------------------------------ Stack Overflow
def so_main_threads(D: dict[str, Any]) -> dict[int, list[str]]:
    """Main-pass thread filter: C/C++-ish tag, allocation hint, >=1 CWE signature."""
    kept: dict[int, list[str]] = {}
    for q in D["questions"]:
        if not set(q["tags"]) & SO_LANG_TAGS:
            continue
        raw = html.unescape(q["title"]) + " " + html.unescape(_strip_tags(q.get("body", "")))
        if not SO_ALLOC_HINT.search(raw):
            continue
        sig = cwe_signatures(raw)
        if sig:
            kept[q["question_id"]] = sig
    return kept


def _strip_tags(h: str) -> str:
    import re
    return re.sub(r"<[^>]+>", " ", h or "")


def so_posts(D: dict[str, Any], qids: set[int]) -> Iterator[tuple[dict[str, Any], str, str, str, str]]:
    """Yield (question, role, post_kind, permalink, cleaned_text) for questions in qids."""
    qmap = {q["question_id"]: q for q in D["questions"] if q["question_id"] in qids}
    owner = {qid: q.get("owner", {}).get("user_id") for qid, q in qmap.items()}
    ans_q = {a["answer_id"]: a["question_id"] for a in D["answers"]}
    for q in qmap.values():
        t = html.unescape(q["title"])
        if t.strip().endswith("?"):
            yield q, "asker", "title", q["link"], "\0TITLE\0" + t
        yield q, "asker", "question", q["link"], so_clean(q.get("body", ""))
    for a in D["answers"]:
        if a["question_id"] in qmap:
            role = "asker" if a.get("owner", {}).get("user_id") == owner[a["question_id"]] else "responder"
            yield qmap[a["question_id"]], role, "answer", f"https://stackoverflow.com/a/{a['answer_id']}", so_clean(a.get("body", ""))
    for c in D["comments"]:
        qid = c["post_id"] if c["post_id"] in qmap else ans_q.get(c["post_id"])
        if qid in qmap:
            role = "asker" if c.get("owner", {}).get("user_id") == owner[qid] else "responder"
            yield (qmap[qid], role, "comment",
                   f"https://stackoverflow.com/questions/{qid}/#comment{c['comment_id']}_{c['post_id']}",
                   so_clean(c.get("body", "")))


def so_units(D: dict[str, Any], qids: set[int], pass_: str, sig: dict[int, list[str]], origin: str,
             mem, extra=None, seen: set[tuple[int, str]] | None = None) -> list[dict[str, Any]]:
    seen = set() if seen is None else seen
    out = []
    for q, role, kind, link, text in so_posts(D, qids):
        sents = [text[len("\0TITLE\0"):]] if text.startswith("\0TITLE\0") else so_interrogatives(text, mem)
        for s in sents:
            if extra is not None and not extra.search(s):
                continue
            if (q["question_id"], s) in seen:
                continue
            seen.add((q["question_id"], s))
            out.append({"unit_key": skey(link, s), "source": "Stack Overflow", "pass": pass_, "origin": origin,
                        "thread_url": q["link"], "post_permalink": link, "role": role, "post_kind": kind,
                        "form": "question", "thread_cwe_signatures": sig.get(q["question_id"], []),
                        "query_buckets": q.get("query_buckets", []), "text": s})
    return out


# ------------------------------------------------------------------ GitHub
def gh_role(author: str | None, issue_author: str | None, assoc: str | None) -> str:
    if author and author == issue_author:
        return "R"
    return "M" if assoc in ("OWNER", "MEMBER", "COLLABORATOR") else "O"


def gh_posts(iss: dict[str, Any]) -> list[tuple[str, str, str]]:
    posts = [("-", "R", iss["body"])]
    posts += [(str(c["id"]), gh_role(c["author"], iss["author"], c["author_association"]), c["body"]) for c in iss["comments"]]
    return posts


def gh_main_units(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for iss in issues:
        url, sig = iss["url"], cwe_signatures(iss["title"] + " " + iss["body"])
        ordc: dict[tuple[str, str], int] = {}

        def emit(cid: str, role: str, form: str, s: str) -> None:
            k = (cid, form)
            o = ordc.get(k, 0)
            ordc[k] = o + 1
            out.append({"unit_key": f"{url}|{cid}|{form}|{o}", "source": "GitHub", "pass": "main", "thread_url": url,
                        "post_permalink": url + (f"#issuecomment-{cid}" if cid != "-" else ""), "role": role,
                        "form": "question" if form == "Q" else "statement", "thread_cwe_signatures": sig,
                        "query_buckets": iss["query_buckets"], "text": s})
        # interrogatives: title first (if it is a question), then every post in order
        if iss["title"].strip().endswith("?"):
            emit("-", "R", "Q", iss["title"].strip())
        for cid, role, body in gh_posts(iss):
            for s in gh_sentences(body, 12, 400):
                if s.endswith("?") and GH_MEM_Q_MAIN.search(s):
                    emit(cid, role, "Q", s)
        # statements prefiltered by the DQ regexes (all roles)
        for cid, role, body in gh_posts(iss):
            for s in gh_sentences(body, 12, 400):
                if dq_prefilter(s):
                    emit(cid, role, "S", s)
    return out


def gh_offcwe_units(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for iss in issues:
        url = iss["url"]
        for cid, role, body in gh_posts(iss):
            o = k = 0
            for s in gh_sentences(body, 15, 350):
                q = s.endswith("?")
                if (q and GH_MEM_Q_OFF.search(s)) or (GH_KEY_OFF.search(s) and k < 4):
                    out.append({"unit_key": f"{url}|{cid}|{o}", "source": "GitHub", "pass": "offcwe", "thread_url": url,
                                "post_permalink": url + (f"#issuecomment-{cid}" if cid != "-" else ""), "role": role,
                                "form": "question" if q else "statement", "query_buckets": iss["query_buckets"],
                                "text": s[:240]})
                    o += 1
                    if not q:
                        k += 1
    return out


def main() -> None:
    so_main = load("so_main.json")
    kept: dict[int, list[str]] = {}
    if so_main:
        kept = so_main_threads(so_main)
        n = write_jsonl(UNITS / "main_so.jsonl", so_units(so_main, set(kept), "main", kept, "search", SO_MEM_MAIN))
        log(f"main_so: {len(kept)} threads kept of {len(so_main['questions'])}; {n} units")
    so_off = load("so_offcwe.json")
    if so_off:
        if not so_main:
            log("NOTE: so_main.json missing - offcwe pass cannot exclude main threads or add 'dropped' threads")
        seen: set[tuple[int, str]] = set()
        targeted = {q["question_id"] for q in so_off["questions"]} - set(kept)
        units = so_units(so_off, targeted, "offcwe", {}, "targeted", SO_MEM_OFF, SO_LEAK_OFF, seen)
        if so_main:
            dropped = {q["question_id"] for q in so_main["questions"]} - set(kept)
            units += so_units(so_main, dropped, "offcwe", {}, "dropped", SO_MEM_OFF, SO_LEAK_OFF, seen)
        log(f"offcwe_so: {write_jsonl(UNITS / 'offcwe_so.jsonl', units)} units")
    gh = load("gh_main.json")
    if gh:
        log(f"main_gh: {write_jsonl(UNITS / 'main_gh.jsonl', gh_main_units(gh))} units from {len(gh)} issues")
    gh = load("gh_offcwe.json")
    if gh:
        log(f"offcwe_gh: {write_jsonl(UNITS / 'offcwe_gh.jsonl', gh_offcwe_units(gh))} units from {len(gh)} issues")


if __name__ == "__main__":
    main()
