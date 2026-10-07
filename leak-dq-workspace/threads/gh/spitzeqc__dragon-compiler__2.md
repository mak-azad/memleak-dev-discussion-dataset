# Semantic test "test-semantic.q" core dump

- URL: https://github.com/spitzeqc/dragon-compiler/issues/2
- Repo: spitzeqc/dragon-compiler (language: C)
- State: open; created 2023-05-16T16:46:18Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · spitzeqc · 2023-05-16T16:46:18Z · https://github.com/spitzeqc/dragon-compiler/issues/2

When calling `boo( a * b + d[y + z] )` in "test-semantic.q", a memory related issue occurs:
```
malloc(): corrupted top size
Aborted (core dumped)
```
