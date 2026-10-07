# [F11/R12] demosaic: high_image leaked on the dual-Markesteijn error path

- URL: https://github.com/THEMANNICHOLAS/nico-lightroom/issues/89
- Repo: THEMANNICHOLAS/nico-lightroom (language: C)
- State: open; created 2026-09-16T00:30:47Z; status ok; passes main

## Issue body

reporter (OWNER) · THEMANNICHOLAS · 2026-09-16T00:30:47Z · https://github.com/THEMANNICHOLAS/nico-lightroom/issues/89

**Severity:** Low (was filed Low-Medium) | **Verdict:** CONFIRMED | **Type:** GPU memory leak
**Source:** split from the #41 static memory-safety audit; independently re-verified against source.

### Where
`src/iop/demosaic.c:1825-1834` (cleanup at `finish:` `:1904-1905`).

### What
```c
high_image = dt_opencl_alloc_device(...);
if(IS_NULL_PTR(high_image)) return FALSE;
if(!process_markesteijn_cl(self, pipe, piece, dev_in, high_image, roi_in, roi_in, FALSE)) return FALSE;   // :1829
...
finish:
  dt_opencl_release_mem_object(high_image);
```

### Why it matters
`process_markesteijn_cl` has dozens of `goto error` paths (device-buffer allocations, kernel enqueues) ending in `return FALSE`, and its `error:` label deliberately does not release its `dev_out` argument. The caller's direct `return FALSE` orphans the full-size `cl_mem`, which stays in device memory until context teardown. The RCD dual sibling at `:1811` correctly uses `goto finish`, confirming an oversight.

### Trigger
A kernel/device failure during a Markesteijn demosaic run; repeats if the failure recurs.

### Suggested fix
Replace `return FALSE` at line 1829 with `goto finish;` (`high_image` is initialized NULL and released unconditionally at `finish:`).

### Verification note
No refutation found. Not "per-tile": a FALSE return aborts the pipe, so it is one buffer per failed run.
