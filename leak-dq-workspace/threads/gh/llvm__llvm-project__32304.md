# Mismatched free vs. operator delete

- URL: https://github.com/llvm/llvm-project/issues/32304
- Repo: llvm/llvm-project (language: LLVM)
- State: open; created 2017-05-07T16:14:03Z; status ok; passes main

## Issue body

reporter (MEMBER) · llvmbot · 2017-05-07T16:14:03Z · https://github.com/llvm/llvm-project/issues/32304

|  |  |
| --- | --- |
| Bugzilla Link | [32957](https://llvm.org/bz32957) |
| Version | 3.9 |
| OS | Linux |
| Reporter | LLVM Bugzilla Contributor |

## Extended Description 
When using LD_PRELOAD=/usr/lib64/libasan.so.4.0.0 (to find bugs in my application), Clang gives

> ==6733==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete) on 0x603000002500
>     #&#8203;0 0x7f606d12dfd0 in operator delete(void*) (/usr/lib64/libasan.so.4.0.0+0xe0fd0)
>     #&#8203;1 0x55ee0b851833 in main (/usr/bin/clang-3.9+0xa833)
>     #&#8203;2 0x7f6067be55fd in __libc_start_main (/lib64/libc.so.6+0x205fd)
>     #&#8203;3 0x55ee0b853db9 in _start (/usr/bin/clang-3.9+0xcdb9)
> 
> 0x603000002500 is located 0 bytes inside of 31-byte region [0x603000002500,0x60300000251f)
> allocated by thread T0 here:
>     #&#8203;0 0x7f606d12b850 in malloc (/usr/lib64/libasan.so.4.0.0+0xde850)
>     #&#8203;1 0x7f606c059ae7 in operator new(unsigned long) (/lib64/libLLVM-3.9.so+0x1b90ae7)

Likely cause is that Clang overrides operator new but not operator delete.
