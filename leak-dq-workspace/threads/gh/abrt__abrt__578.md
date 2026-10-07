# collect kernel memory leaks

- URL: https://github.com/abrt/abrt/issues/578
- Repo: abrt/abrt (language: C)
- State: open; created 2013-02-04T13:13:10Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · mozeq · 2013-02-04T13:13:10Z · https://github.com/abrt/abrt/issues/578

Opened '20121211T07:08:32' by npajkovs as https://fedorahosted.org/abrt/ticket/920

Kmemleak provides a way of detecting possible kernel memory leaks in a
way similar to a tracing garbage collector with the difference that
the orphan objects are not freed but only reported via 
/sys/kernel/debug/kmemleak.

doc http://www.mjmwired.net/kernel/Documentation/kmemleak.txt

{{{
unreferenced object 0xffff880211e2aec0 (size 544):
   comm "X", pid 1377, jiffies 4294790842 (age 147359.137s)
   hex dump (first 32 bytes):
   00 00 00 00 00 00 00 00 00 73 fe 11 02 88 ff ff   .........s......
   00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00   ................
   backtrace:
     [<ffffffff81189293>] create_object+0x123/0x2f0
     [<ffffffff818b51d1>] kmemleak_alloc+0x21/0x50
     [<ffffffff8117e4e3>] kmem_cache_alloc+0xd3/0x110
     [<ffffffff813b9217>] idr_pre_get+0x67/0x90
     [<ffffffff814ad93d>] drm_gem_handle_create+0x3d/0x100
     [<ffffffff814dcd7b>] i915_gem_create+0x6b/0xd0
     [<ffffffff814dcdf9>] i915_gem_create_ioctl+0x19/0x20
     [<ffffffff814aba20>] drm_ioctl+0x2d0/0x520
     [<ffffffff8119eb7a>] do_vfs_ioctl+0x8a/0x2f0
     [<ffffffff8119ee71>] sys_ioctl+0x91/0xa0
     [<ffffffff818d8cd8>] tracesys+0xe1/0xe6
     [<ffffffffffffffff>] 0xffffffffffffffff
}}}

I'm suggesting to add new option --kmemleak to abrt-dump-oops, which will enable catching kmemleak.

