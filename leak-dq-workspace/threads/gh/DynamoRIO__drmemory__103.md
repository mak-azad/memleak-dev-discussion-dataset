# UNINIT parser: many, many (false?) positives

- URL: https://github.com/DynamoRIO/drmemory/issues/103
- Repo: DynamoRIO/drmemory (language: C)
- State: open; created 2014-11-28T02:21:59Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · derekbruening · 2014-11-28T02:21:59Z · https://github.com/DynamoRIO/drmemory/issues/103

_From [derek.br...@gmail.com](https://code.google.com/u/117968039472581148324/) on December 10, 2010 17:57:37_

PR 406720

parser on linux has a ton of (false?) positives

all libc ones are strrchr or strlen, now gone via PR 406535, but the parser executable ones remain:

22:09|glaurung:/work/dr/tot/internal/benchmarks/spec2000/int/parser/release-glaurung.localdomain-test/DrMemory-parser.0  
> grep UNIN _t_ | sort -n | uniq -c  
  11833 UNINITIALIZED READ: 0x0041cd11 reading register eax  
  70380 UNINITIALIZED READ: 0x004663bc reading register eflags  
  19778 UNINITIALIZED READ: 0x004663c7 reading register eflags  
  14032 UNINITIALIZED READ: 0x004663d3 reading register eflags  
   4988 UNINITIALIZED READ: 0x004663de reading register eflags
   1533 UNINITIALIZED READ: 0x004663ea reading register eflags
    860 UNINITIALIZED READ: 0x004663f5 reading register eflags
    211 UNINITIALIZED READ: 0x00466401 reading register eflags
      9 UNINITIALIZED READ: 0x0046640c reading register eflags
 120623 UNINITIALIZED READ: 0x004668ac reading register eflags
  19561 UNINITIALIZED READ: 0x004668bb reading register eflags
  11345 UNINITIALIZED READ: 0x004668e1 reading register eflags
   4298 UNINITIALIZED READ: 0x004668f0 reading register eflags
   5565 UNINITIALIZED READ: 0x0046691e reading register eflags
    586 UNINITIALIZED READ: 0x00466929 reading register eflags
    748 UNINITIALIZED READ: 0x00466953 reading register eflags
      5 UNINITIALIZED READ: 0x0046695e reading register eflags
  81958 UNINITIALIZED READ: 0x004669a4 reading register dl
 153143 UNINITIALIZED READ: 0x0805711d reading register eax
   2409 UNINITIALIZED READ: 0x08057686 reading register esi
   5142 UNINITIALIZED READ: 0x080582cc reading register ebx
   1428 UNINITIALIZED READ: 0x0805832c reading register ecx
   1289 UNINITIALIZED READ: 0x0805838c reading register eax
    478 UNINITIALIZED READ: 0x080583e1 reading register esi
   1191 UNINITIALIZED READ: 0x080586da reading register eax
     46 UNINITIALIZED READ: 0x08058732 reading register ebx
    159 UNINITIALIZED READ: 0x080587ef reading register ebx
    281 UNINITIALIZED READ: 0x08058844 reading register eax
     15 UNINITIALIZED READ: 0x0805a24a reading register al
    647 UNINITIALIZED READ: 0x0805aa29 reading register al
   5068 UNINITIALIZED READ: 0x0805acdc reading register al
   5042 UNINITIALIZED READ: 0x0805afd1 reading register al
   1629 UNINITIALIZED READ: 0x0805c2b3 reading register al
    239 UNINITIALIZED READ: 0x0805c42a reading register al
  91350 UNINITIALIZED READ: 0x0805effa reading register cx
 186472 UNINITIALIZED READ: 0x080610b8 reading register eax
 364640 UNINITIALIZED READ: 0x08061167 reading register esi
 186471 UNINITIALIZED READ: 0x08061245 reading register ebx
 124647 UNINITIALIZED READ: 0x08061308 reading register eax
 201500 UNINITIALIZED READ: 0x080613be reading register eax
 124647 UNINITIALIZED READ: 0x08061453 reading register ebx
 341339 UNINITIALIZED READ: 0x0806166f reading register esi
 151742 UNINITIALIZED READ: 0x08061749 reading register ebx

even with -no_fastpath still hit them:
> grep UN _t_
UNINITIALIZED READ: 0x0805acdc reading register al
UNINITIALIZED READ: 0x0805afd1 reading register al
UNINITIALIZED READ: 0x0805c2b3 reading register al
UNINITIALIZED READ: 0x0805c2b3 reading register al

first one:
(gdb) info line *0x0805acdc
Line 179 of "src/post-process.c" starts at address 0x805acd7 and ends at 0x805ace2 .

Valgrind sees it too (complains at je instead of test) (not sure why
symbols different but line # and address are same):
==5178== Conditional jump or move depends on uninitialised value(s)
==5178==    at 0x805ACDE: build_domains (post-process.c:179)
==5178==    by 0x805CBCA: post_process (post-process.c:985)
==5178==    by 0x804A8A8: analyze_thin_linkage (analyze-linkage.c:759)
==5178==    by 0x80556AF: batch_process (main.c:1615)
==5178==    by 0x8055CF0: main (main.c:1842)

but Valgrind only shows 13499 errors: just artifact of how it marks defined
afterward?  aren't we doing that similarly?

wasn't looking at the latest runs: our count of 13510 is pretty close to valgrind's 13499,
so most if not all of these are real positives

:::Dr.Memory::: ERRORS FOUND:
:::Dr.Memory:::      16 unaddressable access(es)
:::Dr.Memory:::   13510 uninitialized access(es)
:::Dr.Memory:::    4635 invalid free(s)
:::Dr.Memory:::       2 leak(s)

_Original issue: http://code.google.com/p/drmemory/issues/detail?id=103_

