# allocation-size-too-big in mp4dump

- URL: https://github.com/axiomatic-systems/Bento4/issues/748
- Repo: axiomatic-systems/Bento4 (language: C++)
- State: open; created 2022-08-28T08:02:59Z; status ok; passes main

## Issue body

reporter (NONE) · WorldExecute · 2022-08-28T08:02:59Z · https://github.com/axiomatic-systems/Bento4/issues/748

Hi, i find a allocation-size-too-big  error in mp4dump. I saved all my test files [here](https://github.com/WorldExecute/files/tree/main/Bento4)

Here are the details.

For **mp4dump** with [test input](https://github.com/WorldExecute/files/blob/main/Bento4/mp4dump/allocation-size-too-big/test_1):
```
test_1:
=================================================================
==47797==ERROR: AddressSanitizer: requested allocation size 0xfffffffffb000001 (0xfffffffffb001008 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x4c573d in operator new[](unsigned long) (/Bento4/install-asan/bin/mp4dump+0x4c573d)
    #1 0x56a240 in AP4_RtpAtom::AP4_RtpAtom(unsigned int, AP4_ByteStream&) /Bento4/Source/C++/Core/Ap4RtpAtom.cpp:49:21

==47797==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big (/Bento4/install-asan/bin/mp4dump+0x4c573d) in operator new[](unsigned long)
==47797==ABORTING


```


You can use the following setp to reproduce all the problems.
```
git clone https://github.com/axiomatic-systems/Bento4
cd Bento4/
mkdir check && cd check
cmake ../ -DCMAKE_C_COMPILER=clang  -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_FLAGS="-fsanitize=address" -DCMAKE_CXX_FLAGS="-fsanitize=address" -DCMAKE_BUILD_TYPE=Release
make -j
git clone https://github.com/WorldExecute/files.git
./mp4dump ./files/Bento4/mp4dump/allocation-size-too-big/test_1
```
Thanks for your time!
