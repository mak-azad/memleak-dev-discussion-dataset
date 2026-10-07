# free(): invalid pointer

- URL: https://github.com/EionRobb/purple-discord/issues/402
- Repo: EionRobb/purple-discord (language: C)
- State: open; created 2022-04-05T20:41:07Z; status ok; passes main

## Issue body

reporter (NONE) · bodqhrohro · 2022-04-05T20:41:07Z · https://github.com/EionRobb/purple-discord/issues/402

```
(21:53:18) log: Failed to open log file "/home/bodqhrohro/.purple/logs/800376413022453793.log" for reading: Нет такого файла или каталога
(21:53:18) Gtk: IA__gtk_widget_hide: assertion 'GTK_IS_WIDGET (widget)' failed
(21:53:18) g_log: purple_strreplace: assertion 'string != NULL' failed
(21:53:18) g_log: purple_strreplace: assertion 'string != NULL' failed
(21:53:18) LaTeX: Writing Message: И главное джойстик как не странно норм.
(21:53:18) GLib: Source ID 202 was not found when attempting to remove it
(21:53:18) GLib: Source ID 3518746814 was not found when attempting to remove it
(21:53:18) GLib: g_hash_table_remove_internal: assertion 'hash_table != NULL' failed
free(): invalid pointer
@--Type <RET> for more, q to quit, c to continue without paging--dns[2214270]: nobody needs me... =(
dns[2214271]: nobody needs me... =(
dns[2214272]: nobody needs me... =(
bt

Thread 1 "pidgin" received signal SIGABRT, Aborted.
__GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:49
49	../sysdeps/unix/sysv/linux/raise.c: Нет такого файла или каталога.
@(gdb) bt
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:49
#1  0x00007ffff6d0c536 in __GI_abort () at abort.c:79
#2  0x00007ffff6d63e88 in __libc_message (action=action@entry=do_abort, fmt=fmt@entry=0x7ffff6e715f9 "%s\n") at ../sysdeps/posix/libc_fatal.c:155
#3  0x00007ffff6d6b8ea in malloc_printerr (str=str@entry=0x7ffff6e6f82e "free(): invalid pointer") at malloc.c:5628
#4  0x00007ffff6d6ccc4 in _int_free (av=<optimized out>, p=<optimized out>, have_lock=0) at malloc.c:4398
#5  0x00007ffff6d70984 in __GI___libc_free (mem=<optimized out>) at malloc.c:3309
#6  0x00007ffff72faef5 in g_free (mem=<optimized out>) at ../../../glib/gmem.c:199
#7  0x00007ffff0cfa275 in purple_http_url_free (parsed_url=0x555555cf3620) at purple2compat/http.c:3042
#8  purple_http_url_free (parsed_url=0x555555cf3620) at purple2compat/http.c:3033
#9  0x00007ffff0cfa341 in purple_http_connection_free (hc=0x5555576a9700) at purple2compat/http.c:1689
#10 purple_http_connection_terminate (hc=hc@entry=0x5555576a9700) at purple2compat/http.c:1732
#11 0x00007ffff0cfc238 in _purple_http_recv_loopbody (hc=hc@entry=0x5555576a9700, fd=<optimized out>) at purple2compat/http.c:1298
#12 0x00007ffff0cfc8f0 in _purple_http_recv (_hc=0x5555576a9700, fd=<optimized out>, cond=cond@entry=PURPLE_INPUT_READ) at purple2compat/http.c:1309
#13 0x00005555555cdfb2 in pidgin_io_invoke (source=<optimized out>, condition=<optimized out>, data=0x555557c3bf30) at ././pidgin/gtkeventloop.c:73
#14 0x00007ffff72f4be4 in g_main_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:3381
#15 g_main_context_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:4099
#16 0x00007ffff72f4f88 in g_main_context_iterate (context=0x5555556c8b10, block=block@entry=1, dispatch=dispatch@entry=1, self=<optimized out>)
    at ../../../glib/gmain.c:4175
#17 0x00007ffff72f5273 in g_main_loop_run (loop=0x5555574ffd50) at ../../../glib/gmain.c:4373
@--Type <RET> for more, q to quit, c to continue without paging--
#18 0x00007ffff79d7b2a in gtk_main () at /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0
#19 0x0000555555591d70 in main (argc=<optimized out>, argv=<optimized out>) at ././pidgin/gtkmain.c:947
@(gdb) bt full
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:49
        set = 
            {__val = {0, 140737488331376, 140737488331168, 15235366891903932160, 140737488331184, 93825009935840, 93825001761696, 93825025511984, 7, 93825027028816, 7, 93825009935840, 93824992702880, 140737334675844, 8, 15235366891903932160}}
        pid = <optimized out>
        tid = <optimized out>
#1  0x00007ffff6d0c536 in __GI_abort () at abort.c:79
        save_stage = 1
        act = 
          {__sigaction_handler = {sa_handler = 0x555555e6aba0, sa_sigaction = 0x555555e6aba0}, sa_mask = {__val = {18446744073709551496, 0, 15235366891903932160, 5, 18446744073709551496, 0, 8, 93824998683552, 140737340805134, 140737341373632, 140737340800079, 93825001761696, 93824992703002, 8, 8, 0}}, sa_flags = -147864346, sa_restorer = 0x555555e6aba0}
        sigs = 
            {__val = {32, 140737337856323, 206158430240, 140737488331664, 140737488331472, 15235366891903932160, 18446744073709551615, 0, 206158430240, 93825033015552, 93825001761696, 140737335409888, 18446744073709551615, 140737335940448, 140737334674112, 15235366891903932160}}
#2  0x00007ffff6d63e88 in __libc_message (action=action@entry=do_abort, fmt=fmt@entry=0x7ffff6e715f9 "%s\n") at ../sysdeps/posix/libc_fatal.c:155
        ap = {{gp_offset = 24, fp_offset = 21845, overflow_arg_area = 0x7fffffffa4e0, reg_save_area = 0x7fffffffa470}}
        fd = <optimized out>
        list = <optimized out>
@--Type <RET> for more, q to quit, c to continue without paging--
        nlist = <optimized out>
        cp = <optimized out>
#3  0x00007ffff6d6b8ea in malloc_printerr (str=str@entry=0x7ffff6e6f82e "free(): invalid pointer") at malloc.c:5628
#4  0x00007ffff6d6ccc4 in _int_free (av=<optimized out>, p=<optimized out>, have_lock=0) at malloc.c:4398
        size = 0
        fb = <optimized out>
        nextchunk = <optimized out>
        nextsize = <optimized out>
        nextinuse = <optimized out>
        prevsize = <optimized out>
        bck = <optimized out>
        fwd = <optimized out>
        __PRETTY_FUNCTION__ = "_int_free"
#5  0x00007ffff6d70984 in __GI___libc_free (mem=<optimized out>) at malloc.c:3309
        ar_ptr = <optimized out>
        p = <optimized out>
        hook = <optimized out>
        err = 0
#6  0x00007ffff72faef5 in g_free (mem=<optimized out>) at ../../../glib/gmem.c:199
@--Type <RET> for more, q to quit, c to continue without paging--
#7  0x00007ffff0cfa275 in purple_http_url_free (parsed_url=0x555555cf3620) at purple2compat/http.c:3042
#8  purple_http_url_free (parsed_url=0x555555cf3620) at purple2compat/http.c:3033
#9  0x00007ffff0cfa341 in purple_http_connection_free (hc=0x5555576a9700) at purple2compat/http.c:1689
        __func__ = "purple_http_connection_free"
        __func__ = "purple_http_connection_terminate"
#10 purple_http_connection_terminate (hc=hc@entry=0x5555576a9700) at purple2compat/http.c:1732
        __func__ = "purple_http_connection_terminate"
#11 0x00007ffff0cfc238 in _purple_http_recv_loopbody (hc=hc@entry=0x5555576a9700, fd=<optimized out>) at purple2compat/http.c:1298
        redirect = <optimized out>
        len = <optimized out>
        buf = "0\r\n\r\n\244UM#Gn\376\066-!\377\366\212VT\b\302yx(f%\023,Ҷ\325,N\216\321/$\vW\350b)L\322ߥ\227Q\217\252\032COt\245\b\301\234\063\245\025\357\070P\002}]*Itdk\273\252Ŏ\326I\237\232\"\374\032c\336\272\301\252\266\037\344\317\032\357\344\031K{/\325m\f\367\022C\227k\b\231\261\063\372\070Ŕ\235\334\377s\273L\203\071\202\263\r\036\304\315z9\254&c\231\273Y\036\223\063YʧN\307Ɏf\365r\234\343\240$\270v\006v\206\362\v\213\006XCX\201\061\a\200\017\200\006 .a\264\365F\267\271\316m\303\020\062\307^\351_\033\347\320\366\275\325\363\372\a\207\201\225ާ\002\000\000"...
        got_anything = <optimized out>
#12 0x00007ffff0cfc8f0 in _purple_http_recv (_hc=0x5555576a9700, fd=<optimized out>, cond=cond@entry=PURPLE_INPUT_READ) at purple2compat/http.c:1309
        hc = 0x5555576a9700
#13 0x00005555555cdfb2 in pidgin_io_invoke (source=<optimized out>, condition=<optimized out>, data=0x555557c3bf30) at ././pidgin/gtkeventloop.c:73
        closure = 0x555557c3bf30
@--Type <RET> for more, q to quit, c to continue without paging--
        purple_cond = PURPLE_INPUT_READ
#14 0x00007ffff72f4be4 in g_main_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:3381
        dispatch = 0x7ffff7346ef0 <g_io_unix_dispatch>
        prev_source = 0x0
        begin_time_nsec = 0
        was_in_call = 0
        user_data = 0x555557c3bf30
        callback = 0x5555555cdf80 <pidgin_io_invoke>
        cb_funcs = <optimized out>
        cb_data = <optimized out>
        need_destroy = <optimized out>
        source = 0x555557a3e470
        current = 0x55555644c7f0
        i = 6
        __func__ = "g_main_dispatch"
#15 g_main_context_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:4099
#16 0x00007ffff72f4f88 in g_main_context_iterate (context=0x5555556c8b10, block=block@entry=1, dispatch=dispatch@entry=1, self=<optimized out>)
    at ../../../glib/gmain.c:4175
        max_priority = 0
@--Type <RET> for more, q to quit, c to continue without paging--
        timeout = 0
        some_ready = 1
        nfds = <optimized out>
        allocated_nfds = <optimized out>
        fds = 0x5555557a8cc0
#17 0x00007ffff72f5273 in g_main_loop_run (loop=0x5555574ffd50) at ../../../glib/gmain.c:4373
        __func__ = "g_main_loop_run"
#18 0x00007ffff79d7b2a in gtk_main () at /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0
#19 0x0000555555591d70 in main (argc=<optimized out>, argv=<optimized out>) at ././pidgin/gtkmain.c:947
        opt_force_online = 0
        opt_help = <optimized out>
        opt_login = 0
        opt_nologin = 0
        opt_version = <optimized out>
        opt_si = <optimized out>
        opt_config_dir_arg = <optimized out>
        opt_login_arg = <optimized out>
        opt_session_arg = <optimized out>
        search_path = <optimized out>
@--Type <RET> for more, q to quit, c to continue without paging--
        accounts = <optimized out>
        sig_indx = 1
        sigset = {__val = {91142, 0 <repeats 15 times>}}
        errmsg = '\000' <repeats 1208 times>...
        signal_channel = <optimized out>
        signal_status = <optimized out>
        signal_channel_watcher = 1
        segfault_message_tmp = <optimized out>
        error = 0x0
        opt = <optimized out>
        gui_check = <optimized out>
        debug_enabled = 1
        migration_failed = 0
        active_accounts = <optimized out>
        long_options = 
            {{name = 0x5555556382b7 "config", has_arg = 1, flag = 0x0, val = 99}, {name = 0x555555625f79 "debug", has_arg = 0, flag = 0x0, val = 100}, {name = 0x555555633be6 "force-online", has_arg = 0, flag = 0x0, val = 102}, {name = 0x555555627aec "help", has_arg = 0, flag = 0x0, val = 104}, {name = 0x555555633a92 "login", has_arg = 2, flag = 0x0, val = 108}, {name = 0x555555633bf3 "multiple", has_arg = 0, flag = 0x0, val = 109}, {name = 0x555555633bfc "nologin", has_arg = 0, flag = 0x0, val = 110}, {name = 0x5555556382ca "session", has_arg = 1, flag = 0x0, val = 115}, {name = 0x55555562a283@--Type <RET> for more, q to quit, c to continue without paging--
 "version", has_arg = 0, flag = 0x0, val = 118}, {name = 0x5555556382c0 "display", has_arg = 1, flag = 0x0, val = 68}, {name = 0x55555563454b "sync", has_arg = 0, flag = 0x0, val = 83}, {name = 0x0, has_arg = 0, flag = 0x0, val = 0}}
```

## Comment 1091866354

reporter (NONE) · bodqhrohro · 2022-04-07T15:15:44Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1091866354

Just while Pidgin was starting:
```
(17:44:37) discord: sending frame: {"op":1,"d":8}
(17:44:37) prpl-telegram: ping alarm
(17:44:38) util: Writing file accounts.xml to directory /home/bodqhrohro/.purple
(17:44:38) util: Writing file /home/bodqhrohro/.purple/accounts.xml
(17:44:38) discord: got frame data: {"t":null,"s":null,"op":11,"d":null}
(17:44:38) log: Failed to open log file "/home/bodqhrohro/.purple/logs/800376413022453793.log" for reading: Нет такого файла или каталога
(17:44:38) Gtk: IA__gtk_widget_hide: assertion 'GTK_IS_WIDGET (widget)' failed
(17:44:38) g_log: purple_strreplace: assertion 'string != NULL' failed
(17:44:38) g_log: purple_strreplace: assertion 'string != NULL' failed
(17:44:38) LaTeX: Writing Message: А, не, драма совсем свеженькая https://vk.com/wall-36741297_780776<br/><font back="#ffffff" color="#ffffff"> </font> https://vk.com/wall-36741297_780776<br/><font back="#ffffff" color="#ffffff"> </font> Форум Allnokia вычищен полностью придурком модератором, не осталось ни одного обсуждения...<br/><font back="#ffffff" color="#ffffff"> </font> Чт 07 апр 2022 17:43:56<br/>
(17:44:39) GLib: Source ID 32 was not found when attempting to remove it
(17:44:39) GLib: Source ID 145 was not found when attempting to remove it
@--Type <RET> for more, q to quit, c to continue without paging--

Thread 1 "pidgin" received signal SIGSEGV, Segmentation fault.
purple_http_connection_free (hc=0x555555e21100) at purple2compat/http.c:1687
1687			purple_http_connection_set_remove(hc->connection_set, hc);
@(gdb) bt
#0  purple_http_connection_free (hc=0x555555e21100) at purple2compat/http.c:1687
#1  purple_http_connection_terminate (hc=hc@entry=0x555555e21100) at purple2compat/http.c:1732
#2  0x00007ffff0cfc238 in _purple_http_recv_loopbody (hc=hc@entry=0x555555e21100, fd=<optimized out>) at purple2compat/http.c:1298
#3  0x00007ffff0cfc8f0 in _purple_http_recv (_hc=0x555555e21100, fd=<optimized out>, cond=cond@entry=PURPLE_INPUT_READ) at purple2compat/http.c:1309
#4  0x00005555555cdfb2 in pidgin_io_invoke (source=<optimized out>, condition=<optimized out>, data=0x5555578fdb90) at ././pidgin/gtkeventloop.c:73
#5  0x00007ffff72f4be4 in g_main_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:3381
#6  g_main_context_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:4099
#7  0x00007ffff72f4f88 in g_main_context_iterate (context=0x5555556c8b10, block=block@entry=1, dispatch=dispatch@entry=1, self=<optimized out>)
    at ../../../glib/gmain.c:4175
#8  0x00007ffff72f5273 in g_main_loop_run (loop=0x555556a84b30) at ../../../glib/gmain.c:4373
#9  0x00007ffff79d7b2a in gtk_main () at /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0
#10 0x0000555555591d70 in main (argc=<optimized out>, argv=<optimized out>) at ././pidgin/gtkmain.c:947
@(gdb) p
$4 = {account = 0x55555f710370, pc = 0x0, cookie_jar = 0x0, refresh_token = 0x5555568ba990 "", access_token = 0x555557eb35a0 "", 
  id_token = 0x55555fd47f30 <error: Cannot access memory at address 0x55555fd47f30>, 
  csessionid_param = 0x55555f70fe40 <error: Cannot access memory at address 0x55555f70fe40>, 
  sid_param = 0x55555f710350 <error: Cannot access memory at address 0x55555f710350>, 
  client_id = 0x55555faeab60 <error: Cannot access memory at address 0x55555faeab60>, self_gaia_id = 0x5555576c5de0 "", self_phone = 0x0, 
  last_event_timestamp = 0, last_conversation_focused = 0x0, poll_buddy_status_timeout = 0, server_time_offset = 0, last_aid = 0, last_ofs = 0, 
  channel_buffer = 0x0, channel_watchdog = 0, channel_connection = 0x0, channel_keepalive_pool = 0x41, icons_keepalive_pool = 0x5550027b3d44, 
  api_keepalive_pool = 0x726f747561202937, idle_time = 1852793701, active_client_timeout = 1633886266, last_data_received = 1852402796, 
  one_to_ones = <error reading variable: Cannot access memory at address 0x6363615f656c70aa>0x6363615f656c7072, 
  one_to_ones_rev = <error reading variable: Cannot access memory at address 0x6e6f635f746e75a7>0x6e6f635f746e756f, 
  group_chats = <error reading variable: Cannot access memory at address 0xa746365a6>0xa7463656e, 
  sent_message_ids = <error reading variable: Cannot access memory at address 0x69>0x31, refresh_token_timeout = 0, dynamite_token_timeout = 0}
@(gdb) p hc
$5 = (PurpleHttpConnection *) 0x555555e21100
@(gdb) p *hc
$6 = {gc = 0x555557ba8cf0, callback = 0x7ffff6ea3ef0 <main_arena+848>, user_data = 0x900000139, is_reading = 436, is_keepalive = 26, 
  is_cancelling = 462, url = 0x1a000004c0, request = 0x1a000001ce, response = 0x29000004c0, socket_request = 0x50, 
  connection_set = 0x68632e3339373335, socket = 0x2d313230322f7461, request_header = 0x39312e35302d3131, request_header_written = 942813492, 
  request_contents_written = 808595499, main_header_got = 1413825840, headers_got = 1836345390, response_buffer = 0x120000006c, 
  gz_stream = 0xffffffff00000011, contents_reader_buffer = 0x90, contents_reader_requested = 625, redirects_count = 0, length_expected = -152420768, 
  length_got = 32767, length_got_decompressed = 4142546528, is_chunked = 32767, in_chunk = 32, chunks_done = 0, chunk_length = 209, chunk_got = 0, 
  link_global = 0x555557bb4a90 = {0xab0d0, <error reading variable>
@(gdb) 
```

## Comment 1098200106

reporter (NONE) · bodqhrohro · 2022-04-13T15:36:08Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1098200106

```
==1569469== 1 errors in context 1 of 9:
==1569469== Invalid read of size 8
==1569469==    at 0xC3371B1: purple_http_connection_set_remove (http.c:2470)
==1569469==    by 0xC3371B1: purple_http_connection_free (http.c:1687)
==1569469==    by 0xC3371B1: purple_http_connection_terminate (http.c:1732)
==1569469==    by 0xC3390C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==1569469==    by 0xC33977F: _purple_http_recv (http.c:1309)
==1569469==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==1569469==    by 0x548FBE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x548FF87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x5490272: g_main_loop_run (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x4C48B29: gtk_main (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==    by 0x145D6F: main (in /usr/bin/pidgin)
==1569469==  Address 0x71fac8b150bfb66b is not stack'd, malloc'd or (recently) free'd
==1569469== 
==1569469== 
==1569469== 1 errors in context 2 of 9:
==1569469== Invalid read of size 4
==1569469==    at 0xC337335: purple_http_connection_free (http.c:1682)
==1569469==    by 0xC337335: purple_http_connection_terminate (http.c:1732)
==1569469==    by 0xC3390C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==1569469==    by 0xC33977F: _purple_http_recv (http.c:1309)
==1569469==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==1569469==    by 0x548FBE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x548FF87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x5490272: g_main_loop_run (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x4C48B29: gtk_main (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==    by 0x145D6F: main (in /usr/bin/pidgin)
==1569469==  Address 0x93317f8 is 6 bytes after a block of size 226 alloc'd
==1569469==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==1569469==    by 0xC4F13FD: PORT_Alloc_Util (in /usr/lib/x86_64-linux-gnu/libnssutil3.so)
==1569469==    by 0xC4EFC37: SECITEM_CopyItem_Util (in /usr/lib/x86_64-linux-gnu/libnssutil3.so)
==1569469==    by 0x108F00C3: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108CD91E: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108D1664: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108D1EF8: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108D7F78: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108D86D3: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108DFDD9: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x108E46B5: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==1569469==    by 0x1087E792: ssl_nss_read (in /usr/lib/purple-2/ssl-nss.so)
==1569469== 
==1569469== 
==1569469== 1 errors in context 3 of 9:
==1569469== Invalid free() / delete / delete[] / realloc()
==1569469==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==1569469==    by 0xC31A83A: discord_response_callback (libdiscord.c:1446)
==1569469==    by 0xC33718B: purple_http_connection_terminate (http.c:1730)
==1569469==    by 0xC3390C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==1569469==    by 0xC33977F: _purple_http_recv (http.c:1309)
==1569469==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==1569469==    by 0x548FBE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x548FF87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x5490272: g_main_loop_run (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x4C48B29: gtk_main (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==    by 0x145D6F: main (in /usr/bin/pidgin)
==1569469==  Address 0xe055900 is 208 bytes inside a block of size 320 free'd
==1569469==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==1569469==    by 0x51C4E21: pango_glyph_string_free (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51CF6B9: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x54AF937: g_slist_foreach (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x51CFF74: pango_layout_line_unref (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51CFFCA: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51D1F83: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x53FB7C5: g_object_unref (in /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0.7000.2)
==1569469==    by 0x4BB1BA9: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==    by 0x4D5C605: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==    by 0x4D5CEF4: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==    by 0x4D4737C: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==1569469==  Block was alloc'd at
==1569469==    at 0x483E6AF: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==1569469==    by 0x4840DE7: realloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==1569469==    by 0x5495EB7: g_realloc (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==1569469==    by 0x51C4ED3: pango_glyph_string_set_size (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51E0BD4: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51DFFEE: pango_shape_with_flags (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51D0B3F: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51D1E19: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51D409D: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51D6861: ??? (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x51DDD26: pango_renderer_draw_layout (in /usr/lib/x86_64-linux-gnu/libpango-1.0.so.0.4800.10)
==1569469==    by 0x4F9D769: gdk_draw_layout_with_colors (in /usr/lib/x86_64-linux-gnu/libgdk-x11-2.0.so.0.2400.33)
```

## Comment 1099616477

reporter (NONE) · bodqhrohro · 2022-04-14T20:59:45Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1099616477

According to this and https://github.com/majn/telegram-purple/issues/580#issuecomment-1099595713, seems like this memory corruption happens in Pango, huh? I'll try to upgrade it from 1.48 to 1.50 first, if the reason is not its improper usage.

## Comment 1099720849

reporter (NONE) · bodqhrohro · 2022-04-14T23:37:32Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1099720849

```
(01:00:48) log: Failed to open log file "/home/bodqhrohro/.purple/logs/800376413022453793.log" for reading: Нет такого файла или каталога
(01:00:51) Gtk: IA__gtk_widget_hide: assertion 'GTK_IS_WIDGET (widget)' failed
(01:00:51) g_log: purple_strreplace: assertion 'string != NULL' failed
(01:00:51) g_log: purple_strreplace: assertion 'string != NULL' failed
(01:00:52) LaTeX: Writing Message: Возможно и можно.
```

```
==2120401== 1 errors in context 1 of 14:
==2120401== Invalid read of size 8
==2120401==    at 0xC34B1DE: purple_http_response_free (http.c:2806)
==2120401==    by 0xC34B1DE: purple_http_connection_free (http.c:1691)
==2120401==    by 0xC34B1DE: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x10 is not stack'd, malloc'd or (recently) free'd
==2120401== 
==2120401== 
==2120401== 1 errors in context 2 of 14:
==2120401== Invalid read of size 8
==2120401==    at 0xC34B1DA: purple_http_connection_free (http.c:1691)
==2120401==    by 0xC34B1DA: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19e16218 is 2,200 bytes inside a block of size 2,560 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D29DC: combine_clip_as_traps (cairo-traps-compositor.c:219)
==2120401==    by 0x50D29DC: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401==    by 0x50D9FB9: cairo_stroke (cairo.c:2367)
==2120401==    by 0xA91079A: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA926CDC: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==  Block was alloc'd at
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D5329: _cairo_traps_grow (cairo-traps.c:132)
==2120401==    by 0x50D573E: _cairo_traps_add_trap (cairo-traps.c:163)
==2120401==    by 0x506ECCD: _cairo_bo_edge_end_trap (cairo-bentley-ottmann.c:1157)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_bo_edges (cairo-bentley-ottmann.c:1450)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_polygon (cairo-bentley-ottmann.c:1557)
==2120401==    by 0x50D2922: combine_clip_as_traps (cairo-traps-compositor.c:196)
==2120401==    by 0x50D2922: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401== 
==2120401== 
==2120401== 1 errors in context 3 of 14:
==2120401== Invalid read of size 8
==2120401==    at 0xC34B1D1: purple_http_connection_free (http.c:1690)
==2120401==    by 0xC34B1D1: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19e16210 is 2,192 bytes inside a block of size 2,560 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D29DC: combine_clip_as_traps (cairo-traps-compositor.c:219)
==2120401==    by 0x50D29DC: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401==    by 0x50D9FB9: cairo_stroke (cairo.c:2367)
==2120401==    by 0xA91079A: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA926CDC: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==  Block was alloc'd at
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D5329: _cairo_traps_grow (cairo-traps.c:132)
==2120401==    by 0x50D573E: _cairo_traps_add_trap (cairo-traps.c:163)
==2120401==    by 0x506ECCD: _cairo_bo_edge_end_trap (cairo-bentley-ottmann.c:1157)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_bo_edges (cairo-bentley-ottmann.c:1450)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_polygon (cairo-bentley-ottmann.c:1557)
==2120401==    by 0x50D2922: combine_clip_as_traps (cairo-traps-compositor.c:196)
==2120401==    by 0x50D2922: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401== 
==2120401== 
==2120401== 1 errors in context 4 of 14:
==2120401== Invalid read of size 8
==2120401==    at 0xC34B1C8: purple_http_connection_free (http.c:1689)
==2120401==    by 0xC34B1C8: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19e16208 is 2,184 bytes inside a block of size 2,560 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D29DC: combine_clip_as_traps (cairo-traps-compositor.c:219)
==2120401==    by 0x50D29DC: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401==    by 0x50D9FB9: cairo_stroke (cairo.c:2367)
==2120401==    by 0xA91079A: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA926CDC: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==  Block was alloc'd at
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D5329: _cairo_traps_grow (cairo-traps.c:132)
==2120401==    by 0x50D573E: _cairo_traps_add_trap (cairo-traps.c:163)
==2120401==    by 0x506ECCD: _cairo_bo_edge_end_trap (cairo-bentley-ottmann.c:1157)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_bo_edges (cairo-bentley-ottmann.c:1450)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_polygon (cairo-bentley-ottmann.c:1557)
==2120401==    by 0x50D2922: combine_clip_as_traps (cairo-traps-compositor.c:196)
==2120401==    by 0x50D2922: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401== 
==2120401== 
==2120401== 1 errors in context 5 of 14:
==2120401== Invalid read of size 8
==2120401==    at 0xC34B1A8: purple_http_connection_free (http.c:1686)
==2120401==    by 0xC34B1A8: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19e16228 is 2,216 bytes inside a block of size 2,560 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D29DC: combine_clip_as_traps (cairo-traps-compositor.c:219)
==2120401==    by 0x50D29DC: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401==    by 0x50D9FB9: cairo_stroke (cairo.c:2367)
==2120401==    by 0xA91079A: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA926CDC: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==  Block was alloc'd at
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D5329: _cairo_traps_grow (cairo-traps.c:132)
==2120401==    by 0x50D573E: _cairo_traps_add_trap (cairo-traps.c:163)
==2120401==    by 0x506ECCD: _cairo_bo_edge_end_trap (cairo-bentley-ottmann.c:1157)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_bo_edges (cairo-bentley-ottmann.c:1450)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_polygon (cairo-bentley-ottmann.c:1557)
==2120401==    by 0x50D2922: combine_clip_as_traps (cairo-traps-compositor.c:196)
==2120401==    by 0x50D2922: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401== 
==2120401== 
==2120401== 1 errors in context 6 of 14:
==2120401== Invalid read of size 4
==2120401==    at 0xC34B19A: purple_http_connection_free (http.c:1683)
==2120401==    by 0xC34B19A: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19e162c8 is 2,376 bytes inside a block of size 2,560 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D29DC: combine_clip_as_traps (cairo-traps-compositor.c:219)
==2120401==    by 0x50D29DC: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401==    by 0x50D9FB9: cairo_stroke (cairo.c:2367)
==2120401==    by 0xA91079A: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA926CDC: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==  Block was alloc'd at
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D5329: _cairo_traps_grow (cairo-traps.c:132)
==2120401==    by 0x50D573E: _cairo_traps_add_trap (cairo-traps.c:163)
==2120401==    by 0x506ECCD: _cairo_bo_edge_end_trap (cairo-bentley-ottmann.c:1157)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_bo_edges (cairo-bentley-ottmann.c:1450)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_polygon (cairo-bentley-ottmann.c:1557)
==2120401==    by 0x50D2922: combine_clip_as_traps (cairo-traps-compositor.c:196)
==2120401==    by 0x50D2922: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401== 
==2120401== 
==2120401== 1 errors in context 7 of 14:
==2120401== Invalid read of size 4
==2120401==    at 0xC34B18C: purple_http_connection_free (http.c:1681)
==2120401==    by 0xC34B18C: purple_http_connection_terminate (http.c:1732)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x57619AD: purple_signal_emit (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x572A6DB: purple_conversation_new (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19e162a0 is 2,336 bytes inside a block of size 2,560 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D29DC: combine_clip_as_traps (cairo-traps-compositor.c:219)
==2120401==    by 0x50D29DC: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401==    by 0x50D9FB9: cairo_stroke (cairo.c:2367)
==2120401==    by 0xA91079A: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA926CDC: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==  Block was alloc'd at
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x50D5329: _cairo_traps_grow (cairo-traps.c:132)
==2120401==    by 0x50D573E: _cairo_traps_add_trap (cairo-traps.c:163)
==2120401==    by 0x506ECCD: _cairo_bo_edge_end_trap (cairo-bentley-ottmann.c:1157)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_bo_edges (cairo-bentley-ottmann.c:1450)
==2120401==    by 0x506ECCD: _cairo_bentley_ottmann_tessellate_polygon (cairo-bentley-ottmann.c:1557)
==2120401==    by 0x50D2922: combine_clip_as_traps (cairo-traps-compositor.c:196)
==2120401==    by 0x50D2922: create_composite_mask (cairo-traps-compositor.c:499)
==2120401==    by 0x50D3807: clip_and_composite_with_mask (cairo-traps-compositor.c:548)
==2120401==    by 0x50D3807: clip_and_composite (cairo-traps-compositor.c:1039)
==2120401==    by 0x50D5003: clip_and_composite_traps (cairo-traps-compositor.c:1845)
==2120401==    by 0x50D5003: _cairo_traps_compositor_stroke (cairo-traps-compositor.c:2203)
==2120401==    by 0x507B30E: _cairo_compositor_stroke (cairo-compositor.c:157)
==2120401==    by 0x50F7619: _cairo_xlib_surface_stroke (cairo-xlib-surface.c:1619)
==2120401==    by 0x50CC6B5: _cairo_surface_stroke (cairo-surface.c:2377)
==2120401==    by 0x5083953: _cairo_gstate_stroke (cairo-gstate.c:1188)
==2120401==    by 0x507CE59: _cairo_default_context_stroke (cairo-default-context.c:1010)
==2120401== 
==2120401== 
==2120401== 1 errors in context 8 of 14:
==2120401== Invalid free() / delete / delete[] / realloc()
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0xC32E83A: discord_response_callback (libdiscord.c:1446)
==2120401==    by 0xC34B18B: purple_http_connection_terminate (http.c:1730)
==2120401==    by 0xC34D0C7: _purple_http_recv_loopbody.constprop.0 (http.c:1298)
==2120401==    by 0xC34D77F: _purple_http_recv (http.c:1309)
==2120401==    by 0x181FB1: pidgin_io_invoke (in /usr/bin/pidgin)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==    by 0x576181B: purple_signal_emit_vargs (in /usr/lib/libpurple.so.0.14.8)
==2120401==  Address 0x19d3efe0 is 64 bytes inside a block of size 88 free'd
==2120401==    at 0x483F9AB: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x577E764: xmlnode_free (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x577E764: xmlnode_free (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x577E764: xmlnode_free (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x577E764: xmlnode_free (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x5713268: save_cb (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x54A4743: g_timeout_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0xBA51654: conversation_created_cb (plugin.c:91)
==2120401==  Block was alloc'd at
==2120401==    at 0x4840B65: calloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x54A9E70: g_malloc0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x577EA39: xmlnode_set_attrib_full (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x570F611: setting_to_xmlnode (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x5491BAF: g_hash_table_foreach (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x5713143: sync_accounts (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x5713268: save_cb (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x54A4743: g_timeout_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3BE3: g_main_context_dispatch (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A3F87: g_main_context_iterate.constprop.0 (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x54A403E: g_main_context_iteration (in /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0.7000.2)
==2120401==    by 0x4C48D90: gtk_main_iteration (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401== 
==2120401== 
==2120401== 2 errors in context 9 of 14:
==2120401== Syscall param socketcall.sendto(msg) points to uninitialised byte(s)
==2120401==    at 0x5967554: __libc_send (send.c:28)
==2120401==    by 0x5967554: send (send.c:23)
==2120401==    by 0xC5472B7: ??? (in /usr/lib/x86_64-linux-gnu/libnspr4.so)
==2120401==    by 0x100EE9B7: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100F3320: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D7529: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D791C: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E01E4: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E0779: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E267A: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E5664: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E5EF8: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100EBF78: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==  Address 0x92f3196 is 86 bytes inside a block of size 1,105 alloc'd
==2120401==    at 0x4840D7B: realloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0xC505481: PORT_Realloc_Util (in /usr/lib/x86_64-linux-gnu/libnssutil3.so)
==2120401==    by 0x100EEBA4: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100EED8B: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D7507: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D791C: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E01E4: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E0779: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E267A: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E5664: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100E5EF8: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100EBF78: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401== 
==2120401== 
==2120401== 255 errors in context 10 of 14:
==2120401== Conditional jump or move depends on uninitialised value(s)
==2120401==    at 0x4844E5E: __memcmp_sse4_1 (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x1A419B11: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41D1B6: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41F45A: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A3DC791: ??? (in /usr/lib/x86_64-linux-gnu/libsoftokn3.so)
==2120401==    by 0xC3D15F1: PK11_AEADRawOp (in /usr/lib/x86_64-linux-gnu/libnss3.so)
==2120401==    by 0xC3D1BBF: PK11_AEADOp (in /usr/lib/x86_64-linux-gnu/libnss3.so)
==2120401==    by 0x10105BFA: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D6CD0: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D711F: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D72C3: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D7447: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401== 
==2120401== 
==2120401== 276 errors in context 11 of 14:
==2120401== Syscall param socketcall.sendto(msg) points to uninitialised byte(s)
==2120401==    at 0x5967554: __libc_send (send.c:28)
==2120401==    by 0x5967554: send (send.c:23)
==2120401==    by 0xC5472B7: ??? (in /usr/lib/x86_64-linux-gnu/libnspr4.so)
==2120401==    by 0x100EE9B7: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D756E: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D773C: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100F40DA: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100F8765: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x10092752: ssl_nss_write (in /usr/lib/purple-2/ssl-nss.so)
==2120401==    by 0x168AC5BA: do_jabber_send_raw (in /usr/lib/purple-2/libjabber.so.0.0.0)
==2120401==    by 0x168ACAEA: jabber_send_raw (in /usr/lib/purple-2/libjabber.so.0.0.0)
==2120401==    by 0x168ACB72: jabber_stream_init (in /usr/lib/purple-2/libjabber.so.0.0.0)
==2120401==    by 0x168ADD77: jabber_login_callback_ssl (in /usr/lib/purple-2/libjabber.so.0.0.0)
==2120401==  Address 0xd780c15 is 5 bytes inside a block of size 4,096 alloc'd
==2120401==    at 0x483E77F: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0xC5053FD: PORT_Alloc_Util (in /usr/lib/x86_64-linux-gnu/libnssutil3.so)
==2120401==    by 0x100EEBC7: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100F3540: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100FDAB3: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100FE450: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x10092F84: ssl_nss_connect (in /usr/lib/purple-2/ssl-nss.so)
==2120401==    by 0x576B82D: purple_ssl_connect_with_host_fd (in /usr/lib/libpurple.so.0.14.8)
==2120401==    by 0x168B0CA9: jabber_process_packet (in /usr/lib/purple-2/libjabber.so.0.0.0)
==2120401==    by 0x168BD8D3: jabber_parser_element_end_libxml (in /usr/lib/purple-2/libjabber.so.0.0.0)
==2120401==    by 0x6647DF5: ??? (in /usr/lib/x86_64-linux-gnu/libxml2.so.2.9.12)
==2120401==    by 0x664882A: xmlParseChunk (in /usr/lib/x86_64-linux-gnu/libxml2.so.2.9.12)
==2120401== 
==2120401== 
==2120401== 278 errors in context 12 of 14:
==2120401== Conditional jump or move depends on uninitialised value(s)
==2120401==    at 0x4844E5E: __memcmp_sse4_1 (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x1A4199C5: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41C914: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41D17C: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41F45A: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A3DC791: ??? (in /usr/lib/x86_64-linux-gnu/libsoftokn3.so)
==2120401==    by 0xC3D15F1: PK11_AEADRawOp (in /usr/lib/x86_64-linux-gnu/libnss3.so)
==2120401==    by 0xC3D1BBF: PK11_AEADOp (in /usr/lib/x86_64-linux-gnu/libnss3.so)
==2120401==    by 0x10105BFA: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D6CD0: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D711F: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D72C3: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401== 
==2120401== 
==2120401== 353 errors in context 13 of 14:
==2120401== Conditional jump or move depends on uninitialised value(s)
==2120401==    at 0xA91F3B9: murrine_draw_expander (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0xA919674: ??? (in /usr/lib/x86_64-linux-gnu/gtk-2.0/2.10.0/engines/libmurrine.so)
==2120401==    by 0x1643A1: pidgin_cell_renderer_expander_render (in /usr/bin/pidgin)
==2120401==    by 0x4D5C605: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0x4D5CEF4: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0x4D4737C: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0x4D48334: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0x4C4B1AA: ??? (in /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0.2400.33)
==2120401==    by 0x540A6DE: g_closure_invoke (in /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0.7000.2)
==2120401==    by 0x541C523: signal_emit_unlocked_R (in /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0.7000.2)
==2120401==    by 0x5422ABA: g_signal_emit_valist (in /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0.7000.2)
==2120401==    by 0x54234FE: g_signal_emit (in /usr/lib/x86_64-linux-gnu/libgobject-2.0.so.0.7000.2)
==2120401== 
==2120401== 
==2120401== 1012 errors in context 14 of 14:
==2120401== Conditional jump or move depends on uninitialised value(s)
==2120401==    at 0x4844E5E: __memcmp_sse4_1 (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==2120401==    by 0x1A4199C5: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41D1B6: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A41F45A: ??? (in /usr/lib/x86_64-linux-gnu/libfreeblpriv3.so)
==2120401==    by 0x1A3DC791: ??? (in /usr/lib/x86_64-linux-gnu/libsoftokn3.so)
==2120401==    by 0xC3D15F1: PK11_AEADRawOp (in /usr/lib/x86_64-linux-gnu/libnss3.so)
==2120401==    by 0xC3D1BBF: PK11_AEADOp (in /usr/lib/x86_64-linux-gnu/libnss3.so)
==2120401==    by 0x10105BFA: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D6CD0: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D711F: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D72C3: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401==    by 0x100D7447: ??? (in /usr/lib/x86_64-linux-gnu/libssl3.so)
==2120401== 
==2120401== ERROR SUMMARY: 2184 errors from 14 contexts (suppressed: 0 from 0)
```

Didn't you assure it would get much more intelligible with Valgrind? :P  To me, even more of unknown is contacting the known now: the allocation places just jump here and there however they want as well as the freeing places did.

## Comment 1107858106

reporter (NONE) · bodqhrohro · 2022-04-24T14:59:42Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1107858106

Uh oh, still relevant and thus isn't related to the telegram-purple bug:
```
(16:24:01) log: Failed to open log file "/home/bodqhrohro/.purple/logs/800376413022453793.log" for reading: Нет такого файла или каталога
(16:24:01) Gtk: IA__gtk_widget_hide: assertion 'GTK_IS_WIDGET (widget)' failed
(16:24:01) g_log: purple_strreplace: assertion 'string != NULL' failed
(16:24:01) g_log: purple_strreplace: assertion 'string != NULL' failed
(16:24:01) LaTeX: Writing Message: Ещё с тех времён использовал super converter
(16:24:01) GLib: Source ID 1465354016 was not found when attempting to remove it
(16:24:01) GLib: Source ID 4767 was not found when attempting to remove it
@--Type <RET> for more, q to quit, c to continue without paging--

Thread 1 "pidgin" received signal SIGSEGV, Segmentation fault.
purple_http_connection_free (hc=0x5555575c7f40) at purple2compat/http.c:1687
1687			purple_http_connection_set_remove(hc->connection_set, hc);
@(gdb) bt
#0  purple_http_connection_free (hc=0x5555575c7f40) at purple2compat/http.c:1687
#1  purple_http_connection_terminate (hc=hc@entry=0x5555575c7f40) at purple2compat/http.c:1732
#2  0x00007ffff0cde0c8 in _purple_http_recv_loopbody (hc=hc@entry=0x5555575c7f40, fd=<optimized out>) at purple2compat/http.c:1298
#3  0x00007ffff0cde780 in _purple_http_recv (_hc=0x5555575c7f40, fd=<optimized out>, cond=cond@entry=PURPLE_INPUT_READ) at purple2compat/http.c:1309
#4  0x00005555555cdfb2 in pidgin_io_invoke (source=<optimized out>, condition=<optimized out>, data=0x55555757a7c0) at ././pidgin/gtkeventloop.c:73
#5  0x00007ffff72e0be4 in g_main_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:3381
#6  g_main_context_dispatch (context=0x5555556c8b10) at ../../../glib/gmain.c:4099
#7  0x00007ffff72e0f88 in g_main_context_iterate (context=0x5555556c8b10, block=block@entry=1, dispatch=dispatch@entry=1, self=<optimized out>)
    at ../../../glib/gmain.c:4175
#8  0x00007ffff72e1273 in g_main_loop_run (loop=0x5555574b5e30) at ../../../glib/gmain.c:4373
#9  0x00007ffff79d7b2a in gtk_main () at /usr/lib/x86_64-linux-gnu/libgtk-x11-2.0.so.0
#10 0x0000555555591d70 in main (argc=<optimized out>, argv=<optimized out>) at ././pidgin/gtkmain.c:947
@(gdb) p *hc
$6 = {gc = 0x654e207469686f4c, callback = 0x5500696c6170, user_data = 0x5555575c7f70, is_reading = 49, is_keepalive = 0, is_cancelling = 1465679792, 
  url = 0x7fff00000003, request = 0x5555575c7f90, response = 0x7fff00000000, socket_request = 0x20, connection_set = 0x21, 
  socket = 0x6953207469686f4c, request_header = 0x7f006968646e, request_header_written = 1465679808, request_contents_written = 21845, 
  main_header_got = 49, headers_got = 0, response_buffer = 0x5555575c8000, gz_stream = 0x7fff00000003, contents_reader_buffer = 0x5555575c7fe0, 
  contents_reader_requested = 0, redirects_count = 32767, length_expected = 32, length_got = 0, length_got_decompressed = 33, is_chunked = 0, 
  in_chunk = 1768451916, chunks_done = 1968185460, chunk_length = 1650551406, chunk_got = 105, link_global = 0x5555575c8010 = {0x555557578700, 
    <error reading variable>
```
And again this 0x21…

## Comment 1109188223

reporter (NONE) · bodqhrohro · 2022-04-26T01:01:16Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1109188223

```
(02:40:15) log: Failed to open log file "/home/bodqhrohro/.purple/logs/800376413022453793.log" for reading: Нет такого файла или каталога
(02:40:16) Gtk: IA__gtk_widget_hide: assertion 'GTK_IS_WIDGET (widget)' failed
(02:40:16) g_log: purple_strreplace: assertion 'string != NULL' failed
(02:40:16) g_log: purple_strreplace: assertion 'string != NULL' failed
(02:40:17) LaTeX: Writing Message: &gt;customely<br>Уровень инглиша на те времена, ага.
Pidgin 2.14.8 были с ошибками сегментации и попытались просмотреть файл ядра.
Это глюк в программе и вы тут не виноваты.

Если вы можете повторить возникновение ошибки, пожалуйста уведомите
разработчиков, создав отчёт об ошибке на:
https://pidgin.im/development/простая карточка/

Пожалуйста, будьте готовы описать как всё произошло в тот момент
и представить вывод командной строки файла ядра.  Если вы не знаете
как его вывести, пожалуйста, прочитайте инструкцию на
https://pidgin.im/development/wiki/GetABacktrace
dns[3657546]: nobody needs me... =(
Аварийный останов
```
[pidgin-vg13.txt.gz](https://github.com/EionRobb/purple-discord/files/8558853/pidgin-vg13.txt.gz)


## Comment 1113847298

reporter (NONE) · bodqhrohro · 2022-04-29T22:49:29Z · https://github.com/EionRobb/purple-discord/issues/402#issuecomment-1113847298

```
(18:39:23) http: Timeout reached for request 0x1793b9e0
(18:39:23) http: Request 0x1793b9e0 performed without success.
(18:39:23) discord: Got response: [{"id": "969322210630180874", "type": 0, "content": "\u041b\u0435\u0447\u0438\u0442\u0441\u044f \u0442\u043e\u043b\u044c\u043a\u043e \u0440\u0435\u0441\u0442\u0430\u0440\u0442\u043e\u043c \u043c\u0438\u0434\u043b\u0435\u0442\u0430.", "channel_id": "800376413022453793", "author": {"id": "353998319539847188", "username": "bodqhrohro", "avatar": "505f3f46312333333b7602bc4a619f4e", "avatar_decoration": null, "discriminator": "8819", "public_flags": 0}, "attachments": [], "embeds": [], "mentions": [], "mention_roles": [], "pinned": false, "mention_everyone": false, "tts": false, "timestamp": "2022-04-28T19:40:24.150000+00:00", "edited_timestamp": null, "flags": 0, "components": []}]
(18:39:24) gtk-tmatz-xmpp_muc_presence_plugin: timeout_callback_conversation_switched
(18:39:32) util: Writing file prefs.xml to directory /home/bodqhrohro/.purple
(18:39:32) util: Writing file /home/bodqhrohro/.purple/prefs.xml
(18:39:36) util: Writing file blist.xml to directory /home/bodqhrohro/.purple
(18:39:36) util: Writing file /home/bodqhrohro/.purple/blist.xml
(18:39:38) util: Writing file accounts.xml to directory /home/bodqhrohro/.purple
(18:39:38) util: Writing file /home/bodqhrohro/.purple/accounts.xml
(18:39:38) discord: sending frame: {"op":1,"d":15}
(18:39:39) log: Failed to open log file "/home/bodqhrohro/.purple/logs/800376413022453793.log" for reading: Нет такого файла или каталога
(18:39:40) Gtk: IA__gtk_widget_hide: assertion 'GTK_IS_WIDGET (widget)' failed
(18:39:40) g_log: purple_strreplace: assertion 'string != NULL' failed
(18:39:40) g_log: purple_strreplace: assertion 'string != NULL' failed
(18:39:41) LaTeX: Writing Message: Лечится только рестартом мидлета.
(18:39:42) GLib: Source ID 880 was not found when attempting to remove it
Pidgin 2.14.8 были с ошибками сегментации и попытались просмотреть файл ядра.
```
[pidgin-vg16.txt.gz](https://github.com/EionRobb/purple-discord/files/8595139/pidgin-vg16.txt.gz)

