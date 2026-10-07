# [daily-ci] REAL-DEFECT: uninitialised client.cur_tid read in tryOffloadFreeArgvToIOThreads (io_threads.c:937)

- URL: https://github.com/madolson/valkey-agents/issues/29
- Repo: madolson/valkey-agents (language: C)
- State: open; created 2026-09-16T03:47:40Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · madolson · 2026-09-16T03:47:40Z · https://github.com/madolson/valkey-agents/issues/29

`client.cur_tid` is never initialised when a client is created, but `tryOffloadFreeArgvToIOThreads` reads it on every argv free. `createClient` uses `zmalloc` with no `memset` (`src/networking.c:330`), and the only writer of `cur_tid` in the whole tree is `src/networking.c:7203`, which runs only after a read has actually been served on an IO thread. Any client whose read is handled inline on the main thread therefore reaches `src/io_threads.c:936` with a garbage `cur_tid`, and the branch at `src/io_threads.c:937` reads it. The range check on the next line keeps the index in bounds, so the practical damage is a garbage-driven choice of IO thread rather than a crash, but it is genuine UB and it fails both valgrind Daily jobs.

<details>
<summary>Details</summary>

## Job links

Run 35039408935, seen 4 times across both valgrind jobs:

- `test-valgrind-no-malloc-usable-size-test (integration-type)`: https://github.com/valkey-io/valkey/actions/runs/35039408935/job/104615693902
- `test-valgrind-test (integration-type)`: https://github.com/valkey-io/valkey/actions/runs/35039408935/job/104615693991

## Valgrind output

```
==90464== Conditional jump or move depends on uninitialised value(s)
==90464==    at 0x23586F: tryOffloadFreeArgvToIOThreads (io_threads.c:937)
==90464==    by 0x27186E: freeClientArgv (networking.c:2168)
==90464==    by 0x276512: resetClient (networking.c:3787)
==90464==    by 0x277BB8: commandProcessed (networking.c:4311)
==90464==    by 0x277D54: processCommandAndResetClient (networking.c:4357)
==90464==    by 0x278C4F: processInputBuffer (networking.c:4685)
==90464==    by 0x279391: readQueryFromClient (networking.c:4839)
==90464==    by 0x2F0050: callHandler (connhelpers.h:79)
==90464==    by 0x2F0914: connSocketEventHandler (socket.c:318)
==90464==    by 0x1A274B: aeFireFileEvent (ae.c:480)
==90464==    by 0x1A2917: aeProcessQoSEvents (ae.c:516)
==90464==    by 0x1A2A25: aeProcessQoSEventsPreemptively (ae.c:542)
==90464==  Uninitialised value was created by a heap allocation
```

The stack is the main-thread event loop, not an IO thread. That is the point: this client's read was served inline, so `cur_tid` was never written.

## Citations

Analysis at `d6415e766`.

- `src/server.h:1449` declares the field: `uint8_t cur_tid;  /* ID of IO thread currently performing IO for this client */`
- `src/networking.c:330` allocates the client: `client *c = zmalloc(sizeof(client));`. Not `zcalloc`. Grepping the body of `createClient` for `memset` or `cur_tid` returns zero hits. The neighbouring `io_read_state` and `io_write_state` are explicitly initialised at `src/networking.c:409-410`; `cur_tid` is not.
- `src/networking.c:7203` is the only write, inside `ioThreadReadQueryFromClient`: `c->cur_tid = getCurTid();`
- `src/io_threads.c:936-939` is the read:

```c
    int target_id = c->cur_tid;
    if (target_id < 1 || target_id >= server.active_io_threads_num) {
        target_id = (c->id % (server.active_io_threads_num - 1)) + 1;
    }
```

- `src/networking.c:2168` is the caller: `if (c->original_argv || tryOffloadFreeArgvToIOThreads(c, c->argc, c->argv) == C_ERR)`
- "Uninitialised value was created by a heap allocation" matches `zmalloc(sizeof(client))` at `src/networking.c:330`.

Full grep of every `cur_tid` reference in `src/`:

```
src/io_threads.c:936:    int target_id = c->cur_tid;
src/networking.c:7203:    c->cur_tid = getCurTid();
src/server.h:1449:    uint8_t cur_tid;
```

## Introduced by

`a3a839972`, "Redesign IO threading communication model (#3324)", 2026-04-13.

Before #3324 the main thread wrote `cur_tid` itself immediately before every offload, so it was always defined before any read. That commit deleted both of those writes. From its diff:

```
-    if (c->io_write_state == CLIENT_PENDING_IO && c->cur_tid != (uint8_t)tid) tid = c->cur_tid;
-    IOJobQueue *jq = &io_jobs[tid];
-    if (IOJobQueue_isFull(jq)) return C_ERR;
-    c->cur_tid = tid;
```

```
-    if (c->io_read_state == CLIENT_PENDING_IO && c->cur_tid != (uint8_t)tid) tid = c->cur_tid;
-    c->cur_tid = tid;
```

The single surviving write was moved into the IO thread (`+ c->cur_tid = getCurTid();`, now `src/networking.c:7203`), and in the same commit `tryOffloadFreeArgvToIOThreads` was changed from computing the target purely from `c->id` to reading the field:

```
-    size_t tid = (c->id % (server.active_io_threads_num - 1)) + 1;
+    int target_id = c->cur_tid;
+    if (target_id < 1 || target_id >= server.active_io_threads_num) {
+        target_id = (c->id % (server.active_io_threads_num - 1)) + 1;
+    }
```

So the commit started reading a field whose only initialiser it removed.

## Severity

Real defect, low impact. Reading an uninitialised `uint8_t` is UB and must be fixed, but the blast radius is contained:

- The range check at `src/io_threads.c:937` bounds `target_id` to `[1, active_io_threads_num)`. Garbage outside that window falls back to the `c->id`-derived assignment, which is exactly the pre-#3324 behaviour. No out-of-bounds index into `io_private_inbox`.
- Garbage inside the window picks a live IO thread. The argv objects are exclusively owned at that point, so whichever thread runs `ioThreadFreeArgv` (`src/io_threads.c:904`) frees them correctly. Wrong thread, right result.
- The deferred commit is also safe. `spscEnqueue(..., false)` at `src/io_threads.c:974` depends on `commitIOJobs` (`src/io_threads.c:90-94`), which commits every inbox `1 .. active_io_threads_num-1` unconditionally rather than tracking which ones received jobs, so an unexpected target inbox still gets committed.

Net user-visible effect: nondeterministic IO thread selection for argv frees, losing the cache locality the field exists to provide, plus UB that valgrind and MSan will flag. No crash, no leak, no data race identified. The concrete cost today is the two failing valgrind Daily jobs.

## Not a suppression candidate

`src/valgrind.sup` holds only `lzf_compress` cond and value entries, a `FishyValue` entry for `ztrymalloc`, and a `bio_job_in_flight_at_exit` leak entry. Nothing covers this, and it should not be suppressed. The alloc site is `createClient`, not a shutdown path.

## Why only 1 of 7 runs

Whether the uninitialised byte trips the branch depends on what recycled allocator memory happens to contain, so observation is load and history dependent. The defect itself is unconditional.

## Fix direction

Initialise `cur_tid` in `createClient` alongside the existing `io_read_state` and `io_write_state` initialisation at `src/networking.c:409-410`. `0` is the natural value: `getCurTid()` returns `0` for the main thread (`src/io_threads.c:86-88`), and `0` fails the `target_id < 1` check, yielding the `c->id`-derived fallback.

## Related upstream issue

None found. Searched `valkey-io/valkey` for `tryOffloadFreeArgvToIOThreads`, `cur_tid`, and `valgrind uninitialised io_threads`; no matches.

</details>

This was generated by AI but verified, with love, by a human.


## Comment 5779871031

other (CONTRIBUTOR) · akashkgit · 2026-09-22T16:10:34Z · https://github.com/madolson/valkey-agents/issues/29#issuecomment-5779871031

The proposed fix for unconditional jump looks good to me - will raise a PR along with the fix addressing valgrind failures due to definite memory leak bytes in `initSharedQueryBuf()` 
