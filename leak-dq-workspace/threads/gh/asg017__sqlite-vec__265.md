# [Bug]: Multiple memory leaks in vec0 operations (INSERT, DELETE, error paths)

- URL: https://github.com/asg017/sqlite-vec/issues/265
- Repo: asg017/sqlite-vec (language: C)
- State: open; created 2026-02-18T02:23:27Z; status ok; passes main

## Issue body

reporter (NONE) · murillodutt · 2026-02-18T02:23:27Z · https://github.com/asg017/sqlite-vec/issues/265

## Description

PR #258 identifies 7 memory leaks in `sqlite-vec.c` that have not been merged. These leaks occur in INSERT operations, DELETE operations, and error handling paths within vec0 virtual tables.

Since PR #258 has been open without review, I'm filing this as a bug to increase visibility.

## Identified Leaks (from PR #258)

The leaks are in various code paths in `sqlite-vec.c`:

1. **INSERT path** — allocated buffers not freed on early return/error
2. **DELETE path** — chunk data not freed after processing
3. **Error handling** — several error branches skip cleanup of allocated memory
4. **Query result construction** — intermediate buffers leaked in edge cases

## Impact

- Long-running applications that perform many INSERT/DELETE/query operations will see growing memory usage
- Production systems with high-throughput vector operations (e.g., embedding pipelines processing thousands of documents) are most affected
- Memory is not reclaimed until the database connection is closed

## Environment

- sqlite-vec: 0.1.7-alpha.2 and 0.1.7-alpha.10 (PR #258 not merged in either)
- Observed on: macOS ARM64, Linux x64

## Reference

PR #258 contains the specific fixes for all 7 leak sites.

Reported by Murillo Dutt
