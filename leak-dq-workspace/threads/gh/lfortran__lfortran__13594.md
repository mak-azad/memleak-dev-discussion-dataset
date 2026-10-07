# Allocatable scalar derived-type function result assigned to a non-allocatable variable crashes (free(): invalid pointer / SIGSEGV)

- URL: https://github.com/lfortran/lfortran/issues/13594
- Repo: lfortran/lfortran (language: C++)
- State: open; created 2026-09-26T23:20:03Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · certik · 2026-09-26T23:20:03Z · https://github.com/lfortran/lfortran/issues/13594

A function whose result is `type(w), allocatable` crashes at run time when its value is assigned to a plain `type(w)` variable. The component is a single `integer`. Assigning the result to a `type(w), allocatable` variable works.

```fortran
program f12b
implicit none
type :: w
  integer :: c
end type
type(w) :: s
s = mk1()
print *, s%c
if (s%c /= 3) error stop 1
contains
function mk1() result(r)
  type(w), allocatable :: r
  allocate(r)
  r%c = 3
end function
end program
```

```
$ lfortran --no-color f12b.f90 -o l && ./l
free(): invalid pointer
Aborted
$ gfortran f12b.f90 && ./a.out
           3
```

When the function is in a module, the crash is the same. With an `integer :: c(3)` or a character-array component, the program segfaults instead. With `type(w), allocatable :: s`, LFortran prints `3`.

Reproduces on main (e9affe9b).

Found while working on lfortran/lfortran#13570
