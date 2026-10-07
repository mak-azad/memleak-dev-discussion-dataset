# Workspace: diagnostic questions for C/C++ memory-leak bugs (MSR dataset)

Context for whoever, human or AI agent, picks this up in VS Code.

## What this is
A dataset of developer discussions from Stack Overflow and GitHub about C/C++ memory leaks and invalid frees, collected on 2026-10-05. Sentence-level questions and statements were extracted and coded into a 36-code diagnostic-question codebook. **All coding was done by an LLM (Claude); no human has validated it yet.** The advisor's open requests and their status are in `advisor_requirement_plan.md`. Start there.

## Layout
```
advisor_requirement_plan.md   checklist of the advisor's requests: done vs planned, reconciled counts
outputs/                      the CSVs that were shared (coded items, codebook, off-CWE extension)
replication/                  pipeline scripts 01–06, config/queries.json, dq/codebook.py, codes/, snapshot/, tests/
data/raw/                     Stack Overflow API caches from 2026-10-05 (questions + answers + comments, HTML bodies)
                                 so_main_raw_*.json   745 questions, 2,293 answers, 8,706 comments (complete)
                                 so_offcwe_raw_*.json 241 questions; answers/comments TRUNCATED (100 per 80-question batch)
data/interim/                 extraction and coding intermediates (verbatim SO sentences, GitHub key tables)
```

## Setup
```bash
cp .env.example .env            # put GITHUB_TOKEN=... (or rely on `gh auth login`); STACKEXCHANGE_KEY optional
cd replication
python scripts/05_analyze.py --check      # offline; must print "identical to the October 2026 report"
python tests/test_extract.py
# reuse the 2026-10-05 Stack Overflow cache instead of re-downloading:
mkdir -p data/raw && cp ../data/raw/so_main_raw_2026-10-05.json data/raw/so_main.json
```
The token is read in this order: the `GITHUB_TOKEN`/`GH_TOKEN` environment variables, then `.env` (in the workspace root or `replication/`), then `gh auth token`. Never commit `.env`.

## Next tasks (see the plan for details)
- **G1–G3** (needs the token): `python scripts/02_mine_gh.py --pass main --snapshot` and `--pass offcwe --snapshot`, then steps 03 and 04, then the thread export and coverage report.
- **S1–S4**: full Stack Overflow thread export (JSON + Markdown), off-CWE re-fetch with full pagination, `item_source_map.csv`, post-type tabulation.
- **V1–V2**: second human coder and κ (`scripts/06_second_coder.py`).

## Rules
- Don't change the codes in `replication/codes/` without a note in the plan. They are the research record.
- Keep "collected" and "reviewed by the coder" distinct: the coder saw only extracted sentences, not whole threads.
- Quote source text only from the fetched posts, with permalinks. Don't quote from the report, which uses paraphrases.
