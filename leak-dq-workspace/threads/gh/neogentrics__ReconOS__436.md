# KF-209 — Tearing down an address space hands the framebuffer to the page allocator

- URL: https://github.com/neogentrics/ReconOS/issues/436
- Repo: neogentrics/ReconOS (language: C)
- State: closed; created 2026-09-13T20:45:17Z; status ok; passes main

## Issue body

reporter (OWNER) · neogentrics · 2026-09-13T20:45:17Z · https://github.com/neogentrics/ReconOS/issues/436

- **Found:** 13 September 2026, by the first aarch64 boot of checkpoint 21's
  second half: `pmm: asked to free memory below the start of the bitmap`, one
  line after the new self-test passed on x86_64.
- **Cost:** **the screen is handed to whoever allocates next.** On x86_64 there
  is no panic and no message — the bits are marked free and the allocator now
  believes a PCI aperture is memory it owns. Every page of the framebuffer,
  every time a program that mapped it exits.
- **Status:** fixed, kernel 0.2.12.

### What it is

`SYS_MAP` puts a device's own physical pages into a program's page tables —
that is the whole of what it is for, and it is what makes a framebuffer
something a program can draw on rather than copy to.

`addrspace_release` walks those tables when the program ends and calls
`addrspace_release_page` for each page it finds. That function knows two things
that are not the allocator's: the shared page of zeroes, and a page of the page
cache. Everything else goes to `pmm_free_page`.

**A mapped device is a third thing, and nothing told it.**

### Why one architecture panicked and the other did not

This is the entire reason it was found.

`pmm_free_pages` refuses an address below the bitmap's base, by name, because
the subtraction in `page_index` would wrap into an enormous index that passes
the upper bound comfortably. On **aarch64** QEMU's virt machine puts the
adapter's aperture at `0x11000000` and RAM at `0x40000000`, so the address is
below the base and the guard fires.

On **x86_64** the aperture is above RAM's base. Both bounds checks pass. The
bits are marked free, the allocator hands them out, and **the self-test reports
pass** — the pixels really were on the screen, because the corruption happens
afterwards, in the teardown.

Same code, same test, same version. One machine calls it a panic and the other
calls it success. That is the case the second architecture exists for, and it is
the third time this project has been caught by work that was right on the
machine it was written on.

### What was done

Not a special case for framebuffers. **The allocator can only take back what it
handed out**, which is a question only it can answer, so it answers it:
`pmm_owns`. The same two bounds `pmm_free_pages` panics on, asked instead of
enforced — they were always a question as well as a guard, and until something
mapped memory the allocator had never seen, nobody needed to ask.

The teardown asks before freeing. Anything mapped from outside RAM is now the
same case: another BAR, a firmware region, memory a future driver borrows. One
place to answer it rather than one per thing that learns about it later.

### The shape

**A funnel with a list of exceptions is a funnel that is wrong the next time
something is added.** `addrspace_release_page` knew about the zero page and the
page cache because those were the two things that had ever been mapped without
being allocated. It was not wrong; it was complete for what existed. Adding a
third kind of page is what made it incomplete, and nothing in it could say so.

Asking `pmm_owns` inverts that: instead of listing what must not be freed, it
establishes what may be.

---

From the register in [`docs/BUGS.md`](https://github.com/neogentrics/ReconOS/blob/main/docs/BUGS.md).
