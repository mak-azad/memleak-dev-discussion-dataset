# [txiki/process.c] ASan heap-use-after-free when tjs.spawn fails to start executable

- URL: https://github.com/saghul/txiki.js/issues/1095
- Repo: saghul/txiki.js (language: C)
- State: open; created 2026-09-28T14:05:27Z; status ok; passes offcwe

## Issue body

reporter (NONE) · xmzyshypnc · 2026-09-28T14:05:27Z · https://github.com/saghul/txiki.js/issues/1095

## Summary

Calling `tjs.spawn()` with a nonexistent executable frees the native process
wrapper immediately after `uv_spawn()` fails, while libuv still retains the
process handle in its closing queue. Runtime teardown then writes through the
freed handle and ASan reports a heap-use-after-free.

**Severity**: ASan memory-safety finding; the ordinary Release build currently
returns the expected `ENOENT` error rather than visibly crashing.
**Component**: txiki.js `src/mod_process.c` / libuv process teardown
**Version**: master commit `8f1425764108`

## Reproducer

```js
tjs.spawn(["/definitely/not/a/real/executable"]);
```

Run with an ASan-enabled txiki.js binary using the ordinary entrypoint:

```sh
env ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:abort_on_error=1:symbolize=1 \
  tjs run poc.js
```

The ASan build failed on all 10 replay attempts. Eight attempts printed the
same UAF report and two terminated with SIGSEGV before ASan printed a report.
The Release build returned `Error: ENOENT: no such file or directory` with
status 1 on all 10 attempts.

## Sanitizer output

```text
ERROR: AddressSanitizer: heap-use-after-free
WRITE of size 8
    #0 uv__queue_remove       deps/libuv/src/queue.h:87
    #1 uv__finish_close       deps/libuv/src/unix/core.c:360
    #2 uv__run_closing_handles deps/libuv/src/unix/core.c:377
    #3 uv_run                  deps/libuv/src/unix/core.c:475
    #4 TJS_FreeRuntime         src/vm.c:711

freed by thread T0 here:
    #1 tjs_spawn               src/mod_process.c:419

previously allocated by thread T0 here:
    #1 tjs_spawn               src/mod_process.c:159
```

## Root Cause

The failed `uv_spawn()` path reaches:

```c
fail:
    tjs__free(p);
    JS_FreeValue(ctx, obj);
```

`p->process.data` was already set to the `TJSProcess` allocation. Freeing `p`
before libuv has finished closing the process handle leaves libuv's closing
queue pointing into freed memory. `TJS_FreeRuntime()` later runs the loop and
`uv__finish_close()` removes the dangling handle.

The failed-spawn path must complete or cancel the libuv handle lifecycle before
releasing `TJSProcess`, or avoid registering a closeable handle when spawning
fails before initialization.

## Suggested Fix

Make the failed-spawn cleanup follow libuv's handle lifetime rules. The owner
must remain allocated until the process handle's close callback has completed,
or the path must prove that no libuv handle was registered before freeing the
owner.

## Impact

The one-line JavaScript input reaches a native heap-use-after-free during
normal runtime teardown. The Release manifestation is currently latent: it
returns the normal `ENOENT` exception, but the same execution under ASan
performs an invalid write through freed libuv queue storage.

## Credit

xmzyshypnc([@xmzyshypnc](https://github.com/xmzyshypnc)) and Yanjie Zhao([@carol233](https://github.com/carol233)) and Yiyang Liu([@lyyffee](https://github.com/lyyffee))
