# [BUG] Global-buffer-overflow in `wav2swf` in `lib/wav.c:245:24`

- URL: https://github.com/swftools/swftools/issues/239
- Repo: swftools/swftools (language: C)
- State: open; created 2025-03-24T06:58:07Z; status ok; passes main

## Issue body

reporter (NONE) · JJLeo · 2025-03-24T06:58:07Z · https://github.com/swftools/swftools/issues/239

## Description

- Version: Latest commit [`c6a18ab`](https://github.com/swftools/swftools/commit/c6a18ab0658286f98d6ed2b3d0419058e86a14a0)
- Environment:Ubuntu 20.04.6 LTS, Clang 10.0.0

## Steps to reproduce

```bash
export CC="clang -fsanitize=address -g -O0"
export CXX="clang++ -fsanitize=address -g -O0"
./configure && make -j$(nproc)
./src/wav2swf $POC
```

## Sanitizer output

```
root@2dca640e5e71:~/swftools# ./src/wav2swf /root/wav2swf_crash.in 
wav_read: warning - short file (808464404 bytes missing)
=================================================================
==275950==ERROR: AddressSanitizer: global-buffer-overflow on address 0x0000005dbc70 at pc 0x0000005c0665 bp 0x7ffcb11f9400 sp 0x7ffcb11f93f8
READ of size 1 at 0x0000005dbc70 thread T0
    #0 0x5c0664 in wav_convert2mono /root/swftools/lib/wav.c:245:24
    #1 0x4c514f in main /root/swftools/src/wav2swf.c:236:9
    #2 0x7126e3fc7082 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x24082)
    #3 0x41c56d in _start (/root/swftools/src/wav2swf+0x41c56d)

0x0000005dbc70 is located 48 bytes to the left of global variable '<string literal>' defined in 'wav2swf.c:65:22' (0x5dbca0) of size 2
  '<string literal>' is ascii string 'V'
0x0000005dbc70 is located 5 bytes to the right of global variable '<string literal>' defined in 'wav2swf.c:30:21' (0x5dbc60) of size 11
  '<string literal>' is ascii string 'output.swf'
SUMMARY: AddressSanitizer: global-buffer-overflow /root/swftools/lib/wav.c:245:24 in wav_convert2mono
Shadow bytes around the buggy address:
  0x0000800b3730: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0000800b3740: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0000800b3750: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0000800b3760: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0000800b3770: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0000800b3780: 00 00 00 00 00 00 00 00 00 00 00 00 00 03[f9]f9
  0x0000800b3790: f9 f9 f9 f9 02 f9 f9 f9 f9 f9 f9 f9 00 00 00 01
  0x0000800b37a0: f9 f9 f9 f9 00 01 f9 f9 f9 f9 f9 f9 06 f9 f9 f9
  0x0000800b37b0: f9 f9 f9 f9 02 f9 f9 f9 f9 f9 f9 f9 02 f9 f9 f9
  0x0000800b37c0: f9 f9 f9 f9 02 f9 f9 f9 f9 f9 f9 f9 02 f9 f9 f9
  0x0000800b37d0: f9 f9 f9 f9 02 f9 f9 f9 f9 f9 f9 f9 02 f9 f9 f9
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==275950==ABORTING
```


## POC
 
[wav2swf_crash.txt](https://github.com/user-attachments/files/19415662/wav2swf_crash.txt)

## Credit

Reported by Yifan Zhang, [PLL](https://pl.cs.pku.edu.cn/en/)

## Comment 2780218965

reporter (NONE) · JJLeo · 2025-04-05T05:08:31Z · https://github.com/swftools/swftools/issues/239#issuecomment-2780218965

Please let me know if you encounter any issues reproducing it — I can upload a Docker image to help.
