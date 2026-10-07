# Monster Hunter Wilds (2246340)

- URL: https://github.com/ValveSoftware/Proton/issues/8206
- Repo: ValveSoftware/Proton (language: C++)
- State: open; created 2024-10-31T17:22:55Z; status ok; passes main

## Issue body

reporter (NONE) · CreatureDev · 2024-10-31T17:22:55Z · https://github.com/ValveSoftware/Proton/issues/8206

# Compatibility Report
- Name of the game with compatibility issues: Monster Hunter Wilds Beta
- Steam AppID of the game: 2246340

## System Information
- GPU: RTX 4070
- Video driver version: 550
- Kernel version: 6.8.0-40-generic
- Proton version: Experimental

## I confirm:
- [x] that I haven't found an existing compatibility report for this game.
- [x] that I have checked whether there are updates for my system available.

<!-- Please add `PROTON_LOG=1 %command%` to the game's launch options and
attach the generated $HOME/steam-$APPID.log to this issue report as a file.
(Proton logs compress well if needed.)-->

## Symptoms <!-- What's the problem? -->

The game crashes on launch
It appears to be an nvidia exclusive issue. It is fixed using the latest vkd3d-proton build.
Can a new proton hotfix build be released including the vkd3d-proton changes?

## Reproduction

Launch the Monster Hunter Wilds beta on an nvidia system.


## Comment 2450444870

maintainer (MEMBER) · kisak-valve · 2024-10-31T17:31:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450444870

Hello @CreatureDev, the automated [bleeding edge] beta branch (https://github.com/ValveSoftware/Proton/wiki/Proton-Versions#proton-bleeding-edge) should include whatever upstream change to VKD3D-Proton you're interested in while you wait for that change to make it into a more formal release of Proton.

## Comment 2450622534

other (NONE) · JoseZancanaro · 2024-10-31T19:03:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450622534

Hi, using Proton-Experimental [bleeding-edge] fixed the initial crash that also used to happen for me.

Also, after the logo's screen, the following error happen:

![Screenshot_2024-10-31_15-51-04](https://github.com/user-attachments/assets/7164f5a7-f482-47ef-aa6e-1621f24ae72d)

Using `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` in the game's launch options on Steam fixed it, and now it works normally.

Now is just to wait for the open beta to be properly released.

## Comment 2450650359

reporter (NONE) · CreatureDev · 2024-10-31T19:20:20Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450650359

> Using `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` in the game's launch options on Steam fixed it, and now it works normally.

From what I understand this is a driver issue. I created an issue for it as well in the vkd3d-proton repo, though, if it can be fixed there.



## Comment 2450810336

other (NONE) · Zhaltor · 2024-10-31T21:02:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450810336

Game is crashing KDE Plasma on my end, and flickers in fullscreen. Same issues encountered on Dragons Dogma 2 since recent update, been unable to find a fix.

EDIT: Unlike DD2, running with Gamescope seems to fix the issue.

## Comment 2450850521

other (NONE) · Awlexus · 2024-10-31T21:32:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450850521

Hi, I can confirm that. Constant flickering and KDE crashing

## Comment 2450868219

other (NONE) · yoshiweegee · 2024-10-31T21:48:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450868219

Confirming the findings noted in https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450622534. Requiring use of self-built bleeding-edge, error after Re-Engine's splash, fixed with `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2`. Linux Mint 22, NVIDIA GeForce RTX 4070 550.120, Linux 6.8.0-48-generic x86_64

## Comment 2450962915

other (NONE) · foophoof · 2024-10-31T22:33:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450962915

Slightly different results for me, I had to switch to Proton Bleeding Edge in Steam, which allowed the game to start and compile the shaders and reach the "could not connect to servers" screen (as expected since the servers aren't up for another 4-5 hours) without any errors, no need to change any launch options. I'm also using KDE/Plasma and not seeing any flickering.

I'm on Bazzite 41, `Linux bazzite 6.11.5-307.bazzite.fc41.x86_64 #1 SMP PREEMPT_DYNAMIC Mon Oct 28 15:13:19 UTC 2024 x86_64 GNU/Linux`, with Nvidia driver 565.57.01 (current beta driver I believe, I guess the default on Bazzite, I haven't intentionally changed that) on an RTX 3080 Ti.

## Comment 2450996948

other (NONE) · woofr77 · 2024-10-31T23:07:12Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450996948

> Using `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` in the game's launch options on Steam fixed it, and now it works normally.

Tried this plus the bleeding edge experimental, with Void Linux, NVIDIA 550.127 drivers. Still crashes with the same error after RE logo.

EDIT: I just forgot to put %command% lol, fixed. It boots fine now.

## Comment 2451207502

other (NONE) · bk304 · 2024-11-01T03:05:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451207502

My game renders the menu HUD, but not any 3D. Its just a black screen with HUD.

bleeding edge proton experimental
amd 6750xt

## Comment 2451210470

other (NONE) · bk304 · 2024-11-01T03:09:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451210470

> My game renders the menu HUD, but not any 3D. Its just a black screen with HUD.
> 
> bleeding edge proton experimental amd 6750xt

Disabling the upscaller fixed it.
Both AMD FSR 3 and XeSS dont work.

## Comment 2451242105

other (NONE) · alairon · 2024-11-01T03:50:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451242105

> > My game renders the menu HUD, but not any 3D. Its just a black screen with HUD.
> > bleeding edge proton experimental amd 6750xt
> 
> Disabling the upscaller fixed it. Both AMD FSR 3 and XeSS dont work.

Played around with the settings. FSR 3 does work, but only when I set the upscaling mode to "AMD Native AA". It was also the only mode that let me see what I was doing in the character creation menu.

Experimental - bleeding edge/AMD RX6500

## Comment 2451246909

other (NONE) · sorat0mo · 2024-11-01T03:56:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451246909

Once in the main game, the graphics are, to say the least, "not so nice":

![20241101110833_1](https://github.com/user-attachments/assets/07e025a1-8de9-49c5-8520-3549a625e462)
![20241101111115_1](https://github.com/user-attachments/assets/e3c951ce-8671-477c-b892-16c7d67518ff)

Broken textures everywhere. Proton Experimental bleeding edge. NV 3060Ti, Driver version 560.35.03/565.57.01.

## Comment 2451247947

other (NONE) · asier-ochoa · 2024-11-01T03:58:16Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451247947

> Once in the main game, the graphics are, to say the least, "not so nice":
> 
> ![20241101110833_1](https://private-user-images.githubusercontent.com/11853019/382179305-07e025a1-8de9-49c5-8520-3549a625e462.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzA0MzM3NDUsIm5iZiI6MTczMDQzMzQ0NSwicGF0aCI6Ii8xMTg1MzAxOS8zODIxNzkzMDUtMDdlMDI1YTEtOGRlOS00OWM1LTg1MjAtMzU0OWE2MjVlNDYyLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMDElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTAxVDAzNTcyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTRkMTZmZjYwM2ZhMGNhMTNkNjYyZWU2ZDQwZTc2Zjg2ODhkYTA2NmZhOGYxNmU1MjI3YWMxM2Q3OGU3YWU4NmUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.JppnY-wweLLIK5OQi3mzSck4WW7G60fT3EsdXrF1gKs) ![20241101111115_1](https://private-user-images.githubusercontent.com/11853019/382179307-e3c951ce-8671-477c-b892-16c7d67518ff.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzA0MzM3NDUsIm5iZiI6MTczMDQzMzQ0NSwicGF0aCI6Ii8xMTg1MzAxOS8zODIxNzkzMDctZTNjOTUxY2UtODY3MS00NzdjLWI4OTItMTZjN2Q2NzUxOGZmLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMDElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTAxVDAzNTcyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTZmOTQxMGMzZTFkMWU0NDA0ZTJiZWQzNjRjM2I3MWMwMzM1NGMyODBkZDZmMmUwZTA1MTU1NjdlNmU3YjVjODcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.hvdY6ZTcJGTaJZ6ZMrGIHIzKpPWb9W-iiErrILhOtEw)
> 
> Broken textures everywhere. Proton Experimental bleeding edge. NV 3060Ti, Driver version 560.35.03/565.57.01.

Can confirm that I'm having the exact same issue on the same drivers with an RTX 3080.

## Comment 2451263690

other (NONE) · tmlaw01 · 2024-11-01T04:16:26Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451263690

Adding to the above images, these aren't texture problems they appear to be widespread vertex/geometry shading problems. For the near-terrain geometry turning the appropriate settings down to low gets the terrain to actually appear on Nvidia cards (565.57.01). The most notable difference between the settings that I could notice at least by eye was possible displacement mapping which may have been disabled on low settings. Other effects that cause heavy artifacting are fur shading, and animation breaking for any skeletal meshes they are attached to, which can lead to detached limbs and vertex explosions in the most extreme cases.

If there's anything you would like me to try to grab such as API traces please let me know.

## Comment 2451266557

other (NONE) · laviphon · 2024-11-01T04:19:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451266557

Can confirm the same artifacting and performance issues on an RTX 3090.

Tried on Proton Experimental Bleeding Edge as well as GE 9-17

## Comment 2451267728

other (NONE) · sorat0mo · 2024-11-01T04:21:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451267728

> Adding to the above images, these aren't texture problems they appear to be widespread vertex/geometry shading problems. For the near-terrain geometry turning the appropriate settings down to low gets the terrain to actually appear on Nvidia cards (565.57.01). The most notable difference between the settings that I could notice at least by eye was possible displacement mapping which may have been disabled on low settings. Other effects that cause heavy artifacting are fur shading, and animation breaking for any skeletal meshes they are attached to, which can lead to detached limbs and vertex explosions in the most extreme cases.

Setting that option to down did fix the terrain artifacts.

## Comment 2451302967

other (NONE) · ZRivait · 2024-11-01T05:08:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451302967

Running into an issue where game the crashes and completely locks up my system. Running Arch 6.11.5-arch1-1, AMD RX6800XT, mesa 1:24.2.6-1, proton bleeding edge, and running the game in gamescope. The crashes seem to happen randomly, sometimes after 5 minutes, the longest being after 30 minutes. From the proton log I'm getting a VK_ERROR_DEVICE_LOST. I've removed vk_image_aspect warning lines from the log as it seemed to be generating them every frame. The original log was 500MB.
[steam-3065170.log](https://github.com/user-attachments/files/17596219/steam-3065170.log)


## Comment 2451303557

other (NONE) · rfguimaraes · 2024-11-01T05:09:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451303557

I also experienced really bad artifacting and performance issues with RX6500XT and Proton Experimental, GE 9-16, and GE 9-17 on Ubuntu 22.04

## Comment 2451340128

other (NONE) · Doomguy1364 · 2024-11-01T05:54:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451340128

> Running into an issue where game the crashes and completely locks up my system. Running Arch 6.11.5-arch1-1, AMD RX6800XT, mesa 1:24.2.6-1, proton bleeding edge, and running the game in gamescope. The crashes seem to happen randomly, sometimes after 5 minutes, the longest being after 30 minutes. From the proton log I'm getting a VK_ERROR_DEVICE_LOST. I've removed vk_image_aspect warning lines from the log as it seemed to be generating them every frame. The original log was 500MB. [steam-3065170.log](https://github.com/user-attachments/files/17596219/steam-3065170.log)

I also had the beta completely crash my computer, below is a cut from my journal.

After some further testing I was also able to get a similar crash in another game (SCP:5K) using vkd3d. The only difference between the two is in SCP:5K the system would soft recover eventually.

Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:7 pasid:32796)
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:  in process MonsterHunterWi pid 14795 thread vkd3d_queue pid 14951)
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x0000010000008000 from client 10
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00701430
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x0
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
Oct 31 22:14:23 doompc kernel: amdgpu 0000:03:00.0: amdgpu:          RW: 0x0
Oct 31 22:14:33 doompc kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=16021259, emitted seq=16021261
Oct 31 22:14:33 doompc kernel: amdgpu 0000:03:00.0: amdgpu: Process information: process MonsterHunterWi pid 14795 thread vkd3d_queue pid 14951
Oct 31 22:14:35 doompc kernel: amdgpu 0000:03:00.0: amdgpu: MES failed to respond to msg=REMOVE_QUEUE
Oct 31 22:14:35 doompc kernel: [drm:amdgpu_mes_unmap_legacy_queue [amdgpu]] *ERROR* failed to unmap legacy queue
Oct 31 22:14:36 doompc kernel: [drm:gfx_v11_0_hw_fini [amdgpu]] *ERROR* failed to halt cp gfx
Oct 31 22:14:36 doompc kwin_wayland[937]: kwin_wayland_drm: Pageflip timed out! This is a kernel bug
Oct 31 22:14:37 doompc kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
Oct 31 22:14:37 doompc systemd-coredump[15213]: [🡕] Process 1050 (Xwayland) of user 1000 dumped core.

System Specs:
OS: Arch Linux
DE: KDE Plasma 6.2.2 (Wayland)
KERNEL: 6.11.5-arch1-1
CPU: AMD Ryzen 7 7800X3D 8-Core
GPU: AMD Radeon RX 7900 XTX (radeonsi, navi31, LLVM 18.1.8, DRM 3.59, 6.11.5-arch1-1)
GPU DRIVER: 4.6 Mesa 24.2.6-arch1.1
RAM: 32 GB

## Comment 2451340603

other (NONE) · N4gtan · 2024-11-01T05:54:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451340603

Apart from the FSR/XeSS black screen and the weird textures issues, I'm having lot of stuttering with some textures and, sometimes, that stutter completely freezes my entire system forcing me to reboot.

OS: Arch with KDE Wayland
CPU: Ryzen 5 5600X
GPU: Nvidia GTX 1070
Video driver version: 565.57.01-1
Kernel version: 6.11.5.arch1-1
Proton version: Experimental + bleeding-edge

## Comment 2451354448

other (NONE) · minecraft2048 · 2024-11-01T06:10:17Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451354448

The beta seems to kill AMD GPU after running pretty perfectly for several minutes:

```
Nov 01 16:52:04 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=163945, emitted seq=163947
Nov 01 16:52:04 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: Process information: process MonsterHunterWi pid 9151 thread vkd3d_queue pid 9334
Nov 01 16:52:04 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU reset begin!
Nov 01 16:52:04 ifrit-hpc kernel: iommu ivhd1: AMD-Vi: Event logged [INVALID_DEVICE_REQUEST device=0000:00:00.0 pasid=0x00000 address=0xfffffffdf8000000 flags=0x0a00]
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: Dumping IP State
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: Dumping IP State Completed
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: MODE1 reset
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU mode1 reset
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU smu mode1 reset
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU reset succeeded, trying to resume
Nov 01 16:52:06 ifrit-hpc kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000800000).
Nov 01 16:52:06 ifrit-hpc kernel: [drm] VRAM is lost due to GPU reset!
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: PSP is resuming...
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: reserve 0xa00000 from 0x82fd000000 for PSP TMR
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: RAS: optional ras ta ucode is not available
Nov 01 16:47:42 ifrit-hpc kernel: Bluetooth: RFCOMM socket layer initialized
Nov 01 16:47:42 ifrit-hpc kernel: Bluetooth: RFCOMM ver 1.11
Nov 01 16:47:45 ifrit-hpc kernel: warning: `kdeconnectd' uses wireless extensions which will stop working for Wi-Fi 7 hardware; use nl80211
Nov 01 16:52:04 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=163945, emitted seq=163947
Nov 01 16:52:04 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: Process information: process MonsterHunterWi pid 9151 thread vkd3d_queue pid 9334
Nov 01 16:52:04 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU reset begin!
Nov 01 16:52:04 ifrit-hpc kernel: iommu ivhd1: AMD-Vi: Event logged [INVALID_DEVICE_REQUEST device=0000:00:00.0 pasid=0x00000 address=0xfffffffdf8000000 flags=0x0a00]
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: Dumping IP State
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: Dumping IP State Completed
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: MODE1 reset
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU mode1 reset
Nov 01 16:52:05 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU smu mode1 reset
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU reset succeeded, trying to resume
Nov 01 16:52:06 ifrit-hpc kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000800000).
Nov 01 16:52:06 ifrit-hpc kernel: [drm] VRAM is lost due to GPU reset!
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: PSP is resuming...
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: reserve 0xa00000 from 0x82fd000000 for PSP TMR
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: RAS: optional ras ta ucode is not available
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: SMU is resuming...
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413e00 (65.62.0)
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: SMU driver if version not matched
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: use vbios provided pptable
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: SMU is resumed successfully!
Nov 01 16:52:06 ifrit-hpc kernel: [drm] DMUB hardware initialized: version=0x02020020
Nov 01 16:52:06 ifrit-hpc kernel: [drm] kiq ring mec 2 pipe 1 q 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring sdma1 uses VM inv eng 13 on hub 0
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: recover vram bo from shadow start
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: recover vram bo from shadow done
Nov 01 16:52:06 ifrit-hpc kernel: amdgpu 0000:43:00.0: amdgpu: GPU reset(2) succeeded!
Nov 01 16:52:06 ifrit-hpc kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
Nov 01 16:52:06 ifrit-hpc kernel: [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
```

Arch Linux with 6.11.5-zen1-1-zen, PowerColor RX 6700 XT, KDE Plasma Wayland

## Comment 2451355084

other (NONE) · AmandaRoseChaqueta · 2024-11-01T06:10:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451355084

I can confirm both @N4gtan and @Doomguy1364 Issue on my end, The game will sometimes start to stutter so much that it will freeze my computer. One thing I had notice that repeats is that before it freezes, my monitor goes completely black and then the pc freezes, audio keeps playing and I'm forced to hit reset button, no way to recover. (Could this be maybe a GPU leak issue) 

OS: EndeavourOS 
DE: KDE Plasma 6.2.2 (Wayland)
Kernel: 6.11.5-arch1-1 (64-bit)
CPU: AMD Ryzen 5600
GPU: AMD RX6600
Proton version: Experimental and GE Proton 9-15

The most worrying part is the issue not being able to be properly fixed before the beta ends, hopefully capcom ends up extending the time period for it cuz even on the windows side it's rough.


## Comment 2451387298

other (NONE) · TNTftw21 · 2024-11-01T06:42:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451387298

Can confirm the terrain issues reported, even with all settings turned down to the absolute lowest. I agree that it appears to be an issue with terrain "chunks" having their vertices... misplaced. Gameplay objects - particles, characters, decorations, etc. - appear to be unaffected. Also, it might just be my system configuration specifically, but I'm not getting menu effects or certain dialogue.

OS: Mint 21.3
DE: Cinnaon 6.0.4
Kernel: 6.11.3-x64v3-xanmod2
CPU: AMD Ryzen 9 3900X
GPU: NVIDIA RTX 3060 Ti (LHR)
Proton: GE 9-18

Like with others, I had to use `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` to get the game passed the opening logos. Based on similar experiences I've had trying to get Monado working, I'm going to guess that this is a problem with NVIDIA either poorly implementing or outright not implementing features in their Linux drivers.

## Comment 2451407934

other (NONE) · minecraft2048 · 2024-11-01T07:05:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451407934

I managed to catch AMD GPU hang on Steam Deck:

```
[Nov 1 17:44] [drm] Fence fallback timer expired on ring comp_1.0.0
[Nov 1 18:03] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* ring sdma0 timeout, signaled seq=180525, emitted seq=180527
[  +0.000580] [drm:amdgpu_job_timedout [amdgpu]] *ERROR* Process information: process  pid 0 thread  pid 0
[  +0.000619] amdgpu 0000:04:00.0: amdgpu: GPU reset begin!
[  +0.093958] amdgpu 0000:04:00.0: amdgpu: MODE2 reset
[  +0.010152] amdgpu 0000:04:00.0: amdgpu: GPU reset succeeded, trying to resume
[  +0.000586] [drm] PCIE GART of 1024M enabled (table at 0x000000F43FC00000).
[  +0.000122] [drm] PSP is resuming...
[  +0.022186] [drm] reserve 0xa00000 from 0xf43e000000 for PSP TMR
[Nov 1 18:04] amdgpu 0000:04:00.0: amdgpu: SMU is resuming...
[  +0.000379] amdgpu 0000:04:00.0: amdgpu: SMU is resumed successfully!
[  +0.009927] [drm] DMUB hardware initialized: version=0x0300000A
[  +0.077513] [drm] Failed to add display topology, DTM TA is not initialized.
[  +0.014550] [drm] kiq ring mec 2 pipe 1 q 0
[  +0.002349] [drm] VCN decode and encode initialized successfully(under DPG Mode).
[  +0.000441] [drm] JPEG decode initialized successfully.
[  +0.000010] amdgpu 0000:04:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[  +0.000006] amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 1 on hub 0
[  +0.000004] amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 4 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 5 on hub 0
[  +0.000004] amdgpu 0000:04:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 6 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 7 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 8 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 9 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 10 on hub 0
[  +0.000004] amdgpu 0000:04:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 11 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring sdma0 uses VM inv eng 12 on hub 0
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[  +0.000004] amdgpu 0000:04:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[  +0.000003] amdgpu 0000:04:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[  +0.003168] amdgpu 0000:04:00.0: amdgpu: recover vram bo from shadow start
[  +0.000007] amdgpu 0000:04:00.0: amdgpu: recover vram bo from shadow done
[  +0.000110] amdgpu 0000:04:00.0: amdgpu: GPU reset(1) succeeded!
[  +1.135149] input: Steam Deck as /devices/pci0000:00/0000:00:08.1/0000:04:00.4/usb3/3-3/3-3:1.2/0003:28DE:1205.0003/input/input25
```

Steam Deck LCD

## Comment 2451446938

other (NONE) · lorentzforces · 2024-11-01T07:42:03Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451446938

For anyone trying to troubleshoot the terrain/vertex issue, the setting which seems to affect it is called **"Surface Quality"**, and it appears **ONLY** when accessing graphics options via the main menu.

**If you access the graphics settings menu while loaded into the world, this option _will not_ appear.**

## Comment 2451484663

other (NONE) · pixelcluster · 2024-11-01T08:12:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451484663

@minecraft2048 The sdma0 ring hanging is most likely unrelated to the game, that issue should go away if you update to SteamOS 3.6.

(To be clear, this is a different issue compared to the other GPU hangs where for example "ring gfx_0.0.0" times out. These gfx ring timeouts might not be fixed in 3.6, but the SDMA timeout is.)

## Comment 2451521212

other (NONE) · jn64 · 2024-11-01T08:41:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451521212

I get identical amdgpu crash (page fault in thread vkd3d_queue) as https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451340128. Graphics freeze after a few minutes while changing settings in main menu. Sound was still playing normally (not frozen or looping).

I can recover the system using `Alt-SysRq r e i` to kill Xorg, but after such crash it's safer to reboot anyway.

OS: Fedora Linux 39 (Thirty Nine)
KERNEL: 6.11.5-100.fc39.x86_64
CPU: Intel Core i5-8400 @ 2.80GHz
GPU: AMD Radeon RX 6600 (radeonsi, navi23, LLVM 17.0.6, DRM 3.59, 6.11.5-100.fc39.x86_64)
GPU DRIVER: 4.6 Mesa 23.3.6
RAM: 16 GB
Proton Experimental Bleeding Edge (1730411043 experimental-bleeding-edge-9.0-131609-20241031-p824747-w9c0d54-df74b2c-vdd7ad6)

---

Update: setting all graphics settings to the absolute lowest possible, including 1280x720 resolution and 30fps cap, allowed me to play the game for 1hr+ before crashing.

## Comment 2451571176

other (NONE) · Zhaltor · 2024-11-01T09:18:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451571176

Cannot change any settings in game due to menu looping, game isn't unresponsive but it shares the same issues as Dragons Dogma 2 does for me where I cannot use the options menu. 

## Comment 2451579175

other (NONE) · NextWork123 · 2024-11-01T09:25:12Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451579175

for me i don't have issues to go into the game but isn't working fsr3 and intel xess with my rx 6600 tested with proton-exp :/ if i put fsr3 or intel xess i gonna have black screen (seem it needs HAGS) 

## Comment 2451622066

other (NONE) · Eckoa · 2024-11-01T10:00:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451622066

> for me i don't have issues to go into the game but isn't working fsr3 and intel xess with my rx 6600 tested with proton-exp :/ if i put fsr3 or intel xess i gonna have black screen (seem it needs HAGS)

thats not only a linux things its happening to windows users also

## Comment 2451623727

other (NONE) · NextWork123 · 2024-11-01T10:01:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451623727

> > for me i don't have issues to go into the game but isn't working fsr3 and intel xess with my rx 6600 tested with proton-exp :/ if i put fsr3 or intel xess i gonna have black screen (seem it needs HAGS)
> 
> thats not only a linux things its happening to windows users also

oh ok thanks for reporting


## Comment 2451658967

other (NONE) · neon-grim · 2024-11-01T10:29:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451658967

> reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451302967

I'm having the same issue. Game crashes after a certain amount of time, be it 5-30min. Engaging the monster seems to speed up the crash. It doesnt lock up my desktop, its able to recover from the crash.

- Distro: Nixos Unstable
- Kernel: 6.11.5-LQX
- Driver: Mesa 24.2.4
- Compositor: Hyprland
- Proton: GE-Proton-18 & Experimental
- GPU: 7900XTX

Now it actually took my desktop, here is my crash log:
[crashLog.txt](https://github.com/user-attachments/files/17599283/crashLog.txt)


## Comment 2451711600

other (NONE) · weeviltime · 2024-11-01T11:15:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451711600

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451484663

Some of comments about GPU Reset, soft recovery is most likely not related to the game as mentioned. Due to Kernel reports that shows those problems occurring on other instances.

It seems the newest kernels (6.10.5+) have this problem setting up Memory Clock, Boost, Power Capacity way beyond the specifications. I myself had to rollback Linux Kernel to stop from random AMDGPU resets/recovery, it was happening playing WoW and I do have a good machine that would not warrant such problems. But most of them I can only say for AMDGPU users like me.

[Like this Issue in the Kernel/AMDGPU Gitlab](https://gitlab.freedesktop.org/drm/amd/-/issues/3698)
[You can also see many others with similar symptoms.](https://gitlab.freedesktop.org/drm/amd/-/issues/?sort=created_date&state=opened&search=reset&first_page_size=20)

* Distro: ArchLinux
* Kernel: 6.10.5-arch1-1
* Compositor: (yet to test Sway). KDE (latest)
* Proton: Experimental & GE-Proton-17
* Video Card:
  * Driver: AMD AMD Radeon RX 7900 XT (radeonsi, navi31, LLVM 18.1.8, DRM 3.57, 6.10.5-arch1-1)
  * Driver Version: 4.6 (Compatibility Profile) Mesa 24.2.6-arch1.1
  * It's actually AMD Radeon RX Sapphire Pulse 7900XT

## Comment 2451738305

other (NONE) · weeviltime · 2024-11-01T11:39:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451738305

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451711600

I am also reporting that updating to the new MESA (24.2.6-arch1-1 which I did couple of hours ago), and also playing on Sway the game is running smooth! Unlike yesterday at launch which was a stutter mess and random crashes.

Did not upgraded Kernel as of yet due to my comment above.

## Comment 2451741234

other (NONE) · Doomguy1364 · 2024-11-01T11:42:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451741234

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451711600

Not saying you're incorrect, but there definitely has to be something deeper than just a power overdraw/clockrate issue; I was able to play through the entire Silent Hill 2 remake on kernel 6.11.5 without any crashes.

The game maxed out my GPU for the entire 16 hours I played it, during two long play sessions of about 8 hours each, there wasn't a single GPU hang nor crash of the game itself.

System Specs:
OS: Arch Linux
DE: KDE Plasma 6.2.2 (Wayland)
KERNEL: 6.11.5-arch1-1
CPU: AMD Ryzen 7 7800X3D 8-Core
GPU: AMD Radeon RX 7900 XTX (radeonsi, navi31, LLVM 18.1.8, DRM 3.59, 6.11.5-arch1-1)
GPU DRIVER: 4.6 Mesa 24.2.6-arch1.1
RAM: 32 GB

## Comment 2451744330

other (NONE) · weeviltime · 2024-11-01T11:44:58Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451744330

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451741234

You are completely correct, but we do have different GPUs, if I upgrade my Kernel back to latest it is set up as 7900XTX, which are way beyond my actual GPU which is Pulse 7900XT.

Both our cases are anecdotal but I wanted to leave the possible cause here, what may work for me, may not work for you, but if it helps one person out there, then its worth.

Good hunting friend, may we cross paths in Hope.

## Comment 2451772994

other (NONE) · mtdlewald · 2024-11-01T12:09:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451772994

I have gpu hangs and tried downgrading kernel. It didn't fix anything for me.

System Specs:
OS: Arch Linux
DE: SwayWM
KERNEL: 6.11.6-zen1-1-zen
CPU: AMD Ryzen 7 5800X3D 
GPU: AMD Radeon RX 6800 XT 
GPU DRIVER: 4.6 Mesa 24.2.6-arch1.1
RAM: 32 GB

## Comment 2451829084

other (NONE) · alosarjos · 2024-11-01T12:56:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451829084

Does somebody knows if there is some issue with VRAM usage with Proton or something?

Game settings says game should by around 6.64Gb and some other stuff is filling 1.06GB with a total usage of 7.70Gb but MangoHud is reporting 11.7 GiB Vram usage...

I know that unused ram is wasted ram, but I'm not sure if that happens here too

![Captura desde 2024-11-01 13-52-47](https://github.com/user-attachments/assets/5ab2b4e2-0b79-4e68-b4be-fcba7efaa0d7)


## Comment 2451894539

other (NONE) · AnriApricot · 2024-11-01T13:42:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451894539

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450622534

also just got this error, though it was actually ingame. Will try that fix, had only come here to report the error myself, and report back
EDIT: Getting a playable game

## Comment 2451901124

other (NONE) · Recipient4626 · 2024-11-01T13:47:16Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451901124

> [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451484663)

I had this GPU reset problem on my system too (XFX 7900XTX tested on kernels from 6.1 to 6.11), and using `corectrl` to force specified clocks made the system completely stable.
Give it a try :)

Yet Wilds gives
`kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, but soft recovered`
and is the only game that gives this error, so it could be something specific to Wilds.

Also I noticed that GPU reset comes sooner as graphics settings go higher, and a reset can come within a few seconds on Ultra.

System Specs:
```
OS: Arch Linux
DE: KDE Plasma 6.2.2-1 (Wayland)
KERNEL: 6.11.5.arch1-1
CPU: AMD Ryzen 7 7800X3D
GPU: AMD Radeon RX 7900 XTX
GPU DRIVER: mesa 1:24.2.6-1
RAM: 64 GB
```

## Comment 2451909671

other (NONE) · Billli11 · 2024-11-01T13:52:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451909671

For black screen when setting a resolution scale that is not 100 or any upscaling method.
Adding env `VKD3D_CONFIG=disable_uav_compression` should workaround the issue.
REF:[vkd3d-proton pr 2184](https://github.com/HansKristian-Work/vkd3d-proton/pull/2184)

edit: PR2184 has been merged. It should be in proton experimental bleeding edge in next update, should be few hours from now.

## Comment 2451926283

other (NONE) · neon-grim · 2024-11-01T14:03:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451926283

> reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451901124

I basically have the same build as you, to what did you set your clocks? 

> reply https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451909671

works!

## Comment 2451943969

other (NONE) · Recipient4626 · 2024-11-01T14:14:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451943969

My `corectrl` settings:
```
Power limit (W) : 327
Power Profile: 3D Fullscreen
GPU: 2482 MHz
Memory: 1249 MHz
```

## Comment 2452090248

other (NONE) · neon-grim · 2024-11-01T15:39:23Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452090248

> reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2451943969

Thanks, though it still crashes on my end.

## Comment 2452177205

other (NONE) · Vanane · 2024-11-01T16:30:11Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452177205

It's crashing on my machine as well.
It used to crash the entire OS, but now it's only crashing the game itself, sometimes KDE. I haven't seen anything that can relate to memory leak or temperature problem.
I don't think I have done much to explain why it doesn't crash the OS anymore though.

I'm using vulkan-radeon latest version. I used to use amdvlk, but changing for either of them doesn't seem to have any impacts.

I had several issues, most of them have been resolved :
- [x] Setting FSR on will display a black screen, except for the GUI which is unaffected.
	- "Solved" by setting the upscaling mode on "AMD Native AA"
	- Further solved by [this PR on vkd3d](https://github.com/HansKristian-Work/vkd3d-proton/pull/2184)
- [x] The terrain's vertices are unhinged and rendering sudden spikes, holes, walls and whatnot.
	- "Solved" by setting the terrain quality to "Low"
- [ ] Streaming the game on Discord (well, Vesktop) will severely impact the performances, and even crash the game at the second the screenshare is active. Streaming the monitor itself has the same effect.
	- It seems to be related to radeon-vulkan actually, as I don't remember having such problem with amdvlk.
- [ ] The game will crash after any period from 5 to 30 minutes
	- What I tried so far :
		- Using LACT and similar tools to impose another profile, limit the power consumption and GPU clocking, to no avail (tried 2430MHz and  2106MHz, without seemingly any impacts)
		- Using Proton Experimental, both stable and bleeding-edge releases, using Proton GE 9.15 to 9.18, without much difference, except older Proton versions might end in a crash on game boot.

I'm looking forward to test with Mesa 24.2.6, as well as for updates on Proton Experimental.


Still, it sounds promising to me, seeing how the game is fluid otherwise, and demanded little tweaking to get it to boot to actual gameplay.


OS: Arch Linux x86_64
Kernel: Linux 6.11.5-arch1-1
Display (PL2770H): 1920x1080 @ 120 Hz in 27" [External] *
Display (G27F): 1920x1080 @ 120 Hz in 27" [External]
DE: KDE Plasma 6.2.2
WM: KWin (Wayland)
CPU: AMD Ryzen 9 7900X3D (24) @ 5.66 GHz
GPU 1: AMD Radeon RX 7800 XT [Discrete]
GPU 2: AMD Raphael [Integrated]
Memory: 32GB
GPU Driver : Mesa 24.2.5, I'm waiting for the 24.2.6 to be available on Flatpak
Proton version : Experimental [bleeding-edge]


Some pics !
Former bug about the terrain vertices rendering
![Former bug about the terrain vertices rendering](https://github.com/user-attachments/assets/ce727a95-858e-45c5-aa67-0caf3ea2d6fb)
Former FSR-induced black screen bug
![Former FSR-induced black screen bug](https://github.com/user-attachments/assets/4569dd7a-3d7b-46c7-a27b-3a41bd5c2ea4)

Edit :
Small precision about the streaming thingy. It only makes a huge drop in fps when the game is in focus, AND when it's in fullscreen. When out of focus or windowed, it runs just fine.

Edit 2 :
Forgot to say ! I had somewhat of a similar experience with Hitman 3 a few days ago, the game crashing the whole OS after 30-60m of gameplay. This might be related, meaning it wouldn't be specific to some Capcom tech.

## Comment 2452199429

other (NONE) · weeviltime · 2024-11-01T16:41:22Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452199429

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452177205

Yes, I spoke a bit too soon. Same symptoms and tests, game crashes after 5 mins beyond. But no graphical glitch by any means.

## Comment 2452204396

other (NONE) · Keelhauled · 2024-11-01T16:44:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452204396

The crashing seems very similar to how it was in Dragons Dogma 2.
After a seemingly random amount of time hyprland just died completely.
Fortunately amdvlk didn't suffer from that so I just played the rest of DD2 with it.

## Comment 2452226959

other (NONE) · Vanane · 2024-11-01T16:58:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452226959

I'm gonna try playing on the lowest possible settings, windowed mode, and see how far it goes.

By the way, I just found out about that NVidia Reflex setting which seemingly forces GPUs to overclock, or something like that ? I don't know. Thing is, it was activated by default, and it can't be good on AMD hardware :eyes:

Let's see how it goes

Edit : It went quite well for a while, but eventually, it just crashed. So no chance on this side either.

## Comment 2452277045

other (NONE) · Awlexus · 2024-11-01T17:24:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452277045

Using gamescope I was able to configure the game, but only got to the title screen. Right after that my whole screen freezes and if I don't stop it, my GPU crashes. I can reproduce this with Proton Experimental and GE. 

```
System Specs:
OS: Arch Linux
DE: KDE Plasma 6.2.2 (Wayland)
KERNEL: 6.11.5-arch1-1-zen (tried without zen too)
CPU: AMD Ryzen 5 3600 6-Core Processor
GPU: AMD AMD Radeon RX 6900 XT (radeonsi, navi21, LLVM 18.1.8, DRM 3.59, 6.11.5-zen1-1-zen)
GPU DRIVER: 4.6 Mesa 24.2.6-arch1.1
RAM: 32 GB
```


## Comment 2452289187

other (NONE) · igxlin · 2024-11-01T17:31:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452289187

Update: switching to amdvlk cannot help. It crashed again.

---

I switched from radeon to amdvlk. The full screen mode freezes and only window mode works. However, it looks somehow more smoother.

No crash during my play time. I didn't play it for a long while. Not sure if amdvlk solves the crashing issue or not.

## Comment 2452326595

other (NONE) · Vorthas · 2024-11-01T17:55:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452326595

I switched from mesa to amdvlk and while it did let me play for longer, I still had a total system lock up/crash on the chatacabra fight, just more like 5 minutes in instead of 2 minutes in.  I did not use MangoHUD or gamemode when trying it out.

The crash manifested as all my monitors going black for a second then they come back but nothing updates, no sound, couldn't do anything except hard reboot.

All settings were set to high, on a 1440p monitor.  Turning Surface Quality to Low made the weird graphical glitching in the environment go away but the crash remained.

```
System Specs
OS: EndeavourOS
DE: MATE 1.28.2 (X11)
KERNEL: 6.11.5-arch1-1
CPU: AMD Ryzen 7 7800X3D
GPU: AMD AMD Radeon RX 7800 XT (radeonsi, navi32, LLVM 18.1.8, DRM 3.59, 6.11.5-arch1-1)
GPU DRIVER 4.6 (Compatibility Profile) Mesa 24.2.6-arch1.1
RAM: 64 GB
```

## Comment 2452329816

other (NONE) · Zhaltor · 2024-11-01T17:58:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452329816

Switching to amdvlk did resolve some issues but caused brand new ones, it actually let me change settings and stopped plasma from crashing, but it introduced a lot of new graphical artifacts, and the crashes are less frequent but instead of just closing the game, they now freeze my whole system.

## Comment 2452348763

other (NONE) · ToastedWookiee · 2024-11-01T18:10:42Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452348763

Also getting crashes, seeing GPU hangs, as well as one system lock-up within 30 minutes of playing. Running high settings FSR3 at 1440p.

Had to switch Surface Quality to low.

Using mesa-tkg as well as cachyos mesa 24.2.6, using cachyos-proton and bleeding-edge experimental

```
System Specs
OS: CachyOS
DE: Sway 1.10
KERNEL: Linux 6.11.6-2-cachyos - sched-ext: bpfland
CPU: Intel I9-9900k
GPU: Intel Arc A770 16GB
GPU DRIVER: 4.6 Mesa 24.3.0-devel (git-a39d6f5003)
RAM: 64 GB
```

## Comment 2452348920

other (NONE) · mtdlewald · 2024-11-01T18:10:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452348920

I had similar issues on Exoprimal and DD2. This is some RE Engine thing.

## Comment 2452447258

other (NONE) · braiam · 2024-11-01T19:13:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452447258

The game keeps capturing the cursor even if not being the active window. I'm not sure if that's a game issue or a Linux issue.

## Comment 2452466908

other (NONE) · Dwyriel · 2024-11-01T19:28:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452466908

I'm having severe artifacts problems with this game, models either disappearing for a few seconds or polygons being stretched into oblivion (had to do the first hunt completely blind because the screen was covered by just stretched pollies from the monster, but then game crashed after killing it so lost even that little bit of progress as well). 
Also experiencing frequent crashes. I tried recording the game but it just makes it crash even faster (in the first minute or so), [here's the few mins I was able to record](https://www.youtube.com/watch?v=0WqAvfuwb-Q).

I'm on nvidia and tried both driver versions 560.35.03 and the newest 565.57.01, as well as proton-experimental bleeding edge and proton-ge 9.18.

full system specs:
```
OS: ArchLinux
Kernel: 6.11.5-arch1-1
DE: Plasma 6.2.2 (X11)
WM: KWin
CPU: AMD Ryzen 7 5700X3D
GPU: NVIDIA GeForce RTX 3080 
Driver Version: 565.57.01
RAM: 16 GB
```

## Comment 2452480813

other (NONE) · ClearlyClaire · 2024-11-01T19:39:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452480813

I have the same `amdgpu: ring gfx_0.0.0. timeout` in `vkd3d_queue` that reliably occurs after a few minutes of otherwise perfectly-fine gameplay using Proton Experimental's bleeding edge.

```
OS: Debian (testing)
Kernel: 6.11.4-amd64
DE: Gnome 3 (X11)
CPU: AMD Ryzen 9 5950X
GPU: AMD Radeon RX 6900 XT (radeonsi, navi21, LLVM 19.1.1, DRM 3.59, 6.11.4-amd64)
Driver Version: 4.6 (Compatibility Profile) Mesa 24.2.4-1
```

## Comment 2452493662

other (NONE) · Iymarra · 2024-11-01T19:49:20Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452493662

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452466908

I'm also in this situation, running same gpu, same driver, just with Manjaro

## Comment 2452554978

other (NONE) · Green-Sky · 2024-11-01T20:37:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452554978

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452466908

I also had this, but after loading latest bleeding-edge now, it just crashes now (instead?) after ~1-2min.

## Comment 2452555967

other (NONE) · Tinter · 2024-11-01T20:38:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452555967

Been messing with this all evening here. Couldn't launch at first, until I tried Proton Experimental with bleeding edge. GE-Proton9-18 was worse, some models didn't render. Had to switch surface quality to low to get the ground to render properly, which can only be done in the settings from the main menu. Random polygons would still appear. Then I was stuck with occasional freezing, every 5-30 minutes my whole computer would freeze, before recovering after some 30 seconds, but the game would be stuck, although sound would be playing normally. A warning from the Kernel would appear in my log:
`kernel: NVRM: Xid (PCI:0000:01:00): 109, pid=352215, name=MonsterHunterWi, Ch 000000ca, errorString CTX SWITCH TIMEOUT, Info 0x5c0c2`

This is where I am now, lowering everything to the absolute minimum, with FSR on ultra performance seemed to actually improve stability, letting me play an hour before freezing, enough to actually do some content. After that, next attempt did not end in a freeze, but the random polygons would get so intense my whole screen started flickering leaving me unable to see anything. At first just whenever I looked in a specific direction, but soon it appeared no matter where I was looking and I could only navigate by minimap. Here's a not so helpful picture, as it doesn't convey how awful the flickering really was, but at least you can see how impossible it was to tell what was actually going on.
![image](https://github.com/user-attachments/assets/386eca08-d2bb-4c21-a56b-a76574b49eb3)

I don't know what about the settings actually made a difference (Just FSR?) or if it was even just a fluke. Out of 2 runs, it did not cause a lockup within 30 minutes.

```
OS: Arch Linux x86_64
Kernel: Linux 6.11.5-arch1-1
DE: KDE Plasma 6.2.2 (X11)
CPU: AMD Ryzen 5 7600X (12) @ 5.45 GHz
GPU 2: NVIDIA GeForce RTX 2080 Ti Rev. A
Driver Version: nvidia 560.35.03-17
```


## Comment 2452623199

other (NONE) · braiam · 2024-11-01T21:35:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452623199

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452480813

Whatever this crash is, it seems to only affect AMD GPU's, also no video quality configuration seems to affect the behavior. I didn't test with gamescope but I also don't expect anything different.

The way to reproduce it is to pass enough in-game time, and then move the camera (technically, is that something that wasn't in frame now becomes in frame, but moving the camera usually achieve the same results).

## Comment 2452629772

other (NONE) · IceBird3 · 2024-11-01T21:41:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452629772

Hello im quite new to linux and i have the freeze and audio issue already described here as well. 
Game works for like 5-15 mins and then goes into a full freeze for me although I still hear the sound and my friends talking on TS3 and they are also hearing me, my display is completely frozen and does not allow me to click on anything hence I have to restart my PC everytime that happens.


Using Proton Experimental
Idk what is important for the driver so i just put the whole info from my terminal regarding that:


My Specs: 
OS: Linux Mint 22
Kernel: Linux 6.8.0-48-generic
Architecture: x86-64
CPU: AMD Ryzen 7 5800X
GPU: Radeon RX 6800 XT
Driver:

Device-1: AMD Navi 21 [Radeon RX 6800/6800 XT / 6900 XT] driver: amdgpu
    v: kernel
  Display: x11 server: X.Org v: 21.1.11 with: Xwayland v: 23.2.6 driver: X:
    loaded: amdgpu unloaded: fbdev,modesetting,radeon,vesa dri: radeonsi
    gpu: amdgpu resolution: 1: 1920x1080 2: 2560x1440~165Hz 3: 1920x1080
  API: EGL v: 1.5 drivers: kms_swrast,radeonsi,swrast
    platforms: gbm,x11,surfaceless,device
  API: OpenGL v: 4.6 compat-v: 4.5 vendor: amd mesa v: PPA renderer: AMD
    Radeon RX 6800 XT (radeonsi navi21 LLVM 17.0.6 DRM 3.57 6.8.0-48-generic)
  API: Vulkan v: 1.3.275 drivers: N/A surfaces: xcb,xlib



## Comment 2452682224

other (NONE) · CoolMan-Al · 2024-11-01T22:41:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452682224

I am also getting the full gpu crash after a 10 or so minutes as well as the fsr3 not rendering anything bug.

Using Proton Experimental Bleeding Edge with gamemode and mangohud. Issue still happens without gamemode.

EndeavourOS 
Kernel: Linux 6.11.5-zen1-1-zen
DE: KDE Plasma 6.2.2 (Wayland)
CPU: AMD Ryzen 7 5700X
GPU: AMD Radeon RX 6700 XT
Mesa: 1:24.2.5-1
RAM: 32 GB

## Comment 2452825804

other (NONE) · Darkrium · 2024-11-02T03:09:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452825804

Joining the bandwagon to say I also have the exact same freezing issue. I have had mixed results lowering the settings as it seems to last a little longer? Maybe it's just luck and a fluke though.

Nobara 40
Kernel: 6.11.5-200.fsync.fc40.x86_64
DE: KDE Plasma 6.2.2 wayland
CPU: AMD Ryzen 7 5800X
GPU: RX 7800 XT
Mesa: 24.3.0
RAM: 16GB

## Comment 2452827681

other (NONE) · apoisonedgift · 2024-11-02T03:14:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452827681

Same as everyone else. Game crashes anywhere from instantly to 20ish minutes and there seems to be no pattern. Different settings and that don't seem to matter, running it on lowest vs highest makes no difference etc. It does seem like the game runs fairly decently when its not crashing though lol

Arch x86_64
Kernel: 6.11.5-arch1-1
DE: KDE Plasma 6.2.2 x11
CPU: Ryzen 3900XT
GPU: Radeon 6800XT
Mesa: 24.3.0
RAM: 32GB

## Comment 2452835601

other (NONE) · NickelWW · 2024-11-02T03:41:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452835601

same crashes as everyone else, same error in log as that one guy that uploaded his.
crashes usually happen within 5 minutes but a few times happened at more like 10 minutes. 
```
OS: Fedora Linux 41 (KDE Plasma)
KERNEL: 6.11.5-300.fc41.x86_64
CPU: 12th Gen Intel Core i9-12900K
GPU: Radeon RX 7900 XTX
GPU DRIVER: Mesa 24.2.5
RAM: 32 GB DDR4 3200mhz (XMP)
```

## Comment 2452922978

other (NONE) · NTrixner · 2024-11-02T08:42:17Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452922978

Have the same issue with freezing after around 10-20 minutes of gameplay
Tried experimental, GE-Proton9-11, and GE-Proton9-18

> OS: Manjaro KDE
> KERNEL: 6.10.13-3-MANJARO (64 Bit)
> CPU: AMD Ryzen 9 3900X
> GPU: Radeon RX 7900 XT
> GPU DRIVER: Mesa 24.2.4-arch1.0.1
> RAM: 64 GB DDR4 2133 MT/s

Logs are full of this warning:

> vkd3d-proton:vk_image_aspect_flags_from_d3d12: Invalid plane index 0 for format 0.
There's actually so many of these, that it completely blows up the file (180 MiB for about 20 minutes of gameplay), so I can't really attach it.

These are the errors in the log, at different points during the gameplay

> 75760.216:0124:0128:err:kerberos:kerberos_LsaApInitializePackage no Kerberos support, expect problems
> 75760.218:0124:0128:err:ntlm:ntlm_LsaApInitializePackage no NTLM support, expect problems
> 75783.563:0124:0218:err:combase:RoGetActivationFactory Failed to find library for L"Windows.Internal.System.Profile.RegionPolicyEvaluator"

And then at the end:

> radv/amdgpu: The CS has been cancelled because the context is lost. This context is guilty of a soft recovery.
> 76667.976:0124:01bc:err:vkd3d-proton:vkd3d_wait_for_gpu_timeline_semaphore: Failed to wait for Vulkan timeline semaphore, vr -4.
> 76667.976:0124:01bc:warn:vkd3d-proton:d3d12_device_mark_as_removed: Device 0000000044360080 is lost (reason 0x887a0005, "VK_ERROR_DEVICE_LOST").
> 76667.977:0124:01bc:err:vkd3d-proton:vkd3d_wait_for_gpu_timeline_semaphore: Failed to wait for Vulkan timeline semaphore, vr -4.
> 76667.977:0124:01bc:warn:vkd3d-proton:d3d12_device_mark_as_removed: Device 0000000044360080 is lost (reason 0x887a0005, "VK_ERROR_DEVICE_LOST").
> 76667.977:0124:01bc:err:vkd3d-proton:vkd3d_wait_for_gpu_timeline_semaphore: Failed to wait for Vulkan timeline semaphore, vr -4.
> 76667.977:0124:01bc:warn:vkd3d-proton:d3d12_device_mark_as_removed: Device 0000000044360080 is lost (reason 0x887a0005, "VK_ERROR_DEVICE_LOST").
> 76667.978:0124:0480:warn:threadname:NtSetInformationThread Thread renamed to L"wine_threadpool_worker"
> 76667.978:0124:0454:warn:threadname:NtSetInformationThread Thread renamed to L"wine_threadpool_worker"

So I guess somehow the GPU context breaks?

## Comment 2452926521

other (NONE) · Vanane · 2024-11-02T08:58:26Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452926521

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452226959

Here's a log from another crash. I removed all the warning logs about VK plugins that fill almost the entire file, like `vk_image_aspect_flags_from_d3d12` and  `d3d12_pipeline_state_init_graphics_create_info`, and truncated to get only the logs starting from the second the game froze.
It was a complete OS crash, this time, by the way.

[less-steam-3065170.log](https://github.com/user-attachments/files/17606276/less-steam-3065170.log)


This block specifically sounds important, as it could point out to an issue with Mesa :
> radv/amdgpu: The CS has been cancelled because the context is lost. This context is innocent.
> radv: GPUVM fault detected at address 0x800064800000.
> GCVM_L2_PROTECTION_FAULT_STATUS: 0x101431
> 	 CLIENT_ID: (SQC (data)) 0xa
> 	 MORE_FAULTS: 1
> 	 WALKER_ERROR: 0
> 	 PERMISSION_FAULTS: 3
> 	 MAPPING_ERROR: 0
> 	 RW: 0
> X connection to :1 broken (explicit kill or server shutdown).

I've found several issues on some other games/unrelated projects that may point out that there are issues with tensors calculation or smth. So I guess, FSR may be problematic ? idk how it works, i'm just linking words together with my poor knowledge :eyes:

This might be worth trying, too : 
https://gitlab.freedesktop.org/drm/amd/-/issues/2496

Update : I could get almost an entire hour of gameplay, yipeee. But it crashed eventually, even ith that AMD_DEBUG thingy. Game was on High settings, FSR disabled.

## Comment 2452951918

other (NONE) · skygrango · 2024-11-02T10:51:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452951918

if you are using amd gpu
you can try to use RADV_DEBUG=syncshaders with latest proton experimental bleeding edge

This at least got me out of a ten-minute crash, even at the expense of a considerable fps drop.

I can finally play the game normally :)

## Comment 2452958173

other (NONE) · Vanane · 2024-11-02T11:20:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452958173

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452951918

Aside from running the game at 20fps, it didn't prevent it from crashing 10 minutes in.

## Comment 2452963790

other (NONE) · apoisonedgift · 2024-11-02T11:45:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452963790

> if you are using amd gpu you can try to use RADV_DEBUG=syncshaders with latest proton experimental bleeding edge
> 
> This at least got me out of a ten-minute crash, even at the expense of a considerable fps drop.
> 
> I can finally play the game normally :)

I was able to finally finish the doshaguma fight with this... but it wasn't worth it lol. It was running at 40fps the whole time with frame generation ON and all settings on lowest, so it felt and looked absolutely terrible. I also can't say for sure this command stopped the crash because previously I was able to go 15-20 minutes running around exploring and stuff without a crash, then it would just crash randomly. This was abotu 20 minutes also. But first test seems like it works - I won't be doing more testing with that though because it feels awful haha

## Comment 2452964026

other (NONE) · skygrango · 2024-11-02T11:46:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452964026

> [8206 comment ](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452951918)
> 

I'm sorry I couldn't help, I tried to tell you more about my other settings
spec
archlinux with mesa-git
 rx 7900xtx 
1. Use windowed mode (this also means turning off VRR) 
2. Turn off vertical sync 
3.  Turn off NVIDIA Reflex 

I just got through the first chapter and am trying out the multiplayer

## Comment 2452967232

other (NONE) · skygrango · 2024-11-02T11:59:58Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452967232


> I was able to finally finish the doshaguma fight with this... but it wasn't worth it lol. ….. 

I have to turn off frame generation . FSR 3 only.
low fps isn’t good with it …

## Comment 2452968713

other (NONE) · apoisonedgift · 2024-11-02T12:04:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452968713

> > I was able to finally finish the doshaguma fight with this... but it wasn't worth it lol. …..
> 
> I have to turn off frame generation . FSR 3 only. low fps isn’t good with it …

I tried it with and without... it felt about the same either way haha. I think 20fp is going to feel bad regardless of generation or not sadly :P

## Comment 2452982079

other (NONE) · ClearlyClaire · 2024-11-02T12:56:03Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452982079

> if you are using amd gpu you can try to use RADV_DEBUG=syncshaders with latest proton experimental bleeding edge
> 
> This at least got me out of a ten-minute crash, even at the expense of a considerable fps drop.
> 
> I can finally play the game normally :)

This seemed to help, as I've been able to play for much longer (although with fairly poor performances). But I eventually hit the same issue:
<details>
<summary>kernel logs</summary>

```
[ 7039.531343] amdgpu 0000:2f:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=4796796, emitted seq=4796798
[ 7039.531352] amdgpu 0000:2f:00.0: amdgpu: Process information: process MonsterHunterWi pid 20563 thread vkd3d_queue pid 20647
[ 7039.531354] amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
[ 7039.766003] amdgpu 0000:2f:00.0: amdgpu: Dumping IP State
[ 7039.767708] amdgpu 0000:2f:00.0: amdgpu: Dumping IP State Completed
[ 7039.767711] amdgpu 0000:2f:00.0: amdgpu: MODE1 reset
[ 7039.767714] amdgpu 0000:2f:00.0: amdgpu: GPU mode1 reset
[ 7039.767776] amdgpu 0000:2f:00.0: amdgpu: GPU smu mode1 reset
[ 7040.289440] amdgpu 0000:2f:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 7040.290060] [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
[ 7040.290143] [drm] VRAM is lost due to GPU reset!
[ 7040.290145] amdgpu 0000:2f:00.0: amdgpu: PSP is resuming...
[ 7040.369177] amdgpu 0000:2f:00.0: amdgpu: reserve 0xa00000 from 0x83fd000000 for PSP TMR
[ 7040.510805] amdgpu 0000:2f:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 7040.510810] amdgpu 0000:2f:00.0: amdgpu: SMU is resuming...
[ 7040.510815] amdgpu 0000:2f:00.0: amdgpu: smu driver if version = 0x00000040, smu fw if version = 0x00000041, smu fw program = 0, version = 0x003a5a00 (58.90.0)
[ 7040.510818] amdgpu 0000:2f:00.0: amdgpu: SMU driver if version not matched
[ 7040.510850] amdgpu 0000:2f:00.0: amdgpu: use vbios provided pptable
[ 7040.589444] amdgpu 0000:2f:00.0: amdgpu: SMU is resumed successfully!
[ 7040.590902] [drm] DMUB hardware initialized: version=0x02020020
[ 7040.725893] [drm] kiq ring mec 2 pipe 1 q 0
[ 7040.732471] amdgpu 0000:2f:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 7040.732474] amdgpu 0000:2f:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
[ 7040.732476] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
[ 7040.732477] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
[ 7040.732479] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 7040.732480] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 7040.732481] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 7040.732483] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 7040.732484] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 7040.732485] amdgpu 0000:2f:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 7040.732487] amdgpu 0000:2f:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
[ 7040.732488] amdgpu 0000:2f:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
[ 7040.732489] amdgpu 0000:2f:00.0: amdgpu: ring sdma1 uses VM inv eng 14 on hub 0
[ 7040.732491] amdgpu 0000:2f:00.0: amdgpu: ring sdma2 uses VM inv eng 15 on hub 0
[ 7040.732492] amdgpu 0000:2f:00.0: amdgpu: ring sdma3 uses VM inv eng 16 on hub 0
[ 7040.732494] amdgpu 0000:2f:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[ 7040.732495] amdgpu 0000:2f:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[ 7040.732496] amdgpu 0000:2f:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[ 7040.732497] amdgpu 0000:2f:00.0: amdgpu: ring vcn_dec_1 uses VM inv eng 5 on hub 8
[ 7040.732499] amdgpu 0000:2f:00.0: amdgpu: ring vcn_enc_1.0 uses VM inv eng 6 on hub 8
[ 7040.732500] amdgpu 0000:2f:00.0: amdgpu: ring vcn_enc_1.1 uses VM inv eng 7 on hub 8
[ 7040.732501] amdgpu 0000:2f:00.0: amdgpu: ring jpeg_dec uses VM inv eng 8 on hub 8
[ 7040.740670] amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow start
[ 7040.781401] amdgpu 0000:2f:00.0: amdgpu: recover vram bo from shadow done
[ 7040.781428] amdgpu 0000:2f:00.0: amdgpu: GPU reset(2) succeeded!
[ 7040.781647] [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
```

</details>

## Comment 2452982871

other (NONE) · Valmar33 · 2024-11-02T12:59:22Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452982871

> > if you are using amd gpu you can try to use RADV_DEBUG=syncshaders with latest proton experimental bleeding edge
> > This at least got me out of a ten-minute crash, even at the expense of a considerable fps drop.
> > I can finally play the game normally :)
> 
> This seemed to help, as I've been able to play for much longer (although with fairly poor performances). But I eventually hit the same issue:
> kernel logs

One of the odder solutions I found was to build a debug version of vkd3d-proton, dump those DLLs in the game folder, and put `RADV_DEBUG=syncshaders VKD3D_CONFIG=breadcrumbs WINEDLLOVERRIDES="d3d12,d3d12core=n,b" %command%` in the launch options. For whatever reason, this has fully prevented driver and game crashes for me, at the cost of some occasional severe stuttering and performance weirdness.

## Comment 2452985480

other (NONE) · Awlexus · 2024-11-02T13:09:11Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452985480

I tried starting the game after uninstalling everything driver related except mesa and xf86-video-amdgpu drivers, running on proton experimental.

The game got to the stage the stage where it tries to connect and then crashed my CPU

Show something about failing to set up vulkan before the crash

<details>
<summary>Proton logs</summary>

1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_create_pipeline_variant: Failed to create Vulkan graphics pipeline, vr -4.
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Root signature: 65b6e51a25d2ec79
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Shader 0x1: 4d806bfec718e30f
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Topology: 3 (patch vertex count: 0)
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Vertex attributes: 8
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   0: binding 0, format 106, location 0, offset 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   1: binding 1, format 38, location 1, offset 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   2: binding 1, format 38, location 2, offset 4
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   3: binding 2, format 83, location 3, offset 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   4: binding 3, format 83, location 7, offset 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   5: binding 4, format 68, location 4, offset 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   6: binding 4, format 37, location 5, offset 8
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   7: binding 5, format 37, location 6, offset 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Vertex bindings: 6.
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   0: binding 0, input rate 0, stride 0, divisor 1
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   1: binding 1, input rate 0, stride 0, divisor 1
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   2: binding 2, input rate 0, stride 0, divisor 1
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   3: binding 3, input rate 0, stride 0, divisor 1
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   4: binding 4, input rate 0, stride 0, divisor 1
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   5: binding 5, input rate 0, stride 0, divisor 1
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: DSV: #14
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Depth test: 1 (write: 1)
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Depth bounds test: 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Stencil test: 1 (write: 1)
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Logic op enabled: 0 (logic op: 0)
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Sample count: 1 (mask: 0xffffffff, sample shading 0, alpha to coverage 0)
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Rasterizer state:
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Polygon mode: 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Line mode: 0 (width: 1.000000)
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Conservative: 0
1630.307:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Dynamic state: 0xc6b (explicit: 0)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_create_pipeline_variant: Failed to create Vulkan graphics pipeline, vr -4.
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Root signature: 65b6e51a25d2ec79
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Shader 0x1: 4d806bfec718e30f
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Topology: 3 (patch vertex count: 0)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Vertex attributes: 8
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   0: binding 0, format 106, location 0, offset 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   1: binding 1, format 38, location 1, offset 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   2: binding 1, format 38, location 2, offset 4
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   3: binding 2, format 83, location 3, offset 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   4: binding 3, format 83, location 7, offset 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   5: binding 4, format 68, location 4, offset 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   6: binding 4, format 37, location 5, offset 8
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   7: binding 5, format 37, location 6, offset 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Vertex bindings: 6.
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   0: binding 0, input rate 0, stride 0, divisor 1
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   1: binding 1, input rate 0, stride 0, divisor 1
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   2: binding 2, input rate 0, stride 0, divisor 1
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   3: binding 3, input rate 0, stride 0, divisor 1
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   4: binding 4, input rate 0, stride 0, divisor 1
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   5: binding 5, input rate 0, stride 0, divisor 1
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: DSV: #14
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Depth test: 1 (write: 1)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Depth bounds test: 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Stencil test: 1 (write: 1)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Logic op enabled: 0 (logic op: 0)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Sample count: 1 (mask: 0xffffffff, sample shading 0, alpha to coverage 0)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Rasterizer state:
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Polygon mode: 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Line mode: 0 (width: 1.000000)
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state:   Conservative: 0
1630.507:0124:0150:err:vkd3d-proton:d3d12_pipeline_state_log_graphics_state: Dynamic state: 0xc6b (explicit: 0)

</details>

## Comment 2452991658

other (NONE) · dmolin93 · 2024-11-02T13:32:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452991658

> if you are using amd gpu you can try to use RADV_DEBUG=syncshaders with latest proton experimental bleeding edge
> 
> This at least got me out of a ten-minute crash, even at the expense of a considerable fps drop.
> 
> I can finally play the game normally :)

Can also verify that this works but with big emphasis on fps drops. I had to put everything on lowest and got 30-45 FPS in a hunt. With all the settings at lowest the visual clarity was awful so while it was playable it wasn't very fun :sweat_smile: 

## Comment 2453107400

other (NONE) · Eckoa · 2024-11-02T19:41:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2453107400

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2452926521

Issue isn't FSR but the game doing some weird things with sparse mappings apparently. The crashes happen with or without fsr. There's an issue on the mesa tracker that the vkd3d Dev opened on it. https://gitlab.freedesktop.org/mesa/mesa/-/issues/12103

Tldr... Beta be a beta

## Comment 2453108455

other (NONE) · Ember-vee · 2024-11-02T19:46:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2453108455

Just wanna share regarding polygons going everywhere (which seems like it might be Nvidia gpus only) and game freezing within ~30 minutes of starting. 

So it seems restarting my computer makes both of these problems temporarily go away if I have my settings set to minimum (though my specs are not ideal for this so others may be able to use higher.) I am also using AMD fsr 3 with AMD Native AA mode (not sure if there's a difference between this, the intel alternative, or no upscaling with AA).
Doing this, I've been able to play 2 long sessions (2.5h and 1.5h) without any major graphical artifacts, though they both eventually ended with the familiar freeze. I might test later to see if higher settings cause it to freeze sooner or have artifacts.

This was with proton experimental bleeding edge, though GE 9-17/GE 9-18 worked about the same for me in previous testing. Oddly the workaround with UAV compression doesn't seem to work for me so render scale and upscaling are still broken.
Another thing with the polygon artifacts, it seems to deteriorate more over time, affecting fur or similar dynamic parts more often. It'll just start with a part of one creature, then as time goes on it happens to more and more creatures/sections (including the player model). Increasing the model quality setting temporarily resets most if not all such artifacts, though they typically come back quickly for me.

```
OS: Linux Mint 21.3
Kernel Version: 6.8.0-48-generic
CPU: Intel Core i3-10100F
GPU: Nvidia Geforce GTX 1070
GPU DRIVER: 560.35.03
RAM: 16GB (+16GB of swap)
```

## Comment 2453114273

other (NONE) · NickelWW · 2024-11-02T20:09:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2453114273

```
OS: Fedora Linux 41 (KDE Plasma)
KERNEL: 6.11.5-300.fc41.x86_64
CPU: 12th Gen Intel Core i9-12900K
GPU: Radeon RX 7900 XTX
GPU DRIVER: Mesa 24.2.5
RAM: 32 GB DDR4 3200mhz (XMP)
```
with RADV_DEBUG=syncshaders & latest proton experimental, I'm still crashing just as often, but now with worse frames :p

a slight difference, the first time it hung, it recovered, which it had never done before, but then my entire OS had to be restarted when it happened again a few minutes later (as was happening before)

## Comment 2453170013

other (NONE) · WhiteEyeDoll · 2024-11-02T21:45:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2453170013

I was able to hunt all the available monsters on the first day.
Solo hunting. Base camp online features work but did not test party hunting.

Dunes, bushes and other foliage cause some graphical artefacts.
Needed to turn surface quality (from main menu only) and ambient occlusion down for being able to see in front of me but some glitches still remain.

Certain areas cause performance hits. Playing with max settings (minus the previosly mentioned) and 2160p resolution.

```
VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 PROTON_ENABLE_NGX_UPDATER=1 PROTON_HIDE_NVIDIA_GPU=0 PROTON_ENABLE_NVAPI=1 MANGOHUD=1 %command%
```

Proton Bleeding Edge

OS: Arch Linux (KDE Plasma 6, Wayland)
KERNEL: 6.11.5-arch1-1
CPU: 13th Gen Intel Core i9-13900K
GPU: NVIDIA RTX 4080
GPU DRIVER: 560.35.03
RAM: 64GB DDR5


## Comment 2455017989

other (NONE) · jl240 · 2024-11-04T15:29:34Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2455017989

> Hi, using Proton-Experimental [bleeding-edge] fixed the initial crash that also used to happen for me.
> 
> Also, after the logo's screen, the following error happen:
> 
> ![Screenshot_2024-10-31_15-51-04](https://private-user-images.githubusercontent.com/48338648/382082620-7164f5a7-f482-47ef-aa6e-1621f24ae72d.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzA3MzQ0NTQsIm5iZiI6MTczMDczNDE1NCwicGF0aCI6Ii80ODMzODY0OC8zODIwODI2MjAtNzE2NGY1YTctZjQ4Mi00N2VmLWFhNmUtMTYyMWYyNGFlNzJkLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDExMDQlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMTA0VDE1MjkxNFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTYzZWVlMmUwYTg3NzUwYTQ2NmZjMzFjMzBmNTViMmRiYTc4OTFiNGEyOWUyMjJiMjM4YWQwYzQyMjU3YWIyOTImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.dbYzXFJBq_owJPGbH4MOLxj3MznsqnqdDxfbUHal67c)
> 
> Using `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` in the game's launch options on Steam fixed it, and now it works normally.
> 
> Now is just to wait for the open beta to be properly released.

Worked for me, thank you!

## Comment 2460973003

other (NONE) · TheRainbowpixelz · 2024-11-06T23:07:20Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2460973003

any word or anywhere I can see the progress of a cracked beta? sorry if i'm adding to the fluff

## Comment 2636321888

other (NONE) · braiam · 2025-02-05T10:22:11Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636321888

<details><summary>Monster Hunter benchmark still crashes the GPU:</summary>

```
[  610.362842] input: gsr-ui virtual keyboard as /devices/virtual/input/input33
[  670.252409] warning: `wine_sechost_se' uses wireless extensions which will stop working for Wi-Fi 7 hardware; use nl80211
[ 1555.476747] amdgpu 0000:03:00.0: amdgpu: Dumping IP State
[ 1555.478587] amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
[ 1555.488658] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=764163, emitted seq=764165
[ 1555.488662] amdgpu 0000:03:00.0: amdgpu: Process information: process MonsterHunterWi pid 14799 thread vkd3d_queue pid 14948
[ 1555.488664] amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[ 1555.758807] amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset failure
[ 1555.758810] amdgpu 0000:03:00.0: amdgpu: GPU reset begin!
[ 1555.770915] amdgpu: Failed to suspend process 0x8002
[ 1556.047686] amdgpu 0000:03:00.0: amdgpu: MODE1 reset
[ 1556.047691] amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset
[ 1556.047753] amdgpu 0000:03:00.0: amdgpu: GPU smu mode1 reset
[ 1556.564905] amdgpu 0000:03:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 1556.565108] [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
[ 1556.565130] [drm] VRAM is lost due to GPU reset!
[ 1556.565132] amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
[ 1556.640099] amdgpu 0000:03:00.0: amdgpu: reserve 0xa00000 from 0x82fd000000 for PSP TMR
[ 1556.741400] amdgpu 0000:03:00.0: amdgpu: RAS: optional ras ta ucode is not available
[ 1556.754899] amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 1556.754903] amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
[ 1556.754908] amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413e00 (65.62.0)
[ 1556.754911] amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
[ 1556.754943] amdgpu 0000:03:00.0: amdgpu: use vbios provided pptable
[ 1556.815339] amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!
[ 1556.816039] [drm] kiq ring mec 2 pipe 1 q 0
[ 1556.822920] [drm] DMUB hardware initialized: version=0x02020020
[ 1556.989855] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 uses VM inv eng 0 on hub 0
[ 1556.989858] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.1.0 uses VM inv eng 1 on hub 0
[ 1556.989859] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.0 uses VM inv eng 4 on hub 0
[ 1556.989861] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.0 uses VM inv eng 5 on hub 0
[ 1556.989862] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.0 uses VM inv eng 6 on hub 0
[ 1556.989863] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.0 uses VM inv eng 7 on hub 0
[ 1556.989864] amdgpu 0000:03:00.0: amdgpu: ring comp_1.0.1 uses VM inv eng 8 on hub 0
[ 1556.989865] amdgpu 0000:03:00.0: amdgpu: ring comp_1.1.1 uses VM inv eng 9 on hub 0
[ 1556.989866] amdgpu 0000:03:00.0: amdgpu: ring comp_1.2.1 uses VM inv eng 10 on hub 0
[ 1556.989867] amdgpu 0000:03:00.0: amdgpu: ring comp_1.3.1 uses VM inv eng 11 on hub 0
[ 1556.989868] amdgpu 0000:03:00.0: amdgpu: ring kiq_0.2.1.0 uses VM inv eng 12 on hub 0
[ 1556.989869] amdgpu 0000:03:00.0: amdgpu: ring sdma0 uses VM inv eng 13 on hub 0
[ 1556.989871] amdgpu 0000:03:00.0: amdgpu: ring sdma1 uses VM inv eng 14 on hub 0
[ 1556.989872] amdgpu 0000:03:00.0: amdgpu: ring vcn_dec_0 uses VM inv eng 0 on hub 8
[ 1556.989873] amdgpu 0000:03:00.0: amdgpu: ring vcn_enc_0.0 uses VM inv eng 1 on hub 8
[ 1556.989874] amdgpu 0000:03:00.0: amdgpu: ring vcn_enc_0.1 uses VM inv eng 4 on hub 8
[ 1556.989875] amdgpu 0000:03:00.0: amdgpu: ring jpeg_dec uses VM inv eng 5 on hub 8
[ 1556.993539] amdgpu 0000:03:00.0: amdgpu: GPU reset(2) succeeded!
[ 1556.993963] [drm:amdgpu_cs_ioctl [amdgpu]] *ERROR* Failed to initialize parser -125!
[ 1557.007153] snd_hda_codec_hdmi hdaudioC1D0: HDMI: ELD buf size is 0, force 128
[ 1557.007168] snd_hda_codec_hdmi hdaudioC1D0: HDMI: invalid ELD data byte 0
[ 1557.007219] snd_hda_codec_hdmi hdaudioC1D0: HDMI: ELD buf size is 0, force 128
[ 1557.007242] snd_hda_codec_hdmi hdaudioC1D0: HDMI: invalid ELD data byte 0
[ 1900.090240] show_signal: 20 callbacks suppressed
[ 1900.090243] traps: vesktop[14050] trap int3 ip:5592c035010e sp:7ffe7e738740 error:0 in vesktop[606510e,5592bc3a1000+8998000]
[ 1905.608611] snd_hda_codec_hdmi hdaudioC1D0: HDMI: ELD buf size is 0, force 128
[ 1905.608646] snd_hda_codec_hdmi hdaudioC1D0: HDMI: invalid ELD data byte 0
[ 1905.608716] snd_hda_codec_hdmi hdaudioC1D0: HDMI: ELD buf size is 0, force 128
[ 1905.608744] snd_hda_codec_hdmi hdaudioC1D0: HDMI: invalid ELD data byte 0
[ 1905.608847] snd_hda_codec_hdmi hdaudioC1D0: HDMI: ELD buf size is 0, force 128
[ 1905.608875] snd_hda_codec_hdmi hdaudioC1D0: HDMI: invalid ELD data byte 0
[ 1905.699506] snd_hda_codec_hdmi hdaudioC1D0: HDMI: ELD buf size is 0, force 128
[ 1905.699521] snd_hda_codec_hdmi hdaudioC1D0: HDMI: invalid ELD data byte 0
[ 1906.181638] Lockdown: Xorg: raw io port access is restricted; see man kernel_lockdown.7
```

</details>

Restarting the desktop manager brings up the system again. This also happened in the previous beta tests.

## Comment 2636449404

other (NONE) · skygrango · 2025-02-05T11:18:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636449404


> Restarting the desktop manager brings up the system again. This also happened in the previous beta tests.

we need to try this one: https://github.com/HansKristian-Work/vkd3d-proton/commit/1fb838018435f32d8f6e6b8edeabb6ad77d14ab9

## Comment 2636452114

other (NONE) · E3FxGaming · 2025-02-05T11:19:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636452114

Monster Hunter Wilds Benchmark did not crash my GPU, even though the first beta did crash my GPU frequently.
This is obviously no guarantee for the full game to run well.
In the previous beta I had to use performance crippling launch options such as "OFF_RADV_DEBUG=syncshaders" and really reduce my resolution to just play long enough to finish the available content (with multiple restarts).

System:
Arch Linux w/ up-to-date KDE Wayland
Ryzen 7800X3D and Radeon 7900 XTX
linux 6.13.1.arch1-1
mesa 1:24.3.4-1
Proton Experimental [bleeding-edge]

I ran the benchmark twice with Graphics Preset Ultra (FSR Quality, RT off, Frame-Gen off) to make sure the first one wasn't a fluke:

![Image](https://github.com/user-attachments/assets/76f05cb8-e88e-4ec4-8019-7c75365c8907)

![Image](https://github.com/user-attachments/assets/c233b6e4-4cb7-4c3f-a3a8-ef17f858bb24)

I would like to report though that I am unable to enable Ray Tracing - the setting is simply  greyed out and not configurable:

![Image](https://github.com/user-attachments/assets/3e5d709b-e1b3-4588-8fb6-c4406e686cc1)

I tried launching the benchmark with "STEAM_DECK=0" too and the setting remained non-configurable.

The game should know that I'm not on a Steam Deck, since it knows my CPU and GPU by name (and shows it during the benchmark, as well as in the results screen). It also shows 24 GB VRAM in the settings menu, which the Steam Deck would not show.

## Comment 2636468934

other (NONE) · DomiStyle · 2025-02-05T11:27:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636468934

> > Restarting the desktop manager brings up the system again. This also happened in the previous beta tests.
> 
> we need to try this one: [HansKristian-Work/vkd3d-proton@1fb8380](https://github.com/HansKristian-Work/vkd3d-proton/commit/1fb838018435f32d8f6e6b8edeabb6ad77d14ab9)

@braiam That change is already in Proton Experimental (bleeding-edge branch) so you can give it another go.

## Comment 2636472929

other (NONE) · Doomguy1364 · 2025-02-05T11:29:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636472929

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636452114

I had to test myself as I have the EXACT same set up as you; Alias, the benchmark does crash my GPU. I am only using regular proton experimental, so I assume there's some sort of fix in the bleeding-edge version of proton that isn't in the main build yet.

## Comment 2636889619

other (NONE) · Billli11 · 2025-02-05T13:42:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636889619

~~Is the lastest bleeding-edge branch of Proton Experimental include the fixes. https://github.com/HansKristian-Work/vkd3d-proton/pull/2329?~~

~~Still crashing with amdgpu.~~

Distro: Arch Linux
CPU: AMD Ryzen 7 5700X3D  
GPU:AMD Radeon RX 7800 XT  
Mesa: Mesa 25.1.0-devel  
Kenel: 6.13.1-zen1-1-zen  

Edit:1 ran again with high setting. the workaround is working. but still crash if vram usage is more than the card's.

## Comment 2636930420

other (NONE) · apoisonedgift · 2025-02-05T13:59:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636930420

Just chipping in with my experience as another data point...
I had crashes every minute or so when beta 1 was happening. I've been able to run the benchmark tool 3 or 4 times now. But I do have a new PC (same GPU though) so it might be that I'm not getting them as frequently.

Distro: Arch
CPU: AMD Ryzen 9800X3D
GPU AMD Radeon RX 6800 XT
Mesa: 24.3.4-arch1.1
Kernel: 6.13.1-arch-1-1

All settings on high default, but frame gen turned off

Tested with both proton experimental and ge-proton 9-23. GE gave marginally better results in multiple benchmark runs, both stable for the period I ran them.

I expect the CPU is doing better (my previous build was a Ryzen 3900XT) and that I'll still get crashes but less frequently. I'll try some extended benchmark loops tomorrow. Hopefully this is something that will be resolved during beta 2 or sooner now that we have the benchmark access :)

## Comment 2636946189

other (NONE) · victor-borges · 2025-02-05T14:05:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636946189

For anyone, try to turn OFF Steam game recording when running this benchmark/game, for some reason it tanks performance here.

## Comment 2636971606

other (NONE) · rfguimaraes · 2025-02-05T14:15:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2636971606

> I expect the CPU is doing better (my previous build was a Ryzen 3900XT) and that I'll still get crashes but less frequently. I'll try some extended benchmark loops tomorrow. Hopefully this is something that will be resolved during beta 2 or sooner now that we have the benchmark access :)

FIY the second beta will be the same build as the first beta essentially, so the performance will be worse than the benchmark, if that makes sense

## Comment 2637307795

other (NONE) · braiam · 2025-02-05T15:50:30Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637307795

> > > Restarting the desktop manager brings up the system again. This also happened in the previous beta tests.
> > 
> > 
> > we need to try this one: [HansKristian-Work/vkd3d-proton@1fb8380](https://github.com/HansKristian-Work/vkd3d-proton/commit/1fb838018435f32d8f6e6b8edeabb6ad77d14ab9)
> 
> [@braiam](https://github.com/braiam) That change is already in Proton Experimental (bleeding-edge branch) so you can give it another go.

It didn't crash in my multiple runs of the benchmark.

## Comment 2637506873

other (NONE) · Shyclops · 2025-02-05T17:00:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637506873

Running 

Proton Experimental  Bleeding Edge
Arch Linux
AMD Ryzen 7 7700X 8-Core Processor
32GB RAM
RTX 4080 SUPER

All I'm getting for the benchmark is a black screen, when i try to close it, it becomes not responsive

## Comment 2637581814

other (NONE) · braiam · 2025-02-05T17:31:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637581814

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637506873

Did you try stable or non-bleeding edge.

## Comment 2637601893

other (NONE) · elirasza · 2025-02-05T17:40:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637601893

Everything works fine in the benchmark tool except for the framegen. I have tried many presets (with or without FSR, lowest or ultra, several different screen refresh rates, Proton Experimental or GE) with success and framegen seems to be the only option that consistently crashes the game. I only had a run out of 10 with it enabled that finished without crashing.

**Proton :** Experimental
**Kernel :** Arch Linux 6.13.1-arch1-1
**CPU :** AMD Ryzen 9 7900X
**GPU :** AMD Radeon RX 7900 XT
**Driver :** Mesa 24.3.4-arch1.1 (LLVM 19.1.7) stable

Maybe this information could be of use, but other games with FSR built-in framegen like Starfield do not crash.

## Comment 2637606420

other (NONE) · mattipulkkinen · 2025-02-05T17:42:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637606420

With Proton Experimental I was only able to complete the benchmark by switching down to high graphics settings (from Ultra) and disabling frame generation. After switching to Proton Experimental bleeding-edge, I was able to complete the benchmark with both ultra and high graphics settings, and both with FG enabled or not. Whatever magic there is in bleeding-edge seems to have worked.

<details><summary>System info</summary>

```
System:
  Kernel: 6.12.11-200.fc41.x86_64 arch: x86_64 bits: 64
  Desktop: GNOME v: 47.3 Distro: Fedora Linux 41 (Workstation Edition)
Machine:
  Type: Desktop System: ASRock product: X870E Taichi Lite v: N/A
    serial: <superuser required>
  Mobo: ASRock model: X870E Taichi Lite serial: <superuser required>
    UEFI: American Megatrends LLC. v: 3.16 date: 12/18/2024
CPU:
  Info: 8-core model: AMD Ryzen 7 9800X3D bits: 64 type: MT MCP cache:
    L2: 8 MiB
  Speed (MHz): avg: 600 min/max: 600/5269 cores: 1: 600 2: 600 3: 600 4: 600
    5: 600 6: 600 7: 600 8: 600 9: 600 10: 600 11: 600 12: 600 13: 600 14: 600
    15: 600 16: 600
Graphics:
  Device-1: Advanced Micro Devices [AMD/ATI] Navi 31 [Radeon RX 7900 XT/7900
    XTX/7900 GRE/7900M] driver: amdgpu v: kernel
  Device-2: Advanced Micro Devices [AMD/ATI] Granite Ridge [Radeon Graphics]
    driver: amdgpu v: kernel
  Device-3: Realtek Streamplify CAM driver: snd-usb-audio,uvcvideo type: USB
  Display: wayland server: X.Org v: 24.1.4 with: Xwayland v: 24.1.4
    compositor: gnome-shell driver: dri: radeonsi gpu: amdgpu resolution:
    1: 2560x1440~240Hz 2: 2560x1440~60Hz
  API: OpenGL v: 4.6 vendor: amd mesa v: 24.3.4 renderer: AMD Radeon RX
    7900 XT (radeonsi navi31 LLVM 19.1.0 DRM 3.59 6.12.11-200.fc41.x86_64)
  API: EGL Message: EGL data requires eglinfo. Check --recommends.
  Info: Tools: api: glxinfo x11: xdriinfo, xdpyinfo, xprop, xrandr
Audio:
  Device-1: Advanced Micro Devices [AMD/ATI] Navi 31 HDMI/DP Audio
    driver: snd_hda_intel
  Device-2: Advanced Micro Devices [AMD/ATI] Rembrandt Radeon High
    Definition Audio driver: snd_hda_intel
  Device-3: Advanced Micro Devices [AMD] Family 17h/19h/1ah HD Audio
    driver: N/A
  Device-4: Focusrite-Novation Scarlett Solo 4th Gen driver: snd-usb-audio
    type: USB
  Device-5: Generic USB Audio driver: hid-generic,snd-usb-audio,usbhid
    type: USB
  Device-6: Realtek Streamplify CAM driver: snd-usb-audio,uvcvideo type: USB
  API: ALSA v: k6.12.11-200.fc41.x86_64 status: kernel-api
  Server-1: PipeWire v: 1.2.7 status: active
Network:
  Device-1: Realtek driver: r8169
  IF: enp10s0 state: up speed: 1000 Mbps duplex: full mac: <filter>
  Device-2: MEDIATEK driver: mt7925e
  IF: wlp11s0 state: down mac: <filter>
Bluetooth:
  Device-1: MediaTek Wireless_Device driver: btusb type: USB
  Report: btmgmt ID: hci0 state: up address: <filter> bt-v: 5.4
Drives:
  Local Storage: total: 3.64 TiB used: 1.22 TiB (33.6%)
  ID-1: /dev/nvme0n1 vendor: Samsung model: SSD 990 PRO 4TB size: 3.64 TiB
Partition:
  ID-1: / size: 3.64 TiB used: 1.22 TiB (33.6%) fs: btrfs dev: /dev/dm-0
  ID-2: /boot size: 973.4 MiB used: 343 MiB (35.2%) fs: ext4
    dev: /dev/nvme0n1p2
  ID-3: /boot/efi size: 598.8 MiB used: 19.3 MiB (3.2%) fs: vfat
    dev: /dev/nvme0n1p1
  ID-4: /home size: 3.64 TiB used: 1.22 TiB (33.6%) fs: btrfs dev: /dev/dm-0
Swap:
  ID-1: swap-1 type: zram size: 8 GiB used: 264.2 MiB (3.2%) dev: /dev/zram0
Sensors:
  System Temperatures: cpu: 43.5 C mobo: N/A
  Fan Speeds (rpm): N/A
  GPU: device: amdgpu temp: 58.0 C fan: 214 device: amdgpu temp: 38.0 C
Info:
  Memory: total: 48 GiB note: est. available: 46.13 GiB used: 6.57 GiB (14.2%)
  Processes: 514 Uptime: 6h 32m Shell: Zsh inxi: 3.3.37
```

</details> 

<details><summary>Benchmark results</summary>

![Image](https://github.com/user-attachments/assets/5965c65d-107c-4afc-baeb-c94b9482bd86)

![Image](https://github.com/user-attachments/assets/d4b3d1cb-8bdf-4bd8-8ec8-a748fb999fc8)

![Image](https://github.com/user-attachments/assets/06e6f789-c906-4a28-91ed-1e50293b3d2c)

![Image](https://github.com/user-attachments/assets/b0ab3f0c-055e-49d1-8def-e8646dc6ee84)

</details> 

## Comment 2637762003

other (NONE) · Shyclops · 2025-02-05T18:53:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637762003

> > Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637506873)
> 
> Did you try stable or non-bleeding edge.

i think i fixed it
swapped off of nvidia-open-dkms and onto nvidia-open and its working now

but in response to your question, i had tried stable, hotfix and non-bleeding edge and they were all giving me a black screen before

## Comment 2637898160

other (NONE) · elirasza · 2025-02-05T19:55:58Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637898160

It seems the latest build of Experimental fixed the crash when using framegen. Thank you very much !

## Comment 2637983671

other (NONE) · Ponkhy · 2025-02-05T20:44:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2637983671

My game launches but after selecting the language the game crashes/laggs to an unusable state with a black screen and only the cursor showing.

Proton: Experimental
OS: Debian GNU/Linux 12 (bookworm)
Kernel: 6.8.9-3-liquorix-amd64
CPU: AMD Ryzen 9 7900
GPU: RTX 3080
Driver: 550.54.15

## Comment 2638089033

other (NONE) · WhiteEyeDoll · 2025-02-05T21:43:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2638089033

Enabling framegen crashes the benchmark when launching it from the menu. Menu and settings work.
Works when disabling framegen.

![Image](https://github.com/user-attachments/assets/5fb55a1d-fb09-411d-bf9a-c4bdaddb6354)

Proton Bleeding Edge, GE-Proton9-23

OS: Arch Linux (KDE Plasma 6, Wayland)
KERNEL: 6.13.1-arch1-1
CPU: 13th Gen Intel Core i9-13900K
GPU: NVIDIA RTX 4080
GPU DRIVER: nvidia-open-dkms 565.77 (cannot test 570, it currently [breaks DisplayPort MST](https://gitlab.archlinux.org/archlinux/packaging/packages/nvidia-utils/-/issues/25))
RAM: 64GB DDR5

## Comment 2638456293

other (NONE) · ToastedWookiee · 2025-02-06T01:43:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2638456293

OS: CachyOS Arch Linux, KDE Plasma 6 Wayland
Kernel: Linux 6.13.1-2-cachyos
CPU: I9-9900K
GPU: Intel Arc A770 16GB
GPU Driver: mesa-git 25.0.0_devel.200460.e802793dd50
Proton Experimental-Bleeding Edge

Get 2 freezes with GPU hang: change settings to below High, which I have narrowed down to the change of `Distant Shadow Quality` from High to Low causes the hang, otherwise just running the benchmark will hang in ~5s from start while audio continues.


## Comment 2639349152

other (NONE) · NTrixner · 2025-02-06T09:58:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2639349152

OS: Linux Manjaro, KDE
CPU: AMD Ryzen 9 3900X
GPU: AMD RX 7900XT
Proton Experimental-Bleeding Edge

(Sorry about missing Kernel and GPU Driver, I'm at work atm and can't check versions)

Benchmark: No freezes after switching to Proton Experimental-Bleeding Edge. I'm getting around 19600 Points with High Settings and Frame Generation on Balanced, with an average FPS of 115. Drops into the low 80s and even 70s during the beginning of the second scene. But it does run, and for more than one pass as well, so I'm hopeful for the open beta tomorrow.
I think my CPU might be bottlenecking, since I'm still on AM4. FPS and Score don't change much when going to Ultra.

## Comment 2641462862

reporter (NONE) · CreatureDev · 2025-02-07T00:14:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2641462862

I'm still getting some vertex artifacting in the desert after the scene with the chatacabra. Same setup as my original post.
Performance is good otherwise. Getting 20k points, 58fps avg using high settings, dlss4 performance.
I did update the dlss dlls to use dlss4.

## Comment 2641971235

other (NONE) · Vorthas · 2025-02-07T05:20:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2641971235

OS: EndeavourOS, MATE X11
Kernel: Linux 6.12.10-arch1-1
CPU: AMD Ryzen 7 7800X3D
GPU: AMD Radeon RX 7800XT
GPU Driver: Mesa 24.3.4-arch1.1
Proton Experimental Bleeding Edge

Was actually able to play the beta this time with no crashes.  Without bleeding edge, I would get a total freeze (audio stills plays but nothing graphical would happen, couldn't even switch to tty, had to hard reboot).  Didn't notice any graphical artifacts and FPS was reasonably stable at 60 (capped) though it did dip to around 45 or so in some fights.  Playing at 1440p.  Frame generation was turned off.

## Comment 2642038255

other (NONE) · Echilonvibin · 2025-02-07T06:17:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642038255

OS: CachyOS
KERNEL: 6.13.1-1-cachyos-bore
CPU: AMD Ryzen 9 7900X 12-Core
GPU: NVIDIA GeForce RTX 4080
GPU DRIVER: NVIDIA 570.86.16
RAM: 32 GB
Proton Experimental Bleeding Edge

Can play alright, performance is shotty at best. Game crashes after about 10-15 minutes, I've played around with the settings quite a bit as well (I am not using frame gen, as that insta crashes my game). I got some insane graphical artifacting, don't really know why, but ONLY fighting the Doshaguma will cause the artifacting (or just looking at it after a few minutes). I've included all my crash reports if that is of any help. 

[2025_0206_.zip](https://github.com/user-attachments/files/18701957/2025_0206_.zip)

## Comment 2642082295

other (NONE) · calvinkatz · 2025-02-07T06:52:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642082295

OS: CachyOS
KERNEL: 6.13.1-1-cachyos-bore & 6.12.12-1-cachyos-lts
CPU: AMD Ryzen 9800X3D
GPU: AMD Radeon 6950XT
GPU DRIVER: Mesa 24.3.4-cachyos1.2 & AMDVLK 2024.Q4.3
RAM: 64 GB
Proton Experimental

Can launch and play the game but crashes after a few minutes. Lowering settings seems to extend playtime but still crashes after a while. Using AMDVLK results in many graphical artifacts and I would say is unplayable.

## Comment 2642359740

other (NONE) · Eckoa · 2025-02-07T09:11:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642359740

> OS: CachyOS KERNEL: 6.13.1-1-cachyos-bore & 6.12.12-1-cachyos-lts CPU: AMD Ryzen 9800X3D GPU: AMD Radeon 6950XT GPU DRIVER: Mesa 24.3.4-cachyos1.2 & AMDVLK 2024.Q4.3 RAM: 64 GB Proton Experimental
> 
> Can launch and play the game but crashes after a few minutes. Lowering settings seems to extend playtime but still crashes after a while. Using AMDVLK results in many graphical artifacts and I would say is unplayable.

I played for 4hrs today with no issue on my RX 7700s laptop with proton experimental so you shouldnt be crashing and something else might be causing it. You should get some logs to see what might be doing it.

## Comment 2642555951

other (NONE) · IllestRat · 2025-02-07T10:40:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642555951

OS: Arch Linux
KERNEL: Linux 6.13.1-arch1-1
CPU: AMD Ryzen 7 5700X3D
GPU: AMD Radeon 6700XT
GPU DRIVER: Mesa 24.3.4-arch1.1
RAM: 32GB
Proton Experimental & GE-Proton9-23

Game launches fine, the UI loads but nothing 3D renders. After loading into game everything is black except for UI elements. I've tried several different launch options, different Proton versions, changing pretty much everything in graphics settings, and I can't find anyone with my issue or a possible solution. I've attached proton logs + screenshot showing my issue.

![Image](https://github.com/user-attachments/assets/feb4636d-b66b-4173-800a-1cf2722a7022)

[steam-3065170.log](https://github.com/user-attachments/files/18705073/steam-3065170.log)

## Comment 2642567147

other (NONE) · skygrango · 2025-02-07T10:45:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642567147


> Game launches fine, the UI loads but nothing 3D renders. 

try VKD3D_CONFIG=disable_uav_compression or disable FSR

## Comment 2642575097

other (NONE) · IllestRat · 2025-02-07T10:49:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642575097

> > Game launches fine, the UI loads but nothing 3D renders.
> 
> try VKD3D_CONFIG=disable_uav_compression or disable FSR

Thanks, that's the one thing I didn't try disabling because of my bad hardware was FSR. FSR is borked.

## Comment 2642586204

other (NONE) · skygrango · 2025-02-07T10:55:30Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642586204

> > > Game launches fine, the UI loads but nothing 3D renders.
> > 
> > 
> > try VKD3D_CONFIG=disable_uav_compression or disable FSR
> 
> Thanks, that's the one thing I didn't try disabling because of my bad hardware was FSR. FSR is borked.

Try VKD3D_CONFIG=disable_uav_compression if you want to use FSR. frame generation is still borked for me.

## Comment 2642594437

other (NONE) · IllestRat · 2025-02-07T10:59:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2642594437

> > > > Game launches fine, the UI loads but nothing 3D renders.
> > > 
> > > 
> > > try VKD3D_CONFIG=disable_uav_compression or disable FSR
> > 
> > 
> > Thanks, that's the one thing I didn't try disabling because of my bad hardware was FSR. FSR is borked.
> 
> Try VKD3D_CONFIG=disable_uav_compression if you want to use FSR. frame generation is still borked for me.

My mistake I should've included I tried VKD3D_CONFIG=disable_uav_compression, both FSR & Intel XeSS are borked as soon as I disable them rendering in the background works.

Update: Bleeding edge + VKD3D_CONFIG=disable_uav_compression worked. Even frame gen works, turn controller vibration off or you'll get really bad stuttering.

## Comment 2643223643

other (NONE) · Globoplox · 2025-02-07T15:17:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643223643

OS: Arch & Gnome
Kernel: linux-zen 6.13.1.zen1-1
CPU: AMD Ryzen 7 5700X
GPU: AMD Radeon RX 7800 XT
GPU Driver: mesa 1:24.3.4-1  & vulkan-radeon 1:24.3.4-1
Proton Experimental

Beta crash after a few minutes of otherwise seemingly normal gameplay.

[steam-3065170.log](https://github.com/user-attachments/files/18708489/steam-3065170.log)
[journalctl_grep_amdgpu.log](https://github.com/user-attachments/files/18708491/journalctl_grep_amdgpu.log)
Crashes seems to match the timing of a pagefault `GCVM_L2_PROTECTION_FAULT_STATUS`, whatever this may means.

I will probably tweak settings and keep testing for the beta duration

**Edit 1**:
Tried with Proton Experimental Bleeding Edge and `VKD3D_CONFIG=disable_uav_compression` and had a 20 minutes+ session with upscaling and frame gen without a crash. Had a lot of artifacts but I mostly did not notice them unless while actively looking for them.

## Comment 2643237319

other (NONE) · braiam · 2025-02-07T15:23:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643237319

@Globoplox you need the bleeding edge branch to avoid the crash on AMD gpus.

## Comment 2643257410

other (NONE) · NTrixner · 2025-02-07T15:32:16Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643257410

OS: Linux Manjaro, KDE
Kernel: 6.12.11-1-MANJARO
CPU: AMD Ryzen 9 3900X
GPU: AMD RX 7900XT
GPU Driver: amdgpu, Mesa 24.3.4
Proton Experimental-Bleeding Edge

Just tried the Beta and was able to play for a few hours, so the issue with it just completely crashing immediately does seem to be fixed with Proton Experimental Bleeding Edge.
Frame Generation still doesn't work though, since it requires Upscaling, and upscaling makes it so nothing gets rendered (except the menus).
That DID work in the benchmark though, so hopefully it will work in the base game as well.

## Comment 2643297824

other (NONE) · Billli11 · 2025-02-07T15:49:16Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643297824

@NTrixner  
add `VKD3D_CONFIG=disable_uav_compression %command%` to launch option to fix upscaling.  
This was added to  vkd3d workaround when open beta 1 then removed shortly after. https://github.com/HansKristian-Work/vkd3d-proton/pull/2184 https://github.com/HansKristian-Work/vkd3d-proton/pull/2203  
as the workaround is not need for the benchmark. I doubt the full game will need it.

## Comment 2643314482

other (NONE) · NTrixner · 2025-02-07T15:52:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643314482

> [@NTrixner](https://github.com/NTrixner) add `VKD3D_CONFIG=disable_uav_compression %command%` to launch option to fix upscaling. This was added to vkd3d workaround when open beta 1 then removed shortly after. [HansKristian-Work/vkd3d-proton#2184](https://github.com/HansKristian-Work/vkd3d-proton/pull/2184) [HansKristian-Work/vkd3d-proton#2203](https://github.com/HansKristian-Work/vkd3d-proton/pull/2203)

You are an absolute lifesaver, that fixes the issue and now I'm getting ~100fps even at main camp. Thank you!

## Comment 2643683108

other (NONE) · Eckoa · 2025-02-07T18:22:46Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643683108

> > > Game launches fine, the UI loads but nothing 3D renders.
> > 
> > 
> > try VKD3D_CONFIG=disable_uav_compression or disable FSR
> 
> Thanks, that's the one thing I didn't try disabling because of my bad hardware was FSR. FSR is borked.

This is a Beta issue not a proton issue, FSR works fine on the Benchmark as does Frame Generation. The Beta build is older and uses a much older version of FSR that doesnt seem to be implemented well at the point this build was forked from the main code base. It has black screen issues and abysmal ghosting which simply arent there on the benchmark.

## Comment 2644036105

other (NONE) · calvinkatz · 2025-02-07T20:13:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644036105

> OS: CachyOS KERNEL: 6.13.1-1-cachyos-bore & 6.12.12-1-cachyos-lts CPU: AMD Ryzen 9800X3D GPU: AMD Radeon 6950XT GPU DRIVER: Mesa 24.3.4-cachyos1.2 & AMDVLK 2024.Q4.3 RAM: 64 GB Proton Experimental
> 
> Can launch and play the game but crashes after a few minutes. Lowering settings seems to extend playtime but still crashes after a while. Using AMDVLK results in many graphical artifacts and I would say is unplayable.

For me it's an amdgpu timeout:
```text
[  571.039864] amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=320989, emitted seq=320991
[  571.039867] amdgpu 0000:03:00.0: amdgpu: Process information: process MonsterHunterWi pid 7614 thread vkd3d_queue pid 7742
[  571.039868] amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
[  571.286352] amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset failure
```
What I found is that after some recent update the driver is detecting a max clock much higher than expected (2639 vs 2454). Manually setting max clock seems to have resolved my issue.

**Update:** Still crashing even under-clocked.


## Comment 2644228019

other (NONE) · GingerBobRoss · 2025-02-07T22:16:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644228019

Has anyone had any luck with the beta relaunch being able to create or join sessions.
Im on the latest ProtonGE (Not Bleeding-Edge) & ive tried experimental, but I am not able to join or have friends join me.
The game itself connects to the server just fine and you can load into 100 player lobbies, but you are stuck playing so due to a " unable to join/create session" error

## Comment 2644311501

other (NONE) · RandomLegend · 2025-02-07T23:23:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644311501

Currently i can play for around 2 minutes before the game crashing and often taking the whole DE (Hyprland) with it.

## Comment 2644412981

other (NONE) · mattipulkkinen · 2025-02-08T01:34:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644412981

> Has anyone had any luck with the beta relaunch being able to create or join sessions. Im on the latest ProtonGE (Not Bleeding-Edge) & ive tried experimental, but I am not able to join or have friends join me. The game itself connects to the server just fine and you can load into 100 player lobbies, but you are stuck playing so due to a " unable to join/create session" error

I  was able to play with others just fine, both through sending an SOS flare in my own quest or through joining other players' quests in-progress. I was playing on Proton Experimental bleeding-edge.

## Comment 2644446561

other (NONE) · FlameSoulis · 2025-02-08T02:45:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644446561

I'll have to find a way to get the logs, but a friend's Linux Mint 22.1 system with AMD Ryzen 5 7600X and RX 7700XT, and we've determined 'sprinting' seems to cause their crashes. The Suggestion for FSR fixing did work, but even with bleeding-edge, it doesn't appear to resolve the crashing problems. Using a controller also does not resolve the problem (in case it was related to the desktop environment having some hidden binding we weren't aware of).

## Comment 2644505077

other (NONE) · trm109 · 2025-02-08T04:57:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644505077

**For anyone running an AMD Graphics card**, here are my findings.

**Kernels**:
- No difference in stability between kernels. Tested on the Cachy (forgot version), Xanmod (6.12.9), Zen (6.13.1) and normal 6.12.12

**Mesa Version**
- 24.3.2 seems to have ~4-7% increase in FPS over 24.3.2? However a few users also report that 24.3.2 causes a crash.

**Proton Version**
- TKG Proton: _Doesn't work. Immediate crash on launch._
- Proton Experimental - Bleeding Edge: _Worked until I updated ~ 1 hr ago, now it causes the game to get stuck on a grey screen_
- ProtonGE9-23: _Works consistently on my system._
- ProtonGE9-22: _Very likely that this version is unstable for MHWilds. On a different system, I observed that GE9-22 would immediately crash upon loading the initial Chatacabra fight, and was immediately fixed by switching to GE9-23._

**Common Bugs**
FSR Upscaling not working (Beta)
- Seems to work with ProtonGE9-23 / Proton Experimental when you set the launch option `VKD3D_CONFIG=disable_uav_compression`. Be sure to set Upscaling Mode to AMD Native AA. 
- Works without the launch options in the benchmark for me.

FSR Framegen doesn't work / causes crash (Beta & Benchmark)
- I kind of have it working on the lastest Proton Experimental Bleeding Edge. There are some very noticeable artifacts, but it feels smooth enough to be worth it.
- Hasn't crashed yet, will report back if it does.

Grey Screen on launch (Beta)
- For me, removing mangohud from the launch options fixed it.
- If that fails, try ProtonGE9-23.

Game doesn't launch (Benchmark & Beta)
- If you are using gamescope, try launching without. 
- Otherwise, its probably related to your proton version (again, GE9-23 works best for me) and/or your graphics driver versions.

Desktop Environment crashes (Beta & Benchmark)
- This just seems to happen, I haven't found a way to fully fix it.
- Enabling FSR Frame Generation will make it happen faster.
- **There is a issue on the Mesa Gitlab tracking this issue**, but it hasn't had any correspondence from the team.



**Other**
- Steam launch option `VKD3D_DEBUG=none` was basically required for debugging on the **benchmark** (not required for beta). Otherwise, your logs would be filled with debug warnings.
- Hyprland 0.47.x causes a graphical bug, where the desktop/wallpaper flickers. Reverting to 0.46.2 resolved the issue.
- GPU Dropouts seem to be common, anyone saying their DE fails, or their screen freezes before being sent to their DM is likely experiencing a GPU dropout. 
  - The GPU dropouts in `journalctl -p 3` look like this `Feb 07 23:32:24 viceroy kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, but soft recovered`

**Specs**
- AMD Ryzen 7 7700X
- AMD Radeon RX 7900 GRE
- 32GB RAM
- Wayland (Hyprland)
- NixOS

## Comment 2644523034

other (NONE) · DreamingCuttlefish · 2025-02-08T05:48:41Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644523034

OS: Fedora KDE
Kernel: 6.12.11
CPU: AMD Ryzen 7 7800x3d
GPU: AMD RX 6950xt
GPU Driver: amdgpu, Mesa 24.3.3
Proton Experimental-Bleeding Edge

Crashes are reduced for me with bleeding edge but I still ran into a couple, seemingly when under high load/after the game has been open for a while. Sometimes it's just the game, sometimes it's the whole Plasma session including the discord call I'm in. 

## Comment 2644714401

other (NONE) · Eckoa · 2025-02-08T08:07:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644714401

> I'll have to find a way to get the logs, but a friend's Linux Mint 22.1 system with AMD Ryzen 5 7600X and RX 7700XT, and we've determined 'sprinting' seems to cause their crashes. The Suggestion for FSR fixing did work, but even with bleeding-edge, it doesn't appear to resolve the crashing problems. Using a controller also does not resolve the problem (in case it was related to the desktop environment having some hidden binding we weren't aware of).

While i disagree with the idea of running Mint on new hardware considering it tends to lag behind substantially, you would be better served to not guess what the issue is and see if perhaps running newer kernel,mesa,etc. might help.  Assuming mint isnt building their own mesa but using ubuntu or debian mesa it could be as old as an entire year out of date or at best a few months.

I just played for 5hrs straight and in total these past 2 days about 20hrs without crashing on Arch with latest mesa stable, kernel stable, and proton experimental with a Ryzen 7735hs and RX7700s laptop.

## Comment 2644716415

other (NONE) · Eckoa · 2025-02-08T08:13:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644716415

> OS: Fedora KDE Kernel: 6.12.11 CPU: AMD Ryzen 7 7800x3d GPU: AMD RX 6950xt GPU Driver: amdgpu, Mesa 24.3.3 Proton Experimental-Bleeding Edge
> 
> Crashes are reduced for me with bleeding edge but I still ran into a couple, seemingly when under high load/after the game has been open for a while. Sometimes it's just the game, sometimes it's the whole Plasma session including the discord call I'm in.

Now this is interesting, you are running similar software stack to me on arch. The entire session indicates a GPU reset but bleeding edge should be working around that. Does this happen if you run the benchmark on a loop? 

Lets keep in mind that the beta is in fact about 8 months old and has a number of issues. Its being used to simply test the networking of the game. Please use the benchmark to report issues graphically as it is far newer and more representative of the final product and doing fixes for the network beta is kinda of silly when it wont be around in 2 weeks.

## Comment 2644726265

other (NONE) · FlameSoulis · 2025-02-08T08:43:46Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644726265

> While i disagree with the idea of running Mint on new hardware considering it tends to lag behind substantially, you would be better served to not guess what the issue is and see if perhaps running newer kernel,mesa,etc. might help. Assuming mint isnt building their own mesa but using ubuntu or debian mesa it could be as old as an entire year out of date or at best a few months.
> 
> I just played for 5hrs straight and in total these past 2 days about 20hrs without crashing on Arch with latest mesa stable, kernel stable, and proton experimental with a Ryzen 7735hs and RX7700s laptop.

I'm just basing it from their observations. We had 2 hour sessions working fine, but then had another crash happen and they observed they were once again sprinting.

That said, Mint just released an update for Mesa 24.3.4 (Latest release), which I'm actually kind of shocked to see since I agree that it is usually held back quite a bit or at least delayed significantly. That said, the only selectable kernel is 6.8... which has me scratching my head, since I know that's not LTS. Oh well, I'll ask them to run an update for at least the latest Mesa. I have my own system to tinker with (Manjaro), so I can give that a try later (NVIDIA based, but eh... more fun for everyone).

EDIT: Nevermind, it was a flatpak. The latest package that did just come out is 24.2.8. Not too bad, honestly.

## Comment 2644731506

other (NONE) · Billli11 · 2025-02-08T08:59:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644731506

@FlameSoulis  
if the kernel is on 6.8, may be the crash is cause by [this](https://gitlab.freedesktop.org/drm/amd/-/issues/3131)?

Try manually setting your gpu clock speed.

## Comment 2644734003

other (NONE) · FlameSoulis · 2025-02-08T09:04:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644734003

> [@FlameSoulis](https://github.com/FlameSoulis) if the kernel is on 6.8, may be the crash is cause by [this](https://gitlab.freedesktop.org/drm/amd/-/issues/3131)?
> 
> Try manually setting your gpu clock speed.

Oooh... I did see that mentioned a few times in other discussions but I didn't think about it that much. I'll have to look more into it and see if I can explain an easy way for them to try it. All other games they've tried have worked fine so far (Proton or otherwise).

Thanks for the swift response. I'll update if anything happens.

## Comment 2645592235

other (NONE) · ruinedraziel · 2025-02-08T13:24:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2645592235

Game runs "fine" (cpu screaming for help), but I can´t join anyone posted quest or post any of my own, works fine if I'm on single player online, but the only way I can do anything is walking from camp to expeditions. The issue is not happening on Windows on my pc. Anyone got through this already? Erros R31A6-0-0:3 when I'm posting a quest, or R35A6-0-0:3 when I'm trying to join a quest (this include party link or environment link).

## Comment 2645783829

other (NONE) · ullll · 2025-02-08T15:27:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2645783829

I was getting crashes with GE-Proton9-23 and Proton Experimental. After switching to Proton Experimental-Bleeding Edge, I was able to do an hour long run, first a hunt with NPC, then joined an SOS flare hunt. Also enabling FSR framegen no longer cause crash.
Im using Steam flatpak on Fedora Silverblue with kernel 6.12.12 cachyos-lts running on an all-AMD laptop.

## Comment 2645914525

other (NONE) · D-Skye · 2025-02-08T19:34:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2645914525

> Game runs "fine" (cpu screaming for help), but I can´t join anyone posted quest or post any of my own, works fine if I'm on single player online, but the only way I can do anything is walking from camp to expeditions. The issue is not happening on Windows on my pc. Anyone got through this already? Erros R31A6-0-0:3 when I'm posting a quest, or R35A6-0-0:3 when I'm trying to join a quest (this include party link or environment link).

I've also run into this issue with being unable to do any quests online. Turning off crossplay (in the settings at the main menu) allows me to post/join quests again, but obviously greatly reduces the number of players I can play with since most people are going to leave crossplay on.

I'll also report that I still get pretty severe vertex artifacting (AMD 5700x3D, NVIDIA GeForce RTX 3080 570.86.16, Proton Experimental (not bleeding edge)).

## Comment 2645934712

other (NONE) · Eckoa · 2025-02-08T20:43:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2645934712

> Game runs "fine" (cpu screaming for help), but I can´t join anyone posted quest or post any of my own, works fine if I'm on single player online, but the only way I can do anything is walking from camp to expeditions. The issue is not happening on Windows on my pc. Anyone got through this already? Erros R31A6-0-0:3 when I'm posting a quest, or R35A6-0-0:3 when I'm trying to join a quest (this include party link or environment link).

The only thing i havent gotten to work is private lobbies, trying to join one doesnt work but otherwise all the other multiplayer options have worked for me. My friend on windows has the same issue so Im not sure its a proton thing or not

## Comment 2646078186

other (NONE) · ruinedraziel · 2025-02-09T05:32:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2646078186

Installed manjaro on an SSD and downloaded the game, simply installed steam game and discord, game runned fine, even quest posting and joining friends sessions, booted back on my arch, issue is there yet, so maybe is something missing in my arch installation? I'm comparing packages between the two, if anyone else want to try something similar.

## Comment 2646310285

other (NONE) · neon-grim · 2025-02-09T13:44:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2646310285

> reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2644505077

When it comes to the hyprland issue, I can approve that I'm also having the same experience, background blickers in an out, especially visible while windowed. If you have created an issue on the hyprland repo, please link it to me, so I can also make a report.

Secondly, I basically have the same system as you (7900XTX). The game doesnt crash on my end, but I've been experiencing some weird frame time hitching / stutter that werent there when I first booted the game in the second beta. Are you experiencing the same issue?



## Comment 2646323505

other (NONE) · IllestRat · 2025-02-09T14:17:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2646323505

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2643683108

So I tested it on my windows partition, I can run the game on medium settings with frame gen on averaging somewhere between 90-120 FPS. On my Arch setup, Lowest of low settings, Frame Gen on or off + FSR, I get TERRIBLE stuttering issues every few seconds mixed with almost half the frame rate my Windows version gets making it unplayable. My windows drive is a cheap 240GB SSD, meanwhile Linux is running on an M.2 SSD.

What's also odd is I'm not getting other issues others have posted about like hyprland, I get no flickering running the latest hyprland. I'm lost on where I might have messed up to make the game run smooth on Arch. I've tried everything @trm109 listed in their post but to no success. 

## Comment 2646404270

other (NONE) · neon-grim · 2025-02-09T16:56:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2646404270

> Reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2646323505

I just played with steam overlay disabled and without `VKD3D_CONFIG=disable_uav_compression` and my frame times were for the most part stable again. With steam overlay and the env var, I was getting massive frame time spikes every few seconds. 

I'm not using FSR or frame gen and with a mix of ultra and low I'm getting around 60-80 fps (bountiful season drops my fps to 60). Arkvelds fight though feels rather bad, since at times it can drop to the mid 40s. Try disabling Steam overlay and removing the env var.

## Comment 2646645796

other (NONE) · Jibodeah · 2025-02-09T23:11:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2646645796

I still had some system crashes on my AMD (GPU and CPU) system even on Proton Experimental bleeding edge branch. Seems to be a separate issue than the one that was fixed? The crashes are much rarer now at least.

Relevant bit of syslog

```
kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:4 pasid:32820)
kernel: amdgpu 0000:03:00.0: amdgpu:  in process MonsterHunterWi pid 7272 thread vkd3d_queue pid 7334
kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00008000e4600000 from client 0x1b (UTCL2)
kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00401430
kernel: amdgpu 0000:03:00.0: amdgpu: #011 Faulty UTCL2 client ID: SQC (data) (0xa)
kernel: amdgpu 0000:03:00.0: amdgpu: #011 MORE_FAULTS: 0x0
kernel: amdgpu 0000:03:00.0: amdgpu: #011 WALKER_ERROR: 0x0
kernel: amdgpu 0000:03:00.0: amdgpu: #011 PERMISSION_FAULTS: 0x3
kernel: amdgpu 0000:03:00.0: amdgpu: #011 MAPPING_ERROR: 0x0
kernel: amdgpu 0000:03:00.0: amdgpu: #011 RW: 0x0
kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=5310183, emitted seq=5310185
kernel: amdgpu 0000:03:00.0: amdgpu: Process information: process MonsterHunterWi pid 7272 thread vkd3d_queue pid 7567

```

## Comment 2648285644

other (NONE) · Hadrianneue · 2025-02-10T15:01:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2648285644

RT is disabled by capcom as it was with RE4R, bypassing with hidewineexports (requires non-valve proton) results in a silent crash

```
35401.460:0124:01ec:fixme:vkd3d-proton:d3d12_resource_create_reserved: Sparse is not supported for vk_format 126 with 1 samples, falling back to committed resource. Dimensions: width 1920, height 1080, level 1, layers 1. VRAM bloat expected.
35401.629:0124:0160:err:msvcrt:_wassert (L"!succ->pred_back_edge || succ->pred_back_edge == &entry",L"../src-vkd3d-proton/subprojects/dxil-spirv/cfg_structurizer.cpp",2387)
35401.629:0124:0160:trace:seh:raise (22)
```
log from the benchmark
[steam-3424520.log](https://github.com/user-attachments/files/18735495/steam-3424520.log)

tried amdvlk and amdpro, same problem
RX 6700 XT - Mesa 24.3.4-arch1.1 (mesa-git also gives the same error)

## Comment 2660212755

other (NONE) · Zottelchen · 2025-02-14T20:32:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660212755

Additionally to the mentioned issues above I have these fun strechted texture artifacts:
![Image](https://github.com/user-attachments/assets/dd72413b-793d-492b-9a72-7cb78b2ac547)

## Comment 2660690543

other (NONE) · rfsc-mori · 2025-02-15T03:20:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660690543

I'm not sure if this is useful for anyone, but I was using Proton Experimental bleeding edge and still got crashes after a while. I did all these as a troubleshooting attempt: I used a X11 session, used the Arch-packaged Steam instead of Flatpak, disabled my second monitor, disabled Frame Gen and used lowest settings, after this I was able to play for another 3 hours without any crashes.

I'm not sure if any single change would have fixed the problem and I don't plan on playing the Beta much more, but perhaps this could be useful for someone who still experience system crashes.

Note after reading the comment below:
I was already using LACT to limit my GPU Clock to 2510 MHz in 3D_FULL_SCREEN mode. It's a 7900 XTX Nitro+. I still had crashes between 0-30 minutes playing, some crashes happening just after leaving the base camp.

System info: Arch Linux, kernel 6.13.2, mesa 24.3.4, vulkan-radeon, using "steam" package (not steam-native-runtime), CPU: 5950x.

Crashes were happening with the Flatpak version of Steam as well, I did not test if it stopped crashing after disabling X session, second monitor (HDMI) and so on.

I could play the game without crashes on a Windows VM with GPU passthrough in the previous betas, had all settings on Ultra with frame gen for long hours (in other words: I think my hardware is fine).

## Comment 2660720845

other (NONE) · ruinedraziel · 2025-02-15T04:31:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660720845

> Game runs "fine" (cpu screaming for help), but I can´t join anyone posted quest or post any of my own, works fine if I'm on single player online, but the only way I can do anything is walking from camp to expeditions. The issue is not happening on Windows on my pc. Anyone got through this already? Erros R31A6-0-0:3 when I'm posting a quest, or R35A6-0-0:3 when I'm trying to join a quest (this include party link or environment link).

Just reporting back, could not reproduce any of the error codes after I did a clean install of manjaro and arch, tried everything I could think off, almost giving up and deciding to do a Full reinstall of my main system, decided to do steam file check on the game, 1 corrupted file, no more errors posting quests. If anyone is facing this errors u can try this also.

With the crashes, there's one issue with the kernel bosting GPU frequency above the gpu BIOS Max boost causing a page fault wich crashs the entire session, you might wanna try to limit the boost frequency using lact If u are on AMD. This also helps with Dragon's Dogma 2 crashes (this and using most recent proton for the cache issue). U can read about the click boost issue here: https://gitlab.freedesktop.org/drm/amd/-/issues/3131

Dont ignore the lact suggestion, at least try, It really works for the crashes wich kill the entire DE.

This essentially makes the GPU behave like its overclocked, causing instability, just use lact and set the Max GPU frequency to the manufacturer  specs of your GPU.

For the Black screen on menu either go for proton bleeding Edge or disable fsr/set fsr to Native AA.

If the menu is bricked and u cant click on anythin or it behave like the Arrow keys are pressed u can change from amdvlk to radv.

Games works "fine" after this adjustments, of course It still need optimizations on the game side, but at least is playable.

## Comment 2661088886

other (NONE) · ruinedraziel · 2025-02-15T20:25:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2661088886

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660690543

Sorry to hear the lact isn't helping, your setup does look similar to mine, except stronger. 
I'm on dual monitor RX7800xt with a R7 3800x
Using both on Display Port.

 Does your crashes behave like I described? I mean killing the DE session?

Player 5 full quests yesterday, no issues. Maybe It's worth mentioning this game might suffer from a cache bug related to re engine and amdgpu, there is a workaround in vkd3d-proton tested a few days ago, i'm using proton-ge 24, can u teste with that?
https://gitlab.freedesktop.org/mesa/mesa/-/issues/10883

## Comment 2661310307

other (NONE) · cheloide · 2025-02-16T08:08:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2661310307

>Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660690543 by @rfsc-mori :

Have you tried downgrading your kernel? I was crashing non-stop until I downgraded my kernel to *6.1.0-31-amd64* (Debian 12) and mesa drivers 24.2.8-1~bpo12+1 I've read 6.6 works too.

CPU:      AMD Ryzen 5950X
GPU:      AMD Radeon 6900XT
Kernel:  6.1.0-31-amd64
Drivers: mesa 6.1.0-31-amd64

Edit: Game still crashes but it takes considerably longer time to do so.
Edit 2: Current debian kernel (6.11) Env variable `MESA_DISK_CACHE_SINGLE_FILE=0` and [GE-Proton9-25](https://github.com/GloriousEggroll/proton-ge-custom/releases/tag/GE-Proton9-25), zero crashes.

Here's a video with frame generation enabled (FSR3 with native upscaling also known as no upscaling) ultra settings with my setup: https://www.youtube.com/watch?v=_SaBYJVzUeo


Release Edit: `MESA_DISK_CACHE_SINGLE_FILE=0`  and [GE-Proton9-25](https://github.com/GloriousEggroll/proton-ge-custom/releases/tag/GE-Proton9-25), still no crashes (91 min session).

## Comment 2661913004

other (NONE) · rfsc-mori · 2025-02-17T03:58:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2661913004

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2661088886

I had full system crashes with GPU timeout, requiring a power cycle using sysrq to power off.

Possibly related: my setup suffers from the "reset bug" when using VFIO/GPU Passthrough, it rarely recovers when anything goes wrong with the driver. And it's also affected by the GFX_OFF bug that causes system crashes seemingly randomly when its enabled. Note that this GFX_OFF bug didn't happen before a certain kernel version, I think it might have been around 6.7?... I can't recall, but I've decided to just use the known workaround (disable it with ppfeatureflags) and update my system despite the higher idle power usage.

I had tested Proton Experimental [bleeding-edge] and Proton GE 9.24, both had system crashes before trying X11 session and everything I mentioned before. It seemed to crash even if settings were at Lowest, and Frame Gen seemingly made the system crash faster.

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2661310307

I did not try to downgrade my kernel as I had tried that in the previous beta and still had crashes. I cannot recall exactly what versions I had tested but I'm quite confident I've tried 6.11 and 6.12, maybe 6.9 and 6.10 as well. This was before the cache fixes from bleeding-edge though.

I did try to downgrade mesa, but any version older than 24.3 would break my desktop session, requiring a reboot into single-user mode to upgrade the package again to fix the system.

Well, considering that:
- It'd crash no matter the in-game settings
- It'd also crash when using Arch's packaged steam instead of Flatpak

It seems likely that what fixed my system crashes was one of these:
- Maybe disabled VRR since it wasn't available on display settings on X11 even with mutter's experimental-features flag (Note that I did set Option "VariableRefresh" "true" in the Section "OutputClass" on my /etc/X11/xorg.conf.d/20-amdgpu.conf, but did not test if it worked or not - it might have been enabled as I didn't notice the usual issues with a 50 fps game on a 140 Hz monitor.)
- Using a full X11 session instead of Wayland
- Disabling the second monitor (HDMI, 60 Hz, 1080p, no VRR), keeping only the main monitor (Display Port, 140 Hz, 1440p, VRR)

I'll try to test these before the Beta ends but I cannot guarantee I'll have time to do so.

## Comment 2662015697

other (NONE) · IllestRat · 2025-02-17T05:01:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2662015697

> > Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2661913004)
 
Try doing what this person says here with LACT, fixed my crashes if on AMD. FSR and frame gen are still borked though.

> With the crashes, there's one issue with the kernel bosting GPU frequency above the gpu BIOS Max boost causing a page fault wich crashs the entire session, you might wanna try to limit the boost frequency using lact If u are on AMD. This also helps with Dragon's Dogma 2 crashes (this and using most recent proton for the cache issue). U can read about the click boost issue here: https://gitlab.freedesktop.org/drm/amd/-/issues/3131




## Comment 2662125659

other (NONE) · cheloide · 2025-02-17T05:53:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2662125659

> Reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2662015697

I did try LACT, it kept crashing the same as always. The only thing that stopped them for me was adding `MESA_DISK_CACHE_SINGLE_FILE=0` to the launch parameters.

I literally killed all monsters in a single session with the variable (I did not remove LACT though or disabled overclocking though), After "beating" the beta I removed it to try something else after that and it crashed within 5 minutes. You can see some people had the same result from disabling the shader cache [in the Dragon's Dogma 2 bug report](https://gitlab.freedesktop.org/mesa/mesa/-/issues/10883). 

**Disabling the shader cache is the next thing to try if latest proton, downgrading kernel or LACT don't not work.**

Edit for @SleepingLifeAway: I was adding to your reply since lact did nothing for me.

## Comment 2662149887

other (NONE) · IllestRat · 2025-02-17T06:11:27Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2662149887

> > Reply to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2662015697)

I might've messed up but I was suggesting LACT to @rfsc-mori sorry if so. 



## Comment 2663174180

other (NONE) · RavingGrob · 2025-02-17T13:40:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2663174180

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660690543

For me, the thing with LACT isn't that I underclocked my 6900XT — quite the opposite, I boosted it to 2700 MHz. What actually stopped my game from crashing, at least during the beta, was under**volting** by about 40mv. I went further than that afterwards, but 40ish is what made the game not crash at all. No other changes made any difference to stability. 

## Comment 2664269011

other (NONE) · ruinedraziel · 2025-02-18T00:19:20Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2664269011

> > Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2660690543
> 
> For me, the thing with LACT isn't that I underclocked my 6900XT — quite the opposite, I boosted it to 2700 MHz. What actually stopped my game from crashing, at least during the beta, was under**volting** by about 40mv. I went further than that afterwards, but 40ish is what made the game not crash at all. No other changes made any difference to stability. 

Nice! My suggestion isnt to underclock, but to set the Maximum to manufactor Spec, wich kernel is "not respecting" in some cases, 7600xt from xfx is where this problem really sucks, the board can barely stay stable for 20 min game sessions If u dont do this. Maybe, as the system is non intentionally overclocking undervolt is one way to get stable, makes kinda sense I guess. Nice to know!

## Comment 2689746963

other (NONE) · DeathTBO · 2025-02-28T05:17:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689746963

Just downloaded, never played the beta or benchmark. Using Proton Experimental or GE 9-25 I get a message from the anti-tamper.

Running with args: `MESA_DISK_CACHE_SINGLE_FILE=0 %command%`

![Image](https://github.com/user-attachments/assets/d972fabd-3b7b-40b1-848f-6669f1666d4b)

Fedora 41, Kernel 6.12.15, Mesa 24.3.4 5700xt. Proton Log (experimental):

[steam-2246340.log](https://github.com/user-attachments/files/19022406/steam-2246340.log)

## Comment 2689747859

other (NONE) · omegatengu · 2025-02-28T05:17:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689747859

We're getting screwed by Denuvo again

## Comment 2689749024

other (NONE) · RavingGrob · 2025-02-28T05:18:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689749024

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689746963

Try verifying the files, I got that same error message, but doing that fixed it for me.

## Comment 2689751608

other (NONE) · palaciav · 2025-02-28T05:21:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689751608

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689749024

This fixed it for me on Fedora 41.

## Comment 2689751654

other (NONE) · omegatengu · 2025-02-28T05:21:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689751654

It was probably because Capcom didn't click go until after the official launch time by accident, just retry and it should at least launch

## Comment 2689752921

other (NONE) · DeathTBO · 2025-02-28T05:22:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689752921

Thanks guys, I checked some forums and it seems a lot of Windows users were also getting hit by the anti-tamper. I did the verify files and restarted Steam, booting up now.

I wonder if we were just too fast.

## Comment 2689754748

other (NONE) · RavingGrob · 2025-02-28T05:24:22Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689754748

> Thanks guys, I checked some forums and it seems a lot of Windows users were also getting hit by the anti-tamper. I did the verify files and restarted Steam, booting up now.
> 
> I wonder if we were just too fast.

You don't know how hard my heart sank when I saw that message pop up, after all of getting to see the demo and benchmark working properly.

## Comment 2690002027

other (NONE) · 3a33d · 2025-02-28T08:12:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690002027

Game is crashing within 10 minutes and random textures are stretching. Attempted Proton-Hotfix, Proton-Experimental, as well as Proton-9.0.4

## Comment 2690107863

other (NONE) · westlyroots · 2025-02-28T09:07:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690107863

Game crashes GPU during intense scenes. LACT underclocking and undervolting, MESA_DISK_CACHE_SINGLE_FILE=0, and bleeding-edge has seemed to mitigate the issues. Before, I was only able to play a few seconds of the first seikret part. Now, I can get all the way to the first monster fight before my GPU dies. Still not playable. 6700 XT, Arch.

## Comment 2690146710

other (NONE) · neon-grim · 2025-02-28T09:24:41Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690146710

How are you guys able to get pass character creation? For some reason I'm unable to name my character, since the naming field fails to pop up, resulting in me getting stuck.

Edit: Apparently enabling FSR allows me to name my character.

## Comment 2690332955

other (NONE) · KucharczykL · 2025-02-28T10:50:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690332955

> Game is crashing within 10 minutes and random textures are stretching. Attempted Proton-Hotfix, Proton-Experimental, as well as Proton-9.0.4

I did not have any crashes but experienced the textures stretching, too. Applying `PROTON_HIDE_NVIDIA_GPU=1` fixed it but now I can't use DLSS, only FSR (expected since the game now thinks I have an AMD GPU).

## Comment 2690359324

other (NONE) · yumi-780 · 2025-02-28T11:03:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690359324

The game shows abnormal levels of vram usage. (The only app open is steam and the game)

 CPU : r5 5600; GPU : RX 7700XT; Proton : experimental bleeding edge; Mesa : 25.0.0; Kernel : 6.13.4; Nobara 41

![Image](https://github.com/user-attachments/assets/91093eb8-a6ac-4a4a-99ba-2387dea6e3a7)


## Comment 2690379791

other (NONE) · lebocra · 2025-02-28T11:13:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690379791

> The game shows abnormal levels of vram usage. (The only app open is steam and the game)
> 
i can report the same issue, the game is consistently reporting over 9GB of vram in use when btop and LACT report less than 6gb at worst, i've been looking for solutions/workarounds to no avail

## Comment 2690389431

other (NONE) · Doomguy1364 · 2025-02-28T11:18:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690389431

Game is still completely crashing my GPU driver within 5-10 minutes of being open; I've tried with and without MESA_DISK_CACHE_SINGLE_FILE=0 %command%, Proton Hotfix, Proton Experimental to no avail.

Distro:Arch Linux
DE: KDE Plasma (Wayland)
Kernel:6.13.4-arch1-1
RAM:32 GB
GPU Driver:4.6 Mesa 24.3.4-arch1.1
GPU:AMD Radeon RX 7900 XTX (radeonsi, navi31, LLVM 19.1.7, DRM 3.60, 6.13.4-arch1-1)
CPU:AMD Ryzen 7 7800X3D 8-Core



## Comment 2690428338

other (NONE) · SuperMewio · 2025-02-28T11:39:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690428338

I also had a driver reset but it was a single time within a 6 hour play session.

Operating System: Arch Linux 
KDE Plasma Version: 6.3.1
KDE Frameworks Version: 6.11.0
Qt Version: 6.8.2
Kernel Version: 6.13.4-zen1-1-zen (64-bit)
Graphics Platform: Wayland
Processors: 16 × AMD Ryzen 7 5700X3D 8-Core Processor
Memory: 62.7 GiB of RAM
Graphics Processor: AMD Radeon RX 7800 XT
Manufacturer: Gigabyte Technology Co., Ltd.
Product Name: B550 AORUS ELITE AX V2

## Comment 2690438353

other (NONE) · SuperMewio · 2025-02-28T11:44:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690438353

From journalctl

Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00301431
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:          MORE_FAULTS: 0x1
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:          WALKER_ERROR: 0x0
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:          MAPPING_ERROR: 0x0
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:          RW: 0x0
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x00008000e0600000 from client 10


## Comment 2690822053

other (CONTRIBUTOR) · HansKristian-Work · 2025-02-28T14:45:38Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2690822053

Just heads up that if anyone gets a CPU crash in Scarlet Forest there is a fix for it in https://github.com/HansKristian-Work/vkd3d-proton/pull/2363.

> Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:3 pasid:32803)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: in process MonsterHunterWi pid 8123 thread vkd3d_queue pid 8374)
Feb 28 04:20:44 archbtw kernel: amdgpu 0000:09:00.0: amdgpu: in page starting at address 0x00008000e0600000 from client 10

We have seen other reports about GPU faults in that VA range too. Where is this in the game? Given that sharing save games doesn't seem to work, how long does it take to get to a repro spot?

## Comment 2691009477

other (NONE) · Grious · 2025-02-28T15:59:08Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691009477

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689746963

I am getting this issue aswell, tried the with and without the launch arg. Tried with Proton Experimental and GE 9-25, tried verifying and rebooting, any other ideas?

Arch Linux  
Kernal: 6.13.4-zen1
CPU: Intel Core i9-9900K @ 16x 5GHz
GPU: AMD Radeon RX 6950 XT (radeonsi, navi21, LLVM 19.1.7, DRM 3.60, 6.13.4-zen1-1-zen)
Mesa: 24.3.4-1

## Comment 2691038817

other (NONE) · lebocra · 2025-02-28T16:12:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691038817

> > Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2689746963
> 
> I am getting this issue aswell, tried the with and without the launch arg. Tried with Proton Experimental and GE 9-25, tried verifying and rebooting, any other ideas?
> 
I have the same issue, apparently denuvo takes every version of proton as it's own device, meaning you either reached the 5 machine activation or the servers are getting hammered

from what I've seen online your best bet is just waiting until denuvo servers decide to let you in

## Comment 2691062039

other (NONE) · ClearlyClaire · 2025-02-28T16:24:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691062039

Same, I locked myself out of the Denuvo check by changing prefixes too many times while trying to get Dualsense haptics to work.

Otherwise the game played fine on Proton Bleeding Edge when I tried it before I got locked out. That being said, I guess using Bleeding Edge or otherwise changing Proton versions is unadvisable with this game because of the Denuvo activation limit.

## Comment 2691080995

other (NONE) · Andresdiaz16 · 2025-02-28T16:34:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691080995

Guys stop spamming that you have the same issue and just posting "same" with your pc specs, this is cluttering the thread and making it harder for people that are actually trying to look into this to follow.  Read the whole thread, if you find someone has the same issue as you react to it that's what those are for, no need notify 80+ people with the same thing someone else said before. 

## Comment 2691216576

other (NONE) · OnlyNocturnal · 2025-02-28T17:43:42Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691216576

same

Amd Radeon 7900xt
Amd Ryzen 7 7800x3d
Endavour OS

Completly crashing my Gpu driver

## Comment 2691225600

other (NONE) · SuperMewio · 2025-02-28T17:48:51Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691225600

> We have seen other reports about GPU faults in that VA range too. Where is this in the game? Given that sharing save games doesn't seem to work, how long does it take to get to a repro spot?

If it was 4:20 in the morning, maybe between 3 and a half to 4 hours? If it happens again, I will note a more accurate time.

I was around the begining area right before the quest where you head to the forest I believe. Maybe a few quests before. I cannot remember the exact location. I do remember getting back on and checking  to make sure I didn't lose anything at base camp so it may had been near there.

## Comment 2691233987

other (NONE) · Eckoa · 2025-02-28T17:53:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691233987

> We have seen other reports about GPU faults in that VA range too. Where is this in the game? Given that sharing save games doesn't seem to work, how long does it take to get to a repro spot?

Getting to the forest takes maybe 1-2hrs mostly due to cutscenes but if you just skip most of them maybe an hour of play. Its one of the first few quests in the game to visit there

## Comment 2691342727

other (NONE) · calvinkatz · 2025-02-28T18:56:22Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691342727

KERNEL: 6.13.5-2-cachyos
CPU: AMD Ryzen 7 9800X3D
GPU: AMD Radeon RX 6950XT 16GB
GPU DRIVER: 4.6 Mesa 25.1.0-devel (git-eb8017ca68)

I was able to play for about an hour without crash using `MESA_DISK_CACHE_SINGLE_FILE=0`, a -50mV undervolt, and proton-cachyos 9.0-20250211. But now I'm locked out because Denuvo.
VRAM is also an issue and lowering textures and meshes to High resolved. Compared to Windows VRAM usage is ~3-4GB higher.

## Comment 2691401214

other (NONE) · EthanWelsh1999 · 2025-02-28T19:30:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691401214

OS: Fedora 41
CPU: AMD Ryzen 7 7700X
GPU: AMD Radeon RX 6900 XT, 16GB VRAM
Driver: Mesa 24.3.4-8
Proton Experimental Bleeding edge, with `MESA_DISK_CACHE_SINGLE_FILE=0`

Getting crashes somewhat consistently in the Scarlet Forest, during the Uth Duna fight. Was getting crashes intermittently, roughly once every 30 mins prior to that. Possibly the water/rain effects during that fight hitting the VRAM limit? 

Cannot test any further due to the Denuvo error message popping up now but will update further once I can get back in and experiment a bit more


## Comment 2691630832

other (NONE) · froz3n · 2025-02-28T22:10:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691630832

> Getting crashes somewhat consistently in the Scarlet Forest, during the Uth Duna fight. Was getting crashes intermittently, roughly once every 30 mins prior to that. Possibly the water/rain effects during that fight hitting the VRAM limit?


Need more testing, but someone points out this pull request [https://github.com/HansKristian-Work/vkd3d-proton/pull/2363](https://github.com/HansKristian-Work/vkd3d-proton/pull/2363) and it seems to fix my crashes in the forest.

## Comment 2691669093

other (NONE) · PolarisPyra · 2025-02-28T22:42:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691669093

I've had random shader glitches and I have to recompile the in-game shaders each time I launch it 
1) Nvidia 4070 
2) arch linux 6.13.5 
3) hyprland with Wayland 

## Comment 2691691664

other (NONE) · Stryder0 · 2025-02-28T23:04:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691691664

I was able to solve frequent crashing by downgrading my kernel from 6.9.3 to 6.2.0-39. Using GE proton 9-25 (though experimental was also working.) I cannot say why this worked but i thought it would be valuable information to add. This is on pop! OS with a 7900XT GPU. 

## Comment 2691715579

other (NONE) · Billli11 · 2025-02-28T23:30:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691715579

@Stryder0 Look like cause by [this issue](https://gitlab.freedesktop.org/drm/amd/-/issues/3131) 
Try [manually setting clock speed](https://wiki.gentoo.org/wiki/AMDGPU#Power_management).

## Comment 2691847867

other (NONE) · zixaphir · 2025-03-01T02:11:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691847867

> The game shows abnormal levels of vram usage. (The only app open is steam and the game)

Try using an application that shows what's using your VRAM usage. I use nvidia so I'd use `nvidia-smi`. I'm not sure what to use on AMD, but reddit comments say `radeontop` or `radeon-profile`. I had a similar reading and I'd accidentally left ComfyUI running in the background.



## Comment 2691996637

other (NONE) · Grious · 2025-03-01T06:11:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2691996637

The benchmark for this game worked fine but the release seems to be causing a GPU crash on launch and I end up having to reboot the system .  Seems to be some type of page fault.  

Journalctl of the crash: https://pastebin.com/4kMk3PEm

## Comment 2692041178

other (NONE) · DeathTBO · 2025-03-01T07:37:58Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692041178

If it makes anyone feel better. It seems Windows users are crashing too. I had a buddy crash on discovering the forest, and randomly after that too.

So far the game has been relatively stable, but I did crash on the forest and scarlet forest areas. These crashes were hard crashes, my 3 monitors were showing artifacts and it wasn't recovering requiring a forced reboot. The 2nd time around, KDE Plasma tried to recover and restart the shell but it wasn't very stable there.

## Comment 2692176600

other (NONE) · DreiPixel · 2025-03-01T12:16:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692176600

so i did some testing with the VRAM stuff and noticed something weird.

(recorded with amdgpu_top, RX 7900XT so 20GB of Vram)

without anything running i have 3.4 gb ram used.

When i initially start the game, the game says the vram usage is 6.1gb for wilds and 13.63 for others. (after letting it idle in the menu a bit.) 
In amdgpu_top it says the Vram usage is 14285mB, thats almost the same as reported for "others" in game (might changed a bit between the screenshots i took).

after being in the game for a short amount, the game says it over the budget for vram. MHwilds at 6.1GB and other at 17.83GB. Meanwhile amdgpu_top says overall vram usage is about 18gb and wilds itself at about 15gb, 3GB is still the system itself.

So whats reported as others INGAME is also wilds itself. and wilds is increasing its vram usage.

after letting it run for a further amount wilds took ALL the vram and the game came to a crawl.

I tested this with amdvlk, Proton bleeding edge, and latest linux drivers stuff 

edit: this issue is not seen in Windows at all. also currently WAY better performance on windows

## Comment 2692343719

other (NONE) · dmolin93 · 2025-03-01T17:57:51Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692343719

I was having problems with crashes while playing last night, could only go about 20-30 minutes before crashing. Today  I switched to Proton Experimental (bleeding-edge) instead of Proton Hotfix and haven't crashed once. I do get the occasional micro-freeze, like it did right before a crash, but it gets back to normal within a second again.

I do however need to restart the game every now and again, I suspect it's the vram issue many people have reported.

My specs:
 AMD Ryzen 5 7600X
AMD Radeon RX 6700 XT
32 GB RAM
Manjaro w/ 6.13.1-2-MANJARO Kernel

## Comment 2692346032

other (NONE) · bjorkj · 2025-03-01T18:03:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692346032

After fixing the xid 109 error by getting the latest beta of nvidia drivers the game starts.
With proton experimental bleeding edge it now runs with HEAVY glitches. The game is not functional but runs. glitches, massive tearing and other stuff. Starts and character creation and menus works. But once you get into the game, textures start popping but it is mainly shader glitches I would say. The texture popping would make the game playable if it was the only thing that did not work.
No proton commands, just vanilla experimental bleeding edge.

It's something, nothing worked this morning

intel 7100
nvidia 2070 super
driver is 570.86 beta
Debian 12 bookworm 6.1.31 amd64 kernel

Still thinking about getting an old 240gb ssd and running windows on it for a while.


## Comment 2692356777

other (NONE) · GingerBobRoss · 2025-03-01T18:30:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692356777

Currently running Proton-Experimental (Bleeding Edge)
5800x
32GB ram 3600mhz
7900XT
CachyOS | kernel 6.13.5-2 | Mesa 25.0.0

I have the game running somewhat smoothly, but the game will get a massive memory leak causing causing my average 12GB consumption of Vram to Spike to use all 20GB causing me to be forced to quite the game and restart it.
MangoHUD will still report about 12GB of vram usage

![Image](https://github.com/user-attachments/assets/94136a03-878d-4600-b977-a7108e9f3c07)


## Comment 2692377660

other (NONE) · ClearlyClaire · 2025-03-01T19:29:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692377660

I got a crash against the Uth Duna. My build should include https://github.com/HansKristian-Work/vkd3d-proton/pull/2363

<details>
<summary>logs of the crash</summary>

```
[  755.876476] umip_printk: 23 callbacks suppressed
[  755.876482] umip: MonsterHunterWi[7765] ip:15bff6e21 sp:82def5c8: SGDT instruction cannot be used by applications.
[  755.876486] umip: MonsterHunterWi[7765] ip:15bff6e21 sp:82def5c8: For now, expensive software emulation returns the result.
[ 1124.999757] [drm] Fence fallback timer expired on ring comp_1.3.0
[ 1246.310667] [drm] Fence fallback timer expired on ring comp_1.3.0
[ 1442.917095] amdgpu 0000:2f:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:6 pasid:32784)
[ 1442.917105] amdgpu 0000:2f:00.0: amdgpu:  in process MonsterHunterWi pid 7476 thread vkd3d_queue pid 7712
[ 1442.917109] amdgpu 0000:2f:00.0: amdgpu:   in page starting at address 0x00008000d9d99000 from client 0x1b (UTCL2)
[ 1442.917112] amdgpu 0000:2f:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00601430
[ 1442.917115] amdgpu 0000:2f:00.0: amdgpu: 	 Faulty UTCL2 client ID: SQC (data) (0xa)
[ 1442.917117] amdgpu 0000:2f:00.0: amdgpu: 	 MORE_FAULTS: 0x0
[ 1442.917120] amdgpu 0000:2f:00.0: amdgpu: 	 WALKER_ERROR: 0x0
[ 1442.917122] amdgpu 0000:2f:00.0: amdgpu: 	 PERMISSION_FAULTS: 0x3
[ 1442.917123] amdgpu 0000:2f:00.0: amdgpu: 	 MAPPING_ERROR: 0x0
[ 1442.917125] amdgpu 0000:2f:00.0: amdgpu: 	 RW: 0x0
[ 1453.129795] amdgpu 0000:2f:00.0: amdgpu: Dumping IP State
[ 1453.134192] amdgpu 0000:2f:00.0: amdgpu: Dumping IP State Completed
[ 1453.144251] amdgpu 0000:2f:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=810021, emitted seq=810023
[ 1453.144256] amdgpu 0000:2f:00.0: amdgpu: Process information: process MonsterHunterWi pid 7476 thread vkd3d_queue pid 7918
[ 1453.426074] amdgpu 0000:2f:00.0: amdgpu: GPU reset begin!
[ 1453.718349] amdgpu 0000:2f:00.0: amdgpu: MODE1 reset
[ 1453.718356] amdgpu 0000:2f:00.0: amdgpu: GPU mode1 reset
[ 1453.718440] amdgpu 0000:2f:00.0: amdgpu: GPU smu mode1 reset
[ 1454.249903] amdgpu 0000:2f:00.0: amdgpu: GPU reset succeeded, trying to resume
[ 1454.250113] [drm] PCIE GART of 512M enabled (table at 0x0000008000F00000).
[ 1454.250146] [drm] VRAM is lost due to GPU reset!
[ 1454.250148] amdgpu 0000:2f:00.0: amdgpu: PSP is resuming...
[ 1454.329310] amdgpu 0000:2f:00.0: amdgpu: reserve 0xa00000 from 0x83fd000000 for PSP TMR
[ 1454.470140] amdgpu 0000:2f:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
[ 1454.470145] amdgpu 0000:2f:00.0: amdgpu: SMU is resuming...
[ 1454.470150] amdgpu 0000:2f:00.0: amdgpu: smu driver if version = 0x00000040, smu fw if version = 0x00000041, smu fw program = 0, version = 0x003a5a00 (58.90.0)
[ 1454.470154] amdgpu 0000:2f:00.0: amdgpu: SMU driver if version not matched
[ 1454.470187] amdgpu 0000:2f:00.0: amdgpu: use vbios provided pptable
[ 1454.546814] amdgpu 0000:2f:00.0: amdgpu: SMU is resumed successfully!
```
</details>

## Comment 2692435128

other (NONE) · dmolin93 · 2025-03-01T21:48:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692435128

Was stable most of the day, now started crashing with this

<details><summary>journal dump</summary>
<p>

mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:1 pasid:32798)
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:  in process MonsterHunterWi pid 29118 thread vkd3d_queue pid 29486
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00008000e4600000 from client 0x1b (UTCL2)
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00101430
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x0
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
mar 01 22:43:42 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu:          RW: 0x0
mar 01 22:43:51 dennis-pc discord[22343]: 22:43:51.135 › [OverlayUsageStatsManager] ScreenTypeAnalytics: Unknown screen type: -773874800 -773874800
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=22589298, emitted seq=22589300
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: Process information: process MonsterHunterWi pid 29118 thread vkd3d_queue pid 29486
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset failure
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset begin!
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: MODE1 reset
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: GPU mode1 reset
mar 01 22:43:53 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: GPU smu mode1 reset
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: GPU reset succeeded, trying to resume
mar 01 22:43:54 dennis-pc kernel: [drm] PCIE GART of 512M enabled (table at 0x00000082FEB00000).
mar 01 22:43:54 dennis-pc kernel: [drm] VRAM is lost due to GPU reset!
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: PSP is resuming...
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: reserve 0xa00000 from 0x82fd000000 for PSP TMR
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: RAS: optional ras ta ucode is not available
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: SECUREDISPLAY: securedisplay ta ucode is not available
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: SMU is resuming...
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: smu driver if version = 0x0000000e, smu fw if version = 0x00000012, smu fw program = 0, version = 0x00413>
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: SMU driver if version not matched
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: use vbios provided pptable
mar 01 22:43:54 dennis-pc kernel: amdgpu 0000:03:00.0: amdgpu: SMU is resumed successfully!


</p>
</details> 

## Comment 2692435276

other (NONE) · apoisonedgift · 2025-03-01T21:48:30Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692435276

> I got a crash against the Uth Duna. My build should include [HansKristian-Work/vkd3d-proton#2363](https://github.com/HansKristian-Work/vkd3d-proton/pull/2363)
> 
> logs of the crash

I was having a good experience with bleeding edge, but I can't get beyond the Uth Duna fight now. It crashes at the same point in the fight every time. I tried a bunch of different proton versions, different linux kernels, disabling PBO and other stuff, but got myself locked out due to denuvo's stupid authenticate limit. Until the Uth Duna fight I had one crash in about 7 hours and that was just a once off but now its crashed in that same fight every time.

CPU: 9800X3d
GPU: 6800XT
RAM: DDR5 64gb 6000mhz
Arch Linux, everything updated, kernel 6.13.5-arch1-1 (also tried updated zen)
KDE Plasma X11 (but also tried wayland)

## Comment 2692441827

other (NONE) · Zhaltor · 2025-03-01T22:05:59Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692441827

> Currently running Proton-Experimental (Bleeding Edge) 5800x 32GB ram 3600mhz 7900XT CachyOS | kernel 6.13.5-2 | Mesa 25.0.0
> 
> I have the game running somewhat smoothly, but the game will get a massive memory leak causing causing my average 12GB consumption of Vram to Spike to use all 20GB causing me to be forced to quite the game and restart it. MangoHUD will still report about 12GB of vram usage
> 
> ![Image](https://github.com/user-attachments/assets/94136a03-878d-4600-b977-a7108e9f3c07)

What's happening here is Wilds doesn't seem to recognise it's own memory usage. It'll always show your total system usage as "other" and add it's own projected usage on top. As for anyone having issue with the memory usage passively going up, I found that changing your texture settings resolves the issue. I flipped from Highest to High and back to Highest and my GPU memory usage went down and hasn't gone up since. 

## Comment 2692482653

other (NONE) · FlameSoulis · 2025-03-02T00:15:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692482653

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692435276

Somehow, a friend of mine with their setup didn't have any issues, and they aren't running bleeding edge.

CPU: AMD Ryzen 5 7600X
GPU: Radeon RX 7700 XT
RAM: DDR5 32GB 6000MHz
OS: Linux Mint 22.1 (I'll update with kernel info in a bit, but it should be the latest available for the distro)
Cinnamon on X11

## Comment 2692530385

other (NONE) · WhiteEyeDoll · 2025-03-02T03:04:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692530385

CPU: Intel Core i9 13900K
GPU: NVIDIA RTX 4080 OC
RAM: 64GB DDR5
OS: Arch Linux
Desktop: KDE Plasma 6 on Wayland
Kernel: 6.13.5-arch1-1
Driver: nvidia-open-dkms 570.124.04
Proton: Bleeding Edge

Running with default command line, maxed settings, NVIDIA scaling and frame gen creates stretched textures, crashes, and other random visual issues.

Running with: `PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 MANGOHUD=1 %command%` with FSR 3 (and frame generation) makes the game stable.
Some slight visual artifacts here and there still though.

AMD settings without hiding the NVIDIA GPU do not fix the issues for me.

Running at 2160p, 60Hz, AMD Native AA scaling, and maxed out settings sans the DLC high res textures. Only camps and other more intensive areas make the fps drop under 60.

I've gotten past Nu Udra fight so far.

This hints that there are some issues with NVIDIA cards specifically.

## Comment 2692545329

other (NONE) · bk304 · 2025-03-02T04:03:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692545329

Some times in the 3rd biome, my fps drops to 20 and my gpu usage stuck at 99%. I can cause this by returning from 3rd to 2rd biome. Seans to be a bug with unloading/loading texture and models.
Happenned too during Black flame fight.
The strange part is that even if I go back to game's menu, my GPU still at 99%. The only way I find to "fix" is to restart the game.

## Comment 2692574711

other (NONE) · zakk4223 · 2025-03-02T05:58:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692574711

I was having consistent crashes during Uth Duna with mesa 25.0, kernel 6.12.9 and proton bleeding edge.
I swapped to amdvlk and no more crashing. Unfortunately the performance is poor due what feels like constant shader stutter.

## Comment 2692598179

other (NONE) · apoisonedgift · 2025-03-02T07:20:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692598179

> I was having consistent crashes during Uth Duna with mesa 25.0, kernel 6.12.9 and proton bleeding edge. I swapped to amdvlk and no more crashing. Unfortunately the performance is poor due what feels like constant shader stutter.

I was just able to complete the uth duna quest using amdvlk - you are a wonderful human being! Fortunately performance on amdvlk is about the same as mesa for me (maybe slightly less, but more than playable). The shader compilation on amdvlk took over 30 minutes but worth it if I can play haha

Edit: spoke too soon - back at base camp and its stuttery af lol. Going back to mesa now that Uth Duna is done and hoping for the best lol

Further edit for anyone else trying to get this all working... I went back to amdvlk, set mesh detail to medium (instead of high) and set textures to medium and it seems to be stable now. I was originally using the high rest texture pack, but as others have said - something is very wrong with the VRAM usage in this game and I would run out of vram despite having more than enough according to the game. Even on high textures this would happen. Medium has it running nicely. Textures look terrible on medium but at least its playable.

## Comment 2692705428

other (NONE) · theludovyc · 2025-03-02T12:18:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692705428

Hello 👋 

I am happy to not be alone in difficulties 😊 

The  game in beta works "well" but now I have a freeze on languages selection. Fortunately, I can do an alt+tab to close the game with steam (click on "stop" button)(so only the game freezing and not my entire computer)(waiting a little does not change anything)
![Image](https://github.com/user-attachments/assets/6f9a00a1-da7d-452d-ad72-214149cd9187)

I use the nvidia-driver-535 (proprietary) on this computer
![Image](https://github.com/user-attachments/assets/43682dd3-68b2-435e-b6b0-fd348667b62b)

I try with proton hotfix / experimental / bleeding edge, and without and with those args

`PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 MANGOHUD=1 %command%`

`VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` (I try  this one  also with the driver-550, because I have an error about low_latency (like this one https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2450622534) but it didn't work)

## Comment 2692745418

other (NONE) · igxlin · 2025-03-02T13:56:58Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692745418

> Reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692598179

Thanks for the sharing! Switching to AMDVLK works on my end. When using radeon, the game will crash from time to time, which also makes my window manager freeze. After switching to AMDVLK, the game will only freeze for several seconds, instead of messing everything up.

However, due to the freezing, the experience of online gaming is terrible. X<

## Comment 2692752702

other (NONE) · lebocra · 2025-03-02T14:14:30Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692752702

I'm reporting back that amdvlk works for the crashes in my experience, I couldn't play enough to confirm the stuttering others report but in my system it works flawlessly 

## Comment 2692755940

other (NONE) · UleyeyeUwma · 2025-03-02T14:22:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692755940

I believe the GPU timeout is caused by upscaling, while testing and when I finally just gave up, decided to make the game look as good as it can at least, and when I put it at native res without using the upscaling part (no matter if fsr3 AA or leaving the render res at 100%) the game will just freeze for a few seconds, this freeze is only on the game, and I can continue using my pc or any other program, alt tab and all, the game will recover, altho disconnecting me from the online session.

I got to play for 6 hours without gpu timeouts and only a few freezes, no crashes and all in one sitting. Using the radv driver, mesa 25.0.0.

While the freeze happens my gpu goes to 100% during the freeze. My guess is that when this happens during the game, if you are upscaling from a lower res it will timeout the gpu for some reason.

## Comment 2692781963

other (NONE) · igormartimiano · 2025-03-02T15:27:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692781963

Just passing by to register a sprite related bug happening to some of us on AMD, apparently.

Quoting the user BuzzyWasaBee on Reddit: 
>  Monster Hunter Wilds is running surprisingly well. Much better than the beta did. Unfortunately there is an issue I didn't have before that you can see in the screenshots.
>
> The weapon bars on the top left are messed up. There is this big blue thing on the screen when a new quest starts. The item selection on the bottom right is also garbled.
>
> On the second screenshot you can see "quest fail" after a successful hunt.
>
> Not shown, but there are also heavy artifacts around the targeting rectule and also the quick menus corners.
>
> So far I have not seen anyone talk about this. It looks like the graphics for some UI elements are all stacked on top of each other.

Some screenshots I took myself:
![Image](https://github.com/user-attachments/assets/16a5cde1-f919-45ab-8dd7-a4f9d32c38f2)
![Image](https://github.com/user-attachments/assets/208f1626-2680-42be-a47d-b195042f8474)

Sys info:
![Image](https://github.com/user-attachments/assets/2bc69a0a-2186-4b88-b0ee-35fdb9bc7471)
Desktop: Gnome
Kernel: 6.10.6-chos2-chimeraos-1
Proton: Tried both Proton GE 9-25 and Proton Experimental Bleeding Edge

Other reports can be found [here](https://www.reddit.com/r/linux_gaming/comments/1j1fupc/ui_display_bug_in_mh_wilds/), as well as the original post.

## Comment 2692862944

other (NONE) · waycooler · 2025-03-02T19:07:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692862944

A friend of mine (who is playing on Windows) shared this last night: https://steamcommunity.com/app/2246340/discussions/0/596268233570403298

Config file is at steamapps/common/MonsterHunterWilds/config.ini

under [Render], change these two:
ParallelBuildProcessorCount=16
RenderWorkerThreadPriorityAboveNormal=Enable

That thread also suggests fixing a typo in the MinimumStreamingTextureResolution value - I didn't notice any benefit; texture streaming seems broken either way. But changing the two Render settings seems to have made everything else significantly better.

Before changing them, I was able to get close to ~30fps with low-medium settings, except in camps with lots of NPCs, heavy rain, etc. It felt a bit uncomfortable but playable. After changing the config file, I get ~30-40fps with ~high settings and it at least feels much better. Turning on FSR/framegen puts me around ~80fps on average. Camps etc are still a bit worse but much better than before.

Also, previously I was getting very heavy stuttering when starting the game, entering new areas, seeing new monsters (per session, it got better over time). That stuttering seems to be either significantly reduced or completely gone with the config changes.

## Comment 2692874441

other (NONE) · cheloide · 2025-03-02T19:40:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692874441

> I'm reporting back that amdvlk works for the crashes in my experience, I couldn't play enough to confirm the stuttering others report but in my system it works flawlessly

Have you tried `Proton Experimental Bleeding edge`? so far 3 hours into (from Uth duna to several runs of rey dau)

Looks like the Dragon's dogma bug workaround for vkd3d-proton made it into bleeding edge.

Edit 1: Just beat the octopus within a 6 hours session with bleeding edge.
Edit 2: Crashed again after 7 hours while hunting rathalos ???, Page fault
```
Mar 02 20:27:00.339393 kernel: amdgpu 0000:0c:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:4 pasid:32785)
Mar 02 20:27:00.341100 kernel: amdgpu 0000:0c:00.0: amdgpu:  in process MonsterHunterWi pid 10853 thread vkd3d_queue pid 11013
Mar 02 20:27:00.341256 kernel: amdgpu 0000:0c:00.0: amdgpu:   in page starting at address 0x00008000a5249000 from client 0x1b (UTCL2)
Mar 02 20:27:00.341376 kernel: amdgpu 0000:0c:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00401430
Mar 02 20:27:00.341494 kernel: amdgpu 0000:0c:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
Mar 02 20:27:00.341608 kernel: amdgpu 0000:0c:00.0: amdgpu:          MORE_FAULTS: 0x0
Mar 02 20:27:00.341720 kernel: amdgpu 0000:0c:00.0: amdgpu:          WALKER_ERROR: 0x0
Mar 02 20:27:00.341831 kernel: amdgpu 0000:0c:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Mar 02 20:27:00.341958 kernel: amdgpu 0000:0c:00.0: amdgpu:          MAPPING_ERROR: 0x0
Mar 02 20:27:00.342126 kernel: amdgpu 0000:0c:00.0: amdgpu:          RW: 0x0
Mar 02 20:27:10.559368 kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State
Mar 02 20:27:10.559642 kernel: amdgpu 0000:0c:00.0: amdgpu: Dumping IP State Completed
Mar 02 20:27:10.571354 kernel: amdgpu 0000:0c:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=17244064, emitted seq=17244066
Mar 02 20:27:10.571513 kernel: amdgpu 0000:0c:00.0: amdgpu: Process information: process MonsterHunterWi pid 10853 thread vkd3d_queue pid 11013
Mar 02 20:27:10.839359 kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset begin!
Mar 02 20:27:11.067364 kernel: amdgpu 0000:0c:00.0: amdgpu: MODE1 reset
Mar 02 20:27:11.067551 kernel: amdgpu 0000:0c:00.0: amdgpu: GPU mode1 reset
Mar 02 20:27:11.067700 kernel: amdgpu 0000:0c:00.0: amdgpu: GPU smu mode1 reset
Mar 02 20:27:11.583354 kernel: amdgpu 0000:0c:00.0: amdgpu: GPU reset succeeded, trying to resume
Mar 02 20:27:11.583533 kernel: [drm] PCIE GART of 512M enabled (table at 0x0000008000300000).
Mar 02 20:27:11.583548 kernel: [drm] VRAM is lost due to GPU reset!
```

## Comment 2692876245

other (NONE) · dmolin93 · 2025-03-02T19:46:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692876245

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692755940

This seems to have helped me, turned off upscaling (or I put it on fs3 AA) and it's been stable, can even have textures and mesh on high no problems.

## Comment 2692887809

other (NONE) · Eckoa · 2025-03-02T20:16:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692887809

> That thread also suggests fixing a typo in the MinimumStreamingTextureResolution value - I didn't notice any benefit; texture streaming seems broken either way.


thats not a typo, thats the correct value the application is expecting if you grep the values the application recognizes. 

## Comment 2693521090

other (NONE) · Austrum-lab · 2025-03-03T07:41:23Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2693521090

Are anyone succeed to play with DLSS on nvidia card?
With provided dlss I got a missing textures and artifacts, with updated manually (with .dll) and VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 I don't have an artifacts, but got crashes every 15mins.

For now I'm playing with PROTON_HIDE_NVIDIA_GPU=1 and FSR, so it's fine, but it's lower FPS and kinda blurry.

All of this on experimental bleeding edge, other versions doesn't work good for me.

## Comment 2693562614

other (NONE) · apoisonedgift · 2025-03-03T08:04:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2693562614

Well amdvlk was working, but after the most recent update (which wasn't meant to be anything to do with stability/performance) I can't get it to launch without using mesa, and still getting crashes in certain places with mesa lol...

## Comment 2693746139

other (NONE) · Meneldor · 2025-03-03T09:26:23Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2693746139

> Well amdvlk was working, but after the most recent update (which wasn't meant to be anything to do with stability/performance) I can't get it to launch without using mesa, and still getting crashes in certain places with mesa lol...

I also have the issue with amdvlk 2025.1, game does not start at all, it was working with the previous version.

With RadV, I got some crash from time to time but it works most of the time.
Will try without upscaling to see if it's better. 
Uth Duna was not doable, crashed everytime I got into the fight, passed it with amdvlk 2024.Q4.3.

## Comment 2694483347

other (NONE) · igxlin · 2025-03-03T13:53:42Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2694483347

https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692755940

Disable upscaling with mesa works on my end. Thanks for sharing.

## Comment 2694661841

other (NONE) · Hoodstrats · 2025-03-03T14:52:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2694661841

Yo, just jotting down my experience so far. 
```
Distro: Ubuntu 24.04.2 LTS
Kernel: 6.8.0-54-generic
RAM: 32 GB
GPU Driver: 4.6 Mesa 25.0.0 - kisak-mesa
GPU: AMD Radeon RX 6750XT 
CPU:AMD Ryzen 7 3700X 8-Core
```
Proton version: Experimental (not bleeding edge)

Current Steam launch parameters:
`VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 MESA_DISK_CACHE_SINGLE_FILE=0 VKD3D_CONFIG=disable_uav_compression __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 gamemoderun %command%`

In game I have everything set to low with FSR and Frame gen OFF. I can sometimes play for HOURS without issues and other times it crashes within 10 minutes. The crashes cause a full system lock-up which forces me to hard reset the PC. I've also tried playing with FSR and Frame gen ON but the crashes remain the same. They seem to be random and unpredictable. I haven't had consistent issues on 'x' fight like some of the other posts here.

(side note: even with everything on low it still doesn't run that good)

## Comment 2694947322

other (NONE) · dmolin93 · 2025-03-03T16:33:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2694947322

Gotten a new issue since I've gotten into High Rank, sometimes while playing the graphics goes black while the HUD is still visible. I can still control the game but I can't see anything since the game world itself is all black.

## Comment 2695208287

other (NONE) · cheloide · 2025-03-03T18:21:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695208287

> Reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2694947322

Are you using Upscaling? Sounds like the same issue we had in the beta.


## Comment 2695212908

other (NONE) · dmolin93 · 2025-03-03T18:23:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695212908

> Reply to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695208287)

Not using upscaling



## Comment 2695235223

other (NONE) · Austrum-lab · 2025-03-03T18:34:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695235223

> Are anyone succeed to play with DLSS on nvidia card? With provided dlss I got a missing textures and artifacts, with updated manually (with .dll) and VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 I don't have an artifacts, but got crashes every 15mins.

Mmmm, this evening I tried to play with DLSS again (with updated version 310.2) and it was smooth - I mean no lags and texture issues.
Just launched it with only mangohud without any parameters.  Framegen and reflex were also enabled
Strange.

There were game shaders update (idk, just steam downloaded 200mb of precached shaders) and proton (experimental bleeding edge) update today.


After 1.5 hours I got shutters and some texture bugs after that, but I suppose it was because I launched the game without LD_PRELOAD="" (it's an issue for me with steam games - without empty ld_preload it starts shuttering after 30-90 min).

## Comment 2695391565

other (NONE) · itinerare · 2025-03-03T19:50:20Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695391565

I'm also getting wildly inconsistent crashing (sometimes very quickly, sometimes after some hours), with no clear culprit. Thankfully, my system's *generally* been recovering ok (at least enough to let me log back in), though sometimes it needs to be force-rebooted.
I've tried both RADV and AMDVLK thus far-- the experience doesn't feel much different between the two, but given the inconsistency of the crashes it's hard to say. I've been playing with proton experimental, but not bleeding edge; the latter seemed to crash pretty quickly each time I tried it (alone or in conjunction with other tweaks).

While this build's a few years old now, by all indicators it should be able to comfortably run the game on medium settings, give or take, and the game *does* seem to perform pretty well... when not crashing.

As a diagnostic measure, I tried playing with `amdgpu_top` running; interestingly enough, when I hit a crash nothing was visibly maxed out. The game was using a significant amount of VRAM, but not all, with use increasing at a manageable rate (and occasionally decreasing as well).

EDIT: Tried disabling upscaling per the comments here; results are promising thus far!

```
Distro: EndeavourOS (Arch)
Kernel: 6.13.5.arch1-1
Drivers: Mesa 24.3.4; amdvlk 2025.Q1.2
RAM: 32GB
CPU: Intel i7-9700F
GPU: AMD Radeon RX 5700 XT
DE: Gnome (x11)
```

## Comment 2695898497

other (NONE) · brenmous · 2025-03-04T00:45:34Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695898497

I've also had regular page fault errors with radv, Nothing seems to really affect it (graphics settings, proton versions), other than the first few hours of the game were more stable. It can crash within a few minutes to an hour. Seems more often due to intense effects during fights but has also crashed just sitting in menus. I also didn't notice anything weird about GPU usage/VRAM on crash, despite the game warning me it was maxed out.

Using amdvlk (2024.Q4.3-1) it was also crashing. Also weirdly unstable when launching the game - if I try to do anything else while it's launching, I'll get a page fault, and it can take about a minute for the game to actually boot. The intial shader compilation for amdvlk took about 30 minutes compared to 5 or so for radv. I haven't had a crash with amdvlk since turning off upscaling/FSR. Also as someone else noted, the game won't launch for me with amdvlk 2025.Q1.2-1. Using amdvlk also seems like it solves the bug of the VRAM being maxed out in the in-game menu.

When radv works, the performance is actually pretty good. Amdvlk runs slightly worse but still more than acceptable.

```
EndeavourOS (Arch), 6.13.5.arch1-1
Using proton experimental bleeding edge
Mesa 25.0.0_devel.200442.bfa6b9b6551.d41d8cd-1 (git)/amdvlk 2025.Q4.3-1
Intel 12700K
6900XT
```

## Comment 2695938293

other (NONE) · neon-grim · 2025-03-04T01:20:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695938293

Edit: I was able to get the direct storage dll upgrade working. I simply symlink the new ones into the games root directory and then the old ones into the system32 directory of the games prefix. Finally I added a wine override for the two new dlls. I used symlink, since I dont like having external files pasted into the games directory, makes it easier to clean up.

I'm reporting my experience with the game.

I've been able to play through the entire base game without any crashes or other such issues. I do experience the VRAM leak when running the high texture pack, but on high textures this no longer seems to occur. 

The main issue I experience are some rather bad frame pacing, where every second or so a small spike can be observed, this mainly happens when the GPU isnt fully saturated and is also observable on windows, running a 4090. 

Additionally, I run the reframework dll in order to fix ultrawide grey bars, this might help with stability. I also tweaked the ini files to increase thread count and set render thread priority. I tried to swap the direct storage DLL, since the ones included with the game are broken, but this results in the game failing to start. 

I'm currently running at a mix of high, ultra and low settings, with FSR set to quality and frame gen active at 5120x1440@120hz. I have VRR disabled since otherwise I experience flickering with frame gen on. 

The only other issue I experienced was caused by steam overlay, which resulted in my frame times exploding after half an hour, but this is an well known issue with steam.

Here is my setup:

- Proton version: Experimental Bleeding edge / Proton 25
- Mesa: 25.1.0-devel mesa git
- Kernel: cachyos 6.13.4 lavd scheduler 
- Compositor: hyprland 0.47.2 git
- CPU: 7800X3D
- GPU: 7900XTX
- RAM: 32GB CL 30 6000MHZ

Here are the arguments I use:
```hyprTweaks -p; gamemoderun mangohud ENABLE_VKBASALT=1 WINEDLLOVERRIDES="dinput8, dstorage, dstoragecore=n,b" %command%; hyprTweaks -r```

Hyprtweaks is a tool I wrote to set specific hyprland options. I tried disabling rebar but I cant say I noticed a difference.

## Comment 2696005446

other (NONE) · ryzendew · 2025-03-04T02:15:27Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2696005446

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2695938293

explain this more what else needs to be done ```dstorage, dstoragecore=n,b"``` cause adding this the game does not start


## Comment 2696028554

other (NONE) · neon-grim · 2025-03-04T02:36:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2696028554

> reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2696005446

First copy the old DLLs into the system32 directory located in the games prefix.

Then replace the old DLLs in the games root directory with the new files obtained either from the official release on nuget, or from nexus mod.

Then add the launch argument with the dll override.

That said, you only need to do this, if simply replacing the DLLs in the games directory doesnt work.

## Comment 2696602003

other (NONE) · Brainde4dNerd · 2025-03-04T08:23:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2696602003

I experimented a bit with my settings yesterday evening and wanted to share my overall impressions: 

What I found for me is that it is hugely AMD FSR dependent. When FSR3 was active I had consistent crashes after a few minutes into a Odogaron Fight. Didn't matter how much I tweaked my settings. I was using Mangohud to monitor my VRAM usage. On 2560x1080p (lower than native) with High resolution texture packs and overall high graphics settings, it showed consistent 5-6Gb of usage. Which should be managable with a 16Gb GPU. Still crashed. 

I tried the Process count and priority fix via the config.ini, seemed to help a little bit with loading assets, but raisung CPU temperatures by 10°C while doing so. Going back into the game it crashed again after a few minutes.

Switching back to native resolution (3440x1440) and dropping my Texture resolution to medium and tweaking a few other settings had about the same VRAM usage, maybe 6-7Gb, but I got the game to run at ~40FPS in the Camp and about 60 in the Scarlet Forest and other areas. Here I got a good game session in of about 3 Hours. When I picked up a item in the scarlet forest it suddenly crashed - oh well it was just about time to go to sleep.

I mostly get hard crashes where I have to restart my PC, sometimes I get crashes where my Debian KDE /w Wayland resets back to desktop - here I noticed a lot of times that there were still Steam services running and even some MHWilds related tasks (checked with htop) and when I tried to start up the game again, it wouldn't start. While rebooting it showed some process termination timeouts from steam-related processes.
Rarely I could get back to fighting after a few seconds where the graphics driver seemed to have recovered.

I was running on Proton Experimental the entire time. I will try and get a log and System information in next time.

TLDR: I think my crashes are still VRAM-related even if I only get a reported 50% Memory usage at max. I will try radeontop today and monitor my memory usage this way.

## Comment 2696732307

other (NONE) · joker1007 · 2025-03-04T09:05:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2696732307

I think this game doesn't handle VRAM very well anyway.
I used Proton bleeding edge and turned down the graphics settings considerably, but it still consumed almost all of the 16GB of VRAM. Probably, there is a VRAM leak.
Nevertheless, I was able to continue the session for a reasonable length of time.
The longest session I have ever been able to run continuously was about 4 hours, and the settings and environment at that time were as follows

```
Kernel: Linux 6.13.5-gentoo
Mesa: 25.0.0
CPU: AMD Ryzen 9 5900X
GPU: AMD Radeon RX 6900 XT (16GB VRAM)
Memory: 64GB

Proton: experimental (bleeding edge)
Game Resolution: 1920x1080
FPS Limit: 60
Texture Quality: High
Upscaling: none
Vulkan Driver: RADV

and using gamescope (embedded mode)
```

FPS was generally 60 fps, but often stuttering.

If FSR is enabled, it crashes frequently even if I'm using only anti aliasing.
If I'm not using FSR, I can often continue for about one mission.
Also, I'm not sure if it's because of the changing Proton version or the crashes, but being locked out for 24 hours by anti-tamper is very stressful.

I have not tried amdvlk yet.

## Comment 2697077151

other (NONE) · TomateSoft · 2025-03-04T10:55:42Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697077151

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2696028554

Hi,

Just to confirm that this solved MOST crashes for me too (99%).
As an explainer: what this is is an update to DirectStorage 1.2.3 (apparently current version shipped with the game is 1.2.2). On Windows people did that as a fix to the stutter and freezes that plague the game and in turn it seems to prevent those gpu timeout crashes we do get on linux (if I understand correctly this thread).

My system;
```
Operating System: CachyOS Linux 
KDE Plasma Version: 6.3.2
KDE Frameworks Version: 6.11.0
Qt Version: 6.8.2
Kernel Version: 6.13.5-2-cachyos (64-bit)
Graphics Platform: Wayland
Processors: 12 × AMD Ryzen 5 7600X 6-Core Processor
Memory: 30.5 GiB of RAM
Graphics Processor 1: AMD Radeon RX 6800
Graphics Processor 2: AMD Radeon Graphics
Manufacturer: Micro-Star International Co., Ltd.
Product Name: MS-7D78
System Version: 1.0

I used the default AMD driver on CachyOS
```


The procedure I followed using @neon-grim comments
```
1- download dll upgrade from nexus mod "DirectStorage 1.2.2 Upgrade to 1.2.3 - IO Stutter Fix"
2- copy from steam/steamapps/common/MonsterHunterWilds/ dstorage.dll and dstoragecore.dll to steam/steamapps/compatdata/2246340/pfx/drive_c/windows/system32/ 
3- unzip the upgrade dll into steam/steamapps/common/MonsterHunterWilds/
4- make sure to disable any upscaling and framegen generation in the graphic options AND do not use the hi-res texture pack (I set texture quality to high for my 16GB VRAM GPU)
```

I used to crash quickly and reproducibly everytime, in the first 20s of gameplay in the tutorial and now I played a couple hours and also noticed a big stability improvement to the framerate (I also played a couple hours on release without crashes, the crashes started after the update 2 days ago).

I still get crashes here and there but at least I did complete the tutorial.

## Comment 2697268578

other (NONE) · magoolachub · 2025-03-04T11:48:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697268578

Update: not a placebo, new dstorage.dll does seem to load but dstoragecore.dll does not, I think if you just replace the dstorage.dll in the game exe folder with the new one and leave dstoragecore.dll alone it would have the same effect as following the above guide

I believe the above posts relating to the directstorage dll's are a placebo
Placing the new .dll files into the same directory as the game's EXE without any further commands is sufficient to have wine prioritise using these dll's rather than any wine provided builtin .dll as this is the default behaviour
However, doing so will result in the game not launching as it fails to load these new dll's and wine doesn't provide builtin options for these to fallback on and so the game won't launch
If you copy and paste the old .dll files shipped with the game to the system32 folder in the prefix these dll's then function as the builtin fallback
So by setting WINEDLLOVERRIDE to n, b you are telling the game to first load the native dll (the new dll you have provided) and then if that fails (which it does) load the builtin (the old dlls you copied to system32)

So, you're not using the new dll's at all, if the new dll's worked you could just drop them in the game exe directory and launch the game.

sry if I got anything wrong but pretty sure that's how it works and is what's happening

## Comment 2697364560

other (NONE) · TomateSoft · 2025-03-04T12:18:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697364560

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697268578

I'm actualy not using the WINEDLLOVERRIDE as you can see my description of the procedure I followed. Could you explain why you think the new DLL would fail to load?
For a test and using your comment I did try right now launching the game twice with `WINEDLLOVERRIDES="dstorage, dstoragecore=n" %command%`, so I believe this prevents from falling back into the wine builtin libraries since I'm using only the `n` flag as you explained correct? It launches without issues. This could still be anecdotal evidence of course.

However I had 100% crash in the first 20s to 30s of gameplay for the last 2 days (probably tried to play 20 times overall) until I did this dll upgrade. This is without changing anything: I did not update anything in my system nor did I change any of my in game settings (the ones I described). This seems to prove that this absolutely alleviate this issue in my scenario. I still had 1 crash over the course of 4 launching of the game and 3 hours of gameplay but at least it's now absolutely playable.

## Comment 2697407926

other (NONE) · magoolachub · 2025-03-04T12:29:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697407926

@TomateSoft could you please delete the old dll files you copied to the prefix system32 folder and then let me know if it still works? I think even if you set winedlloverrides to just n it will still fall back to b. If the game still works with no dstorage/dstoragecore in system32 then I guess it's some other issue on my system.

## Comment 2697431173

other (NONE) · yumi-780 · 2025-03-04T12:38:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697431173

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697268578

I used to not be able launch with the new dlls, so I tried using the launch option + copying the old dlls in sys32 as explained above, which did indeed fix it. What's weird is that removing those doesn't make it not launch, but I think this is simply because the files in the directory gets reverted to the ones pasted in sys32, as repasting the new dlls in the directory make it fail to launch again.

## Comment 2697502770

other (NONE) · magoolachub · 2025-03-04T13:04:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697502770

Looked into this a bit more, I think the ones in system32 still count as native rather than builtin, not sure, but the load preference is definitely exe folder first, then system32, more info [here.](https://gitlab.winehq.org/wine/wine/-/wikis/Wine-User's-Guide#dll-overrides)

When checking the proton logs, I can see that the game loads the new dstorage.dll seemingly without error however fails to load dstoragecore.dll and falls back to the one in system32 (at least on my system)

```
1196.587:0128:01f4:trace:loaddll:build_module Loaded L"Z:\\transistor\\magoo\\steamapps\\common\\MonsterHunterWilds\\dstoragecore.dll" at 00006FFFF6150000: native
1196.588:0128:01f4:trace:loaddll:free_modref Unloaded module L"Z:\\transistor\\magoo\\steamapps\\common\\MonsterHunterWilds\\dstoragecore.dll" : native
1196.589:0128:01f4:trace:seh:register_module_exception_directory count 85, max_count 512.
1196.589:0128:01f4:trace:loaddll:build_module Loaded L"C:\\windows\\system32\\dstoragecore.dll" at 00006FFFF6150000: native
```

so it's using the new dstorage.dll (1.2.3) but the original dstoragecore.dll (1.2.2) and there is some change which could explain why its alleviated instant crashing for some, apologies and will edit my original post

I've also been suffering from intermittent amdgpu page fault crashes so hopefully this helps

## Comment 2697617864

other (NONE) · TomateSoft · 2025-03-04T13:38:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697617864

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697502770

Yes that's it! I tried removing the dlls from system32 as you suggested and indeed it couldn't launch (black screen). When I added the old dstoragecore.dll back into the folder it finally launched and if instead I add the new dstoragecore.dll instead it black screens too...
So that's a pretty crazy situation, we run with mixed versions but at least it does work for now.

## Comment 2697997575

other (NONE) · carloscheddar · 2025-03-04T15:19:22Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2697997575

Bleeding Edge proton from yesterday(March 3) fixed most of my crashes. It only crashed for me after hours of playing when entering a new area instead of randomly crashing during fights so it's much better. I haven't changed anything else so I'm assuming it has to do with fixes pushed to proton.

```
Kernel: Linux 6.13.5-zen1
Mesa: Mesa 24.3.4-arch1.1
CPU: AMD Ryzen 9 3900X
GPU: AMD Radeon RX 6800 XT (16GB VRAM)
Memory: 32GB

Proton: experimental (bleeding edge)
Game Resolution: 5120x1440
FPS Limit: 60
Texture Quality: High
Upscaling: FSR3
Vulkan Driver: RADV
```

## Comment 2698787822

other (NONE) · dmolin93 · 2025-03-04T20:09:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2698787822

Added the new dll, proton experimental with bleeding edge, FSR3 but put on AA Native. Constantly crashing on high rank Uth Duna fight.

After latest crash the game refuses to go full screen, if I try to full screen it via plasma it just disappears.
Edit: Rebooting solved the fullscreen issue

Edit 2: After rebooting I could do the Uth Duna fight without crashing, guess something needed to get flushed out.

![Image](https://github.com/user-attachments/assets/484b2b17-e917-4561-8d14-855ee2c9e850)

## Comment 2698807158

other (NONE) · DeathTBO · 2025-03-04T20:17:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2698807158

The story missions for Uth Duna and Rathalos were the two that crashed me constantly. However, I have had very few issues since then. Proton GE 9-25 and even RE Framework. I am gonna try the new dll, but I doubt it will make a change.

They did just release some patch notes which included this:

    Performance & Stability

    Screen Rendering and Force Quits: Addressed issues causing screen rendering problems and force quits under certain conditions.
    Fixed game crashing issues.
    Fixes various glitch.
    Added stability and gameplay performance improvements.


## Comment 2698902368

other (NONE) · dmolin93 · 2025-03-04T21:04:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2698902368

I think the new dll made the game more unstable for me, crashed about 3 times in an hour when it's been quite stable for a couple of days.

## Comment 2700051964

other (NONE) · Miyazono1 · 2025-03-05T07:06:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2700051964

not sure if anyone else has reported this same issue, but my game will open and run fine for a while, but eventually VRAM usage overcaps and the game tanks down to single digit FPS. only fix i could find is restarting, where the cycle repeats.

RX7900XT and 5800x3D

## Comment 2700084496

other (NONE) · ghost · 2025-03-05T07:26:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2700084496

> not sure if anyone else has reported this same issue, but my game will open and run fine for a while, but eventually VRAM usage overcaps and the game tanks down to single digit FPS. only fix i could find is restarting, where the cycle repeats.
> 
> RX7900XT and 5800x3D

Same for me : let the game ran all the night, VRAM didn't move that much, but it seems that when you're moving around (when you're doing streaming asset), you're feeding more VRAM than you free it. Textures set to high, I've reached my 16gb VRAM cap. No issues on windows.

It seems that there is a VRAM leak on linux

## Comment 2700111834

other (NONE) · Billli11 · 2025-03-05T07:42:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2700111834

@Miyazono1 @gouineblade  
Did you downloaded the high texture pack and using highest texture setting ?  
Try lower the texture setting to high.

## Comment 2701032325

other (NONE) · theludovyc · 2025-03-05T14:00:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701032325

> https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2692705428

I finally manage to launch the game with proton bleeding edge, nvdia drive 550 and those args
`PROTON_HIDE_NVIDIA_GPU=1 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 %command%`

I can play in medium at 60 fps, but I have some artifacts...

## Comment 2701220383

other (NONE) · wwmm · 2025-03-05T15:10:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701220383

> https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2700051964

@Miyazono1 which gpu driver are you using? I have the same card running on `Mesa 24.3.4`, `kernel 6.13.5` and Proton Experimental and although VRAM usage gets quite high with the high resolution texture pack (sometimes almost 18 GB of VRAM is used) this did not break the game (or the computer) yet on my side.

Something that may be helping in my case is that my monitor is plugged in the Ryzen 9900X builtin GPU instead of on my RX7900XT. So all the desktop stuff that would be using GPU memory is running in the integrated card instead of the RX7900XT that is being used only by the game. What frees some additional memory to it. 

## Comment 2701253526

other (NONE) · RavingGrob · 2025-03-05T15:20:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701253526

I'm not sure if this one instance of "try reinstalling the game" was a fluke — but I was consistently unable to progress past a HR monster, and no matter what I changed, it crashed every hunt, 20+ times minimum. 

Reinstalled the game and I didn't crash once for the rest of my play session.

Perhaps something with Capcom's internal shader cache or proton's got corrupted? I saw someone on Windows had to purge the Shader cache, a few days ago. 

Edit: now that I'm thinking about it, upon the fresh install and allowing proton to compile the Shaders, capcom's "compiling shaders" screen never showed up even once. 

## Comment 2701621904

other (NONE) · mattipulkkinen · 2025-03-05T17:33:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701621904

There does seem to be something weird going on with the game's VRAM usage. The game displays VRAM usage for the game itself as well as "Other Applications", but only the "Other Applications" number seems to reflect reality.

<details><summary>The game's VRAM display with nvtop overlayed</summary>

![Image](https://github.com/user-attachments/assets/89f44ce2-d735-4385-b80d-2ccee17ec80d)

</details> 

Over time total displayed VRAM usage keeps creeping up, up to a point, and then it yo-yos around that point. Turning down the texture quality from highest down to just high improved the situation for me and the displayed VRAM usage no longer goes above my system total VRAM. I was able to play up to and past the credits with bleeding-edge Proton. Before this the game would eventually lock up for several minutes before recovering in a degraded extremely low-performance state.

Besides this VRAM issue the game has been working nicely for me. Only in one instance I ran into a problem where the whole world went black, except for white lights coming out of the spots where particle effects are supposed to be. I managed to blindly enter the tent (which I suppose loads another scene in game engine terms) and that fixed the issue, and I haven't seen it since. This could very well just be a bug in the game.

<details><summary>Graphics settings</summary>

![Image](https://github.com/user-attachments/assets/fcb68b3a-e3e4-42dd-ba3a-9d79bc6bb76c)

![Image](https://github.com/user-attachments/assets/e17106da-32c2-45d2-8e5e-2fb1f993b2b5)

![Image](https://github.com/user-attachments/assets/bce8a747-312d-409a-b940-70e901c00ea7)

</details> 

<details><summary>System information</summary>

```
Computer Information:
Manufacturer: ASRock
Model: X870E Taichi Lite
Form Factor: Desktop
No Touch Input Detected
Processor Information:
CPU Vendor: AuthenticAMD
CPU Brand: AMD Ryzen 7 9800X3D 8-Core Processor
CPU Family: 0x1a
CPU Model: 0x44
CPU Stepping: 0x0
CPU Type: 0x0
Speed: 5269 MHz
16 logical processors
8 physical processors
Hyper-threading: Supported
FCMOV: Supported
SSE2: Supported
SSE3: Supported
SSSE3: Supported
SSE4a: Supported
SSE41: Supported
SSE42: Supported
AES: Supported
AVX: Supported
AVX2: Supported
AVX512F: Supported
AVX512PF: Unsupported
AVX512ER: Unsupported
AVX512CD: Supported
AVX512VNNI: Supported
SHA: Supported
CMPXCHG16B: Supported
LAHF/SAHF: Supported
PrefetchW: Unsupported
BMI1: Supported
BMI2: Supported
F16C: Supported
FMA: Supported
Operating System Version:
Fedora Linux 41 (Workstation Edition) (64 bit)
Kernel Name: Linux
Kernel Version: 6.13.5-300.vanilla.fc41.x86_64
X Server Vendor: The X.Org Foundation
X Server Release: 12401006
X Window Manager: GNOME Shell
Steam Runtime Version: steam-runtime_0.20241127.109674
Client Information:
Version: 1738026274
Browser GPU Acceleration Status: Disabled
Browser Canvas: Unavailable
Browser Canvas out-of-process rasterization: Disabled
Browser Direct Rendering Display Compositor: Disabled
Browser Compositing: Disabled
Browser Multiple Raster Threads: Enabled
Browser OpenGL: Disabled
Browser Rasterization: Disabled
Browser Raw Draw: Disabled
Browser Skia Graphite: Disabled
Browser Video Decode: Disabled
Browser Video Encode: Disabled
Browser Vulkan: Disabled
Browser WebGL: Unavailable
Browser WebGL2: Unavailable
Browser WebGPU: Disabled
Browser WebNN: Disabled
Video Card:
Driver: AMD AMD Radeon Graphics (radeonsi, raphael_mendocino, LLVM 19.1.7, DRM 3.61, 6.13.5-300.vanilla.fc41.x86_64)
Driver Version: 4.6 (Compatibility Profile) Mesa 25.0.0
Desktop Color Depth: 24 bits per pixel
Monitor Refresh Rate: 119 Hz
VendorID: 0x1002
DeviceID: 0x13c0
Revision Not Detected
Number of Monitors: 2
Number of Logical Video Cards: 2
Primary Display Resolution: 2560 x 1440
Desktop Resolution: 5120 x 2035
Primary Display Size: 24.02" x 13.39" (27.48" diag), 61.0cm x 34.0cm (69.8cm diag)
Primary VRAM: 512 MB
Sound card:
Audio device: USB Mixer
Memory:
RAM: 47235 Mb
VR Hardware:
VR Headset: None detected
Miscellaneous:
UI Language: English
LANG: en_US.UTF-8
Total Hard Disk Space Available: 3813806 MB
Largest Free Hard Disk Block: 1784494 MB
Storage:
Number of SSDs: 2
SSD sizes: 5000G,4000G
Number of HDDs: 0
Number of removable drives: 1
Removable drive sizes: 62G
```

</details> 

[proton log.zip](https://github.com/user-attachments/files/19093771/proton.log.zip)

## Comment 2701814872

other (NONE) · MattyPixels · 2025-03-05T18:59:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701814872

> The game shows abnormal levels of vram usage. (The only app open is steam and the game)
> 
> CPU : r5 5600; GPU : RX 7700XT; Proton : experimental bleeding edge; Mesa : 25.0.0; Kernel : 6.13.4; Nobara 41
> 
> ![Image](https://github.com/user-attachments/assets/91093eb8-a6ac-4a4a-99ba-2387dea6e3a7)

To add to this issue:

-  If I use Steam installed via pacman (so it uses system libraries, such as MESA 25 and vulkan-radeon 25), there's this VRAM issue.
-  If I use the Steam Flatpak, which uses it's own libraries, it doesn't, it has normal VRAM usage.

As a temporary test, I've downgraded MESA and vulkan-radeon to version 24, and the VRAM issue is gone.

- OS : CachyOS (Arch based)
- Kernel : 6.13.5-2-cachyos
- CPU : AMD Ryzen 7 7800X3D @ 5.05 GHz
- GPU : AMD Radeon RX 7800 XT
- GPU Driver : amdgpu


## Comment 2701986914

other (NONE) · calvinkatz · 2025-03-05T20:24:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701986914

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701253526

Similar results for me as well. I did go a bit further and cleared:
* `~/.cache/mesa_shader_cache*`
* Steam compat directory for Wilds: `2246340`
* vkd3d files in game folder

After removing those items I verified game files, installed the updated `dstorage.dll`, and installed latest REFramework. It's been stable for a few hours with FSR completely disabled and using TAA instead.

* OS: CachyOS
* Kernel: 6.13.5-2-cachyos
* DE: KDE Plasma 6.3.2 (Wayland)
* CPU: AMD Ryzen 7 9800X3D
* GPU: AMD Radeon RX 6950 XT
* Driver: Mesa 25.1.0-devel (git-eb8017ca68)
* Proton: Bleeding Edge
* Launch Opts: `WINEDLLOVERRIDES="dinput8.dll=n,b" LD_PRELOAD="" gamescope -W 2560 -H 1440 -r 120 -f --hdr-enabled -- %command%`

Update: I enabled FSR Balanced and Frame Generation midway through my session (about 3hrs) and haven't crashed yet after about another 3hrs. It does stutter and sometimes temporarily freeze for half a second when switching zones.

## Comment 2702588513

other (NONE) · Jibodeah · 2025-03-06T02:19:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2702588513

I've managed to get past the Uth Duna story fight (which in ~5 previous attempts I would crash within a few minutes) by uninstalling and reinstalling the game and doing most everything that @calvinkatz did as well. That said it still wasn't perfect, there were many micro stutters which is suspect was some of those deleted cache files regenerating themselves. I also had multiple seconds long freezes which I suspect would've disconnected me had I been playing multiplayer.

A small note that REFramework seems to require the updated `dstorage.dll` (which I installed by simply replacing the one in the game files directory), otherwise the game crashes on boot with a wine C++ runtime assertion error.

* OS: Fedora 41
* Kernel: 6.13.5
* DE: KDE Plasma 6.3.2 (Wayland)
* CPU: AMD Ryzen 5 7600X
* GPU: AMD Radeon RX 6700 XT (12GB VRAM)
* Driver: Mesa 25.0.0
* Proton: Bleeding Edge
* Launch Opts: `WINEDLLOVERRIDES="dinput8.dll=n,b" gamemoderun %command%`

## Comment 2702687569

other (NONE) · SteveDaSteve · 2025-03-06T03:17:30Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2702687569

The game has done nothing but crash on boot on my setup. I’ve tried a good few proton versions (Hotfix, Experimental, GE, Experimental Bleeding Edge) and some launch options tweaks to no avail. Specifically, I have tried `PROTON_HIDE_NVIDIA_GPU=1 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 %command%` and a few variations that consist of one or a few of the commands mentioned.

I think the crash reporting tool is also crashing, as the only thing I find in the crash reports are folders with "MiniDump.dmp.tmp" files. Unfortunately, I am having trouble getting the file off of the machine so I can upload it here; I will update this comment with the attachment if I can figure out how to get it. (EDIT: It appears I cannot upload a .tmp file to a GitHub comment and the terminal woln't let me zip it either)

Trying to run this in Steam-Headless running in Unraid, so I can stream it to my Steamdeck on the only better hardware I have available. This setup ran the Open Beta Test and Benchmark Tool fine, so I'm not sure what changed that is making it crash.

OS: Debian GNU/Linux 12 (bookworm)
KERNEL: 6.6.68-Unraid
CPU: 12th Gen Intel Core i5-1235U
GPU: NVIDIA RTX 2000 Ada Generation
GPU DRIVER: NVIDIA 570.86.16
RAM: 64 GB

## Comment 2703065857

other (NONE) · Equivocal90 · 2025-03-06T07:48:12Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2703065857

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701814872

That is likely a Mesa 25 issue as running Steam Flatpak with mesa-git also results in the same abnormal VRAM reporting.

## Comment 2703279976

other (NONE) · ghost · 2025-03-06T09:26:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2703279976

> [@Miyazono1](https://github.com/Miyazono1) [@gouineblade](https://github.com/gouineblade) Did you downloaded the high texture pack and using highest texture setting ? Try lower the texture setting to high.

My textures are set to high

## Comment 2704570833

other (NONE) · froz3n · 2025-03-06T18:00:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2704570833

> That is likely a Mesa 25 issue as running Steam Flatpak with mesa-git also results in the same abnormal VRAM reporting.

Seems like this is the same issue : https://gitlab.freedesktop.org/mesa/mesa/-/issues/12686 ? The last known good version is Mesa 24.3.4, so yeah seems to be Mesa 25 issue.



## Comment 2704592642

other (NONE) · XaratosS · 2025-03-06T18:10:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2704592642

Hello. I thought I would chip in with my findings. I looked at the dmesg of my System. I am running Arch Linux with an AMD RX 7900 XTX. 
This shows up in dmesg:

```
[ 5600.258115] umip: MonsterHunterWi[18239] ip:7db75b44 sp:7da60530: SGDT instruction cannot be used by applications.
[ 5600.258120] umip: MonsterHunterWi[18239] ip:7db75b44 sp:7da60530: For now, expensive software emulation returns the result.
[ 5632.305033] umip: MonsterHunterWi[18241] ip:7e971c3c sp:7e460530: SGDT instruction cannot be used by applications.
[ 5632.305041] umip: MonsterHunterWi[18241] ip:7e971c3c sp:7e460530: For now, expensive software emulation returns the result.
[ 5636.245160] umip: MonsterHunterWi[18237] ip:15ed7fa52 sp:7d16f0b8: SGDT instruction cannot be used by applications.
[ 5886.606022] umip_printk: 19 callbacks suppressed
[ 5886.606027] umip: MonsterHunterWi[18237] ip:15ed7fa52 sp:7d16f0b8: SGDT instruction cannot be used by applications.
[ 5886.606033] umip: MonsterHunterWi[18237] ip:15ed7fa52 sp:7d16f0b8: For now, expensive software emulation returns the result.
[ 5888.315547] umip: MonsterHunterWi[18251] ip:154e671ce sp:807ef090: SGDT instruction cannot be used by applications.
[ 5888.315555] umip: MonsterHunterWi[18251] ip:154e671ce sp:807ef090: For now, expensive software emulation returns the result.
[ 5888.316690] umip: MonsterHunterWi[18251] ip:1575e2385 sp:807efa30: SGDT instruction cannot be used by applications.
[ 6183.257296] umip_printk: 31 callbacks suppressed
[ 6183.257303] umip: MonsterHunterWi[18237] ip:15ed7fa52 sp:7d16f0b8: SGDT instruction cannot be used by applications.
[ 6183.257311] umip: MonsterHunterWi[18237] ip:15ed7fa52 sp:7d16f0b8: For now, expensive software emulation returns the result.
[ 6185.010673] umip: MonsterHunterWi[18252] ip:154e671ce sp:80bef090: SGDT instruction cannot be used by applications.
[ 6185.010682] umip: MonsterHunterWi[18252] ip:154e671ce sp:80bef090: For now, expensive software emulation returns the result.
[ 6185.011714] umip: MonsterHunterWi[18252] ip:1575e2385 sp:80befa30: SGDT instruction cannot be used by applications.
[ 6342.697258] umip_printk: 9 callbacks suppressed
[ 6342.697264] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 6342.697271] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
[ 6368.907033] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 6368.907043] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
[ 6395.467613] umip: MonsterHunterWi[18239] ip:155488f0e sp:7da6f5a0: SGDT instruction cannot be used by applications.
[ 6464.684164] umip_printk: 3 callbacks suppressed
[ 6464.684170] umip: MonsterHunterWi[18244] ip:154af0fc1 sp:7f3ff708: SGDT instruction cannot be used by applications.
[ 6464.684178] umip: MonsterHunterWi[18244] ip:154af0fc1 sp:7f3ff708: For now, expensive software emulation returns the result.
[ 6518.064061] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 6518.064072] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
[ 6818.704075] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 6818.704084] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
[ 6884.568612] umip: MonsterHunterWi[18240] ip:7e4716d8 sp:7e060530: SGDT instruction cannot be used by applications.
[ 6884.568619] umip: MonsterHunterWi[18240] ip:7e4716d8 sp:7e060530: For now, expensive software emulation returns the result.
[ 6993.091811] umip: MonsterHunterWi[18240] ip:7e471c20 sp:7e060530: SGDT instruction cannot be used by applications.
[ 6993.091820] umip: MonsterHunterWi[18240] ip:7e471c20 sp:7e060530: For now, expensive software emulation returns the result.
[ 6993.228542] umip: MonsterHunterWi[18254] ip:15e6d473f sp:814eeb08: SGDT instruction cannot be used by applications.
[ 6993.228556] umip: MonsterHunterWi[18254] ip:15e6d473f sp:814eeb08: For now, expensive software emulation returns the result.
[ 6994.695369] umip: MonsterHunterWi[18237] ip:15ed7fa52 sp:7d16f0b8: SGDT instruction cannot be used by applications.
[ 7119.382465] umip_printk: 43 callbacks suppressed
[ 7119.382471] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: SGDT instruction cannot be used by applications.
[ 7119.382479] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: For now, expensive software emulation returns the result.
[ 7119.382886] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: SGDT instruction cannot be used by applications.
[ 7119.382890] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: For now, expensive software emulation returns the result.
[ 7119.440117] umip: MonsterHunterWi[18240] ip:154af0fc1 sp:7e06f778: SGDT instruction cannot be used by applications.
[ 7250.078204] umip_printk: 23 callbacks suppressed
[ 7250.078209] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: SGDT instruction cannot be used by applications.
[ 7250.078215] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: For now, expensive software emulation returns the result.
[ 7250.078453] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: SGDT instruction cannot be used by applications.
[ 7250.078456] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: For now, expensive software emulation returns the result.
[ 7250.078578] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f708: SGDT instruction cannot be used by applications.
[ 7394.589021] umip_printk: 5 callbacks suppressed
[ 7394.589032] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 7394.589041] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
[ 7415.783041] perf: interrupt took too long (2650 > 2500), lowering kernel.perf_event_max_sample_rate to 75000
[ 7513.154248] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 7513.154259] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
[ 7855.515251] umip: MonsterHunterWi[18253] ip:1587aaaf9 sp:810edf40: SGDT instruction cannot be used by applications.
[ 7855.515266] umip: MonsterHunterWi[18253] ip:1587aaaf9 sp:810edf40: For now, expensive software emulation returns the result.
[ 7912.929115] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f778: SGDT instruction cannot be used by applications.
[ 7912.929126] umip: MonsterHunterWi[18239] ip:154af0fc1 sp:7da6f778: For now, expensive software emulation returns the result.
[ 8210.984153] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: SGDT instruction cannot be used by applications.
[ 8210.984171] umip: MonsterHunterWi[18254] ip:1587aaaf9 sp:814edf50: For now, expensive software emulation returns the result.
```

I have the following drivers installed for the System:

```
mesa 1:24.3.4-1
mesa-utils 9.0.0-5
xf86-video-amdgpu 23.0.0-2
```

The Kernel that I am using is 6.13.5-zen1-1-zen. 

The issue that I am having is, that the game just freezes whenever I play with other people. Singleplayer is completly fine. 


## Comment 2705389196

other (NONE) · AmandaRoseChaqueta · 2025-03-07T02:41:24Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2705389196

Seems like the latest Blending Edge version of proton fixed the crashes for me, run for 7 hours without encounter them! Before it took only 5 minutes into a hunt to cause a gpu driver timeout.

Hopefully this lands soon for normal experimental.

## Comment 2705511047

other (NONE) · Eckoa · 2025-03-07T04:38:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2705511047

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2704592642


Pretty positive thats a big nothing burger, UMIP prevents certain things executing in user space and wine fixed issues with it some time ago. This is likely just noise in dmesg.

You can try adding `clearcpuid=514` to your kernel launch parameters to disable UMIP to see what happens and it will clear up dmesg

## Comment 2705558576

other (NONE) · calvinkatz · 2025-03-07T05:23:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2705558576

> Seems like the latest Blending Edge version of proton fixed the crashes for me, run for 7 hours without encounter them! Before it took only 5 minutes into a hunt to cause a gpu driver timeout.
> 
> Hopefully this lands soon for normal experimental.

Seconded. I luckily got a 9070XT today, ran with the same settings as my previous post and no issues other than the same stuttering every now and then. FSR and Frame Generation all worked without crashing.

## Comment 2706071285

other (NONE) · Brainde4dNerd · 2025-03-07T10:20:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2706071285

So after my last post I tried a few things:

I still had consistent crashing after a few minutes into fights in Ruins of Wyveria and Scarlet Forest - VRAM reported normal usage. (7-8Gb out of 16Gb). So I got a little desperate.

Tried the directstorage.dll - fix. Seemed to have helped with texture streaming. But no help with my crashes.

Tried the CPU-count fix in (already reported that last time) setting it from 8 to 16. Apparently helped with some of the stutter but no guarantee, can be placebo too.

Proton Experimental bleeding-edge - no real improvement for me.

I then installed the latest REFramework from NexusMods found here: https://www.nexusmods.com/monsterhunterwilds/mods/93
Just drag and drop the .dll into the MHWilds game folder, it starts automagically with the game.
I feel like the game was running a bit smoother and it has a fix for the ugly bars on the sides of a Ultrawide monitor, and apparently fixes some of the issues with Capcoms Denuovo , but no fix for the crashes.
Still would recommend installing it.

amdvlk 1.4 on mesa 22.3 didn't work me, Game wouldn't even start.

After that I tried going to Debian Trixie (Testing release) from my currently Debian 12 stable - because of the updated 24.3.4 Mesa drivers. Lo and behold - without me doing anything extra after the update I got a message for Vulkan shaders - which I didn't turn on myself. Like other reported it took an eternity to do the preshader-caching. Game started up as usual. Trying a few hunts and for what seemed to be the spots where the game usally crashed, I got a lagspike of about half second to a second and the game recovered fine - multiple times. VRAM usage the same as before, running on 3440x1440p.

Haven't tried out FSR yet.

Anyone who can confirm what I found? (Mesa 24.3.4 update)

OS: Debian GNU/Linux 12 ("testing" release)
KERNEL: 6.12.12
CPU: AMD Ryzen 9 5950X
GPU: AMD Radeon RX6900XTXH
GPU DRIVER: Mesa 24.3.4
RAM: 32 GB

## Comment 2706083136

other (NONE) · ghost · 2025-03-07T10:25:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2706083136

> After that I tried going to Debian Trixie (Testing release) from my currently Debian 12 stable - because of the updated 24.3.4 Mesa drivers. Lo and behold - without me doing anything extra after the update I got a message for Vulkan shaders - which I didn't turn on myself. Like other reported it took an eternity to do the preshader-caching. Game started up as usual. Trying a few hunts and for what seemed to be the spots where the game usally crashed, I got a lagspike of about half second to a second and the game recovered fine - multiple times. VRAM usage the same as before, running on 3440x1440p.
> 
> Haven't tried out FSR yet.
> 
> Anyone who can confirm what I found? (Mesa 24.3.4 update)

Is it possible that when you were crashing, you didn't have the fix commited to proton-experimental yet?

## Comment 2706201391

other (NONE) · Brainde4dNerd · 2025-03-07T11:21:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2706201391

> Is it possible that when you were crashing, you didn't have the fix commited to proton-experimental yet?

As far as I remember I switched over to Proton Experimental Bleeding Edge shortly after my last post and didn't switch back since then. (3 days ago)

I am going to update this evening againg as I am not 100% certain if I have't reverted back to non-bleeding edge while testing...

## Comment 2707259811

other (NONE) · Brainde4dNerd · 2025-03-07T19:38:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707259811

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2706201391

Yup just checked, had Proton Experimental Bleeding Edge for the entire time, so it was still crashing for me yesterday, even with the latest fix...

Of course, this requires a few more hours of testing, for which I am happy to sacrifice myself for the common good :p

## Comment 2707371576

other (NONE) · SteveDaSteve · 2025-03-07T20:26:12Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707371576

> A follow up on https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2702687569

I managed to get my crash report if anybody is interested. I generated this crash report today, running Proton Experimental Bleeding Edge, with no launch options: [MiniDump.dmp.tmp.zip](https://github.com/user-attachments/files/19133076/MiniDump.dmp.tmp.zip)

I also just went and ran MHWilds with `PROTON_LOG=1 %command%`, same Proton version, to generate this log: [steam-2246340.log](https://github.com/user-attachments/files/19133371/steam-2246340.log)

## Comment 2707746551

other (NONE) · ZeroKnight · 2025-03-07T23:57:20Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707746551

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2705511047

I've been going crazy the last couple of days trying to find other reports of this behavior in the Mesa and vkd3d issue trackers and not finding anyone mentioning this specific behavior with VRAM. Didn't think to check here until now; so glad I'm not the only one experiencing this.

To add on with my own observations, I noticed this immediately after updating to the `20250305` openSUSE Tumbleweed snapshots, coming from a `20250130` snapshot, which meant going from the same last-known-good Mesa **24.3.4** to Mesa **25.0.0** as others have.

To clarify, unlike some others in this thread I am *not* experiencing any crashes, so I think there are two separate issues at play here affecting different sets of people. I fortunately haven't experienced even a single crash, but the VRAM exhaustion ends up effectively the same.

## System/Environment Information

- OS: openSUSE Tumbleweed
- CPU: AMD Ryzen 7 5700X
- GPU: AMD Radeon RX 7900 XT (GFX1100/Navi31)
- RAM: 32GB DDR4

| Tumbleweed Snapshot | Date In Use | VRAM Issue? | Kernel Version | Mesa Version | Proton Version                  |
| ------------------- | ----------- | :---------: | -------------- | ------------ | ------------------------------- |
| `20250130`          | 2025-03-03  | No          | 6.11.5-1.1     | 24.3.4       | Experimental (**Not bleeding**) |
| `20250305`          | 2025-03-04  | **Yes**     | 6.13.5-1.1     | 25.0.0       | Experimental (**Not bleeding**) |

Unfortunately, I don't know what precise Proton Experimenal builds I was using at each time, but I had been using the non-bleeding Experimental since launch day.

### Mesa **24.3.4** Observations (Good)

The game did not over-report VRAM and did not exceed the maximum amount of my card (20GB). If anything, it appeared to vastly *under*-report usage as observed in [Mesa#12686][1]; I recall MHW only reporting about 8-10GB total when `btop` reported around 18-19GB used. The grey "Other Applications" bar in-game was quite low.

Since the game never overshot my total VRAM (as far as I know), it never ended up doing the cascading VRAM spilling into GTT which causes the eventual indefinite performance drop-off as has been an issue ever since [Mesa PR 6833][2] and well-reported over the years: [8763][3], [5902][4], [9371][5], [12713][6], etc.

The game played with its usual stuttering and performance issues, but it never had the VRAM overflow issue. I could (and did) play for several hours at a time without ever crashing, restarting, or experiencing any launching issues.

### Mesa **25.0.0** Observations (Bad)

This is when the VRAM *over*-reporting began. Right when you get to the start screen, VRAM is already reported much higher in-game than it ever was before, with the characteristic huge value for "Other Applications" as shown by @MattyPixels in https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2701814872.

Playing the game for even 10 minutes while moving through areas and loading in different textures/effects, VRAM *rapidly* climbs with the in-game VRAM usage showing upwards of **25.8GB** for me; well over my actual 20GB capacity. Using **amdgpu_top**, I can see that once all of my VRAM is allocated, GTT allocations gradually rise higher and higher. Once GTT exceeds around 4-5GB on my system, the infamous massive performance degradation happens, GPU usage stays pinned at 100%, and framerate drops to an awful, inconsistent 16-20FPS.

---

I never experienced a crash on either Mesa version in 41 hours of playtime on Proton Experimental (95% of that time was on Mesa 24.3.4). I'm hesitant to believe that *this particular issue* is Proton-related, but I wanted to add my findings here to help others with the same issue that happen to find themselves here.


[1]: https://gitlab.freedesktop.org/mesa/mesa/-/issues/12686 "[radv][regression] Multiple games detect the wrong amount of vram"
[2]: https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/6833 "radv: Improve spilling on discrete GPUs."
[3]: https://gitlab.freedesktop.org/mesa/mesa/-/issues/8763 "RADV preferred memory heap performance issues"
[4]: https://gitlab.freedesktop.org/mesa/mesa/-/issues/5902 "RADV driver, for reasons unknown to me, reluctant to use GTT memory"
[5]: https://gitlab.freedesktop.org/mesa/mesa/-/issues/9371 "radv massive performance hit in max vram saturation scenarios"
[6]: https://gitlab.freedesktop.org/mesa/mesa/-/issues/12713 "radv: spurious allocation failures if GTT is small, regardless of VRAM size"


## Comment 2707770232

other (NONE) · Brainde4dNerd · 2025-03-08T00:20:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707770232

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707746551

**Can confirm, I think the Mesa 24.3.4 update is the way to go**

For me at least. 

I just stopped a longer session on my part - game was running really good, well apart from the MHWilds-specific stutters of course. Game would get lag-spikes from time to time but always recovered. I tried FSR Quality and got a little improvement in framerate (from 55-60ish to 65-70fps) Even Frame-Gen worked and it bumbed my frames to 100-140 depending on the location, but it seemed to have more lag-spikes now.... 

I could play the game for 4 hours non-stop without it crashing once, before it would crash regularly. (Even had a crash in a loading screen once :/ )

So we could argue that is more related to a driver-issue than Proton?



## Comment 2707996766

other (NONE) · dotaxis · 2025-03-08T04:16:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707996766

I'm getting pretty bad audio crackling on my copy using bleeding-edge. Can't say much about performance yet because the audio is so distracting.

Edit: Fixed this by adding `PULSE_LATENCY_MSEC=30` to the launch options.

## Comment 2708014022

other (NONE) · calvinkatz · 2025-03-08T04:38:03Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708014022

Regarding the stuttering and temporary freezes in my situation I was able to resolve. I use ZFS and at some point I had changed the `primarycache` and `secondarycache` properties. Resetting those to `all` eliminated almost all the stuttering/freezes I have. Default is `all` but might be worth double-checking.

The game appears to use around 6-7GiB of RAM so having 16GB or more for extra page cache may alleviate some of the stuttering. For reference I have 64GB of RAM and ARC (read cache) is using ~38GB with just Discord and the game running.


## Comment 2708041740

other (NONE) · cheloide · 2025-03-08T05:41:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708041740

> Reply to: https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2707746551

My experience has been the opposite.

Currently on Debian 12 with Mesa 25 (from kisak's repo) with proton bleeding edge with no crashes so far. I crashed often with Mesa 24 (I may have crashed with 25 when I was testing stuff but it may have been proton updates what fixed the crashes). 

I have the same vram usage with 24 and 25, not looking at whatever MH shows .

```
OS: Debian GNU/Linux 12 (bookworm) x86_64
Kernel: 6.12.12+bpo-amd64
Resolution: 3440x1440, 1080x1920
DE: lightdm-xsession
WM: Openbox
CPU: AMD Ryzen 9 5950X (32) @ 5.084GHz
GPU: AMD ATI Radeon RX 6900 XT
Memory:  64GB
```
Launch options:
`WINEDLLOVERRIDES="dinput8.dll=n,b" MANGOHUD=1 gamemoderun %command%`

Current settings: 3440x1440 Ultra with FSR disabled and render 100% (40-80 fps).

## Comment 2708086826

other (NONE) · carloscheddar · 2025-03-08T07:11:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708086826

Latest bleeding edge (March 7) worked smoothly and it's the first time I didn't crash. No launch options other than gamemoderun. 

```Kernel: Linux 6.13.5-zen1
Mesa: Mesa 24.3.4-arch1.1
CPU: AMD Ryzen 9 3900X
GPU: AMD Radeon RX 6800 XT (16GB VRAM)
Memory: 32GB

Proton: experimental (bleeding edge)
Game Resolution: 5120x1440
FPS Limit: Unlimited
Texture Quality: High
Upscaling: FSR3
Vulkan Driver: RADV```

## Comment 2708230088

other (NONE) · tr1p0p · 2025-03-08T11:54:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708230088

I confirm i also got a memory leak since mesa 25 update, causing double the size of VRAM on MH:Wild (but no sign of this on corectrl for example)

```
             .',;::::;,'.                 tripop@localhost-live
         .';:cccccccccccc:;,.             ---------------------
      .;cccccccccccccccccccccc;.          OS: Fedora Linux 41 (Workstation Edition) x86_64
    .:cccccccccccccccccccccccccc:.        Host: MS-7D14 (1.0)
  .;ccccccccccccc;.:dddl:.;ccccccc;.      Kernel: Linux 6.13.5-cachyos2.fc41.x86_64
 .:ccccccccccccc;OWMKOOXMWd;ccccccc:.     Uptime: 27 mins
.:ccccccccccccc;KMMc;cc;xMMc;ccccccc:.    Packages: 2842 (rpm), 15 (flatpak-system), 188 (flatpak-user)
,cccccccccccccc;MMM.;cc;;WW:;cccccccc,    Shell: fish 3.7.0
:cccccccccccccc;MMM.;cccccccccccccccc:    Display (LG Electronics 42"): 1920x1080 @ 60 Hz in 42" [External]
:ccccccc;oxOOOo;MMM000k.;cccccccccccc:    Display (24G2W1G5): 1920x1080 @ 60 Hz in 24" [External]
cccccc;0MMKxdd:;MMMkddc.;cccccccccccc;    DE: GNOME 47.4
ccccc;XMO';cccc;MMM.;cccccccccccccccc'    WM: Mutter (Wayland)
ccccc;MMo;ccccc;MMW.;ccccccccccccccc;     WM Theme: Adwaita
ccccc;0MNc.ccc.xMMd;ccccccccccccccc;      Theme: Adwaita [GTK2/3/4]
cccccc;dNMWXXXWM0:;cccccccccccccc:,       Icons: Papirus [GTK2/3/4]
cccccccc;.:odl:.;cccccccccccccc:,.        Font: Cantarell (11pt) [GTK2/3/4]
ccccccccccccccccccccccccccccc:'.          Cursor: Adwaita (24px)
:ccccccccccccccccccccccc:;,..             Terminal: GNOME Terminal 3.54.0
 ':cccccccccccccccc::;,.                  Terminal Font: Source Code Pro (10pt)
                                          CPU: AMD Ryzen 5 5600 (12) @ 4.47 GHz
                                          GPU: AMD Radeon RX 7600 [Discrete]
                                          Memory: 6.07 GiB / 15.54 GiB (39%)
                                          Swap: 1.25 MiB / 8.00 GiB (0%)
                                          Disk (/): 1.24 TiB / 1.81 TiB (68%) - btrfs
                                          
                                          Locale: fr_FR.UTF-8

```

Screenshots : 
![Image](https://github.com/user-attachments/assets/c29831ec-506f-481e-8ce2-470a73c9f6ba)
![Image](https://github.com/user-attachments/assets/e810a31b-e0e8-47fa-8100-5c0955dfa808)
![Image](https://github.com/user-attachments/assets/8d8a50c2-9176-4c3b-82d6-e26e496e22b0)

## Comment 2708435012

other (NONE) · Eckoa · 2025-03-08T18:32:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708435012

> I confirm i also got a memory leak since mesa 25 update, causing double the size of VRAM on MH:Wild (but no sign of this on corectrl for example)

Im not sure its a memory leak as much as VRAM being misreported as on Mesa 25. VRAM usage for me was roughly the same but Wilds just thought i was using obscene amounts of VRAM that wasnt being used. It almost seems like its reading system memory usage as VRAM usage vs actual VRAM usage.

## Comment 2708439292

other (NONE) · tr1p0p · 2025-03-08T18:41:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708439292

Well, I don't know about that. What I can say, at least, it's the fact having the same setup of kernel config and all with Mesa 25 is causing my computer to freeze entirely during the game, but I downgrade Mesa and since then no issue with last proton experimental bleeding-edge.

So maybe it's more on Mesa side, dunno.

## Comment 2708442230

other (NONE) · Eckoa · 2025-03-08T18:47:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708442230

> Well, I don't know about that. What I can say, at least, it's the fact having the same setup of kernel config and all with Mesa 25 is causing my computer to freeze entirely during the game, but I downgrade Mesa and since then no issue with last proton experimental bleeding-edge.
> 
> So maybe it's more on Mesa side, dunno.

its definitely on the mesa side, this isnt a proton issue as far as i can tell. Hopefully it can be sorted out for 25.0.1 otherwise  going to have to reproduce and make a report of the mesa tracker.

## Comment 2708459400

other (NONE) · Vorthas · 2025-03-08T19:31:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708459400

So I've been having no issues earlier this week on proton experimental (bleeding edge), but as of yesterday (March 7th) I started having crashing randomly after starting any investigation.  These aren't consistent crashes though.

![Image](https://github.com/user-attachments/assets/fbcc33ce-8c86-422f-b790-5d49ec3ef29d)

OS: EndeavourOS
Kernel: 6.13.2-arch1-1
CPU: Ryzen 7 7800X3D
RAM: 64 GB
GPU: RX 7800XT
Mesa version 24.3.4-arch1.1

Game resolution 2560x1440p
Game settings: all Ultra settings except I turn Depth of Field off
FPS: usually a stable 60 FPS with some dips here and there with no frame gen

## Comment 2708466954

other (NONE) · Eckoa · 2025-03-08T19:54:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2708466954

looks like VRAM issue was bisected in mesa about a week ago, if you wish to help with any testing or want updates on it you need to look here as its not a proton issue

https://gitlab.freedesktop.org/mesa/mesa/-/issues/12686

## Comment 2709017528

other (NONE) · dotaxis · 2025-03-09T18:58:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2709017528

> Well, I don't know about that. What I can say, at least, it's the fact having the same setup of kernel config and all with Mesa 25 is causing my computer to freeze entirely during the game, but I downgrade Mesa and since then no issue with last proton experimental bleeding-edge.
> 
> So maybe it's more on Mesa side, dunno.

My machine was freezing entirely even on Mesa 24.3.4 until I turned frame gen off. Shame since I only get 65 FPS without it.

## Comment 2709090281

other (NONE) · UsernamesAreNotMyThing · 2025-03-09T22:00:38Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2709090281

@kisak-valve I think this issue is worthy of the Mesa drivers label, as the reported issue with VRAM reporting has been confirmed to be a regression in the Mesa driver, which has [already been bisected](https://gitlab.freedesktop.org/mesa/mesa/-/commit/a565f2994fec38e20cce46589698dd5487e3ea61).

## Comment 2716033200

other (NONE) · Billli11 · 2025-03-12T00:24:51Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2716033200

A fix just merged to fix mesa 25 vram regression.  [MR](https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34005)  
The fix should be included in [25.0.2](https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/34005#note_2819034)  
Which scheduled to release at [2025-03-19](https://docs.mesa3d.org/release-calendar.html#calendar)

## Comment 2717438231

other (NONE) · minecraft2048 · 2025-03-12T10:43:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2717438231

I saw some stutters, and dmesg is spammed by a lot of split locks and umip problems:

```
[  +0.000005] x86/split lock detection: #DB: MonsterHunterWi/3569678 took a bus_lock trap at address: 0x1555a4a7c
[  +0.000238] x86/split lock detection: #DB: MonsterHunterWi/3569678 took a bus_lock trap at address: 0x15cd0f7e8
[ +24.652423] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x15b64c899
[  +0.001304] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000010] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000003] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000002] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000002] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000002] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000002] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000002] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.000002] x86/split lock detection: #DB: MonsterHunterWi/3569671 took a bus_lock trap at address: 0x158f94ef6
[  +0.002582] umip_printk: 39 callbacks suppressed
[  +0.000003] umip: MonsterHunterWi[3569671] ip:1563e572c sp:7af2eba8: SGDT instruction cannot be used by applications.
[  +0.000003] umip: MonsterHunterWi[3569671] ip:1563e572c sp:7af2eba8: For now, expensive software emulation returns the result.
[  +0.373473] umip: MonsterHunterWi[3569672] ip:1563e572c sp:7b32ed58: SGDT instruction cannot be used by applications.
[  +0.000009] umip: MonsterHunterWi[3569672] ip:1563e572c sp:7b32ed58: For now, expensive software emulation returns the result.
[  +0.511322] umip: MonsterHunterWi[3569672] ip:1563e572c sp:7b32e9b8: SGDT instruction cannot be used by applications.
[ +11.436050] handle_bus_lock: 268 callbacks suppressed
[  +0.000004] x86/split lock detection: #DB: MonsterHunterWi/3569674 took a bus_lock trap at address: 0x1555a4a7c
[  +0.000180] x86/split lock detection: #DB: MonsterHunterWi/3569674 took a bus_lock trap at address: 0x15cd0f7e8
[  +1.930138] x86/split lock detection: #DB: MonsterHunterWi/3569684 took a bus_lock trap at address: 0x15cb0089c
[  +0.000013] x86/split lock detection: #DB: MonsterHunterWi/3569684 took a bus_lock trap at address: 0x1591b3b68
[  +0.000006] x86/split lock detection: #DB: MonsterHunterWi/3569684 took a bus_lock trap at address: 0x15d1bc31d
[  +0.000005] x86/split lock detection: #DB: MonsterHunterWi/3569684 took a bus_lock trap at address: 0x15a2977a4
[  +0.000665] x86/split lock detection: #DB: MonsterHunterWi/3569684 took a bus_lock trap at address: 0x1545bfeb5
[  +0.000007] x86/split lock detection: #DB: MonsterHunterWi/3569684 took a bus_lock trap at address: 0x15d9f1159
[  +1.224582] x86/split lock detection: #DB: MonsterHunterWi/3569673 took a bus_lock trap at address: 0x1555a4a7c
[  +0.000221] x86/split lock detection: #DB: MonsterHunterWi/3569673 took a bus_lock trap at address: 0x15cd0f7e8
[Mar12 21:22] x86/split lock detection: #DB: MonsterHunterWi/3569675 took a bus_lock trap at address: 0x1555a4a7c
[  +0.000185] x86/split lock detection: #DB: MonsterHunterWi/3569675 took a bus_lock trap at address: 0x15cd0f7e8
[  +3.308408] x86/split lock detection: #DB: MonsterHunterWi/3569673 took a bus_lock trap at address: 0x1555a4a7c
[  +0.000177] x86/split lock detection: #DB: MonsterHunterWi/3569673 took a bus_lock trap at address: 0x15cd0f7e8

```

I'm on Arch Linux 6.13.4-zen1-1-zen, Ryzen 9 9900X processor

## Comment 2717918579

other (NONE) · Billli11 · 2025-03-12T13:38:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2717918579

@minecraft2048 You'll need to disable Split lock detection/mitigation. [(Arch wiki)](https://wiki.archlinux.org/title/Steam/Game-specific_troubleshooting#Split_lock_detection/mitigation)  
You can  also
```
sudo  bash -c 'echo 0 > /proc/sys/kernel/split_lock_mitigate'
```  
or  
```
sudo sysctl kernel.split_lock_mitigate=0
```  
if you want to disable it in run time but don't want to use gamemode for some reason. [(Kernel docs)](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/kernel.html#id98)

## Comment 2718602915

other (NONE) · Akezhar · 2025-03-12T17:24:08Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2718602915

> > Well, I don't know about that. What I can say, at least, it's the fact having the same setup of kernel config and all with Mesa 25 is causing my computer to freeze entirely during the game, but I downgrade Mesa and since then no issue with last proton experimental bleeding-edge.
> > So maybe it's more on Mesa side, dunno.
> 
> My machine was freezing entirely even on Mesa 24.3.4 until I turned frame gen off. Shame since I only get 65 FPS without it.

I'm also experiencing random freezes when using frame gen, everything seems to be working fine when I turn it off.

## Comment 2723423454

other (NONE) · ruinedraziel · 2025-03-14T04:24:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2723423454

Hi, just passing to add, I'm just downloaded GE-Proton26, and using gamemoderun %command% /WineDetectionEnabled:False was able to enable Ray Tracing, and it worked on dragon's dogma 2 also.

![Image](https://github.com/user-attachments/assets/be395f40-07bb-4975-8591-c8d6e864e5a9)
And it actually worked.
![Image](https://github.com/user-attachments/assets/12e05954-d1bf-4248-8f98-8a9e7a67b039)

That said, after the last patch I now see a message saying I need an ssd for the game to run properly, and the performance seems to have worsened, not sure if it's a placebo. But the game is on 3500Mb NVME m2 drive.

Any ideas about this?

## Comment 2723695773

other (NONE) · westlyroots · 2025-03-14T06:02:59Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2723695773

Performance and stability has gotten a lot better for me with mesa 25.1 and the latest version of proton, but it seems that my GPU pagefaults are still around albeit rarer. Just crashed during a second late-game hunt: 
```Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:6 pasid:32797)
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:  in process MonsterHunterWi pid 4213 thread vkd3d_queue pid 4339
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:   in page starting at address 0x00008000e0400000 from client 0x1b (UTCL2)
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00601430
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:          MORE_FAULTS: 0x0
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:          WALKER_ERROR: 0x0
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:          MAPPING_ERROR: 0x0
Mar 14 01:48:38 archie kernel: amdgpu 0000:0a:00.0: amdgpu:          RW: 0x0
Mar 14 01:48:45 archie rtkit-daemon[1106]: Supervising 8 threads of 5 processes of 1 users.
Mar 14 01:48:45 archie rtkit-daemon[1106]: Supervising 8 threads of 5 processes of 1 users.
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: Dumping IP State
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: Dumping IP State Completed
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=1333509, emitted seq=1333511
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: Process information: process MonsterHunterWi pid 4213 thread vkd3d_queue pid 4333
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: Starting gfx_0.0.0 ring reset
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: Ring gfx_0.0.0 reset failure
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: GPU reset begin!
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: MODE1 reset
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: GPU mode1 reset
Mar 14 01:48:49 archie kernel: amdgpu 0000:0a:00.0: amdgpu: GPU smu mode1 reset
```
Using Arch 6.13.6-arch1-1, 6700 XT, Ryzen 5600X, 16GB 3600MT/s DDR4, Proton experimental (non-bleeding), mesa 25.1 git on Hyprland.

-- Update: amdvlk has somewhat worse performance but has no pagefault issues from what I can tell. Only saw slight artifacting once over multiple hours of playing. Will use it until I'm able to solve the issue with mesa's drivers on wilds.

## Comment 2726976064

other (NONE) · neon-grim · 2025-03-15T20:06:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2726976064

> reply to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2716033200

I can confirm that the vram leak seems to be fixed with the latest commit. I had to wait a bit for chaotic nyx to get updated to a commit which includes the changes, but after testing the game seems to run a loot smoother on my 7900XTX. That said, running the HD texture pack DLC still causes asset streaming issues, so I recommend just playing with textures on high.



## Comment 2727151906

other (NONE) · shrublet · 2025-03-16T02:55:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2727151906

BTW, to anybody with Nvidia GPUs who have been using `PROTON_HIDE_NVIDIA_GPU`, it seems another way to mitigate the vertex/texture issues and hangs is by setting the DirectX feature level to 12 instead of 12.2 like `VKD3D_FEATURE_LEVEL=12_0`. I hadn't seen this posted on the discussion forums or here, but somebody mentioned this in [an issue](https://github.com/HansKristian-Work/vkd3d-proton/issues/2183#issuecomment-2500285717) on the vkd3d-proton repo as helping, and it absolutely does. There are still a select few spots in the desert esp that feature messed up textures, but monsters, etc. no longer seem to start exploding after 10 minutes. I played around an hour without any major issues besides the desert as prev mentioned. Directly south of base camp in the plains, I found it pretty laggy depending on the direction I was facing, but YMMV. I've been able to use DLSS and frame gen totally fine. My full launch params are below, but feel free to remove the dll overrides and the frame rate cap. This is running with Proton Experimental bleeding edge, flatpak Steam, and with a 3080 on driver ver 570.86. Mesh quality is high as changing it to medium did not seem to change or otherwise affect the severity of the instances there was issues (desert). Surface quality is on low, and I did not test how setting it to high affected things.
```
WINEDLLOVERRIDES="dinput8.dll,dxgi.dll=n,b" VKD3D_FEATURE_LEVEL=12_0 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 VKD3D_FRAME_RATE=164 %command% /WineDetectionEnabled:False
```

Edit: Starting from 570.133.07 and kernel 6.14, it seems I'm running into GPU hang issues again and these options don't work anymore at least for me :(. I have to use `PROTON_HIDE_NVIDIA_GPU` again to fix the meshes freaking out

## Comment 2737233464

other (NONE) · CoolMan-Al · 2025-03-19T16:10:17Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2737233464

I've found a weird bug with this game and it's stupid link party feature. Though it isn't much of an issue, just thought I'd post it just in case.
I am using GE-Proton9-26 since it has the fixes from experimental build that fixed the usual gpu crashes. I also have REFramework installed and the dstorage.dll 1.2.3 from nexusmods (without dstoragecore.dll). In REFramework, I'm using the skip intros, unlimited character edits and persistent glow removal mods.
Throughout the entirety of the game, it's been fine and playable. However, recently I discovered that whenever I join a link party and load into a quest while in that party, I start to stutter like crazy and then eventually run into gfx timeout crash. Whenever I play solo, through SOS or by joining lobby members, I don't get this problem.

```
OS: EndeavourOS Linux x86_64
Host: MS-7B85 1.0
Kernel: 6.13.7-zen1-1-zen
Resolution: 1920x1080
DE: Plasma 6.3.3
WM: kwin
Terminal: alacritty
CPU: AMD Ryzen 7 5700X (16) @ 4.663GHz
GPU: AMD Radeon RX 6700 XT
Video Driver: Mesa 25.0.1-arch1.2
Memory: 32014MiB
```

Launch options are:
```
LD_PRELOAD="" WINEDLLOVERRIDES="dinput8=n,b" gamemoderun %command%
```

Other than this, the game works as intended.

## Comment 2739936724

other (NONE) · Akezhar · 2025-03-20T10:50:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2739936724

I have an odd find to report, as I mentioned I've had random freezes when using frame generation; lately I've tried using the `/WineDetectionEnabled:False` parameter to see how ray tracing looks in the game and I've found that when RT is enabled I don't get the random freezes from using frame generation, I've tested with disableing RT again and the freezes come back; I'm not sure why that the case or what I could do to gather more useful data but for now I've been playing with both on for a few days and the freezes are completely gone.

It would be interesting to see if other people experience the same thing.

## Comment 2739946932

other (NONE) · Akezhar · 2025-03-20T10:54:12Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2739946932

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2737233464

I've had the game crash on me only while playing with a friend but couldn't figure out what's causing it, I'll have to test if it's indeed the party link feature.

## Comment 2744963638

other (NONE) · codebam · 2025-03-22T03:53:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2744963638

Getting major performance issues and lots of "PSO compatibility hash mismatch" in my proton logs in Oilwell Basin. 7900XTX

I think it's recompiling shaders in a loop or something. It can be somewhat resolved by putting settings on low.

## Comment 2764736233

other (NONE) · Najimaru76 · 2025-03-30T20:40:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2764736233

Game run very badly with my Nvidia RTX 4080 / i5 14600k.
Tried all the tinkering suggested here and it still run bad with lot of fps drops, meshes explosions etc...
Is this a proton issue or Nvidia linux driver problem?

## Comment 2769764581

other (NONE) · matthewh626 · 2025-04-01T15:29:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2769764581

![Image](https://github.com/user-attachments/assets/4bc036e0-c812-495f-a762-59477b4eab6a)
im getting serious shader issues, the fps is fine but it looks like this:
has anyone else been getting anything like this?
im using a radeon 6600, proton bleeding edge (tried various GE versions too but with the same results) nobara linux and mesa 25.0.2. 
does anyone have any ideas on how to fix this?

## Comment 2774684471

other (NONE) · Akezhar · 2025-04-03T07:05:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2774684471

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2769764581

Did it ever look normally at some point?
If it actually is a shader issue you could try deleting the game cache from the game install folder and it will rebuild it, hopefully properly this time.

The files you want to delete should be `shader.cache`, `vkd3d-proton.cache`, and `vkd3d-proton.cache.write`; On the next game start it will rebuild the shaders.

## Comment 2776755697

other (NONE) · simifor · 2025-04-03T19:39:49Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2776755697

@matthewh626 I have the same card but the game looks normal to me, tried on proton experimental bleeding edge with mesa git and mesa 25.0.2 with the same result/, I'm curious if it happens to you in the main menu as well as that also shows 3d models.

If you add this to the game's launch parameters (right click on game in library and select properties): `PROTON_LOG=1 %command%`. You'll get a new file in your home folder called `steam-2246340.log` after you run the game, upload it as it might have relevant information.

If the menu interface is visible, also try sharing your graphics settings.

## Comment 2777498458

other (NONE) · avalonv · 2025-04-04T03:56:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777498458

As of today's update, game is not working at all, even after reinstalling. Boots to a black screen which freezes the system for several minutes.

Tested on latest mesa / proton bleeding edge on a 7700XT.

## Comment 2777502319

other (NONE) · eyoung · 2025-04-04T04:00:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777502319

> As of today's update, game is not working at all, even after reinstalling. Boots to a black screen which freezes the system for several minutes.
> 
> Tested on latest mesa / proton bleeding edge on a 7700XT.

I'm seeing the same thing. It does seem to eventually launch if I wait long enough... We'll see if it works after the shaders update

Update: Graphics are very broken and very psychedelic 

## Comment 2777509243

other (NONE) · SuperMewio · 2025-04-04T04:08:10Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777509243

My computer locks up instead of "eventually launching up." Seen on reddit of the game having extreme graphical issues after waiting for the game to actually launch.

## Comment 2777548234

other (NONE) · wwmm · 2025-04-04T04:48:46Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777548234

I was also having the instant Mesa page fault crash with the latest game update.  After deleting all the cache files inside `steamapps/common/MonsterHunterWilds` the game was able to launch.

## Comment 2777572002

other (NONE) · SuperMewio · 2025-04-04T05:09:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777572002

Tried deleting all storage files, game still failed to launch.
- Replaced direct storage files with v1.2.2 I acquired from NuGet
- Game now launches and works
- Re-replaced the v1.2.3 direct storage files, game fails to start
Sounds related to the new direct storage files maybe?

## Comment 2777605742

other (NONE) · codebam · 2025-04-04T05:38:22Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777605742

My game started after some waiting like others said, but I have shader issues and the game doesn't look right. On latest mesa, latest proton-tkg, and latest kernel. 7900XTX

## Comment 2777611244

other (NONE) · patrickrifici · 2025-04-04T05:43:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777611244

> Tried deleting all storage files, game still failed to launch.
> 
> * Replaced direct storage files with v1.2.2 I acquired from NuGet
> * Game now launches and works
> * Re-replaced the v1.2.3 direct storage files, game fails to start
>   Sounds related to the new direct storage files maybe?

My game initially launched once then had the same mesa crashes until I applied your fix, thank you. This worked on my 7900 XTX, I am getting a friend to test it on his 6950 XT as well.

EDIT: Confirmed the above works on his 6950 XT. I have tested on both Proton Experimental and GE-Proton 9.27 (under Arch, friend has tested under Fedora), the older DirectStorage DLLs work. No texture or rendering issues.



## Comment 2777637382

other (NONE) · codebam · 2025-04-04T06:04:41Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777637382

This works for me as well. Downloaded and copied dstorage.dll and dstoragecore.dll 1.2.2 from NuGet using `dotnet` and the shaders look fine.

## Comment 2777677861

other (NONE) · FlameSoulis · 2025-04-04T06:34:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777677861

> Tried deleting all storage files, game still failed to launch.
> 
>     * Replaced direct storage files with v1.2.2 I acquired from NuGet
> 
>     * Game now launches and works
> 
>     * Re-replaced the v1.2.3 direct storage files, game fails to start
>       Sounds related to the new direct storage files maybe?

Can confirm this indeed fixed the issue for Mint 22.1. Issue was getting the files without dotnet (ran into the annoying ```Error: [/usr/lib/dotnet/host/fxr] does not exist``` situation), but the nuget files opened fine with the archive manager, and from there, just a case of rename the older files in the game's root directory and then swapping them in ``_storage_`` as well.

## Comment 2777686732

other (NONE) · Billli11 · 2025-04-04T06:40:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777686732

@FlameSoulis `_storage_` is created by reframework afaik.  
I think we better backup those dstorage dll in case another update broke it again.

## Comment 2777691941

other (NONE) · XaratosS · 2025-04-04T06:43:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777691941

Uhhhh can somebody help me out so that I can get my game running again? I kinda need to figure out to download v1.2.2 of the direct storage file. 

## Comment 2777710952

other (NONE) · Billli11 · 2025-04-04T06:55:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777710952

@XaratosS https://www.nuget.org/packages/Microsoft.Direct3D.DirectStorage/1.2.2  
There are download link on the side.  
rename it to `microsoft.direct3d.directstorage.1.2.2.zip` and extract it

>sha256sum
8a7f9809b4630d22796445ab9aa44181458d0f73f03705b1dfafd79410e07334  dstorage.dll v1.2.2
77c7b3acf5b5a9acec6ad3ed7aa3c33e1ad43e73116b437adfcd26965a079b2b  dstoragecore.dll v1.2.2
882d95c3012aa4e49bee48fe7e2305dbf3aa06df001e431a6606aec756feff6c  dstorage.dll v1.2.3
d74bcf152b741cc85de21351951355eaaac03e0652af5f2622b6daf1abb3f5b4  dstoragecore.dll v1.2.3

## Comment 2777712264

other (NONE) · XaratosS · 2025-04-04T06:55:46Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777712264

> [@XaratosS](https://github.com/XaratosS) https://www.nuget.org/packages/Microsoft.Direct3D.DirectStorage/1.2.2 There are download link on the side. rename it to `microsoft.direct3d.directstorage.1.2.2.zip` and extract it

How the hell did I not see that...Thanks. I think I need coffee right now. 

## Comment 2777824328

other (NONE) · SuperMewio · 2025-04-04T07:37:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777824328

(If you use ark, it will open it up without needing to renaming it, the link above is exactly what I used.)

## Comment 2777839017

other (NONE) · dabossoyou · 2025-04-04T07:45:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777839017

I am playing on steam deck. I was able to get it running with the fix but it's consistently crashing more than before, which I never really crashed at all besides 2-3 times in my ~90 hrs. Any tips?

## Comment 2777840498

other (NONE) · plasmamax1 · 2025-04-04T07:46:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777840498

Just replacing the dstoragecore.dll with the 1.2.2 version was enough to get the game running again after the update.

## Comment 2777884922

other (NONE) · dabossoyou · 2025-04-04T08:08:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777884922

Okay, so now I'm getting an error message, here's the image. What the heck is going on? I purchased the digital deluxe edition.

![Image](https://github.com/user-attachments/assets/f402e574-8080-4d70-b15e-bad41ef885be)

## Comment 2777893076

other (NONE) · patrickrifici · 2025-04-04T08:12:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777893076

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777884922

If you've been swapping Proton versions to try and resolve this issue, each one counts as a new activation against Denuvo. And because of that you're unfortunately locked out since you get 5 activations per 24hrs.

## Comment 2777908928

other (NONE) · dabossoyou · 2025-04-04T08:19:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777908928

Ahh gotcha. Is there any chance it will take less than 24 hrs?

## Comment 2777912881

other (NONE) · patrickrifici · 2025-04-04T08:21:16Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777912881

Not that I'm aware of. You might be able to contact Denuvo support and explain the situation but chances are that'll take longer than 24hrs too.

## Comment 2778032599

other (NONE) · TimothyGs · 2025-04-04T09:13:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2778032599

> Ahh gotcha. Is there any chance it will take less than 24 hrs?

From my own experience, it's 24 hours from the first of the 5 activations. So if you logged in yesterday and then switched proton versions 4 times today (for example), you're in luck and should gain access again soon 👍 

Also, for those still wanting to use DS 1.2.3, [this mod](https://www.nexusmods.com/monsterhunterwilds/mods/127?tab=posts) still works. There's a stickied comment that explains how to enable it on linux, tried it myself and it works!

## Comment 2778492914

other (NONE) · Najimaru76 · 2025-04-04T12:03:26Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2778492914

On my Nvidia 4080 it’s worse…
Will try to post proton logs later 

## Comment 2779213629

other (NONE) · matthewh626 · 2025-04-04T16:17:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2779213629

@simifor
the main menu has the same issues
im using the lowest graphics preset but changing the graphics setting, enabling or disabling any frame gen/upscaling doesnt seem to make a diffreance
it generated a log file but its 6.7GB so i obviously couldnt upload it





## Comment 2779340245

other (NONE) · Uklosk · 2025-04-04T17:23:41Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2779340245

> > Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2777884922)
> 
> If you've been swapping Proton versions to try and resolve this issue, each one counts as a new activation against Denuvo. And because of that you're unfortunately locked out since you get 5 activations per 24hrs.

Valve should ban this shitty DRM from Steam.

## Comment 2779417855

other (NONE) · november781 · 2025-04-04T17:55:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2779417855

Post title update 1 I'm getting reports that DirectStorage needs to be downgraded to get the game to launch. I can't actually test the fix since I ran afoul of everyone's favorite anti-tamper solution while trying to figure out why I was crashing.

https://www.reddit.com/r/MonsterHunter/comments/1jrgqpk/no_longer_able_to_launch_wilds_linuxsteamos/

## Comment 2779504798

other (NONE) · SuperMewio · 2025-04-04T18:45:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2779504798

> Also, for those still wanting to use DS 1.2.3, [this mod](https://www.nexusmods.com/monsterhunterwilds/mods/127?tab=posts) still works. There's a stickied comment that explains how to enable it on linux, tried it myself and it works!

I followed these instructions but used the games original dll files and it also worked. Used the dstorage files from NuGet in system32 however.

## Comment 2779937218

other (NONE) · weeviltime · 2025-04-05T00:12:50Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2779937218

I tested with official DirectStorage dll from Microsoft. from 1.2.1 to 1.2.3.

* Only 1.2.1 worked for me launching the game with this Steam command:
`WINEDLLOVERRIDES="dstorage,dstoragecore=n,b" gamemoderun %command%` 
* Didn't put any `dstorage{core}.dll`  in ` system32`, there is no need for it.

## Comment 2779951272

other (NONE) · ruinedraziel · 2025-04-05T00:31:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2779951272

I just extract the nupkg for 1.2.2 and replace both dll on the game's folder, worked, no command changed whatsover.

## Comment 2780628326

other (NONE) · gregory112 · 2025-04-05T09:22:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2780628326

I wonder if I do anything wrong but after title update 1 I did not experience any crash, presumably already using DirectStorage 1.2.3. Did not modify anything apart from the launch command. How come mine does not crash while everyone else does??? Or does it happen due to the fact that I hid Nvidia as AMD GPU with PROTON_HIDE_NVIDIA_GPU?

My launch command:
```
PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 prime-run mangohud %command%
```

EDIT: yep, it's 1.2.3, confirmed it with the sha256sum `882d95c3012aa4e49bee48fe7e2305dbf3aa06df001e431a6606aec756feff6c  dstorage.dll`

EDIT: My setup:
i7-12800H
RTX 3070 Ti Mobile
Linux 6.13.8
nvidia-open-dkms 570.133.07

## Comment 2780638165

other (NONE) · Billli11 · 2025-04-05T09:54:26Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2780638165

@gregory112 May be it's only on amd( radv )?  

Nvidia driver usually more resilience against shader bug, amdvlk too.

Looked a few post, most of the player who provided gpu name,  
all are amd gpu, and/or steam deck.

## Comment 2780842758

other (NONE) · yat-L · 2025-04-05T15:32:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2780842758

I replace the files with 1.2.2 and it worked.
Here's detailed step of what I did:
1. Download the nupkg file from link above.
2. Unsip the file, after unzipping, go ti native/bin/X64, there are 2 files, `dstroage.dll` and `dstroagecore.dll`
3. copy and file and replace the file with the same name in `/home/USERNAME/.steam/steam/steamapps/common/MonsterHunterWilds`
4. launch the game

System info:
Arch Linux
AMD 6750XT
R5 7500F

PS. don't worry about messing things up, you can always verify file integrity in Steam to undo your changes.

## Comment 2781348291

other (NONE) · shrublet · 2025-04-06T10:18:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781348291

> Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2727151906)

I seem to have finally figured a way to use DLSS while avoiding the current Nvidia issues. It's held strong for a few separate launches and a couple hour session. By reporting your GPU to Wine as an AMD card, but with DXVK reporting it as an Nvidia card, it'll allow enabling NVAPI features. Currently my launch parameters are as follows:
```
WINEDLLOVERRIDES="dinput8.dll,dxgi.dll=n,b" PROTON_HIDE_NVIDIA_GPU=1 DXVK_CONFIG="dxgi.hideAmdGpu=True;dxgi.customVendorId=10de" DXVK_NVAPI_GPU_ARCH=GA100 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 %command%
```
`WINEDLLOVERRIDES` is for REFramework and DLSSTweaker to utilize the aforementioned dlssg to fsr3 mod. I'm reporting my GPU as Ampere as it's what I have, but you can use `AD100` for Ada or `GB200` for Blackwell. I'm also still disabling Reflex via `VKD3D_DISABLE_EXTENSIONS` since afaik it's still broken and causes inconsistent frametimes, but that isn't necessary to add. Hopefully this works for others on Nvidia hardware too.

Edit: FG flicker issue was due to a post-processing mod I forgot I had enabled. Fixed by disabling, and removed mention.

## Comment 2781363748

other (NONE) · ruinedraziel · 2025-04-06T10:59:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781363748

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2780628326

Thats interesting, can you provide wich proton version?

## Comment 2781393871

other (NONE) · Maselkov · 2025-04-06T12:16:25Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781393871

For some reason, I am also not afflicted with the crash, using AMD gpu. I even removed my prefix and remade it, and it still works fine

9800x3d
9070XT
Mesa 25.1.0-devel (git-248edb43c3) RADV
Proton experimental bleeding edge, but I tested using 9.0.4 and it also worked
Linux 6.13.8-arch1-1

Verified that it's using Dstorage 1.2.3 via sha256, and verified integrity of game files as well.

## Comment 2781462874

other (NONE) · ruinedraziel · 2025-04-06T14:54:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781462874

Nice going to try mesa-git then

Edit: No dice, 1.2.3 crashs the system, even with Mesa 25.1.0-devel (git-78c73a4aeb)

## Comment 2781821730

other (NONE) · ruinedraziel · 2025-04-07T01:39:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781821730

<details><summary>Running the game with directstorage 1.2.3 causes page fault on dmesg for me:</summary>

```
[  653.544649] umip: MonsterHunterWi[7804] ip:162d28c33 sp:41f2c0: SGDT instruction cannot be used by applications.
[  653.544653] umip: MonsterHunterWi[7804] ip:162d28c33 sp:41f2c0: For now, expensive software emulation returns the result.
[  653.556029] umip: MonsterHunterWi[7804] ip:1613454bb sp:4164a8: SGDT instruction cannot be used by applications.
[  653.556035] umip: MonsterHunterWi[7804] ip:1613454bb sp:4164a8: For now, expensive software emulation returns the result.
[  656.557866] umip: MonsterHunterWi[7804] ip:15f67c03d sp:41de10: SGDT instruction cannot be used by applications.
[  657.657746] gmc_v11_0_process_interrupt: 9 callbacks suppressed
[  657.657753] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:4 pasid:32786)
[  657.657760] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 8000)
[  657.657763] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x000080025c1f8000 from client 10
[  657.657765] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00401030
[  657.657768] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[  657.657770] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x0
[  657.657772] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x0
[  657.657774] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x3
[  657.657776] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  657.657778] amdgpu 0000:09:00.0: amdgpu:      RW: 0x0
[  659.011024] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.011030] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.011033] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.011036] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x004C1070
[  659.011038] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[  659.011040] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x0
[  659.011042] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x0
[  659.011043] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x7
[  659.011045] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  659.011047] amdgpu 0000:09:00.0: amdgpu:      RW: 0x1
[  659.432200] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.432207] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.432210] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.432212] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x004C1070
[  659.432214] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[  659.432216] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x0
[  659.432218] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x0
[  659.432220] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x7
[  659.432221] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  659.432223] amdgpu 0000:09:00.0: amdgpu:      RW: 0x1
[  659.448685] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.448689] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.448691] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.448694] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x004C1071
[  659.448696] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[  659.448698] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1
[  659.448699] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x0
[  659.448701] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x7
[  659.448703] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  659.448705] amdgpu 0000:09:00.0: amdgpu:      RW: 0x1
[  659.448710] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:4 pasid:32786)
[  659.448712] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.448715] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.458027] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.458031] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.458033] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.458036] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x004C1071
[  659.458037] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[  659.458039] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1
[  659.458041] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x0
[  659.458043] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x7
[  659.458050] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  659.458052] amdgpu 0000:09:00.0: amdgpu:      RW: 0x1
[  659.458057] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.458060] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.458062] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.458068] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.458070] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.458072] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.483864] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.483868] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.483870] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
[  659.483873] amdgpu 0000:09:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x004C1071
[  659.483874] amdgpu 0000:09:00.0: amdgpu:      Faulty UTCL2 client ID: TCP (0x8)
[  659.483876] amdgpu 0000:09:00.0: amdgpu:      MORE_FAULTS: 0x1
[  659.483878] amdgpu 0000:09:00.0: amdgpu:      WALKER_ERROR: 0x0
[  659.483880] amdgpu 0000:09:00.0: amdgpu:      PERMISSION_FAULTS: 0x7
[  659.483881] amdgpu 0000:09:00.0: amdgpu:      MAPPING_ERROR: 0x0
[  659.483883] amdgpu 0000:09:00.0: amdgpu:      RW: 0x1
[  659.483889] amdgpu 0000:09:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:56 vmid:4 pasid:32786)
[  659.483891] amdgpu 0000:09:00.0: amdgpu:  in process MonsterHunterWi pid 7804 thread vkd3d_queue pid 7953)
[  659.483893] amdgpu 0000:09:00.0: amdgpu:   in page starting at address 0x0000800163e70000 from client 10
```

</details>

Can save the system crash if I stops it on time.

This might need some patches, games will probably come with dstorage 1.2.3 in the future.

## Comment 2781845383

other (NONE) · gregory112 · 2025-04-07T02:04:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781845383

> > Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2780628326)
> 
> Thats interesting, can you provide wich proton version?

It's Proton Experimental, last updated at 5 April 2025.

> [@gregory112](https://github.com/gregory112) May be it's only on amd( radv )?
> 
> Nvidia driver usually more resilience against shader bug, amdvlk too.
> 
> Looked a few post, most of the player who provided gpu name, all are amd gpu, and/or steam deck.

Last I checked at https://www.protondb.com/app/2246340 the ones getting borked are all AMD though, but there might be some people that do not get crash with AMD so I am not really sure.

> > Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2727151906)
> 
> I seem to have finally figured a way to use DLSS while avoiding the current Nvidia issues. It's held strong for a few separate launches and a couple hour session. By reporting your GPU to Wine as an AMD card, but with DXVK reporting it as an Nvidia card, it'll allow enabling NVAPI features.

I think I will try this too. With my current setup, I still get stutter frequently, especially when (presumably) loading textures for the first time. After a while of experiencing stutters here and there I begin to get smoother FPS a little bit. With MangoHUD I see that during stutters my CPU/GPU usage goes down, meaning that it is probably I/O issues, which probably are related to DirectStorage.



## Comment 2782070375

other (NONE) · gregory112 · 2025-04-07T05:37:42Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2782070375

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2781348291

Well, I must say that after using this command I am able to use DLSS without getting vertex explosions. I have also combined it with some other flags that are said to disable DirectStorage (?) not sure if this is possible. However, I have got the best FPS with lowest stutter (still exists sometimes) with these tweaks:
1. Use REFramework, it disables Capcom anti tamper and eliminates 90% of my stutter, enabled with that dinput8.dll setting, I'm not sure that it is even playable without this mod at this point
2. Hide Nvidia GPU to work around vertex explosion issues, pyroveil didn't help for me
3. Disabling Reflex as others have mentioned (VK_NV_low_latency2)
4. Use DLSS, but not frame generation
5. Adding some settings regarding ReBAR, I believe through `VKD3D_CONFIG=no_upload_hvv,force_host_cached`. Some use `no_upload_hv`, I think this one is a typo, it's `no_upload_hvv` in VKD3D_CONFIG. But due to the fact that with typo settings some people can get it working, probably adding that does not add anything, so you may be able to just use force_host_cached probably. Haven't tried with reflex enabled.

Here is my command:
```
WINEDLLOVERRIDES="dinput8.dll,dxgi.dll=n,b" DXVK_CONFIG="dxgi.hideAmdGpu=True;dxgi.customVendorId=10de" DXVK_NVAPI_GPU_ARCH=GA100 PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1 VKD3D_CONFIG=no_upload_hvv,force_host_cached VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 prime-run %command% -noDirectStorage
```

I use Proton Experimental, Nvidia driver 570, RTX 3070 Ti mobile.
EDIT: DXVK_NVAPI_GPU_ARCH should be GA100, supported values are here: https://github.com/jp7677/dxvk-nvapi/blob/master/README.md

## Comment 2782839783

other (NONE) · shrublet · 2025-04-07T10:24:51Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2782839783

> Here is my command:
> 
> ```
> WINEDLLOVERRIDES="dinput8.dll,dxgi.dll=n,b" DXVK_CONFIG="dxgi.hideAmdGpu=True;dxgi.customVendorId=10de" DXVK_NVAPI_GPU_ARCH=GA100 PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1 VKD3D_CONFIG=no_upload_hvv,force_host_cached VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 prime-run %command% -noDirectStorage
> ```

Friendly reminder `PROTON_ENABLE_NVAPI` does not exist anymore since Proton 9.0, and NVAPI is enabled by default when possible unless explicitly disabled with `PROTON_DISABLE_NVAPI`.
https://github.com/ValveSoftware/Proton/blob/a62e072e949676917c9f7724bcd34b4e2f8bb53d/proton#L1667-L1668
Also where did `-noDirectStorage` come from? I couldn't find reference to it anywhere and I don't think forcing CPU decompression would be advisable anyways if you can utilize direct storage GPU decompression which I'd imagine would be much faster. 

## Comment 2782887192

other (NONE) · Billli11 · 2025-04-07T10:43:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2782887192

@shrublet  
Probably  placebo.  
no `noDirectStorage` string in the exe.
`sed -n -Ee '/no[dD]irect[sS]torage/p' MonsterHunterWilds.exe|hexdump -C`

## Comment 2783091967

other (NONE) · gregory112 · 2025-04-07T12:00:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2783091967

> Also where did `-noDirectStorage` come from? I couldn't find reference to it anywhere and I don't think forcing CPU decompression would be advisable anyways if you can utilize direct storage GPU decompression which I'd imagine would be much faster.

Well, I saw it in protondb. Out of desperation, I tried to just combine all the flags and ENVs. `-noDirectStorage` was probably used in some other games so perhaps people just put it there. I did not try to remove the flags, just wishful thinking that it might work. Also how do you get GPU DirectStorage? As mine always said CPU in the option. Read somewhere that the game will always show CPU, do you guys get GPU there?

However, here is my take: I used REFramework but did not use DLSSTweaker, therefore I do not put `dxgi.dll` file in the game files. Presumably adding `"dxgi.dll=n,b"` causes it to load native dxgi first. I wonder if this can instead be removed when not using DLSSTweaker mod.

Now, for DXVK_NVAPI_GPU_ARCH, I read that it supports some values. Previously I mistakenly placed GA104 there, and my stutters are gone. However, when I put GA100, my stutters went back. I was afraid of tweaking these flags or switching Proton versions that Denuvo might soft ban me. However, I believe by putting `GA104` there the env probably does not do anything that it can be removed completely, or probably it makes some DXVK components falied to load, but it does remove 90% of the stutters for me. Nonetheless, same as you I also use Ampere.

Some discussions about DirectStorage I found here: https://www.nexusmods.com/monsterhunterwilds/mods/127?tab=posts

## Comment 2785024710

other (NONE) · shrublet · 2025-04-08T01:49:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2785024710

@gregory112 
Apparently you can install Special K to verify if GPU decompression is working correctly. I currently don't have my game installed on an NVME drive anyways, so I wouldn't expect it to say GPU. 

You don't need to include `dxgi.dll` in your `WINEDLLOVERRIDES` and I only included it for context of everything that may/may not affect the results I was personally getting. It won't do any harm having it since it'll just fall back on built-in, but its totally unnecessary.

`DXVK_NVAPI_GPU_ARCH` may or may not be needed, and I haven't tested without since I had spent the evening a/b testing a bunch of stuff already. I wasn't sure how reporting as AMD and then as Nvidia affected the architecture it is reported as, since by default, the dxvk-nvapi documentation says it reports as Pascal for other vendors, and I wanted to ensure DLSS features would function correctly. I'm not sure about what could cause stutters, and I'm wary to make performance claims generally. But, if it seems better for you, then by all means. I'd try to verify on multiple runs what seems to be affecting performance though to eliminate margin of error/external factors.

## Comment 2785125839

other (NONE) · gregory112 · 2025-04-08T03:23:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2785125839

@shrublet 
I did some testing myself. Mine is in an NVMe drive. I kid you not, after removing some flags and testing with them `DXVK_NVAPI_GPU_ARCH=GA104` removes 90% of the stutters for me. GA104 is not even on the list of valid values. Tried removing it, or using GA100, got stutters. I think for now I will stay like this for a while until anyone got better flags. For now what I am aiming for is to eliminate stutters, as they are very annoying. Your flags have allowed me to use DLSS and I got better FPS for this, but the sttuters are very well annoying.

## Comment 2786161151

other (NONE) · Billli11 · 2025-04-08T11:42:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2786161151

A workaround for Direct storage 1.2.3 have been merged to vkd3d-proton.  
https://github.com/HansKristian-Work/vkd3d-proton/pull/2435

~~I don't think Proton experimental[breeding edge] is updated yet.~~

You can try with the build artifact [here](https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/14332198232)

Edit 1:  
Looks like proton experimental[breeding edge] has been updated

## Comment 2787998902

other (NONE) · ruinedraziel · 2025-04-09T01:04:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2787998902

> A workaround for Direct storage 1.2.3 have been merged to vkd3d-proton. [HansKristian-Work/vkd3d-proton#2435](https://github.com/HansKristian-Work/vkd3d-proton/pull/2435)
> 
> ~I don't think Proton experimental[breeding edge] is updated yet.~
> 
> You can try with the build artifact [here](https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/14332198232)
> 
> Edit 1: Looks like proton experimental[breeding edge] has been updated

Working here!

## Comment 2788042963

other (NONE) · dabossoyou · 2025-04-09T01:17:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2788042963

I'm experiencing way more crashes today than I have been in recent days after installing the fix after update. Has anything been changed?

## Comment 2788334089

other (NONE) · codebam · 2025-04-09T05:39:11Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2788334089

Tried stable and unstable versions of mesa / linux / proton and I experience stuttering in oilwell bason no matter what I do

## Comment 2788351723

other (NONE) · DeathTBO · 2025-04-09T05:52:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2788351723

I noticed GPU utilization drops massively to around 70% when there are more than 2 hunters battling a monster. My CPU is never above 40% average/single core (5900x 5ghz). I also have a 5700xt, Kernel 6.14, Mesa 25.0.2.

## Comment 2788361259

other (NONE) · Billli11 · 2025-04-09T05:59:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2788361259

@codebam Are you using hd texture pack?  
Those known to cause stuttering.  
also mesa 25.0.1 have problem with vram usage, try at least update to 25.0.2.

## Comment 2788472562

other (NONE) · codebam · 2025-04-09T06:39:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2788472562

I was using HD textures, but it happens with them off as well, and I was mistaken I actually tested with 25.0.3

## Comment 2790340936

other (NONE) · Najimaru76 · 2025-04-09T16:35:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2790340936

Since last update on Proton Hotfix (04/09/2025), my directstorage issues are fixed.

Using a Nvidia RTX 4080 I can now play almost as good as my Win11 partition using those launch options:

> PROTON_HIDE_NVIDIA_GPU=1 DXVK_CONFIG="dxgi.hideAmdGpu=True;dxgi.customVendorId=10de" DXVK_NVAPI_GPU_ARCH=AD100 %command%

Check the DXVK_NVAPI_GPU_ARCH value here for your NV GPU:
    GK100 (Kepler)
    GM000 (Maxwell Gen1)
    GM200 (Maxwell Gen2)
    GP100 (Pascal)
    GV100 (Volta)
    TU100 (Turing)
    GA100 (Ampere)
    AD100 (Ada)
    GB200 (Blackwell)

EDIT 1: After playing a few hours. I still have problems with huge stutters when I relaunch the game after it compiled the shaders.

If I delete the shader.cache2 file from the game folder, and right after the in game shader compile screen, with the launch options I mentionned before, the game run perfectly fine.
If I close the game and launch it back, even after rebooting my computer. I have huge stutters.

So I compared the shader.cache2 file from my Win11 partition and Cachyos (Arch) partition.
Linux Cachyos: file size is **63,6 MB (63 569 624)** (each time it recreate the file, it's always around 63,6 MB)
Windows 11: file size is **885,3 MB (885 252 320)**

So i'm wondering, when closing the game properly on Linux, it doesn't write the shader.cache2 properly?

EDIT 2:
I took the shader.cache2 file from Win11 and copied it to Linux, same result and when I closed the game, file size was 63,6 MB again.
So copy / pasted again the W11 file to Linux, but this time changed it to read only:

```
❯ ls shader.cache2
.r--r--r-- 885M naj  8 avril 23:12  shader.cache2
```
And no more stutters >_<... game is very responsive, around 110 FPS with DLSS and FG.
Some minor vertex explosions are back on the Plains map, but nothing unplayable.

My Linux setup is:

![Image](https://github.com/user-attachments/assets/44682a3b-b7cd-47ed-818e-ed04acbbfea9)

Using Proton Hotfix.

I hope it helps



## Comment 2796383500

other (NONE) · gregory112 · 2025-04-11T09:41:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2796383500

> EDIT 2: I took the shader.cache2 file from Win11 and copied it to Linux, same result and when I closed the game, file size was 63,6 MB again. So copy / pasted again the W11 file to Linux, but this time changed it to read only:
> 
> ```
> ❯ ls shader.cache2
> .r--r--r-- 885M naj  8 avril 23:12  shader.cache2
> ```
> 
> And no more stutters >_<... game is very responsive, around 110 FPS with DLSS and FG. Some minor vertex explosions are back on the Plains map, but nothing unplayable.

I believe I used to get stutters here and there and while stuttering, the game seems to be trying to recreate/recompile some shader caches every time. For now, I am almost stutter free. You might want to also try `__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1`, although I am not sure this works for your case, as this removes the shader cache size limit as Nvidia seems to be pruning shader cache from time to time.

Also, do you have Vulkan shader cache setting enabled on Steam? I didn't before, but now I do, you might also want to try that

My final current setup that is still working for me (almost stutter free):
Proton Experimental bleeding-edge
3070 Ti Mobile, driver version 570 (nvidia-open)
Vulkan shader cache enabled, it has been downloaded and has been processed
DLSS Ultra Performance, but no frame generation
REFramework mod (dinput8.dll), might try to remove it later
Disable Reflex, might also try to remove it later
Command:
```
WINEDLLOVERRIDES="dinput8.dll=n,b" PROTON_HIDE_NVIDIA_GPU=1 DXVK_CONFIG="dxgi.hideAmdGpu=True;dxgi.customVendorId=10de" DXVK_NVAPI_GPU_ARCH=GA100 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 %command%
```

## Comment 2796499310

other (NONE) · Najimaru76 · 2025-04-11T10:23:54Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2796499310



Hello,

> You might want to also try `__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1`, although I am not sure this works for your case, as this removes the shader cache size limit as Nvidia seems to be pruning shader cache from time to time.

Tried with that, same problem :'(

> Also, do you have Vulkan shader cache setting enabled on Steam?

Yes it was enabled.

For now i'll use my ghetto fix with the shader (the game one, not vulkan) from w11 :/

## Comment 2819185759

other (NONE) · SeikuRyu · 2025-04-21T18:16:46Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2819185759

Switching from bleeding edge to proton hotfix *seems* to have helped with my stuttering, haven't tried building shaders from w11 or anything, running with ReFramework.

## Comment 2847082984

other (NONE) · Grausiga · 2025-05-02T12:23:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2847082984

In case anyone also experiences the game getting stuck on "Initializing Network" when starting: For me, it was because of using Proton Hotifx, it also happened when using the version 10 beta. After going back to 9-27, it worked again.

## Comment 2847612852

maintainer (COLLABORATOR) · alasky17 · 2025-05-02T16:17:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2847612852

@Grausiga Could you provide some more details about what system you are running into this issue on?  Please copy your system information from Steam (Steam -> Help -> System Information and Steam -> Help -> Steam Runtime Diagnostics) and put each in a [gist](https://gist.github.com/), then include a link to the gists in this issue report.

## Comment 2847888425

other (NONE) · Grausiga · 2025-05-02T18:55:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2847888425

@alasky17 

Yes, of course! 

Runtime information: https://gist.github.com/Grausiga/28dbdac959fe2eac78beaf023c64a916

System Information: https://gist.github.com/Grausiga/94d9e86a228925e0fd52c676879a1b76

## Comment 2880196030

other (NONE) · mlassnig · 2025-05-14T13:10:51Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2880196030

> In case anyone also experiences the game getting stuck on "Initializing Network" when starting: For me, it was because of using Proton Hotifx, it also happened when using the version 10 beta. After going back to 9-27, it worked again.

In the current default setup (no monkeypatched dstorage etc.., no custom defined Proton version) it's still stuck on "Initializing network" for me. Don't even see 9-27 in the list of available Proton versions, but I've tried various combinations of Experimental, Experimental(bleeding-edge), Hotfix, 10.0-1-beta, and 9.0-4; all with and without changed dstorage. Changing the Proton Versions also triggered Denuvo eventually, so was locked out for 24h. All other games work perfectly.

[System](https://gist.github.com/mlassnig/293488a5479d38b366e56e690700c497), [Runtime](https://gist.github.com/mlassnig/52acc2039f66a5a1c62a9e1ef038dc5e)


## Comment 2888760222

other (NONE) · RedStoNExLo · 2025-05-18T04:28:26Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2888760222

> EDIT 1: After playing a few hours. I still have problems with huge stutters when I relaunch the game after it compiled the shaders.

I had the exactly same issue, and it might related to shader cache not cached correctly, causing shader recompiled every time the game boots.

> EDIT 2:
I took the shader.cache2 file from Win11 and copied it to Linux, same result and when I closed the game, file size was 63,6 MB again.
So copy / pasted again the W11 file to Linux, but this time changed it to read only:

But I failed to use the W11 `shader.cache2`. It cause in-game shader compilation every time the game boots.

Finally, I solved it by specifying `__GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1` with `__GL_SHADER_DISK_CACHE_PATH="/absolute/path/to/custom/directory"`. The cached shader is around 2.2GB. No more stutter.

My finally options (Ryzen7700, RTX4070, Proton9):
```
PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1 DXVK_CONFIG="dxgi.hideAmdGpu=True;dxgi.customVendorId=10de" DXVK_NVAPI_GPU_ARCH=AD100 VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2 __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 __GL_SHADER_DISK_CACHE_PATH="/absolute/path/to/custom/directory" WINEDLLOVERRIDES="dstorage.dll,dstoragecore.dll,dinput8.dll=n,b" %command%
```

Hope this helps.

## Comment 2888773000

other (NONE) · Grausiga · 2025-05-18T05:07:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2888773000

> > In case anyone also experiences the game getting stuck on "Initializing Network" when starting: For me, it was because of using Proton Hotifx, it also happened when using the version 10 beta. After going back to 9-27, it worked again.
> 
> In the current default setup (no monkeypatched dstorage etc.., no custom defined Proton version) it's still stuck on "Initializing network" for me. Don't even see 9-27 in the list of available Proton versions, but I've tried various combinations of Experimental, Experimental(bleeding-edge), Hotfix, 10.0-1-beta, and 9.0-4; all with and without changed dstorage. Changing the Proton Versions also triggered Denuvo eventually, so was locked out for 24h. All other games work perfectly.
> 
> [System](https://gist.github.com/mlassnig/293488a5479d38b366e56e690700c497), [Runtime](https://gist.github.com/mlassnig/52acc2039f66a5a1c62a9e1ef038dc5e)

I should've been more specific, I used Proton-GE and installed it myself and I can confirm the game still works using Proton-GE 9-27 on my system.

## Comment 2898880836

other (NONE) · r4ulill0 · 2025-05-21T18:34:47Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2898880836

I have been experiencing crashes frequently after the first title update.

Launch parameters: `WINEDLLOVERRIDES="dstorage.dll,dstoragecore.dll,dinput8.dll=n,b" PROTON_LOG=1 %command%`
Proton version: Hotfix (it happened with experimental too)
Kernel: 6.14.6-arch1-1
CPU: AMD Ryzen 5 7600X 6-Core Processor
GPU: AMD Radeon RX 7800 XT
[Complete system info](https://gist.github.com/r4ulill0/07755635b61b008c13236203064f3602)
[Steam diagnostics](https://gist.github.com/r4ulill0/4059f9baff35e6a942f72938aef8e21b)
[Proton log](https://gist.github.com/r4ulill0/22807feb54c42e6bedd585296010680b)

Checking the proton log it seems that a division by zero happens but I'm not that familiar with .NET nor proton/wine to investigate further than that.

## Comment 2903781127

other (NONE) · wyldlock · 2025-05-23T09:04:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-2903781127

Linux Mint 22.1 Cinnamon with AMD Ryzen 7 5700X and Nvidia 4060TI with 570.153.02 driver. Using Gamemode %command% switch on Experimental branch, the game loads and runs, but when exiting using the in-game menu, it freezes and superuser key must be used to get back to desktop. At that point it remains 'running' in Steam until force stopped. Both with and without __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 , shaders have to be compiled again at every game start. (I'm assuming this is related to the failed game shutdown.) I tried checking all files after install and deleting the crashreport dll and exe file as well. Nothing results in successful game closure and the game always requires shader compile. 

## Comment 3015102117

other (NONE) · Raikiri · 2025-06-28T08:27:11Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3015102117

As of June 2025 I'm still getting vertex explosions after ~10 minutes of gameplay every time. It starts like this:

![Image](https://github.com/user-attachments/assets/079234d8-0e8e-4f09-96d1-44396de1f548)

They get worse the longer I play, quickly making the game unplayable because they obstruct the entire screen.

## Comment 3015983291

other (NONE) · AppleNectar · 2025-06-28T18:54:51Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3015983291

> But I failed to use the W11 shader.cache2. It cause in-game shader compilation every time the game boots.
>
>Finally, I solved it by specifying __GL_SHADER_DISK_CACHE_SKIP_CLEANUP=1 with __GL_SHADER_DISK_CACHE_PATH="/absolute/path/to/custom/directory". The cached shader is around 2.2GB. No more stutter.
>
>My finally options (Ryzen7700, RTX4070, Proton9):

I tried using these two options with a similar hardware configuration, but in the end `shader.cache2` was not written correctly, causing severe stutters the next time I booted up.
(`__GL_SHADER_DISK_CACHE_PATH` specifies the absolute path to where `shader.cache2` will be created)

In my case, I had no choice but to either delete `shader.cache2` every time and make it take 30 minutes to boot up, or copy compiled on Windows 11 to Linux and make it read-only.

OS: Linux Mint 22.1
Kernel: 6.11.0-26
CPU: Ryzen 5700X3D
RAM: 32GB
GPU: 4070Ti Super
Proton: 9.0-4 or Experimental or Hotfix

## Comment 3016030164

other (NONE) · Raikiri · 2025-06-28T21:05:16Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3016030164

I can confirm that if I delete `shader.cache2` and let it rebuild every launch, the stuttering disappears. No command line arguments. If I allow vulkan shader caching, the rebuilding takes just ~3 min for me. I think deleting `shader.cache2' before every launch is an acceptable workaround for me.

## Comment 3016254868

other (NONE) · AppleNectar · 2025-06-29T03:05:17Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3016254868

> I can confirm that if I delete shader.cache2 and let it rebuild every launch, the stuttering disappears. No command line arguments. If I allow vulkan shader caching, the rebuilding takes just ~3 min for me. I think deleting `shader.cache2' before every launch is an acceptable workaround for me.

Compilation times were similar even with vulkan shader pre-caching enabled. Do I need to allow background Vulkan shader processing in Steam's settings?

## Comment 3016781651

other (NONE) · Raikiri · 2025-06-29T15:19:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3016781651

For me pre-caching makes the shader compilation progress bar much faster: from ~20min without pre-caching to ~1min with it. So yes, I do have it enabled.

## Comment 3026905609

other (NONE) · jefferyrlc · 2025-07-02T08:15:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3026905609

If I use GE, then I can't use any of my controllers. If I use Proton 9.0-4 I get a complete graphics stack crash after a while.
Arch Linux
KDE Plasma Wayland
RX 6800XT
Mesa 25.1.4


## Comment 3045750563

other (NONE) · hoppyhopps · 2025-07-07T16:09:38Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3045750563

Game has unplayable stuttering if you manage to fully load in to the lobby. Often crashes shortly after you join a lobby.  Guaranteed crashes if you attempt to forge or change equipment if you launch the game without it compiling shaders.  

Tried the shader cache fixes listed above, but neither seems to do anything. Copying a compiled shader pack from Win11 just forces the game to recompile shaders every launch. 

OS: Arch Linux
Kernel: Linux 6.15.5-arch1-1
DE: KDE Plasma, Wayland session
GPU: RTX 5080 driver version 575.64.03
CPU: Ryzen 7 9800X3D
Proton: Proton Experimental

## Comment 3064096975

other (NONE) · Vorthas · 2025-07-11T22:44:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3064096975

Using Proton Experimental, which has worked in the past, I recently hard crashed Wilds as soon as I killed the Seregios in the story quest in the recent update.  I can fight Lagiacrus no problem and do the whole fight with Seregios, but as soon as Seregios dies, I crash to desktop immediately.  Otherwise I got no stuttering and a clean 60 FPS (no frame gen) at 1440p in most places (sometimes goes down a little in the Scarlet Forest).

System Specs
OS: EndeavourOS
DE: MATE 1.28.2 (X11)
KERNEL: 6.15.5-arch1-1
CPU: AMD Ryzen 7 7800X3D
GPU: AMD Radeon RX 7800 XT (radeonsi, navi32, LLVM 20.1.7, DRM 3.63, 6.15.5-arch1-1)
GPU DRIVER 4.6 (Compatibility Profile) Mesa 25.1.5-arch1.1
RAM: 64 GB


## Comment 3068626089

other (NONE) · KenchanPrfm · 2025-07-14T09:31:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3068626089

I left this game before TU1 and I came back after TU2.
After TU2 the game crashes after about 5 to 60 minutes of play for me.
Same for Steamdeck and PC.
Switching proton versions had no effect.
I tested Proton 9.0-4, 10.0-1, 10.0-2-rc, Experimental (include Bleeding-Edge) and Hotfix, but all of these are not working for me.

I can not decide whether the game's problem (this game has too many problems, include crash bug.) or my environment problem, I did not see this problem before TU1, so there is something wrong now.

PC
OS: EndeavourOS rolling rolling
Kernel: x86_64 Linux 6.15.6-arch1-1
CPU: AMD Ryzen 7 5700X 8-Core @ 16x 4.66584GHz
GPU: AMD Radeon RX 7700 XT (radeonsi, navi32, LLVM 20.1.7, DRM 3.63, 6.15.6-arch1-1)
Driver: 25.1.5-1
RAM: 32013MiB

Steamdeck
OS: 3.7.14

## Comment 3078490439

other (NONE) · KenchanPrfm · 2025-07-16T13:01:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3078490439

I got Proton log by using "PROTON_LOG=1" option.
The log size is 6.5 GB, so I cut out last 10000 lines.
I saw vkd3d-proton output many warn messages.

[MHWs_log_tail_10000.log](https://github.com/user-attachments/files/21258282/MHWs_log_tail_10000.log)

## Comment 3078597737

other (NONE) · XaratosS · 2025-07-16T13:22:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3078597737

> I got Proton log by using "PROTON_LOG=1" option. The log size is 6.5 GB, so I cut out last 10000 lines. I saw vkd3d-proton output many warn messages.
> 
> [MHWs_log_tail_10000.log](https://github.com/user-attachments/files/21258282/MHWs_log_tail_10000.log)

Have you tried proton-ge10.8?

## Comment 3084051795

other (NONE) · KenchanPrfm · 2025-07-17T13:20:40Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3084051795

> > I got Proton log by using "PROTON_LOG=1" option. The log size is 6.5 GB, so I cut out last 10000 lines. I saw vkd3d-proton output many warn messages.
> > [MHWs_log_tail_10000.log](https://github.com/user-attachments/files/21258282/MHWs_log_tail_10000.log)
> 
> Have you tried proton-ge10.8?

I tried GE-Proton10-8 but unfortunately it didn't change anything.

## Comment 3095885753

other (NONE) · KenchanPrfm · 2025-07-21T09:26:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3095885753

I solved the problem. The problem caused by  reframework.

## Comment 3364482390

other (NONE) · cerroverb · 2025-10-03T06:51:27Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3364482390

> I solved the problem. The problem caused by reframework.

does reframework still not work? i use mods so this is incredibly discouraging if so

## Comment 3364508420

other (NONE) · Billli11 · 2025-10-03T07:00:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3364508420

@cerroverb latest nightly should fixed the problem
https://github.com/praydog/REFramework-nightly/releases


## Comment 3367971701

other (NONE) · cerroverb · 2025-10-04T06:52:42Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3367971701

> [@cerroverb](https://github.com/cerroverb) latest nightly should fixed the problem https://github.com/praydog/REFramework-nightly/releases

crashes on starting to render the main menu with this version installed on ge proton 10-17 cachyos. 5080m and intel ultra 9 cpu. not sure what the issue is as i have weaker PCs that can run the game with no issues, but they're AMD, so it's definitely an Nvidia or Intel issue.



## Comment 3367971992

other (NONE) · cerroverb · 2025-10-04T06:53:30Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3367971992

> I can confirm that if I delete `shader.cache2` and let it rebuild every launch, the stuttering disappears. No command line arguments. If I allow vulkan shader caching, the rebuilding takes just ~3 min for me. I think deleting `shader.cache2' before every launch is an acceptable workaround for me.

i can't even find this file in my own installation. i have processing vulkan shaders before game turned off though

## Comment 3367982885

other (NONE) · Billli11 · 2025-10-04T07:12:06Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3367982885

@cerroverb reframework nightly 1190 working on my end.  
![Image](https://github.com/user-attachments/assets/a29f332d-6f1e-4d6d-afd0-e8a70b06751d)

```
sha256sum dinput8.dll 
075ef6679f0cf56078652217468b2224f80c5f6168298777e435f9c71a724924  dinput8.dll
```

~~Did you also swapped AMD FSR's dll to SDK 2.0.0 ( FSR 3.1.5 and 4.0.2 . Latest optiscaler ship with those).~~
~~Try reverting it back to original or SDK 1.1.4 ( FSR 3.1.4 )~~

Edit:2 Retested. the offender is libxess.dll 2.1.0. Reverted it back to 1.3.1 should fix it

## Comment 3369016598

other (NONE) · Pluto-j · 2025-10-05T12:13:29Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3369016598

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/a86cb0fd-06a9-412c-889e-81162849706b" />
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/d21cefae-f118-4463-8fe6-1123169af784" />

(Sorry , I used Google translator)

A previously fixed issue with incorrect VRAM usage reporting has reoccurred.
Since this issue started occurring, sessions have started crashing randomly.
However, the session crash only occurs when playing Wilds and has not yet been encountered while playing any other games.

The VRAM usage misreporting issue occurs in all of the following Proton versions:
- Proton Experimental (Bleeding-Edge Ver.)
- GE Proton 10-10
- Proton-CachyOS-10.0-20250919

Just to be sure, I replaced dstorage.dll and dstoragecore.dll with the 1.2.2 version and tested it, but the problem remained unchanged.

I tried deleting it and then reinstalling it, but that didn't change anything.
I tried using the latest version of REFramework available on github, but there was no difference.

CPU : Ryzen 7 3700X
GPU : Radeon RX6750XT (radeonsi, navi22, LLVM 20.1.8, DRM 3.64, 6.16.8-273-tkg-eevdf-llvm)
MEM : 48GB
OS : Endeavour OS
DE : hyprland
Kernel : 6.16.8-273-tkg-eevdf-llvm
GPU Driver : 4.6 (Compatibility Profile) Mesa 25.1.7-arch1.1


## Comment 3419962845

other (NONE) · lanceturbes · 2025-10-19T21:12:48Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3419962845

Still get major vertex explosions on NVIDIA hardware no matter which Proton version I use and no matter how many times I clear shader caches (not just the `shader.cache2` file, but also the vkd3d ones and the entire shadercache folder for MHW inside steamapps).

Also get major stuttering throughout any subsequent session following an initial session with shader cache compilation. In other words, the first launch of the game (with the initial in-game shader compilation step) experiences smooth gameplay (with the only caveat being vertex explosions, especially noticeable in the Windward Plains), but any game session (subsequent launch) where a shader cache was already present (i.e., no in-game shader compilation step on startup) experiences constant stuttering when going through every area, almost like it's trying to re-compile everything on the fly as I play, seemingly not actually using the original cache at all.

I have shader pre-caching enabled in Steam. I always wait for the pre-caching to complete before playing (after a first launch, I am never asked to wait for pre-caching in Steam though).

No mods are installed (fresh game installation). In-game settings are set to Ultra preset, but same problems occur even on Low preset. Frame generation is working fine. Upscaling is working fine.

Proton: Proton 9.0-4 (Stable), Proton Experimental (No Beta)
CPU: Ryzen 7 9800X3D
GPU: NVIDIA RTX 4080 SUPER 16GB
RAM: 64GB DDR5
OS: Fedora 42
DE: KDE Plasma 6.4.5 (No difference in GNOME for me)
Kernel: 6.16.12-200.fc42.x86_64
GPU Driver: 580.95.05 (via `akmod-nvidia-open`)

## Comment 3445903494

other (NONE) · lumenapollo · 2025-10-25T05:32:05Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3445903494

Game crashes on title screen with a fresh install. Renders the first few frames but freezes intermittently with shortening intervals until stopping completely.

Proton: GE 10-21, Proton Experimental (tested with both bleeding edge and without)
CPU: Intel Core Ultra 9 285H
GPU: NVIDIA GeForce RTX 5070 Laptop GPU (580.95.05) / Intel Graphics
RAM: 32 GiB
OS: Nobara 42
Kernel: 6.17.4-201.nobara.fc42.x86_64 (64-bit)
DE: KDE Plasma 6.4.4

[steam-2246340.log](https://github.com/user-attachments/files/23139360/steam-2246340.log)

## Comment 3445923799

other (NONE) · Eckoa · 2025-10-25T05:45:12Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3445923799

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3445903494

Its an Nvidia driver issue, it works fine on 575 but all 580 drivers are broken in this and a number of games

## Comment 3476932147

other (NONE) · arisupocket · 2025-11-01T22:41:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3476932147

> > Replying to [#8206 (comment)](https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3445903494)
> 
> Its an Nvidia driver issue, it works fine on 575 but all 580 drivers are broken in this and a number of games

can confirm im on 580 on a 5080m and the game can't render graphics at all, freezes after shader comp

## Comment 3593250771

other (NONE) · Puppy2Git · 2025-11-30T20:05:26Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3593250771

Game works perfectly fine when the in game shaders are compiled. But any further launch causes the game to crash on a black screen before anything loads. (Clearing the shaders and verifying game files resolves it, but requires to regenerate shaders every launch)

Proton: Experimental (Today), GE-Proton10-25
CPU: i7 12th gen KF
GPU: Rx 9070 XT
RAM: 32 GB
OS: Bazzite
Kernel: 6.17.7-ba19.fc43.x86_64
GPU DRIVER: 4.6 Mesa 25.3.0
DE: KDE Plasma 6.53 (Wayland)

Log: (With Proton Experimental)
[steam-2246340.log](https://github.com/user-attachments/files/23841717/steam-2246340.log)


## Comment 3593266412

other (NONE) · lorentzforces · 2025-11-30T20:11:14Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3593266412

@Puppy2Git this sounds similar to issues I've encountered on other games recently, can you try launching with `PROTON_USE_WINED3D=1 %command%` and report if that works around this particular issue for you?

## Comment 3593276753

other (NONE) · Puppy2Git · 2025-11-30T20:15:46Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3593276753

Attempting to run it with the argument causes a message to appears saying that it was an unsupported graphics card. Also it triggered the anti-tamper and I am locked out for another 24hours... 

## Comment 3594111734

other (NONE) · Puppy2Git · 2025-12-01T01:04:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3594111734

@lorentzforces Out of curiosity what size is your `shader.cache`?

## Comment 3597796948

other (NONE) · Puppy2Git · 2025-12-01T17:09:41Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3597796948

Well... I deleted the `config.ini` and it booted. 

## Comment 3661937435

other (NONE) · Globoplox · 2025-12-16T18:52:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3661937435

OS: Arch & Gnome
Kernel: linux-zen 6.17.9.zen1-1
CPU: AMD Ryzen 7 5700X
GPU: AMD Radeon RX 7800 XT
GPU Driver: mesa 1:25.3.1-2 & vulkan-radeon 1:25.3.1-2
Proton Experimental Bleeding Edge

Since today's Title Update 4 I'm experiencing crashes within 5 or 10 minutes of otherwise normal gameplay. It was working flawlessly yesterday.
It does not seems to be related to frame gen or upscaling.
No mod, deleted various cache file I found, tried a full reinstall.

Journalctl is showing a page fault GCVM_L2_PROTECTION_FAULT_STATUS that seems to match the timing of the crashes.
Sometime the crash break the whole desktop environment.

[steam-2246340.log](https://github.com/user-attachments/files/24198058/steam-2246340.log)
[jctl-grep-amdgpu.log](https://github.com/user-attachments/files/24198078/jctl-grep-amdgpu.log)

Some crashes showed an actual error:
<img width="1906" height="1080" alt="Image" src="https://github.com/user-attachments/assets/05d1fb10-c0ce-41e3-a738-40db5d8bd8b1" />

The stacktrace and addresses are consistent across crash as far as I have seen

## Comment 3668988465

other (NONE) · lumenapollo · 2025-12-18T08:21:28Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3668988465

Game now no longer makes it to the title screen, now freezing and crashing at the 'Initialising network" message.

GPU: RTX 5070
NVIDIA Driver Version: 580.105.08
CPU: Intel Core Ultra 9 285H
Kernel: 6.17.12-200.nobara.fc43.x86_64 (64-bit)
Proton: GE 10-26/bleeding edge

[steam-2246340.log](https://github.com/user-attachments/files/24230793/steam-2246340.log)

<img width="278" height="198" alt="Image" src="https://github.com/user-attachments/assets/6bce5a95-90ca-4675-a604-ded5b7130201" />

## Comment 3669311005

other (NONE) · ljtnono · 2025-12-18T09:27:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3669311005

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3668988465

same with you. 

## Comment 3677863937

maintainer (MEMBER) · kisak-valve · 2025-12-20T14:33:03Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3677863937

Monster Hunter: Wilds - crash on video playback

Issue transferred from https://github.com/ValveSoftware/Proton/issues/9325.
@juxuanu posted on 2025-12-20T07:59:47:

# Compatibility Report
- Name of the game with compatibility issues: Monster Hunter: Wilds
- Steam AppID of the game: 2246340

## System Information
- GPU: AMD Radeon RX 6750 XT
- Video driver version: Mesa 25.3.2
- Kernel version: 6.18.2-3-cachyos (64 bits)
- Link to full system information report as Gist:
  - https://gist.github.com/juxuanu/b4272ee7a9b64c0f90c1af799a26b0e9
  - https://gist.github.com/juxuanu/062f5893faa07594c6259ef593e32c10
- Proton version: 10.0.20251126 (proton-cachyos). I tried with a few, including GE, Experimental, 9...

## I confirm:
- [x] that I haven't found an existing compatibility report for this game. The other one is for unrelated crashes, which I don't experience.
- [x] that I have checked whether there are updates for my system available.

<!-- Please add `PROTON_LOG=1 %command%` to the game's launch options and
attach the generated $HOME/steam-$APPID.log to this issue report as a file.
(Proton logs compress well if needed.)-->
https://drive.proton.me/urls/YJF1KR8DPW#HsINia3AqQSd (I compressed it with zstd and github won't let me attach it)

## Symptoms <!-- What's the problem? -->
When hovering over the list of weapon types in the armory, a little video plays to showcase each of them. Sometimes it fails to load, then either directly freezes (sound still plays) and then the crash window appears, or that happens right after navigating away from the menu where the videos are shown.

## Reproduction
When selecting a weapon type, either at the beginning or going to an armory (talk to NPC Gemma), as described above.

## Comment 3677962817

other (NONE) · lumenapollo · 2025-12-20T17:04:56Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3677962817

> Game now no longer makes it to the title screen, now freezing and crashing at the 'Initialising network" message.
> 
> GPU: RTX 5070 NVIDIA Driver Version: 580.105.08 CPU: Intel Core Ultra 9 285H Kernel: 6.17.12-200.nobara.fc43.x86_64 (64-bit) Proton: GE 10-26/bleeding edge
> 
> [steam-2246340.log](https://github.com/user-attachments/files/24230793/steam-2246340.log)
> <img alt="Image" width="278" height="198" src="https://private-user-images.githubusercontent.com/240119342/527977564-6bce5a95-90ca-4675-a604-ded5b7130201.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjYyNTA1MTMsIm5iZiI6MTc2NjI1MDIxMywicGF0aCI6Ii8yNDAxMTkzNDIvNTI3OTc3NTY0LTZiY2U1YTk1LTkwY2EtNDY3NS1hNjA0LWRlZDViNzEzMDIwMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUxMjIwJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MTIyMFQxNzAzMzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1kNTExZDE1MWEyZTE2MTAwMzE1OTE0N2Y0YWM4YmZhNGNhMmQ5ZDNkMDMyY2NmMTg5YTYwZjZlY2NlZDI5NDc1JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.t9OeSZU4HCp3qv6pmo2tyLiOmLQ-YXRRo74TnbDV1Lg">

After updating to Nvidia driver 590.48.01, the game now boots properly.

Unfortunately, it is plagued by visual glitches as seen here.

![Image](https://github.com/user-attachments/assets/8657e86e-2ff4-4fe0-a320-2b3890da53ee)

Disabling DLSS reduces (but does not eliminate) the amount of visual glitches.

![Image](https://github.com/user-attachments/assets/eb5d8170-bf7e-4564-b64c-3a6f2ef265d6)

## Comment 3689028004

other (NONE) · monoai · 2025-12-24T08:07:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3689028004

Does anyone know the state of Haptics in this game? I was trying to play it while wired and I'm pretty sure it treats some kind of 4th-5th audio channel as haptics rather than the actual intended vibration cues in the game (so-called Menu items should vibrate the controller and such)

I saw that @ClearlyClaire tried earlier in this thread but I don't see anyone else making an attempt to make haptics work.

## Comment 3694278512

other (NONE) · Beethoven-n · 2025-12-27T22:55:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3694278512

i've got a weird issue where the game allows me to alt tab, but repeatedly crams focus back to it. i will have to spam click my browser for a solid 30 seconds to wrestle focus back from the game. help

## Comment 3717157583

other (NONE) · ruinedraziel · 2026-01-07T03:14:34Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3717157583

Ray tracing no longer works, you can enable with the parameter /WineDetectionEnable=False, but the game just crashes now on loading if ray tracing is enabled.

GE-Proton 10-28
RX 7800XT
Arch Linux 6.18.3-arch1-1
Mesa 26.0.0-devel (git-04071c5f9a)


edit:
this appears to be fixed or was a Shaders compilation issue, just worked fine with Mesa 26.0.0-devel (git-13926b3492)

## Comment 3750409129

other (NONE) · Akezhar · 2026-01-14T16:29:13Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3750409129

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3677863937

I'm having the same issue, the videos work fine at first but after some time they just stop loading and if you open the menu the game crashes.
There are also some video tips during specific fights (i.e. the new gogmazios fight) that have the same issue but they don't cause the game to crash after one stops loading.
Every other video seems to be working fine.

## Comment 3750500800

other (NONE) · juxuanu · 2026-01-14T16:47:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3750500800

I am getting random network disconnects on long play sessions, which the friend I play with, who uses Windows, does not suffer. It seems to be a Linux only issue.

## Comment 3857707620

other (NONE) · MrLixam · 2026-02-06T03:15:07Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3857707620

currently getting repeating crashes on multiple versions of proton, including
- proton experimental [bleeding edge]
- proton 10.0-4
- proton 9.0-4
- proton GE 10.29-2

game crashes since version 1.040.03.00 till 1.040.03.02

the crashes still occur without any overlay or launch options on every proton version listed above

cpu: amd Ryzen 7 5800X
gpu: Radeon 7900 XTX
kernel version: 6.18.7.arch1-1
mesa 25.3.4-1

included is a screenshot of the crash window, as I can't copy the text included in it

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/ff787e1b-8f40-4ea3-97d5-2f3f586d86fd" />

## Comment 3942207606

other (NONE) · Semperverus · 2026-02-23T02:32:09Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3942207606

I believe I may have isolated the issue, but I'd like to confirm with the community. Can everyone on an AMD GPU share what their Anti-Aliasing setting is, and if it is not already off, try turning Anti-Aliasing off?

I noticed that when I turned it off, certain blur effects on many cutscenes such as Depth-of-Field began working correctly for various objects, most noticably the ones closest to the camera (example: the glowing blue lizard on the tree during the cutscene where you first enter the forest was blurred properly with AA off).

I have seen issues with Anti-Aliasing before in other games, most infamously in Phasmophobia after a botched update, and I know that certain types of AA can cause issues on AMD GPUs via Proton specifically.

After disabling, the crashes similar to the ones you all have posted here stopped happening. I was finally able to make it through the forest cutscene, and despite the jagged edges, the rest of the visual fidelity increased.

## Comment 3947837206

other (NONE) · simifor · 2026-02-23T23:05:35Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3947837206

@Semperverus I'm closest to the quematrice cutscene where it's chasing some palicos carrying a big piece of meat, I disabled upscaling to have control over AA, but with FXAA+TAA I didn't really anything off. How noticeable is the issue? or does it depend on the cutscene itself?

## Comment 3948497178

other (NONE) · Semperverus · 2026-02-24T02:17:43Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3948497178

@simifor for me it was causing the crashes to happen pretty frequently, *mostly* on cutscenes (the forest entry was the most consistent and repeatable), but occasionally in the open world. Once I turned off AA, the problem stopped.

## Comment 3949837247

other (NONE) · MrLixam · 2026-02-24T07:47:52Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3949837247

Not home so I can't test but the crashes disappeared at some point, didn't change anti aliasing, may have been something that was updated in the meantime.

I do also remember changing some CPU settings back to defaults, but I'm not certain that was what stopped crashes for me

## Comment 3974203431

other (NONE) · NINNiT · 2026-02-27T17:40:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-3974203431

I'm also getting the Crash on Preview Video Playback, e.g the small embedded videos in the weapon menu. 
`mesa 26.1`, `proton-cachyos 10.0.20260207-3`

Some videos play, but after some time only a loading icon is displayed. This is immediately followed by a crash. 

I know Mods should only be used as a last resort, however disabling the Embedded Videos using `reframework` nightly and [this mod](https://www.nexusmods.com/monsterhunterwilds/mods/3906?tab=description) at least lets me play the game. 




## Comment 4064139454

maintainer (MEMBER) · kisak-valve · 2026-03-15T23:15:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-4064139454

Monster Hunter Wilds – Severe graphical artifacts on NVIDIA RTX 5000 series (Linux, Proton-GE and Proton 9)

Issue transferred from https://github.com/ValveSoftware/Proton/issues/9577.
@syberre374 posted on 2026-03-15T23:10:36:

Hardware:
- GPU: NVIDIA RTX 5070
- Driver: 590.48.01
- CPU: Intel i5-10400F
- RAM: 16 GB DDR4
- Resolution: 2560×1080 (21:9 ultrawide)
- OS: Garuda Linux KDE (Arch-based)
- Kernel: 6.18.5-zen

Proton versions tested:
- Proton 9.0-4
- Proton Experimental
- Proton-GE 10-32
- Proton-GE 9.x
- Wine-GE 9.x (via Heroic)

Summary of the issue:
The game launches and runs, but there are constant graphical artifacts:
- flickering lines on edges
- disappearing/reappearing geometry
- shimmering borders
- unstable image reconstruction

These artifacts appear:
- with DLSS ON or OFF
- with TAA
- with FSR2
- with Frame Generation OFF
- with Vulkan forced (PROTON_NO_D3D12=1)
- with NVAPI disabled (PROTON_HIDE_NVIDIA_GPU=1)

What was tested:
- clean compatdata prefix
- Vulkan forced
- DX12 disabled
- NVAPI disabled
- DXVK_ASYNC=1
- multiple Proton versions
- Wine-GE via Heroic
- Steam Runtime enabled
- different resolutions
- internal resolution scaling

Results:
Nothing removes the artifacts.  
The issue seems specific to:
- NVIDIA RTX 4000/5000 series
- DX12 rendering path
- ultrawide resolutions (2560×1080)

Expected behavior:
Stable image without flickering or disappearing geometry.

Actual behavior:
Constant artifacts regardless of settings or Proton version.

Notes:
This looks like a DX12 + NVIDIA + ultrawide issue in the RE Engine.  
Other players with RTX 4000/5000 report similar behavior.

## Comment 4290169347

maintainer (MEMBER) · kisak-valve · 2026-04-21T16:27:21Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-4290169347

Monster hunter wilds runs okay in 10.x but not in 11

Issue transferred from https://github.com/ValveSoftware/Proton/issues/9693.
@carloscarucce posted on 2026-04-21T16:17:12:

# Compatibility Report
- Name of the game with compatibility issues: Monster Hunnter: Wilds
- Steam AppID of the game: 2246340

## System Information
- GPU: RTX 5070
- Video driver version: Nvidia 580.126.09
- Kernel version: 6.17.0-22-generic
- Link to full system information report as [Gist](https://gist.github.com/): https://gist.github.com/carloscarucce/cf42da3487c8f034bbb068e48203fbea
- Proton version: 11

## I confirm:
- [ ] that I haven't found an existing compatibility report for this game.
- [x] that I have checked whether there are updates for my system available.

I have found a compatibility issue at https://github.com/ValveSoftware/Proton/issues/8206 but not related to this specific issue

<!-- Please add `PROTON_LOG=1 %command%` to the game's launch options and
attach the generated $HOME/steam-$APPID.log to this issue report as a file.
(Proton logs compress well if needed.)-->

[steam-2246340.log](https://github.com/user-attachments/files/26939856/steam-2246340.log)

## Symptoms <!-- What's the problem? -->
Game runs okay in version 10.4 but doesn't in version 11

## Reproduction
Set specific version for game to 10.X -> Confirm that it runs stable (mostly)
Set proton version to 11 (beta, currently) it crashes before the intro video.

Something changed between versions that made it less compatible.

## Comment 4301120468

maintainer (COLLABORATOR) · alasky17 · 2026-04-23T01:36:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-4301120468

@carloscarucce Thank you for the report! Unfortunately we've been unable to reproduce this failure so far and the log doesn't have any significant hints, which makes it nearly impossible to triage without further information.  In order to try to narrow down the source of the failure, could you try dropping in dxvk and vkd3d-proton from the working Proton version (presumably Proton 10.0-4?) into the failing Proton version to see if that fixes the problem/changes the behavior?  If Proton is stored in the default location, you can just: 

cp -rf ~/.steam/steam/steamapps/common/Proton 10.0/files/lib/dxvk/* ~/.steam/steam/steamapps/common/Proton 11.0/files/lib/dxvk/.
cp -rf ~/.steam/steam/steamapps/common/Proton 10.0/files/lib/vkd3d-proton/* ~/.steam/steam/steamapps/common/Proton 11.0/files/lib/vkd3d-proton/.

After testing, you can simply delete the contents of Proton 11.0/files/lib/dxvk and Proton 11.0/files/lib/vkd3d-proton and use the Steam properties -> Installed Files -> "verify integrity of tool files" feature to redownload the correct Proton 11 files.

## Comment 4672347302

other (NONE) · carloscarucce · 2026-06-10T16:44:17Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-4672347302

Thanks for the suggestions @alasky17 

Just re-downloaded the game today along Proton eleven and updated the nvidia drivers.

Now the game is working as intended with much better performance, compared to proton 10 

## Comment 4701903593

maintainer (MEMBER) · kisak-valve · 2026-06-14T13:32:15Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-4701903593

Monster Hunter Wilds requires PROTON_USE_SDL=1 to work with a Flydigi Vader 5 Pro

Issue transferred from https://github.com/ValveSoftware/steam-for-linux/issues/13319.
@v1ld posted on 2026-06-14T13:28:35:

I have to launch Monster Hunter Wilds with `PROTON_USE_SDL=1 gamemoderun %command% /HID/UseISteamInput:False` for the Vader 5 Pro to be recognized within the game.  The controller shows up with no problems in the game's Library page, with all extended buttons active.  I can modify them and they stay saved unlike many other reports.  However, without the explicit enable of SDL the controller is not detected by the game.

Steam >  Settings > Controller lists the controller as a `Vader 5 Pro: X-Box Pad`, which is a bit unexpected.  Proton GE does not work at allnor does the latest CachyOS Proton 11 merge, the latter is a bit surprising.

I'm using Proton Experimental on Arch Linux with the `steam-devices` and `game-devices-udev` packages installed.

I have been using [padctl](https://github.com/BANANASJIM/padctl) but thought I'd test where Steam support is at now and I'm frankly surprised this works so well now, thanks for your efforts as it's a great controller option. I fully uninstalled padctl just for this test.

## Comment 4709880002

other (NONE) · Najimaru76 · 2026-06-15T16:08:00Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-4709880002

Hello,

Installed back the game after almost 1 year, I don't have weird artifacts, vertex explosions or stuttering but almost 50% of the time I crash when the game load to a new zone or a cutescene:

<img width="356" height="293" alt="Image" src="https://github.com/user-attachments/assets/5109fa76-a485-485b-9edf-e4addfdfdef9" />

I use latest cachyos LTS kernel, RTX drivers and proton 11.

Thanks

## Comment 5043283654

other (NONE) · TheLioN25 · 2026-07-22T07:50:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5043283654

I'd like to contribute another reproducible case involving Intel Battlemage and the xe kernel driver.

My system:

- GPU: Intel Arc B570 (Battlemage)
- Driver: Intel open-source Mesa 26.1.4
- Kernel: 7.1.3-2-cachyos
- Desktop: KDE Plasma 6 (Wayland)

Proton versions tested:

- Proton 10.0-4
- GE-Proton 11-4

The game consistently freezes while navigating equipment-related menus, especially while:

- Forging equipment
- Comparing armor
- Changing equipment sets

After the freeze, Wine first reports that the application is not responding, followed a few seconds later by an "Unhandled exception" dialog.

At exactly the same time, the kernel reports:

```text
xe 0000:05:00.0: [drm] Tile0: GT0: Engine reset: engine_class=rcs
xe 0000:05:00.0: [drm] Tile0: GT0: Timedout job ... in MonsterHunterWi
xe 0000:05:00.0: [drm] Xe device coredump has been created
```

The issue is reproducible with both Mesa 26.1.4 and Mesa 26.1.5.

Mesa 26.1.4 improves desktop recovery after the GPU reset, but both Mesa versions eventually trigger the same xe engine timeout.

After several days of testing, I opened an issue in the Intel xe kernel tracker containing the complete investigation, kernel logs and devcoredump information:

https://gitlab.freedesktop.org/drm/xe/kernel/-/issues/8641

If needed, I can also provide the Proton log, the xe devcoredump, or perform any additional testing.

Thank you for your time and for maintaining Proton. Please let me know if you need any additional information, logs, or if you would like me to perform further testing.

<img width="2048" height="1113" alt="Image" src="https://github.com/user-attachments/assets/3e8b96e3-b4ad-44d4-bf10-657d6a49a757" />
<img width="1809" height="1035" alt="Image" src="https://github.com/user-attachments/assets/73261249-572b-403f-ad15-dbc334fa6710" />

## Comment 5199279473

maintainer (MEMBER) · kisak-valve · 2026-08-06T01:15:49Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5199279473

Monster Hunter Wilds (AppID 2246340) crashes on startup — winedmo SourceReader fails with MF_E_UNSUPPORTED_BYTESTREAM_TYPE (c00d36c4)

Issue transferred from https://github.com/ValveSoftware/Proton/issues/10040.
@KeyonAshton posted on 2026-08-06T00:46:50:

Compatibility tool versions tested: Proton 9.0 (stable), Proton Experimental — crash reproduces on both

System info:

GPU: AMD Radeon RX 7900 XTX
Mesa/RADV: 26.0.3
Kernel: 7.0.0
Distro: Kubuntu

Steps to reproduce:

Launch Monster Hunter Wilds
Let it load through to the server connection / DLC verification / autosave warning screen
Dismiss the autosave warning
Game crashes within a few seconds

Observed behavior:
Game shows a crash dialog: Failed to create SourceReader with registered byte stream handler. error(c00d36c4) (MF_E_UNSUPPORTED_BYTESTREAM_TYPE), followed by repeated EXCEPTION_ACCESS_VIOLATION (c0000005). Proton log shows err:dmo:create_placeholder_file Creating tag file h264-used immediately before the crash loop, suggesting the crash occurs while attempting H.264 video decode via winedmo.

Ruled out:

Not GPU/driver-related (reproduces across 5 different Proton builds)
Not memory/OOM related
Not mod-related (reproduces with all mods, including REFramework, removed)
Not save-data related (reproduces on fresh install with no save)
Setting WINEDLLOVERRIDES="winedmo=" does not resolve it — instead fails earlier with Library winedmo.dll (which is needed by "mfmp4srcsnk.dll") not found, then crashes the same way, indicating no fallback path exists for MP4 playback without winedmo
Host FFmpeg (8.0.1) has H.264 decode support confirmed present and registered

Proton log: [steam-2246340.zip](https://github.com/user-attachments/files/30766990/steam-2246340.zip)

## Comment 5199311650

other (NONE) · skarekrow · 2026-08-06T01:21:31Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5199311650

@KeyonAshton I had success adding `%command%` /WineDetectionEnabled:False` as a launch option, it seems the games wine detection is causing these segfaults.

## Comment 5199730935

other (NONE) · amtoaer · 2026-08-06T02:33:33Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5199730935

I can also confirm that the game works after adding the `/WineDetectionEnabled:False` option. However, I still experience noticeable stuttering and frame drops with Proton 11 (tested with Proton GE 11.3 and proton-cachyos-11.0-20260703), whereas Proton 10 (tested with GE-Proton 10-34) runs perfectly.

I am using an Nvidia GeForce RTX 4070 Ti Super with the latest 610.57.04 driver and the following launch options:

`PROTON_USE_SDL=1 gamemoderun %command% /HID/UseISteamInput:False /WineDetectionEnabled:False`

With Proton 10, after enabling frame generation and adjusting a few graphics settings, the game consistently stays above 130 FPS. With Proton 11, however, severe stuttering occurs when the first dialogue box appears and when entering the camp for the first time, as if the game were loading assets in extreme slow motion. Even after waiting for the stuttering to subside, the frame rate continues to fluctuate between 110 and 130 FPS during normal gameplay.

## Comment 5219758373

other (NONE) · KeyonAshton · 2026-08-07T16:50:01Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5219758373

I haven't fully gone into the game yet (busy right now), but i was able to finally get to the title screen with that launch option. Thank you.

## Comment 5221007941

other (NONE) · hoppyhopps · 2026-08-07T19:05:55Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5221007941

Could not get the game to launch without adding `PROTON_HIDE_NVIDIA_GPU=1 %command% /WineDetectionEnabled:False` to my launch options.  Simply hiding my GPU, or disable wine detection was not enough for me. It required both.

Nvidia GeForce RTX 5080, driver 610.57.04.

The game more or less works perfectly as long as I select Proton Hotfix, I just can't use any nvapi features like DLSS or DLSS-FG so I am stuck to FSR3.1.  If I use a non-Hotfix version of Proton, such as 11, or a GE/Cachy fork, then the game will not close gracefully and instead needs to be stopped.

Arch Linux on Linux 7.1.6-arch1-1 using Proton Hotfix as said above. 

## Comment 5223990344

other (NONE) · cerroverb · 2026-08-08T02:04:36Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5223990344

> Replying to https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5221007941

game also no longer works for me on any of my AMD setups nor my laptop 5080 on anything other than hotfix. I'm able to enable low latency+boost mode however at least

## Comment 5224296735

other (NONE) · Eckoa · 2026-08-08T03:29:45Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5224296735

strange, the game just worked for me after verifying game files and deleting my config file in the game dir. It only crashed on the first launch after the update then no problems since

## Comment 5332433070

maintainer (COLLABORATOR) · alasky17 · 2026-08-18T18:33:37Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5332433070

@KeyonAshton @amtoaer @skarekrow @hoppyhopps Is anyone still hitting a failure that requires `/WineDetectionEnabled:False`?  Due to the timing of the reports, I suspect that folks were testing experimental (not bleeding-edge) and Proton-GE which did not yet have the vkd3d-proton fix for this issue.  Current Proton - Experimental should have the fix shipping (no need for bleeding-edge).  Please let me know if you still have any issues without hiding Wine on Proton - Experimental.  

I do not know if Proton-GE has the fix yet or not (although I imagine the latest build probably would).

## Comment 5332572228

other (NONE) · hoppyhopps · 2026-08-18T18:46:38Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5332572228

@alasky17 At the previous time of writing, the only version that worked properly for me was hotfix.  It's possible I failed to test bleeding-edge and that the issue had been resolved from the beginning.

I have just tested now with Experimental and all Nvidia features seem to work, making `PROTON_HIDE_NVIDIA_GPU=1` irrelevant, it also seems to work totally fine when I was not disabling wine detection.

I would assume that a newer release of GE would also work fine.

Thanks!

## Comment 5335183334

other (NONE) · skarekrow · 2026-08-18T22:57:59Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5335183334

@alasky17 another working report here! Though I was using cachyos proton at the time of writing, I swapped to experimental to see if it would launch.

I assume a newer version of cachyos proton will be cut and it will also work. The 20260703 version required that flag, which is the latest one tagged currently. 

## Comment 5378369174

other (NONE) · PseudoResonance · 2026-08-22T06:09:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5378369174

The 4 August update (1.0.42) started throwing errors upon starting 3D render at the title screen, however they could be safely ignored and game was still playable. Proton 11.0-2 completely broke the game for me, and game crashes to desktop upon starting 3D render. Game launches perfectly on hotfix though, with no errors either.

System Information:
- GPU: Nvidia RTX 3070 Mobile
- Video driver version: Nvidia 610.57.04
- Kernel version: 6.18.45
- Proton version: Proton 11.0 and 11.0-2


## Comment 5380446728

maintainer (MEMBER) · kisak-valve · 2026-08-22T12:34:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5380446728

Hello @PseudoResonance, please add [`PROTON_LOG=1 %command%`](https://github.com/ValveSoftware/Proton#runtime-config-options) to the game's launch options, reproduce the regression, and attach the generated $HOME/steam-$APPID.log to this issue report as a file. (Proton logs compress well if needed.) Also, please share the error dialog text.

## Comment 5734595773

other (NONE) · M0urban · 2026-09-18T18:41:53Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5734595773

Currently having an issue, where the games freezes and becomes unrespondable, but sound are still playing. The only reproducable spot I could find is the tiny river behind the the tiny bowling area in the grand hub. See image below

<img width="2560" height="1403" alt="Image" src="https://github.com/user-attachments/assets/3f259bfa-3606-434c-a41a-0df5b6d91b75" />

System Information:

CPU: 9800X3D
GPU: Nvidia RTX 5080
Video driver version: Nvidia 615.71.09
Kernel version: 7.2.6 on cachyos
Proton version: 1787945902 hotfix-20260828-ptr-x86_64, also tried experimental

Here are the logs from PROTON_LOG=1:

[steam-2246340.zip](https://github.com/user-attachments/files/32392813/steam-2246340.zip)



## Comment 5743081812

other (NONE) · Eckoa · 2026-09-19T15:29:32Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5743081812

> Currently having an issue, where the games freezes and becomes unrespondable, but sound are still playing. The only reproducable spot I could find is the tiny river behind the the tiny bowling area in the grand hub. See image below

not a proton issue, its an Nvidia 615 issue, rollback drivers till its fixed as it has already been reported

## Comment 5761215264

other (NONE) · sakuramochi2110 · 2026-09-21T13:24:17Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5761215264

Monster Hunter Wilds: reproducible NVIDIA Xid 109 / VK_ERROR_DEVICE_LOST near Grand Hub Barrel Bowling area on RTX 5070 Ti

## Summary

<details><summary>A GPU hang reproduces at approximately the same location near the hill where Barrel Bowling can be played in the Grand Hub. The user reports near-100% reproduction on Bazzite Linux across repeated attempts. Windows 11 on the exact same PC, RTX 5070 Ti, game, save and location passes without the freeze (user-reported comparison; Windows driver/build details were not captured).</summary>

## Environment

- GPU: NVIDIA GeForce RTX 5070 Ti 16 GB (16303 MiB reported)
- Driver: NVIDIA 615.71.09
- Kernel module: NVIDIA UNIX Open Kernel Module
- OS: Bazzite 44, image 44.20260919.0 (bazzite-gnome-nvidia-open)
- Kernel: 7.2.4-ogc3.1.fc44.x86_64
- Game: Monster Hunter Wilds
- Steam AppID: 2246340
- Game Build ID: 24705561
- Proton: Proton Experimental, experimental-11.0-20260910b-x86_64
- VKD3D-Proton commit: 0bd10357df3f6b65e0a7c4d272acdd6c46249ff8
- Vulkan loader/instance version: 1.4.341
- NVIDIA physical-device Vulkan API version: 1.4.351

Environment values were checked against previously captured OS/module, Steam manifest, Proton version, VKD3D build and Vulkan records. No new system tests were performed to prepare this report.

## Reproduction

1. Launch Monster Hunter Wilds.
2. Load the affected save.
3. Enter the Grand Hub.
4. Move toward the hill near the Barrel Bowling activity.
5. The game freezes at approximately the same location.
6. The NVIDIA kernel driver reports Xid 109.

The user performed all in-game navigation. No save is included in this submission.

## Kernel failure

Fault-test event (JST):

```text
2026-09-21T20:32:15.055995+09:00 [HOST] kernel: NVRM: Xid (PCI:0000:01:00): 109, pid=19713, name=MonsterHunterWi, channel 0x00000010, errorString CTX SWITCH TIMEOUT, Info 0x15c017
```

The channel `0x00000010` and Info `0x15c017` match multiple previous reproductions, including the captured 2026-09-21 20:02:04.303095 event (PID 12963) and the earlier descriptor_heap-option test. Some earlier attempts had different channel/Info values; not all reproductions were byte-identical.

The fault-test launch was 20:30:52, Xid was 20:32:15.055995 (~83 seconds later), and process exit was 20:32:53. A previous descriptor_heap-option attempt took ~290 seconds from launch to Xid. Navigation/loading time was not controlled, so this is not evidence of a fault-option timing effect.

## VKD3D fault capture

A single diagnostic run used only these additional launch variables:

```text
VKD3D_CONFIG=fault VKD3D_DEBUG=warn VKD3D_LOG_FILE=/absolute/diagnostic/path/vkd3d-fault.log %command%
```

The log path above is a public placeholder. All three actual values were verified in the game process environment (PID 19713). No breadcrumbs, shader dump/override, descriptor_heap, PROTON_LOG or other additional workaround was combined with this test. The configuration was restored to empty after game exit.

The fault-reporting path actually ran:

```text
DEVICE_LOST received, reporting fault.
Desc:
Address [0]: 000000df00e95bf0 (granularity 10), type UnknownPC
Failed to wait for Vulkan timeline semaphore, vr -4.
Failed to submit queue(s), vr -4.
```

- Fault address: `0x000000df00e95bf0`.
- Address type: `UnknownPC`.
- Granularity: `10`, exactly as printed; no numeric-base conversion is assumed.
- D3D12 removal reason: `0x887a0005`.
- Vulkan error: `VK_ERROR_DEVICE_LOST`.
- Fault description is empty. No vendor information was printed; `deviceFaultVendorBinary` was false in the captured Vulkan features.
- Timeline-wait and queue-submission failures were logged, but no specific Vulkan queue index or responsible command was identified.

The full VKD3D log has no wall-clock timestamps per line; its error ordering is preserved, but precise cross-log ordering against the kernel Xid cannot be established from those lines alone.

## VA lookup

```text
Found no candidate VA entries.
VA range [000000def3e90000, 000000def4690000) [size = 8388608 (0x800000)]
Fault offset: 218127344 (0xd005bf0)
Cookie: 0.
VkBuffer [N/A]
```

VKD3D could not map the fault address to a tracked resource/allocation. The displayed nearby allocation does not contain the fault address and is not identified as the offending resource. The log's generic suggestion of unused memory/out-of-bounds access is not proof of an out-of-bounds access or a game bug, particularly with address type `UnknownPC`.

## GPU state

Ten-second sampling during the fault test:

| JST timestamp | GPU utilization | VRAM MiB | Temperature | Power | GPU/memory MHz | PCIe |
|---|---:|---:|---:|---:|---|---|
| 20:32:03.777 | 52% | 8911 / 16303 | 61 C | 141.35 W | 2842 / 14001 | Gen5 x16 |
| 20:32:13.814 | 100% | 9266 / 16303 | 54 C | 77.61 W | 2857 / 14001 | Gen5 x16 |
| 20:32:23.851 | 2% | 9266 / 16303 | 49 C | 42.99 W | 307 / 405 | Gen1 x16 |
| 20:32:54.138 | 3% | 1049 / 16303 | 47 C | 50.43 W | 1545 / 7001 | Gen5 x16 |

The last pre-Xid sample was ~1.24 seconds before the kernel message (approximately two seconds); it need not precede the actual start of the hang. After Xid, utilization dropped and the link temporarily reported Gen1 x16, returning to Gen5 x16 after game exit. `nvidia-smi -q` responded at approximately +9 and +69 seconds; GPU Recovery Action was `None`. No additional Xid, GSP timeout or explicit GPU reset was observed in the captured test/post-event interval. Sampling does not rule out shorter transient events.

## Tests already performed

- Minimum graphics settings did not prevent the issue.
- Reboot did not prevent the issue.
- `VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2` did not prevent the issue.
- `VKD3D_CONFIG=descriptor_heap` did not prevent the issue. The variable reached the process, but direct logging of internal path activation was not obtained.
- `VKD3D_CONFIG=fault` did not prevent the issue and still reproduced Xid 109 at the same user-reported location; it was a diagnostic, not a proposed fix.
- Windows 11 on the exact same PC/GPU/save/location does not reproduce the issue, according to the user.

## Additional observations

In the 60 seconds before the fault-test Xid, 44 visible `MonsterHunterWi` bus_lock trap records were found. Four `handle_bus_lock` suppression records reported 1075, 2, 134 and 959 callbacks (2170 total; not all attributable to the game). The last visible game bus_lock was at 20:31:57.715108, 17.340887 seconds before Xid. No bus_lock-to-Xid causal claim is made.

An earlier capture recorded PCIe `BadTLP+`/`CorrErr+` before reproduction. Its before/after AER comparison showed no counter increase (60 captured sections, all zero), and its NVIDIA samples reported no replay-count increase. No contemporaneous AER error or link-down/retrain event was identified in that capture. This was a separate earlier collection, not continuous PCIe/AER counter monitoring of the fault test. No PCIe causal claim is made.

The fault-test cache was observed only: `vkd3d-proton.cache` remained 6,573,400 bytes with mtime 20:01:52.576070; `vkd3d-proton.cache.write` was 1,040 bytes with mtime 20:31:50.442485 at/after the event. No cache deletion, renaming or manual editing was performed.

The recorded journal includes a clock discontinuity. The fault-test +/-60-second excerpt and bus_lock count were corrected by filtering individual journal record timestamps; initial invalid monitor artifacts were excluded from the submission.

A full nvidia-bug-report capture was started approximately 0.36 seconds after an earlier Xid reproduction and completed successfully; it is available privately if needed. It is deliberately not attached publicly. Initial public evidence is limited to `evidence.txt`; the ~6.5 MB full VKD3D log is also not attached.

## Questions for maintainers

1. Does the UnknownPC device-fault address provide useful information for narrowing this down?
2. Since the installed release build appears to have breadcrumbs disabled (based on the previously recorded source/binary inspection), would you like me to reproduce this with a trace-enabled vkd3d-proton build?
3. Would shader dumping, auto-capture, or another VKD3D diagnostic be useful for identifying the workload responsible for the hang?
4. Should this also be reported directly to NVIDIA with the nvidia-bug-report captured immediately after Xid 109?

Possibly related:
https://github.com/HansKristian-Work/vkd3d-proton/issues/3290

[evidence.txt](https://github.com/user-attachments/files/32468705/evidence.txt)

[system-info.txt](https://github.com/user-attachments/files/32468717/system-info.txt)

</details>

## Comment 5761787963

other (NONE) · Eckoa · 2026-09-21T14:05:39Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5761787963

@sakuramochi2110 read the above reply

Known driver issue

## Comment 5762654793

other (NONE) · sakuramochi2110 · 2026-09-21T15:02:18Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5762654793

> [@sakuramochi2110](https://github.com/sakuramochi2110) read the above reply
> 
> Known driver issue

@Eckoa Thanks for pointing this out. I tested the rollback to the 610 driver branch.

I rebased Bazzite from:

- Bazzite 44.20260919
- NVIDIA Open 615.71.09
- Kernel 7.2.4-ogc3.1.fc44

to:

- Bazzite 44.20260908
- NVIDIA Open 610.57.04
- Kernel 7.2.3-ogc3.1.fc44

I kept the same RTX 5070 Ti, the same save file, the same Proton Experimental build (`experimental-11.0-20260910b-x86_64`), and empty Steam launch options.

With 615.71.09, the freeze was reproducible almost every time near the Barrel Bowling hill in the Grand Hub, with NVIDIA Xid 109 / CTX SWITCH TIMEOUT.

After switching to 610.57.04, I tested the exact same location by going through it about 3 times. There were no freezes or crashes, and during the monitored test window I observed:

- 0 NVIDIA Xid events
- 0 GSP timeouts
- 0 GPU resets
- 0 AER/PCIe errors

I have also continued playing for a while on 610.57.04 and have not encountered the issue again so far.

So, in my testing, rolling back from 615.71.09 to 610.57.04 appears to avoid the issue.

However, this is not a driver-only A/B test because the Bazzite rebase also changed the kernel from 7.2.4 to 7.2.3, so I don't want to conclude that 615.71.09 alone is definitely the cause.

For now, I plan to stay on 610.57.04 since the game appears stable.

If possible, could you link the existing NVIDIA bug/report you mentioned? I'd like to compare my Xid 109 logs and symptoms with that report.

Thanks for the help.

## Comment 5762841274

other (NONE) · Eckoa · 2026-09-21T15:14:57Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5762841274

> If possible, could you link the existing NVIDIA bug/report you mentioned? I'd like to compare my Xid 109 logs and symptoms with that report.

Nvidia doesnt do open bug tracking, read here as im the one who reported it (bug 6756147)

https://forums.developer.nvidia.com/t/615-release-feedback-discussion/382815/125

Nvidia will fix it when they get to it, your AI stuff isnt gonna help the issue

## Comment 5762930343

other (NONE) · sakuramochi2110 · 2026-09-21T15:21:02Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5762930343

@Eckoa Thanks for the information and for reporting this to NVIDIA.

I'll stay on 610.57.04 for now, since it has been stable for me so far.

I'll keep an eye on future NVIDIA driver releases and retest once a fix becomes available.

Thanks again for your help.

## Comment 5787591187

other (NONE) · FeiAiJie · 2026-09-23T01:51:44Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5787591187

GPU: AMD Radeon RX 9070 XT GIGABYTE GAMING OC (RDNA4, gfx1201/Navi 48)
Driver: Mesa 26.2.3 / RADV (vulkan-radeon 3:26.2.3-1), Vulkan API 1.4.354
CPU: AMD Ryzen 7 9800X3D
RAM: 64GB DDR5-6000 (EXPO enabled)
Kernel: 7.2.6-1-cachyos (CachyOS)
Proton: Proton - Experimental, build 25406101 (experimental-11.0-20260917b) — verified current as of report
Launch options: WINEDLLOVERRIDES="dinput8.dll,dstorage.dll,dstoragecore.dll=n,b" PROTON_LOG=1 %command%  (no WineDetectionEnabled:False)
Mods: none (I use Fluorine Manager and launched via Steam, I like to keep my installations clean, WINEDLLOVERRIDES="dinput8.dll,dstorage.dll,dstoragecore.dll=n,b" is just there, I am not sure if it causes an impact.)

amdgpu 0000:03:00.0: [gfxhub] page fault (src_id:0 ring:24 vmid:6 pasid:3127)
amdgpu 0000:03:00.0:  Process MonsterHunterWi pid 1143323 thread vkd3d_queue pid 1143519
amdgpu 0000:03:00.0:   in page starting at address 0x0000000000000000 from client 10
amdgpu 0000:03:00.0: GCVM_L2_PROTECTION_FAULT_STATUS:0x00601430
amdgpu 0000:03:00.0:          Faulty UTCL2 client ID: SQC (data) (0xa)
amdgpu 0000:03:00.0:          MORE_FAULTS: 0x0
amdgpu 0000:03:00.0:          WALKER_ERROR: 0x0
amdgpu 0000:03:00.0:          PERMISSION_FAULTS: 0x3
amdgpu 0000:03:00.0:          MAPPING_ERROR: 0x0
amdgpu 0000:03:00.0:          RW: 0x0
amdgpu 0000:03:00.0: Dumping IP State
amdgpu 0000:03:00.0: Dumping IP State Completed
amdgpu 0000:03:00.0: [drm] AMDGPU device coredump file has been created
amdgpu 0000:03:00.0: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
amdgpu 0000:03:00.0: ring gfx_0.0.0 timeout, signaled seq=167576366, emitted seq=167576369
amdgpu 0000:03:00.0:  Process MonsterHunterWi pid 1143323 thread vkd3d_queue pid 1143519
amdgpu 0000:03:00.0: Starting gfx_0.0.0 ring reset
amdgpu 0000:03:00.0: Ring gfx_0.0.0 reset succeeded
amdgpu 0000:03:00.0: [drm] device wedged, but no recovery needed

[kernel_log.txt](https://github.com/user-attachments/files/32543358/kernel_log.txt)
[steam-2246340.log](https://github.com/user-attachments/files/32543359/steam-2246340.log)

## Comment 5813872643

maintainer (MEMBER) · kisak-valve · 2026-09-24T12:15:19Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5813872643

Monster Hunter Wilds (2246340)

Issue transferred from https://github.com/ValveSoftware/Proton/issues/10171.
@devMonou posted on 2026-09-24T02:36:56:

# Compatibility Report
- Name of the game with compatibility issues: Monster Hunter Wilds
- Steam AppID of the game: 2246340

## System Information
- CPU: Ryzen 7 7800X3D
- GPU: RTX 5070
- Video driver version: nvidia 615.71.09
- Kernel version: Linux 7.2.7-200.fc44.x86_64 (Fedora 44 KDE)
- Proton version: experimental-11.0-20260917b-x86_64
- Link to Full System Information Report as [Gist](https://gist.github.com/devMonou/30310208b3e5ca00ef1d4262ff255e56)

## I confirm:
- [x] that I haven't found an existing compatibility report for this game.
- [x] that I have checked whether there are updates for my system available.

[steam-2246340.log](https://github.com/user-attachments/files/32589758/steam-2246340.log)

## Symptoms <!-- What's the problem? -->
The game consistently freezes and handler threads drop completely during the "Eye of the Storm" weather transition sequence. Standard log tracking handlers handler tasks dump zero system errors, but a deep trace log captures an explicit loop crash immediately following Streamline (sl.interposer.dll) framework hooks trying to call local high-resolution windows timers.

## Reproduction
Start the game from a save at the start of the Chapter 2 Main Mission "The Eye of the Storm" and proceed. The game should crash shortly after leaving Kunafa right before you fully enter the dunes.

## Comment 5837538637

other (NONE) · FeiAiJie · 2026-09-25T18:32:34Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5837538637

Follow-up to previous commnet (2026-09-23)

Same SQC (data) GPUVM protection fault, still reproducing consistently. Did more testing and crying, if there is a fast track to playing this game stable, let me know. Full details and a fresh devcoredump are also posted on the related vkd3d-proton tracker: https://github.com/HansKristian-Work/vkd3d-proton/issues/3290

Reproduces identically for the following (address 0x0, client SQC (data), PERMISSION_FAULTS: 0x3, ring timeout/reset — same every time):
- GE-Proton11-7 (stock)
- Self-built vkd3d-proton master (472989aa)
- Proton - Experimental, stock (experimental-11.0-20260917b)
- Proton - Experimental, bleeding-edge (472989aa — same commit as the self-built test)

Tried testing if it was caused by storage/discord/settings: BTRFS/filesystem (fresh nodatacow install, crashed on first load), Discord GPU acceleration (disabled, no difference), plus mods/settings/RT/shader-cache from my original report.

Bumped CachyOS kernel 7.2.6 to7.2.7 since last comment and checked its changelog. Only display-path and VRAM-cgroup amdgpu branches touched, nothing in the GFX/shader path.

Closing note: consistency across five Proton/vkd3d-proton builds plus filesystem/background-process changes makes me speculate if its a deterministic RADV/Mesa bug on RDNA4, not vkd3d-proton or Proton packaging.

## Comment 5842929695

other (NONE) · steponblue · 2026-09-26T03:52:04Z · https://github.com/ValveSoftware/Proton/issues/8206#issuecomment-5842929695

# Compatibility Report
Monster Hunter Wilds - 2246340

## System Information
- GPU: NVIDIA GeForce RTX 4070 SUPER
- Video driver version: NVIDIA 615.71.09
- Kernel version: Linux 7.2.6-arch2-1
- Link to full system information report as [Gist](https://gist.github.com/steponblue/6541f5dc7a8e815ef9147dba3086f4b7)
- Proton version: 1790346343 experimental-bleeding-edge-11.0-439972-20260925-p58a40f-wb326fb-d52fe92-v472989-x86_64
- Issue persists across several stable Proton versions as well.

## Symptoms

When using the '/WineDetectionEnabled:False' launch option to hide Wine detection to enable ray tracing, severe vertex explosions occur in the Windward Plains, accompanied by an FPS increase of around 10-30 frames, depending on what mods are currently installed. The majority of testing was done without any mods, where the FPS increase was roughly 10, and the exploding vertex issues persisted. There are no other issues present in any other maps when /WineDetectionEnabled:False is used.

The vertex explosions occur whether RT is enabled or not, both at startup and with fresh shader caches. The same is true for DLSS, FrameGen and mesh LOD. The only thing I can find that prevents the explosions is removing the /WineDetectionEnabled:False launch option, which disables RT and hurts performance.

[Google Drive Video Link - Running around near the explosions](https://drive.google.com/file/d/1X2IYcTNQDzJD49m0jUNmal_mDK-IcuYQ/view?usp=sharing)
[Google Drive Video Link - Freecam near the affected surfaces](https://drive.google.com/file/d/1q6l71TT7tsMsMLg0_efIyAs8xyNrzHsa/view?usp=sharing)

## Reproduction

Launch MHWilds with /WineDetectionEnabled:False in the launch options and go to the Windward Plains.

## Troubleshooting
The minimum launch options that cause the issue to persist are:
/WineDetectionEnabled:False

Most launch options tested were tested with:
gamemoderun %command% /WineDetectionEnabled:False

The launch options that have been tested with no impact on the exploding vertices are:
VKD3D_DISABLE_EXTENSIONS=VK_EXT_mesh_shader
VKD3D_DISABLE_EXTENSIONS=VK_NV_raw_access_chains
PROTON_HIDE_NVIDIA_GPU=1 PROTON_ENABLE_NVAPI=1
VKD3D_CONFIG=no_upload_hvv
VKD3D_CONFIG=single_queue
VKD3D_DISABLE_EXTENSIONS=VK_NV_low_latency2
VKD3D_CONFIG=disable_uav_compression

Shader caches were cleared between each test.

[steam-2246340.log](https://github.com/user-attachments/files/32675762/steam-2246340.log)

