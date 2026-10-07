# darktable-cli: `-t N` below the CPU count corrupts the heap

- URL: https://github.com/darktable-org/darktable/issues/22436
- Repo: darktable-org/darktable (language: C)
- State: open; created 2026-09-29T04:30:44Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · kofa73 · 2026-09-29T04:30:44Z · https://github.com/darktable-org/darktable/issues/22436

**TL;DR:** GraphicsMagick's initialization resets the OpenMP thread count that
`-t N` set, so parallel loops on the main thread run with more threads than
the per-thread buffers were sized for. darktable-cli then crashes. One-line
fix: re-apply the thread count after the Magick init in `dt_init()`.

## Reproduce

On a machine with more than 4 CPUs, with a GraphicsMagick build:

```
darktable-cli src/tests/integration/images/xtransIV.raf out.png \
  --core --disable-opencl -t 4 --configdir /tmp/dtcfg
```

Result: `free(): invalid size`, `munmap_chunk(): invalid pointer`, or SIGSEGV.
Without `-t`, or with `-t` equal to the CPU count, the export works.

## Cause

1. `dt_init()` calls `omp_set_num_threads(N)` (`src/common/darktable.c:1668`).
2. Later, `InitializeMagickEx()` (`:2052`) calls `omp_set_num_threads()` with
   the CPU count, through `InitializeMagickResources()`.
3. `dt_get_num_threads()` still returns N, so the pools from
   `dt_alloc_perthread()` hold N slots, but OpenMP starts one thread per CPU.
   Threads N and up write past the end (e.g. X-Trans Markesteijn/FDC
   demosaic).

The pipe worker threads in the GUI set their own thread count
(`src/control/jobs.c`), so the GUI is not affected. darktable-cli renders
on the main thread.

## Fix

After the GraphicsMagick / ImageMagick init block in `dt_init()`:

```c
#ifdef _OPENMP
  // InitializeMagickResources() sets the thread count to the number of CPUs
  omp_set_num_threads(darktable.num_openmp_threads);
#endif
```

Tested on a 12-CPU machine: `-t 1`, `-t 4` and `-t 8` then succeed.

## Notes

- The integration test runner is not affected: it exports
  `OMP_THREAD_LIMIT=4` alongside `-t 4`. Running a test's command by hand
  without it crashes on `0068`, `0100` and `0145` (X-Trans).
- Whether the bug appears depends on init order. If G'MIC's static
  constructor initializes GraphicsMagick before `dt_init()`, darktable's
  setting comes last and nothing overflows.
- Related: #13727 / PR #13736 clamped `-t` to the CPU count, which fixed
  `-t` above the CPU count, not below it.
- Not checked: ImageMagick builds (`MagickWandGenesis()`).

