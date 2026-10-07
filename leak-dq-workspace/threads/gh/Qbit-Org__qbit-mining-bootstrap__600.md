# 3.x.x: a 400k-window frontend's resident set ratchets up with block landings to ~3.3 GB over a 5.5 h soak

- URL: https://github.com/Qbit-Org/qbit-mining-bootstrap/issues/600
- Repo: Qbit-Org/qbit-mining-bootstrap (language: Python)
- State: closed; created 2026-09-30T00:14:36Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · djh58 · 2026-09-30T00:14:36Z · https://github.com/Qbit-Org/qbit-mining-bootstrap/issues/600

## What the weekly soak found

The first full `soak-weekly` run (#575 item 2, PR #588) took about 5.5 h: one server lifetime, two frontends, a 400k window, and 13 cycles of the mainnet-shape-130-addresses, rental-churn-bursts-and-storms and tip-delivery workloads. It passed every gate except resident memory: [run 36612534287](https://github.com/Qbit-Org/qbit-mining-bootstrap/actions/runs/36612534287), artifact `prism-load-soak-weekly`.

Everything else held for the full lifetime:
- exact reconciliation, including partitions restored from their archives;
- zero shortfall in all 104 phases, and every tip-delivery budget met;
- 4 partition rollovers, with 3 partitions archived, detached and dropped by `share-archive` under load;
- descriptors flat at 233;
- 16 database connections per frontend with no drift;
- `pg_wal` peak 1040 MiB;
- no payout divergence.

Resident memory, as the floor (minimum) of each 25.5-minute cycle, in MiB:

| cycle | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| fe-0 | 486 | 678 | 662 | 741 | 934 | 991 | 975 | 996 | 1251 | 1261 | 1263 | 1724 | 1719 |
| fe-1 | 484 | 1945 | 2382 | 2771 | 2991 | 2977 | 3027 | 3315 | 3304 | 3301 | 3308 | 3299 | 3308 |

The window-peak slope after a one-hour warm-up was +134 MiB/h on fe-0 and +24 MiB/h on fe-1, against a 16 MiB/h bound. fe-0 also reached 2.10x its warm-up peak (bound 2x).

## What it looks like

- **Every step comes from a block landing.** Every step of more than 150 MiB happens in a mainnet-shape `steady_state` phase, where the preset lands its 2 scheduled blocks per cycle; each landing builds a 400k-window audit. No step coincides with a partition rollover or a retention pass: the retention commands run in their own process.
- **Shorter runs show the same step.** In shorter local runs a single landing lifts a frontend by about 800 MiB (520 to 1,300 MiB). The memory is sometimes returned later: one frontend went from 2.2 GiB back to 0.9 GiB.
- **fe-1 has plateaued.** It climbs to about 3.3 GB in the first 2 h, then stays within about 30 MiB through roughly 16 more landings. A per-landing leak would keep growing; this looks like allocator high-water retention of large transient allocations.
- **fe-0 has not plateaued.** Its floor was still ratcheting at 5.5 h, from 1263 to 1724 MiB at cycle 12, and may be heading for the same ceiling.

## Questions

1. Is the retained memory allocator retention (freed but not returned) or live data held after a landing, for example cached windows or audit bodies? A heap census across a landing would tell.
2. What is the steady-state ceiling for a 400k-window frontend, and does it scale with the window (and with #521's 2,600-address shapes)?
3. What memory limit should production frontends get, and should the RSS alerting and the resident-set bound in `docs/prism-capacity-readiness.md` (2x the warm-up peak, #226, #244) account for the landing step?

## The gate

The weekly soak's RSS gates stay as they are: the envelope slope of at most 16 MiB/h after an hour, and 2x the warm-up peak. A follow-up to #588 marks the RSS rows as an expected failure that names this issue. The weekly job then passes while every other gate passes and RSS fails as expected, and turns back into a real gate once this is resolved.

Refs #575, #226, #244


## Comment 5917355463

reporter (MEMBER) · djh58 · 2026-09-30T18:34:31Z · https://github.com/Qbit-Org/qbit-mining-bootstrap/issues/600#issuecomment-5917355463

## Investigation: why a 400k-window frontend ratchets to ~3.3 GB

Refs #600. Related: #185 (coordinator RSS did not return after a candidate storm), #226, #244, #242.

**Short answer.** The ratchet is **allocator retention, not live data**. Every block landing on a frontend makes a ~1.4 GB transient allocation burst of millions of small allocations. glibc keeps the freed memory in its per-thread arenas and does not give it back. The live heap returns to its pre-landing size after every landing. It plateaus at ~3.2–3.3 GB once the arenas that landing work runs in have each reached their high-water mark, after roughly 4–6 landings on that frontend. A `malloc_trim(0)` returns RSS to baseline, and so does jemalloc. This is the same mechanism #185/#226 found in the Python coordinator (glibc arena fragmentation under a flat in-use count), carried over to the native server, which exports RSS only (see capacity-readiness "Retention or fragmentation?").

## Method

- **Build.** Scratch release build of #588's head (199b5d7c, server source identical to 3.x.x apart from #588's fd gauge). Not committed. It adds:
  - an in-process sampler (1 s) that logs `VmRSS`, glibc `mallinfo2` and the arena count (`malloc_info`);
  - markers at each landing phase;
  - `malloc_trim` triggers (manual, and optionally after each landing);
  - an env-gated F4 prototype (below).
- **Run shape.** A scratch soak preset loops `mainnet-shape-130-addresses` in one server lifetime:
  - 2 frontends, 400 sessions, 400k window (416k shares at landing);
  - 2 scheduled landings per 10-minute cycle;
  - `PRISM_REFRESH_BUILD_THREADS=4` (the 8-vCPU CI value) and 4 runtime workers.
- **Host.** Everything ran under the shared heavy lock, pinned to 4 cores, one run at a time.
- **Live bytes** = `uordblks + hblkhd`. **Retained** = `fordblks`: free bytes glibc holds inside its arenas.
- **Gates.** All six runs finished with harness exit 0: exact reconciliation, no shortfall.

## Q1: allocator retention or live data?

**Retention.** Run A (glibc, default settings, 50 min), on the frontend that landed:

| after landing # | RSS floor (MiB) | live (MiB) | free in arenas (MiB) |
|---|---|---|---|
| 0 (warm-up) | 595 | 264 | 343 |
| 2 | 1352 | 251 | 1102 |
| 4 | 1978 | 347 | 1719 |
| 5 | 2524 | 246 | 2275 |

The live heap is flat at 250–350 MiB between landings in every run, so no cache, window snapshot or audit body is retained. A manual `malloc_trim(0)` at 44 min took RSS from 2,531 to 327 MiB on fe-0 in 101 ms, and from 2,466 to 315 MiB on fe-1 in 134 ms. The arena count is 16–18 (threads 13–17) and flat all run, so there is no thread leak.

Attribution of one 416k-share landing, measured as live heap:

| phase | live (MiB) | change |
|---|---|---|
| before | 263 | |
| window read | 533 | +270 |
| `build_claim_parts` | 769 | +236 |
| peak inside `landing_from_parts` | 1628 | +860 (1003 MiB of it mmapped) |
| end of landing | 769 | back down; free-in-arenas +580 |
| after the window and parts are dropped | ~260 | the rest also stays as arena free |

The retained part is small-allocation churn:
- `AcceptedShare` has 5 `String`s per share and `CountedShare` has 4, over ~400k shares, built at least twice: once by `build_claim_parts`, and again by `verify_audit_view`'s `build_prism_reward_manifest` re-derivation.
- `landing_from_parts` also builds a `serde_json::Value` of the whole body, which is converted to a raw value and then dropped.

The large contiguous buffers are mmapped and do go back to the OS.

## Q2: where does it plateau, and what does it scale with?

- **Plateau.** ~3.2–3.3 GB at 400k with glibc defaults.
  - Run E: all 6 landings on one frontend. Floor 574 → 1951 → 1964 → 3153 → 3157 → 3165 MiB; the last two landings added nothing.
  - Calibration run 36612534287: fe-1 at 3.30–3.33 GB for ~16 landings, VmHWM 3,857 MiB.
  - The plateau is reached after about 4–6 landings **on that frontend**. It is driven by landings, not by time. A frontend that has not landed stays at 580–700 MiB, like fe-0 in the calibration run until it began landing.
- **Why it plateaus.** Each thread keeps using the same glibc arena. Landing work runs on blocking-pool, builder and runtime threads. Once each arena that work touches has reached its high-water mark, later landings reuse that free memory. So the ceiling is roughly the number of arenas that landing work touches times each arena's share of the ~1.4 GB burst. It is bounded, not a leak.
- **Window size.** Roughly linear. Run F at 200k (208k shares):
  - live baseline 126–144 MiB (400k: 250–260);
  - landing live peak ~520 MiB (400k: ~1,630);
  - first step +400–450 MiB (400k: +750–1,380);
  - floor 1.0–1.06 GB after 3–4 landings (400k: 2.5–3.2 GB).
  - Extrapolation, not measured: a 500k window gives a ~4 GB plateau and ~5 GB HWM.
- **Sessions and addresses.** Not varied here. Their live data is part of the flat 250 MiB baseline. The landing burst scales with window shares, not sessions. The 2,600-address shape grows `payout_policy_manifest.accounts` and prior balances (per account), which is small next to per-share data.

## Q3: fix options, measured at 400k (30 min, 6–7 landings)

| option | landing frontend RSS floor | landing peak | cost | verdict |
|---|---|---|---|---|
| glibc default (A, E) | 2.5 GB after 5, plateau 3.2 GB | 2.2–3.9 GB | — | the bug |
| `MALLOC_ARENA_MAX=2` (B) | 1.77 GB after 7, still rising (1.5 GB free in 2 arenas) | 2.1 GB | full refresh 13.1 s vs 7.5 s (n=2), tip max 2.2 s vs 1.5 s | no: partial fix, slower |
| **jemalloc** (C, `LD_PRELOAD` of Ubuntu 5.3.0) | **460–527 MiB, flat over 7 landings** | 1.3–1.5 GB, returned within seconds | delta refresh p50 686 vs 720 ms, p90 837 vs 962; tip p50 791 vs 848 ms | **best**: saves ~2.7 GB of plateau |
| `malloc_trim(0)` after each landing (D) | 745–823 MiB over 6 landings | 1.7–1.9 GB | 38–56 ms per trim on a spawned thread; refresh p50 639 ms | good, zero-dependency; saves ~2.4 GB |
| F4: stored body without a `Value` tree, streamed snapshot digest (E) | unchanged, plateau 3.17 GB | live peak 1,628 → ~1,160 MiB | none seen | cuts the transient ~470 MiB but not retention; secondary |
| bound a cache | n/a | n/a | n/a | nothing to bound: live heap is flat |

Recommended:
1. **Make jemalloc the global allocator.** Use `tikv-jemallocator` in `qbit-prism-server`'s `main.rs` (a new dependency that builds bundled C), or install `libjemalloc2` in the image and set `LD_PRELOAD`.
2. If a new dependency is unwelcome, **call `malloc_trim(0)` off-runtime after each landing** as a first step. That is about 10 lines, and `libc` is already a dependency. Trimming after full window rebuilds would also absorb the remaining ~250 MiB of creep.
3. **Reduce the transient separately.** The F4 changes help. A larger win would come from interning the ~130–2,600 distinct `miner_id` / `order_key` / `p2mr_program_hex` strings, or from a streaming `verify_audit_view` comparison instead of re-deriving the whole reward manifest. That would cut both the peak and the allocation churn; not measured.

## Q4: production memory limit per frontend today

- **400k window, current binary (glibc).** Plateau 3.2–3.3 GB; observed HWM 3,857 MiB (calibration) and 3,915 MiB (run E).
  - Recommend a **5 GiB hard limit per frontend** and an **RSS warning at 4 GiB**.
  - Two frontends per host need 10 GiB plus PostgreSQL.
- **After jemalloc.** Floor ~0.5 GB and peak ~1.5 GB, so **2.5 GiB**.
- **After trim-after-landing.** Floor ~0.8 GB and peak ~1.9 GB, so **3 GiB**.
- Scale roughly linearly with the window.

**Soak gate and the capacity-readiness bound (#226, #244).** A landing adds ~1.0–1.4 GB for a few seconds even with jemalloc. A frontend that did not land during the warm-up hour has a warm-up peak of ~0.6–0.7 GB, so its first later landing exceeds 2x the warm-up peak under any allocator.
- The resident-set bound should use per-cycle floors (as #600's table does).
- Alternatively, the warm-up must include a landing on every frontend.
- The RSS alert needs the landing transient as headroom.

## Side note (not #600)

Calibration fe-1 logged one `ALERT: offered candidate could not be processed; kept for reconciliation` at 20:49:58Z: "payout revision changed while observing chain state". This happened during the soak, with the block accepted by the node. It is worth a look by whoever owns the reconciliation path.

The instrumentation was local to a scratch build and is not committed. No server code changed.


## Comment 6011876773

maintainer (MEMBER) · RobertClarke · 2026-10-06T07:52:28Z · https://github.com/Qbit-Org/qbit-mining-bootstrap/issues/600#issuecomment-6011876773

Fixed by #627 (`fd96c154`, malloc_trim after each landing). The weekly 5.5 h soak at `c95febb3`, which includes #627, passes every resident-memory gate: dispatched run 37403129136, job 112075275351, 332 samples over 5.52 h, 4.52 h after a 60 min warm-up.
- **load-fe-0:** peak 1,026.9 MiB after warm-up against 880.3 MiB during it (1.17×; ≤ 2×); window-peak slope +8.65 MiB/h (≤ 16).
- **load-fe-1:** peak 1,292.7 MiB against 1,141.3 MiB (1.13×); slope −15.75 MiB/h.
- **Both frontends:** one server lifetime each; descriptors flat; DB connections peak 16; WAL peak 1,040 MiB; 4 rollovers; 2 partitions archived; 0 payout divergences; worst per-sample share-ACK p99 21.8 ms.

The job's only failing row is the expected-failure marker itself: "#600 looks fixed: every resident-memory row passed". A follow-up PR sets `soak-weekly`'s `rss_expected_failure` to null, so the weekly soak gates resident memory for real. #628 (jemalloc) and #629 (per-cycle floors) stay open as optional follow-ups.
