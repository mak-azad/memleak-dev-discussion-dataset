# RSS stays ~21 GB above what the engine accounts for: freed memory is not returned to the OS

- URL: https://github.com/VoxLogicA-Project/VoxLogicA-2/issues/56
- Repo: VoxLogicA-Project/VoxLogicA-2 (language: Python)
- State: open; created 2026-09-06T14:53:18Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · vincenzoml · 2026-09-06T14:53:18Z · https://github.com/VoxLogicA-Project/VoxLogicA-2/issues/56

After the loop expander stopped materializing whole sequences, the engine's own
accounting drops to 1.9 GB while the process keeps 23-30 GB resident. The gap
is memory the engine has released and the allocator has not given back.

## Measured

`brats026_4mod_309.imgql`, 309 cases, 4 modalities, on fmt-5000, engine at
`fbd0e15`. Columns are the engine's own memory log:

| t | accounted | RSS | gap |
|---|---|---|---|
| 5 s | 22.8 GB | 27.3 GB | 4.5 GB |
| 115 s | 1.9 GB | 30.6 GB | **28.7 GB** (peak) |
| 606 s | 1.9 GB | 26.6 GB | 24.6 GB |
| 1806 s | 1.9 GB | 24.1 GB | 22.2 GB |
| 2406 s | 1.9 GB | 23.3 GB | 21.3 GB |

`RssAnon` is 24.4 GB of a 24.4 GB `VmRSS`; file-backed is 11 MB. nnU-Net's
dataloader workers are separate processes (3.5 GB, not counted above).

## It is retained heap, not PyTorch

At 115 s the gap was already 28.7 GB and the GPU was at 0% -- training had not
started. The residency is what image production left behind, not what nnU-Net
allocated.

The reassuring half: when training did start, RSS **fell** (30.6 -> 23.3 GB)
rather than rising. nnU-Net is allocating INTO the retained heap instead of on
top of it, so the memory is reusable by this process. Nothing is leaking in the
sense of being unreachable.

## Why it still matters

On a shared machine the process looks like it holds 23 GB. The OOM killer reads
RSS, not our accounting, so a run that is genuinely small can be killed for
memory that is free-but-unreturned -- and other users' work with it. This host
is shared with two other people's trainings.

## What to try

`malloc_trim(0)` after a large release -- the engine already knows when one
happened, since `_reclaim_memory` and the eviction paths are the only places
that free at this scale. It belongs there and not in an environment variable
(`MALLOC_TRIM_THRESHOLD_` and friends are exactly the kind of outside knob
AGENTS.md forbids as a fix).

Worth checking first whether the retention is glibc arena fragmentation from
many large short-lived buffers, in which case the buffer pool's own reuse may
already be the better lever, and a trim would only paper over it.

## How to measure it

The engine's memory log already carries both numbers, so the gap is
`rss_mb - accounted_mb` per sample. Compare the peak gap and the gap at steady
state, same program, same machine, with and without the trim.

## Comment 5560045468

reporter (CONTRIBUTOR) · vincenzoml · 2026-09-06T14:55:02Z · https://github.com/VoxLogicA-Project/VoxLogicA-2/issues/56#issuecomment-5560045468

Measured, and the mechanism is now isolated. `malloc_trim` is the right lever
after all -- the first experiment that said otherwise was the flawed one.

## Where the memory is

On the live run (`brats026_4mod_309.imgql`, 40 minutes in, accounted 1.9 GB):

```
Rss  24,402,636 kB   Pss_Anon 24,391,108 kB   Pss_File 1,610 kB
[heap]                18.6 GB
everything else        4.7 GB   (largest single anonymous mapping: 2.0 GB)
```

So it is the **brk heap**, not a set of large mappings.

## Why, and why the first test missed it

glibc mmaps allocations above its mmap threshold and munmaps them on free, so a
4 MB image buffer is returned immediately -- which is what the first experiment
showed, and it was measuring the wrong regime. glibc RAISES that threshold
dynamically to the size of any mmap-ed block it frees. One freed 4 MB buffer is
enough; from then on buffers of that size come from the heap, and freed heap is
not returned.

Controlled experiment on the same host and interpreter, 1000 buffers of 4 MB,
after one warm-up allocate-and-free to raise the threshold:

| stage | RSS | `[heap]` |
|---|---|---|
| peak | 3.94 GB | 3.91 GB |
| after `del` + `gc.collect()` | 3.94 GB | 3.91 GB |
| after `malloc_trim(0)` | **0.04 GB** | **0.00 GB** |

Freeing returned nothing. The trim returned 3.90 of 3.91 GB.

That is exactly the shape of this workload: many image-sized buffers, allocated
and freed repeatedly, after the first free has moved them all into the heap.

## What to do

Call `malloc_trim(0)` after a large release. The engine already knows when one
happened -- `_reclaim_memory` and the eviction paths are the only places that
free at this scale -- so it belongs there, on a threshold of bytes released,
not on every eviction (the call walks the heap's free lists and is not free).

Not an environment variable: `MALLOC_MMAP_THRESHOLD_` would also pin the
threshold and prevent the migration into the heap, but that is an outside knob
configuring correctness, which AGENTS.md rules out as a fix.

## How the next run will show it

The engine's memory log carries both numbers, so the gap is
`rss_mb - accounted_mb` per sample. On this run: 28.7 GB peak gap, 21.3 GB at
steady state, against an accounted 1.9 GB. Same program, same machine, with the
trim, is the comparison.

## Comment 5560060045

reporter (CONTRIBUTOR) · vincenzoml · 2026-09-06T14:57:36Z · https://github.com/VoxLogicA-Project/VoxLogicA-2/issues/56#issuecomment-5560060045

Measured the cost, and the conclusion reverses: **do not trim.** The retained
heap is earning its keep.

Same host and interpreter, 2 GB in 4 MB pieces, allocate / free / reallocate
and touch every page, alternating:

| | RSS while idle | reallocate + touch 2 GB |
|---|---|---|
| heap kept | 1.99 GB | **7 ms** |
| after `malloc_trim(0)` | 0.04 GB | **172-190 ms** |

Giving the heap back costs about 25x on the next allocation -- roughly 90 ms
per GB re-faulted, so ~1.8 s for a 20 GB heap. Negligible once in a six-hour
run, ruinous if the engine trimmed after each reclaim wave: at 170 nodes/s with
image buffers allocated and freed continuously, every 7 ms reallocation becomes
180 ms.

There is also direct evidence from the run this issue is about. When nnU-Net
training started, RSS FELL from 30.6 to 23.3 GB: the training allocated INTO
the retained heap instead of on top of it. The retention was not waste, it was
reuse.

## What stands

The observation is still true -- RSS sits ~21 GB above what the engine accounts
for, and the Linux OOM killer reads RSS, not our accounting, so on a shared
machine a genuinely small run can be killed for memory that is free. That is
worth knowing and worth not being surprised by.

But the fix proposed above is worse than the problem in the general case. The
only defensible version is far narrower: trim when the engine KNOWS it has
entered a long phase that will not allocate -- one node in flight, ready queue
empty, sustained -- which is exactly the state of a run sitting inside
`nnunet.train_internal` for forty minutes. That is a heuristic, and a heuristic
that fires wrongly costs 25x, so it needs a real case before it is worth
writing.

Leaving this open as the record of the measurement rather than as work to do.
