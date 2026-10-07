#  Allocation-size-too-big in parseSWF_DEFINESOUND

- URL: https://github.com/libming/libming/issues/295
- Repo: libming/libming (language: C)
- State: open; created 2023-12-11T07:28:35Z; status ok; passes main

## Issue body

reporter (NONE) · pip-izony · 2023-12-11T07:28:35Z · https://github.com/libming/libming/issues/295

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
[PoC.zip](https://github.com/libming/libming/files/13632176/PoC.zip)
## Expected behavior 
Print error or warning messages handled within swftophp.
## Current behavior
```
header indicates a filesize of 5226 but filesize is 3456
<?php
$m = new SWFMovie(10);

ming_setscale(1.0);
$m->setRate(170.679688);
$m->setDimension(7451, 20678);

/* Note: xMin and/or yMin are not 0! */

$m->setFrames(43582);
/*Unknown block type 577*/
/*Unknown block type 501*/
/*Unknown block type 172*/
/*Unknown block type 488*/
/*Unknown block type 853*/
/*Unknown block type 396*/
/*Unknown block type 378*/
/*Unknown block type 309*/
/*Unknown block type 491*/
/*Unknown block type 243*/
/*Unknown block type 364*/
/*Unknown block type 882*/
/*Unknown block type 453*/
/*Unknown block type 833*/
/*Unknown block type 251*/
/*Unknown block type 293*/
/*Unknown block type 244*/
/*Unknown block type 211*/
/*Unknown block type 813*/
/*Unknown block type 861*/
/*Unknown block type 124*/
/*Unknown block type 919*/
/*Unknown block type 175*/
/*Unknown block type 130*/
/*Unknown block type 543*/
/*Unknown block type 954*/
/*Unknown block type 563*/
/*Unknown block type 273*/
/*Unknown block type 742*/
/*Unknown block type 948*/
/*Unknown block type 161*/
/*Unknown block type 459*/
/*Unknown block type 718*/
/*Unknown block type 217*/
/*Unknown block type 461*/
/*Unknown block type 287*/
/*Unknown block type 488*/
/*Unknown block type 96*/
/*Unknown block type 457*/
 Stream out of sync after parse of blocktype 33 (SWF_DEFINETEXT2). 1724 but expecting 1477.

/* SWF_DEFINETEXT2 */
$character4721 = new SWFText(2);
$character4721->moveTo(0, -22963);
outputSWF_TEXT_RECORD: can't process text record: fonts information list is NULL
$character4721->addString("X");
=================================================================
==1320393==ERROR: AddressSanitizer: requested allocation size 0xfffffffffffffffb (0x800 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x7fe4d24b4887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x55bf19bbff17 in readBytes (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x57f17)
    #2 0x55bf19bb8f74 in parseSWF_DEFINESOUND (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x50f74)
    #3 0x55bf19b8aee4 in blockParse (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x22ee4)
    #4 0x55bf19b8a3ca in readMovie (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x223ca)
    #5 0x55bf19b8ac3d in main (/home/smb8508/Desktop/work_space/debuging/libming/util/swftophp+0x22c3d)
    #6 0x7fe4d2029d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

==1320393==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145 in __interceptor_malloc
==1320393==ABORTING
```
