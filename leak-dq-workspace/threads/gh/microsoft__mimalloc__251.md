# mimalloc override + valgrind

- URL: https://github.com/microsoft/mimalloc/issues/251
- Repo: microsoft/mimalloc (language: C)
- State: open; created 2020-05-23T20:35:38Z; status ok; passes main

## Issue body

reporter (NONE) · christoph-cullmann · 2020-05-23T20:35:38Z · https://github.com/microsoft/mimalloc/issues/251

Hi,

if you use valgrind for debugging (which is often very useful), this works ok with mimalloc and override beside that for the free's (if you use C++), you will get a lot of warnings about mismatching delete/delete[]/free usage.

Example: 

==171393== Mismatched free() / delete / delete []
==171393==    at 0x483A9AB: free (vg_replace_malloc.c:540)
==171393==    by 0x317E26: Ur::MessageHandler::~MessageHandler() (in /home/cullmann/projects/build/libur.default.release/libur/test/test_gcallocator_exe)
==171393==    by 0x2FF2FC: Ur::StaticInitializer::~StaticInitializer() (in /home/cullmann/projects/build/libur.default.release/libur/test/test_gcallocator_exe)
==171393==    by 0x4A53536: __run_exit_handlers (in /usr/lib/libc-2.31.so)
==171393==    by 0x4A536ED: exit (in /usr/lib/libc-2.31.so)
==171393==    by 0x4A3C029: (below main) (in /usr/lib/libc-2.31.so)
==171393==  Address 0x4be0420 is 0 bytes inside a block of size 64 alloc'd
==171393==    at 0x483A50F: operator new[](unsigned long) (vg_replace_malloc.c:433)
==171393==    by 0x3174D6: Ur::MessageHandler::MessageHandler() (in /home/cullmann/projects/build/libur.default.release/libur/test/test_gcallocator_exe)
==171393==    by 0x2FF170: Ur::StaticInitializer::StaticInitializer() (in /home/cullmann/projects/build/libur.default.release/libur/test/test_gcallocator_exe)
==171393==    by 0x2C4CFD: _GLOBAL__sub_I_test_gcallocator.cpp (in /home/cullmann/projects/build/libur.default.release/libur/test/test_gcallocator_exe)
==171393==    by 0x48189C: __libc_csu_init (in /home/cullmann/projects/build/libur.default.release/libur/test/test_gcallocator_exe)
==171393==    by 0x4A3BFAF: (below main) (in /usr/lib/libc-2.31.so)

This can be avoided, if one doesn't redirect directly but still do an extra call inside the overriding by enforcing to use the

#define MI_FORWARD1(fun,x)      { return fun(x); }

variant of forwarding.

Would it be possible to have this as a cmake option? I can patch that file to always use this variant, but I assume other people will stumble over this sooner or later, too.

(or is there some more appropriate way to handle this?)

## Comment 648272497

other (NONE) · hp48gx · 2020-06-23T16:26:12Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-648272497

I just tried to modify alloc-override.c and define the redirection as an extra call.
However we have segfaults: we have a binary statically linked to mimalloc.o and dynamically linked to another library (HyperScan). it seems that calls to 'free' from the main binary are correctly dispatched to mimalloc, but calls from the .so are not: they still invoke libC (and segfault, obviously)

#4  <signal handler called>
#5  0x00000035c803aa1f in **free () from /lib/libc.so.7**
#6  0x00000035bca041f3 in ?? () from /usr/local/lib/libhs.so.4
#7  0x00000035bc9f9d38 in ?? () from /usr/local/lib/libhs.so.4
#8  0x00000035bca24c33 in ?? () from /usr/local/lib/libhs.so.4
#9  0x00000035bc8077c6 in ?? () from /usr/local/lib/libhs.so.4
#10 0x00000035bc803967 in ?? () from /usr/local/lib/libhs.so.4
#11 0x00000035bc803d01 in hs_compile_multi () from /usr/local/lib/libhs.so.4

## Comment 652907565

other (NONE) · hp48gx · 2020-07-02T09:49:18Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-652907565

I'm interested too in making valgrind and mimalloc work together.
In some tests, we noticed this, which we cannot explain:

[18:01:40] :	 [Step 2/2] -- Valgrind Check: cpp-tests ... ==13792== Memcheck, a memory error detector
[18:01:40] :	 [Step 2/2] ==13792== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
[18:01:40] :	 [Step 2/2] ==13792== Using Valgrind-3.14.0 and LibVEX; rerun with -h for copyright info
...
[18:01:40] :	 [Step 2/2] ==13792== Invalid free() / delete / delete[] / realloc()
[18:01:40] :	 [Step 2/2] ==13792==    at 0x48369AB: free (vg_replace_malloc.c:530)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5F56629: check_free (dlerror.c:202)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5F56629: check_free (dlerror.c:186)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5F56AB1: free_key_mem (dlerror.c:221)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5F56AB1: __dlerror_main_freeres (dlerror.c:239)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5EFCB71: __libc_freeres (in /lib/x86_64-linux-gnu/libc-2.28.so)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x482D19E: _vgnU_freeres (vg_preloaded.c:77)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5DCDE89: __run_exit_handlers (exit.c:132)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5DCDEB9: exit (exit.c:139)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5DB80A1: (below main) (libc-start.c:342)
[18:01:40] :	 [Step 2/2] ==13792==  Address 0x12358a0 is 0 bytes inside data symbol "_mi_page_empty"
[18:01:40] :	 [Step 2/2] ==13792== 
[18:01:40] :	 [Step 2/2] ==13792== Invalid free() / delete / delete[] / realloc()
[18:01:40] :	 [Step 2/2] ==13792==    at 0x48369AB: free (vg_replace_malloc.c:530)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5F56AB9: free_key_mem (dlerror.c:223)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5F56AB9: __dlerror_main_freeres (dlerror.c:239)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5EFCB71: __libc_freeres (in /lib/x86_64-linux-gnu/libc-2.28.so)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x482D19E: _vgnU_freeres (vg_preloaded.c:77)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5DCDE89: __run_exit_handlers (exit.c:132)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5DCDEB9: exit (exit.c:139)
[18:01:40] :	 [Step 2/2] ==13792==    by 0x5DB80A1: (below main) (libc-start.c:342)
[18:01:40] :	 [Step 2/2] ==13792==  Address 0x15b79e0 is 0 bytes inside data symbol "_mi_heap_main"

Relevant source code is probably this one:
https://sources.debian.org/src/glibc/2.28-10/dlfcn/dlerror.c/

But we are not sure how to interpret the diagnostic message: Address ... is 0 bytes inside data symbol "_mi_heap_main"

## Comment 751503060

other (CONTRIBUTOR) · Qix- · 2020-12-27T18:50:17Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-751503060

For me, this is taking the form of mimalloc (as a debug build) raising an assert whilst under valgrind:

```
==8574== error calling PR_SET_PTRACER, vgdb might block
mimalloc: assertion failed: at "/src/microsoft/mimalloc/src/alloc.c":95, mi_heap_malloc
  assertion: "p == NULL || mi_usable_size(p) >= size"
==8574==
==8574== Process terminating with default action of signal 6 (SIGABRT)
==8574==    at 0x48C918B: raise (raise.c:51)
==8574==    by 0x48A8858: abort (abort.c:79)
==8574==    by 0x404425: _mi_assert_fail (options.c:337)
==8574==    by 0x40DD61: mi_heap_malloc (alloc.c:95)
==8574==    by 0x40DB3E: mi_heap_new (heap.c:194)
==8574==    by 0x41B8D8: test_allocator_heap_new (alloc.h:10)
```

## Comment 959006248

reporter (NONE) · christoph-cullmann · 2021-11-03T12:57:26Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-959006248

True, I tried again with current stable mimalloc and yes, if I run a program that overrides new/delete with the mimalloc operators inside valgrind I get faults like:

```
==1117531== Invalid read of size 1
==1117531==    at 0x413AE1: mi_free (in /local/ssd/cullmann/build/libur.default.release/libur/test/test_maprange_exe)
==1117531==    by 0x31BF73: Ur::StaticInitializer::~StaticInitializer() (in /local/ssd/cullmann/build/libur.default.release/libur/test/test_maprange_exe)
==1117531==    by 0x4A5E4A6: __run_exit_handlers (in /usr/lib/libc-2.33.so)
==1117531==    by 0x4A5E64D: exit (in /usr/lib/libc-2.33.so)
==1117531==    by 0x2F7B29: main (in /local/ssd/cullmann/build/libur.default.release/libur/test/test_maprange_exe)
==1117531==  Address 0x4800060 is not stack'd, malloc'd or (recently) free'd
==1117531== 
==1117531== 
==1117531== Process terminating with default action of signal 11 (SIGSEGV): dumping core
==1117531==  Access not within mapped region at address 0x4800060
==1117531==    at 0x413AE1: mi_free (in /local/ssd/cullmann/build/libur.default.release/libur/test/test_maprange_exe)
==1117531==    by 0x31BF73: Ur::StaticInitializer::~StaticInitializer() (in /local/ssd/cullmann/build/libur.default.release/libur/test/test_maprange_exe)
==1117531==    by 0x4A5E4A6: __run_exit_handlers (in /usr/lib/libc-2.33.so)
==1117531==    by 0x4A5E64D: exit (in /usr/lib/libc-2.33.so)
==1117531==    by 0x2F7B29: main (in /local/ssd/cullmann/build/libur.default.release/libur/test/test_maprange_exe)
==1117531==  If you believe this happened as a result of a stack
==1117531==  overflow in your program's main thread (unlikely but
==1117531==  possible), you can try to increase the size of the
==1117531==  main thread stack using the --main-stacksize= flag.
==1117531==  The main thread stack size used in this run was 18446744073709551615.
```


## Comment 959683104

maintainer (COLLABORATOR) · daanx · 2021-11-03T16:38:09Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-959683104

Hi all, apologies for not replying earlier in this thread. Valgrind (and asan) is awesome! However, these tools work by knowing about the allocator (and asan for example uses its own allocator). This kind of deep integration is needed to avoid false positives as you are seeing here.

As such, I do not think that mimalloc can work "out of the box" with Valgrind (or asan) and that more work is needed to make that happen (I guess hooking into specific api calls?). For now, I recommend not using mimalloc when using Valgrind or asan, and only using mimalloc for release/debug builds.  This is what the [Koka](http://koka-lang.org) compiler does for example.

However, it would be great if a Valgrind/asan expert could make mimalloc work natively with those tools and I would be inclined to accept such a PR :-)  


## Comment 959692517

other (CONTRIBUTOR) · Qix- · 2021-11-03T16:40:55Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-959692517

Valgrind has a very friendly group of maintainers and its own issue tracker, I'm not sure how much they spill over to Github though. It might be worth it for a maintainer of mimalloc to open an issue on their tracker and refer back to this issue for potential guidance.

## Comment 1004242799

other (CONTRIBUTOR) · tiran · 2022-01-03T17:27:41Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1004242799

Valgrind's Memcheck has [API hooks](https://valgrind.org/docs/manual/mc-manual.html#mc-manual.mempools) for custom memory allocators. The API is powerful and supports even two level memory pools. Among others Postgres' custom [memory allocator](https://github.com/postgres/postgres/blob/master/src/backend/utils/mmgr/mcxt.c) uses the Valgrind API. It is also quiet efficient because the API does not add dependency on external libraries or does not even use function calls. It's just a bunch of macros that inject assembly code. When a process is run under Valgrind then Memchecker is able to detect and the assembly instructions.

For example the Intel asm for ``VALGRIND_MEMPOOL_ALLOC`` are 20 instructions. Most of them are move or rotate plus one ``lea`` and one ``xchg``. There is no ``call`` or conditional jump at all.

<details>
<summary>VALGRIND_MEMPOOL_ALLOC asm</summary>

```
$ objdump -drwCS -Mintel ./CMakeFiles/mimalloc-static.dir/src/alloc.c.o
 ...
  #if MI_VALGRIND
  VALGRIND_MEMPOOL_ALLOC(heap, p, size);
    16f1:       48 c7 45 a0 05 13 00 00         mov    QWORD PTR [rbp-0x60],0x1305
    16f9:       48 8b 45 98             mov    rax,QWORD PTR [rbp-0x68]
    16fd:       48 89 45 a8             mov    QWORD PTR [rbp-0x58],rax
    1701:       48 8b 45 e0             mov    rax,QWORD PTR [rbp-0x20]
    1705:       48 89 45 b0             mov    QWORD PTR [rbp-0x50],rax
    1709:       48 8b 45 90             mov    rax,QWORD PTR [rbp-0x70]
    170d:       48 89 45 b8             mov    QWORD PTR [rbp-0x48],rax
    1711:       48 c7 45 c0 00 00 00 00         mov    QWORD PTR [rbp-0x40],0x0
    1719:       48 c7 45 c8 00 00 00 00         mov    QWORD PTR [rbp-0x38],0x0
    1721:       48 8d 45 a0             lea    rax,[rbp-0x60]
    1725:       bb 00 00 00 00          mov    ebx,0x0
    172a:       89 da                   mov    edx,ebx
    172c:       48 c1 c7 03             rol    rdi,0x3
    1730:       48 c1 c7 0d             rol    rdi,0xd
    1734:       48 c1 c7 3d             rol    rdi,0x3d
    1738:       48 c1 c7 33             rol    rdi,0x33
    173c:       48 87 db                xchg   rbx,rbx
    173f:       48 89 d0                mov    rax,rdx
    1742:       48 89 45 d8             mov    QWORD PTR [rbp-0x28],rax
    1746:       48 8b 45 d8             mov    rax,QWORD PTR [rbp-0x28]
  #endif

```
</details>

The most important APIs are

* ``VALGRIND_CREATE_MEMPOOL_EXT(pool, redzone_bytes, is_zeroed, flags)``
* ``VALGRIND_DESTROY_MEMPOOL(pool)``
* `` VALGRIND_MEMPOOL_ALLOC(pool, addr, size)``
* ``VALGRIND_MEMPOOL_FREE(pool, addr)``
* ``VALGRIND_MEMPOOL_CHANGE(pool, addrA, addrB, size)``
* ``VALGRIND_MAKE_MEM_NOACCESS(addr, size)``
* ``VALGRIND_MAKE_MEM_UNDEFINED(addr, size)``
* ``VALGRIND_MAKE_MEM_DEFINED(addr, size)``
* ``RUNNING_ON_VALGRIND``

You can find my experimental branch at https://github.com/microsoft/mimalloc/compare/dev...tiran:valgrind?expand=1 . (disclaimer: it doesn't work yet).

## Comment 1004832215

other (CONTRIBUTOR) · tiran · 2022-01-04T13:56:47Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1004832215

More useful links:

- Postgres is having [some issues](https://www.mail-archive.com/pgsql-hackers@lists.postgresql.org/msg83832.html) with their Valgrind code. It may not be the best example.
- The SMALL memory allocator https://github.com/tarantool/small has full Valgrind integration.
- [jemalloc 4.5](https://github.com/jemalloc/jemalloc/blob/4.5.0/include/jemalloc/internal/valgrind.h) has Valgrind integration. jemalloc 5.0 removed Valgrind code.
- OpenLDAP's [lmdb](https://github.com/openldap/openldap/blob/master/libraries/liblmdb/mdb.c) has Valgrind code, too. 

## Comment 1007624883

maintainer (COLLABORATOR) · daanx · 2022-01-07T18:13:41Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1007624883

Very cool @tiran; thanks for the pointers! I have also been looking into asan support which works similarly. 

However, I think we talked about having the goal of having valgring/asan integration in mimalloc as always enabled, but I think that will not work while maintaining good performance. (for example, mimalloc `malloc` is about 20 instructions as well :-) 
Maybe a way to do this while maintaining best performance is to link mimalloc dynamically and offer a way to use either the release one, or the valgrind one when debugging.

I think I have time later this month to try to take your branch and see if we can make it work.

## Comment 1007632585

other (CONTRIBUTOR) · tiran · 2022-01-07T18:23:06Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1007632585

I agree, the valgrind code should be optional and not enabled by debug. My branch has the code behind ``#ifdef MI_VALGRIND``. A separate debug build shared lib sounds like a great idea.

## Comment 1009720935

other (CONTRIBUTOR) · tiran · 2022-01-11T08:47:19Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1009720935

jemalloc 4.5 used an additional trick to reduce the performance impact of Valgrind macros. It had a global variable that was initialized on startup. The variable was checked before every call to a Valgrind macro or helper method. Mimalloc could use the same approach in addition to ``#ifdef MI_VALGRIND``. If I know my assembly right, then the code only adds a load + conditional JMP.

```
in_valgrind = (RUNNING_ON_VALGRIND != 0) ? true : false;
```

```
if (unlikely(in_valgrind)) {
    ...
}
```

## Comment 1296461762

maintainer (COLLABORATOR) · daanx · 2022-10-31T02:34:39Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1296461762

Very late followup -- but I just got around to adding initial valgrind support in the latest `dev` and `dev-slice` (v2) branches.  I was all quite tricky but it currently seems to work quite well over various tests. If anyone wants to give it a try, let me know how it goes.  I do not yet apply the "global variable" trick -- I wonder if it is needed since the performance impact is fairly minor as far as I can tell.

See the comments in `test/test-wrong.c` file on how to do a quick test to see if it is working, and I added a section to the `readme.md` (in the new branches) that show how to run valgrind if overriding the standard `malloc`/`free`.


## Comment 1300608438

reporter (NONE) · christoph-cullmann · 2022-11-02T15:00:50Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1300608438

Hi, thanks that you did work on this, I will give this some try.

## Comment 1300721197

reporter (NONE) · christoph-cullmann · 2022-11-02T15:44:06Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1300721197

First feeback, the dev-slice branch failed to compile here due to our more restrictive compiler flags:
```

diff --git a/src/include/mimalloc-new-delete.h b/src/include/mimalloc-new-delete.h
index 2749a0b..1c12fad 100644
--- a/src/include/mimalloc-new-delete.h
+++ b/src/include/mimalloc-new-delete.h
@@ -44,8 +44,8 @@ terms of the MIT license. A copy of the license can be found in the file
   void operator delete[](void* p, std::align_val_t al) noexcept { mi_free_aligned(p, static_cast<size_t>(al)); }
   void operator delete  (void* p, std::size_t n, std::align_val_t al) noexcept { mi_free_size_aligned(p, n, static_cast<size_t>(al)); };
   void operator delete[](void* p, std::size_t n, std::align_val_t al) noexcept { mi_free_size_aligned(p, n, static_cast<size_t>(al)); };
-  void operator delete  (void* p, std::align_val_t al, const std::nothrow_t& tag) noexcept { mi_free_aligned(p, static_cast<size_t>(al)); }
-  void operator delete[](void* p, std::align_val_t al, const std::nothrow_t& tag) noexcept { mi_free_aligned(p, static_cast<size_t>(al)); }
+  void operator delete  (void* p, std::align_val_t al, const std::nothrow_t&) noexcept { mi_free_aligned(p, static_cast<size_t>(al)); }
+  void operator delete[](void* p, std::align_val_t al, const std::nothrow_t&) noexcept { mi_free_aligned(p, static_cast<size_t>(al)); }
```

tag is unused


## Comment 1300763471

reporter (NONE) · christoph-cullmann · 2022-11-02T16:00:38Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1300763471

Beside this, first tests look fine, if I use the

--soname-synonyms='somalloc=*mimalloc*'

switch valgrind seems to work fine on first glance with just using the mimalloc-new-delete.h for new/delete overwriting.

## Comment 1300903244

reporter (NONE) · christoph-cullmann · 2022-11-02T16:55:48Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1300903244

Unfortunately for me some of the programs we have crash during the run of the global destructors.

(I only used the mimalloc-new-delete.h to overwrite new/delete)
```

**mimalloc: warning: mi_free: pointer might not point to a valid heap region: 0x555555ce7d40
(this may still be a valid very large allocation (over 64MiB))

Program received signal SIGSEGV, Segmentation fault.
mi_checked_ptr_segment (p=0x555555ce7d40, msg=0x555555715c95 "mi_free") at /local/ssd/cullmann/build/pipe.profiler/mimalloc/src/src/alloc.c:481
481         if mi_likely(_mi_ptr_cookie(segment) == segment->cookie) {
(gdb) bt
#0  mi_checked_ptr_segment (p=0x555555ce7d40, msg=0x555555715c95 "mi_free") at /local/ssd/cullmann/build/pipe.profiler/mimalloc/src/src/alloc.c:481
#1  0x0000555555a7ddee in mi_free (p=0x555555cd3b54 <out_buf+20>) at /local/ssd/cullmann/build/pipe.profiler/mimalloc/src/src/alloc.c:498
#2  0x000055555589814f in std::__1::default_delete<bblock_maxima_t>::operator()[abi:v15001](bblock_maxima_t*) const (this=0x200004b29a0, __ptr=0x555555cd3b54 <out_buf+20>)
    at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/unique_ptr.h:48
#3  std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >::reset[abi:v15001](bblock_maxima_t*) (this=0x200004b29a0, __p=0x0)
    at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/unique_ptr.h:305
#4  std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >::~unique_ptr[abi:v15001]() (this=0x200004b29a0)
    at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/unique_ptr.h:259
#5  std::__1::__destroy_at[abi:v15001]<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, 0>(std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >*) (
    __loc=0x200004b29a0) at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/construct_at.h:63
#6  std::__1::destroy_at[abi:v15001]<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, 0>(std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >*) (
    __loc=0x200004b29a0) at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/construct_at.h:88
#7  std::__1::allocator_traits<std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > >::destroy[abi:v15001]<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, void, void>(std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > >&, std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >*) (__p=0x200004b29a0) at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/allocator_traits.h:317
#8  std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > >::__base_destruct_at_end[abi:v15001](std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >*) (this=0x200004d4c78, __new_last=0x200004b29a0)
    at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/vector:833
#9  std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > >::__clear[abi:v15001]() (this=0x200004d4c78) at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/vector:827
#10 std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > >::~vector[abi:v15001]() (this=0x200004d4c78) at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/vector:436
#11 std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >::~pair (this=0x200004d4c70) at /local/ssd/cullmann/build/pipe.profiler/usr/include/boost/container/detail/std_fwd.hpp:39
#12 std::__1::__destroy_at[abi:v15001]<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >, 0>(std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >*) (__loc=0x200004d4c70)
    at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/construct_at.h:63
#13 std::__1::destroy_at[abi:v15001]<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >, 0>(std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >*) (__loc=0x200004d4c70)
    at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/construct_at.h:88
#14 std::__1::allocator_traits<std::__1::allocator<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > > >::destroy[abi:v15001]<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >, void, void>(std::__1::allocator<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > >&, std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >*) (__p=0x200004d4c70) at /local/ssd/cullmann/build/pipe.profiler/usr/bin/../include/c++/v1/__memory/allocator_traits.h:317
#15 absl::container_internal::NodeHashMapPolicy<CrlEdge const*, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >::delete_element<std::__1::allocator<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > > > (alloc=0x555555c805c8 <get_bblock_maximas(CrlEdge*, bool)::bblockMaxima+32>, 
    pair=0x200004d4c70) at /local/ssd/cullmann/build/pipe.profiler/usr/include/absl/container/node_hash_map.h:571
#16 absl::container_internal::node_slot_policy<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >&, absl::container_internal::NodeHashMapPolicy<CrlEdge const*, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > >::destroy<std::__1::allocator<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > > > (
    alloc=0x555555c805c8 <get_bblock_maximas(CrlEdge*, bool)::bblockMaxima+32>, slot=<optimized out>) at /local/ssd/cullmann/build/pipe.profiler/usr/include/absl/container/internal/node_slot_policy.h:62
#17 absl::container_internal::hash_policy_traits<absl::container_internal::NodeHashMapPolicy<CrlEdge const*, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std:--Type <RET> for more, q to quit, c to continue without paging--
:__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >, void>::destroy<std::__1::allocator<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > > > (
    alloc=0x555555c805c8 <get_bblock_maximas(CrlEdge*, bool)::bblockMaxima+32>, slot=<optimized out>) at /local/ssd/cullmann/build/pipe.profiler/usr/include/absl/container/internal/hash_policy_traits.h:101
#18 absl::container_internal::raw_hash_set<absl::container_internal::NodeHashMapPolicy<CrlEdge const*, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > >, absl::container_internal::HashEq<CrlEdge const*, void>::Hash, absl::container_internal::HashEq<CrlEdge const*, void>::Eq, std::__1::allocator<std::__1::pair<CrlEdge const* const, std::__1::vector<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> >, std::__1::allocator<std::__1::unique_ptr<bblock_maxima_t, std::__1::default_delete<bblock_maxima_t> > > > > > >::destroy_slots (this=0x555555c805a8 <get_bblock_maximas(CrlEdge*, bool)::bblockMaxima>)
    at /local/ssd/cullmann/build/pipe.profiler/usr/include/absl/container/internal/raw_hash_set.h:1961
#19 0x00007ffff7cccfa5 in __run_exit_handlers (status=0, listp=0x7ffff7e6a760 <__exit_funcs>, run_list_atexit=run_list_atexit@entry=true, run_dtors=run_dtors@entry=true) at exit.c:113
#20 0x00007ffff7ccd120 in __GI_exit (status=<optimized out>) at exit.c:143
#21 0x00007ffff7cb5297 in __libc_start_call_main (main=main@entry=0x555555879d00 <main(int, char**)>, argc=argc@entry=16, argv=argv@entry=0x7fffffffd838) at ../sysdeps/nptl/libc_start_call_main.h:74
#22 0x00007ffff7cb534a in __libc_start_main_impl (main=0x555555879d00 <main(int, char**)>, argc=16, argv=0x7fffffffd838, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, 
    stack_end=0x7fffffffd828) at ../csu/libc-start.c:381
#23 0x0000555555864665 in _start () at ../sysdeps/x86_64/start.S:115**

```

## Comment 1300905146

maintainer (COLLABORATOR) · daanx · 2022-11-02T16:56:36Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1300905146

Thanks @christoph-cullmann -- I fixed the compiler warning and good to hear it seems to work for you now. I also tested myself on the benchmark suite programs and things worked as well. It took quite a while to make this work as I kept getting errors in multithreaded programs but I finally figured out I had a misunderstanding of how the model worked :-). 

In the test file (`test/test-wrong.c`) it is very cool to see valgrind catch byte precise heap buffer overflows/underflows where they happen.

@tiran : if you find time it would be great if you could test this with the Python integration.  

## Comment 1300925563

maintainer (COLLABORATOR) · daanx · 2022-11-02T17:05:13Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1300925563

> Unfortunately for me some of the programs we have crash during the run of the global destructors.
> 
> (I only used the mimalloc-new-delete.h to overwrite new/delete)
> 
> ```
> 
> **mimalloc: warning: mi_free: pointer might not point to a valid heap region: 0x555555ce7d40
> (this may still be a valid very large allocation (over 64MiB))
> 
> Program received signal SIGSEGV, Segmentation fault.
> mi_checked_ptr_segment (p=0x555555ce7d40, msg=0x555555715c95 "mi_free") at /local/ssd/cullmann/build/pipe.profiler/mimalloc/src/src/alloc.c:481
> 481         if mi_likely(_mi_ptr_cookie(segment) == segment->cookie) {
> (gdb) bt
> #0  mi_checked_ptr_segment (p=0x555555ce7d40, msg=0x555555715c95 "mi_free") at /local/ssd/cullmann/build/pipe.profiler/mimalloc/src/src/alloc.c:481
> #1  0x0000555555a7ddee in mi_free (p=0x555555cd3b54 <out_buf+20>) at 
> ```

ah that is not good -- but this has nothing to do with valgrind I think ?

It looks like a pointer is being deleted that was not allocated by mimalloc:

- maybe you got a pointer that came from a library that uses its own allocator, 
- or perhaps the pointer points to static memory, 
-  or (and I think this may be it), the pointer was allocated with a regular `malloc` (that you don't override), but freed using `delete` (which you do override). 

Try to run the program without linking to mimalloc and using `LD_PRELOAD` to see if the crash still occurs. If not, it is surely pointer mixing from different allocators. (but to stay in the topic of this issue, unfortunately, valgrind does not work with LD_PRELOAD).


(ps. ah, just in case, a work-around is to go into `mimalloc-new-delete.h` and replace the `mi_free` calls to `mi_cfree` (checked free). Slightly slower but won't segfault for wrong pointers (but also not free those pointers))

## Comment 1301238436

reporter (NONE) · christoph-cullmann · 2022-11-02T20:57:03Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1301238436

Will try LD_PRELOAD.
The container in question is from abseil.

## Comment 1301814931

reporter (NONE) · christoph-cullmann · 2022-11-03T09:07:55Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1301814931

Ok, issue in our code base, malloc vs. delete. Nice to have this found, valgrind didn't catch this.

## Comment 1480864012

other (NONE) · FrankHB · 2023-03-23T09:31:54Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1480864012

I'm using `LD_PRELOAD` and there is exact the same issue.

Given the fact that it immediately behaves wrongly in the calls of `std::allocator` functions, I'm not sure what exactly goes wrong. Perhaps a valgrind issue of incompatibility of aliases?

```
==13952== Mismatched free() / delete / delete []
==13952==    at 0x484426F: free (/usr/src/debug/valgrind/valgrind-3.20.0/coregrind/m_replacemalloc/vg_replace_malloc.c:884)
==13952==    by 0x31A92F: std::__new_allocator<char const*>::deallocate(char const**, unsigned long) (/usr/include/c++/12.1.0/bits/new_allocator.h:158)
==13952==    by 0x315CDC: std::allocator_traits<std::allocator<char const*> >::deallocate(std::allocator<char const*>&, char const**, unsigned long) (/usr/include/c++/12.1.0/bits/alloc_traits.h:496)
==13952==    by 0x3105A3: std::_Vector_base<char const*, std::allocator<char const*> >::_M_deallocate(char const**, unsigned long) (/usr/include/c++/12.1.0/bits/stl_vector.h:387)
==13952==    by 0x30A753: std::_Vector_base<char const*, std::allocator<char const*> >::~_Vector_base() (/usr/include/c++/12.1.0/bits/stl_vector.h:366)
==13952==    by 0x305BB6: std::vector<char const*, std::allocator<char const*> >::~vector() (/usr/include/c++/12.1.0/bits/stl_vector.h:733)

...

==13952==    at 0x48432E3: operator new[](unsigned long) (/usr/src/debug/valgrind/valgrind-3.20.0/coregrind/m_replacemalloc/vg_replace_malloc.c:652)
==13952==    by 0x31A9AB: std::__new_allocator<char const*>::allocate(unsigned long, void const*) (/usr/include/c++/12.1.0/bits/new_allocator.h:137)
==13952==    by 0x315D91: std::allocator_traits<std::allocator<char const*> >::allocate(std::allocator<char const*>&, unsigned long) (/usr/include/c++/12.1.0/bits/alloc_traits.h:464)
==13952==    by 0x310697: std::_Vector_base<char const*, std::allocator<char const*> >::_M_allocate(unsigned long) (/usr/include/c++/12.1.0/bits/stl_vector.h:378)
==13952==    by 0x30A804: void std::vector<char const*, std::allocator<char const*> >::_M_range_initialize<char const* const*>(char const* const*, char const* const*, std::forward_iterator_tag) (/usr/include/c++/12.1.0/bits/stl_vector.h:1687)
==13952==    by 0x305B3F: std::vector<char const*, std::allocator<char const*> >::vector(std::initializer_list<char const*>, std::allocator<char const*> const&) (/usr/include/c++/12.1.0/bits/stl_vector.h:677)```
```

It is even more problematic when using `tcmalloc` (with other errors). And `snmalloc` just fails to initialize.

The only working one I've tried is `jemalloc`, probably due to [this change](https://github.com/jemalloc/jemalloc/commit/2319152d9f5d9b33eebc36a50ccf4239f31c1ad9).

Everything seems OK without memcheck, except that `snmalloc` also crashes with callgrind (but it was at least OK with some old version of G++ one year ago). This may be another issue...


## Comment 1481701222

maintainer (COLLABORATOR) · daanx · 2023-03-23T18:29:24Z · https://github.com/microsoft/mimalloc/issues/251#issuecomment-1481701222

Hi @FrankHB,  I have recently been improving valgrind and asan support, and the latest `dev`/`dev-slice` branches have Windows ETW support as well. For Valgrind, did you read this: <https://github.com/microsoft/mimalloc#valgrind> ?

It should work well with static linking and malloc/free overriding. I have not been able to make valgrind work with LD_PRELOAD..  as I understood at the time, this is not really possible since valgrind tries to take over malloc/free itself. (which is why we need the funny command line even with static linking).  
If you think it can be made to work even with LD_PRELOAD let me know how :-)
