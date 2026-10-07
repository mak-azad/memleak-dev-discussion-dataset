# Content index: developer-discussion dataset for C/C++ memory leaks

Written 2026-10-07 for the advisor. This page answers the advisor's requests and points to the file for each answer.

## Status in one paragraph

All data requests are complete except human validation. We collected full Stack Overflow and GitHub threads, with coverage reports and a map from every coded item to its source post. One LLM (Claude) assigned all labels. No human has checked any label. A blind sample of 200 units is ready for a second coder.

## Key numbers

All counts are for the main pass (the seven target CWEs), unless the row says otherwise.

| Quantity | Value | Where it comes from |
| --- | --- | --- |
| Stack Overflow threads retrieved, then kept by the thread filter | 745, then 480 | `leak-dq-workspace/advisor_requirement_plan.md` §0 |
| Stack Overflow threads with at least one coded unit | 346 (915 units) | same |
| GitHub issues retrieved | 305 | same |
| GitHub issues with at least one coded unit | 191 (57 questions, 464 statements) | same |
| Threads and units the advisor counted | 537 threads (346 + 191), 972 question items, 464 statements | §0 explains why these are a subset of the full data |
| Rows linking coded items to source posts, both passes | 2,614 | `leak-dq-workspace/item_source_map.csv` |
| Thread files exported | 955 Stack Overflow, 483 GitHub | `leak-dq-workspace/threads/` |

## The advisor's requests

| Request | Status | Answer is in |
| --- | --- | --- |
| Sources, queries, collection dates, date ranges | Done | `advisor_requirement_plan.md` §1 and `replication/config/queries.json` |
| Selection criteria, duplicate handling, stage counts | Done | `advisor_requirement_plan.md` §0 and §2 |
| Definitions of thread, post, question, statement | Done | `advisor_requirement_plan.md` §3 |
| How questions were extracted and coded, and whether wording is verbatim | Done | `advisor_requirement_plan.md` §4 |
| Which material the coder read | Done: only the extracted sentences | `advisor_requirement_plan.md` §4.6 |
| Traceability from each item to its source | Done | `item_source_map.csv`, `replication/scripts/09_item_source_map.py` |
| Full Stack Overflow threads: code blocks, all answers and comments, order, IDs, roles, timestamps, accepted flag, permalinks | Done | `threads/so/<question_id>.json` and `.md` |
| Coverage summary: missing, deleted, truncated posts, with dates | Done | `coverage_so_summary.md`, `coverage_so.csv` |
| Full GitHub threads | Done | `threads/gh/`, `coverage_gh_summary.md`, `coverage_gh.csv` |
| Independent validation of the labels | **Not done** | Sample: `validation/second_coder_sample.csv`. Protocol: `replication/docs/ADJUDICATION.md` |
| Release policy for post text | **Not decided** | `advisor_requirement_plan.md` row 6.4 |

## What the re-fetch on 2026-10-07 showed

1. The main Stack Overflow data had not changed since 2026-10-05. No post was edited or deleted.
2. The off-CWE Stack Overflow data had been cut. Answers grew from 307 to 783, and comments from 700 to 2,903.
3. The re-fetch found units that no one coded: 96 on Stack Overflow, 492 on GitHub (main pass), and 274 on GitHub (off-CWE pass). We left the published counts unchanged and did not code them.
4. Four hand codes have no matching unit now. Two have no known cause. Details are in `advisor_requirement_plan.md` §8.2.
5. For 13 GitHub issues, GitHub reports 16 more comments than its API returns. We cannot get the text of those 16 comments.

## Limits to read before citing any number

- **LLM-coded.** Claude assigned every label, and the coder read only the extracted sentences, not whole threads.
- **No agreement figure yet.** We report no kappa until a human labels the sample.
- **Roles.** For 25 Stack Overflow questions the owner has no user ID, so the asker or responder role is not reliable for those posts.
- **GitHub repository language.** The language field describes the repository, not the file that the issue discusses.
- **Codebook history.** No log was kept during coding. `replication/docs/CODEBOOK_CHANGELOG.md` is a reconstruction, and it says so.
- **Old status file.** `status.md` is the 2026-10-06 snapshot. `leak-dq-workspace/advisor_requirement_plan.md` replaces it.

## Decisions we need from the advisor

1. Who is the second coder for the 200-unit sample?
2. Should we code the uncoded re-fetch units, or keep the published counts fixed? We kept them fixed.
3. May we release post text, or only IDs, keys, codes, and scripts? Stack Overflow text is CC BY-SA. GitHub text belongs to its authors.

## Map of the repository

| Path | Content |
| --- | --- |
| `content_index.md` | This page |
| `status.md` | Old status snapshot of 2026-10-06 |
| `leak-dq-workspace/advisor_requirement_plan.md` | Full status of every request, reconciled counts (§0), re-fetch results (§8) |
| `leak-dq-workspace/threads/` | Full thread exports, `so/` and `gh/` |
| `leak-dq-workspace/item_source_map.csv` | Item, unit key, post, permalink, thread, verbatim sentence |
| `leak-dq-workspace/coverage_*.csv` and `coverage_*_summary.md` | Coverage reports |
| `leak-dq-workspace/outputs/` | The CSVs shared earlier: coded items, codebook, off-CWE extension |
| `leak-dq-workspace/validation/` | Blind sample for the second coder |
| `leak-dq-workspace/methods_draft.tex` | Draft methods text, LaTeX |
| `leak-dq-workspace/replication/` | Scripts (steps 1 to 10), search queries, hand codes, codebook, tests |
| `leak-dq-workspace/data/interim/` | Extraction and coding intermediates |
| `leak-dq-workspace/PROGRESS.md` | Session log and open items |

The raw API caches (`data/raw/`) and the API keys (`.env`) are not in the repository.

## How to reproduce

1. To recompute every report table offline, run `cd leak-dq-workspace/replication && python3 scripts/05_analyze.py --check`. The output must say "identical to the October 2026 report".
2. To refetch the data, copy `.env.example` to `.env`, add the keys, and run `./run_all.sh`. `replication/README.md` lists the steps and the Stack Overflow cache files that the coverage step needs.
