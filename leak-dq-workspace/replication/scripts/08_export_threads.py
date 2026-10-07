"""Step 8 - export full threads as JSON plus readable Markdown.

  python scripts/08_export_threads.py --source so
  python scripts/08_export_threads.py --source gh     # needs data/raw/gh_main.json and gh_offcwe.json (step 2)

Output (workspace root): threads/so/<question_id>.json and .md
                         threads/gh/<owner>__<repo>__<number>.json and .md, coverage_gh.csv, coverage_gh_summary.md

Stack Overflow data source per thread:
  - threads in so_main_cached.json: the 2026-10-05 collection (the data the coded units came from).
    The fresh re-query had identical counts and bodies (see coverage_so_summary.md).
  - threads only in the off-CWE pass: so_offcwe.json, the refetch with full paging.
  A question in both passes is exported once, from the main data, and lists both passes.

Each JSON file holds the question (HTML body, code blocks intact) and a flat chronological `events`
list of answers and comments. Roles, permalinks, and the asker/responder rule match
03_extract_units.py (`so_posts`): role is "asker" if the author's user_id equals the question owner's.
When an author has no user_id (deleted account), that rule marks the post "asker" when the owner
has none either. `author_id_missing` flags those posts. Do not read the role of such posts as reliable.
"""
from __future__ import annotations

import argparse
import csv
import html
import importlib
import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any

from common import CODES, RAW, ROOT

OUT = ROOT.parent / "threads"
QID_RX = re.compile(r"/questions/(\d+)")


def iso(ts: int | None) -> str | None:
    """Convert a Unix timestamp to an ISO 8601 UTC string."""
    return None if ts is None else datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class _Md(HTMLParser):
    """Small HTML-to-Markdown converter. Keeps <pre><code> blocks as fenced code."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.in_pre = False
        self.list_stack: list[str] = []
        self.href: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        if tag == "pre":
            self.in_pre = True
            self.out.append("\n\n```\n")
        elif tag == "code" and not self.in_pre:
            self.out.append("`")
        elif tag in ("p", "div", "blockquote"):
            self.out.append("\n\n> " if tag == "blockquote" else "\n\n")
        elif tag == "br":
            self.out.append("  \n")
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
            self.out.append("\n")
        elif tag == "li":
            self.out.append("\n- " if not self.list_stack or self.list_stack[-1] == "ul" else "\n1. ")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a":
            self.href.append(a.get("href"))
            self.out.append("[")
        elif tag == "img":
            self.out.append(f"![{a.get('alt') or ''}]({a.get('src') or ''})")
        elif re.fullmatch(r"h[1-6]", tag):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "hr":
            self.out.append("\n\n---\n\n")

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre":
            self.in_pre = False
            self.out.append("\n```\n\n")
        elif tag == "code" and not self.in_pre:
            self.out.append("`")
        elif tag in ("ul", "ol") and self.list_stack:
            self.list_stack.pop()
            self.out.append("\n")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("*")
        elif tag == "a":
            h = self.href.pop() if self.href else None
            self.out.append(f"]({h})" if h else "]")
        elif tag in ("p", "div", "blockquote") or re.fullmatch(r"h[1-6]", tag):
            self.out.append("\n\n")

    def handle_data(self, data: str) -> None:
        self.out.append(data)


def html_to_md(h: str) -> str:
    """Convert a Stack Overflow HTML body to Markdown, keeping code blocks verbatim."""
    p = _Md()
    p.feed(h or "")
    p.close()
    return re.sub(r"\n{3,}", "\n\n", "".join(p.out)).strip()


# ------------------------------------------------------------------ Stack Overflow
def coded_thread_ids() -> tuple[set[int], set[int]]:
    """Return (main-pass threads with >=1 non-NA code, off-CWE threads with >=1 non-NA code)."""
    out: list[set[int]] = []
    for name in ("main_so", "offcwe_so"):
        ids: set[int] = set()
        for r in csv.DictReader((CODES / f"{name}.csv").open()):
            if any(c.strip() and c.strip() != "NA" for c in r["codes"].split(",")):
                m = QID_RX.search(r["thread_url"])
                if m:
                    ids.add(int(m.group(1)))
        out.append(ids)
    return out[0], out[1]


def author(o: dict[str, Any] | None) -> dict[str, Any]:
    """Return the author fields of a post owner."""
    o = o or {}
    return {"author_user_id": o.get("user_id"), "author_display_name": html.unescape(o.get("display_name") or ""),
            "author_id_missing": o.get("user_id") is None}


def build_so_thread(D: dict[str, Any], q: dict[str, Any], flags: dict[str, Any]) -> dict[str, Any]:
    """Build the JSON structure of one Stack Overflow thread."""
    qid = q["question_id"]
    owner_id = (q.get("owner") or {}).get("user_id")
    ans = [a for a in D["answers"] if a["question_id"] == qid]
    ans_ids = {a["answer_id"] for a in ans}
    events: list[dict[str, Any]] = []
    for a in ans:
        events.append({"post_type": "answer", "post_id": a["answer_id"], "parent_id": qid,
                       **author(a.get("owner")), "role": "asker" if (a.get("owner") or {}).get("user_id") == owner_id else "responder",
                       "is_accepted": bool(a.get("is_accepted")), "permalink": f"https://stackoverflow.com/a/{a['answer_id']}",
                       "score": a.get("score"), "created_utc": iso(a.get("creation_date")), "_ts": a["creation_date"],
                       "last_edit_utc": iso(a.get("last_edit_date")), "last_activity_utc": iso(a.get("last_activity_date")),
                       "license": a.get("content_license"), "body_html": a.get("body", "")})
    for c in D["comments"]:
        if c["post_id"] == qid or c["post_id"] in ans_ids:
            events.append({"post_type": "comment", "post_id": c["comment_id"], "parent_id": c["post_id"],
                           "parent_type": "question" if c["post_id"] == qid else "answer",
                           **author(c.get("owner")), "role": "asker" if (c.get("owner") or {}).get("user_id") == owner_id else "responder",
                           "is_accepted": None, "permalink": f"https://stackoverflow.com/questions/{qid}/#comment{c['comment_id']}_{c['post_id']}",
                           "score": c.get("score"), "created_utc": iso(c.get("creation_date")), "_ts": c["creation_date"],
                           "edited": c.get("edited"), "license": c.get("content_license"), "body_html": c.get("body", "")})
    events.sort(key=lambda e: (e["_ts"], e["post_type"] != "answer", e["post_id"]))
    for e in events:
        del e["_ts"]
    return {"source": "Stack Overflow", "question_id": qid, "url": q["link"], "title": html.unescape(q["title"]),
            "tags": q.get("tags", []), "score": q.get("score"), "view_count": q.get("view_count"),
            "answer_count": q.get("answer_count"), "is_answered": q.get("is_answered"),
            "accepted_answer_id": q.get("accepted_answer_id"), "created_utc": iso(q.get("creation_date")),
            "last_activity_utc": iso(q.get("last_activity_date")), "license": q.get("content_license"),
            **author(q.get("owner")), "permalink": q["link"], "body_html": q.get("body", ""),
            **flags, "events": events}


def so_md(t: dict[str, Any]) -> str:
    """Render one Stack Overflow thread as Markdown in chronological order."""
    L = [f"# {t['title']}", "",
         f"- URL: {t['url']}", f"- Tags: {', '.join(t['tags'])}", f"- Asked: {t['created_utc']} by {t['author_display_name'] or 'unknown'}",
         f"- Score: {t['score']}, answers: {t['answer_count']}, accepted answer id: {t['accepted_answer_id']}",
         f"- Passes: {', '.join(t['passes'])}; data source: {t['data_source']}", "", "## Question", "", html_to_md(t["body_html"]), ""]
    for e in t["events"]:
        kind = "Answer" if e["post_type"] == "answer" else f"Comment on {e['parent_type']} {e['parent_id']}"
        acc = " [ACCEPTED]" if e["is_accepted"] else ""
        L += [f"## {kind} {e['post_id']}{acc}", "",
              f"{e['role']} · {e['author_display_name'] or 'unknown'} · {e['created_utc']} · score {e['score']} · {e['permalink']}", "",
              html_to_md(e["body_html"]), ""]
    return "\n".join(L)


def export_so() -> None:
    """Export all Stack Overflow threads of both passes, one file per question id."""
    ext = importlib.import_module("03_extract_units")
    main_d = json.loads((RAW / "so_main_cached.json").read_text())
    off_d = json.loads((RAW / "so_offcwe.json").read_text())
    kept = set(ext.so_main_threads(main_d))
    main_coded, off_coded = coded_thread_ids()
    main_ids = {q["question_id"] for q in main_d["questions"]}
    off_ids = {q["question_id"] for q in off_d["questions"]}
    d = OUT / "so"
    d.mkdir(parents=True, exist_ok=True)
    n = 0
    for D, src, label in ((main_d, "so_main_cached (2026-10-05 collection)", "main"),
                          (off_d, "so_offcwe (refetch with full paging)", "offcwe")):
        for q in D["questions"]:
            qid = q["question_id"]
            if label == "offcwe" and qid in main_ids:
                continue
            passes = [p for p, s in (("main", main_ids), ("offcwe", off_ids)) if qid in s]
            flags = {"passes": passes, "data_source": src, "in_main_retained_480": qid in kept,
                     "in_main_nonNA_coded_346": qid in main_coded, "in_offcwe_nonNA_coded": qid in off_coded}
            t = build_so_thread(D, q, flags)
            (d / f"{qid}.json").write_text(json.dumps(t, ensure_ascii=False, indent=1))
            (d / f"{qid}.md").write_text(so_md(t))
            n += 1
    print(f"threads/so: {n} threads; main retained {len(kept)}; main non-NA coded {len(main_coded)}; "
          f"off-CWE non-NA coded {len(off_coded)}")


# ------------------------------------------------------------------ GitHub
GH_ROLE_NAME = {"R": "reporter", "M": "maintainer", "O": "other"}
CPP_LANGS = {"C", "C++", "Objective-C", "Objective-C++", "CUDA"}


def gh_event(cid: Any, kind: str, author_login: str | None, assoc: str | None, role: str, created: str | None,
             permalink: str, body: str, updated: str | None = None) -> dict[str, Any]:
    """Build one GitHub event (issue body or comment)."""
    return {"post_type": kind, "post_id": cid, "author_login": author_login, "author_association": assoc,
            "role": role, "role_name": GH_ROLE_NAME[role], "created_utc": created, "updated_utc": updated,
            "permalink": permalink, "body_markdown": body}


def build_gh_thread(iss: dict[str, Any], passes: list[str], ext: Any) -> dict[str, Any]:
    """Build the JSON structure of one GitHub thread. Role rule: gh_role from 03_extract_units.py."""
    url = iss["url"]
    events = [gh_event("-", "issue_body", iss["author"], iss["author_association"], "R", iss.get("created_at"), url,
                       iss["body"], iss.get("updated_at"))]
    for c in sorted(iss["comments"], key=lambda c: (c.get("created_at") or "", c["id"])):
        role = ext.gh_role(c["author"], iss["author"], c["author_association"])
        events.append(gh_event(c["id"], "comment", c["author"], c["author_association"], role, c.get("created_at"),
                               c.get("html_url") or f"{url}#issuecomment-{c['id']}", c["body"], c.get("updated_at")))
    keys = ("status", "fetched_utc", "final_url", "repo", "repo_language", "number", "state", "state_reason",
            "created_at", "updated_at", "closed_at", "labels", "comments_reported", "query_buckets")
    return {"source": "GitHub", "url": url, "passes": passes, "title": iss["title"], "author_login": iss["author"],
            **{k: iss.get(k) for k in keys}, "events": events}


def gh_md(t: dict[str, Any]) -> str:
    """Render one GitHub thread as Markdown in chronological order."""
    L = [f"# {t['title'] or '(unavailable)'}", "", f"- URL: {t['url']}", f"- Repo: {t['repo']} (language: {t['repo_language']})",
         f"- State: {t['state']}; created {t['created_at']}; status {t['status']}; passes {', '.join(t['passes'])}", ""]
    for e in t["events"]:
        L += [f"## {'Issue body' if e['post_type'] == 'issue_body' else 'Comment ' + str(e['post_id'])}", "",
              f"{e['role_name']} ({e['author_association']}) · {e['author_login'] or 'unknown'} · {e['created_utc']} · {e['permalink']}",
              "", e["body_markdown"], ""]
    return "\n".join(L)


def export_gh() -> None:
    """Export all GitHub threads and write coverage_gh.csv and coverage_gh_summary.md."""
    ext = importlib.import_module("03_extract_units")
    d = OUT / "gh"
    d.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    raw = {p: json.loads((RAW / f"gh_{p}.json").read_text()) for p in ("main", "offcwe")}
    passes_of: dict[str, list[str]] = {}
    for p, issues in raw.items():
        for iss in issues:
            passes_of.setdefault(iss["url"].lower(), []).append(p)
    written: set[str] = set()
    for pass_, issues in raw.items():
        for iss in issues:
            key = iss["url"].lower()
            if key not in written:  # an issue found by both passes is written once and lists both passes
                written.add(key)
                t = build_gh_thread(iss, passes_of[key], ext)
                name = f"{iss['repo'].replace('/', '__')}__{iss['number']}"
                (d / f"{name}.json").write_text(json.dumps(t, ensure_ascii=False, indent=1))
                (d / f"{name}.md").write_text(gh_md(t))
            lang = iss.get("repo_language")
            rows.append({"pass": pass_, "url": iss["url"], "status": iss["status"], "final_url": iss.get("final_url") or "",
                         "repo": iss["repo"], "repo_language": lang or "", "is_c_cpp_repo": "" if iss["status"] == "unavailable" else int(lang in CPP_LANGS),
                         "state": iss.get("state") or "", "created_at": iss.get("created_at") or "",
                         "comments_reported": iss.get("comments_reported") if iss.get("comments_reported") is not None else "",
                         "comments_fetched": len(iss["comments"]), "fetched_utc": iss["fetched_utc"]})
            rep = rows[-1]["comments_reported"]
            rows[-1]["comments_not_returned"] = max(0, rep - len(iss["comments"])) if rep != "" else ""
    with (OUT.parent / "coverage_gh.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    ok = [r for r in rows if r["status"] != "unavailable"]
    dates = sorted(r["created_at"] for r in ok if r["created_at"])
    lines = ["# GitHub coverage", "", f"Fetch run: {max(r['fetched_utc'] for r in rows)} (UTC).", "",
             "| Pass | Issues | ok | moved | unavailable | C/C++ repo | other language or none |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for p in ("main", "offcwe"):
        rs = [r for r in rows if r["pass"] == p]
        c = lambda s: sum(r["status"] == s for r in rs)  # noqa: E731
        cc = sum(r["is_c_cpp_repo"] == 1 for r in rs)
        lines.append(f"| {p} | {len(rs)} | {c('ok')} | {c('moved')} | {c('unavailable')} | {cc} | {len(rs) - c('unavailable') - cc} |")
    lines += ["", f"Issue creation dates, all fetched issues: {dates[0]} to {dates[-1]}." if dates else "No dates."]
    mism = [r for r in ok if r["comments_not_returned"] not in ("", 0)]
    lines.append(f"Issues where GitHub reports more comments than the REST comments endpoint returned: {len(mism)} "
                 f"({sum(r['comments_not_returned'] for r in mism)} comments in total). Repeating the request gives the same counts, "
                 "so the endpoint does not return those comments. Their text is not available to us.")
    lines.append(f"Unique issues: {len(written)}; an issue found by both passes is exported once.")
    (OUT.parent / "coverage_gh_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main() -> None:
    """Parse arguments and run the chosen export."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["so", "gh"], required=True)
    a = ap.parse_args()
    export_so() if a.source == "so" else export_gh()


if __name__ == "__main__":
    main()
