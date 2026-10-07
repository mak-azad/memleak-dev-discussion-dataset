# Memory usage seems to be directly proportional to map size

- URL: https://github.com/mapcrafter/mapcrafter/issues/257
- Repo: mapcrafter/mapcrafter (language: C++)
- State: open; created 2017-07-02T13:12:46Z; status ok; passes offcwe

## Issue body

reporter (NONE) · spekdrum · 2017-07-02T13:12:46Z · https://github.com/mapcrafter/mapcrafter/issues/257

Hi,
Love mapcrafter!
Once my map got bigger (now is about 5.4 Gb) Mapcrafter stopped working. Process gets killed instantly passed 15 minutes more or less. I saw in server logs process got killed by the system due to high ram usage (swap too). Tried to render with the simplest options (top view, no shaders) and lasts a bit more but finally it gets killed either way. Maybe I'm doing something wrong... but memory usage shouldn't be directly proportional to map size, isn't it? 

System specs: 
Debian
AMD dual core 1.3 Ghz
1GB RAM

Just compiled last version: e05dd4a0c4dd62928fa473e74444e00d92388a10
Same behaviour

## Comment 312910978

maintainer (MEMBER) · m0r13 · 2017-07-04T16:00:22Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-312910978

You are right, usually this shouldn't happen. Which version did you use before you compiled that latest version? How many threads are you running? Can you observe how much memory is exactly used before Mapcrafter is killed? A gigabyte of memory might be used up quickly if you are running multiple threads (> 4).

## Comment 312914767

reporter (NONE) · spekdrum · 2017-07-04T16:24:12Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-312914767

Sorry but I can't remember which version was... I thinks it was on May but last version behaves the same way.
I'm running just one thread. Memory used is almost the entire RAM and SWAP (2GB of swap space).  I'm preparing a little video showing exactly what happens to help you find the problem, monitoring with htop.

## Comment 312919204

reporter (NONE) · spekdrum · 2017-07-04T16:54:52Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-312919204

I found the first version I tried: 5d63220817fa19c31788366d9827afb68fb7495d
With last version (e05dd4a), just tried again to record the video and now (for the first time) is not reporting "process killed" but this:
```
terminate called after throwing an instance of 'std::bad_alloc'75/25550 16.53/s ETA 16m 30s
  what():  std::bad_alloc
```
I uploaded this video (hidden):
https://youtu.be/wouhOAJ06G8

## Comment 313882535

other (CONTRIBUTOR) · Bjarno · 2017-07-08T21:38:04Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-313882535

I added support for new blocks in Minecraft 1.11 and Minecraft 1.12 (the only change between the version you reported to be working, and the current version). I had to rewrite some parts of the application. I expect, but am not entirely sure, that I might have added a memory leak (easily to miss). I'll try to replicate this problem on a smaller virtual machine (I have 4GB on my server, and a smaller world, so I did not run into problems).

I'll check if my changes might result in memory leak, just to be sure.

## Comment 530934500

other (NONE) · DaMatrix · 2019-09-12T17:51:38Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-530934500

this is still an issue. i'm attempting to render a 100kx100k world, and left my computer running overnight only to find that my 12GB of RAM was full, along with most of my 1TB swap partition (yes, i'm aware that that's a rediculous size for swap, it's left over from an older project, cut me some slack :P). i've been able to render 20kx20k maps without this kind of usage in the past, using identical config.

## Comment 955762012

other (NONE) · alvarlagerlof · 2021-10-31T17:34:57Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955762012

I'm attempting to run this now on a small map in docker and the memory usage just keeps on growing until it gets killed.

## Comment 955762864

other (NONE) · miclav · 2021-10-31T17:40:32Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955762864

Hi
Indeed, the block map is huge and the memory allocation keeps growing
during map rendering.
I currently have a local branch, not submitted yet, that includes block map
optimisation, lower memory usage and other features.
Hoping it will allow small configs to work properly.
I’m planning to have that ready before end of year.


On Sun, Oct 31, 2021 at 13:35 Alvar Lagerlöf ***@***.***>
wrote:

> I'm attempting to run this now on a small map in docker and the memory
> usage just keeps on growing until it gets killed.
>
> —
> You are receiving this because you are subscribed to this thread.
> Reply to this email directly, view it on GitHub
> <https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955762012>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AC2XGQQVIGLRSPBVR6SA2ZLUJV445ANCNFSM4DROKJ6Q>
> .
> Triage notifications on the go with GitHub Mobile for iOS
> <https://apps.apple.com/app/apple-store/id1477376905?ct=notification-email&mt=8&pt=524675>
> or Android
> <https://play.google.com/store/apps/details?id=com.github.android&referrer=utm_campaign%3Dnotification-email%26utm_medium%3Demail%26utm_source%3Dgithub>.
>
>
-- 
Michael


## Comment 955763220

other (NONE) · alvarlagerlof · 2021-10-31T17:43:02Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955763220

> I currently have a local branch, not submitted yet, that includes block map

That's built on your world117 right?

## Comment 955763355

other (NONE) · miclav · 2021-10-31T17:44:04Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955763355

Right

On Sun, Oct 31, 2021 at 13:43 Alvar Lagerlöf ***@***.***>
wrote:

> I currently have a local branch, not submitted yet, that includes block map
>
> That's built on your world117 right?
>
> —
> You are receiving this because you commented.
>
>
> Reply to this email directly, view it on GitHub
> <https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955763220>,
> or unsubscribe
> <https://github.com/notifications/unsubscribe-auth/AC2XGQT4YKMMFOZVUYP4R73UJV53FANCNFSM4DROKJ6Q>
> .
> Triage notifications on the go with GitHub Mobile for iOS
> <https://apps.apple.com/app/apple-store/id1477376905?ct=notification-email&mt=8&pt=524675>
> or Android
> <https://play.google.com/store/apps/details?id=com.github.android&referrer=utm_campaign%3Dnotification-email%26utm_medium%3Demail%26utm_source%3Dgithub>.
>
>
-- 
Michael


## Comment 955763637

other (NONE) · alvarlagerlof · 2021-10-31T17:46:09Z · https://github.com/mapcrafter/mapcrafter/issues/257#issuecomment-955763637

Good to hear! Looking forwards to it.
