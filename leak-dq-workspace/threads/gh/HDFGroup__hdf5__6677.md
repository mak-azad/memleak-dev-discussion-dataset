# Malformed file leaves library shutdown unable to converge ("infinite loop closing library"), ~1.6MB leaked

- URL: https://github.com/HDFGroup/hdf5/issues/6677
- Repo: HDFGroup/hdf5 (language: C)
- State: open; created 2026-09-19T15:37:50Z; status ok; passes main

## Issue body

reporter (NONE) · x4evexnol · 2026-09-19T15:37:50Z · https://github.com/HDFGroup/hdf5/issues/6677

## Summary

Opening a specific class of malformed HDF5 file and then closing the library (`H5close()` / the `LLVMFuzzerTestOneInput` teardown path used by `test/fuzz/h5_read_fuzzer.c`) causes the shutdown loop in `H5.c` to never reach `pending == 0` within its 100-iteration cap:

```c
} while (pending && ntries++ < 100);

if (pending) {
    fprintf(stderr, "HDF5: infinite loop closing library\n");
    ...
}
```

It gives up, prints `HDF5: infinite loop closing library`, and LeakSanitizer confirms **1,643,732 bytes across 18 allocations** are never freed.

## Severity / impact

Not a security vulnerability — this is a bounded, one-time leak, not an accumulating one. I tested running the same malformed file twice in one process, and running it alongside 7 *other* distinct malformed files in the same process: all three cases leak the exact same 1,643,732 bytes / 18 allocations, no more. So this doesn't grow into a memory-exhaustion vector in a long-running process. But some internal bookkeeping (looks ID/type-registry related, given the shutdown loop is tearing down `H5I`, `H5T`, etc. in dependency order) is clearly left in a state the shutdown path can't resolve, which seems worth fixing on correctness grounds — and the warning message is user-visible noise for any embedding application every time this input shape is hit.

## Reproduction

Built with `-fsanitize=address,undefined -fno-sanitize-recover=all` disabled (recovering mode, so the process reaches the close path instead of aborting on the first UBSan report) against current `develop` (commit `7489f285bee1b597586ccd660228376890a00ab4`), then ran the fuzz target on a malformed `.h5` file:

```
$ ASAN_OPTIONS=detect_leaks=1 h5_read_fuzzer repro.h5
...
HDF5: infinite loop closing library
SUMMARY: AddressSanitizer: 1643732 byte(s) leaked in 18 allocation(s).
```

I minimized the triggering input from a 2,749-byte fuzzer-found seed down to 1,674 bytes with `libFuzzer -minimize_crash=1`; it still reproduces the identical leak byte-for-byte. I didn't attach the binary file here since it's a raw malformed `.h5` blob, but I'm happy to share it directly (e.g. by email, or paste as a base64/hex block) if that's useful for triage — just let me know the preferred channel.

## Notes

This was found via an automated fuzzing/sanitizer research pipeline replaying a stored corpus against a sanitizer-instrumented rebuild of upstream `develop`, independent research (not affiliated with the project).

## Comment 5762829913

other (CONTRIBUTOR) · mattjala · 2026-09-21T15:14:14Z · https://github.com/HDFGroup/hdf5/issues/6677#issuecomment-5762829913

Please do attach the malformed .h5 file to this issue -  it will be extremely difficult for us to replicate this and confirm a fix without it.

## Comment 5763791235

reporter (NONE) · x4evexnol · 2026-09-21T16:19:54Z · https://github.com/HDFGroup/hdf5/issues/6677#issuecomment-5763791235

Here is the repro file (base64-encoded inline). Save and decode with: `base64 -d > close_leak_repro.h5` then pipe in the block below.

Quick repro: build `h5_read_fuzzer` with `-fsanitize=address,undefined -fsanitize-recover=all` at `develop` commit `7489f285`, run `ASAN_OPTIONS=detect_leaks=1 ./h5_read_fuzzer close_leak_repro.h5`, expect `HDF5: infinite loop closing library` + `1,643,732 byte(s) leaked in 18 allocation(s)`.

```
SIlIREYNChoKAQAAEAAgICDFIAEABQAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP////////////////////////////////8AAAAAAAAAAAAAACAAAAAA/wAAAAAAAAAAAAAA/+QAAAARAAAAAAAAAAAAAAAAbG9nAAAAAAAAAAD/////////////AAAAAAAAAAAAAAAAABIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP/kAAAAAAAAAAAAAAAAAAAAAGxvZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//wAAAABIiUhERg0KGgoBAAAQACAgIMUgAgQFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/////////////////////////////////wAAAAAAAAAgAAAAAP8AAAAAAAAAAGtra2sNChoKYv///////////////////////////////////////////wAAAAAAAAAAAAAAAAASAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/AAAAAAAAAABra2trDQoaCmL///////////////////////////////////////////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/+QAAAAAAAAAAAAAAAAAAAAAbG9nAAAAAH//AAAAAAAAAAAAc3RkaW8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODg4ODAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP8AAAAAAAAAAGtra2sNChoKYv///////////////////////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABra2trDQoaCmL//////////////////////////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAACLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLiwAAAADqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABra2trDQoaCmL///////////////////////////////////////////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/+QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```
