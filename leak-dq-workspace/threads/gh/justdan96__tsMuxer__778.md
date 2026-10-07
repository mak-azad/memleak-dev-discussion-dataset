# Alloc-dealloc-mismatch on tsMuxer

- URL: https://github.com/justdan96/tsMuxer/issues/778
- Repo: justdan96/tsMuxer (language: C++)
- State: open; created 2023-10-06T08:07:19Z; status ok; passes main

## Issue body

reporter (NONE) · Frank-Z7 · 2023-10-06T08:07:19Z · https://github.com/justdan96/tsMuxer/issues/778

### Description

**We found a alloc-dealloc-mismatch (operator new [] vs operator delete) error when using tsMuxer/tsmuxer.**

### ASAN Log

```shell
=================================================================
==4087327==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0x610000000040
    #0 0x5d946d in operator delete(void*) (/afltest/tsMuxer/tsMuxer/tsmuxer+0x5d946d)
    #1 0x6e88a3 in MatroskaDemuxer::readClose() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1041:42
    #2 0x6fca23 in MatroskaDemuxer::~MatroskaDemuxer() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.h:11:35
    #3 0x6fcc97 in MatroskaDemuxer::~MatroskaDemuxer() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.h:11:33
    #4 0x73ed9e in METADemuxer::DetectStreamReader(BufferedReaderManager const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) /afltest/tsMuxer/tsMuxer/metaDemuxer.cpp:669:9
    #5 0x6bb225 in detectStreamReader(char const*, MPLSParser*, bool) /afltest/tsMuxer/tsMuxer/main.cpp:114:34
    #6 0x6c76ef in main /afltest/tsMuxer/tsMuxer/main.cpp:689:17
    #7 0x7ffff798b082 in __libc_start_main /build/glibc-BHL3KM/glibc-2.31/csu/../csu/libc-start.c:308:16
    #8 0x530d5d in _start (/afltest/tsMuxer/tsMuxer/tsmuxer+0x530d5d)

0x610000000040 is located 0 bytes inside of 184-byte region [0x610000000040,0x6100000000f8)
allocated by thread T0 here:
    #0 0x5d8d1d in operator new[](unsigned long) (/afltest/tsMuxer/tsMuxer/tsmuxer+0x5d8d1d)
    #1 0x6f3be7 in MatroskaDemuxer::matroska_add_stream() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1893:53
    #2 0x6ee754 in MatroskaDemuxer::matroska_parse_tracks() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1746:19
    #3 0x6e9989 in MatroskaDemuxer::matroska_read_header() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1228:19
    #4 0x6e7b5a in MatroskaDemuxer::openFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1027:5
    #5 0x73c0d9 in METADemuxer::DetectStreamReader(BufferedReaderManager const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) /afltest/tsMuxer/tsMuxer/metaDemuxer.cpp:608:18
    #6 0x6bb225 in detectStreamReader(char const*, MPLSParser*, bool) /afltest/tsMuxer/tsMuxer/main.cpp:114:34
    #7 0x6c76ef in main /afltest/tsMuxer/tsMuxer/main.cpp:689:17
    #8 0x7ffff798b082 in __libc_start_main /build/glibc-BHL3KM/glibc-2.31/csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch (/afltest/tsMuxer/tsMuxer/tsmuxer+0x5d946d) in operator delete(void*)
==4087327==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==4087327==ABORTING

```

### Location

0x610000000040 is located 0 bytes inside of 184-byte region [0x610000000040,0x6100000000f8)
allocated by thread T0 here:
    #0 0x5d8d1d in operator new[](unsigned long) (/afltest/tsMuxer/tsMuxer/tsmuxer+0x5d8d1d)
    #1 0x6f3be7 in MatroskaDemuxer::matroska_add_stream() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1893:53
    #2 0x6ee754 in MatroskaDemuxer::matroska_parse_tracks() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1746:19
    #3 0x6e9989 in MatroskaDemuxer::matroska_read_header() /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1228:19
    #4 0x6e7b5a in MatroskaDemuxer::openFile(std::\__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /afltest/tsMuxer/tsMuxer/matroskaDemuxer.cpp:1027:5
    #5 0x73c0d9 in METADemuxer::DetectStreamReader(BufferedReaderManager const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, bool) /afltest/tsMuxer/tsMuxer/metaDemuxer.cpp:608:18
    #6 0x6bb225 in detectStreamReader(char const*, MPLSParser*, bool) /afltest/tsMuxer/tsMuxer/main.cpp:114:34
    #7 0x6c76ef in main /afltest/tsMuxer/tsMuxer/main.cpp:689:17
    #8 0x7ffff798b082 in \__libc_start_main /build/glibc-BHL3KM/glibc-2.31/csu/../csu/libc-start.c:308:16


![image-20231006143638493](https://github.com/justdan96/tsMuxer/assets/67280615/ab3efd40-72b4-4fcd-8fbd-f12f858584aa)

![image-20231006143714557](https://github.com/justdan96/tsMuxer/assets/67280615/04b82d02-5e69-4774-b937-303f071e9727)

![image-20231006143835928](https://github.com/justdan96/tsMuxer/assets/67280615/3a375a1b-51b1-4bb1-a40d-0bb8c5840d28)

![image-20231006144239334](https://github.com/justdan96/tsMuxer/assets/67280615/295340e5-7dd3-4f2d-ae78-96be7b57164e)

![image-20231006151150514](https://github.com/justdan96/tsMuxer/assets/67280615/aed450c4-6329-4753-9893-89f06f89ad24)

![image-20231006151242007](https://github.com/justdan96/tsMuxer/assets/67280615/a5b03961-e1ba-4be0-9756-652f778deb4b)

![image-20231006151341860](https://github.com/justdan96/tsMuxer/assets/67280615/2a6c2910-b0f3-4812-bee6-41d0f9ab909f)

#### Destructor of class MatroskaDemuxer：

![image-20231006151517201](https://github.com/justdan96/tsMuxer/assets/67280615/bddeb039-a2ce-41ec-9c69-d9cc1401ce68)

![image-20231006151642860](https://github.com/justdan96/tsMuxer/assets/67280615/d2e87fd8-a335-4887-877e-34953477b4b5)


### Version

```shell
./tsmuxer --version
tsMuxeR version git-2539d07. github.com/justdan96/tsMuxer
```

tsMuxeR version git-2539d07 is the latest version.

### Reference

https://github.com/justdan96/tsMuxer

### **Actual Behavior**

Alloc-dealloc-mismatch

### PoC

PocTsmuxer.mkv:  https://github.com/Frank-Z7/z-vulnerabilitys/blob/main/PocTsmuxer.mkv

### Reproduction

```shell
cd tsMuxer
./tsMuxer/tsmuxer PocTsmuxer.mkv
```

### Environment

```
ubuntu:20.04
gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.2)
clang version 10.0.0-4ubuntu1
afl-cc++4.09
```

### Credit

Zeng Yunxiang ([[Huazhong University of Science and Technology](http://cse.hust.edu.cn/)](http://cse.hust.edu.cn/))
Song Jiaxuan

## Comment 1772427170

maintainer (COLLABORATOR) · jcdr428 · 2023-10-20T09:53:06Z · https://github.com/justdan96/tsMuxer/issues/778#issuecomment-1772427170

@Frank-Z7 I can't understand the reason for this "mismatch".
tracks is a MatroskaTrack[64]:

![image](https://github.com/justdan96/tsMuxer/assets/56721609/a3968bac-ecd8-4e74-b456-5d22d723ab42)

Edit: ok, so the char[] was cast to a MastroskaTrack object in line 1893. I believe the mismatch is solved simply by casting the MastroskaTrack back to the original char[] then we can delete[].

Commit pushed, can you please check tomorrow's release.
