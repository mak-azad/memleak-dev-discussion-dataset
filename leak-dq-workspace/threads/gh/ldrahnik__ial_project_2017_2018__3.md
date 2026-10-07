# Valgrind

- URL: https://github.com/ldrahnik/ial_project_2017_2018/issues/3
- Repo: ldrahnik/ial_project_2017_2018 (language: C)
- State: open; created 2020-07-29T09:33:02Z; status ok; passes main

## Issue body

reporter (OWNER) · ldrahnik · 2020-07-29T09:33:02Z · https://github.com/ldrahnik/ial_project_2017_2018/issues/3

```
valgrind --leak-check=full --track-origins=yes -v ./shreya -i ./tests/test08.in A D -d -o

==5625== 
==5625== HEAP SUMMARY:
==5625==     in use at exit: 128 bytes in 1 blocks
==5625==   total heap usage: 124 allocs, 123 frees, 14,154 bytes allocated
==5625== 
==5625== Searching for pointers to 1 not-freed blocks
==5625== Checked 70,984 bytes
==5625== 
==5625== 128 bytes in 1 blocks are definitely lost in loss record 1 of 1
==5625==    at 0x4C31D2F: realloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
==5625==    by 0x1093BC: parseInputToGraphRoute (graph.c:118)
==5625==    by 0x109E4B: getGraph (graph.c:276)
==5625==    by 0x10B550: main (shreya.c:65)
==5625== 
==5625== LEAK SUMMARY:
==5625==    definitely lost: 128 bytes in 1 blocks
==5625==    indirectly lost: 0 bytes in 0 blocks
==5625==      possibly lost: 0 bytes in 0 blocks
==5625==    still reachable: 0 bytes in 0 blocks
==5625==         suppressed: 0 bytes in 0 blocks
==5625== 
==5625== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
==5625== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
