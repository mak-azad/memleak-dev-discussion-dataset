# Implement maximum amount of memory for a container to grow to in WAMR

- URL: https://github.com/project-ocre/ocre-runtime/issues/117
- Repo: project-ocre/ocre-runtime (language: C)
- State: open; created 2026-01-07T14:58:20Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · kr-t · 2026-01-07T14:58:20Z · https://github.com/project-ocre/ocre-runtime/issues/117

Maximum memory size is allocated in `wasm_memory.c` on line 1960:
```C
map_size = max_page_count * num_bytes_per_page;
```
WASM page is 65k, while max_page_count is configurable either via binary compilation with flag: `--max-memory=4194304` or with module instantiation during the runtime:
```C
	/* Limit max memory pages to prevent excessive memory allocation with shared memory */
	InstantiationArgs inst_args = {
		.default_stack_size = curr_container_arguments->stack_size,
		.host_managed_heap_size = curr_container_arguments->heap_size,
		.max_memory_pages = 64  /* Limit to 64 pages = 4MB max */
	};
```

We would like the runtime to be configurable during the runtime, both in shell while creating the container and via API calls.

On Linux systems it's not an issue due to how memory is growing via virtualization, but it's an issue on Zephyr port. We want to be able to run containers which were compiled with unnecessary big `--max-memory` parameters via runtime configuration.
