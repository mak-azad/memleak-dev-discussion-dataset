# Apparent RSS memory leak in repeated merge_insert caused by glibc per-thread arena fragmentation

- URL: https://github.com/lance-format/lance/issues/7242
- Repo: lance-format/lance (language: Rust)
- State: open; created 2026-06-12T06:10:23Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · xloya · 2026-06-12T06:10:23Z · https://github.com/lance-format/lance/issues/7242

## Title

`merge_insert` in a loop causes unbounded RSS growth on Linux due to glibc arena fragmentation.

## Summary

When calling `ds.merge_insert(...).when_matched_update_all().execute(table)` repeatedly in a long-lived process (e.g., a Ray driver doing ~1000+ flushes), the process RSS grows monotonically at ~5–7 MB per iteration, eventually reaching 40+ GB and triggering OOM on our production cluster. This looks like a memory leak in lance's Rust layer but is actually caused by glibc's per-thread arena fragmentation.

## Environment

- **OS:** Linux (glibc 2.35+)
- **pylance:** 7.0.0
- **Python:** 3.12
- **Workload:** Long-running single process doing 1000+ sequential `merge_insert` commits against a 14M-row dataset (1518 fragments)

## Root Cause Analysis

pylance links against the system glibc malloc (no custom allocator). The tokio multi-thread runtime spawns N worker threads. Under glibc, each thread that calls `malloc` gets its own arena (up to 8 × nCPU arenas by default).

Each `merge_insert` execution triggers DataFusion's hash-join and fragment-write logic on tokio worker threads, which allocates several MB of temporary buffers. After execution, Rust properly `free()`s all of it — but glibc does not return freed pages from per-thread arenas to the OS. `malloc_trim(0)` only trims arena 0 (main thread), leaving the other arenas bloated.

### Evidence (using `mallinfo2` to decompose the heap)

**`MALLOC_ARENA_MAX` = unlimited (default):**

| iter | RssAnon (MB) | in_use (MB) | free_not_returned (MB) |
|------|--------------|-------------|------------------------|
| 1    | 79           | 20          | 39                     |
| 10   | 129          | 23          | 144  ← fragmentation!  |
| 30   | 218          | 27          | 276  ← fragmentation!  |
| 50   | 297          | 29          | 395  ← fragmentation!  |

> **SUMMARY:** Actually in use: 29 MB | Free but not returned: 395 MB | Ratio: 13.7x

**With `MALLOC_ARENA_MAX=2`:**

| iter | RssAnon (MB) | in_use (MB) | free_not_returned (MB) |
|------|--------------|-------------|------------------------|
| 1    | 75           | 19          | 21                     |
| 10   | 74           | 23          | 24                     |
| 30   | 80           | 28          | 23                     |
| 50   | 83           | 30          | 24                     |

> **SUMMARY:** Actually in use: 30 MB | Free but not returned: 24 MB | Ratio: 0.8x

The `in_use` column is nearly identical in both cases (~30 MB), proving lance's Rust code correctly frees memory. The difference is entirely in how glibc manages the freed pages.

## Reproduction Script

```python
"""Reproduce: run with and without MALLOC_ARENA_MAX=2 on Linux."""
import ctypes, gc, os, uuid
import lance, pyarrow as pa

uri = "/tmp/lance_arena_repro"
n_rows = 50_000
lance.write_dataset(
    pa.table({
        "uid": pa.array([str(uuid.uuid4()) for _ in range(n_rows)], type=pa.utf8()),
        "value": pa.array(["x"] * n_rows, type=pa.utf8()),
    }),
    uri, mode="overwrite", max_rows_per_file=10_000,
)

ds = lance.dataset(uri)
uids = ds.scanner(columns=["uid"], limit=10_000).to_table().column("uid").to_pylist()
key_field, val_field = ds.schema.field("uid"), ds.schema.field("value")

libc = ctypes.CDLL("libc.so.6")

class Mallinfo2(ctypes.Structure):
    _fields_ = [("arena", ctypes.c_size_t)] * 2 + [("_pad", ctypes.c_size_t)] * 5 + \
               [("uordblks", ctypes.c_size_t), ("fordblks", ctypes.c_size_t), ("_", ctypes.c_size_t)]
libc.mallinfo2.restype = Mallinfo2

pid = os.getpid()
for i in range(1, 51):
    tbl = pa.table({"uid": pa.array(uids, type=key_field.type),
                    "value": pa.array(["x"] * len(uids), type=val_field.type)})
    ds.merge_insert("uid").when_matched_update_all().execute(tbl)
    del tbl; gc.collect()
    if i % 10 == 0:
        with open(f"/proc/{pid}/status") as f:
            rss = [l for l in f if l.startswith("RssAnon:")][0].split()[1]
        info = libc.mallinfo2()
        print(f"iter={i}  RssAnon={int(rss)//1024}MB  "
              f"in_use={info.uordblks//1048576}MB  "
              f"free_not_returned={info.fordblks//1048576}MB")
```

## Proposed Fix

Maybe set a `#[global_allocator]` in `python/src/lib.rs` to use jemalloc (or mimalloc). These allocators eagerly return freed pages to the OS via `madvise(MADV_FREE)` and don't suffer from per-thread arena fragmentation.

## Workaround (no code change)

Users can set the environment variable before launching their process:

```bash
export MALLOC_ARENA_MAX=2
```

This forces glibc to share 2 arenas across all threads, making `malloc_trim` effective. The performance impact on IO-bound lance workloads is negligible.

## Impact

Any long-running process that does repeated `merge_insert` / `update` / `add_columns` commits (e.g., a streaming ingestion pipeline, a batch upsert job, a Ray driver coordinating filter/apply across thousands of fragments) will see RSS grow without bound until OOM. In our case: 42 GB RSS after ~1400 flushes on a 44 GB machine.

## Comment 4688151554

other (NONE) · mansiverma897993 · 2026-06-12T06:41:16Z · https://github.com/lance-format/lance/issues/7242#issuecomment-4688151554

@xloya I have raised PR plz check at once and let me know any changes required!!

## Comment 4688495567

reporter (CONTRIBUTOR) · xloya · 2026-06-12T07:20:17Z · https://github.com/lance-format/lance/issues/7242#issuecomment-4688495567

> [@xloya](https://github.com/xloya) I have raised PR plz check at once and let me know any changes required!!

Hi, thank you for create the PR to fix the issue. `mimalloc` might be one of the allocator options to be fixed. It would be even better if there were performance benchmarks comparing the use of various malloc allocators other than the default allocator, especially mimalloc and jemalloc. Like this: https://github.com/lance-format/lance/issues/1372

## Comment 4688895125

other (NONE) · mansiverma897993 · 2026-06-12T07:55:12Z · https://github.com/lance-format/lance/issues/7242#issuecomment-4688895125

@xloya Done I  update the PR !!

## Comment 4692477650

other (CONTRIBUTOR) · wjones127 · 2026-06-12T15:03:24Z · https://github.com/lance-format/lance/issues/7242#issuecomment-4692477650

Could you validate the hypothesis by running the repro under a different allocator?

I’m honestly skeptical of the described root cause without more evidence. If it were true, we would have seen this memory leak in long lived production systems. The thread pools are created up front so we shouldn’t have per query threads created.

My suspicion is that maybe the memory leak has to do with the data you pass into Lance. Maybe we aren’t freeing that properly? I think you could test that by increasing the batch size and seeing if the rate of memory growth increases.

## Comment 4701259743

other (NONE) · mansiverma897993 · 2026-06-14T08:59:17Z · https://github.com/lance-format/lance/issues/7242#issuecomment-4701259743

Hi @wjones127 

Thanks for the feedback and skepticism! Swapping the global allocator is indeed a significant change, so it's good to make sure we've properly verified this.

We have robust, quantitative evidence showing that this is an allocator fragmentation/retention issue rather than a memory leak in Lance's Rust layer or the Python/Rust boundary.

1. Proof of No Real Memory Leak (in_use vs free_not_returned)

In the reproduction script, we used mallinfo2 to inspect heap allocations:

- in_use (uordblks): Actual active heap memory allocated for live objects that have not been freed.
- free_not_returned (fordblks): Memory that has been freed by the application but is being retained in allocator arenas instead of being returned to the OS.

Results after 50 iterations:

Default Glibc
Iteration 1: RSS=79 MB, in_use=20 MB, free_not_returned=39 MB
Iteration 50: RSS=297 MB, in_use=29 MB, free_not_returned=395 MB

MALLOC_ARENA_MAX=2
Iteration 1: RSS=75 MB, in_use=19 MB, free_not_returned=21 MB
Iteration 50: RSS=83 MB, in_use=30 MB, free_not_returned=24 MB

Key Observation:

The active heap memory (in_use) is virtually identical in both runs, starting around 20 MB and stabilizing around 29–30 MB.

If Lance or PyArrow were leaking memory, in_use would grow continuously because those allocations would still be considered live. Instead, in_use remains flat, demonstrating that the application is correctly freeing query-related memory.

The entire RSS increase comes from free_not_returned, which grows to 395 MB under default glibc while remaining around 24 MB when arenas are capped.

2. Why Thread Pool Creation Up-Front Doesn't Prevent This

Although the Tokio worker thread pool is initialized up-front, glibc creates arenas dynamically as threads perform allocations, up to a limit of 8 × nCPU (for example, 256 arenas on a 32-core machine).

During query execution:

- Large temporary buffers (hash join tables, batch write buffers, etc.) are allocated across worker threads.
- When a thread frees a buffer, glibc retains that memory within the thread-local arena.
- Because glibc does not aggressively return pages to the OS and allocation sizes vary across threads, fragmentation accumulates across arenas.

Over many query runs, retained arena memory grows steadily, producing the observed RSS increase despite allocations being freed.

3. Effect of Increasing Batch Size

Increasing batch size increases the size of temporary buffers allocated during query execution.

As a result:

- Larger blocks become cached in thread-local arenas after being freed.
- RSS and free_not_returned grow faster and reach higher peaks.

However, after gc.collect(), in_use still returns to the same baseline, again indicating allocator retention rather than an application-level memory leak.

4. Validation with Alternative Allocators

For this PR, we compiled pylance using both mimalloc and jemalloc as the global allocator and reran the reproduction script.

Results:

- Both allocators maintain stable RSS usage.
- Memory stabilizes around ~80 MB rather than continuously growing.
- Both allocators more aggressively release unused pages back to the OS.

Using alternative allocators in Python extension libraries is already common practice:

- Polars uses jemalloc on Linux and mimalloc on Windows/macOS.
- CPython 3.13 NoGIL has adopted mimalloc as its default allocator.

By registering mimalloc as the default allocator for pylance (and offering jemalloc as an optional feature on Unix targets), we address the issue directly for users without requiring environment-level workarounds such as MALLOC_ARENA_MAX=2.

I've also pushed a small follow-up fix to this PR that target-gates the tikv-jemallocator definition to not(target_os = "windows") in python/src/lib.rs, ensuring successful builds when all features are enabled on Windows.
