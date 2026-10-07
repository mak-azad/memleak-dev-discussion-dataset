# LeakSanitizer: detected memory leaks

- URL: https://github.com/neurobin/shc/issues/155
- Repo: neurobin/shc (language: C)
- State: open; created 2023-08-17T07:46:26Z; status ok; passes main

## Issue body

reporter (NONE) · yangfar · 2023-08-17T07:46:26Z · https://github.com/neurobin/shc/issues/155

When I compiled shc in afl-gcc and fsanitize mode and converted sh to an executable file, I found a memory leak.
https://github.com/kn007/silk-v3-decoder/commit/07bfa0f56bbfcdacd56e2e73b7bcd10a0efb7f4c

Details:
fl-clang-fast 2.57b by <lszekeres@google.com>
afl-llvm-pass 2.57b by <lszekeres@google.com>
[+] Instrumented 82 locations (ASAN/MSAN mode, ratio 100%).

=================================================================
==61537==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 65 byte(s) in 1 object(s) allocated from:
    #0 0x493e59 in realloc (/home/yzy/fuzzsoftware/shc/local/bin/shc+0x493e59)
    #1 0x4c6385 in write_C /home/yzy/fuzzsoftware/shc/src/shc.c:1221:16
    #2 0x4ca7d0 in do_all /home/yzy/fuzzsoftware/shc/src/shc.c:1348:6
    #3 0x4cb11f in main /home/yzy/fuzzsoftware/shc/src/shc.c:1358:2

Direct leak of 44 byte(s) in 1 object(s) allocated from:
    #0 0x493e59 in realloc (/home/yzy/fuzzsoftware/shc/local/bin/shc+0x493e59)
    #1 0x4c82fa in write_C /home/yzy/fuzzsoftware/shc/src/shc.c:1246:16
    #2 0x4ca7d0 in do_all /home/yzy/fuzzsoftware/shc/src/shc.c:1348:6
    #3 0x4cb11f in main /home/yzy/fuzzsoftware/shc/src/shc.c:1358:2
Cmd: 
./shc -f /home/root/shc/converter.sh -o converter
Ubuntu:
x86_64 x86_64 x86_64 GNU/Linux

Thanks!

## Comment 1879272310

other (NONE) · mdeweerd · 2024-01-05T21:22:40Z · https://github.com/neurobin/shc/issues/155#issuecomment-1879272310

Also found by cppcheck:
```
src/shc.c(1033): error (memleak): Memory leak: ptr
src/shc.c(1088): error (memleak): Memory leak: text
src/shc.c(1037): error (memleakOnRealloc): Common realloc mistake: 'shll' nulled but not freed upon failure
src/shc.c(1065): error (memleakOnRealloc): Common realloc mistake: 'opts' nulled but not freed upon failure
src/shc.c(1090): error (memleakOnRealloc): Common realloc mistake: 'text' nulled but not freed upon failure
src/shc.c(1099): error (memleakOnRealloc): Common realloc mistake: 'text' nulled but not freed upon failure
```
