# attempting free on address which was not malloc()-ed in AP4_HdlrAtom::~AP4_HdlrAtom

- URL: https://github.com/axiomatic-systems/Bento4/issues/385
- Repo: axiomatic-systems/Bento4 (language: C++)
- State: open; created 2019-04-20T11:46:59Z; status ok; passes main

## Issue body

reporter (NONE) · zjuchenyuan · 2019-04-20T11:46:59Z · https://github.com/axiomatic-systems/Bento4/issues/385

POC: [mp42aac_poc2.zip](https://github.com/axiomatic-systems/Bento4/files/3100076/mp42aac_poc2.zip)

```
# ./mp42aac mp42aac_poc2 /dev/null
=================================================================
==1166==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x60200000ef50 in thread T0
    #0 0x7ffff6f03caa in operator delete[](void*) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99caa)
    #1 0x55fafb in AP4_HdlrAtom::~AP4_HdlrAtom() /d/prog/Bento4/Source/C++/Core/Ap4HdlrAtom.h:61
    #2 0x55fafb in AP4_HdlrAtom::~AP4_HdlrAtom() /d/prog/Bento4/Source/C++/Core/Ap4HdlrAtom.h:61
    #3 0x5b4a77 in AP4_List<AP4_Atom>::DeleteReferences() /d/prog/Bento4/Source/C++/Core/Ap4List.h:476
    #4 0x5b4a77 in AP4_AtomParent::~AP4_AtomParent() /d/prog/Bento4/Source/C++/Core/Ap4Atom.cpp:512
    #5 0x4d9bc3 in AP4_ContainerAtom::~AP4_ContainerAtom() /d/prog/Bento4/Source/C++/Core/Ap4ContainerAtom.h:48
    #6 0x4d9bc3 in AP4_ContainerAtom::~AP4_ContainerAtom() /d/prog/Bento4/Source/C++/Core/Ap4ContainerAtom.h:48
    #7 0x5b4a77 in AP4_List<AP4_Atom>::DeleteReferences() /d/prog/Bento4/Source/C++/Core/Ap4List.h:476
    #8 0x5b4a77 in AP4_AtomParent::~AP4_AtomParent() /d/prog/Bento4/Source/C++/Core/Ap4Atom.cpp:512
    #9 0x54d7ef in AP4_File::~AP4_File() /d/prog/Bento4/Source/C++/Core/Ap4File.cpp:84
    #10 0x54d7ef in AP4_File::~AP4_File() /d/prog/Bento4/Source/C++/Core/Ap4File.cpp:88
    #11 0x43ef9f in main /d/prog/Bento4/Source/C++/Apps/Mp42Aac/Mp42Aac.cpp:303
    #12 0x7ffff652882f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #13 0x442fb8 in _start (/d/p/latest/7.mp42aac+0x442fb8)

0x60200000ef50 is located 0 bytes inside of 1-byte region [0x60200000ef50,0x60200000ef51)
allocated by thread T0 here:
    #0 0x7ffff6f036b2 in operator new[](unsigned long) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x996b2)
    #1 0x55ac7f in AP4_String::Assign(char const*, unsigned int) /d/prog/Bento4/Source/C++/Core/Ap4String.cpp:165
    #2 0x55ac7f in AP4_String::operator=(char const*) /d/prog/Bento4/Source/C++/Core/Ap4String.cpp:123

SUMMARY: AddressSanitizer: bad-free ??:0 operator delete[](void*)
==1166==ABORTING
```

This bug was found by [NESA Lab](https://nesa.zju.edu.cn).
