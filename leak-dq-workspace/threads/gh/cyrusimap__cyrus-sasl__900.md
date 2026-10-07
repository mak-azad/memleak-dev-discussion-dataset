# Memory leak in sasl_server_new() and sasl_client_new() on error paths (missing destroy_conn call)

- URL: https://github.com/cyrusimap/cyrus-sasl/issues/900
- Repo: cyrusimap/cyrus-sasl (language: C)
- State: open; created 2026-10-04T10:30:31Z; status ok; passes main

## Issue body

reporter (NONE) · nguyentruong190 · 2026-10-04T10:30:31Z · https://github.com/cyrusimap/cyrus-sasl/issues/900

### Summary

In `sasl_server_new()` (`lib/server.c`) and `sasl_client_new()` (`lib/client.c`), the connection context (`*pconn`) and its connection parameters (`sparams` / `cparams`) are allocated up front. However, when an error occurs during initialization, the cleanup paths bypass `(*pconn)->destroy_conn(*pconn)`, leading to memory leaks on every failed call.

### Root Cause Analysis

#### 1. Server side (`lib/server.c:1047-1188`)
In `sasl_server_new()`:
```c
1042   *pconn = sasl_ALLOC(sizeof(sasl_server_conn_t));
...
1047   serverconn->sparams = sasl_ALLOC(sizeof(sasl_server_params_t));   /* 232 bytes */
...
1053   (*pconn)->destroy_conn = &server_dispose;
1054   result = _sasl_conn_init(*pconn, service, flags, SASL_CONN_SERVER, ...);
1059   if (result != SASL_OK)
           goto done_error;
```
When an error occurs (such as invalid arguments, `_sasl_alloc_utils` failure, or `_sasl_conn_init` failure), control jumps to `done_error`:
```c
1182  done_error:
1183    _sasl_conn_dispose(*pconn);
1184    sasl_FREE(*pconn);
1185    *pconn = NULL;
1186    return result;
```
`_sasl_conn_dispose()` (`lib/common.c:922`) only cleans up the base connection buffers (`service`, `serverFQDN`, `error_buf`, etc.). It does **not** free `sparams`. The parameters block is only freed in `server_dispose()` (`lib/server.c:51`):
```c
static void server_dispose(sasl_conn_t *pconn)
{
    ...
    if (s_conn->sparams) sasl_FREE(s_conn->sparams);
    _sasl_conn_dispose(pconn);
}
```
Because `done_error` directly calls `_sasl_conn_dispose()` instead of `(*pconn)->destroy_conn()`, `sparams` is leaked on every failure after line 1047 (exactly 232 bytes per failed call).

#### 2. Client side (`lib/client.c:446-549`)
In `sasl_client_new()`:
- **Premature return without cleanup (line 455):**
  ```c
  result = _sasl_conn_init(*pconn, service, flags, SASL_CONN_CLIENT, ...);
  if (result != SASL_OK) RETURN_VAL(*pconn, result);
  ```
  If `_sasl_conn_init()` returns an error, `RETURN_VAL` returns immediately without freeing `*pconn` or `conn->cparams`.
- **Error tail skips `client_dispose` (lines 542-549):**
  ```c
  failed_client_new:
    _sasl_conn_dispose(*pconn);
    sasl_FREE(*pconn);
    *pconn = NULL;
    return result;
  ```
  `cparams` (and any per-connection `mech_list` allocated at line 493) is only freed inside `client_dispose()` (lines 363-382). Skipping `destroy_conn` leaks `cparams` and `conn->mech_list`.

---

### Minimal Reproduction (Server side)

Calling `sasl_server_new` with a colon-formatted peer address (expecting semicolon format `host;port`):
```c
sasl_conn_t *conn = NULL;
int rc = sasl_server_new("imap", "localhost", NULL, NULL, "192.0.2.2:52341", NULL, 0, &conn);
/* rc = -7 (SASL_BADPARAM), conn = NULL */
```

AddressSanitizer output:
```
Direct leak of 232 byte(s) in 1 object(s) allocated from:
    #1 sasl_server_new lib/server.c:1047:23
SUMMARY: AddressSanitizer: 232 byte(s) leaked in 1 allocation(s).
```

Running $N$ failing calls leaks exactly $232 \times N$ bytes.

---

### Proposed Fix

#### `lib/server.c`:
```diff
--- a/lib/server.c
+++ b/lib/server.c
@@ -1182,7 +1182,10 @@ int sasl_server_new(const char *service,
  done_error:
-  _sasl_conn_dispose(*pconn);
+  if ((*pconn)->destroy_conn)
+      (*pconn)->destroy_conn(*pconn);
+  else
+      _sasl_conn_dispose(*pconn);
   sasl_FREE(*pconn);
   *pconn = NULL;
   return result;
```

#### `lib/client.c`:
```diff
--- a/lib/client.c
+++ b/lib/client.c
@@ -455,1 +455,1 @@ int sasl_client_new(const char *service,
-  if (result != SASL_OK) RETURN_VAL(*pconn, result);
+  if (result != SASL_OK) goto failed_client_new;
@@ -543,7 +543,10 @@ int sasl_client_new(const char *service,
  failed_client_new:
-  _sasl_conn_dispose(*pconn);
+  if ((*pconn)->destroy_conn)
+      (*pconn)->destroy_conn(*pconn);
+  else
+      _sasl_conn_dispose(*pconn);
   sasl_FREE(*pconn);
   *pconn = NULL;
   return result;
```

*(Note: `server_dispose` and `client_dispose` both call `_sasl_conn_dispose()` internally, so using `else` ensures clean disposal without double-free).*

I have verified the fix locally with ASan and existing regression tests. If this looks good to maintainers, I can submit a PR with this change.

