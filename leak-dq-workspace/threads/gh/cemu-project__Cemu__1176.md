# AMD 780M Vulkan renderer leads to corrupted textures 

- URL: https://github.com/cemu-project/Cemu/issues/1176
- Repo: cemu-project/Cemu (language: C++)
- State: open; created 2024-04-15T14:49:43Z; status ok; passes offcwe

## Issue body

reporter (NONE) · Not4ce · 2024-04-15T14:49:43Z · https://github.com/cemu-project/Cemu/issues/1176

### Current Behavior

Enabling vulkan on rdna 3 based cards, such as 780m igpus break pebbles and textures in-game. Also broken shadows that eventually garble and have corrupted textures. Observed in MK8 and BOTW. No graphical or texture enhancements applied, can be replicated on two seperate 780m devices

Vram allocation does not change anything. Only fixed by changing renderer to OpenGL, and seems to be Rdna3/780m specific. Was unable to test on a discrete rdna3 card, no issue on Rdna2 and Nvidia counterparts (6800xt and 3070)

### Expected Behavior

Nil graphical issues and not garbled textures 

### Steps to Reproduce

Enabling vulkan renderer 
Playing any game: Breath of the wild etc

### System Info (Optional)

OS: Windows 11 22631.3374	KB5035942
GPU: 780M on Ryzen Z1 Extreme and 7840u


### Emulation Settings (Optional)

Default with no mods or changed 

Also Tested with: 
BCML enabled 
Second Wind enabled 
No graphical mods or changes on 1.2.6 and 2.0 cemu 

### Logs (Optional)

[log.txt](https://github.com/cemu-project/Cemu/files/14980653/log.txt)

Tested with OpenGl that had no issues, followed by switching to Vulkan with issues (UMA frame buffer set to 6gigs on system) 

## Comment 2057100121

maintainer (MEMBER) · Exzap · 2024-04-15T15:12:05Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2057100121

Edited to update: This should be fixed in 2.7. Early beta builds are available for testing at https://cemu.info/ActionBuilds.php

## Comment 2057112316

maintainer (MEMBER) · Exzap · 2024-04-15T15:17:40Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2057112316

Something you can do to help in the meantime is upload a Vulkan validation log. The steps to do this are:
1) Download the Vulkan SDK and install it from [here](https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-sdk.exe) (you can uninstall it afterwards)
2) Restart your PC
3) Open Cemu (use a recent version like v2.0-78), in the menu tick `Debug -> Logging -> Vulkan validation layer`
4) Trigger the glitch (avoid doing too much other stuff, it makes the log harder to read)
5) Upload log.txt

## Comment 2057114899

reporter (NONE) · Not4ce · 2024-04-15T15:18:53Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2057114899

> AMD has a track record of needing 1-2 years to get their drivers up to standard (we have reports like this for every new generation). This combined with the fact that it works on everything else points towards an issue with their driver. However, we don't know for certain unless someone does some digging. I will keep this open for visibility and in case someone with the affected hardware and the necessary know-how wants to look into this.

Thank you for getting back. I had a similar line of thought and I found this very strange, as I am unable to replicate this on RDNA 2

As per AMDs own documentation, their vulkan implementation is the exact same on both RDNA 2 and 3. I wish I had a discrete RDNA 3 card to test this, but if a future driver update from AMD remedies the issue, I will update or close this ticket 

As it stands, I am disappointed at amd, as all handheld devices use AMD Apus, and I am unable to distinguish if this is an APU driver or RDNA 3 issue 

PS: I tried seperate driver versions and ddu with no success. Thank you for keeping an eye on this 

## Comment 2057228713

reporter (NONE) · Not4ce · 2024-04-15T16:11:48Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2057228713

> Something you can do to help in the meantime is upload a Vulkan validation log. The steps to do this are:
> 
>     1. Download the Vulkan SDK and install it from [here](https://sdk.lunarg.com/sdk/download/latest/windows/vulkan-sdk.exe) (you can uninstall it afterwards)
> 
>     2. Restart your PC
> 
>     3. Open Cemu (use a recent version like v2.0-78), in the menu tick `Debug -> Logging -> Vulkan validation layer`
> 
>     4. Trigger the glitch (avoid doing too much other stuff, it makes the log harder to read)
> 
>     5. Upload log.txt

The last version I tried which is [this](https://github.com/cemu-project/Cemu/releases/tag/v2.0-46) was broken 

**However, 2.0-78 has seemingly fixed the issue!** Heres the log attached below with vulkan debugger

What I can conclude is the last version I had downloaded (2.0-46) just did not play nice. Strangely my 6800xt never had issues with any version (including 1.2.6), so its rdna3 driver related bug on older builds
[log.txt](https://github.com/cemu-project/Cemu/files/14981549/log.txt)

Image of 1.2.6 corruption:
<img width="960" alt="1 2 6f" src="https://github.com/cemu-project/Cemu/assets/167106518/1e33a3d0-ff4d-43ae-994b-87f17f003635">

Thank you for walking me through this 

## Comment 2058323663

reporter (NONE) · Not4ce · 2024-04-16T06:27:36Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2058323663

Welp, @Exzap turns out Cemu2.0-78 only fixes the pebbles or greatly reduces the amount of initial corruption. After further playing the game and wind waker, the issue is still present. I have recorded a video for reference and the prior vulkan debug log is still valid 

As usual, I'm unable to replicate this on my desktops with rdna2 and ampere cards and can reliably repeat this on any 780m based device like Ally/Win. The only fix is using OpenGL and rolling back drivers doesn't change anything 

Kindly let me know if you require further logs or information, kind regards

https://github.com/cemu-project/Cemu/assets/167106518/90821224-c345-43a7-bb59-38f82fcb9135

## Comment 2150922164

other (NONE) · Squall-Leonhart · 2024-06-05T20:36:56Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2150922164

> As per AMDs own documentation, their vulkan implementation is the exact same on both RDNA 2 and 3. I wish I had a discrete RDNA 3 card to test this, but if a future driver update from AMD remedies the issue, I will update or close this ticket

Their Hardware ISA however, is not.
RDNA3 has an ISA bug with signedness reinterpretation for example.

More recent findings have come to light regarding the Gfx11 Delta colour changes and their assumption of a general compressed layout for resources + abitrary reinterpretation for DCC introduced somewhat of a perfect storm for graphical misbehavior if assumptions have been made, or if a particular sampler needs a particular layout when attempting to reuse it in a feedback loop.

RDNA2 _is_ affected under very specific conditions, the van gogh in the steam deck for instance has artifacts in WWHD, and the same set of extensions that should resolve RDNA3's texture layout misbehavior resolved similar troubles DXVK had with RDNA2 in games such as GTA4,  with RDNA3 no known operations will result in a DCC being disabled,  which was not highlighted in the ISA manual but had to be dug out of their PAL or MESA commits. GPU-Open has not been updated for these ISA changes either.

## Comment 2160580144

reporter (NONE) · Not4ce · 2024-06-11T11:58:48Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2160580144

> > As per AMDs own documentation, their vulkan implementation is the exact same on both RDNA 2 and 3. I wish I had a discrete RDNA 3 card to test this, but if a future driver update from AMD remedies the issue, I will update or close this ticket
> 
> Their Hardware ISA however, is not. RDNA3 has an ISA bug with signedness reinterpretation for example.
> 
> More recent findings have come to light regarding the Gfx11 Delta colour changes and their assumption of a general compressed layout for resources + abitrary reinterpretation for DCC introduced somewhat of a perfect storm for graphical misbehavior if assumptions have been made, or if a particular sampler needs a particular layout when attempting to reuse it in a feedback loop.
> 
> RDNA2 _is_ affected under very specific conditions, the van gogh in the steam deck for instance has artifacts in WWHD, and the same set of extensions that should resolve RDNA3's texture layout misbehavior resolved similar troubles DXVK had with RDNA2 in games such as GTA4, with RDNA3 no known operations will result in a DCC being disabled, which was not highlighted in the ISA manual but had to be dug out of their PAL or MESA commits. GPU-Open has not been updated for these ISA changes either.

Hey, thank you for clarifying that and filling in the gaps. I assumed 2 and 3 used the same ISA but that certainly explains the discrepency here

As far as I can tell, all RDNA3 cards are affected including someone I know with a 7900XTX. Seems like its a waiting game for RDNA 3 users which is a shame, as a lot of portables are/will be based on RDNA 3/3.5

## Comment 2342713665

other (NONE) · dstrnad · 2024-09-11T06:17:18Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2342713665

Just fyi, similar issue was recently fixed in ryujinx and sudachi. Tested on BOTW. Dont know if it is exactly the same issue, but the artifacts/ glitches looked exactly the same in the switch version like they look in cemu. So there might be a way to fix it despite the fact that it is probably RDNA driver related?

## Comment 2343215704

maintainer (MEMBER) · Exzap · 2024-09-11T10:11:01Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2343215704

They implemented the `VK_EXT_attachment_feedback_loop_layout` extension which fixed it. This extension has been on our radar for a while since it would probably also help us improve performance.
Unfortunately it's not trivial to implement the extension and since I am bogged down by other work right now I can't work on it anytime soon. But if anyone else wants to take a shot that would be appreciated

For context ryujinx' PR: https://github.com/Ryujinx/Ryujinx/pull/7226

## Comment 2355785060

reporter (NONE) · Not4ce · 2024-09-17T13:23:13Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2355785060

> They implemented the `VK_EXT_attachment_feedback_loop_layout` extension which fixed it. This extension has been on our radar for a while since it would probably also help us improve performance. Unfortunately it's not trivial to implement the extension and since I am bogged down by other work right now I can't work on it anytime soon. But if anyone else wants to take a shot that would be appreciated
> 
> For context ryujinx' PR: [Ryujinx/Ryujinx#7226](https://github.com/Ryujinx/Ryujinx/pull/7226)

Even though you guys cant work on it anytime soon, I appreciate the heads up with this being on your radar. As more gaming handhelds ship with amd apus, this being broken on 24.8.1 still mean the most popular gaming handhelds are locked out (Rog ally, legion go, acer, zotac devices)

But i appreciate the ongoing improvements that go into cemu and the work that contributors put in. I am hopeful this will be resolved one day 

## Comment 2356028553

maintainer (COLLABORATOR) · goeiecool9999 · 2024-09-17T14:30:28Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2356028553

I've experimented with ``VK_EXT_attachment_feedback_loop_layout`` in order to try and fix a different issue on Vega GPU's. Using the extension didn't show any difference in behaviour on that card, but I'm curious if it could fix these issues. If you want to help test it there's a build available here: https://github.com/goeiecool9999/Cemu/actions/runs/10904371233
The implementation is pretty messy at the moment so if it improves rendering there will be more work required to get it in a merge-able state. But at least it could give us an idea about whether or not it would work.

## Comment 2357418781

reporter (NONE) · Not4ce · 2024-09-18T03:26:46Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2357418781

> I've experimented with `VK_EXT_attachment_feedback_loop_layout` in order to try and fix a different issue on Vega GPU's. Using the extension didn't show any difference in behaviour on that card, but I'm curious if it could fix these issues. If you want to help test it there's a build available here: https://github.com/goeiecool9999/Cemu/actions/runs/10904371233 The implementation is pretty messy at the moment so if it improves rendering there will be more work required to get it in a merge-able state. But at least it could give us an idea about whether or not it would work.

Hi just tested, and I want to report back, that fork completely solves the issue!

First boot was weird, with app losing 60% of its frametime, but subsequent boots have been flawless. Here are some screenshots:
<img width="959" alt="Botw sample 1" src="https://github.com/user-attachments/assets/6157884c-89ea-41a3-9a59-dd3413701890">
<img width="959" alt="Botw Sample 2" src="https://github.com/user-attachments/assets/757b550a-54ea-4d3a-924f-eba1fed41710">

By default, it has "Accurate barriers (vulkan)" enabled under Debug. Keeping that off seem to cause no issue, with enabled costing 2-3 miliseconds in frametime vs off (in action)

<img width="959" alt="Botw Accurate binaries on" src="https://github.com/user-attachments/assets/436a7e27-7077-494c-9ea9-ec41574c8423">
<img width="959" alt="Botw Accurate binaries off" src="https://github.com/user-attachments/assets/96d6a5d6-124a-45cb-b090-e1df3b42f739">

Overall, I plan on using this build for a longer session after this. Texture corruption from pebbles and all the aliasing seem to be resolved for now. Thank you the heads up, I will be passing this onto some personal acquintances that have been waiting for a cemu resolution, and so far so good

I tried finding a log file, there was none. But if you require any further info/logs, please let me know😊. @dstrnad might also find this useful, if they have a similar use case 

## Comment 2357695736

other (NONE) · dstrnad · 2024-09-18T07:20:50Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2357695736

I can also confirm that this fork seems to completely fix the issue. No black/ colourful glitches anymore. I tested on Rog Ally. Accurate barriers settings on/off makes no difference now, the issue is gone. Good job @goeiecool9999 and thanks for the heads up @Not4ce. I will finally try to play the game now, if I can test anything else just let me know. It would be awesome if this could get merged at some point.

## Comment 2358982362

other (NONE) · dstrnad · 2024-09-18T16:59:00Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2358982362

Bad news, the fork sometimes crashes when opening or exiting inventory and map menus. Weird is that I can open or close the map/ inventory couple of times (even like 10,20,30 times) and it is ok, but then it randomly freezes the whole game and cemu crashes. 
I deleted all shader caches to be sure, but still happens.

## Comment 2365050464

maintainer (COLLABORATOR) · goeiecool9999 · 2024-09-21T07:56:06Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2365050464

@dstrnad What version are your drivers? There have been lots of reports of instability with 24.8.1 (#1323), although mostly with different symptoms than you're describing. If you are on 24.8.1 and downgrading to 24.7.1 fixes the instability we know it's probably not anything I changed.

## Comment 2368875576

other (NONE) · dstrnad · 2024-09-23T17:07:08Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2368875576

@goeiecool9999 I’m on 24.3.1. I plan to test it under linux, so we can rule out any windows driver related issues.

## Comment 2372048665

other (NONE) · TheOneEyedGrimReaper · 2024-09-24T18:49:40Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2372048665

> I've experimented with `VK_EXT_attachment_feedback_loop_layout` in order to try and fix a different issue on Vega GPU's. Using the extension didn't show any difference in behaviour on that card, but I'm curious if it could fix these issues. If you want to help test it there's a build available here: https://github.com/goeiecool9999/Cemu/actions/runs/10904371233 The implementation is pretty messy at the moment so if it improves rendering there will be more work required to get it in a merge-able state. But at least it could give us an idea about whether or not it would work.

where can i download this build?
or i need to build it myself?

## Comment 2372062300

maintainer (COLLABORATOR) · goeiecool9999 · 2024-09-24T18:53:23Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2372062300

> where can i download this build? or i need to build it myself?

@TheOneEyedGrimReaper 
The interface isn't the most intuitive. At the bottom of the page I linked there's a section called "artifacts". Pick your platform from the list and click the small download icon on the right (edit: clicking the name works too). 

## Comment 2372066162

other (NONE) · TheOneEyedGrimReaper · 2024-09-24T18:55:25Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2372066162

> > where can i download this build? or i need to build it myself?
> 
> @TheOneEyedGrimReaper The interface isn't the most intuitive. At the bottom of the page I linked there's a section called "artifacts". Pick your platform from the list and click the small download icon on the right (edit: clicking the name works too).

lel.
so i was the blind.
thanks man.

## Comment 2372850922

reporter (NONE) · Not4ce · 2024-09-25T03:45:25Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2372850922

> @goeiecool9999 I’m on 24.3.1. I plan to test it under linux, so we can rule out any windows driver related issues.

This would be very much appreciated. Sorry for the late reply, @dstrnad is correct and testing on linux would help which i am unable to do 

Cemu crashes after 30 minutes of use with exception x0409, which to my understanding is a stack buffer overrun, so something gets corrupted around 20-30minutes. As far as i can tell, the driver may not be the issue. I have tried 6 driver versions so far, ranging from 24.3.1 to 24.8.1 (including 3 seperate devices, and the technical preview drivers from amd)

<img width="249" alt="Screenshot 2024-09-25 134629" src="https://github.com/user-attachments/assets/ced46d3c-8432-4665-8f00-58fe138f0938">

<img width="249" alt="Screenshot 2024-09-25 125310" src="https://github.com/user-attachments/assets/5030d1ef-0b51-42cb-ba76-ff9344550677">


I will also attach the actual crash log here, which i suspect may not help too much? But why not. If you need anything else, please let me know @goeiecool9999. So far, the crashes can happen at any time in shrine/overwold/zone, looks to be related to how long cemu was running  
<img width="443" alt="Screenshot 2024-09-25 124925" src="https://github.com/user-attachments/assets/7a7b6752-56dd-45c1-af74-de53cc2f3143">

[Cemu crash.zip](https://github.com/user-attachments/files/17124225/Cemu.crash.zip)


## Comment 2374286216

maintainer (COLLABORATOR) · goeiecool9999 · 2024-09-25T14:38:51Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2374286216

@Not4ce I'm not very familiar with the windows event viewer and I don't know if it contains useful information. If you could send cemu's log.txt after a crash instead that's more likely to contain a helpful clue. I'm mainly interested in seeing the stack trace at the end of the file.

## Comment 2380389254

other (NONE) · TheOneEyedGrimReaper · 2024-09-28T03:42:53Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2380389254

@goeiecool9999 
Hi again!
Can you check your cemu fork?

It tries to eat more than my actualy allocated vram and then freezes up my rog ally completely.

## Comment 2397033940

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-07T14:05:51Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2397033940

> it tries to eat more than my actualy allocated vram and then freezes up my rog ally completely

I didn't change anything related to GPU memory allocation. Are you sure you're running out of VRAM and not regular memory?

## Comment 2397875150

other (NONE) · Valkyr2 · 2024-10-07T20:53:55Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2397875150

Hi, tested your build, works like a charm for me. I'll test it further this week. thanks for sharing this

## Comment 2398176121

other (NONE) · TheOneEyedGrimReaper · 2024-10-07T23:40:42Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2398176121

> > it tries to eat more than my actualy allocated vram and then freezes up my rog ally completely
> 
> I didn't change anything related to GPU memory allocation. Are you sure you're running out of VRAM and not regular memory?

yep i'm sure of it.
somehow it sees my 6gb allocated vram for 10gb and when it's going over 6gb it freezes my rog ally.
the official cemu build that has the ground texture bug doesn't even try to eat more than 3gb of vram and i can play for hours without any other problem than the ground tex bug.

## Comment 2432752698

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-23T16:11:40Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2432752698

I found a memory leak and fixing it appears to make GPU memory usage stable. Let me know if this improves stability.
New build here: https://github.com/goeiecool9999/Cemu/actions/runs/11482812478

## Comment 2433517875

other (NONE) · dstrnad · 2024-10-23T21:41:21Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2433517875

I think you fixed it. I’ve been testing for an hour on linux (bazzite, Rog ally) and memory seems stable, no crashes so far and no glitches. I will test more, but good job 👍 

## Comment 2434236223

other (NONE) · aASDa213ASD · 2024-10-24T04:10:48Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2434236223

@goeiecool9999 Hey, wanted to pay my little thanks here, quite impressed with the work you've done!
Apart from a massive perfomance hit it solves the issue with artifacts on **RDNA3** gpu (**RX 7800 XT** in my case) completely. I'd like to ask you and not just you but perhaps everybody a question regarding Vulkan vs OpenGl war. I can clearly see that by default I get 20 frames per second less on your fork, don't really care about barriers as long as artifacts are not there. However I seem to be running Opengl just fine as well on 160 frames (even higher than on vulkan for some reason), so may anybody explain to me why we prefer vulkan over opengl at this point?
Or I just happened to be the lucky guy getting more frames on opengl than on vulkan with my gpu?
What's.. the catch here?

All the tests were made on 2560x1440p with FPS++ on 165.0 lock.
Worth noting that OS is Arch Linux, tested both amdvlk / radeon-vulkan drivers (no difference at all).

Here's my frametime on **Vulkan** with **accurate barriers disabled**:
![image](https://github.com/user-attachments/assets/dc2a2b68-ae69-4bdc-abee-062f67bbc1da)
And all the same **but** **accurate barriers enabled** this time (may feel like the issue is entirely gone as well, but trust me it's still there, just less noticeable):
![image](https://github.com/user-attachments/assets/816c5e29-ca36-4e51-89ca-eb6deef2be58)
Now your cemu fork with **feedback_loop_layout** with **accurate barriers disabled**:
![image](https://github.com/user-attachments/assets/cad92eb3-e6c2-413e-8c2f-c32883526596)
And the same but with **accurate barriers enabled**:
![image](https://github.com/user-attachments/assets/ee5c81ab-e759-4e9d-b057-eb2b54158349)
OpenGl (please explain to me why it happens to be more performant):
![image](https://github.com/user-attachments/assets/e390d9d5-daa4-4469-a1a3-d244d899b96e)


## Comment 2434324516

other (NONE) · Squall-Leonhart · 2024-10-24T05:20:34Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2434324516

Because prior to RDNA2 the legacy ATI Opengl ICD still in use was not optimized for multicore and was 50-75% slower than it is now
, it is still not as capable as vulkan for emulating all aspects of the Latte gpu with just AMD's extension set, as AMD implements them as specc'd while nvidia lets the developer get away with using them in ways less defined.

With AMD's design ~~mistake~~ decision in RDNA3, the only resolution means the renderer falls back to cpu limited synchronisation operations more often.

The hit is likely to be worse on nvidia since layout transitions there are known to cause 15% hits.

## Comment 2434905884

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-24T10:32:51Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2434905884

> However I seem to be running Opengl just fine as well on 160 frames (even higher than on vulkan for some reason), so may anybody explain to me why we prefer vulkan over opengl at this point?

>Worth noting that OS is Arch Linux

Historically AMD's official OpenGL drivers on windows performed very poorly. On Linux however mesa is actually one of the best drivers out there and was one of the recommended solutions for AMD's bad performance. Though installing a different operating system is not convenient for most end-users as you might imagine so Cemu needed a different solution. Vulkan.

The tradeoff between OpenGL and Vulkan is essentially this: OpenGL is easier to develop applications with because the API is a lot less complex. This simplicity also means the driver does a lot of things behind the scenes without telling the developer. You just have to cross your fingers that the implementation is efficient. This leads to unpredictable performance and makes performance problems harder to debug. Vulkan is intended to take away a lot of that guesswork and make everything explicit. That's why Vulkan is notoriously verbose to get anything done. Even displaying a single triangle. The developer has to decide a lot more things. How to synchronize, when to send work to the GPU, etc.
So why does OpenGL perform better in some cases? Because it receives a minimum amount of information required to define what needs to be rendered on the GPU and is free to optimize it however it likes. If a driver does this well performance is good (mesa). If it doesn't performance is bad (AMD's windows driver). With Vulkan you get a bunch of predictable operations that you have to make efficient use of. The only optimization the driver can do is make those individual operations as efficient as possible. When Cemu's Vulkan backend was written it provided significantly better performance than AMD's OpenGL driver (and probably still does, idk it's been a while since I compared) meaning AMD users don't need to switch to a different OS anymore. Cemu's Vulkan backend also supports asynchronous shader compilation meaning it can prevent stutter that normally happens when compiling uncached shaders by temporarily skipping the associated draw calls until they're done compiling. This is apparently not impossible to implement on OpenGL, but I've heard it's a lot easier with Vulkan.
You can use whichever backend you prefer. Although in recent years the Vulkan backend has received more attention than OpenGL.

Another benefit of Vulkan which doesn't matter at all for cemu is the ability to prepare work for the GPU on multiple threads. That means that in theory a well designed game engine for example can use high core count systems more effectively. OpenGL is single-threaded by design.

## Comment 2435470961

other (NONE) · aASDa213ASD · 2024-10-24T14:34:06Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2435470961

That answers pretty much explains all in and outs regarding the question. I know that Vulkan is successor to OpenGL and it SHOULD (in theory) perform much better than OpenGL and was quite surprised to see the other picture, much obliged for the explanation why that even happens to me.

By walking left-n-right on the map a little hitting a bunch of monsters I can tell that OpenGL struggles to render a lot of stuff at a time since my framerate drops to 90 from 165 on any explosion (even with pre-downloaded shaderCache) which lowkey corresponds to single-threaded nature of it.

In any case you did a great job and I couldn't be happier, awaiting your work to be implemented in the main branch.

## Comment 2436548612

reporter (NONE) · Not4ce · 2024-10-25T00:09:12Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2436548612

> I found a memory leak and fixing it appears to make GPU memory usage stable. Let me know if this improves stability. New build here: https://github.com/goeiecool9999/Cemu/actions/runs/11482812478

Can confirm works. It fixed the game crashing circa 30 minutes in, which indeed seemed to be the a memory leak as @TheOneEyedGrimReaper was thinking. One hindsight, a clear sigh was degraded game frame rate over longer duration of play in the same zone 

Thank you for the hard work! Much appreciated. Game was fine on a 1 hour game session of second wind on my Ally

Performance is unchanged, just more stable now with no slowdown half an hour in. I tested across Rdna 2 and 3 cards and 4 devices and 3 driver version. Really hope these fixes are merged into the primarily stable build to benefit more users that are unaware of this 

## Comment 2438610314

other (NONE) · aASDa213ASD · 2024-10-25T19:05:19Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2438610314

Had the game running for about 10 hours in total, can confirm that there's no crashes no matter what I'm busy doing here. Except one single exception (not sure if it doesn't appear in the normal cemu as well): if you remove framerate limit and bring up some menu (like bomb selection) your fps will jump to insane numbers effectively overloading something to the point that renderer stops responding and the game will be frozen until restart. Doesn't seem to happen if any framerate limit supplied by either FPS++ or any external stuff like Mangohud / RTSS / Etc. Again thanks @goeiecool9999 for the dedication and doing my job for me, as stated waiting @Exzap here to take a look and merge it, 20 frames drop was totally worth it, I hate OpenGL.

Regarding OpenGL it even produces some interesting visual glitches that Vulkan doesn't:
![image](https://github.com/user-attachments/assets/2f75033f-40c7-4c3f-b51a-6b0dcc4ef00b)

Same location on Vulkan (no settings changed):
![image](https://github.com/user-attachments/assets/4315fb36-7c69-43e9-9543-ea4bc342b0c8)


## Comment 2448665245

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-30T23:29:34Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2448665245

I've made some more changes. This build might improve performance (but temper your expectations). I'm interested to hear if it does.
https://github.com/goeiecool9999/Cemu/actions/runs/11602523437

## Comment 2448979290

reporter (NONE) · Not4ce · 2024-10-31T04:14:45Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2448979290

> I've made some more changes. This build might improve performance (but temper your expectations). I'm interested to hear if it does. https://github.com/goeiecool9999/Cemu/actions/runs/11602523437

Well, the results are very interesting to say the least

Device: Z1E and Desktop with 12600K + 6800xt
Drivers: 24.9.1 and 24.10.1
Windows: 23H2 
Data: HML logs with afterburner + general gameplay

As far as testing methodology goes, I used a set-path that includes BOTW's internal zone change + heavy load, moving between Gerudo to central Hyrule over the course of 5 minutes. The same settings. tdp, gpu clocks, resolution and time of day was used to minimise variables, with Fps++ to uncap to max refresh rate. For the numbers below, I waited for shaders to compile on the set path and did 3 runs afterwards taking their average

Cemu 2.2 stable + unchecked updates:
- Faster by 1.5 - 2 milisecond consistently
- Looks like the fix was ported to the main branch
- Constant tendency to stutter when compiling shaders. Repeatable 400 milisecond pauses on every new zone, or camera movement on old cached-zone that trigger a new effect  

<img width="959" alt="2 2" src="https://github.com/user-attachments/assets/99752a3d-d704-4750-afed-1b420bb073a4">
<img width="129" alt="Cemu 2 2" src="https://github.com/user-attachments/assets/07a20cd6-1da8-4613-85c8-b98dd840805f">

Heres the stutter:
<img width="128" alt="2 2 stutter" src="https://github.com/user-attachments/assets/b17cc694-e279-4e6d-9db9-de44d09c3cf3">

The stutter is from my 2nd run. The initial run had 3 or so 450ms pauses. This is expected since the cpu budget is exceeded, but the new experimental build seems to avoid or minimise this somehow 

Cemu 5640d58 (new build)
- Consistently slower by 1.5-2ms on fresh/compiled shader runs
- Cpu usage slightly slower. It seems to go easier on some cpu cores compared to 2.2 (cpu core 14 and 7 were clocking lower on 5640d58)
- Avoids 300-500ms shader compilation stutter completely. Possibly the first time i have seen this on cemu. Cold runs on new drivers are stable with minimal stutter. 
<img width="959" alt="Cemu 5640d58" src="https://github.com/user-attachments/assets/0b8d8e8b-be31-4cea-860d-e15d26b86bc1">

<img width="119" alt="Cemu 5640d58" src="https://github.com/user-attachments/assets/15e69548-4fb2-4265-97d9-ae20587a5433">

Frametimes:
<img width="128" alt="Cemu 5640d58 frametimes" src="https://github.com/user-attachments/assets/a130e796-2968-4930-8a0c-7bb2635c3784">

Screenshots and data were from Ally Z1E at 25w of tdp. 5640d58  is 3-5% slower when cpu bound but offers better frametimes compared to 2.2 stable. The frame-time delta itself is very good on 5640d58, only deviating by 15% at worst case. With VRR, it eliminates any perceptible judder or compilation hitches as long as the baseline frametime is below 20ms. I was hard pressed to find any +5ms variation at all, which visually presents as "slow down/hitching" 

Curious whats different in this build, and if this benefit extends to Nvidia gpus. As is, having slightly higher framtimes, but stuttering is a worse experience. I would always go for a build that is smooth in motion, such as: 5640d58. Both builds are pretty good, but 2.2 reminds of a fixed 1.2.6 build. I will be sticking with 5640d58 on my desktop and Ally 


## Comment 2449401092

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-31T09:23:18Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449401092

I don't understand your results. 
> - Looks like the fix was ported to the main branch

I'm not aware of any change between 2.0-78 and 2.2 that can explain it being fixed, nor can I explain why my branch has less stutters. There's no reason for performance to be improved between my builds and 2.2. If anything it should be _worse_. I was mainly interested in a performance comparison between the latest build I [linked](https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2448665245) and [the one before](https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2432752698) as made some changes that I thought might reduce the performance impact.

## Comment 2449498874

other (NONE) · Squall-Leonhart · 2024-10-31T10:13:28Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449498874

> Looks like the fix was ported to the main branch

its visible in your screenshot that is not.

## Comment 2449512107

other (NONE) · dstrnad · 2024-10-31T10:20:55Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449512107

I don’t see any release or pull request for the main branch either,  but honestly, I can’t spot the issue in his particular screenshot. However, the issue is so noticeable in the game that I doubt @Not4ce wouldn’t have noticed it

## Comment 2449689843

reporter (NONE) · Not4ce · 2024-10-31T12:05:40Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449689843

> > Looks like the fix was ported to the main branch
> 
> its visible in your screenshot that is not.

Correct, it says 2.2 but i dont know how the newer naming nomenclature works post 1.2.6. If the build wasnt updated, then its AMDs driver update 24.10.1 from a week ago that fixed the issue. I have exlusively used the "modified" build from goeiecool till now.

> I don’t see any release or pull request for the main branch either, but honestly, I can’t spot the issue in his particular screenshot. However, the issue is so noticeable in the game that I doubt @Not4ce wouldn’t have noticed it
 
Yup, looks like 24.10.1 fixes it on Windows. I recall you using Linux, I wonder if there are any changes there on the Mesa drivers front 

> I don't understand your results.
> 
> > * Looks like the fix was ported to the main branch
> 
> I'm not aware of any change between 2.0-78 and 2.2 that can explain it being fixed, nor can I explain why my branch has less stutters. There's no reason for performance to be improved between my builds and 2.2. If anything it should be _worse_. I was mainly interested in a performance comparison between the latest build I [linked](https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2448665245) and [the one before](https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2432752698) as made some changes that I thought might reduce the performance impact.

Results are repeatable and I have attached the logs as 7zip files below. 2.2 related bug seems to be resolved due to the driver update this month from AMD. If others can test and chime in on Windows, that would help, esp re:stutter on 2.2 

Cemu 5640d58 seems to be 20%~ faster on some scenes compared to your old build 1211a31 with memory fix. Running upto Kakariko village 5640d58 can maintain 51fps vs 39fps on 1211a31. Generally, over a 8 minute like for like run, with my earlier described methodology, the overall uplift is closer to 15% on average. 

After playing hours of cemu to compare builds across 3 devices, it seems clear on my systems that 5640d58 simply stutters less. I will attach the afterburner .hml logs below

Stable 2.2 : 10 stutters over 8 minutes with 600ms pause (207ms on average)
![image](https://github.com/user-attachments/assets/a01e4208-f0d1-4c1f-81f5-c66e38a6c303)
 
Cemu 5640d58: 6 Stutters over 8 minutes averaging 160 ms 
![image](https://github.com/user-attachments/assets/2eb446af-2ac3-47a3-bc31-fa361d3ee740)

Stable stutters almost twice as often, with most hitches being north of 200ms and some terrible 600ms hitches. As far as average fps goes

2.2 - Avg: 59fps, 0.1%: 27fps
5640d58 - Avg: 51fps, 0.1%: 39fps
1211a31  - Avg:40fps, 0.1%: 27fps


At this point, im very curious as to why stable 2.2 reliably stutters more. I do not plan on updating to 24h2, till Microsoft addresses Alderlake performance degradation, so I cant say if this is 23h2 specific.

I am curious if other windows users notice this discrepency between the builds but whatever the case, the experimental build seem to be very smooth on my end/amd hardware compared to stable. The logs are below this, which ran through a set-path, fixed time of day, and so on

[Cemu Test 2.zip](https://github.com/user-attachments/files/17587390/Cemu.Test.2.zip)


## Comment 2449701040

other (NONE) · Valkyr2 · 2024-10-31T12:12:10Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449701040

Hello, thanks for the build
I did some testing, here is what I got.
- old build : 62 fps with accurate barriers, 73 without
- new build : 87 with, 101 without
- 2.2 : 102 with, 130 without

and i can confirm that somehow the black squares texture corruption on RDNA3 does no longer occur at all on the 2.2 version
recently updated graphics driver to 24.10.1, perhaps it has something to do with it

## Comment 2449819858

other (NONE) · Squall-Leonhart · 2024-10-31T13:16:08Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449819858

nothing is fixed in 24.10, if anything its just as broken as 24.9

## Comment 2449924731

reporter (NONE) · Not4ce · 2024-10-31T14:03:52Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2449924731

> nothing is fixed in 24.10, if anything its just as broken as 24.9

Can you provide an example. Due to the 10mb upload limit here, heres a catbox link of 2.2 running fine on 24.10.1 on my end. There are no texture corruption on other zones either, seems to be resolved on my end with the latest drivers

https://files.catbox.moe/6apabw.mp4

## Comment 2450171510

other (NONE) · aASDa213ASD · 2024-10-31T15:28:19Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2450171510

@Not4ce 

# Cemu
Latest Cemu 2.2 downloaded from [here](https://github.com/cemu-project/Cemu/releases/tag/v2.2), texture artifacts are there no matter what.

# PC Specs
OS: Arch Linux x86_64
Kernel: Linux 6.11.5-zen1-1-zen
MOTHER: MAG B550 TOMAHAWK (MS-7C91) (2.0)
​CPU: AMD Ryzen 7 5800X3D (16) @ 4.55 GHz
GPU: AMD Radeon RX 7800 XT (amdgpu)
Memory: 9.88 GiB / 31.27 GiB (32%)

# No accurate barriers
![image](https://github.com/user-attachments/assets/9dd73adc-710b-4d75-940c-724b7f109beb)

# Accurate barriers
![image](https://github.com/user-attachments/assets/75695715-675d-4786-8dd4-54a11ea69b7b)

# Fun fact
I tried to screenshot my artifacts and even got a FRAME where I can see NO ARTIFACTS means they are not there every single frame, but rather appearing and vanishing constantly. Current fps is locked to 120.


## Comment 2450215117

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-31T15:46:55Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2450215117

> At this point, im very curious as to why stable 2.2 reliably stutters more

I haven't been entirely scientific. I merged some changes from main that happened after the release of 2.2. So it could be one of those as well. Anyways, if the new driver really does make the problem go away that's preferable because like I said before, I'm not very happy with the implementation of my fix using the extension. I would probably want to rewrite it to get it in a merge-able state.

## Comment 2450257353

other (NONE) · aASDa213ASD · 2024-10-31T16:05:18Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2450257353

@goeiecool9999 Regarding difference between [your previous build](https://github.com/goeiecool9999/Cemu/actions/runs/11482812478) and [a new one](https://github.com/goeiecool9999/Cemu/actions/runs/11602523437)

# [dcdfa82](https://github.com/goeiecool9999/Cemu/actions/runs/11482812478)
![image](https://github.com/user-attachments/assets/ad02addb-61c0-4f1b-8ae9-bdba2988bfa6)

# [5640d58](https://github.com/goeiecool9999/Cemu/actions/runs/11602523437)
![image](https://github.com/user-attachments/assets/f9d7a884-aceb-43ec-a828-a1d399ce0d65)

# Summary
On average I'm getting around 5 frames more than I did on previous build, sometimes  dcdfa82 jumps to 160 as well but it doesn't happen to keep that number and drop to 145-150-155 while 5640d58 is able to jump even higher to 163 and keep itself around 155 stable without random drops to 145 for 0 reason.
Good job I guess?

## Comment 2450285524

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-31T16:16:47Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2450285524

The performance penalty for the image memory barriers seems to be far less with mesa compared to windows. I would say that tiny of a difference is probably not statistically significant. The difference that Valkyr2 reported is more in line with my expectations.

## Comment 2450409308

other (NONE) · aASDa213ASD · 2024-10-31T17:14:42Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2450409308

Anyway I assume that I'm cpu-necked so it's not like my renderer is overloaded with anything, GPU is under 50% load while couple of my cpu cores go up to 100%. Maybe that's why I can't see much of a difference.
If that would really help I could test windows as well in some future.

## Comment 2451013749

maintainer (COLLABORATOR) · goeiecool9999 · 2024-10-31T23:27:14Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2451013749

The term bottleneck really only applies when you're dealing with parallel processes where one process depends on the output of another (or a chain of processes). The CPU and GPU are effectively parallel processes. While the GPU is processing one frame the CPU can work on the next frame simultaneously. This means that a frame can take up to 1/fps seconds to process on the CPU AND 1/fps seconds to process on the GPU before you see stutters. Like with all pipelines there's a latency increase but the performance improvement of having both processors do work simultaneously is worth it in the vast majority of cases. If the GPU is the bottleneck (assuming no FPS cap) it would be active 100% of the time and the CPU would be idle some percent of the time waiting for the work queue to have space for the frame it just processed. If the CPU is the bottleneck the CPU is active 100% of the time and the GPU idles some of the time waiting for the work queue to be non-empty.
You're gonna think: "Well then obviously I'm CPU bottlenecked in Cemu". But it's not that straightforward because Cemu's main CPU thread busy-waits (I believe to avoid unpredictable scheduler latency or unnecessary core migrations). So you won't see the true idle time in monitoring tools.
The main takeaway is this: For ideal performance and for the term "bottleneck" to be meaningful the CPU and GPU should only wait for each other when the GPU work queue is either empty or full.

I'm going off of what others tell me but Breath of the Wild's engine on Wii U is designed in such a way where the CPU waits for the GPU to be completely idle somewhere during the frame. That means that the GPU will _always_ be idle for some time during the frame until the CPU submits more work, no matter how fast or slow the CPU or GPU are. So even if the GPU was a potato you would not see 100% utilisation. You can improve the time between the CPU resuming when GPU is idle and the CPU submitting more work by getting a faster CPU, but you can also decrease the amount of time the CPU has to wait for the GPU to become idle by getting a faster GPU. Without **measuring** which of these delays is longer it's difficult to tell which component would give the biggest performance improvement (and even when you do it might not be obvious).

To tie it back to my point about the term "bottleneck": Normally if one component is a bottleneck upgrading the other wouldn't make a difference. In this scenario upgrading _either_ can have a positive impact. So neither can be said to be a true bottleneck.
I don't know why I decided to type this out since you didn't ask, but maybe you find it interesting (or someone else).

(PS: I think GPU utilisation actually becomes a proxy for those delays I mentioned earlier. As the GPU approaches infinite speed GPU utilisation approaches zero. As the CPU approaches infinite speed GPU utilisation approaches 100%. So if GPU usage is 50% the CPU and GPU are evenly matched, when it's at 75% that means it's slower and may be worth upgrading. if GPU usage is 25% you might consider upgrading the CPU. I'm not sure. That part might be blatant misinformation :sweat_smile:)

## Comment 2453119839

other (NONE) · aASDa213ASD · 2024-11-02T20:33:12Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2453119839

@goeiecool9999 @Not4ce @Squall-Leonhart @Valkyr2  I'm back with some.. Let's just say I'm not sure if this is good or a bad thing that I'm about to report.
First of all thanks @goeiecool9999 for writing this all down for me, would never know Cemu works this way.

I'm now writing from my Windows 11 Pro 24H2 (OS Build 26100.2033) instance on the same exact PC, specs of which you can see above in [this message](https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2450171510).
My graphics driver is shown on AMD Adrenaline Software as follows (24.10.1 10/11/2024):
![image](https://github.com/user-attachments/assets/df11c860-4974-4dbe-b240-0236978708f8)

This exact driver has nothing to offer regarding Vulkan emulation issues on it's release notes which you can find [here](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-10-1.html).

As well I downloaded Cemu 2.2 from latest releases again from [here](https://github.com/cemu-project/Cemu/releases/tag/v2.2) which also doesn't have any fixes regarding Vulkan emulation.

**You already feel where I'm leading, right?**

Not a single artefact problem on Cemu 2.2 on Windows 11 24H2 with 24.10.1 AMD GPU driver:
![Untitled](https://github.com/user-attachments/assets/8d562407-abd2-4db8-9702-6604c360d8b3)

On Linux, on the other hand Mesa and Vulkan-Radeon packages got updated recently so I checked that out as well - no changes I'm still artefacting.
![image](https://github.com/user-attachments/assets/a508701a-5169-42dc-aac5-a028ae86df96)

Both Cemu are set up identically on both machines with the same resolution, graphics packs, etc.
I've `Above 4GB decoding` and `Resizable bar`  features enabled on my bios if that matters.
Worth noting that I've played for almost an hour running around searching for anything related or similar to what I've used to see on Cemu 2.2 - nothing. Not a single artefact was found. Not a single visual glitch.
The only difference that really concerns me is that my Cemu title says `[Vulkan] [Generic]` on Linux while it shows `[Vulkan] [AMD GPU]` on Windows.

Here's my latest installed packages on Linux:
```bash
[aasda@arch ~]$ sudo pacman -Q | grep mesa
lib32-mesa 1:24.2.6-1
libva-mesa-driver 1:24.2.6-1
mesa 1:24.2.6-1
mesa-utils 9.0.0-5

[aasda@arch ~]$ sudo pacman -Q | grep vulkan
lib32-vulkan-icd-loader 1.3.295-1
lib32-vulkan-radeon 1:24.2.6-1
vulkan-headers 1:1.3.295-1
vulkan-icd-loader 1.3.295-1
vulkan-radeon 1:24.2.6-1
```

Least to say - I'm confused. I have tons of questions, perhaps everyone here as well.
If anyone has a single assumption or even a clue about why that works/doesn't work and what exactly affects it - please let me know because it drives me nuts when I don't understand something. If there's anything more I can provide/test/experiment with - let me know as well, will def do. Want this problem to be gone for good and we are getting close.

## Comment 2453387834

other (NONE) · Squall-Leonhart · 2024-11-03T11:12:11Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2453387834

it's worth noting (and something i've seen in Switch emulation too) that once a pipeline is cached in a good state, artifacts that occured on a bad build may not occur with that bad build after a good build has updated the cache.

## Comment 2453803806

other (NONE) · aASDa213ASD · 2024-11-04T04:23:57Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2453803806

Well I removed all of my shaderCache folder and nothing really changed on Linux.
Windows is totally alright though. I hate it.


## Comment 2469661390

other (NONE) · aASDa213ASD · 2024-11-12T05:46:34Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469661390

@goeiecool9999 The water in Gerudo town is still cracked on 5640d58
![image](https://github.com/user-attachments/assets/de82b646-f6dc-4d3c-b36d-225fa427246f)


## Comment 2469663315

other (NONE) · Squall-Leonhart · 2024-11-12T05:48:29Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469663315

that requires accurate barriers turned on.

## Comment 2469665035

other (NONE) · aASDa213ASD · 2024-11-12T05:50:12Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469665035

@Squall-Leonhart Uh, yeah, that seems like a solution.
Btw, do you ever notice an interesting RED DOT in the distant fog that appears for a brief millisecond? Perhaps.. it can also be fixed with accurate barriers.

![image](https://github.com/user-attachments/assets/91ee10cc-ee27-4936-8cba-2933c53bfcf0)


## Comment 2469669046

other (NONE) · Squall-Leonhart · 2024-11-12T05:54:13Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469669046

the red dots back O_O

## Comment 2469670086

other (NONE) · aASDa213ASD · 2024-11-12T05:55:15Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469670086

@Squall-Leonhart easier to show than explain: https://www.twitch.tv/player_killer_paradigma/clip/WonderfulFitKathyNinjaGrumpy-4z-7KcYDoG9nqUpA

Here's its lowkey BLACK, but if I would get somewhat blue sky it would be red.

![image](https://github.com/user-attachments/assets/b7522bba-25c3-47ea-866d-fc5176b4e85f)



## Comment 2469674053

other (NONE) · Squall-Leonhart · 2024-11-12T05:59:01Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469674053

~~that looks like specular aliasing to me~~

i didn't see that in the clip... wtf.

## Comment 2469679924

other (NONE) · aASDa213ASD · 2024-11-12T06:04:04Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2469679924

> i didn't see that in the clip... wtf.

It's hard to catch if you have low refresh rate monitor like 60 for example, because I stream at 90 frames per second, but if you are at least 90hz you can easily catch this one single frame with black dot (easier to see on 0.25x speed but even there it's hard to get this exact frame)

It's not AS annoying as artifacts so I can even ignore it however that is.. here and I never saw anyone mentioning this.

And I mean it appears quite rarely and only in the distance, so if you don't happen to look far and have some wall infront of you - it's a non issue.

But if you look far that happens often, here's number 2:
![image](https://github.com/user-attachments/assets/cd6b0769-a7b9-4acc-bec2-ec091fe15739)


## Comment 2506234043

other (NONE) · cooljimy84 · 2024-11-28T14:20:03Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2506234043

> I've made some more changes. This build might improve performance (but temper your expectations). I'm interested to hear if it does. https://github.com/goeiecool9999/Cemu/actions/runs/11602523437

So this version (appimage) fixes my issue with MK8 stuttering, it goes from a solid 60fps to sutter to 55fps then back up to 60fps.
AMD Ryzen 9 7940HS w/ Radeon 780M Graphics
linux 6.8.0-48-generic #48-Ubuntu SMP PREEMPT_DYNAMIC Fri Sep 27 14:04:52 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux
libva info: VA-API version 1.20.0
libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/radeonsi_drv_video.so
libva info: Found init function __vaDriverInit_1_20
libva info: va_openDriver() returns 0
vainfo: VA-API version: 1.20 (libva 2.12.0)
vainfo: Driver version: Mesa Gallium driver 24.0.9-0ubuntu0.2 for AMD Radeon Graphics (radeonsi, gfx1103_r1, LLVM 17.0.6, DRM 3.57, 6.8.0-48-generic)

Not sure if this helps, but all the textures were fine in MK8, just this very noticable stutter.


## Comment 2523101984

other (NONE) · Squall-Leonhart · 2024-12-06T12:21:41Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2523101984

24.12.1 has resolved the crashing issues, and seem to be generally better vulkan drivers then amd has released since about 24.3.1 (I mean, starcitizen is fixed too so yeah) so testing should be performed on those from now on.

## Comment 2537899329

other (NONE) · zorn-v · 2024-12-12T06:09:02Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2537899329

> I've made some more changes. This build might improve performance (but temper your expectations). I'm interested to hear if it does. https://github.com/goeiecool9999/Cemu/actions/runs/11602523437

This build also fixes visual glitches on AMD GPU in Paper Mario: Color Splash
It looks like this in 2.5
![изображение](https://github.com/user-attachments/assets/bf6c449b-d9e1-48e9-b708-d6f39b0c39e9)


## Comment 2538282337

other (NONE) · geowarin · 2024-12-12T09:09:43Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2538282337

> I've made some more changes. This build might improve performance (but temper your expectations). I'm interested to hear if it does. https://github.com/goeiecool9999/Cemu/actions/runs/11602523437

@goeiecool9999 This build fixes both the texture corruption and the frame pacing issues I have in BOTW. 
Thank you!
I'm on Linux with a 7800XT


## Comment 2609741118

other (NONE) · dstrnad · 2025-01-23T12:55:49Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2609741118

> They implemented the `VK_EXT_attachment_feedback_loop_layout` extension which fixed it. This extension has been on our radar for a while since it would probably also help us improve performance. Unfortunately it's not trivial to implement the extension and since I am bogged down by other work right now I can't work on it anytime soon. But if anyone else wants to take a shot that would be appreciated
> 
> For context ryujinx' PR: https://github.com/Ryujinx/Ryujinx/pull/7226

Is there any update on the merge of this issue please? Been testing the last version from @goeiecool9999  for several months now, works great, fixes the issue, but would be nice to be able to officially update Cemu again. Thx

## Comment 2613892960

other (NONE) · cooljimy84 · 2025-01-25T10:01:59Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2613892960

I switched from the flatpak to appimage and the issue went away. I'm sure I could have found a newer vulkan for mint os, but path of least resistance wins.

## Comment 2776398707

other (NONE) · davidef02 · 2025-04-03T16:49:24Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2776398707

I started having the texture corruption problem once I got a whqd monitor (with a 7700xt)... is there any update on the merge with main? Or could someone upload the @goeiecool9999 latest build, because the download's options are all expired. Thanks

## Comment 2776545906

other (NONE) · zorn-v · 2025-04-03T17:58:42Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2776545906

Also surprised why it is not merged to master.
Linux AppImage - https://dropmefiles.com/8evMd

## Comment 2776565485

other (NONE) · davidef02 · 2025-04-03T18:07:56Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2776565485

> Also surprised why it is not merged to master. Linux AppImage - https://dropmefiles.com/8evMd

Could you pass me the windows version? Thank you very much

## Comment 2818220487

other (NONE) · aASDa213ASD · 2025-04-21T11:25:20Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2818220487

> > Also surprised why it is not merged to master. Linux AppImage - https://dropmefiles.com/8evMd
> 
> Could you pass me the windows version? Thank you very much

@layard32 So far as I tested months ago, it's fixed on windows drivers for RDNA3 gpus, the issue remains on Linux with any driver vulkan implementation eg amdvlk / radeon-vulkan. So on Linux you play with the build mister @goeiecool9999 created (_thanks you SO MUCH_), on windows you can play official cemu and things should be fine. Just make sure you have the latest adrenaline driver installed.

You can read my post about my windows vs linux tests here: https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2453119839

## Comment 2821900583

other (NONE) · Squall-Leonhart · 2025-04-22T16:41:46Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2821900583

one reason this isn't merged as is, is it decimates performance on the nvidia driver.

> it's fixed on windows drivers for RDNA3 gpus,

Absolutely, is not.

## Comment 2823961438

other (NONE) · aASDa213ASD · 2025-04-23T11:22:44Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2823961438

@Squall-Leonhart uuh... how do you explain https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2453119839 then?

_no offence just trying to grasp your point_

## Comment 2824103149

other (NONE) · Ammar-Sadaoui · 2025-04-23T12:20:12Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2824103149

> one reason this isn't merged as is, is it decimates performance on the nvidia driver.
> 
> > it's fixed on windows drivers for RDNA3 gpus,
> 
> Absolutely, is not.

can be added as options to turn on and off ?

## Comment 2824147220

maintainer (MEMBER) · Exzap · 2025-04-23T12:37:13Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2824147220

I am not sure what the current state of @goeiecool9999's fork is exactly but from what I understand it's not optimal and it can hurt performance on some drivers and it may not even cover all the cases where there is an actual feedback loop. The latter is a problem outside the scope of the fork, there are design decisions in Cemu's Vulkan renderer code that make it hard to implement the feedback loop extension.

I believe the better way forward, which is in line with what modern Vulkan wants us to do, is to also adopt `VK_KHR_dynamic_rendering_local_read` (together with `VK_EXT_attachment_feedback_loop_layout`). But it requires us to switch from renderpasses to dynamic rendering as well as fundamentally resdesign said core parts of the renderer so that we can properly and efficiently track feedback loop dependencies. Adopting the new extensions will lock out users on old GPUs because they don't get driver updates anymore. So it's not really as straightforward of a decision. On the upside I think it could help improve performance for everyone else, at least in theory. But we'll see if that turns out to be true.

This will all happen eventually but there are too many unknowns to give any sort of ETA. In the meantime you can use the fork.

## Comment 2851144640

other (NONE) · HimanshuBansal112 · 2025-05-05T14:12:24Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-2851144640

I am also having issue in paper mario color splash with vulkan as zorn-v said in this issue. Please fix the issue. I am also using Radeon 780M. (Works fine with OpenGL)

![Image](https://github.com/user-attachments/assets/fc945573-8da8-42be-ab1a-9464bfb921fa)

## Comment 3155064135

other (NONE) · s7nr1s3 · 2025-08-05T12:44:07Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3155064135

Hi, I was wondering, is there a way to get expired builds downloaded. They are all currently expired (unavailable).

I am particularly looking for the Windows version. Currently playing Fast Racing Neo with a 7900XTX and there are many artifacts, especially after a few minutes play including in the game menus. In the game itself, artifacts are all over the screen, like a mask with green, blue and other color blocks on the top of the image (they are a bit less in the beginning and are gradually increasing over time). Accurate barriers (Vulkan) are enabled. OpenGL works with no artifacts whatsoever but slows the game down by about 1/3 and I also get lower FPS (20 to 30) - my GPU is also not listed in Edit Game Profile under OpenGL). This is with the latest stable Windows AMD driver from end of June 2025.

If I completely disable anti-aliasing (to 1) artifacts become less but do not disappear. Could someone please help me download an older build for Windows (currently all expired) or maybe suggest something else to get rid of/reduce the artifacts. In another Github thread someone suggested artifacts were a result of OOM (out-of-memory) problem - I don't think this is the problem for me - the 7900XTX has 24GB of VRAM and I have 32GB of RAM too. Many thanks in advance for any help.



## Comment 3367819401

other (NONE) · carsondiaz0 · 2025-10-04T03:15:56Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3367819401

Hello! The fork made by @goeiecool9999 is unavailable to access at the current time. I would love to be able to have a copy as I am experiencing visual glitches as a result of the AMD chip in my Legion Go S.

## Comment 3367955214

other (NONE) · dstrnad · 2025-10-04T06:24:50Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3367955214

Hi @carsondiaz0 , here you go, enjoy: https://drive.google.com/file/d/14k4kMqwQKQOrq9vuUsJVbMXq1UTSQmRi/view?usp=drivesdk


## Comment 3368392011

other (NONE) · carsondiaz0 · 2025-10-04T16:23:22Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3368392011

@dstrnad you are absolutely goated. I have spent hours of my life trying to resolve the issue. You have saved my sanity. Thanks dude

## Comment 3374619864

other (NONE) · s7nr1s3 · 2025-10-06T23:22:08Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3374619864

Hi @dstrnad, thanks a lot for sharing the archive. I've tried the same game (Fast Racing Neo) with the listed cemu version for Windows (Vulkan 7900XTX). The square pixel palette noise is still there, but I believe it is less compared to the latest (original) cemu. It always starts with almost no noise that keeps getting more with time. Xenia (Vulkan again) exhibits similar behavior with certain games where cache must be manually cleared once in a while, otherwise it starts displaying pixel vertices/completely breaks the graphics. I also disabled the Accurate Barriers (Vulkan) option and I think this also helped a little. Normally I play with Vsync on (Experimental) so changed this too to triple buffering instead but it became worse.

Just a question, all games with the cemu version from the archive appeared automatically, the same with settings made in the original cemu, once I started it. It is like Windows treats it like the same program. Shall I instead let's say rename the original cemu and start anew?

@carsondiaz0, did the archive make things any better for you on the Go S?

## Comment 3690633605

maintainer (COLLABORATOR) · goeiecool9999 · 2025-12-25T00:08:45Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3690633605

I have tried a different approach to fix the problem using the vulkan extension. If anyone would like to help test it out that would be greatly appreciated. Do you see any visual bugs? What is the performance like?
Thanks in advance.
https://github.com/goeiecool9999/Cemu/actions/runs/20495530909

Edit:
Please try this one instead: https://github.com/goeiecool9999/Cemu/actions/runs/20540106405

## Comment 3695587228

other (CONTRIBUTOR) · ImSapphire · 2025-12-29T06:32:53Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3695587228

@goeiecool9999 I tested 70a88773cf008c65eaef2d6171b9d59899f7c28a in The Legend of Zelda: Breath of the Wild, on an AMD Radeon RX 7700XT running under Linux (RADV, Mesa 25.3.2). Performance seems to be about the same, and I am not noticing any of the graphical artifacts when looking into certain spots of water in the Zora's Domain.

Didn't do too much gameplay testing, since for some reason my DualSense controller via SDL does not work in builds from CI (appears in device list and can add it, but joysticks, buttons, and triggers do not do anything). I haven't tried building from source yet since Arch Linux does not have WxWidgets 3.3.x.

## Comment 3697956519

other (CONTRIBUTOR) · ImSapphire · 2025-12-30T01:02:27Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3697956519

Was able to build from source so my controller works now. Got a GPU reset about an hour into playing BotW while inside the Hawa Koth Shrine.

<details>
<summary>System journal</summary>

```
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=128134896, emitted seq=128134898
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu:  Process cemu pid 1127553 thread LatteThread pid 1127779
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
Dec 29 18:57:33 elysium kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Dec 29 18:57:33 elysium org_kde_powerdevil[1517]: [1012471] Udev event detected
Dec 29 18:57:33 elysium lact[861]: 2025-12-30T00:57:33.671629Z  INFO lact_daemon: got kernel drm subsystem event, reloading GPUs
Dec 29 18:57:33 elysium lact[861]: 2025-12-30T00:57:33.729678Z  INFO lact_daemon::server::handler: initialized amdgpu controller for GPU 1002:747E-1043:0516-0000:03:00.0 at '/sys/class/drm/card1/device'
Dec 29 18:57:33 elysium lact[861]: 2025-12-30T00:57:33.730085Z  INFO lact_daemon::server::handler: initialized amdgpu controller for GPU 1002:1638-1043:187C-0000:0e:00.0 at '/sys/class/drm/card0/device'
Dec 29 18:57:33 elysium lact[861]: 2025-12-30T00:57:33.730110Z  INFO lact_daemon::server::handler: GPU list reloaded with 2 devices, reapplying configuration
Dec 29 18:57:33 elysium lact[861]: 2025-12-30T00:57:33.731017Z  INFO lact_daemon::server::handler: configuration applied
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Dumping IP State Completed
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: [drm] AMDGPU device coredump file has been created
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: [drm] Check your /sys/class/drm/card1/device/devcoredump/data
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: ring gfx_0.0.0 timeout, signaled seq=128134897, emitted seq=128134900
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu:  Process cemu pid 1127553 thread LatteThread pid 1127779
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Starting gfx_0.0.0 ring reset
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: amdgpu: Ring gfx_0.0.0 reset succeeded
Dec 29 18:57:43 elysium kernel: amdgpu 0000:03:00.0: [drm] device wedged, but recovered through reset
Dec 29 18:57:43 elysium org_kde_powerdevil[1517]: [1012471] Udev event detected
Dec 29 18:57:43 elysium kwin_wayland[1109]: Atomic modeset test failed! Permission denied
Dec 29 18:57:43 elysium kwin_wayland[1109]: Atomic modeset test failed! Permission denied
Dec 29 18:57:43 elysium kwin_wayland[1109]: atomic commit failed: Permission denied
Dec 29 18:57:43 elysium kwin_wayland[1109]: Atomic modeset test failed! Permission denied
Dec 29 18:57:43 elysium kwin_wayland[1109]: Atomic modeset test failed! Permission denied
Dec 29 18:57:43 elysium kwin_wayland[1109]: drmModeListLessees() failed: Permission denied
Dec 29 18:57:43 elysium lact[861]: 2025-12-30T00:57:43.906066Z  INFO lact_daemon: got kernel drm subsystem event, reloading GPUs
Dec 29 18:57:43 elysium lact[861]: 2025-12-30T00:57:43.913964Z  INFO lact_daemon::server::handler: initialized amdgpu controller for GPU 1002:747E-1043:0516-0000:03:00.0 at '/sys/class/drm/card1/device'
Dec 29 18:57:43 elysium lact[861]: 2025-12-30T00:57:43.914278Z  INFO lact_daemon::server::handler: initialized amdgpu controller for GPU 1002:1638-1043:187C-0000:0e:00.0 at '/sys/class/drm/card0/device'
Dec 29 18:57:43 elysium lact[861]: 2025-12-30T00:57:43.914291Z  INFO lact_daemon::server::handler: GPU list reloaded with 2 devices, reapplying configuration
Dec 29 18:57:43 elysium lact[861]: 2025-12-30T00:57:43.914414Z  INFO lact_daemon::server::handler: configuration applied
```

</details>

<details>
<summary>Cemu stdout/stderr</summary>

```
radv/amdgpu: The CS has been cancelled because the context is lost. This context is guilty of a hard recovery.
terminate called after throwing an instance of 'std::runtime_error'
  what():  failed to submit command buffer. Error -4
Aborted!
Error: signal 6:
/usr/lib/libc.so.6(+0x9890c) [0x7f90bce9890c]
/usr/lib/libc.so.6(+0x3e4d0) [0x7f90bce3e4d0]
/usr/lib/libc.so.6(+0x9890c) [0x7f90bce9890c]
/usr/lib/libc.so.6(gsignal+0x20) [0x7f90bce3e3a0]+0x20) [0x7f90bce3e3a0]
/usr/lib/libc.so.6(abort+0x26) [0x7f90bce2557a]+0x26) [0x7f90bce2557a]
/usr/lib/libstdc++.so.6(+0x97bf6) [0x7f90bd297bf6]
/usr/lib/libstdc++.so.6(+0xb1eba) [0x7f90bd2b1eba]
/usr/lib/libstdc++.so.6(_ZSt10unexpectedv+0) [0x7f90bd2975d9]+0) [0x7f90bd2975d9]
/usr/lib/libstdc++.so.6(+0xb2176) [0x7f90bd2b2176]
bin/Cemu_relwithdebinfo(VulkanRenderer::UnrecoverableError(char const*) const [clone .cold]+0x16) [0x564ed4c663d8]
bin/Cemu_relwithdebinfo(VulkanRenderer::SubmitCommandBuffer(VkSemaphore_T*, VkSemaphore_T*)+0x3f2) [0x564ed50a6282]
bin/Cemu_relwithdebinfo(VulkanRenderer::AcquireNextSwapchainImage(bool)+0x1e7) [0x564ed50a87f7]
bin/Cemu_relwithdebinfo(VulkanRenderer::DrawBackbufferQuad(LatteTextureView*, RendererOutputShader*, bool, int, int, int, int, bool, bool)+0x5e) [0x564ed50a959e]
bin/Cemu_relwithdebinfo(LatteRenderTarget_copyToBackbuffer(LatteTextureView*, bool)+0x1d1) [0x564ed5052041]
bin/Cemu_relwithdebinfo(LatteCP_ProcessRingbuffer()+0xbd4) [0x564ed504db84]
bin/Cemu_relwithdebinfo(Latte_ThreadEntry()+0x528) [0x564ed4dbb458]
/usr/lib/libstdc++.so.6(GraphicPack2::EnablePatches() [clone .cold]+0x46) [0x7f90bd2e55a4]
/usr/lib/libc.so.6(+0x9698b) [0x7f90bce9698b]
/usr/lib/libc.so.6(XMLConfig<CemuConfig>::Save(std::__cxx11::basic_string<wchar_t, std::char_traits<wchar_t>, std::allocator<wchar_t> > const&) [clone .cold]+0x2) [0x7f90bcf1a9cc]
```

</details>

Unfortunately I restarted Cemu after the crash without grabbing the log.txt, so I don't have that info.

## Comment 3698900384

maintainer (COLLABORATOR) · goeiecool9999 · 2025-12-30T10:05:22Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3698900384

That's odd to say the least. I wouldn't expect any of my changes to cause a GPU crash. I also don't see anything suspicious in the validation layers that might cause this. Can you double-check if it also happens on the branch point commit 13c6d497?

## Comment 3700177026

other (CONTRIBUTOR) · foresto · 2025-12-30T18:51:38Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3700177026

It might also be worth trying with different kernel versions. The amdgpu driver changes often, and sometimes gets things wrong.

https://gitlab.freedesktop.org/drm/amd/-/issues/

## Comment 3701919667

other (NONE) · aASDa213ASD · 2025-12-31T10:22:22Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3701919667

@goeiecool9999 thanks for your work, it's weird to me that YOU don't face the same issue but the only trying to solve it? I do remember your first ever message, that you've been trying to solve some other issue on Vega GPUs, but still.

sadly I don't have my arch installation in it's glory and won't be able to test out your new attempts to at least confirm it doesn't crash the kernel, but I might return back to my arch some time soon just to do it.

and if you don't mind socializing, it would be really great to have your discord, because I'd like to ask a question or two, let me know how you feel about it, regards :)

## Comment 3747094037

maintainer (COLLABORATOR) · goeiecool9999 · 2026-01-14T00:09:01Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3747094037

> Got a GPU reset about an hour into playing BotW while inside the Hawa Koth Shrine.

I ran into GPU resets on current versions of Cemu on my Vega/GCN GPU. I managed to fix that issue by using RADV_DEBUG=llvm. Perhaps it is the same problem that you ran into and it's not caused by my changes. Were you using any of the Sheikah slate runes?
I also made a few more changes. This is the CI build which also has the commit if you want to compile it yourself.
https://github.com/goeiecool9999/Cemu/actions/runs/20743506165
Hopefully in combination with the environment variable it's stable.
I know it'd be a bit tedious but if the combination of the environment variable plus my new changes fix the GPU reset it would also be nice to see if the crash still occurs without the environment variable. That way we know if it was my additional changes or the environment variable that resolved the crash.

## Comment 3802408627

other (CONTRIBUTOR) · ImSapphire · 2026-01-27T00:14:35Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-3802408627

it seemed fine running with `RADV_DEBUG=llvm` set while on that branch, but not sure if I played long enough to run into the bug. It could very well also just be AMD drivers being unstable as per usual, I've been running into some GPU resets in other applications recently after upgrading drivers that was solved by a linux-firmware downgrade. Will try more at some point

## Comment 4953193408

maintainer (COLLABORATOR) · goeiecool9999 · 2026-07-12T23:25:26Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-4953193408

Is this still an issue with the latest action builds?

## Comment 4953886936

other (NONE) · geowarin · 2026-07-13T02:26:56Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-4953886936

> Is this still an issue with the latest action builds?

I downloaded the latest commit appimage build and played BotW for a few hours (arch, mesa 26.1.4, 7800 XT).
I did not notice any texture corruption. The bug seems to be fixed for me. Thank you!

## Comment 5688520872

other (NONE) · Ash-Knight · 2026-09-15T21:45:21Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-5688520872

> Is this still an issue with the latest action builds?

Problem is still there for me unfortunately. I'm using a handheld device with Ryzen AI HX 9 365 with Radeon 880m GPU, driver mesa 26.2.2-arch3.2, cemu 2.6


## Comment 5688788946

maintainer (MEMBER) · Exzap · 2026-09-15T22:11:28Z · https://github.com/cemu-project/Cemu/issues/1176#issuecomment-5688788946

@Ash-Knight Try the latest appimage from https://cemu.info/ActionBuilds.php
