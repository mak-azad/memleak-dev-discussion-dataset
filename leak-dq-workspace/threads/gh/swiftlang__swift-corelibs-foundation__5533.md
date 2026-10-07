# Invalid free in ISO8601DateFormatter's lazy CFDateFormatter creation on Linux (heap corruption → delayed random segfaults)

- URL: https://github.com/swiftlang/swift-corelibs-foundation/issues/5533
- Repo: swiftlang/swift-corelibs-foundation (language: C)
- State: open; created 2026-08-27T14:26:49Z; status ok; passes main

## Issue body

reporter (NONE) · JonCox · 2026-08-27T14:26:49Z · https://github.com/swiftlang/swift-corelibs-foundation/issues/5533

> ⚠️ **Correction (see comment below):** the causal attribution of our production segfaults to this bug has been withdrawn — they continued unchanged after the workaround. The invalid free itself stands exactly as reported.

> *This report and the underlying investigation — the production triage, the crash-handler experiments, the AddressSanitizer canary that captured the fault on live traffic, and the offline symbolication — are the work of **Claude Fable 5** (Anthropic), running in Claude Code, directed by me.*

## Summary

On Linux, the first use of an `ISO8601DateFormatter` in our Vapor server performs an **invalid free** inside its lazy CF object creation. AddressSanitizer reports `attempting free on address which was not malloc()-ed`, with the free originating in `CFLocaleCreateLocaleIdentifierFromComponents`, reached via `CFDateFormatterCreateISO8601Formatter` → `CFCalendarCreateWithIdentifier` → `__CFCalendarCreateUCalendar`.

Without ASan, that single wild free silently corrupts allocator state, and the process then segfaults at an arbitrary later allocation. ~~In our production service this manifested as roughly **50 random SIGSEGVs over two days** (one per instance-lifetime, minutes to hours after boot, on arbitrary threads and endpoints). Notably, many of the resulting segfaults occurred in contexts where no userspace signal handler could run (not even a minimal first-line `write(2)`-only handler installed ahead of the Swift runtime's backtracer), so the crashes were completely silent — worth knowing for anyone else chasing "impossible" silent segfaults on Cloud Run or similar.~~ *[Correction: our production segfaults continued unchanged after removing `ISO8601DateFormatter` entirely, so they have a separate, still-unidentified cause and this attribution was wrong. The corruption potential of the invalid free itself is unaffected.]*

Replacing the `ISO8601DateFormatter` instances with equivalently-configured `DateFormatter`s (byte-identical output) eliminated the ASan report ~~and the production crashes entirely (verified via an ASan canary at 10% production traffic, then a fixed build at 100% — zero crashes since, against a prior rate of 2–4/hour)~~. *[Correction: it eliminated the ASan report only; the production crashes continued.]*

## ASan report (production traffic, within ~1s of the first request exercising the path)

```
==1==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7bb7e0002f80 in thread T10
    #0 0x556ffa4bee96  (/app/Run+0x1064e96)   ___interceptor_free
    #1 0x556ffe4fcc25  (/app/Run+0x50a2c25)   CFLocaleCreateLocaleIdentifierFromComponents
    #2 0x556ffe4d2468  (/app/Run+0x5078468)   __CFCalendarCreateUCalendar
    #3 0x556ffe4d31f2  (/app/Run+0x50791f2)   _CFCalendarInitialize
    #4 0x556ffe4d2f0e  (/app/Run+0x5078f0e)   CFCalendarCreateWithIdentifier
    #5 0x556ffe4ec214  (/app/Run+0x5092214)   __CreateCFDateFormatter
    #6 0x556ffe4ebe8b  (/app/Run+0x5091e8b)   CFDateFormatterCreateISO8601Formatter
    #7 0x556ffe5685dd  (/app/Run+0x510e5dd)   Foundation.ISO8601DateFormatter._cfObject getter
                                              ($s10Foundation20ISO8601DateFormatterC9_cfObject33_15CDC4FF71F593B54F66EA9CF55D4C14LLSo06CFDateD3Refavg)
    #8 0x556ffe5693a6  (/app/Run+0x510f3a6)   Foundation.ISO8601DateFormatter.string(from:)
                                              ($s10Foundation20ISO8601DateFormatterC6string4fromSS0A10Essentials0C0V_tF)
    #9–#12                                    application code (a NIOLock-serialised shared formatter,
                                              called from a request-handling path)
    #13+                                      swift concurrency machinery (swift_job_run, dispatch worker)

Address 0x7bb7e0002f80 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: bad-free (/app/Run+0x1064e96) (BuildId: ff8edfecd2f34f1450ae87756007b6362c8f0d5a)
```

Frames were symbolised offline with `llvm-symbolizer --obj=Run` against the exact binary; the mangled Swift names above are verbatim.

## Formatter configuration

```swift
let formatter = ISO8601DateFormatter()          // default formatOptions
formatter.timeZone = TimeZone(identifier: "Europe/London")!
// wrapped in a class serialising access through a lock; only ever used while holding the lock
```

A second instance with `TimeZone(identifier: "UTC")` existed in the same process. The reported call was `string(from:)` on a Swift-concurrency task thread, in a server handling concurrent requests; the formatter's CF object was being created lazily on that first use.

## Reproducibility

- **In the application: effectively deterministic.** The ASan build reported it within ~1 second of the first request that exercised the path. ~~The production epidemiology matched one corruption event early in every process's life (every instance eventually segfaulted; no instance survived a day).~~ *[Correction: withdrawn — those crashes turned out to have a separate cause.]*
- **Minimal standalone repro: not yet.** A single-threaded 3-line program (create formatter, set the same time zone, `string(from:)`) under the same toolchain and ASan does **not** report — so the bug appears state- or concurrency-dependent (plausibly racing CFLocale/CFCalendar/ICU cache initialisation against other threads creating `DateFormatter`s/`Calendar`s, which our server does at startup and per-request).

## Environment

- swift-corelibs-foundation as shipped in the `swift:6.3-noble` Docker images; reported under the image published 2026-08-18 (`swift@sha256:56ef1be2c1ca36f4c52440357dc1fcdfdb5e113587134fcadeef57c225c71b54`, Swift 6.3.3). ~~Production crashes with the same signature also occurred on the previous `6.3-noble` image (`sha256:69bf1f0281e13d82c9e49d67c2dd1dcc8c00bad738c860f4323d7078787ec8ea`), so this does not appear to be a 6.3.3 regression.~~ *[Correction: that inference relied on the withdrawn crash attribution; whether the invalid free also occurs on earlier 6.3 images has not been tested.]*
- Ubuntu 24.04.4 (noble) runtime, glibc 2.39-0ubuntu8.8, ICU 74.2 (`libicuuc.so.74.2`), x86_64.
- Release build, `--static-swift-stdlib`, `-cross-module-optimization`; ASan builds additionally `--sanitize=address` (reported under both abort and `-sanitize-recover=address` modes, two independent builds with different BuildIds, identical stack).
- Vapor 4.122.0 server under Swift structured concurrency; the formatter call sites are ordinary request-handling code.

## Related issues (searched; none covers this)

- #4566 (SR-7745, open) reports `ISO8601DateFormatter.string(from:)` producing garbled output under concurrent use on Linux — the nearest relative. This report differs in two ways: every access to our formatter was serialised through a lock (so this is not concurrent use of one formatter — if there is a race, it is against other CF locale/calendar users in the process, or no race at all), and the failure is an invalid free during the lazy CF object creation rather than incorrect output.
- #5450 (open) reports `DateFormatter.string(from:)` raising SIGILL on x86_64 Linux release builds under Swift 6.1 — same neighbourhood of code, different failure mode (and its author's workaround was to move *to* `ISO8601DateFormatter`, the opposite direction to ours).
- #3597 (SR-9154, closed) reported `ISO8601DateFormatter` init segfaulting on Linux in the Swift 4.2 era — the crash was in the same lazy `__cfObject` creation this report concerns. That defect was fixed, but it shows this creation path has prior history on Linux.
- No existing issue or PR mentions `CFLocaleCreateLocaleIdentifierFromComponents`, `__CFCalendarCreateUCalendar`, or an invalid free on this path.

## Impact and workaround

One invalid free per process corrupts the heap. ~~With glibc malloc or jemalloc this produced delayed, arbitrary-location segfaults that were extremely hard to attribute (and frequently unhandleable — the faulting contexts often could not run any signal handler, defeating both the Swift runtime backtracer and a minimal custom SIGSEGV handler).~~ *[Correction: withdrawn with the crash attribution above.]*

Workaround ~~that fully resolved it for us~~ *[correction: it removes the invalid free; it did not resolve our crashes]*: replace `ISO8601DateFormatter` with a `DateFormatter` configured as `locale = en_US_POSIX`, `dateFormat = "yyyy-MM-dd'T'HH:mm:ssZZZZZ"`, same time zone — output is byte-identical for our cases and it parses both `Z` and `±hh:mm` designators.


## Comment 5440787116

reporter (NONE) · JonCox · 2026-08-27T14:43:03Z · https://github.com/swiftlang/swift-corelibs-foundation/issues/5533#issuecomment-5440787116

**Correction to this report's impact claims (the core finding stands).**

Continued production monitoring after filing has falsified the causal part of this report: with `ISO8601DateFormatter` completely removed from the service (the `DateFormatter` workaround deployed to 100% of traffic), our segfaults continue at the same rate (~4/hour under peak traffic; 36 further crashes on the first day of the fixed build). The overnight canary window that "verified" the workaround covered only low-traffic hours in which the crashes were rare on any build, so the verification was far weaker than the report presented.

What remains valid, and is still worth fixing:

- The AddressSanitizer-captured invalid free in `CFLocaleCreateLocaleIdentifierFromComponents`, during `ISO8601DateFormatter`'s lazy CF object creation, is real — captured exactly as described, reproduced across two independent builds, with the stack and environment details unchanged.
- The byte-identical `DateFormatter` replacement works as described.

What to disregard:

- The claim that this free was the cause of our production segfaults, and that the workaround "fully resolved" them. Our crashes evidently have a separate, still-unidentified cause; this invalid free is a genuine but — in our case — apparently lower-consequence defect.

Apologies for the overreach in the original framing.

*Like the report, this correction was written by Claude Fable 5 (Anthropic), running in Claude Code.*

## Comment 5453483560

reporter (NONE) · JonCox · 2026-08-28T14:04:51Z · https://github.com/swiftlang/swift-corelibs-foundation/issues/5533#issuecomment-5453483560

*This comment was written by **Claude Fable 5** (Anthropic), running in Claude Code, directed by me.*

**Closing the loop on the earlier correction:** the production segfaults that this report originally (and wrongly) attributed to the invalid free have now been root-caused, fixed, and verified. The actual cause was unrelated to Foundation: a Swift compiler bug in which reading a bare closure out of generic-`inout` storage (`Mutex`, `NIOLockedValueBox`, or any equivalent box) permanently wraps the stored value in an extra pair of reabstraction thunks per read, growing it until a call overflows its thread's stack — already on file as swiftlang/swift#91348, where we've added `-O`/Linux reproduction details and measurements. With the closure storage fixed in our app, the crashes stopped completely.

The invalid free reported here remains a real, separate defect, captured exactly as described in the report above — only the crash attribution (already struck through) was wrong. Nothing further from our side on this issue.


## Comment 5456403985

other (CONTRIBUTOR) · parkera · 2026-08-28T18:44:00Z · https://github.com/swiftlang/swift-corelibs-foundation/issues/5533#issuecomment-5456403985

https://github.com/swiftlang/swift-corelibs-foundation/pull/5535
