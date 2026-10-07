# Adjudication protocol (planned, not yet run)

Status: **planned**. No second coder has labelled any unit. All existing codes come from one LLM coder (Claude). This document says how the human validation will run, so the rules exist before any data is compared.

## Roles

| Role | Who | Task |
| --- | --- | --- |
| First coder | Claude (LLM) | Made all existing codes in `codes/*.csv`. Its codes are fixed. |
| Second coder | One human | Labels a blind sample with `docs/CODEBOOK.md` only. |
| Tie-breaker | A second human, who has not seen either label | Labels only the units where the first two coders disagree. |

## Steps

1. Run steps 1-4 so `data/coded/*.csv` holds the sentence text of every unit.
2. Draw the sample: `python scripts/06_second_coder.py sample --n 200 --seed 7 --out ../validation/second_coder_sample.csv`. The sheet hides the first coder's codes.
3. The second coder reads the sentence and the permalink. The second coder may open the permalink for context. The second coder fills `codes` with one or more codebook ids, or `NA`.
4. Compute agreement: `python scripts/06_second_coder.py kappa ../validation/second_coder_sample.csv`. Report Cohen's kappa per code and per dimension with the bootstrap 95% interval, the NA-versus-diagnostic kappa, and exact agreement with its Wilson interval.
5. List every unit where the two code sets differ. The tie-breaker labels those units blind. The tie-breaker sees the sentence and the permalink, not the two earlier labels.
6. The final label of a disputed unit is the code set that at least two of the three coders gave. If all three code sets differ, the unit is marked `unresolved` and the two coders and the tie-breaker discuss it. The agreed label is then recorded with the note `discussed`.

## Rules

- **Unit of agreement.** One unit is one extracted sentence. A code set is exact-equal only when both sets match.
- **NA counts as a label.** A disagreement between NA and a diagnostic code is a disagreement. This checks the NA decisions, which no one has validated.
- **No changes to `codes/*.csv` during labelling.** The first coder's codes stay as the research record. Adjudicated labels go in a new file, `validation/adjudicated.csv`, with columns `unit_key, first_codes, second_codes, third_codes, final_codes, method`.
- **Codebook changes.** If a disagreement shows that a codebook rule is unclear, write the new rule in `docs/CODEBOOK_CHANGELOG.md` with the date and the units that prompted it. Do not apply a changed rule to units outside the sample without recoding them and recording the count.
- **Reporting.** The paper reports the sample size, the sampling frame (strata and seed), the kappa values with intervals, and the number of units that went to the tie-breaker. It states that the sample covers 200 of the coded units and that the remaining units are not human-validated.

## Known limits

- A sample of 200 units over about 30 codes gives wide kappa intervals for rare codes. Report the interval, and mark codes with fewer than 5 occurrences in either coder as "too rare to estimate".
- The sample is stratified, not proportional. Overall agreement is therefore not an estimate for the whole dataset unless it is re-weighted by stratum size.
