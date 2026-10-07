# (CXX-W2049) Use of `realloc` without aliasing can lead to memory leaks

- URL: https://github.com/pousoupou/parCer/issues/2
- Repo: pousoupou/parCer (language: C)
- State: open; created 2024-08-10T19:17:20Z; status ok; passes main

## Issue body

reporter (OWNER) · pousoupou · 2024-08-10T19:17:20Z · https://github.com/pousoupou/parCer/issues/2

## Description
Found realloc assignment to the same expression as passed to the first argument. The return value of `realloc` is assigned to the same expression as passed to the first argument. The problem with this construct is that if `realloc` fails, it returns a null pointer but does not deallocate the original memory. **Probably resulting in the seg fault.**

## Occurrences
There is 1 occurrence of this issue in the repository.

See all occurrences on DeepSource &rarr; [app.deepsource.com/gh/pousoupou/parCer/issue/CXX-W2049/occurrences/](https://app.deepsource.com/gh/pousoupou/parCer/issue/CXX-W2049/occurrences/)

