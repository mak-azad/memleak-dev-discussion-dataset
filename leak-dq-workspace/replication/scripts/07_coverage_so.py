"""Step 7 - Stack Overflow coverage report: cached 2026-10-05 data versus a fresh re-query.

  python scripts/07_coverage_so.py

Input (data/raw/):
  so_<pass>_cached.json   copy of the 2026-10-05 collection (never overwritten)
  so_<pass>.json          fresh refetch from `01_mine_so.py --pass <pass> --snapshot`

Output (workspace root):
  coverage_so.csv         one row per snapshot question
  coverage_so_summary.md  counts per pass and status, with the fetch date

Status values, first match wins:
  missing     question absent from the fresh fetch (deleted, closed, or inaccessible)
  edited      question body, or the body of a post present in both fetches, changed
  new_posts   the fresh fetch holds answers or comments that the cached fetch lacks
  ok          nothing changed
Off-CWE rows with `new_posts` are the threads that the truncated 2026-10-05 batches cut.
"""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import RAW, ROOT

OUT_DIR = ROOT.parent
FIELDS = ["pass", "question_id", "status", "body_sha1_cached", "body_sha1_fresh", "answers_cached",
          "answers_fresh", "comments_cached", "comments_fresh", "edited_posts", "new_answers", "new_comments",
          "fetched_utc"]


def sha1(text: str) -> str:
    """Return the first 12 hex characters of the SHA-1 of text."""
    return hashlib.sha1((text or "").encode()).hexdigest()[:12]


def load(path: Path) -> dict[str, Any]:
    """Read one raw cache file."""
    return json.loads(path.read_text())


def index(D: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Group answers and comments by question id."""
    ans_q = {a["answer_id"]: a["question_id"] for a in D["answers"]}
    out: dict[int, dict[str, Any]] = {q["question_id"]: {"q": q, "answers": {}, "comments": {}} for q in D["questions"]}
    for a in D["answers"]:
        if a["question_id"] in out:
            out[a["question_id"]]["answers"][a["answer_id"]] = a
    for c in D["comments"]:
        qid = c["post_id"] if c["post_id"] in out else ans_q.get(c["post_id"])
        if qid in out:
            out[qid]["comments"][c["comment_id"]] = c
    return out


def compare(pass_: str, fetched: str) -> list[dict[str, Any]]:
    """Return one coverage row per cached question."""
    old = index(load(RAW / f"so_{pass_}_cached.json"))
    new = index(load(RAW / f"so_{pass_}.json"))
    rows = []
    for qid, o in old.items():
        n = new.get(qid)
        row: dict[str, Any] = {"pass": pass_, "question_id": qid, "body_sha1_cached": sha1(o["q"].get("body", "")),
                               "answers_cached": len(o["answers"]), "comments_cached": len(o["comments"]),
                               "fetched_utc": fetched}
        if n is None:
            rows.append({**row, "status": "missing", "body_sha1_fresh": "", "answers_fresh": "", "comments_fresh": "",
                         "edited_posts": "", "new_answers": "", "new_comments": ""})
            continue
        edited = int(sha1(n["q"].get("body", "")) != row["body_sha1_cached"])
        edited += sum(sha1(n["answers"][i].get("body", "")) != sha1(a.get("body", ""))
                      for i, a in o["answers"].items() if i in n["answers"])
        edited += sum(sha1(n["comments"][i].get("body", "")) != sha1(c.get("body", ""))
                      for i, c in o["comments"].items() if i in n["comments"])
        new_a, new_c = set(n["answers"]) - set(o["answers"]), set(n["comments"]) - set(o["comments"])
        status = "edited" if edited else "new_posts" if (new_a or new_c) else "ok"
        rows.append({**row, "status": status, "body_sha1_fresh": sha1(n["q"].get("body", "")),
                     "answers_fresh": len(n["answers"]), "comments_fresh": len(n["comments"]),
                     "edited_posts": edited, "new_answers": len(new_a), "new_comments": len(new_c)})
    return rows


def main() -> None:
    """Write coverage_so.csv and coverage_so_summary.md."""
    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    rows: list[dict[str, Any]] = []
    for p in ("main", "offcwe"):
        rows += compare(p, fetched)
    with (OUT_DIR / "coverage_so.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    cnt: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    tot: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in rows:
        cnt[r["pass"]][r["status"]] += 1
        for k in ("answers_cached", "answers_fresh", "comments_cached", "comments_fresh", "new_answers", "new_comments"):
            tot[r["pass"]][k] += int(r[k] or 0)
    lines = ["# Stack Overflow coverage: 2026-10-05 cache versus fresh re-query", "",
             f"Fresh re-query run: {fetched} (UTC). Cached collection: 2026-10-05.", "",
             "| Pass | Questions | ok | edited | new_posts | missing |", "| --- | --- | --- | --- | --- | --- |"]
    for p in ("main", "offcwe"):
        c = cnt[p]
        lines.append(f"| {p} | {sum(c.values())} | {c['ok']} | {c['edited']} | {c['new_posts']} | {c['missing']} |")
    lines += ["", "| Pass | Answers cached | Answers fresh | Comments cached | Comments fresh |",
              "| --- | --- | --- | --- | --- |"]
    for p in ("main", "offcwe"):
        t = tot[p]
        lines.append(f"| {p} | {t['answers_cached']} | {t['answers_fresh']} | {t['comments_cached']} | {t['comments_fresh']} |")
    lines += ["", "Rows with status `missing` have no fresh data. Their cached text stays the source for the export.",
              "Off-CWE `new_posts` rows are expected: the cached off-CWE batches stopped at 100 answers and 100 comments."]
    (OUT_DIR / "coverage_so_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
