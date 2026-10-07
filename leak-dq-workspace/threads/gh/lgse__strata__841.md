# perf(preview): investigate RSS reduction with reusable parent-side workers

- URL: https://github.com/lgse/strata/issues/841
- Repo: lgse/strata (language: Rust)
- State: open; created 2026-09-11T23:43:49Z; status ok; passes offcwe

## Issue body

reporter (COLLABORATOR) · ogarza · 2026-09-11T23:43:49Z · https://github.com/lgse/strata/issues/841

### Problem or use case

Follow-up to #839 / #824: investigate reducing the closed-preview RSS footprint without weakening per-decode sandbox isolation. This is **possible future work**, not an implemented fix or a prerequisite added to #839.

A new 100-cycle open/close experiment on the PR evidence binary found:

| Closed checkpoint | Application RSS (MiB) | Allocator-free arena memory (MiB) | Estimated allocator in-use (MiB) |
| --- | ---: | ---: | ---: |
| 1 | 215.1 | 35.68 | 46.30 |
| 20 | 282.2 | 100.14 | 46.41 |
| 100 | 316.1 | 133.87 | 46.38 |
| After 20 seconds idle | 315.5 | 134.03 | 46.22 |

Approximately 98 MiB additional **freed memory retained by glibc** accounts for most of the approximately 101 MiB RSS increase. Estimated allocator in-use memory stays approximately flat. All **733 tracked GTK pixel owners released**, with **101 returns to zero** (initial preview plus 100 cycles). No media-helper/FFmpeg descendants remained at closed checkpoints; FDs/threads did not accumulate, settling at 24/73. Arena count stayed at 32; secondary arenas larger than 6 MiB increased from 4 to 19.

This supports allocator retention, **not a demonstrated live-buffer leak or another GTK/GStreamer defect**. Strata creates a new reader thread per session ([source](https://github.com/lgse/strata/blob/63cd18c74ca3ca7d6d8876979e99eb5adf39c52e/src/sandbox/media.rs#L72)) and fresh pixel/sample vectors per frame ([source](https://github.com/lgse/strata/blob/63cd18c74ca3ca7d6d8876979e99eb5adf39c52e/src/media.rs#L201)); this is a likely trigger, not a call-stack-proven attribution or a proven optimization.

### Proposed solution

**First A/B test a small, lazy, bounded pool of parent-side reader/coordinator threads. Keep a fresh bubblewrap sandbox, FFmpeg processes and pipes for every decode generation.** Original-file parsing remains sandboxed; namespaces, single-input read-only mounts, device policy, permissions and transport validation must not broaden.

Implementation requirements:

- Tear down the previous job's renderer/descendants and reap its child before reassigning the worker. Keep cancellation prompt without blocking GTK on a join.
- Use fresh per-job cancellation, protocol state, deadlines and result channels/generation identity. Reject late results after seek, selection change, close or window destruction.
- Replace thread-lifetime completion (`JoinHandle::is_finished`) with per-job completion. Keep the four-session cap independent of thread availability; retain slots through buffered playback and preserve fifth-player busy behavior and bounded queues.
- Preserve the 30-second paused decoder/audio cleanup and retained frame/position. An idle parent thread is not a live decoder; document and bound its retained resources.
- Measure thread reuse **before** adding a buffer pool. If subsequently needed, recycle pixels only after GTK's **last** bytes owner releases them, bound retained capacity, and fully initialize/validate each new payload before presentation. Do not introduce sandbox-writable shared textures.

Acceptance evidence should compare the unchanged implementation and candidate under the same workload for at least 100 cycles, including closed/idle RSS/PSS, allocator in-use/free memory, texture ownership, threads/FDs, descendants and startup/seek latency. Exercise cancellation, failed/malformed output, seek/resize, pause/resume and multiple windows/chooser sessions. Require a measured improvement without security/lifecycle regressions; do not assume pooling establishes a universal RAM/VRAM plateau.

### Alternatives considered

- **No change:** existing ownership is bounded and the measurements do not demonstrate increasing live allocations. Keep the RSS caveat if the optimization does not justify its complexity.
- **Global allocator settings:** the earlier PR evidence's separate `MALLOC_ARENA_MAX=2` run supports allocator retention, but changes process-wide behavior. No production override is recommended from these measurements alone.
- **Call `malloc_trim(0)` on close:** a one-off diagnostic after the final idle only reduced RSS from 315.5 to 309.6 MiB (approximately 5.9 MiB). This is not evidence of a sufficient fix.
- **Reuse sandboxed decoders across files:** out of scope. A compromised decoder could persist into subsequent files, and this would change the current isolation/reset boundary. This proposal is distinct from thumbnail-helper process reuse in #516, which explicitly excludes Space previews.

### Visual examples

N/A — memory/resource optimization; no UI redesign proposed.

### Strata version

PR #839, commit `63cd18c74ca3ca7d6d8876979e99eb5adf39c52e`; existing source-built debug evidence binary, identical to the cached quality build. SHA256: `b35cec0f8b1a945f3b4c014a06a5e6abd59ebe4a6edf05502b68d0a830c0d663`.

### Additional context

- Native Arch environment: glibc 2.44, GTK 4.22.4, GStreamer 1.28.6. Generated 1080p A/V fixture, software decoding, Cairo renderer, private Xvfb/D-Bus/AT-SPI, isolated HOME and real audio sinks disabled. No inherited desktop session or sandbox/ptrace permission changes.
- The existing [native runner and fixture instructions](https://github.com/lgse/strata/blob/63cd18c74ca3ca7d6d8876979e99eb5adf39c52e/docs/evidence/824/README.md#ownership-and-resource-evidence) reproduce the cycle workload with `python3 docs/evidence/824/native_smoke.py after --cycles 100` and the documented evidence binary placement.
- For the new allocator measurements, a local GDB-Python wrapper hosted that runner, attached only to its own application child at closed checkpoints, collected `malloc_info`, and detached before continuing. No allocator environment override. A 3-cycle instrumentation smoke run and the 100-cycle run completed. Raw diagnostics remain local under `target/839-rss/`, not committed artifacts.
- Allocator in-use estimate: global `system/current` minus free `total/rest` and `total/fast` when present, plus `total/mmap`. Includes allocator overhead/thread caches; **not** a reachability/leak census. GDB instrumentation can affect timing.
- No production changes or application rebuild were made for this investigation; full Rust/canonical E2E suites were not rerun. Hardware/GPU, speakers, ARM64 and release-optimized builds remain unverified. The separate legacy GtkMediaFile/GtkGstSink/GstPlay runtime patches are not implicated, changed or retired by these findings.


## Comment 5641965506

reporter (COLLABORATOR) · ogarza · 2026-09-11T23:54:45Z · https://github.com/lgse/strata/issues/841#issuecomment-5641965506

## Follow-up: pinpointed glibc retention mechanism

The investigation is now narrowed to specific allocator paths, using the **exact installed glibc source and matching runtime symbols**, rather than RSS alone.

**Source identity:** Arch `glibc 2.44+r24+g16be1518495f-1`, libc build ID `503200d7fda94a5dc6058d7e0694e5d1dcb2e372`. Build-ID-matched `malloc/arena.c` and `malloc/malloc.c` from Arch debuginfod were byte-for-byte identical to upstream revision `16be1518495f`.

### Where retention happens

1. **[`_int_free_chunk`, `malloc.c:4082–4089`](https://sourceware.org/git/?p=glibc.git;a=blob;f=malloc/malloc.c;hb=16be1518495f#l4082): dynamic thresholds.** Freeing an eligible mmap allocation raises `mp_.mmap_threshold` and sets `mp_.trim_threshold = 2 * mp_.mmap_threshold`. In the measured process, dynamic adjustment was enabled and the thresholds were **3,649,520 bytes** for mmap and **7,299,040 bytes (6.9609 MiB)** for trimming. The allocation that originally raised them has **not** been stack-traced.

2. **[`heap_trim`, `arena.c:554–558`](https://sourceware.org/git/?p=glibc.git;a=blob;f=malloc/arena.c;hb=16be1518495f#l554): the retention gate.** The normal free path reaches this function for secondary arenas. Its tail-shrinking path returns without reclaiming memory when:
   ```c
   top_size < mp_.trim_threshold
   ```
   The threshold is checked **per arena**, not against the combined free memory across the process.

3. **[`__malloc_arena_thread_freeres`, `arena.c:856–879`](https://sourceware.org/git/?p=glibc.git;a=blob;f=malloc/arena.c;hb=16be1518495f#l856): arenas outlive reader threads.** Thread exit releases the thread cache and detaches from its arena; an unowned arena is put on a reusable free list, not destroyed outright. [`reused_arena`/`arena_get2`](https://sourceware.org/git/?p=glibc.git;a=blob;f=malloc/arena.c;hb=16be1518495f#l727) rotate through existing arenas when the limit is reached and no free-list arena is available. New per-session reader threads plausibly spread frame allocations across these arenas, but their exact assignments have not been traced.

4. **[`mtrim`, `malloc.c:4452–4503`](https://sourceware.org/git/?p=glibc.git;a=blob;f=malloc/malloc.c;hb=16be1518495f#l4452): why `malloc_trim()` only partly helps.** It walks free chunks in bins and uses `MADV_DONTNEED`, but invokes the tail-trimming `systrim` step only for the **main** arena. It does **not** invoke `heap_trim` for secondary-arena top chunks, so the large free tails above remain.

### Fresh 40-cycle measurements

Same existing PR #839 debug evidence binary, generated A/V fixture and isolated native runner. GDB read `mp_` and each arena's free top chunk at closed checkpoints, in addition to `malloc_info`.

| Closed checkpoint | RSS MiB | Allocator-free MiB | Estimated allocator in-use MiB | Secondary-arena free tails, total MiB |
| --- | ---: | ---: | ---: | ---: |
| 1 | 222.52 | 43.08 | 46.33 | 30.05 |
| 20 | 275.30 | 94.27 | 46.46 | 82.84 |
| 40 | 309.16 | 127.26 | 46.40 | 115.76 |
| After 20 seconds idle | 308.66 | 127.42 | 46.23 | 115.77 |

At final idle, **17 secondary arenas each retained a free tail of 6.6148–6.6720 MiB**, just below the **6.9609-MiB** threshold. All secondary free tails together account for **115.77 MiB** of the **127.42 MiB** allocator-free total. Their approximately **85.7-MiB** increase closely tracks the approximately **86.6-MiB** RSS increase.

A one-off diagnostic `malloc_trim(0)` reduced RSS from **308.66 to 297.83 MiB**, but left the **115.77 MiB secondary-tail total unchanged**, consistent with the source above. This identifies retained free tails rather than merely hypothesizing increasing live allocations or interior fragmentation.

### Implications and limits

This is a **workload-sensitive allocator policy/limitation**, not proof of memory corruption, leaked live objects, or a universally incorrect glibc policy. The recommendation remains to **A/B test bounded parent-side reader-thread reuse while retaining fresh sandbox/decoder processes for each generation**. We have not yet proved which allocation raised the global threshold or measured whether worker reuse materially improves the result. No production allocator override or glibc patch is recommended without separate validation.

All 40 cycles completed under private Xvfb/D-Bus/AT-SPI, software/Cairo rendering and disabled real audio sinks. Only the experiment's child was traced; no ptrace/sandbox permissions or allocator settings were changed. No production edits, dependency changes or rebuilds; full Rust/canonical E2E suites were not rerun for diagnosis of an unchanged binary. Instrumentation can affect timing, and GPU/ARM64/release-optimized behavior remains unverified. Raw allocator states/XML and the local diagnostic remain under `target/839-rss/pinpoint-40/` and `target/839-rss/pinpoint.py`; these are local artifacts, not committed files.


## Comment 5642131666

reporter (COLLABORATOR) · ogarza · 2026-09-12T00:21:46Z · https://github.com/lgse/strata/issues/841#issuecomment-5642131666

## Follow-up: standalone tests support expected allocator behavior, not a demonstrated glibc leak

A small standalone C/Python harness now reproduces and distinguishes **allocator retention/reuse, fragmentation and an intentional leak**, without GTK, FFmpeg or sandbox processes.

**All 9 checks passed on glibc 2.44 / GCC 16.2.1**, followed by three additional complete successful runs to check thread-scheduling stability. “Passed” includes correctly detecting the deliberately leaking positive control—not ignoring it.

### Experiment

Four allocator arenas, with background threads keeping arenas attached. Each job allocates and touches eight `621 × 349 × 4`-byte payloads on a producer thread, then frees them on the main thread. Run 32 jobs, compare the 8-job warm-up with the end, then call `malloc_trim(0)` once.

The native experiment fixes the mmap/trim thresholds to the previously observed **3,649,520 / 7,299,040 bytes**. These settings apply only to the test process. This isolates the trimming mechanism; it does **not** reproduce the allocation that originally raised Strata's dynamic threshold.

| Case | RSS before → after explicit trim | Allocator-used | Allocator-free |
| --- | ---: | ---: | ---: |
| Fresh producer thread per job | 28.65 → 22.04 MiB | 0.01 MiB | 26.59 MiB |
| One persistent producer | 8.81 → 2.20 MiB | 0.01 MiB | 7.12 MiB |
| Fresh threads, lower only trim threshold to 128 KiB | 2.70 → 2.58 MiB | 0.01 MiB | 0.51 MiB |
| Live small anchors between freed payloads (fragmentation control) | 31.96 → 4.82 MiB | 0.02 MiB | 29.89 MiB |
| Deliberately lose one payload per job (leak control) | 51.81 → 46.02 MiB | 26.46 MiB | 23.29 MiB |

Key observations:

- With fresh threads, **arena size and allocator-used memory stopped growing after warm-up**, showing that retained memory was reused by later identical work.
- **19.85 MiB of secondary-arena free tails survived explicit trim**, consistent with the source paths identified in the previous follow-up. Free interior pages in the fragmentation control were reclaimed instead, without freeing its live anchors.
- Persistent-worker reuse and changing only the trimming threshold each reduced retained arena memory as predicted.
- The intentional leak increased allocator-used memory. A separate LeakSanitizer build detected exactly **32 lost allocations / 27,741,312 bytes**; the other four ownership cases had no reported leaks. LeakSanitizer replaces the allocator, so its build tests ownership only—not native glibc retention or RSS.

### Conclusion / next step

**For this investigated mechanism, the evidence strongly supports glibc behaving as implemented/designed: retaining reusable memory under its trimming policy, rather than leaking the freed payloads.** That policy trades a higher retained footprint for cheaper subsequent allocation; “working as designed” does not mean the tradeoff is ideal for Strata.

This is not proof that glibc or all of Strata is leak-free, nor that this policy is optimal on every platform. The standalone workload deliberately controls arena placement, buffer sizes and a single producer at a time. Its worker-reuse improvement does not yet establish the result for the real application.

**Recommended next step remains a Strata A/B experiment with bounded parent-side reader-worker reuse, preserving fresh sandbox/FFmpeg processes and the existing security/lifecycle limits.** There is no demonstrated basis here for treating this as a glibc leak or shipping a global allocator override.

