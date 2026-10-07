# cui9 ceiling leg can PANIC (MiEnsureTable: out of physical pages) instead of refusing

- URL: https://github.com/peryaudo/proskrnl/issues/141
- Repo: peryaudo/proskrnl (language: C)
- State: open; created 2026-08-09T11:41:14Z; status ok; passes main

## Issue body

reporter (OWNER) · peryaudo · 2026-08-09T11:41:14Z · https://github.com/peryaudo/proskrnl/issues/141

## What happened

During a `make fulltest` fan-out (26 legs, `-j8`) the `cui9` leg failed with:

```
[KTEST] cmd interactive start
...
[PANIC] MiEnsureTable: out of physical pages
console_expect: never saw the cmd verdict
== cui9: FAIL ==
```

It did **not** reproduce: the same tree passed `tools/fulltest.sh cui9` alone
and passed `cui9` in two subsequent full 26-leg runs
(`[KTEST] cui9 ceiling procs=319 err=3221225478 capped=0 availmb0=467 availmb=17`,
floor 250).

## Why it is structural rather than a one-off

`tests/run/run.sh cui9` drives the guest to memory exhaustion on purpose and
requires the machine to **refuse** (`err != 0`). It reaches that point with
~17 MiB free out of 467 MiB. Whichever allocation happens to find zero pages
decides the outcome, and `arch/x86_64/mmu.c:49` `MiEnsureTable` has no refusal
path at all:

```c
uint64_t table = MiAllocatePage();
if (table == 0)
{
    KiPanic("MiEnsureTable: out of physical pages");
}
```

So if the loser is a page-table page rather than an allocation that can
propagate a status, the ceiling test dies instead of measuring. That is a race
between the guest's own allocation orders, which is why it is intermittent.

## Reproduction

Not deterministic. `make fulltest` (full 26-leg fan-out) on a loaded box; the
leg's own log is `build/fulltest/views/cui9/build/tests/cui9.log`, and the
signature is the `[PANIC] MiEnsureTable` line with no `[KTEST] cui9 ceiling`
line after it.

## Scope

Pre-existing; noticed while landing the NLS upcase table
(`fold-nls-upcase-table`), which cannot be the cause — it adds 2866 bytes of
kernel `.rodata` and changes no ASCII name comparison, and the cui9 image has
no non-ASCII names. Filed rather than chased because the fix is a decision
about the fault path, not about that branch.
