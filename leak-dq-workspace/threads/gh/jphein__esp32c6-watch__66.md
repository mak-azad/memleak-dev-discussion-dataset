# [crash] Heap free-list corruption ('Bad free?') tearing down the Slint scene on framebuffer-app launch — 100% reproducible on v0.12.1

- URL: https://github.com/jphein/esp32c6-watch/issues/66
- Repo: jphein/esp32c6-watch (language: Rust)
- State: open; created 2026-07-26T23:55:16Z; status ok; passes main

## Issue body

reporter (OWNER) · jphein · 2026-07-26T23:55:16Z · https://github.com/jphein/esp32c6-watch/issues/66

**Reproducible 100 % on v0.12.1 / HEAD `8617a16` — no local changes needed.** Launch any framebuffer game (e.g. `launch 0`, Snake) and the allocator's own integrity check fires:

```
panicked at linked_list_allocator-0.10.6/src/hole.rs:554:9:
Freed node (0x40820b00) aliases existing hole (0x40820aa0[112])! Bad free?
```

This is JP's report: "watch crashed in the apps menu". It is **not** a new regression — it reproduces on a clean baseline build of HEAD.

## Backtrace (symbolized against the matching ELF)

```
ShellUi::suspend_scene                     src/ui/slint_shell.rs:429
  main loop app-launch arm                 src/main.rs:4521
  -> drop_glue::<Option<WatchShell>>
  -> VRc<ItemTreeVTable, InnerWatchShell>::drop        vtable-0.4.0/src/vrc.rs:108
  -> drop_in_place::<InnerWatchShell>
  -> drop_glue::<Conditional<InnerComponent_energypage_913>>
  -> drop_glue::<Property<bool>>
  -> PropertyHandle::drop                  i-slint-core-1.17.1/properties.rs:816
  -> PANIC (bad free)
```

The freed node **lies inside** the existing hole (`0xaa0 + 112 = 0xb10 > 0xb00`), so this is a double-free or a free of an interior pointer — not merely exhaustion.

## Why it surfaces here

Framebuffer apps (`kind: Framebuffer`, `AppFlags::SUSPEND`) need ~51 KB, so the launch path calls `suspend_scene()` to drop the whole Slint component tree first. Heap immediately before the drop:

```
[HEAP] pre-fb pre-drop: main_free=20072 recl_free=57344 total_free=77416 need=51455
```

Main pool is down to **20 KB** while the framebuffer needs **51 KB**, so the allocation depends on the drop succeeding *and* on the reclaimed pool. The drop is where the corrupted free-list is walked, so that's where it panics — the corruption may well have been introduced earlier by an out-of-bounds write.

## Leading hypothesis: the two heaps / stack geometry

`main.rs` installs two pools:

```rust
esp_alloc::heap_allocator!(size: 198 * 1024);                              // main
esp_alloc::heap_allocator!(#[esp_hal::ram(reclaimed)] size: 56 * 1024);    // reclaimed
```

The reclaimed region sits **above the stack**, and stack = `_stack_start - _bss_end` (~60 KB currently). If the reclaimed pool overlaps or abuts the stack — or if a large framebuffer allocation is served from it — then stack growth and heap allocations can write over each other, which is exactly the shape that produces "freed node aliases existing hole". `need=51455` vs `recl_free=57344` shows the framebuffer is sized right at that pool's capacity, so this path is worth auditing first.

Related: this is very likely the same underlying defect behind the other faults seen on 2026-07-26, all of which are corruption/margin symptoms rather than logic bugs:
- `memory allocation of 7168 bytes failed` on the Climate screen (per-tick model rebuild; separately mitigated by a render-fingerprint gate)
- `Instruction access fault mepc=0x2` in `esp_rtos::task::task_wrapper` after adding ONE Embassy task (A/B: 0/4 vs 4/4 @50 s)
- `Store/AMO access fault mtval=0x3f4da82f` with `ra = ppRxFragmentProc`, 100 % @2.7 s, flipped on by a **16-byte `.bss` shift** with no functional change — i.e. layout-sensitive latent corruption

See #65 for the margin analysis.

## Suggested investigation order

1. **Verify the two pools and the stack do not overlap.** Print each pool's base/size and `_stack_start`/`_bss_end` at boot and assert disjointness. This is cheap and would immediately confirm or kill the hypothesis.
2. **Find where the framebuffer is actually allocated from** (main vs reclaimed) and whether `need=51455` can ever exceed that pool.
3. **Bisect `suspend_scene`.** Does dropping the scene panic without a framebuffer allocation in flight? If yes, the corruption predates the launch and the drop is only the detector.
4. **Check for an out-of-bounds writer.** Prime suspects are the DMA ring buffers and any `unsafe` slice construction around the display/framebuffer path.
5. Consider enabling any available allocator debug/canary support to catch the *writer* rather than the *detector*.

## Test-harness gap this exposed

`tools/watch_soak.py` only resets and watches **boot + idle** — it never launches an app. It therefore reported "0 % crash = stable" for builds that reliably crash the moment a game is opened. A UI-exercising stress pass (launch every registry index, return home, repeat) reproduces this in seconds and should become part of the gate.


## Comment 5119636890

reporter (OWNER) · jphein · 2026-07-29T15:03:52Z · https://github.com/jphein/esp32c6-watch/issues/66#issuecomment-5119636890

## The recorded hypothesis in this issue is REFUTED from the ELF

An audit re-derived the geometry from `target/riscv32imac-unknown-none-elf/release/esp32c6-watch` (`nm`/`readelf`) and the stack/reclaimed-pool collision theory does not survive it.

The panic:

```
panicked at linked_list_allocator-0.10.6/src/hole.rs:554:9:
Freed node (0x40820b00) aliases existing hole (0x40820aa0[112])! Bad free?
```

Measured layout:

| region | range |
|---|---|
| main pool `HEAP` | `0x4081b07c .. 0x4084987c` (size `0x2e800`) |
| `.bss` | `0x4081a920 .. 0x4085ac58` |
| `_bss_end` / stack floor | `0x4085ac58` |
| `.dram2_uninit` (reclaimed, 64 KB) | `0x4086e610` |

**`0x40820b00` is inside the MAIN pool, ~232 KB below the stack floor and ~150 KB from the reclaimed pool.** A stack overflow cannot reach it, so the framebuffer-vs-stack theory is dead for this fault. Cross-region misfree is also ruled out: esp-alloc dispatches by pointer bounds (`esp-alloc-0.10.0/src/heap/llff.rs:32-38`) and the regions are far apart.

*Caveat, stated honestly:* those addresses come from a HEAD build while the panic is from v0.12.1. The main pool occupies 72% of `.bss` starting at the same base, so the region attribution is CONFIRMED-with-caveat, not bit-exact.

## What the assert actually says — it is not the predicate we assumed

`hole.rs:554` is the **third** assert, and it differs from `:501`/`:537`:

- `:501`/`:537` fire when the block being freed runs **into the next** hole — the "size too large" signature.
- `:554` fires when the **preceding hole already covers the pointer being freed**.

Here `0xaa0 + 112 = 0xb10 > 0xb00`, so the freed pointer is **96 bytes inside a 112-byte free block, with exactly 16 bytes left over.**

Signature: a **double free / interior-pointer free of a 16-byte block that had already merged into a 96-byte hole**, or a previous free that over-claimed by 16 B. Notably, `sizeof(SingleLinkedListPinNode<DependencyNode>)` on this 32-bit target is exactly **16 bytes** — the allocation Slint property teardown frees en masse.

Also worth recording: a stray-write cause is *less* consistent with this dump than assumed. `Hole{size,next}` occupies the first 8 bytes of a free block, and `112` is a tidy plausible size, not the pointer-shaped garbage a smashed size word would produce.

## Mechanisms checked and cleared

The leading code-level hypothesis — a mis-tagged `PropertyHandle` pointer reconstructed into a wrong-size `Layout` — was **refuted three independent ways**:

1. **The dep-node drop protocol is symmetric.** `DependencyListHead::drop` nulls only the first node's `prev`; every other `prev` points into another node's `next` cell, never into the property. A leaked tracker leaves no pointer into a freed property.
2. **The cache is explicitly released at teardown, before any property dies.** `free_graphics_resources` → `release()` → `cache.remove(index)` drops the `Box<PropertyTracker>` while properties are still alive, and `#[pin_drop]` guarantees `unregister_item_tree` runs before the struct's `Property` fields drop (111 generated call sites).
3. **There is a generation counter.** `cache_index`/`cache_generation` are validated on every access; a stale index can never be honoured. Worst case from a missed release is a slab **leak**, never a dangling write.

The tagged pointer itself is clean: every consumer masks both tag bits via `pointer_to_binding()`, and `binding_drop::<B>` is monomorphised from the same `B` that allocated, so no size mismatch is reachable.

Properties are **not** individually heap-allocated either — they are inline fields of one `VRc` block, so intra-component "write into a dropped Property" cannot corrupt the free list. Teardown hands the allocator only two kinds of block: `Box<BindingHolder<B>>` frees and 16-byte dep-node deallocs.

## Where to look instead

A double free (or over-large free) of a **small block during property teardown**, with the free list already inconsistent *before* the frame that panics. The crash frame (`Conditional<...> → Property<bool> → PropertyHandle::drop`) is consistent with the dep-node dealloc inside `binding_drop`.

**Decisive next experiment** (queued, needs hardware): build with the `heap-forensics` feature and run a `harvest_free` sweep bracketing `suspend_scene()` **with the old scene drop restored**. If the post-drop sweep reports `stop=nomem` with a large `left` while `free()` jumped, the bad free is localised to the teardown — and it reproduces without needing the crash. If both sweeps report `stop=budget`, the corruption is a stale hazard rather than a live one.

Related: this matters for #75 too. While this is unfixed, "high free but allocation failed" can never be *fully* attributed to fragmentation.


## Comment 5413187211

reporter (OWNER) · jphein · 2026-08-25T16:03:37Z · https://github.com/jphein/esp32c6-watch/issues/66#issuecomment-5413187211

## 2026-08-25: the crash does NOT reproduce — and the fix's successor constraint is now measured

On today's main (653246d, v0.12.1, story+debug-console image on mythic-throne): **12+ framebuffer launch/teardown cycles across all six games, zero panics** — every game launched, took tap input, tore down to Watchface, and answered ping. The suspend-instead-of-teardown fix holds.

What replaced the crash is a **capacity refusal**, working as designed but worth recording:

```
[HEAP] pre-fb pre-drop:  main_free=27052 recl_free=36096 total_free=63148 need=51455
[HEAP] app enter (fresh): main_free=19256 recl_free=65536 -> recl 14080 after grab
```

The framebuffer needs 51,455 B from ONE pool. At fresh boot the reclaimed pool (65,536) fits it. **With WiFi up, the blob's spill takes the reclaimed pool to ~36 KB and no pool fits — the launch is refused silently** (logged, but on-glass it just doesn't open). Two consequences:

1. On `debug-console` builds this is permanent: main.rs holds WiFi up whenever the console is compiled in, so games only launch in the pre-WiFi boot window. Tooling artifact, not a user bug.
2. On release builds it depends on whether WiFi teardown actually returns the spill. Untestable from a console image (see 1) — needs a release-image check: bring WiFi up (story/climate), let it idle off, then launch a game.

Leaving this open until (2) is answered on a release image; if the spill returns, this issue can close as fixed-with-known-constraint.
