# Heap-buffer-overflow when processing an png file in png_read_chunk()

- URL: https://github.com/swftools/swftools/issues/202
- Repo: swftools/swftools (language: C)
- State: open; created 2023-07-01T08:50:15Z; status ok; passes main

## Issue body

reporter (NONE) · Hee-won · 2023-07-01T08:50:15Z · https://github.com/swftools/swftools/issues/202

Hi there

We would like to share that the latest version of pdf2swf causes heap-buffer-overflow when executed with a crafted png input.

We assume that the invalid memory access happens due to the improper processing malformed input in png_read_chunk() in spite of the error handling.

Here is the output of program with address sanitizer attached.

Bug Report
=================================================================
==32129==ERROR: AddressSanitizer: allocator is out of memory trying to allocate 0x9c000000 bytes
    #0 0x7f9ccb581808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x56345b1588fa in png_read_chunk /home/ubuntu/targets/swftools/lib/png.c:63
    #2 0x56345b158cab in png_read_header /home/ubuntu/targets/swftools/lib/png.c:106
    #3 0x56345b15bc0f in png_load /home/ubuntu/targets/swftools/lib/png.c:498
    #4 0x56345b131d40 in MovieAddFrame /home/ubuntu/targets/swftools/src/png2swf.c:494
    #5 0x56345b12e2f6 in main /home/ubuntu/targets/swftools/src/png2swf.c:822
    #6 0x7f9ccad9e082 in __libc_start_main ../csu/libc-start.c:308

==32129==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: out-of-memory ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144 in __interceptor_malloc
==32129==ABORTING

### Environment
OS: Ubuntu 20.04.5 LTS
Release: latest commit of master branch on this github 
Program: png2swf

### How to reproduce
$ png2swf poc-file
poc-file is attached.
[poc-file.txt](https://github.com/matthiaskramm/swftools/files/11925311/poc-file.txt)


## Comment 1707911459

other (NONE) · choonginlee · 2023-09-06T08:36:00Z · https://github.com/swftools/swftools/issues/202#issuecomment-1707911459

The release tested is commit [772e55a](https://github.com/matthiaskramm/swftools/commit/772e55a271f66818b06c6e8c9b839befa51248f4)
