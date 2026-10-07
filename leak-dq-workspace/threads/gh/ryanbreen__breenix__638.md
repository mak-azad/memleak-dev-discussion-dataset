# aarch64: heap corruption panic under starvation — linked_list_allocator hole.rs:554 "Freed node aliases existing hole! Bad free?" (starved100 max serial-90, NEW)

- URL: https://github.com/ryanbreen/breenix/issues/638
- Repo: ryanbreen/breenix (language: Rust)
- State: open; created 2026-08-22T18:32:20Z; status ok; passes main

## Issue body

reporter (OWNER) · ryanbreen · 2026-08-22T18:32:20Z · https://github.com/ryanbreen/breenix/issues/638

## Signature

```
KERNEL PANIC!
panicked at /Users/wrb/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/linked_list_allocator-0.10.5/src/hole.rs:554:9:
Freed node (0xffff00005038e0f0) aliases existing hole (0xffff00005038e0f0[104])! Bad free?
```

Observed once in the round-2 confirm battery on `fix/607-576-zero-pc-family` @ `2a2eeefc`:
`starved-gate 100/profile` (14 host `yes` hogs @ `nice -n 19`), `max` profile, boot 90. The boot
panics and then times out (45 s). Preserved in-repo:
`docs/planning/teardown-unification/607-576-serials/round2-gates/starved100-max-NEW-heap-alloc-panic-serial-90.txt:695-698`.

Never observed on `main` — the round-2 baseline slot ran 300 boots on `main` @ `9602d6d4` (clean
100/profile + starved 50/profile) with zero heap-allocator panics of any kind. Not in the
pre-adjudicated signature list (#555/#536/#586/#612/#613/#599/#622-624/#627/#628/#576/#626/#633/#635/#637).

## Why this matters here

`linked_list_allocator`'s "Freed node aliases existing hole" fires when a free is applied to a
kernel-heap node that is already free (a double free or a corrupted free-list pointer) — the exact
failure class that would leave a **stale context image sitting in a reused kernel stack page**, which
is precisely the kind of producer #635's family needs to exist. Filed as producer-family-suspect and
cross-referenced against #635 (aarch64 ret-dispatch transfers to a kernel-STACK resume PC,
`FAR==ELR==x30==x29`, `ESR=0x8600000e`), #633 (thread-id-as-resume-value shape), and #637 (EL0 resumed
at a kernel address) — not claimed to be the same defect as any of them, but the double-free class is
a plausible producer for a stale/reused-stack-page write that later shows up as one of those three
consumer-side faces.

## Round-2 evidence context

This heap panic surfaced during T3-G PR2's round-2 confirm slot (`fix/607-576-zero-pc-family`,
coordinator ruling R41), which narrowed the aarch64 ret-dispatch resume-PC validation to a
kernel-text-range predicate. The branch's diff does not touch the heap allocator; this is disclosed as
new/unfiled/unattributed evidence surfaced by the same soak battery, not attributed to that PR's
change.

## Next step

Root-cause on the allocator's own free/coalesce path — likely candidate is a double-free or an
over-eager coalesce racing a concurrent allocation from another CPU under heap-lock contention induced
by host starvation (this only reproduced under the 14-hog starved-gate leg, never under the idle
clean-gate leg in 200+200 boots). Reproduce under GDB with a breakpoint on the panicking
`hole.rs:554` assertion and walk the free-list state at the point of the aliasing free.

## Comment 5382883504

reporter (OWNER) · ryanbreen · 2026-08-22T22:16:08Z · https://github.com/ryanbreen/breenix/issues/638#issuecomment-5382883504

## Sibling, not parent — and the "heap corruption is upstream of the resume-PC family" theory is falsified (T3-G PR3)

The producer-side RCA for #635/#633/#637 considered this issue as a candidate **root** for the
resume-PC family: one heap corruption producing every bad resume PC downstream. That does not
survive the evidence, and I am recording the falsification rather than leaving the theory standing.

* The four byte-identical #635 captures carry **no** heap panic, and the boot that carries this
  issue's panic carries **no** #635 face. Neither is a precondition for the other.
* In the #635 captures the allocator is *live on the faulting register file* — `x0` resolves exactly
  to `kernel::memory::heap::ALLOCATOR`, offset 0 — i.e. concurrent with the fault, not upstream of
  it.

### What the two do share, and it is worth keeping on the record

Both land in the same phase and are driven by the same actor. The faulting thread in every #635
capture is a userspace thread blocked in a syscall, running
`scheduler::reclaim_terminated_threads`, inside the kernel heap allocator, on its own kernel stack.
`scheduler.rs` has the reaper return `Vec<Box<Thread>>` and `drop(reclaimed_threads)` run **outside**
the lock and **outside** `without_interrupts`. That is the one call chain that frees both a
`Box<Thread>` (this issue's resource) and a kernel-stack slot (#635's and #576's). Same root-cause
*class* — reclaiming a still-referenced object — different resource.

So: sibling in phase and in actor, separate defect until a custody probe says otherwise. Staying
open on its own terms.

### One containment change from PR-A that touches this neighbourhood

A refused resume PC now repoints the per-CPU `kernel_stack_top`/`user_sp_scratch` at the CPU's own
idle stack before redirecting, so a CPU that refuses stops executing on a stack the reaper may
reclaim and re-scrub, and the refusal drain terminates the thread the record names rather than
leaving it Running on a CPU. Neither is a fix for this issue; both remove a way the two could
compound.

