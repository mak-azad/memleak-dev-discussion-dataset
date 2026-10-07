# Winamp - Crash after for some port connects

- URL: https://github.com/wineasio/wineasio/issues/23
- Repo: wineasio/wineasio (language: C)
- State: open; created 2021-03-16T19:00:30Z; status ok; passes main

## Issue body

reporter (NONE) · BlueMax · 2021-03-16T19:00:30Z · https://github.com/wineasio/wineasio/issues/23

Hallo,
i've set up **Winamp/ASIO** and even though audio quality is more or less beautiful it **crashes quite reliably after switching some tracks.** It seems somewhat buffer dependent. The greater the buffer in the Winamp ASIO plugin the lower the chance to crash (thus set to max). I also played with WineASIO configs in regedit and Jack buffers but it didn't help.

I've put up a video for demonstration below. There are roughly 3 parts. The first one shows the ASIO plugin behavior, skipping some tracks until it crashes. The second part shows the same without ASIO (via DirectSound/Loopback/zita-a2j instead). It runs flawlessly. The 3rd part shows a very specific behavior of the ASIO plugin in Carla when moving any element/box when the ASIO plugin is present. It crashes Wine/WineASIO immediately and produces somewhat high stress on the Jack backend (massive xruns) so that even QJackQtl needs some time to recover (and also crashed audio in the video below). This could be related.

If you look closely during track changes you can see that the **'Winamp' element (in Carla) is flickering shortly**. That's probably a re-initialization of the Jack device that is somewhat flakey i guess. It can repeat that only for some time then it crashes (Wine/WineASIO?).

There is also weird behavior when manually trying to connect the WineASIO ports. **Ports do not connect until Winamp is 'paused'**. During 'play' you cannot connect. It just flickers once as it would have crashed. But 'jack-matchmaker' can somehow connect it reliably though (QjackCtl can not, tries for some time and gives up). But that's probably not directly the cause for the crashes. If ports do not get connected at all it crashes nevertheless when skipping some tracks (as it still re-initializes). Something seems to stack up in the background because of re-initialization.

Long story short. I guess the culprit is the permanent re-initialization of the WineASIO device in Jack whenever you play/stop/skip. Maybe some resources are not freed, memory leak or something adds up in the background. I don't know. 

**Would it be possible to keep the WineASIO device somehow persistent/reserved so it wouldn't re-initialze every time?**

Video: https://dl.dropboxusercontent.com/s/sib48o0sku10eyk/WineASIO-Winamp-Crash.mkv
17MB, h264/RGB, 1080p

Arch Linux 5.11.6
jack2 v1.9.17
Carla 2.3.0.RC1.r8.g892314005-1
jack-matchmaker v0.9.0
Winamp v5.666
[Winamp ASIO plugin v0.67z4](https://sourceforge.net/projects/winamp-asio-plugin)
Wine v6.4
wineasio-git r50.4b23797-2 (2021.03.12)

## Comment 801446667

maintainer (MEMBER) · falkTX · 2021-03-17T21:13:04Z · https://github.com/wineasio/wineasio/issues/23#issuecomment-801446667

Persistent asio connection will be a host/app job, wineasio should not try to do that, it is likely not technically possible anyway.
Since this winamp plugin is open-source, it is likely best to report issue there instead. Or better yet, to try to fix it.


## Comment 801465956

reporter (NONE) · BlueMax · 2021-03-17T21:50:19Z · https://github.com/wineasio/wineasio/issues/23#issuecomment-801465956

That behavior is probably correct though (for Windows). I rather thought about a general Wine/WineASIO improvement. But if you say its not advisable let's forget about that.

Then the question is why does it crash after some time? Its very unlikely that this happens on Windows. Its a long-standing plugin. It also happens with the original (unmodded) plugin. All other ASIO plugins i've found do not find the WineASIO driver at all (only ASIO4ALL - but that's useless).

Should i file a Wine bug or can you take a look what's going on? I'm not sure what component is responsible for the bug (and who's in charge for that).

## Comment 801469483

maintainer (MEMBER) · falkTX · 2021-03-17T21:58:07Z · https://github.com/wineasio/wineasio/issues/23#issuecomment-801469483

Crash could be in JACK too, I do not think this would be a Wine bug (though you are welcome to try different versions of wine to see if it makes any difference)

I mention modifying the plugin because of the start/stop driver behaviour is not something I see will change in wineasio. Usually when a tool does something like this, it is bad coding on the application side.
One notable one is audacity, that using portaudio it stops and starts the driver only when playback or recording is active. And we end up with exactly the same issue as we have here with JACK open/close multiple times.

And if we can change the start/stop behaviour of the asio plugin, it likely fixes this issue too.
So seems best to me to try and tackle this by going into that direction first.


## Comment 801558348

reporter (NONE) · BlueMax · 2021-03-18T01:59:41Z · https://github.com/wineasio/wineasio/issues/23#issuecomment-801558348

> Crash could be in JACK too

Not sure. The behavior when moving the Winamp node in Carla causing a crash is suspicious indeed. But it seems to be (at least from Jacks view) just a "stress situation" that Jack can handle gracefully. Jack hits many xruns but survives and comes back when it cools down (1-2 seconds).

The Winamp crash due to skipping tracks is Wine only (crash or freeze). Jack seems unaffected without any xruns and still works properly.
 
> I mention modifying the plugin because of the start/stop driver behaviour is not something I see will change in wineasio. Usually when a tool does something like this, it is bad coding on the application side.

I'm not sure how Winamp internals work but output plugins probably need to unregister cleanly on stop by (Winamp API) design. Switching plugins in settings dialog during playback usually doesn't have any effect until stop/play.
The driver start/stop behavior itself (at least for me) is not a problem (can be handled by external auto-connectors). But the crashes are.

> One notable one is audacity, that using portaudio it stops and starts the driver only when playback or recording is active. And we end up with exactly the same issue as we have here with JACK open/close multiple times.

I've tested that. It does open/close every time indeed but it doesn't crash no matter how often restarted and the node in Carla can be moved without problems. Not tested with the new Audacity v3 though.

> And if we can change the start/stop behaviour of the asio plugin, it likely fixes this issue too.
> So seems best to me to try and tackle this by going into that direction first.

That's probably above my head but i could ask the mod coder about the plugin behavior.

Unless you still have some ideas i think there is nothing more about WineASIO then. Feel free to close and thank you so far!
Maybe i bring this up on the Jack bug tracker again to catch some more thoughts.
