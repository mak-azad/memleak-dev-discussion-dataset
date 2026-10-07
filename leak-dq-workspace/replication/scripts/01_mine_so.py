"""Step 1 - mine Stack Overflow questions, answers and comments.

  python scripts/01_mine_so.py --pass main            # rerun the searches in config/queries.json
  python scripts/01_mine_so.py --pass main --snapshot # refetch the exact question IDs of the Oct-2026 run
  python scripts/01_mine_so.py --pass offcwe [--snapshot]

Output: data/raw/so_<pass>.json  {"questions": [...], "answers": [...], "comments": [...]}
Each question carries `query_buckets` (CWE ids for main, theme ids for offcwe).

Search results drift over time (new posts, vote changes, deletions); use --snapshot
for a faithful replication and plain search to extend the corpus.
"""
from __future__ import annotations

import argparse
import json
from typing import Any

from common import RAW, SNAPSHOT, chunks, load_config, log, se_get, se_paged

FILTER = "withbody"


def search(pass_: str) -> dict[int, dict[str, Any]]:
    cfg = load_config()[f"so_{pass_}"]
    qs: dict[int, dict[str, Any]] = {}
    for bucket, lst in cfg["queries"].items():
        for q, tag in lst:
            for sort in cfg["sorts"]:
                d = se_get("/search/advanced", q=q, tagged=tag, sort=sort, order="desc",
                           pagesize=str(cfg["pagesize"]), filter=FILTER)
                for it in d.get("items", []):
                    e = qs.setdefault(it["question_id"], {**it, "query_buckets": []})
                    if bucket not in e["query_buckets"]:
                        e["query_buckets"].append(bucket)
                log(f"{bucket:22} {q!r:45} {tag:4} {sort:9} -> {len(d.get('items', []))} (quota {d.get('quota_remaining')})")
    return qs


def from_snapshot(pass_: str) -> dict[int, dict[str, Any]]:
    snap = json.loads((SNAPSHOT / "so_question_ids.json").read_text())[pass_]
    buckets = {s["question_id"]: s.get("query_cwes") or s.get("search_themes") or [] for s in snap}
    qs: dict[int, dict[str, Any]] = {}
    for ch in chunks(list(buckets), 100):
        for it in se_paged(f"/questions/{';'.join(map(str, ch))}", filter=FILTER):
            qs[it["question_id"]] = {**it, "query_buckets": buckets[it["question_id"]]}
    missing = set(buckets) - set(qs)
    if missing:
        log(f"{len(missing)} snapshot questions no longer available (deleted/closed): {sorted(missing)[:10]}...")
    return qs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pass", dest="pass_", choices=["main", "offcwe"], required=True)
    ap.add_argument("--snapshot", action="store_true")
    a = ap.parse_args()
    qs = from_snapshot(a.pass_) if a.snapshot else search(a.pass_)
    ids = list(qs)
    answers: list[dict[str, Any]] = []
    comments: list[dict[str, Any]] = []
    for ch in chunks(ids, 80):
        s = ";".join(map(str, ch))
        answers += se_paged(f"/questions/{s}/answers", filter=FILTER, sort="votes", order="desc")
        comments += se_paged(f"/questions/{s}/comments", filter=FILTER)
    for ch in chunks([a_["answer_id"] for a_ in answers], 80):
        comments += se_paged(f"/answers/{';'.join(map(str, ch))}/comments", filter=FILTER)
    out = RAW / f"so_{a.pass_}.json"
    out.write_text(json.dumps({"questions": list(qs.values()), "answers": answers, "comments": comments}))
    log(f"wrote {out}: {len(qs)} questions, {len(answers)} answers, {len(comments)} comments")


if __name__ == "__main__":
    main()
