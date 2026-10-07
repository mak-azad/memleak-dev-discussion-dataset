# Fix malloc/delete mismatch in Linux resource path detection

- URL: https://github.com/NanoMichael/MicroTeX/issues/193
- Repo: NanoMichael/MicroTeX (language: C++)
- State: closed; created 2026-08-13T07:36:38Z; status ok; passes main

## Issue body

reporter (NONE) · Danmoreng · 2026-08-13T07:36:38Z · https://github.com/NanoMichael/MicroTeX/issues/193

## Problem

`LaTeX::queryResourceLocation` allocates `userdata_fallback` with `asprintf`, then releases it with `delete`. On Linux this is an allocator mismatch (`malloc` vs. `operator delete`) and undefined behavior.

AddressSanitizer reports:

```text
ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete)
  #1 tex::LaTeX::queryResourceLocation(...) src/latex.cpp:59

allocated by:
  #3 asprintf
  #4 tex::LaTeX::queryResourceLocation(...) src/latex.cpp:57
```

The issue is triggered whenever `HOME` is set and `LaTeX::init` queries resource locations. It was reproduced against current `master` (`0e3707f6dafebb121d98b53c64364d16fefe481d`) with GCC and ASan/UBSan on Linux.

## Proposed fix

Avoid the temporary C allocation entirely:

```cpp
char* home = getenv("HOME");
if (home != NULL && strcmp(home, "") != 0) {
  paths.push(string(home) + "/.local/share/clatexmath/");
}
```

This removes the allocator mismatch and the GNU-specific `asprintf` call. The change has been verified with an ASan/UBSan test run in a downstream application. I will follow up with a small pull request.

