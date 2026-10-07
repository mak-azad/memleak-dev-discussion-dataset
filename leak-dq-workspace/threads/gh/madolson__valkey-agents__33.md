# [daily-ci] FLAKY-TEST: valgrind cluster jobs fail on a fork child's definite loss from the BIO cluster-config save

- URL: https://github.com/madolson/valkey-agents/issues/33
- Repo: madolson/valkey-agents (language: C)
- State: open; created 2026-09-16T03:50:32Z; status ok; passes main

## Issue body

reporter (OWNER) · madolson · 2026-09-16T03:50:32Z · https://github.com/madolson/valkey-agents/issues/33

The daily valgrind cluster jobs intermittently fail on a "60 bytes definitely lost" report through `clusterSaveConfigImpl` (`cluster_legacy.c:1128`), but the loss is reported by the diskless-replication **fork child**, not by valkey-server. The child does not have the BIO worker thread, so the `tmpfilename` sds that thread had live on its stack at fork time has no remaining reference and valgrind calls it definitely lost. The parent's own summary in the same run is `definitely lost: 0 bytes in 0 blocks`, and `clusterSaveConfigImpl` frees the string on every path. The test fails because `find_valgrind_errors` (`tests/support/util.tcl:622`) scans the whole stderr file with no PID scoping while the server runs under `--trace-children=yes` without `--child-silent-after-fork=yes` (`tests/support/server.tcl:351`).

<details>
<summary>Details</summary>

## Jobs

- `test-valgrind-test (cluster)` run 34792420918: https://github.com/valkey-io/valkey/actions/runs/34792420918/job/103819010936
- `test-valgrind-no-malloc-usable-size-test (cluster)` run 35039408935: https://github.com/valkey-io/valkey/actions/runs/35039408935/job/104615693926

Seen 6 times across 2 of the 7 consecutive failing Daily runs (2026-09-10 through 2026-09-16).

## The report, verbatim

Run 34792420918. Parent is 76027, reporting PID is 76089.

```
==76027== Command: /home/runner/work/valkey/valkey/src/valkey-server ./tests/tmp/valkey.conf.7323.1144
==76089== HEAP SUMMARY:
==76089==     in use at exit: 2,810,989 bytes in 14,625 blocks
==76089== 52 bytes in 1 blocks are definitely lost in loss record 1,158 of 1,492
==76089==    at 0x484DB80: realloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==76089==    by 0x342758: ztryrealloc_usable_internal (zmalloc.c:376)
==76089==    by 0x342802: ztryrealloc_usable (zmalloc.c:406)
==76089==    by 0x342919: zrealloc_usable (zmalloc.c:431)
==76089==    by 0x2B6D6E: _sdsMakeRoomFor (sds.c:280)
==76089==    by 0x2B6F79: sdsMakeRoomFor (sds.c:311)
==76089==    by 0x2B7F1F: sdscatfmt (sds.c:667)
==76089==    by 0x1C3F33: clusterSaveConfigImpl (cluster_legacy.c:1128)
==76089==    by 0x1C4641: clusterSaveConfigFromBio (cluster_legacy.c:1231)
==76089==    by 0x1B0004: bioProcessBackgroundJobs (bio.c:329)
==76089==    by 0x4A17B83: start_thread (pthread_create.c:447)
==76089==    by 0x4AA4CC3: clone (clone.S:100)
==76089== LEAK SUMMARY:
==76089==    definitely lost: 52 bytes in 1 blocks
==76089==    indirectly lost: 782 bytes in 1 blocks
==76089==      possibly lost: 40,041 bytes in 874 blocks
==76089==    still reachable: 2,770,090 bytes in 13,748 blocks
==76089==         suppressed: 24 bytes in 1 blocks
...
==76027== LEAK SUMMARY:
==76027==    definitely lost: 0 bytes in 0 blocks
==76027==    indirectly lost: 0 bytes in 0 blocks
==76027==      possibly lost: 41,999 bytes in 897 blocks
==76027==    still reachable: 2,837,154 bytes in 12,881 blocks
```

76089 is the RDB fork child, from the server log in the same job:

```
76027:M 14 Sep 2026 01:12:31.097 * Background RDB transfer started by pid 76089 to pipe through parent process
76089:C 14 Sep 2026 01:12:31.130 * Fork CoW for RDB: current 7 MB, peak 7 MB, average 7 MB
```

Run 35039408935 is the same shape: parent 75485 clean, child 75547 loses 60 bytes, and
`75485:M 16 Sep 2026 01:09:50.651 * Background RDB transfer started by pid 75547 to pipe through parent process`.

## Why the parent is not leaking

`clusterSaveConfigImpl` has one allocation of `tmpfilename`, at `src/cluster_legacy.c:1128`:

```c
tmpfilename = sdscatfmt(sdsempty(), "%s.tmp-%i-%I", server.cluster_configfile, (int)getpid(), mstime());
```

Every path after that line reaches the single `cleanup:` label, which frees it at
`src/cluster_legacy.c:1194-1201` (`sdsfree(tmpfilename); sdsfree(content);`). No early return, no
second allocation site. That matches the parent reporting 0 definitely lost.

`fork()` copies only the calling thread. In the child, `bioProcessBackgroundJobs` (`src/bio.c:258`)
never existed, its stack is not a leak-check root, and the sole reference is gone. That is also why
it is "definitely lost" rather than "possibly lost": a live sds pointer is an interior pointer and
would only be "possibly lost", which these runs hide with `--show-possibly-lost=no`.

The child's `suppressed: 24 bytes in 1 blocks` is the existing `bio_job_in_flight_at_exit`
suppression in `src/valgrind.sup` (74ad2f923, #3277) firing on the `bio_job` struct. That
suppression already recognizes this phenomenon, but it only matches `fun:malloc ... fun:allocBioJob`,
so anything allocated deeper inside job processing, like this `tmpfilename`, is still reported.

## What made it start

`f1addd8f3` (2026-09-01), "Use BIO thread for cluster config saving in
cluster-config-save-behavior best-effort mode (#2555)". Before it, `clusterSaveConfigImpl` ran only
on the main thread, which is the forking thread, so `tmpfilename` was always reachable in the child.
#2555 added `BIO_CLUSTER_SAVE` (`src/bio.h:57`) and `clusterSaveConfigFromBio`
(`src/cluster_legacy.c:1229-1232`), moving the allocation onto a non-forking thread's stack. The
failures begin 2026-09-10.

The failing test is `tests/unit/cluster/misc.tcl:226`, `cluster-config-save-behavior best-effort
mode - node continues running when config save fails`. It widens the window deliberately:
`create_nodes_conf_folder` (`tests/unit/cluster/misc.tcl:190-196`) replaces `nodes.conf` with a
directory so every BIO save takes the `rename()` failure path plus rate-limited `serverLog` plus
`unlink()` before reaching `cleanup:`, and its `cluster failover takeover` triggers the full sync
that forks. It only fires when the fork lands inside that window, hence 2 of 7 runs.

## The over-assert

- `tests/support/util.tcl:631` matches `{ at 0x}` against the entire stderr buffer.
- `tests/support/util.tcl:647` requires `definitely lost: 0 bytes` somewhere in the buffer without
  checking whose summary it belongs to.
- `tests/support/server.tcl:351` launches with `--trace-children=yes` and no
  `--child-silent-after-fork=yes`, so children append to the same stderr file.

Neither check is scoped to the server PID, so a fork child's leak summary fails the test file even
when the server is clean.

## Suggested direction

Add `--child-silent-after-fork=yes` at `tests/support/server.tcl:351` and `tests/instances.tcl:67`.
That removes the whole class of "reachable only from a non-forking thread" false positives rather
than extending the suppression once per downstream allocation site. Broadening
`bio_job_in_flight_at_exit` to match `fun:bioProcessBackgroundJobs` also works but keeps the same
trap open for IO threads and any future worker. The cost of the first option is losing leak checks
in fork children, which the suite cannot do reliably today anyway for exactly this reason.

## Ruled out

- A leaking path in `clusterSaveConfigImpl`: one allocation site, one `cleanup:` exit.
- A leak in the long-lived server: parent is clean in both runs.
- A parent shutdown race: shutdown does not cancel BIO threads. `bioKillThreads` (`src/bio.c:366`)
  is reachable only from `killThreads` (`src/debug.c:2332`), which runs only from
  `doFastMemoryTest` in `printCrashReport` (`src/debug.c:2537`).
- Runner, network, or toolchain problems.

No existing `valkey-io/valkey` issue tracks this.

</details>

This was generated by AI but verified, with love, by a human.

