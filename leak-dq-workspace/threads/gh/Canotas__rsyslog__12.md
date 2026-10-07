# [omsentinel][CRITICAL] free() on string literals: scope, grant_type, auth_domain crash on shutdown

- URL: https://github.com/Canotas/rsyslog/issues/12
- Repo: Canotas/rsyslog (language: None)
- State: open; created 2026-03-19T14:36:55Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · bd0c · 2026-03-19T14:36:55Z · https://github.com/Canotas/rsyslog/issues/12

## Description

In `setInstParamDefaults()`, three fields are initialized with string literals. `freeInstance()` calls `free()` on all three unconditionally, even when the user has not provided them in the config. Freeing a string literal is undefined behaviour — in practice a crash or heap corruption.

## Affected locations

**File:** `plugins/omsentinel/omsentinel.c`

`setInstParamDefaults()` (lines ~1643-1645):
```c
pData->scope      = (uchar*)"https://monitor.azure.com/.default"; // string literal
pData->grant_type = (uchar*)"client_credentials";                 // string literal
pData->auth_domain= (uchar*)"login.microsoftonline.com";          // string literal
```

`freeInstance()` (lines ~363-366):
```c
free(pData->scope);       // UB if user didn't set 'scope'
free(pData->grant_type);  // UB if user didn't set 'grant_type'
free(pData->auth_domain); // UB if user didn't set 'auth_domain'
```

All three parameters are **optional** in the config descriptor. A typical deployment omitting them will crash on module unload or rsyslog restart.

## Impact

Undefined behaviour (likely SIGSEGV or heap corruption) during shutdown or config reload whenever any of these three optional parameters is omitted from the config.

## Fix

Replace the literal assignments in `setInstParamDefaults` with `strdup()`:
```c
pData->scope       = (uchar*)strdup("https://monitor.azure.com/.default");
pData->grant_type  = (uchar*)strdup("client_credentials");
pData->auth_domain = (uchar*)strdup("login.microsoftonline.com");
```

## Comment 4091172222

reporter (COLLABORATOR) · bd0c · 2026-03-19T15:49:49Z · https://github.com/Canotas/rsyslog/issues/12#issuecomment-4091172222

Pull Request associée : #31
