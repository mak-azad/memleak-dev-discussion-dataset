# imhttp: realloc(pReadBuf) overwrites pointer — original buffer leaked on OOM

- URL: https://github.com/Canotas/rsyslog/issues/65
- Repo: Canotas/rsyslog (language: None)
- State: open; created 2026-03-19T16:41:34Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · bd0c · 2026-03-19T16:41:34Z · https://github.com/Canotas/rsyslog/issues/65

## Module: imhttp (contrib/imhttp/imhttp.c)

## Description
In `postHandler()`, when the incoming Content-Length exceeds the current read buffer, the code calls `realloc()` and assigns the result directly back to `connWrkr->pReadBuf`. If `realloc()` returns NULL (OOM), the original buffer pointer is overwritten with NULL — the original allocation is lost (leaked) and cannot be freed later.

## Root Cause
```c
// line 909
connWrkr->pReadBuf = realloc(connWrkr->pReadBuf, ri->content_length+1);
if (!connWrkr->pReadBuf) {
    // original pReadBuf is now gone — memory leaked
    FINALIZE;
}
```

## Impact
**HIGH** — Memory leak per failed request under memory pressure. After this, `connWrkr->pReadBuf` is NULL but `readBufSize` is stale, leading to inconsistent state on subsequent requests.

## Fix
```c
void *newBuf = realloc(connWrkr->pReadBuf, ri->content_length+1);
if (!newBuf) {
    mg_cry(conn, "%s() - realloc failed!\n", __FUNCTION__);
    rc = 500;
    FINALIZE;
}
connWrkr->pReadBuf = newBuf;
connWrkr->readBufSize = ri->content_length+1;
```

## Affected File
`contrib/imhttp/imhttp.c` — `postHandler()` line ~909
