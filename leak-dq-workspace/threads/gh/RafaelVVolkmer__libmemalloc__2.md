# Valgrind Reports Memory Leak on GC Stack Scanning

- URL: https://github.com/RafaelVVolkmer/libmemalloc/issues/2
- Repo: RafaelVVolkmer/libmemalloc (language: None)
- State: open; created 2025-08-23T22:54:58Z; status ok; passes main

## Issue body

reporter (OWNER) · RafaelVVolkmer · 2025-08-23T22:54:58Z · https://github.com/RafaelVVolkmer/libmemalloc/issues/2

## Description

When running applications that use the `libmemalloc` **Garbage Collector (GC)** under **Valgrind**, the tool consistently reports **memory leaks** and **invalid memory access warnings**.

This happens because the GC attempts to **scan the stack of a running thread** while executing inside the GC’s own thread.  
Valgrind interprets this as accessing **invalid or out-of-bounds memory regions**, since the GC is walking through another thread’s stack frame without proper suspension.

---

## Steps to Reproduce

1. Build any multithreaded application with `libmemalloc` GC enabled.  
2. Run the application with Valgrind:
3. Observe Valgrind logs, which typically include:
- "Invalid read of size X"
- Memory leak reports even though GC should have reclaimed memory

---

## Root Cause

- The GC does not suspend other threads before scanning their stacks.
- As a result, it tries to traverse the memory of a live stack from another thread.
- Valgrind correctly flags this as an invalid memory access and a potential memory leak.

---

##  Expected Behavior

1. The GC should safely scan memory without causing Valgrind to detect invalid access.
2. hread stacks must only be scanned if:
3. They are safely suspended, or The scan is performed by the owning thread.

---

##  Impact

High —  Developers running apps with Valgrind may see false positives that obscure real issues.
High —  Risk of unsafe memory accesses in multithreaded environments if the GC continues scanning live stacks.
Low — Reduces trust in the GC’s correctness when analyzed with Valgrind.

---

##Environment

- `Libmemalloc version:` latest
- `Platform:` Linux (tested with Valgrind 3.21.0)
- `Application type:` multithreaded app using GC

---

 _Reported by [Rafael V. Volkmer](mailto:rafael.v.volkmer@gmail.com)_

