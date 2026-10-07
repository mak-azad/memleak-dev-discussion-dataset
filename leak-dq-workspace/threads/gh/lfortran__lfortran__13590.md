# Memory leak: wr = [wr, wrap(s)] leaks the character buffer of a nested derived-type component

- URL: https://github.com/lfortran/lfortran/issues/13590
- Repo: lfortran/lfortran (language: C++)
- State: open; created 2026-09-26T23:18:44Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · certik · 2026-09-26T23:18:44Z · https://github.com/lfortran/lfortran/issues/13590

Growing an allocatable array with an array constructor leaks the string buffer of a nested component when the new element is a structure constructor. Here the element type contains a derived type with a `character` component. valgrind reports one buffer lost per constructor element.

```fortran
program e
implicit none
type :: w
    character(len=2) :: c
end type
type :: wrap
    type(w) :: inner
end type
type(w) :: s
type(wrap), allocatable :: wr(:)
s%c = 'ab'
allocate(wr(1))
wr = [wr, wrap(s)]
print *, wr(2)%inner%c
end program
```

```
$ lfortran --no-color --realloc-lhs-arrays e.f90 -o le && valgrind --leak-check=full ./le
ab
==25160== 2 bytes in 1 blocks are definitely lost in loss record 1 of 1
==25160==    at 0x4846828: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==25160==    by 0x486F383: default_alloc (lfortran_intrinsics.c:300)
==25160==    by 0x4881252: _lfortran_malloc_alloc (lfortran_intrinsics.c:5580)
==25160==    by 0x1093E9: main
==25160==    definitely lost: 2 bytes in 1 blocks
```

The output is correct. Only the buffer is leaked. Variants that do not leak:

- `wr = [wrap(s), wrap(s)]` into a fixed-size `wr(2)`
- `x = wrap(s)` into a scalar
- `ws = [ws, s]` with `type(w), allocatable :: ws(:)`
- `wr = [wr(1), wr(2)]`

Reference compiler: GFortran 13.3 compiles and runs the program (`ab`), but its own temporary also leaks (4 bytes definitely lost), so it cannot serve as a leak-free reference. The LFortran leak is separate: an LFortran-allocated string buffer from `_lfortran_malloc_alloc` in `main` is never freed.

Reproduces on main (e9affe9b).

Found while working on lfortran/lfortran#13570
