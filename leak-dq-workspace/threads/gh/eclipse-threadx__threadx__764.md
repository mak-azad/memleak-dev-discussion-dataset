# Investigate AddressSanitizer-like diagnostics for ThreadX

- URL: https://github.com/eclipse-threadx/threadx/issues/764
- Repo: eclipse-threadx/threadx (language: C)
- State: open; created 2026-09-22T20:39:30Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · fdesbiens · 2026-09-22T20:39:30Z · https://github.com/eclipse-threadx/threadx/issues/764

ThreadX provides focused diagnostics such as optional stack checking, API object validation, memory-pool information, event tracing, and module memory protection. It does not provide a general mechanism comparable to AddressSanitizer for detecting out-of-bounds access, use-after-free, or related memory errors. Following #319, I want this investigation to establish whether such support is practical and what a focused implementation would cover.

The investigation needs to determine:

- Which fault classes are in scope: stack, pool, global, and arbitrary-buffer overflows; use-after-free; double release; leaks; and invalid object access.
- Which environments can be supported: the Linux simulation port, embedded GCC or Clang builds, other supported compilers, emulators, and physical targets.
- Whether compiler sanitizer runtimes can be used without introducing prohibited dependencies, unacceptable licensing constraints, or assumptions that do not hold on bare-metal targets.
- Whether ThreadX-specific alternatives are useful, including guarded pool blocks, red zones, allocation quarantine, control-block integrity checks, or MPU/MMU guard regions.
- The required configuration and public API, including how diagnostics identify the offending thread, object, address, and operation.
- The effects on determinism, interrupt latency, code size, RAM consumption, SMP operation, modules, and supported pointer widths.
- How to test the feature with complete regression coverage and how to document the supported and unsupported cases.

I expect the outcome to be a written recommendation defining supported targets and fault classes, a proposed design and test strategy, measured or bounded overhead, and smaller implementation issues where appropriate. The investigation may also conclude that only target- or toolchain-specific guidance is feasible.

No project resources are currently committed to this work. I welcome help from contributors with ThreadX internals, embedded toolchain, or sanitizer-runtime experience.
