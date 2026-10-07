# EXIT or a runtime error inside a called routine crashes: bad free in IRXBEXEC cleanup

- URL: https://github.com/mvslovers/rexx370/issues/262
- Repo: mvslovers/rexx370 (language: C)
- State: closed; created 2026-09-30T07:14:46Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · mgrossmann · 2026-09-30T07:14:46Z · https://github.com/mvslovers/rexx370/issues/262

A plain `EXIT` inside a routine reached by `CALL` or a function call aborts the process on the host. So does any runtime error raised inside such a routine.

```rexx
call f
say 'back'
exit
f:
exit 0
```

Host: SIGABRT (exit 134). AddressSanitizer:

```
attempting free on address which was not malloc()-ed
  #1 irxstor irx#stor.c:109
  #4 IRXBEXEC irx#bvm.c:3780
allocated by: IRXBEXEC irx#bvm.c:960 (call frame array)
```

Suspected mechanism: the VM cleanup frees `proxy_parser->call_args` as a separate allocation. With an active call frame, that pointer points into the call-frame block allocated at `irx#bvm.c:960`.

Second repro, a runtime error in a function: `v = f(1)` / `exit` / `f: return arg(1,'Exists')`. `'Exists'` is rejected (#280), and the error inside `f` takes the same path.

MVS behaviour is not measured. A wrong FREEMAIN is the likely outcome; that is inferred.

Suite: `ARGOPT` is listed but not run (`norun`) until this is fixed, because it takes the whole driver down.

Found by the SC28-1883-0 conformance suite (#261): expected values and page references in `docs/spec-tests/`, execs in `test/spec/`. Repros run on the host build (bytecode VM unless noted).


## Comment 5910045487

reporter (CONTRIBUTOR) · mgrossmann · 2026-09-30T11:15:15Z · https://github.com/mvslovers/rexx370/issues/262#issuecomment-5910045487

Resolved in PR #287. Also fixes the exec losing its own ARG() after the first CALL/RETURN (same cause). Verified on MVS batch + TSO (JOB01417).
