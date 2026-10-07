# Valgrind "Conditional jump or move depends on uninitialised value"

- URL: https://github.com/jnz/q3vm/issues/33
- Repo: jnz/q3vm (language: C)
- State: open; created 2022-12-15T13:43:21Z; status ok; passes offcwe

## Issue body

reporter (NONE) · mingodad · 2022-12-15T13:43:21Z · https://github.com/jnz/q3vm/issues/33

When testing `bin/linux/q3cpp`:
```
valgrind bin/linux/q3cpp bg_lib.c > /dev/null
==32739== Memcheck, a memory error detector
==32739== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32739== Using Valgrind-3.17.0 and LibVEX; rerun with -h for copyright info
==32739== Command: bin/linux/q3cpp bg_lib.c
==32739== 
==32739== Conditional jump or move depends on uninitialised value(s)
==32739==    at 0x10E9DC: substargs (macro.c:340)
==32739==    by 0x10E339: expand (macro.c:201)
==32739==    by 0x10E17A: expandrow (macro.c:164)
==32739==    by 0x10AFB5: process (cpp.c:77)
==32739==    by 0x10AE10: main (cpp.c:39)
==32739== 
==32739== 
==32739== HEAP SUMMARY:
==32739==     in use at exit: 50,801 bytes in 665 blocks
==32739==   total heap usage: 934 allocs, 269 frees, 130,682 bytes allocated
==32739== 
==32739== LEAK SUMMARY:
==32739==    definitely lost: 854 bytes in 151 blocks
==32739==    indirectly lost: 0 bytes in 0 blocks
==32739==      possibly lost: 1,396 bytes in 344 blocks
==32739==    still reachable: 48,551 bytes in 170 blocks
==32739==         suppressed: 0 bytes in 0 blocks
==32739== Rerun with --leak-check=full to see details of leaked memory
==32739== 
==32739== Use --track-origins=yes to see where uninitialised values come from
==32739== For lists of detected and suppressed errors, rerun with: -s
==32739== ERROR SUMMARY: 2 errors from 1 contexts (suppressed: 0 from 0)
```
