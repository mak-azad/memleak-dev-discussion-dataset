# Memory leak on edge condition in reallocation -- general behavior of allocation functions?

- URL: https://github.com/AeneasVerif/eurydice/issues/393
- Repo: AeneasVerif/eurydice (language: C)
- State: open; created 2026-04-07T19:57:18Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · protz · 2026-04-07T19:57:18Z · https://github.com/AeneasVerif/eurydice/issues/393

From Claude (Opus 4.6):

This needs careful investigation because the underlying Rust function is infallible (per my comment in the source code). See https://doc.rust-lang.org/std/vec/struct.Vec.html#method.resize -- meaning that this might be another case of "Rust panics, Eurydice has some other unspecified behavior".

But perhaps for memory allocation functions we want to try harder and actually abort. To be discussed.

### 11. `alloc_vec_resize` leaks memory on realloc failure

**_JP_**: perhaps legit, TBD

**File:** `eurydice_glue.h:501`

```c
(v)->ptr = EURYDICE_REALLOC((v)->ptr, new_len * sizeof(T));
```

If `realloc` returns NULL, the original pointer is overwritten and lost. The allocated memory leaks, and subsequent accesses dereference NULL.

**Test snippet:**
```c
// When system is near OOM:
Eurydice_vec v = Eurydice_vec_alloc2(10, sizeof(int));
// Fill v...
// Now attempt a huge resize:
alloc_vec__alloc__vec__Vec_T___resize(&v, SIZE_MAX / 2, 0, int, _, _);
// realloc returns NULL; v.ptr is now NULL; original 40 bytes leaked
```

**Suggested fix:**
```c
    else {                                                                     \
      char *new_ptr = EURYDICE_REALLOC((v)->ptr, new_len * sizeof(T));         \
      if (new_ptr == NULL) {                                                   \
        fprintf(stderr, "vec resize: allocation failed\n");                    \
        exit(255);                                                             \
      }                                                                        \
      (v)->ptr = new_ptr;                                                      \
      for (size_t i = (v)->len; i < new_len; i++)                              \
        ((T *)(v)->ptr)[i] = elt;                                              \
      (v)->len = new_len;                                                      \
      (v)->capacity = new_len;                                                 \
    }
```

