# free(): invalid pointer

- URL: https://github.com/RRZE-HPC/WINIC/issues/4
- Repo: RRZE-HPC/WINIC (language: C++)
- State: open; created 2025-08-23T10:09:12Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · TobiasRTR · 2025-08-23T10:09:12Z · https://github.com/RRZE-HPC/WINIC/issues/4

On x86 the STD instruction (Opcode 4692) causes `free(): invalid pointer` to be printed.
This is because STD changes the order of string operations, so after measuring it, the next string operation causes heap corruption.
STD is an example why i chose to wrap every benchmark in its own subprocess, as even if segfaults and other signals are handled, instructions can have side effects that cannot be mitigated and cause crashes.
It still would be nice to hide this from the user and prevent the error message to be printed.
