# Diagnostic questions for memory-leak and invalid-free bugs: replication package

This package reproduces the findings of the report *Diagnostic Questions for Memory-Leak / Invalid-Free Bugs: Evidence from Stack Overflow and GitHub* (October 2026). It mines Stack Overflow and GitHub, extracts sentence-level units, joins them with the hand codes, and recomputes every frequency table in the report.

There are two levels of reproduction:

| Level | Needs | Result |
| --- | --- | --- |
| **A. Recompute the tables** | Python ≥ 3.10, nothing else | `python scripts/05_analyze.py --check` rebuilds every number in the report from `codes/*.csv` and verifies it against `results/expected.json`. |
| **B. Re-mine and re-join** | network, `GITHUB_TOKEN`, optional `STACKEXCHANGE_KEY` | `./run_all.sh` refetches the exact threads of the October 2026 run (`snapshot/`), re-extracts units, joins them with the hand codes, and reports join rates and newly appearing units. |

## Quick start

```bash
python scripts/05_analyze.py --check        # level A, offline: prints "identical to the October 2026 report"
python tests/test_extract.py                # unit-selection rules

export GITHUB_TOKEN=ghp_...                 # level B
export STACKEXCHANGE_KEY=...                # optional; without it the StackExchange quota is 300 requests/day per IP
./run_all.sh                                # snapshot replication
./run_all.sh --search                       # rerun the searches instead (corpus will drift)
```

## Pipeline

```
config/queries.json ─┐
snapshot/*.json  ────┼─> 01_mine_so.py ─┐
                     └─> 02_mine_gh.py ─┴─> data/raw/ ─> 03_extract_units.py ─> data/units/*.jsonl
                                                                                     │
codes/*.csv (hand codes, keyed by unit_key) ─────────────────> 04_join_codes.py <───┘
                                                                     │
                                       data/coded/*.csv   data/to_code/*.csv (new, uncoded units)
                                                                     │
codes/*.csv ──────────────────────────────────────────────> 05_analyze.py ─> results/*.csv, summary.md
                                                            06_second_coder.py ─> sample + Cohen's κ
```

| Step | Script | What it does |
| --- | --- | --- |
| 1 | `01_mine_so.py --pass main\|offcwe [--snapshot]` | StackExchange API: questions with bodies, all answers, comments on questions and answers. |
| 2 | `02_mine_gh.py --pass main\|offcwe [--snapshot]` | GitHub REST: issue search, issue body and all comments, plus author association. |
| 3 | `03_extract_units.py` | Applies the thread filter and unit-selection rules from `dq/codebook.py` and assigns stable `unit_key`s. |
| 4 | `04_join_codes.py` | Joins units to hand codes. Writes uncoded units, with their text, to `data/to_code/`, and counts orphaned codes. |
| 5 | `05_analyze.py [--check]` | Thread reach per diagnostic question (DQ), per-CWE shares, role × dimension, off-CWE themes and new DQs. |
| 6 | `06_second_coder.py sample\|kappa` | Draws a stratified blind sample of exactly *n* units (strata: source × dimension, NA included) for a second labeller. Computes per-code and per-dimension κ with bootstrap 95% intervals, and exact agreement with a Wilson interval. |
| 7 | `07_coverage_so.py` | Diffs the cached 2026-10-05 Stack Overflow data against a fresh re-query. Writes `coverage_so.csv` and `coverage_so_summary.md` in the workspace root. |
| 8 | `08_export_threads.py --source so\|gh` | Exports full threads, chronological, as `threads/<source>/*.json` and `*.md`. The `gh` mode also writes `coverage_gh.csv`. |
| 9 | `09_item_source_map.py [--strict]` | Links each row of `outputs/*.csv` to its unit key, source post, and verbatim sentence. Verifies every link. Writes `item_source_map.csv`. |
| 10 | `10_post_type_table.py` | Counts Stack Overflow units by post type and role. Writes `results/so_units_by_post_type.csv`. |

## The two passes

- **main**: the seven target CWEs (401, 459, 590, 761, 762, 763, 789). Stack Overflow uses 55 queries × 2 sort orders, and a thread is kept only if it has a C/C++-ish tag, an allocation keyword and at least one CWE signature (480 of 745 threads). GitHub uses 32 issue searches (305 issues). Units are 1,107 Stack Overflow interrogatives, 75 GitHub interrogatives and 661 GitHub statements prefiltered by the DQ regexes.
- **offcwe**: leak questions outside the seven CWEs. Stack Overflow uses 38 themed queries plus the 265 threads the main pass dropped; GitHub uses 18 themed issue searches (179 issues). Units are 380 Stack Overflow interrogatives (after a leak-relevance filter) and 616 GitHub sentences.

## Unit keys (how hand codes survive re-mining)

| Source / pass | `unit_key` | Breaks when |
| --- | --- | --- |
| Stack Overflow (both) | `sha1(post_permalink + "\x1f" + sentence)[:16]` | the post text is edited |
| GitHub main | `issue_url\|comment_id\|form\|ordinal` (`-` = title or body; form Q/S) | earlier selected sentences in the same post change |
| GitHub offcwe | `issue_url\|comment_id\|ordinal` | the same |

Tested here: re-extracting from the October 2026 Stack Overflow cache gives 480 threads and 1,107 + 380 units, with a 100% join. The GitHub path is covered by `tests/test_extract.py`, but it has not been run end-to-end against the live API (see Provenance).

## Extending the study

- **Add queries.** Edit `config/queries.json`, run steps 1–4 *without* `--snapshot`, code `data/to_code/*.csv`, and append the coded rows to `codes/<pass>_<source>.csv`. Then run step 5; drop `--check` because the numbers will change.
- **Change selection rules or the codebook.** Edit `dq/codebook.py` and bump `CODEBOOK_VERSION`. Changing a regex changes which units exist, so re-run steps 3–4 and inspect the orphan and new counts. Add new DQ codes to `DQ_LABELS` and document them in `docs/CODEBOOK.md`.
- **Second labeller.** `python scripts/06_second_coder.py sample --n 200 --out ../validation/second_coder_sample.csv` (protocol: `docs/ADJUDICATION.md`). A blind coder fills `codes` using `docs/CODEBOOK.md`; then run `python scripts/06_second_coder.py kappa ../validation/second_coder_sample.csv`. Run steps 1–4 first so the sample carries sentence text.
- **New source** (mailing lists, Bugzilla, Chromium/Mozilla trackers). Write a `0x_mine_<src>.py` that emits the raw shape of step 2, add an extractor in step 3 with a stable key, and add a `codes/<pass>_<src>.csv`.
- **LLM-assisted coding.** `data/to_code/*.csv` is the natural input. Keep the human codes as the reference and report κ between the model and the human coder.

## Provenance and known deviations

- **GitHub collection in October 2026** used logged-out search-API calls and the issue page's embedded timeline, read through a browser, because the API was blocked from the analysis sandbox. The embedded timeline can omit the middle of long threads. `02_mine_gh.py` uses the authenticated REST API instead, so a replication may surface extra units; they appear in `data/to_code/`.
- **GitHub text was sanitized** in transit: URLs were replaced by `<url>`, and `=` became ` := `. This affects only the stored text, not selection or keys.
- **Malformed query dropped.** One GitHub query from the original run (a malformed OR query for CWE-761) returned millions of results and was discarded; it is not in the config.
- **One coder.** All units were hand-coded by a single coder (Claude, the AI model), with no agreement figure yet. Step 6 exists to fix that.
- **Search drift.** Search results change over time, so use `--snapshot` for a faithful replication. Deleted or closed posts are logged and simply go missing.
- **Licensing.** Stack Overflow content is CC BY-SA, and GitHub issue text belongs to its authors. The package ships IDs, keys and codes only; post text is refetched locally into `data/` (git-ignored).

## Layout

```
codes/       hand codes (unit_key, URLs, role, CWE signatures or theme, codes): the research artefact
config/      queries.json (all search queries of both passes)
docs/        CODEBOOK.md (definitions plus include/exclude rules)
dq/          codebook.py (labels, regexes, cleaning and splitting rules: single source of truth)
results/     tables from step 5; expected.json = numbers in the October 2026 report
scripts/     01–06 pipeline, common.py
snapshot/    exact Stack Overflow question IDs and GitHub issue URLs of the October 2026 run
tests/       unit-selection rule tests
```
