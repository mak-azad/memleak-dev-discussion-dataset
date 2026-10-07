# Memory leak

- URL: https://github.com/uTox/uTox/issues/1554
- Repo: uTox/uTox (language: C)
- State: open; created 2022-11-30T04:40:03Z; status ok; passes main

## Issue body

reporter (NONE) · ghost · 2022-11-30T04:40:03Z · https://github.com/uTox/uTox/issues/1554

```
  --silent                 Set the verbosity level to 0, disable all debugging output.
  --debug=<file>           Set a file for utox to log errors to.

=================================================================
==30226==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 11168 byte(s) in 349 object(s) allocated from:
    #0 0x7f97d4e73411 in __interceptor_calloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7f97d46eaf3f  (/usr/lib/libfontconfig.so.1+0xaf3f)

Direct leak of 4096 byte(s) in 1 object(s) allocated from:
    #0 0x7f97d4e727ea in __interceptor_realloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7f97d46e8df3  (/usr/lib/libfontconfig.so.1+0x8df3)

Direct leak of 1024 byte(s) in 1 object(s) allocated from:
    #0 0x7f97d4e727ea in __interceptor_realloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7f97d46e8dd5  (/usr/lib/libfontconfig.so.1+0x8dd5)

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x7f97d4e73a89 in __interceptor_malloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7f97d4700f25  (/usr/lib/libfontconfig.so.1+0x20f25)

Indirect leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f97d4e73411 in __interceptor_calloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7f97d470511d  (/usr/lib/libfontconfig.so.1+0x2511d)

Indirect leak of 14 byte(s) in 1 object(s) allocated from:
    #0 0x7f97d4e26faa in __interceptor_strdup /usr/src/debug/gcc/libsanitizer/asan/asan_interceptors.cpp:439
    #1 0x7f97d47007d8 in FcValueSave (/usr/lib/libfontconfig.so.1+0x207d8)

SUMMARY: AddressSanitizer: 16590 byte(s) leaked in 354 allocation(s).

```

utox 0.18.1-2


