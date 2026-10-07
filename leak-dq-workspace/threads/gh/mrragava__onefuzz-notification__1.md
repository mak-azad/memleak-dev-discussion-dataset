# setup/fuzz - AddressSanitizer: bad-free (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x511f10) in free

- URL: https://github.com/mrragava/onefuzz-notification/issues/1
- Repo: mrragava/onefuzz-notification (language: C)
- State: open; created 2021-06-25T01:48:12Z; status ok; passes main

## Issue body

reporter (OWNER) · mrragava · 2021-06-25T01:48:12Z · https://github.com/mrragava/onefuzz-notification/issues/1

## Files

* input: [crash-f4c53c26f28d6ba480acb490b5ceab3729ac50fa](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-crashes-032590c6e8ea524cb32942a29c898a62&filename=crash-f4c53c26f28d6ba480acb490b5ceab3729ac50fa)
* exe: [setup/fuzz]( https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-setup-a7ec4edefc00598fae7acd01bc3d636f&filename=fuzz)
* report: [e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-unique-reports-032590c6e8ea524cb32942a29c898a62&filename=e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json)

## Repro

 `onefuzz --endpoint https://oefuzzingtest2instance.azurewebsites.net repro create_and_connect oft-unique-reports-032590c6e8ea524cb32942a29c898a62 e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json`

## Call Stack

```#0 0x511f10 in free (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x511f10)
#1 0x54ae96 in LLVMFuzzerTestOneInput /__w/onefuzz-notification/onefuzz-notification/simple-libfuzzer/simple.c:38:24
#2 0x42e9f7 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x42e9f7)
#3 0x41ee8a in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x41ee8a)
#4 0x429e50 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x429e50)
#5 0x41cb52 in main (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x41cb52)
#6 0x7ffff6a99bf6 in __libc_start_main /build/glibc-S9d2JN/glibc-2.27/csu/../csu/libc-start.c:310
#7 0x41cbc9 in _start (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x41cbc9)
```

## ASAN Log

```INFO: Seed: 307833847
INFO: Loaded 1 modules   (21 inline 8-bit counters): 21 [0x788fb0, 0x788fc5), 
INFO: Loaded 1 PC tables (21 PCs): 21 [0x5664c8,0x566618), 
setup/fuzz: Running 1 inputs 1 time(s) each.
Running: /tmp/.tmpOuUOZ2/crash-f4c53c26f28d6ba480acb490b5ceab3729ac50fa
=================================================================
==5782==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7fffffffd020 in thread T0
    #0 0x511f10 in free (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x511f10)
    #1 0x54ae96 in LLVMFuzzerTestOneInput /__w/onefuzz-notification/onefuzz-notification/simple-libfuzzer/simple.c:38:24
    #2 0x42e9f7 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x42e9f7)
    #3 0x41ee8a in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x41ee8a)
    #4 0x429e50 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x429e50)
    #5 0x41cb52 in main (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x41cb52)
    #6 0x7ffff6a99bf6 in __libc_start_main /build/glibc-S9d2JN/glibc-2.27/csu/../csu/libc-start.c:310
    #7 0x41cbc9 in _start (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x41cbc9)

Address 0x7fffffffd020 is located in stack of thread T0 at offset 32 in frame
    #0 0x54a5ff in LLVMFuzzerTestOneInput /__w/onefuzz-notification/onefuzz-notification/simple-libfuzzer/simple.c:8

  This frame has 1 object(s):
    [32, 36) 'cnt' (line 9) <== Memory access at offset 32 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism or swapcontext
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: bad-free (/onefuzz/blob-containers/fuzz3rpz7enxyexcq/fuzz+0x511f10) in free
==5782==ABORTING
```

## Comment 869080975

reporter (OWNER) · mrragava · 2021-06-27T00:51:06Z · https://github.com/mrragava/onefuzz-notification/issues/1#issuecomment-869080975

Duplicate found.

* input: [crash-884903fbc80b23c96a92eda563ef82fd6716052b](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-crashes-032590c6e8ea524cb32942a29c898a62&filename=crash-884903fbc80b23c96a92eda563ef82fd6716052b)
* exe: [setup/fuzz]( https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-setup-a7ec4edefc00598fae7acd01bc3d636f&filename=fuzz)
* report: [e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-unique-reports-032590c6e8ea524cb32942a29c898a62&filename=e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json)

## Comment 869080977

reporter (OWNER) · mrragava · 2021-06-27T00:51:07Z · https://github.com/mrragava/onefuzz-notification/issues/1#issuecomment-869080977

Duplicate found.

* input: [crash-884903fbc80b23c96a92eda563ef82fd6716052b](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-crashes-032590c6e8ea524cb32942a29c898a62&filename=crash-884903fbc80b23c96a92eda563ef82fd6716052b)
* exe: [setup/fuzz]( https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-setup-a7ec4edefc00598fae7acd01bc3d636f&filename=fuzz)
* report: [e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-unique-reports-032590c6e8ea524cb32942a29c898a62&filename=e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json)

## Comment 869080979

reporter (OWNER) · mrragava · 2021-06-27T00:51:07Z · https://github.com/mrragava/onefuzz-notification/issues/1#issuecomment-869080979

Duplicate found.

* input: [crash-884903fbc80b23c96a92eda563ef82fd6716052b](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-crashes-032590c6e8ea524cb32942a29c898a62&filename=crash-884903fbc80b23c96a92eda563ef82fd6716052b)
* exe: [setup/fuzz]( https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-setup-a7ec4edefc00598fae7acd01bc3d636f&filename=fuzz)
* report: [e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json](https://oefuzzingtest2instance.azurewebsites.net/api/download?container=oft-unique-reports-032590c6e8ea524cb32942a29c898a62&filename=e711c125516bc2ef456fb7841568f294f62c84046576effdcbdae316e4a66b12.json)
