# Allocation-size-too-big in parseSWF_DEFINELOSSLESS

- URL: https://github.com/libming/libming/issues/296
- Repo: libming/libming (language: C)
- State: open; created 2023-12-11T07:33:04Z; status ok; passes main

## Issue body

reporter (NONE) · pip-izony · 2023-12-11T07:33:04Z · https://github.com/libming/libming/issues/296

## Environment
Ubuntu 22.04.3 LTS
## Compiler
clang version 11.0.0
Target: x86_64-unknown-linux-gnu
Thread model: posix
## Step to reproduce
```cd libming 
./autogen.sh
./configure --disable-shared --disable-freetype
cd util
./swftophp <PoC file>
```
## Contents of PoC file
```
Unzip the file below.
```
[PoC.zip](https://github.com/libming/libming/files/13632243/PoC.zip)
## Expected behavior 
Print error or warning messages handled within swftophp.
## Current behavior
```
header indicates a filesize of 117901066 but filesize is 185
<?php
$m = new SWFMovie(10);

ming_setscale(1.0);
$m->setRate(7.027344);
$m->setDimension(0, 0);
$m->setFrames(22279);
=================================================================
==1320433==ERROR: AddressSanitizer: requested allocation size 0xfffffffffffffffe (0x800 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x7f8af5eb4887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x563438bf7f17 in readBytes (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x57f17)
    #2 0x563438be900b in parseSWF_DEFINELOSSLESS (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x4900b)
    #3 0x563438bc2ee4 in blockParse (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x22ee4)
    #4 0x563438bc23ca in readMovie (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x223ca)
    #5 0x563438bc2c3d in main (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x22c3d)
    #6 0x7f8af5a29d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

==1320433==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145 in __interceptor_malloc
==1320433==ABORTING
```
