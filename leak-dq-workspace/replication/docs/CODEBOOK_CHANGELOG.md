# Codebook revision log

**This log is a retrospective reconstruction.** No log was kept while the codebook was developed in October 2026. The entries below come from `docs/CODEBOOK.md`, `dq/codebook.py`, and the project notes. They do not record the order of edits within a phase, and they do not record which units the first coder re-labelled after a change. Do not cite this file as a contemporaneous record.

The only version identifier in the code is `CODEBOOK_VERSION = "2026-10-05"`.

## Reconstructed history

| Phase | What changed | Source of this fact |
| --- | --- | --- |
| 1. Top-down seed | Started from the evidence dimensions the researcher specified: allocation, ownership, deallocation, escape, control flow, lifetime, aliasing. | `advisor_requirement_plan.md` row 4.3 |
| 2. Bottom-up extension during main-pass coding | Added dimensions and codes that the data needed: Report interpretation (V1, R2-R5), Composite cleanup (N1-N3), Cross-module (X1), and four non-diagnostic codes (G, T1, P, K). The main pass ended with 32 codes. | Row 4.3; `dq/codebook.py` header ("32 original") |
| 3. Off-CWE pass | Added four codes: RK (resource kind), R6 (RSS growth versus allocator retention), D5 (use after release), H1 (earlier heap corruption). Added the theme list for the off-CWE pass. The codebook has 36 codes after this phase. | Row 4.3; `docs/CODEBOOK.md` ("Added in the off-CWE pass") |
| 4. Documentation | `docs/CODEBOOK.md` wrote the include and exclude rules for each code. Version 2026-10-05. | `docs/CODEBOOK.md` line 3 |

## Observations from reading the files (cause not recorded)

- `DQ_PATTERNS` in `dq/codebook.py` names the report-verdict pattern `R1`. The codebook and the codes name the same code `V1`. The pattern list is only a regex prefilter, so this does not change any code. The reason for the two names is not recorded.
- The main-pass prefilter patterns cover only some codes (for example, there is no pattern for L4, or for the off-CWE codes). Codes were assigned by hand on the prefiltered sentences, not by the patterns.

## Rules for future entries

Add one row for every change, with the date, the code ids, the rule text before and after, the reason, and the number of units that need re-coding. Bump `CODEBOOK_VERSION` in `dq/codebook.py` in the same commit. See `docs/ADJUDICATION.md` for when a change is allowed.
