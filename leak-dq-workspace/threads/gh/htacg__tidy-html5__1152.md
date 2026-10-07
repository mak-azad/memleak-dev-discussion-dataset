# [BUG] Memory leaks in `defaultAlloc` at `src/alloc.c:64:45`

- URL: https://github.com/htacg/tidy-html5/issues/1152
- Repo: htacg/tidy-html5 (language: C)
- State: open; created 2025-05-26T08:49:45Z; status ok; passes main

## Issue body

reporter (NONE) · JJLeo · 2025-05-26T08:49:45Z · https://github.com/htacg/tidy-html5/issues/1152

## Description

- Version: Latest commit [d08ddc2](https://github.com/htacg/tidy-html5/commit/d08ddc2860aa95ba8e301343a30837f157977cba)
- Environment: Ubuntu 20.04.6 LTS, Clang 18.1.8
- Fuzzing harness: https://github.com/google/oss-fuzz/blob/master/projects/tidy-html5/tidy_general_fuzzer.c

**Please let me know if you encounter any issues reproducing it — I can upload a Docker image to help.**

## Steps to reproduce

```bash
export CC="clang"
export CXX="clang++"
export CFLAGS="-fsanitize=address -g -O0 -fno-omit-frame-pointer"
export CXXFLAGS="-fsanitize=address -g -O0 -fno-omit-frame-pointer -stdlib=libc++"
export LIB_FUZZING_ENGINE="-fsanitize=fuzzer"

mkdir work
cd work
cmake -GNinja ..
ninja

wget https://github.com/google/oss-fuzz/raw/refs/heads/master/projects/tidy-html5/tidy_general_fuzzer.c
${CC} ${CFLAGS} -c -I../include \
    tidy_general_fuzzer.c -o tidy_general_fuzzer.o
${CXX} ${CXXFLAGS} -std=c++11 tidy_general_fuzzer.o \
    -o tidy_general_fuzzer \
    $LIB_FUZZING_ENGINE libtidy.a
./tidy_general_fuzzer $POC
```

## Sanitizer output

```
==14016==ERROR: LeakSanitizer: detected memory leaks

Indirect leak of 9856 byte(s) in 88 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x56d9f9 in prvTidyNewNode /src/tidy-html5/src/lexer.c:1426:26
    #3 0x56d9f9 in TagToken /src/tidy-html5/src/lexer.c:1587:18
    #4 0x56d9f9 in GetTokenFromStream /src/tidy-html5/src/lexer.c:2886:32
    #5 0x56d9f9 in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #6 0x478271 in ParseXMLElement /src/tidy-html5/src/parser.c:5667:20
    #7 0x474143 in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1077:25
    #8 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #9 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #10 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #11 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #12 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #13 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #14 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 9296 byte(s) in 166 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x5708e7 in prvTidyNewAttribute /src/tidy-html5/src/lexer.c:4156:28
    #3 0x5708e7 in ParseAttrs /src/tidy-html5/src/lexer.c:4241:18
    #4 0x5708e7 in GetTokenFromStream /src/tidy-html5/src/lexer.c:2894:34
    #5 0x5708e7 in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #6 0x478271 in ParseXMLElement /src/tidy-html5/src/parser.c:5667:20
    #7 0x474143 in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1077:25
    #8 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #9 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #10 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #11 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #12 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #13 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #14 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 2912 byte(s) in 26 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x56aba4 in prvTidyNewNode /src/tidy-html5/src/lexer.c:1426:26
    #3 0x56aba4 in prvTidyTextToken /src/tidy-html5/src/lexer.c:1558:18
    #4 0x56aba4 in GetTokenFromStream /src/tidy-html5/src/lexer.c:2839:21
    #5 0x56aba4 in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #6 0x478271 in ParseXMLElement /src/tidy-html5/src/parser.c:5667:20
    #7 0x474143 in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1077:25
    #8 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #9 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #10 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #11 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #12 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #13 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #14 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 458 byte(s) in 166 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x5eed03 in prvTidytmbstrndup /src/tidy-html5/src/tmbstr.c:32:34
    #3 0x59fda9 in ParseAttribute /src/tidy-html5/src/lexer.c:3735:23
    #4 0x56efea in ParseAttrs /src/tidy-html5/src/lexer.c:4211:28
    #5 0x56efea in GetTokenFromStream /src/tidy-html5/src/lexer.c:2894:34
    #6 0x56efea in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #7 0x478271 in ParseXMLElement /src/tidy-html5/src/parser.c:5667:20
    #8 0x474143 in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1077:25
    #9 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #10 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #11 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #12 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #13 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #14 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #15 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 199 byte(s) in 88 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x5eed03 in prvTidytmbstrndup /src/tidy-html5/src/tmbstr.c:32:34
    #3 0x56e408 in TagToken /src/tidy-html5/src/lexer.c:1589:21
    #4 0x56e408 in GetTokenFromStream /src/tidy-html5/src/lexer.c:2886:32
    #5 0x56e408 in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #6 0x478271 in ParseXMLElement /src/tidy-html5/src/parser.c:5667:20
    #7 0x474143 in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1077:25
    #8 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #9 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #10 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #11 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #12 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #13 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #14 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 112 byte(s) in 1 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x56d9f9 in prvTidyNewNode /src/tidy-html5/src/lexer.c:1426:26
    #3 0x56d9f9 in TagToken /src/tidy-html5/src/lexer.c:1587:18
    #4 0x56d9f9 in GetTokenFromStream /src/tidy-html5/src/lexer.c:2886:32
    #5 0x56d9f9 in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #6 0x47514f in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1112:16
    #7 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #8 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #9 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #10 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #11 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #12 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #13 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 91 byte(s) in 25 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x5eed03 in prvTidytmbstrndup /src/tidy-html5/src/tmbstr.c:32:34
    #3 0x5a6101 in ParseValue /src/tidy-html5/src/lexer.c:4119:17
    #4 0x56fc3d in ParseAttrs /src/tidy-html5/src/lexer.c:4236:17
    #5 0x56fc3d in GetTokenFromStream /src/tidy-html5/src/lexer.c:2894:34
    #6 0x56fc3d in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #7 0x478271 in ParseXMLElement /src/tidy-html5/src/parser.c:5667:20
    #8 0x474143 in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1077:25
    #9 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #10 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #11 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #12 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #13 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #14 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #15 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

Indirect leak of 2 byte(s) in 1 object(s) allocated from:
    #0 0x6c464d in malloc (/out/tidy_general_fuzzer.fuzz+0x6c464d)
    #1 0x5dd8a4 in defaultAlloc /src/tidy-html5/src/alloc.c:64:45
    #2 0x5eed03 in prvTidytmbstrndup /src/tidy-html5/src/tmbstr.c:32:34
    #3 0x56e408 in TagToken /src/tidy-html5/src/lexer.c:1589:21
    #4 0x56e408 in GetTokenFromStream /src/tidy-html5/src/lexer.c:2886:32
    #5 0x56e408 in prvTidyGetToken /src/tidy-html5/src/lexer.c:2501:12
    #6 0x47514f in ParseHTMLWithNode /src/tidy-html5/src/parser.c:1112:16
    #7 0x41e5bf in prvTidyParseXMLDocument /src/tidy-html5/src/parser.c:6439:13
    #8 0x41e5bf in prvTidyDocParseStream /src/tidy-html5/src/tidylib.c:1502:9
    #9 0x41485d in tidyDocParseFile /src/tidy-html5/src/tidylib.c:1178:18
    #10 0x41485d in tidyParseFile /src/tidy-html5/src/tidylib.c:1107:12
    #11 0x40b999 in TidyXhtml /src/tidy_general_fuzzer.c:128:7
    #12 0x4108d4 in LLVMFuzzerTestOneInput /src/tidy_general_fuzzer.c:154:3
    #13 0x653d0a in main (/out/tidy_general_fuzzer.fuzz+0x653d0a)

SUMMARY: AddressSanitizer: 22926 byte(s) leaked in 561 allocation(s).
```

## POC

[tidy-html5_crash_3.txt](https://github.com/user-attachments/files/20438303/tidy-html5_crash_3.txt)

## Credit

Reported by Yifan Zhang, [PLL](https://pl.cs.pku.edu.cn/en/)


## Comment 3167094901

other (NONE) · morslm · 2025-08-08T08:59:22Z · https://github.com/htacg/tidy-html5/issues/1152#issuecomment-3167094901

It happens at this location: https://github.com/htacg/tidy-html5/blob/d08ddc2860aa95ba8e301343a30837f157977cba/src/parser.c#L1112

This code fragment:
```
node = TY_(GetToken)(doc, mode);
...
if (node)
    parser = GetParserForNode(doc, node);
else
    something_to_do = no;
```
A node is created that isn't properly linked to the DOM structure.

## Comment 5436548855

other (NONE) · psumbera · 2026-08-27T08:40:05Z · https://github.com/htacg/tidy-html5/issues/1152#issuecomment-5436548855

I retested this with the attached PoC against the exact vulnerable tidy commit d08ddc2860aa95ba8e301343a30837f157977cba and could not reproduce it. I also tried an exact Clang 18.1.8 + libc++ 18 setup and a system-libcxxabi mix, with the same result: the input completed cleanly and did not trigger an ASan leak report. If a different reproducer or build setup is needed, please share it.
