# Memory leak in sndfile-convert

- URL: https://github.com/libsndfile/libsndfile/issues/922
- Repo: libsndfile/libsndfile (language: C)
- State: open; created 2023-03-10T08:47:11Z; status ok; passes main

## Issue body

reporter (NONE) · 5hadowblad3 · 2023-03-10T08:47:11Z · https://github.com/libsndfile/libsndfile/issues/922

Hi, there.

There is a memory leak in sndfile-convert from the newest commit (a005d98fc499945e). It seems this issue is related to an elder CVE mentioned in issue #398.

To reproduce, run:
~~~~
./sndfile-convert poc tmp.mp3
~~~~

[poc.zip](https://github.com/libsndfile/libsndfile/files/10940191/memory_leak_sndfile-convert.ogg.zip)
(unzip first)


Here is the trace reported by ASAN:
~~~~
==1567492==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 8144 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x5aecd9 in psf_allocate  /benchmark/libsndfile/src/common.c:45:13

Direct leak of 336 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd606d86e in lame_init (/lib/x86_64-linux-gnu/libmp3lame.so.0+0x1486e)

Indirect leak of 134840 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd606da7e in lame_init (/lib/x86_64-linux-gnu/libmp3lame.so.0+0x14a7e)

Indirect leak of 88584 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd606d9c0 in lame_init (/lib/x86_64-linux-gnu/libmp3lame.so.0+0x149c0)

Indirect leak of 20480 byte(s) in 2 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61e1225 in mdct_init (/lib/x86_64-linux-gnu/libvorbis.so.0+0x4225)

Indirect leak of 16384 byte(s) in 2 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e5960  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8960)

Indirect leak of 16384 byte(s) in 1 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61950c5 in ogg_stream_init (/lib/x86_64-linux-gnu/libogg.so.0+0x30c5)

Indirect leak of 15784 byte(s) in 13 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f5a92 in _book_unquantize (/lib/x86_64-linux-gnu/libvorbis.so.0+0x18a92)

Indirect leak of 12776 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x6463d9 in ogg_open  /benchmark/libsndfile/src/ogg.c:713:24
    #2 0x4ffdb5 in main  /benchmark/libsndfile/programs/sndfile-convert.c:290:16
    #3 0x7f5bd5e3b082 in __libc_start_main /build/glibc-SzIz7B/glibc-2.31/csu/../csu/libc-start.c:308:16

Indirect leak of 10500 byte(s) in 29 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61f609a in vorbis_book_init_decode (/lib/x86_64-linux-gnu/libvorbis.so.0+0x1909a)
    #2 0x7f5bd61e5b43  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8b43)

Indirect leak of 10500 byte(s) in 29 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61f601a in vorbis_book_init_decode (/lib/x86_64-linux-gnu/libvorbis.so.0+0x1901a)
    #2 0x7f5bd61e5b43  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8b43)

Indirect leak of 8943 byte(s) in 1 object(s) allocated from:
    #0 0x4ca2e8 in realloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:164:3
    #1 0x7f5bd6196c85 in ogg_sync_buffer (/lib/x86_64-linux-gnu/libogg.so.0+0x4c85)

Indirect leak of 8192 byte(s) in 1 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61950e7 in ogg_stream_init (/lib/x86_64-linux-gnu/libogg.so.0+0x30e7)

Indirect leak of 5784 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61ed27d in vorbis_info_init (/lib/x86_64-linux-gnu/libvorbis.so.0+0x1027d)

Indirect leak of 4096 byte(s) in 1 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61950d6 in ogg_stream_init (/lib/x86_64-linux-gnu/libogg.so.0+0x30d6)

Indirect leak of 4096 byte(s) in 2 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61e120e in mdct_init (/lib/x86_64-linux-gnu/libvorbis.so.0+0x420e)

Indirect leak of 3712 byte(s) in 29 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f618f in vorbis_book_init_decode (/lib/x86_64-linux-gnu/libvorbis.so.0+0x1918f)
    #2 0x7f5bd61e5b43  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8b43)

Indirect leak of 3208 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f3f16  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x16f16)

Indirect leak of 2848 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f2346 in res0_unpack (/lib/x86_64-linux-gnu/libvorbis.so.0+0x15346)

Indirect leak of 2784 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e5b18  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8b18)

Indirect leak of 2772 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd606da63 in lame_init (/lib/x86_64-linux-gnu/libmp3lame.so.0+0x14a63)

Indirect leak of 2625 byte(s) in 29 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61f60e7 in vorbis_book_init_decode (/lib/x86_64-linux-gnu/libvorbis.so.0+0x190e7)
    #2 0x7f5bd61e5b43  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8b43)

Indirect leak of 1328 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61eeca9  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x11ca9)

Indirect leak of 1120 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61ef445  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x12445)

Indirect leak of 800 byte(s) in 1 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61f12e4 in res0_look (/lib/x86_64-linux-gnu/libvorbis.so.0+0x142e4)

Indirect leak of 800 byte(s) in 100 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61f134a in res0_look (/lib/x86_64-linux-gnu/libvorbis.so.0+0x1434a)

Indirect leak of 464 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x64804e in ogg_vorbis_open  /benchmark/libsndfile/src/ogg_vorbis.c:466:10

Indirect leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x5aecf0 in psf_allocate  /benchmark/libsndfile/src/common.c:48:25

Indirect leak of 232 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e5822  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8822)

Indirect leak of 200 byte(s) in 9 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f122b in res0_look (/lib/x86_64-linux-gnu/libvorbis.so.0+0x1422b)

Indirect leak of 80 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f11b5 in res0_look (/lib/x86_64-linux-gnu/libvorbis.so.0+0x141b5)

Indirect leak of 80 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61f1166 in res0_look (/lib/x86_64-linux-gnu/libvorbis.so.0+0x14166)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e589a  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x889a)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e5880  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8880)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61e5933  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8933)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x4c9f6f in malloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x7f5bd61e5923  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8923)

Indirect leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61ed9ac in vorbis_synthesis_headerin (/lib/x86_64-linux-gnu/libvorbis.so.0+0x109ac)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e5868  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8868)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e59c3  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x89c3)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e59ab  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x89ab)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61e5850  (/lib/x86_64-linux-gnu/libvorbis.so.0+0x8850)

Indirect leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61edae8 in vorbis_synthesis_headerin (/lib/x86_64-linux-gnu/libvorbis.so.0+0x10ae8)

Indirect leak of 4 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61edaf8 in vorbis_synthesis_headerin (/lib/x86_64-linux-gnu/libvorbis.so.0+0x10af8)

Indirect leak of 1 byte(s) in 1 object(s) allocated from:
    #0 0x4ca127 in calloc  /dependence/llvm11/llvm-11.0.0.src/projects/compiler-rt/lib/asan/asan_malloc_linux.cpp:154:3
    #1 0x7f5bd61eda56 in vorbis_synthesis_headerin (/lib/x86_64-linux-gnu/libvorbis.so.0+0x10a56)

SUMMARY: AddressSanitizer: 389289 byte(s) leaked in 278 allocation(s).
Aborted

~~~~


