# test_back_comp: heap-use-after-free -- ReferenceState printed after cg_free()

- URL: https://github.com/CGNS/CGNS/issues/978
- Repo: CGNS/CGNS (language: C)
- State: open; created 2026-08-05T20:47:07Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · brtnfld · 2026-08-05T20:47:07Z · https://github.com/CGNS/CGNS/issues/978

`src/tests/test_back_comp.c` frees the `ReferenceState` string and then prints it:

https://github.com/CGNS/CGNS/blob/develop/src/tests/test_back_comp.c#L432-L438

```c
    if (cg_state_read(&state))
      cg_error_exit();
    if ( ! compareValuesChr(state,"ReferenceQuantities"))
      cg_error_exit();
    cg_free(state);

    printf("\nReferenceState = %s\n",state);   /* <-- state was freed on the line above */
```

`cg_state_read()` allocates via `cgi_malloc` (`cgnslib.c:19300`), `cg_free()`
releases it (`cgnslib.c:24627`), and the `printf` then reads it.

### Reproduction

Build with AddressSanitizer and run the test:

```
cmake -DCMAKE_BUILD_TYPE=Debug \
      -DCMAKE_C_FLAGS="-g -O1 -fsanitize=address -fno-omit-frame-pointer" \
      -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address" \
      -DCMAKE_SHARED_LINKER_FLAGS="-fsanitize=address" \
      -DCGNS_ENABLE_TESTS=ON ...
ctest -R test_back_comp
```

```
==535512==ERROR: AddressSanitizer: heap-use-after-free on address 0x7b57d91eb5c0
READ of size 3 at 0x7b57d91eb5c0 thread T0
    #2 in printf
    #3 in main src/tests/test_back_comp.c:438

freed by thread T0 here:
    #1 in cg_free src/cgnslib.c:24627
    #2 in main src/tests/test_back_comp.c:436

previously allocated by thread T0 here:
    #1 in cgi_malloc src/cgns_internals.c:93
    #2 in cg_state_read src/cgnslib.c:19300
    #3 in main src/tests/test_back_comp.c:432

SUMMARY: AddressSanitizer: heap-use-after-free src/tests/test_back_comp.c:438 in main
```

The test passes in ordinary builds because the freed block usually still holds
the old bytes, so this only surfaces under a sanitizer.

### Suggested fix

Move the `printf` above the `cg_free(state)`.

### Notes

- Present on `develop` (`8c1e96b`); the `cg_free` call dates to 3c42e51c, the
  `printf` to afbbbc9e.
- Bug is in the test, not in the library.
- Found while running the test suite under ASAN/LSan during review of #916; it
  is unrelated to that PR, which does not touch this file.
- Two other tests fail the same ASAN run for a different, also pre-existing
  reason -- `C_code_read_descriptor` and `C_code_read_nondimensional` leak the
  buffer returned by `cg_descriptor_read` (`cgnslib.c:21365`). Happy to fold
  those into this issue or file separately, whichever you prefer.

