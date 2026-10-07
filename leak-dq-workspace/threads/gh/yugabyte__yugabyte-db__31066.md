# [YSQL] Add memory context cleanup to prevent memory leak

- URL: https://github.com/yugabyte/yugabyte-db/issues/31066
- Repo: yugabyte/yugabyte-db (language: C)
- State: open; created 2026-04-13T16:31:08Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · GauravSingh-yb · 2026-04-13T16:31:08Z · https://github.com/yugabyte/yugabyte-db/issues/31066

Jira Link: [DB-20951](https://yugabyte.atlassian.net/browse/DB-20951)
### Description

### Summary

`getYsqlStatementStats` in `pg_stat_statements.c` implements the YSQL /statements HTTP export by loading query text with `qtext_load_file()` and iterating pgss_hash while holding `pgss->lock`. Transient allocations (qbuffer, StringInfo in `yb_add_hist_json`, and any future work in this path) are tied to `CurrentMemoryContext`. We should bound that work in a dedicated short-lived memory context and tear it down on all exit paths (including ERROR), to avoid leaks and to match PostgreSQL conventions for this kind of helper.

### Problem

- **Context ambiguity**: Allocations use whatever `CurrentMemoryContext` is when the web handler runs. If that context is long-lived, any allocation that is not explicitly freed can persist much longer than the request.
- **Error / longjmp:** A future ereport(ERROR)-style exit from this path could skip explicit cleanup unless guarded (e.g. `PG_TRY` / `PG_FINALLY`) and would also risk leaving `pgss->lock` held and hash-seq state inconsistent unless handled carefully.


### Issue Type

kind/bug

### Warning: Please confirm that this issue does not contain any sensitive information

- [x] I confirm this issue does not contain any sensitive information.

[DB-20951]: https://yugabyte.atlassian.net/browse/DB-20951?atlOrigin=eyJpIjoiNWRkNTljNzYxNjVmNDY3MDlhMDU5Y2ZhYzA5YTRkZjUiLCJwIjoiZ2l0aHViLWNvbS1KU1cifQ
