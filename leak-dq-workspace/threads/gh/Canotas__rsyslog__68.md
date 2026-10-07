# imhttp: pworkbuf memory leaked on error path in basicAuthHandler()

- URL: https://github.com/Canotas/rsyslog/issues/68
- Repo: Canotas/rsyslog (language: None)
- State: open; created 2026-03-19T16:41:53Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · bd0c · 2026-03-19T16:41:53Z · https://github.com/Canotas/rsyslog/issues/68

## Module: imhttp (contrib/imhttp/imhttp.c)

## Description
In `parse_auth_header()`, when the decoded auth header exceeds the static work buffer, a heap buffer is allocated and stored in `auth->pworkbuf`. In `basicAuthHandler()`, if `parse_auth_header()` succeeds but `read_auth_file()` fails or returns early, the dynamically allocated `auth->pworkbuf` is never freed.

## Root Cause
```c
// basicAuthHandler — no cleanup of auth.pworkbuf on any exit path
struct auth_s auth = { .workbuf_len=0, .pworkbuf=NULL, ... };
if (!parse_auth_header(conn, &auth)) { return 0; }  // pworkbuf may be allocated
return read_auth_file(filep, &auth);  // pworkbuf never freed
```

## Impact
**MEDIUM** — Memory leak per authenticated request when the auth header is larger than the static buffer. Leads to slow OOM under high traffic.

## Fix
```c
finalize:
    if (auth.workbuf_len > 0 && auth.pworkbuf != auth.workbuf) {
        free(auth.pworkbuf);
    }
```

## Affected File
`contrib/imhttp/imhttp.c` — `basicAuthHandler()` line ~818-856
