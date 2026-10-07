# The netebpfext fuzzer should check for memory leaks

- URL: https://github.com/microsoft/ebpf-for-windows/issues/4063
- Repo: microsoft/ebpf-for-windows (language: C)
- State: open; created 2024-12-02T16:46:35Z; status ok; passes main

## Issue body

reporter (MEMBER) · Alan-Jowett · 2024-12-02T16:46:35Z · https://github.com/microsoft/ebpf-for-windows/issues/4063

The netebpfext fuzzer should check for memory leaks.

## Comment 2512138456

maintainer (COLLABORATOR) · shankarseal · 2024-12-02T16:48:48Z · https://github.com/microsoft/ebpf-for-windows/issues/4063#issuecomment-2512138456

Consider the cases where there can be memory leaks on error-paths other than memory allocation.
