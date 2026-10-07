# Valgrind reports a memory leak.

- URL: https://github.com/damus-io/nostrdb/issues/24
- Repo: damus-io/nostrdb (language: C)
- State: open; created 2024-01-01T22:39:33Z; status ok; passes main

## Issue body

reporter (NONE) · eznix86 · 2024-01-01T22:39:33Z · https://github.com/damus-io/nostrdb/issues/24

here is the full report:
```
valgrind  --leak-check=full  ./ndb search --limit 2 --oldest-first 'nosy ostrich'
==90548== Memcheck, a memory error detector
==90548== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==90548== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==90548== Command: ./ndb search --limit 2 --oldest-first nosy\ ostrich
==90548== 
using db '.'
mdb_env_open failed, error 22
==90548== 
==90548== HEAP SUMMARY:
==90548==     in use at exit: 528 bytes in 2 blocks
==90548==   total heap usage: 9 allocs, 7 frees, 3,146,979 bytes allocated
==90548== 
==90548== 528 (280 direct, 248 indirect) bytes in 1 blocks are definitely lost in loss record 2 of 2
==90548==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==90548==    by 0x11635B: ndb_init (nostrdb.c:3222)
==90548==    by 0x10E557: main (ndb.c:133)
==90548== 
==90548== LEAK SUMMARY:
==90548==    definitely lost: 280 bytes in 1 blocks
==90548==    indirectly lost: 248 bytes in 1 blocks
==90548==      possibly lost: 0 bytes in 0 blocks
==90548==    still reachable: 0 bytes in 0 blocks
==90548==         suppressed: 0 bytes in 0 blocks
==90548== 
==90548== For lists of detected and suppressed errors, rerun with: -s
==90548== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

The memory leak is negligible but it would be nice to add some kind of report in case of memory leak in the CI.

## Comment 1873511629

other (CONTRIBUTOR) · jb55 · 2024-01-01T22:47:11Z · https://github.com/damus-io/nostrdb/issues/24#issuecomment-1873511629

On Mon, Jan 01, 2024 at 02:39:44PM -0800, Bruno Bernard wrote:
>here is the full report:
>```
>valgrind  --leak-check=full  ./ndb search --limit 2 --oldest-first 'nosy ostrich'
>==90548==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
>==90548==    by 0x11635B: ndb_init (nostrdb.c:3222)
>==90548==    by 0x10E557: main (ndb.c:133)
>```
>
>The memory leak is negligible but it would be nice to add some kind of report in case of memory leak in the CI.

how does valgrind determine leaks in this case? of course this is
leaking because free only happens on ndb_destroy.


## Comment 1873528651

reporter (NONE) · eznix86 · 2024-01-01T23:45:55Z · https://github.com/damus-io/nostrdb/issues/24#issuecomment-1873528651

While reading the code, I saw that. But Valgrind spits the memory leaks as it sees it happening during the execution. Even if memory is freed at the end using `ndb_destroy`. _Maybe_ a proper fix would be to free the memory right after it is no longer needed. What do you think ?

Also, it is negligible. 280 Bytes ¯\_(ツ)_/¯ 

## Comment 1873532224

other (CONTRIBUTOR) · jb55 · 2024-01-01T23:58:06Z · https://github.com/damus-io/nostrdb/issues/24#issuecomment-1873532224

On Mon, Jan 01, 2024 at 03:46:06PM -0800, Bruno Bernard wrote:
>While reading the code, I saw that. But Valgrind spits the memory leaks
>as it sees it happening during the execution. Even if memory is freed
>at the end using `ndb_destroy`. _Maybe_ a proper fix would be to free
>the memory right after it is no longer needed. What do you think
>instead of waiting at the end.

That wouldn't make any sense. Everything is needed in ndb until the
database is closed.


## Comment 1873916061

reporter (NONE) · eznix86 · 2024-01-02T11:34:29Z · https://github.com/damus-io/nostrdb/issues/24#issuecomment-1873916061

I agree, but I think it's something related with the calloc. Rather than the ndb itself. I can close the issue. But it would be nice to have some kind of memory leak checker in the CI. What do you think ?

## Comment 1874156714

other (CONTRIBUTOR) · jb55 · 2024-01-02T15:16:12Z · https://github.com/damus-io/nostrdb/issues/24#issuecomment-1874156714

On Tue, Jan 02, 2024 at 03:34:40AM -0800, Bruno Bernard wrote:
>I agree, but I think it's something related with the calloc. Rather
>than the ndb itself. I can close the issue. But it would be nice to
>have some kind of memory leak checker in the CI. What do you think ?

yeah for sure, ideally without these false positives.


## Comment 1874873881

reporter (NONE) · eznix86 · 2024-01-03T05:39:42Z · https://github.com/damus-io/nostrdb/issues/24#issuecomment-1874873881

Valgrind has some suppression features. I will push it for the CI, when I have some time
