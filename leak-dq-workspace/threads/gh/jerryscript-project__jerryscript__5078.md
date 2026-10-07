# AddressSanitizer: attempting free on address which was not malloc()-ed

- URL: https://github.com/jerryscript-project/jerryscript/issues/5078
- Repo: jerryscript-project/jerryscript (language: C)
- State: open; created 2023-04-29T05:48:44Z; status ok; passes main

## Issue body

reporter (NONE) · Ye0nny · 2023-04-29T05:48:44Z · https://github.com/jerryscript-project/jerryscript/issues/5078

###### JerryScript revision
Commit: https://github.com/jerryscript-project/jerryscript/commit/05dbbd134c3b9e2482998f267857dd3722001cd7
Version: v3.0.0

###### Build platform
Ubuntu 20.04.5 LTS (Linux 5.4.0-144-generic x86_64)

###### Build steps
```sh
python ./tools/build.py --clean --compile-flag=-m32 --compile-flag=-fno-omit-frame-pointer --compile-flag=-fno-common --compile-flag=-fsanitize=address --compile-flag=-g --strip=off --lto=off --error-messages=on --system-allocator=on --logging=on --line-info=on --stack-limit=20
```

###### Test case
```javascript
// poc.js
class s { static { ( ) => { class s { static { } ; } } ; } }
```

###### Execution steps & Output
```
$ ./jerryscript/build/bin/jerry poc.js
=================================================================
==2012485==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0xff975ce0 in thread T0
    #0 0xf79dd414 in __interceptor_free ../../../../../src/libsanitizer/asan/asan_malloc_linux.cc:122
    #1 0x56648b87 in jmem_heap_free_block_internal ./jerryscript/jerry-core/jmem/jmem-heap.c:477
    #2 0x566bca69 in scanner_release_next ./jerryscript/jerry-core/parser/js/js-scanner-util.c:262
    #3 0x5672aac8 in parser_parse_class_body ./jerryscript/jerry-core/parser/js/js-parser-expr.c:825
    #4 0x5672aac8 in parser_parse_class ./jerryscript/jerry-core/parser/js/js-parser-expr.c:1110
    #5 0x56734f84 in parser_parse_statements ./jerryscript/jerry-core/parser/js/js-parser-statm.c:2787
    #6 0x566bab25 in parser_parse_source ./jerryscript/jerry-core/parser/js/js-parser.c:2280
    #7 0x5664d3cf in jerry_parse_common ./jerryscript/jerry-core/api/jerryscript.c:412
    #8 0x5664d631 in jerry_parse ./jerryscript/jerry-core/api/jerryscript.c:480
    #9 0x56742644 in jerryx_source_parse_script ./jerryscript/jerry-ext/util/sources.c:52
    #10 0x56742701 in jerryx_source_exec_script ./jerryscript/jerry-ext/util/sources.c:63
    #11 0x56645d04 in main ./jerryscript/jerry-main/main-desktop.c:156
    #12 0xf75f4ed4 in __libc_start_main (/lib32/libc.so.6+0x1aed4)
    #13 0x56648fb4 in _start (./jerryscript/build/bin/jerry+0x12fb4)

Address 0xff975ce0 is located in stack of thread T0 at offset 1584 in frame
    #0 0x5673438c in parser_parse_statements ./jerryscript/jerry-core/parser/js/js-parser-statm.c:2601

  This frame has 44 object(s):
    [32, 36) 'do_while_statement' (line 2827)
    [48, 52) 'loop' (line 2828)
    [64, 68) 'loop' (line 3106)
    [80, 84) 'loop' (line 3232)
    [96, 100) 'loop' (line 954)
    [112, 116) 'loop' (line 1110)
    [128, 132) 'loop' (line 2128)
    [144, 148) 'loop' (line 2180)
    [160, 164) 'loop' (line 2226)
    [176, 180) 'loop' (line 895)
    [192, 196) 'do_while_statement' (line 930)
    [208, 216) 'else_statement' (line 3195)
    [240, 248) 'if_statement' (line 776)
    [272, 280) 'branch' (line 1316)
    [304, 312) 'with_statement' (line 834)
    [336, 344) 'iterator' (line 1990)
    [368, 376) 'iterator' (line 2017)
    [400, 408) 'iterator' (line 2065)
    [432, 440) 'iterator' (line 2147)
    [464, 472) 'loop_iterator' (line 2156)
    [496, 504) 'iterator' (line 2549)
    [528, 536) 'iterator' (line 1809)
    [560, 568) 'if_statement' (line 796)
    [592, 600) 'else_statement' (line 797)
    [624, 632) 'iterator' (line 798)
    [656, 664) 'iterator' (line 904)
    [688, 696) 'with_statement' (line 864)
    [720, 732) 'lit_location' (line 2618)
    [752, 764) 'switch_statement' (line 3107)
    [784, 796) 'for_in_of_statement' (line 3231)
    [816, 828) 'location' (line 2385)
    [848, 860) 'for_in_of_statement' (line 1139)
    [880, 892) 'start_location' (line 1140)
    [912, 924) 'end_location' (line 1140)
    [944, 956) 'switch_statement' (line 1991)
    [976, 988) 'switch_statement' (line 2018)
    [1008, 1024) 'try_statement' (line 2863)
    [1040, 1056) 'label' (line 3174)
    [1072, 1088) 'label_statement' (line 2090)
    [1104, 1120) 'label_statement' (line 2173)
    [1136, 1152) 'label_statement' (line 2550)
    [1168, 1184) 'try_statement' (line 1808)
    [1200, 1224) 'while_statement' (line 953)
    [1264, 1300) 'for_statement' (line 1506) <== Memory access at offset 1584 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: bad-free ../../../../../src/libsanitizer/asan/asan_malloc_linux.cc:122 in __interceptor_free
==2012485==ABORTING
```

---
with debugging mode(--debug)
###### Outputs
```
ICE: Assertion 'context_p->next_scanner_info_p->type == SCANNER_TYPE_CLASS_STATIC_BLOCK_END' failed at ./jerryscript/jerry-core/parser/js/js-parser-expr.c(parser_parse_class_body):822.
Error: JERRY_FATAL_FAILED_ASSERTION
Aborted
```



Credits: @Ye0nny, @EJueon of the seclab-yonsei.


