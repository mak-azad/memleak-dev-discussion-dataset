"""Step 5 - frequency tables behind the report. Runs offline from codes/*.csv.

  python scripts/05_analyze.py            # write results/*.csv and results/summary.md
  python scripts/05_analyze.py --check    # also compare headline numbers with results/expected.json

Definitions (match the report):
  * thread reach of a DQ = number of distinct threads with >=1 unit carrying that code
  * a thread is "diagnostic" if it has >=1 code outside NON_DIAGNOSTIC
  * roles: SO asker/responder; GitHub reporter (R) -> asker, maintainer (M) / other (O) -> responder
  * per-CWE shares use thread_cwe_signatures (regex, multi-label) and only diagnostic threads
  * role x dimension shares count occurrences; generic root-cause requests (G) are folded into
    "Report interpretation"; non-diagnostic codes are excluded from denominators
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from typing import Any

from common import CODES, RESULTS, log
from dq.codebook import DQ_LABELS, NON_DIAGNOSTIC, THEMES

CWES = ["CWE-401", "CWE-459", "CWE-590", "CWE-761", "CWE-762", "CWE-763", "CWE-789"]
DIMS = ["Report interpretation", "Lifetime", "Deallocation", "Allocation", "Control flow", "Ownership",
        "Composite cleanup", "Escape / aliasing", "Cross-module"]


def load_rows() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    main: list[dict[str, Any]] = []
    for r in csv.DictReader((CODES / "main_so.csv").open()):
        main.append({"src": "SO", "thread": r["thread_url"], "role": r["role"], "form": "question",
                     "cwes": [c for c in r["thread_cwe_signatures"].split(";") if c], "codes": r["codes"].split(",")})
    for r in csv.DictReader((CODES / "main_gh.csv").open()):
        main.append({"src": "GH", "thread": r["issue_url"], "role": "asker" if r["role"] == "R" else "responder",
                     "maintainer": r["role"] == "M", "form": "question" if r["form"] == "Q" else "statement",
                     "cwes": [c for c in r["thread_cwe_signatures"].split(";") if c], "codes": r["codes"].split(",")})
    off: list[dict[str, Any]] = []
    for r in csv.DictReader((CODES / "offcwe_so.csv").open()):
        off.append({"src": "SO", "thread": r["thread_url"], "role": r["role"], "theme": r["theme"],
                    "origin": r["origin"], "codes": r["codes"].split(",")})
    for r in csv.DictReader((CODES / "offcwe_gh.csv").open()):
        off.append({"src": "GH", "thread": r["issue_url"], "role": "asker" if r["role"] == "R" else "responder",
                    "theme": r["theme"], "codes": r["codes"].split(",")})
    return main, off


def diag(codes: list[str]) -> list[str]:
    return [c for c in codes if c not in NON_DIAGNOSTIC]


def write_csv(name: str, header: list[str], rows: list[list[Any]]) -> None:
    with (RESULTS / name).open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def analyze_main(rows: list[dict[str, Any]]) -> dict[str, Any]:
    threads: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"SO": set(), "GH": set()})
    occ: dict[str, Counter[str]] = defaultdict(Counter)
    for r in rows:
        for c in r["codes"]:
            if c == "NA":
                continue
            threads[c][r["src"]].add(r["thread"])
            occ[c][r["role"]] += 1
    dq_rows = []
    for k, (dim, q) in DQ_LABELS.items():
        if k in ("RK", "R6", "D5", "H1"):
            continue
        so, gh = len(threads[k]["SO"]), len(threads[k]["GH"])
        a, rsp = occ[k]["asker"], occ[k]["responder"]
        dq_rows.append([k, dim, q, so + gh, so, gh, a, rsp, round(100 * a / (a + rsp)) if a + rsp else 0])
    dq_rows.sort(key=lambda x: -x[3])
    write_csv("dq_frequencies.csv", ["dq", "dimension", "question", "threads", "so_threads", "gh_threads",
                                     "asker_occ", "responder_occ", "asker_share_pct"], dq_rows)

    tcodes: dict[str, set[str]] = defaultdict(set)
    tcwes: dict[str, list[str]] = {}
    for r in rows:
        tcwes[r["thread"]] = r["cwes"]
        tcodes[r["thread"]].update(diag(r["codes"]))
    dthreads = {t for t, cs in tcodes.items() if cs}
    cwe_rows, cwe_n = [], {}
    for cwe in CWES:
        ts = [t for t in dthreads if cwe in tcwes[t]]
        cnt = Counter(c for t in ts for c in tcodes[t])
        cwe_n[cwe] = len(ts)
        for c, n in cnt.most_common(6):
            cwe_rows.append([cwe, len(ts), c, n, round(100 * n / len(ts))])
    write_csv("per_cwe_top_dqs.csv", ["cwe", "diagnostic_threads", "dq", "threads", "share_pct"], cwe_rows)

    groups = {"SO askers": lambda r: r["src"] == "SO" and r["role"] == "asker",
              "SO responders": lambda r: r["src"] == "SO" and r["role"] == "responder",
              "GH reporters (statements)": lambda r: r["src"] == "GH" and r["form"] == "statement" and r["role"] == "asker",
              "GH responders (statements)": lambda r: r["src"] == "GH" and r["form"] == "statement" and r["role"] == "responder"}
    role_rows, ns = [], {}
    for g, f in groups.items():
        c: Counter[str] = Counter()
        for r in rows:
            if f(r):
                for k in r["codes"]:
                    if k == "G":
                        c["Report interpretation"] += 1
                    elif k not in NON_DIAGNOSTIC:
                        c[DQ_LABELS[k][0]] += 1
        n = sum(c.values())
        ns[g] = n
        for d in DIMS:
            role_rows.append([g, n, d, c[d], round(100 * c[d] / n) if n else 0])
    write_csv("role_by_dimension.csv", ["group", "n_diagnostic_occ", "dimension", "occ", "share_pct"], role_rows)
    return {"diagnostic_threads": len(dthreads), "so_threads_with_questions": len({r["thread"] for r in rows if r["src"] == "SO"}),
            "gh_issues_with_units": len({r["thread"] for r in rows if r["src"] == "GH"}),
            "dq_threads": {r[0]: r[3] for r in dq_rows}, "cwe_threads": cwe_n, "role_group_n": ns}


def analyze_off(rows: list[dict[str, Any]]) -> dict[str, Any]:
    tt: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"SO": set(), "GH": set()})
    tdq: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for r in rows:
        d = diag(r["codes"])
        if r["theme"] in ("IN", "NA") or not d:
            continue
        tt[r["theme"]][r["src"]].add(r["thread"])
        for c in d:
            tdq[r["theme"]][c].add(r["thread"])
    th_rows = []
    for th in sorted(tt, key=lambda t: -(len(tt[t]["SO"]) + len(tt[t]["GH"]))):
        so, gh = len(tt[th]["SO"]), len(tt[th]["GH"])
        top = sorted(tdq[th].items(), key=lambda kv: -len(kv[1]))[:5]
        th_rows.append([th, THEMES[th], so + gh, so, gh, " · ".join(f"{c} ({len(v)})" for c, v in top)])
    write_csv("offcwe_themes.csv", ["theme", "label", "threads", "so", "gh", "top_dqs"], th_rows)
    new = {}
    for c in ("RK", "R6", "D5", "H1"):
        new[c] = len({r["thread"] for r in rows if c in r["codes"]})
    write_csv("offcwe_new_dqs.csv", ["dq", "question", "threads"], [[c, DQ_LABELS[c][1], n] for c, n in new.items()])
    inside = {r["thread"] for r in rows if r["theme"] == "IN" and diag(r["codes"])}
    return {"offcwe_threads": len(set().union(*[v["SO"] | v["GH"] for v in tt.values()])) if tt else 0,
            "theme_threads": {r[0]: r[2] for r in th_rows}, "new_dq_threads": new, "inside_seven_threads": len(inside)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    main_rows, off_rows = load_rows()
    res = {"main": analyze_main(main_rows), "offcwe": analyze_off(off_rows)}
    (RESULTS / "results.json").write_text(json.dumps(res, indent=1))
    m, o = res["main"], res["offcwe"]
    top = sorted(m["dq_threads"].items(), key=lambda kv: -kv[1])[:6]
    md = ["# Results summary", "",
          f"- Diagnostic threads (main pass): {m['diagnostic_threads']}",
          f"- Top DQs by thread reach: " + ", ".join(f"{k} {v}" for k, v in top),
          f"- Diagnostic threads per CWE signature: " + ", ".join(f"{k} {v}" for k, v in m["cwe_threads"].items()),
          f"- Off-CWE threads: {o['offcwe_threads']} (plus {o['inside_seven_threads']} SO threads inside the seven CWEs)",
          f"- Off-CWE themes: " + ", ".join(f"{k} {v}" for k, v in o["theme_threads"].items()),
          f"- New DQs: " + ", ".join(f"{k} {v}" for k, v in o["new_dq_threads"].items()), "",
          "Tables: dq_frequencies.csv, per_cwe_top_dqs.csv, role_by_dimension.csv, offcwe_themes.csv, offcwe_new_dqs.csv"]
    (RESULTS / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    if a.check:
        exp = json.loads((RESULTS / "expected.json").read_text())
        bad = [k for k in exp if json.dumps(exp[k], sort_keys=True) != json.dumps(res[k], sort_keys=True)]
        log("CHECK: identical to the October 2026 report" if not bad else f"CHECK: differs in {bad}")


if __name__ == "__main__":
    main()
