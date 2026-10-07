# Advisor requirements: status and plan

Prepared 2026-10-06 for the MSR paper's developer-discussion dataset. All counts below were recomputed from the files in this folder. The markers mean:

- `[x]` done and verified against the data
- `[~]` partial: something exists but it is incomplete or needs rework
- `[ ]` not done: still needs to be collected or written

The advisor asked us to keep finished procedures separate from planned work. Every row below is one or the other, never both.

---

## 0. Reconciling the advisor's counts (verified)

The advisor counted **537 threads (346 Stack Overflow + 191 GitHub), 972 question items and 464 GitHub statements**. Those numbers are correct for `diagnostic_questions_coded.csv`, but that file is a **subset**:

1. It covers the **main pass only** (the seven target CWEs). The outside-the-seven pass is in a separate file, `diagnostic_questions_offcwe_coded.csv`.
2. It leaves out **407 units coded NA** (off-topic or rhetorical): 192 Stack Overflow questions, 18 GitHub questions and 197 GitHub statements.
3. It leaves out threads that were retrieved but contained no extractable unit.

### Stack Overflow, main pass

| Stage | Threads | Units | Rule |
| --- | --- | --- | --- |
| Retrieved (unique question IDs) | 745 | — | 55 queries × 2 sort orders (relevance, votes) × top 10; de-duplicated by question_id |
| Retained by thread filter | 480 | — | has a C/C++-ish tag, an allocation keyword, and ≥1 CWE regex signature |
| ≥1 memory-related interrogative | 380 | 1,107 questions | sentence ends in `?`, matches the memory regex, 10–450 chars; de-duplicated per thread |
| ≥1 non-NA code (advisor's count) | **346** | **915** (610 asker, 305 responder) | |
| ≥1 diagnostic code (excluding T1/G/P/K) | 334 | — | the population behind the report's frequency tables |

Raw content held for the 346 threads: 346 question bodies, **1,098 answers** (matches the advisor's 1,098) and **3,791 comments**. For all 480 retained threads: 1,347 answers and 4,702 comments.

### GitHub, main pass

| Stage | Issues | Units | Rule |
| --- | --- | --- | --- |
| Search hits | 320 | — | 32 queries × top 10 (a 33rd malformed query was discarded) |
| Unique issues retained | 305 | — | de-duplicated by URL; no further filter |
| ≥1 extracted unit | 216 | 75 questions + 661 statements | questions: `?` + memory regex; statements: diagnostic-question regex prefilter |
| ≥1 non-NA code (advisor's count) | **191** | **57 questions** (29 reporter, 28 responder) + **464 statements** | |
| ≥1 diagnostic code | 166 | — | |

### Outside-the-seven pass (not in the advisor's file)

| Source | Retrieved | Units coded | Notes |
| --- | --- | --- | --- |
| Stack Overflow | 241 targeted questions (38 queries) + 265 threads the main pass dropped | 380 questions in 209 threads | **answers and comments truncated** (see §2) |
| GitHub | 180 hits → 179 unique issues (18 queries) | 616 units in 126 issues | |
| Result | 197 threads outside the seven CWEs; 79 Stack Overflow threads turned out to be inside them | | |

---

## 1. Collection

| | Item | Status | Evidence / file | Action |
| --- | --- | --- | --- | --- |
| 1.1 | Sources searched | `[x]` | Stack Overflow via the StackExchange API 2.3; GitHub issue search API plus the issue pages | — |
| 1.2 | Exact search queries | `[x]` | `replication/config/queries.json` (both passes, both sources) | — |
| 1.3 | Collection dates | `[x]` | All collection happened on **2026-10-05**. Stack Overflow main cache written 11:57 UTC-4, off-CWE cache 12:36; GitHub on the same day | Record in the paper |
| 1.4 | Covered date range, Stack Overflow | `[x]` | main: questions 2008-08-04 → 2026-08-28, posts up to 2026-09-21; off-CWE: questions 2008-09-05 → 2025-03-28 | — |
| 1.5 | Covered date range, GitHub | `[x]` | Issue creation dates, 2004-09-03 → 2026-10-05, from the 2026-10-07 REST re-fetch (`coverage_gh.csv`, `coverage_gh_summary.md`). 484 issue records, 483 unique issues (one issue is in both passes) | — |
| 1.6 | How C/C++ leak discussions were identified | `[x]` | Stack Overflow: `c`/`c++` tag in the query, plus the tag / allocation-keyword / CWE-signature filter (`dq/codebook.py`). GitHub: `language:c` or `language:c++` on most queries, plus sanitizer-message strings | Note that GitHub was **not** filtered after search, so some non-C/C++ issues (Rust, Go, Godot) are in the 305; their units were coded NA |

## 2. Selection

| | Item | Status | Evidence / file | Action |
| --- | --- | --- | --- | --- |
| 2.1 | Inclusion / exclusion criteria | `[x]` | §0 tables; `dq/codebook.py` (thread filter, sentence filters) | Write them up as prose |
| 2.2 | Duplicate handling | `[x]` | question_id / issue URL de-duplication across queries; (thread, sentence) de-duplication within a thread | Cross-site duplicates were not checked: state this |
| 2.3 | Stage counts, Stack Overflow | `[x]` | §0 | — |
| 2.4 | Stage counts, GitHub | `[x]` | §0 | — |
| 2.5 | Completeness of the raw Stack Overflow data | `[x]` | **Main pass complete**: the 2026-10-07 re-query returned the same 745 / 2,293 / 8,706 questions, answers and comments, with no deleted or edited post. **Off-CWE pass was truncated and is now refetched with full paging** (answers 307 → 783, comments 700 → 2,903). The 380 coded off-CWE units come from the truncated data (see §8) | — |

## 3. Units and counts

| | Item | Status | Definition / count | Action |
| --- | --- | --- | --- | --- |
| 3.1 | Thread | `[x]` | one Stack Overflow question with its answers and comments, or one GitHub issue with its comments | — |
| 3.2 | Post / comment | `[x]` | Stack Overflow: question body, answer, comment (on a question or an answer). GitHub: issue body, issue comment | — |
| 3.3 | Extracted question | `[x]` | one sentence ending in `?` that passes the memory regex; Stack Overflow titles count if they end in `?` | — |
| 3.4 | Statement | `[x]` | GitHub only: a declarative sentence selected by the diagnostic-question regex prefilter (main) or the leak-keyword filter (off-CWE, max 4 per post) | — |
| 3.5 | Counts per unit type | `[x]` | §0 | — |
| 3.6 | Asker vs responder | `[x]` | Stack Overflow: matched on post owner user_id against the question owner. GitHub: issue author = reporter; owner/member/collaborator = maintainer; anyone else = other | — |
| 3.7 | Post-type breakdown (question body / answer / comment) for Stack Overflow units | `[x]` | `results/so_units_by_post_type.csv`. Main pass, 915 coded units: 135 titles (14.8%), 358 question bodies (39.1%), 81 answers (8.9%), 341 comments (37.3%). Counts by role and for the off-CWE pass are in the file | — |

## 4. Extraction and coding

| | Item | Status | Facts | Action |
| --- | --- | --- | --- | --- |
| 4.1 | How questions were extracted | `[x]` | scripted: HTML/Markdown cleaned (code blocks and quotes removed), sentences split by regex, filters applied (`scripts/03_extract_units.py`) | — |
| 4.2 | Wording preserved or synthesized | `[x]` | **Units are verbatim sentences.** Exceptions: GitHub text had URLs replaced by `<url>` and `=` turned into ` := `, and was truncated to 240–300 chars. The 28+4 **canonical diagnostic questions and the "usually asked as" phrasings in the report are synthesized** by the coder | State this explicitly in the paper |
| 4.3 | How the codebook was developed | `[x]` | top-down seed from the user-specified evidence dimensions (allocation, ownership, deallocation, escape, control flow, lifetime, aliasing), then bottom-up extension during coding (report interpretation, composite cleanup, cross-module, 4 non-diagnostic codes); 4 more codes added in the off-CWE pass (RK, R6, D5, H1). Docs: `docs/CODEBOOK.md` | No codebook revision log was kept: say so |
| 4.4 | Multiple codes per item | `[x]` | yes: 1–4 codes per unit, mostly 1–2 | — |
| 4.5 | Automated / LLM-assisted steps | `[x]` | **automated:** retrieval, filtering, sentence extraction, regex prefilter (selection only, never coding). **LLM:** *all* coding labels were assigned by Claude (an LLM) reading the extracted sentences in batches. No human coded any unit | Must be disclosed as LLM-coded |
| 4.6 | What was read when labelling | `[x]` | **Only the extracted sentences**, each shown with its role. Question bodies, answers and comments were not read as whole threads, and long sentences were shown truncated (~200–260 chars). Collected ≠ reviewed: thousands of answers and comments were collected but only their extracted interrogatives were labelled | State this explicitly |
| 4.7 | Per-thread CWE labels | `[x]` | regex signatures, not manual; noisy (CWE-761 contaminated) | — |

## 5. Validation

| | Item | Status | Facts | Action |
| --- | --- | --- | --- | --- |
| 5.1 | Who reviewed the data | `[x]` (none) | **No independent human review.** One LLM coder | — |
| 5.2 | Items independently checked | `[ ]` | 0. A 200-unit blind sample is drawn: `validation/second_coder_sample.csv` (seed 7). No human has labelled it | A human labels the sample, then run `06_second_coder.py kappa` (task V1) |
| 5.3 | Disagreement resolution | `[ ]` | Protocol written in `replication/docs/ADJUDICATION.md`. It has not been run | Run it after the second coder finishes (task V2) |
| 5.4 | What remains unvalidated | `[x]` | all 2,614 non-NA code assignments over 2,839 units (plus the NA decisions themselves); per-thread CWE labels; NA decisions; role assignment edge cases | — |
| 5.5 | Spot checks performed | `[~]` | the coder eyeballed regex-prefilter precision and checked that example links resolve; these are informal and unquantified | Don't report them as validation |

## 6. Traceability and reproducibility

| | Item | Status | Evidence / file | Action |
| --- | --- | --- | --- | --- |
| 6.1 | Item → source URL | `[x]` | every coded row has the thread URL plus the post permalink (Stack Overflow answer/comment anchors; GitHub `#issuecomment-id`) | — |
| 6.2 | Item → original text | `[x]` | Stack Overflow: verbatim sentence from step 3. GitHub: recovered by the REST re-fetch. `item_source_map.csv` has a sentence for 2,612 of 2,614 rows. The 2 other rows are orphaned codes (see §8) | — |
| 6.3 | Scripts | `[x]` | `replication/` (steps 01–06, tests, README) | — |
| 6.4 | Releasable data | `[~]` | codes, keys, IDs, queries: releasable. Post text: CC BY-SA (Stack Overflow) / authors' (GitHub). Release IDs and scripts, or text with attribution | Decide release policy with the advisor |

## 7. Full Stack Overflow threads (advisor's second message)

| | Item | Status | Evidence | Action |
| --- | --- | --- | --- | --- |
| 7.1 | Full question bodies with code blocks | `[x]` | `data/raw/so_main.json` (HTML `body`, code intact) for all 745 | Export (S1) |
| 7.2 | All answers | `[x]` | 2,293 answers (main) and 783 (off-CWE, refetched). Both complete | — |
| 7.3 | Comments on questions and answers | `[x]` | 8,706 (main) and 2,903 (off-CWE, refetched). Both complete. The advisor's review had **none**, so ours fills that gap | — |
| 7.4 | Chronological order | `[x]` | `creation_date` on every post and comment | Sort in the export |
| 7.5 | IDs | `[x]` | question_id, answer_id, comment_id, post_id | — |
| 7.6 | Author roles | `[x]` | Owner user_id, display name, and the asker / responder role in every export file. 25 questions have an owner without a user_id (deleted account). Their role is not reliable, and `author_id_missing` flags them | — |
| 7.7 | Timestamps | `[x]` | creation, last-activity and edited flag | — |
| 7.8 | Accepted-answer status | `[x]` | `accepted_answer_id`, `is_accepted` | — |
| 7.9 | Permalinks | `[x]` | question link; answer and comment permalinks built from IDs | — |
| 7.10 | Map spreadsheet item → source post and thread | `[x]` | `item_source_map.csv`, 2,614 rows. Every row was checked against `codes/*.csv` (0 mismatches) | — |
| 7.11 | Coverage summary (missing, deleted, inaccessible, truncated) with dates | `[x]` | `coverage_so.csv`, `coverage_so_summary.md`, `coverage_gh.csv`, `coverage_gh_summary.md`. Fetch date 2026-10-07 | — |
| 7.12 | JSON plus readable export | `[x]` | `threads/so/` (955 threads) and `threads/gh/` (483 threads), each as `.json` and `.md` | — |
| 7.13 | Which material was read when labelling | `[x]` | §4.6 | — |

---

## Task list (planned work, not yet done)

**Stack Overflow** (can run in the cloud session or locally; no token needed, but a `STACKEXCHANGE_KEY` raises the quota)
- [x] **S1** (done 2026-10-07; `threads/so/`, `coverage_so.csv`): Build `threads/so/<qid>.json` and `<qid>.md` from the main cache: chronological, code blocks kept, roles, accepted flag, permalinks. Re-query all IDs to detect deletions or edits since 2026-10-05, and write `coverage_so.csv`.
- [x] **S2** (done 2026-10-07; only the 241 targeted threads were truncated, the 265 dropped threads come from the complete main cache): Re-fetch the off-CWE threads (241 + 265) with full pagination; re-extract and diff against the 380 coded units.
- [x] **S3** (done 2026-10-07; `item_source_map.csv`): Write `item_source_map.csv`: item_id → unit_key → post type → post id → permalink → thread URL → verbatim sentence.
- [x] **S4** (done 2026-10-07; `results/so_units_by_post_type.csv`): Tabulate units by post type (body / answer / comment) and role.

**GitHub** (needs `GITHUB_TOKEN`; run locally, e.g. in VS Code)
- [x] **G1** (done 2026-10-07; both passes fetched, 0 unavailable): `python replication/scripts/02_mine_gh.py --pass main --snapshot` and `--pass offcwe --snapshot` to get full issue bodies and all comments, with dates.
- [x] **G2** (done 2026-10-07; see §8 for the join result): Re-extract units (step 03), join to codes (step 04), report the join rate, and list the units the browser timeline missed in `data/to_code/`.
- [x] **G3** (done 2026-10-07; `threads/gh/`, `coverage_gh.csv`): Export `threads/gh/*.json|md` and `coverage_gh.csv`.

**Validation and write-up**
- [~] **V1** (sample drawn, human labelling not done): Second human coder on a stratified sample of about 200 units; compute κ per code and per dimension.
- [~] **V2** (protocol and reconstructed revision log written in `replication/docs/`; not yet run): Adjudication protocol (two coders plus a third to break ties) and a codebook revision log.
- [~] **W1** (draft in `methods_draft.tex`; the human-validation sentence must change after V1): Methods text for the paper, drawn from §1–§6, separating done from planned work.


---

## 8. Re-fetch results, 2026-10-07 (done)

**Limits first.** The published counts in §0 did not change. Nobody has coded the new units below. The 4 orphaned codes in §8.2 are not explained in full. The 13 issues in §8.3 have comment text that we cannot get.

### 8.1 Stack Overflow

| Pass | Questions | Answers: 2026-10-05 → 2026-10-07 | Comments: 2026-10-05 → 2026-10-07 | Edited or deleted posts |
| --- | --- | --- | --- | --- |
| main | 745 | 2,293 → 2,293 | 8,706 → 8,706 | 0 |
| off-CWE (241 targeted threads) | 241 | 307 → 783 | 700 → 2,903 | 0 |

- Main pass: the 480 threads, 1,107 units and 100% join with the hand codes were reproduced.
- Off-CWE pass: all 380 coded units still join. Re-extraction finds **96 new units** in the answers and comments that the truncation had cut. They are in `replication/data/to_code/offcwe_so.csv`.
- 31 questions are in both passes. The thread export holds 955 unique Stack Overflow threads.

### 8.2 GitHub: join of the 2026-10-05 hand codes with the REST re-fetch

| Pass | Issues | Units re-extracted | Matched to a hand code | New (uncoded) units | Orphaned codes |
| --- | --- | --- | --- | --- | --- |
| main | 305 | 1,226 | 734 of 736 codes | 492 | 2 |
| off-CWE | 179 | 888 | 614 of 616 codes | 274 | 2 |

- **New units.** In the main pass, 487 of the 492 new units are in posts that had no coded unit. This fits comments that the logged-out browser timeline did not show. We did not test the browser behaviour.
- **Orphans.** The 4 codes with no matching unit are `llvm/llvm-project#52997` (issue body, D3), `davitkalantaryan/xdr_rpc#4` (issue body, R4), `rust-lang/unsafe-code-guidelines#316` (comment 1009298561, NA) and `awmc000/readability#1` (issue body, ordinal 3, NA). Only the first two have a non-NA code.
- **Cause, as far as known.** In the first two issues the matching sentence is in the issue *title*. The 2026-10-05 run seems to have selected statements from the title plus the body. We tested adding the title in step 03. It restored those two units but broke other keys (9 and 3 orphans), so we reverted it. The other two orphans have no known cause. The four issues show no activity after 2026-03-22 (field `updated_at`), and all four posts still exist.
- **Consequence.** Two non-NA items have no sentence in `item_source_map.csv` (`text_status` = `unit_not_found`). Their codes and permalinks remain in the file.

### 8.3 GitHub coverage

- 484 issue records, 483 unique issues (`nginx/njs#1099` is in both passes). All were fetched: 0 unavailable, 0 moved.
- Issue creation dates: 2004-09-03 to 2026-10-05.
- Repository language, as GitHub reports it: main, 266 of 305 issues in C or C++ repositories; off-CWE, 165 of 179. This classifies the repository, not the file that the issue discusses.
- For 13 issues (16 comments in total) GitHub reports more comments than the REST endpoint returns. Repeating the request gives the same result. The text of those comments is not available.

### 8.4 New files

| File | Content |
| --- | --- |
| `threads/so/*.json\|md`, `threads/gh/*.json\|md` | Full threads in chronological order, with code blocks, roles, permalinks |
| `coverage_so.csv`, `coverage_so_summary.md`, `coverage_gh.csv`, `coverage_gh_summary.md` | Coverage per thread |
| `item_source_map.csv` | 2,614 rows: item → unit key → post → permalink → thread → sentence. Every link was verified |
| `results/so_units_by_post_type.csv` | Stack Overflow units by post type and role |
| `validation/second_coder_sample.csv` | 200-unit blind sample, seed 7, codes empty |
| `replication/docs/ADJUDICATION.md`, `replication/docs/CODEBOOK_CHANGELOG.md` | Planned protocol; reconstructed revision log |
| `methods_draft.tex` | Draft methods text for the paper |
| `PROGRESS.md` | Session log with the commands to resume |
