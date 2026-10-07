# tooling: release_at returns a string literal that range_satisfied frees, crashing dep verify

- URL: https://github.com/briar-systems/mach/issues/3865
- Repo: briar-systems/mach (language: C)
- State: closed; created 2026-09-23T21:53:23Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · octalide · 2026-09-23T21:53:23Z · https://github.com/briar-systems/mach/issues/3865

## What

`release_at` (`src/lang/driver/deps.mach:3335`) starts from `var best: str = ""` and returns that literal when no release tag names the commit. On the other paths it returns an allocated string. `range_satisfied` (`deps.mach:2404`) frees the result unconditionally with `fin { str_free(a, have); }`, so the untagged case frees a string literal.

With the page allocator that becomes `munmap` of the read-only data page holding the literal. It only takes effect when the literal happens to start a page. On the #3779 branch (dev plus #3861, `5286673e6`) it does: gdb shows `munmap(0x1864000, 1)` from `str_free` in `range_satisfied`, and the next `str_empty("")` in `release_at` reads the unmapped page and segfaults. `mach.cli.cmd.dep.verify:version_pins_are_checked_against_every_range` crashes 8 times out of 8, locally and in CI (`test x86_64-linux`, run 35922146704). On dev the unmap fails silently, so the bug is latent there and the next unrelated change that moves `.rodata` exposes it again.

The `release_at_head` callers never free the result: `src/cli/cmd/dep.mach` lines 923, 1017, 1096 and 4223, and `src/cli/cmd/init.mach:917`. So today one caller frees a value that is sometimes not owned, and the others leak the value when it is.

## Expected

`release_at` and `release_at_head` return an owned string on every path, the empty result included. Every caller frees what it receives.

## Acceptance

- [ ] `release_at` returns an allocated string on every path, and every caller of `release_at` and `release_at_head` frees it.
- [ ] `version_pins_are_checked_against_every_range` passes on a tree where the literal starts a page, such as `5286673e6` (the #3779 head).
