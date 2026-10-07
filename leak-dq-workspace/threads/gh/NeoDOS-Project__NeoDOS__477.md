# [KERNEL] Unsynchronized user/heap slot allocation: concurrent spawns can share a slot

- URL: https://github.com/NeoDOS-Project/NeoDOS/issues/477
- Repo: NeoDOS-Project/NeoDOS (language: Rust)
- State: closed; created 2026-10-04T19:17:28Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · alexis900 · 2026-10-04T19:17:28Z · https://github.com/NeoDOS-Project/NeoDOS/issues/477

## Context

Found while auditing process-resource ownership for #476 (`FREE_BAD`). The
global kernel-heap allocator was clean (`FREE_BAD = 0`), but the paging
**resource-slot tables are unsynchronized** and can double-allocate under
concurrent spawns.

## Observed (code)

`neodos-kernel/src/arch/x64/paging.rs`:

```rust
static mut SLOT_USED: [bool; 128];       // user code+stack slots (256 KB each)
static mut HEAP_SLOT_USED: [bool; 16];   // per-process 2 MB heaps

pub fn alloc_heap_slot() -> Option<HeapSlot> {
    for (i, slot) in HEAP_SLOT_USED.iter_mut().enumerate() {   // non-atomic RMW
        if !*slot { *slot = true; return Some(...); }          // check-then-set
    }
    None
}
// alloc_user_slot does the same over SLOT_USED (count free -> pick -> set true)
```

Call sites run **outside** the scheduler critical section:

- `usermode.rs::create_process_from_ob_path` → `alloc_user_slot()` (`:187`),
  then `spawn_usermode` → `alloc_heap_slot()` (`:257`); the scheduler lock is
  only taken later, inside `add_ring3_process_with_stack`.
- Reachable from `syscall/ob/create/process.rs::handler_ob_create(Process)`,
  `services/manager.rs`, `services/mod.rs`, `stress_spawn.rs`.

Two CPUs spawning concurrently can both read the same slot as free and both set
it used → **two processes share one user slot** (ELF/code+stack overwrite → user
`#PF`, cf. #384) or **one 2 MB heap**, and the shared slot is then freed twice
on teardown.

## Impact

- Two processes aliasing a user window (code/stack) or a heap region.
- Double free of a paging slot on teardown.
- Plausible contributor to the #384 user `#PF` / #476 corruption family
  (not demonstrated in the #476 audit: `[FREE_BAD]` slot-race = 0 in the
  campaigns, because the window is only a few instructions and the churn had at
  most 2 concurrent spawners).

## Evidence

- Source above; the audit added `[FREE_BAD] kind=ALREADY_FREE
  allocator=paging_{user,heap}_slot` and a direct CAS-based double-allocation
  detector (`paging_{user,heap}_slot_race`) on
  `investigation/476-allocator-free-bad` (commit `cac7cd8`), report
  `docs/investigation/issue-476-allocator-free-bad.md`.
- The detector never fired on a **real** event in VBox SMP2 churn campaigns
  (2×32 ×6 boots); it only caught synthetic test state before the fix.

## Proposed fix

Claim slots with an atomic `compare_exchange(false, true)` (retry the next slot
on failure) for both `alloc_user_slot` and `alloc_heap_slot`; keep the owner tag
for diagnostics. Minimal, no policy/ABI change.

## Related

- #476 (Ring-0 INVALID_OPCODE / frame corruption, open)
- #384 (NeoInit user `#PF`, open)
- #383 (allocator free-list corruption, closed)


## Comment 6002108269

reporter (COLLABORATOR) · alexis900 · 2026-10-05T20:10:42Z · https://github.com/NeoDOS-Project/NeoDOS/issues/477#issuecomment-6002108269

## Estado: FIX MERGEADO en `develop`

PR #481 fusionada (squash) → merge commit `d522ebf` en `develop` (== origin/develop).

### Defecto (demostrado por código)
`alloc_user_slot`/`alloc_heap_slot` hacían `load()` + `compare_exchange` pero **ignoraban el resultado del CAS y devolvían el slot**. Dos CPUs podían obtener el mismo slot (ventana de usuario / heap 2 MB) y liberarlo dos veces.

### Fix
Claim atómico autoritativo: `claim_first_free`/`claim_at` con `compare_exchange(false,true,AcqRel)`; en contención se salta al siguiente slot libre (nunca se entrega uno reclamado por otra CPU). Se conservan los owner tags y la detección `AlreadyFree` del free-path.

### Validación
- `neodev test`: 825/825 (incluye la regresión `paging_slot_claim_atomic`).
- QEMU SMP1/2/4 ×2: `paging_*_slot_race = 0`, `FREE_BAD = 0`, #PF/#GP/#UD = 0, panic = 0.

Informe: `docs/investigation/issue-477-slot-alloc-race-fix.md`. Se puede cerrar.
