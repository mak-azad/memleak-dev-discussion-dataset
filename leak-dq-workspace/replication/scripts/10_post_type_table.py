"""Step 10 - tabulate Stack Overflow units by post type and role.

  python scripts/10_post_type_table.py

Input:  data/units/main_so.jsonl, data/units/offcwe_so.jsonl (field `post_kind`: title, question, answer, comment)
        codes/main_so.csv, codes/offcwe_so.csv (to separate NA units from coded units)
Output: results/so_units_by_post_type.csv

A unit is "coded" when it has at least one code other than NA. The unit list comes from the
re-extraction, so new off-CWE units without a code are labelled `uncoded_new` and kept out of both
other groups. Counts only: the table makes no inference, so it has no confidence interval.
"""
from __future__ import annotations

import csv
from collections import Counter

from common import CODES, RESULTS, UNITS, log, read_jsonl

KINDS = ("title", "question", "answer", "comment")
ROLES = ("asker", "responder")


def status(codes: dict[str, str], key: str) -> str:
    """Return coded, NA, or uncoded_new for one unit key."""
    if key not in codes:
        return "uncoded_new"
    return "coded" if any(c.strip() and c.strip() != "NA" for c in codes[key].split(",")) else "NA"


def main() -> None:
    """Write the post-type table."""
    rows: list[list[str | int]] = []
    for pass_ in ("main", "offcwe"):
        units = read_jsonl(UNITS / f"{pass_}_so.jsonl")
        codes = {r["unit_key"]: r["codes"] for r in csv.DictReader((CODES / f"{pass_}_so.csv").open())}
        c: Counter[tuple[str, str, str]] = Counter((status(codes, u["unit_key"]), u["post_kind"], u["role"]) for u in units)
        for st in ("coded", "NA", "uncoded_new"):
            tot = sum(v for (s, _, _), v in c.items() if s == st)
            for kind in KINDS:
                for role in ROLES:
                    n = c[(st, kind, role)]
                    rows.append([pass_, st, kind, role, n, tot, f"{100 * n / tot:.1f}" if tot else ""])
            log(f"{pass_:7} {st:12} total {tot}")
    with (RESULTS / "so_units_by_post_type.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pass", "unit_status", "post_kind", "role", "units", "units_in_status", "percent_of_status"])
        w.writerows(rows)


if __name__ == "__main__":
    main()
