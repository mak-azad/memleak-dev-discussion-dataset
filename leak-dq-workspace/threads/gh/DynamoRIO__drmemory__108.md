# UNINIT gcc: many false positives

- URL: https://github.com/DynamoRIO/drmemory/issues/108
- Repo: DynamoRIO/drmemory (language: C)
- State: open; created 2014-11-28T02:22:05Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · derekbruening · 2014-11-28T02:22:05Z · https://github.com/DynamoRIO/drmemory/issues/108

_From [derek.br...@gmail.com](https://code.google.com/u/117968039472581148324/) on December 10, 2010 17:57:39_

PR 408123

After fixing PR 406714 gcc test now runs but we have many more errors than Valgrind finds.
One possibility is that like cygwin windows apps bitlevel precision may be needed to
avoid false positives, not just false negatives, as gcc uses a lot of structs with
bitfields.

Valgrind: ERROR SUMMARY: 29 errors from 1 contexts (suppressed: 17 from 1)

vs

:::Dr.Memory::: ERRORS FOUND:
:::Dr.Memory:::      30 unaddressable access(es)
:::Dr.Memory:::    4227 uninitialized access(es)
:::Dr.Memory:::    4761 invalid free(s)
:::Dr.Memory:::    1121 leak(s)
:::Dr.Memory:::          (re-run with -check_leaks for details)
:::Dr.Memory::: ERRORS IGNORED:
:::Dr.Memory:::       0 ignored pre-app leak(s)
:::Dr.Memory:::       0 suppressed error(s)
:::Dr.Memory:::       0 suppressed leak(s)
:::Dr.Memory:::       9 possible leak(s)
:::Dr.Memory:::       0 error(s) beyond -report_max
> grep INVAL _t_ | sort | uniq -c
   4761 INVALID FREE: 0x00000000
> grep -A 1 UNINIT _t_  | grep -vE 'UNINIT|--' | sort | uniq -c | sort -n
      2   0x0046640c  74 a2                jz     $0x004663b0
      5   0x0814fbc1  83 bd 38 fa ff ff 1e cmp    0xfffffa38(&#37;ebp) $0x0000001e
 (v) 15   0x08114309  f6 46 30 03          test   0x30(&#37;esi) $0x03
     22   0x0046582c  f6 47 28 01          test   0x28(&#37;edi) $0x01
     33   0x08119cfd  f6 47 30 08          test   0x30(&#37;edi) $0x08
     35   0x08114b20  f6 46 30 10          test   0x30(&#37;esi) $0x10
     49   0x0811536c  f6 46 30 01          test   0x30(&#37;esi) $0x01
     69   0x00465a9b  f6 46 28 01          test   0x28(&#37;esi) $0x01
     69   0x0811f35c  0f 85 1f 03 00 00    jnz    $0x0811f681
     69   0x0811f365  85 c0                test   &#37;eax &#37;eax
     74   0x0811f26c  0f 85 1b 04 00 00    jnz    $0x0811f68d
     74   0x0811f275  85 c0                test   &#37;eax &#37;eax
     79   0x0811f18c  0f 85 f5 03 00 00    jnz    $0x0811f587
     79   0x0811f195  85 c0                test   &#37;eax &#37;eax
     82   0x0811c2f4  f6 41 30 08          test   0x30(&#37;ecx) $0x08
    161   0x08116b26  f6 42 1c 08          test   0x1c(&#37;edx) $0x08
    367   0x08114aec  a8 20                test   &#37;al $0x20
    404   0x081140bc  f6 43 2c 01          test   0x2c(&#37;ebx) $0x01
    947   0x08116afd  f6 41 1c 18          test   0x1c(&#37;ecx) $0x18
   1592   0x0804fc19  39 9d d8 fe ff ff    cmp    0xfffffed8(&#37;ebp) &#37;ebx

_Original issue: http://code.google.com/p/drmemory/issues/detail?id=108_

