# Allocation-size-too-big in parseSWF_DEFINELOSSLESS2

- URL: https://github.com/libming/libming/issues/297
- Repo: libming/libming (language: C)
- State: open; created 2023-12-11T07:35:23Z; status ok; passes main

## Issue body

reporter (NONE) · pip-izony · 2023-12-11T07:35:23Z · https://github.com/libming/libming/issues/297

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
[PoC.zip](https://github.com/libming/libming/files/13632269/PoC.zip)
## Expected behavior 
Print error or warning messages handled within swftophp.
## Current behavior
```
header indicates a filesize of 169083242 but filesize is 164
<?php
$m = new SWFMovie(10);

ming_setscale(1.0);
$m->setRate(10.078125);
$m->setDimension(1, -2);

/* Note: xMin and/or yMin are not 0! */

$m->setFrames(6165);
=================================================================
==1320439==ERROR: AddressSanitizer: requested allocation size 0xfffffffffffffff9 (0x800 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x7f56906b4887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55e07ceb1f17 in readBytes (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x57f17)
    #2 0x55e07cea337c in parseSWF_DEFINELOSSLESS2 (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x4937c)
    #3 0x55e07ce7cee4 in blockParse (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x22ee4)
    #4 0x55e07ce7c3ca in readMovie (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x223ca)
    #5 0x55e07ce7cc3d in main (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x22c3d)
    #6 0x7f5690229d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

==1320439==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145 in __interceptor_malloc
==1320439==ABORTING
```
