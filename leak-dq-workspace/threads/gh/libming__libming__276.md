# allocation-size-too-big in readBytes

- URL: https://github.com/libming/libming/issues/276
- Repo: libming/libming (language: C)
- State: open; created 2023-07-21T03:35:50Z; status ok; passes main

## Issue body

reporter (NONE) · Wayne-Bai · 2023-07-21T03:35:50Z · https://github.com/libming/libming/issues/276

There is an allocation-size-too-big issue and the poc is in the attachment.

command: ``` ./swftophp poc-1```

```
==22513==ERROR: AddressSanitizer: requested allocation size 0xfffffffff7efdfbf (0xfffffffff7efefc0 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x4ad350 in malloc /home/eval/build/llvm_tools/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145
    #1 0x5212ab in readBytes /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/read.c:227:17
    #2 0x51d8c1 in parseABC_STRING_INFO /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/parser.c:3068:30
    #3 0x51e07d in parseABC_CONSTANT_POOL /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/parser.c:3175:5
    #4 0x51fb37 in parseABC_FILE /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/parser.c:3426:3
    #5 0x52033e in parseSWF_DOABC /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/parser.c:3481:3
    #6 0x4fc2b0 in blockParse /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/blocktypes.c:145:14
    #7 0x4fbf39 in readMovie /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/main.c:265:11
    #8 0x4fb633 in main /home/eval/Desktop/libming-CVE-2018-8962/obj-aflgo/util/../../util/main.c:350:2
    #9 0x7fec449f4c86 in __libc_start_main /build/glibc-CVJwZb/glibc-2.27/csu/../csu/libc-start.c:310

==22513==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big /home/eval/build/llvm_tools/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145 in malloc
==22513==ABORTING
```
[poc-1.zip](https://github.com/libming/libming/files/12116025/poc-1.zip)

