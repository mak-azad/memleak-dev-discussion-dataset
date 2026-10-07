# Crash: static-stdlib and static variable initialisation 

- URL: https://github.com/swiftlang/swift/issues/61669
- Repo: swiftlang/swift (language: Swift)
- State: open; created 2022-10-21T16:56:59Z; status ok; passes main

## Issue body

reporter (NONE) · patrick-zippenfenig · 2022-10-21T16:56:59Z · https://github.com/swiftlang/swift/issues/61669

**Describe the bug**
Using `static-stdlib` and static variable initialisation that calls `swift_once` causes bad-frees. A simple reproducible test just reads `CommandLine.arguments` with `-sanitize=address` enabled.

**Steps To Reproduce**
Run on docker swift:5.7.0-jammy plattform linux/amd64

```
echo "print(CommandLine.arguments)" > test.swift
swiftc -static-stdlib -sanitize=address test.swift
./test
==5796==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x558d119001e0 ...
```

```
lldb test
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'lldb'
(lldb) target create "test"
Current executable set to '/app/SwiftOnceTest/test' (x86_64).
(lldb) run
Process 5792 launched: '/app/SwiftOnceTest/test' (x86_64)
=================================================================
==5792==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x55555656f240 in thread T0
    #0 0x555555629fd2  (/app/SwiftOnceTest/test+0xd5fd2)
    #1 0x5555559b3ecf  (/app/SwiftOnceTest/test+0x45fecf)
    #2 0x55555582797c  (/app/SwiftOnceTest/test+0x2d397c)
    #3 0x7ffff7af5f67  (/lib/x86_64-linux-gnu/libc.so.6+0x99f67)
    #4 0x55555596e0ab  (/app/SwiftOnceTest/test+0x41a0ab)
    #5 0x555555827a48  (/app/SwiftOnceTest/test+0x2d3a48)
    #6 0x7ffff7af5f67  (/lib/x86_64-linux-gnu/libc.so.6+0x99f67)
    #7 0x55555596e0ab  (/app/SwiftOnceTest/test+0x41a0ab)
    #8 0x555555827ac3  (/app/SwiftOnceTest/test+0x2d3ac3)

Address 0x55555656f240 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: bad-free (/app/SwiftOnceTest/test+0xd5fd2)
==5792==ABORTING
(lldb) AddressSanitizer report breakpoint hit. Use 'thread info -s' to get extended information about the report.
Process 5792 stopped
* thread #1, name = 'test', stop reason = Deallocation of non-allocated memory
    frame #0: 0x00005555556338b0 test`::AsanDie() at asan_rtl.cpp:45:7
Target 0: (test) stopped.
(lldb) bt
* thread #1, name = 'test', stop reason = Deallocation of non-allocated memory
  * frame #0: 0x00005555556338b0 test`::AsanDie() at asan_rtl.cpp:45:7
    frame #1: 0x000055555564aa2c test`__sanitizer::Die() at sanitizer_termination.cpp:55:7
    frame #2: 0x0000555555631e97 test`::~ScopedInErrorReport() at asan_report.cpp:190:7
    frame #3: 0x000055555562e51c test`::ReportFreeNotMalloced() at asan_report.cpp:239:1
    frame #4: 0x000055555562a036 test`::__interceptor_free() at asan_malloc_linux.cpp:112:3
    frame #5: 0x00005555559b3ed0 test`_swift_stdlib_getUnsafeArgvArgc + 400
    frame #6: 0x000055555582797d test`one-time initialization function for _unsafeArgv + 13
    frame #7: 0x00007ffff7af5f68 libc.so.6`___lldb_unnamed_symbol3495 + 232
    frame #8: 0x000055555596e0ac test`swift_once + 92
    frame #9: 0x0000555555827a49 test`one-time initialization function for arguments + 25
    frame #10: 0x00007ffff7af5f68 libc.so.6`___lldb_unnamed_symbol3495 + 232
    frame #11: 0x000055555596e0ac test`swift_once + 92
    frame #12: 0x0000555555827ac4 test`static Swift.CommandLine.arguments.getter : Swift.Array<Swift.String> + 20
    frame #13: 0x000055555566136f test`main + 31
    frame #14: 0x00007ffff7a85d90 libc.so.6`___lldb_unnamed_symbol3139 + 128
    frame #15: 0x00007ffff7a85e40 libc.so.6`__libc_start_main + 128
    frame #16: 0x00005555555a96c5 test`_start + 37

```

**Expected behavior**
Not crashing

**Environment (please fill out the following information)**
 - docker swift:5.7.0-jammy plattform linux/amd64
 - docker swift:5.60-jammy plattform linux/amd64


**Additional context**
The error was initially discovered with the help of @Lukasa in https://github.com/swift-server/async-http-client/issues/642 and lead to random crashes in trivial code that accesses a static variable.

