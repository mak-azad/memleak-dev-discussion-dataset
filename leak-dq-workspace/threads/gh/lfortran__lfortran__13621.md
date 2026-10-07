# reshape of a class(t) array: the 16-byte result temporary is overflowed by memmove (class LHS) and is never freed

- URL: https://github.com/lfortran/lfortran/issues/13621
- Repo: lfortran/lfortran (language: C++)
- State: open; created 2026-09-27T01:24:57Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · certik · 2026-09-27T01:24:57Z · https://github.com/lfortran/lfortran/issues/13621

`reshape` of a polymorphic `class(w), allocatable` array allocates a 16-byte heap block for its result. When the result is assigned to another `class(w)` array, `main` copies the whole array data into that block with `memmove` and writes past its end. In every case, including when the result is passed to a `type(w)` dummy, the block is never freed. The overflow happens even when the destination is already allocated and the only component is a scalar `integer`.

## Heap overflow (class to class)

```fortran
program w08
implicit none
type :: w
  integer :: c
end type
class(w), allocatable :: a(:), b(:)
allocate(a(4), b(4))
a%c = [1,2,3,4]
b = reshape(a, [4])
print *, b%c
if (any(b%c /= [1,2,3,4])) error stop 1
end program
```

```console
$ lfortran w08.f90 -o w08.out && valgrind ./w08.out
==17641== Invalid write of size 8
==17641==    at 0x4852E1B: memmove (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==17641==    by 0x109AC2: main (in w08.out)
==17641==  Address 0x4d00110 is 0 bytes after a block of size 16 alloc'd
==17641==    at 0x4846828: malloc (...)
==17641==    by 0x486F383: default_alloc (lfortran_intrinsics.c:300)
==17641==    by 0x4881252: _lfortran_malloc_alloc (lfortran_intrinsics.c:5580)
==17641==    by 0x109737: main (in w08.out)
... (4 invalid 8-byte writes in total)
1 2 3 4
==17641== ERROR SUMMARY: 6 errors from 4 contexts
==17641==    definitely lost: 16 bytes in 1 blocks
```

With larger components the overflow shows up without valgrind. For `character(len=2) :: c` and `b` unallocated, compiled with `--realloc-lhs-arrays`:

```console
zz
free(): invalid next size (fast)
```

With `character(len=2) :: c(3)`, the program prints the wrong value (`ab`) and stops with `ERROR STOP 1`. gfortran runs all of these variants correctly with no valgrind errors.

## Leak (class to a type(w) dummy)

```fortran
program y2
implicit none
type :: w
  integer :: c
end type
class(w), allocatable :: a(:)
allocate(a(4))
a%c = [1,2,3,4]
call s(reshape(a, [2,2]))
contains
subroutine s(x)
  type(w), intent(in) :: x(:,:)
  print *, x%c
  if (x(2,2)%c /= 4) error stop 1
end subroutine
end program
```

```console
$ lfortran y2.f90 -o y2.out && valgrind --leak-check=full ./y2.out
1 2 3 4
==26361== 16 bytes in 1 blocks are definitely lost in loss record 1 of 1
==26361==    at 0x4846828: malloc (...)
==26361==    by 0x486F383: default_alloc (lfortran_intrinsics.c:300)
==26361==    by 0x4881252: _lfortran_malloc_alloc (lfortran_intrinsics.c:5580)
==26361==    by 0x109AFE: main (in y2.out)
```

The values are right here, but the 16-byte block leaks on every `reshape` call.

A copy `b = a` without `reshape` is valgrind-clean, so the problem is specific to the class-array `reshape` result. The wrong values in #13592 (`reshape` of a class array assigned to a `type(w)` array) may come from the same temporary.

Reproduces on main (e9affe9b).

Found while working on lfortran/lfortran#13570
