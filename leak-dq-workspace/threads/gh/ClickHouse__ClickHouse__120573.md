# `IAST::intrusive_ptr_release` calls `dynamic_cast<void *>` on an already-destroyed object — latent UB, interior-pointer free under `operator delete` on any AST class whose `IAST` base is not at offset 0

- URL: https://github.com/ClickHouse/ClickHouse/issues/120573
- Repo: ClickHouse/ClickHouse (language: C++)
- State: open; created 2026-09-17T11:13:30Z; status ok; passes main

## Issue body

reporter (MEMBER) · qoega · 2026-09-17T11:13:30Z · https://github.com/ClickHouse/ClickHouse/issues/120573

# `IAST::intrusive_ptr_release` calls `dynamic_cast<void *>` on an already-destroyed object — latent UB, interior-pointer free under `operator delete` on any AST class whose `IAST` base is not at offset 0

### Describe what's wrong

The non-recursive AST deleter in `src/Parsers/IAST.cpp` (`intrusive_ptr_release`, `LinkedList::create`) destroys the node with `ptr->~IAST()` and only then computes the address of the complete object with `dynamic_cast<void *>(ptr)` to reuse the storage for a `LinkedList` element, which is later released with `operator delete(list_head)`.

`dynamic_cast` on an object whose lifetime has ended is undefined behaviour. In practice, under the Itanium ABI, the dynamic type during and after `~IAST()` is `IAST`, so the cast may return the address of the `IAST` base subobject instead of the complete object. For any AST class whose `IAST` base is **not** at offset 0 (multiple inheritance with a non-`IAST` first base) the deleter then frees an interior pointer.

### Where

`src/Parsers/IAST.cpp`, `intrusive_ptr_release` → `LinkedList::create`:

```cpp
ASTs children;
children.swap(ptr->children);
ptr->~IAST();                                                   // object is dead here
LinkedList * elem = new (dynamic_cast<void *>(ptr)) LinkedList; // UB: dynamic_cast on a destroyed object
...
list_head->~LinkedList();
operator delete(list_head);                                     // frees whatever the cast returned
```

### Why the existing test does not catch it natively

`src/Parsers/tests/gtest_ast_deleter.cpp` deliberately uses `struct ASTCounting : public StackDecrementer, public DB::IAST` (the `IAST` base is at a non-zero offset), i.e. exactly the layout this code is meant to handle, and it passes in CI.

It passes only because clang does not store the `IAST` vtable pointer in the (base-object) destructor when nothing in the destructor observes it, so the stale derived vptr still gives the right offset-to-top. That is an implementation detail, not a guarantee; a compiler or build mode that resets the vptr in destructors (Fil-C's clang does) exposes it immediately.

### Evidence

Running `unit_tests_dbms --gtest_filter=ASTDeleter.*` with a Fil-C build of master (memory-safe C/C++ toolchain, AArch64):

```
filc safety error: cannot free ptr with ptr != lower (ptr = 0xf246365d7b00,0xf246365d7af0,0xf246365d7b40,...).
    src/Common/memory.h:183:17: untrackMemory<> (inlined)
    src/Common/AllocationInterceptors.cpp:180:31: operator delete(void*)
    src/Parsers/IAST.cpp:74:17: DB::intrusive_ptr_release(DB::IAST const*)
    contrib/boost/boost/smart_ptr/intrusive_ptr.hpp:76:23: ~intrusive_ptr (inlined)
    src/Parsers/tests/gtest_ast_deleter.cpp:68:5: ASTDeleter_SimpleChain_Test::TestBody()
```

`ptr` is 16 bytes past the start of the allocation (`lower`): the freed pointer is the `IAST` subobject inside the `ASTWithDecrementer` object. With the fix below the suite passes on the same build (5 tests).

### Impact

- Production AST classes all seem to have an `IAST`-derived first base, so the interior-pointer free does not happen with the current compiler; the defect is **latent UB** that depends on codegen.
- Any future AST class with a non-`IAST` first base, or a compiler change in destructor vptr handling, turns it into a heap corruption (jemalloc frees the wrong slot) or an ASan "attempting free on address which was not malloc()-ed".

### Fix

Take the complete-object address while the object is alive (one line moved; comment added):

```cpp
ASTs children;
children.swap(ptr->children);
void * storage = dynamic_cast<void *>(ptr);
ptr->~IAST();
LinkedList * elem = new (storage) LinkedList;
```

Native behaviour is unchanged for classes with `IAST` at offset 0; the existing `ASTDeleter` unit tests cover the multiple-inheritance layout. PR incoming.

