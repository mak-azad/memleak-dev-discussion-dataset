# Consider an asdf_free() for buffers the library allocates on the caller's behalf

- URL: https://github.com/asdf-format/libasdf/issues/250
- Repo: asdf-format/libasdf (language: C)
- State: closed; created 2026-09-04T15:29:58Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · cruzzil · 2026-09-04T15:29:58Z · https://github.com/asdf-format/libasdf/issues/250

# Consider an `asdf_free()` for buffers the library allocates on the caller's behalf

Four public entry points allocate a buffer and hand ownership to the caller,
and the documented way to release it is a bare `free()`:

| Function | Header |
|---|---|
| `asdf_write_to_mem` | `asdf/file.h:318` — "a buffer is allocated with `malloc()` … The caller is responsible for freeing the buffer with `free()`." |
| `asdf_ndarray_read_all` | `asdf/core/ndarray.h:463` |
| `asdf_ndarray_read_tile_ndim` | `asdf/core/ndarray.h:492` |
| `asdf_ndarray_read_tile_2d` | `asdf/core/ndarray.h:525` |

That makes the allocator part of the ABI rather than an implementation
detail, which has two consequences.

## Callers can crash on Windows

A DLL and the application linking it can be built against different C runtimes,
and each CRT keeps its own heap. `free()` on a pointer from another CRT's
`malloc()` is undefined and in practice corrupts the heap or aborts. This is
the standard reason libraries that cross a DLL boundary export their own
deallocator, and it applies here as soon as libasdf ships as a DLL.

It is invisible on Linux and macOS, where there is one system allocator, so it
would not show up in CI.

## libasdf cannot change its own allocator

Because the contract names `free()`, these four functions can never use an
arena, a pool, a debug allocator, or a tracking allocator — not even
internally, and not even behind a build flag. A `asdf_config_t` allocator hook,
if one were ever wanted, could not cover them.

The same constraint binds re-implementations. I maintain a Rust implementation
of this ABI ([libasdf-rs](https://github.com/cruzzil/asdf)), and these
four functions are the only places it cannot use Rust's allocator: it has to
call `malloc` directly so that a caller's `free()` is valid. Everything else in
the library is allocator-agnostic.

## Suggested change

Export a deallocator and document it as the way to release these buffers:

```c
/**
 * Free a buffer allocated by libasdf on the caller's behalf
 *
 * Use this for buffers returned by `asdf_write_to_mem`,
 * `asdf_ndarray_read_all` and the `asdf_ndarray_read_tile_*` family when they
 * were asked to allocate. Passing NULL is a no-op.
 */
ASDF_EXPORT void asdf_free(void *ptr);
```

The initial implementation is one line — `free(ptr)` — so this is a
documentation and forward-compatibility change rather than a behavioural one.
It is source-compatible for every existing caller: `free()` keeps working for
as long as the implementation uses `malloc()`, so the docs can recommend
`asdf_free()` and deprecate the bare `free()` at whatever pace suits.

Happy to open a PR if this seems worth doing.


## Comment 5584823321

maintainer (COLLABORATOR) · embray · 2026-09-08T12:03:02Z · https://github.com/asdf-format/libasdf/issues/250#issuecomment-5584823321

Agreed on both points. For the next release I really want to clean up the memory allocation story for libasdf-managed objects, especially frequently used ones like `asdf_value_t`.

Fortunately those all have their own destructors so swapping out allocation strategies can be done easily.

I’m also on the fence about all the functions you mentioned returning raw memory buffers directly as opposed to some wrapper struct, but having at least one function that exposes the raw memory is valuable either way. I agree having an `asdf_free` for those is advantageous.

## Comment 5593278511

reporter (CONTRIBUTOR) · cruzzil · 2026-09-08T23:25:21Z · https://github.com/asdf-format/libasdf/issues/250#issuecomment-5593278511

Agree a wrapper struct is better but you'd still need a destructor for it in some form. 

## Comment 5601383635

maintainer (COLLABORATOR) · embray · 2026-09-09T11:52:21Z · https://github.com/asdf-format/libasdf/issues/250#issuecomment-5601383635

Yep.  That will probably be a future change though, not for now.  
