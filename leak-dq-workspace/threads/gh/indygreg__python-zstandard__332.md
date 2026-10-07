# ZstdDecompressor.decompress: excessive allocation (crash) on 13-byte malformed frame (decompressor.c:335); should raise ZstdError

- URL: https://github.com/indygreg/python-zstandard/issues/332
- Repo: indygreg/python-zstandard (language: C)
- State: open; created 2026-08-10T08:05:01Z; status ok; passes main

## Issue body

reporter (NONE) · plotarmordev · 2026-08-10T08:05:01Z · https://github.com/indygreg/python-zstandard/issues/332

## Repo
[indygreg/python-zstandard](https://github.com/indygreg/python-zstandard)

## Summary
`ZstdDecompressor().decompress()` pre-allocates the full Frame_Content_Size (FCS) from the frame header WITHOUT capping; a 13-byte malformed frame declaring a corrupt FCS makes it call `PyBytes_FromStringAndSize` for a ~1.1 TB buffer at `c-ext/decompressor.c:335`, causing an ASan **allocation-size-too-big ABORT** (in production: a huge `MemoryError`) — i.e. a crash/DoS on a tiny untrusted decompression input, rather than the documented `ZstdError`.

## Trigger (13 bytes)
hex: `28b52ffde06c06060663636363`

## Evidence
ASan (binding C-ext built with `-fsanitize=address`):
```
ERROR: AddressSanitizer: requested allocation size 0x66c6c6c00000121 exceeds maximum supported size
    #3 PyBytes_FromStringAndSize
    #4 Decompressor_decompress c-ext/decompressor.c:335
SUMMARY: AddressSanitizer: allocation-size-too-big
ABORTING
```

## Expected
The Frame_Content_Size field of a malformed/short frame must not cause an over-allocation; the decompressor should reject such input (raise `ZstdError` / cap the buffer & grow dynamically), as single-shot malloc of an attacker-controlled FCS is unsafe (CWE-789).

## Note
This binding C-ext path is NOT covered by OSS-Fuzz (only upstream zstd core is) and has no advisory.

