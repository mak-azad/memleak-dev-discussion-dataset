# Memory leak: nullify of a class(*) pointer array drops its 16-byte class wrapper without freeing it

- URL: https://github.com/lfortran/lfortran/issues/13969
- Repo: lfortran/lfortran (language: C++)
- State: open; created 2026-10-03T21:11:41Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · certik · 2026-10-03T21:11:41Z · https://github.com/lfortran/lfortran/issues/13969

`nullify` on a `class(*), pointer :: up(:)` array pointer discards the 16-byte class wrapper that the preceding pointer association allocated, without freeing it. Each `up => u; nullify(up)` cycle leaks 16 bytes.

## Reproducer

```fortran
program nullify_leak
implicit none
class(*), allocatable, target :: u(:)
class(*), pointer :: up(:)
integer :: i
allocate(u, source=[1,2,3,4,5,6])
do i = 1, 3
    up => u
    nullify(up)
end do
up => u
print *, "ok"
end program
```

## LFortran

```
$ lfortran nullify_leak.f90 -o a_lf && valgrind --leak-check=full ./a_lf
 ok
HEAP SUMMARY:
    in use at exit: 48 bytes in 3 blocks
  total heap usage: 7 allocs, 4 frees, 4,200 bytes allocated

48 bytes in 3 blocks are definitely lost in loss record 1 of 1
   at 0x4846828: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
   by 0x486F3C3: default_alloc (lfortran_intrinsics.c:300)
   by 0x4880A70: _lfortran_malloc_alloc (lfortran_intrinsics.c:5649)
   by 0x109C1C: main (in a_lf)

LEAK SUMMARY:
   definitely lost: 48 bytes in 3 blocks
ERROR SUMMARY: 1 errors from 1 contexts
```

3 nullifies leak 3 x 16 bytes; the final association (not nullified) is freed correctly.

## GFortran

```
$ gfortran nullify_leak.f90 -o a_gf && valgrind --leak-check=full ./a_gf
 ok
   definitely lost: 0 bytes in 0 blocks
ERROR SUMMARY: 0 errors from 0 contexts
```

Reproduces on main (76cf7af).

Found while working on #13606.
