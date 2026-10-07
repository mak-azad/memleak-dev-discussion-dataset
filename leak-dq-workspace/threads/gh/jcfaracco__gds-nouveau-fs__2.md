# Memory Leak in DMA Error Path (nvfs-core.c:536)

- URL: https://github.com/jcfaracco/gds-nouveau-fs/issues/2
- Repo: jcfaracco/gds-nouveau-fs (language: Batchfile)
- State: open; created 2025-11-08T21:05:31Z; status ok; passes main

## Issue body

reporter (OWNER) · jcfaracco · 2025-11-08T21:05:31Z · https://github.com/jcfaracco/gds-nouveau-fs/issues/2

The `nvfs_get_p2p_dma_mapping()` function allocates a `pci_dev_mapping` structure but may not properly free it in all error scenarios. When `nvfs_get_dma_address()` fails after allocation, the cleanup path doesn't consistently free the allocated structure, leading to gradual memory exhaustion under high error rates. This is particularly problematic in production environments where transient DMA errors can occur frequently.

  - [ ] Audit all error paths in nvfs_get_p2p_dma_mapping() to identify missing cleanup
  - [ ] Add proper kfree() calls for pci_dev_mapping structures in error scenarios
  - [ ] Implement RAII-style cleanup using goto labels for consistent error handling
  - [ ] Add memory leak detection tests using kmemleak or custom tracking
  - [ ] Review related functions like nvfs_get_dma_address() for similar patterns
  - [ ] Update function documentation to clarify ownership semantics
  - [ ] Add static analysis annotations for memory ownership
