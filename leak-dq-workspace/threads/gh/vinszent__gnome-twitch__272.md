# Possible memory leak

- URL: https://github.com/vinszent/gnome-twitch/issues/272
- Repo: vinszent/gnome-twitch (language: C)
- State: open; created 2017-05-06T18:38:24Z; status ok; passes main

## Issue body

reporter (NONE) · mecjuszfufecjusz · 2017-05-06T18:38:24Z · https://github.com/vinszent/gnome-twitch/issues/272

I noticed that GT becomes a resource hog after a while, e.g. now, after few hours of watching/listening to streams (various channels, changing quality etc.), GT’s memory usage stands at 1453 MB. Fresh run and firing up a favourite channel uses ~165 MB. This is a regular behaviour.

GT version 0.4.0, Ubuntu 16.10 via webupd8.org PPA.

## Comment 300009206

maintainer (OWNER) · vinszent · 2017-05-08T22:30:19Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-300009206

I've been investigating this for a while and I'm pretty sure it's not from my code. From my own experiments it seems like the leak comes from the player backends. It's worse with higher resolution streams, i.e. source. Unfortunately the easiest thing to do, is to just restart GT until I can find a way to mitigate it.

## Comment 300013343

other (CONTRIBUTOR) · dengelt · 2017-05-08T22:53:32Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-300013343

I ran `gnome-twitch` with valgrind for a very short while and just browsed some menus (no player backend loaded), and these were the 10 biggest memory leaks according to valgrind:

```
==17459== 12,087 (24 direct, 12,063 indirect) bytes in 1 blocks are definitely lost in loss record 17,405 of 17,508
==17459==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==17459==    by 0x62A0E08: g_malloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B9342: g_slice_alloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B996D: g_slice_alloc0 (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6C813BA: json_array_new (json-array.c:59)
==17459==    by 0x6C8CC9F: json_parse_array (json-parser.c:508)
==17459==    by 0x6C8C97C: json_parse_object (json-parser.c:712)
==17459==    by 0x6C8D6AA: json_parser_load (json-parser.c:1013)
==17459==    by 0x6C8DC83: json_parser_load_from_data (json-parser.c:1169)
==17459==    by 0x11DE0B: new_send_message_json_with_version (gt-twitch.c:368)
==17459==    by 0x11DF16: new_send_message_json (gt-twitch.c:395)
==17459==    by 0x125F9D: fetch_followed_streams (gt-twitch.c:2052)
==17459== 
==17459== 16,384 bytes in 1 blocks are definitely lost in loss record 17,426 of 17,508
==17459==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==17459==    by 0x62A0E08: g_malloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62ABE7B: ??? (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x400F649: call_init.part.0 (dl-init.c:72)
==17459==    by 0x400F75A: call_init (dl-init.c:30)
==17459==    by 0x400F75A: _dl_init (dl-init.c:120)
==17459==    by 0x4000CD9: ??? (in /lib/x86_64-linux-gnu/ld-2.24.so)
==17459== 
==17459== 22,512 (2,048 direct, 20,464 indirect) bytes in 4 blocks are definitely lost in loss record 17,444 of 17,508
==17459==    at 0x4C2DDCF: realloc (vg_replace_malloc.c:785)
==17459==    by 0xC3D804A: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D8861: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D8B9F: FcPatternAddInteger (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xAD588E1: ??? (in /usr/lib/x86_64-linux-gnu/libcairo.so.2.11400.8)
==17459==    by 0xA07823F: ??? (in /usr/lib/x86_64-linux-gnu/libpangocairo-1.0.so.0.4000.5)
==17459==    by 0xBF62FC2: ??? (in /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0.4000.5)
==17459==    by 0xC185C19: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18709F: pango_itemize_with_base_dir (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18F308: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC191357: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0x5050CE9: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-3.so.0.2200.12)
==17459== 
==17459== 25,340 (8,448 direct, 16,892 indirect) bytes in 11 blocks are definitely lost in loss record 17,449 of 17,508
==17459==    at 0x4C2DDCF: realloc (vg_replace_malloc.c:785)
==17459==    by 0xC3D804A: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D8741: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D58D8: FcFontRenderPrepare (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D5C3F: FcFontMatch (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xBF63797: ??? (in /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0.4000.5)
==17459==    by 0xBF6396C: ??? (in /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0.4000.5)
==17459==    by 0xC1859C3: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC185EBC: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18709F: pango_itemize_with_base_dir (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18F308: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC191357: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459== 
==17459== 33,799 (3,072 direct, 30,727 indirect) bytes in 6 blocks are definitely lost in loss record 17,464 of 17,508
==17459==    at 0x4C2DDCF: realloc (vg_replace_malloc.c:785)
==17459==    by 0xC3D804A: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D8861: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D8B9F: FcPatternAddInteger (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xAD588E1: ??? (in /usr/lib/x86_64-linux-gnu/libcairo.so.2.11400.8)
==17459==    by 0xA07823F: ??? (in /usr/lib/x86_64-linux-gnu/libpangocairo-1.0.so.0.4000.5)
==17459==    by 0xBF62FC2: ??? (in /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0.4000.5)
==17459==    by 0xC185C19: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18709F: pango_itemize_with_base_dir (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18F308: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC191357: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0x4F82E07: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-3.so.0.2200.12)
==17459== 
==17459== 52,076 (32 direct, 52,044 indirect) bytes in 1 blocks are definitely lost in loss record 17,472 of 17,508
==17459==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==17459==    by 0x62A0E08: g_malloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B9342: g_slice_alloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B996D: g_slice_alloc0 (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6C88DDD: json_node_alloc (json-node.c:127)
==17459==    by 0x6C8C4D5: json_parse_value (json-parser.c:439)
==17459==    by 0x6C8C9A1: json_parse_object (json-parser.c:723)
==17459==    by 0x6C8CEC4: json_parse_array (json-parser.c:531)
==17459==    by 0x6C8C97C: json_parse_object (json-parser.c:712)
==17459==    by 0x6C8D6AA: json_parser_load (json-parser.c:1013)
==17459==    by 0x6C8DC83: json_parser_load_from_data (json-parser.c:1169)
==17459==    by 0x11DE0B: new_send_message_json_with_version (gt-twitch.c:368)
==17459== 
==17459== 58,087 (32 direct, 58,055 indirect) bytes in 1 blocks are definitely lost in loss record 17,473 of 17,508
==17459==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==17459==    by 0x62A0E08: g_malloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B9342: g_slice_alloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B996D: g_slice_alloc0 (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6C88DDD: json_node_alloc (json-node.c:127)
==17459==    by 0x6C8C42C: json_parse_value (json-parser.c:422)
==17459==    by 0x6C8C9A1: json_parse_object (json-parser.c:723)
==17459==    by 0x6C8C826: json_parse_object (json-parser.c:717)
==17459==    by 0x6C8CEC4: json_parse_array (json-parser.c:531)
==17459==    by 0x6C8C97C: json_parse_object (json-parser.c:712)
==17459==    by 0x6C8D6AA: json_parser_load (json-parser.c:1013)
==17459==    by 0x6C8DC83: json_parser_load_from_data (json-parser.c:1169)
==17459== 
==17459== 58,351 (64 direct, 58,287 indirect) bytes in 1 blocks are definitely lost in loss record 17,474 of 17,508
==17459==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==17459==    by 0x62A0E08: g_malloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62BAEE7: g_memdup (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6289641: ??? (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6289A79: ??? (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6C8C897: json_parse_object (json-parser.c:773)
==17459==    by 0x6C8D6AA: json_parser_load (json-parser.c:1013)
==17459==    by 0x6C8DC83: json_parser_load_from_data (json-parser.c:1169)
==17459==    by 0x11DE0B: new_send_message_json_with_version (gt-twitch.c:368)
==17459==    by 0x11DF16: new_send_message_json (gt-twitch.c:395)
==17459==    by 0x120BDD: gt_twitch_top_games (gt-twitch.c:867)
==17459==    by 0x1371BD: fetch_items (gt-top-game-container.c:70)
==17459== 
==17459== 180,049 (64 direct, 179,985 indirect) bytes in 2 blocks are definitely lost in loss record 17,487 of 17,508
==17459==    at 0x4C2BBAF: malloc (vg_replace_malloc.c:299)
==17459==    by 0x62A0E08: g_malloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B9342: g_slice_alloc (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x62B996D: g_slice_alloc0 (in /lib/x86_64-linux-gnu/libglib-2.0.so.0.5000.3)
==17459==    by 0x6C88DDD: json_node_alloc (json-node.c:127)
==17459==    by 0x6C8C4D5: json_parse_value (json-parser.c:439)
==17459==    by 0x6C8C9A1: json_parse_object (json-parser.c:723)
==17459==    by 0x6C8C826: json_parse_object (json-parser.c:717)
==17459==    by 0x6C8CEC4: json_parse_array (json-parser.c:531)
==17459==    by 0x6C8C97C: json_parse_object (json-parser.c:712)
==17459==    by 0x6C8D6AA: json_parser_load (json-parser.c:1013)
==17459==    by 0x6C8DC83: json_parser_load_from_data (json-parser.c:1169)
==17459== 
==17459== 237,142 (82,944 direct, 154,198 indirect) bytes in 108 blocks are definitely lost in loss record 17,491 of 17,508
==17459==    at 0x4C2DDCF: realloc (vg_replace_malloc.c:785)
==17459==    by 0xC3D804A: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D8741: ??? (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xC3D58D8: FcFontRenderPrepare (in /usr/lib/x86_64-linux-gnu/libfontconfig.so.1.8.0)
==17459==    by 0xBF635D8: ??? (in /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0.4000.5)
==17459==    by 0xBF6396C: ??? (in /usr/lib/x86_64-linux-gnu/libpangoft2-1.0.so.0.4000.5)
==17459==    by 0xC1859C3: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC185EBC: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18709F: pango_itemize_with_base_dir (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC18F308: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0xC191357: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4000.5)
==17459==    by 0x4F82E07: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-3.so.0.2200.12)
```

A lot of the stuff seems to be from libraries like gtk or pango or glib, but there's also some code from gnome-twitch there.

Unfortunately I didn't have the patience to run it in valgrind for a long time or play streams like this ;)

The full command I used is `valgrind --leak-check=full -v ./build/src/gnome-twitch`

## Comment 300016573

maintainer (OWNER) · vinszent · 2017-05-08T23:13:27Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-300016573

@dengelt Yes I've used Valgrind to do leak checking as well. Although there are leaks from my own code, they are pretty minor and aren't the cause of the leak that @mecjuszfufecjusz is talking about.

EDIT: I've also noticed other video players like Totem and MPV itself showing this kind of memory usage, when opening streams in them.

## Comment 300018864

other (CONTRIBUTOR) · TingPing · 2017-05-08T23:27:59Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-300018864

There is a valgrind file in glib (i believe it is installed) to ignore false positives and a few exist for gtk too.

## Comment 300029833

reporter (NONE) · mecjuszfufecjusz · 2017-05-09T00:45:12Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-300029833

I’ll just add that behaviour described by me was happening on Cairo backend, but I will try others as well.

## Comment 329983623

reporter (NONE) · mecjuszfufecjusz · 2017-09-16T17:35:37Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-329983623

Sorry for the silence. MPV seems to leak as well.

## Comment 340525115

maintainer (OWNER) · vinszent · 2017-10-30T17:40:25Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-340525115

So I've done some more investigating and I experimented with the GStreamer's own playback example ([here](https://github.com/GStreamer/gst-examples/tree/master/playback/player)). If I open and close a video/stream repeatedly, basically what GT does, the memory usage just increases. So I'm pretty sure this is an issue with GStreamer. However I've been unable to find out where it's leaking memory, both Valgrind and GStreamer's own debuggging tools say everything is fine... When I have time I'll try follow up with the GStreamer devs.

## Comment 377649995

other (NONE) · ptkato · 2018-03-31T00:10:21Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-377649995

Any news on this topic? Sometimes I notice that my memory usage is too high, when I go check, it's GT consuming like 2GB.

## Comment 378864795

maintainer (OWNER) · vinszent · 2018-04-05T08:49:28Z · https://github.com/vinszent/gnome-twitch/issues/272#issuecomment-378864795

Sorry, I haven't made much progress on this issue. I'm still certain it's not a bug in GT however as I can see this leak in many video apps on my system. I starting to suspect it might be a bug in libav (which has had its fair share of leaks in the past). Also I don't see this leak when playing any other codec, e.g. VP9, with the exact same GStreamer pipeline.
