# [Feature request] Device name override

- URL: https://github.com/kcat/openal-soft/issues/1243
- Repo: kcat/openal-soft (language: C++)
- State: open; created 2026-02-11T06:48:53Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · ThreeDeeJay · 2026-02-11T06:48:53Z · https://github.com/kcat/openal-soft/issues/1243

It's been brought to my attention that one of the reasons some advice against installing OpenAL Soft into the game folder is that in rare cases, it crashes.
> This installation should be sufficient for most games, however, certain games (i.e. Kane & Lynch 2: Dog Days) may require a global installation of OpenAL Soft.[[5]](https://www.pcgamingwiki.com/wiki/Glossary:Surround_sound#cite_note-6)[[6]](https://www.pcgamingwiki.com/wiki/Glossary:Surround_sound#cite_note-7)
https://www.pcgamingwiki.com/wiki/Glossary:Surround_sound#OpenAL

So I just looked into that game and according to Rapture3D, it crashes unless the device name is `Generic Software`:
> Remove all *_oal.dll files from your Windows system32 or sysWOW64 directory except for rapture3d_oal.dll. Rapture3D also needs to be set to masquerade as "Generic Software" or the game will not start.
https://www.blueripplesound.com/compatible_openal_games

So I hard-coded that new name and compiled it:
https://github.com/ThreeDeeJay/openal-soft/actions/runs/21894113748

And sure enough, now the game starts and uses OpenAL32.dll without issues (I hear both HRTF and reverb, too):

<img width="601" height="148" alt="Image" src="https://github.com/user-attachments/assets/7b0aa139-215d-4abf-a192-5868bcf37430" />

<img width="1270" height="214" alt="Image" src="https://github.com/user-attachments/assets/e4a8239b-4b21-41fb-9e34-b8ce9bf9151a" />

Though I think a proper fix would require an option to override the device name in the ini, like we can currently do with vendor, version and renderer.

I know some games sometimes expect `Generic Software` or `Generic Hardware`, but I'm not sure if/what other games crash without it. Plus it would also simplify the OpenAL Soft installation instructions on PCGamingWiki, which I think is how many are introduced to it.

Also I think I mentioned somewhere that setting the OpenAL device name to be the same as the playback device name would allow using Creative ALchemy's dsound wrapper with OpenAL Soft, to fix games that crash with DSOAL, like https://github.com/kcat/dsoal/issues/88, while still being able to use OpenAL Soft HRTF. 👀👌 

## Comment 3886220408

other (NONE) · mirh · 2026-02-11T18:36:43Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3886220408

This is literally #757 with ⅒ of the thought put into it.
Worse, idk why those quotes with broken references and bringing up a game which we figured out yesterday (with jury still out on whether hex edit of the exe or saves can work decently).


## Comment 3888063239

maintainer (OWNER) · kcat · 2026-02-12T00:54:01Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3888063239

This seems to really be asking for an option to spoof the driver name, to replace the `OpenAL Soft` part of device names with something different. So the device names `"OpenAL Soft"`, `"OpenAL Soft on ..."` could become `"Generic Software"`, `"Generic Software on ..."` (or `"Generic Hardware"` or any other configurable string). Aside from the file being `soft_oal.dll` it would present Generic Software devices like `wrap_oal.dll` does (of course the devices themselves won't be bug- or feature-compatible with the wrapper driver, so anything that relies on the quirks or feature-set of the wrapper driver may still have issues, but it should be enough to get some games working).

This would be more practical nowadays since commit 6accc37a96e724df5da74bc935b3cd716b01674f moved the device name prefix handling out of the backends, reducing the number of places that need to worry about the "all devices" prefix. That commit also changed the backends to avoid directly setting the device name, which would also make it more practical to fake individual device driver names. Although making it configurable in a way to avoid conflicts (defining a driver name that is identical to an enumerated device name) might still be tricky. Or whether this feature needs to be available outside of Windows, given non-Windows systems haven't had to really deal with problems like this.

## Comment 3888128151

other (NONE) · mirh · 2026-02-12T01:15:42Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3888128151

The router should just pick up the first driver with that name in the list of the available ones, so my remotely educate guess is that this could win or loose depending on which OpenAL32.dll a game loads first (system32 or own folder) and on the location of soft_oal.
Also, if the wine guys weren't so callous with audio, this could be a linux problem too (as in, the system driver passthrough would have to compete with the built-in wrap_oal).

Regardless, while this re-spin of what I had called `ALSOFT_NAME` would be acceptable for whatever the prototyping that might have been needed, it's stupid to foresee as part of any official guide.
The proper course of action is to implement that device name matching thing.
Not only there are games only caring for that pre-router behaviour, if I had to take a guess it's far more likely there are ones treating generic software as a second class citizen (like STALKER) than illiterate developers hardcoding it for the last hurrah of their old ass engine in 2010.

## Comment 3888452273

reporter (CONTRIBUTOR) · ThreeDeeJay · 2026-02-12T03:20:13Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3888452273


Whichever method gets us past the K&L2 (maybe others) startup crash is cool with me, though I'd prefer the least user friction for the sake of noob-friendly guides (PCGW and Airtable) because pasting a 2-liner into the INI would be way easier than explaining how to properly hex edit or install other mods, plus K&L2 also needs `reverse-y=true` anyway so might as well kill 2 birds with the same stone, i.e. make it a 3-liner paste like:
```
[game_compat]
reverse-y=true
device-override=Generic Software
```
Though personally I was also still looking forward to being able to test different device names in some problematic games, and use ALchemy with OpenAL Soft for those pesky games that crash or lack features when using DSOAL.

## Comment 3889853699

maintainer (OWNER) · kcat · 2026-02-12T09:52:56Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3889853699

> Also, if the wine guys weren't so callous with audio, this could be a linux problem too (as in, the system driver passthrough would have to compete with the built-in wrap_oal).

A passthrough for OpenAL isn't a good idea in either case, I even advocated for Wine to remove it after I added it originally, because there were subtle but significant differences with, e.g. calling conventions, and stuff with resource allocators (threads, heap memory), that cause friction between the Windows side and the Linux side. It'd take a lot of work, both for Wine, as well as OpenAL Soft to add extensions that Wine would need for this lower level interaction, for no real benefit since the Windows build is fully functional (aside from Wine not having the best device configuration options for OpenAL Soft to autodetect it, but `alsoft.ini` can configure the devices as you want).

> The proper course of action is to implement that device name matching thing.
> Not only there are games only caring for that pre-router behaviour, if I had to take a guess it's far more likely there are ones treating generic software as a second class citizen (like STALKER) than illiterate developers hardcoding it for the last hurrah of their old ass engine in 2010.

There's two different things here. The "masquerading" feature referenced in the Rapture3D page, needed for K&L2 that hardcodes `"Generic Software"` or Battlefield 2142 that wants `"Generic Hardware"` when hardware audio is enabled, would be a config option to change the `OpenAL Soft` name and `OpenAL Soft on ...` prefix to what those games need.

Fooling Creative's router to put OpenAL Soft devices first to use by default, is a completely separate thing. That would either be done by including unprefixed names in the "basic"/driver enumerated names, or an option to define extra names to enumerate with the driver name which map to something else.

## Comment 3891554140

other (NONE) · mirh · 2026-02-12T15:17:03Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3891554140

> Whichever method gets us past the K&L2 (maybe others) startup crash is cool with me

AFAIU that was just the game being cursed *in general*, and then depending on whatever random heap glitches on one's computer you might have different likelihoods even just depending on dll load order.
Admittedly for the moment it doesn't appear to have much different solutions, but as it's literally the only game to do this for 0 reasons it would be kinda annoying for it to dictate the general train of thought for guides (I think warzone 2100 did something like that too once, but an indie developer screwing up his codebase with zero testing is something else entirely)

> though I'd prefer the least user friction for the sake of noob-friendly guides

Yes, and that is 100% playing nice with the official router, as I tried to explore and explain in the course of a dozen comments.
You just drop soft_oal in the windows folder and you call it a day for EVERY game (well dsoal aside).
If any you should open a feature request for a built-in compatibility database (as I think I may already have hinted somewhere).

> for no real benefit since the Windows build is fully functional

Wouldn't oal-soft direct interfacing with native pipewire offer better latency or cpu usage?
Also, now that I think to it.. isn't that in line with what they are trying to do in the new WoW64 architecture with EVERY possible dll?

> or Battlefield 2142 that wants "Generic Hardware" when hardware audio is enabled

I'm 99% sure that's just dumb people not understanding how the router works, I covered that extensively in #757

> Fooling Creative's router to put OpenAL Soft devices first to use by default, is a completely separate thing

It's not "fooling" to have a driver name to be identical to the enumerated device name?
Perhaps you could argue it's against the spirit of modern openal, but 20 years ago that was a bit of the expectation tbh (obviously there would be a knob for it, but not wanting to mess up with others use cases is also why I spent so much effort in my later comments).

## Comment 3892469001

reporter (CONTRIBUTOR) · ThreeDeeJay · 2026-02-12T17:52:18Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3892469001

> Yes, and that is 100% playing nice with the official router, as I tried to explore and explain in the course of a dozen comments.

I never understood the need to even interact with the router when we just wanna force OpenAL Soft.
If the game comes with a OpenAL32.dll that's a router, giving the system soft_oal.dll the highest priority would probably be fine.
But what if it's already an OpenAL library (e.g. an old OpenAL Soft, or Rapture3D like I think some Dirt games do)? That'd throw the system router (and libraries) out the window and cause some confusion when adding/updating OpenAL Soft to the system folder and it being ignored by the game. Of course we could just suggest deleting the local DLL but I think we also kill 2 birds with one stone by just replacing it to begin with.

> You just drop soft_oal in the windows folder and you call it a day for EVERY game (well dsoal aside).

Wouldn't that also require a modified router or can soft_oal guarantee highest priority on its own?
Either way, that's probably a good idea to do at least once but relying solely on it can be a double-edged sword. Because there may be cases where we *don't* want to upgrade OALS (e.g. newer builds broke lipsyncing in Deus Ex, not sure if that was ever fixed though DSOAL works better anyway AFAIK). Plus keeping a static version per game ensures it remains working as tested no matter what DLL the system/other games use. Even my database keeps track of what DLL was tested when specified on profiles, so we know if we ever need to downgrade or track down any potential regression commit.

## Comment 3893677574

maintainer (OWNER) · kcat · 2026-02-12T22:13:07Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3893677574

> Yes, and that is 100% playing nice with the official router, as I tried to explore and explain in the course of a dozen comments.
> You just drop soft_oal in the windows folder and you call it a day for EVERY game (well dsoal aside).

OpenAL Soft does play nice with the official router. It provides a unique driver name through the standard "driver" enumeration query, and prefixes the names given in the extended "all devices" enumeration (OpenAL Soft even prefixes capture device names, something `wrap_oal.dll` neglects to do, to be on good behavior). This ensures the intended behavior and won't step on anyone's toes to cause the router to misbehave, the definition of "playing nice".

This will not work for every game, as some games are written to expect the wrapper driver and/or hardware drivers by hardcoding certain device names, which there can never be a single solution to pacify all games. Some of the solutions depend on lying/spoofing names, which will invariably not play nice if those names already exist, or if one game wants one name over the other, and the other game wants the other name over the one.

The best course of action, I think, is to provide options to do the necessary spoofing that different games may need. Afterward, maybe OpenAL Soft can try to detect if it's being used in certain games and auto-enable the required options, but in the presence of the router, there's still a risk of conflicts that need manual intervention (e.g. if the game requires `"Generic Software"`, then `wrap_oal.dll` will need to be removed to avoid duplicating the name, but archived/restorable for games that rely on its quirks/bugs). This also depends on whether the user even wants OpenAL Soft to butt in and take over; sure there are reasons to want it to, but if a game is known to work fine enough in its default configuration, some may not care and just want it to work as they remember it working. Simply having OpenAL Soft shouldn't automatically interfere with games not designed or configured to use it.

> Wouldn't oal-soft direct interfacing with native pipewire offer better latency or cpu usage?

Not by a significant margin, I don't think. The vast majority of processing time is going to be in OpenAL Soft's renderer, which runs directly on the CPU regardless of it being the Windows build or not.

If we're talking about some kind of CPU emulation, then yes. Having the x86 Windows executable thunk to a native ARM OpenAL Soft library, for example, OpenAL Soft can do its processing with native ARM code instead of x86 code being JIT compiled or interpreted to ARM, which would be notably faster. Whether it would be so much faster to warrant making a proper thunk would be a question (JIT compilers are rather good these days).

> Also, now that I think to it.. isn't that in line with what they are trying to do in the new WoW64 architecture with EVERY possible dll?

The new WoW64 architecture is to avoid requiring native 32-bit libraries on a 64-bit system. So Wine can run 32-bit and 64-bit Windows app on a 64-bit Linux system without any host 32-bit libraries. With it, you actually want to stay in Win32 land as much as possible and use the Win32 DLLs where they exist and are practical, since going to/from host Linux code means switching the CPU between 32-bit and 64-bit mode, and ensuring any allocations done in the Linux code is aware when that memory may need to be accessed in 32-bit code to be allocated in the lower 32-bit address space (or else having a thunk to do some shadowing).

> It's not "fooling" to have a driver name to be identical to the enumerated device name?

It is, because in this context, OpenAL Soft is the driver. No matter what the output is, it's OpenAL Soft processing the OpenAL commands to generate the output. It wouldn't be the "Speakers (SB X-Fi Surround 5.1)" driver, for example, but OpenAL Soft which just happens to be outputting to the "Speakers (SB X-Fi Surround 5.1)" device, as denoted by the "OpenAL Soft on Speakers (SB X-Fi Surround 5.1)" device name. This is how Rapture3D and the wrapper driver behave too.

For "Speakers (SB X-Fi Surround 5.1)" to be the driver, that would be signalling that the OpenAL implementation is directly working with that device to process OpenAL commands and effectuate rendering. This is why `ct_oal.dll` does provide the device name as the driver name, because it is driving the named device to process the OpenAL commands.

> Perhaps you could argue it's against the spirit of modern openal, but 20 years ago that was a bit of the expectation tbh (obviously there would be a knob for it, but not wanting to mess up with others use cases is also why I spent so much effort in my later comments).

It was pretty messy in the past, prior to the `ALC_ENUMERATE_ALL_EXT` extension that helped solidify the idea of `ALC_DEVICE_SPECIFIER` being a "driver name" and `ALC_ALL_DEVICES_SPECIFIER` being the output device name (prefixed with the driver name as necessary to avoid name clashes between drivers). Back in the old old days, there wasn't even an enumeration extension, so the device name given to `alcOpenDevice` was a total free-for-all (the SI would even accept configuration strings). Then the `ALC_ENUMERATION_EXT` extension was added to help standardize expected device names, but at least in Windows with the router, it wasn't detailed enough since multiple drivers could use the same device, so `ALC_ENUMERATE_ALL_EXT` was created soon after with the idea that `ALC_ENUMERATION_EXT` would give basic driver names and `ALC_ENUMERATE_ALL_EXT` would give individual outputs for those drivers.

Granted this setup is still kinda messy with its own problems, but it's cleaner and more structured than it used to be. Regardless, this just goes to show that older apps making these assumptions need workarounds that break this structure, which invites conflicts if done automatically or by default, thus needing per-game care.

## Comment 3894044349

other (NONE) · mirh · 2026-02-12T23:59:29Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3894044349

> I never understood the need to even interact with the router when we just wanna force OpenAL Soft.

... because that's the way openal was meant to be used, but *even more importantly* because you just have to install soft_oal once and then just forget it?

> But what if it's already an OpenAL library (e.g. an old OpenAL Soft, or Rapture3D like I think some Dirt games do)?

I don't know of a single game that ships with openal-soft (except perhaps some modern FOSS thingie that regardless would be up to them to handle) and as for rapture3d.. I can't remember how they handle enumeration, but worst case scenario isn't any different from now?

> Of course we could just suggest deleting the local DLL but I think we also kill 2 birds with one stone by just replacing it to begin with.

You aren't killing any second bird if *even for the API that already took care of somewhat handling forward updates* you have people bother with each single game installation?
Of course there will always be exceptions, but KL2 ***supposedly*** hardcoding GS or dirt3 coming with R3D are the absolute exceptions that would always need to be read on their individual PCGW page anyway.

> or can soft_oal guarantee highest priority on its own?

### *YES.*
That's why I have kept banging for that issue left and right for the past half a decade, ever since noticing that even the freaking EnumerateWin32 sample exhibited the same behaviour that for 13 years people thought was Mass Effect being quirky and buggy.

> Either way, that's probably a good idea to do at least once but relying solely on it can be a double-edged sword.

Not really, I feel like I banged my head against everything and the kitchen sink possible already in #757

> Because there may be cases where we don't want to upgrade OALS

... ok and? Putting aside that regressions can always happen and we are here to find and fix them, that case would be ALWAYS a pain in the neck that would require special casing?

> This will not work for every game, as some games are written to expect the wrapper driver and/or hardware drivers by hardcoding certain device names, which there can never be a single solution to pacify all games.

Not at all in any way. It's just plain `alcOpenDevice(NULL)` all the way down, at most with *DirectSound3D* for the oldest cruft
(and how/why would they even do otherwise? almost every card model had a different name)

> This is how Rapture3D and the wrapper driver behave too.

The wrapper driver can afford to do that because rain or shine the router will always pick it up at last.

> This is why `ct_oal.dll` does provide the device name as the driver name, because it is driving the named device to process the OpenAL commands.

And that's the implicit reasoning the standard router works by to pick up the default device.
Also of note that depending on the dll load order, default `ALC_ENUMERATE_ALL_EXT` can decide to pick up generic software.

## Comment 3894713819

maintainer (OWNER) · kcat · 2026-02-13T03:54:20Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3894713819

> Not at all in any way. It's just plain `alcOpenDevice(NULL)` all the way down, at most with DirectSound3D for the oldest cruft

For apps that only ever call `alcOpenDevice(NULL)` (or `alcOpenDevice("")`, etc), doing anything to make the Creative's router use `soft_oal`'s `alcOpenDevice` by default would be fine, but there's no way to do that in a correct and safe way. At best, a `[game_compat]` config option to make OpenAL Soft enumerate devices differently to trick Creative's router would be needed (as well as ensuring the user doesn't have real hardware and drivers to cause duplicate names).

> (and how/why would they even do otherwise? almost every card model had a different name)

Going by the Rapture3D compatibility list, at least Battlefield 2142 seems to use `"Generic Hardware"` when configured to use hardware audio, rather than any specific device name (maybe it also looks for devices with/without specific EAX extensions, `AL_VENDOR`/`AL_RENDERER` strings, and/or certain patterns in device names, but that's not really relevant to the device name enumeration discussion). Incidentally I notice in the router, if the app tries to open `"Generic Hardware"` and it can't be found in the enumerated driver name list, it tries to look for `"Generic Software"` instead (`"Generic Hardware on ..."` names aren't handled, and if `"Generic Software"` doesn't exist, it basically then gives up).

> The wrapper driver can afford to do that because rain or shine the router will always pick it up at last.

Not necessarily. The directory order the router searches is:

* the same directory as `OpenAL32.dll` (if it's not the same as the system directory), then
* the current working directory, then
* the executable directory (if it's not the same as the current working directory), then
* the system directory (if it's not the current working directory or executable directory)

Within each directory, it searches for files named `*oal.dll` using `FindFirstFile`/`FindNextFile`. If `wrap_oal.dll` is found in an earlier directory (e.g. if an app comes with an `OpenAL32.dll` router and `wrap_oal.dll` in the executable directory, while `soft_oal.dll` and others are in the system directory), the wrapper driver will be picked up first. Or if `FindFirstFile`/`FindNextFile` decide not to return files sorted by name, or if there's other driver files that get sorted after `wrap_`. There's no direct mention of `wrap` in the code, it only usually ends up last by happenstance (`w` being the fourth-to-last letter of the alphabet helps for alphabetical sorting, but is by no means foolproof).

Looking a bit more at the router's code, it seems there may be other issues as well. To determine which device it tries to open by default (when calling `alcOpenDevice(NULL)` or equivalent), it does so by loading `dsound.dll` from the system directory and calling `DirectSoundEnumerateA`, taking the first proper device name. It then searches the "basic"/driver names it enumerated previously, doing an exact compare all the names (which being the basic/driver names, would really only be able to match hardware drivers; if it doesn't find a match, then it searches for the first one that contains `X-Fi`, then `Audigy`, then `Generic Hardware`, then `Generic Software`, then it takes the first name if all previous checks failed).

The issue here is that `DirectSoundEnumerateA` gives strings using the current code page, where OpenAL Soft's strings are always UTF-8. So even if OpenAL Soft returns unprefixed device names for the basic/driver enumeration to try to match Windows' reported default name, the comparison can fail if it contains any incompatible encoded characters. Windows can be set to use a UTF-8 codepage to help, though I don't think that's recommended on older Windows versions. Another issue is, if COM isn't initialized when the router makes that call, the device names it gets may be truncated (OpenAL Soft using WASAPI doesn't suffer this problem, though even the DSound backend works around it by initializing COM as needed to avoid truncation). So even if the strings' characters are compatible, it may still fail to match depending on what the app has done.

## Comment 3898736463

reporter (CONTRIBUTOR) · ThreeDeeJay · 2026-02-13T18:37:36Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3898736463

> ... because that's the way openal was meant to be used, but _even more importantly_ because you just have to install soft_oal once and then just forget it?

I meant specifically in cases (probably most) _when we just wanna force OpenAL Soft_ no matter what. In those cases, the router just seems like an unnecessary (sometimes slower) middle-man, unless it does provide any benefits I'm yet to see? Also, are we really gonna trust noobs to mess around their system folders? And god forbid someone gets the bright idea that DSOAL should be installed the same way and somehow stumbles their way into taking ownership and replacing the system dsound.dll, potentially breaking a ton of apps. 

Not to mention if they want HRTF with a system-wide installation (which won't be automatically turned on 9/10 times because AFAIK most people's playback devices aren't detected as headphones), they would also need to copy alsoft.ini into `%APPDATA%` (unless it can also be read from the system folder? idk). Or just drop the INI into the game folder which they should be doing for game-specific settings anyway, but in that case they might as well just copy everything in one go. Sure, it's easier (and maybe even better) for users we can trust know their way around safely manipulating system files but I'm trying to assume the lowest common denominator with a simple drag and drop per game. So the way I see it, it comes down to easy but potentially risky and/or ineffective (i.e. game includes library as OpenAL32.dll) versus slightly repetitive/inconvenient but mostly guaranteed way to work *and* stay working.

> I don't know of a single game that ships with openal-soft (except perhaps some modern FOSS thingie that regardless would be up to them to handle)

The biggest one I know is Minecraft and there's a handful [here](https://steamdb.info/search/?a=patchnotes&q=%22openal-soft%22&appid=) and there's [some in my database](https://airtable.com/appayGNkn3nSuXkaz/shrT4aLa9ulWKQ5Dv) (there's a lot more that I haven't marked as built-in) and it's hard to tell which ones added sof_oal as OpenAL32.dll but yeah, I've seen enough to be worried about it causing confusion. 

> KL2 _**supposedly**_ hardcoding GS

I just checked and it is indeed the case.

<img width="588" height="99" alt="Image" src="https://github.com/user-attachments/assets/d983c4d6-6214-4484-8ec4-d93bd939992b" />

And this fixed the crash:
<img width="541" height="86" alt="Image" src="https://github.com/user-attachments/assets/c0b31c5b-3841-49b6-b581-27f246795727" />
But then again, it goes back to my point of making it as easy as possible for the commonfolk: pasting the [3-liner](https://github.com/kcat/openal-soft/issues/1243#issuecomment-3888452273) is way easier than learning proper hex editing, and even assuming they know how, they'd still need the line to invert the sound field. And on that same note, it would also be easier to add `device-override=Generic Software` in games that expect it even if they don't crash, to save people the further hassle of unearthing the game config file where they have to set the device name to use OpenAL Soft (e.g. Unreal engine 3/4), which is why [Rapture3D bothered implementing masquerading](https://www.blueripplesound.com/compatible_openal_games) and even they sometimes recommended replacing the local OpenAL32.dll (though I don't like their idea of having to delete all other *_oal.dll from the system folder).

So I don't see what all the fuss is about. https://github.com/kcat/openal-soft/issues/757 seems like a good idea for a default behavior (though renaming the playback device, especially if messing with the registry, or setting environmental variables doesn't really sound noob-friendly) but this one is more about combating game-specific exceptions to the rule so I don't see why these have to be mutually exclusive.

## Comment 3963179114

other (NONE) · mirh · 2026-02-26T00:50:02Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3963179114

> but there's no way to do that in a correct and safe way. 

How not? You just have it take the name of the device currently default in the OS and that's it (this is for `ALC_ENUMERATION_EXT` at least, I don't want to think to ALL_EXT now).

> (as well as ensuring the user doesn't have real hardware and drivers to cause duplicate names).

I'm pretty damn sure that's a not a problem considering that I'm not aware of an openal implementation that comes alphabetically \*later\* than *soft_oal* (other than *wrap_oal* of course).

> Going by the Rapture3D compatibility list, at least Battlefield 2142 seems to use "Generic Hardware" when configured to use hardware audio

~~That's just (for the third time) bollocks from people that didn't understand the~~
I just checked the game, and [as you can see](https://www.pcgamingwiki.com/wiki/File:BF2142_Audio.jpg) "Hardware" is not the best one you want. To enable the "Creative X-Fi" setting you need the `EAX5.0` extension to be present (which obviously they didn't have, putting even aside getting accepted as the default device). I couldn't find any "direct mention" of anybody then.
Also of note if somebody ever wanted to experiment, inside of *BF2142Audio.dll* I also found `EAX-RAM` mentions (`BF2OpenAL.dll` is instead just a renamed 2.1.8.1 *wrap_oal.dll*).

> if the app tries to open "Generic Hardware" and it can't be found in the enumerated driver name list, it tries to look for 

.... I already unpacked that far and wide in #757, the order of loading is:
1. search for a driver whose name **exactly** matches the default system audio device
2. search for a partial match if the device name contains 'X-Fi' (obviously only a thing in later routers)
3. search for a partial match if the device name contains 'Audigy'
4. search any driver name that is a partial match with 'Generic Hardware' ("DirectSound3D" previously)
5. search any driver name that is a partial match with 'Generic Software' ("DirectSound" previously)
6. pick the first device in the enumeration order regardless

> Not necessarily. The directory order the router searches is:

I didn't say *for last*. I said *at last*, as in "eventually" when no driver name is exactly matching your device (which happens always ***if*** you are on Vista+ without dsoal or a soundblaster).

> So even if the strings' characters are compatible, it may still fail to match depending on what the app has done.

And older programs (and routers before 2006) used MMSYSTEM which had a 32 characters limit. I had already mentioned that, and my last posts were even pitches for some automatic compatibility mechanism (I had missed the codepage aspect though, nice to keep in mind).

---
> In those cases, the router just seems like an unnecessary (sometimes slower) middle-man, unless it does provide any benefits I'm yet to see?

It is kind of unncessary, *but* besides the "benefit" of playing nice by the rules as I'm telling you it allows to forget about having to tinker with every single game.
I will admit that I totally did not even consider using "Generic Software" in #757, but even without second guessing how games may treat it cancerously like "Generic Hardware" it can still fail as I am saying. A game that ships with its own openal32 and wrap_oal (like any UE3 one) is going to beat you in the enumeration order if you aim for points number 4 or 5.

> Also, are we really gonna trust noobs to mess around their system folders? 

There is no trust other than the already supposedly normal system installation of soft_oal.

> I just checked and it is indeed the case.

I know it's in the exe, twice actually. My doubt was about the chunk of decompiled code that ghidra showed me, not exactly being straightforward to interpret into how those strings are used (including supposedly allowing directsound too).

> the further hassle of unearthing the game config file where they have to set the device name to use OpenAL Soft 

### THAT IS LITERALLY WHAT LEAD ME TO FIGURE OUT #757 IT WAS NEVER A BUG OR LIMIT OF GAMES

> https://github.com/kcat/openal-soft/issues/757 seems like a good idea for a default behavior 

Tbf I'm open even for that *not* be default if preserving the natural order of things is of the utmost importance (or at least by default it could be just applied automatically to whatever could meet some general detactable criteria of "old as hell"). Honestly, the hardest thing to decide seemed just the enviroment variable name for the knob.

> (though renaming the playback device, especially if messing with the registry, or setting environmental variables doesn't really sound noob-friendly)

That was all just part of my experimenting with how viable the alternatives were. The TL;DR at the end is just that either you aim for OG hardware device name matching path (except in this one stupid bugged case of KL2) or you are going to have a bad time and special casing forever.

## Comment 3963889934

maintainer (OWNER) · kcat · 2026-02-26T04:26:20Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3963889934

> > but there's no way to do that in a correct and safe way.
> 
> How not? You just have it take the name of the device currently default in the OS and that's it (this is for `ALC_ENUMERATION_EXT` at least, I don't want to think to ALL_EXT now).

As well as ensure there isn't another driver providing the same name, or else there's no guarantee the router will use OpenAL Soft for the default name over the other driver. It would still need some manual user intervention on top of some config option to safely alter enumeration behavior like this.

> > (as well as ensuring the user doesn't have real hardware and drivers to cause duplicate names).
> 
> I'm pretty damn sure that's a not a problem considering that I'm not aware of an openal implementation that comes alphabetically *later* than _soft_oal_ (other than _wrap_oal_ of course).

Alphabetical ordering is only relevant when the dlls are in the same directory. `ct_oal.dll` can be picked up after `soft_oal.dll`, and `wrap_oal.dll` can be picked up before `soft_oal.dll`, depending on which directories they're all in. And which directories are searched first depends on where the exe is, where OpenAL32.dll is (whether the game has its own with the executable, or uses a preinstalled one in the system directory), and what the current working directory is. I can't just assume it'll work to drop a DLL or two in somewhere and set a config option; the load order of the driver DLLs is a bit too volatile to ensure the desired DLL will always handle a given name when two or more DLLs enumerate the same name.

This is likely the reason why the Rapture3D page continually suggests removing the other driver DLLs from the system and app directories for games that need its driver masquerading option, because there's no guarantee one of them can't be picked up anyway and manage to get itself used for the name the Rapture3D driver is trying to masquerade as.

> And older programs (and routers before 2006) used MMSYSTEM which had a 32 characters limit.

That is probably the same reason why DirectSoundEnumerateA/W may give truncated names. Without COM initialized, DSound itself seems to fall back to using MMSYSTEM (or the same underlying methods) to retrieve the device info in a small fixed-size buffer to give to the callback, whereas COM being initialized allows it to query the relevant info in a larger or dynamic buffer size.

> > Also, are we really gonna trust noobs to mess around their system folders?
> 
> There is no trust other than the already supposedly normal system installation of soft_oal.

FWIW, I've always wanted to have a proper installer so a user didn't have to be copying files into the system directories manually. It's just never something I've learned how to properly make. And realistically, these days on Windows/Mac, OpenAL Soft is typically going to be provided by the game and used directly, instead of installed as a driver to use through the system OpenAL (not that it wouldn't still be useful, just not as much as it may have been 10 to 20 years ago).

## Comment 3968046585

other (NONE) · mirh · 2026-02-26T17:20:56Z · https://github.com/kcat/openal-soft/issues/1243#issuecomment-3968046585

> As well as ensure there isn't another driver providing the same name, or else there's no guarantee the router will use OpenAL Soft for the default name over the other driver.

I thought your concern was about ***not*** wanting to disrupt whatever else may already be existing, as opposed to making sure openal-soft can win even in those cases.
Well.. rejoice, because now that I was thinking to it, *ct_oal* uses path number 2 or 3. Meaning that *soft_oal* being "the last of the first one" would still have you on top (I guess *nvopenal* and *cm_oal* would need to delete their sysytem dll but come on at this point).

> Alphabetical ordering is only relevant when the dlls are in the same directory.

Yes, sorry. I meant with respect to loading system dlls.

> the load order of the driver DLLs is a bit too volatile to ensure the desired DLL will always handle a given name when two or more DLLs enumerate the same name.

I'm not sure how many people you are thinking are installing an openal driver (with the exception of this very one) in the year of the lord 2026.

> This is likely the reason why the Rapture3D page continually suggests removing the other driver DLLs

Yes, because they only ever tried to do path number 4 or 5?

> OpenAL Soft is typically going to be provided by the game and used directly, instead of installed as a drive

Unless you are phantasizing about having a loader mechanism for using newer system provided versions in programs that have it built-in (akin to how physx does it), I'm not sure how it pertains the issue.

Maybe that this auto-renaming thing could just apply when the dll gets loaded through the router?

> (not that it wouldn't still be useful, just not as much as it may have been 10 to 20 years ago)

No disrespect, and maybe I'm partial to this, but I feel like 10 to 20 years old games are probably still the greater use case.
