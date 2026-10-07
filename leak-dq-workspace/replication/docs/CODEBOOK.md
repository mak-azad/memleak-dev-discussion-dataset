# Codebook

Version 2026-10-05. Machine-readable labels live in `dq/codebook.py`; this file adds the coding rules.

## Coding rules

- **Unit.** One sentence: an interrogative everywhere, plus a prefiltered diagnostic statement on GitHub.
- **Codes per unit.** Assign one or more codes (usually 1–2), following the evidence the sentence asks for (questions) or asserts (statements). Use NA when the sentence is not about the memory/resource diagnosis.
- **Code the evidence, not the topic.** "Should I free the string returned by getenv?" is A2 (API allocation contract), not D1.
- **Non-diagnostic codes** (G, T1, P, K, NA) are kept for completeness but excluded from all diagnostic frequency tables.
- **Theme (off-CWE pass only).** One theme per unit, from the list below. Use IN when the unit belongs to one of the seven target CWEs and NA when it is not relevant.

## Diagnostic questions

| Code | Dimension | Question | Include when | Boundary / exclude |
| --- | --- | --- | --- | --- |
| V1 | Report interpretation | Is the suspected leak/invalid free real, or a false positive / benign report? | Overall verdict on whether a report or snippet is a genuine leak/invalid free, incl. false-positive and 'is this bad?' questions. | Asks what a tool category means -> R2. Asks whose code is at fault -> R3. |
| R2 | Report interpretation | What does the tool's report category or runtime error mean (definitely/indirectly/possibly lost, still reachable, suppressed, invalid pointer)? | Meaning of a tool category or runtime message: definitely/indirectly/possibly lost, still reachable, suppressed, 'free(): invalid pointer', 'corrupted top size', 'fasttop'. | A verdict on this specific case -> also V1. |
| R3 | Report interpretation | Is the report caused by my code, or by a library, runtime, or the tool itself? | Attribution: my code vs. library, runtime, driver, or the tool itself; includes 'does it grow if I call the library more?'. | Global cleanup at exit with no attribution question -> L1. |
| R4 | Report interpretation | Where was the block allocated / where does the leak or bad free originate? | Locating the origin: allocation stack, which line, getting more detail from the tool. | How to run/configure the tool in general -> R5. |
| R5 | Report interpretation | How do I detect, configure, or suppress this with the tool? | Tooling: how to detect, configure, suppress, or which tool to use. | Not counted as program evidence; kept to separate tool literacy from diagnosis. |
| A1 | Allocation | Is this memory on the heap at all (vs. stack, static, string literal)? | Storage class: heap vs stack/static/string literal/read-only; deleting stack objects; freeing literals. | Pointer offset within a heap block -> D2. |
| A2 | Allocation | Does this function/API allocate what it returns (must the caller free it)? | API allocation contract: does a function (getenv, strdup, strtok, library calls) return memory the caller must free? | General caller/callee responsibility without an API -> O1. |
| A3 | Allocation | Which allocator family produced this pointer (malloc/new/new[]/custom/library)? | Allocator family / which allocator (malloc vs new vs new[] vs custom/operator new override). | Whether the deallocator matches -> D3. |
| A4 | Allocation | Is the allocation size bounded and validated (untrusted input, overflow, huge/negative size, failure)? | Allocation size bound/validity: huge, negative, overflowed, untrusted sizes; allocation failure (NULL / bad_alloc). | Growth over time -> L3. |
| O1 | Ownership | Who is responsible for releasing this memory (caller vs. callee contract)? | Who releases: caller vs callee, owner of a returned pointer, ownership contract. | Ownership moved into a container/smart pointer/library -> O2. |
| O2 | Ownership | Was ownership transferred (to a container, smart pointer, library, or object), so someone else releases it? | Ownership transfer to container, smart pointer, library object, BSTR, numpy array; stealing vs borrowed references. | Refcount imbalance itself -> N2. |
| D1 | Deallocation | Is there a matching release for this allocation, and where should it go? | Existence/placement of the release: 'do I need to free this?', 'where should free go?', missing free. | Release missing only on error/exception paths -> C1; per-iteration -> C2. |
| D2 | Deallocation | Is the pointer passed to free exactly the one the allocator returned (not offset/advanced)? | Pointer identity at free: incremented/advanced/offset pointer, keeping the original pointer. | Pointer to non-heap memory -> A1. |
| D3 | Deallocation | Is the deallocator the right one for the allocator (free vs delete vs delete[] vs library free)? | Deallocator matches allocator: free/delete/delete[], placement new, library-specific free, mismatch warnings. | Different module heaps -> X1. |
| D4 | Deallocation | Is the pointer valid to free right now (initialized, not already freed, not dangling)? | Validity at free time: uninitialized, already freed (double free), dangling, NULL-setting after free. | Access (not free) after release -> D5. |
| C1 | Control flow | Is the memory released on every path: error handling, early return, exceptions, longjmp? | Release on all paths: error handling, early return, exceptions (incl. constructors), longjmp, failed close(). | Loop/realloc-specific -> C2. |
| C2 | Control flow | Is the old block released on each loop iteration / reallocation (realloc failure, reassignment in a loop)? | Per-iteration/reallocation release: realloc failure losing the original pointer, malloc in a loop, reassignment in loops. | Reassignment outside a loop -> E1. |
| L1 | Lifetime | Must the memory be freed before program exit, or is exit-time retention acceptable? | Exit-time policy: must memory/resources be freed before exit; does the OS reclaim; singletons/globals at shutdown. | Reachability class meaning -> R2. |
| L2 | Lifetime | Is the object destroyed when its lifetime ends (scope exit, destructor called, virtual destructor)? | Object lifetime end: scope exit, destructor called or not, virtual destructor, union members, placement-new destruction. | Destructor body incomplete -> N3. |
| L3 | Lifetime | Does memory keep growing with repetitions (retained longer than needed, unbounded growth)? | Growth with repetition: memory/handles grow per call/cycle/frame; unbounded retention while reachable. | Allocator retention rather than live data -> R6. |
| L4 | Lifetime | Are threads joined/detached so that their resources are released? | Thread lifetime: join/detach, pthread_exit vs return, teardown races with worker threads. |  |
| E1 | Escape / aliasing | Was the last reference overwritten or lost before release? | Lost last reference: pointer overwritten/reassigned before release. | Inside a realloc/loop pattern -> also C2. |
| E2 | Escape / aliasing | Does the pointer escape (global, struct field, return value) so it must be released elsewhere? | Escape: stored in a global/field/container or returned, so release must happen elsewhere. |  |
| E3 | Escape / aliasing | Do other aliases or copies refer to the same block (shallow copy, copy ctor, two owners)? | Aliasing/copies: shallow copies, copy constructor/assignment (rule of three), two pointers to one block. |  |
| N1 | Composite cleanup | Are nested sub-allocations released (struct members, list nodes, 2-D arrays) before/with the parent? | Nested sub-allocations: struct members, list nodes, 2-D arrays, freeing parent vs children. |  |
| N2 | Composite cleanup | Is a reference cycle or refcount imbalance preventing release? | Reference cycles / refcount imbalance: shared_ptr cycles, weak_ptr, Py_INCREF/DECREF, COM AddRef/Release, kernel refcounts. |  |
| N3 | Composite cleanup | Does the cleanup routine / destructor release every resource the object owns? | Completeness of a cleanup routine/destructor: does it release every owned resource. |  |
| X1 | Cross-module | Are allocation and release done by the same module/runtime heap (DLL, CRT, FFI boundary)? | Cross-module heaps: DLL/CRT boundaries, FFI (ctypes, JNI, cgo), mixed runtimes. |  |
| G | Non-diagnostic | Generic: why does this leak/crash? (no specific evidence asked) | Generic root-cause request naming no specific evidence ('why does this leak?', 'how do I fix it?'). | Non-diagnostic. |
| T1 | Non-diagnostic | Triage: reproducer, full trace, version, build flags | Triage: reproducer, full trace, version, build flags. | Non-diagnostic. |
| P | Non-diagnostic | Prevention / best-practice advice | Prevention/best-practice advice (smart pointers, avoid new). | Non-diagnostic. |
| K | Non-diagnostic | Allocator internals (how free knows the size, etc.) | Allocator internals (how free knows the size, free lists). | Non-diagnostic. |
| RK | Resource kind | What kind of resource is held (memory, fd, socket, handle, JNI ref, GPU object, thread), and which call releases it? | Resource kind and releaser: fd, socket, handle, JNI local ref, cgo handle, GPU buffer, thread, mempool — and the call that releases it. | Added in the off-CWE pass. |
| R6 | Report interpretation | Is the growth in RSS / task-manager memory leaked memory, or freed memory the allocator has not returned (fragmentation, arenas, caches)? | Is RSS/task-manager growth leaked memory or freed memory the allocator keeps (arenas, fragmentation, caches, malloc_trim). | Added in the off-CWE pass. |
| D5 | Deallocation | Is the block accessed after it was released (use after free, dangling reference)? | Use after release: access through a dangling pointer/handle after free/delete/teardown. | Added in the off-CWE pass. |
| H1 | Deallocation | Was the heap already corrupted before the failing free/malloc (earlier overflow)? | Prior heap corruption: the crash in free/malloc is caused by an earlier overflow. | Added in the off-CWE pass. |
| NA | Non-diagnostic | Not relevant | Off-topic, rhetorical, meta (downvotes), or raw tool output. | |

## Themes (off-CWE pass)

| Code | Meaning |
| --- | --- |
| RES | Non-memory resource leak (fd, socket, handle, cgo/JNI handle) ~ CWE-772/775 |
| THR | Thread / process lifetime ~ CWE-404 |
| GRW | Growth without a classic leak (allocator retention, fragmentation, caches) ~ CWE-400/770 |
| REF | Reference counting in bindings / COM / kernel ~ CWE-911 |
| GPU | GPU / graphics memory |
| KER | Kernel memory (kmemleak) |
| POOL | Memory pools, arenas, custom allocators |
| DF | Double free ~ CWE-415 |
| UAF | Use after free / dangling ~ CWE-416 |
| HC | Heap corruption surfacing at free/malloc ~ CWE-122/787 |
| UNI | Uninitialised memory in leak reports ~ CWE-457/908 |
| LIB | Library / runtime global cleanup |
| INFO | 'Leak' meaning information disclosure ~ CWE-200 |
| IN | Inside the seven target CWEs |
| NA | Not relevant |
