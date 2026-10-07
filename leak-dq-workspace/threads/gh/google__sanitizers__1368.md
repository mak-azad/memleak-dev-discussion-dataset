# Possible ASAN false positive when calling std::ostringstream's str when overriding new+delete

- URL: https://github.com/google/sanitizers/issues/1368
- Repo: google/sanitizers (language: C)
- State: open; created 2021-01-23T10:30:03Z; status ok; passes main

## Issue body

reporter (NONE) · jyaif · 2021-01-23T10:30:03Z · https://github.com/google/sanitizers/issues/1368

When running my program with ASAN, I'm getting an error when using std::ostringstream. Something special with the program is that it's overriding the new and delete operators.

Here's a simplified repro case:

```c++
#include <sstream>

char big_chunk[1000000];
char* alloc = big_chunk;

void *operator new(std::size_t sz)  {
   char* a = alloc;
   alloc += ((sz +7)&~7);
   return a;
}

void operator delete(void *p) noexcept {
}

void operator delete(void* p, std::size_t) noexcept {
}

int main() {
  std::ostringstream stream;
  stream << "a long string that will need allocation";
  stream.str();
  return 0;
}
```

When compiled and ran with:
```
clang++ --std=c++17 main.cpp -fsanitize=address -O0 -g && ./a.out
```

I'm getting the following error, which I believe is a false positive:
```
=================================================================
==17820==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x0001081fc380 in thread T0
    #0 0x108392c0d in wrap__ZdlPv+0x7d (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x55c0d)
    #1 0x1081f11dc in main main.cpp:21
    #2 0x7fff20354620 in start+0x0 (libdyld.dylib:x86_64+0x15620)

0x0001081fc380 is located 0 bytes inside of global variable 'big_chunk' defined in 'main.cpp:3:6' (0x1081fc380) of size 1000000
SUMMARY: AddressSanitizer: bad-free (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x55c0d) in wrap__ZdlPv+0x7d
==17820==ABORTING
Abort trap: 6
```
(main.cpp:21 corresponds to the stream.str(); line)
