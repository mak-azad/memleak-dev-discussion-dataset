# Forza Horizon 6 (2483190)

- URL: https://github.com/ValveSoftware/Proton/issues/9789
- Repo: ValveSoftware/Proton (language: C++)
- State: open; created 2026-05-15T06:55:51Z; status ok; passes main

## Issue body

reporter (NONE) · luneko · 2026-05-15T06:55:51Z · https://github.com/ValveSoftware/Proton/issues/9789

# Compatibility Report
- Name of the game with compatibility issues: Forza Horizon 6
- Steam AppID of the game: 2483190

## System Information
- GPU: AMD Radeon RX 9070 XT
- Video driver version: Mesa 26.1.0
- Kernel version: Linux 7.0.5-zen1
- Link to full system information report as [Gist](https://gist.github.com/): https://gist.github.com/luneko/4f3366412129edfcf8e662802c494bfe
- Proton version: Experimental, Bleeding Edge

## I confirm:
- [x] that I haven't found an existing compatibility report for this game.
- [x] that I have checked whether there are updates for my system available.

<!-- Please add `PROTON_LOG=1 %command%` to the game's launch options and
attach the generated $HOME/steam-$APPID.log to this issue report as a file.
(Proton logs compress well if needed.)-->
Game spams the log file when using "PROTON_LOG=1" and gets to big to be uploaded. (6GB raw, 200mb archived) If there is an alternative where I can upload it I will gladly do so.

EDIT: Managed to get a Proton log that is small enough to upload here. This is only logging during the splash screen when launching the game. Everything else gets to big to quick. It seems to be spamming the same stuff over and over.
[steam-2483190 (3).zip](https://github.com/user-attachments/files/27802812/steam-2483190.3.zip)

## Symptoms <!-- What's the problem? -->
- Severe stutters. Some of them are visible in frametimes (world loading) but some cannot be seen in the frame graph. (Game does not move for a fraction of time)
- Turning ray tracing on crashes the game with GPU Error.
- On Startup game only shows a black screen until window is manually focused. _(Fixed in experimental-bleeding-edge-11.0-362204-20260515-p0e017a-wa4366f-d60978e-vd27571)_

## Reproduction
- Run the games benchmark or start playing normally.

<!--
1. You can find the Steam AppID in the URL of the shop page of the game.
   e.g. for `The Witcher 3: Wild Hunt` the AppID is `292030`.
2. You can find your driver and Linux version, as well as your graphics
   processor's name in the system information report of Steam.
3. You can retrieve a full system information report by clicking
   `Help` > `System Information` in the Steam client on your machine.
4. Please copy it to your clipboard by pressing `Ctrl+A` and then `Ctrl+C`.
   Then paste it in a [Gist](https://gist.github.com/) and post the link in
   this issue.
5. Also, please copy the contents of `Help` > `Steam Runtime Diagnostics` to
   the gist.
6. Please search for open issues and pull requests by the name of the game and
   find out whether they are relevant and should be referenced above.
-->


## Comment 4457695164

other (NONE) · LuxiP7 · 2026-05-15T07:01:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4457695164

I'm guessing the fix for black screen is just adding FH6 id to force_below_hack
https://github.com/ValveSoftware/wine/blob/bleeding-edge/dlls/winex11.drv/window.c#L3613

I would create a pull request but I don't have FH6 so can't test properly

## Comment 4457997771

other (NONE) · yobson1 · 2026-05-15T07:44:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4457997771

also getting the same stutters and game crashing if ray tracing is turned on with 9070xt on KDE plasma. kernel `7.0.5-2-cachyos` mesa `26.1.0`. i tried the default proton that steam selected which was 10.0, experimental, bleeding edge, proton-ge and proton-cachyos all have the issues. the stutters manifest in an odd and very unpleasing way too where it slows the game down briefly during the sutter

## Comment 4458009920

other (NONE) · RSXEnthusiast · 2026-05-15T07:46:59Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4458009920

For Nvidia GPUs, the game seems to universally crash at higher graphical settings with a FHC00 error. It only seems to happen when the GPU is near maxxed out. Ray tracing also does not work at all, though I'd guess it's due to the same reasons higher graphical settings don't work, as it throws the same error.

To repro, try launching the game at maxxed settings and observe the crash. At min settings it should launch and play fine.

I have also tried all the proton versions.

## Comment 4458103033

other (NONE) · Insprill · 2026-05-15T08:03:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4458103033

7900XTX, mesa `26.1.0`, `7.0.6-1-cachyos`, Hyprland v0.55.1.

If you park your car and, in third person, look around slowly, frame times will be extremely consistent (~9.5ms for me). If you start spinning the camera around fast (via mouse or controller), it will become a stuttery mess (0.4ms min, 70ms max). GPU usage stays at 99% while this is happening. Driving, or doing donuts, does *not* cause this to happen even though the camera movement is the same.

While driving frametimes are also inconsistent, but not always. It will be smooth for several seconds, then randomly frametimes will double or triple. It could last for only a couple frames, or upwards of a full second before returning to normal. When this happens, physics seem to slow down which makes driving almost impossible. Limiting FPS to 60 mostly resolves this. VSync does not effect it.

## Comment 4458780929

other (NONE) · cranberry3148 · 2026-05-15T09:53:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4458780929

This fixed the crashes for me:
```
VKD3D_CONFIG=no_upload_hvv,single_queue PROTON_VKD3D_HEAP=1 %command%
```

Arch Linux 7.0.3-zen1-2-zen
Proton GE 10-34
NVIDIA Driver Version: 595.71.05

## Comment 4458793550

other (NONE) · RSXEnthusiast · 2026-05-15T09:55:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4458793550

> This fixed the crashes for me:
> 
> ```
> VKD3D_CONFIG=no_upload_hvv,single_queue PROTON_VKD3D_HEAP=1 %command%
> ```

No dice on that for me unfortunately. What are your system specs?

## Comment 4458817183

other (NONE) · ettkatthej · 2026-05-15T09:58:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4458817183

Adding some more details, to show how bad the stuttering is (dualboot). Fingers crossed MS will assist since it's steam deck verified.

<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/1197484d-e646-4f4d-99bc-0fe71e5069a6" />

<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/8f1de112-e2e9-41d7-9cd2-56bf6abd5497" />

## Comment 4459010099

other (NONE) · yobson1 · 2026-05-15T10:30:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4459010099

runs much smoother on windows for me too now that i moved the game to my windows drive. it still has some stutters and they do exhibit the same very distracting physics slowdown as on linux but they are far less frequent on windows making it far more playable

## Comment 4459824497

other (NONE) · ben-mcginty · 2026-05-15T12:39:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4459824497

I wouldn't say _unofficial_ per se, as Playground themselves say that they support Steam Deck, but nothing more than that (and thus they only support the specific hardware configuration that deck provides), but honestly it could go either way.

## Comment 4459888072

other (NONE) · ben-mcginty · 2026-05-15T12:49:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4459888072

https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4458009920
> For Nvidia GPUs, the game seems to universally crash at higher graphical settings with a FHC00 error. It only seems to happen when the GPU is near maxxed out. Ray tracing also does not work at all, though I'd guess it's due to the same reasons higher graphical settings don't work, as it throws the same error.

This is what I'm experiencing too broadly speaking. I have observed that GPU usage spikes, and then crashes to 0 as the application becomes unresponsive and then has to be killed, or wait for its crash reporter to kick in.

## Comment 4460130386

reporter (NONE) · luneko · 2026-05-15T13:25:17Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460130386

I managed to get a proton log that is small enough to upload to GitHub and added it to the main post. 

This is only what happens during the initial splash screen of the game as everything else gets to big to quickly. I hope it's still useful. The log where I let the full benchmark run trough is over 6GB. 

## Comment 4460360969

other (NONE) · RSXEnthusiast · 2026-05-15T13:58:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460360969

> This is what I'm experiencing too broadly speaking. I have observed that GPU usage spikes, and then crashes to 0 as the application becomes unresponsive and then has to be killed, or wait for its crash reporter to kick in.

This is identical behavior to my experiences.

## Comment 4460580429

other (NONE) · hamcoremusic · 2026-05-15T14:23:14Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460580429

> This fixed the crashes for me:
> 
> ```
> VKD3D_CONFIG=no_upload_hvv,single_queue PROTON_VKD3D_HEAP=1 %command%
> ```
> 
> Arch Linux 7.0.3-zen1-2-zen Proton GE 10-34 NVIDIA Driver Version: 595.71.05

It's worth noting that PROTON_VKD3D_HEAP=1 seems to be a cachy-proton specific flag as some users have reported.

## Comment 4460609043

other (NONE) · ben-mcginty · 2026-05-15T14:27:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460609043

I'm using Fedora 44 KDE with those flags (in an attempt to get it to work), but still face crashes. I've found that turning down the graphics settings helps alleviate some but not all. For reference it defaulted to the 'Extreme' preset for my system, but I've had to turn that down all the way to medium.
More specifically: `PROTON_ENABLE_WAYLAND=1 PROTON_ENABLE_NVAPI=1 PROTON_ENABLE_HIDRAW=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=no_upload_hvv,single_queue GST_PLUGIN_FEATURE_RANK=protonvideoconvert:MAX %command%`
(I found it on a reddit comment and it seems to somewhat work)

Edit: for further reference I'm using the RPM Fusion-provided non-free Nvidia driver v. `595.71.05`

## Comment 4460693368

other (NONE) · hamcoremusic · 2026-05-15T14:37:57Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460693368

> I'm using Fedora 44 KDE with those flags (in an attempt to get it to work), but still face crashes. I've found that turning down the graphics settings helps alleviate some but not all. For reference it defaulted to the 'Extreme' preset for my system, but I've had to turn that down all the way to medium. More specifically: `PROTON_ENABLE_WAYLAND=1 PROTON_ENABLE_NVAPI=1 PROTON_ENABLE_HIDRAW=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=no_upload_hvv,single_queue GST_PLUGIN_FEATURE_RANK=protonvideoconvert:MAX %command%` (I found it on a reddit comment and it seems to somewhat work)
> 
> Edit: for further reference I'm using the RPM Fusion-provided non-free Nvidia driver v. `595.71.05`

That was my comment! You can actually clean this up a lot as someone reported below my comment if you use GE-Proton. If not, keep the NVAPI flag for regular Proton

`PROTON_ENABLE_WAYLAND=1 VKD3D_CONFIG=no_upload_hvv,single_queue %command%` should suffice and if you have `gamemode` installed you can add that in before `%command%`

Please see [this comment](https://www.reddit.com/r/linux_gaming/comments/1tdm434/comment/olwi0rm/) explaining most of the flags

I still get crashes on Fedora 44 KDE Plasma Desktop Edition with a RTX 3090, Ryzen 9 5900X, and 64GB DDR4 RAM. I am using the RPM Fusion open kernel NVIDIA drivers 595.71.05.

## Comment 4460719030

other (NONE) · ben-mcginty · 2026-05-15T14:41:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460719030

Thanks :) I was more putting it in there for the devs to fix for verbosity (it seems to be a weird game, as FH4/5 ran really well through Proton) as it's just the stock Proton Experimental. Thanks for linking to that thread, I'll have to go in and clean all of the flags in all of my games up.

## Comment 4460805022

other (NONE) · Ahpoto · 2026-05-15T14:52:41Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4460805022

9070XT 5700X3D Cachyos-bore KDE Plasma Wayland

Mesa version 26.1.0. I tried plugging the controller, uncapping fps and and disabling v-sync, tried disabling rebar in bios, to no avail.

This is what I get with the benchmark. Hope it can help.

<img width="3839" height="2159" alt="Image" src="https://github.com/user-attachments/assets/e09e57cf-a861-48a3-aca5-ccefc39abb0c" />

## Comment 4461704973

other (NONE) · AkihaTatsu · 2026-05-15T17:02:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4461704973

> For Nvidia GPUs, the game seems to universally crash at higher graphical settings with a FHC00 error. It only seems to happen when the GPU is near maxxed out. Ray tracing also does not work at all, though I'd guess it's due to the same reasons higher graphical settings don't work, as it throws the same error.
> 
> To repro, try launching the game at maxxed settings and observe the crash. At min settings it should launch and play fine.
> 
> I have also tried all the proton versions.

Adding a data point on **RTX 5090 / Blackwell GB202**.

- **GPU:** NVIDIA GeForce RTX 5090 (GB202, PCI `10de:2b85`)
- **Driver:** NVIDIA open kernel module **595.71.05** (`nvidia-open-dkms`)
- **Kernel:** Linux 7.0.6-1-cachyos (stable, not -rc)
- **Proton tested:** `proton-cachyos-11.0-20260429-slr` (community — noted only because that is what reproduced here; stock `Valve Proton Experimental` / `11.0-beta3` / `10.0` / `GE-Proton10-34` all bundle different vkd3d-proton revisions but all of them generate the same crash).
- **Symptom on Linux:** game hangs after ~3 min of open-world driving, game writes `CrashReport.xml` with `REASON="Video card"` / `REASON_INFO=0x0000000000000102` (DXGI `WAIT_TIMEOUT` → device-removed). Settings (preset, DLSS mode, RT, framerate cap, V-Sync, resolution) do **not** avoid it.

The kernel-side fault is **Xid 109 `CTX SWITCH TIMEOUT`**, three
confirmed events across two boots:

```
NVRM: Xid (PCI:0000:01:00): 109, pid=159175, name=forzahorizon6.e, channel 0x00000029, errorString CTX SWITCH TIMEOUT, Info 0x3c03f
NVRM: Xid (PCI:0000:01:00): 109, pid=174356, name=forzahorizon6.e, channel 0x00000029, errorString CTX SWITCH TIMEOUT, Info 0x30c03f
NVRM: Xid (PCI:0000:01:00): 109, pid=98371,  name=forzahorizon6.e, channel 0x0000001f, errorString CTX SWITCH TIMEOUT, Info 0x3c02c
```

VRAM usage at crash was 4.9 GB / 29.0 GB budget on the latest run — not a memory-pressure case. The Xid is the **first** event in the kernel log; the user-mode `ACCESS_VIOLATION_WRITE` is downstream of the device-removed swapchain.


## Comment 4461959785

other (NONE) · Botiplz · 2026-05-15T17:43:50Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4461959785

I dug through my game crash reports and found something interesting when comparing it to Windows reports:

- I have a NVIDIA RTX 4080 with 16GB VRAM and 32GB of RAM which gets shown correctly in the crash report:

```
<THP_CPU0Name Value="AMD Ryzen 7 7700X 8-Core Processor/>
<THP_GPU0Description Value="NVIDIA GeForce RTX 4080"/>
<MEM_LIMIT Value="33231736832"/>
```

- What I noticed:: My game always crashes while using about 16GB of RAM (about the same amount as my VRAM):

```
<MEM_USED Value="1606627328"/>
```

I dug through some Windows Crash logs online which seems to contains fields like `VIDEO_SHARED_BUDGET, VRAM_USED, VIDEO_SHARED_USED` for VRAM usage. I didn't see those in my Linux crash reports.

Totally speculative theory: What if the game crashes when MEM_USED goes to/exceeds your GPUs VRAM, i.e. 16/32GB RAM gets used, but you have 16GB VRAM which the game can't handle because of some shared memory shenanigans -> crash.


## Comment 4462663479

other (NONE) · galacticaledge · 2026-05-15T19:13:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4462663479

> I'm guessing the fix for black screen is just adding FH6 id to force_below_hack https://github.com/ValveSoftware/wine/blob/bleeding-edge/dlls/winex11.drv/window.c#L3613
> 
> I would create a pull request but I don't have FH6 so can't test properly

Just made a [pull request](https://github.com/ValveSoftware/wine/pull/327). Hopefully it works just like with FH4 and FH5.

UPDATE: It's in bleeding-edge now. Glad to have made my first Proton contribution :)

## Comment 4463618715

reporter (NONE) · luneko · 2026-05-15T21:03:15Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4463618715

> > I'm guessing the fix for black screen is just adding FH6 id to force_below_hack https://github.com/ValveSoftware/wine/blob/bleeding-edge/dlls/winex11.drv/window.c#L3613
> > I would create a pull request but I don't have FH6 so can't test properly
> 
> Just made a [pull request](https://github.com/ValveSoftware/wine/pull/327). Can anyone test it for me since I cannot do it myself right now.

Can confirm that the black screen issue is fixed with latest bleeding-edge from 1hr ago.

Performance wise I was able to minimize stutters by locking the game to 60FPS and setting the overall graphics to "High". Of course this is not optimal but atleast playable on day 1.

## Comment 4463867120

other (NONE) · chaosfreak93 · 2026-05-15T21:42:09Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4463867120

Setting "Environment Texture Quality" higher then "High" causes stutters. Paired with locking FPS higher then 60FPS is causing severe slow downs for me.

## Comment 4464359927

other (NONE) · M-Gilly · 2026-05-15T22:55:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4464359927

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4463618715

Black screen issue was fixed for me too. 

## Comment 4464379637

other (NONE) · mrtonguelicker · 2026-05-15T23:00:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4464379637

Adding some kernel level fault traces from a RX 9070XT (gfx1201, Navi 48) on a different kernel branch than OP with the aim of narrowing down the responsible layer. 

### System

GPU: AMD Radeon RX 9070 XT (gfx1201, RDNA 4, Navi 48)
CPU: Ryzen 7 9800X3D (Zen 5 iGPU also present at 0000:11:00.0, dGPU at 0000:03:00.0)
Kernel: 6.18.26-2-lts (different from OP's 7.0.5-zen1, same bug, suggests userspace)
Mesa: 26.0.6 
Proton Experimental, bleeding-edge wine (force_below_hack black-screen fix applied)
FH6 vkd3d-proton program hash: 1bd3f2dd7c19e82e

### Reproduction

Launch FH6 with ray tracing enabled in-game. System fully locks within seconds of RT being exercised (benchmark, or entering the world). No GPU reset begin! is ever logged, so amdgpu never recovers and the desktop hangs with it, requiring a hard restart.

### Test 1: stock launch options, RT on

amdgpu 0000:03:00.0: amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:7 pasid:200)
amdgpu 0000:03:00.0: amdgpu:  Process forzahorizon6.e pid 8135 thread vkd3d_queue pid 8274
amdgpu 0000:03:00.0: amdgpu:   in page starting at address 0x00008000f1198000 from client 10
amdgpu 0000:03:00.0: amdgpu: GCVM_L2_PROTECTION_FAULT_STATUS:0x00701431
amdgpu 0000:03:00.0: amdgpu:          Faulty UTCL2 client ID: SQC (data) (0xa)
amdgpu 0000:03:00.0: amdgpu:          MORE_FAULTS: 0x1
amdgpu 0000:03:00.0: amdgpu:          WALKER_ERROR: 0x0
amdgpu 0000:03:00.0: amdgpu:          PERMISSION_FAULTS: 0x3
amdgpu 0000:03:00.0: amdgpu:          MAPPING_ERROR: 0x0
amdgpu 0000:03:00.0: amdgpu:          RW: 0x0

Fault repeats roughly nine times at the same address before journald stops capturing.

### Test 2: RADV_DEBUG=nobvh8 %command%, RT on
Identical fault, identical address (0x00008000f1198000) in a fresh game launch (different pid, different pasid).

### Test 3: RADV_PERFTEST=emulate_rt %command%, RT on
Same fault class (SQC data scalar load, gfxhub, vkd3d_queue thread), but now with two addresses interleaved: 0x00008000f1198000 and 0x00008000e82c2000. Software emulated RT changes which shaders RADV emits for the RT pipeline so the surface of bad addresses shifts but the overall bug is preserved.

## Comment 4466575574

other (NONE) · drkhac · 2026-05-16T10:24:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4466575574

Loading into the game and just normal racing sometimes throws the code FHC00 code [Error](https://imgur.com/a/IZYrTEu)
OS: Bazzite 44 (Fedora 44 based)
Kernel: 6.17.7-ba29.fc43.x86_64
GPU: NVIDIA GeForce RTX 4050 Laptop
Driver: 595.58.03
Proton: GE-Proton10-34 (i have also used other Proton versions as well)
Status: Gets past intro races and character creation but crashes on open world load with Video Card Crash FHCOO
Launch options that got furthest: PROTON_ENABLE_NVAPI=1 PROTON_HIDE_NVIDIA_GPU=0 VKD3D_CONFIG=no_upload_hvv,single_queue VKD3D_SHADER_CACHE_PATH=/tmp/vkd3d-cache %command%

## Comment 4466716432

other (NONE) · dyfrgi · 2026-05-16T11:33:39Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4466716432

Same NVidia crash on CTX SWITCH TIMEOUT. NixOS 26.05 (unstable), kernel 6.18.28, NVidia driver 595.71.05, GeForce RTX 5080.

Has anyone found good workarounds for the NVidia crashes?

## Comment 4466720812

other (NONE) · ben-mcginty · 2026-05-16T11:35:50Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4466720812

I've found that if you turn down the graphics settings way down (I have a 5080 and am running it on low), the crashes happen less often, but still happen.

## Comment 4467199933

other (NONE) · craimasjien · 2026-05-16T15:00:17Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467199933

I've done some testing with logging enabled in multiple parts of Proton, [filed a bug report on vkd3d](https://github.com/HansKristian-Work/vkd3d-proton/issues/3032) as I suspect the issue is originating from there. 

## Comment 4467317163

other (NONE) · scorthyn · 2026-05-16T15:47:34Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467317163

9800x3D + 9070xt on cachyOS, RT crashes game and theres horrible stutters even tho fps are high. 

## Comment 4467414738

other (NONE) · DevMau5x · 2026-05-16T16:21:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467414738

I’m also seeing stuttering and important Frametime spikes issue on Bazzite with an AMD RX 6950 XT.

System:

OS: Bazzite
GPU: AMD Radeon RX 6950 XT
RAM: 96 GB
Storage: internal NVMe
Proton: GE-Proton latest gives the best result so far, but the issue is still present

Symptoms:
The game has severe frametime spikes / FPS drops when rapidly rotating the camera with the right joystick. This happens even on Medium preset with FPS capped around 80 FPS. GPU usage is not maxed out, usually around ~80%, but as soon as I rotate the camera quickly in circles, FPS drops hard and frametime spikes.

GE-Proton latest improves the issue significantly compared to other Proton versions I tested, but it does not fully solve it.

I generated a Proton log. The full log was huge, around 6 GB for 2min of in game, so I filtered repeated warnings/errors. The most suspicious result was a massive number of repeated illegal-instruction exceptions:

5114501 warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.

Context around the first repeated exceptions shows repeated SIGSYS and EXCEPTION_ILLEGAL_INSTRUCTION on the same thread:

523.783:0158:015c:trace:seh:sigsys_handler SIGSYS, rax 0x50, rip 0x6ffff7d99a5c.
523.799:0158:015c:trace:seh:sigsys_handler SIGSYS, rax 0x50, rip 0x6ffff7d99a5c.
523.799:0158:015c:trace:seh:sigsys_handler SIGSYS, rax 0x8c, rip 0x6ffff7d99acf.
523.799:0158:015c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
523.799:0158:015c:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=00006FFFF7C66164

This makes me think the issue may be Proton/Wine/VKD3D-related rather than a raw GPU, CPU, RAM, or anything on hardware.

Reproduction:

Launch the game on Bazzite with GE-Proton latest.
Load into the open world.
Use a controller.
Stand still or drive slowly.
Rapidly rotate the camera in circles using the right joystick.
Observe severe frametime spikes and FPS drops.

## Comment 4467482541

other (NONE) · craimasjien · 2026-05-16T16:44:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467482541

@DevMau5x, it’s definitely a Linux compatibility issue. I spent hours yesterday playing FH6 on Windows 11 with ray tracing enabled and noticed the Linux performance was subpar. I suspect it’s related to vkd3d, particularly since the issue doesn’t seem to depend on the hardware.  The symptoms are identical on both AMD and Nvidia GPUs. 

## Comment 4467542541

other (NONE) · dyfrgi · 2026-05-16T17:03:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467542541

This let me play for half an hour just now on my NVidia card. This is with **proton-cachyos-11.0-20260506-slr-x86_64_v3** on NixOS 26.05 (unstable), with a 9950X3D and 5080, running in the Niri compositor. All settings on ultra but no RT. xwayland-satellite has some issues with Forza games right now which result in them overlaying the Steam window (https://github.com/Supreeeme/xwayland-satellite/issues/392), but gamescope works okay.

```
VKD3D_CONFIG=enable_experimental_features,descriptor_heap PROTON_VKD3D_HEAP=1 gamescope -W 3440 -H 1440 -w 3440 -h 1440 -f -S integer --adaptive-sync -- %command%
```
WARNING: DO NOT GRAB THIS BLINDLY AND USE IT. You need a version of proton with the correct patches to enable the descriptor heap. proton-cachyos is the only widely distributed one I'm aware of.

Benchmark came it at 86fps, but I had some stuttering towards the end of the first race. Also, there's a blur bug with gamescope when running at native resolution. Looks like it's over a year old so I've got no hope for a fix any time soon. There is a workaround of building with `-fno-fast-math`, though. https://github.com/ValveSoftware/gamescope/issues/1924. I had hoped that `-S integer` would fix it but it did not change anything.

## Comment 4467583889

reporter (NONE) · luneko · 2026-05-16T17:21:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467583889

> [@DevMau5x](https://github.com/DevMau5x), it’s definitely a Linux compatibility issue. I spent hours yesterday playing FH6 on Windows 11 with ray tracing enabled and noticed the Linux performance was subpar. I suspect it’s related to vkd3d, particularly since the issue doesn’t seem to depend on the hardware. The symptoms are identical on both AMD and Nvidia GPUs.

FH5 had pretty much the same issue with streaming in assets and it was never fully fixed. I think it was just less relevant because altering Environmental settings and locking FPS would get rid of the issue. But now with FH6 having better graphics, and therefore bigger assets, this might be the issue here.
Also suspecting a vkd3d issue here so let's hope this can be fixed so the game can be enjoyed fluently on the penguin :)

## Comment 4467598264

other (NONE) · SuperMewio · 2026-05-16T17:24:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467598264

I played for 4-6 hours yesterday and crashed only once that being said, my friend also crashed once on Windows with the same error I got. so that crash is likely irrelevant.

I am also on cachyos with heap enabled (enabled correctly like dyfrgi's message). Prior, I was getting the same crashing seconds after being in-game with the same error.

Runs great on my RTX 5070 mobile. Around 80 fps on high with dlaa and no frame gen.

My launch options for comparisons sake, I never cleaned up anything that may be unneeded. `VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_USE_NTSYNC=1 PROTON_VKD3D_HEAP=1 PROTON_ENABLE_WAYLAND=1 PROTON_ENABLE_HDR=1 PROTON_DLSS_UPGRADE=1 %command% /WineDetectionEnabled:False`

Operating System: CachyOS Linux 
KDE Plasma Version: 6.6.5
KDE Frameworks Version: 6.26.0
Qt Version: 6.11.1
Kernel Version: 7.0.8-1-cachyos (64-bit)
Graphics Platform: Wayland
Processors: 16 × AMD Ryzen AI 7 350 w/ Radeon 860M
Memory: 32 GiB of RAM (30.4 GiB usable)
Graphics Processor 1: AMD Radeon 860M Graphics
Graphics Processor 2: NVIDIA GeForce RTX 5070 Laptop GPU
Manufacturer: HP
Product Name: OMEN Gaming Laptop 17z-db100

## Comment 4467612731

other (NONE) · pflavio · 2026-05-16T17:28:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467612731

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467598264

Could you please post your launch arguments, too? When using @dyfrgi ones adjusted for my resolution the Steam keyboard opens, then the game starts (I can hear the intros and background music) but it's behind a Steam loading screen. When I close that one, the game closes, too.

## Comment 4467615065

other (NONE) · SuperMewio · 2026-05-16T17:28:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467615065

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467612731

I edited my message with my launch option seconds before your response haha

## Comment 4467639496

other (NONE) · pflavio · 2026-05-16T17:40:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467639496

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467615065

Thank you! I tried with ``VKD3D_CONFIG=enable_experimental_features,descriptor_heap PROTON_VKD3D_HEAP=1 %command%`` and it starts but crashes like before (a few meters into the intro race). Damn I hope this gets an official fix or updated Proton version by someone soon. I'm on an up-to-date Bazzite system with a 4090, 9800X3D and 64 GB DDR5 RAM for reference.

## Comment 4467705065

other (NONE) · SuperMewio · 2026-05-16T18:07:12Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467705065

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467639496

From my understanding, you need the cachyos variant of proton to be able to use heap. It recently updated with the blackscreen fix too so you can launch the game easier.

https://github.com/CachyOS/proton-cachyos

## Comment 4467708517

other (NONE) · pflavio · 2026-05-16T18:09:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467708517

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467705065

Yeah I'm using CachyOS Proton Latest :)

## Comment 4467781843

other (NONE) · leberschnitzel · 2026-05-16T18:41:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467781843

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467639496

I had the same problem, just crashing right when the handover was from video to gameplay, and I need to disable ray tracing in game

## Comment 4467787316

other (NONE) · pflavio · 2026-05-16T18:43:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467787316

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467781843

Had as in it works now? If so, what are your options? I disabled RT already, but it still crashes.

## Comment 4467793102

other (NONE) · leberschnitzel · 2026-05-16T18:46:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467793102

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4467787316

it works without raytracing for me. Still crashes when I enable it.

## Comment 4468002719

other (NONE) · serhii-nakon · 2026-05-16T20:20:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468002719

Guys here issue with game itself and need bunch of workarounds to be done on vkd3d-proton side
Like PR here https://github.com/HansKristian-Work/vkd3d-proton/pull/3029 - allow at least run game with RT and it still crashes after some time in race
And new one PR https://github.com/HansKristian-Work/vkd3d-proton/pull/3033 - Here huge PR for it 
If you want to try - download build for this PR https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/25965683046/artifacts/7034546231 

And replace vkd3d libs by commands like this 

```
cp -vr Downloads/vkd3d-proton/x64/* .steam/steam/compatibilitytools.d/GE-Proton10-34/files/lib/wine/vkd3d-proton/x86_64-windows/
cp -vr Downloads/vkd3d-proton/x86/* .steam/steam/compatibilitytools.d/GE-Proton10-34/files/lib/wine/vkd3d-proton/i386-windows/
```

PS: From PR description seems need to add something like this and use latest possible Mesa (git version suggested)
```
RADV_EXPERIMENTAL=heap radv_wait_for_vm_map_updates=true %command%
```

## Comment 4468786526

other (NONE) · pbellchambers · 2026-05-17T01:36:50Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468786526

I tested out the above and it solved everything for me _with ray tracing disabled_ (nvidia 3080ti on ubuntu 26.04). Previously I was stuck with everything in very low settings and capped at 36fps to lower the frequency of crashes, now with that vkd3d patch I have everything set ultra with uncapped fps, no crashes at all after several hours, and almost no stuttering. 

Still causing crashes:
- Ray tracing on
- `Nvidia Reflex Low Latency`, if that's on then the game freezes on loading (doesn't even get to the main menu). I guess that must be a different issue?

## Comment 4468796828

other (NONE) · ol1fer · 2026-05-17T01:40:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468796828

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468786526

@pbellchambers 
just looking at this now and your post came in, which is 'the above'? i'm literally having this issue now and really wanna know what fixes it?

## Comment 4468877779

other (NONE) · ben-mcginty · 2026-05-17T02:15:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468877779

I did that and it fixed the stuttering and everything, but it completely broke Steam Input - my controller was being picked up as a controller and a keyboard. I'm just using the default controller config so I don't think that's it.

## Comment 4468882140

other (NONE) · ben-mcginty · 2026-05-17T02:17:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468882140

> just looking at this now and your post came in, which is 'the above'? i'm literally having this issue now and really wanna know what fixes it?

Download the actions run and run the command to patch Proton GE, then select it as the Proton version. You can use ProtonUp to download the specific Proton version to patch.



## Comment 4468921330

other (NONE) · ol1fer · 2026-05-17T02:26:52Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468921330

> > just looking at this now and your post came in, which is 'the above'? i'm literally having this issue now and really wanna know what fixes it?
> 
> Download the actions run and run the command to patch Proton GE, then select it as the Proton version. You can use ProtonUp to download the specific Proton version to patch.


I downloaded cachyos proton via protonplus (since i had it installed) and use

VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_VKD3D_HEAP=1 %command%

solved the stuttering issue. seems to be okay, i'll report back if game has further issues.


## Comment 4468957152

other (NONE) · RPINerd · 2026-05-17T02:33:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468957152

## System Information
- GPU: AMD Radeon RX 6900 XT
- Video driver version: Mesa 26.0.6-1
- Kernel version: Linux 7.0.8-arch1-1
- Proton version: 10, 11, Experimental
- [System Gist](https://gist.github.com/RPINerd/ccf0173772bc2c8012e6c967d64cd2a7)

## Symptoms <!-- What's the problem? -->
- "Lunging" framerates. I wouldn't call these stutters because they don't drop that low or that quickly. Instead it's more like every 2-6 second while driving time slows down and then everything lurches back up to full speed

## Reproduction
- Drive around anywhere.

## Some things I've already tried (probably not exhaustive list)
- Frame capping
- V-sync
- FSR (AA and Scaling)
- gamemoderun %command%
- Proton-GE (10-34 I believe?)
- Windowed
- Lower resolution
- Disabling VPN

## Comment 4468962605

other (NONE) · Titaniumtown · 2026-05-17T02:36:19Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468962605

@RPINerd VPN would have nothing to do with it. But did you try @serhii-nakon's suggestion?

## Comment 4468966749

other (NONE) · ol1fer · 2026-05-17T02:38:52Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468966749

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468957152

@RPINerd that's exactly what i had. it's almost like my fps was still high but the physics engine was stuttering. i used the cachyos proton version (i got it via protonplus which is just a little app for downloading and installing proton verisons) and then make sure to swap to that version in steam properties on the game and then set launch options to `VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_VKD3D_HEAP=1 %command%`



## Comment 4468995521

other (NONE) · Tixx7 · 2026-05-17T02:56:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468995521

> I tested out the above and it solved everything for me (nvidia 3080ti on ubuntu 26.04). Previously I was stuck with everything in very low settings and capped at 36fps to lower the frequency of crashes, now with that vkd3d patch I have everything set ultra with uncapped fps, no crashes at all after several hours, and almost no stuttering.
> 
> One setting does still cause the game to crash: `Nvidia Reflex Low Latency`, if that's on then the game freezes on loading (doesn't even get to the main menu). I guess that must be a different issue?

Have you tried if ray-tracing also still crashes the game? You mentioned everything set to ultra, which i assume means the ultra preset which doesnt have any ray-tracing enabled but please clarify.

## Comment 4469084732

other (NONE) · RPINerd · 2026-05-17T03:21:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469084732

> [@RPINerd](https://github.com/RPINerd) VPN would have nothing to do with it. But did you try [@serhii-nakon](https://github.com/serhii-nakon)'s suggestion?

Yeah I figured VPN was irrelevant, but just wanted to put all the tinkering out there, including the hail-marys lol

I just tried the run commands provided by their post, and while they felt like maybe they reduced the frequency ever so slightly, they definitely did not fix the issue.

Currently building the latest mesa from git..

Also I'm not doing any RT at all, so those crashes are not a concern for my use case :)

## Comment 4469217931

other (NONE) · CRKrJ4K · 2026-05-17T03:47:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469217931

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468966749

I have the same issue, but those launch options didn't fix it for me.

14900KS, 7900 XTX, CachyOS w/20260506-cachyos-proton

## Comment 4469381938

other (NONE) · Nition · 2026-05-17T04:51:40Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469381938

Just to add one more data point, I've got two of the common issues reported here:

- The "Lunging" framerate as described above, where it feels more like the physics engine is playing catchup than a normal framerate issue.
- A crash when getting past the main menu if ray tracing is on.

I don't get any crashes with raytracing off.

**OS:** Fedora KDE Plasma v44
**CPU:** AMD Ryzen 9 5950X
**GPU:** AMD Radeon RX 6900 XT

I haven't tried any special fixes or alternative Proton versions at this stage.

## Comment 4469393577

other (NONE) · kassieclaire · 2026-05-17T04:58:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469393577

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468002719

Seems like this gets about 20-30 seconds into the benchmark for me, low ray tracing, then crashes in the same way as before. For reference I'm running at 4k with fsr4 performance on a 9070xt with cachyos using gamescope, using the latest cachyos-proton

## Comment 4469413297

other (NONE) · mrtonguelicker · 2026-05-17T05:09:24Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469413297

> Seems like this gets about 20-30 seconds into the benchmark for me, low ray tracing, then crashes in the same way as before. For reference I'm running at 4k with fsr4 performance on a 9070xt with cachyos using gamescope, using the latest cachyos-proton

I tried this with 1440p Extreme RT Native AA and got about 5 seconds of gameplay before crash. Atleast I'm now able to load into a lobby with this new PR unlike before where it would crash and load at all.

## Comment 4469839291

other (NONE) · htims1989 · 2026-05-17T08:02:28Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469839291

Proton bleeding edge + `bash -c 'ulimit -s 8192; exec "$@"' -- %command%` got it running for me on Steam Headless container on UNRAID with a 5060 Ti. I let Claude Opus 4.6 loose to get it running, hope it helps someone 😄 

EDIT: it set everything to ultra @ 1440p120 but was getting frame drops, trying high (it crashed when trying to change).

EDIT2: High seems to work fine, I've just got audio issues - sounds drops at random points and doesn't come back.

## Comment 4469843248

other (NONE) · 0x8008 · 2026-05-17T08:04:18Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469843248

Exact same issues on 7500F+9060XT, NixOS, Proton-cachy newest. Currently trying out @ol1fer 's suggestion.

ETA: Did not work. Tried the vkd3d-proton fix as well, it stutters SLIGHTLY less but now I get no audio at all.

## Comment 4469915938

other (NONE) · DevMau5x · 2026-05-17T08:28:12Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469915938

> [@RPINerd](https://github.com/RPINerd) that's exactly what i had. it's almost like my fps was still high but the physics engine was stuttering. i used the cachyos proton version (i got it via protonplus which is just a little app for downloading and installing proton verisons) and then make sure to swap to that version in steam properties on the game and then set launch options to `VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_VKD3D_HEAP=1 %command%`

Having the same issue (like graphics elements are struggling to be loaded) with hard slowdowns on my 6950 XT I tried latest CachyOS proton with the command line described and effectively I did observe smaller spikes on mangohud and the game is now playable. There is a lot of performance lost (alternates between 90-125fps in High settings 3440x1440 and GPU stays at 80-85%, never goes to 99% anymore). But it is indeed the issue, I am glad to be fixed on the problem and stop digging on it, I hope Proton/VKD3D devs will be able to figure it out in the following days/weeks.

## Comment 4469921853

other (NONE) · 0x8008 · 2026-05-17T08:30:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469921853

Newest proton-cachyos, NixOS Yarara unstable, kernel 7.0.5, without the vkd3d-proton workarounds (they only break sound for me, no other changes). The only setting that does seem to trully matter is environment texture quality. Doing anything else does not cause any changes for me.


Env. quality LOW:
<img width="2418" height="1309" alt="Image" src="https://github.com/user-attachments/assets/6c1ec8c7-7f64-4876-93bb-7d4e9fe535df" />


Env. quality HIGH:
<img width="2374" height="1311" alt="Image" src="https://github.com/user-attachments/assets/ea83e1f7-f87c-4fec-ad0c-ba39a894d8a1" />

## Comment 4469925606

other (NONE) · pbellchambers · 2026-05-17T08:32:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4469925606

> [@pbellchambers](https://github.com/pbellchambers) just looking at this now and your post came in, which is 'the above'? i'm literally having this issue now and really wanna know what fixes it?

@ol1fer  This one: https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468002719


> Have you tried if ray-tracing also still crashes the game? You mentioned everything set to ultra, which i assume means the ultra preset which doesnt have any ray-tracing enabled but please clarify.

@Tixx7 Ah yeah, it still crashes with ray tracing enabled (but is at least fully stable for me with it off now). Edited my post to clarify.

## Comment 4470323260

other (NONE) · serhii-nakon · 2026-05-17T10:39:59Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470323260

One more clarification, more likely provided command line from PR will not work itself as author expects, it require to replace vkd3d files inside proton too 

## Comment 4470498927

other (NONE) · Deytron · 2026-05-17T11:37:15Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470498927

For some reason, when running this game through Gamescope (for 4K and HDR), the resolution setting is... random ?

I'm running Gamescope on my HTPC with `gamescope -W 3840 -w 3840 -H 2160 -h 2160 -r 120 -f --adaptive-sync -e --hdr-enabled -- steam -gamepadui`

And every time I change the resolution ingame, it changes to a random one, as reported by MangoHud.
To get 4K, I need to switch three times between the previous resolution and 3840x2160 to finally get the full resolution

## Comment 4470837616

other (NONE) · cccyberwolke · 2026-05-17T13:34:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470837616

@RPINerd I had the same issues. On CachyOS, with an 7900 XTX and Ryzen 7 9800X3D. Ran horribly until i limited the frame rate in the menu (the exact value didn't matter) and set Textures to Low. Everything else maxed, except Raytracing (which crashes the game). V-Sync disabled, the game is now buttery smooth. Increasing texture quality introduces stutters and slowdowns again. I have a lot of RAM and VRAM free, but that does not seem to matter

EDIT: I am using gamemoderun (default settings) and proton experimental set in steam, no other tweaks

## Comment 4470877964

other (NONE) · serhii-nakon · 2026-05-17T13:50:34Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470877964

@cccyberwolke I have exactly the same, currently I refunded game and going to buy regular version on May 19 - can you check PR fix - did it change anything for you?

## Comment 4470888488

other (NONE) · treyguitar · 2026-05-17T13:54:49Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470888488

@serhii-nakon I tried the vkd3d PR but the only notable thing is the RT crash is postponed by a little. The benchmark race starts and then crash. The frame drops are unfortunately still there. I can stand not having RT but the bad frame pacing is unbearable unfortunately.

## Comment 4470906689

other (NONE) · serhii-nakon · 2026-05-17T14:01:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470906689

> [@serhii-nakon](https://github.com/serhii-nakon) I tried the vkd3d PR but the only notable thing is the RT crash is postponed by a little. The benchmark race starts and then crash. The frame drops are unfortunately still there. I can stand not having RT but the bad frame pacing is unbearable unfortunately.

Is your setup is Nvidia or AMD gpu based?

In general it would be nice if everyone that tested PR fixes will describe their setup like OS, mesa version, kernel and firmware versions too, and how they installed files into their proton (to make sure that it replaces proper files) - I think it would help to collect proper reports to improve original PR

## Comment 4470968607

other (NONE) · treyguitar · 2026-05-17T14:22:15Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4470968607

@serhii-nakon AMD 9070xt, mesa git 26.2, kernel 7.0.8 cachyos, proton experimental, launch parameters as described in the PR. PR built from git and files replaced in ~/.steam/steam/steamapps/common/Proton - experimental/files/lib/wine/vkd3d-proton/x86_64-windows/

## Comment 4471153341

other (NONE) · RPINerd · 2026-05-17T15:05:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4471153341

> ... Ran horribly until ... set Textures to Low. Everything else maxed, 

@cccyberwolke I just tested this out (medium textures though instead of low) and the lunging is greatly diminished!

I'm also running Proton Experimental, Mesa git, and launch opts:
`VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_VKD3D_HEAP=1 %command%`

## Comment 4471738491

other (NONE) · dino460 · 2026-05-17T17:23:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4471738491

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468002719

Tested this exactly on my machine yesterday, for a while, and it ran almost perfectly.

CPU: intel core i5-10400F
GPU: NVIDIA RTX 2080 Ti
OS: Pop_OS 22.04 (had to manually installed NVIDIA 595.71.05 drivers)
Kernel: 6.5
Mesa: 23.2
Proton: GE 10.34

Apart from a weird frame time pacing at times, it ran great, at 70+ FPS on the countryside, and 40+ in Tokyo.

## Comment 4472131339

other (NONE) · RPINerd · 2026-05-17T18:40:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472131339

An aside from the performance issues, I also can't see vinyls/logos when in the designer.. and a cursory duckduck showed no widespread complaints of this so I'm thinking it's linux based? Any ideas?

<img width="2397" height="1297" alt="Image" src="https://github.com/user-attachments/assets/fdfe435e-352a-4344-9853-b484347a49d2" />

## Comment 4472369057

other (NONE) · Nition · 2026-05-17T20:14:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472369057

Texture quality certainly seems like the "lunging framerate" culprit. I just tried it with literally everything else on Ultra/Extreme but texture quality on Low and it's now nice and smooth.

I guess textures streaming in as you drive is taking longer than it should through Proton.

## Comment 4472442411

other (NONE) · DevMau5x · 2026-05-17T20:37:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472442411

> Texture quality certainly seems like the "lunging framerate" culprit. I just tried it with literally everything else on Ultra/Extreme but texture quality on Low and it's now nice and smooth.
> 
> I guess textures streaming in as you drive is taking longer than it should through Proton.

Same for me on my 6950 XT I can finally play without too much of lunging/slowdowns and close to max perf.
Using latest Proton GE and with (In Game) Environment texture quality Low / Environement Geometry Quality Very Low
Everything else is set to Extrem or high and No RT obviously.

## Comment 4472485085

other (NONE) · SomeKay · 2026-05-17T20:57:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472485085

> [@RPINerd](https://github.com/RPINerd) I had the same issues. On CachyOS, with an 7900 XTX and Ryzen 7 9800X3D. Ran horribly until i limited the frame rate in the menu (the exact value didn't matter) and set Textures to Low. Everything else maxed, except Raytracing (which crashes the game). V-Sync disabled, the game is now buttery smooth. Increasing texture quality introduces stutters and slowdowns again. I have a lot of RAM and VRAM free, but that does not seem to matter
> 
> EDIT: I am using gamemoderun (default settings) and proton experimental set in steam, no other tweaks

Can confirm that setting textures to low makes the hitching go away and in Benchmark Mode I go in the Stutter statistic from hundreds to about 10. I have tried many Proton versions, V-Sync settings, FPS limits, etc. and textures on low actually fixes it. Thank you for the find!

If it means anything, my configuration:
- CPU: i5-12400F
- GPU: Radeon RX 9070 OC
- RAM: 64 GB DDR4-3600
- OS: CachyOS
- Kernel: Linux 7.0.8-1-cachyos
- Mesa: 26.1.0-arch2.1

## Comment 4472529373

other (NONE) · OppaiHacker · 2026-05-17T21:16:44Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472529373

Play Time: 7.5h
Consistent crashes after approximately 40 minutes of gameplay.

Proton: Proton Experimental

Tested Protons: 
- Proton Experimental 
- Proton Hotfix 
- Proton-GE 
- Proton 10.0-4

Launch Options:
`PROTON_ENABLE_WAYLAND=1 PROTON_ENABLE_NVAPI=1 PROTON_ENABLE_HIDRAW=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=no_upload_hvv,single_queue GST_PLUGIN_FEATURE_RANK=protonvideoconvert:MAX %command%`


System Specifications:
- OS: Arch Linux
- Hyperland v0.55.2
- Kernel: 7.0.8-arch1-1
- GPU: NVIDIA RTX 5080
- NVIDIA Driver: 595.71.05
- CPU: AMD Ryzen 7 5700X
- RAM: 64 GB DDR4-3600

In-Game Settings:
- Resolution: 1440p (2K)
- Graphics: Low Preset
- FPS: Capped at 60
- RT / DLSS: Off

## Comment 4472563786

other (NONE) · TheLulanius · 2026-05-17T21:26:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472563786

i only managed to get into the game twice, and when i did its for reasons i cant seem to replicate. All the other times i get the very first intro screen with the warnings, a short audio clip from the playground games intro screen and then it just freezes. If i dont touch it it stays like this forever, if i click something in the window (always starts in windowed mode) it immediately turns completely black and i get an "is not responding" error.  

Tested Protons:

- Proton Experimental
- Proton Hotfix
- Proton-GE 10.34
- Proton 10.0-4
- Proton 11 (beta)
- dwproton 10.0-26


Launch Options:

various, but currently
`PROTON_ENABLE_NVAPI=1 SDL_VIDEODRIVER=wayland %command%`

System Specifications:

- OS: Ubuntu 26.04
- Gnome 50.1
- Kernel: 7.0.0-15-generic
- GPU: NVIDIA RTX 3060
- NVIDIA Driver: 595.58.03
- CPU: AMD Ryzen 5 5600
- RAM: 64 GB DDR4-3200


## Comment 4472589818

other (NONE) · Nition · 2026-05-17T21:38:26Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472589818

Have you got raytracing on by any chance? That seems to cause an immediate crash on getting past the main menu for anyone on Proton.

## Comment 4472594309

other (NONE) · dyfrgi · 2026-05-17T21:40:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472594309

> Tested Protons:
>     * Proton Experimental
>     * Proton Hotfix
>     * Proton-GE
>     * Proton 10.0-4
> 
> 
> Launch Options: `PROTON_ENABLE_WAYLAND=1 PROTON_ENABLE_NVAPI=1 PROTON_ENABLE_HIDRAW=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=no_upload_hvv,single_queue GST_PLUGIN_FEATURE_RANK=protonvideoconvert:MAX %command%`

@TheLulanius These settings don't work with those Protons. PROTON_VKD3D_HEAP is not available on any of the ones that Steam ships. You should install proton-cachyos if you want to use it.

## Comment 4472597402

other (NONE) · TheLulanius · 2026-05-17T21:42:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472597402

> Have you got raytracing on by any chance? That seems to cause an immediate crash on getting past the main menu for anyone on Proton.

No, its disabled. But i dont even get into the main menu, just the very first startup screen

## Comment 4472599321

other (NONE) · TheLulanius · 2026-05-17T21:43:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472599321

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472594309

thanks, but those arent my launch paramaters, but those of OppaiHacker who uses Arch

## Comment 4472618684

other (NONE) · MementoMortes · 2026-05-17T21:52:24Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472618684

My personal observations with the game on an `NVIDIA RTX 4080 Super` and Steams own Experimental Proton currently are:

- Ray Tracing -> broken
- Screen-Space reflections and GI -> broken
- Shader Quality > lowest setting -> increasingly unstable
- Full Screen -> unstable
- DLSS Settings -> unstable
- Fast driving -> unstable

I'm pretty much under the impression that anything that tanks your FPS way below your set Max FPS leads to a crash.

I tried this on the benchmark. If I set max FPS to 60 and use the Ultra preset, no issues at all. 120 and the game crashes consistently while loading into the benchmark.

I also tried this with the `PROTON_HIDE_NVIDIA_GPU=1` env set and I can run both, 60 FPS cap and 120 FPS cap without issue.

This also translates to playing the game. With `PROTON_HIDE_NVIDIA_GPU=1` I can pretty consistently play 40+ minutes, especially when not going full speed while without, I either crash instantly or after 5-10 minutes. There is probably an additional issue which causes crashes when streaming in assets, textures etc. As I now only crash while loading into a scene or while going full speed with a fast car.

## Comment 4472667351

other (NONE) · voxain · 2026-05-17T22:15:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4472667351

Thank god this is a general issue. I thought I was going insane.

## Comment 4475833903

other (NONE) · cccyberwolke · 2026-05-18T08:32:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4475833903

> An aside from the performance issues, I also can't see vinyls/logos when in the designer.. and a cursory duckduck showed no widespread complaints of this so I'm thinking it's linux based? Any ideas?
> 
> <img alt="Image" width="2000" height="1082" src="https://private-user-images.githubusercontent.com/1577654/593737067-fdfe435e-352a-4344-9853-b484347a49d2.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzkwOTMyODcsIm5iZiI6MTc3OTA5Mjk4NywicGF0aCI6Ii8xNTc3NjU0LzU5MzczNzA2Ny1mZGZlNDM1ZS0zNTJhLTQzNDQtOTg1My1iNDg0MzQ3YTQ5ZDIucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUxOCUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MThUMDgyOTQ3WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9YTg4MmIxOTBhZTJhYTk4YWQ2MmQ3YWI5Njg1MzM2ZGZkYjhkNzZiOWI3YmYyNmQ4MjgzZGM3YTQxOTFiZDBmOCZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.EOU9-o5ZAS8J_DAS5i9_wQhlRuXG-tIyfo8Xx4UHDXY">

Yes, i have the exact same issues, nothing found to fix it yet. Livery building works fine otherwise it seems

## Comment 4476328231

other (NONE) · fbt · 2026-05-18T09:33:19Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4476328231

The crash has been acknowledged as a driver problem on nvidia: https://forums.developer.nvidia.com/t/595-release-feedback-discussion/362561/433

## Comment 4476351222

other (NONE) · ben-mcginty · 2026-05-18T09:36:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4476351222

That's fantastic news that they have identified the root cause of the problem!

> Thank you and everyone else who reported the crash with Forza Horizon 6. We have root caused the issue and will ship a fix in an upcoming driver release. The bug for tracking this issue is 6181953.

## Comment 4476613080

other (NONE) · craimasjien · 2026-05-18T10:10:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4476613080

> The crash has been acknowledged as a driver problem: https://forums.developer.nvidia.com/t/595-release-feedback-discussion/362561/433

I am very curious to see what they found as being caused by the Nvidia driver, since on AMD the issues are the exact same.

## Comment 4476628503

other (NONE) · 0x8008 · 2026-05-18T10:12:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4476628503

...and yet the game is borderline unplayable on AMD+AMD in my case at the moment? I switched to Windows just to test and I not only can play the game fine, but also using way higher settings. Not looking good

## Comment 4477137907

other (NONE) · CRKrJ4K · 2026-05-18T11:20:39Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4477137907

> ...and yet the game is borderline unplayable on AMD+AMD in my case at the moment? I switched to Windows just to test and I not only can play the game fine, but also using way higher settings. Not looking good

Try with these: `VKD3D_CONFIG=no_upload_hvv,single_queue PROTON_VKD3D_HEAP=1 %command%`

Then set texture quality to Low. For me it made it, not perfect, but at least playable as it reduce the slow downs significantly.

PC: 14900KS, 7900 XTX, Proton: 20260506-cachyos

## Comment 4480577858

other (NONE) · sub0x0ne · 2026-05-18T18:16:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4480577858

> ...and yet the game is borderline unplayable on AMD+AMD in my case at the moment? I switched to Windows just to test and I not only can play the game fine, but also using way higher settings. Not looking good

No? I have 5800X3D + 7900XT on Bazzite latest. Played all weekend on Ultra preset @ 4K + FSR Quality, locked 60 fps, v-sync off.

Just have to start the game in desktop mode to avoid resolution bugging out.


## Comment 4482259481

other (NONE) · pbellchambers · 2026-05-18T21:12:15Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4482259481

I see there's a new proton hotfix version (I assume the `hotfix-20260518-fh6` in the version file means it's for this game), anyone know what it's supposed to fix? (ray tracing still seems to cause an instant crash)

## Comment 4482274483

other (NONE) · RSXEnthusiast · 2026-05-18T21:14:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4482274483

> I see there's a new proton hotfix version (I assume the `hotfix-20260518-fh6` in the version file means it's for this game), anyone know what it's supposed to fix? (ray tracing still seems to cause an instant crash)

Just tested, it seems to fix the black screen issue that's resolved by tabbing out and back into the game.

## Comment 4485726899

reporter (NONE) · luneko · 2026-05-19T08:12:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4485726899

> > I see there's a new proton hotfix version (I assume the `hotfix-20260518-fh6` in the version file means it's for this game), anyone know what it's supposed to fix? (ray tracing still seems to cause an instant crash)
> 
> Just tested, it seems to fix the black screen issue that's resolved by tabbing out and back into the game.

Black screen issue was fixed already a few days ago with normal Proton Bleeding-Edge. Hotfix might be related to this https://github.com/HansKristian-Work/vkd3d-proton/pull/3033

## Comment 4486405305

other (NONE) · vialolis · 2026-05-19T09:33:47Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4486405305

Pre shader cache turned off
Idk but without proton_log I get no responding game in start loading screen.
Proton 11.0
`PROTON_LOG=0 PROTON_ENABLE_WAYLAND=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%`

It's very unstable, so it can work and not. But right now I have some stable working but still crashing while playing with error FHC00

Fedora Linux KDE Plasma Wayland
Kernel: 7.0.5-cachyos1.fc44.x86_64
Ryzen 5 5600
RTX 3080 10GB
Driver Version: 595.71.05

## Comment 4486928582

other (NONE) · gomander · 2026-05-19T10:41:50Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4486928582

I'm trying to run the game on a 7800X3D, RTX 4090 system running CachyOS (7.0.9), using the latest Cachy Proton SLR and `VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_VKD3D_HEAP=1 %command%`. Game is installed on an NVMe SSD. Ray-tracing off, of course. Other graphics options don't seem to matter, including environment texture quality.

This is the best setup I've found so far, and allows me to load into the game and begin gameplay semi-reliably. The game runs really smooth. The problem is that the game consistently crashes within 5 minutes of driving. I can make it into Tokyo city ~60% of the time, but going anywhere else more or less instantly crashes the game with the standard FHC00 "Video Card Crash" error.

Something that also bothers me is that this game doesn't seem to play nice with niri. The game window is just black, and the game instead renders inside my Steam client's window. It can't be individually moved or fullscreened. So I'm stuck with the game only taking up a quarter of my actual screen.

I've tried many other combinations of launch options and Proton versions, but have yet to find anything that helps with these crashes or windowing issues. GE Proton has the lurching game speed issue, the latest Proton Hotfix seems to work equally well as Cachy Proton.

## Comment 4487024633

other (NONE) · ol1fer · 2026-05-19T10:53:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4487024633

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4486928582

are you using raytracing? try the highest settings preset with rt off

## Comment 4487089324

other (NONE) · gomander · 2026-05-19T11:02:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4487089324

> are you using raytracing? try the highest settings preset with rt off

Nope, the game always crashes in the loading screen before reaching gameplay with ray-tracing on. This is a crash after reaching gameplay, anywhere from instantly to ~5 minutes into driving. Seems to depend on where I drive. Tokyo city seems relatively stable, but as soon as I try to go anywhere else, it crashes. I've tried to do the Tokyo Day Trip Daikoku mission something like 10 times, and I've only ever managed to complete the first leg once.

## Comment 4487179239

other (NONE) · AnhNhan · 2026-05-19T11:14:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4487179239

> Something that also bothers me is that this game doesn't seem to play nice with niri. The game window is just black, and the game instead renders inside my Steam client's window. It can't be individually moved or fullscreened. So I'm stuck with the game only taking up a quarter of my actual screen.

@gomander see https://github.com/Supreeeme/xwayland-satellite/issues/392

I didn't try the gamescope arg yet. I'd tried running the game via GNOME instead of niri and it worked for me. Haven't played since discovering that thread yet.

## Comment 4487429589

other (NONE) · gomander · 2026-05-19T11:50:14Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4487429589

@AnhNhan wow, thanks for finding this! Running the game through gamescope did indeed work to run the game in fullscreen. So then it's a bug in xwayland-satellite, I guess. Running the game in gamescope had the humourous side-effect of making the crash report window appear in fullscreen as well.

## Comment 4489330915

other (NONE) · ccalhoun1999 · 2026-05-19T15:27:34Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4489330915

There are a few bugs related to this game and xwayland-satellite, I found PROTON_ENABLE_WAYLAND=1 helps avoid some of them on proton-ge (like it spawning inside the steam window rather than as its own window)

## Comment 4489850249

maintainer (MEMBER) · kisak-valve · 2026-05-19T16:28:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4489850249

Forza Horizon 6 Black screen with audio on SteamOS 3.9 Stable

Issue transferred from https://github.com/ValveSoftware/SteamOS/issues/2424.
@NicoGIT74 posted on 2026-05-16T17:22:10:

#### Your system information

* Steam client version: 1778281814
* SteamOS version: 3.9 (Build 20260511.1000)
* Opted into Steam client beta?: [Yes/No] Yes
* Opted into SteamOS beta?: [Yes/No] Yes
* Have you checked for updates in Settings > System?: [Yes/No] Yes

#### Please describe your issue in as much detail as possible:

When booting Forza Horizon 6 (Premium Edition Early Access), the game is booting with no image (Black screen) when in fullscreen mode and this in both desktop or gaming mode. The only way to fix the issue is to boot the game in desktop mode and to alt-tab 2x or alt-enter (windowed) once (But gives bad resolution).

Issue is present on custom build (9800x3d + 9070xt) and is also present on Steam Deck with the same SteamOS 3.9 build/version and channels (Main + Steam Deck stable). Fix is also working the same way on Steam Deck, but gaming mode require custom button mapping (R3/R4) to alt-enter (Which again gives bad resolution but actually displays something)

#### Steps for reproducing this issue:

1. Install and boot Forza Horizon 6 normally, then problem is immediately present.
2. Problem is also present even with ajusted graphics settings after temporary fix
***
@NicoGIT74 commented on 2026-05-16T17:23:28:

Please note like said in the title that audio is working correctly in background on both platform at any time, so no game freeze.

Also, issue is not present on SteamOS 3.7.24 for Steam Deck stable
***
@MadaoDev commented on 2026-05-19T01:24:45:

I got you brother this fixed it for me. When you enter the game, press alt + Enter when you can hear the sound. This should fix the issue. Fixes it both for SteamOS for Legion GO 2 and my steammdeck (for handhelds map 2 back buttons to do it once and then no need to redo it)

## Comment 4489878984

maintainer (MEMBER) · kisak-valve · 2026-05-19T16:32:13Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4489878984

Hello @NicoGIT74, please test how the game behaves with the bleeding edge beta of Proton Experimental (https://github.com/ValveSoftware/Proton/wiki/Proton-Versions#proton-bleeding-edge).

## Comment 4490035363

other (NONE) · RPINerd · 2026-05-19T16:50:45Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4490035363

> Livery building works fine otherwise it seems

That's the weird part, you can place the liveries on the car just fine, all the scaling/skewing/coloring etc. works as normal, its like the thumbnails are just not in the right location somehow..

I also noticed that after you try and apply one at random, its' thumbnail is then present but the other 1 or 2 that were previously visible dissapear

## Comment 4490686088

other (NONE) · LiamGingsjo · 2026-05-19T18:13:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4490686088

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4486405305

I was able to get Horizon 6 working almost perfectly for multiple hours with Proton on an nvidia 3060 with Proton Experimental by modifying it a bit, I used 

"PROTON_MEDIA_USE_GST=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%"

and in the files of Proton Experimental, I replaced ./files/lib/wine/vkd3d-proton/(i386 for x86 and x86_64 for x64)/d3d12.dll,d3d12core.dll, with those from this workflow run of vkd3d
https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/26098606335

## Comment 4491252488

other (NONE) · ofujiiro · 2026-05-19T19:23:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4491252488

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4490686088

Hi Liam,
could you share your other settings ? i'm running a 3070 with 550.163.01 drivers and with your exact fix it doesn't seem to work (crashes after 15 seconds of gameplay)
Best!

## Comment 4491318482

other (NONE) · LiamGingsjo · 2026-05-19T19:31:37Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4491318482

> Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4491252488)

I'm using 595.71.05 on Fedora 44, game set to High preset, make sure steam doesn't verify or update experimental

## Comment 4491340502

other (NONE) · Nisio110 · 2026-05-19T19:34:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4491340502

I've also been trying it (I'm on fedora 43 with an RTX 3060) to no avail. The furthest I've managed to get in the intro sequence before a crash has been with GE-Proton10-34 if that means anything. (I'm able to get to just after the Shinkansen part)

## Comment 4491562456

other (NONE) · AnejMajnik · 2026-05-19T20:02:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4491562456

I get the game booting in steam client, but if i close steam as soon as it says "running" i can bypass that.. I am using rx 9070 xt, and except for the stuttering/rubberbanding (which changing graphics settings or capping fps doesnt solve) it runs fine.. And yeah also RT crashes the whole game, but i dont use it anyway.. Someone tag me when a fix for stuttering/rubberbanding is found please <3

## Comment 4492212219

other (NONE) · matejss · 2026-05-19T21:29:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492212219

I can confirm terrible performance on 9070 (non XT), 5700x3D and 32GB of 3600Mhz ram on Fedora 44 KDE with Mesa 26.0.6. On all low settings i get somewhat stable 60fps. High / Ultra / Extreme settings (non RT) are terrible and give me 25-35fps.
Interestingly enough, my GPU is pretty much on constant 99% usage with only 120-150W power draw (where max is 220W). 
This issue happens exclusively in Forza Horizon 6.
There is also stuttering from time to time when driving.

## Comment 4492270343

other (NONE) · PolygonError · 2026-05-19T21:37:57Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492270343

running with Proton Hotfix, had to press alt enter once I heard the intros finish otherwise it was just a black screen.
massive stuttering when driving through the world with settings set to Extreme, when set to High stuttering was lessened quite a bit.
turning on ray tracing causes instant crash
unfortunately steam overlay still causing framedrop issues after 20-40 minutes due to ~~https://github.com/ValveSoftware/steam-for-linux/issues/11446~~ https://github.com/ValveSoftware/gamescope/issues/163, but unloading the steam overlay causes steam input to stop working and my PS5 controller is not recognized by the game.
otherwise playable

OS: Artix Linux
WM: KDE Plasma 6.6.5
GPU: AMD Radeon RX 9070 XT
CPU: AMD Ryzen 7 5700X3D
Video driver version: mesa 26.0.6-1
Kernel version: Linux 7.0.5-zen1-1-zen
RAM: 64GB DDR4 3200Mhz

`VKD3D_CONFIG=no_upload_hvv,single_queue PROTON_VKD3D_HEAP=1 gamescope -b -H 1440 -r 360 --force-grab-cursor --mangoapp -- %command%`

## Comment 4492815812

other (NONE) · yamborghinifly · 2026-05-19T23:02:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492815812

> > This is what I'm experiencing too broadly speaking. I have observed that GPU usage spikes, and then crashes to 0 as the application becomes unresponsive and then has to be killed, or wait for its crash reporter to kick in.
> 
> This is identical behavior to my experiences.

Almost agreed 
Currently I can't get even past the intro mission - not even on low settings. 
Crash logger tells me that my GPU driver has been killed. 

Using Proton Experimental with NVIDIA 2080Ti (595.71.05) and AMD Ryzen 5 7600X3D on Linux 7.0.3-1-MANJARO with Cosmic. 

EDIT: 
I also tried GE Proton10-4 - the game doesn't even start with this. 

Launch options:
VKD3D_CONFIG=descriptor_heap,enable_experimental_features PROTON_VKD3D_HEAP=1 %command% gamescope -W 2560 -H 1440 -r 165 --hdr-enabled --hdr-itm-enable --adaptive-sync -f --force-grab-cursor --steam -- %command%

## Comment 4492933602

other (NONE) · vultux · 2026-05-19T23:16:09Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492933602

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492815812

Hi,

Try with this variable:

VKD3D_CONFIG="descriptor_heap,pipeline_cache_control,single_queue"

With *`single_queue`* I was able to play for a few minutes and even hours. It's not ideal because it worsens performance, but it helped, at least until a correction comes out.

_If it doesn't work, try running the game without any startup strings, until you reach the Festival and you can get the first save._

## Comment 4493132510

other (NONE) · akeru-8 · 2026-05-19T23:45:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4493132510

Logitech G920 - erratic FFB and self-steering on Linux (CachyOS / proton-cachyos-slr)
System: CachyOS (Arch Linux), kernel 7.0.9, AMD RX 7900 XTX, proton-cachyos-slr 11.0.20260506. Wheel: Logitech G920 (USB ID 046d:c262), detected by the game, firmware up to date (verified on Windows).
The wheel is completely unusable. As soon as a save is loaded, it starts turning by itself (both while driving and while sitting in menus) sometimes slowly, sometimes with full force. The FFB is all over the place: it randomly cuts out, comes back, and switches between near-zero and violent forces within fractions of a second. There's also a noticeable lag between what the car is doing and what the wheel actually does. None of this changes with in-game FFB settings.
The wheel works fine in other games on the same setup: ETS2, BeamNG, Dirt Rally 2.0, Automobilista 2, The Crew Motorfest.
Worth noting: Playground Games officially requires Logitech G HUB for G920/G29 support, and G HUB doesn't exist on Linux. That's probably not unrelated.

## Comment 4493177748

other (NONE) · yamborghinifly · 2026-05-19T23:52:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4493177748

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492933602

single_queue did work - thanks a bunch! Though true - it worsens performance. I'll upload a benchmark when needed.

## Comment 4493880351

other (NONE) · Nition · 2026-05-20T02:08:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4493880351

Using an old wired XBox 360 controller here, but yes it's fine.

## Comment 4494762478

other (NONE) · Wolfhound905 · 2026-05-20T05:20:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4494762478

Using latest bleeding edge experimental, getting freezing during tutorial. I did the benchmark and that seemed to get all the way to the end before crashing. I get Video Card Crash error. 

https://github.com/user-attachments/assets/e5d1d605-7d33-4144-b2ee-9829744060fc

<img width="500" height="200" alt="Image" src="https://github.com/user-attachments/assets/16f07d5e-a0ee-46aa-bc37-986781c22507" /> 

<img width="200" height="90" alt="Image" src="https://github.com/user-attachments/assets/c67579eb-a42c-48d7-8ecd-dd68a606d971" />

## Comment 4495012960

other (NONE) · guff0 · 2026-05-20T06:02:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4495012960

Does anyone have controller issues? For me it keeps displaying after some time  “Controller disconnected” but the controller works outside of the game. The annoying thing is that the game needs a full restart to detect the controller again.
The issue appears regardless of connection method (wired on usb 2.0, wired on usb 3.0, Bluetooth). I have an Xbox series S/X controller.

Tried but did not work:
- switched between xpad and xone
- switched between steam input on and off
- tried proton experimental & Hotfix
- updated controller firmware
- disabled usb auto suspend

Partial proton logs:

grep -iE "xinput|plug|joy|disconnect|error" ~/steam-2483190.log
4388.633:0074:0078:trace:loaddll:build_module Loaded L"C:\\windows\\system32\\plugplay.exe" at 0000000140000000: builtin
4389.006:0090:00b4:trace:loaddll:build_module Loaded L"C:\\windows\\system32\\drivers\\winexinput.sys" at 00006FFFFE6D0000: builtin
4389.007:0090:00b4:fixme:xinput:pdo_pnp code 0xc, not implemented!
4389.008:0090:00b4:fixme:xinput:pdo_pnp code 0xc, not implemented!
4389.363:0148:014c:trace:loaddll:build_module Loaded L"C:\\windows\\system32\\XINPUT1_3.dll" at 00006FFFFC9F0000: builtin
4389.460:0128:012c:trace:loaddll:build_module Loaded L"C:\\windows\\system32\\XInput1_4.dll" at 00006FFFF68C0000: builtin
4389.461:0128:015c:warn:threadname:NtSetInformationThread Thread renamed to L"SDL_joystick"
4389.461:0128:015c:warn:threadname:dispatch_exception Thread renamed to "SDL_joystick"
4389.470:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage 000c:0001 not implemented!
4389.470:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage 0001:0080 not implemented!
4389.470:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ffbc:0088 not implemented!
4389.470:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ff00:0001 not implemented!
4389.470:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ff00:0002 not implemented!
4389.471:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ff00:0004 not implemented!
4389.471:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage 000c:0001 not implemented!
4389.471:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ff00:0001 not implemented!
4389.471:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ff00:0002 not implemented!
4389.471:0128:012c:fixme:dinput:hid_joystick_device_try_open device usage ff00:0004 not implemented!
4389.473:0128:0168:warn:threadname:NtSetInformationThread Thread renamed to L"wine_xinput_hid_update"
4389.758:0128:012c:fixme:xinput:XInputGetBatteryInformation index 0, type 0, battery 000000000010F028.
4390.738:0148:01a8:warn:seh:OutputDebugStringA "Runtime Service struct SErrorImpl Created\n"
4390.738:0148:01a8:warn:seh:dispatch_exception "Runtime Service struct SErrorImpl Created\n"
4402.294:0148:01a8:warn:vkd3d-proton:d3d12core_GetDebugInterface: Returning DXGI_ERROR_SDK_COMPONENT_MISSING.
Fossilize WARN:  ... warning spam detected at fossilize_errors.hpp:163, silencing.
4403.298:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage 000c:0001 not implemented!
4403.298:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage 0001:0080 not implemented!
4403.298:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ffbc:0088 not implemented!
4403.299:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ff00:0001 not implemented!
4403.299:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ff00:0002 not implemented!
4403.300:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ff00:0004 not implemented!
4403.300:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage 000c:0001 not implemented!
4403.300:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ff00:0001 not implemented!
4403.300:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ff00:0002 not implemented!
4403.300:0148:0308:fixme:dinput:hid_joystick_device_try_open device usage ff00:0004 not implemented!
.
.
4415.909:0148:035c:warn:threadname:NtSetInformationThread Thread renamed to L"wine_xinput_hid_update"

## Comment 4495070167

other (NONE) · AnejMajnik · 2026-05-20T06:09:26Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4495070167

I got no issues with my PS5 controller bluetooth, although I do need to use steam input

## Comment 4495334650

other (NONE) · DotFlav · 2026-05-20T06:38:30Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4495334650

Did anyone manage to run the game with Ray Tracing? 

I've tried like every Proton version and launch command imaginable, though I assume this has to be fixed on the GPU driver level?

## Comment 4496966741

other (NONE) · drkhac · 2026-05-20T09:48:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4496966741

> Does anyone have controller issues? For me it keeps displaying after some time  “Controller disconnected” but the controller works outside of the game. The annoying thing is that the game needs a full restart to detect the controller again.
> The issue appears regardless of connection method (wired on usb 2.0, wired on usb 3.0, Bluetooth). I have an Xbox series S/X controller.
> 
I have an 8BiT DO xbox controller works fine, I went into steam big picture mode(BPM) and set it one time in BPM and it always connects and works fine. It is both wired and wireless.

## Comment 4497245212

other (NONE) · LordDaveTheKind · 2026-05-20T10:12:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4497245212

> Did anyone manage to run the game with Ray Tracing?

I was able to do it with (and I quote) ["the horrible workarounds"](https://github.com/HansKristian-Work/vkd3d-proton/pull/3033) on AMD hardware (Radeon RX 9070XT).

Best notes on how to build mesa-git from source are here: https://gist.github.com/Venemo/a9483106565df3a83fc67a411191edbd.



## Comment 4498127676

other (NONE) · mitchellurgero · 2026-05-20T11:56:12Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4498127676

If you're getting the freezing bug in tutorial on nvidia just lock FPS to anything under 75.

## Comment 4498513724

other (NONE) · Wingdom · 2026-05-20T12:44:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4498513724

Edit: I found my solution, disabling hidraw. Open protontricks, select the default wine prefix for FH6, run a wine cmd shell, open the control panel by running control.exe, open game controllers, then under Advanced Settings at the bottom, check the box for Enable SDL and check the box for Disable hidraw. I still don't really know why this is necessary for FH6, but not for other games using the same proton versions.

> Trying to debug my controller not working has been a learning experience, but hasn't actually fixed anything for me.
> 
> System: Bazzite 44 (Fedora-based, system Steam), KDE Plasma 6.6.4, kernel 6.19.14, Ryzen 7 5700X, Radeon RX 9060 XT
> Proton versions tested: Proton Hotfix, Proton Experimental, GE-Proton 10-34, CachyOS Proton
> Controllers tested: Xbox controller (the current one with usb-c), Steam Controller - Both work in Steam Big Picture and in other Proton games, but no controller prompt appears at any point in FH6
> 
> Logs from `WINEDEBUG=+wgi,+xinput,+hid PROTON_LOG=1`:
> The HID layer correctly detects and registers the Steam virtual gamepad:
> ```
> lnxev_device_create dev ..., node "/dev/input/event256", desc {vid 28de, pid 11ff, ..., is_gamepad 1, ...}
> bus_create_hid_device desc {vid 28de, pid 11ff, ..., is_gamepad 1, ...}
> ```
> XInput correctly picks it up, creates child PDOs, and the game polls it in a loop:
> ```
> add_device device_id L"WINEXINPUT\\VID_28DE&PID_11FF&MI_00"
> create_child_pdos ... gamepad device / xinput device
> XInputGetCapabilitiesEx unk 1, index 0-3 ...
> XInputGetState index 0-3 ... (continuous polling)
> ```
> However, the entire WGI output is only these two lines:
> ```
> fixme:combase:RoGetActivationFactory (L"Windows.Gaming.Input.Gamepad", ...): semi-stub
> fixme:combase:RoGetActivationFactory (L"Windows.Gaming.Input.RawGameController", ...): semi-stub
> ```
> No device enumeration occurs in WGI. The `wine_wginput_worker` thread starts, but `Gamepads()` / `RawGameControllers()` return empty — the stub does not bridge to the HID-detected gamepad despite it being present and correctly flagged is_gamepad 1.
> 
> Wine's implementation of WGI doesn't find any controllers and returns an empty list, so FH6 stays in keyboard/mouse mode. This happens even though the controller is correctly detected at every other level of the stack — it seems like the bug is Wine's WGI doesn't see devices that are already known to Wine's own HID and XInput layers. No Steam Input configuration or launch options is fixing this for me.

## Comment 4501151529

other (NONE) · Robozone05 · 2026-05-20T18:00:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4501151529

Operating System: CachyOS Linux 
KDE Plasma Version: 6.6.5
KDE Frameworks Version: 6.26.0
Qt Version: 6.11.1
Kernel Version: 7.0.9-1-cachyos (64-bit)
Graphics Platform: Wayland
Processors: 16 × AMD Ryzen 7 9800X3D 8-Core Processor
Memory: 32 GiB of RAM (30,7 GiB usable)
Graphics Processor: AMD Radeon RX 9070 XT
Manufacturer: Micro-Star International Co., Ltd.
Product Name: MS-7E51
System Version: 1.0

I have the same problem with stutters. I tried a bunch of fixes but nothing works. I think its a driver problem (maybe). 
I can say that i have between 130 and 160 fps on Extreme and 1440p resolution. Also if i activate RT the game is crashing instantly.

The rest of my games are working like a charm. One of them is Dune Awakening.

## Comment 4502867463

other (NONE) · ZenithFluff · 2026-05-20T21:39:57Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4502867463

I have my fps locked to 60 and ray tracing off and i tried cachyos verison of proton and i tried launch settings and it still gives me the gpu crash error Idk what to do

## Comment 4502872221

other (NONE) · matejss · 2026-05-20T21:40:44Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4502872221

> I can confirm terrible performance on 9070 (non XT), 5700x3D and 32GB of 3600Mhz ram on Fedora 44 KDE with Mesa 26.0.6. On all low settings i get somewhat stable 60fps. High / Ultra / Extreme settings (non RT) are terrible and give me 25-35fps.
Interestingly enough, my GPU is pretty much on constant 99% usage with only 120-150W power draw (where max is 220W).
This issue happens exclusively in Forza Horizon 6.
There is also stuttering from time to time when driving.

I have discovered, that major FPS drop is caused by car reflections (non RT ones). By turning them off it dropped my GPU usage on ultra settings from constant 99% on 60fps lock to waving 70-90%. Its still underperforming to what this GPU is capable off, but at least now its playable.

## Comment 4502888814

other (NONE) · luluco250 · 2026-05-20T21:43:37Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4502888814

I don't even get stutters per se, but rather it feels like the game has frame pacing issues. Like, it's smooth but frames get delivered inconsistently, with vsync on or off, capped at 60, 120 or even uncapped FPS.

If I put it on the low preset it seems to improve. In particular I found that increasing the environment textures setting introduces the pacing issues, which is odd because the game reports I have plenty of vram even for the "Extreme" texture preset, but anything above low presents issues.

Maybe there's some sort of bottleneck with texture streaming?

Resolution does not seem to matter, I get the same frame pacing issues at 3840x1080 fullscreen or 1600x900 windowed. Upscaling doesn't help either. Again, lowering textures had an impact for me, but the game looks pretty horrible on the "Low" setting so fixing this would be nice.

I have basically no issues running other games other than the occasional Unity game with bottlenecked scripts. BeamNG.drive runs extremely well with the native port.

I haven't tried using Proton-GE and my default is Proton Experimental on Steam.
One bug I have is if I don't enable Steam Input the game fails to recognize controllers which are connected while it's running. So a pre-connected controller is fine, but connecting one during it or if it reconnects it doesn't get picked up anymore until restarting the game.

Update: I can have everything on Ultra and only need to turn down textures to Low and suddenly my frame pacing issues are severely reduced, though they still occur occasionally.

I should mention that the game only reports 12.6GB of VRAM even though my GPU has 16GB.

Update 2: Sometimes the game seems to get stuck at 30 FPS regardless of settings, but changing resolutions/full screen/windowed seems to fix this. Not sure if a game bug or a Linux/Wine/Proton bug.

<details>
<summary>
PC specs
</summary>
Arch Linux with CachyOS V3 repos.

AMD Ryzen 5900XT

32GB DDR4 and Swap on PCIe 4x4

AMD Radeon 6800XT 16GB

Game is installed on a PCIe 4x4 non-root drive with BTRFS, root drive is PCIe 3x4 EXT4.

KDE Plasma 6.6.4 on Wayland

Linux-Zen 7.0.2
</details>

## Comment 4503101161

other (NONE) · guff0 · 2026-05-20T22:21:28Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4503101161

Managed to fix my issue by removing PROTON_ENABLE_HIDRAW=1 from the launch options.

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4495012960


## Comment 4505523939

other (NONE) · TheNumerus · 2026-05-21T06:51:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4505523939

Adding my data point here. After some 14 hours in game I got 4 crashes. One crash after a race loading screen (with proper error box, I don't remember the exact error unfortunately ), two freezes in the middle of online race (visuals froze, but music continued) and one case where the game just vanished without any error box. The whole time I have the weird "simulation slowdowns", but that may be a game or AMD issue, since my friend with the same GPU has them in Windows too. 

I'm using proton hotfix the whole time (not sure which exact version). One major issue with the game is that after launch, in 4/5 cases, the audio just stops when transitioning from intro movies to main menu. There are occasional crackles, but no proper sound. 

Otherwise I'm playing on extreme preset without RT, with framerates between 40-80 depending on region. HDR in gamescope works flawlessly. I'm playing with Xbox gamepad (Series generation) through USB cable without any issues.

GPU: AMD RX 7900 XT
CPU: AMD Ryzen 5950X
RAM: 64 GB
Mesa version: 26.0.6-arch1.1
Distro: EndeavourOS
Kernel: 7.0.8-arch1-1
KDE version: 6.6.5
Launch parameters: `gamescope --hdr-enabled -f -W 2560 -H 1440 -- %command%`

## Comment 4505540060

other (NONE) · mrtonguelicker · 2026-05-21T06:54:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4505540060

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4505523939

Set environment textures and geometry detail to low, they’ll help tremendously with the “simulation slowdowns” 

## Comment 4509034009

other (NONE) · Killer-9000 · 2026-05-21T14:03:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4509034009

I haven't seen anyone else mention it here, but the stuttering only happens at high gpu usage for me, locking it to 60 fps with slightly lower settings, so the usage remains around 50/60%, the game rarely stutters during normal gameplay.

GPU: AMD Radeon RX 9070 XT
Video driver version: 26.0.6-arch1.1
Kernel version: 7.0.5-arch1-1
Proton version: Experimental, Bleeding Edge
Launch options: PROTON_ENABLE_WAYLAND=1 PROTON_ENABLE_HDR=1 DXVK_HDR=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=no_upload_hvv,single_queue PROTON_SET_GAME_DRIVE=1 WINEDLLOVERRIDES="winmm=n,b;steam_api64=n,b;steamclient64=n,b;version=n,b" %command%

Extreme:
<img width="1171" height="750" alt="Image" src="https://github.com/user-attachments/assets/8468f31d-7cb8-4efe-92ef-ebdf92b7a948" />

Extreme, Low Enviroment Texture Quality, High Enviroment Geometry Quality:
<img width="1176" height="750" alt="Image" src="https://github.com/user-attachments/assets/1bc6854c-9eb3-4f0f-8e86-6961ca09655f" />

## Comment 4509355624

other (NONE) · AnejMajnik · 2026-05-21T14:40:40Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4509355624

Update, for me the combination of new mesa (26.1.1), new proton hotfix and setting world textures and geometry to low while keeping the rest at ultra has more or less resolved stuttering.. Feels bad having it on low with rx 9070 xt, but it is what it is..

## Comment 4512074104

reporter (NONE) · luneko · 2026-05-21T19:27:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4512074104

Game is enjoyable for me on 9070 XT using the current bleeding-edge proton, locking fps to 60 and using extreme preset with environment textures set to low, no RT. Some microstutters still exist, especially when going fast.
Still hope we can make some new discoveries to fix the issue as a whole and enjoy the game on max fidelity as it was already an issue in FH5 also.

Thanks to anyone that conrtibuted so far!

## Comment 4512125921

other (NONE) · jefmes · 2026-05-21T19:35:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4512125921

Adding my 2 cents, game is running well enough on a 9070 XT w/ Ryzen 9800X3D, but RT is still causing crashes at any setting. Running latest Proton-CachyOS-SLR as of 5/21/2026 with the following variables set in Steam:

PROTON_FSR4_UPGRADE=1 PROTON_ENABLE_WAYLAND=1 DXVK_HDR=1 %command%

<img width="2403" height="1315" alt="Image" src="https://github.com/user-attachments/assets/c38e6811-a7b1-4342-ab88-f7d766bb3271" />

## Comment 4514860594

other (NONE) · mitchellurgero · 2026-05-22T03:57:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4514860594

Not sure if anyone else has seen this but I just got the infamous "FHE01" crash error come up BUT my game is still playable.

## Comment 4516395152

other (NONE) · Psykatte · 2026-05-22T07:29:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4516395152

I was getting FHC00 crashes after seconds of gameplay, I reduced the crashes by dropping to low settings, 720p, 20 fps; bumping this up to even 30 fps would drastically increase crashing.

Moving from bleeding edge experimental to proton-cachyos-11.0-20260506-slr didn't change this crashing.

Moving from proton-cachyos-11.0-20260506-slr to **proton-cachyos-11.0-20260429-slr**-x86_64_v3 has allowed me to play for 2hr on high settings whereas before I could only play a minute if lucky.

Perhaps inspecting the differences between proton-cachyos-11.0-20260429-slr and proton-cachyos-11.0-20260506-slr could shed light on the FHC00 crashes people are getting.

OS: CachyOS x86_64
Kernel: Linux 7.0.9-1-cachyos
DE: KDE Plasma 6.6.5
WM: KWin (Wayland)
CPU: AMD Ryzen 5 2600 (12) @ 3.40 GHz
GPU: NVIDIA GeForce RTX 2080 Ti Rev. A [Discrete]
Driver: 595.71.05-1
Memory: 31.24 GiB

## Comment 4517943366

other (NONE) · Ap-Cristian · 2026-05-22T10:39:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4517943366

Can confirm proton-cachyos-11.0-20260429+ fixes FHC00, there are micro stutters ocasionally but the game is very playable on ultra. Thank you @Psykatte.

OS: Arch x86_64
Kernel: 7.0.9-arch1-1
DE: Hyprland
WM: Hyprland (Wayland)
CPU: AMD Ryzen 7 8845HS (15)
GPU: NVIDIA GeForce RTX 4060 [Discrete]
Driver: 595.71.05-1
Memory: 14.9 GiB

## Comment 4519459467

other (NONE) · Izu-3 · 2026-05-22T14:11:19Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4519459467

Just throwing my hat in the ring that I'm also having major issues, the game seems to pause very frequently before lurching forward, something which worsens the longer my machine's been running (??). From what I can ascertain it's something to do with read issues from disk, because every spike comes with a drop in CPU/GPU usage and a very temporary high read from my SSD (which is being used exclusively on the game at the time). The game is stable in that it doesn't crash, but it's still unplayable no matter what settings, reducing texture/env detail to very low doesn't improve it. I also have the issue with none of the livery graphics showing in the menu making that impossible to use.

Tried multiple revisions of proton and none of them fix the issue; latest cachyOS proton breaks my audio completely.

OS: Garuda Linux x86_64
Kernel: 7.0.9-zen1-1-zen
DE: KDE Plasma 6.6.5
WM: KWin (Wayland)
CPU: AMD Ryzen 5 2600X (12) @ 3.60 GHz
GPU: AMD Radeon RX 9060 XT
Driver: Mesa 26.0.6-arch1.1
Memory: 31.28GB

## Comment 4520072219

other (NONE) · A402B · 2026-05-22T15:33:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520072219

> I tested out the above and it solved everything for me _with ray tracing disabled_ (nvidia 3080ti on ubuntu 26.04). Previously I was stuck with everything in very low settings and capped at 36fps to lower the frequency of crashes, now with that vkd3d patch I have everything set ultra with uncapped fps, no crashes at all after several hours, and almost no stuttering.
> 
> Still causing crashes:
> 
> * Ray tracing on
> * `Nvidia Reflex Low Latency`, if that's on then the game freezes on loading (doesn't even get to the main menu). I guess that must be a different issue?


Hi [pbellchambers](https://github.com/pbellchambers), could you please share your configuration of proton and commands? I'm on Ubuntu as well and I can't get past the tutorial without it crashing on very low settings. I would love to know what your solution is.

OS: Ubuntu 26.04
Proton version tested: Experimental, hotfix, Cachy-OS
NVIDIA: 3050
Ram: 16gb

## Comment 4520490051

other (NONE) · ccalhoun1999 · 2026-05-22T16:16:41Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520490051

I am also dealing with horrific lurching on a 9070xt on medium settings. The slower the car the better it is, but endgame S1+ spec races are pretty much unplayable even with medium settings.
edit: even on very low settings the lurching is bad.

## Comment 4520673074

reporter (NONE) · luneko · 2026-05-22T16:36:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520673074

> Adding my 2 cents, game is running well enough on a 9070 XT w/ Ryzen 9800X3D, but RT is still causing crashes at any setting. Running latest Proton-CachyOS-SLR as of 5/21/2026 with the following variables set in Steam:
> 
> PROTON_FSR4_UPGRADE=1 PROTON_ENABLE_WAYLAND=1 DXVK_HDR=1 %command%
> <img alt="Image" width="2000" height="1094" src="https://private-user-images.githubusercontent.com/5678101/596315852-c38e6811-a7b1-4342-ab88-f7d766bb3271.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzk0Njc4ODUsIm5iZiI6MTc3OTQ2NzU4NSwicGF0aCI6Ii81Njc4MTAxLzU5NjMxNTg1Mi1jMzhlNjgxMS1hN2IxLTQzNDItYWI4OC1mN2Q3NjZiYjMyNzEucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUyMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MjJUMTYzMzA1WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NWNiNDYyYmUwM2RlNGNkYzg5YmRjZTUyMzZiNmE1NzRkZDdmYTAyMzhjMWE5YjZmYTliN2MyNGRlMjg3Y2QzZSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.-65kZtEQOoPROSGiy38hk0Xl3gB4EPgl9C-4Q_Ovfww">

Do you not get frequent stutters and physics slowdowns? For me the game is unplayable with the same settings on my 9070XT. My CPU is a 5800X3D though, but it never was a bottleneck so far.

## Comment 4520867557

other (NONE) · mitchellurgero · 2026-05-22T16:56:12Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520867557

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520072219

Lock FPS to 30 or lower for the tutorial worked for me but it seems results may vary


## Comment 4521380205

other (NONE) · Killer-9000 · 2026-05-22T17:49:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521380205

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520673074

Just changed my stuff to his, and my stutters are gone. Before I was running proton experimental [bleeding edge]. I'll play for a bit, and see if I encounter any crashes, since I didn't with experimental.

PROTON_ENABLE_WAYLAND=1 DXVK_HDR=1 %command%
proton-cachyos-11.0-20260506-slr-x86_64_v3

<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/3924409f-0f47-42ee-b024-d2cebe4ca4da" />

Side note, oof look at my cpu framerate vs his, I should upgrade at some point, maybe when ddr5 comes down in price.

## Comment 4521429558

other (NONE) · jefmes · 2026-05-22T17:55:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521429558

Nothing significant enough to keep me from playing for two hours yesterday.
I'm usually pretty sensitive to microstutter so any that was there wasn't
bad at all. Interesting thought on the CPU difference, I wonder if it's
just exacerbated on the 5800X3D at this point.

On Fri, May 22, 2026, 9:36 AM Luneko ***@***.***> wrote:

> *luneko* left a comment (ValveSoftware/Proton#9789)
> <https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520673074>
>
> Adding my 2 cents, game is running well enough on a 9070 XT w/ Ryzen
> 9800X3D, but RT is still causing crashes at any setting. Running latest
> Proton-CachyOS-SLR as of 5/21/2026 with the following variables set in
> Steam:
>
> PROTON_FSR4_UPGRADE=1 PROTON_ENABLE_WAYLAND=1 DXVK_HDR=1 %command%
> [image: Image]
> <https://private-user-images.githubusercontent.com/5678101/596315852-c38e6811-a7b1-4342-ab88-f7d766bb3271.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Nzk0Njc4ODUsIm5iZiI6MTc3OTQ2NzU4NSwicGF0aCI6Ii81Njc4MTAxLzU5NjMxNTg1Mi1jMzhlNjgxMS1hN2IxLTQzNDItYWI4OC1mN2Q3NjZiYjMyNzEucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9QUtJQVZDT0RZTFNBNTNQUUs0WkElMkYyMDI2MDUyMiUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNjA1MjJUMTYzMzA1WiZYLUFtei1FeHBpcmVzPTMwMCZYLUFtei1TaWduYXR1cmU9NWNiNDYyYmUwM2RlNGNkYzg5YmRjZTUyMzZiNmE1NzRkZDdmYTAyMzhjMWE5YjZmYTliN2MyNGRlMjg3Y2QzZSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmcmVzcG9uc2UtY29udGVudC10eXBlPWltYWdlJTJGcG5nIn0.-65kZtEQOoPROSGiy38hk0Xl3gB4EPgl9C-4Q_Ovfww>
>
> Do you not get frequent stutters and physics slowdowns? For me the game is
> unplayable with the same settings on my 9070XT. My CPU is a 5800X3D though,
> but it never was a bottleneck so far.
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4520673074>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ABLKIFIQMIQFUZUEWVD3R6344B6Y3AVCNFSM6AAAAACY7A37LWVHI2DSMVQWIX3LMV43OSLTON2WKQ3PNVWWK3TUHM2DKMRQGY3TGMBXGQ>
> .
> You are receiving this because you commented.Message ID:
> ***@***.***>
>


## Comment 4521571918

reporter (NONE) · luneko · 2026-05-22T18:12:22Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521571918

<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/d16d6d40-8e9d-40b4-a6ce-9975cca67ed9" />
This is how it looks for me using latest Cachy Proton and the same settings (except HDR disabled) and the stutters are unbearable. What Distro, Kernel and Mesa are you guys running if I may ask?

## Comment 4521683838

other (NONE) · drkhac · 2026-05-22T18:24:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521683838

I'm running Bazzite on a Laptop with Nvidia 4050 and 32GB ram

## Comment 4521684877

other (NONE) · pbellchambers · 2026-05-22T18:24:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521684877

> Hi [pbellchambers](https://github.com/pbellchambers), could you please share your configuration of proton and commands? I'm on Ubuntu as well and I can't get past the tutorial without it crashing on very low settings. I would love to know what your solution is.
> 
> OS: Ubuntu 26.04 Proton version tested: Experimental, hotfix, Cachy-OS NVIDIA: 3050 Ram: 16gb

@A402B 

OS: Ubuntu 26.04
CPU: AMD Ryzen 7950X
GPU: Nvidia 3080ti
Driver: 595.71.05 (the default one from `apt install nvidia-driver-595`)
Proton: Experimental

Then replace the vkd3d-proton files in the proton experimental install directory (instructions from [this comment](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468002719)), change the <steam_library_location> part to wherever your steam library is located, and you'll need to repeat this whenever steam updates proton until that PR gets merged and included:

> download build for this PR https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/25965683046/artifacts/7034546231
> 
> And replace vkd3d libs by commands like this
> 

```
cp -vr Downloads/vkd3d-proton/x64/* <steam_library_location>/steamapps/common/Proton\ -\ Experimental/files/lib/wine/vkd3d-proton/x86_64-windows/
cp -vr Downloads/vkd3d-proton/x86/* <steam_library_location>/steamapps/common/Proton\ -\ Experimental/files/lib/wine/vkd3d-proton/i386-windows/
```

Finally...

Launch Options: `RADV_EXPERIMENTAL=heap radv_wait_for_vm_map_updates=true %command%`
Game Options: Ray tracing off, Nvidia Reflex Low Latency off, everything else whatever you want

Runs great after that, ~49 hours played, no crashing at all. I do get some occasional stuttering, but this seems to be the same as on windows. Turning down texture quality and car reflections seems to reduce it.


For reference, in-game settings and benchmark...
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/8bce827e-550d-4152-b4f7-41efd819e229" />

## Comment 4521906496

other (NONE) · Gotolei · 2026-05-22T18:54:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521906496

> An aside from the performance issues, I also can't see vinyls/logos when in the designer.. and a cursory duckduck showed no widespread complaints of this so I'm thinking it's linux based? Any ideas?
> [img]

I'm seeing the same on my end. In this screen (Any home/garage menu > Cars > Designs and paints > Apply designs and vinyls > Apply a vinyl shape/logo/mask shape) only a couple shapes ever show up. They're still there and can be selected and put on the car. Going back to the menu, whatever item was selected will now be the only one visible in the menu.

I'm not sure if this is related or not, but some materials/shaders? appear invisible in the world itself. In one case, some of the gradient effects behind the level counter in player nameplates show as transparent. I've also seen other instances of other things glitching out in gameplay along these same lines, but I don't have screenshots of them handy.

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/c3b0afb1-897c-40dd-8ace-f22004461913" />
<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/7b1d56b7-41df-48e7-a09e-477d1ec43f77" />

Proton Experimental 23289363, i5-10400f, RX-6600XT, EndeavourOS KDE X11

## Comment 4522207428

other (NONE) · matejss · 2026-05-22T19:41:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4522207428

I tried literally everything and that is basically the best framerate i can gain with this game (unless i also disable shadows completely, then i get +10fps. FSR only lifts fps by like 3-7fps, so there is something very bizarre going on. I did proton experimental bleeding edge, proton GE 10-34, Proton CachyOS, native wayland, xwayland, mesa 26.0.6, 26.1, git 26.1.1, vkd3d horizon fixes.
I no longer have any idea what can i do to gain more, playable FPS in this game. Person with same GPU can get 90fps on all extreme except terrain quality which is a known bug.
I also tried disabling rebar, but no success here either.

<img width="2559" height="1439" alt="Image" src="https://github.com/user-attachments/assets/99c79ab4-0488-49e6-b96f-697ef77ea22e" />

Proton_log spams insane amount of errors within minutes, so i assume its the source of the problem

`matejss@matejss:~$ tail -n 10000 steam-2483190.log | cut -c1-120 | sort | uniq -c | sort -rn | head -30
     33 23224.295:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     33 23224.295:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     33 23224.295:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     30 23224.269:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     29 23224.269:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     29 23224.269:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     26 23224.315:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     26 23224.315:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     26 23224.315:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     24 23224.295:0140:026c:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=000000014446
     21 23224.292:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     21 23224.292:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     21 23224.292:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     21 23224.288:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     21 23224.287:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     21 23224.286:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     21 23224.274:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     21 23224.274:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     21 23224.273:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     21 23224.272:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     21 23224.272:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     21 23224.269:0140:026c:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=000000014446
     20 23224.301:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     20 23224.301:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     20 23224.301:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     20 23224.300:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     20 23224.300:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
     20 23224.300:0140:026c:trace:seh:call_vectored_handlers calling handler at 000000014534B378 code=c000001d flags=0
     20 23224.289:0140:026c:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
     20 23224.289:0140:026c:trace:seh:call_vectored_handlers handler at 000000014534B378 returned ffffffff
matejss@matejss:~$ grep -c 'ILLEGAL_INSTRUCTION' steam-2483190.log
3520701
`

## Comment 4522793463

other (NONE) · CRKrJ4K · 2026-05-22T21:23:41Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4522793463

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4522207428

Have you tried setting the texture quality to low?

## Comment 4522873824

other (NONE) · matejss · 2026-05-22T21:39:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4522873824

> > Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4522207428)
> 
> Have you tried setting the texture quality to low?

Yes, as you can see on my benchmark it is on low. I have also tried setting geometry and car quality to low - did not help.
I went basically through EVERY possible setting, from resolution, to upscaling to every possible quality option one by one and analyzed the performance impact.
Highest impacts are:
1. Texture quality - known issue, having it on low on medium usually solves it
2. Car reflections - With many cars in the race having it above medium provides quite a performance loss, hence i have it on very low to have somehow playable FPS
3. Shadows. Difference between off -> low is big. 10FPS minimum. low -> extreme almost no difference at all, frankly extreme gives me 1-2fps more on average than low somehow

FSR:
Off -> Quality gives me about 5fps on average
Quality -> Ultra performance another 5-10. Something is definietly off here

i even tried switching resolution from 1440p to 1080p to see if somehow it has any effect - almost same performance and GPU usage.

My gpu is on constant 99% usage (unless i limit to 60fps then we are in 80s and 90s), max wattage at around 140-150W. VRAM sticks with 4-7GB usage, CPU at around 50% per core, Thermals in their 40s C. GPU clocks are properly utilized.

Raytracing obviously eats FPS or crashes, so its permanently off.

Most importantly it happens only in forza horizon 6. Diablo 4? Everything works perfectly, GPU is utilized and its also a DX12 game so VKD3D is used.
Benchmark? Proper utilization as well



## Comment 4523000705

other (NONE) · mitchellurgero · 2026-05-22T22:08:39Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4523000705

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4468002719

EDIT: the quote reply was removed by a moderator - you need to read the comment I replied to (see link above) to get the fix I mention below.

If anyone is reading this and you're on nvidia this also works! However your launch options should be instead:

`PROTON_ENABLE_WAYLAND=1 PROTON_HIDE_NVIDIA_GPU=0 PROTON_ENABLE_NVAPI=1 PROTON_USE_NTSYNC=0 PROTON_ENABLE_NVAPI=1 PROTON_ENABLE_NGX_UPDATER=1 PROTON_NVIDIA_LIBS=1 PROTON_VKD3D_HEAP=1  VKD3D_CONFIG=no_upload_hvv,single_queue WINEDLLOVERRIDES="winmm=n,b;steam_api64=n,b" %command%`

The example copy commands above are if you're using GE-Proton 10-34 only, you have to modify the paths if you're using a different version of proton!!!

## Comment 4523333156

other (NONE) · CRKrJ4K · 2026-05-22T23:27:24Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4523333156

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4522873824

Ah I see, apologies. I replied on mobile so I missed that.

I'm getting ~170W-190W GPU power draw @ 4k, 99% usage, and max quality (minus RT & texture) on my 7900 XTX. Either their engine is amazingly efficient or its not pulling enough power. I don't remember how much power FH5 pulled

For me, setting texture quality to low didn't completely take away the pausing/stutters, but it at least made it playable

## Comment 4524061799

other (NONE) · fbt · 2026-05-23T03:44:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4524061799

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4523000705

I was going to avoid adding noise, but this is getting a bit ridiculous.

I run a 3060Ti on Arch with X11. For me, the game works almost entirely fine, with some slowdowns on asset streaming (which is a famous problem of their engine anyway), with *ONE* option and *ANY* relatively fresh proton version, where vkd3d supports the flag:

```
VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%
```

This stops the crashing and all the egregious stuttering.
Obviously, the name of the flag implies that the feature is incomplete and/or broken in some way, but it seems to be sufficient to run Horizon 6.

Performance is better with Experimental or CachyOS protons, GE-34 stutters noticeably.

In my case I also add `no_upload_hvv` to VKD3D_CONFIG, as this seems to make my system behave better, as the mobo hasn't been updated to support resizable BAR.

FURTHERMORE, a lot of the options you've provided here are either not doing anything or just irrevant:

* `PROTON_HIDE_NVIDIA_GPU=0 PROTON_ENABLE_NVAPI=1 PROTON_ENABLE_NGX_UPDATER=1` this does nothing, it's the default with an nvidia card.
* `PROTON_NVIDIA_LIBS=1` this looks like a CachyOS-Proton feature, may actually be doing something. Unsure if it's present in a current version tho, can't find much on it.
* `WINEDLLOVERRIDES="winmm=n,b;steam_api64=n,b"` completely irrelevant here
* `PROTON_USE_NTSYNC=0` unsure why you'd disable ntsync, its performance is at least on par with fsync on a modern system
* `PROTON_VKD3D_HEAP` does nothing unless you're using a very specific CachyOS-Proton, and then it just enables `i_want_broken_descriptor_heap`.

UPD: Fun fact: `PROTON_ENABLE_NGX_UPDATER` is NOT a Proton flag. It's an NVIDIA one 🤷.
UPD1: This does not fix the decal menu nor issues with transparency on ghost cars, but these are nuisances at best.

## Comment 4524067081

other (NONE) · mitchellurgero · 2026-05-23T03:46:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4524067081

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4524061799

I just simply was posting what worked for my nvidia 3060ti, im sure there are a few env vars there that could be removed but it works for me and has been solid for hours for me. No stutters, no crashing.

## Comment 4524191190

other (NONE) · philpax · 2026-05-23T04:47:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4524191190

> I run a 3060Ti on Arch with X11. For me, the game works almost entirely fine, with some slowdowns on asset streaming (which is a famous problem of their engine anyway), with _ONE_ option and _ANY_ relatively fresh proton version, where vkd3d supports the flag:
> 
> ```
> VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%
> ```

You legend! I can confirm that I was able to clear the tutorial with these. Extreme settings, 2560x1440, 144hz, 9950X3D / RTX 5090 / NVIDIA 595.58.03 / Linux 7.0.1 / Proton Experimental / NixOS 25.11+unstable packages.

## Comment 4524793312

other (NONE) · vialolis · 2026-05-23T08:21:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4524793312

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4521684877

2 Days playing with no crash FHC00 and stuttering but after crash FHC01 after wheelspin. And where players in horizon live?

## Comment 4525165087

other (NONE) · Danil0v3s · 2026-05-23T11:24:52Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4525165087

> I was going to avoid adding noise, but this is getting a bit ridiculous.
> 
> I run a 3060Ti on Arch with X11. For me, the game works almost entirely fine, with some slowdowns on asset streaming (which is a famous problem of their engine anyway), with _ONE_ option and _ANY_ relatively fresh proton version, where vkd3d supports the flag:
> 
> ```
> VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%
> ```

This one paired with Proton Hotfix fixed the issues for me.

One caveat though is DLSS has a weird bug with some shiny stuff on the screen. Regular AA will do it for now

## Comment 4525193358

other (NONE) · drkhac · 2026-05-23T11:38:44Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4525193358

> VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%

This also worked for me on 
Bazzite 44
Nvidia 4050

## Comment 4525313845

other (NONE) · MementoMortes · 2026-05-23T12:16:59Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4525313845

Just for clarification because people keep talking about manually copying files from vkd3d-proton into their local steam installation...

I was under the impression that the official way to test the changes is by changing the version of Proton Experimental to the Proton Experimental [bleeding-edge] version in Steam and set VKD3D_CONFIG to the experimental flags or am I missing something here which makes it necessary to manually manage those files?

## Comment 4525402177

other (NONE) · phamaralbr · 2026-05-23T12:49:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4525402177

Was any definitive fix found for the stuttering? It seems like on windows, disabling HAGS makes the game perfectly smooth.

I'm stuck with the low textures workaround but even then I get a lot of hiccups.

## Comment 4525673710

other (NONE) · Robozone05 · 2026-05-23T14:32:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4525673710

> Was any definitive fix found for the stuttering? It seems like on windows, disabling HAGS makes the game perfectly smooth.
> 
> I'm stuck with the low textures workaround but even then I get a lot of hiccups.

Im in the same boat and i have the same question.

## Comment 4525814536

other (NONE) · dyfrgi · 2026-05-23T15:33:22Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4525814536

Looks like bleeding-edge just pulled in some more vkd3d-proton changes, but is still missing the last 11 or so commits from https://github.com/HansKristian-Work/vkd3d-proton/tree/forza-workarounds. That means that it has the basic descriptor heap changes but is missing the FH6-specific changes, but it may be just as good as proton-cachyos now as that has an even older version of the descriptor heap changes. If you want to try it, note that the flag is different, `VKD3D_CONFIG=i_want_broken_descriptor_heap` (I assume that `enable_experimental_features` is still required, too).

I'd be interested to hear about experiences with bleeding-edge 20260523. I'd also love to see a NixOS config that builds and uses the forza-workarounds branch and uses that along with some appropriate Proton base version (11.0?).

## Comment 4526166839

other (NONE) · b1zzu · 2026-05-23T18:11:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4526166839

The gameplay run smoothly on my RX 7800 XT, but in the the **Vinyl Select** page there is no preview of the vinyl

## Comment 4526377926

other (NONE) · RPINerd · 2026-05-23T19:53:13Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4526377926

> The gameplay run smoothly on my RX 7800 XT, but in the the **Vinyl Select** page there is no preview of the vinyl

Yeah I'm hoping this gets addressed sooner rather than later, I'm really getting the itch to start customizing 

## Comment 4526556741

other (NONE) · murderbymodem · 2026-05-23T21:21:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4526556741

> The gameplay run smoothly on my RX 7800 XT, but in the the **Vinyl Select** page there is no preview of the vinyl

I'm seeing the same issues with the vinyl decals - this is the main issue with this game that I'd like to see addressed. 

I've not experienced any game crashes or major issues on AMD hardware (9800X3D + 9070XT). Any performance issues were resolved by lowering the graphics settings, which I'm fine with as apparently even on Windows there are performance issues on AMD GPUs currently.

I'm on CachyOS KDE using [Proton Bleeding Edge](https://github.com/ValveSoftware/Proton/wiki/Proton-Versions) and only the following launch arguments:
`PROTON_FSR4_UPGRADE=1 gamescope -w 2560 -h 1440 -r 120 -f -- %command%`

## Comment 4526847816

other (NONE) · RPINerd · 2026-05-23T23:53:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4526847816

I'm trying to check some logging, any idea how to disable these spamming messages in the proton logs?

```
02246.257:0128:0270:fixme:vkd3d-proton:d3d12_command_list_resolve_subresource: Unsupported combination of resolve parameters.
102246.275:0128:0270:fixme:vkd3d-proton:d3d12_command_list_select_resolve_path: Selected resolve path 3 for mode 3, format 41, but destination image cannot be used as a render target.
102246.275:0128:0270:fixme:vkd3d-proton:d3d12_command_list_resolve_subresource: Unsupported combination of resolve parameters.
102246.294:0128:0270:fixme:vkd3d-proton:d3d12_command_list_select_resolve_path: Selected resolve path 3 for mode 3, format 41, but destination image cannot be used as a render target.
102246.295:0128:0270:fixme:vkd3d-proton:d3d12_command_list_resolve_subresource: Unsupported combination of resolve parameters.
102246.312:0128:0270:fixme:vkd3d-proton:d3d12_command_list_select_resolve_path: Selected resolve path 3 for mode 3, format 41, but destination image cannot be used as a render target.
102246.312:0128:0270:fixme:vkd3d-proton:d3d12_command_list_resolve_subresource: Unsupported combination of resolve parameters.
102246.330:0128:0270:fixme:vkd3d-proton:d3d12_command_list_select_resolve_path: Selected resolve path 3 for mode 3, format 41, but destination image cannot be used as a render target.
102246.330:0128:0270:fixme:vkd3d-proton:d3d12_command_list_resolve_subresource: Unsupported combination of resolve parameters.
102246.348:0128:0270:fixme:vkd3d-proton:d3d12_command_list_select_resolve_path: Selected resolve path 3 for mode 3, format 41, but destination image cannot be used as a render target.
102246.348:0128:0270:fixme:vkd3d-proton:d3d12_command_list_resolve_subresource: Unsupported combination of resolve parameters.
```

I looked on the debug channels from the official wine docs, but doing WINEDEBUG=fixme-all doesn't remove them..

## Comment 4529281559

other (NONE) · tomme87 · 2026-05-24T16:10:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4529281559

I got it running pretty good with this:
```
VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap gamemoderun gamescope -W 3840 -H 2160 -r 60 -f -- %command%
```

I had som performance issues so was experimenting with some options like this:
```
VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap PROTON_FSR4_UPGRADE=1 gamemoderun gamescope -w 2560 -h 1440 -F fsr -W 3840 -H 2160 -r 120 -f -- %command%
```

But it kept crashing on startup, so I decided to revert to my last known good and now the game freezes at the beginning of the playground games splash screen. And whatever I do I can't get any further, it always(*) freezes there.. Proton Hotfix btw.

Wish I stopped experimening xD

(*)For some strange reason it works if i set `PROTON_LOG=1`, but then the game is stuttering alot, and is not playable.

edit: fixed it, se comment below.

## Comment 4529505735

other (NONE) · mitchellurgero · 2026-05-24T17:41:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4529505735

> But it kept crashing on startup, so I decided to revert to my last known good and now the game freezes at the beginning of the playground games splash screen. And whatever I do I can't get any further, it always(*) freezes there.. Proton Hotfix btw.

Do you have nvidia reflex or dlss turned on?


## Comment 4529632135

other (NONE) · tomme87 · 2026-05-24T18:36:59Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4529632135

> > But it kept crashing on startup, so I decided to revert to my last known good and now the game freezes at the beginning of the playground games splash screen. And whatever I do I can't get any further, it always(*) freezes there.. Proton Hotfix btw.
> 
> Do you have nvidia reflex or dlss turned on?

nvidia reflex might have been on, but not dlss.

I ended up re-installing the game. And now I have no issues, even the initial performance issues is gone, it just rock solid 60fps.

## Comment 4529799734

other (NONE) · A402B · 2026-05-24T19:54:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4529799734

Hey everyone, I have a potential solution! :)

OS: Ubuntu 26.04 (Means I'm using Wayland and Gnome 50)
Proton: Cachy-OS-11.0 2026 0506 version SLR     I got this from the cachy-os repo
Nvidia 3050 8gb VRAM
I was experiencing crashing and terrible performance like you all. I couldn't even get 30 seconds through the tutorial without it freezing and crashing. (error FHC00)

My solution was to update the Nvidia drivers to **595.71.05**! I used the command ubuntu-drivers in the terminal to update it.
And in the launch options for steam:

PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%

With graphics set to HIGH (Not HIGH+RT!) it works wonderfully at 60fps, no more crashes and very very very infrequent microstutters.

## Comment 4530623272

other (NONE) · mukarramarif · 2026-05-25T00:13:24Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4530623272

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4492270343

good fix for g16 amd 370HX 4060ti with running latest proton bleeding edge

## Comment 4533073177

other (NONE) · OGCardoc · 2026-05-25T09:13:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4533073177

> > VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%
> 
> This also worked for me on Bazzite 44 Nvidia 4050

This fixed it for me - i had a issue where it would just crash with the FHC00 error aswell.

OS: Linux Mint 22.3 x86_64 
Kernel: 6.8.0-117-generic 
CPU: AMD Ryzen 9 5900X (24) @ 3.700G 
GPU: NVIDIA GeForce RTX 3080 
Memory: 32010MiB 
Proton Hotfix (todays date: 25. of May 2026)
Startup commands in steam:
`VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%`


## Comment 4535822948

other (NONE) · GSDragoon · 2026-05-25T16:50:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4535822948

Like many others, I've been experimenting all sorts of things trying to get the stuttering and fps drops to improve. I just found something today that makes a significant improvement that I haven't read about yet.

`DISABLE_LOW_LATENCY_LAYER=1`
You can read more about it here: https://github.com/Korthos-Software/low_latency_layer

The stutters and fps drops are still there, but adding that makes a significant improvement. None of the other options seemed to make a difference, including LOW_LATENCY_LAYER=0, which is strange.

This low latency layer seems to be something in proton-cachyos but not the official proton versions. Or am I wrong?

I tested this using the latest official proton-cachyos (20260506) as well as the latest build from https://github.com/CachyOS/proton-cachyos/actions/workflows/snapshot.yml using the FH6 hotfix files from vkd3d-proton. This gives me the best performance.

Full command/envs:
> DISABLE_LOW_LATENCY_LAYER=1 PROTON_ENABLE_WAYLAND=1 PROTON_USE_NTSYNC=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap,avoid_image_buffer_aliasing,null_buffer_siblings RADV_EXPERIMENTAL=heap radv_wait_for_vm_map_updates=true %command%

I haven't tried with the just released version of the low latency layer that disables it by default. Maybe I'll submit a PR or bug report on cachy to get it updated.

My system:
Operating System: CachyOS Linux 
KDE Plasma Version: 6.6.5
Kernel Version: 7.0.10-1-cachyos (64-bit)
Processors: 16 × AMD Ryzen 7 9800X3D 8-Core Processor
Memory: 64 GiB of RAM
Graphics Processor: AMD Radeon RX 6800
Mesa 26.1.1-arch2.1

## Comment 4535867449

maintainer (MEMBER) · kisak-valve · 2026-05-25T16:59:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4535867449

Hello @GSDragoon, adding a third party Vulkan layer and then disabling it to see an improvement is fairly strong evidence that it's an issue with that layer being added to the render stack and is not a Proton issue. You should follow up with the maintainers of that Vulkan layer.

## Comment 4536218939

other (NONE) · dyfrgi · 2026-05-25T18:03:47Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4536218939

I've been playing fairly successfully with proton-cachyos-20260506 for a while now, but with two notable issues.

Startup options: `VKD3D_CONFIG=enable_experimental_features,descriptor_heap PROTON_VKD3D_HEAP=1 PROTON_ENABLE_WAYLAND=1 gamescope -w 3440 -h 1440 -W 3440 -H 1440 -f -S integer --adaptive-sync -r 144 -- %command%`

In-game settings: Ultra preset graphics. 3440x1440, 72fps or unlocked frame rate, no vsync, full screen off, TAA enabled, DLSS stuff all off.

1. When starting the game, the resolution is... wrong? It looks like it's being scaled up considerably. If I change the resolution in the settings to 1024x768, then back to 3440x1440, then back to 1024x768, then back to 3440x1440 again, it is sharp and no longer looks like it's being scaled. This behavior is the same regardless of scaling config I pass to gamescope.
2. After running for about 40 minutes, the frame timing becomes terrible. The average frame rate, when uncapped, is steady at 85 or so out in the world. However, the *look* of it is as if it's delivering 3 frames at a time. Unsteady panning, like 3:2 pulldown on a 60Hz TV but *way* worse. I can also see the refresh rate of my monitor varying wildly. I have an AOC CU34G2X which is a 48-144Hz variable rate VA panel. Brightness changes dramatically when the refresh varies so I can see exactly when the bad frame timing starts.

PROTON_ENABLE_WAYLAND is probably doing nothing here, or at least nothing useful.

Besides those two issues, the game is running reasonably well. If the frame timing issue is addressed I'd describe it as "works well enough". The resolution workaround is irritating but would be less so if I only had to do so once a session not every 40 minutes or so.

My system:
OS: NixOS 26.05 (Yarara, currently unstable)
Compositor: Niri
Kernel: 6.18.28
CPU: AMD 9950X3D
GPU: NVidia 5080
Mesa version: 26.1.1
Proton version: proton-cachyos-11.0-20260506-slr-x86_64_v3


## Comment 4544604510

other (NONE) · Stream5710 · 2026-05-26T13:42:53Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4544604510

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4529281559 

This works, and also fixed audio issues I've had (where I could hear nothing but little popping noises if there was any to begin with)  with `VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%` without gamescope.
I just had to adjust gamescope options to my display and remove `gamemoderun` which conflicts with my system.
FHE01 crash still happens which looks like a game issue and is also reported on Windows, but when it happens I can't click the button in the crash handler.

OS: PikaOS 4
DE: KDE Plasma 6.5.4
Kernel: 7.0.8-pikaos
CPU: Ryzen 5 2600
GPU: RTX 4060 Ti 8GB
Nvidia Driver: 595.71.05
Mesa: 26.1.1-101pika1
Proton: Hotfix (May 25, 2025)

## Comment 4546886864

maintainer (MEMBER) · kisak-valve · 2026-05-26T17:28:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4546886864

Forza Horizon 6 - Video Card Crash (Code: FHC00) at high speeds on Linux (Pop!_OS / COSMIC Wayland / NVIDIA RTX 4060)

Issue transferred from https://github.com/ValveSoftware/Proton/issues/9822.
@Kpun11th posted on 2026-05-26T17:06:08:

Hello,

I am experiencing a consistent game crash with Error Code: FHC00 (Video Card Crash) while playing Forza Horizon 6 on Linux. 

The game successfully launches using Proton Hotfix. The built-in Benchmark Mode runs perfectly fine from start to finish without any crashes. However, in the actual game, the crash happens consistently during high-speed driving (around 120+ MPH) when streaming environments or driving past dense areas (like cherry blossom fields).

Right before the crash, the game freezes for about 1 second, attempts to recover and moves forward for a split second, then completely freezes and throws the FHC00 error. Steam then becomes unresponsive (zombie process) and requires a manual 'pkill' in the terminal to close.

I have already tried using launch options like PROTON_FORCE_VULKAN_HEAP_SIZE, VKD3D_CONFIG=no_upload_hbm, and PROTON_VKD3D_HEAP=1, but the high-speed streaming crash persists.

System Specifications:
- OS: Pop!_OS 22.04 LTS (with COSMIC Desktop Environment / Wayland)
- CPU: AMD Ryzen 5
- GPU: NVIDIA GeForce RTX 4060 (8GB VRAM)
- RAM: 32 GB
- NVIDIA Driver Version: 580.159.03
- Compatibility Tool: Proton Hotfix

Please let me know if you need any proton logs or additional details. Thank you!

## Comment 4548262779

other (NONE) · fyoory · 2026-05-26T20:02:37Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4548262779

Hi,

I had to play with this a bit to get it stable on Manjaro Linux here and thought others may benefit from the changes that got me to stable, albeit on 'low' or 'medium' presets for now.  Windows runs fine on high here but I did not test extensively on Windows.  Just a run to see if it was stable, gauge the auto-detected frame rates, while trying to get linux to run it.

My workaround in case it helps anyone else.

NVIDIA workaround — stable multi-hour sessions on 4060 Ti / Manjaro / proton-cachyos
System: 
TUF Gaming X570 Plus-Wifi
Ryzen 7 5700G
64GB RAM
TUF Gaming 4060 Ti OC 8GB
Manjaro Linux
KDE Plasma X11
mwhd-nvidia driver 595.71.05
proton-cachyos-11.0-20260506
 
1. Create `/etc/sysctl.d/99-fh6.conf`
 
```
vm.nr_hugepages=1024
fs.file-max=2097152
fs.inotify.max_user_watches=524288
```

Then apply with `sudo sysctl --system`.
 
2. Steam launch options

```
mangohud PULSE_LATENCY_MSEC=60 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap gamemoderun %command%
```
 
3. In-game preset
 
Low or Medium (Medium works but at a slightly lower frame rate).
 
The key fix appears to be `VKD3D_CONFIG=descriptor_heap`, which changes how VKD3D manages D3D12 descriptor heaps and prevents the Xid 109 CTX SWITCH TIMEOUT that otherwise causes crashes. The sysctl hugepages tweak also helps by reducing TLB pressure. Without these changes the game crashed reliably within minutes on NVIDIA hardware.

Hopefully NVIDIA gets off their tails and fixes this as I should be able to run at least 'high' preset here and probably more. ;/

But it got it workable for me for the time being.

## Comment 4549901770

other (NONE) · CRKrJ4K · 2026-05-26T23:32:39Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4549901770

Updated to `proton-cachyos-11.0-20260519-slr-x86_64_v3`

Now I can play the game without any VKD3D specific launch options, and get the same performance as before when i was using `VKD3D_CONFIG=no_upload_hvv,single_queue`. However, texture quality set to Low is still required.

Also, `LOW_LATENCY_LAYER=1` is working well. Using my Gamesir G7 Pro 8k @ 4k polling rate is now usable via xinput, and @ 8k polling rate is noticeably better via xinput but still has too much input lag to be viable.

System: 14900KS, 7900 XTX, CachyOS

## Comment 4551067779

other (NONE) · A402B · 2026-05-27T03:53:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4551067779

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4546886864

Hi Kpun11th, update your NVIDIA driver to the latest version (595), I had the same crash as you and updating my driver fixed it.

## Comment 4552067369

other (NONE) · Itz-Shame · 2026-05-27T06:42:34Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4552067369

I'm kinda having similar issues using both cachy proton and experimental. I've noticed for me though that it only crashes if it's my second time opening the game. If I first boot in then launch it it plays as smooth as butter but as soon as I close it I can't make it past the welcome back screen without a crash until I reboot.

System Specifications:

    OS: Arch w/ Hyprland
    CPU: Intel I7 13700KF
    GPU: NVIDIA GeForce RTX 4090 
    RAM: 32 GB
    NVIDIA Driver Version: 595.71.05
    Compatibility Tool: Proton Experimental (Bleeding Edge) and proton-cachyos


## Comment 4552579224

other (NONE) · weinzii · 2026-05-27T07:54:25Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4552579224

Has someone fixed the issue where the vinyls are invisible?

<img width="2560" height="1435" alt="Image" src="https://github.com/user-attachments/assets/80c35d92-ac8a-4a38-b44b-bed903680f0b" />

## Comment 4552932402

other (NONE) · msadev · 2026-05-27T08:44:49Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4552932402

I’m also seeing consistent GPU crashes during the intro/tutorial on NVIDIA.

The game launches correctly and reaches the intro, but it crashes after around 10 seconds with the Forza GPU crash dialog:

```text
code FHC00
```

This happens with both **Proton Hotfix** and **Proton Experimental**.

System details:

```text
OS: Debian GNU/Linux 13 (trixie) 64-bit
Kernel: 6.12.90+deb13-amd64
GPU: NVIDIA RTX 3070 8GB
Driver: 610.43.02
NVIDIA kernel module: Open Kernel Module
Resolution: 3440x1440
Settings during one of the tests: High
Performance before crash: 80+ FPS
```

The crash does not look like a normal game crash. The kernel logs show NVIDIA GPU errors, including Xid 109 and Xid 13. I also see `vkd3d_queue` involved in one of the crashes.

Relevant kernel log excerpts:

```text
NVRM: Xid (PCI:0000:26:00): 109, pid=31058, name=forzahorizon6.e, channel 0x00000010, errorString CTX SWITCH TIMEOUT, Info 0xc012

NVRM: Xid (PCI:0000:26:00): 109, pid=32565, name=forzahorizon6.e, channel 0x00000014, errorString CTX SWITCH TIMEOUT, Info 0xc016

NVRM: Xid (PCI:0000:26:00): 13, Graphics Exception: SKEDCHECK23_CONSTANT_BUFFER_SIZE failed

NVRM: Xid (PCI:0000:26:00): 13, pid=35713, name=vkd3d_queue, Graphics Exception: ESR 0x407020=0x80 0x407028=0x0 0x40702c=0xc4d6f 0x407030=0x0

NVRM: Xid (PCI:0000:26:00): 13, pid=35713, name=forzahorizon6.e, Graphics Exception: channel 0x0000001f, Class 0000c7c0, Offset 00000000, Data 00000000

NVRM: Xid (PCI:0000:26:00): 109, pid=39612, name=forzahorizon6.e, channel 0x00000014, errorString CTX SWITCH TIMEOUT, Info 0xc016
```

I tested different launch options and graphics settings, but none of them had any noticeable effect on the issue.

Current status: the game is still not playable for me on **NVIDIA 610.43.02** with **Proton Hotfix / Proton Experimental**.

## Comment 4552967528

other (NONE) · OGCardoc · 2026-05-27T08:49:54Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4552967528

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4552932402

Which launch args do you have ?
I had the same issues but adding the following launch args fixed the crashes for me:
`VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%`

## Comment 4553254629

other (NONE) · msadev · 2026-05-27T09:26:41Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4553254629

> 
> Which launch args do you have ? I had the same issues but adding the following launch args fixed the crashes for me: `VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%`

I already tested with the suggested launch options:

```bash
VKD3D_CONFIG=enable_experimental_features,i_want_broken_descriptor_heap %command%
```

Unfortunately, I still get the same GPU crash, but it now happens even earlier: before reaching the game menu.

The crash still shows the Forza GPU crash dialog with code **FHC00**, and the kernel logs still show NVIDIA Xid errors similar to the previous ones:

```text
NVRM: Xid 109, name=forzahorizon6.e, errorString CTX SWITCH TIMEOUT
NVRM: Xid 13, Graphics Exception: SKEDCHECK23_CONSTANT_BUFFER_SIZE failed
NVRM: Xid 13, name=vkd3d_queue
```

This also happens with both Proton Hotfix and Proton Experimental.

So on my system, enabling `i_want_broken_descriptor_heap` does not improve the situation. It actually makes the crash occur before the menu instead of during the intro/tutorial.

## Comment 4553326249

other (NONE) · OGCardoc · 2026-05-27T09:36:22Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4553326249

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4553254629

Hmm - I just noticed you are running the new Nvidia 610.xx driver - have you tried the 595 version? As far as I know the 610 should be brand new, so it could cause some issues.

## Comment 4553345171

other (NONE) · msadev · 2026-05-27T09:39:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4553345171

> 
> Hmm - I just noticed you are running the new Nvidia 610.xx driver - have you tried the 595 version? As far as I know the 610 should be brand new, so it could cause some issues.

Yes, I initially tested the game on the **595 NVIDIA driver** and had the same issue there as well.

I actually had high hopes for the new **610.43.02** driver and upgraded specifically to see if it would improve or fix the crash, but unfortunately the behavior is still the same on my system (except i don't have the prelaunch nvidia driver minimum requirement window)

So at least in my case, this does not seem to be a regression introduced only by 610.xx. The crash happened on 595 too, and still happens on 610.


## Comment 4554576710

other (NONE) · RPINerd · 2026-05-27T12:39:12Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4554576710

> Has someone fixed the issue where the vinyls are invisible?

I'm also curious if anyone on linux has normal vinyl thumbnails, or if it's just a small number of us affected for some reason..

Either way it's really killing me now not being able to customize :(



## Comment 4554605303

other (NONE) · Izu-3 · 2026-05-27T12:43:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4554605303

> > Has someone fixed the issue where the vinyls are invisible?
> 
> I'm also curious if anyone on linux has normal vinyl thumbnails, or if it's just a small number of us affected for some reason..

Friend of mine has a perfectly functional game including thumbnails on their 9070XT under linux. Their game also worked OOTB on default proton as well, which is a mystery to me. So it's definitely something which is fixable, it's just a matter of how and why.

## Comment 4554643193

other (NONE) · RPINerd · 2026-05-27T12:51:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4554643193

> Friend of mine has a perfectly functional game including thumbnails on their 9070XT under linux.

What distro, kernel and such? (If you know offhand)

## Comment 4554679029

other (NONE) · Izu-3 · 2026-05-27T12:57:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4554679029

> What distro, kernel and such? (If you know offhand)

openSUSE, kde6.6.5/wayland, kernel 7.0.6-1 and mesa 26.1.0

## Comment 4554774522

other (NONE) · RPINerd · 2026-05-27T13:08:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4554774522

@weinzii, @cccyberwolke, @Gotolei 

You guys! Thanks to @Izu-3 here, I tried something that never even occured to me since Valve themselve recommended Experimental at launch. I just booted the game with 10.whatever is the latest and vinyls thumbnails are back!! Maybe see if it works for you? If so there is a clear regression between 10 and 11 that is the root cause

## Comment 4554817195

other (NONE) · Izu-3 · 2026-05-27T13:13:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4554817195

...huh. That's wild, I can confirm that 10.0-4 fixes the livery editor here too.

## Comment 4556498351

other (NONE) · weinzii · 2026-05-27T16:28:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4556498351

> [@weinzii](https://github.com/weinzii), [@cccyberwolke](https://github.com/cccyberwolke), [@Gotolei](https://github.com/Gotolei)
> 
> You guys! Thanks to [@Izu-3](https://github.com/Izu-3) here, I tried something that never even occured to me since Valve themselve recommended Experimental at launch. I just booted the game with 10.whatever is the latest and vinyls thumbnails are back!! Maybe see if it works for you? If so there is a clear regression between 10 and 11 that is the root cause

lmao, yeah works with 10.0-4! Thanks! :-)

## Comment 4557437273

other (NONE) · fyoory · 2026-05-27T18:27:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4557437273

Anyone know what this steam patch fixes, maybe related (am hoping)?

```
Version Number:

Steam: 364.933

Bug fixes and changes

General

Performance and stability fixes
```

## Comment 4558163350

maintainer (MEMBER) · kisak-valve · 2026-05-27T19:55:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4558163350

Forza Horizon 6 no longer launches after Hotfix 2 (May 27) - EXCEPTION_ILLEGAL_INSTRUCTION loop on Manjaro AMD

Issue transferred from https://github.com/ValveSoftware/Proton/issues/9826.
@jakgraftak posted on 2026-05-27T19:52:56:

# Compatibility Report
- Name of the game with compatibility issues: Forza Horizon 6
- Steam AppID of the game: 2483190

## System Information
- GPU: AMD Radeon RX 7900 XT 20GB
- Video driver version: Mesa 26.1.1-arch1.2
- Kernel version: 6.12.91-1-MANJARO
- Link to full system information report as [Gist](https://gist.github.com/): <!-- to be added -->
- Proton version: Proton Experimental (bleeding-edge), Proton Hotfix, GE-Proton 10-34

## I confirm:
- [x] that I haven't found an existing compatibility report for this game.
- [x] that I have checked whether there are updates for my system available.

## Symptoms
After the Hotfix 2 update (version 364.933, May 27 2026), the game no longer launches. Steam reports the game as running but no window ever appears. The process stays alive indefinitely. Before this update the game ran fine for a week.

The Proton log immediately spams EXCEPTION_ILLEGAL_INSTRUCTION (0xc000001d) across multiple threads from the moment the process starts, and never progresses past this point. Ends with a SIGSYS (blocked syscall).

## Reproduction
1. Install Forza Horizon 6 on Manjaro Linux with AMD GPU
2. Set Proton to any recent version (Hotfix, Experimental bleeding-edge, GE-Proton 10-34)
3. Launch the game
4. Steam shows game as running, no window appears, ILLEGAL_INSTRUCTION loop starts immediately and never stops

[steam-2483190.log](https://github.com/user-attachments/files/28321516/steam-2483190.log)

## Comment 4559505376

other (NONE) · Psykatte · 2026-05-27T23:25:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4559505376

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4516395152

Latest update to FH6 makes the previously stable configs crash with FCH00. :I

`VKD3D_CONFIG=descriptor_heap PROTON_VKD3D_HEAP=1 %command%` on proton-cachyos-11.0-20260506-slr is stable for me now.

## Comment 4559988701

other (NONE) · murderbymodem · 2026-05-28T01:09:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4559988701

> Forza Horizon 6 no longer launches after Hotfix 2 (May 27) - EXCEPTION_ILLEGAL_INSTRUCTION loop on Manjaro AMD
> 
> Issue transferred from [#9826](https://github.com/ValveSoftware/Proton/issues/9826). [@jakgraftak](https://github.com/jakgraftak) posted on 2026-05-27T19:52:56:


Reporting that I played a few hours of multiplayer races today post-hotfix with no issues. 

Computer Information:
Manufacturer: Micro-Star International Co., Ltd.
Model: PRO B650-P WIFI (MS-7D78)
CPU Brand: AMD Ryzen 7 9800X3D 8-Core Processor
Kernel Version: 7.0.10-1-cachyos
AMD AMD Radeon RX 9070 XT (radeonsi, gfx1201, ACO, DRM 3.64, 7.0.10-1-cachyos)
Driver Version: 4.6 (Compatibility Profile) Mesa 26.1.1-arch2.1

Proton Experimental (bleeding-edge)

Still using low graphics settings, for best performance/low power draw and because I haven't tested if hitching is still an issue with higher settings.

`PROTON_FSR4_UPGRADE=1 gamescope -w 2560 -h 1440 -r 120 -f -- %command%`



## Comment 4561282115

other (NONE) · fbt · 2026-05-28T06:12:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4561282115

> [@weinzii](https://github.com/weinzii), [@cccyberwolke](https://github.com/cccyberwolke), [@Gotolei](https://github.com/Gotolei)
> 
> You guys! Thanks to [@Izu-3](https://github.com/Izu-3) here, I tried something that never even occured to me since Valve themselve recommended Experimental at launch. I just booted the game with 10.whatever is the latest and vinyls thumbnails are back!! Maybe see if it works for you? If so there is a clear regression between 10 and 11 that is the root cause

I became curious, and decided to put newer vkd3d into Proton 10-4... and the decal selector menu is broken. That narrows it down. The game then promptly crashed with the usual gpu error tho which confuses me.

UPD: JFYI I've switched the flag to `descriptor_heap` because Proton Experimental [bleeding-edge] seems to have pulled in the full descriptor heap implementation as of less then a day ago. H6 works as smoothly as it was before, which is to say a bit jittery at times. NVIDIA 3060Ti, Intel i5, updated Arch.

## Comment 4565464297

other (NONE) · jakgraftak · 2026-05-28T15:07:54Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4565464297

Update: tried `VKD3D_CONFIG=descriptor_heap` on both Proton 10 and Proton Experimental bleeding-edge, same result on both. Game still doesn't launch.

Interestingly the SIGSYS codes are different compared to my earlier log — now seeing `0xeb`, `0xc1`, `0xb4` instead of `0x4`, `0xe`, `0xd7` — but the EXCEPTION_ILLEGAL_INSTRUCTION loop is identical otherwise. Not sure if that's relevant but figured I'd mention it.

Setup: Manjaro, RX 7900 XT 20GB, Ryzen 7 7700X, Mesa 26.1.1, kernel 6.12.91-1-MANJARO

[steam-2483190.log](https://github.com/user-attachments/files/28352307/steam-2483190.log)

## Comment 4565951687

other (NONE) · Izu-3 · 2026-05-28T16:02:41Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4565951687

Interesting occurrence just now testing the game after a 150mb patch dropped on Steam. Tried booting the game, and it was having extreme issues trying to load the game from disk before getting stuck on the loading screen with very little disk activity, everything else on that nvme drive functioning just fine. Restarting the game to try again, it ran the first boot setup again and it'd logged me out before getting stuck loading again. Third time I tried the benchmark and after a really big struggle, it did start but would constantly freeze entirely where lurches tend to happen.

Rebooting my machine, the issue went away and it's back to a somewhat stuttery 30fps like it tends to be on a clean boot (but importantly, no lurches, even if I remove the fps cap). Makes me wonder if there's some package or background process on my distro (and potentially others) which is causing the severe lurches, since they seem to be asset streaming related...?

## Comment 4570231663

other (NONE) · JpnRndr01 · 2026-05-29T03:33:10Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4570231663

Noticed a new issue with at least Fedora 43 with Nvidia cards, the game crashes without fail during race transitions, so when you go from free roam into race menu and it flashes up the game logo it just crashes without fail, regardless of version of proton 

Also would like to say thank you to valve and the people who are contributing to get fh6 to work somewhat well on Linux, shame Microsoft did a half measure with just SteamOs support

## Comment 4570475895

other (NONE) · 0x000C0A71 · 2026-05-29T04:17:19Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4570475895

I get the small popup, a black window, and then a FHE01 crash. Cannot get past that

## System Info
- GPU: RX 9070 XT
- CPU Ryzen 9950X3D
- Driver: Mesa 26.2.0-devel (git-eb17e7b102)
- Kernel version: 6.18.32
- Proton version: GE-Proton10-34 (tried hotfix, experimental, and dw-proton aswell with _even less_ success)
- Launch options: `PROTON_ENABLE_WAYLAND=1 VKD3D_CONFIG=no_upload_hvv,single_queue RADV_EXPERIMENTAL=heap radv_wait_for_vm_map_updates=true %command%`

## Comment 4573379677

other (NONE) · RusticLights · 2026-05-29T09:43:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4573379677

EDIT: Played with this setup for a bit with no crashes and the performance as it is, seems consistent. Interestingly subbing fsr scaling for anti-aliasing which i was intending to do, causes the frame graph go all over again. Lower gpu load makes for less stutter/rubberbanding, pretty sure i've seen that talked about among all the reports. Guess i'm just concurring that then :P
Really hoping things get ironed out for this game. I think with this and other things to try out, i'm quite close to tolerating it to not switch in my windows ssd just to play 👍 

Bazzite 44, 7800X3D & 9070XT here. Found some interesting results.
The main problem is still the texture options (high setting causes the stuttering), but Proton 10.0-4 with no launch options, and locked at 60fps or under gives me (so far) the most windows like results. Meaning the least amount of "stutterbanding" if you will. Though it does reintroduce the extra blackscreen alt-tabbing work.

<details>
<summary>1. Windows, 72fps. See the super dense gpu graph.</summary>
<img width="1720" height="720" alt="Image" src="https://github.com/user-attachments/assets/0c5a9f76-6b98-4685-9618-feabdb403f99" />
</details>

<details>
<summary>2. Proton 10.0-4, 72fps,  note the much more sporadic gpu graph. Even with low textures it's a stutterfest. It's the same or worse at higher/unlocked fps.</summary>
<img width="1720" height="720" alt="Image" src="https://github.com/user-attachments/assets/59a482de-1611-4599-ae9f-9f5ec3bc241a" />
</details>

<details>
<summary>3. 60fps lock and low textures. Note the much denser graph. I'd wager over half of the frames are closer to that one area. To the eyes it's much smoother as well.</summary>
<img width="1720" height="720" alt="Image" src="https://github.com/user-attachments/assets/51e85f02-58f8-403d-90df-b49cfa266c9a" />
</details>

Lower fps lock is tough to demonstrate as then the graph gets maxed out at 75fps, so it doesn't show how varied the frames would be.


Bazzite 44
CPU: AMD Ryzen 7 7800X3D
RAM: 32GB
GPU: 9070 XT
Mesa 26.0.5
KDE Plasma Version: 6.6.4
KDE Frameworks Version: 6.26.0
Kernel 6.19.14-ogc5.1.fc44.x86_64 (64-bit)
Wayland


## Comment 4575996649

other (NONE) · TheNumerus · 2026-05-29T13:56:12Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4575996649

So with latest proton bleeding-edge I can run raytracing now, thanks to merged changes in `vkd3d-proton`. The reflections are broken, performance is subpar, but at least it doesn't crash. 

<details>
<summary>Benchmark Result</summary>
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/a5144f5c-c74a-4545-9e36-6de5aeffe6c9" />
</details>

<details>
<summary>Reflections screenshot</summary>
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/1fc40dd1-b27c-4bac-a291-884c1b2c4446" />
</details>



## Comment 4576440499

other (NONE) · RusticLights · 2026-05-29T14:45:30Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4576440499

> So with latest proton bleeding-edge I can run raytracing now, thanks to merged changes in `vkd3d-proton`. The reflections are broken, performance is subpar, but at least it doesn't crash.
> Benchmark Result
> Reflections screenshot

Oh dang, thanks for posting. I hadn't tried bleeding-edge today yet. Getting much more stable performance than it has been before (and yeah, RT settings don't crash). Texture and environment geometry settings still cause the stutter-rubberbanding though.

My non-RT benchmarks look quite similar to what i had with proton10.0-4, the stutter counts stay in single digits (with those couple settings on low).

In fact, i noticed an odd result. With RT the gpu usage looks almost similar to [windows](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4573379677) but the stutter goes up compared to RT off.
<details>
<summary>RT-off</summary>
<img width="3440" height="1440" alt="Image" src="https://github.com/user-attachments/assets/a82899bd-01a2-4453-8f1b-874dd73e45cb" />
</details>
<details>
<summary>RT-on (gpu usage is more stable but stutter goes up)</summary>
<img width="3440" height="1440" alt="Image" src="https://github.com/user-attachments/assets/3ef8c6e6-b81c-43bb-a7d7-94d7eb19ce95" />
</details>


## Comment 4579344598

other (NONE) · kostadinsh · 2026-05-29T19:54:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4579344598

The game still launches behind a black window on the Sway window manager, and each time it loses focus be it by switching workspaces or moving my mouse to another monitor, the game again goes behind the black window, and I have to make it fullscreen with Super+F for it to show up.

Also sometimes, when the game is not focused - it tends to freeze with just the sound playing and has to be restarted.

I can't really get a log since it grows to 2GB by the time the intro finishes loading.

Sway version: 1.12
Kernel version: 7.0.10
Mesa version: commit e2631eca0f
GPU: AMD Radeon RX 6800
Proton version: bleeding-edge from today

## Comment 4580833067

other (NONE) · RafaelHGOliveira · 2026-05-30T00:15:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4580833067

After the recent NVIDIA 610.43.02 driver update on CachyOS, the game crashes within a few minutes regardless of Proton version — with Ray Tracing disabled as well.

**System:**
- CPU: AMD Ryzen 7 5700X3D
- GPU: NVIDIA GeForce RTX 4070 SUPER
- Driver: NVIDIA 610.43.02 (CachyOS)
- Kernel: Linux 7.0.10-2-cachyos
- Proton versions tested: Proton-CachyOS (11.0-20260520-slr), GE-Proton10-34, Proton Experimental, Proton Hotfix

**Already tested:**
- `VKD3D_CONFIG=enable_experimental_features,descriptor_heap`
- `PROTON_VKD3D_HEAP=1`
- Manually applied DLLs from [vkd3d-proton PR #3033](https://github.com/HansKristian-Work/vkd3d-proton/pull/3033) (Forza Horizon 6 workarounds) — crash persists
- RT disabled

Anyone else seeing this with NVIDIA 610 specifically?

## Comment 4581205008

other (NONE) · Ramalama2 · 2026-05-30T01:43:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4581205008

PROTON_VKD3D_HEAP=1 is useless and doesnt exists anymore.

On nvidia in Linux, you need to run the game at least once without:
"VKD3D_CONFIG=enable_experimental_features,descriptor_heap"

It will Crash anyway after 10s, max 2mins...
after it crashed, you need to use:
VKD3D_CONFIG=enable_experimental_features,descriptor_heap

Im on the 610 driver with an RTX6000 Blackwell GPU.

With the newest Proton hotfix from 29.05.2026 you need now additionally:
VKD3D_DISABLE_EXTENSIONS=VK_EXT_present_timing (at least if you use gamescope)

Otherwise all the fixes and proton workarounds are almost all for AMD Graphic cards, nvidia seems not to be loved by the linux community xD

## Comment 4582879719

other (NONE) · eyenalxai · 2026-05-30T12:53:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4582879719

stutters on AMD GPUs seem to have been fixed on Windows according to this video: https://www.youtube.com/watch?v=QmsM5hfbmwE

no changes on linux for me. any updates/workarounds on that besides setting textures and geometry to low (still stutters for me on 9060XT)? i think it's more important than having RT on. 
 

## Comment 4582938490

other (NONE) · phamaralbr · 2026-05-30T13:19:57Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4582938490

> stutters on AMD GPUs seem to have been fixed on Windows according to this video: https://www.youtube.com/watch?v=QmsM5hfbmwE
> 
> no changes on linux for me. any updates/workarounds on that besides setting textures and geometry to low (still stutters for me on 9060XT)? i think it's more important than having RT on.

I'm looking for the same answer. Game has worked fine since day one for me, no crashes and no other problems exept the stutter.

So i'm stuck playing on low textures and even then I get stutters. Really looking forward for a fix on this.

## Comment 4583125103

other (NONE) · fbt · 2026-05-30T14:41:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583125103

Upgrading to the 610 nvidia driver has now made Horizon 6 immediately and reliably crash with the same gpu error for me with `descriptor_heap` on, not even reaching the menu. Without it, the game crashes after a bit of driving, as usual.

Checked it with a clean prefix, same thing.

```
[ 3602.676884] NVRM: Xid (PCI:0000:01:00): 109, pid=128176, name=forzahorizon6.e, channel 0x00000016, errorString CTX SWITCH TIMEOUT, Info 0x1c01c
[ 3731.783586] NVRM: Xid (PCI:0000:01:00): 13, Graphics Exception: SKEDCHECK23_CONSTANT_BUFFER_SIZE failed
[ 3731.786969] NVRM: Xid (PCI:0000:01:00): 13, Graphics Exception: ESR 0x407020=0x80 0x407028=0x0 0x40702c=0xc0db1 0x407030=0x0
[ 3731.790031] NVRM: Xid (PCI:0000:01:00): 13, pid=136437, name=forzahorizon6.e, Graphics Exception: channel 0x00000016, Class 0000c7c0, Offset 00000000, Data 00000000
```

Arch, Nvidia 3060Ti, nvidia-open 610.43.02-1.
Same picture with Proton Experimental, Hotfix and latest CachyOS-proton.

UPD: PROTON_HIDE_NVIDIA_GPU=1 + descriptor_heap gets me to the menu, but the game reliably crashes with the same error once it finishes loading.
UPD1: https://github.com/HansKristian-Work/vkd3d-proton/issues/3077#issuecomment-4583369031 this has been reported to the vkd3d-proton issue tracker.
UPD2: It works with proton-cachyos-11.0-20260520-slr-x86_64 and `PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%`. It looks like the issue is specifically between the 610 driver and the absolute latest descriptor_heap code, as the older incomplete implementation works fine.

## Comment 4583467880

other (NONE) · Shijikori · 2026-05-30T16:48:19Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583467880

I've recently noticed some graphical issues? Some textures seem to get corrupted. It's often the gravel/dirt/grass textures but sometimes the pavement as well. It kinda looks like bump maps or normal maps are getting fuzzed up which causes a sort of grid pattern or stripes in textures. I also occasionally see some wildly corrupted textures which kinda look like black textures. I doubt this is a VRAM limitation issue as I have 16GB of VRAM and have yet to fill it up.

It happens between all environment graphics settings. I am not sure if it happens to be related to proton. I use Proton 10-4 at the moment. No particular launch options have made any difference to this issue.

Performance seems otherwise okay. Some amount of hitching but nothing that particularly bothered me at largely ultra settings.

## System Info

Operating System: Kubuntu 26.04 LTS
KDE Plasma Version: 6.6.4
KDE Frameworks Version: 6.24.0
Qt Version: 6.10.2
Kernel Version: 7.0.0-17-generic (64-bit)
Graphics Platform: Wayland
Processors: 16 × AMD Ryzen 7 7700X 8-Core Processor
Memory: 32 GiB of RAM (31.0 GiB usable)
Graphics Processor: AMD Radeon RX 6800 XT
Manufacturer: Gigabyte Technology Co., Ltd.
Product Name: B650 AORUS ELITE AX
Mesa Drivers: Mesa 26.0.3-1ubuntu1 (LLVM 21.1.8)

## Screenshots

Stripe pattern on sand textures (happens consistently, I am not sure if that one is intended but seems odd to me)
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/a514da10-fbc7-4a94-9529-7684c20c70e0" />

Pavement texture corruption
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/8e0a5768-ddd6-4503-aafa-29afecb2c85f" />

Similar corruption on dirt road.
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/9192d95b-cca2-476b-a3d5-41afb18034d7" />

I haven't noticed this before but more severe corruption of textures (on Proton Experimental bleeding-edge, I don't recall having this issue with 10-4)
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/81f02ce1-4e50-4287-9f13-958e6a3d2ce6" />

## Comment 4583489848

other (NONE) · oneandonlyno1 · 2026-05-30T16:58:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583489848

**System:**
- OS: CachyOS (rolling)
- Kernel: Linux 7.0.10-1-cachyos
- CPU: AMD Ryzen 9 5950X
- GPU: NVIDIA GeForce RTX 4080 (16 GB VRAM)
- Driver: NVIDIA 595.71.05
- RAM: 125 GiB
- DE: KDE Plasma 6 (Wayland)
- Proton: 

<img width="367" height="36" alt="Image" src="https://github.com/user-attachments/assets/d1111dde-f9c4-4da1-83af-3c386db24831" />

---

I'm using rtx 4080 on cachyos - for me game works 98% fine - has stutters on certain occasions, but doesn't crash - I'm using proton-cachyos(steam runtime)  + startup options:

`PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%`

my graphic settings are basicaly extreme - everything maxed out EXCEPT OF RAYTRACING - raytracing instantly crashes game


<img width="3443" height="1437" alt="Image" src="https://github.com/user-attachments/assets/21c74d0b-0eec-4d98-a9fb-1ecf72265308" />

Environment texture quality -> low benchmark:

<img width="3443" height="1437" alt="Image" src="https://github.com/user-attachments/assets/96c1d063-8887-4eba-9c99-eca44aab0694" />

environment texture + geometry low

<img width="3443" height="1437" alt="Image" src="https://github.com/user-attachments/assets/f5503fe5-3a58-4c28-9dd3-76f1392e4a8d" />

## Comment 4583555488

other (NONE) · syzzori · 2026-05-30T17:28:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583555488

i can confirm the game crashes on 610 with the newest cachyos proton ver 0521slr 
reverting to 595.80 fixes the issue, when will nvidia stop with the ai slop...

## Comment 4583678665

other (NONE) · RafaelHGOliveira · 2026-05-30T18:19:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583678665

**Update:** Downgrading back to NVIDIA driver **595.71.05** resolved the crashes completely. With the following launch options the game runs perfectly — **including with Ray Tracing enabled**:

```
VKD3D_CONFIG=enable_experimental_features,descriptor_heap game-performance dlss-swapper %command%
```

Proton version: **Proton-CachyOS 11.0-20260521-slr** (latest at the time of writing).

So it looks like the regression is specific to the NVIDIA 610 driver series. Rolling back to 595 is a viable workaround for now.

## Comment 4583742932

other (NONE) · CRKrJ4K · 2026-05-30T18:31:59Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583742932

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583467880

I've also seen these texture issues on my son's PC (Windows 11, 6900XT). So I think its more of a game bug than anything else.

Edit: forgot to add that it doesn't happen all the time, the occurrence seems to be random

## Comment 4584003746

other (NONE) · Shijikori · 2026-05-30T19:08:53Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4584003746

> Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4583742932)

It's rather consistent for me. As in : it will happen frequently with certain textures at certain areas of the game and other areas will see little to no issue (Tokyo area is generally okay).

At this point, it's been bound to happen any time I play and might happen within 5 minutes. Though it's possible that I will return to an area previously affected and not immediately experience the issue. Hanging around will always bring it.

I've seen comments going the way of this being a game bug but it wasn't quite clear to me as I could not see anyone share similar issues with screenshots on Windows. General tips like reducing environment texture quality or increasing it does not help what so ever, the issue will sprout up anyway. Same thing for shader quality.



## Comment 4584231060

other (NONE) · fbt · 2026-05-30T19:45:34Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4584231060

> It works with proton-cachyos-11.0-20260520-slr-x86_64

Just to highlight this, as I've updated the post kinda quietly: the alternative to downgrading the nvidia drivers is to grab an older vkd3d with older descriptor_heap code. For me, 610 drivers provide a noticeable performance boost.

## Comment 4584294543

other (NONE) · sharunkumar · 2026-05-30T19:53:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4584294543

`proton-cachyos-slr 11.0.20260521` seems to have some regression, I was using the flags `PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap,no_upload_hvv,single_queue %command%` but it looks like the game crashes consistently on the version above

I've reverted to using version `11.0.20260506` for this reason

my nvidia driver version: `610.43.02`

## Comment 4584559059

other (NONE) · RafaelHGOliveira · 2026-05-30T20:26:10Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4584559059

It looks like there might be a conflict between certain proton-cachyos versions and the NVIDIA 610 driver series. In my case, the game crashes after a few seconds with nvidia 610 across all Proton versions I tried (hotfix, GE, cachyos, experimental). Downgrading back to **595.71.05** while keeping the latest proton-cachyos (`11.0.20260521`) resolves the crashes entirely — game runs fine with RT enabled too.

So the issue seems to be at the nvidia 610 + vkd3d/proton interaction level, not solely a proton version regression.

## Comment 4585196228

other (NONE) · Ramalama2 · 2026-05-30T23:56:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585196228

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4581205008

Why did i got 5 Downvotes?
Because im the only one with a Blackwell GPU on 610 Driver and latest Proton Experimental, where the game works without issues ?

Maybe another tip if the game crashes instantly when you enter the game, i had to delete the Shader-Cache and Proton Prefix:
1. Stop/Quit Steam and:
`.../<Steam-Library>/steamapps/compatdata/2483190`
`.../<Steam-Library>/steamapps/shadercache/2483190`

It will rebuild everything again when you launch Forza. You will need to set your graphic Settings afterwards, but the game should work.
First Launch: only: `VKD3D_DISABLE_EXTENSIONS=VK_EXT_present_timing %command%`
-> Then the game will Crash, but this step is needed to build correct Shaders and so on...
-> After you played 10s or little more and the game Crashed, you should be perfect now to add the descriptor_heap workaround. (descriptor_heap is only needed on blackwell i think)
Second Launch: `VKD3D_CONFIG=enable_experimental_features,descriptor_heap VKD3D_DISABLE_EXTENSIONS=VK_EXT_present_timing %command%`

Then everything should be perfect and the game work without Crashes.
Ray Tracing -> The only thing that i didn't tryed, but i think you shouldn't enable it.
DLSS/DLAA/Frame Generation/Everything else except RT, works perfectly fine here without issues.

Cheers

## Comment 4585229877

other (NONE) · oneandonlyno1 · 2026-05-31T00:12:49Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585229877

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585196228

because you're wrong - `PROTON_VKD3D_HEAP=1` still exists and is used in proton-cachyos-slr - which is the proton version that currently works with raytracing / mfg / dlss and so on

## Comment 4585315424

other (NONE) · CRKrJ4K · 2026-05-31T00:57:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585315424

> > Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585196228)
> 
> because you're wrong - `PROTON_VKD3D_HEAP=1` still exists and is used in proton-cachyos-slr - which is the proton version that currently works with raytracing / mfg / dlss and so on

Depends on the version. If it's the newest, 20260521, the changelog says it's been removed.

https://github.com/CachyOS/proton-cachyos/releases/tag/cachyos-11.0-20260521-slr

## Comment 4585707778

other (NONE) · dudekr · 2026-05-31T04:32:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585707778

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585315424

I modified the launcher options and so far this works on my 5080 card:

PROTON_DLSS_UPGRADE=1 PROTON_ENABLE_WAYLAND=1 PROTON_VKD3D_HEAP=1 %command%

I have not had a chance to test ray tracing yet.

OS:  CachyOS,  proton-cachyos-11.0-20260521-slr   nvidia driver 610

## Comment 4585851489

other (NONE) · fbt · 2026-05-31T05:48:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4585851489

> PROTON_VKD3D_HEAP=1

There is a 99.9(9)% chance that if you remove this, nothing will change. Your game just runs fine without descriptor_heap, apparently.

Just tried it out of curiosity: no, my game still dies once I start driving with the latest cachyos-proton, and crashes in the menu with VKD3D_CONFIG=descriptor_heap. PROTON_VKD3D_HEAP doesn't do anything in cachyos-11.0-20260521-slr, which makes sense as _it has been removed_.

## Comment 4586800823

other (NONE) · JpPgn612 · 2026-05-31T13:18:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4586800823

Hello
So I have a problem: When I boot the game, the different logos showed before the main menu do have sound, but once I reach the main menu, the sound simply disappeared completely

I tried many different protons, but it's the same result every time

## Comment 4586964716

other (NONE) · polimon-git · 2026-05-31T14:10:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4586964716

> Hello So I have a problem: When I boot the game, the different logos showed before the main menu do have sound, but once I reach the main menu, the sound simply disappeared completely

Have you tried unplugging it and plugging it back in?

No, seriously. I'll assume you're running pipewire.
Download qpwgraph, you'll notice that forza horizon 6 has two nodes connected to your output device

right click -> disconnect -> right click -> undo disconnect

do it for both nodes and you'll have audio again

## Comment 4587238883

other (NONE) · Ramalama2 · 2026-05-31T16:03:15Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4587238883

> > PROTON_VKD3D_HEAP=1
> 
> There is a 99.9(9)% chance that if you remove this, nothing will change. Your game just runs fine without descriptor_heap, apparently.
> 
> Just tried it out of curiosity: no, my game still dies once I start driving with the latest cachyos-proton, and crashes in the menu with VKD3D_CONFIG=descriptor_heap. PROTON_VKD3D_HEAP doesn't do anything in cachyos-11.0-20260521-slr, which makes sense as _it has been removed_.

You need the enable_experimental_features, without it, VKD3D_CONFIG=descriptor_heap has no effect.

## Comment 4587347221

other (NONE) · fbt · 2026-05-31T16:36:26Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4587347221

> You need the enable_experimental_features, without it, VKD3D_CONFIG=descriptor_heap has no effect.

From all my testing, this isn't true. I'm not even sure where enable_experimental_features came from initially. I'm currently running the version of cachyos-proton that pulled in a slightly earlier version of vkd3d, and the game crashes without both `VKD3D_CONFIG=descriptor_heap` and `PROTON_VKD3D_HEAP=1` present (and works smooth as butter with them). The experimental flag seems to change nothing.

In a newer cachyos-proton (cachyos-11.0-20260521) , the flag `PROTON_VKD3D_HEAP` has been removed, and `VKD3D_CONFIG=descriptor_heap` alone toggles the feature. Which I know because if it's on with this proton version, the game crashes immediately. You can also see it in the proton log, it says explicitly that descriptor heap has been enabled.

I've isolated as many variables as I could, and my crash is 100% a result of some interplay between 610 nvidia drivers and vkd3d's current descriptor heap implementation. Which is confirmed by multiple similar reports on their tracker, as well as the fact that it works with either slightly older versions of this code or slightly older drivers.

## Comment 4587810024

other (NONE) · fbt · 2026-05-31T19:15:34Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4587810024

> 100% a result of some interplay between 610 nvidia drivers and vkd3d's current descriptor heap implementation

Soooo I've decided to test which is the most recent vkd3d-proton build that still works, and it's literally the previous one: https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/26635336889

Running with those vkd3d dlls and `descriptor_heap` now, the game's smooth and no gpu crash in sight. Definitely a better (and easier) solution than downgrading your gpu drivers.

Reported this to the relevant vkd3d-proton thread, of course.

## Comment 4588191600

other (NONE) · RafaelHGOliveira · 2026-05-31T21:45:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4588191600

> Running with those vkd3d dlls and `descriptor_heap` now, the game's smooth and no gpu crash in sight. Definitely a better (and easier) solution than downgrading your gpu drivers.

Tried the older vkd3d-proton build (run 26635336889) on **NVIDIA 610.43.02** — game still crashed for me. Couldn't get it stable regardless of the `descriptor_heap` combination.

What actually still worked was downgrading back to **595.71.05** with the **latest** proton-cachyos (`11.0-20260521-slr`). With 595, `VKD3D_CONFIG=descriptor_heap` is still required — without it the game crashes too. With it, everything runs fine including RT.

So for me the old vkd3d DLLs didn't bridge the gap on 610; the driver itself seems to be the issue.

**System:** RTX 4070 SUPER · Ryzen 7 5700X3D · CachyOS · Kernel 7.0.10-2-cachyos

## Comment 4588229185

other (NONE) · CRKrJ4K · 2026-05-31T22:02:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4588229185

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4587810024

Tried using the dlls from the given link & unfortunately didn't change anything for my setup. Game still hesitates/stutters. Thank you for providing the link though.

```
14900KS
7900 XTX
CachyOS w/7.0.10 kernel
proton-cachyos-11.0-20260521-slr-x86_64_v3
```

## Comment 4588466987

other (NONE) · fbt · 2026-05-31T22:50:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4588466987

> 7900 XTX

All this descriptor_heap stuff is only relevant for Nvidia, AMD cards have their own, largely separate, set of issues with Horizon 6.

## Comment 4597195301

other (NONE) · vultux · 2026-06-01T23:05:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4597195301

Folks with Nvidia who are crashing the game in the menu.

Removes the variable (everything, it's no longer needed):
`VKD3D_CONFIG="descriptor_heap"`

It will load and go through the menu, it will probably recreate the shader_cache, when trying to load a race it will crash.

Simply reload the game, as the shader_cache will already be created, it will no longer crash.

Remembering that every time you change the startup string the game recreates the shader_cache and will crash again.

Works with: **proton-cachyos-slr-11.0.20260521** and **Nvidia Driver 610.43.02**

_EDIT: It keeps crashing after a while. I believe that the safest thing is to downgrade the Nvidia driver, until an update comes out. People who use Windows are also having problems._

## Comment 4599466153

other (NONE) · Cr0phiXx · 2026-06-02T06:44:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4599466153

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4597195301

~~Currently the most stable for me is exactly as @fbt described.~~

~~I downloaded a seperate version of proton-cachyos, extracted everything to a folder and replaced the vkd3d-proton files with these:
https://github.com/HansKristian-Work/vkd3d-proton/actions/runs/26635336889~~

~~This is the proton-cachyos I downloaded seperately. This might not be the correct one for you:
https://github.com/CachyOS/proton-cachyos/releases/download/cachyos-11.0-20260521-slr/proton-cachyos-11.0-20260521-slr-x86_64_v3.tar.xz~~

~~The files which need to be replaced are located in: 
proton-cachyos-11.0-20260521-slr-x86_64_v3/files/lib/wine/vkd3d-proton/~~

~~The x86 files go into "i386-windows" and the x64 files go into: "x86_64-windows".~~

~~Then copy that whole proton folder into:
/usr/share/steam/compatibilitytools.d (this folder might be different for you. I use CachyOS, if you do aswell, you should be good. If you don't use CachyOS you should check if that is the correct folder for your distro)~~

~~Restart Steam and select that proton Version to start Forza with.~~

~~These are the parameters I run the game with:
DXVK_FRAME_RATE=120 VKD3D_CONFIG=enable_experimental_features,descriptor_heap,no_upload_hvv,single_queue %command%~~

~~From what I found, all those VKD3D_CONFIG commands are still needed because the descriptor heap stuff is not the only broken thing on the game. Reports say that there is something broken with ReBAR hence "no_upload_hvv,single_queue" are still needed.~~

9800X3D
RTX 4080
NVIDIA 610.43.02
Linux 7.0.10-2-cachyos

Can pretty confidently say it's something with descriptor heap in the current vkd3d-proton and the 610.42 Drivers


## Comment 4600979924

other (NONE) · fbt · 2026-06-02T09:24:13Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4600979924

> It keeps crashing after a while.

Ye, it still does crash for me without descriptor_heap. Pre-cached shaders, if you enable them in Steam settings, however, do help with game performance a lot, it turns out. And it loads in under a minute.

## Comment 4601526782

other (NONE) · Ramalama2 · 2026-06-02T10:34:25Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4601526782

Same here, without descriptor_heap i get a lot more FPS, but a crash after 10s-2m of gaming.
With descriptor_heap i get no Crashes and can play forever on my Blackwell GPU, but around 20-30fps less and a lot worse 1% lows.

## Comment 4604445427

other (NONE) · CarlosGonzalez20 · 2026-06-02T16:23:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4604445427

I tried Proton 11 beta and it works fine. With Proton-cachy 11, Proton Experimental, and Hotfix, it always crashes.

## Comment 4606723976

other (NONE) · samuelskovbakke · 2026-06-02T20:25:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4606723976

Has anyone been able to completely fix the stuttering issue yet?

## Comment 4608697140

other (NONE) · urwrstkn8mare · 2026-06-03T02:57:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4608697140

when using descriptor_heap, is anyone experiencing the issue described here? https://github.com/HansKristian-Work/vkd3d-proton/issues/2872#issuecomment-4579915077 

i am experiencing that but like alot of others in this thread, without descriptor_heap the game crashes after a few minutes. 

i also had stuttering for a bit but what solved it is just removing all the options other than descriptor_heap (for OOM errors i just added an FPS cap but it seems like adding the enable_experimental_features option also fixes it)

EDIT:

turns out i've fixed the issue by downgrading to proton-cachyos-slr 1:11.0.20260506-1(also using dlss-swapper and 610 nvidia driver not sure what effects those have)

now it works great just the performance in Extreme-RT isn't as good as it is on windows so i had to put it down to Ultra-RT - otherwise everything working great every once in a while you'll get a stutter but not a big deal. seems like some sort of regression with the new descriptor_heap stuff merged in the latest proton-cachyos from vkd3d-proton

## Comment 4611024628

other (NONE) · eyenalxai · 2026-06-03T09:43:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4611024628

> stutters on AMD GPUs seem to have been fixed on Windows according to this video: https://www.youtube.com/watch?v=QmsM5hfbmwE
> 
> no changes on linux for me. any updates/workarounds on that besides setting textures and geometry to low (still stutters for me on 9060XT)? i think it's more important than having RT on.

perfect performance for me on windows, exactly like in the video, no stutters whatsoever except for initial few related to shader compilation i presume. such a shame :( 

## Comment 4612106200

other (NONE) · fbt · 2026-06-03T12:04:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4612106200

Good news, everyone! A fix for the borked decal menus has been merged into vkd3d-proton: https://github.com/HansKristian-Work/vkd3d-proton/pull/3086

<img width="1920" height="1200" alt="Image" src="https://github.com/user-attachments/assets/1231e8a0-d5ba-4d04-92ad-99350194d2d9" />

## Comment 4615828378

other (NONE) · dyfrgi · 2026-06-03T19:05:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4615828378

OS: NixOS
NVIDIA driver version: 595.71.05
Proton version: bleeding edge
CPU: 9950X3D
GPU: NVIDIA 5080

I have been playing stably on NVIDIA 5080 with no hitching, ultra settings, no RT, with these flags:
`LD_PRELOAD= DISABLE_LOW_LATENCY_LAYER=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap PROTON_VKD3D_HEAP=1 gamescope -W 3440 -H 1440 -w 3440 -h 1440 -f -S integer -r 144 -- %command%`

This is on Proton Bleeding Edge, which got the fh6 workarounds merged into it a few days back. I'm pretty sure that several of these don't do anything with that version and it would be safe to change to this:
`LD_PRELOAD= VKD3D_CONFIG=descriptor_heap gamescope -W 3440 -H 1440 -w 3440 -h 1440 -f -S integer -r 144 -- %command%`

The `LD_PRELOAD=` is necessary to work around https://github.com/ValveSoftware/gamescope/issues/697. You can also put it back for the game itself if you like:
`LD_PRELOAD= VKD3D_CONFIG=descriptor_heap gamescope -W 3440 -H 1440 -w 3440 -h 1440 -f -S integer -r 144 -- LD_PRELOAD="$LD_PRELOAD" %command%`. That will get the Steam overlay back, if that's a thing you want.

gamescope is there to work around https://github.com/Supreeeme/xwayland-satellite/issues/392. You probably don't need it if you aren't using xwayland-satellite.

## Comment 4617400518

other (NONE) · mitchellurgero · 2026-06-03T22:58:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4617400518

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4615828378

How did you get this to work? I'm on the latest nvidia driver (tho on a 3060) and I can't even get the game to load unless I use proton-cachy.


## Comment 4617599051

other (NONE) · dyfrgi · 2026-06-03T23:37:28Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4617599051

> > Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4615828378)
> 
> How did you get this to work? I'm on the latest nvidia driver (tho on a 3060) and I can't even get the game to load unless I use proton-cachy.

Ah, I neglected to mention that I'm running 595.71.05.

## Comment 4618517415

other (NONE) · glarmer · 2026-06-04T02:49:13Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4618517415

> Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4615828378)

For me on a 5080 and the latest nvidia drivers, the most stable configuration is downgrading to proton-cachy [proton-cachyos-11.0-20260506-slr](https://github.com/CachyOS/proton-cachyos/releases/download/cachyos-11.0-20260506-slr) and using the following launch parameters `VKD3D_CONFIG=descriptor_heap PROTON_VKD3D_HEAP=1 %command%`. With this I can set everything to extreme **without** RT. Enabling RT will result in a crash.

The [earlier comments instructions](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4599466153) that aim to get the latest cachy proton working by replacing the VKD3D .DLLs still result in crashes for me even when updating the launch parameters.


## Comment 4620330495

other (NONE) · Cr0phiXx · 2026-06-04T08:20:40Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4620330495

> > Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4615828378)
> 
> For me on a 5080 and the latest nvidia drivers, the most stable configuration is downgrading to proton-cachy proton-cachyos-11.0-20260506-slr and using the following launch parameters `VKD3D_CONFIG=descriptor_heap PROTON_VKD3D_HEAP=1 %command%`. With this I can set everything to extreme **without** RT. Enabling RT will result in a crash.
> 
> The [earlier comments instructions](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4599466153) that aim to get the latest cachy proton working by replacing the VKD3D .DLLs still result in crashes for me even when updating the launch parameters.

~~That's very interesting. Someone else suggested using proton-cachyos-11.0-20260506-slr and I tried that but it didn't work out for me. Especially when "no_upload_hvv,single_queue" are missing in VKD3D_CONFIG. Do you have resizeable BAR enabled in your BIOS?
Also do you still experience stutters or are they gone for you?~~

Edit: Btw the proton-cachyos version you  linked, leads to a 404

Edit2: I retested it with [proton-cachyos-11.0-20260506-slr](https://github.com/CachyOS/proton-cachyos/releases/download/cachyos-11.0-20260506-slr/proton-cachyos-11.0-20260506-slr-x86_64.tar.xz) and the given start commands from other users and I can now confirm that the game even runs without the annoying hitches.
These are my start parameters: `DXVK_FRAME_RATE=120 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=descriptor_heap %command%`

## Comment 4620637142

other (NONE) · urwrstkn8mare · 2026-06-04T09:02:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4620637142

@Cr0phiXx what nvidia drivers are u using? it worked for me with the 610 drivers, resizable bar enabled in bios, and no other vkd3d_config other than descriptor_heap (also PROTON_VKD3D_HEAP=1)

## Comment 4621541190

other (NONE) · Cr0phiXx · 2026-06-04T11:03:42Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4621541190

> [@Cr0phiXx](https://github.com/Cr0phiXx) what nvidia drivers are u using? it worked for me with the 610 drivers, resizable bar enabled in bios, and no other vkd3d_config other than descriptor_heap (also PROTON_VKD3D_HEAP=1)

I have 610.43 installed. I also updated my comment above. I must have forgotten to add PROTON_VKD3D_HEAP=1, when I tested proton-cachyos-11.0-20260506-slr yesterday.
With the given start parameters the game now runs smooth. Not the same performance as on windows but the annoying fps dips are gone.

## Comment 4624216394

other (NONE) · fbt · 2026-06-04T16:39:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4624216394

A thing that completely slipped my mind is that because the commit that outright breaks Horizon 6 is the one that enables the workarounds for the game... you can just disable the workarounds if you use an nvidia card. With this, the latest vkd3d-proton, and 610 drivers, the game runs fine for me: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds`

The workarounds seem to only affect amd anyway.

The one issue that still persists on my end is this problem with being ghosted in FP (with or without the workarounds): 

<img width="1920" height="1200" alt="Image" src="https://github.com/user-attachments/assets/46a504d4-d680-4ce1-90b8-38c7c0c05ad7" />

## Comment 4624428003

other (NONE) · leberschnitzel · 2026-06-04T17:06:52Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4624428003

I'm playing on
AMD Ryzen 7 7800X3D
AMD Radeon RX 9070 XT
64 GB RAM

I use Proton-CachyOS Latest (which as of writing is 11.0-20260521-slr)
as start command I use `VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%`
In game I still put Environment Textures to Low to reduce stutters.
But it works nicely now, even with raytracing

With Environment Texture Quality on extreme:

<img width="3440" height="1440" alt="Image" src="https://github.com/user-attachments/assets/7c114c97-e172-49f0-bef9-fab223351962" />

On Low:

<img width="3440" height="1440" alt="Image" src="https://github.com/user-attachments/assets/d1c42a03-ccce-49e0-9b3b-4663f06dccb3" />

The stutters are just massively better like that.
For me that works well enough, but getting rid of the stutters somehow would be great.

## Comment 4626156859

other (NONE) · mattredact · 2026-06-04T21:15:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4626156859

Anyone seeing the high-speed / area-transition stutter improve on 26.1.2, or is it the same?

## Comment 4636430451

other (NONE) · CRKrJ4K · 2026-06-05T23:42:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4636430451

> Anyone seeing the high-speed / area-transition stutter improve on 26.1.2, or is it the same?

if you are referring to mesa, I'm on 26.2 & there is no change in stutters/hesitations

`PC: 14900KS, 7900 XTX`

## Comment 4649636375

other (NONE) · phamaralbr · 2026-06-08T13:48:30Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4649636375

Hey everyone, if you are still experiencing stuttering, please take a moment to vote on the issue and select your GPU over at [forzafeedback](https://forzafeedback.atlassian.net/servicedesk/customer/portal/36/FH6BR-196). The developers reset the vote count after the last hotfix, but the performance issues persist. We need to keep this on their radar to ensure it gets addressed.

## Comment 4652877158

other (NONE) · Shijikori · 2026-06-08T19:51:09Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4652877158

upgrading Mesa to the 26.0.8 drivers in the resolute-proposed repo helped out with graphical issues. at least it minimised them. I still have occasional issues with the terrain. Some changes in graphical settings and increasing the local Mesa shader cache seems to have mitigated this further.
This is the full set of launch options I run now:
```
RADV_EXPERIMENTAL=heap MESA_SHADER_CACHE_MAX_SIZE=10G radv_wait_for_vm_map_updates=true %command%
```
technically, the heap environment variable and the wait for vm map updates variable are not necessary. It's just to force the driver to use the fixes implemented to address issues with the game.

I also tried forcing anisotropic filtering to 8x but that seems to heavily impact the resolution of car liveries so i'm no longer setting it.


## Comment 4665049245

other (NONE) · CRKrJ4K · 2026-06-09T23:34:43Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4665049245

> Hey everyone, if you are still experiencing stuttering, please take a moment to vote on the issue and select your GPU over at [forzafeedback](https://forzafeedback.atlassian.net/servicedesk/customer/portal/36/FH6BR-196). The developers reset the vote count after the last hotfix, but the performance issues persist. We need to keep this on their radar to ensure it gets addressed.

voted, but there's no point in commenting explaining your system setup. They've already closed a Linux topic with the community manager stating `The PC version of Forza Horizon 6 is supported on Windows 10 / 11 and SteamOS devices. The game is not supported on Linux.`, and I don't think he liked it when everyone pointed out SteamOS is obviously Linux.

## Comment 4673961839

other (NONE) · mkopec · 2026-06-10T20:02:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4673961839

Game spawns 2 windows, one real game window and one black fullscreen window. With PROTON_ENABLE_WAYLAND=1, switching focus between the two results in:

```
Assertion failed: `!status && "vkGetPastPresentationTimingEXT"` in `dlls/winevulkan/loader_thunks.c:5414`
```

Tested on GE-Proton and proton-cachyos, on Sway, with a 9070 XT. Has anyone seen the same behavior? I'd switch to upstream Proton, but the lack of HDR is a bit of a deal breaker :(

## Comment 4674802216

other (NONE) · mattredact · 2026-06-10T21:38:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4674802216

Same issue on my 9070XT on Hyprland.

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4673961839



## Comment 4701375880

other (NONE) · itsmeadarsh2008 · 2026-06-14T09:48:41Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4701375880

AFAIK, Forza Horizon 6 is working fine on Proton-CachyOS, while I am getting on FHE01, FHE00 like errors on Fedora KDE Plasma (Using Proton Hotfix and Experimental both), I have NVIDIA Graphics.

## Comment 4701501305

other (NONE) · jpietek · 2026-06-14T10:44:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4701501305

Any update on raytracing on Nvidia? Is the root cause why it crashes known and described somewhere?

## Comment 4701505074

other (NONE) · oneandonlyno1 · 2026-06-14T10:46:29Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4701505074

> Any update on raytracing on Nvidia? Is the root cause why it crashes known and described somewhere?

Raytracing and frame gen works fine - driver 610 on Cachyos + proton Cachyos slr 21 05 

## Comment 4701744175

other (NONE) · Cr0phiXx · 2026-06-14T12:28:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4701744175

> > Any update on raytracing on Nvidia? Is the root cause why it crashes known and described somewhere?
> 
> Raytracing and frame gen works fine - driver 610 on Cachyos + proton Cachyos slr 21 05 

Can you explain what start parameters you use? Because I use that proton + driver combination you said works but enabling Global Illumination Raytracing crashes the game the moment i leave the options menu.

Edit: I double checked again. Enabling Raytraced Reflections works but Raytraced Global Illumination (GI) still crashes the game instantly.

## Comment 4712317150

other (NONE) · Skeletonek · 2026-06-15T20:49:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4712317150

Tested the new update (375.327) and unfortunately for the AMD cards the stuttering is still not fixed

Tested on Arch Linux with Proton CachyOS 11 20260521-slr
GPU: AMD Radeon RX 9070

## Comment 4712668330

other (NONE) · Deytron · 2026-06-15T21:38:54Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4712668330

> Tested the new update (375.327) and unfortunately for the AMD cards the stuttering is still not fixed
> 
> Tested on Arch Linux with Proton CachyOS 11 20260521-slr GPU: AMD Radeon RX 9070

Oh my god will they fix it one day

## Comment 4713089643

other (NONE) · oneandonlyno1 · 2026-06-15T22:47:24Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4713089643

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4701744175

```
PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap gamescope -W 3440 -H 1440 -w 3440 -h 1440 -r 175 -f --force-grab-cursor --  %command%
```

replace 3440/1440 with your screen width and height, and 175 with your screen refresh rate

proton-cachyos-11.0-20260520-slr-x86_64_v3  - this is exact version of proton
```
NVIDIA-SMI 610.43.02              KMD Version: 610.43.02     CUDA UMD Version: 13.3 
```
those are drivers & libs - and as I said - with this combo basically everything works for me - preset RT ULTRA on 4080 with enabled framegen x3 and every RT feature - however some stutters can be observed when maxed out - game feels less playable with the RT features enabled

also, if you had issue with "low resolution being upscaled to high resolution" using the gamescope with params I gave above - press alt enter - it will switch to true fullscreen mode and switch from 480p -> 1440p upscaling to true 1440p rendering and work perfectly fine 




## Comment 4713831687

other (NONE) · RafaelHGOliveira · 2026-06-16T00:48:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4713831687

Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4701744175

Worked for me without gamescope. Game runs fine, but it crashes as soon as I enable RT.

## Comment 4713937741

other (NONE) · glarmer · 2026-06-16T01:12:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4713937741

Use `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds` to get RT to work on latest CachyOS proton + nvidia 610.43.02, as noted earlier in the thread one of the VKD3D commits causes issues and this circumvents it. 

While it is playable, there are still a fair few issues with RT though in my experience:
- Changing frame-gen options in game can cause weird behaviour until relaunching the game
- Some parts of some cars in some situations will render transparently
- Some smoke effects occasionally render all pixelly - most obvious with the red smoke checkpoints on the night time street races

## Comment 4716244726

other (NONE) · Cr0phiXx · 2026-06-16T07:58:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4716244726

> Use `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds` to get RT to work on latest CachyOS proton + nvidia 610.43.02, as noted earlier in the thread one of the VKD3D commits causes issues and this circumvents it.
> 
> While it is playable, there are still a fair few issues with RT though in my experience:
> 
>     * Changing frame-gen options in game can cause weird behaviour until relaunching the game
> 
>     * Some parts of some cars in some situations will render transparently
 
How is the performance with that? I remember really annoying stutters with any proton version different than `proton-cachyos-20260506`.

 
>     * Some smoke effects occasionally render all pixelly - most obvious with the red smoke checkpoints on the night time street races

This was mentioned in the latest changelogs. Should be fixed with the latest update from the Game itself. 

## Comment 4718498301

other (NONE) · Redemption198 · 2026-06-16T12:02:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4718498301

On my Steam Deck LCD, SteamOS 3.8.9 Build: 20260612.1, Proton Experimental my usb gamepad inputs get queued/delayed after playing for a while. Fox example, in a menu I quickly spam the left stick and let go, the UI selection keeps moving for a while, then stops.

## Comment 4719002424

maintainer (MEMBER) · kisak-valve · 2026-06-16T13:01:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4719002424

Forza Horizon 6 / Mint / Nvidia - Game not starting

Issue transferred from https://github.com/ValveSoftware/Proton/issues/9877.
@SolarMyth79 posted on 2026-06-16T09:36:17:

# Compatibility Report
- Forza Horizon 6
- Steam AppID: 2483190

## System Information
- NVIDIA GeForce RTX 3060 Ti/PCIe/SSE2
- Video driver version: 4.6.0 NVIDIA 595.71.05
- AMD Ryzen 5 7600X
- Linux Mint 22.3 (64 bit)
- Kernel Version: 6.8.0-124-generic
- Proton version: Experimental

## I confirm:
- [x] that I haven't found an existing compatibility report for this game.
- [x] that I have checked whether there are updates for my system available.

## Symptoms <!-- What's the problem? -->

Game does not start in Steam.  "Play" button turns to "Launching" then "Running", stays like that for about a minute, then turns back to "Play".

[steam-2483190.log](https://github.com/user-attachments/files/28995354/steam-2483190.log)

https://gist.github.com/SolarMyth79/c4f5f1c3f7b4646531d3efc47b33140b

## Comment 4724243946

other (NONE) · mattredact · 2026-06-16T22:44:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4724243946

Is micro stuttering still an issue on the 9070XT since the patch yesterday? 

## Comment 4731643541

other (NONE) · eyenalxai · 2026-06-17T14:39:44Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4731643541

> Is micro stuttering still an issue on the 9070XT since the patch yesterday?

Still stutters on 9060XT even on the lowest settings. 

edit: also compared to windows where I can play at 1440p with FSR 4 AA (so no upscaling) on Extreme settings at a stable 75 FPS, i can't even reach 75 FPS on linux when the stutters don't happen on identical settings. not to mention that you can't upgrade to FSR 4 from FSR 3 even when using Proton-GE. all of this is a huge reduction in quality of experience. 

## Comment 4734116957

other (NONE) · itsmeadarsh2008 · 2026-06-17T18:50:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4734116957

Day 34 of asking to release a patch for Forza Horizon 6, when I use any Launch commands, I just get Black Screen. Fedora KDE Plasma on every Proton version: I have tried the CachyOS one too. I have an Nvidia GeForce RTX 3050, but it still crashes. Is this because of the new 610 ver of Nvidia Proprietary Drivers?

## Comment 4736217810

other (NONE) · fbt · 2026-06-17T22:51:26Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4736217810

> I have an Nvidia GeForce RTX 3050, but it still crashes. Is this because of the new 610 ver of Nvidia Proprietary Drivers?

If you're running a pre-Blackwell Nvidia GPU with 610 drivers, the current workarounds for Horizon 6 in vkd3d-proton cause a crash with descriptor_heap, yes. It has been root caused to the driver itself, so we're waiting for a fix. Without descriptor_heap it just crashes a bit later.

Meanwhile, you can disable application workarounds (and enable the one that works explicitly):
`VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing`

If your game crashes on resolution/focus changes, you might also want to add `VKD3D_DISABLE_EXTENSIONS=VK_EXT_present_timing`. In my case this stops the game from sometimes crashing on switching desktops.

## Comment 4757980684

other (NONE) · vultux · 2026-06-20T12:57:39Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4757980684

>I have an Nvidia GeForce RTX 3050, but it still crashes. Is this because of the new 610 ver of Nvidia Proprietary Drivers?
Try with **proton-cachyos-11.0-20260520-slr-x86**

**Startup Options** _(adapt to your PC configuration)_
`VKD3D_CONFIG=descriptor_heap VKD3D_FRAME_RATE=120 gamescope -W 3840 -H 2160 -r 120 --adaptive-sync --hdr-enabled --mangoapp --force-grab-cursor --rt -f -- %command%`

## Comment 4758411855

other (NONE) · itsmeadarsh2008 · 2026-06-20T14:10:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758411855

> > I have an Nvidia GeForce RTX 3050, but it still crashes. Is this because of the new 610 ver of Nvidia Proprietary Drivers?
> > Try with **proton-cachyos-11.0-20260520-slr-x86**
> 
> **Startup Options** _(adapt to your PC configuration)_ VKD3D_CONFIG=descriptor_heap VKD3D_FRAME_RATE=120 gamescope -W 3840 -H 2160 -r 120 --adaptive-sync --hdr-enabled --mangoapp --force-grab-cursor --rt -f %command%

Will this work on a 1080p monitor? Will work on newest nvidia drivers?

## Comment 4758578070

other (NONE) · vultux · 2026-06-20T14:47:52Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758578070

> Will this work on a 1080p monitor? Will work on newest nvidia drivers?

You have to test it. It works in my setup with the latest Nvidia driver on Arch Linux with CachyOS Kernel.

`cat /sys/module/nvidia/version`
`610.43.02`

Unfortunately Linux has a lot of variation, so it's not guaranteed that what works for one user will work for everyone.

Only on FH6 I have to use this version of proton: `proton-cachyos-11.0-20260520-slr-x86` in the other games it works without problem with the latest version: `proton-cachyos-11.0-20260601-slr-x86`

Remember to change the initialization option for your setup, change Frame_Rate to your monitor frame rate and `-r` too.

Something like this: `VKD3D_CONFIG=descriptor_heap VKD3D_FRAME_RATE=120 gamescope -W 1920 -H 1080 -r 120 --adaptive-sync --hdr-enabled --mangoapp --force-grab-cursor --rt -f %command%`

## Comment 4758758545

other (NONE) · itsmeadarsh2008 · 2026-06-20T15:30:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758758545

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758578070

<details><summary>Bro, gamescope is crashing for some reason, also the logs don't appear to be readable. I am on Fedora KDE Plasma 44</summary>

<img width="690" height="198" alt="Image" src="https://github.com/user-attachments/assets/734f1c26-b2c6-4b19-afdf-3b8903da6658" />

```
           PID: 130594 (gamescope-wl)
           UID: 1000 (adarsh)
           GID: 1000 (adarsh)
        Signal: 6 (ABRT)
     Timestamp: Sat 2026-06-20 20:59:45 IST (3s ago)
  Command Line: gamescope -W 1920 -H 1080 -r 120 --adaptive-sync --hdr-enabled --mangoapp --force-grab-cursor --rt -f /home/adarsh/.local/share/Steam/ubuntu12_32/steam-launch-wrapper -- /home/adarsh/.local/share/Steam/ubuntu12_32/reaper SteamLaunch AppId=2483190 -- /home/adarsh/.local/share/Steam/steamapps/common/SteamLinuxRuntime_4/_v2-entry-point --verb=waitforexitandrun -- /home/adarsh/.local/share/Steam/compatibilitytools.d/cachyos-11.0-20260520-slr/proton waitforexitandrun /home/adarsh/.local/share/Steam/steamapps/common/ForzaHorizon6/forzahorizon6.exe
    Executable: /usr/bin/gamescope
 Control Group: /user.slice/user-1000.slice/user@1000.service/app.slice/app-steam@05bc6e243bdd461584fff61231273e4e.service
          Unit: user@1000.service
     User Unit: app-steam@05bc6e243bdd461584fff61231273e4e.service
         Slice: user-1000.slice
     Owner UID: 1000 (adarsh)
       Boot ID: 2577c9b99cb64dc1acdb4e59f661f733
    Machine ID: 45e738370c4449a88054dfb943e39fbe
      Hostname: fedora
       Storage: /var/lib/systemd/coredump/core.gamescope-wl.1000.2577c9b99cb64dc1acdb4e59f661f733.130594.1781969385000000.zst (present)
  Size on Disk: 16.6M
       Package: gamescope/3.16.23-1.fc44
      build-id: f87d2da84016572464de52497cb8a0f1ee478eeb
       Message: Process 130594 (gamescope-wl) of user 1000 dumped core.
                
                Module libspa-videoconvert.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-session-manager.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-metadata.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-adapter.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-client-device.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-client-node.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-protocol-native.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libpipewire-module-rt.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libspa-dbus.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libspa-journal.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libspa-support.so from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libVkLayer_MESA_device_select.so from rpm mesa-26.0.8-1.fc44.x86_64
                Module libxcb-sync.so.1 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libX11-xcb.so.1 from rpm libX11-1.8.13-1.fc44.x86_64
                Module libxcb-randr.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-glx.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libgvfscommon.so from rpm gvfs-1.60.0-1.fc44.x86_64
                Module libgvfsdbus.so from rpm gvfs-1.60.0-1.fc44.x86_64
                Module libdconfsettings.so from rpm dconf-0.49.0-5.fc44.x86_64
                Module libseccomp.so.2 from rpm libseccomp-2.6.0-3.fc44.x86_64
                Module libsqlite3.so.0 from rpm sqlite-3.51.2-1.fc44.x86_64
                Module libjson-glib-1.0.so.0 from rpm json-glib-1.10.8-5.fc44.x86_64
                Module libatspi.so.0 from rpm at-spi2-core-2.60.4-1.fc44.x86_64
                Module libglycin-2.so.0 from rpm glycin-2.1.1-1.fc44.x86_64
                Module libXinerama.so.1 from rpm libXinerama-1.1.5-10.fc44.x86_64
                Module libXrandr.so.2 from rpm libXrandr-1.5.4-7.fc44.x86_64
                Module libwayland-egl.so.1 from rpm wayland-1.24.0-3.fc44.x86_64
                Module libtinysparql-3.0.so.0 from rpm tinysparql-3.11.1-1.fc44.x86_64
                Module libcloudproviders.so.0 from rpm libcloudproviders-0.4.0-1.fc44.x86_64
                Module libatk-bridge-2.0.so.0 from rpm at-spi2-core-2.60.4-1.fc44.x86_64
                Module libepoxy.so.0 from rpm libepoxy-1.5.10-12.fc44.x86_64
                Module libatk-1.0.so.0 from rpm at-spi2-core-2.60.4-1.fc44.x86_64
                Module libgdk_pixbuf-2.0.so.0 from rpm gdk-pixbuf2-2.44.4-2.fc44.x86_64
                Module libcairo-gobject.so.2 from rpm cairo-1.18.4-6.fc44.x86_64
                Module libgdk-3.so.0 from rpm gtk3-3.24.52-1.fc44.x86_64
                Module libgtk-3.so.0 from rpm gtk3-3.24.52-1.fc44.x86_64
                Module libdecor-gtk.so from rpm libdecor-0.2.5-2.fc44.x86_64
                Module libbrotlicommon.so.1 from rpm brotli-1.2.0-3.fc44.x86_64
                Module libblkid.so.1 from rpm util-linux-2.41.4-8.fc44.x86_64
                Module liblzma.so.5 from rpm xz-5.8.2-2.fc44.x86_64
                Module libbrotlidec.so.1 from rpm brotli-1.2.0-3.fc44.x86_64
                Module libbz2.so.1 from rpm bzip2-1.0.8-23.fc44.x86_64
                Module libdatrie.so.1 from rpm libdatrie-0.2.14-2.fc44.x86_64
                Module libselinux.so.1 from rpm libselinux-3.10-1.fc44.x86_64
                Module libmount.so.1 from rpm util-linux-2.41.4-8.fc44.x86_64
                Module libgmodule-2.0.so.0 from rpm glib2-2.88.1-1.fc44.x86_64
                Module libxml2.so.2 from rpm libxml2-2.12.10-6.fc44.x86_64
                Module libgraphite2.so.3 from rpm graphite2-1.3.14-20.fc44.x86_64
                Module libfreetype.so.6 from rpm freetype-2.14.3-1.fc44.x86_64
                Module libpng16.so.16 from rpm libpng-1.6.58-1.fc44.x86_64
                Module libz.so.1 from rpm zlib-ng-2.3.3-3.fc44.x86_64
                Module libthai.so.0 from rpm libthai-0.1.30-2.fc44.x86_64
                Module libfribidi.so.0 from rpm fribidi-1.0.16-4.fc44.x86_64
                Module libgio-2.0.so.0 from rpm glib2-2.88.1-1.fc44.x86_64
                Module libfontconfig.so.1 from rpm fontconfig-2.17.0-4.fc44.x86_64
                Module libharfbuzz.so.0 from rpm harfbuzz-14.1.0-2.fc44.x86_64
                Module libpangoft2-1.0.so.0 from rpm pango-1.57.1-1.fc44.x86_64
                Module libdbus-1.so.3 from rpm dbus-1.16.2-1.fc44.x86_64
                Module libwayland-cursor.so.0 from rpm wayland-1.24.0-3.fc44.x86_64
                Module libcairo.so.2 from rpm cairo-1.18.4-6.fc44.x86_64
                Module libpango-1.0.so.0 from rpm pango-1.57.1-1.fc44.x86_64
                Module libpangocairo-1.0.so.0 from rpm pango-1.57.1-1.fc44.x86_64
                Module libSDL3.so.0 from rpm SDL3-3.4.10-1.fc44.x86_64
                Module libpcre2-8.so.0 from rpm pcre2-10.47-1.fc44.1.x86_64
                Module libuuid.so.1 from rpm util-linux-2.41.4-8.fc44.x86_64
                Module libglib-2.0.so.0 from rpm glib2-2.88.1-1.fc44.x86_64
                Module libgobject-2.0.so.0 from rpm glib2-2.88.1-1.fc44.x86_64
                Module libgudev-1.0.so.0 from rpm libgudev-238-9.fc44.x86_64
                Module libvmaf.so.3 from rpm vmaf-3.0.0-5.fc44.x86_64
                Module libjpeg.so.62 from rpm libjpeg-turbo-3.1.3-1.fc44.x86_64
                Module libICE.so.6 from rpm libICE-1.1.2-4.fc44.x86_64
                Module libSM.so.6 from rpm libSM-1.2.5-4.fc44.x86_64
                Module libsystemd.so.0 from rpm systemd-259.6-1.fc44.x86_64
                Module libexpat.so.1 from rpm expat-2.8.1-1.fc44.x86_64
                Module libXau.so.6 from rpm libXau-1.0.12-4.fc44.x86_64
                Module libGLdispatch.so.0 from rpm libglvnd-1.7.0-9.fc44.x86_64
                Module libGLX.so.0 from rpm libglvnd-1.7.0-9.fc44.x86_64
                Module liblua-5.4.so from rpm lua-5.4.8-5.fc44.x86_64
                Module libwacom.so.9 from rpm libwacom-2.19.0-1.fc44.x86_64
                Module libevdev.so.2 from rpm libevdev-1.13.6-2.fc44.x86_64
                Module libmtdev.so.1 from rpm mtdev-1.1.6-12.fc44.x86_64
                Module libaom.so.3 from rpm aom-3.13.3-1.fc44.x86_64
                Module libSvtAv1Enc.so.3 from rpm svt-av1-3.1.2-2.fc44.x86_64
                Module librav1e.so.0 from rpm rust-rav1e-0.8.1-3.fc44.x86_64
                Module libdav1d.so.7 from rpm dav1d-1.5.3-1.fc44.x86_64
                Module libyuv.so.0 from rpm libyuv-0-0.61.20260213git6067afd.fc44.x86_64
                Module libjsoncpp.so.26 from rpm jsoncpp-1.9.6-3.fc44.x86_64
                Module libXt.so.6 from rpm libXt-1.3.1-4.fc44.x86_64
                Module libxcb-errors.so.0 from rpm xcb-util-errors-1.0.1-7.fc44.x86_64
                Module libxcb-res.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-icccm.so.4 from rpm xcb-util-wm-0.4.2-9.fc44.x86_64
                Module libxcb-ewmh.so.2 from rpm xcb-util-wm-0.4.2-9.fc44.x86_64
                Module libxcb-composite.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-xinput.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-xfixes.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-shm.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-render-util.so.0 from rpm xcb-util-renderutil-0.3.10-9.fc44.x86_64
                Module libxcb-render.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-present.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libxcb-dri3.so.0 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libseat.so.1 from rpm seatd-0.9.3-1.fc44.x86_64
                Module liblcms2.so.2 from rpm lcms2-2.16-7.fc44.x86_64
                Module libvulkan.so.1 from rpm vulkan-loader-1.4.341.0-1.fc44.x86_64
                Module libGLESv2.so.2 from rpm libglvnd-1.7.0-9.fc44.x86_64
                Module libgbm.so.1 from rpm mesa-26.0.8-1.fc44.x86_64
                Module libEGL.so.1 from rpm libglvnd-1.7.0-9.fc44.x86_64
                Module libxcb.so.1 from rpm libxcb-1.17.0-7.fc44.x86_64
                Module libffi.so.8 from rpm libffi-3.5.2-2.fc44.x86_64
                Module libGL.so.1 from rpm libglvnd-1.7.0-9.fc44.x86_64
                Module libudev.so.1 from rpm systemd-259.6-1.fc44.x86_64
                Module libpixman-1.so.0 from rpm pixman-0.46.2-3.fc44.x86_64
                Module libinput.so.10 from rpm libinput-1.31.3-1.fc44.x86_64
                Module libluajit-5.1.so.2 from rpm luajit-2.1.1767980792-1.fc44.x86_64
                Module libeis.so.1 from rpm libei-1.5.0-2.fc44.x86_64
                Module libdecor-0.so.0 from rpm libdecor-0.2.5-2.fc44.x86_64
                Module libXi.so.6 from rpm libXi-1.8.3-1.fc44.x86_64
                Module libavif.so.16 from rpm libavif-1.3.0-4.fc44.x86_64
                Module libXcursor.so.1 from rpm libXcursor-1.2.3-4.fc44.x86_64
                Module libopenvr_api.so.2.0.0 from rpm openvr-2.12.14-2.fc44.x86_64
                Module libdisplay-info.so.3 from rpm libdisplay-info-0.3.0-1.fc44.x86_64
                Module libpipewire-0.3.so.0 from rpm pipewire-1.6.6-1.fc44.x86_64
                Module libcap.so.2 from rpm libcap-2.78-1.fc44.x86_64
                Module libXmu.so.6 from rpm libXmu-1.2.1-5.fc44.x86_64
                Module libXtst.so.6 from rpm libXtst-1.2.5-4.fc44.x86_64
                Module libliftoff.so.0 from rpm libliftoff-0.5.0-5.fc44.x86_64
                Module libwlroots-0.18.so from rpm wlroots0.18-0.18.3-5.fc44.x86_64
                Module libSDL2-2.0.so.0 from rpm sdl2-compat-2.32.68-1.fc44.x86_64
                Module libxkbcommon.so.0 from rpm libxkbcommon-1.13.1-2.fc44.x86_64
                Module libwayland-server.so.0 from rpm wayland-1.24.0-3.fc44.x86_64
                Module libdrm.so.2 from rpm libdrm-2.4.134-1.fc44.x86_64
                Module libXRes.so.1 from rpm libXres-1.2.2-7.fc44.x86_64
                Module libXxf86vm.so.1 from rpm libXxf86vm-1.1.6-4.fc44.x86_64
                Module libXext.so.6 from rpm libXext-1.3.6-5.fc44.x86_64
                Module libXrender.so.1 from rpm libXrender-0.9.12-4.fc44.x86_64
                Module libXcomposite.so.1 from rpm libXcomposite-0.4.6-7.fc44.x86_64
                Module libXfixes.so.3 from rpm libXfixes-6.0.1-7.fc44.x86_64
                Module libXdamage.so.1 from rpm libXdamage-1.1.6-7.fc44.x86_64
                Module libX11.so.6 from rpm libX11-1.8.13-1.fc44.x86_64
                Module libwayland-client.so.0 from rpm wayland-1.24.0-3.fc44.x86_64
                Module gamescope from rpm gamescope-3.16.23-1.fc44.x86_64
                Stack trace of thread 130597:
                #0  0x00007f42f8e7bdcc __pthread_kill_implementation (libc.so.6 + 0x74dcc)
                #1  0x00007f42f8e20f8e raise (libc.so.6 + 0x19f8e)
                #2  0x00007f42f8e087b3 abort (libc.so.6 + 0x17b3)
                #3  0x000055a87e7d1140 _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZN9gamescope19CWaylandInputThreadC4EvEUlvE_EEEEE6_M_runEv (gamescope + 0x6a140)
                #4  0x00007f42f90523b6 execute_native_thread_routine (libstdc++.so.6 + 0x523b6)
                #5  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #6  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130594:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8eefe7e __poll (libc.so.6 + 0xe8e7e)
                #4  0x000055a87e830bf3 _Z12wlserver_runv (gamescope + 0xc9bf3)
                #5  0x000055a87e7a0ee7 main (gamescope + 0x39ee7)
                #6  0x00007f42f8e0a681 __libc_start_call_main (libc.so.6 + 0x3681)
                #7  0x00007f42f8e0a798 __libc_start_main@@GLIBC_2.34 (libc.so.6 + 0x3798)
                #8  0x000055a87e7b8605 _start (gamescope + 0x51605)
                
                Stack trace of thread 130598:
                #0  0x00007f42f8efb3fd syscall (libc.so.6 + 0xf43fd)
                #1  0x00007f42f72cf4eb g_cond_wait (libglib-2.0.so.0 + 0x784eb)
                #2  0x00007f42f726158c g_async_queue_pop_intern_unlocked (libglib-2.0.so.0 + 0xa58c)
                #3  0x00007f42f7261605 g_async_queue_pop (libglib-2.0.so.0 + 0xa605)
                #4  0x00007f42eac2b74c fc_thread_func (libpangoft2-1.0.so.0 + 0x474c)
                #5  0x00007f42f72d4d12 g_thread_proxy (libglib-2.0.so.0 + 0x7dd12)
                #6  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #7  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130595:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8efd935 epoll_wait (libc.so.6 + 0xf6935)
                #4  0x000055a87e8109dd _ZN9gamescope7CWaiterILm1024EE10PollEventsEi.constprop.0.isra.0 (gamescope + 0xa99dd)
                #5  0x000055a87e82df28 _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZN9gamescope12CAsyncWaiterINS3_11CRawPointerINS3_9IWaitableEEELm1024EEC4EPKcEUlvE_EEEEE6_M_runEv (gamescope + 0xc6f28)
                #6  0x00007f42f90523b6 execute_native_thread_routine (libstdc++.so.6 + 0x523b6)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130596:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8efd935 epoll_wait (libc.so.6 + 0xf6935)
                #4  0x000055a87e8109dd _ZN9gamescope7CWaiterILm1024EE10PollEventsEi.constprop.0.isra.0 (gamescope + 0xa99dd)
                #5  0x000055a87e81ccc8 _ZNSt6thread11_State_implINS_8_InvokerISt5tupleIJZN9gamescope12CAsyncWaiterINS3_2RcI8commit_tLb1EEELm1024EEC4EPKcEUlvE_EEEEE6_M_runEv (gamescope + 0xb5cc8)
                #6  0x00007f42f90523b6 execute_native_thread_routine (libstdc++.so.6 + 0x523b6)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130601:
                #0  0x00007f42f8efb3fd syscall (libc.so.6 + 0xf43fd)
                #1  0x00007f42f72d04a9 g_cond_wait_until (libglib-2.0.so.0 + 0x794a9)
                #2  0x00007f42f726154d g_async_queue_pop_intern_unlocked (libglib-2.0.so.0 + 0xa54d)
                #3  0x00007f42f72d6b12 g_thread_pool_thread_proxy (libglib-2.0.so.0 + 0x7fb12)
                #4  0x00007f42f72d4d12 g_thread_proxy (libglib-2.0.so.0 + 0x7dd12)
                #5  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #6  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130602:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8ef04a6 ppoll (libc.so.6 + 0xe94a6)
                #4  0x00007f42f729f125 g_main_context_iterate_unlocked.isra.0 (libglib-2.0.so.0 + 0x48125)
                #5  0x00007f42f729f2e7 g_main_loop_run (libglib-2.0.so.0 + 0x482e7)
                #6  0x00007f42ea9a16c2 gdbus_shared_thread_func.lto_priv.0 (libgio-2.0.so.0 + 0xf76c2)
                #7  0x00007f42f72d4d12 g_thread_proxy (libglib-2.0.so.0 + 0x7dd12)
                #8  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #9  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130600:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8ef04a6 ppoll (libc.so.6 + 0xe94a6)
                #4  0x00007f42f729f125 g_main_context_iterate_unlocked.isra.0 (libglib-2.0.so.0 + 0x48125)
                #5  0x00007f42f729f1e3 g_main_context_iteration (libglib-2.0.so.0 + 0x481e3)
                #6  0x00007f42f729f231 glib_worker_main (libglib-2.0.so.0 + 0x48231)
                #7  0x00007f42f72d4d12 g_thread_proxy (libglib-2.0.so.0 + 0x7dd12)
                #8  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #9  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130605:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76977 __GI___futex_abstimed_wait_cancelable64 (libc.so.6 + 0x6f977)
                #3  0x00007f42f8e793e2 pthread_cond_timedwait@@GLIBC_2.3.2 (libc.so.6 + 0x723e2)
                #4  0x00007f42f51f4f5c n/a (libnvidia-glcore.so.610.43.02 + 0x9f4f5c)
                #5  0x00007f42f5645a11 n/a (libnvidia-glcore.so.610.43.02 + 0xe45a11)
                #6  0x00007f42f51f5114 n/a (libnvidia-glcore.so.610.43.02 + 0x9f5114)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130613:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76977 __GI___futex_abstimed_wait_cancelable64 (libc.so.6 + 0x6f977)
                #3  0x00007f42f8e793e2 pthread_cond_timedwait@@GLIBC_2.3.2 (libc.so.6 + 0x723e2)
                #4  0x00007f42e1dde63c n/a (libVkLayer_steam_fossilize.so + 0x6063c)
                #5  0x00007f42e1e4f540 n/a (libVkLayer_steam_fossilize.so + 0xd1540)
                #6  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #7  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130614:
                #0  0x00007f42ef619746 n/a (libnvidia-gpucomp.so.610.43.02 + 0x1a19746)
                #1  0x00007f42ef637d56 n/a (libnvidia-gpucomp.so.610.43.02 + 0x1a37d56)
                #2  0x00007f42ef638971 n/a (libnvidia-gpucomp.so.610.43.02 + 0x1a38971)
                #3  0x00007f42ef63902f n/a (libnvidia-gpucomp.so.610.43.02 + 0x1a3902f)
                #4  0x00007f42ee1f783e n/a (libnvidia-gpucomp.so.610.43.02 + 0x5f783e)
                #5  0x00007f42ef244c31 n/a (libnvidia-gpucomp.so.610.43.02 + 0x1644c31)
                #6  0x00007f42ee1f788e n/a (libnvidia-gpucomp.so.610.43.02 + 0x5f788e)
                #7  0x00007f42ef245013 n/a (libnvidia-gpucomp.so.610.43.02 + 0x1645013)
                #8  0x00007f42ee0b9bfe n/a (libnvidia-gpucomp.so.610.43.02 + 0x4b9bfe)
                #9  0x00007f42ef2461b1 n/a (libnvidia-gpucomp.so.610.43.02 + 0x16461b1)
                #10 0x00007f42ee0f7d96 n/a (libnvidia-gpucomp.so.610.43.02 + 0x4f7d96)
                #11 0x00007f42e12a2024 n/a (libnvidia-glvkspirv.so.610.43.02 + 0xa2024)
                #12 0x00007f42e12a2836 _nv002nvvm (libnvidia-glvkspirv.so.610.43.02 + 0xa2836)
                #13 0x00007f42f5672306 n/a (libnvidia-glcore.so.610.43.02 + 0xe72306)
                #14 0x00007f42f567afe2 n/a (libnvidia-glcore.so.610.43.02 + 0xe7afe2)
                #15 0x00007f42f567cdfa n/a (libnvidia-glcore.so.610.43.02 + 0xe7cdfa)
                #16 0x00007f42f57a58db n/a (libnvidia-glcore.so.610.43.02 + 0xfa58db)
                #17 0x00007f42f567dd67 n/a (libnvidia-glcore.so.610.43.02 + 0xe7dd67)
                #18 0x00007f42f567e125 n/a (libnvidia-glcore.so.610.43.02 + 0xe7e125)
                #19 0x00007f42f5795f00 n/a (libnvidia-glcore.so.610.43.02 + 0xf95f00)
                #20 0x00007f42f551cd05 n/a (libnvidia-glcore.so.610.43.02 + 0xd1cd05)
                #21 0x00007f42e1e10f46 n/a (libVkLayer_steam_fossilize.so + 0x92f46)
                #22 0x000055a87e833b79 _ZN13CVulkanDevice15compilePipelineEjj10ShaderTypejjjjb (gamescope + 0xccb79)
                #23 0x000055a87e836273 _ZN13CVulkanDevice19compileAllPipelinesEv (gamescope + 0xcf273)
                #24 0x00007f42f90523b6 execute_native_thread_routine (libstdc++.so.6 + 0x523b6)
                #25 0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #26 0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130623:
                #0  0x00007f42ea45fa45 blur_surface.constprop.0.isra.0 (libdecor-gtk.so + 0x6a45)
                #1  0x00007f42ea45fe81 libdecor_plugin_gtk_frame_new (libdecor-gtk.so + 0x6e81)
                #2  0x00007f42f963789a libdecor_decorate (libdecor-0.so.0 + 0x289a)
                #3  0x000055a87e7c938d _ZN9gamescope15CWaylandBackend22CreateVirtualConnectorEm (gamescope + 0x6238d)
                #4  0x000055a87e814f4c _Z17steamcompmgr_mainiPPc (gamescope + 0xadf4c)
                #5  0x000055a87e82354e _ZL21steamCompMgrThreadRuniPPc (gamescope + 0xbc54e)
                #6  0x00007f42f90523b6 execute_native_thread_routine (libstdc++.so.6 + 0x523b6)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130621:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8efd935 epoll_wait (libc.so.6 + 0xf6935)
                #4  0x00007f42c808b008 impl_pollfd_wait (libspa-support.so + 0x1c008)
                #5  0x00007f42c8074528 loop_iterate (libspa-support.so + 0x5528)
                #6  0x00007f42f976b1c1 do_loop (libpipewire-0.3.so.0 + 0x831c1)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130606:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76977 __GI___futex_abstimed_wait_cancelable64 (libc.so.6 + 0x6f977)
                #3  0x00007f42f8e791cc pthread_cond_wait@@GLIBC_2.3.2 (libc.so.6 + 0x721cc)
                #4  0x00007f42f51f4efc n/a (libnvidia-glcore.so.610.43.02 + 0x9f4efc)
                #5  0x00007f42f563fd3e n/a (libnvidia-glcore.so.610.43.02 + 0xe3fd3e)
                #6  0x00007f42f51f5114 n/a (libnvidia-glcore.so.610.43.02 + 0x9f5114)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130622:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8eefe7e __poll (libc.so.6 + 0xe8e7e)
                #4  0x000055a87e88feb5 _ZL12run_pipewireP14pipewire_state (gamescope + 0x128eb5)
                #5  0x00007f42f90523b6 execute_native_thread_routine (libstdc++.so.6 + 0x523b6)
                #6  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #7  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130603:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76674 __syscall_cancel (libc.so.6 + 0x6f674)
                #3  0x00007f42f8ef04a6 ppoll (libc.so.6 + 0xe94a6)
                #4  0x00007f42f729f125 g_main_context_iterate_unlocked.isra.0 (libglib-2.0.so.0 + 0x48125)
                #5  0x00007f42f729f1e3 g_main_context_iteration (libglib-2.0.so.0 + 0x481e3)
                #6  0x00007f42e989611d dconf_gdbus_worker_thread (libdconfsettings.so + 0x511d)
                #7  0x00007f42f72d4d12 g_thread_proxy (libglib-2.0.so.0 + 0x7dd12)
                #8  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #9  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130599:
                #0  0x00007f42f8efb3fd syscall (libc.so.6 + 0xf43fd)
                #1  0x00007f42f72cf4eb g_cond_wait (libglib-2.0.so.0 + 0x784eb)
                #2  0x00007f42f726158c g_async_queue_pop_intern_unlocked (libglib-2.0.so.0 + 0xa58c)
                #3  0x00007f42f72d5d64 g_thread_pool_spawn_thread (libglib-2.0.so.0 + 0x7ed64)
                #4  0x00007f42f72d4d12 g_thread_proxy (libglib-2.0.so.0 + 0x7dd12)
                #5  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #6  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130608:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76977 __GI___futex_abstimed_wait_cancelable64 (libc.so.6 + 0x6f977)
                #3  0x00007f42f8e793e2 pthread_cond_timedwait@@GLIBC_2.3.2 (libc.so.6 + 0x723e2)
                #4  0x00007f42f51f4f5c n/a (libnvidia-glcore.so.610.43.02 + 0x9f4f5c)
                #5  0x00007f42f5653392 n/a (libnvidia-glcore.so.610.43.02 + 0xe53392)
                #6  0x00007f42f51f5114 n/a (libnvidia-glcore.so.610.43.02 + 0x9f5114)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130609:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76977 __GI___futex_abstimed_wait_cancelable64 (libc.so.6 + 0x6f977)
                #3  0x00007f42f8e793e2 pthread_cond_timedwait@@GLIBC_2.3.2 (libc.so.6 + 0x723e2)
                #4  0x00007f42f51f4f5c n/a (libnvidia-glcore.so.610.43.02 + 0x9f4f5c)
                #5  0x00007f42f562c5dd n/a (libnvidia-glcore.so.610.43.02 + 0xe2c5dd)
                #6  0x00007f42f51f5114 n/a (libnvidia-glcore.so.610.43.02 + 0x9f5114)
                #7  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #8  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                
                Stack trace of thread 130612:
                #0  0x00007f42f8e82412 __syscall_cancel_arch (libc.so.6 + 0x7b412)
                #1  0x00007f42f8e7662c __internal_syscall_cancel (libc.so.6 + 0x6f62c)
                #2  0x00007f42f8e76977 __GI___futex_abstimed_wait_cancelable64 (libc.so.6 + 0x6f977)
                #3  0x00007f42f8e793e2 pthread_cond_timedwait@@GLIBC_2.3.2 (libc.so.6 + 0x723e2)
                #4  0x00007f42f51f4f5c n/a (libnvidia-glcore.so.610.43.02 + 0x9f4f5c)
                #5  0x00007f42f57719d9 n/a (libnvidia-glcore.so.610.43.02 + 0xf719d9)
                #6  0x00007f42f57547b6 n/a (libnvidia-glcore.so.610.43.02 + 0xf547b6)
                #7  0x00007f42f51f5114 n/a (libnvidia-glcore.so.610.43.02 + 0x9f5114)
                #8  0x00007f42f8e79d19 start_thread (libc.so.6 + 0x72d19)
                #9  0x00007f42f8efd64c __clone3 (libc.so.6 + 0xf664c)
                ELF object binary architecture: AMD x86-64
```

</details>

## Comment 4758796723

other (NONE) · vultux · 2026-06-20T15:39:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758796723

You use Fedora, I use Arch Linux with CachyOS kernel. Different versions of gamescope, drivers, etc... Have you thought about migrating to CachyOS? It is excellent for games.

EDIT: Ok, now that I saw that FH6 has updated. Try these options: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds gamescope -W 1920 -H 1080 -r 60 --force-grab-cursor -f %command%`

_Change `-r 60` for your monitor's refresh rate._

If your monitor supports HDR and VRR, you can add: `--adaptive-sync --hdr-enabled` If you want to see the graphs, install Mangohud and put it in the string: `--mangoapp`

## Comment 4758869111

other (NONE) · itsmeadarsh2008 · 2026-06-20T15:56:13Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758869111

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758796723

I have a 120Hz Laptop Screen. I have tried CachyOS first, but I was stuck in installation because there were some issues with the Wi-Fi connections in Live Boot (Installation Phase). I could have tried USB tethering to provide an internet connection, too, but it was not great.

Edit: If they provide, pre compiled non-rolling release, things would have been different.

## Comment 4758892422

other (NONE) · vultux · 2026-06-20T16:01:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758892422

> I have a 120Hz Laptop Screen. I have tried CachyOS first, but stuck in installation because there were some issues with the Wi-Fi connections in Live Boot (Installation Phase). I could have tried USB tethering to provide an internet connection, too, but it was not great.
> 
> Edit: If they provide, pre compile non-rolling release, things would have been different.

You can install plugged into the cable first and check if the Wifi is detected later, if it is not it is necessary to search the laptop's wifi adapter and download any driver or firmware that is missing.

Tested with the string: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds gamescope -W 1920 -H 1080 -r 60 --force-grab-cursor -f %command%`

On my computer it is only working if I use: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds`

## Comment 4758936168

other (NONE) · itsmeadarsh2008 · 2026-06-20T16:11:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758936168

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758892422

still crashes. 
Also: If I don't use any Launch Options especially on Proton CachyOS Latest (installed via ProtonPlus), Proton Hotfix, it works nicely, but crashes when the initial race starts,

## Comment 4758987032

other (NONE) · vultux · 2026-06-20T16:22:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758987032

> still crashes. Also: If I don't use any Launch Options especially on Proton CachyOS Latest (installed via ProtonPlus), Proton Hotfix, it works nicely, but crashes when the initial race starts,

Yes, mine is also crashing if I don't use the option: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds`

Try this: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds %command%`

It's not the best option to have more FPS, but it's cleaner and more stable, good for testing.

The VKD3D_CONFIG=descriptor_heap,**skip_application_workarounds** disable its built-in per-game workarounds.


## Comment 4759123367

other (NONE) · itsmeadarsh2008 · 2026-06-20T16:51:52Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4759123367

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4758987032

Nahh man, I think I should wait for whom?? I don't know, should I wait for Nvidia to patch or Forza Horizon 6 to patch? Or Valve Proton? I'm confused. The game started, but it crashed just right after optimising the PC 100%. Most people are using the 595 version of Nvidia Drivers to play the game. I will try to downgrade later. If it works, I will report it here as a fix.

## Comment 4759161882

other (NONE) · vultux · 2026-06-20T16:59:35Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4759161882

> Nahh man, I think I should wait for whom?? I don't know, should I wait for Nvidia to patch or Forza Horizon 6 to patch? Or Valve Proton? I'm confused. The game started, but it crashed just right after optimising the PC 100%. Most people are using the 595 version of Nvidia Drivers to play the game. I will try to downgrade later. If it works, I will report it here as a fix.

Yep, now I've found out that HDR is no longer working, for any game, because KDE Plasma has updated to version 6.7.

Linux requires patience, but even so I don't go back to Windows. If it doesn't work on Linux then I don't play it.

Try CachyOS again when you have time, it's pretty good.

**EDIT:** 
I tested it this way:

**No gamescope**, only: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds %command%` 

_(game → KWin → display)_

The game loads but crashes when I try to join a race.

**With gamescope**: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds VKD3D_FRAME_RATE=120 gamescope -W 3840 -H 2160 -r 120 --mangoapp --force-grab-cursor -f -- %command%`

_(game → gamescope → KWin → display)_

The game loaded and when entering a race it worked.
But as I said I use Arch Linux so Gamescope is the latest version, everything is latest version. In other Linux distros it may be different.

## Comment 4759954380

other (NONE) · fastoslinux · 2026-06-20T20:51:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4759954380

After some online races, I get a crash with the FHE21 error, is there any fix for this?

## Comment 4760044359

other (NONE) · k4lim · 2026-06-20T21:31:25Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4760044359

I've tried all of the fixes mentioned on [ProtonDB](https://www.protondb.com/app/2483190) and I got it running exactly once with the following settings:

Proton version: `cachyos-11.0-20260520-slr`  
launch options: `PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%`

After ending my session it never worked again, no matter what settings I use. Currently I'm stuck after the photosensitive seizure warning where I get the following screen and then nothing else is happening:  

<details>
  <summary>screenshot</summary>
<img width="2560" height="1440" alt="Image" src="https://github.com/user-attachments/assets/f2402851-bd4c-43f5-9034-a7aec6df3f97" />
</details>

The time it worked it was running fine without any stuttering and alright performance.

My system information:  
```
OS: Manjaro Linux
KERNEL: 6.12.94-1-MANJARO
CPU: AMD Ryzen 7 3700X 8-Core
GPU: NVIDIA GeForce RTX 3070
GPU DRIVER: NVIDIA 610.43.02
RAM: 32 GB
``` 

## Comment 4760125389

other (NONE) · vultux · 2026-06-20T22:08:17Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4760125389

> After ending my session it never worked again, no matter what settings I use. Currently I'm stuck after the photosensitive seizure warning where I get the following screen and then nothing else is happening:

Try with: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds`

## Comment 4760485288

other (NONE) · k4lim · 2026-06-21T00:58:11Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4760485288

> Try with: `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds`

This did not help, same result :/

> Most people are using the 595 version of Nvidia Drivers to play the game. I will try to downgrade later. If it works, I will report it here as a fix.

Is this a valid fix? I was on that version before but it wasn´t working with that version either. The game told me to upgrade - so I did.

## Comment 4760541428

other (NONE) · itsmeadarsh2008 · 2026-06-21T01:24:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4760541428

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4760485288

I checked protondb for fixes, they are using 595

## Comment 4761537432

other (NONE) · Aeldit · 2026-06-21T09:32:36Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761537432

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4759161882

Using a slightly modified version of this, `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds VKD3D_FRAME_RATE=72 gamescope -W 2560 -H 1440 -r 72 -- %command%` (in the quoted post there were some issues with double dashes in the command arguments) with cachyos kernel `7.0.12-1-cachyos`, nvidia drivers `610.43.02` with an RTX 3050 laptop, it runs perfectly well.

## Comment 4761604926

other (NONE) · itsmeadarsh2008 · 2026-06-21T10:04:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761604926

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761537432

Not working still crashes.

## Comment 4761645237

other (NONE) · MementoMortes · 2026-06-21T10:21:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761645237

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761537432

Are all ray tracing related settings off and did you try turning shader quality to minimum?

## Comment 4761657903

other (NONE) · itsmeadarsh2008 · 2026-06-21T10:26:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761657903

Yes. I did. It's working on CachyOS except Fedora.

On Sun, 21 Jun, 2026, 15:51 Artemis, ***@***.***> wrote:

> *MementoMortes* left a comment (ValveSoftware/Proton#9789)
> <https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761645237>
>
> Nahh man, I think I should wait for whom?? I don't know, should I wait for
> Nvidia to patch or Forza Horizon 6 to patch? Or Valve Proton? I'm confused.
> The game started, but it crashed just right after optimising the PC 100%.
> Most people are using the 595 version of Nvidia Drivers to play the game. I
> will try to downgrade later. If it works, I will report it here as a fix.
>
> Yep, now I've found out that HDR is no longer working, for any game,
> because KDE Plasma has updated to version 6.7.
> Linux requires patience, but even so I don't go back to Windows. If it
> doesn't work on Linux then I don't play it.
> Try CachyOS again when you have time, it's pretty good.
> *EDIT:* I tested it this way:
> *No gamescope*, only: VKD3D_CONFIG=descriptor_heap,skip_application_workarounds
> %command%
> *(game → KWin → display)*
> The game loads but crashes when I try to join a race.
> *With gamescope*: VKD3D_CONFIG=descriptor_heap,skip_application_workarounds
> VKD3D_FRAME_RATE=120 gamescope --W 3840 -H 2160 --r 120 --mangoapp
> --force-grab-cursor -f -- %command%
> *(game → gamescope → KWin → display)*
> The game loaded and when entering a race it worked. But as I said I use
> Arch Linux so Gamescope is the latest version, everything is latest
> version. In other Linux distros it may be different.
>
> Using a slightly modified version of this, VKD3D_CONFIG=descriptor_heap,skip_application_workarounds
> VKD3D_FRAME_RATE=72 gamescope -W 2560 -H 1440 -r 72 -- %command% (in the
> quoted post there were some issues with double dashes in the command
> arguments) with cachyos kernel 7.0.12-1-cachyos, nvidia drivers 610.43.02
> with an RTX 3050 laptop, it runs perfectly well.
>
> Not working still crashes.
>
> Are all ray tracing related settings off and did you try turning shader
> quality to minimum?
>
> —
> Reply to this email directly, view it on GitHub
> <https://github.com/ValveSoftware/Proton/issues/9789?email_source=notifications&email_token=ARFAFKWCHI2A3LONKXQXHVD5A6ZLNA5CNFSNUABFM5UWIORPF5TWS5BNNB2WEL2JONZXKZKDN5WW2ZLOOQXTINZWGE3DINJSGM32M4TFMFZW63VHMNXW23LFNZ2KKZLWMVXHJLDGN5XXIZLSL5RWY2LDNM#issuecomment-4761645237>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/ARFAFKQPPMC433B6UDJDCID5A6ZLNAVCNFSNUABFKJSXA33TNF2G64TZHMYTENJQHE4DQOBQHNEXG43VMU5TINBVGE4TIMRSGMZ2C5QC>
> .
> You are receiving this because you commented.Message ID:
> ***@***.***>
>


## Comment 4761742686

other (NONE) · k4lim · 2026-06-21T11:05:28Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4761742686

> Using a slightly modified version of this, `VKD3D_CONFIG=descriptor_heap,skip_application_workarounds VKD3D_FRAME_RATE=72 gamescope -W 2560 -H 1440 -r 72 -- %command%` (in the quoted post there were some issues with double dashes in the command arguments) with cachyos kernel `7.0.12-1-cachyos`, nvidia drivers `610.43.02` with an RTX 3050 laptop, it runs perfectly well.

This kinda made it better? I was now able to start the game, set all video settings to the lowest setting with RTX off. I could then drive for just a second before I got the video card error `FHC20` and the game crashed.



## Comment 4765655636

other (NONE) · itsmeadarsh2008 · 2026-06-22T06:52:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4765655636

Update: I have changed my Nvidia Drivers to the Production Branch (610 Feature Version to 595 stable). Still Crashes. This game is something that works great on CachyOS, not on Fedora. Looks like I have to change my distro to play FH6 (have to install 155 GB again 😢). My other games are running super smooth except this.

## Comment 4773255562

other (NONE) · k4lim · 2026-06-22T21:30:17Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4773255562

Just installed cachyOS just to play the game... After some minutes I get the FHC00 error code. grrr

## Comment 4774107668

other (NONE) · RafaelHGOliveira · 2026-06-22T23:35:06Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4774107668

@k4lim Try adding this to your Steam launch options:

`VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%`

Also make sure you're using **Proton Experimental** or **proton-cachyos** (latest). Which one did you try?

## Comment 4777303459

other (NONE) · TaraSophieDev · 2026-06-23T08:35:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4777303459

Are there any news or fixes about the weird rubberband stuttering on amd gpus, like the 9070xt?

Already tried newest versions of Proton: Hotfix, Experimental, GE, Cachyos Proton.
And various Env Variables.

## Comment 4779469832

other (NONE) · eyenalxai · 2026-06-23T13:01:57Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4779469832

> Are there any news or fixes about the weird rubberband stuttering on amd gpus, like the 9070xt?
> 
> Already tried newest versions of Proton: Hotfix, Experimental, GE, Cachyos Proton. And various Env Variables.

Nope. It also stutters on Steam Machine btw according to Digital Foundry: https://www.youtube.com/watch?v=WhWtLi_FqLo&t=927s

## Comment 4780732613

other (NONE) · itsmeadarsh2008 · 2026-06-23T15:24:57Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4780732613

> > Are there any news or fixes about the weird rubberband stuttering on amd gpus, like the 9070xt?
> > 
> > Already tried newest versions of Proton: Hotfix, Experimental, GE, Cachyos Proton. And various Env Variables.
> 
> Nope. It also stutters on Steam Machine btw according to Digital Foundry: https://www.youtube.com/watch?v=WhWtLi_FqLo&t=927s

Microsoft being Microsoft 🥀

## Comment 4786282794

other (NONE) · linoshkmalayil · 2026-06-24T05:48:56Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4786282794

It seems like with each update the game performance on Linux is getting worse and worse.

Benchmark running Extreme RT, FSR Quality.
On 364.933 version: 78fps.
On 375.327 version: 67fps.
On 382.893 version: 60fps.

While the Windows performance remains consistent since 364.933 giving 92fps.

System:
Ryzen 7 5800x
32GB DDR4 3200MHz
AMD RX9070XT 
Arch Linux + KDE Plasma + Proton-CachyOS

## Comment 4787775213

other (NONE) · Oingy-Boingy · 2026-06-24T09:25:17Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4787775213

I've had a number of crashes now with the `FHC20` error code, which isn't listed in the known error codes on the Forza website [here](https://support.forza.net/hc/en-us/articles/51642089902739-Forza-Horizon-6-PC-Crash-Error-Codes), however the closest error code `FHC21` is listed and is related to running an unsupported OS. Looks like there is some OS detection going on and then it crashes.

Annoyingly the game worked fine for me for two hours on Proton 11 (Beta) with the below launch options:
`PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap %command%`

System:
Intel i9-9900k
32GB DDR4 3200MHz
NVIDIA GeForce 2080ti
Arch 7.0.12 + Hyprland 0.55.4-1 + Proton 11 (Beta) (in Steam dropdown list)
Nvidia 610.43.02-2 (nvidia-open-dkms Arch package) 

### Fixed

`VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%` and Proton Experimental seems to have cured it, apologies.

## Comment 4793063078

other (NONE) · tuxmanxd · 2026-06-24T19:50:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4793063078

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4787775213

THANK YOU SO MUCH THIS MADE IT WORK FLAWLESSSLY FOR ME I REALLY APPRECIATE IT

## Comment 4798512735

other (NONE) · dino460 · 2026-06-25T10:59:02Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4798512735

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4787775213

What driver version are you on? I tried your launch options on my i5 10400f + 2080ti and it's still struggling a lot on driver version 595. I'm on Pop_OS 22, so no 610 yet...

## Comment 4800733003

other (NONE) · SolarMyth79 · 2026-06-25T14:55:18Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4800733003

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4719002424

experimental-11.0-20260622b now detects forzahorizon6.exe and applies 2 configs + shader quirks, but 62s hang before window creation persists unchanged. RTX 3060 Ti, driver 595.71.05.

Updated log for experimental-11.0-20260622b:
[steam-2483190.log](https://github.com/user-attachments/files/29342328/steam-2483190.log)

## Comment 4800972520

other (NONE) · tuxmanxd · 2026-06-25T15:19:00Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4800972520

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4800733003

As @Oingy-Boingy mentioned in his comment adding VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing fixes the hangs

## Comment 4801470273

other (NONE) · tuxmanxd · 2026-06-25T15:56:54Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4801470273

> > Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4787775213
> 
> What driver version are you on? I tried your launch options on my i5 10400f + 2080ti and it's still struggling a lot on driver version 595. I'm on Pop_OS 22, so no 610 yet...

I'm on nixos unstable with driver 610 

## Comment 4802625216

other (NONE) · JohnnySun · 2026-06-25T17:55:11Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4802625216

Adding a SteamOS / Intel Xe handheld data point. This is not an initial launch crash; it is specifically triggered by SteamOS suspend/resume.

### System

- Game: Forza Horizon 6, app id `2483190`
- Device: MSI Claw 8 AI+ A2VM handheld
- GPU: Intel Lunar Lake integrated Arc Graphics 130V/140V, kernel driver `xe`
- Kernel: `6.16.12-valve24-1-neptune-616-gc748040e4712`
- Mesa / ANV: `vulkan-intel 25.3.0.213835.radeonsi_25.3.0-4.1` (`lib32-vulkan-intel` same build)
- gamescope: `3.16.23.2-1`
- Proton: Proton Experimental, tested on 2026-06-26
- In-game settings from the game crash report: `1920x1200`, Medium preset, FSR Balanced, 60 FPS cap
- Ray tracing is off in the crash report: `UserConfig_RTGIQuality=Off`, `UserConfig_RTReflectionQuality=Off`
- gamescope is running at the native panel resolution, `1920x1200`

### Repro

1. Launch FH6 through SteamOS game mode.
2. Enter the game and wait until it is playable.
3. Press the power button to suspend the handheld.
4. Resume from suspend.

### Result

After resume, the presented image freezes. In some runs audio continues for a while while the HUD/image stays frozen; in other runs audio also stops. The process may remain alive briefly, then the game writes a crash/hang report.

The game crash report consistently points at a video device removal path:

```xml
REASON="Video card"
BUCKET="Device removed: Unknown error: 0x00000102"
EXCEPTION="ACCESS_VIOLATION_WRITE"
```

The Steam/journal side shows Intel userspace failing submissions after the resume failure:

```text
steam[...] intel: the execbuf ioctl keeps returning ENOMEM
```

I did not see system RAM exhaustion or a kernel OOM during the repro. `MemAvailable` was still around 18 GB in one captured failed run, and Forza RSS was around 4.3 GB. I also did not see a clear `xe` GPU reset/hang message in `journalctl -k` around the resume; suspend/resume itself completed normally (`PM: suspend entry (s2idle)` -> `PM: suspend exit`).

During the frozen state, the Forza process was still present, with many threads waiting in `ntsync_schedule`, and vkd3d queue/fence/swapchain related threads mostly in futex waits. The GPU activity had dropped to zero (`act_freq=0`) after the freeze.

### Workarounds already tried

- Ensured gamescope is not downscaling to Steam Deck resolution; compositor is now `1920x1200`, matching the panel. No change.
- RT is already off. No change.
- Medium settings / FSR Balanced / 60 FPS cap. No change.
- Pre-sleep `SIGSTOP` of the game, then `SIGCONT` 2 seconds after resume. No change; still produced `Device removed: Unknown error: 0x00000102`.
- Same test but delaying `SIGCONT` until 15 seconds after resume. No change.
- Higher handheld power/TDP limits. No change; this does not look power-limit related.

This looks close to the Intel `xe` / vkd3d FH6 hang class reported in HansKristian-Work/vkd3d-proton#3050, but in this case the reliable trigger is SteamOS suspend/resume rather than launch or entering gameplay. Happy to collect a Proton log, ANV/vkd3d debug output, or specific `xe` debugfs snapshots if that would help.

## Comment 4808604568

other (NONE) · pflavio · 2026-06-26T10:14:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4808604568

> ### Fixed
> 
> `VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%` and Proton Experimental seems to have cured it, apologies.

Doesn't work for me unfortunately. It's a bit baffling I still can't play a game I pre-ordered, FH4 and FH5 were working just fine. I'm on an up to date Bazzite system with a 9800x3D and a 4090.


## Comment 4817717475

other (NONE) · SolarMyth79 · 2026-06-27T13:09:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4817717475

> > Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4800733003)
> 
> As [@Oingy-Boingy](https://github.com/Oingy-Boingy) mentioned in his comment adding VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing fixes the hangs

Still not working for me with this launch command, unfortunately.

## Comment 4819832133

other (NONE) · KhorneFlakez1337 · 2026-06-27T17:48:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4819832133

Can't get the game to launch on Manjaro at all, no matter which workaround I tried

Using a 7800X3D with a 9060XT

It did run shortly after it came out, but I wasn't playing it on my PC since then, but rather my Steam Deck
Now that I am trying to play it on my PC again, it just doesn't launch at all

## Comment 4823469645

other (NONE) · MustardForBreakfast · 2026-06-28T00:46:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4823469645

> `VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%` and Proton Experimental seems to have cured it, apologies.

switching to Proton Experimental seems to have resolved the FHC20 crashes for me, but now the game flickers like a strobe light during gameplay. Curiously the mangohud framerate displays as "unl" (unlimited?).

I am using the same launch configs.

## Comment 4825340298

other (NONE) · sharunkumar · 2026-06-28T08:10:23Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4825340298

The following works for me on RTX 4080 Laptop GPU, Ultra + RT + DLSS Enabled (previously it used to crash with RT)

Proton: proton-cachyos-11.0-20260601

Launch Flags: `PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap,skip_application_workarounds %command%`

## Comment 4826294465

other (NONE) · Oingy-Boingy · 2026-06-28T13:49:14Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4826294465

> > Replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4787775213)
> 
> What driver version are you on? I tried your launch options on my i5 10400f + 2080ti and it's still struggling a lot on driver version 595. I'm on Pop_OS 22, so no 610 yet...

Edited my comment to add I'm on 610.43.02-2 and the Arch package I'm using. Not sure that will help for Pop OS though 

## Comment 4831974570

other (NONE) · itsmeadarsh2008 · 2026-06-29T11:32:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4831974570

Update: Forza Horizon 6 is working seamlessly smooth on CachyOS with Proton-CachyOS Latest. If you feel lag in games: Set this as Launch Options: `VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%`

without this launch options, you feel lag while getting crashing race track boundaries.

## Comment 4834539167

other (NONE) · TaraSophieDev · 2026-06-29T16:02:44Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4834539167

> Update: Forza Horizon 6 is working seamlessly smooth on CachyOS with Proton-CachyOS Latest. If you feel lag in games: Set this as Launch Options: `VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%`
> 
> without this launch options, you feel lag while getting crashing race track boundaries.

@itsmeadarsh2008 
Is this for AMD or Nvidia?
Tried that on EndavourOS with latest CachyOS Proton and the Launch options, but still lags.

## Comment 4834856389

other (NONE) · itsmeadarsh2008 · 2026-06-29T16:38:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4834856389

> > Update: Forza Horizon 6 is working seamlessly smooth on CachyOS with Proton-CachyOS Latest. If you feel lag in games: Set this as Launch Options: `VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%`
> > without this launch options, you feel lag while getting crashing race track boundaries.
> 
> [@itsmeadarsh2008](https://github.com/itsmeadarsh2008) Is this for AMD or Nvidia? Tried that on EndavourOS with latest CachyOS Proton and the Launch options, but still lags.

Nvidia

## Comment 4835040424

other (NONE) · k4lim · 2026-06-29T16:58:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4835040424

Update on my end:

Proton Version: `Proton Experimental`
Launch options:   `VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%`

Kernel: `Linux 7.1.2-2-cachyos`

Work's wthout any issues now. Performance is good, no stutters.

## Comment 4838689860

other (NONE) · HypestHyper · 2026-06-30T00:10:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4838689860

Proton Version: Proton Experimental

Launch options: VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing %command%

Kernel: Linux 7.1.2-2-cachyos
CachyOS with Hyprland

Been experiencing some rubberbanding and stutters too on an rx 7700xt.
The launch options helped a bit, but at least on my end, im seeing some other problems. Before using these launch options, frame time usually averaged around 9-15ms but randomly spikes to 50ms. The launch options made it a bit more bearable, where it peaks around 20ms but way smoother, though a bit unstable.

At least for my GPU, there seems to be some power management issues when running games through steal/proton. For some reason, it starts to power throttle around 170-180w.

I use LACT for management, and that's set to 250w. And it can pull 250w no problem in furmark. But steam/proton caps around 170w with gpu at 100%. 

Got some help from an llm with logging and monitoring scripts and seems like I'm hitting TDC which is weird because all my temps are pretty ok. And furmark didn't complain either. 10 mins under full load 250w.

As for raytracing, experiencing issues same as everyone in this thread. Though for some reason only happens after game restart. Rtx works fine, but if i keep it on then restart, it errors aut when loading the game/map. I have to turn it off in teh start screen.

## Comment 4839933451

other (NONE) · enesaltinkaya · 2026-06-30T04:42:50Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4839933451

> At least for my GPU, there seems to be some power management issues when running games through steal/proton. For some reason, it starts to power throttle around 170-180w.
  
Gpu is not being utilized fully; 5090 should chug 450-550 watts in this games.
  
<img width="500" alt="Image" src="https://github.com/user-attachments/assets/a1fc1461-7141-45cb-af35-961d7d85d4c4" />

<img width="500" alt="Image" src="https://github.com/user-attachments/assets/c51cc39e-c878-46d2-bd73-b7f7da84d681" />

  
  
  
**Windows**  screenshot from a youtube game reviewer.
  
<img width="400" alt="Image" src="https://github.com/user-attachments/assets/003091ee-56a2-43b0-a7ed-93363d230643" />


## Comment 4841443662

other (NONE) · HypestHyper · 2026-06-30T08:34:26Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4841443662

> Gpu is not being utilized fully; 5090 should chug 450-550 watts in this games.

Check mangohud and enable the power throttle on the graph. See if it does the same thing. Something is messed up and im pretty sure this is not an end-user machine issue.

Have you had the chance to test any other games through steam/proton and outside?

I also tested 3dmark (demo) both on dx12 and vulkan and they both cap around 180 with power throttle. And as mentioned in my earlier comment, furmark ran natively pulls 250w no problem.

Here is FH6
![Screenshot_20260630_113028_Kimi.jpg](https://github.com/user-attachments/assets/ff1f8f8a-e471-453d-af7f-3ddee788c709)

Here is furmark native
![Screenshot_20260630_113213_Kimi.jpg](https://github.com/user-attachments/assets/83924f3e-2629-4414-886b-492d855fb278)

## Comment 4841664821

other (NONE) · enesaltinkaya · 2026-06-30T09:03:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4841664821

Furmark 600watts.  
Witcher3 425watts. dxvk.  
Ghost of Tsushima 500wats. vkd3d, descriptor_heap.  
Cyberpunk 550watts, vkd3d ,descriptor_heap.  
  
Other games i cant max out gpu, i have a relatively old cpu.  
  
Looks fine on Ghost of Tsushima and Cyberpunk.  
So issue is with this forza game it looks like.

## Comment 4850689736

other (NONE) · Jakeshadow · 2026-07-01T05:55:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4850689736

For reference — the black screen on startup was fixed in Proton Bleeding Edge (11.0-362204-20260515). If you're still seeing it, make sure you've opted into Bleeding Edge beta in Steam.

The severe stuttering issue is more interesting — it manifests as micro-freezes that don't always show up in frametime graphs, which suggests it might be shader compilation stutter or a resource streaming bottleneck rather than a pure rendering problem. A few things worth trying:
- Enable `DXVK_ASYNC=1` if your Proton build supports it (async shader compilation)
- Clear the shader cache (`steamapps/shadercache/2483190/`)
- If you're on a 9000 series AMD card, Mesa 26.1.x had known issues with certain DX12 title workloads — Mesa 26.2+ (git) has improvements

Ray tracing crashing with GPU error on RDNA4 is likely a Mesa/RADV bug — worth reporting separately on the Mesa GitLab with a RADV_DEBUG hang report.

One other thing: Forza Horizon (5 and 6) uses anti-cheat that has had mixed Proton compatibility across versions. If you're getting kicked from online sessions or the game refuses to connect to servers, that's a separate layer from the rendering issues here.

## Comment 4862331024

other (NONE) · MustardForBreakfast · 2026-07-02T04:56:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4862331024

@Jakeshadow thanks for the response.
Re: severe stuttering, I tried both `DXVK_ASYNC=1` and blowing away the cache directory you called out, but the issue persists. I'm running an NVIDIA card.

```
OS: Bazzite
KERNEL: 6.19.14-ogc5.1.fc44.x86_64
CPU: AMD Ryzen 7 9800X3D 8-Core
GPU: NVIDIA GeForce RTX 4080 SUPER
GPU DRIVER: NVIDIA 595.71.05
RAM: 31 GB
```

## Comment 4875151717

other (NONE) · dorogush · 2026-07-03T10:15:38Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4875151717

With stock CachyOS kernel `7.1.2-3` Forza Horizon 6 runs fine. RX 9070.
With `7.2-rc1-4` - HDMI FRL, VRR, ALLM, HDR10 - all are working fine. Cyberpunk, Expedition 33 run fine. Forza Horizon 6 crashes on load
```
Error: Video Card Crash. Code: FHC20
```
Tried different proton versions and start parameters. The only thing that resolves the issue is going back to `7.1.2-3`.
I guess this is not a Proton issue but I don't know where I can report it.

## Comment 4885517692

other (NONE) · srinidhikrs · 2026-07-05T09:19:14Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4885517692

Facing blackscreen issue after intro video in FH6. GPU is AMD 7900 xtx . Using ubuntu steam with proton experimental (latest bleeding edge) . Some times the game works fine after intro video and sometimes there is blackvideo freeze (without audio) after intro. Please refer to attached video and suggest solution to make it work reliably 

Thanks
Srinidhi

https://github.com/user-attachments/assets/2d19ed3b-2e92-4452-b095-f284e7770e63

## Comment 4994237150

other (NONE) · samuelskovbakke · 2026-07-16T16:27:58Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4994237150

Are the stuttering issues still being actively investigated? Or has someone come up with a "surefire" way to fix it with launch options?

---
My system:

OS: NixOS

DE/WM: Niri

GPU: AMD RX 9070 XT

CPU: Ryzen 7 7800X3D

## Comment 4994274999

other (NONE) · enesaltinkaya · 2026-07-16T16:32:01Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4994274999

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4994237150

you might want to try "amdgpu.vm_update_mode=3" kernel param.  
that helped with my 7900xtx. i lowered environmental textures from extreme to high or lower.  then it was silky smooth. 
im unplugged that gpu since, so i cant test again to be sure.  
just give it a try.

## Comment 4994595612

other (NONE) · srinidhikrs · 2026-07-16T17:08:24Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4994595612

any suggestions for blackscreen issue after intro video in FH6 with proton experimental (latest bleeding edge) and amd 7900xtx?

## Comment 5004687642

reporter (NONE) · luneko · 2026-07-17T15:12:48Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5004687642

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4994237150

They are definetly still there. For me the game is only playable by setting environmental texture to "low" and locking fps to 60, which of course is not what you'd want to do with higher end cards.
As for the previously suggested kernel parameters I don't think it changes anything.

If this issue is still being investigated, idk, but I sure hope it is.

## Comment 5007157105

other (NONE) · kurayamin0 · 2026-07-17T20:20:08Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5007157105

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4885517692

For me adding the following to the Steam launch options.
```
VKD3D_CONFIG=skip_application_workarounds,descriptor_heap,avoid_image_buffer_aliasing PROTON_VKD3D_HEAP=1 %command%
```
Right Click > Properties > General > Launch Options

Also if you navigate to ~/.local/share/Steam/steamapps/shadercache/2483190 and delete that folder, then Verify the Integrity of game files under steam

Right Click > Properties > Installed Files > Verify integrity of game files

This doesn't fix the stuttering issues, which since the last patch have gotten far worse and also get far worse as you play it. Similar to a memory leak. Ultimately the system will crash after about an hour.

## Comment 5007340163

other (NONE) · CRKrJ4K · 2026-07-17T20:47:18Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5007340163

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-4994237150

Afaik the stuttering is due to the way the game is coded. The "fixes" that the vkd3d dev made were attempts to work around their shoddy code. 

There are lots of Windows users with stuttering issues so maybe one day they'll fix their game. For now, all they care about is plugging loopholes in farming credits & resetting lap times.

## Comment 5009897698

other (NONE) · srinidhikrs · 2026-07-18T04:27:13Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5009897698

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5007157105

<img width="1850" height="1088" alt="Image" src="https://github.com/user-attachments/assets/5bf5698d-4c0b-4c5a-a548-60958aa3a0f4" />


Still the black screen issue is happening even after adding the suggested launch options.



## Comment 5013094814

other (NONE) · EmeraldSnorlax · 2026-07-18T22:02:50Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5013094814

Hi all,

I'm experiencing perhaps the strangest bug with Proton yet in Forza Horizon 6.

When fast traveling to ("loading into") Shikisai-no-Oka (whether from the map, or at the start/end of a race, exiting photography mode nearby), loading can take 3-5 minutes on an SSD, much longer than the expected 5-10 second loading times experienced when "loading into" any other location. 

When driving up to the same location normally ("streaming into") Shikisai-no-Oka, no issues happen.

This area of the map has very dense flower fields; perhaps related to that?

<details>

<summary>Proton version info</summary>


```
Proton: 1784330736 experimental-bleeding-edge-11.0-398902-20260717-pe346d3-w91e9e8-d6b20f6-v3dfc6f
SteamGameId: 2483190
Command: ['/home/rain/.local/share/Steam/steamapps/common/ForzaHorizon6/forzahorizon6.exe']
Options: {'gamedrive', 'forcelgadd'}
depot: 4.0.20260608.242786
pressure-vessel: 0.20260601.0
pressure-vessel-arm64: 0.20260601.0
scripts: 0.20260601.0
steamrt4: 4.0.20260608.242786 steamrt4 4.0.20260608.242786
Kernel: Linux 7.1.2-arch3-1 #1 SMP PREEMPT_DYNAMIC Fri, 03 Jul 2026 23:25:36 +0000 x86_64
Language: LC_ALL None, LC_MESSAGES None, LC_CTYPE None
```
</details>

Attached is a Proton log that matches the version information above, that contains me launching the game, entering the open world, and then fast-traveling via the map to Shikisai-no-Oka.

Please take care extracting, as the log file is 9.0GiB un-gzipped.

https://cloud.disroot.org/s/WysDcRciojJwSxF

A small excerpt from towards the end of the log is below, in case you do not wish to download.

<details>

<Summary>Excerpt</Summary>

```
190387.172:0144:0268:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
190387.172:0144:0268:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=00000001415B4BD0
190387.172:0144:0268:trace:seh:dispatch_exception rip=00000001415b4bd0 rsp=0000000017a1dec8 rbp=0000000017a1df61 eflags=00010246
190387.172:0144:0268:trace:seh:dispatch_exception rax=00000003082c80b0 rbx=0000000000000020 rcx=0000000307ed23d0 rdx=0000000017a1df18
190387.172:0144:0268:trace:seh:dispatch_exception rsi=00000003082c8f30 rdi=000000030806e128  r8=0000000307ed9000  r9=0000000000000010
190387.172:0144:0268:trace:seh:dispatch_exception r10=00000001415b4bd0 r11=0000000017a1df90 r12=000000008cedc0c0 r13=00000000a1c42f20
190387.172:0144:0268:trace:seh:dispatch_exception r14=0000000000000010 r15=0000000307ed9000 mxcsr=00001faa cs=0033 ss=002b
190387.172:0144:0268:trace:seh:call_vectored_handlers calling handler at 0000000145374FC8 code=c000001d flags=0
190387.172:0144:0268:trace:seh:call_vectored_handlers handler at 0000000145374FC8 returned ffffffff
190387.172:0144:0268:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
190387.172:0144:0268:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=00000001415B4450
190387.172:0144:0268:trace:seh:dispatch_exception rip=00000001415b4450 rsp=0000000017a1dd68 rbp=0000000017a1de70 eflags=00010287
190387.172:0144:0268:trace:seh:dispatch_exception rax=00000003082c80b0 rbx=0000000307ed24d0 rcx=0000000307ed23d0 rdx=00000003082c80b0
190387.172:0144:0268:trace:seh:dispatch_exception rsi=00000003082c80b0 rdi=0000000307ed23d0  r8=0000000000000010  r9=0000000017a1df10
190387.172:0144:0268:trace:seh:dispatch_exception r10=00006ffffc8e0000 r11=0000000017a1db80 r12=0000000000000020 r13=0000000307ed9000
190387.172:0144:0268:trace:seh:dispatch_exception r14=0000000000000010 r15=0000000017a1e1c0 mxcsr=00001faa cs=0033 ss=002b
190387.172:0144:0268:trace:seh:call_vectored_handlers calling handler at 0000000145374FC8 code=c000001d flags=0
190387.172:0144:0268:trace:seh:call_vectored_handlers handler at 0000000145374FC8 returned ffffffff
190387.172:0144:0268:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
190387.172:0144:0268:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=00000001415B5490
190387.172:0144:0268:trace:seh:dispatch_exception rip=00000001415b5490 rsp=0000000017a1dc68 rbp=0000000017a1dd11 eflags=00010206
190387.172:0144:0268:trace:seh:dispatch_exception rax=000000000d0e1700 rbx=0000000307ed23d0 rcx=0000000307ed23d0 rdx=0000000017a1df10
190387.172:0144:0268:trace:seh:dispatch_exception rsi=0000000000000010 rdi=0000000017a1df10  r8=0000000017a1e1c0  r9=00000000000000e0
190387.172:0144:0268:trace:seh:dispatch_exception r10=00006ffffc8e0000 r11=00006ffffc8fe721 r12=0000000000000020 r13=0000000307ed9000
190387.172:0144:01a8:trace:seh:sigsys_handler SIGSYS, rax 0x2a, rip 0xe2068a.
190387.172:0144:0268:trace:seh:dispatch_exception r14=00000003082c80b0 r15=0000000000000000 mxcsr=00001faa cs=0033 ss=002b
190387.172:0144:0268:trace:seh:call_vectored_handlers calling handler at 0000000145374FC8 code=c000001d flags=0
190387.172:0144:0268:trace:seh:call_vectored_handlers handler at 0000000145374FC8 returned ffffffff
190387.172:0144:0268:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
190387.172:0144:01a8:trace:seh:sigsys_handler SIGSYS, rax 0xf, rip 0xe2068a.
190387.172:0144:0268:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=00000001415B1C70
190387.172:0144:0268:trace:seh:dispatch_exception rip=00000001415b1c70 rsp=0000000017a1dbd8 rbp=0000000017a1dd11 eflags=00010202
190387.172:0144:0268:trace:seh:dispatch_exception rax=0000000017a1dc20 rbx=0000000307ed2520 rcx=00000003082c9180 rdx=0000000017a1dc40
190387.172:0144:0268:trace:seh:dispatch_exception rsi=0000000017a1df10 rdi=0000000307ed23d0  r8=0000000000000010  r9=0000000017a1dc30
190387.172:0144:01a8:trace:seh:sigsys_handler SIGSYS, rax 0xf, rip 0xe2068a.
190387.172:0144:0268:trace:seh:dispatch_exception r10=00006ffffc8e0000 r11=00006ffffc8fe721 r12=0000000000000020 r13=0000000307ed9000
190387.172:0144:0268:trace:seh:dispatch_exception r14=00000003082c80b0 r15=0000000000000000 mxcsr=00001faa cs=0033 ss=002b
190387.172:0144:0268:trace:seh:call_vectored_handlers calling handler at 0000000145374FC8 code=c000001d flags=0
190387.172:0144:0268:trace:seh:call_vectored_handlers handler at 0000000145374FC8 returned ffffffff
190387.172:0144:01a8:trace:seh:sigsys_handler SIGSYS, rax 0x55, rip 0xe2068a.
190387.172:0144:0268:warn:seh:dispatch_exception backtrace: --- Exception 0xc000001d.
190387.172:0144:0268:trace:seh:dispatch_exception code=c000001d (EXCEPTION_ILLEGAL_INSTRUCTION) flags=0 addr=00000001415B1D6C
190387.172:0144:0268:trace:seh:dispatch_exception rip=00000001415b1d6c rsp=0000000017a1dbd8 rbp=0000000017a1dd11 eflags=00010206
190387.172:0144:0268:trace:seh:dispatch_exception rax=0000000017a1dc40 rbx=0000000307ed2520 rcx=0000000000de3028 rdx=0000000000000040
190387.172:0144:0268:trace:seh:dispatch_exception rsi=0000000017a1df10 rdi=0000000307ed23d0  r8=000000000000ffff  r9=00000000000001f3
190387.172:0144:0268:trace:seh:dispatch_exception r10=000000014a8850e0 r11=0000000017a1dbc0 r12=0000000000000020 r13=0000000307ed9000
190387.172:0144:0268:trace:seh:dispatch_exception r14=00000003082c80b0 r15=0000000000000000 mxcsr=00001faa cs=0033 ss=002b
190387.172:0144:0268:trace:seh:call_vectored_handlers calling handler at 0000000145374FC8 code=c000001d flags=0
190387.172:0144:0268:trace:seh:call_vectored_handlers handler at 0000000145374FC8 returned ffffffff
```
</details>

I am already using low environment and texture settings.

## Comment 5058190228

maintainer (MEMBER) · kisak-valve · 2026-07-23T12:07:20Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5058190228

Forza Horizon 6 – Microsoft authentication succeeds but Xbox profile initialization fails on Steam Deck

Issue transferred from https://github.com/ValveSoftware/Proton/issues/10000.
@Scrali posted on 2026-07-23T09:06:42:

## System Information

- Steam Deck OLED
- SteamOS Stable (latest)
- Game: Forza Horizon 6 (Steam)
- Proton: all 
- Steam Account: scrali

## Problem

Microsoft authentication completes successfully using the QR code sign-in.

After authentication, the game immediately displays:

> "Sign In Required - You may not proceed without being signed in to a profile."

The Xbox profile is never loaded.

## Expected behavior

After signing in with Microsoft, the game should load my Xbox profile and synchronize my cloud save, exactly as it does on Windows.

## Actual behavior

Authentication succeeds, but profile initialization fails.

## What I tested

- Same Steam account on Windows → Works perfectly.
- Same Xbox account on Windows → Works perfectly.
- Cloud save loads correctly on Windows.
- On Steam Deck, a second Xbox account (without a Steam license) reaches the expected **"Account Mismatch"** screen.
- Reinstalled the game.
- Deleted the Proton prefix.
- Verified game files.
- Tested Proton Stable, Hotfix and Experimental.
- Signed out and back into the Microsoft account several times.

## Conclusion

The authentication process appears to work correctly.

The failure occurs after successful Microsoft sign-in, when Forza Horizon 6 attempts to initialize the Xbox profile on SteamOS/Proton.

Since the exact same Steam account and Xbox account work correctly on Windows, this appears to be a SteamOS/Proton-specific issue rather than an account or licensing problem.

If needed, I can provide Proton logs and screenshots.

## Comment 5123330600

other (NONE) · ChivuAndrei2003 · 2026-07-29T21:01:07Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5123330600

I can reproduce severe and frequent traversal stutter on a **256 GB Steam Deck LCD** running the latest stable SteamOS and the latest Proton Experimental.

The issue is especially noticeable in **Tokyo City**. The stutters become more frequent and severe when driving at high speed, which makes it appear related to world or asset streaming rather than normal low framerate.

The game can otherwise maintain a reasonable average framerate, but the frametime spikes make driving feel very inconsistent. Repeatedly driving through the same areas does not appear to eliminate the stuttering completely.

### Configuration

- **Device:** Steam Deck LCD 256 GB
- **SteamOS:** Latest stable version
- **Proton:** Latest Proton Experimental
- **Ray tracing:** Disabled
- **Installation location:** Internal SSD
- **Graphics preset:** very low with environmental textures textures on low 
- **FPS limit:** off

I can provide a MangoHud frametime graph or a short recording from a reproducible route in Tokyo City if that would be useful.

## Comment 5161766744

other (NONE) · NKkrisz · 2026-08-03T02:44:10Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5161766744

Anyone else not really able to use online/multiplayer features (e.g. convoys, see players on the map instead of drivatars, online races)?

This has been happening to me for over week now on both my Steam Deck running SteamOS and desktop using Fedora Linux 44 KDE Edition.

Saw some other similar reports on [Reddit](https://www.reddit.com/r/ForzaHorizon/comments/1v9e0zd/fh6_steam_multiplayer_not_working_any_fixes/) and Steam, maybe it might be a Linux/Proton related issue?

So far I have tried different Proton versions, disabling/enabling crossplay, signing in/out my Microsoft account, but no luck. Online information in the game's settings seem to indicate everything is fine even though that's not the case.

## Comment 5161857791

other (NONE) · dino460 · 2026-08-03T03:03:16Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5161857791

I've still barely been able to play. I've managed to play a little while around launch, but the updates rapidly broke the game more and more. Now, no matter what either the game barely goes above 40 FPS with HEAVY unplayable stuttering, or outright doesn't launch. 

I'm on Pop OS 22.02
GPU: intel i5-10400f
GPU: NVIDIA RTX 2080Ti (610.43 X11 proprietary)
RAM: 16GB (DDR4 2666MHz)
1TB M.2 SSD (ext4) with plenty of free space

No matter the settings (no RT, with and without DLSS/DLAA) the game stutters like crazy. I've tried multiple launch arguments from here and from ProtonDB, with Proton Cachy, GE, Hotfix, Experimental. I have a friend with a similar PC on Windows that can play with pretty good performance, which is extremely frustrating.

## Comment 5169575773

other (NONE) · eyenalxai · 2026-08-03T17:22:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5169575773

does it still stutter on AMD GPUs? particularly on 9000s series if that matters

## Comment 5169947689

other (NONE) · rafalcieslak · 2026-08-03T17:58:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5169947689

> Anyone else not really able to use online/multiplayer features (e.g. convoys, see players on the map instead of drivatars, online races)?

@NKkrisz Not sure how much this help you, but I had a similar problem where overall the connection to game servers seemed fine, I passed diagnostics, could view leaderboards download tunes and liveries, but newer saw any other players (couldn't enable Horizon Life) and couldn't purchase aftermarket cars (the game asked me to complete prologue first, which I did long before).

In my case it was related to using `ipv6.disable=1` in my kernel cmdline, which completely deactivates IPv6 system-wide. *Removing* this option resolved my issues, and I could use all online features normally.

Which is a bit odd, because neither my ISP nor my home router support IPv6. This suggests the game doesn't actually need IPv6 connectivity, but gets confused when IPv6 support is completely missing.

This theory is lightly supported by the fact that one of the more common tips for fixing Forza Horizon 5 connectivity _on Windows_ was installing Teredo daemons (an IPv6 tunneling technology). Apparently this game engine is sensitive to IPv6 availability.

## Comment 5187266279

other (NONE) · Scrali · 2026-08-05T03:41:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5187266279

> Replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5058190228
____________________________________________________________________________________________________________________________________________________

Update: I finally solved the issue

After several weeks of troubleshooting with Steam Support, Xbox Support, Forza Support, and testing many different solutions, I finally managed to fix the problem.

The error I was getting was:

"Sign In Required – You may not proceed without being signed in to a profile."

What finally worked
Forced the game to use Proton 11.
Launched the game in windowed mode, because in fullscreen I only had a black screen while the game audio was playing.
Started the game from Desktop Mode on the Steam Deck.
During the Microsoft sign-in process, I changed the sign-in method to use Microsoft Authenticator instead of the default authentication flow.
I completed the sign-in using the Steam Deck's web browser and approved the login with the Microsoft Authenticator app.
It didn't work on the first attempt—I had to repeat the sign-in process several times before it finally succeeded.

Eventually, the Xbox profile loaded correctly, and the game now works normally.

How I found this solution

The idea came to me while testing the sign-in process on my Windows laptop.

I noticed that the Microsoft sign-in interface on my laptop was different from the one displayed on the Steam Deck. I suspected that the authentication flow itself might be different.

I then tried to reproduce that same authentication flow on the Steam Deck by using the browser and Microsoft Authenticator instead of the default login process.

After a few attempts, it finally worked.

Conclusion

I can't say with certainty what the root cause was, but it appears that the issue was related to the Microsoft authentication flow rather than my Xbox account, Steam account, or cloud save.

Hopefully this helps anyone else experiencing the same issue on Steam Deck.

I'd also like to thank everyone who took the time to help me troubleshoot this problem, including the Steam, Xbox, and Forza support teams, as well as the Reddit and Proton communities. Your suggestions and feedback helped me narrow down the cause and eventually find a working solution. I hope this post helps someone else in the future.

## Comment 5191531449

other (NONE) · Koli0842 · 2026-08-05T12:09:21Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5191531449

> does it still stutter on AMD GPUs? particularly on 9000s series if that matters

I think so, yes. I'm currently Proton-GE 11.3, I wanted to try wayland native and never bothered to switch back to upstream Proton. It's also a predictable traversal stutter, for example hotlapping in rivals mode, it always seems to spike at the same place. Feels like some data streaming stuff. I have a 9070XT, and normally around 100 fps.

## Comment 5191744282

other (NONE) · Ramalama2 · 2026-08-05T12:31:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5191744282

Good News, at least for myself xD

RTX6000 + Nvidia 610.57 Drivers + latest https://github.com/CachyOS/proton-cachyos/releases (proton-cachyos-11.0-20260703-slr-x86_64_v3.tar.xz)

Everything Works, Raytracing and everything...
Everything on Ultra(Extreme) with Framegen (2x) @4k = ~120fps
So FPS is really great either.

No Special Starting arguments are required, i removed them all.
Latest Steam Beta + latest gamescope (self compiled etc), and all Updates on Steam etc...

It's the first time since i can even Play the Game and it finally works without any issues!

There are still some minor Bugs, but nothing gamebreaking:
-> After some time, the FPS drops, like there is some leak, after around 2h Gameplay it drops from 120fps to around 80...
-> Im not sure if its FrameGen or another setting, i think its related to Framegen, sometimes going into Pause Menu and back, lets the game somehow weirdly flickering/wiggle, but it fixes itself when entering and exiting the Pause menu again.

That's all, no other bugs.

Cheers

## Comment 5193937629

other (NONE) · arexon · 2026-08-05T15:41:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5193937629

@Ramalama2 do you still get stutters when the textures quality is set to anything but low?

## Comment 5193959705

other (NONE) · enesaltinkaya · 2026-08-05T15:43:40Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5193959705

> [@Ramalama2](https://github.com/Ramalama2) do you still get stutters when the textures quality is set to anything but low?

stutters are still there with 610.57.  
either with low or extreme texture quality.

## Comment 5198579571

other (NONE) · Ramalama2 · 2026-08-05T23:32:55Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5198579571

> [@Ramalama2](https://github.com/Ramalama2) do you still get stutters when the textures quality is set to anything but low?

You mean like missing frames? no its buttery smooth, i think that i get constantly between 80-125fps, 99% of the time 120fps.
1% of the time, i think the lowest by "feeling" probably 80fps...
Just when the game runs for a longer time the fps drops, but its constantly buttery smooth.

With wiggling/flickering i mean -> the picture itself in the gameplay moves every frame around 3-4px into a random direction, its hard to describe. Its definitively not low fps or stutters. And it fixes itself ehen entering/exiting pause menu.

Cheers

## Comment 5199510655

other (NONE) · dino460 · 2026-08-06T01:56:18Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5199510655

Tried using the latest proton-cachy and no args like @Ramalama2 on 610.43 on PopOS but the game crashes before the intro cutscenes with error FHC20

## Comment 5208539306

other (NONE) · Ramalama2 · 2026-08-06T19:24:05Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5208539306

> Tried using the latest proton-cachy and no args like [@Ramalama2](https://github.com/Ramalama2) on 610.43 on PopOS but the game crashes before the intro cutscenes with error FHC20

610.43 crashed here too, but ingame for me. Try 610.57

## Comment 5208637544

other (NONE) · dino460 · 2026-08-06T19:40:33Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5208637544

> > Tried using the latest proton-cachy and no args like [@Ramalama2](https://github.com/Ramalama2) on 610.43 on PopOS but the game crashes before the intro cutscenes with error FHC20
> 
> 610.43 crashed here too, but ingame for me. Try 610.57

I'll try as soon as I can. I'm on PopOS and they still don't have a 610.57 release. Could be a while until then, they tend to be very slow with their NVIDIA driver releases

## Comment 5218968369

other (NONE) · fbt · 2026-08-07T15:30:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5218968369

> RTX6000 + Nvidia 610.57 Drivers + latest https://github.com/CachyOS/proton-cachyos/releases (proton-cachyos-11.0-20260703-slr-x86_64_v3.tar.xz)
> 
> Everything Works, Raytracing and everything... Everything on Ultra(Extreme) with Framegen (2x) [@4k](https://github.com/4k) = ~120fps So FPS is really great either.

Curious. Upgrading to 610.57 for me got rid of the startup crash, and yes, the game now doesn't crash at all with no startup options. But:
- It still performs better with `descriptor_heap`
- There are still these weird slowdowns, mostly in freeroam, as described many times above, with things kinda slowing down, then lurching forward. This doesn't seem to be affected by any of the settings that I've tried. It happens even on the lowest quality preset.

3060Ti (8G VRAM), i5-12600KF, 32G RAM, loads from a modern SSD. X11, no gamescope (it makes things way worse).

It's playable, but behaves like there's a purely software bottleneck somewhere in my case 🤔
The only thing I haven't done after the latest driver update is wipe the prefix, because doing so wipes all your locally saved liveries etc.

UPD: I've bit the bullet and wiped the prefix after sharing all the stuff I cared about. Didn't change a thing. What did help is switching to Proton 11, the one Steam provides. The weird hitching is almost gone, and the game is almost entirely smooth outside of Tokyo.

UPD1: I've also noticed that Horizon 6, and it's the only game that does this, *really* doesn't like it if I have a youtube video running in the background. Stutters, FPS loss. Stop the video, the game becomes smooth. Never seen this before.

## Comment 5227828543

other (NONE) · sapphired18 · 2026-08-08T19:51:14Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5227828543

this is kinda out of topic but,
somebody said the problem is the linux kernel itself 
https://www.reddit.com/r/linux_gaming/comments/1uh21xu/comment/ou4k9y9/?context=3

maybe we need some kernel patch for this https://lists.freedesktop.org/archives/amd-gfx/2026-May/145646.html 
https://lore.kernel.org/lkml/?q=Explicit+sync+for+PRT+unmaps (for amd)

## Comment 5231571694

other (NONE) · Cr0phiXx · 2026-08-09T12:41:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5231571694

I'm on CachyOS, AMD 9800X3D & RTX 4080 (610.57.04) and mainly use the most recent proton-cachyos-slr. At some point the slowdowns/stutters were fixed, but they reappeared in a later proton-cachyos update. 

I switched back to proton-cachyos-11.0-20260506-slr-x86_64_v3, which has been the most stable version for me so far (always running with PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=descriptor_heap in the launch options). Even with this version, though, I'd see FPS dip into the low 90s when spawning at my Garage (Soko 78) and driving left along the coast of the city.

Fix found: Yesterday I came across a mod on Nexus Mods that replaces the D3D12Core.dll shipped with FH6 (an older DirectX 12 Agility SDK build) with a more recent one. After swapping the file in the game folder, the same route now runs at a rock-solid 120 FPS with no dips — tested repeatedly across different in-game weather conditions and times of day. Occasionally it dips to ~105–110 while driving elsewhere with heavy traffic and weather, but this happens far less often than with the old DLL.

For Confirmation: I reverted to the original D3D12Core.dll, and immediately after turning left out of the Garage in the same location/weather/time, FPS dropped back to 95–110.

I'm not sure if I'm allowed to link the mod directly, but it can be found by searching "DirectX 12 Agility SDK For Forza Horizon 6" on Nexus Mods.

## Comment 5305146824

other (NONE) · dino460 · 2026-08-16T01:31:22Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5305146824

Still trying to make it work on my 2080 Ti. I've changed to CachyOS and 610.57.04 driver, but still nothing. Tried Proton 11, Experimental, proton-cachyos-11.0-20260703-slr-x86_64_v3, and nothing. With and without launch options. It either doesn't launch, or freezes at the startup video.

## Comment 5307901273

other (NONE) · dino460 · 2026-08-16T14:23:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5307901273

Reinstalled the game and deleted the intro videos. Now it at least opens and allows me to play with Proton CachyOS 11 20260703 (native) and no arguments. Hitches seem much less present if Environment Quality settings are low, and overall hitching is much better, but there are texture and geometry flickering. Still playable, but slightly annoying for a AAA game...

Last hurdle is the TERRIBLE performance. Although it's playable, on my i5-10400f + 16 GB (2666 MHz) RAM + RTX 2080 Ti it barely scrapes over 30 FPS both on medium and high. Sometimes it spikes to 40-ish, but it's usually around low 30's and even mid to high 20's.

I'll play around with the arguments, but it's still quite sad that performance is so bad, considering a friend with a similar system and slightly worse GPU gets great performance on Windows.

## Comment 5344668075

other (NONE) · Shijikori · 2026-08-19T15:58:51Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5344668075

> replying to https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5231571694

GODS! Thank you SO MUCH! For sharing this dll swap/upgrade

It does not improve performance for me (I'd say it's likely doing the opposite and hurting it to be somewhat inline with the experience I had at launch, which is still acceptable to me). The one thing it does though is... there have been API fixes to GPU synchronization. I no longer experience missing textures, neon texture artifacts or normal map fuckery. It's just as pristine as it was on launch.

That safer GPU synchronization might be what's causing the reduced performance but that's a tradeoff I'm willing to make for a game without jarring texture bugs.

EDIT : Update on that... The texture issues still happen just less often I guess. So that's not a complete fix. Performance seems to be actually inline with what it was before, so i don't know why it was slower the other time i played. I'm just done doing the weeklies so I played long enough to see it happen.

## Comment 5351880202

other (NONE) · fbt · 2026-08-20T05:45:39Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5351880202

> > replying to [#9789 (comment)](https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5231571694)

If you don't trust some random uploader on nexus (which is reasonable), you can grab the new dll from the actual DirectX 12 Agility SDK. You don't have to install anything to just rip the .dll out.

It does, in fact, seem to help.



## Comment 5359591749

other (NONE) · Shijikori · 2026-08-20T17:45:04Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5359591749

From what I can tell, because I'm testing again... I've been running `vm_update_mode=3` for a while due to driver bugs in older kernel versions which caused Minecraft to crash with shaders otherwise. I tried without that option and I get lots of hitching. So, that option definitely helps but, on my system, it also causes issues with the texture streaming which I can't reason for why/when they happen.

EDIT : Forget that, Mesa 26.1.7 introduces the problem causing the hitching because I've just experimented with a couple different options and it still hitches. I think I'll make a local build of a newer release in the mean time to use with anything that is having problems with the new release.

EDIT 2 : PROTON_LOG was set which was the actual reason for the severity of the hitching as it outputs GBs of data in a few minutes. With `vm_update_mode` at default -1 value, it's still hitching and slowing down but that is actually mitigated with a 60fps in-game lock and tweaks to environment quality, like previously reported. So I guess I have the choice between graphical issues with high performance or lower performance without graphical issues. Since I simply intend to no longer run with mode 3 unless more games need it, I think I'll go for the performance tradeoff which removes graphical issues from the equation.

## Comment 5409459862

other (NONE) · linoshkmalayil · 2026-08-25T11:05:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5409459862

> UPD1: I've also noticed that Horizon 6, and it's the only game that does this, _really_ doesn't like it if I have a youtube video running in the background. Stutters, FPS loss. Stop the video, the game becomes smooth. Never seen this before.

Few questions:
Are you using the [nvidia-vaapi-driver](https://github.com/elFarto/nvidia-vaapi-driver)?
Are you doing youtube playback on browser or streaming via video player?

The reason I asked this is because as far as I know NVIDIA does not officially support VAAPI and all the solutions that do GPU accelerated video decoding in Linux on NVIDIA GPUs use CUDA (instead of the video decoder engine) which may cause slowdowns in graphics processing.

## Comment 5430504550

other (NONE) · fbt · 2026-08-26T20:07:27Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5430504550

> Few questions: Are you using the [nvidia-vaapi-driver](https://github.com/elFarto/nvidia-vaapi-driver)? Are you doing youtube playback on browser or streaming via video player?

Nope, stock upstream proprietary driver. It behaves like this when played the browser specifically. But that conversation is probably beyond the scope of the thread, I was just surprised that it seemingly affects Horizon 6 and nothing else.

## Comment 5527213438

other (NONE) · samuelskovbakke · 2026-09-03T14:22:47Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5527213438

Will this Microslop game ever see the light of day on Linux? I get that there are "workarounds", but those do not eliminate stuttering completely, and with every update the game seems to break even harder than before. Is this just me?

## Comment 5528550813

other (NONE) · CRKrJ4K · 2026-09-03T16:08:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5528550813

> Will this Microslop game ever see the light of day on Linux? I get that there are "workarounds", but those do not eliminate stuttering completely, and with every update the game seems to break even harder than before. Is this just me?

I'm sure they have their Copilot data centers working on it as we speak

## Comment 5653613612

other (NONE) · yourfate · 2026-09-13T13:36:54Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5653613612

Regression: game hangs on the first intro video (after the photosensitivity screen).
Video freezes on first frame, audio stops, Steam overlay freezes. Process stays alive
with two threads spinning at 100% CPU, the rest waiting in ntsync/futex.

Worked: 2026-09-09 (NVIDIA 610.57.04, kernel 7.2.2-cachyos)
Broken since system update 2026-09-12: NVIDIA 615.71.09 (open modules), kernel 7.2.4-cachyos.
Game build 25104224 (unchanged between working and broken). intel i5-13600k, RTX 4090, KDE Plasma 6.7.5 Wayland.

Same result with Proton Experimental, proton-cachyos (SLR and native builds).
PROTON_NO_NTSYNC=1 does not help.

Timing-sensitive:
- PROTON_LOG=1                         -> works
- PROTON_LOG=1 WINEDEBUG=-all          -> hangs
- PROTON_LOG=1 WINEDEBUG=+seh          -> works
The exe raises ~280k handled EXCEPTION_ILLEGAL_INSTRUCTION (vectored handler) during
startup, so the slowdown from +seh tracing seems to hide a race.

System info: https://gist.github.com/yourfate/9b7bb4e87d202009ec326420fcc5cca1


I tried debugging this with the help of claude, this is the result.

## Comment 5739982298

other (NONE) · Kwarrtz · 2026-09-19T06:39:46Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5739982298

I'm also having significant stutters, but no crashes on any graphics settings I've tried (including raytracing). The pattern to the stutters is:
- While moving they're continuous, happening every couple of seconds, but are completely absent when stationary. They seem more frequent at higher speeds.
- They persist largely unchanged on the second lap of a track (i.e. they're independent of caching).
- They happen everywhere on the map, not only in dense city regions.
- With VSync on the stutters are reflected in the Steam overlay 1% low graph, with VSync off it's much less consistent whether they're caught.
- They are as far as I can tell independent of graphics settings and FPS cap. They occur on Low and Ultra, with and without RT.

I've tried Proton Experimental, Hotfix, 9, and the CachyOS SLR fork, as well as half a dozen launch option combinations mentioned in this thread, none of which makes a difference.

The one thing I noticed which I haven't seen reported elsewhere is that the stutters seem to correlate with large storage reads, as reported by both mangohud and iostat, leading me to believe that (in my case at least) it's an asset streaming issue. iostat shows r_await hovering around 0.3 ms and aqu-sz around 0-0.2 even while the stutters are occuring, plus the game is installed on a fast NVMe, so I don't _think_ it's an actual storage issue. Still, just in case, I tried:
- switching the I/O scheduler from kyber to none,
- raising the lookahead to 4096,
- setting `nvme_core.default_ps_max_latency_us=0`,

none of which made a difference. 

Other apparent non-issues: I have multiple GBs of headroom in both system RAM and VRAM while playing, and CPU and GPU utilization as reported by mangohud are relatively consistent through the stutters. A `perf` sample during 30 seconds of driving with heavy stutters showed `[JIT] tid 10316` at 50%, `ntdll.dll` at 5%, and nothing else above 5%.

Software info: CachyOS, kernel 7.2.5-1, KDE Plasma 6.7.5, mesa 3:26.2.2-2
Hardware info: Ryzen 9700X, RX 9070 XT, 32 GB DDR5-6000, Samsung 990 Pro 4 TB

## Comment 5752857760

other (NONE) · To0wnn · 2026-09-20T21:39:47Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5752857760

# Forza Horizon 6 — crash at `section_two_transition_in` (2nd cutscene)

**Update (23 Sep 2026): solved, and it was not Proton or the driver. It was the game build.**

I originally reported this as a driver/vkd3d issue. That was wrong, and I'm correcting it here in case anyone else is chasing the same ghost.

## What actually fixed it

Updating the game from **build 354221** to **build 440853**. Nothing else changed — same GPU, same driver (615.71.09), same GE-Proton11-7, same headless setup.

Build 354221 crashed at the second cutscene every single time, 4–8 minutes in. Build 440853 has been stable for hours.

Looking back at this thread, everyone who reported getting *past* the intro was already on a newer build. That correlation was there all along; I just didn't see it.

## What did NOT help (all reverted)

In case it saves someone the effort — none of these made any difference on 354221:

| Attempt | Result |
|---|---|
| Driver downgrade 615.71.09 → 610.57.04 | no change |
| `VKD3D_CONFIG=single_queue` / `descriptor_heap` / `no_upload_hvv` combinations | no change |
| `WINEFSYNC=0` | changed the failure mode (ACCESS_VIOLATION → clean watchdog exit), didn't fix it |
| `VKD3D_DISABLE_EXTENSIONS=VK_EXT_mesh_shader,VK_NV_raw_access_chains` | no change |
| Replacing `D3D12Core.dll` with a newer Agility SDK | no effect — `WINEDLLOVERRIDES` has `d3d12core=n`, so vkd3d-proton's own is used regardless |
| Patching the game's PlayFab/libHttpClient DLLs | no change (this was me going down a rabbit hole) |

## The one genuinely useful finding

If you launch `wine` directly from the GE-Proton tree instead of going through the `proton` entry point, **most `PROTON_*` variables silently do nothing**. Verified with `grep -rl` across every binary in `files/{lib,lib64,bin}`:

```
PROTON_ENABLE_WAYLAND       only in the proton script   → no-op
PROTON_DISABLE_LSTEAMCLIENT not found anywhere          → no-op
PROTON_USE_NTSYNC           not found anywhere          → no-op
PROTON_VKD3D_HEAP           not found anywhere          → no-op
VKD3D_CONFIG                found in d3d12core.dll      → works
WINEFSYNC                   found in ntdll.so           → works
```

Also worth knowing: wine logs `ntsync: up and running` and `/dev/ntsync` exists, but `strings` on `ntdll.so` shows no ntsync code at all — only fsync. So `WINEFSYNC` is the only sync knob that does anything in this build.

If you're troubleshooting a non-Steam launch, verify your launch options actually reach the game before drawing conclusions from them. I wasted days on variables that were never read.


## Comment 5754528409

other (NONE) · edmundselliot · 2026-09-21T02:14:03Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5754528409

Reporting a crash during gameplay on September 20, 2026. The game ran for approximately 11 minutes before exiting. Its crash report records `tokyo_tower`, online `Life` mode, and `ACCESS_VIOLATION_WRITE`. Reproducibility has not yet been established; this is one captured incident.

### System and versions

- Steam AppID: 2483190
- Game build: 440853; Steam build ID: 25104224
- Ubuntu 26.04 LTS; kernel 7.0.0-31-generic; GNOME Wayland session
- Intel Core Ultra 7 265F; NVIDIA GeForce RTX 5070
- NVIDIA Linux driver: 595.84
- Proton Experimental; installed version file checked after the crash: `experimental-11.0-20260910b-x86_64`
- Graphics: 3440×1440, Extreme preset, 60 FPS limit, ray tracing / frame generation / Reflex off

Steam's launch record for this session includes these options (log directory omitted):

```text
PROTON_LOG=1 PROTON_VKD3D_HEAP=1 VKD3D_CONFIG=enable_experimental_features,descriptor_heap VKD3D_DISABLE_EXTENSIONS=VK_EXT_mesh_shader,VK_NV_raw_access_chains %command%
```

### Captured failure

The game report and Wine debugger agree on a write access violation at `forzahorizon6.exe+0x1e3fe93`, attempting to write to `0x146dfea88`. The debugger shows `lock cmpxchgl %ecx, 8(%r8)` with `r8=0x146dfea80`. The first 15 stack-frame offsets agree with the game's own crash report.

The kernel journal contains no entries around the crash (19:04–19:11 PDT), including no NVIDIA Xid or OOM kill. The game reports `D3D_HR_ERROR=0` and VRAM usage below its reported budget. No recent minidump was found in the game directory or Proton prefix.

This identifies the immediate exception, but does not establish the upstream cause or whether it is a game or Proton defect. No controlled comparison with another Proton version has been performed for this incident.

<details>
<summary>Game CrashReport.xml — selected diagnostic fields</summary>

```xml
<BUILD Value="440853" />
<UTC Value="2026-09-21_02-09-49" />
<D3D_HR_ERROR Value="0x00000000" />
<LOCATION Value="tokyo_tower" />
<ONLINE Value="Life" />
<UPTIME Value="665.331055" />
<STACK_TRACE Value="0x1e3fe93,0x4c190f6,0x4c18845,0x4c16024,0x38bb6d2,0x4c1f693,0x4c20e64,0x4c0176b,0x4008382,0x214a260,0xec0d35,0x2a7016e,0x2a6ff4e,0x42a3ab,0x3524f76,0x0," />
<STACK_HASH Value="0x133c7a21" />
<REASON Value="Unhandled Exception" />
<EXCEPTION Value="ACCESS_VIOLATION_WRITE" />
<EXCEPTION_INFO Value="0x0000000146dfea88" />
<VRAM_BUDGET Value="10827857920" />
<VRAM_USED Value="9574481920" />
<CRASH_FROM_ASSERT Value="0" />
```

</details>

<details>
<summary>Proton log — Wine debugger registers and backtrace</summary>

```text
Unhandled exception: page fault on write access to 0x0000000146dfea88 in 64-bit code (0x00000141e3fe93).
0904:fixme:dbghelp:elf_search_auxv can't find symbol in module
Register dump:
 rip:0000000141e3fe93 rsp:0000000016a9f2b0 rbp:00000003fa6aa8d0 eflags:00010202 (  R- --  I   - - - )
 rax:0000000044066940 rbx:00000003fc15bf90 rcx:0000000044066941 rdx:0000000016a9f330
 rsi:0000000016a9f330 rdi:0000000016a9f378  r8:0000000146dfea80  r9:0000000000000047 r10:0000000000000000
 r11:0000000000000202 r12:000000002fcaaf50 r13:0000000000000001 r14:0000000016a9f4f8 r15:0000000000000000
Stack dump:
0x00000016a9f2b0:  00000003fa528e68 0000000141e3feb3
0x00000016a9f2c0:  0000000016a9f350 0000000140956219
0x00000016a9f2d0:  0000000000000000 0000000000000000
0x00000016a9f2e0:  0000000016a9f378 0000000144c190f6
0x00000016a9f2f0:  00000003fc26ed78 00000000ffffffff
0x00000016a9f300:  00006ffffff3f034 00006ffffff61617
0x00000016a9f310:  00000003fc15bf90 00000003fc26ed78
0x00000016a9f320:  00000003fa6aa8d0 0000000144c18845
0x00000016a9f330:  0000000000000000 00000003fa529528
0x00000016a9f340:  00000003f88de8e0 00000003f88dba50
0x00000016a9f350:  00000003fa5ccfc0 00000003fa529528
0x00000016a9f360:  0000000000000000 0000000144c16024
Backtrace:
=>0 0x00000141e3fe93 in forzahorizon6 (+0x1e3fe93) (0x000003fa6aa8d0)
  1 0x00000144c190f6 in forzahorizon6 (+0x4c190f6) (0x000003fa6aa8d0)
  2 0x00000144c18845 in forzahorizon6 (+0x4c18845) (0x000003f88de8e0)
  3 0x00000144c16024 in forzahorizon6 (+0x4c16024) (0x00000016a9f3b0)
  4 0x000001438bb6d2 in forzahorizon6 (+0x38bb6d2) (0x00000016a9f469)
  5 0x00000144c1f693 in forzahorizon6 (+0x4c1f693) (0x00000016a9f570)
  6 0x00000144c20e64 in forzahorizon6 (+0x4c20e64) (0x00000016a9f570)
  7 0x00000144c0176b in forzahorizon6 (+0x4c0176b) (0000000000000000)
  8 0x00000144008382 in forzahorizon6 (+0x4008382) (0000000000000000)
  9 0x0000014214a260 in forzahorizon6 (+0x214a260) (0x00000016a9f7c0)
  10 0x00000140ec0d35 in forzahorizon6 (+0xec0d35) (0x00000016a9f7c0)
  11 0x00000142a7016e in forzahorizon6 (+0x2a7016e) (0000000000000000)
  12 0x00000142a6ff4e in forzahorizon6 (+0x2a6ff4e) (0x00000016a9ff79)
  13 0x0000014042a3ab in forzahorizon6 (+0x42a3ab) (0x00000016a9ff79)
  14 0x00000143524f76 in forzahorizon6 (+0x3524f76) (0x00000016a9ff79)
  15 0x006fffffec1649 in kernel32 (+0x11649) (0x00000016a9ff79)
  16 0x006ffffff40e0f in ntdll (+0x10e0f) (0x00000016a9ff79)
  17 0x00000145432baa in forzahorizon6 (+0x5432baa) (0x00000016a9ff79)
0x00000141e3fe93 forzahorizon6+0x1e3fe93: lock cmpxchgl %ecx, 8(%r8)
```

</details>

These are excerpts from the captured reports, not a complete Proton log. The rotated Proton logs have been retained locally. Is there a specific logging configuration or runtime capture that would help investigate this signature?


## Comment 5879379794

other (NONE) · coops924 · 2026-09-28T21:49:31Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5879379794

Adding some data on the stutter side in case it helps whoever ends up looking at perf.

Setup: RX 6900 XT, Ryzen 9 7950X3D, 96GB RAM, CachyOS (kernel 7.2.8), Mesa 26.2.3, Proton Experimental bleeding-edge (11.0-442053-20260928).

I'm seeing basically what @Kwarrtz described. While driving I get short stalls, for me roughly every 10 seconds, 60-150ms each. Graphics settings make no difference (maxed out without upscaling still hitches the same), CPU load is low when it happens and GPU clocks don't move. Never had this on Windows on the same machine.

With PROTON_LOG=1 the log is almost entirely `EXCEPTION_ILLEGAL_INSTRUCTION` (c000001d), around 30k per second during gameplay, coming from several threads and all handled by a vectored handler inside forzahorizon6.exe (handler at 0x1453B0E88, one of the faulting addresses is 0x1454CA3A7). I'm assuming that's the anti-tamper. The log hit 4.7GB in about two minutes.

The interesting part is that with logging on (so every exception gets slower) the stalls got way worse. The game would stop submitting to the direct queue for 100-220ms about every 1.1s. I had VKD3D_QUEUE_PROFILE running at the same time, and during those gaps there are no long fence waits and no sparse binding activity, it just isn't submitting anything. So it really looks like exception dispatch cost is what stalls the render thread, and my guess is the normal-speed case is the same thing just less often.

For reference a bare SIGILL round trip on this kernel is ~1.6us, so at 30k/s the kernel side is small. Most of the cost has to be on the Wine dispatch side.

Happy to share the queue profile or a trimmed log if anyone wants them.


## Comment 5879874518

other (NONE) · Avrarus · 2026-09-28T22:27:32Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5879874518

System Information
- GPU: NVIDIA GeForce RTX 3060 (Low Hash Rate)
- Video driver version: NVIDIA 615.71.09 (open kernel modules, nvidia-open-dkms)
- Kernel version: Linux 7.2.8-1-cachyos
- Distro: CachyOS
- Proton versions tested: Proton Experimental (bleeding-edge), Proton Hotfix, Proton-CachyOS (SLR and native)

Symptoms
The game never shows any window, black or otherwise. Steam shows the game as running, and the process consumes ~99-100% of one CPU core continuously. It self-terminates after roughly 60-90 seconds with no error in the Proton log, no Wine exception, no vkd3d output, and no kernel Xid or segfault.

This happens with every launch option combination I've tried (descriptor_heap, enable_experimental_features, PROTON_VKD3D_HEAP=1, empty launch options, PROTON_ENABLE_WAYLAND=1 with and without), on both X11 (implicitly via XWayland) and native Wayland front-ends. Prefix was wiped between tests. Shader cache was cleared between tests.

Debugging with gdb while the process is running (thread apply all bt on all threads) shows:
- Two worker threads idle in NtWaitForSingleObject (normal)
- The main thread is spinning in a busy loop entirely inside forzahorizon6.exe itself, near the D3D12SDKVersion export, never entering vkd3d-proton, Wine's d3d12/dxgi code, or any driver code.

Proton logs (WINEDEBUG=+loaddll) show the game loading through COMCTL32.dll and then, in the same run, Mono/Xalia components load (these are Proton's own, not the game's), and the process exits shortly after. No d3d12.dll internals, no dxgi calls, and critically no vkd3d-proton log lines appear at all (tested with VKD3D_DEBUG=warn), meaning the game never reaches the point of creating a D3D12 device.

This looks different from the reported black-screen-until-focused issue (already fixed) and from the in-game GPU-hang crashes discussed above. It looks like the game hangs in its own startup code before ever touching the renderer — possibly around GDK/Xbox services initialization, though I have not been able to confirm that specifically.

Happy to provide the full Proton log, the gdb backtrace output, or test further launch option combinations if useful.

## Comment 5924926492

other (NONE) · Kwarrtz · 2026-10-01T04:46:11Z · https://github.com/ValveSoftware/Proton/issues/9789#issuecomment-5924926492

Following up on my previous comment, I think I've narrowed down the cause of my stuttering quite a bit. TLDR; it's definitely occurring during asset streaming, maybe as a result of the GPU stalling while memory for tiled textures gets remapped. As I guess others have reported in the past, setting Environment Texture Quality to Low greatly reduces (but does not eliminate) the stutters, while no other setting I tried makes a significant difference. Also, I did see the same exceptions as @coops924 but I'm relatively confident they're not related, at least in my case.

<details><summary>I'll put some of my detailed testing results below. If anyone wants to see specific raw logs I'm happy to provide them.</summary>

**System:** 9700X, 9070 XT, CachyOS (kernel 7.2.7), mesa 3:26.2.3
**Game settings:** graphics preset Ultra (no RT), no launch options, Proton Experimental 11.0-20260924

As stated before, the primary symptom is that I experience significant, randomly-timed stutter while driving anywhere on the map above speeds of about 100 kph, which vanish completely when stationary. According to mangohud frametime logging the stutters manifest as 50-400 ms windows of roughly doubled frametimes, totalling to around 100 ms/s of lost time on average.

In my last comment I said that GPU utilization is steady during the stutters, which is true as reported by mangohud, but *not* by amdgpu_top. When I'm parked with no stuttering, amdgpu_top shows steady GFX utilization at around 98%, but when driving it fluctuates in the range 75-90%. I'm guessing the discrepancy is down to additional smoothing/coarser sampling on the mangohud side, or maybe different definitions of what constitutes a busy core. In any case, the stutters do seem to correlate with _some_ amount of genuine GPU stalling.

My Proton logs looked exactly like coops described, 9 GB of the same error. I also saw the periodic stutters every second with logging turned on. However, with logging off, the exceptions don't seem to correlate with the stutters at all. Based on some `perf stat -e signal:signal_deliver` runs, they come in regular bursts, and happen exactly as often while parked as while driving (about 37,000 per second). So, not sure what's going on there, but I don't think it's related.

As I noted before, the stutters _do_ seem to line up very well with disk reads, which I was able to confirm a bit more quantitatively by running mangohud logging and `perf stat -e syscalls:sys_enter_pread64` simultaneously. However, `perf trace` never caught a pread longer than 5 ms, so I still don't think disk IO is itself the cause of the slowdowns. Instead, the best candidate I was able to find for a culprit is `amdgpu_gem_va_ioctl`, which I understand to be the main handler function for mapping and unmapping GPU virtual memory. `funclatency` showed ~5,000 calls/s when driving, adding up to total wall clock time of right around the expected 100 ms/s, compared with basically 0 while parked. I also ran with `VKD3D_QUEUE_PROFILE=1` and looking at the results by eye in Perfetto, it does seem like almost all of the windows of long frametimes are associated with `SPARSE FLUSH`es on the copy queue track. Finally, `perf lock` shows much higher activity on `drm_exec_lock_obj` while driving (~500 waits/s, ~20 ms/s) than while parked. So, all that together with the dependence on environment texture quality is why I'm suspecting that heavy memory remapping during asset streaming is what's stalling out the GPU. Somehow.

Also, for completeness, I tried `VKD3D_CONFIG=no_upload_hvv`, `RADV_PERFTEST=localbos`, and disabling ReBAR in UEFI, none of which had a noticeable impact.

</details>
