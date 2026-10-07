# Bug: fpmsyncd: glibc heap fragmentation causes unbounded memory growth under route churn

- URL: https://github.com/sonic-net/sonic-buildimage/issues/28245
- Repo: sonic-net/sonic-buildimage (language: C)
- State: open; created 2026-07-06T02:40:33Z; status ok; passes offcwe

## Issue body

reporter (NONE) · rejithomas-arista · 2026-07-06T02:40:33Z · https://github.com/sonic-net/sonic-buildimage/issues/28245

### Is it platform specific

generic

### Importance or Severity

High

### Description of the bug

fpmsyncd RSS grows unboundedly under route churn (repeated route add/withdraw cycles) and is never released to the OS. glibc malloc retains freed heap memory in internal free lists; scattered in-use allocations prevent brk() top-of-heap trimming. fpmsyncd never calls malloc_trim(), so physical pages are never reclaimed.

This is not a code-level memory leak. malloc_info() called inside fpmsyncd confirmed 24 GB obtained from OS but only ~650 KB actually in use — the rest is free inside glibc's allocator bins. malloc_trim(0) via gdb reclaimed all memory instantly (24 GB → 25 MB).

Workaround/Fix: LD_PRELOAD jemalloc for fpmsyncd. jemalloc uses mmap-based extents with automatic dirty-page purging. A/B test on same device with 100K routes: glibc grew to 20+ GB under churn, jemalloc stayed under 265 MB through 61 million route updates.

### Steps to Reproduce

1. Advertise 100K IPv4+IPv6 routes with ECMP to a SONiC device
2. Cause route churn (e.g. remove `neighbor <pg> next-hop-self` on upstream peer)
3. Observe fpmsyncd RSS growing continuously
4. Stop the churn — RSS stays at peak, never decreases

### Actual Behavior and Expected Behavior

  ### Observed behavior

  - fpmsyncd RSS grew to 20+ GB and was never released
  - `malloc_info()` inside fpmsyncd confirmed: 24 GB from OS, only ~650 KB in use,
    rest sitting in glibc free lists
  - `malloc_trim(0)` via gdb reclaimed all memory instantly (24 GB → 25 MB),
    confirming no code-level leak

  ### Expected behavior

  fpmsyncd should release freed route memory back to the OS.


### Relevant log output

```shell
# fpmsyncd at 24 GB RSS with only 149 routes in APP_DB
  root  61  24.4g 24.1g 7840 S  0.0 79.2 fpmsyncd

  VmRSS:  25246988 kB
  VmData: 25289036 kB

  # malloc_info (called inside fpmsyncd via gdb) shows memory is FREE, not leaked
  <total type="rest" count="52" size="25826589843"/>     <!-- 24 GB FREE in bins -->
  <system type="current" size="25827164160"/>             <!-- 24 GB from OS -->
  # In use: only ~650 KB

  # malloc_trim(0) reclaimed everything
  Before: VmRSS = 25,246,916 kB  (24.1 GB)
  After:  VmRSS =      25,776 kB  (25 MB)

  # A/B test — 5 churn cycles, same device, same routes
  jemalloc: RSS 62-78 MB, released automatically on withdraw
  glibc:    RSS 127-143 MB, never released, grows each cycle
```

### Output of `show version`, `show techsupport`

```shell
build_version: '20251110.23'
Platform: x86_64-arista_7060x6_64pe_b
HwSKU: Arista-7060X6-64PE-B-O128
```

### Attach files (if any)

_No response_

## Comment 4982311524

other (CONTRIBUTOR) · zjswhhh · 2026-07-15T15:25:24Z · https://github.com/sonic-net/sonic-buildimage/issues/28245#issuecomment-4982311524

Hi @deepak-singhal0408 - can you help triage? Thanks.  

## Comment 5055216359

other (CONTRIBUTOR) · deepak-singhal0408 · 2026-07-23T06:32:13Z · https://github.com/sonic-net/sonic-buildimage/issues/28245#issuecomment-5055216359

@rejithomas-arista, In latest Master code, we have enabled tcmalloc in FRR. So I would prefer to use tcmalloc even for fpmsyncd over jemalloc (unless data proves that jemalloc is more performant for our usecases)..

If you are testing this with zmq enabled, 
then please check this issue https://github.com/sonic-net/sonic-buildimage/issues/28369 and the enhancements planned in fpmsyncd area in the comment. I plan to benchmark jemalloc mem_release performance with tcmalloc mem_release()->event driven(call Release() from an Idle triggered/chunked-abortable) on new dispatch thread planned. 

Will share my findings on this. thanks,



## Comment 5210256561

other (CONTRIBUTOR) · deepak-singhal0408 · 2026-08-07T00:17:40Z · https://github.com/sonic-net/sonic-buildimage/issues/28245#issuecomment-5210256561

Following up on this. Alongside the discussion in [this thread](https://github.com/sonic-net/SONiC/pull/2481#issuecomment-5210045099), posting the benchmarking data here.

### How it was tested

A standalone harness modelling the fpmsyncd route path — a producer thread feeding a coalescing map, a dispatch thread draining/serialising/freeing, an idle window every cycle, and a small fraction of long-lived entries to reproduce the heap-top pinning you described. 500k routes × 4 cycles, 3 runs per configuration, allocator selected via `LD_PRELOAD`.

### Results (medians of 3 runs)

| Configuration | Held after going idle | Returned to OS? | Worst-case stall on the route-ingest thread |
|---|---:|:---:|---:|
| glibc (today) | 399 MB of 401 MB peak | ❌ never | 5.0 ms |
| tcmalloc, no explicit release | 369 MB of 371 MB | ❌ never | 2.9 ms |
| glibc + `malloc_trim` | 24 MB | ✅ | 7.8 ms |
| **tcmalloc + idle-triggered release** | **91 MB** | ✅ | **1.1 ms** |
| jemalloc (decay 1 s) | 61 MB | ✅ | 9.4 ms |
| jemalloc (decay 100 ms) | 59 MB | ✅ | 9.9 ms |

Two things this confirms:

1. **The bug is real.** With glibc the floor is essentially the peak — the memory never comes back.
2. **Switching to tcmalloc alone does not fix it.** It has to be explicitly asked to release; that's the second row, which ratchets just like glibc.

### On jemalloc

It works. It bounds memory with no application code at all, and returns ~30 MB more than the tcmalloc path does — consistent with the field numbers in your report.

The cost turns up on the other axis. jemalloc had the worst tail of all six configurations — ~9–10 ms versus ~1 ms for tcmalloc — and ~10% more page faults when memory is reused shortly after being released.

That lines up with how the two release paths behave. jemalloc's decay purge is driven by allocation activity and runs to completion once started, so it tends to stay quiet while idle and then do its work during a burst, on a thread that is also serving routes, with no way to cut it short. The tcmalloc path we're using is the inverse: it only starts after the queue has been empty for a while, hands memory back in 4 MiB slices, and re-checks between slices whether routes have arrived — if they have, it stops immediately and steps aside.

Since route convergence latency is what we're most protective of, we took the configuration with the lower tail, accepting a ~30 MB higher floor.

A secondary reason: FRR is already built with tcmalloc by default in master (`ENABLE_FRR_TCMALLOC ?= y`), and fpmsyncd runs in that same container — so using jemalloc here would mean running two allocators side by side in one container.

The release mechanism itself is specified in the HLD above and ships with the [28369](https://github.com/sonic-net/sonic-buildimage/issues/28369) work, since it reuses that change's dispatch thread to detect the busy→idle edge.


## Comment 5211987151

reporter (NONE) · rejithomas-arista · 2026-08-07T03:36:09Z · https://github.com/sonic-net/sonic-buildimage/issues/28245#issuecomment-5211987151

Thanks Deepak, this is useful data to understand the decision. One clarification: was the jemalloc run done with background_thread:true, or only with decay tuning?

The reason I ask is that the explanation says jemalloc purge is driven by allocation activity and can run on the route-serving thread during a burst. That is true for foreground decay, but my suggestion was specifically jemalloc with background purge enabled. Without background_thread:true, the 9-10 ms tail seems to be measuring foreground purge behavior rather than the configuration I had in mind.
It may be worth adding that data point to remove any ambiguity.  Thanks for doing this work! 

 

## Comment 5352712074

other (CONTRIBUTOR) · deepak-singhal0408 · 2026-08-20T07:20:40Z · https://github.com/sonic-net/sonic-buildimage/issues/28245#issuecomment-5352712074

Following up on the allocator discussion with measured data.

I ran a deeper benchmark to separate three questions: **allocator choice**, **release mechanism**, and **release timing** — measured across three load regimes (burst-then-drain, saturation, sustained congestion).

The comparison is **tcmalloc + our idle-triggered release hook** (as proposed in the HLD) versus **jemalloc + `background_thread:true` + decay**, plus two control arms that isolate the allocator from the release mechanism:

| arm | allocator | release mechanism | role |
|---|---|---|---|
| `Afull` | gperftools tcmalloc | idle-triggered hook, 64 MB slices, 2.5 s debounce | candidate (HLD) |
| `B` | jemalloc | `background_thread:true,dirty_decay_ms:1000,muzzy_decay_ms:0` | candidate |
| `Bdef` | jemalloc | `background_thread:true` at **stock decay** (10 s / 10 s) | candidate, nothing else tuned |
| `Anorel` | gperftools tcmalloc | none (hook compiled out) | control |
| `Bnodecay` | jemalloc | none (`decay_ms:-1`) | control |

The two controls make the 2x2: with the release mechanism removed from each allocator, any difference between `Afull` and `B` can be attributed to the allocator or to the mechanism rather than to both at once. `Bdef` appears in Case 3.

---

## Case 1 — Burst, then drain

Congestion drives the coalescing map to a fixed depth cap, then clears. n=5/arm.

| arm | RSS peak | RSS resting | minor faults (k / M routes) |
|---|---|---|---|
| `Afull` — tcmalloc + hook | **117.7 MB** | 47.4 MB | **6.9** |
| `B` — jemalloc + decay | 184.5 MB | **28.0 MB** | 36.2 |
| `Anorel` — tcmalloc, no release | 143.4 MB | 143.4 MB | 3.6 |
| `Bnodecay` — jemalloc, no decay | 1506.3 MB | 1506.3 MB | 50.1 |

Both mechanisms reclaim. They trade differently:

* **tcmalloc + hook leads on peak** (36 % lower) **and page faults** (5.2x fewer).
* **jemalloc leads on resting RSS** (41 % lower, 28.0 vs 47.4 MB), using the allocator alone.

The control arms confirm each mechanism is doing the work: with release off, tcmalloc rests at 143 MB and jemalloc grows to 1.5 GB.

One caveat on the peak column: that gap traces to a coalescing differential in the harness, so I'd treat it as harness-specific until it's confirmed against FRR's real offer pattern.

## Case 2 — Saturation

HLD Appendix A.2 reports drain throughput unchanged within ±1.5 % while the hook runs, measured against a paced offer. This case re-measures at **saturation** with the consumer unthrottled, where a cost on the send thread becomes visible.

Operating rate located by sweep (ceiling ~690 k/s); n=5/arm. `coalesced` is 0 throughout, so delivered work equals offered work.

| arm | drain ceiling (k routes/s) | CPU µs/route | vs `Anorel` |
|---|---|---|---|
| `Anorel` — tcmalloc, no release | **689.0 ± 20.9** | 2.141 | baseline |
| `B` — jemalloc + decay | **685.7 ± 22.1** | 2.139 | −0.5 % (n.s.) |
| `Afull` — tcmalloc + hook | 661.6 ± 9.3 | 2.251 | **−4.0 %, t = −2.68** |
| `Bnodecay` — jemalloc, no decay | 653.3 ± 15.9 | 2.301 | −5.2 % |

**1. Both allocators reach the same ceiling.** Pooled tcmalloc 675.3 vs jemalloc 669.5 k/s, +0.9 %, t = +0.56. The workload sets maximum throughput, not the allocator.

**2. The idle-triggered hook costs ~4 % of that ceiling** (`Afull` vs `Anorel`, same allocator), corroborated independently by CPU per route (2.251 vs 2.141, +5.1 %).

**3. The cost is the thread, not the timing.** During the bursts `Afull` ran the hook **1** time; `B` purged **63** times. jemalloc purged ~60x more often during churn and held its full rate, because `background_thread:true` runs it off the critical path. Our hook shares the send thread, so its inline bookkeeping plus one slice costs 4 %.

**4. Decay helps throughput.** `B` vs `Bnodecay` is +5.0 % (t = +2.66) — a compact working set beats an unbounded one, so reclaiming is a net win on rate.

## Case 3 — Sustained congestion (map held at the cap for 60 s, then one idle window)

This is the regime the thread argued about: jemalloc's background thread purging mid-burst while routes are still flowing.

| arm | delivery/s | minflt / 1k | RSS peak | terminal RSS (3 reps) | reclaims **during** burst |
|---|---|---|---|---|---|
| `Afull` | 51 038 | 27.4 | 379.8 MB | 51.5 / 49.2 / 47.8 MB | 0 |
| `B` (jemalloc, tuned) | **56 268** | 65.9 | 433.2 MB | **32.5 / 32.6 / 32.5 MB** | 126 / 134 / 135 |
| `Bdef` (jemalloc, **stock** decay) | 66 783 | 72.6 | 566.8 MB | 33.0 / 33.3 / 32.8 MB | 82 / 104 / 146 |

**The preemption asymmetry is real**, measured in both directions: jemalloc purged ~130 times and reclaimed ~1 GB while routes were still flowing; our hook released only after delivery stopped, in every arm and every rep. That is by construction, and it is a real property of the idle-triggered design.

**The page-fault penalty is real too** — 2.3–2.6x more minor faults, paid during the storm.

**Throughput held anyway.** Despite purging ~1 GB mid-burst and taking 2.5x the faults, jemalloc delivered the *highest* route rate. On this data, background purging leaves route processing intact under sustained load.

**The zero-tuning version of the proposal works.** `Bdef` reached the same resting RSS (~33 MB) as the tuned arm. Tuning `dirty_decay_ms`/`muzzy_decay_ms` buys a lower peak (433 vs 567 MB); resting RSS lands the same either way.

---

## Environment

* **Real code.** The harness drives the actual coalescing map and `zmq_send` path, so it *is* the allocation pattern rather than a simulation of it.
* **One allocator per binary** — separate binaries per arm, no `LD_PRELOAD`. Each run is gated by `ldd` + `nm` + `/proc/<pid>/maps` checks confirming exactly one allocator is mapped and the hook is present or compiled out as intended.
* **Identical consumer binary for every arm**, so any sink throttle is common-mode.
* **Arms interleaved** (reps outer, arms inner), so host drift hits every arm equally.
* **Noise floor measured, not assumed** — one arm run against itself under two labels. Every claim above exceeds that floor.
* **Bare-metal, CPU-pinned container** (`--cpuset-cpus=0-7`).
* **Burst capped on map depth, not duration.** Duration control produced high-water marks from 360 k to 960 k — a 2.6x swing in the quantity under study.

## Why KVM was abandoned

I planned this on a KVM t0 testbed and ran it on a bare-metal, CPU-pinned container instead: KVM steal time introduces noise at the same scale as the effects being measured. The trade is that FRR's real offer pattern remains untested — the main external-validity gap in everything above.

---

## Overall assessment

**On the allocator:** both reach the same ceiling (t = +0.56), so performance leaves the choice open.

**On the release mechanism:** this is where the data moved me. The decisive comparison is **application-managed release on the send thread** vs **allocator-managed release on a background thread**:

* Our hook costs ~4 % of ceiling throughput and carries ~200 lines of application code, a slicing policy, an abort predicate, and idle detection.
* `background_thread:true` holds full rate, purges 60x more aggressively, reaches a 41 % lower resting RSS, and carries one config string.

**The idle trigger also has a design problem independent of the benchmark.** Its premise is that an idle FPM socket implies a quiescent heap, but that window is exactly when `AsyncDBUpdater`'s min-priority thread drains the deferred APPL_DB write-back (`ZmqProducerStateTable` defaults to `dbPersistence = true`). So the release lands on that work rather than on an idle process, while an allocator background thread avoids the coupling entirely.

The HLD's underlying concern — that reclaiming during churn costs processing rate — holds for release on the send thread, which Case 2 measures at 4 %. Case 3 shows it does not hold once release moves off that thread: jemalloc reclaimed ~1 GB mid-burst and still delivered the highest rate. `background_thread` makes that move for free.

**On balance I'm leaning towards jemalloc + `background_thread:true`** for fpmsyncd and dropping the idle-triggered hook, with `dirty_decay_ms:1000,muzzy_decay_ms:0` as optional tuning for a lower peak (stock defaults already reach the same resting RSS).

On running two allocators inside `docker-fpm-frr`: the container already does. zebra and bgpd link gperftools tcmalloc via `pkg.frr.tcmalloc`, while fpmsyncd and everything else use glibc malloc. Each process links exactly one allocator at build time and they share no address space, so this changes which allocator fpmsyncd uses rather than mixing allocators anywhere. The build units stay independent as well — tcmalloc comes from `sonic-frr`, jemalloc would come from `sonic-swss`, and neither build affects the other. The cost is one more library in the image.

This is the direction suggested earlier in the review, so happy to hear if there are other concerns before I revise the HLD.

---

### Two corrections on my earlier comment

I'd said the hook would be needed under any allocator — the data points the other way.

Appendix A.2's "±1.5 % drain throughput" figure holds for a paced offer; at saturation the number is 4.0 % (Case 2).

Raw data, harness, and per-run CSVs available if useful.


## Comment 5390745822

reporter (NONE) · rejithomas-arista · 2026-08-24T04:29:51Z · https://github.com/sonic-net/sonic-buildimage/issues/28245#issuecomment-5390745822

Thanks Deepak for the follow-up and for taking the time to validate this giving a well-supported basis for the design decision. This too answers my question about background_thread:true  . Appreciate you documenting the methodology, trade-offs, and corrections so the reasoning is clear for future reference.
