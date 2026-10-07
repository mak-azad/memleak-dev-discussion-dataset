# Frame arena: restore a graceful mid-frame OOM path

- URL: https://github.com/pusewicz/bielik2d-c/issues/65
- Repo: pusewicz/bielik2d-c (language: C)
- State: open; created 2026-08-04T15:51:06Z; status ok; passes main

## Issue body

reporter (OWNER) · pusewicz · 2026-08-04T15:51:06Z · https://github.com/pusewicz/bielik2d-c/issues/65

Since the tagged-seam reroute (bk-alloc branch), s_chunk_create's allocations abort on OOM before bk_frame_alloc's null-return path can trigger, so the documented assert-then-drop-the-frame's-work contract is dead code — real memory exhaustion mid-frame now aborts the process. This undoes the glitch-vs-crash rationale in the allocator design spec §6 (docs/superpowers/specs/2026-08-03-bk-alloc-design.md). DEVIATIONS.md records the state as shipped. Follow-up: decide whether the frame arena should get a non-aborting growth path (per-frame drop-work restored) or the spec's exception should be formally retired.
