# sw/os sh: xf upload missing OOM check and leaks its 256KB staging buffer on cancel

- URL: https://github.com/awdemos/zeitlos/issues/5
- Repo: awdemos/zeitlos (language: C)
- State: open; created 2026-09-25T01:30:21Z; status ok; passes main

## Issue body

reporter (OWNER) · awdemos · 2026-09-25T01:30:21Z · https://github.com/awdemos/zeitlos/issues/5

## Summary
The kernel shell's `xf` upload command leaks its 256 KB staging buffer on cancelled/failed transfers and doesn't check the allocation.

## Evidence
`sw/os/sh.c:723-743`: `tmp = k_mem_alloc(UPLOAD_MAX_SIZE)` (256 KB) has no NULL check — the sibling `xmf` command right below does check. On OOM, `xfer_recv(0)` would write the upload over the BIOS/zero page. And when `bytes_received == 0` (cancelled/failed), `k_mem_free(tmp)` is skipped — a permanent 256 KB leak of the kernel pool, fatal on a 1 MB board.

## Impact
Kernel memory exhaustion / memory-over-zero-page write.

## Suggested fix
Add the NULL check and move the free after the size check so it runs on every path.

A tested fix is ready — happy to open a PR.

