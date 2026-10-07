# Possible memory leak

- URL: https://github.com/clibs/buffer/issues/20
- Repo: clibs/buffer (language: C)
- State: open; created 2026-06-04T19:09:19Z; status ok; passes main

## Issue body

reporter (NONE) · Florisheinen1 · 2026-06-04T19:09:19Z · https://github.com/clibs/buffer/issues/20

I have encountered an error with a possible memory leak and an out-of-bounds memory access as a result:

https://github.com/clibs/buffer/blob/736ba3cc161d6ab2ac64303ed3c14ccce42e12a5/buffer.c#L134-L138

1. The `len` variable gets set even when the `realloc` call fails, resulting in out-of-bounds reads and writes.
2. According to the [C reference](https://en.cppreference.com/c/memory/realloc),the original pointer is still valid if the reallocation fails. In the current implementation, it immediately overwrites both `self->alloc` as well as `self->data` before it returns, making it impossible to free the original allocation. Unless of course the caller has a copy of the allocation pointer, but that seems quite unlikely to me.

Fixing this would be relatively straightforward, through some reordering of statements and storing the reallocation result in a temporary value.
