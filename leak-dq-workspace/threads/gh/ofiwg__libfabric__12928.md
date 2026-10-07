# core: default FI_PROVIDER_PATH crashes - invalid free

- URL: https://github.com/ofiwg/libfabric/issues/12928
- Repo: ofiwg/libfabric (language: C)
- State: closed; created 2026-09-30T12:56:33Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · codambro · 2026-09-30T12:56:33Z · https://github.com/ofiwg/libfabric/issues/12928

**Describe the bug**
seeing CXI criterion tests all failing with a crash for `munmap_chunk(): invalid pointer`
First introduced in commit:
e1fa856913284582fe7d338f327619dc6810d38b

**To Reproduce**
Running CXI provider libfabric criterion tests all crash

**Expected behavior**
Tests pass

**Output**
```
libfabric:79499:1790705302::core:core:ofi_load_dl_prov():828<info> default provider directory: "/scratch/libfabric-e1fa85691328/build/lib/libfabric"
libfabric:79499:1790705302::core:core:fi_param_get_():373<info> variable provider_path=<not set>
munmap_chunk(): invalid pointer
[----] prov/cxi/test/cuda.c:584: Unexpected signal caught below this line!
[FAIL] cuda::dmabuf_stress: CRASH!
```


**Additional context**
From copilots analysis:

Looking at `fabric.c`, the new `ofi_default_provdir()` / `ofi_find_prov_libs()` code has two problems, and both fit the log (the crash happens after `fi_param_get_` returns, i.e. inside the `!provdir` branch, whose inner logs are all `FI_DBG` so nothing else prints at `info` level).

*1. `free()` on a pointer that may be a string literal — the direct `munmap_chunk(): invalid pointer` candidate*

`ofi_default_provdir()` returns one of two kinds of pointer:

heap (`malloc`'d `tmp`) when `dladdr()` succeeds and the path contains a separator
the compile-time constant `PROVDLDIR` in every other case (dladdr fails, no `/` in `dli_fname`, or the `malloc` fails and it hits `goto out`)
But `fabric.c:916` unconditionally does `free(def_provdir)`. Freeing `.rodata` is exactly what glibc reports as `munmap_chunk(): invalid pointer`. The function needs to either always `strdup()` the fallback, or return an "is owned" flag.

Related, `strdup()`'s result is passed to `strrchr()` without a NULL check.

*2. `ofi_find_prov_libs()` can pull in a second copy of the provider*

The `!provdir` path now calls `ofi_find_prov_libs()` before scanning `def_provdir`. That builds `lib<prov>-fi.so` names and `dlopen`s them off the default loader search path (`LD_LIBRARY_PATH`/rpath). In the CXI unit-test environment that very likely resolves to an installed/stale `libcxi-fi.so` while the test binary already has the in-tree cxi provider, so you get the same provider registered twice from two different `libfabric` images. That both explains "problems getting the default provider info for the cxi provider" (wrong/duplicate `fi_info` from the stale copy) and produces cross-heap free/double-free crashes like the one in `cuda::dmabuf_stress`.

Quick way to confirm which one it is: run the test with `FI_PROVIDER_PATH` set explicitly to the build dir. If the crash disappears, it's #2 (`ofi_find_prov_libs` is skipped); if it still crashes, note that the explicit-path branch also falls through to `free(def_provdir)`, so check with `FI_LOG_LEVEL=debug` whether a second `libcxi-fi.so` gets opened. Running under `valgrind` or with `MALLOC_CHECK_=3` will point at the exact free.




## Comment 5913716101

other (NONE) · SeanP-2023 · 2026-09-30T14:50:17Z · https://github.com/ofiwg/libfabric/issues/12928#issuecomment-5913716101

copilot found the issue quickly, here is what it said after we set the FI_PROVIDER_PATH:

libfabric:489:1790721418::core:core:ofi_load_dl_prov():828<info> default provider directory: "/scratch/pollards/hpc-shs-devbootstrap/libfabric/install/lib/libfabric"
libfabric:489:1790721418::core:core:fi_param_get_():382<info> read string var provider_path=/scratch/pollards/hpc-shs-devbootstrap/libfabric/install/lib/libfabric
free(): invalid pointer
[----] Warning! The test `domain::simple` crashed during its setup or teardown.
[====] Synthesis: Tested: 1 | Passing: 0 | Failing: 1 | Crashing: 1
(.venv) (none):/scratch/pollards/hpc-shs-devbootstrap/libfabric/prov/cxi/test #

That log nails it. Two things confirm the diagnosis:

1. The crash is free(def_provdir), and def_provdir is a string literal.

PROVDLDIR is -DPROVDLDIR=\"$(pkglibdir)\" in Makefile.am, i.e. $(libdir)/libfabric — which for your build is exactly /scratch/pollards/hpc-shs-devbootstrap/libfabric/install/lib/libfabric. That is character-for-character what got printed as "default provider directory". So ofi_default_provdir() returned the .rodata constant, not a malloc'd string (either dladdr() returned 0, or it fell through goto out after a failed malloc). Your earlier log is the same story: /scratch/libfabric-e1fa85691328/build/lib/libfabric is that build's pkglibdir.

Then fabric.c:916 does an unconditional free(def_provdir) → free(): invalid pointer.

2. The timing matches exactly.

The last thing logged is read string var provider_path=..., then the crash. Nothing in between: no registering provider, no dlopen warning. So it never got as far as actually loading anything — it split the string, scanned, and died at the free. That's also why setting FI_PROVIDER_PATH didn't help: the free(def_provdir) is on every path, including the explicit-path branch.

So the earlier "duplicate provider via ofi_find_prov_libs()" theory is secondary — this is a straight ownership bug in the new ofi_default_provdir() helper: it returns either heap memory or a compile-time constant, and the caller always frees it.

The fix is to make ownership unambiguous — have ofi_default_provdir() return strdup(PROVDLDIR) on every fallback path (and handle strdup failure by skipping the free), or return a separate bool owned out-param. Also worth fixing while you're in there: strdup(info.dli_fname) result is dereferenced by strrchr() without a NULL check, and goto out on malloc failure leaks nothing but silently returns the literal. copilot fixed the issue and now our test is no longer crashing, I can upload the diff file for reference to a perm fix for the problem

## Comment 5914049941

other (NONE) · SeanP-2023 · 2026-09-30T15:08:39Z · https://github.com/ofiwg/libfabric/issues/12928#issuecomment-5914049941

[def_prov_patch.txt](https://github.com/user-attachments/files/32862811/def_prov_patch.txt)

## Comment 5914122811

other (CONTRIBUTOR) · ooststep · 2026-09-30T15:12:50Z · https://github.com/ofiwg/libfabric/issues/12928#issuecomment-5914122811

Thanks for the report.  The secondary finding is benign.  Providers will be prioritized either by version or by discovery order if that feature is requested (defining '@' in FI_PROVIDER_PATH). System level installed providers (discovered during `ofi_find_prov_libs()`, would be deprioritized in these cases.

My PR #12930 should address the other, real, discoveries - plus a couple others I noticed while adding the fixes.

## Comment 5914778734

other (NONE) · SeanP-2023 · 2026-09-30T15:50:37Z · https://github.com/ofiwg/libfabric/issues/12928#issuecomment-5914778734

I re-ran with your PR and our test passes. Thanks!
