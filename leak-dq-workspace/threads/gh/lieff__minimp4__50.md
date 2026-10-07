# Heap buffer overflow via integer overflow in stsz/stts malloc size (CWE-190/CWE-122)

- URL: https://github.com/lieff/minimp4/issues/50
- Repo: lieff/minimp4 (language: C)
- State: open; created 2026-02-17T03:41:12Z; status ok; passes main

## Issue body

reporter (NONE) · ByamB4 · 2026-02-17T03:41:12Z · https://github.com/lieff/minimp4/issues/50

## Summary

Multiple heap buffer overflow vulnerabilities exist in `MP4D_open()` caused by 32-bit integer overflow in `malloc` size calculations. The multiplications `sample_count * 4` and `ts_count * 4` use 32-bit unsigned arithmetic even on 64-bit systems, allowing an attacker to allocate a small buffer while the subsequent loop writes far beyond it.

## Root Cause

In `minimp4.h`, the `MALLOC` macro performs:
```c
#define MALLOC(t, p, size) p = (t)malloc(size); if (!(p)) { ERROR("out of memory"); }
```

The `size` argument is computed using 32-bit arithmetic before being widened to `size_t` for `malloc()`.

### Vulnerable site 1: `stsz` box (line ~2810)

```c
tr->sample_count = READ(4);           // attacker-controlled, unsigned int (32-bit)
MALLOC(unsigned int*, tr->entry_size, tr->sample_count * 4);  // 32-bit overflow!
for (i = 0; i < tr->sample_count; i++) {
    tr->entry_size[i] = (sample_size ? sample_size : READ(4));
}
```

- `tr->sample_count` is `unsigned int` (32-bit)
- The literal `4` is `int` (32-bit)
- The multiplication `unsigned int * int` produces `unsigned int` (32-bit), which overflows at 2^32
- This 32-bit result is then implicitly widened to `size_t` for `malloc` — but the overflow has already occurred

**Critically**, when `sample_size != 0`, the loop writes `sample_size` to every entry WITHOUT calling `READ()`, so the loop is not bounded by `payload_bytes`/EOF. This allows the full overflow to be exploited.

### Vulnerable site 2: `stts` box (line ~2858)

```c
unsigned count = READ(4);
unsigned ts_count = count;
MALLOC(unsigned int*, tr->timestamp, ts_count * 4);   // 32-bit overflow!
MALLOC(unsigned int*, tr->duration,  ts_count * 4);    // 32-bit overflow!
```

Same root cause. The realloc guard `if (k + sc > ts_count)` uses `sizeof(unsigned)` (which is `size_t` on 64-bit), but the initial allocation has already overflowed.

## Proof of Concept

Craft an MP4 file containing an `stsz` box with:
- `sample_size = 1` (non-zero, so entries are filled without reading from file)
- `sample_count = 0x40000001`

Result:
1. `malloc(0x40000001 * 4)` → `malloc(0x00000004)` due to 32-bit truncation → allocates **4 bytes**
2. Loop runs `0x40000001` iterations, writing `tr->entry_size[i] = 1` for each
3. After index 0, all writes are **out of bounds** → **heap buffer overflow write**

The attacker controls both the value written (`sample_size`) and the number of OOB writes. This is sufficient for arbitrary code execution via heap metadata corruption.

## Impact

- **Type**: Heap buffer overflow write (CWE-122) via integer overflow (CWE-190)
- **Severity**: High (CVSS ~8.8 — attacker crafts malicious MP4 file)
- **Exploitability**: High — attacker controls write value and count; no ASLR/heap layout knowledge needed for DoS, standard heap exploitation techniques for RCE
- **Attack vector**: User opens crafted `.mp4` file with any application using minimp4 for demuxing

## Suggested Fix

Use `(size_t)` cast to force 64-bit arithmetic on 64-bit systems:

```diff
- MALLOC(unsigned int*, tr->entry_size, tr->sample_count * 4);
+ MALLOC(unsigned int*, tr->entry_size, (size_t)tr->sample_count * sizeof(unsigned int));
```

```diff
- MALLOC(unsigned int*, tr->timestamp, ts_count * 4);
- MALLOC(unsigned int*, tr->duration,  ts_count * 4);
+ MALLOC(unsigned int*, tr->timestamp, (size_t)ts_count * sizeof(unsigned int));
+ MALLOC(unsigned int*, tr->duration,  (size_t)ts_count * sizeof(unsigned int));
```

Additionally, consider adding a sanity check on `sample_count` (e.g., rejecting values > some reasonable maximum like 100M samples, or validating against `payload_bytes`).

## Additional: avcC box overflow

The `BOX_avcC` handler (line ~3028) allocates `malloc((size_t)box_bytes)` for `tr->dsi`, then writes SPS/PPS data via `*p++` in loops controlled by `numOfSequenceParameterSets` and `sequenceParameterSetLength` from the file. These lengths are not validated against the allocation size. When the sum of declared SPS/PPS lengths exceeds `box_bytes`, the writes go past the allocated buffer.

## Environment

- minimp4 version: latest (main branch, Feb 2026)
- Discovered via: manual source code audit
- Affects: 32-bit and 64-bit platforms (the overflow is in 32-bit unsigned arithmetic regardless of platform word size)

## Comment 4148251369

other (NONE) · YongRui0402 · 2026-03-28T15:20:18Z · https://github.com/lieff/minimp4/issues/50#issuecomment-4148251369

Fixed in maintained fork: https://github.com/YongRui0402/minimp4

Cast malloc size calculations to `(size_t)` to prevent 32-bit integer overflow in stsz/stts/stsc/stco handlers. Also added sanity check on sample_count.
