# ==8524==ERROR: LeakSanitizer: detected memory leaks

- URL: https://github.com/scylladb/seastar/issues/228
- Repo: scylladb/seastar (language: C++)
- State: open; created 2016-12-13T19:18:09Z; status ok; passes main

## Issue body

reporter (NONE) · opope · 2016-12-13T19:18:09Z · https://github.com/scylladb/seastar/issues/228

Centos 7.2, boost 1.58, gcc version 5.2.1, built with
./configure.py --enable-dpdk --static-stdc++

ran the fast tests:
./test.py --fast
and got few of these errors, I assume they are real memory leaks:

=================================================================
==8524==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 1344 byte(s) in 56 object(s) allocated from:
    #0 0x7f50592a6c02 in operator new(unsigned long, std::nothrow_t const&) (/opt/scylladb/lib64/libasan.so.2+0x99c02)
    #1 0x7f5058685d65 in __cxa_thread_atexit (/opt/scylladb/lib64/libstdc++.so.6+0x8bd65)

Indirect leak of 5376 byte(s) in 224 object(s) allocated from:
    #0 0x7f50592a6c02 in operator new(unsigned long, std::nothrow_t const&) (/opt/scylladb/lib64/libasan.so.2+0x99c02)
    #1 0x7f5058685d65 in __cxa_thread_atexit (/opt/scylladb/lib64/libstdc++.so.6+0x8bd65)

SUMMARY: AddressSanitizer: 6720 byte(s) leaked in 280 allocation(s).



## Comment 325047048

other (NONE) · verc11 · 2017-08-25T22:22:05Z · https://github.com/scylladb/seastar/issues/228#issuecomment-325047048

Did you find a solution? I'm running into the same issue on RHEL7 where almost all tests fail with the following leaks-
==19197==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f313f264d7a in realloc (/opt/scylladb/lib64/libasan.so.2+0x98d7a)
    #1 0xffa1cd  (/livevol/seastar-master/build/debug/tests/weak_ptr_test+0xffa1cd)

Indirect leak of 30 byte(s) in 2 object(s) allocated from:
    #0 0x7f313f2649fa in malloc (/opt/scylladb/lib64/libasan.so.2+0x989fa)
    #1 0x7f313ac0d949 in __GI___strdup (/lib64/libc.so.6+0x86949)



## Comment 340261402

other (NONE) · CuthbertJungle · 2017-10-29T13:11:36Z · https://github.com/scylladb/seastar/issues/228#issuecomment-340261402

i also see this on Ubuntu 16.04

==7582==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 176 byte(s) in 2 object(s) allocated from:
    #0 0x7f380f72aec0 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.3+0xc6ec0)
    #1 0x7f3809b5e4a8 in lt__malloc (/usr/lib/x86_64-linux-gnu/libltdl.so.7+0x24a8)

but also have this:
==6469==WARNING: ASan doesn't fully support makecontext/swapcontext functions and may produce false positives in some cases!

so could well be false positives. Not sure how you confirm !

## Comment 421258959

other (CONTRIBUTOR) · tchaikov · 2018-09-14T07:34:34Z · https://github.com/scylladb/seastar/issues/228#issuecomment-421258959

i debugged this leak reported by ASan. and i believe it's caused by libhwloc. it `dlopen()`s its plugins. its plugins are opened using `libltdl` which allocates 88 bytes for each `lt__handle` struct, when `dlopen()` is called. a minimal reproducer can be whipped up with the sequence of 

1. hwloc_topology_init()
1. hwloc_topology_load()
1. hwloc_topology_destroy()


## Comment 555902666

maintainer (MEMBER) · avikivity · 2019-11-20T08:48:27Z · https://github.com/scylladb/seastar/issues/228#issuecomment-555902666

There are two ways to fix this:
1. fix the problem upstream (in  hwloc or libltdl, wherever the problem is) and wait for package updates
2. whitelist these leaks so lsan ignores them

## Comment 782878268

other (CONTRIBUTOR) · balusch · 2021-02-21T15:45:05Z · https://github.com/scylladb/seastar/issues/228#issuecomment-782878268

> i debugged this leak reported by ASan. and i believe it's caused by libhwloc. it `dlopen()`s its plugins. its plugins are opened using `libltdl` which allocates 88 bytes for each `lt__handle` struct, when `dlopen()` is called. a minimal reproducer can be whipped up with the sequence of
> 
> 1. hwloc_topology_init()
> 2. hwloc_topology_load()
> 3. hwloc_topology_destroy()

Hello, I met the same problem caused by libhwloc.so, have you solved it?
