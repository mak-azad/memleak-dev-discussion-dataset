# [TEST-FAILURE] Leaked memory in debugCommand (debug.c:569)

- URL: https://github.com/BChan-0/valkey/issues/224
- Repo: BChan-0/valkey (language: C)
- State: open; created 2026-07-30T03:42:59Z; status ok; passes main

## Issue body

reporter (OWNER) · BChan-0 · 2026-07-30T03:42:59Z · https://github.com/BChan-0/valkey/issues/224

<!-- valkey-ci-agent:memory-error:6717d324bc90c6ded1c2 -->
<!-- valkey-ci-agent:memory-error:occurrences:1 -->

**Summary**

`Leaked memory in debugCommand (debug.c:569)` in `tests/unit/dummy-memory.tcl` is failing in CI.

**Failing test(s)**

- Test name: `[no test]`
- Test file: `tests/unit/dummy-memory.tcl`
- CI link(s):
    - `test-sanitizer-address-clang`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244610#step:9:1)
    - `test-sanitizer-address-gcc`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244306#step:9:1)
    - `test-sanitizer-force-defrag`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244216#step:9:1)
    - `test-valgrind-misc`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244200#step:9:1)
    - `test-valgrind-no-malloc-usable-size-misc`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244163#step:9:1)
    - `test-valgrind-no-malloc-usable-size-test`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244269#step:8:1)
    - `test-valgrind-test`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244319#step:8:1)

**Error stack trace**

```
Sanitizer error: 
=================================================================
==6086==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 41 byte(s) in 1 object(s) allocated from:
    #0 0x5621317f9e33 in malloc (/home/runner/work/valkey/valkey/src/valkey-server+0x20de33) (BuildId: 15d5375fe17d9df88056cc97072348acfa6e2312)
    #1 0x562131c01013 in ztrymalloc_usable_internal /home/runner/work/valkey/valkey/src/zmalloc.c:172:17
    #2 0x562131c01013 in zmalloc_usable /home/runner/work/valkey/valkey/src/zmalloc.c:268:17
    #3 0x562131af3da7 in _sdsnewlen /home/runner/work/valkey/valkey/src/sds.c:102:22
    #4 0x56213193428f in debugCommand /home/runner/work/valkey/valkey/src/debug.c:569:9
    #5 0x562131b414a7 in call /home/runner/work/valkey/valkey/src/server.c:3933:5
    #6 0x562131b456cc in processCommand /home/runner/work/valkey/valkey/src/server.c:4700:9
    #7 0x562131a43451 in processCommandAndResetClient /home/runner/work/valkey/valkey/src/networking.c:3942:9
    #8 0x562131a43451 in processInputBuffer /home/runner/work/valkey/valkey/src/networking.c:4246:13
    #9 0x562131a2529e in readQueryFromClient /home/runner/work/valkey/valkey/src/networking.c:4359:17
    #10 0x562131b5e23f in callHandler /home/runner/work/valkey/valkey/src/./connhelpers.h:79:18
    #11 0x562131b5e23f in connSocketEventHandler /home/runner/work/valkey/valkey/src/socket.c:301:14
    #12 0x562131855e80 in aeProcessEvents /home/runner/work/valkey/valkey/src/ae.c:486:17
    #13 0x5621318568fc in aeMain /home/runner/work/valkey/valkey/src/ae.c:543:9
    #14 0x562131b55ba8 in main /home/runner/work/valkey/valkey/src/server.c:7832:5
    #15 0x7f641f02a1c9  (/lib/x86_64-linux-gnu/libc.so.6+0x2a1c9) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #16 0x7f641f02a28a in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2a28a) (BuildId: 8e9fd827446c24067541ac5390e6f527fb5947bb)
    #17 0x56213175efe4 in _start (/home/runner/work/valkey/valkey/src/valkey-server+0x172fe4) (BuildId: 15d5375fe17d9df88056cc97072348acfa6e2312)

SUMMARY: AddressSanitizer: 41 byte(s) leaked in 1 allocation(s).

```

**Environments:** `test-sanitizer-address-clang`, `test-sanitizer-address-gcc`, `test-sanitizer-force-defrag`, `test-valgrind-misc`, `test-valgrind-no-malloc-usable-size-misc`, `test-valgrind-no-malloc-usable-size-test`, `test-valgrind-test`

---
*Auto-created by Test Failure Detector*
<!-- valkey-ci-agent:memory-error:last-key:30499308370 -->

## Comment 5126157642

reporter (OWNER) · BChan-0 · 2026-07-30T03:43:01Z · https://github.com/BChan-0/valkey/issues/224#issuecomment-5126157642

Test failed again on 2026-07-30.

**New error stack trace**

```
Valgrind error: ==8335== Memcheck, a memory error detector
==8335== Copyright (C) 2002-2022, and GNU GPL'd, by Julian Seward et al.
==8335== Using Valgrind-3.22.0 and LibVEX; rerun with -h for copyright info
==8335== Command: /home/runner/work/valkey/valkey/src/valkey-server ./tests/tmp/valkey.conf.8330.2
==8335== 
==8335== 
==8335== HEAP SUMMARY:
==8335==     in use at exit: 972,349 bytes in 13,544 blocks
==8335==   total heap usage: 18,055 allocs, 4,511 frees, 1,383,159 bytes allocated
==8335== 
==8335== 41 bytes in 1 blocks are definitely lost in loss record 900 of 1,111
==8335==    at 0x4846828: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==8335==    by 0x318E1D: ztrymalloc_usable_internal (zmalloc.c:172)
==8335==    by 0x31905C: zmalloc_usable (zmalloc.c:268)
==8335==    by 0x29065E: _sdsnewlen (sds.c:102)
==8335==    by 0x2909EB: sdsnewlen (sds.c:169)
==8335==    by 0x290AAA: sdsdup (sds.c:190)
==8335==    by 0x1E8220: debugCommand (debug.c:569)
==8335==    by 0x2ADB0C: call (server.c:3933)
==8335==    by 0x2B0420: processCommand (server.c:4700)
==8335==    by 0x24CE00: processCommandAndResetClient (networking.c:3942)
==8335==    by 0x24DC65: processInputBuffer (networking.c:4246)
==8335==    by 0x24E131: readQueryFromClient (networking.c:4359)
==8335== 
==8335== LEAK SUMMARY:
==8335==    definitely lost: 41 bytes in 1 blocks
==8335==    indirectly lost: 0 bytes in 0 blocks
==8335==      possibly lost: 40,781 bytes in 836 blocks
==8335==    still reachable: 931,527 bytes in 12,707 blocks
==8335==         suppressed: 0 bytes in 0 blocks
==8335== Reachable blocks (those to which a pointer was found) are not shown.
==8335== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==8335== 
==8335== For lists of detected and suppressed errors, rerun with: -s
==8335== ERROR SUMMARY: 36 errors from 36 contexts (suppressed: 0 from 0)


```

**Failed in:**
- `test-sanitizer-address-clang`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244610#step:9:1)
- `test-sanitizer-address-gcc`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244306#step:9:1)
- `test-sanitizer-force-defrag`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244216#step:9:1)
- `test-valgrind-misc`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244200#step:9:1)
- `test-valgrind-no-malloc-usable-size-misc`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244163#step:9:1)
- `test-valgrind-no-malloc-usable-size-test`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244269#step:8:1)
- `test-valgrind-test`: [CI link](https://github.com/BChan-0/valkey/actions/runs/30499308370/job/90735244319#step:8:1)
