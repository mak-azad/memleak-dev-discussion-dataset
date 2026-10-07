# Primary-production and wide-CBS builds leave ~20 GB unreclaimable, for 1.4 GB of live data

- URL: https://github.com/eduaguilera/whep/issues/777
- Repo: eduaguilera/whep (language: R)
- State: open; created 2026-08-13T08:09:28Z; status ok; passes offcwe

## Issue body

reporter (COLLABORATOR) · lbm364dl · 2026-08-13T08:09:28Z · https://github.com/eduaguilera/whep/issues/777

## Symptom

Building the primary-production and wide-CBS tables leaves ~20 GB resident in
the process that cannot be freed, for 1.4 GB of live data.

Measured at 1901-2022, in a fresh session doing nothing else:

```
after get_primary_production() + get_wide_cbs():  rss 21.6 GB   peak 27.7 GB
after gc(full = TRUE):                            rss 20.8 GB
after 3x gc(full = TRUE):                         rss 20.6 GB
live objects kept:                                1.42 GB
```

The build cache is not the cause — it holds 3.14 GB in total:

```
primary_prod__1901__2022   1.22 GB      cbs_built__1901__2022   0.48 GB
primary_prod__1896__2027   1.24 GB      cbs_wide__1901__2022    0.20 GB
```

So ~19 GB is memory R has freed internally but not returned to the OS. It is not
reachable garbage, and no amount of `gc()` recovers it.

## Why it matters

It is a floor under every downstream consumer, paid whether or not that consumer
needs production or CBS again. In `build_carbon_balance(years = 1901:2022)` it is
~20 GB of a 65.6 GB peak (see #624), and it is why reordering that function's
reads cannot help: the floor is already there before the first gridded reader
runs.

It will do the same to any other full-span pipeline built on the same chain.

## Cause

Allocation pattern, not a leak. The chain makes many large short-lived
allocations; R's allocator keeps the freed blocks in its own pools rather than
returning them, and the resident set never comes back down. Nothing here is
holding a reference — `gc()` proves that.

## What would actually fix it

Run the chain in a subprocess and return only the result. The child's entire
address space goes back to the OS on exit, so the parent keeps the 1.4 GB and
none of the 19 GB. That is the standard remedy for allocator fragmentation and
the only one that works without rewriting the chain's allocation pattern.

Costs to weigh before doing it: a dependency (`callr` or similar), serialisation
of the result across the process boundary, and error/progress propagation that
currently comes through `cli` in-process.

The alternative — reducing the number and size of transient allocations inside
`build_primary_production()` / `build_commodity_balances()` — is more invasive
and I have not scoped it.

## Not urgent

`build_carbon_balance()` now completes at 65.6 GB, so nothing is blocked on this.
Filing it so the measurement is not re-derived: the next person to look at a
full-span peak will otherwise spend the time I did concluding that the caches are
to blame. They are not.


## Comment 5396481763

reporter (COLLABORATOR) · lbm364dl · 2026-08-24T14:15:39Z · https://github.com/eduaguilera/whep/issues/777#issuecomment-5396481763

## Re-measured, and the diagnosis needs splitting in three

The symptom reproduces. The conclusion — "no amount of `gc()` recovers it ...
a subprocess is the only remedy that works" — does not. One `malloc_trim(0)`
call recovers most of it, in place, in milliseconds, with every live object
untouched.

Measured at `2005-2015` (a window, not the full span: this box was running
nine other agents and a 28 GB peak was not worth the risk), same chain,
`get_primary_production()` then `get_wide_cbs()`, default configuration:

| checkpoint | resident | live (`gc`) | glibc freed-but-kept |
| --- | --- | --- | --- |
| after both builds | 8.13 GB | 3.58 GB | 3.18 GB |
| after `3x gc(full = TRUE)` | 7.10 GB | 1.45 GB | 4.29 GB |
| after `malloc_trim(0)` | **3.01 GB** | 1.45 GB | 4.29 GB |
| after clearing the build cache + gc | 3.89 GB | 0.33 GB | 5.41 GB |
| after `malloc_trim(0)` | **1.89 GB** | 0.33 GB | 5.41 GB |

Peak RSS 9.41 GB, build 241.9 s. A second independent run agreed to within
0.8 GB at every checkpoint (3.08 GB and 1.96 GB after the two trims).

So the 5.65 GB "floor" after `gc()` is not one thing:

- **4.09 GB is glibc's main arena** holding blocks it has freed and not
  returned. `mallinfo2()` names it exactly (`fordblks` = 4.29 GB), and
  `malloc_trim(0)` hands it back at no runtime cost. `gc()` cannot: freeing
  an R vector calls `free()`, and what `free()` does with the page afterwards
  is glibc's decision, not R's.
- **~1.5 GB is not glibc's at all.** `arrow::default_memory_pool()` is
  **mimalloc** here, and after the parquet reads it reports
  `bytes_allocated = 0.000 GB, max_memory = 1.52 GB` — segments kept by
  arrow's own allocator, which `malloc_trim()` cannot see. Running with
  `ARROW_DEFAULT_MEMORY_POOL=system` removes it (resident after the
  production build: 2.50 GB against 4.40 GB).
- **The rest is live**, and one part of it is a genuine duplicate — see below.

`n64m = 0` at every checkpoint: there are no secondary (per-thread) arenas, so
`MALLOC_ARENA_MAX` and the 16 data.table threads are not implicated.

## The duplicate the cache table is showing

The issue's own cache listing has both `primary_prod__1901__2022` (1.22 GB) and
`primary_prod__1896__2027` (1.24 GB). That is not overhead, it is two builds of
primary production for one request: `get_primary_production(years)` builds the
window asked for, and `get_wide_cbs(years)` builds the `.context_years()`
window (`+/-5`) that the CBS chain needs. Both get cached under their own key.
At `2005-2015` that is `primary_prod__2000__2020` 0.446 GB plus
`primary_prod__2005__2015` 0.294 GB, and a whole extra run of the production
chain in time.

A `years = NULL` request does not pay this — `.cache_key()` keeps the bare key
for both callers, so there is one build. It is only explicit windows, which is
exactly what `build_carbon_balance(years = 1901:2022)` passes.

Deduplicating it means serving the narrow window by filtering the wider build,
and on `main` that changes values: it is the year-scoping identity of #833 /
#625. #844 establishes the identity exactly for primary production at 2010 and
1995, which would make the dedup defensible — but that is a decision for
whoever owns #833, not a mechanical fix, so I have not made it.

## Three remedies, measured

| configuration | build | peak RSS | resident after `gc` | after `malloc_trim(0)` |
| --- | --- | --- | --- | --- |
| as shipped | 241.9 s | 9.41 GB | 7.10 GB | 3.01 GB |
| `ARROW_DEFAULT_MEMORY_POOL=system` | 253.4 s | 8.79 GB | 7.98 GB | 2.50 GB |
| `MALLOC_MMAP_THRESHOLD_=MALLOC_TRIM_THRESHOLD_=131072` | 356.3 s | 7.76 GB | 3.91 GB | 2.91 GB |
| both | 301.2 s | 6.12 GB | 2.90 GB | 1.72 GB |

One run each, on a box running nine other agents: read the time column as
indicative (a repeat of the shipped configuration came in at 196.9 s against
241.9 s) and the memory columns as solid, because those deltas dwarf the
spread.

- Pinning glibc's thresholds stops the arena growing in the first place — large
  blocks go to `mmap` and come back on `free` — so it is the only knob that
  lowers the **peak** as well, at the cost of mmap churn.
- `malloc_trim(0)` reaches the same resting place for free, and does nothing for
  the peak.
- `ARROW_DEFAULT_MEMORY_POOL=system` does not shrink the floor, it makes it
  *reclaimable*: the residue moves out of mimalloc, where nothing can reach it,
  into the arena a trim can return. That is why its `after gc` is *higher* and
  its `after trim` lower.

The subprocess remedy still works, and it is still the only one that also
returns the peak of the chain itself. It is not the only one that works, and it
is not the cheapest.

## Whether it is really a floor under the next phase

"It is ~20 GB of a 65.6 GB peak" is the part of the issue that does not follow
from the measurement, and it is half wrong. Whether the floor adds to a later
phase's peak depends on the **size class** that phase allocates, because that
is what decides whether glibc can reuse the free blocks.

Same session, after the chain and `gc()` (resident 7.27 GB, live 1.45 GB,
4.46 GB free inside the arena), standing in two different 4 GB phase-2 loads:

| phase 2 | resident | growth for 4 GB of new live data | source |
| --- | --- | --- | --- |
| 256 x 16 MB blocks | 8.49 GB | **+1.22 GB** | 2.79 GB came out of the arena's free blocks |
| 8 x 0.5 GB blocks | 10.77 GB | **+3.50 GB** | all fresh `mmap`; arena untouched |

So a tabular consumer largely reuses the floor and pays almost nothing for it,
while a phase allocating half-gigabyte vectors — which is what a gridded reader
does — cannot touch it and pays it in full. `build_carbon_balance()` is in the
second class, so the issue's conclusion happens to hold *there*; the general
claim that it is a floor under "every downstream consumer" does not.

The useful corollary: it is exactly in the second class that a trim between the
phases pays, because the memory the gridded phase cannot reuse is the memory a
trim can return.

## Interaction with #844

#844 takes the yield chain out of the year scoping, so a scoped
`build_primary_production()` reads and computes the whole series and trims. That
moves a scoped build's allocation profile towards a full-range one, and it does
it *twice* per scoped request while the duplicate above stands. The 74.5 s ->
128.6 s the PR reports is the visible half; the memory half is unmeasured, and
every number in this thread was taken on `main` (34e91824), not on that branch.

## What I would and would not do

**Documentation and a harness, not a code change.** Two of the three components
are allocator behaviour, and WHEP's own contribution — the duplicated
primary-production build — cannot be removed without taking a position on the
year-scoping identity that belongs to #833. So #869 ships the measurement and
the recipe, and changes no package code:

- `validation/memory_floor.R` re-derives the split on demand at a configurable
  window: resident/peak from `/proc/self/status`, live from `gc()`, the glibc
  split from `mallinfo2()`, the arrow residue from the pool. It builds the
  two-function `malloc_trim`/`mallinfo2` shim itself; with no compiler or off
  glibc those columns come back `NA` and the live-vs-resident pair still works.
- `validation/README.md` gets the table, the two env-var knobs, and the note
  that `MALLOC_*` must be set in the launching shell — glibc reads them before
  `.Renviron` is parsed, so `~/.Renviron` does nothing for those two.
  `ARROW_DEFAULT_MEMORY_POOL` is the exception and does work from there.

**What I deliberately did not do, and why it is your call.** The one thing that
would make the trim available *inside* WHEP — an exported `whep_release_memory()`
— needs `malloc_trim()`, which R cannot reach without compiled code. That means
a `src/` directory and `NeedsCompilation: yes` for a package that has neither
today, for a helper that is a no-op off glibc. It is ~15 lines and mechanical to
write; it is a packaging decision, not a coding one, so say the word and I will
open it. Given the additivity result above it is the change with the most to
gain: a trim between the tabular and gridded phases of
`build_carbon_balance()` is exactly the case where the freed blocks cannot be
reused anyway.

Numbers here are `main` at 34e91824, R 4.5.2, glibc 2.39, 16 data.table threads,
`2005-2015`.

