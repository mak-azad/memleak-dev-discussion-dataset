# Fix for Mismatched delete / delete[] in Memory Deallocation

- URL: https://github.com/OpenGene/fastp/issues/625
- Repo: OpenGene/fastp (language: C++)
- State: open; created 2025-07-06T17:48:14Z; status ok; passes main

## Issue body

reporter (NONE) · peppapig450 · 2025-07-06T17:48:14Z · https://github.com/OpenGene/fastp/issues/625

## Summary
While running Valgrind, I noticed several "Mismatched free() / delete / delete[]" errors across the codebase. Arrays allocated with `new[]` are being freed with `delete` instead of `delete[]`, causing undefined behavior and potential memory corruption.

## Evidence
```
==190175== Mismatched free() / delete / delete []
==190175==    at 0x49037A7: operator delete(void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==190175==    by 0x409F5C8: Stats::~Stats() (src/stats.cpp:114)
==190175==  Address 0x4f72f80 is 0 bytes inside a block of size 9,400 alloc'd
==190175==    at 0x4901007: operator new[](unsigned long) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==190175==    by 0x409EC7A: Stats::Stats(Options*, bool, int, int) (src/stats.cpp:39)
```

## Build Environment

#### Compile Flags:
```makefile
CXXFLAGS := -std=c++11 -O0 -g -fno-omit-frame-pointer -pthread -MD -MP -I$(DIR_INC)
LD_FLAGS := $(foreach librarydir,$(LIBRARY_DIRS),-L$(librarydir)) $(LIBS) $(LD_FLAGS)
```

#### Valgrind Command:
```shell
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./fastp -i testdata/R2.fq -o test.fq
```

#### Valgrind Output:
[Uploaded here.](https://gist.github.com/peppapig450/5aa8056b9248c3c009b1c59d0bbeba0f)

## Root Cause
In C++, arrays allocated with new[] need to be freed using delete[] rather than delete. Using the wrong deallocation operator is undefined behavior.

## Affected Files and Lines

### `src/stats.cpp` - Stats class destructor (~line 114-138)
**Problem:**
```cpp
// Constructor allocates with new[]
mCycleQ30Bases[i] = new long[mBufLen];      // line 39
mCycleQ20Bases[i] = new long[mBufLen];      // line 42  
mCycleBaseContents[i] = new long[mBufLen];  // line 45
mCycleBaseQual[i] = new long[mBufLen];      // line 48
mCycleTotalBase = new long[mBufLen];        // line 51
mCycleTotalQual = new long[mBufLen];        // line 54

// Destructor incorrectly uses delete
delete mCycleQ30Bases[i];     // Should be delete[]
delete mCycleQ20Bases[i];     // Should be delete[]
delete mCycleBaseContents[i]; // Should be delete[]
delete mCycleBaseQual[i];     // Should be delete[]
delete mCycleTotalBase;       // Should be delete[]
delete mCycleTotalQual;       // Should be delete[]
```

### `src/filterresult.cpp` - FilterResult class (~line 25)
**Problem:**
```cpp
// Constructor
mCorrectionMatrix = new long[64];  // line 19

// Destructor  
delete mCorrectionMatrix;          // Should be delete[]
```

### `src/stats.cpp` - Stats::summarize() method (~line 188-190)
Arrays allocated in `summarize()` and stored in `mQualityCurves`/`mContentCurves` maps are likely freed with `delete` instead of `delete[]`.

### `src/stats.cpp` - Stats::extendBuffer() method
Multiple `new[]` allocations that may be incorrectly freed.

## Impact
- **Memory corruption** leading to unpredictable behavior
- **Potential crashes** during cleanup/destruction
- **Potentially impacts scientific reproducibility** due to unstable execution
- **Security implications** from heap corruption

## Proposed Fix
Replace all `delete` calls with `delete[]` for arrays:

```cpp
// In Stats destructor
delete[] mCycleQ30Bases[i];
delete[] mCycleQ20Bases[i]; 
delete[] mCycleBaseContents[i];
delete[] mCycleBaseQual[i];
delete[] mCycleTotalBase;
delete[] mCycleTotalQual;

// In FilterResult destructor  
delete[] mCorrectionMatrix;
```

I'd be happy to submit a PR with these fixes if that would be helpful. The changes are straightforward and I can include all necessary `delete` → `delete[]` conversions.

### Optional Future Enhancement
Consider migrating to modern C++ containers (`std::vector<long>`, `std::array<long, N>`) to eliminate manual memory management entirely, but the immediate priority is fixing the current undefined behavior.


## Comment 4118711903

other (NONE) · gregdev00 · 2026-03-24T14:23:33Z · https://github.com/OpenGene/fastp/issues/625#issuecomment-4118711903

I think this mr fixes it: https://github.com/OpenGene/fastp/pull/670
