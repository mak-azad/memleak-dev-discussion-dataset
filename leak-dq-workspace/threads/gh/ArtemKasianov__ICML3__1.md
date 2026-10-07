# Could variable gene ID lengths cause free(): invalid pointer error?

- URL: https://github.com/ArtemKasianov/ICML3/issues/1
- Repo: ArtemKasianov/ICML3 (language: C)
- State: open; created 2026-07-16T09:08:15Z; status ok; passes main

## Issue body

reporter (NONE) · albidgy · 2026-07-16T09:08:15Z · https://github.com/ArtemKasianov/ICML3/issues/1

Hello,

I encountered an issue where ICML3 crashes with the following error:
```bash
free(): invalid pointer
```
Could variable lengths of gene identifiers within the input data potentially lead to this type of error?
In my case, the input contained gene IDs with highly different lengths. After replacing the original identifiers with uniform identifiers (e.g., gene_000001, gene_000002), the analysis completed successfully.
I would like to clarify whether differences in gene ID length or format can affect memory handling in ICML3 and potentially result in this error.

Thank you!
