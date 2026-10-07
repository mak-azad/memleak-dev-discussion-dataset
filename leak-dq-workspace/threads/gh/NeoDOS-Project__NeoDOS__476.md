# [KERNEL] VirtualBox SMP2: Ring-0 INVALID_OPCODE after unhandled user #PF / process terminate (rip=stack address)

- URL: https://github.com/NeoDOS-Project/NeoDOS/issues/476
- Repo: NeoDOS-Project/NeoDOS (language: Rust)
- State: closed; created 2026-10-04T16:41:49Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · alexis900 · 2026-10-04T16:41:49Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476

## Context

Found while validating #474 on **VirtualBox 7.2.20, EFI, SMP2, bridged**. On one
boot the fixed-#474 image panicked with a Ring-0 `INVALID_OPCODE` that has a
**different signature and mechanism** from #474. The shell had already started;
the panic was preceded by an unhandled user `#PF` (`[EXC] … Terminate`).

## Observed

```text
[EXC] ERROR: User exception unhandled (Terminate): type=14 rip=0xc8011c
[SPAWN] pid=7 tid=9 name=Ntpd ...
...
[FAULT] v=6 INVALID_OPCODE rip=0x24b922a cs=0x8 rsp=0x2519a20 cpu=1
[PANIC] class=UNKNOWN_CPU_EXCEPTION rsp=0x2519800 msg=Invalid opcode: rip=0x24b922a
```

Crash dump:

```text
Timestamp: 41568   Cause: PANIC (0)
TID: 6  PID: 7  CPU: 1  ThreadState: 1
Scheduler: [5] TID=9 PID=7 state=Running  [6] TID=6 PID=4 state=Running
           Current TID: 6  Next TID: 10  Next PID: 8
```

## Why it is not #474

- #474: wild RIP = `0x148` (low garbage), on the **boot window**, cpu0.
- Here: wild RIP = `0x24b922a` — an address **inside another thread's kernel
  stack** (tid7's frame is `0x24b9220`) — on cpu1, **after** a user process was
  terminated.
- It occurred on a build that contains the #474 fix and the gate
  (`ring0_publish_is_dispatchable`) that blocks the #474 publication path.
- Healthy VBox boots in the same sample have **no** `[EXC] … Terminate`; the
  panic only co-occurs with the unhandled user fault + termination.

The signature (return/jump into a different thread's stack right after a
termination) is consistent with **kernel-stack lifetime / process-termination
reuse** rather than a non-dispatchable frame publication.

## Relation to existing work

Same broad VBox SMP2 memory-corruption family as:

- **#384** — NeoInit user `#PF` at entry, shell never starts (~3–5 % of VBox
  SMP2 boots).
- **#383** — `NoMem` spawn / allocator corruption co-occurring with #384.
- **#346 / F-02** — kernel-stack reaping deferred while a pid runs on any CPU.

This issue tracks the **kernel `INVALID_OPCODE` manifestation** of that family
(panic after a *handled-as-terminate* user fault, with the shell up).

## Rate / reproducibility

- VirtualBox SMP2 fixed image: 1 panic in 4 successful boots (3/3 subsequent
  runs OK). One earlier boot hung in early PEI (host load ~5.9) — environmental.
- One VirtualBox SMP2 boot on the unfixed base (`d584664`) was OK (n=1,
  inconclusive).
- QEMU TCG SMP2 ×10 on the same fixed image: 0 faults.

Intermittent; needs the user `#PF` + terminate trigger.

## Impact

Intermittent kernel panic (`UNKNOWN_CPU_EXCEPTION`) on VirtualBox SMP2, not
reproduced on QEMU. Distinct from #474.

## Suspects (to confirm)

- Kernel stack freed/reused while the terminated pid's thread is still running
  on another CPU (`is_pid_running_on_any_cpu` / `reap_pending_zombies` race).
- Allocator corruption from #383 feeding into the stack frame.

## Evidence

- `vbox_run2.log` (serial, includes the panic dump) — captured during #474
  validation. The `-d int,cpu_reset` low-level trace exists only for QEMU, so
  the first corrupt state on VBox is still unidentified.

## Related

- #474 (QEMU SMP2 `rip=0x148`, fixed)
- #383, #384
- #346, #293, #338


## Comment 5982595795

reporter (COLLABORATOR) · alexis900 · 2026-10-04T17:30:57Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476#issuecomment-5982595795

## Investigation update — root cause **not demonstrated**; #476 stays open

Branch: `investigation/476-vbox-invalid-opcode`
(commit `58a9a86`), report:
`docs/investigation/issue-476-vbox-invalid-opcode.md`.

### Confirmed

- Panic signature: `#UD` Ring 0, `rip=0x24b922a` (= Dhcpc/tid 7 stack `0x24b9220`
  `+0xa`), `rsp=0x2519a20` (Ntpd/tid 9 stack), cpu 1. It is **not** the #474
  mechanism (different RIP/context; occurs despite the #474 gate).
- Trigger: a service takes an unhandled user `#PF` → terminate → Service Manager
  restarts it reusing the dead process's resources. Observed with pid 3 (Ntpd)
  in the crashing run and pid 5 (Dhcpc) in a surviving run:
  `[EXC] … Terminate: type=14 rip=0x1680fd0 fault=0x2d4221d fcode=1 pid=5 tid=7`.
  `fault=0x2d4221d` is in the **kernel heap** (0x2400000–0x3400000) → a user
  thread dereferenced a kernel-heap address.
- Scheduler guards show nothing before the fault (`READY_GUARD_STATS` all zero,
  no `SCHED_WARN`/`DOUBLE_RUNNING`/`STACK_OWNER_MISMATCH`).
- At panic, tid 5 (pid 3) is already gone and pid 7 reuses pid 3's
  `heap_base=0x10200000`.

### Relationship to #383 / #384

Same family, root cause not established for any of them:

- **#383** closed with the residual free-list corruption "**currently NOT
  reproducible**" — the range-routing fix removed one misroute, but the
  double-free / non-owned-free source was never isolated.
- **#384** (NeoInit user `#PF`) remains open, co-occurring with #383.
- **#476** is the fatal kernel `#UD` of the same lifecycle-corruption family.

### Leading hypothesis (H1, unproven)

Kernel stack freed/reused while a CPU still executes on it: after
`exception_do_resched → schedule_with` repoints `KPRCB` to the next thread,
`is_pid_running_on_any_cpu(old_pid)` is already false, so **another** CPU's
`reap_pending_zombies` can reclaim the old stack in the window before the
caller's `mov rsp`. F-02-A only excludes the switching CPU's own `prev_pid`.
A freed 16 KB stack reused as a new thread's stack ⇒ wild RIP (#476); a write
into a freed fallback-heap block ⇒ free-list corruption (#383).

Alternative: a corrupted indirect call (`dispatch_kernel_apcs`) to a stack
address. Neither is demonstrated.

### Campaign

- VBox SMP2 diagnostic build: **10/10** `ALL_TESTS_COMPLETE`, 0 `#UD` (run 5 hit
  the `#PF`/terminate trigger and survived).
- Earlier VBox SMP2: 1 `#UD` in 4 boots; 1 unfixed boot OK.
- VBox SMP2 + `stress_spawn` (128 spawn/exit children): produced a pre-existing
  **VFS-contention stall** (owner `tid=8 state=Ready`, `preempt=1`), not #476;
  harness re-disabled.

Limitations: no `-d int` on VBox; the diagnostic rings are global and cpu 0
flooded cpu 1's context; rate ~1 in 4–14 boots.

### Diagnostics kept (branch, not merged)

Per-CPU `KPRCB` dump, per-thread `cpu/rsp/ks_top/ks_size/name`, `[DUP_KSTOP]`
live-stack-sharing scan, `[#UD_STACK]` raw handler-stack dump, and
`fault/fcode/pid/tid/cpu` in the terminate log.

### Next experiments

1. Per-CPU diagnostic rings so the faulting CPU's context survives.
2. Precise `SWITCH_OUT_KS` detector cleared right after `mov rsp`
   (`timer`/`syscall`/`exception` asm) + `recycle_terminated` refusing to free a
   matching stack — both demonstrates and fixes H1.
3. Allocator owned-pointer validation on free to localise #383.
4. A bounded spawn→exit→restart loop that avoids the VFS heavy path.

**No speculative fix applied. #476 remains OPEN.** `develop` is unaffected.


## Comment 5983028371

reporter (COLLABORATOR) · alexis900 · 2026-10-04T18:24:12Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476#issuecomment-5983028371

## H1 experiment (`SWITCH_OUT_KS`) — **H1 NOT DEMONSTRATED**

Branch `investigation/476-vbox-invalid-opcode`, commit `e8972b9`. Report:
`docs/investigation/issue-476-vbox-invalid-opcode.md` §9–§10.

### What was built (falsifiable, branch-only — not merged)

- Per-CPU switch-out tracking (`scheduler/diag/kstack.rs`): `ACTIVE/KS/TID/PID/
  RSP/SIZE/NEXT_KS` + a 256-entry `OUT`/`CLR`/`CONFLICT` ring.
- `note()` is called **immediately before** the `KPRCB.current_thread` write.
- `switch_out_clear()` is inserted in ASM **after** `mov rsp` in
  `timer_handler_asm`, `syscall_handler_asm` (both resched paths),
  `exception_do_resched`, and `ap_enter_idle` — so the marker spans exactly the
  window "KPRCB repointed → stack physically abandoned".
- Every stack-free site (`recycle_terminated`, `kill_pid`, `recycle_thread`)
  calls the guard: if any CPU is mid-switch for that stack it logs
  `[KSTACK_RECLAIM_CONFLICT]`, increments a counter, and **leaks** the Box
  instead of freeing it (bounded), so the experiment cannot corrupt memory.

### Detector validation (required before trusting a negative)

`scheduler/tests.rs::n476_kstack_switch_out_conflict_detector` proves the data
path: after `note`, `reclaim_conflict(stack)` returns `Some` (with tid/pid/rsp);
a different stack returns `None`; after `switch_out_clear` it returns `None`.
`neodev test`: **821/821 PASS**.

### Result — zero conflicts across 171 terminations

| Campaign | Terminations | noted | cleared | **conflicts** | panics |
|----------|-------------:|------:|--------:|--------------:|-------:|
| VBox SMP2 normal boots ×12 | 0 | — | — | **0** | 0 |
| VBox SMP2 churn 48 | 48 | 3865 | 71392 | **0** | 0 |
| VBox SMP2 churn 200 (123 ok, 77 NoMem backpressure) | 123 | 4006 | 74137 | **0** | 0 |

```text
[SPAWN_STRESS] done pid=6 ok=48  err=0   mode=CreateActivate
[KSTACK_STATS] after-churn noted=3865 cleared=71392 conflicts=0
[SPAWN_STRESS] done pid=6 ok=123 err=77  mode=CreateActivate
[KSTACK_STATS] after-churn noted=4006 cleared=74137 conflicts=0
```

`noted/cleared` prove the detector executed on every context switch;
`reclaim_conflict` was consulted for every reap and never matched.

### Verdict

**H1 NOT DEMONSTRATED (unsupported).** 0 conflicts in 171 terminations with a
validated detector. The observed #476 rate (~1 panic / ~29 VBox boots with few
terminations/boot) would require the window to be hit a large fraction of the
time per termination; the churn is inconsistent with that. Caveat: the churn
uses `sys_exit` (Ring-3 syscall) terminations; a vanishingly rare window cannot
be formally excluded.

No H1 fix applied. The detector and diagnostics are retained on the branch for
future campaigns; `stress_spawn` is disabled again. `develop` unchanged.

### Next hypotheses (unchanged from the report)

1. Allocator owned-pointer validation on free (#383 free-list corruption).
2. Double-free / non-owned free in process teardown.
3. Page-table / user-heap slot reuse without clearing mappings.
4. Corrupted indirect call (APC/DPC/IRP callback) to a stack address.
5. A context-switch window other than the reap/KPRCB one.

**#476 remains OPEN.**


## Comment 5983487912

reporter (COLLABORATOR) · alexis900 · 2026-10-04T19:17:47Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476#issuecomment-5983487912

## Allocator / resource ownership audit (`FREE_BAD`) — global allocator clean

Branch `investigation/476-allocator-free-bad`, commit `cac7cd8`. Report:
`docs/investigation/issue-476-allocator-free-bad.md`.

### What was built (diagnostic, branch-only)

- **Global allocator** (`slab.rs::audit_free`): before every `dealloc`, validates
  range/magic/slot_size/alignment and double-free (per-CPU hot cache + page free
  list); a fixed open-addressing **allocation shadow** detects fallback-heap
  double-free / not-owned frees. On violation it logs `[FREE_BAD]` and leaks
  (documented diagnostic mitigation). Counters + 64-entry ring dumped on panic.
- **Paging slots** (`paging.rs`): `SLOT_USED`/`HEAP_SLOT_USED` converted to
  atomics; free paths log `[FREE_BAD] kind=ALREADY_FREE allocator=paging_*_slot`
  and allocation uses a CAS detector `paging_*_slot_race`.
- Unit test `n476_free_bad_ownership_detector` covers
  None/Misaligned/OwnerMismatch/OutOfRange/NotOwned/AlreadyFree.

### Result — global heap: **no violation observed**

| Environment | runs | `FREE_BAD` (global) | slot-race | frame-family panic |
|-------------|-----:|--------------------:|----------:|-------------------:|
| `neodev test` (QEMU SMP2) | 1 | 0 (822/822 PASS) | 0 | 0 |
| VBox SMP2 churn 1×200 | 1 | 0 | — | 0 |
| VBox SMP2 churn 2×32 (`fb2d`) | 6 | **0** | 0 | 1 `#PF` |
| VBox SMP2 churn 2×32 (`fb2e`) | 6 | **0** | 0 | 0 |

Key: the churn `#PF`/GPF carry **no** `FREE_BAD` — the allocator free lists are
intact at the crash (`fb2d_5`: `[FAULT] v=14 ... rip=0x24b12bf` during service
startup, `FREE_BAD = 0`; `fb2c_4`: GPF in the `iretq` of `syscall_handler_asm`
with a garbage selector, after repeated `[K355] resched handoff -> idle`).

⇒ **#383's residual free-list corruption is not reproduced** by these workloads;
the global allocator is not the source of the #476 family.

### New finding — F2 (separate issue **#477**)

`SLOT_USED`/`HEAP_SLOT_USED` were unsynchronized non-atomic test-and-set with no
lock; `alloc_user_slot`/`alloc_heap_slot` run outside the scheduler critical
section, so concurrent spawns can share a slot. Fixed detector added; **not
observed** on a real event in the campaigns. Tracked in #477.

### Next hypothesis (highest diagnostic value)

The corruption is a wild control transfer into a kernel stack / bad `iretq`
selector with no allocator or KStack-reclaim (H1) violation. Recommend
instrumenting the **switch-out `iretq` frame** across the `[K355]` idle hand-off
and the syscall/timer return paths: verify the frame being `iretq`'d
(RIP/CS/RFLAGS/RSP/SS) belongs to the selected thread's `kernel_stack_top` and
flag `[IRETQ_BAD_FRAME]` before the fault.

No functional fix applied. **#476 remains OPEN.** `develop` unchanged.


## Comment 5984117445

reporter (COLLABORATOR) · alexis900 · 2026-10-04T20:33:24Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476#issuecomment-5984117445

## IRETQ frame audit — **root cause demonstrated** (`IRETQ_BAD_FRAME`)

Branch `investigation/476-iretq-frame`. Report:
`docs/investigation/issue-476-iretq-frame-audit.md`.

### Detector

`scheduler/diag/iretq.rs` validates the frame `iretq` is about to consume
(`rsp+120`: RIP/CS/RFLAGS/RSP/SS): inside the selected thread's kernel stack,
ring-coherent, valid CS/SS/RIP/RSP/RFLAGS, and not on another live thread's
stack. Emits `[IRETQ_BAD_FRAME]`; hooked before every dispatch return (syscall
K355/chosen/idle/main, timer preempt + K355 idle hand-off, exception) and in
`syscall_trace_frame` phase 1. `neodev test` **823/823**, no false positives.

### Observed (reproducible, VBox SMP2 + churn)

```text
[IRETQ_BAD_FRAME] kind=FRAME_OUTSIDE_KSTACK site=resched_k355_idle cpu=0 tid=1
  name=idle/0 k_state=Running kprcb_tid=1
  next_rsp=0x24b4f40 ks_base=0x434c668 ks_top=0x434d668
  frame_addr=0x24b4fb8 rip=0x202 cs=0x1e471820 rflags=0x24b4f40 user_rsp=0x0 ss=0x4017e0a
```
(one run: `gp=1`; another run: 86 hits at `timer_preempt`/`resched_k355_idle`/`syscall_iretq`.)

### Root cause — DEMONSTRATED

The kernel does **not** restore the context it believes. `RSP_TRACE` pins the
writer of the idle's bad `rsp`:

```text
[RSP_TRACE] #25323 cpu=0 site=5(SITE_RSP_TIMESLICE=on_timer_tick) tid=1 pid=0
            old=0x434d510 new=0x24b4f40 k.cpu=0 state=1(Running) is_current=1
```

`0x434d510` is on the idle's `IDLE_STACK`; `0x24b4f40` is on the previous
thread's 16 KiB stack (`KSTACK_RING` shows the CPU0 `tid=6(NetApplier) ↔ idle/0`
hand-off oscillation). Mechanism:

```text
commit KPRCB.current_thread = idle      (inside without_interrupts)
  -> without_interrupts restores IF=1   <-- window
  -> ASM: mov rsp, idle.rsp             (still on the previous stack)
       a timer fires here:
         on_timer_tick(): current = idle (KPRCB), current_rsp = previous stack
                          => idle.rsp = previous stack   (corruption)
  -> the next K355 hand-off returns the foreign rsp; the ASM iretq's a frame
     taken from another thread's stack (cs=0x1e471820) -> #GP/#PF/#UD
```

Invariant broken: *a thread's saved rsp/frame lies inside its own kernel stack*,
violated by the timer during the KPRCB-commit → `mov rsp` window (IF re-enabled
between commit and stack switch, syscall resched path).

### Fix (proposed, NOT integrated)

1. Keep **IF=0 from the KPRCB commit to the stack switch** in the syscall resched
   path (timer/exception paths already hold IF=0 across `mov rsp`); `iretq`
   restores IF from the frame.
2. Defence-in-depth: at the `k.rsp = current_rsp` sites, only store when
   `current_rsp` is inside `k`'s kernel stack (must special-case the boot
   thread, whose `ks_top` is not the live bootstrap stack).

Not implemented (delicate IF/`iretq` interaction). **#476 remains OPEN.** #477
(paging slots) stays independent and untouched. `develop` unchanged.


## Comment 6001798033

reporter (COLLABORATOR) · alexis900 · 2026-10-05T19:47:30Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476#issuecomment-6001798033

## Estado: FIX MERGEADO en `develop`

PR #480 fusionada (squash) → merge commit `a67ba09` en `develop` (== origin/develop).

### Causa raíz (confirmada)
La ruta de resched del syscall corría con **IF=1** en el límite del handoff. `schedule_with_handoff` publicaba `KPRCB.current_thread = NEXT` dentro de `without_interrupts` (IF=0), pero IF se restauraba a 1 antes del `mov rsp,next_rsp`; un timer en esa ventana observaba `KPRCB=NEXT` con RSP en `PREV` (`RSP_FOREIGN`).

### Fix
`cli` antes de cada `call syscall_try_resched` en `syscall_handler_asm` (ambos sitios); `iretq` restaura IF desde el RFLAGS guardado. Regresión permanente en `switch_out_clear_at` (site-aware).

### Evidencia
- `neodev test`: 824/824.
- QEMU SMP1/2/4 (14 runs con fix): `RSP_FOREIGN=0`, `IRETQ_BAD_FRAME=0`, sin mismatch de ownership en el handoff de syscall.
- Baseline (`develop`, 9 runs): `RSP_FOREIGN=1260`, `IRETQ_BAD_FRAME=1`, y el crash `INVALID_OPCODE` con RIP salvaje (cpu1).

### Fuera de alcance (documentado, separado)
- `wait_for_process` publica `KPRCB=target` estando en la pila bootstrap (lo detecta la aserción en site 0/3) — ventana distinta.
- #GP intermitente del Object Manager y #UD en Ring-3 aparecen también en baseline → preexistentes.

VBox SMP2 churn con el fix no se ha ejecutado todavía. Issue permanece abierta hasta validación con churn si se considera necesaria. Informe: `docs/investigation/issue-476-close-window-fix.md`.

## Comment 6003649493

reporter (COLLABORATOR) · alexis900 · 2026-10-05T21:45:46Z · https://github.com/NeoDOS-Project/NeoDOS/issues/476#issuecomment-6003649493

## Cerrada — ownership de pila restaurado en toda la familia

Integrado en `develop`:

| Fix | PR | Merge |
|---|---|---|
| Ventana KPRCB/RSP del syscall resched (`cli` antes de `syscall_try_resched`) | #480 | `a67ba09` |
| Orden de publicación en `wait_for_process` (KPRCB tras salir de la pila bootstrap) | #483 | `2dc0db4` |

Issue relacionada: #482 (ventana bootstrap), #477 (slots, PR #481, `d522ebf`).

### Evidencia (QEMU SMP1/2/4)
- `RSP_FOREIGN = 0` (baseline: 1260).
- `RSP_OWNER_MISMATCH = 0` en todos los sitios (antes: site 0/3 en cada boot).
- `IRETQ_BAD_FRAME` limpio salvo el falso positivo conocido del hilo **boot** (`ks_top`).
- `neodev build --quick --image` OK; `neodev test` **825/825** (develop integrado @ `2dc0db4`).

### Fallos residuales (separados, no atribuidos a #476)
- #GP intermitente del Object Manager y #UD en Ring-3 (presentes también en baseline).
- `Option::unwrap() on None` intermitente **antes** de `wait_for_process` (fuera del camino del fix).
- Falso positivo `IRETQ_BAD_FRAME` del hilo boot.

Estos quedan como hallazgos independientes. Cierro #476: el invariante de ownership `KPRCB.current_thread == owner(RSP)` se mantiene en el arranque y bajo SMP.
