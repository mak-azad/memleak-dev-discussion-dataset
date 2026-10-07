# Bug: Allocation-Size-Too-Big Error in Q3DImporter::InternReadFile

- URL: https://github.com/assimp/assimp/issues/6356
- Repo: assimp/assimp (language: C++)
- State: open; created 2025-09-18T13:39:01Z; status ok; passes main

## Issue body

reporter (NONE) · ahuo1 · 2025-09-18T13:39:01Z · https://github.com/assimp/assimp/issues/6356

## Environment
- OS: Ubuntu 22.04
- Compiler: clang 13.0.1
- C++ Standard: C++17
- Sanitizers: AddressSanitizer (ASan) + UndefinedBehaviorSanitizer (UBSan)
- Assimp Version: 6.0.2 / master commit [0581ed5](https://github.com/assimp/assimp/commit/0581ed5f114ebea8654d3ce16cd5b64f59b8c7b3)

## Build Instructions
```
export CC=clang-13
export CXX=clang++-13
export CFLAGS="${CFLAGS} -fsanitize=address -O1 -g"
export CXXFLAGS="${CXXFLAGS} -fsanitize=address -O1 -g"
export LDFLAGS="${LDFLAGS} -fsanitize=address"

export LIB_FUZZING_ENGINE="-fsanitize=fuzzer"

cmake CMakeLists.txt -G "Ninja" -DBUILD_SHARED_LIBS=OFF -DASSIMP_BUILD_ZLIB=ON \
                                -DASSIMP_BUILD_TESTS=ON -DASSIMP_BUILD_ASSIMP_TOOLS=OFF \
                                -DASSIMP_BUILD_SAMPLES=OFF
cmake --build .

$CXX $CXXFLAGS $LIB_FUZZING_ENGINE -std=c++11 -I./include \
        fuzz/assimp_fuzzer.cc -o ./assimp_fuzzer  \
        ./lib/libassimp.a ./contrib/zlib/libzlibstatic.a
```

## Reproduction
Run the fuzzer with a crafted input file:
```
./assimp_fuzzer poc
```

## Observed Behavior
Program crashes with ASan/UBSan report:

```
==1959368==ERROR: AddressSanitizer: requested allocation size 0x1c1b04999f0 (0x1c1b049a9f0 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x519efd in operator new(unsigned long) (/assimp_fuzzer+0x519efd)
    #1 0x1489ccc in __gnu_cxx::new_allocator<Assimp::Q3DImporter::Material>::allocate(unsigned long, void const*) /usr/bin/../lib/gcc/x86_64-linux-gnu/11/../../../../include/c++/11/ext/new_allocator.h:127:27
    #2 0x1489ccc in std::allocator_traits<std::allocator<Assimp::Q3DImporter::Material> >::allocate(std::allocator<Assimp::Q3DImporter::Material>&, unsigned long) /usr/bin/../lib/gcc/x86_64-linux-gnu/11/../../../../include/c++/11/bits/alloc_traits.h:464:20
    #3 0x1489ccc in std::_Vector_base<Assimp::Q3DImporter::Material, std::allocator<Assimp::Q3DImporter::Material> >::_M_allocate(unsigned long) /usr/bin/../lib/gcc/x86_64-linux-gnu/11/../../../../include/c++/11/bits/stl_vector.h:346:20
    #4 0x1489ccc in Assimp::Q3DImporter::Material* std::vector<Assimp::Q3DImporter::Material, std::allocator<Assimp::Q3DImporter::Material> >::_M_allocate_and_copy<Assimp::Q3DImporter::Material const*>(unsigned long, Assimp::Q3DImporter::Material const*, Assimp::Q3DImporter::Material const*) /usr/bin/../lib/gcc/x86_64-linux-gnu/11/../../../../include/c++/11/bits/stl_vector.h:1511:29
    #5 0x957941 in Assimp::BaseImporter::ReadFile(Assimp::Importer*, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, Assimp::IOSystem*) /root/assimp/code/Common/BaseImporter.cpp:131:9
    #6 0x522c01 in Assimp::Importer::ReadFile(char const*, unsigned int) /root/assimp/code/Common/Importer.cpp:709:30
    #7 0x52082b in Assimp::Importer::ReadFileFromMemory(void const*, unsigned long, unsigned int, char const*) /root/assimp/code/Common/Importer.cpp:507:9
    #8 0x51c8ba in LLVMFuzzerTestOneInput /root/assimp/fuzz/assimp_fuzzer.cc:57:34
    ...
```

## Root Cause Analysis
https://github.com/assimp/assimp/blob/0581ed5f114ebea8654d3ce16cd5b64f59b8c7b3/code/AssetLib/Q3D/Q3DLoader.cpp#L122-L133
The crash occurs in the Q3DImporter::InternReadFile function, where the importer reads the number of materials (numMats) directly from the input file without validation. This value is then used in a call to materials.reserve(numMats) and later in a loop with materials.emplace_back(). Since numMats is attacker-controlled, a malicious file can specify an extremely large value, leading the program to request an allocation far exceeding addressable memory. This results in an allocation-size-too-big error under ASan and causes the process to terminate.


The attached file contains a proof-of-concept.
[poc.zip](https://github.com/user-attachments/files/22407575/poc.zip)

## Comment 3369234100

other (NONE) · carnil · 2025-10-05T18:20:58Z · https://github.com/assimp/assimp/issues/6356#issuecomment-3369234100

CVE-2025-11274 seems to have been assigned for this issue.

## Comment 3675353198

other (NONE) · BrannonKing · 2025-12-19T14:50:15Z · https://github.com/assimp/assimp/issues/6356#issuecomment-3675353198

What if they put in a negative number? The casting there will turn that into a very large number.
