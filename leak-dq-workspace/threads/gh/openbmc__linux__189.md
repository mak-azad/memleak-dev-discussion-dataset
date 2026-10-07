# kmemleak detected in fsi master

- URL: https://github.com/openbmc/linux/issues/189
- Repo: openbmc/linux (language: C)
- State: open; created 2020-04-07T22:24:21Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · shenki · 2020-04-07T22:24:21Z · https://github.com/openbmc/linux/issues/189

Running 5.4.28-00243-g757f8a4d828d on tacoma (ast2600)

```
unreferenced object 0xb4c76080 (size 64):
  comm "openpower-proc-", pid 834, jiffies 4294958303 (age 48632.290s)
  hex dump (first 32 bytes):
    73 6c 61 76 65 40 30 30 3a 30 30 00 63 61 74 69  slave@00:00.cati
    6f 6e 5f 69 64 00 ff ff ff ff ff ff ff ff ff ff  on_id...........
  backtrace:
    [<f784ec53>] __kmalloc_track_caller+0x108/0x234
    [<7171ff6a>] kvasprintf+0x64/0xcc
    [<4b2c151e>] kvasprintf_const+0x70/0x84
    [<2366eb74>] kobject_set_name_vargs+0x34/0xa8
    [<da392fbd>] dev_set_name+0x40/0x5c
    [<95e3591d>] fsi_master_scan+0x15c/0x7e0
    [<9729cf80>] fsi_master_rescan+0x3c/0x54
    [<baaabd03>] master_rescan_store+0x1c/0x28
    [<e0dce244>] dev_attr_store+0x24/0x30
    [<87b299fc>] sysfs_kf_write+0x48/0x54
    [<89c19ac5>] kernfs_fop_write+0x124/0x24c
    [<e753a67b>] __vfs_write+0x4c/0x1dc
    [<71e0cd50>] vfs_write+0xbc/0x18c
    [<7e334600>] ksys_write+0x74/0xec
    [<233bb279>] sys_write+0x18/0x1c
    [<3ffa8e8f>] ret_fast_syscall+0x0/0x54
```

## Comment 610653889

other (NONE) · mdmillerii · 2020-04-07T22:35:49Z · https://github.com/openbmc/linux/issues/189#issuecomment-610653889

This is dev_set_name. 

Was there a trigger?   Is the driver trying to set the name after the device was added?
