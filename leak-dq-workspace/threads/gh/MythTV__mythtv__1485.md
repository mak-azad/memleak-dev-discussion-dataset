# mythpreviewgen has memory allocation/deallocation mismatch

- URL: https://github.com/MythTV/mythtv/issues/1485
- Repo: MythTV/mythtv (language: C++)
- State: open; created 2026-09-11T06:38:40Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · SteveErl · 2026-09-11T06:38:40Z · https://github.com/MythTV/mythtv/issues/1485

<!--
Thank you for reporting an issue in MythTV.

This issue tracker is for bugs and issues found within MythTV.
If you require more general support please see the support section
of our website: https://www.mythtv.org/support


Please fill in as much of the template below as you're able to.

Platform: Distro and output of `uname -a` (Linux/UNIX), or version and 32/64-bit (Windows)
MythTV version: the version of MythTV you are running (master, fixes/31, etc)
Package version: if using a packaged version of MythTV, please provide repository/version
Component: if known, please specify the affected component (e.g. frontend/backend)
-->

* **Platform**: Linux Mint 22.3, 6.8.0-136-generic 136-Ubuntu SMP PREEMPT_DYNAMIC Wed Jul 1 21:53:05 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux, Qt version 6.4.2

* **MythTV version**: v36, v37-Pre

* **Package version**:

* **Component**: _mythpreviewgen_

### What steps will reproduce the bug?

<!--
Please enter details about your bug, preferably including simple navigation
instructions to reproduce the bug in mythfrontend, or the startup options you
are using for any MythTV command line applications.
-->
A build with **AddressSanitizer** enabled shows the following error when **mythpreviewgen** is run.
```
$ /usr/bin/mythpreviewgen --size 0x0 --chanid 4187 --starttime 20260911033500
==2142048==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete []) on 0x72c41dce5800
    #0 0x72c4504ff1f8 in operator delete[](void*) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:155
    #1 0x72c44d918401 in PreviewGenerator::LocalPreviewRun() /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/previewgenerator.cpp:717
    #2 0x72c44d907a6d in PreviewGenerator::RunReal() /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/previewgenerator.cpp:144
    #3 0x5cfb96c3b0ae in preview_helper(unsigned int, QDateTime, long long, std::chrono::duration<long, std::ratio<1l, 1l> >, QSize, QString const&, QString const&) /home/uma/build/myth36Steve/mythtv/mythtv/programs/mythpreviewgen/mythpreviewgen.cpp:107
    #4 0x5cfb96c3c5ae in main /home/uma/build/myth36Steve/mythtv/mythtv/programs/mythpreviewgen/mythpreviewgen.cpp:179
    #5 0x72c44b22a1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #6 0x72c44b22a28a in __libc_start_main_impl ../csu/libc-start.c:360
    #7 0x5cfb96c39c24 in _start (/usr/bin/mythpreviewgen+0xbc24) (BuildId: 62356cc66fd7c2ee63581d78fd0a7399daacb8fe)

0x72c41dce5800 is located 0 bytes inside of 3686464-byte region [0x72c41dce5800,0x72c41e069840)
allocated by thread T0 here:
    #0 0x72c4504fcf1d in posix_memalign ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x72c448c4acc4 in av_malloc libavutil/mem.c:107
    #2 0x72c44da317fc in MythVideoFrame::CreateBuffer(VideoFrameType, int, int) /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/mythframe.cpp:442
    #3 0x72c44e53da9b in MythPreviewPlayer::GetScreenGrabAtFrame(unsigned long, bool, int&, int&, int&, float&) /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/mythpreviewplayer.cpp:136
    #4 0x72c44e53bc5e in MythPreviewPlayer::GetScreenGrab(std::chrono::duration<long, std::ratio<1l, 1l> >, int&, int&, int&, float&) /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/mythpreviewplayer.cpp:33
    #5 0x72c44d91b9f3 in PreviewGenerator::GetScreenGrab(ProgramInfo const&, QString const&, std::chrono::duration<long, std::ratio<1l, 1l> >, long long, int&, int&, int&, float&) /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/previewgenerator.cpp:839
    #6 0x72c44d917f2f in PreviewGenerator::LocalPreviewRun() /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/previewgenerator.cpp:695
    #7 0x72c44d907a6d in PreviewGenerator::RunReal() /home/uma/build/myth36Steve/mythtv/mythtv/libs/libmythtv/previewgenerator.cpp:144
    #8 0x5cfb96c3b0ae in preview_helper(unsigned int, QDateTime, long long, std::chrono::duration<long, std::ratio<1l, 1l> >, QSize, QString const&, QString const&) /home/uma/build/myth36Steve/mythtv/mythtv/programs/mythpreviewgen/mythpreviewgen.cpp:107
    #9 0x5cfb96c3c5ae in main /home/uma/build/myth36Steve/mythtv/mythtv/programs/mythpreviewgen/mythpreviewgen.cpp:179
    #10 0x72c44b22a1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #11 0x72c44b22a28a in __libc_start_main_impl ../csu/libc-start.c:360
    #12 0x5cfb96c39c24 in _start (/usr/bin/mythpreviewgen+0xbc24) (BuildId: 62356cc66fd7c2ee63581d78fd0a7399daacb8fe)

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch ../../../../src/libsanitizer/asan/asan_new_delete.cpp:155 in operator delete[](void*)
```
This error means that a block of memory was allocated using the C-style function **av_malloc()**, but later code tried to free that memory using the C++ operator **delete**. In C++, memory allocation and deallocation methods must always be paired correctly to prevent undefined behavior.

### How often does it reproduce? Is there a required condition?
Always. No.

### What is the expected behaviour?

<!--
If possible, please provide textual (e.g. logging) output. Screenshots may be more
appropriate for graphical bugs in mythfrontend.
-->
Memory allocation and deallocation methods should be paired.

### What do you see instead?

<!--
If possible, please provide textual (e.g. logging) output. Screenshots may be more
appropriate for graphical bugs in mythfrontend.
-->
Memory allocation and deallocation methods are inconsistent.

### Additional information

<!--
Please tell us anything else you think we should know to help reproduce the bug.
-->

