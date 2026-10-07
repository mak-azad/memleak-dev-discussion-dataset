# [security] GPAC MP4Box: concurrency heap-use-after-free in gf_fq_pop

- URL: https://github.com/gpac/gpac/issues/3874
- Repo: gpac/gpac (language: C)
- State: open; created 2026-08-21T02:46:28Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ZIllR0 · 2026-08-21T02:46:28Z · https://github.com/gpac/gpac/issues/3874

## 1. Summary

When `MP4Box -add` ingests a truncated AV1 elementary stream, the av1dmx demuxer hits a stream-failure path and calls `gf_filter_pid_drop_packet` (filter_pid.c:7316), which pops from the pid instance's lock-free queue via `gf_fq_pop` (filter_queue.c:254). In the same lock-free scheduler session, a pid-instance deletion task (`gf_filter_pid_inst_delete_task`, filter_pid.c:452) may run concurrently and free that queue object (`gf_filter_pid_inst_del` → free of the `gf_fq` allocated by `gf_fq_new`). The demuxer thread then reads the freed queue node → **heap-use-after-free**.




## 2. How to reproduce

### 2.1 Get the source / build

Same as the companion report:

```bash
git clone https://github.com/gpac/gpac.git && cd gpac   # commit 2fd5a06 (2026-08-20)
./configure --enable-sanitizer && make -j$(nproc)       # binary: bin/gcc/MP4Box
```

### 2.2 PoC input

The PoC is a truncated AV1 elementary stream, attached as [PoC.zip](https://github.com/user-attachments/files/31288202/PoC.zip) and unzip it to obtain `id009` (sha256: `f595eb3696914afe279f83e874b76db82ceccd662cc92e6a89a337f0594e22c7`; a
truncated AV1 bitstream; the demuxer fails mid-stream and enters the drop-packet path).

### 2.3 Run the reproducer

```bash
export ASAN_OPTIONS='detect_leaks=0:abort_on_error=1:symbolize=1'
setarch -R ./bin/gcc/MP4Box -threads 8 -noprog -add id009:dopt: -new /tmp/out.mp4
# repeat until crash (typically within 10-20 invocations)
```

Note: `setarch -R` disables ASLR (Linux); omit on macOS. `-threads 8` is significant — the 8+ scheduler threads exercise the teardown race.

## 3. ASAN report (full, current master, mainstream build)

```
==49120==ERROR: AddressSanitizer: heap-use-after-free on address 0x606000006050 at pc 0x7ffff445b400 bp 0x7fffea907a20 sp 0x7fffea907a10
READ of size 1 at 0x606000006050 thread T6
    #0 0x7ffff445b3ff in gf_fq_pop filter_core/filter_queue.c:254
    #1 0x7ffff440ddd6 in gf_filter_pid_drop_packet filter_core/filter_pid.c:7316
    #2 0x7ffff499c0c0 in av1dmx_process filters/reframe_av1.c:1514
    #3 0x7ffff44b9ca6 in gf_filter_process_task filter_core/filter.c:3257
    #4 0x7ffff448010f in gf_fs_thread_proc filter_core/filter_session.c:2420
    #5 0x7ffff34c8723 in RunThread utils/os_thread.c:234
    #6 0x7ffff0ed6ac2 in start_thread nptl/pthread_create.c:442
    #7 0x7ffff0f6884f  (/lib/x86_64-linux-gnu/libc.so.6+0x12684f)
freed by thread T8 here:
    #0 0x7ffff7676537 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x7ffff43e3daa in gf_filter_pid_inst_del filter_core/filter_pid.c:71
    #2 0x7ffff4416ca0 in gf_filter_pid_inst_delete_task filter_core/filter_pid.c:452
    #3 0x7ffff448010f in gf_fs_thread_proc filter_core/filter_session.c:2420
    #4 0x7ffff34c8723 in RunThread utils/os_thread.c:234
    #5 0x7ffff0ed6ac2 in start_thread nptl/pthread_create.c:442
previously allocated by thread T2 here:
    #0 0x7ffff7676887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x7ffff445a0f7 in gf_fq_new filter_core/filter_queue.c:68
    #2 0x7ffff4416a12 in gf_filter_pid_inst_new filter_core/filter_pid.c:...
    #3 0x7ffff448010f in gf_fs_thread_proc filter_core/filter_session.c:2420

SUMMARY: AddressSanitizer: heap-use-after-free filter_core/filter_queue.c:254 in gf_fq_pop
==49120==ABORTING
```

## 4. Additional notes

- I noticed that upstream recently published commit 563859e5 ("utils: Avoid  mutex access after release", 2026-08-20). However, this bug still   triggers under that commit: re-tested with the attached PoC on master including 563859e5, the crash reproduces on the first invocation with the identical stack (heap-use-after-free in `gf_fq_pop`, filter_queue.c:254). That commit only modifies `gf_mx_v` (os_thread.c) and does not affect this pid-instance queue race.



## Comment 5840251906

other (NONE) · AetherAI3 · 2026-09-25T22:00:01Z · https://github.com/gpac/gpac/issues/3874#issuecomment-5840251906

## Proposed fix (R3 external-refcount) — UNVERIFIED, pending local ASAN

Analysis at pin `2fd5a06ab226767900fd86edb5a1e8bfc1010640` confirms the reporter's mechanism and points to a fix that also closes sibling issue #3867 (heap-UAF in `gf_mx_v` on `pidinst->pck_mx`).

**Root cause recap**

`gf_filter_pid_inst_delete_task` at `filter_pid.c:437-446` acquires `filter->tasks_mx` around the `pid->destinations` update, then **releases at :446 before** calling `gf_filter_pid_inst_del(pidinst)` at `:452`. Inside `gf_filter_pid_inst_del`, `gf_fq_del(pidinst->packets)` at `:71` frees the queue and `gf_mx_del(pidinst->pck_mx)` at `:72` frees its mutex. Meanwhile a concurrent `gf_filter_pid_drop_packet` reaches `gf_fq_pop`, and `filter_queue.c:252` reads `fq->use_mx` **before** any lock is taken — dangling on the freed queue. Matches the reporter's ASAN echo exactly.

**Why simple "widen `tasks_mx`" (R1) fails**

Holding `filter->tasks_mx` across the full `gf_filter_pid_inst_del` call deadlocks: `gf_filter_pid_inst_del` re-acquires the **same** mutex at `:78` (via `pidinst->pid->filter->tasks_mx`, which equals `filter->tasks_mx` since `filter = pid->filter` at `:411`) for the props ref decrement. Non-recursive → self-deadlock.

**Why "queue-external lock" (R2) is incomplete**

`pidinst->pck_mx` is also called by `gf_fq_head`, `gf_fq_add`, `gf_fq_count` on the same queue. Locking only `gf_fq_pop` leaves #3867 open.

**R3 — external refcount, piggybacking existing `tasks_mx`**

Add `volatile u32 refcount` + `Bool pending_delete` to `GF_FilterPidInst`. Readers (`gf_filter_pid_drop_packet`, `_get_packet`, `_get_first_packet`, `_peek_packet`, `gf_fq_count` callers) acquire `pid->filter->tasks_mx`, check `pending_delete`, `safe_int_inc(refcount)`, release, do their work, `safe_int_dec(refcount)`. The delete task piggybacks its existing critical section at `:437-446`: sets `pending_delete = GF_TRUE`, checks `refcount == 0` **while still holding tasks_mx**; if nonzero, `TASK_REQUEUE` and return; if zero, release and proceed to `gf_filter_pid_inst_del` as today.

Reuses the mutex `gf_filter_pid_drop_packet` already acquires later in the same function at `~:7351` for state accounting ("make sure we lock the tasks mutex before getting the packet count…") — no new lock introduced. Avoids R1's deadlock because the widened hold only covers the check + refcount bump, not the whole `gf_fq_pop`. Closes #3867 as free-side collateral: `pidinst->pck_mx` is inside `pidinst` and cannot be freed while `refcount > 0`.

**Gates before I open a PR**

1. Confirm `filter->tasks_mx` is non-recursive (`gf_mx_new(..., GF_FALSE)` or `PTHREAD_MUTEX_NORMAL`).
2. Full reader audit — every consumer of `pidinst->packets` / `pidinst->pck_mx` in the tree gets the guard.
3. Apply patch, `./configure --enable-sanitizer && make -j$(nproc)`, run the reporter's PoC 30+ iterations under `ASAN_OPTIONS='detect_leaks=0:abort_on_error=1:symbolize=1'` + `setarch -R`; zero UAF reports.
4. Reproduce #3867 on the patched build; confirm the `gf_mx_v` UAF also stops.

I'll open the PR once the four gates clear locally. Full analysis chain (constraint set, witness ordering, adversarial review) is banked and available on request.

## Comment 5840450912

other (NONE) · AetherAI3 · 2026-09-25T22:20:20Z · https://github.com/gpac/gpac/issues/3874#issuecomment-5840450912

## Correction: fix requires two ordered patches, not just R3

Deeper analysis on the pinned corpus at `2fd5a06` surfaces a second UAF that R3 (my earlier comment) implicitly assumes is already fixed.

**The second bug (F2)** — `gf_fs_thread_proc` at `filter_session.c:2408` dereferences `task->filter->name` (and `->process_task_queued`, `->tasks`) with **no lock held and no `filter->finalized` check**. `gf_filter_post_remove` (posted at `filter_pid.c:516`) schedules a deferred filter free; between that post and the free, an in-flight task can reach `:2408` and read a dangling `GF_Filter`. The session-level `tasks_in_process` counter is additive-only — it doesn't gate teardown.

**Why R3 alone is incomplete** — R3's guard at `gf_filter_pid_drop_packet:7302/:7310` reads `pid->filter->tasks_mx` to acquire the mutex. That's on the same `GF_FilterPid`/`GF_Filter` chain F2 says can be freed. R3's own mutex-acquire can UAF if the parent filter is being torn down concurrently.

**Proposed order — two patches:**

1. **F2 first** — add refcount + `pending_delete` to `GF_Filter`, gated by a session-level lock (`session->filters_mx` or `session->tasks_mx`) that covers **all** `gf_fs_post_task` sites, completion paths, and `gf_filter_del`. Combined with a session-drain that rejects new task posts once `pending_delete` is set (handles the reentrant `gf_filter_pid_send_event` pattern that would otherwise deadlock a naive drain). The correctness signal cannot live only inside `GF_Filter` because that storage dies with the filter; the outer lock is what makes it survive.
2. **R3 on top** — pidinst external refcount as previously described. Still required after F2 because `gf_filter_pid_inst_swap_delete` destroys pidinst independently of filter teardown.

**Ruled out during review:** a pure `filter->finalized` dispatch-side check — probabilistic (no memory barrier) and the flag's storage is itself UAF-prone.

**Gates I want to clear locally before opening the PR:**

1. Confirm the exact `GF_Filter` free site (likely `gf_filter_del`) and its line, and verify no existing quiescence/barrier already serializes it against dispatch.
2. Grep every `gf_fs_post_task` caller and every task completion path; each must hold the session lock across refcount ops.
3. Full ASAN repro under threaded stress (dynamic filter removal while a demux is active) — 30+ iterations, zero UAF.
4. Verify R3's `pid->filter->tasks_mx` acquire lands under the same lock introduced by F2, so R3's own guard doesn't UAF.
5. Repro #3867's PoC on the patched build; confirm `gf_mx_v` UAF also stops.

Full analysis chain (constraint sets, witness orderings, adversarial repair reviews, orthogonal-hunt residuals) is banked and available on request.
