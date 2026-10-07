# allocator_test fails - alloc-dealloc-mismatch

- URL: https://github.com/scylladb/seastar/issues/111
- Repo: scylladb/seastar (language: C++)
- State: open; created 2016-01-23T06:04:36Z; status ok; passes main

## Issue body

reporter (NONE) · npmadhu · 2016-01-23T06:04:36Z · https://github.com/scylladb/seastar/issues/111

allocator_test fails - the problem is that new uses posix_memalign to allocate - the unique_ptr uses std::delete - solution is to use a custom deleter for unique_ptr.

AddressSanitizer output
==2551==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete []) on 0x60900000d780
#0 0x7fa1424d502a in operator delete[](void*) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x9a02a)

```
#1 0x41375c in std::default_delete<char []>::operator()(char*) const (/home/seamaster/seastar/build/debug/tests/allocator_test_g+0x41375c)
#2 0x40f7d4 in std::unique_ptr<char [], std::default_delete<char []> >::~unique_ptr() (/home/seamaster/seastar/build/debug/tests/allocator_test_g+0x40f7d4)
```

fix - diff attached.
[allocator_test.txt](https://github.com/scylladb/seastar/files/101726/allocator_test.txt)

