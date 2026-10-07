# Alloc-dealloc-mismatch 

- URL: https://github.com/thunlp/THULAC/issues/37
- Repo: thunlp/THULAC (language: C++)
- State: open; created 2018-07-18T02:34:19Z; status ok; passes main

## Issue body

reporter (NONE) · fCorleone · 2018-07-18T02:34:19Z · https://github.com/thunlp/THULAC/issues/37

When I give an empty file to the program train_c, I found this issue:
```
=================================================================
==19071==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x7f51e6a9b800
    #0 0x7f51e5ac4b2a in operator delete(void*) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99b2a)
    #1 0x404318 in thulac::TaggingLearner::~TaggingLearner() include/cb_tagging_learner.h:48
    #2 0x404318 in main src/train_c.cc:65
    #3 0x7f51e50e982f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #4 0x404c98 in _start (/home/mfc_fuzz/newprogram/THULAC/train_c+0x404c98)

0x7f51e6a9b800 is located 0 bytes inside of 200000-byte region [0x7f51e6a9b800,0x7f51e6acc540)
allocated by thread T0 here:
    #0 0x7f51e5ac46b2 in operator new[](unsigned long) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x996b2)
    #1 0x403ff8 in thulac::TaggingLearner::TaggingLearner(int, int, int) include/cb_tagging_learner.h:42
    #2 0x403ff8 in main src/train_c.cc:57
    #3 0x464fdf  (/home/mfc_fuzz/newprogram/THULAC/train_c+0x464fdf)

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch ??:0 operator delete(void*)
==19071==HINT: if you don't care about these warnings you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==19071==ABORTING
```
