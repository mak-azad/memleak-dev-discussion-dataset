# Alloc-dealloc-mismatch in function openWavFile

- URL: https://github.com/dilawar/sound/issues/4
- Repo: dilawar/sound (language: C)
- State: open; created 2018-07-24T10:35:37Z; status ok; passes main

## Issue body

reporter (NONE) · fouzhe · 2018-07-24T10:35:37Z · https://github.com/dilawar/sound/issues/4

I used **gcc 5.4 and AddressSanitizer**  to build **[sound](https://github.com/dilawar/sound/commit/357c2c57e2127dbd996b7e7dce90148f08cf7cbf)**, this [file](https://github.com/fouzhe/security/blob/master/sound/alloc_dealloc_mismatch_openWavFile) can cause alloc-dealloc-mismatch when executing this command:

```shell
./parseSpeech -f alloc_dealloc_mismatch_openWavFile
```

This is the ASAN information:

```shell
Input file : alloc_dealloc_mismatch_openWavFileSize of chunk8
wBufferLength : 1080764maxInSamples 1080764
=================================================================
==8789==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x7fcd33711800
    #0 0x7fcd3277cb2a in operator delete(void*) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99b2a)
    #1 0x407655 in WavFile::openWavFile(char*) /home/fouzhe/my_fuzz/sound/src/wav-file.cc:402
    #2 0x4025c2 in main /home/fouzhe/my_fuzz/sound/main.cc:148
    #3 0x7fcd31a9882f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #4 0x402a38 in _start (/home/fouzhe/my_fuzz/sound/parseSpeech+0x402a38)

0x7fcd33711800 is located 0 bytes inside of 1080764-byte region [0x7fcd33711800,0x7fcd338195bc)
allocated by thread T0 here:
    #0 0x7fcd3277c6b2 in operator new[](unsigned long) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x996b2)
    #1 0x4070d9 in WavFile::openWavFile(char*) /home/fouzhe/my_fuzz/sound/src/wav-file.cc:345

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch ??:0 operator delete(void*)
==8789==HINT: if you don't care about these warnings you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==8789==ABORTING
```





