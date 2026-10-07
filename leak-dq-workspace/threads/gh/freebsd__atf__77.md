# After upgrade to 0.22: Testing AddressSanitizer instrumented code is bothersome atf-c itself is leaking memory.

- URL: https://github.com/freebsd/atf/issues/77
- Repo: freebsd/atf (language: C)
- State: open; created 2024-12-04T12:16:37Z; status ok; passes main

## Issue body

reporter (NONE) · kevemueller · 2024-12-04T12:16:37Z · https://github.com/freebsd/atf/issues/77

After upgrade to 0.22 testing AddressSanitizer instrumented code on a platform with strong AddressSanitizer support (Linux, MacOS) shows leaks within atf.
These tests were previously running through without atf producing any leaks.

Here is a run logged on MacOS against atf from brew.
==> atf: stable 0.22 (bottled)

Atf should not leak memory, to help testers focus on their code.

```
20241204-091449 I 35378 cli/main.cpp:343: kyua 0.13
20241204-091449 I 35378 cli/main.cpp:348: Command line: kyua --config=none --variable parallelism=16 test --kyuafile=Kyuafile --build-root=build/pkg.S2fSHiksxA
20241204-091449 I 35378 store/write_backend.cpp:111: Populating new database with schema from /usr/local/Cellar/kyua/0.13_2/share/kyua/store/schema_v3.sql
20241204-091449 I 35378 store/write_backend.cpp:116: New metadata entry 1733303689
20241204-091449 I 35378 utils/process/executor.cpp:782: Spawned subprocess with exec_handle 35379
20241204-091453 I 35378 utils/process/executor.cpp:634: Waited for subprocess with exec_handle 35379
20241204-091453 W 35378 engine/atf.cpp:133: Test case list wrote to stderr: 
=================================================================
==35379==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 48 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108865b08 in atf_tp_get_tcs+0x25 (libatf-c.1.dylib:x86_64+0x3b08)
    #2 0x000108869c1c in atf_tp_main+0x665 (libatf-c.1.dylib:x86_64+0x7c1c)
    #3 0x000107ce9c88 in main checksum.c:185
    #4 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x0001088683c2 in atf_map_init_charpp+0x43 (libatf-c.1.dylib:x86_64+0x63c2)
    #2 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #3 0x000107ce9efd in atfu_tp_add_tcs checksum.c:190
    #4 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #5 0x000107ce9c88 in main checksum.c:185
    #6 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x0001088683c2 in atf_map_init_charpp+0x43 (libatf-c.1.dylib:x86_64+0x63c2)
    #2 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #3 0x000107ce9d8f in atfu_tp_add_tcs checksum.c:188
    #4 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #5 0x000107ce9c88 in main checksum.c:185
    #6 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x0001088683c2 in atf_map_init_charpp+0x43 (libatf-c.1.dylib:x86_64+0x63c2)
    #2 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #3 0x000107ce9e46 in atfu_tp_add_tcs checksum.c:189
    #4 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #5 0x000107ce9c88 in main checksum.c:185
    #6 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x0001088683c2 in atf_map_init_charpp+0x43 (libatf-c.1.dylib:x86_64+0x63c2)
    #2 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #3 0x000107ce9cd8 in atfu_tp_add_tcs checksum.c:187
    #4 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #5 0x000107ce9c88 in main checksum.c:185
    #6 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x0001088683c2 in atf_map_init_charpp+0x43 (libatf-c.1.dylib:x86_64+0x63c2)
    #2 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #3 0x000107ce9fb4 in atfu_tp_add_tcs checksum.c:191
    #4 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #5 0x000107ce9c88 in main checksum.c:185
    #6 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867ffa in atf_list_init+0x25 (libatf-c.1.dylib:x86_64+0x5ffa)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9cd8 in atfu_tp_add_tcs checksum.c:187
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867fe8 in atf_list_init+0x13 (libatf-c.1.dylib:x86_64+0x5fe8)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9cd8 in atfu_tp_add_tcs checksum.c:187
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867ffa in atf_list_init+0x25 (libatf-c.1.dylib:x86_64+0x5ffa)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9fb4 in atfu_tp_add_tcs checksum.c:191
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867ffa in atf_list_init+0x25 (libatf-c.1.dylib:x86_64+0x5ffa)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9d8f in atfu_tp_add_tcs checksum.c:188
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x0001088681e8 in atf_list_append+0x28 (libatf-c.1.dylib:x86_64+0x61e8)
    #2 0x0001088684ba in atf_map_insert+0x8e (libatf-c.1.dylib:x86_64+0x64ba)
    #3 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #4 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #5 0x000107ce9efd in atfu_tp_add_tcs checksum.c:190
    #6 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #7 0x000107ce9c88 in main checksum.c:185
    #8 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x0001088681e8 in atf_list_append+0x28 (libatf-c.1.dylib:x86_64+0x61e8)
    #2 0x0001088684ba in atf_map_insert+0x8e (libatf-c.1.dylib:x86_64+0x64ba)
    #3 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #4 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #5 0x000107ce9d8f in atfu_tp_add_tcs checksum.c:188
    #6 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #7 0x000107ce9c88 in main checksum.c:185
    #8 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867fe8 in atf_list_init+0x13 (libatf-c.1.dylib:x86_64+0x5fe8)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9e46 in atfu_tp_add_tcs checksum.c:189
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867ffa in atf_list_init+0x25 (libatf-c.1.dylib:x86_64+0x5ffa)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9e46 in atfu_tp_add_tcs checksum.c:189
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867fe8 in atf_list_init+0x13 (libatf-c.1.dylib:x86_64+0x5fe8)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9d8f in atfu_tp_add_tcs checksum.c:188
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867ffa in atf_list_init+0x25 (libatf-c.1.dylib:x86_64+0x5ffa)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9efd in atfu_tp_add_tcs checksum.c:190
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867fe8 in atf_list_init+0x13 (libatf-c.1.dylib:x86_64+0x5fe8)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9efd in atfu_tp_add_tcs checksum.c:190
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x0001088681e8 in atf_list_append+0x28 (libatf-c.1.dylib:x86_64+0x61e8)
    #2 0x0001088684ba in atf_map_insert+0x8e (libatf-c.1.dylib:x86_64+0x64ba)
    #3 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #4 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #5 0x000107ce9cd8 in atfu_tp_add_tcs checksum.c:187
    #6 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #7 0x000107ce9c88 in main checksum.c:185
    #8 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x0001088681e8 in atf_list_append+0x28 (libatf-c.1.dylib:x86_64+0x61e8)
    #2 0x0001088684ba in atf_map_insert+0x8e (libatf-c.1.dylib:x86_64+0x64ba)
    #3 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #4 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #5 0x000107ce9e46 in atfu_tp_add_tcs checksum.c:189
    #6 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #7 0x000107ce9c88 in main checksum.c:185
    #8 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x0001088681e8 in atf_list_append+0x28 (libatf-c.1.dylib:x86_64+0x61e8)
    #2 0x0001088684ba in atf_map_insert+0x8e (libatf-c.1.dylib:x86_64+0x64ba)
    #3 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #4 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #5 0x000107ce9fb4 in atfu_tp_add_tcs checksum.c:191
    #6 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #7 0x000107ce9c88 in main checksum.c:185
    #8 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x000108867fe8 in atf_list_init+0x13 (libatf-c.1.dylib:x86_64+0x5fe8)
    #2 0x000108868394 in atf_map_init_charpp+0x15 (libatf-c.1.dylib:x86_64+0x6394)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9fb4 in atfu_tp_add_tcs checksum.c:191
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x00010886847f in atf_map_insert+0x53 (libatf-c.1.dylib:x86_64+0x647f)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9fb4 in atfu_tp_add_tcs checksum.c:191
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x00010886847f in atf_map_insert+0x53 (libatf-c.1.dylib:x86_64+0x647f)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9d8f in atfu_tp_add_tcs checksum.c:188
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x00010886847f in atf_map_insert+0x53 (libatf-c.1.dylib:x86_64+0x647f)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9efd in atfu_tp_add_tcs checksum.c:190
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x00010886847f in atf_map_insert+0x53 (libatf-c.1.dylib:x86_64+0x647f)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9e46 in atfu_tp_add_tcs checksum.c:189
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0001094eef12 in malloc+0x82 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xdff12)
    #1 0x00010886847f in atf_map_insert+0x53 (libatf-c.1.dylib:x86_64+0x647f)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9cd8 in atfu_tp_add_tcs checksum.c:187
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 7 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x000108868493 in atf_map_insert+0x67 (libatf-c.1.dylib:x86_64+0x6493)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9e46 in atfu_tp_add_tcs checksum.c:189
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 7 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x000108868493 in atf_map_insert+0x67 (libatf-c.1.dylib:x86_64+0x6493)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9fb4 in atfu_tp_add_tcs checksum.c:191
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 7 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x000108868493 in atf_map_insert+0x67 (libatf-c.1.dylib:x86_64+0x6493)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9efd in atfu_tp_add_tcs checksum.c:190
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 7 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x000108868493 in atf_map_insert+0x67 (libatf-c.1.dylib:x86_64+0x6493)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9d8f in atfu_tp_add_tcs checksum.c:188
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

Indirect leak of 7 byte(s) in 1 object(s) allocated from:
    #0 0x0001094e14b9 in strdup+0x109 (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xd24b9)
    #1 0x000108868493 in atf_map_insert+0x67 (libatf-c.1.dylib:x86_64+0x6493)
    #2 0x0001088683d5 in atf_map_init_charpp+0x56 (libatf-c.1.dylib:x86_64+0x63d5)
    #3 0x000108863e5c in atf_tc_init+0x60 (libatf-c.1.dylib:x86_64+0x1e5c)
    #4 0x000107ce9cd8 in atfu_tp_add_tcs checksum.c:187
    #5 0x000108869be4 in atf_tp_main+0x62d (libatf-c.1.dylib:x86_64+0x7be4)
    #6 0x000107ce9c88 in main checksum.c:185
    #7 0x7ff8018b92cc in start+0x70c (dyld:x86_64+0xfffffffffff4f2cc)

SUMMARY: AddressSanitizer: 873 byte(s) leaked in 31 allocation(s).
```

## Comment 2517973624

other (CONTRIBUTOR) · kevans91 · 2024-12-04T16:36:33Z · https://github.com/freebsd/atf/issues/77#issuecomment-2517973624

Just a side note that I've been working on lsan support for FreeBSD, so in the not-so-distant future we can hopefully avoid cases like this.

## Comment 2525258130

other (CONTRIBUTOR) · ngie-eign · 2024-12-07T17:44:46Z · https://github.com/freebsd/atf/issues/77#issuecomment-2525258130

1. I'm curious how you got \*SAN to work on MacOS since the homebrew package I have doesn't seem to support ASAN out of the box -_-...
2. Building the code with LSAN exposes a lot of leaked memory... much of seems benign (application exit cleans up malloced memory), but I totally understand the lowered value of ASAN in downstream consumers when using ATF.

I will be creating GH issues for the items LSAN reports.

PS `scan-build`/`scan-view` reveals some other issues as well, but the issues reported seem to have lower signal than LSAN. LSAN reports a lot more actionable data on memory leaks and the default `scan-build` set is reporting a bunch of false positives based on the platforms ATF supports (example: non-POSIX standard `getcwd(..)` use).

## Comment 2525261279

reporter (NONE) · kevemueller · 2024-12-07T17:55:47Z · https://github.com/freebsd/atf/issues/77#issuecomment-2525261279

Hi Enji, 
any magic needed to get LSAN working on MacOS is in the ```build.xml``` that I posted in #78. The traces that started this issues are from ```freebsd/pkg```. The ```build.xml``` in that project is also from me, you got here the fancified version, which is still pending approval from @bapt there (https://github.com/freebsd/pkg/pull/2382).

Is discussed in #78, when building the same way here in atf, the MacOS traces are not useful, but the Ubuntu traces are.
At pkg, both are working fine.
There is a subtle difference in Sanitizer defaults on Linux vs. MacOS. On MacOS you must run with ```ASAN_OPTIONS=detect_leaks=1```, wherea on Linux that is the default.












## Comment 2563731845

reporter (NONE) · kevemueller · 2024-12-27T14:03:09Z · https://github.com/freebsd/atf/issues/77#issuecomment-2563731845

I have added --HEAD support to the ```brew``` package of ```atf``` and am running now against git on MacOS with ```pkg```.
HEAD introduced another leak inside ATF in ```atf_tc_run```.
As nobody volunteered to review the automake changes, I am happy to clean up that patch and resubmit it for approval. You should have leak detection in your CI build so at least there are not new leaks added.

## Comment 2563898495

other (CONTRIBUTOR) · ngie-eign · 2024-12-27T17:34:15Z · https://github.com/freebsd/atf/issues/77#issuecomment-2563898495

> I have added --HEAD support to the `brew` package of `atf` and am running now against git on MacOS with `pkg`.

Could you please share that formula?

> HEAD introduced another leak inside ATF in `atf_tc_run`. As nobody volunteered to review the automake changes, I am happy to clean up that patch and resubmit it for approval.

😔

Smaller diffs result in quicker review turnaround times. I realize that not much could be done here since this is a major proposed infrastructure change, but as Scotty once said... ["I'm givin' her all she's got, Captain!"](https://www.youtube.com/watch?v=QEs_hO8BP9E).

> You should have leak detection in your CI build so at least there are not new leaks added.

I'm working as hard as I can this week to get as much done before I get sucked into the abyss of "product development" (translation: meetings, work interrupts, and bureaucracy) next week.

Gotta love that my employer only gives me 5 days off for the Xmas holiday/New Year's Day...

## Comment 2563907611

other (CONTRIBUTOR) · ngie-eign · 2024-12-27T17:48:04Z · https://github.com/freebsd/atf/issues/77#issuecomment-2563907611

If you're running into indirect memory leaks with atf-c running `atf_tc_run(..)`, that's known (atf-c++ leaks memory with its macros). I've tried tackling that twice, but ran into problems (it's an onion peeling situation).
Also, the LSAN runs will fail until the memory leak issues are resolved. Something I learned as an SRE at Meta: broken alarms result in apathy. We need to fix the memory leak issues either at the same time, or ignore the failures until everything is fixed.
I think it makes sense to introduce LSAN CI support on the fix-memory-leaks branch. If you want to work with me on that, that would be great.

## Comment 2563955474

reporter (NONE) · kevemueller · 2024-12-27T18:59:45Z · https://github.com/freebsd/atf/issues/77#issuecomment-2563955474

The changes are upstreamed to brew.
```sh
brew update; brew unlink atf; brew install --HEAD atf
``` 
will give you ```atf``` from git HEAD. The ```release``` atf will remain on disk, but is not linked to be the default. If you want to be sure do ```uninstall``` instead of ```unlink```.

I am nowhere to blame anybody here. I just saw those promising changes in your preview and was surprised none of them made it into HEAD.

I was briefly looking at the atf codebase and was honestly afraid to even touch it with a stick. It looks extremely fragile to me. I am not sure I will be able to help, but I will take a look at your ```fix-memory-leaks``` branch and try to contribute there.
You have not introduced there the CI run with my LSAN fixes. How are you detecting the leaks, how are you ensuring that you don't introduce any regression?

Exactly that was annoying at ```pkg``` end, the std::vector issue caused false-positives, which are the worst you can have in a CI run. I have introduced there ```https://github.com/freebsd/pkg/blob/main/Leak.suppress.in``` so we have a list of known leaks and can ensure that new leaks are flagged loudly by CI. Over time, when people out of fun and curiosity remove the leaks, the list of exemptions will reduce to zero.

You can adopt the same strategy with ```atf``` to make your CI green (and hopefully still have time to fix those leaks) for your downstream users.

## Comment 2563975854

other (CONTRIBUTOR) · ngie-eign · 2024-12-27T19:33:12Z · https://github.com/freebsd/atf/issues/77#issuecomment-2563975854

> The changes are upstreamed to brew.
> 
> ```shell
> brew update; brew unlink atf; brew install --HEAD atf
> ```
> 
> will give you `atf` from git HEAD. The `release` atf will remain on disk, but is not linked to be the default. If you want to be sure do `uninstall` instead of `unlink`.

Yeah. That's a whole lot cleaner than what I have currently.

It would be _extremely_ helpful if similar patterns could be used with lutok and kyua. The lutok CI work I started yesterday involves .

> I am nowhere to blame anybody here. I just saw those promising changes in your preview and was surprised none of them made it into HEAD.

It's ok. I'm doing what I can to chew through things getting review along the way.

> I was briefly looking at the atf codebase and was honestly afraid to even touch it with a stick. It looks extremely fragile to me. I am not sure I will be able to help, but I will take a look at your `fix-memory-leaks` branch and try to contribute there. You have not introduced there the CI run with my LSAN fixes. How are you detecting the leaks, how are you ensuring that you don't introduce any regression?

The memory management piece is really annoying. Most of the memory leaks seem to be happening on the C side, and the C++ side where non-smart pointers are being used.

I've been manually checking on MacOS and Ubuntu 24.04--it's incredibly tedious :(... Once the CI stuff is in (and cmake after that) it will be more automated. I just want to call `ctest` and have the build artifacts be checked, instead of the current system of having to bootstrap all 3 items (atf, kyua, lutok) in order to just run tests *sigh*.

> Exactly that was annoying at `pkg` end, the std::vector issue caused false-positives, which are the worst you can have in a CI run. I have introduced there `https://github.com/freebsd/pkg/blob/main/Leak.suppress.in` so we have a list of known leaks and can ensure that new leaks are flagged loudly by CI. Over time, when people out of fun and curiosity remove the leaks, the list of exemptions will reduce to zero.
>
> You can adopt the same strategy with `atf` to make your CI green (and hopefully still have time to fix those leaks) for your downstream users.

Ok, that's really nice! I'll try to take a look at that.

## Comment 5485676414

other (CONTRIBUTOR) · ngie-eign · 2026-08-31T22:33:26Z · https://github.com/freebsd/atf/issues/77#issuecomment-5485676414

@kevemueller : could you please confirm whether or not the issues still exist with atf-0.24?

## Comment 5790426675

other (CONTRIBUTOR) · ngie-eign · 2026-09-23T06:53:22Z · https://github.com/freebsd/atf/issues/77#issuecomment-5790426675

This still hasn't been fully fixed yet, as can be seen on this branch: https://github.com/ngie-eign/atf/tree/issue-167 . The number of issues cited by ASAN+LSAN has been reduced considerably though in 0.24-0.26, as anticipated in preparation for the release.

## Comment 5845857848

other (CONTRIBUTOR) · ngie-eign · 2026-09-26T11:23:30Z · https://github.com/freebsd/atf/issues/77#issuecomment-5845857848

There's at least 1 prominent leak in `atf-c/tc.c` that needs to be resolved still which will impact libpkg's tests. Will work on it once I get back next week.
