"""Step 6 - inter-rater reliability.

  # 0) steps 1-4 first, so data/coded/*.csv carries the sentence text of every unit
  # 1) draw a stratified blind sample for a second labeller (first-coder codes hidden)
  python scripts/06_second_coder.py sample --n 200 --seed 7 --out ../validation/second_coder_sample.csv
  # 2) the second labeller fills `codes` using docs/CODEBOOK.md (comma-separated ids; NA for non-diagnostic)
  # 3) compare
  python scripts/06_second_coder.py kappa ../validation/second_coder_sample.csv

Sampling: strata are (source, dimension of the first code), with NA as its own dimension, so the
sample also checks the NA decisions. The quota is n // number-of-strata per stratum, capped by the
stratum size. Any quota left over goes to strata with unused units, one unit at a time in a fixed
order. The sample has exactly n units. Units without text are refused: run steps 1-4 first.

Kappa is Cohen's kappa on presence/absence, per DQ code and per evidence dimension (multi-label).
Units that neither coder gave a code count as agreement on every code. The output gives a bootstrap
95% interval (1,000 resamples of units, seed 7) with each kappa, a row for NA versus diagnostic, and
unit-level exact agreement (same code set) with a Wilson 95% interval.
"""
from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from typing import Iterable

from common import CODED, CODES
from dq.codebook import DQ_LABELS

FILES = ("main_so", "main_gh", "offcwe_so", "offcwe_gh")
SOURCE = {"so": "Stack Overflow", "gh": "GitHub"}


def cohen_kappa(a: list[int], b: list[int]) -> float:
    """Cohen's kappa for two binary label vectors. Returns 1.0 when chance agreement is 1."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def bootstrap_ci(a: list[int], b: list[int], reps: int = 1000, seed: int = 7) -> tuple[float, float]:
    """Percentile 95% bootstrap interval of kappa, resampling units."""
    rnd = random.Random(seed)
    n = len(a)
    ks = []
    for _ in range(reps):
        idx = [rnd.randrange(n) for _ in range(n)]
        ks.append(cohen_kappa([a[i] for i in idx], [b[i] for i in idx]))
    ks.sort()
    return ks[int(0.025 * reps)], ks[int(0.975 * reps) - 1]


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion k/n."""
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def first_codes() -> dict[str, dict[str, str]]:
    """Map unit_key to the first coder's codes and the unit's context. Needs data/coded/*.csv for text."""
    out: dict[str, dict[str, str]] = {}
    for name in FILES:
        p = CODED / f"{name}.csv"
        src = SOURCE[name.split("_")[1]]
        if p.exists():
            for r in csv.DictReader(p.open()):
                out[r["unit_key"]] = {"codes": r["codes"], "text": r["text"], "source": src, "role": r["role"],
                                      "form": r["form"], "post_permalink": r["post_permalink"]}
        else:  # text unavailable without steps 1-4
            for r in csv.DictReader((CODES / f"{name}.csv").open()):
                out.setdefault(r["unit_key"], {"codes": r["codes"], "text": "", "source": src, "role": r["role"],
                                               "form": r.get("form", ""), "post_permalink": ""})
    return out


def dimension(codes: str) -> str:
    """Evidence dimension of the first code; NA for non-diagnostic units."""
    return DQ_LABELS.get(codes.split(",")[0].strip(), ("NA",))[0]


def allocate(sizes: dict[tuple[str, str], int], n: int) -> dict[tuple[str, str], int]:
    """Equal quota per stratum, capped by stratum size, leftover handed out one unit at a time."""
    quota = {s: min(sz, n // len(sizes)) for s, sz in sizes.items()}
    order = sorted(sizes)
    while sum(quota.values()) < n:
        grew = False
        for s in order:
            if quota[s] < sizes[s] and sum(quota.values()) < n:
                quota[s] += 1
                grew = True
        if not grew:
            break
    return quota


def sample(n: int, seed: int, out: str | None) -> None:
    """Write a blind stratified sample of exactly n units."""
    fc = first_codes()
    empty = [k for k, v in fc.items() if not v["text"]]
    if empty:
        sys.exit(f"{len(empty)} units have no text (e.g. {empty[0]}). Run steps 1-4 first, so data/coded/*.csv has the sentences.")
    strata: dict[tuple[str, str], list[str]] = defaultdict(list)
    for k, v in fc.items():
        strata[(v["source"], dimension(v["codes"]))].append(k)
    if sum(map(len, strata.values())) < n:
        sys.exit("fewer units than the requested sample size")
    rnd = random.Random(seed)
    quota = allocate({s: len(ks) for s, ks in strata.items()}, n)
    keys: list[str] = []
    for s in sorted(strata):
        keys += rnd.sample(sorted(strata[s]), quota[s])
    rnd.shuffle(keys)
    f = open(out, "w", newline="") if out else sys.stdout
    w = csv.writer(f)
    w.writerow(["unit_key", "source", "role", "form", "post_permalink", "text", "codes"])
    for k in keys:
        v = fc[k]
        w.writerow([k, v["source"], v["role"], v["form"], v["post_permalink"], v["text"], ""])
    if out:
        f.close()
    print(f"sample: {len(keys)} units in {len(strata)} strata (seed {seed})", file=sys.stderr)
    for s in sorted(strata):
        print(f"  {s[0]:15} {s[1]:26} population {len(strata[s]):4} sampled {quota[s]}", file=sys.stderr)


def report(rows: Iterable[tuple[str, list[int], list[int]]]) -> None:
    """Print kappa with a bootstrap interval for each (label, first-coder vector, second-coder vector)."""
    for name, a, b in rows:
        if sum(a) + sum(b):
            lo, hi = bootstrap_ci(a, b)
            print(f"{name:26} {cohen_kappa(a, b):6.2f}  [{lo:5.2f}, {hi:5.2f}] {sum(a):8} {sum(b):9}")


def kappa(path: str) -> None:
    """Compare the second coder's sheet with the first coder's codes."""
    fc = first_codes()
    rows = [r for r in csv.DictReader(open(path)) if r["codes"].strip() and r["unit_key"] in fc]
    blank = sum(1 for r in csv.DictReader(open(path)) if not r["codes"].strip())
    a_sets = [{c.strip() for c in fc[r["unit_key"]]["codes"].split(",") if c.strip()} for r in rows]
    b_sets = [{c.strip() for c in r["codes"].split(",") if c.strip()} for r in rows]
    unknown = {c for s in b_sets for c in s} - set(DQ_LABELS) - {"NA"}
    print(f"units compared: {len(rows)}   units left blank by the second coder (not compared): {blank}")
    if unknown:
        print(f"WARNING: codes not in the codebook: {sorted(unknown)}")
    agree = sum(x == y for x, y in zip(a_sets, b_sets))
    lo, hi = wilson(agree, len(rows))
    print(f"exact agreement (same code set): {agree}/{len(rows)} = {agree / len(rows):.2f}  Wilson 95% [{lo:.2f}, {hi:.2f}]\n")
    print(f"{'code':26} {'kappa':>6}  {'95% bootstrap':14} {'n_first':>8} {'n_second':>9}")
    report([(c, [int(c in s) for s in a_sets], [int(c in s) for s in b_sets]) for c in DQ_LABELS])
    print("\ndimension")
    dims = sorted({v[0] for v in DQ_LABELS.values()})
    report([(d, [int(bool({k for k, v in DQ_LABELS.items() if v[0] == d} & s)) for s in a_sets],
             [int(bool({k for k, v in DQ_LABELS.items() if v[0] == d} & s)) for s in b_sets]) for d in dims])
    print("\nNA (non-diagnostic) versus diagnostic")
    report([("NA", [int("NA" in s or not s) for s in a_sets], [int("NA" in s or not s) for s in b_sets])])


def main() -> None:
    """Parse arguments and run the chosen command."""
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("sample")
    s.add_argument("--n", type=int, default=200)
    s.add_argument("--seed", type=int, default=7)
    s.add_argument("--out", default=None, help="CSV path; default is stdout")
    k = sp.add_parser("kappa")
    k.add_argument("path")
    a = ap.parse_args()
    sample(a.n, a.seed, a.out) if a.cmd == "sample" else kappa(a.path)


if __name__ == "__main__":
    main()
