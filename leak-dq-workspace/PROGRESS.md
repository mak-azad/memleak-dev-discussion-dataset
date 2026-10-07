# Progress log for the advisor-request plan

Last update: 2026-10-07. Plan file: `/home/akazad/.claude/plans/can-you-read-qa-coverage-question-so-gh-fancy-river.md`.
Results and counts: `advisor_requirement_plan.md`, section 8.
All commands run from `replication/`. Load the keys first: `set -a; source ../.env; set +a`.

## Done (all verified)

- Preflight, A1 to A5, B0 to B3, C1 (sample drawn), C2 (documents written), C3 (draft written).
- Checks that passed on 2026-10-07: `05_analyze.py --check` prints "identical"; `tests/test_extract.py` prints ok; `09_item_source_map.py --strict` reports 0 mismatches over 2,614 rows.
- Wiki ingest done: `wiki/pipeline/dev-discussion-dataset.md`, decision D-2026-10-07, index, open question, log.
- Nothing is committed. The whole workspace is untracked in Git. `.env` and `replication/data/` are ignored.

## Not done (needs a human)

- [ ] V1: a human labels `validation/second_coder_sample.csv`. Then run `python3 scripts/06_second_coder.py kappa ../validation/second_coder_sample.csv`.
- [ ] V2: run the protocol in `replication/docs/ADJUDICATION.md` on the disagreements.
- [ ] Update the validation sentence in `methods_draft.tex` after V1.
- [ ] Decide whether to code the uncoded units found on re-fetch (96 Stack Overflow, 492 + 274 GitHub). Today they stay uncoded (decision D-2026-10-07).
- [ ] Decide the release policy for post text (row 6.4).
- [ ] Decide about the 4 orphaned hand codes (section 8.2). Two have no known cause.
- [ ] Decide whether to commit the new scripts and documents. Do not commit `threads/`, `data/`, or `.env`. They hold post text or keys.

## To rerun everything

`cd replication && set -a && source ../.env && set +a && ./run_all.sh`
This refetches both sources. The Stack Overflow cache copies in `replication/data/raw/*_cached.json` must exist first. Copy them from `../data/raw/*_2026-10-05.json`.
