# `malloc(): corrupted top size` after allocating array of polymorphic data type elements

- URL: https://github.com/flang-compiler/flang/issues/1437
- Repo: flang-compiler/flang (language: C)
- State: open; created 2024-01-15T16:16:27Z; status ok; passes offcwe

## Issue body

reporter (COLLABORATOR) · pawosm-arm · 2024-01-15T16:16:27Z · https://github.com/flang-compiler/flang/issues/1437

When the compiler's frontend is generating a piece of IR for `alloc04` call to the Fortran runtime library, for the polymorphic data type the `len` parameter is always 0 (namely, `internal constant i64 0`). The alloc04 function in flang runtime, when it detects that there is a zero-sized memory requirement, replaces it with 16-byte requirement, so there is always valid pointer to allocated memory returned. In the following example, slightly more than 16-bytes is allocated, and since it uses the `Source` parameter for the `Allocate` instruction which causes the allocated memory is immediately filled with `n`'s, it is clearly going beyond the allocated memory:

```
program minalloc
  Integer, parameter :: n = 7
  Class(*),Pointer :: f1(:, :)
  Allocate(f1(n, n), Source = n)
  Print *, Size(f1, 1)
end
```

Note that it is sufficient to get rid of `Source = n`, and the problem goes unnoticed. But it is still there.
In case of latest glibc versions, this always causes `malloc(): corrupted top size` on a subsequent malloc (in the example above, it will happen in the `Print` instruction). In case of the old glibc, it is enough to increase the `n` parameter significantly (e.g. to 4096) and it will also start failing.

