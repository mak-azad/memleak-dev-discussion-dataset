# File descriptor leak?

- URL: https://github.com/Keriew/augustus/issues/1207
- Repo: Keriew/augustus (language: C)
- State: open; created 2025-04-24T19:09:58Z; status ok; passes offcwe

## Issue body

reporter (NONE) · kuuff · 2025-04-24T19:09:58Z · https://github.com/Keriew/augustus/issues/1207

I didn't stopped augustus for a while, kept alt-tabbing out of it. I'm not sure for how long. Maybe a week? Then Augustus stopped playing sounds. Not all of them, some sounds were played sometimes. I believe that background city sounds stopped playing. Moreover I couldn't save the game, Augustus didn't show file names of save files (it was an empty list) and when I tried to save it claimed that file permissions are wrong.

I really wanted to save, and luckily I run a debug build, so I attached to it and found that the real error is "too many open files". I used prlimit from root to increase limits for the process (it was 8192), and voila sounds started working and I could save the game.

There is two things though...

1. It is not just debug build but a build with lua embedded in it. I'm sure lua doesn't do this. I work with files only by calling lua_dofile passing a file name to it. lua_dofile opens and closes files. But I decided to mention it because... you know, shit happens.
2. It was not the latest commit, it was 5d8fc66ba7dccb38dfff1cf17e19cda60ae03e1a.

To make sure that (1) and (2) do not play any role, I pulled the latest commit in master and run augustus while checking it with lsof. I saw there multiple file descriptors for the same files (lsof output attached below). New duplicates arrive very infrequently (maybe 1 per minute?), but I think if you let augustus to run for a week, you can exhaust 8k file descriptors with this frequency.

Probably I should add one more detail. It is Campaign Reconquered (Tarentum, 4th mission). I don't think it matters though.

Below the debug session. perror wrote the error into the other terminal were I started augustus from, I couldn't run gdb from there because alsa-overruns spam, but believe me it was too many files opened error. I've lost Augustus log in terminal. Didn't thought to save it at once, and then it was buried.

```
$ gdb --pid 4568
GNU gdb (Gentoo 15.2 vanilla) 15.2
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://bugs.gentoo.org/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word".
Attaching to process 4568
[New LWP 4586]
[New LWP 4585]
[New LWP 4584]
[New LWP 4583]
[New LWP 4579]
[New LWP 4578]
[New LWP 4577]
[New LWP 4576]
[New LWP 4575]
[New LWP 4574]
[New LWP 4570]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib64/libthread_db.so.1".
0x00007f35442e75df in poll () from /lib64/libc.so.6
(gdb) b game_file_write_saved_game
Breakpoint 1 at 0x55c9f43e1017: file /home/user/src/augustus/src/game/file.c, line 452.
(gdb) continue
Continuing.

Thread 1 "augustus" hit Breakpoint 1, game_file_write_saved_game (
    filename=0x55c9f46cbe40 <corrected_filename> "/home/user/.local/share/augustus/augustus/savegames/go-incoming.svx") at /home/user/src/augustus/src/game/file.c:452
452	    return game_file_io_write_saved_game(filename);
(gdb) s
game_file_io_write_saved_game (
    filename=0x55c9f46cbe40 <corrected_filename> "/home/user/.local/share/augustus/augustus/savegames/go-incoming.svx") at /home/user/src/augustus/src/game/file_io.c:1735
1735	{
(gdb) list
1730	    }
1731	    return savegame_read_file_info(info, save_version);
1732	}
1733	
1734	int game_file_io_write_saved_game(const char *filename)
1735	{
1736	    resource_set_mapping(RESOURCE_CURRENT_VERSION);
1737	    init_savegame_data(SAVE_GAME_CURRENT_VERSION);
1738	
1739	    log_info("Saving game", filename, 0);
(gdb) n
1736	    resource_set_mapping(RESOURCE_CURRENT_VERSION);
(gdb)
1737	    init_savegame_data(SAVE_GAME_CURRENT_VERSION);
(gdb)
1739	    log_info("Saving game", filename, 0);
(gdb)
1740	    savegame_save_to_state(&savegame_data.state);
(gdb)
1742	    FILE *fp = file_open(filename, "wb");
(gdb)
1743	    if (!fp) {
(gdb)
1744	        log_error("Unable to save game", 0, 0);
(gdb) p filename
$1 = 0x55c9f46cbe40 <corrected_filename> "/home/user/.local/share/augustus/augustus/savegames/go-incoming.svx"
(gdb) p perror("")
'perror' has unknown return type; cast the call to its declared return type
(gdb) p (int)perror("")
$2 = 0
(gdb) continue
Continuing.

Thread 1 "augustus" hit Breakpoint 1, game_file_write_saved_game (
    filename=0x55c9f46cbe40 <corrected_filename> "/home/user/.local/share/augustus/augustus/savegames/go-incoming.svx") at /home/user/src/augustus/src/game/file.c:452
452	    return game_file_io_write_saved_game(filename);
(gdb) d
Delete all breakpoints, watchpoints, tracepoints, and catchpoints? (y or n) y
(gdb) continue
Continuing.

[Thread 0x7f350f82d6c0 (LWP 4586) exited]
[Thread 0x7f3530f2e6c0 (LWP 4585) exited]
[Thread 0x7f35317fa6c0 (LWP 4584) exited]
[Thread 0x7f3531ffb6c0 (LWP 4583) exited]
[Thread 0x7f35439ff6c0 (LWP 4570) exited]
[Thread 0x7f3533fff6c0 (LWP 4576) exited]
[Thread 0x7f35337fe6c0 (LWP 4577) exited]
[Thread 0x7f3532ffd6c0 (LWP 4578) exited]
[Thread 0x7f35327fc6c0 (LWP 4579) exited]
[Thread 0x7f3538cbd6c0 (LWP 4575) exited]
[Thread 0x7f35395ff6c0 (LWP 4574) exited]
[Inferior 1 (process 4568) exited normally]
(gdb)
The program is not being run.
(gdb)
```

Output of lsof, last several lines. It is the latest commit (21a87fd16ffea8ca3a4a91ff7946c599975b69cc), limits are not exhausted (yet?). Three ConcreteMaker.ogg are opened.
```
$ lsof -p 19993 | nl
...
    88	augustus 19993  user  21w     FIFO               0,12       0t0 20208536 pipe
    89	augustus 19993  user  22r      CHR             116,33       0t0      460 /dev/snd/timer
    90	augustus 19993  user  23u      CHR              116,2       0t0      658 /dev/snd/pcmC0D0p
    91	augustus 19993  user  24u      CHR              116,7       0t0      668 /dev/snd/controlC0
    92	augustus 19993  user  25r      REG               8,54     29274  8266996 /home/user/src/augustus/res/assets/Sounds/Prefect.ogg
    93	augustus 19993  user  26r      REG               8,54     30918  8266991 /home/user/src/augustus/res/assets/Sounds/Engineer.ogg
    94	augustus 19993  user  27r      REG               8,54     37479  8266989 /home/user/src/augustus/res/assets/Sounds/Brickworks.ogg
    95	augustus 19993  user  28r      REG               8,54     16287  8266995 /home/user/src/augustus/res/assets/Sounds/Ox.ogg
    96	augustus 19993  user  29r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
    97	augustus 19993  user  30r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
    98	augustus 19993  user  31r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
    99	augustus 19993  user  32r      REG               8,54     30918  8266991 /home/user/src/augustus/res/assets/Sounds/Engineer.ogg
```

While I composed this bug report augustus got more file descriptors open:
```
$ lsof -p 19993 | nl | tail
    95	augustus 19993  user  28r      REG               8,54     16287  8266995 /home/user/src/augustus/res/assets/Sounds/Ox.ogg
    96	augustus 19993  user  29r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
    97	augustus 19993  user  30r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
    98	augustus 19993  user  31r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
    99	augustus 19993  user  32r      REG               8,54     30918  8266991 /home/user/src/augustus/res/assets/Sounds/Engineer.ogg
   100	augustus 19993  user  33r      REG               8,54     37479  8266989 /home/user/src/augustus/res/assets/Sounds/Brickworks.ogg
   101	augustus 19993  user  34r      REG               8,54     16287  8266995 /home/user/src/augustus/res/assets/Sounds/Ox.ogg
   102	augustus 19993  user  35r      REG               8,54     39313  8266990 /home/user/src/augustus/res/assets/Sounds/ConcreteMaker.ogg
   103	augustus 19993  user  36r      REG               8,54     29274  8266996 /home/user/src/augustus/res/assets/Sounds/Prefect.ogg
   104	augustus 19993  user  37r      REG               8,54     30918  8266991 /home/user/src/augustus/res/assets/Sounds/Engineer.ogg
```

## Comment 2828982890

maintainer (COLLABORATOR) · crudelios · 2025-04-24T22:16:17Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2828982890

Hi,

This seems to be a bug from SDL. At least I tried reproducing it on macOS but `ls` is not giving me any duplicate files.

Can you tell me which version of SDL and SDL_mixer you're using, please?

## Comment 2829390922

reporter (NONE) · kuuff · 2025-04-25T05:13:35Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2829390922

media-libs/libsdl-1.2.68::gentoo
media-libs/sdl-mixer-1.2.12_p20221010::gentoo

## Comment 2829613188

maintainer (COLLABORATOR) · crudelios · 2025-04-25T07:37:16Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2829613188

You should also have version 2 of both libsdl and libsdl_mixer as those as version 1 is incompatible with augustus. Can you check, please?

Oh and also the libvorbis version, please!

## Comment 2829785655

reporter (NONE) · kuuff · 2025-04-25T08:53:02Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2829785655

Sorry.
media-libs/libsdl2-2.30.7-r1::gentoo
media-libs/sdl2-mixer-2.6.3-r1::gentoo
media-libs/libvorbis-1.3.7-r1::gentoo

There are updates for them, I kinda slacked for few months and didn't update my system. I'll try to update them and look into the issue, but it will take some time, it is Gentoo.

## Comment 2829794735

maintainer (COLLABORATOR) · crudelios · 2025-04-25T08:56:58Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2829794735

Yeah gentoo takes its time to update. I used it for a little while a very very long time ago back in the early 2000's, installation took a full day!

Sdl and mixer shouldn't take too long, but the dependencies will definitely take some time.

I'm going to check on linux as well, but I can say that it's sdl that handles the audio files, I only pass the audio file name string and the libraries do the rest. So I think it's either sdl/sdl_mixer or some deeper issue.

## Comment 2833342554

reporter (NONE) · kuuff · 2025-04-27T09:09:56Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2833342554

I think I've found the reason. It was SDL2-mixer built without vorbis support. I have rebuilt it with +vorbis, and now I see no these .ogg files opened in lsof. I still think it is a bug (either augustus or sdl2-mixer doesn't handle errors properly) but it is a minor issue I believe. A very special case.

> Sdl and mixer shouldn't take too long, but the dependencies will definitely take some time.

I didn't updated my system for some time, so I need to start with emerge --sync to update repos, and then emerge wants to update 300+ packages. I could try to pick just sdl2, but emerge could still choose to upgrade to a lower version because something depends on in. So I decided to do a full upgrade.

While it was doing it I've found that it builds rustc a dozen of times. I figured out I need to move to rust-bin, to avoid that, but the time was wasted. Plus I've lost time when /var/tmp/distfiles used all the free space on the disk. It is one more interesting issue I need to dig into, because I use eclean distfiles and still 20G of space is not enough. I cleared it with rm *, but wtf. Now I cannot build mesa, because of a bug in a ebuild. Updating Gentoo after a pause is an adventure. Though this time is more adventurous than average.



## Comment 2833376452

maintainer (COLLABORATOR) · crudelios · 2025-04-27T10:31:39Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-2833376452

It seems to be an issue with sdl mixer. I looked at the code and check if we handle the errors properly, and we do, so the issue is inside the library.

I'll post an issue to sdl_mixer, it's probably never been found before because it's very rare that the mixer is installed without vorbis support. 

Also, yeah gentoo is complicated. Actually I'm installing it to a vm,I was trying to see if I could reproduce your issue!

## Comment 3042176463

maintainer (COLLABORATOR) · Sephirex95 · 2025-07-06T16:26:19Z · https://github.com/Keriew/augustus/issues/1207#issuecomment-3042176463

Since this is deemed to be an SDL mixer quirk, can we close this issue?
