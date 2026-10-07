# Week5 Lab 18 - Cleanup Double Free (18_cleanup_double_free/bug.c)

- URL: https://github.com/molru-1/Week5/issues/19
- Repo: molru-1/Week5 (language: C)
- State: open; created 2026-10-01T08:23:32Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · molru-1 · 2026-10-01T08:23:32Z · https://github.com/molru-1/Week5/issues/19

Week5 Lab 18 - Cleanup Double Free

Code path: memory-debugging-lab/challenges/18_cleanup_double_free/bug.c
Bug type: Cleanup double free

Reproduction:
1) Build and run; multiple deletes of same memory

Expected:
Only one free per allocation

Notes:
GDB or printf tracing recommended.

