# 'interceptor_via_lib' not working when issue happens in third-party lib dl_init

- URL: https://github.com/google/sanitizers/issues/1849
- Repo: google/sanitizers (language: C)
- State: open; created 2025-02-18T10:26:39Z; status ok; passes main

## Issue body

reporter (NONE) · myk502 · 2025-02-18T10:26:39Z · https://github.com/google/sanitizers/issues/1849

Hi, I meet up with an issue with address sanitizer. It complains about 'attempting free on address which was not malloc()' error which happens during a third party lib (libtorch_cpu.so) initilization step, but I can not supress it with interceptor_via_lib options.

So here is my suppresion file:

`
interceptor_via_lib=libtorch_cpu.so
interceptor_via_fun=dnnl_engine_create
`
And this is my ASAN_OPTIONS: 
`
export ASAN_OPTIONS=suppressions=./myasan.supp
`

However when I run the program with all these supressions enabled, I still get the error:

> ==1698675==ERROR:_AddressSanitizer:_attempting free on address which was not malloc()-ed: 0x7f5cb661cf00 in thread T0
#0 0x7f5d55ee340f in interceptor free ../../../../ssrc/libsanitizer/asan/asan_malloc linux.cc:122
#1 0x7f5d5066ba8c in dnnl_engine_create (/usr/local/1ib/python3.8/dist-packages/torch/lib/libtorch_cpu.so+0x5583a8c)
#2 0x7f5d4c809de4 in ideep::engine::cpu engine() (/usr/local/lib/python3.8/distpackages/torch/lib/libtorch_cpu.so+0x1721de4)
#3 0x7f5d4c010b79 in _GLOBAL_sub_I_IDeepRegistration.cpp (/usr/local/lib/jpython3.8/dist-packages/torch/lib/libtorch_cpu.so+0xf28b79
#4 0x7f5d5682cb99 in call init/build/glibc-FcRMWW/glibc-2.31/el:/dl-init.c:72
#5 0x7f5d5682cca0 in call_init /build/glibc-FcPRMWW/glibc-2.31/elf/dl-init.c:30
#6 0x7f5d5682cca0 in _dl_init /build/glibc-FcRMwW/glibc-2.31/elf/dl-iinit.c:119
#7 0x7f5d5681c139 (/lib64/ld-linux-x86-64.so.2+0x1139)
Address 0x7f5cb66lcf00 is a wild pointer.
SUMMARY: AddressSanitizer: bad-free ../../../.../src/libsanitizer/asan/asan_malloc linux.cc:122in interceptor free
==1698675==ABORTING


## Comment 2665218898

reporter (NONE) · myk502 · 2025-02-18T10:30:13Z · https://github.com/google/sanitizers/issues/1849#issuecomment-2665218898

So is there any way asan could actually supress the error & warning happened during dl_init here in third party lib?

## Comment 3231680640

other (NONE) · mariadb-RoelVandePaar · 2025-08-28T03:25:42Z · https://github.com/google/sanitizers/issues/1849#issuecomment-3231680640

Try this syntax (`:` instead of `=`). Also make sure to use a recent Clang/LLVM etc.
```
interceptor_via_lib:libtorch_cpu.so
interceptor_via_fun:dnnl_engine_create
```
Use one line per suppression. 

Also note that comments after suppression are not allowed. They have to be above it, like this:
```
# some comment
some_suppression
```
