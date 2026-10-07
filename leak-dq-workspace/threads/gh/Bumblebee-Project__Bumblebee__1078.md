# unreferenced object in kmemleak

- URL: https://github.com/Bumblebee-Project/Bumblebee/issues/1078
- Repo: Bumblebee-Project/Bumblebee (language: C)
- State: open; created 2021-04-20T16:36:23Z; status ok; passes offcwe

## Issue body

reporter (NONE) · Bogdan107 · 2021-04-20T16:36:23Z · https://github.com/Bumblebee-Project/Bumblebee/issues/1078

I got an error:
```
# cat /sys/kernel/debug/kmemleak
unreferenced object 0xffff979c19298440 (size 32):                                                                                                                                                                                             
  comm "bumblebeed", pid 15450, jiffies 4294694353 (age 8127.681s)                                                                                                                                                                            
  hex dump (first 32 bytes):
    5c 5f 53 42 5f 2e 50 43 49 30 2e 47 50 31 37 2e  \_SB_.PCI0.GP17.
    56 47 41 5f 00 00 00 00 00 00 00 00 00 00 00 00  VGA_............
  backtrace:
    [<0000000064e54179>] acpi_ut_initialize_buffer+0x36/0x6b
    [<000000004aca805b>] acpi_ns_handle_to_pathname+0x4d/0x72
    [<0000000049979e1a>] acpi_get_name+0x58/0x7c
    [<0000000002ecd249>] 0xffffffffc032b70d
    [<000000003551212e>] 0xffffffffc032b94c
    [<0000000072714275>] 0xffffffffc033131b
    [<000000009e0690cb>] do_one_initcall+0x57/0x200
    [<00000000381878d9>] do_init_module+0x87/0x2a0
    [<000000008ad02371>] __do_sys_finit_module+0xb5/0x120
    [<0000000013d803ea>] do_syscall_64+0x33/0x80
    [<000000005f189bb5>] entry_SYSCALL_64_after_hwframe+0x44/0xa9
unreferenced object 0xffff979c19298220 (size 32):
  comm "bumblebeed", pid 15450, jiffies 4294694353 (age 8127.681s)
  hex dump (first 32 bytes):
    5c 5f 53 42 5f 2e 50 43 49 30 2e 47 50 31 37 2e  \_SB_.PCI0.GP17.
    56 47 41 5f 00 00 00 00 00 00 00 00 00 00 00 00  VGA_............
  backtrace:
    [<0000000064e54179>] acpi_ut_initialize_buffer+0x36/0x6b
    [<000000004aca805b>] acpi_ns_handle_to_pathname+0x4d/0x72
    [<0000000049979e1a>] acpi_get_name+0x58/0x7c
    [<0000000002ecd249>] 0xffffffffc032b70d
    [<000000003551212e>] 0xffffffffc032b94c
    [<0000000072cc7276>] 0xffffffffc033137f
    [<000000009e0690cb>] do_one_initcall+0x57/0x200
    [<00000000381878d9>] do_init_module+0x87/0x2a0
    [<000000008ad02371>] __do_sys_finit_module+0xb5/0x120
    [<0000000013d803ea>] do_syscall_64+0x33/0x80
    [<000000005f189bb5>] entry_SYSCALL_64_after_hwframe+0x44/0xa9

# dmesg | grep -i PCI0.GP17
[   27.223546] bbswitch: Found discrete VGA device 0000:05:00.0: \_SB_.PCI0.GP17.VGA_
[   27.223576] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xF8,0xD8,0x86,0xA4,0xDA,0x0B,0x1B,0x47,0xA7,0x2B,0x60,0x42,0xA6,0xB5,0xBE,0xE0} 0x100 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   27.223591] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xA0,0xA0,0x95,0x9D,0x60,0x00,0x48,0x4D,0xB3,0x4D,0x7E,0x5F,0xEA,0x12,0x9F,0xD4} 0x102 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND

# dmesg | grep -i bbswitch
[   27.223525] bbswitch: version 0.8
[   27.223542] bbswitch: Found discrete VGA device 0000:01:00.0: \_SB_.PCI0.GPP0.PEGP
[   27.223546] bbswitch: Found discrete VGA device 0000:05:00.0: \_SB_.PCI0.GP17.VGA_
[   27.223576] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xF8,0xD8,0x86,0xA4,0xDA,0x0B,0x1B,0x47,0xA7,0x2B,0x60,0x42,0xA6,0xB5,0xBE,0xE0} 0x100 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   27.223591] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xA0,0xA0,0x95,0x9D,0x60,0x00,0x48,0x4D,0xB3,0x4D,0x7E,0x5F,0xEA,0x12,0x9F,0xD4} 0x102 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   27.223592] bbswitch: No suitable _DSM call found.

# dmesg -l err,warn | grep -v VBox | grep -v xfs | grep -v rtc | grep -v ELAN
[    1.394441] ACPI BIOS Error (bug): Could not resolve symbol [\_SB.PCI0.GPP1.WLAN], AE_NOT_FOUND (20201113/dswload2-162)
[    1.394457] ACPI Error: AE_NOT_FOUND, During name lookup/catalog (20201113/psobject-220)
[    1.831431] Expanded resource Reserved due to conflict with PCI Bus 0000:00
[    2.056303] pci 0000:00:00.2: can't derive routing for PCI INT A
[    2.056305] pci 0000:00:00.2: PCI INT A: not connected
[    2.057526]  PPR X2APIC NX GT IA GA PC GA_vAPIC
[    2.080444] DLM installed
[    2.159607] ACPI Error: AE_NOT_FOUND, While resolving a named reference package element - \_PR_.P000 (20201113/dspkginit-438)
[    2.160273] ACPI: Invalid passive threshold
[    2.589492] r8169 0000:02:00.0: can't disable ASPM; OS doesn't have ASPM control
[    2.642741] usb: port power management may be unreliable
[    2.664015] i8042: PNP: PS/2 appears to have AUX port disabled, if this is incorrect please boot with i8042.nopnp
[    8.228772] nvidia: loading out-of-tree module taints kernel.
[    8.228804] nvidia: module license 'NVIDIA' taints kernel.
[    8.228807] Disabling lock debugging due to kernel taint
[    8.373428] NVRM: loading NVIDIA UNIX x86_64 Kernel Module  460.67  Thu Mar 11 00:11:45 UTC 2021
[   10.619821] ================================================================================
[   10.619824] UBSAN: shift-out-of-bounds in drivers/gpu/drm/amd/amdgpu/../amdkfd/kfd_device_queue_manager.c:1140:32
[   10.619828] shift exponent 64 is too large for 64-bit type 'long long unsigned int'
[   10.619831] CPU: 0 PID: 3675 Comm: udevd Tainted: P           OE   T 5.11.15-gentoo-x86_64 #2
[   10.619835] Hardware name: HP HP Pavilion Gaming Laptop 15-ec1xxx/87B1, BIOS F.20 11/04/2020
[   10.619837] Call Trace:
[   10.619840]  dump_stack+0x77/0x97
[   10.619847]  ubsan_epilogue+0x5/0x40
[   10.619850]  __ubsan_handle_shift_out_of_bounds.cold+0x61/0xed
[   10.619854]  initialize_cpsch.cold+0x30/0x35 [amdgpu]
[   10.620242]  device_queue_manager_init+0x207/0x3e0 [amdgpu]
[   10.620580]  kgd2kfd_device_init.cold+0x168/0x373 [amdgpu]
[   10.620957]  amdgpu_amdkfd_device_init+0x145/0x180 [amdgpu]
[   10.621284]  amdgpu_device_ip_init+0x378/0x3a4 [amdgpu]
[   10.621662]  amdgpu_device_init.cold+0x429/0x735 [amdgpu]
[   10.622026]  amdgpu_driver_load_kms+0x59/0x1e0 [amdgpu]
[   10.622317]  amdgpu_pci_probe+0xf8/0x180 [amdgpu]
[   10.622600]  local_pci_probe+0x42/0x80
[   10.622606]  ? _cond_resched+0x16/0x40
[   10.622610]  pci_call_probe+0x5a/0x120
[   10.622614]  ? kernfs_create_link+0x5d/0xa0
[   10.622618]  pci_device_probe+0xb8/0x100
[   10.622621]  really_probe+0x104/0x480
[   10.622624]  driver_probe_device+0xcd/0xe0
[   10.622627]  device_driver_attach+0xc0/0xe0
[   10.622630]  __driver_attach+0x8a/0x160
[   10.622633]  ? device_driver_attach+0xe0/0xe0
[   10.622635]  ? device_driver_attach+0xe0/0xe0
[   10.622637]  bus_for_each_dev+0x89/0xe0
[   10.622642]  bus_add_driver+0x12b/0x200
[   10.622646]  driver_register+0x8f/0xe0
[   10.622649]  ? 0xffffffffc24a1000
[   10.622651]  do_one_initcall+0x57/0x200
[   10.622657]  do_init_module+0x87/0x2a0
[   10.622662]  __do_sys_init_module+0x13c/0x1c0
[   10.622667]  do_syscall_64+0x33/0x80
[   10.622672]  entry_SYSCALL_64_after_hwframe+0x44/0xa9
[   10.622676] RIP: 0033:0x7fb4f57a883a
[   10.622680] Code: 48 8b 0d 29 c6 0b 00 f7 d8 64 89 01 48 83 c8 ff c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 44 00 00 49 89 ca b8 af 00 00 00 0f 05 <48> 3d 01 f0 ff ff 73 01 c3 48 8b 0d f6 c5 0b 00 f7 d8 64 89 01 48
[   10.622683] RSP: 002b:00007ffc9b026ed8 EFLAGS: 00000246 ORIG_RAX: 00000000000000af
[   10.622687] RAX: ffffffffffffffda RBX: 00005600180e7b10 RCX: 00007fb4f57a883a
[   10.622689] RDX: 00005600180d5c00 RSI: 0000000001069d59 RDI: 00007fb4f23bc010
[   10.622691] RBP: 00007fb4f23bc010 R08: 0000000000000000 R09: 00007fb4f3425d68
[   10.622693] R10: 0000000000008000 R11: 0000000000000246 R12: 00005600180d5c00
[   10.622695] R13: 00005600180dbe70 R14: 0000000000000000 R15: 00005600181089a0
[   10.622713] ================================================================================
[   11.646107] amdgpu 0000:05:00.0: amdgpu: Unsupported power profile mode 0 on RENOIR
[   26.135526] ================================================================================
[   26.135532] UBSAN: array-index-out-of-bounds in drivers/net/wireless/realtek/rtw88/phy.c:1661:35
[   26.135538] index 5 is out of range for type 'u8 [5]'
[   26.135541] CPU: 2 PID: 74 Comm: kworker/u32:2 Tainted: P           OE   T 5.11.15-gentoo-x86_64 #2
[   26.135546] Hardware name: HP HP Pavilion Gaming Laptop 15-ec1xxx/87B1, BIOS F.20 11/04/2020
[   26.135550] Workqueue: phy0 ieee80211_scan_work
[   26.135560] Call Trace:
[   26.135563]  dump_stack+0x77/0x97
[   26.135571]  ubsan_epilogue+0x5/0x40
[   26.135575]  __ubsan_handle_out_of_bounds.cold+0x43/0x48
[   26.135580]  rtw_get_tx_power_params+0x70c/0xa60 [rtw88_core]
[   26.135600]  ? check_hw_ready+0x4f/0xa0 [rtw88_core]
[   26.135616]  rtw_phy_get_tx_power_index+0x4b/0xe0 [rtw88_core]
[   26.135632]  rtw_phy_set_tx_power_level+0xd2/0x1a0 [rtw88_core]
[   26.135648]  rtw_set_channel+0xc1/0x120 [rtw88_core]
[   26.135664]  rtw_ops_config+0x87/0xc0 [rtw88_core]
[   26.135679]  ieee80211_hw_config+0x84/0x100
[   26.135683]  ieee80211_scan_state_set_channel+0x81/0x180
[   26.135688]  ieee80211_scan_work+0x19f/0x2a0
[   26.135693]  process_one_work+0x1f0/0x3a0
[   26.135700]  worker_thread+0x4f/0x320
[   26.135704]  ? process_one_work+0x3a0/0x3a0
[   26.135708]  kthread+0x120/0x140
[   26.135713]  ? __kthread_bind_mask+0x60/0x60
[   26.135716]  ret_from_fork+0x22/0x30
[   26.135723] ================================================================================
[   27.223576] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xF8,0xD8,0x86,0xA4,0xDA,0x0B,0x1B,0x47,0xA7,0x2B,0x60,0x42,0xA6,0xB5,0xBE,0xE0} 0x100 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   27.223591] bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xA0,0xA0,0x95,0x9D,0x60,0x00,0x48,0x4D,0xB3,0x4D,0x7E,0x5F,0xEA,0x12,0x9F,0xD4} 0x102 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
[   27.223592] bbswitch: No suitable _DSM call found.
[   27.440040] ACPI Warning: \_SB.PCI0.GPP0.PEGP._DSM: Argument #4 type mismatch - Found [Buffer], ACPI requires [Package] (20201113/nsarguments-61)
[   28.442823] ================================================================================
[   28.442828] UBSAN: shift-out-of-bounds in drivers/gpu/drm/amd/amdgpu/../display/dc/dml/dcn21/display_rq_dlg_calc_21.c:288:38
[   28.442833] shift exponent 4294966273 is too large for 32-bit type 'int'
[   28.442837] CPU: 2 PID: 15336 Comm: X Tainted: P           OE   T 5.11.15-gentoo-x86_64 #2
[   28.442841] Hardware name: HP HP Pavilion Gaming Laptop 15-ec1xxx/87B1, BIOS F.20 11/04/2020
[   28.442843] Call Trace:
[   28.442845]  dump_stack+0x77/0x97
[   28.442852]  ubsan_epilogue+0x5/0x40
[   28.442855]  __ubsan_handle_shift_out_of_bounds.cold+0x61/0xed
[   28.442859]  handle_det_buf_split.isra.0.cold+0x1c/0x4b [amdgpu]
[   28.443198]  dml_rq_dlg_get_rq_params+0x205/0x240 [amdgpu]
[   28.443523]  dml21_rq_dlg_get_dlg_reg+0x194/0x2a0 [amdgpu]
[   28.443838]  ? sched_clock_cpu+0x10/0xe0
[   28.443845]  ? dml21_rq_dlg_get_rq_reg+0x3a0/0x3a0 [amdgpu]
[   28.444148]  dcn20_calculate_dlg_params+0x48b/0x740 [amdgpu]
[   28.444473]  dcn21_validate_bandwidth_fp+0x212/0x380 [amdgpu]
[   28.444808]  dcn21_validate_bandwidth+0x29/0x40 [amdgpu]
[   28.445127]  dc_validate_global_state+0x313/0x4e0 [amdgpu]
[   28.445451]  amdgpu_dm_atomic_check+0x8ed/0x980 [amdgpu]
[   28.445788]  drm_atomic_check_only+0x22e/0x480
[   28.445796]  drm_atomic_commit+0x13/0x60
[   28.445800]  drm_atomic_helper_set_config+0x70/0xc0
[   28.445814]  drm_ioctl_kernel+0xb3/0x100
[   28.445818]  drm_ioctl+0x235/0x420
[   28.445825]  amdgpu_drm_ioctl+0x49/0x80 [amdgpu]
[   28.446069]  __x64_sys_ioctl+0x8d/0xc0
[   28.446074]  do_syscall_64+0x33/0x80
[   28.446079]  entry_SYSCALL_64_after_hwframe+0x44/0xa9
[   28.446085] RIP: 0033:0x7f1d5342a807
[   28.446090] Code: 01 75 a5 49 8d 3c 1c e8 f7 fe ff ff 85 c0 78 a6 5b 4c 89 e0 5d 41 5c c3 66 2e 0f 1f 84 00 00 00 00 00 90 b8 10 00 00 00 0f 05 <48> 3d 01 f0 ff ff 73 01 c3 48 8b 0d 29 66 0c 00 f7 d8 64 89 01 48
[   28.446093] RSP: 002b:00007ffdc26835b8 EFLAGS: 00000246 ORIG_RAX: 0000000000000010
[   28.446098] RAX: ffffffffffffffda RBX: 00007ffdc26835f0 RCX: 00007f1d5342a807
[   28.446100] RDX: 00007ffdc26835f0 RSI: 00000000c06864a2 RDI: 000000000000000f
[   28.446102] RBP: 00000000c06864a2 R08: 0000000000000000 R09: 00005561ab0b1a70
[   28.446104] R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000000000
[   28.446106] R13: 000000000000000f R14: 00005561aa5bdc60 R15: 00005561aa778c20
[   28.446129] ================================================================================
```

Kernel 5.11.15-gentoo-x86_64
x11-misc/bumblebee 3.2.1_p20210112-r4
sys-power/bbswitch 0.8-r5


## Comment 1336517894

other (NONE) · andreas-thalhammer · 2022-12-04T21:09:30Z · https://github.com/Bumblebee-Project/Bumblebee/issues/1078#issuecomment-1336517894

I have the same, my hardware is a Lenovo Legion 5 Pro (AMD Ryzen 7 5800H). The hybrid graphics configuration consists of 1) AMD Radeon RX Vega 8 "Green Sardine", which should be considered as "integrated", and 2) Nvidia GeForce RTX 3070 Mobile (GA104M).

Nouveau currently doesn't support the Nvidia GeForce RTX 30 series of graphics cards. I am **not** using the proprietary closed-source/binary-only Nvidia drivers.

I have to set graphics to "dynamic" in the UEFI settings (BIOS setup) in order for Linux to work correctly, the alternative (default) setting of "discrete" graphics causes any output (including text mode) to act up in Linux. My understanding of this is that with the "discrete" setting the Nvidia card will be used by UEFI on startup, which Linux cannot handle with the nouveau driver (yet).

The graphics card specifics:
```
# lspci -nn | grep VGA
01:00.0 VGA compatible controller [0300]: NVIDIA Corporation GA104M [GeForce RTX 3070 Mobile / Max-Q] [10de:24dd] (rev a1)
06:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Cezanne [Radeon Vega Series / Radeon Vega Mobile Series] [1002:1638] (rev c5)
```

The integrated CPU Radeon graphics core (apparently \_SB_.PCI0.GP17.VGA_) is accelerated and loaded correctly by AMDGPU which I have compiled into the kernel (not as a module). The following dmesg snippet is from Gentoo kernel 6.0.11 (in this configuration I have the nouveau module blacklisted, so it isn't loaded later-on):

```
[drm] amdgpu kernel modesetting enabled.
amdgpu: vga_switcheroo: detected switching method \_SB_.PCI0.GP17.VGA_.ATPX handle
ATPX version 1, functions 0x00000001
ATPX Hybrid Graphics
amdgpu: Ignoring ACPI CRAT on non-APU system
amdgpu: Virtual CRAT table created for CPU
amdgpu: Topology: Add CPU node
amdgpu 0000:06:00.0: vgaarb: deactivate vga console
amdgpu 0000:06:00.0: enabling device (0006 -> 0007)
[drm] initializing kernel modesetting (RENOIR 0x1002:0x1638 0x17AA:0x3A4F 0xC5).
[drm] register mmio base: 0xD1500000
[drm] register mmio size: 524288
[drm] add ip block number 0 <soc15_common>
[drm] add ip block number 1 <gmc_v9_0>
[drm] add ip block number 2 <vega10_ih>
[drm] add ip block number 3 <psp>
[drm] add ip block number 4 <smu>
[drm] add ip block number 5 <dm>
[drm] add ip block number 6 <gfx_v9_0>
[drm] add ip block number 7 <sdma_v4_0>
[drm] add ip block number 8 <vcn_v2_0>
[drm] add ip block number 9 <jpeg_v2_0>
amdgpu 0000:06:00.0: amdgpu: Fetched VBIOS from VFCT
amdgpu: ATOM BIOS: 113-CEZANNE-020
Loading firmware: amdgpu/green_sardine_sdma.bin
[drm] VCN decode is enabled in VM mode
[drm] VCN encode is enabled in VM mode
[drm] JPEG decode is enabled in VM mode
amdgpu 0000:06:00.0: amdgpu: Trusted Memory Zone (TMZ) feature enabled
amdgpu 0000:06:00.0: amdgpu: PCIE atomic ops is not supported
amdgpu 0000:06:00.0: amdgpu: MODE2 reset
[drm] vm size is 262144 GB, 4 levels, block size is 9-bit, fragment size is 9-bit
amdgpu 0000:06:00.0: amdgpu: VRAM: 4096M 0x000000F400000000 - 0x000000F4FFFFFFFF (4096M used)
amdgpu 0000:06:00.0: amdgpu: GART: 1024M 0x0000000000000000 - 0x000000003FFFFFFF
amdgpu 0000:06:00.0: amdgpu: AGP: 267419648M 0x000000F800000000 - 0x0000FFFFFFFFFFFF
[drm] Detected VRAM RAM=4096M, BAR=4096M
[drm] RAM width 128bits DDR4
[drm] amdgpu: 4096M of VRAM memory ready
[drm] amdgpu: 30057M of GTT memory ready.
[drm] GART: num cpu pages 262144, num gpu pages 262144
[drm] PCIE GART of 1024M enabled.
[drm] PTB located at 0x000000F4FFC00000
Loading firmware: amdgpu/green_sardine_asd.bin
Loading firmware: amdgpu/green_sardine_ta.bin
amdgpu 0000:06:00.0: amdgpu: PSP runtime database doesn't exist
amdgpu 0000:06:00.0: amdgpu: PSP runtime database doesn't exist
Loading firmware: amdgpu/green_sardine_dmcub.bin
[drm] Loading DMUB firmware via PSP: version=0x0101001F
Loading firmware: amdgpu/green_sardine_pfp.bin
Loading firmware: amdgpu/green_sardine_me.bin
Loading firmware: amdgpu/green_sardine_ce.bin
Loading firmware: amdgpu/green_sardine_rlc.bin
Loading firmware: amdgpu/green_sardine_mec.bin
Loading firmware: amdgpu/green_sardine_vcn.bin
[drm] Found VCN firmware Version ENC: 1.17 DEC: 5 VEP: 0 Revision: 2
amdgpu 0000:06:00.0: amdgpu: Will use PSP to load VCN firmware
[drm] reserve 0x400000 from 0xf4ff400000 for PSP TMR
amdgpu 0000:06:00.0: amdgpu: RAS: optional ras ta ucode is not available
amdgpu 0000:06:00.0: amdgpu: RAP: optional rap ta ucode is not available
amdgpu 0000:06:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
amdgpu 0000:06:00.0: amdgpu: SMU is initialized successfully!
[drm] Display Core initialized with v3.2.198!
[drm] DMUB hardware initialized: version=0x0101001F
[drm] kiq ring mec 2 pipe 1 q 0
[drm] VCN decode and encode initialized successfully(under DPG Mode).
[drm] JPEG decode initialized successfully.
kfd kfd: amdgpu: Allocated 3969056 bytes on gart
amdgpu: sdma_bitmap: 3
memmap_init_zone_device initialised 1048576 pages in 7ms
amdgpu: HMM registered 4096MB device memory
amdgpu: SRAT table not found
amdgpu: Virtual CRAT table created for GPU
amdgpu: Topology: Add dGPU node [0x1638:0x1002]
kfd kfd: amdgpu: added device 1002:1638
amdgpu 0000:06:00.0: amdgpu: SE 1, SH per SE 1, CU per SH 8, active_cu_number 8
amdgpu 0000:06:00.0: amdgpu: ring gfx uses VM inv eng 0 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring kiq_2.1.0 uses VM inv eng 11 on hub 0
amdgpu 0000:06:00.0: amdgpu: ring sdma0 uses VM inv eng 0 on hub 1
amdgpu 0000:06:00.0: amdgpu: ring vcn_dec uses VM inv eng 1 on hub 1
amdgpu 0000:06:00.0: amdgpu: ring vcn_enc0 uses VM inv eng 4 on hub 1
amdgpu 0000:06:00.0: amdgpu: ring vcn_enc1 uses VM inv eng 5 on hub 1
amdgpu 0000:06:00.0: amdgpu: ring jpeg_dec uses VM inv eng 6 on hub 1
[drm] Initialized amdgpu 3.48.0 20150101 for 0000:06:00.0 on minor 0
fbcon: amdgpudrmfb (fb0) is primary device
[drm] DSC precompute is not needed.
Console: switching to colour frame buffer device 320x100
amdgpu 0000:06:00.0: [drm] fb0: amdgpudrmfb frame buffer device
```

When I try to load bbswitch, I get this error in dmesg (and the module isn't loaded at all, i.e. it is not listed by lsmod as loaded):
```
# modprobe bbswitch
modprobe: ERROR: could not insert 'bbswitch': No such device
# dmesg -t | tail
bbswitch: version 0.8
bbswitch: Found discrete VGA device 0000:01:00.0: \_SB_.PCI0.GPP0.PEGP
bbswitch: Found discrete VGA device 0000:06:00.0: \_SB_.PCI0.GP17.VGA_
bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xF8,0xD8,0x86,0xA4,0xDA,0x0B,0x1B,0x47,0xA7,0x2B,0x60,0x42,0xA6,0xB5,0xBE,0xE0} 0x100 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xA0,0xA0,0x95,0x9D,0x60,0x00,0x48,0x4D,0xB3,0x4D,0x7E,0x5F,0xEA,0x12,0x9F,0xD4} 0x102 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
bbswitch: No suitable _DSM call found.
```

I do not get any kernel panics with only the AMDGPU driver. When I also load nouveau, the kernel reports similar errors as the original reporter. The following error is with nouveau loaded, Gentoo Linux and kernel 5.18.14: (the first driver loaded is AMDGPU, in-kernel, dmesg similar to the above with the newer kernel; thereafter nouveau is loaded, dmesg is like this:)
```
ACPI Warning: \_SB.PCI0.GPP0.PEGP._DSM: Argument #4 type mismatch - Found [Buffer], ACPI requires [Package] (20211217/nsarguments-61)
pci 0000:01:00.0: optimus capabilities: enabled, status dynamic power, hda bios codec supported
VGA switcheroo: detected Optimus DSM method \_SB_.PCI0.GPP0.PEGP handle
nouveau 0000:01:00.0: enabling device (0000 -> 0003)
nouveau 0000:01:00.0: NVIDIA GA104 (b74000a1)
nouveau 0000:01:00.0: bios: version 94.04.3f.00.c4
Loading firmware: nvidia/ga104/nvdec/scrubber.bin
nouveau 0000:01:00.0: fb: 8192 MiB GDDR6
nouveau 0000:01:00.0: DRM: VRAM: 8192 MiB
nouveau 0000:01:00.0: DRM: GART: 536870912 MiB
nouveau 0000:01:00.0: DRM: BIT table 'A' not found
nouveau 0000:01:00.0: DRM: BIT table 'L' not found
nouveau 0000:01:00.0: DRM: TMDS table version 2.0
nouveau 0000:01:00.0: DRM: DCB version 4.1
nouveau 0000:01:00.0: DRM: DCB outp 00: 02800f66 04610020
nouveau 0000:01:00.0: DRM: DCB outp 01: 01811f36 04600010
nouveau 0000:01:00.0: DRM: DCB outp 02: 01811f32 00020010
nouveau 0000:01:00.0: DRM: DCB outp 03: 01022f46 04600020
nouveau 0000:01:00.0: DRM: DCB outp 04: 01022f42 00020020
nouveau 0000:01:00.0: DRM: DCB outp 05: 02033f52 00020010
nouveau 0000:01:00.0: DRM: DCB conn 00: 00020047
nouveau 0000:01:00.0: DRM: DCB conn 01: 00001146
nouveau 0000:01:00.0: DRM: DCB conn 02: 00002246
nouveau 0000:01:00.0: DRM: DCB conn 03: 00010361
nouveau 0000:01:00.0: DRM: MM: using COPY for buffer copies
nouveau 0000:01:00.0: [drm] Cannot find any crtc or sizes
[drm] Initialized nouveau 1.3.1 20120801 for 0000:01:00.0 on minor 1
nouveau 0000:01:00.0: [drm] Cannot find any crtc or sizes
nouveau 0000:01:00.0: [drm] Cannot find any crtc or sizes
nouveau 0000:01:00.0: vgaarb: changed VGA decodes: olddecodes=io+mem,decodes=none:owns=none
amdgpu 0000:06:00.0: vgaarb: changed VGA decodes: olddecodes=io+mem,decodes=none:owns=none
nouveau 0000:01:00.0: can't change power state from D3cold to D0 (config space inaccessible)
nouveau 0000:01:00.0: can't change power state from D3cold to D0 (config space inaccessible)
nouveau 0000:01:00.0: can't change power state from D3cold to D0 (config space inaccessible)
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G                T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x2b/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/tu102.c:31 tu102_bar_bar2_wait+0xd1/0xe0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:tu102_bar_bar2_wait+0xd1/0xe0 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 67 50 4d 85 e4 75 03 4c 8b 27 e8 f1 fe 77 fc 4c 89 e2 48 c7 c7 52 60 68 c0 48 89 c6 e8 c6 08 df fc <0f> 0b eb a9 e8 b6 29 e9 fc 66 0f 1f 44 00 00 f3 0f 1e fa 41 54 53
RSP: 0018:ffffaefa4327f888 EFLAGS: 00010246
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff9406b0f39d60 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: ffff9406102e71a0
R13: ffff940670d2d400 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_bar_bar2_init+0x40/0x50 [nouveau]
 nvkm_instmem_init+0x45/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/g84.c:35 g84_bar_flush+0xf9/0x110 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:g84_bar_flush+0xf9/0x110 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 6f 50 4d 85 ed 75 03 4c 8b 2f e8 e9 07 78 fc 4c 89 ea 48 c7 c7 1c 60 68 c0 48 89 c6 e8 be 11 df fc <0f> 0b eb a8 e8 ae 32 e9 fc 66 66 2e 0f 1f 84 00 00 00 00 00 0f 1f
RSP: 0018:ffffaefa4327f830 EFLAGS: 00010046
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda898 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000246
R13: ffff9406102e71a0 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nv50_instobj_release+0x2f/0xc0 [nouveau]
 nvkm_instobj_load+0x4a/0xb0 [nouveau]
 nvkm_instmem_init+0x61/0x80 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/subdev/bar/tu102.c:58 tu102_bar_bar1_wait+0xd1/0xe0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:tu102_bar_bar1_wait+0xd1/0xe0 [nouveau]
Code: 8b 40 10 48 8b 78 10 4c 8b 67 50 4d 85 e4 75 03 4c 8b 27 e8 11 fe 77 fc 4c 89 e2 48 c7 c7 52 60 68 c0 48 89 c6 e8 e6 07 df fc <0f> 0b eb a9 e8 d6 28 e9 fc 66 0f 1f 44 00 00 f3 0f 1e fa 49 89 c8
RSP: 0018:ffffaefa4327f8a0 EFLAGS: 00010246
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940600bda840 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: ffff9406102e71a0
R13: ffff940670d2d400 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_bar_init+0x2d/0x50 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
------------[ cut here ]------------
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/outp.c:252 nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Code: 0f 87 4e 17 09 00 49 89 6c 24 38 e9 63 ff ff ff 0f 0b e9 5c ff ff ff 48 8b 45 08 83 78 38 03 0f 86 4e ff ff ff e9 00 17 09 00 <0f> 0b e9 42 ff ff ff 4c 89 e6 48 89 ef e8 c2 01 00 00 e9 32 ff ff
RSP: 0018:ffffaefa4327f880 EFLAGS: 00010246
RAX: 0000000000000000 RBX: 0000000000000004 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff9406a07ae800 R08: ffff9406313be9c0 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x59/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: i2c: aux 0006: begin idle timeout ffffffff
nouveau 0000:01:00.0: i2c: aux 0006: begin idle timeout ffffffff
------------[ cut here ]------------
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/outp.c:252 nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Code: 0f 87 4e 17 09 00 49 89 6c 24 38 e9 63 ff ff ff 0f 0b e9 5c ff ff ff 48 8b 45 08 83 78 38 03 0f 86 4e ff ff ff e9 00 17 09 00 <0f> 0b e9 42 ff ff ff 4c 89 e6 48 89 ef e8 c2 01 00 00 e9 32 ff ff
RSP: 0018:ffffaefa4327f880 EFLAGS: 00010246
RAX: 0000000000000000 RBX: 0000000000000004 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff9406a07ac800 R08: 00000000ffffbfff R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x59/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: i2c: aux 0003: begin idle timeout ffffffff
nouveau 0000:01:00.0: i2c: aux 0003: begin idle timeout ffffffff
------------[ cut here ]------------
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/outp.c:252 nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Code: 0f 87 4e 17 09 00 49 89 6c 24 38 e9 63 ff ff ff 0f 0b e9 5c ff ff ff 48 8b 45 08 83 78 38 03 0f 86 4e ff ff ff e9 00 17 09 00 <0f> 0b e9 42 ff ff ff 4c 89 e6 48 89 ef e8 c2 01 00 00 e9 32 ff ff
RSP: 0018:ffffaefa4327f880 EFLAGS: 00010246
RAX: 0000000000000000 RBX: 0000000000000002 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940610a0f900 R08: 00000000fffffffb R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x59/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
------------[ cut here ]------------
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/outp.c:252 nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Code: 0f 87 4e 17 09 00 49 89 6c 24 38 e9 63 ff ff ff 0f 0b e9 5c ff ff ff 48 8b 45 08 83 78 38 03 0f 86 4e ff ff ff e9 00 17 09 00 <0f> 0b e9 42 ff ff ff 4c 89 e6 48 89 ef e8 c2 01 00 00 e9 32 ff ff
RSP: 0018:ffffaefa4327f880 EFLAGS: 00010246
RAX: 0000000000000000 RBX: 0000000000000004 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff9406a07ae400 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x59/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: i2c: aux 0004: begin idle timeout ffffffff
nouveau 0000:01:00.0: i2c: aux 0004: begin idle timeout ffffffff
------------[ cut here ]------------
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/outp.c:252 nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Code: 0f 87 4e 17 09 00 49 89 6c 24 38 e9 63 ff ff ff 0f 0b e9 5c ff ff ff 48 8b 45 08 83 78 38 03 0f 86 4e ff ff ff e9 00 17 09 00 <0f> 0b e9 42 ff ff ff 4c 89 e6 48 89 ef e8 c2 01 00 00 e9 32 ff ff
RSP: 0018:ffffaefa4327f880 EFLAGS: 00010246
RAX: 0000000000000000 RBX: 0000000000000002 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940610a0f280 R08: 00000000ffffffbf R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x59/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
------------[ cut here ]------------
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/outp.c:252 nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:nvkm_outp_init+0x1bc/0x1e0 [nouveau]
Code: 0f 87 4e 17 09 00 49 89 6c 24 38 e9 63 ff ff ff 0f 0b e9 5c ff ff ff 48 8b 45 08 83 78 38 03 0f 86 4e ff ff ff e9 00 17 09 00 <0f> 0b e9 42 ff ff ff 4c 89 e6 48 89 ef e8 c2 01 00 00 e9 32 ff ff
RSP: 0018:ffffaefa4327f880 EFLAGS: 00010246
RAX: 0000000000000000 RBX: 0000000000000002 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff940610a0f600 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: 0000000000000000
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x59/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: timer: stalled at ffffffffffffffff
------------[ cut here ]------------
nouveau 0000:01:00.0: timeout
WARNING: CPU: 5 PID: 38637 at drivers/gpu/drm/nouveau/nvkm/engine/disp/tu102.c:42 tu102_disp_init+0x543/0x560 [nouveau]
Modules linked in: nf_tables nfnetlink btusb btrtl cdc_ether btbcm btintel usbnet btmtk bluetooth r8152 mii nouveau xt_hl ip6t_rt ipt_REJECT nf_reject_ipv4 xt_LOG nf_log_syslog xt_limit xt_addrtype xt_tcpudp xt_conntrack ip6table_filter ip6_tables nf_conntrack_netbios_ns nf_conntrack_broadcast nf_nat_ftp nf_nat nf_conntrack_ftp nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 iptable_filter ip_tables x_tables bpfilter sch_fq_codel fuse
CPU: 5 PID: 38637 Comm: X Tainted: G        W       T 5.18.14-gentoo-TPP #1
Hardware name: LENOVO 82JQ/LNVNB161216, BIOS GKCN54WW 05/05/2022
RIP: 0010:tu102_disp_init+0x543/0x560 [nouveau]
Code: 24 20 48 8b 40 10 48 8b 78 10 4c 8b 67 50 4d 85 e4 74 20 e8 af 2f 71 fc 4c 89 e2 48 c7 c7 1f b7 68 c0 48 89 c6 e8 84 39 d8 fc <0f> 0b b8 f0 ff ff ff eb 92 4c 8b 27 eb db e8 6a 5a e2 fc 66 2e 0f
RSP: 0018:ffffaefa4327f828 EFLAGS: 00010246
RAX: 0000000000000000 RBX: ffff940670d2d400 RCX: 0000000000000000
RDX: 0000000000000000 RSI: 0000000000000000 RDI: 0000000000000000
RBP: ffff9406e0c4a810 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000000 R12: ffff9406102e71a0
R13: ffff9406e0c4a810 R14: 0000000000000000 R15: 0000059e15832fd7
FS:  00007fe84b0f6980(0000) GS:ffff940c11d40000(0000) knlGS:0000000000000000
CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
CR2: 000056472358a439 CR3: 0000000181e78000 CR4: 0000000000750ee0
PKRU: 55555554
Call Trace:
 <TASK>
 nvkm_disp_init+0x7c/0xf0 [nouveau]
 nvkm_engine_init+0xb2/0x130 [nouveau]
 nvkm_subdev_init+0x9b/0xf0 [nouveau]
 ? ktime_get+0x3b/0xb0
 nvkm_device_init+0x12a/0x1d0 [nouveau]
 nvkm_udevice_init+0x48/0x70 [nouveau]
 nvkm_object_init+0x3d/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nvkm_object_init+0x72/0x130 [nouveau]
 nouveau_do_resume+0x26/0xd0 [nouveau]
 nouveau_pmops_runtime_resume+0x80/0x160 [nouveau]
 pci_pm_runtime_resume+0xa5/0xd0
 ? pci_pm_freeze_noirq+0x120/0x120
 __rpm_callback+0x35/0x120
 ? pci_pm_freeze_noirq+0x120/0x120
 rpm_callback+0x6a/0x80
 rpm_resume+0x50b/0x790
 __pm_runtime_resume+0x49/0x80
 nouveau_drm_open+0x70/0x1f0 [nouveau]
 drm_file_alloc+0x198/0x270
 drm_open+0xde/0x270
 drm_stub_open+0xc2/0x160
 chrdev_open+0xd2/0x230
 ? cdev_device_add+0xa0/0xa0
 do_dentry_open+0x160/0x3c0
 path_openat+0xd23/0x1270
 do_filp_open+0xa1/0x160
 do_sys_openat2+0xc3/0x190
 __x64_sys_openat+0x54/0xa0
 do_syscall_64+0x60/0x90
 entry_SYSCALL_64_after_hwframe+0x49/0xb3
RIP: 0033:0x7fe84b8c5f99
Code: 41 00 3d 00 00 41 00 74 58 64 8b 04 25 18 00 00 00 85 c0 75 7c 41 89 da 44 89 e2 48 89 ee bf 9c ff ff ff b8 01 01 00 00 0f 05 <48> 3d 00 f0 ff ff 0f 87 9b 00 00 00 48 8b 54 24 28 64 48 2b 14 25
RSP: 002b:00007ffd41adef40 EFLAGS: 00000246 ORIG_RAX: 0000000000000101
RAX: ffffffffffffffda RBX: 0000000000000000 RCX: 00007fe84b8c5f99
RDX: 0000000000080002 RSI: 000056299fbd3ad0 RDI: 00000000ffffff9c
RBP: 000056299fbd3ad0 R08: 0000000000000000 R09: 0000000000000000
R10: 0000000000000000 R11: 0000000000000246 R12: 0000000000080002
R13: 000056299fbd3ad0 R14: 000056299fbd3ad0 R15: 000056299fbd21e0
 </TASK>
---[ end trace 0000000000000000 ]---
nouveau 0000:01:00.0: disp: init failed, -16
nouveau 0000:01:00.0: init failed with -16
nouveau: X[4313]:00000000:00000080: init failed with -16
nouveau: DRM-master:00000000:00000000: init failed with -16
nouveau: DRM-master:00000000:00000000: init failed with -16
nouveau 0000:01:00.0: DRM: Client resume failed with error: -16
nouveau 0000:01:00.0: DRM: resume failed with: -16
bbswitch: loading out-of-tree module taints kernel.
bbswitch: version 0.8
bbswitch: Found discrete VGA device 0000:01:00.0: \_SB_.PCI0.GPP0.PEGP
bbswitch: Found discrete VGA device 0000:06:00.0: \_SB_.PCI0.GP17.VGA_
bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xF8,0xD8,0x86,0xA4,0xDA,0x0B,0x1B,0x47,0xA7,0x2B,0x60,0x42,0xA6,0xB5,0xBE,0xE0} 0x100 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
bbswitch: failed to evaluate \_SB_.PCI0.GP17.VGA_._DSM {0xA0,0xA0,0x95,0x9D,0x60,0x00,0x48,0x4D,0xB3,0x4D,0x7E,0x5F,0xEA,0x12,0x9F,0xD4} 0x102 0x0 {0x00,0x00,0x00,0x00}: AE_NOT_FOUND
bbswitch: No suitable _DSM call found.
```

How I see it, bbswitch isn't causing the kernel panics, but nouveau is. However, bbswitch also doesn't correctly detect those specific graphics cards.

Since bbswitch isn't even loaded, bumblebeed then has nothing to do:
```
bumblebeed[nnnn]: No switching method available. The dedicated card will always be on.
```

sys-kernel/gentoo-sources-6.0.11 (amdgpu and nouveau from the kernel)
sys-power/bbswitch-0.8_p20211129
x11-misc/bumblebee-3.2.1_p20210112-r4 USE="bbswitch" VIDEO_CARDS="nouveau -nvidia"

