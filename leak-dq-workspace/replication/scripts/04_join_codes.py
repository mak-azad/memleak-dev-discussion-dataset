"""Step 4 - join extracted units with the hand codes.

  python scripts/04_join_codes.py

For each <pass>_<source> it reports:
  matched    units that already have a hand code (codes/<pass>_<source>.csv)
  new        units with no code -> data/to_code/<pass>_<source>.csv (text included, ready to label)
  orphaned   codes whose unit no longer exists (post edited/deleted, thread changed)

Coding new units: fill the `codes` column (comma-separated DQ ids from dq/codebook.py;
NA for non-diagnostic) and, for offcwe files, `theme`. Then append the rows to
codes/<pass>_<source>.csv (the analysis only needs the columns already there).
"""
from __future__ import annotations

import csv

from common import CODED, CODES, TO_CODE, UNITS, log, read_jsonl


def main() -> None:
    for name in ("main_so", "main_gh", "offcwe_so", "offcwe_gh"):
        up, cp = UNITS / f"{name}.jsonl", CODES / f"{name}.csv"
        if not up.exists():
            log(f"{name}: no units (run steps 1-3)")
            continue
        units = read_jsonl(up)
        codes = {r["unit_key"]: r for r in csv.DictReader(cp.open())}
        matched = [u for u in units if u["unit_key"] in codes]
        new = [u for u in units if u["unit_key"] not in codes]
        orphan = set(codes) - {u["unit_key"] for u in units}
        with (CODED / f"{name}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["unit_key", "thread_url", "post_permalink", "role", "form", "theme", "codes", "text"])
            for u in matched:
                c = codes[u["unit_key"]]
                w.writerow([u["unit_key"], u["thread_url"], u["post_permalink"], u["role"], u["form"],
                            c.get("theme", ""), c["codes"], u["text"]])
        with (TO_CODE / f"{name}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["unit_key", "thread_url", "post_permalink", "role", "form", "theme", "codes", "text"])
            for u in new:
                w.writerow([u["unit_key"], u["thread_url"], u["post_permalink"], u["role"], u["form"], "", "", u["text"]])
        rate = 100 * len(matched) / max(1, len(units))
        log(f"{name}: {len(units)} units | matched {len(matched)} ({rate:.1f}%) | new {len(new)} | orphaned codes {len(orphan)}")


if __name__ == "__main__":
    main()
