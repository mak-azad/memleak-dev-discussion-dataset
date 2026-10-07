# Stack overflow detected by ASan on Linux 32-bit

- URL: https://github.com/bdwgc/bdwgc/issues/978
- Repo: bdwgc/bdwgc (language: C)
- State: open; created 2026-09-28T06:02:29Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · ivmai · 2026-09-28T06:02:29Z · https://github.com/bdwgc/bdwgc/issues/978

Source: master (e50d792d)
Build: https://github.com/ivmai/bdwgc-fork/actions/runs/36379717096/job/108792763453
Config: `ubuntu-latest configure --disable-shared --enable-dynamic-loading --enable-rwlock clang -O0 -fsanitize=address -m32`

Contents of gctest.log:
```
Supported VDBs: manual uffdwp mprotect
Switched to incremental mode
Using userfaultfd in write-protect mode
==10951==Running thread 9859 was not suspended. False leaks are possible.
==10951==Running thread 9929 was not suspended. False leaks are possible.
==10951==Running thread 10024 was not suspended. False leaks are possible.
==10951==Running thread 10025 was not suspended. False leaks are possible.
==10951==Running thread 10026 was not suspended. False leaks are possible.
==10951==Running thread 10030 was not suspended. False leaks are possible.
==10951==Running thread 10031 was not suspended. False leaks are possible.
==10951==Running thread 10032 was not suspended. False leaks are possible.
==10951==Running thread 10064 was not suspended. False leaks are possible.
==10951==Running thread 10128 was not suspended. False leaks are possible.
==10956==Running thread 9859 was not suspended. False leaks are possible.
==10956==Running thread 9929 was not suspended. False leaks are possible.
==10956==Running thread 10024 was not suspended. False leaks are possible.
==10956==Running thread 10025 was not suspended. False leaks are possible.
==10956==Running thread 10026 was not suspended. False leaks are possible.
==10956==Running thread 10030 was not suspended. False leaks are possible.
==10956==Running thread 10031 was not suspended. False leaks are possible.
==10956==Running thread 10032 was not suspended. False leaks are possible.
==10956==Running thread 10064 was not suspended. False leaks are possible.
==10956==Running thread 10128 was not suspended. False leaks are possible.
GC Warning: Heap grown by 87368 KiB while GC was disabled
AddressSanitizer:DEADLYSIGNAL
=================================================================
==10965==ERROR: AddressSanitizer: stack-overflow on address 0xe8efa100 (pc 0x5bbf3c4c bp 0xe8ef8928 sp 0xe8ef8860 T8)
    #0 0x5bbf3c4c in GC_mark_from /home/runner/work/bdwgc-fork/bdwgc-fork/build/../mark.c:970:20
    #1 0x5bbf2ab2 in GC_mark_some /home/runner/work/bdwgc-fork/bdwgc-fork/build/../mark.c:523:7
    #2 0x5bbc83be in GC_stopped_mark /home/runner/work/bdwgc-fork/bdwgc-fork/build/../alloc.c:979:9
    #3 0x5bbc7893 in GC_try_to_collect_inner /home/runner/work/bdwgc-fork/bdwgc-fork/build/../alloc.c:680:8
    #4 0x5bbcc0d7 in GC_try_to_collect_general /home/runner/work/bdwgc-fork/bdwgc-fork/build/../alloc.c:1454:12
    #5 0x5bbcc2bb in GC_gcollect /home/runner/work/bdwgc-fork/bdwgc-fork/build/../alloc.c:1486:9
    #6 0x5bbbc521 in run_one_test /home/runner/work/bdwgc-fork/bdwgc-fork/build/../tests/gctest.c:1784:5
    #7 0x5bbb8ea8 in thr_run_one_test /home/runner/work/bdwgc-fork/bdwgc-fork/build/../tests/gctest.c:2367:3
    #8 0x5bc2e8ac in GC_pthread_start_inner /home/runner/work/bdwgc-fork/bdwgc-fork/build/../pthread_start.c:62:12
    #9 0x5bc01fd7 in GC_call_with_stack_base /home/runner/work/bdwgc-fork/bdwgc-fork/build/../misc.c:2562:12
    #10 0x5bc21aba in GC_pthread_start /home/runner/work/bdwgc-fork/bdwgc-fork/build/../pthread_support.c:2845:10
    #11 0x5bb72933 in asan_thread_start(void*) asan_interceptors.cpp.o
    #12 0xf2674f76  (/lib32/libc.so.6+0x8af76) (BuildId: a6ac4013957ce900e167743cd60a25daff1344bb)
    #13 0xf2709c67  (/lib32/libc.so.6+0x11fc67) (BuildId: a6ac4013957ce900e167743cd60a25daff1344bb)

SUMMARY: AddressSanitizer: stack-overflow /home/runner/work/bdwgc-fork/bdwgc-fork/build/../mark.c:970:20 in GC_mark_from
Thread T8 created by T0 here:
    #0 0x5bb5a693 in pthread_create (/home/runner/work/bdwgc-fork/bdwgc-fork/build/gctest+0xa2693) (BuildId: b65584a13c433c441d96023cf7b1cc5c557a7823)
    #1 0x5bc21898 in GC_pthread_create /home/runner/work/bdwgc-fork/bdwgc-fork/build/../pthread_support.c:2929:12
    #2 0x5bbb7aa3 in main /home/runner/work/bdwgc-fork/bdwgc-fork/build/../tests/gctest.c:2556:17
    #3 0xf260ec74  (/lib32/libc.so.6+0x24c74) (BuildId: a6ac4013957ce900e167743cd60a25daff1344bb)

==10965==ABORTING
Child process failed, pid= 10965, status= 0x100
Test failed
==10974==Running thread 9859 was not suspended. False leaks are possible.
...
==10975==Running thread 10128 was not suspended. False leaks are possible.
FAIL gctest (exit status: 134)
```

