"""Step 9 - map every coded item in outputs/*.csv to its source post, unit key, and verbatim sentence.

  python scripts/09_item_source_map.py [--strict]

Output (workspace root): item_source_map.csv, one row per (item, code), the grain of the shared CSVs.

How the shared CSVs link to the hand codes (verified here, not assumed):
  outputs/diagnostic_questions_coded.csv    item_id `so:N` / `gh:N`: N is the 0-based row of codes/main_so.csv
                                            or codes/main_gh.csv. NA rows are absent from the CSV, so ids skip them.
  outputs/diagnostic_questions_offcwe_coded.csv   no item_id. Rows come in the order of codes/offcwe_{so,gh}.csv,
                                            one row per code. We walk both lists in step and check each row.
Each linked row must agree on source, post permalink, role, and the set of codes. GitHub roles map
R -> asker and M, O -> responder; the main file's `maintainer` flag must equal (role == M). `--strict` exits
with status 1 on any mismatch. Without it the script reports the mismatches and writes the rows it could verify.

Verbatim sentences come from data/units/*.jsonl (step 3). GitHub sentences stay empty until the
GitHub re-fetch (step 2) and step 3 have run. `text_status` is `verbatim`, `unavailable_until_gh_refetch`
(GitHub units not extracted yet), or `unit_not_found` (the code has no matching unit in the re-extraction: an orphan).
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import OrderedDict
from pathlib import Path
from typing import Any

from common import CODES, ROOT, UNITS, log, read_jsonl

WS = ROOT.parent
OUT_COLS = ["item_id", "source", "pass", "unit_key", "post_type", "post_id", "permalink", "thread_url", "role", "form",
            "gh_role", "dq_code", "dq_dimension", "verbatim_sentence", "text_status"]


def read_csv(p: Path) -> list[dict[str, str]]:
    """Read a CSV file into dict rows."""
    with p.open(newline="") as f:
        return list(csv.DictReader(f))


def codeset(s: str) -> set[str]:
    """Split a comma-separated code string into a set."""
    return {c.strip() for c in s.split(",") if c.strip()}


def shared_role(source: str, role: str) -> str:
    """Translate a hand-code role to the shared-CSV role. GitHub: R is asker, M and O are responder."""
    if source == "GitHub":
        return "asker" if role == "R" else "responder"
    return role


def non_na(rows: list[dict[str, str]]) -> list[tuple[int, dict[str, str]]]:
    """Return (original row index, row) for rows with at least one non-NA code."""
    return [(i, r) for i, r in enumerate(rows) if codeset(r["codes"]) - {"NA"}]


def so_post(permalink: str, kind: str | None) -> tuple[str, str]:
    """Return (post_type, post_id) from a Stack Overflow permalink."""
    if m := re.search(r"/a/(\d+)", permalink):
        return "answer", m.group(1)
    if m := re.search(r"#comment(\d+)_", permalink):
        return "comment", m.group(1)
    q = re.search(r"/questions/(\d+)", permalink)
    return (kind or "question"), (q.group(1) if q else "")


def gh_post(comment_id: str) -> tuple[str, str]:
    """Return (post_type, post_id) for a GitHub comment id; `-` is the issue title or body."""
    return ("issue_title_or_body", "-") if comment_id == "-" else ("comment", comment_id)


def group_items(rows: list[dict[str, str]]) -> "OrderedDict[str, list[dict[str, str]]]":
    """Group main-file rows by item_id, keeping file order."""
    g: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for r in rows:
        g.setdefault(r["item_id"], []).append(r)
    return g


def link_main(prefix: str, source_name: str, shared: "OrderedDict[str, list[dict[str, str]]]", codes: list[dict[str, str]],
              units: dict[str, dict[str, Any]], bad: list[str]) -> list[dict[str, Any]]:
    """Link `so:N` or `gh:N` items of the main file to codes rows by index and verify."""
    out = []
    for item_id, rs in shared.items():
        if not item_id.startswith(prefix + ":"):
            continue
        n = int(item_id.split(":")[1])
        c = codes[n] if n < len(codes) else None
        first = rs[0]
        if (c is None or c.get("post_permalink", c.get("issue_url")) is None
                or codeset(c["codes"]) != {r["dq_code"] for r in rs}
                or shared_role(source_name, c["role"]) != first["role"]
                or (prefix == "gh" and (c["role"] == "M") != (first["maintainer"] == "True"))):
            bad.append(f"{item_id}: codes/role differ from row {n}")
            continue
        if prefix == "so" and c["post_permalink"] != first["post_permalink"]:
            bad.append(f"{item_id}: permalink differs from row {n}")
            continue
        if prefix == "gh":
            pl = c["issue_url"] + (f"#issuecomment-{c['comment_id']}" if c["comment_id"] != "-" else "")
            if pl != first["post_permalink"]:
                bad.append(f"{item_id}: permalink differs from row {n}")
                continue
        out += rows_for(item_id, source_name, "main", c, rs, units)
    return out


def rows_for(item_id: str, source: str, pass_: str, c: dict[str, str], rs: list[dict[str, str]],
             units: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    """Build the output rows of one linked item (one per code)."""
    u = units.get(c["unit_key"])
    if source == "Stack Overflow":
        ptype, pid = so_post(rs[0]["post_permalink"], (u or {}).get("post_kind"))
        if u and u.get("post_kind") == "title":
            ptype = "title"
    else:
        ptype, pid = gh_post(c["comment_id"])
    text = (u or {}).get("text", "")
    gh_loaded = any(k.startswith("https://github.com/") for k in units)
    status = "verbatim" if text else "unavailable_until_gh_refetch" if (source == "GitHub" and not gh_loaded) else "unit_not_found"
    return [{"item_id": item_id, "source": source, "pass": pass_, "unit_key": c["unit_key"], "post_type": ptype,
             "post_id": pid, "permalink": r["post_permalink"], "thread_url": r["thread_url"], "role": r["role"],
             "form": r["form"], "gh_role": c["role"] if source == "GitHub" else "", "dq_code": r["dq_code"], "dq_dimension": r["dq_dimension"],
             "verbatim_sentence": text, "text_status": status} for r in rs]


def link_offcwe(source_name: str, shared: list[dict[str, str]], codes: list[dict[str, str]],
                units: dict[str, dict[str, Any]], bad: list[str]) -> list[dict[str, Any]]:
    """Walk the off-CWE shared rows and the non-NA code rows in step, one unit at a time."""
    out = []
    pos = 0
    tag = "offcwe_so" if source_name == "Stack Overflow" else "offcwe_gh"
    for idx, c in non_na(codes):
        want = codeset(c["codes"]) - {"NA"}
        rs = shared[pos:pos + len(want)]
        pl = c.get("post_permalink") or (c["issue_url"] + (f"#issuecomment-{c['comment_id']}" if c["comment_id"] != "-" else ""))
        if (len(rs) != len(want) or {r["dq_code"] for r in rs} != want
                or any(r["post_permalink"] != pl or r["role"] != shared_role(source_name, c["role"]) for r in rs)):
            bad.append(f"{tag}:{idx}: shared rows at offset {pos} do not match")
            return out  # the walk is out of step; stop rather than guess
        pos += len(want)
        out += rows_for(f"{tag}:{idx}", source_name, "offcwe", c, rs, units)
    if pos != len(shared):
        bad.append(f"{tag}: {len(shared) - pos} shared rows left over after the walk")
    return out


def main() -> None:
    """Build and write item_source_map.csv."""
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    main_csv = read_csv(WS / "outputs" / "diagnostic_questions_coded.csv")
    off_csv = read_csv(WS / "outputs" / "diagnostic_questions_offcwe_coded.csv")
    units: dict[str, dict[str, Any]] = {}
    for name in ("main_so", "main_gh", "offcwe_so", "offcwe_gh"):
        p = UNITS / f"{name}.jsonl"
        if p.exists():
            units.update({u["unit_key"]: u for u in read_jsonl(p)})
        else:
            log(f"note: {p.name} missing; sentences for that file stay empty")
    bad: list[str] = []
    shared = group_items(main_csv)
    out: list[dict[str, Any]] = []
    out += link_main("so", "Stack Overflow", shared, read_csv(CODES / "main_so.csv"), units, bad)
    out += link_main("gh", "GitHub", shared, read_csv(CODES / "main_gh.csv"), units, bad)
    for src, name in (("Stack Overflow", "offcwe_so"), ("GitHub", "offcwe_gh")):
        out += link_offcwe(src, [r for r in off_csv if r["source"] == src], read_csv(CODES / f"{name}.csv"), units, bad)
    for b in bad[:20]:
        log("MISMATCH", b)
    n_in = len(main_csv) + len(off_csv)
    log(f"shared rows {n_in}; mapped rows {len(out)}; mismatches {len(bad)}")
    with (WS / "item_source_map.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLS)
        w.writeheader()
        w.writerows(out)
    if a.strict and (bad or len(out) != n_in):
        sys.exit(1)


if __name__ == "__main__":
    main()
