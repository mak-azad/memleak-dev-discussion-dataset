# New issue: alloc-dealloc-mismatch

- URL: https://github.com/cmu462/DrawSVG/issues/12
- Repo: cmu462/DrawSVG (language: C)
- State: open; created 2022-07-06T08:10:17Z; status ok; passes main

## Issue body

reporter (NONE) · Cvjark · 2022-07-06T08:10:17Z · https://github.com/cmu462/DrawSVG/issues/12

Hi, i found something unusual in this repo, is it some kind of new bug ?

### sample file 
[id3_alloc-dealloc-mismatch.zip](https://github.com/cmu462/DrawSVG/files/9052908/id3_alloc-dealloc-mismatch.zip)


### reproduce
command to reproduce : `./drawsvg [sample file]`
The command will open a new window to display the svg file, close it and the crash info are as fellowed.

### crash info
```
==41561==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x7ff1d825f800
    #0 0x536d40 in operator delete(void*) /home/bupt/Desktop/tools/llvm-12.0.1/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cpp:160
    #1 0x5bc830 in CMU462::OSDText::~OSDText() /home/bupt/Desktop/DrawSVG/CMU462/src/osdtext.cpp:35:3
    #2 0x591428 in CMU462::Viewer::~Viewer() /home/bupt/Desktop/DrawSVG/CMU462/src/viewer.cpp:56:3
    #3 0x582515 in main /home/bupt/Desktop/DrawSVG/src/main.cpp:116:1
    #4 0x7ff1e6f12c86 in __libc_start_main /build/glibc-CVJwZb/glibc-2.27/csu/../csu/libc-start.c:310
    #5 0x45e1b9 in _start (/home/bupt/Desktop/DrawSVG/bu/drawsvg+0x45e1b9)

0x7ff1d825f800 is located 0 bytes inside of 264372-byte region [0x7ff1d825f800,0x7ff1d82a00b4)
allocated by thread T0 here:
    #0 0x5364a8 in operator new[](unsigned long) /home/bupt/Desktop/tools/llvm-12.0.1/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cpp:102
    #1 0x5bdb1e in CMU462::OSDText::init(bool) /home/bupt/Desktop/DrawSVG/CMU462/src/osdtext.cpp:58:10
    #2 0x591c2b in CMU462::Viewer::init() /home/bupt/Desktop/DrawSVG/CMU462/src/viewer.cpp:124:17
    #3 0x5824cb in main /home/bupt/Desktop/DrawSVG/src/main.cpp:110:10
    #4 0x7ff1e6f12c86 in __libc_start_main /build/glibc-CVJwZb/glibc-2.27/csu/../csu/libc-start.c:310

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch /home/bupt/Desktop/tools/llvm-12.0.1/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cpp:160 in operator delete(void*)
==41561==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==41561==ABORTING
```


