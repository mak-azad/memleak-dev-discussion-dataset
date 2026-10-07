# Week5 Lab 04 - Double Free (04_double_free/bug.c)

- URL: https://github.com/molru-1/Week5/issues/2
- Repo: molru-1/Week5 (language: C)
- State: closed; created 2026-10-01T08:23:32Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · molru-1 · 2026-10-01T08:23:32Z · https://github.com/molru-1/Week5/issues/2

Week5 Lab 04 - Double Free

Code path: memory-debugging-lab/challenges/04_double_free/bug.c
Bug type: Double Free

Reproduction:
1) Build according to README
2) Run the program and trigger double free

Expected:
Program should not free the same memory twice; detect and prevent double free.

Notes:
Use gdb to trace allocations/frees, or print statements to verify.

