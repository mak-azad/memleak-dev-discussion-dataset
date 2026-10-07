# Make behavior of memory allocation functions uniform

- URL: https://github.com/smackers/smack/issues/177
- Repo: smackers/smack (language: C)
- State: open; created 2016-06-13T01:35:00Z; status ok; passes main

## Issue body

reporter (MEMBER) · zvonimir · 2016-06-13T01:35:00Z · https://github.com/smackers/smack/issues/177

Currently `malloc` cannot fail, while `calloc` can nondeterministally fail and return `0`. We should make that uniform, and maybe have a command like option that turns on nondeterministic failures.


## Comment 5433953537

other (CONTRIBUTOR) · shaobo-he · 2026-08-27T03:23:03Z · https://github.com/smackers/smack/issues/177#issuecomment-5433953537

#853 settles one half of this: `malloc(0)` and `alloca(0)` now behave uniformly with every other allocation. All three memory models used to treat a size-zero request specially — the default left the result unassigned, `reuse` and `no-reuse` returned null — and they now return a real, non-null, distinct block of size zero that must not be dereferenced and must be freed, following the SV-COMP rule that allocation never fails.

That leaves `calloc` as the remaining non-uniform case this issue describes: it still returns null nondeterministically, so a program is verified against an allocation failure that `malloc` in the same program cannot have. If the option suggested here is added, the natural shape is one switch that turns nondeterministic failure on for every allocation function at once, rather than `calloc` differing by default.

One related observation while measuring #853: an allocation request that is negative as a signed value — `malloc(SIZE_MAX)`, which reaches `$$alloc` as a negative `ref` — is silently pruned by `assume $sle.ref.bool($0.ref, n)`, so the rest of the path is dead rather than the allocation failing or the size being rejected. Same on develop and on #853; worth deciding alongside the failure switch.

