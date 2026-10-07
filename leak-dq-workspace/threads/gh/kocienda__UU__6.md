# mismatch malloc/delete

- URL: https://github.com/kocienda/UU/issues/6
- Repo: kocienda/UU (language: C++)
- State: open; created 2022-12-30T03:29:52Z; status ok; passes main

## Issue body

reporter (NONE) · stolk · 2022-12-30T03:29:52Z · https://github.com/kocienda/UU/issues/6

valgrind reports this:
```
==360970== Mismatched free() / delete / delete []
==360970==    at 0x484B8AF: operator delete(void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==360970==    by 0x149FC2: UU::BasicString<char, std::char_traits<char>, 256ul>::~BasicString() (in /home/bram/src/iota/build/search)
==360970==    by 0x13B889: output_refs(Env const&, std::vector<UU::TextRef, std::allocator<UU::TextRef> >&) (in /home/bram/src/iota/build/search)
==360970==    by 0x13A992: main (in /home/bram/src/iota/build/search)
==360970==  Address 0x51d4040 is 0 bytes inside a block of size 2,097,152 alloc'd
==360970==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==360970==    by 0x14923B: UU::BasicString<char, std::char_traits<char>, 256ul>::ensure_capacity(unsigned long) (in /home/bram/src/iota/build/search)
==360970==    by 0x1745D9: UU::BasicString<char, std::char_traits<char>, 256ul>::BasicString(unsigned long) (in /home/bram/src/iota/build/search)
==360970==    by 0x13B3DA: output_refs(Env const&, std::vector<UU::TextRef, std::allocator<UU::TextRef> >&) (in /home/bram/src/iota/build/search)
==360970==    by 0x13A992: main (in /home/bram/src/iota/build/search)
```

The code allocated with `malloc()` and frees with `delete`.

