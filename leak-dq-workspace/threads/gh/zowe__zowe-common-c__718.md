# TRACK_MEMORY in alloc.c cannot be switched on at run time, and stops recording silently

- URL: https://github.com/zowe/zowe-common-c/issues/718
- Repo: zowe/zowe-common-c (language: C)
- State: open; created 2026-09-22T20:01:56Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · JoeNemo · 2026-09-22T20:01:56Z · https://github.com/zowe/zowe-common-c/issues/718

## Summary

The `TRACK_MEMORY` facility in `c/alloc.c` cannot be used for the job it exists
to do. It is meant to let us analyse a leak on the binary a customer already
has, which means it has to be switchable at run time. Today it is switchable
only by rebuilding, the run-time dial that remains is unreachable, and even
when it is compiled in it stops recording early and silently.

This came up while reviewing #712. The CSI leak fixes in that PR are a separate
matter; this issue is about the facility itself.

## Why it matters

Memory management is the layer everything else in this repo sits on. We should
be able to answer "where is this leaking" from a running system, without
shipping a rebuilt module first. That is the only reason to have a tracker
rather than just reading the code.

## Blocking faults

These two make the tracker unusable regardless of how it is switched on.

**1. It goes blind after 25000 cumulative allocations, not 25000 live ones.**
`trackAllocation` returns silently once `allocationsTracked` reaches
`ALLOCATIONS_TO_TRACK`. `trackFree` stamps the slot with `(char*)(-1)` but never
decrements the counter and never reuses the slot, so the table fills with
corpses. A server that allocates per request exhausts it in minutes, after
which nothing is recorded and nothing is reported about having stopped.

**2. No serialization.** `allocationsTracked++` and the three array stores are
unprotected. ZSS dispatches services into subtasks and ZIS is cross-memory.
Concurrent use yields a wrong ledger, not merely a partial one.

## Defects

**3. The wrong-size-free detector only fires for two magic lengths.** In
`trackFree`:

```c
if ((length != allocationLengths[i]) &&
    ((272 == length) || (296 == length)))
```

The comparison of the freed length against the recorded length is exactly the
check that catches `safeFree(p, sizeof(pointer))`, which is #711 and part of
#712. It is gated behind two constants from somebody's one-off investigation,
with the crash line commented out below it. Generalising the condition is a
few lines in a debug path and would have caught both of those years ago. This
is the highest value item here.

**4. `showOutstanding()` has no prototype in any header.** `c/stcbase.c:137`
calls it bare. `jwt/tests/jwt-test.c:825` carries a hand-written
`int showOutstanding(void);` inside a function body, with a comment explaining
the `-DTRACK_MEMORY` requirement. The workaround has been copied rather than
the header fixed.

**5. `%x` used to print pointers**, twice in `showOutstanding`. Truncates on
64-bit and is undefined behaviour. `%p` is correct.

**6. Guard mismatch between definitions and call sites.** The definitions are
behind `#if ((!METTLE || WRITSTAT) && TRACK_MEMORY)` while the call sites are
behind `#ifdef TRACK_MEMORY`. On a METTLE build without WRITSTAT, which is ZIS,
defining `TRACK_MEMORY` compiles the calls and omits the functions.

## Coverage holes

**7. Key-8 storage is invisible.** `safeMalloc31Key8` and `safeFree31Key8`
maintain `k8Bytes` but never call `trackAllocation` or `trackFree`.

**8. `allocationNames` stores the caller's pointer, not a copy.** Correct for
the string literals that callers normally pass, dangling for anything
constructed.

## Dead weight

**9.** The lazy-init loop in `trackAllocation` is redundant. The arrays are
`static` and therefore already zero, and the loop runs only when the counter is
zero so it can never re-initialise.

**10.** `trackFree` has no `break` after a match, so it always walks the whole
table.

## Verified sound, so nobody re-audits these

`safeMalloc64`, `safeFree64` and the `ByToken` variants all delegate to the
tracking internals. `safeRealloc` routes through `safeMalloc` and `safeFree`,
so the ledger stays balanced. `safeFree` is literally `safeFree31`, so there is
no allocator mismatch in any of the paired calls.

## Proposed direction

Roughly sixty lines in one file, keeping the existing design rather than
replacing it:

- reuse slots so capacity tracks live allocations instead of cumulative ones
- serialize the ledger
- move the level test ahead of `trackAllocation` and `trackFree` rather than
  ahead of the `printf`, so a tracking-capable build costs one predictable
  branch when the level is zero
- declare `showOutstanding()` and a level setter and getter in `h/alloc.h`
- generalise the wrong-size-free check from item 3

That combination lets us ship the facility compiled in and dormant, and turn it
on where the problem is. Item 3 stands alone and could go first.

## Scope

After the 3.6 release. This is the allocator that everything depends on, so the
change wants a quiet window and a small, reviewable diff rather than a large
one landed near a freeze.


## Comment 5794065727

other (CONTRIBUTOR) · ChongZhou-Broadcom · 2026-09-23T11:33:36Z · https://github.com/zowe/zowe-common-c/issues/718#issuecomment-5794065727

I noticed that you self-assigned this issue, so I will not fix all of the mentioned problems in my PR.

But I would like to put here an AI-generated to-do list, hoping it could be helpful to the one who will be working on this in the future.

The list is based on the whole description of this issue. _(because not all mentioned problems are found in the "Proposed direction" section.)_

---

1. trackAllocation/trackFree count cumulative allocations, not live ones — table fills with dead (char*)(-1) slots and goes blind after 25000 total allocs, silently.
2. No locking around allocationsTracked++ and the three array writes — unsafe under ZSS subtask dispatch / ZIS cross-memory concurrency.
3. Wrong-size-free detector in trackFree only fires for two hardcoded lengths (272/296) instead of a general length != allocationLengths[i] check — it was said to be the highest-value single fix, and it should be generalized to catch arbitrary incorrect lengths.
4. showOutstanding() has no header prototype anywhere — called bare in c/stcbase.c:137, and re-declared locally as a workaround in jwt/tests/jwt-test.c:825.
5. showOutstanding uses %x to print pointers (twice) — truncates on 64-bit, undefined behavior; should be %p.
6. Guard mismatch: definitions are gated by #if ((!METTLE || WRITSTAT) && TRACK_MEMORY) but call sites by #ifdef TRACK_MEMORY — on METTLE without WRITSTAT (i.e. ZIS), defining TRACK_MEMORY compiles calls to functions that don't exist.
7. safeMalloc31Key8/safeFree31Key8 never call trackAllocation/trackFree — Key-8 storage is invisible to the tracker.
8. allocationNames stores the caller's raw pointer instead of copying the string — fine for literals, dangles for constructed strings.
9. Lazy-init loop in trackAllocation is redundant — arrays are static (already zero) and the loop only runs when the counter is zero, so it can never re-init anything.
10. trackFree never breaks after finding a match — always walks the entire table.

