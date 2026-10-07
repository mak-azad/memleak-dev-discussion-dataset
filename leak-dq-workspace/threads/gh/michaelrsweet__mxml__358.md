# Heap use-after-free in `mxml_load_data()` error cleanup (double deletion of an already-freed descendant)

- URL: https://github.com/michaelrsweet/mxml/issues/358
- Repo: michaelrsweet/mxml (language: C)
- State: open; created 2026-09-27T14:46:04Z; status ok; passes offcwe

## Issue body

reporter (NONE) · suywang · 2026-09-27T14:46:04Z · https://github.com/michaelrsweet/mxml/issues/358

## Summary

The common `error:` epilogue of `mxml_load_data()` deletes two nodes without first checking whether the first delete already released the second one. `mxmlDelete()` is recursive, so when `first` is a descendant of `node`, the `mxmlDelete(node)` call frees `first` on the way, and the following `mxmlDelete(first)` then dereferences freed memory.

## Affected versions
v4.0.5 and v4.0.6
This is caused by the fix introduced for issue #354 

## Root cause

`mxml-file.c`, at the end of `mxml_load_data()`:

```c
1454:  // Common error return...
1455:  error:
1456:
1457:  if (node && node != first)
1458:    mxmlDelete(node);
1459:
1460:  mxmlDelete(first);
1461:
1462:  free(buffer);
1463:
1464:  return (NULL);
```

The guard tests `node != first` only. It does not test whether `first` is a
*descendant* of `node`.

And `mxmlDelete()` is recursive — `mxml-node.c`:

```c
136:  mxmlRemove(node);
137:
138:  // Delete children...
139:  for (current = node->child; current; current = next)
140:  {
...
156:    // Free child...
157:    mxml_free(current);
158:  }
159:
160:  // Then free the memory used by the parent node...
161:  mxml_free(node);
```

`node` becomes an ancestor of `first` on the ordinary close-tag path — `mxml-file.c`:

```c
1299:        node   = parent;
1300:        parent = parent->parent;
```

after which a second root node reaches the epilogue with `node` still pointing at that ancestor. So `mxmlDelete(node)` at :1458 releases `first` as part of the subtree, and `mxmlDelete(first)` at :1460 re-enters `mxmlDelete()` on a dangling pointer. It dereferences it immediately, in `mxmlRemove()` — `mxml-node.c`:

```c
751: void
752: mxmlRemove(mxml_node_t *node)
753: {
...
756:   // Range check input...
757:   if (!node || !node->parent)
```

which is exactly where AddressSanitizer reports the read. The second `mxml_free()` on that address is never reached, so this is a use-after-free caused by a double deletion rather than two `free()` calls on one pointer.

The same delete also frees the caller's `top`:

`mxml_load_data()` uses the caller's node as its initial parent:

```c
844:  parent     = top;
845:  first      = NULL;
```

In this scenario the close-tag branch has already set `node = parent` (`:1299`), so the `node` that `mxmlDelete(node)` deletes at `:1458` *is* the caller's `top`. Nothing in the error path distinguishes a node mxml allocated from the node the caller passed in, so the caller's node is freed along with everything else.

That makes a second use-after-free, this one landing in the caller: after a **failed** load `top` is dangling, while after a successful one it is still the caller's. `mxmlLoadString()` returns NULL, and the caller's own `mxmlDelete(top)` then operates on freed memory. 

`testmxml.c` builds a node, loads into it, and deletes it at the end:

```c
 84:  tree    = mxmlNewElement(xml, "element");
...
111:  mxmlOptionsSetTypeValue(options, MXML_TYPE_TEXT);
112:  mxmlLoadString(tree, options, "<group type='string'>string string string</group>");
```

That is the documented pattern, and it only stays safe today because every document in the test is well formed. Feed the test a malformed one and the cleanup at the end of `main()` operates on freed memory.

## Reproduction

Ubuntu 20.04

AddressSanitizer
```bash
./mxml_double_free_asan poc_mxml_load_data_double_free.xml
```

same without the sanitizer flags
```bash
/mxml_double_free_plain poc_mxml_load_data_double_free.xml
```

Please refer to the attached package for specific compilation commands.

## PoC

[poc_mxml_error_handling.tar.gz](https://github.com/user-attachments/files/32701825/poc_mxml_error_handling.tar.gz)

## Error Log

AddressSanitizer
```
==2063569==ERROR: AddressSanitizer: heap-use-after-free on address 0x6080000000b8 at pc 0x00000040c071 bp 0x7ffc56d93cc0 sp 0x7ffc56d93cb0
READ of size 8 at 0x6080000000b8 thread T0
    #0 0x40c070 in mxmlRemove /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:757
    #1 0x40d6c5 in mxmlDelete /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:136
    #2 0x405b16 in mxml_load_data /home/autoresearch/advtaint/0day/repos/mxml/mxml-file.c:1460
    #3 0x409ef9 in mxmlLoadString /home/autoresearch/advtaint/0day/repos/mxml/mxml-file.c:239
    #4 0x40282e in main /tmp/opencode/triage/verify/v_mxml.c:10
    #5 0x70632ae68082 in __libc_start_main ../csu/libc-start.c:308
    #6 0x40273d in _start (/tmp/opencode/triage/verify/v_mxml+0x40273d)

0x6080000000b8 is located 24 bytes inside of 88-byte region [0x6080000000a0,0x6080000000f8)
freed by thread T0 here:
    #0 0x70632b16640f in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:122
    #1 0x40bcd0 in mxml_free /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:913
    #2 0x40d794 in mxmlDelete /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:157
    #3 0x405b0a in mxml_load_data /home/autoresearch/advtaint/0day/repos/mxml/mxml-file.c:1458
    #4 0x409ef9 in mxmlLoadString /home/autoresearch/advtaint/0day/repos/mxml/mxml-file.c:239
    #5 0x40282e in main /tmp/opencode/triage/verify/v_mxml.c:10
    #6 0x70632ae68082 in __libc_start_main ../csu/libc-start.c:308

previously allocated by thread T0 here:
    #0 0x70632b166a06 in __interceptor_calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:153
    #1 0x40c463 in mxml_new /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:931
    #2 0x40d37a in mxmlNewText /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:692
    #3 0x405066 in mxml_load_data /home/autoresearch/advtaint/0day/repos/mxml/mxml-file.c:895
    #4 0x409ef9 in mxmlLoadString /home/autoresearch/advtaint/0day/repos/mxml/mxml-file.c:239
    #5 0x40282e in main /tmp/opencode/triage/verify/v_mxml.c:10
    #6 0x70632ae68082 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: heap-use-after-free /home/autoresearch/advtaint/0day/repos/mxml/mxml-node.c:757 in mxmlRemove
Shadow bytes around the buggy address:
  0x0c107fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c107fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c107fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c107fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c107fff8000: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa
=>0x0c107fff8010: fa fa fa fa fd fd fd[fd]fd fd fd fd fd fd fd fa
  0x0c107fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c107fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c107fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c107fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c107fff8060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==2063569==ABORTING
```

same without the sanitizer flags
```
[harness] input: "x</x><y>" (8 bytes)
[harness] calling mxmlLoadString(top=0x5690a59db510, options=0x5690a59db480)
<y> cannot be a second root node after <(null)> on line 1.
[harness] mxmlLoadString returned (nil)
[harness] (reached only if no memory error was detected)
Segmentation fault (core dumped)
```

## Impact

This is heap corruption with a reliable crash.  Whether it can be pushed further depends on the allocator and the surrounding heap state.


## CWE

CWE-416 Use After Free


## Comment 5892601868

maintainer (OWNER) · michaelrsweet · 2026-09-29T14:45:04Z · https://github.com/michaelrsweet/mxml/issues/358#issuecomment-5892601868

Seems like the solution here is to bump the reference count for the "first" node so that it isn't immediately deleted.

## Comment 5902775187

reporter (NONE) · suywang · 2026-09-30T02:18:28Z · https://github.com/michaelrsweet/mxml/issues/358#issuecomment-5902775187

Thanks for looking into this. I dug in a bit more and have a patch against v4.0.6 (attached for reference).

I confirmed that simply retaining first does not prevent the UAF: mxmlDelete(node) still recursively frees first, and the same ASan heap-use-after-free is reported.

The approach I tested is to make first consistently represent the first node added by the current load operation: it is assigned immediately after each successful node creation, and cleared when a SAX callback releases that node. The error path then deletes only the nodes added by this load, rather than using the current node cursor for cleanup.

This fixes both cases I was seeing:

the #354 malformed-input leak does not come back;
the #358 UAF is gone, including the case where node has become the caller-supplied top.

I also added regression coverage for malformed input, caller-provided top, and SAX callbacks. The new tests fail on v4.0.6 (ASan reports the UAF) and pass with the patch; the full test suite passes with ASan on Linux (also checked with UBSan).

One behavior change worth noting: when loading into a caller-provided top, a failed load now removes the nodes added by that load, instead of leaving partial siblings attached to top.

Happy to adjust the patch if you'd prefer a different approach. 

[mxml-fix-354-358.patch](https://github.com/user-attachments/files/32836547/mxml-fix-354-358.patch)
