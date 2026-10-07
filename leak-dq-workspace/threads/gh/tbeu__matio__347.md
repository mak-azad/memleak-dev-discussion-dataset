# allocation-size-too-big in InflateRankDims via ReadNextStructField

- URL: https://github.com/tbeu/matio/issues/347
- Repo: tbeu/matio (language: C)
- State: open; created 2026-09-13T05:55:41Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · kingkingkingson · 2026-09-13T05:55:41Z · https://github.com/tbeu/matio/issues/347

## Summary

`matdump -d` on a crafted compressed MAT5 struct asks `InflateRankDims` to `calloc` a file-controlled rank (`0x1ffffffc0` bytes). AddressSanitizer aborts with `allocation-size-too-big`. The rank comes from the zlib-compressed struct field header in `ReadNextStructField` and is not capped before the allocation.

## Affected version

- Repository: https://github.com/tbeu/matio
- Version: **1.6.0** (cloned `master` HEAD)
- Branch: `master`
- Commit: `b1355a2b4532766d04eafa00299168c76fcf452f`
- CWE: CWE-770 / CWE-400
- Error class: **allocation-size-too-big**
- Site: `InflateRankDims / src/inflate.c:220 ← ReadNextStructField / src/mat5.c:1736`

## Build

Need HDF5 + zlib so `matdump` can read compressed MAT5. AddressSanitizer with `allocator_may_return_null=0` (default abort) makes the oversized `calloc` visible. The hitting input is stored as `input.sav` but is fed to `matdump` as a MAT file.

```bash
sudo apt-get install -y cmake gcc libhdf5-dev zlib1g-dev
git clone https://github.com/tbeu/matio.git && cd matio
git checkout b1355a2b4532766d04eafa00299168c76fcf452f

cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DCMAKE_INSTALL_PREFIX="$PWD/install" \
  -DCMAKE_C_FLAGS="-fsanitize=address,undefined -fno-omit-frame-pointer -g" \
  -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address,undefined" \
  -DCMAKE_SHARED_LINKER_FLAGS="-fsanitize=address,undefined"
cmake --build build --parallel
cmake --install build
```

## Reproduce

```bash
export PREFIX="$PWD/install"
export ASAN_OPTIONS="allocator_may_return_null=0:max_allocation_size_mb=256:detect_leaks=0"

"$PREFIX/bin/matdump" -d input.sav
```

Expected: `SUMMARY: AddressSanitizer: allocation-size-too-big` in `__interceptor_calloc`, stack through `InflateRankDims` ← `ReadNextStructField`.

## Sanitizer evidence

```
==953==ERROR: AddressSanitizer: requested allocation size 0x1ffffffc0 (0x200000fc0 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000 (thread T0)
    #0 0x7f156b244a57 in __interceptor_calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:154
    #1 0x7f156ab77b13 in InflateRankDims /src/matio/src/inflate.c:220
    #2 0x7f156ac4ee7f in ReadNextStructField /src/matio/src/mat5.c:1736
    #3 0x7f156ac6d8c2 in Mat_VarReadNextInfo5 /src/matio/src/mat5.c:6628
    #4 0x7f156ab70893 in Mat_VarReadNextPredicate /src/matio/src/mat.c:3063
    #5 0x55a9fd5e1db5 in main /src/matio/tools/matdump.c:1883

==953==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:154 in __interceptor_calloc
```

## Suggested fix

In `InflateRankDims` / `ReadNextStructField`, reject file-controlled `rank` values that cannot produce a reasonable `dims` allocation (the function already has a `rank > 13` check on some paths; apply a similar bound before `calloc`).

[input.sav.zip](https://github.com/user-attachments/files/32155545/input.sav.zip)
