# Heap Buffer Overflow in dlt_daemon_udp_clientmsg_send

- URL: https://github.com/COVESA/dlt-daemon/issues/900
- Repo: COVESA/dlt-daemon (language: C)
- State: open; created 2026-07-16T03:45:38Z; status ok; passes offcwe

## Issue body

reporter (NONE) · cryptcrack · 2026-07-16T03:45:38Z · https://github.com/COVESA/dlt-daemon/issues/900

## Summary

When the DLT daemon sends a DLT message via UDP multicast, the second memcpy in dlt_daemon_udp_clientmsg_send uses incorrect pointer arithmetic, writing past the allocated buffer deterministically. The cast (int*)data + size1 scales the destination address by sizeof(int), so the write actually lands at byte offset 4*size1 of a buffer that was only size1 + size2 bytes long.

An external DLT client that sends any normal DLT message (e.g. a context registration) causes additional firings. The bug triggers immediate abort under AddressSanitizer; on a plain glibc build it also aborts via glibc's native heap checks (malloc(): corrupted top size).

## Vulnerable Code

File: src/daemon/udp_connection/dlt_daemon_udp_socket.c — function dlt_daemon_udp_clientmsg_send:
```
220: void dlt_daemon_udp_clientmsg_send(DltDaemonClientSockInfo *clientinfo,
221:                                    void *data1, int size1, void *data2, int size2, int verbose)
222: {
...
226:     if ((clientinfo->isvalidflag == ADDRESS_VALID) &&
227:         (size1 > 0) && (size2 > 0)) {
228:         void *data = (void *)calloc((size_t)(size1 + size2), sizeof(char)); 
...
234:         memcpy(data, data1, (size_t)size1);                                 
235:         memcpy((int*)data + size1, data2, (size_t)size2);                     /* <--- Vuln BUG: writes at 4*size1 */
236:
237:         if (sendto(g_udp_sock_fd, data, (size_t)(size1 + size2), 0, ...) < 0)
...
241:         free(data);
```

## Root Cause

- Line 235: (int*)data + size1 evaluates, under C pointer arithmetic rules, to address data + sizeof(int)*size1 = data + 4*size1.
- Allocation is size1 + size2 bytes.
- Second memcpy end offset = 4*size1 + size2.
- Overflow length = 4*size1 + size2 - (size1 + size2) = 3*size1 bytes.
- The guard size1 > 0 && size2 > 0 (line 226) is satisfied by every normal multicast send, so the overflow occurs on every call.

## Reproduction method

Enable the "WITH_UDP_CONNECTION=ON" option and run the daemon.



## Log
```
=================================================================
==50273==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x507000000328 at pc 0x7a0fd366f303 bp 0x7fffc7197750 sp 0x7fffc7196ef8
WRITE of size 52 at 0x507000000328 thread T0
    #0 0x7a0fd366f302 in memcpy ../../../../src/libsanitizer/sanitizer_common/sanitizer_common_interceptors_memintrinsics.inc:115
    #1 0x5dfc0440ee36 in dlt_daemon_udp_clientmsg_send /root/dlt-daemon/src/daemon/udp_connection/dlt_daemon_udp_socket.c:235
    #2 0x5dfc0440ecf8 in dlt_daemon_udp_dltmsg_multicast /root/dlt-daemon/src/daemon/udp_connection/dlt_daemon_udp_socket.c:210
    #3 0x5dfc0436736e in dlt_daemon_client_send /root/dlt-daemon/src/daemon/dlt_daemon_client.c:260
    #4 0x5dfc04355011 in dlt_daemon_log_internal /root/dlt-daemon/src/daemon/dlt-daemon.c:2881
    #5 0x5dfc0434e82e in main /root/dlt-daemon/src/daemon/dlt-daemon.c:1677
    #6 0x7a0fd338c1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #7 0x7a0fd338c28a in __libc_start_main_impl ../csu/libc-start.c:360
    #8 0x5dfc043494c4 in _start (/root/dlt-daemon/build/src/daemon/dlt-daemon+0x234c4) (BuildId: d1bd727f339baca8b516bb61902742768c5c4a6b)

0x507000000328 is located 26 bytes after 78-byte region [0x5070000002c0,0x50700000030e)
allocated by thread T0 here:
    #0 0x7a0fd3671340 in calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x5dfc0440edc1 in dlt_daemon_udp_clientmsg_send /root/dlt-daemon/src/daemon/udp_connection/dlt_daemon_udp_socket.c:227
    #2 0x5dfc0440ecf8 in dlt_daemon_udp_dltmsg_multicast /root/dlt-daemon/src/daemon/udp_connection/dlt_daemon_udp_socket.c:210
    #3 0x5dfc0436736e in dlt_daemon_client_send /root/dlt-daemon/src/daemon/dlt_daemon_client.c:260
    #4 0x5dfc04355011 in dlt_daemon_log_internal /root/dlt-daemon/src/daemon/dlt-daemon.c:2881
    #5 0x5dfc0434e82e in main /root/dlt-daemon/src/daemon/dlt-daemon.c:1677
    #6 0x7a0fd338c1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #7 0x7a0fd338c28a in __libc_start_main_impl ../csu/libc-start.c:360
    #8 0x5dfc043494c4 in _start (/root/dlt-daemon/build/src/daemon/dlt-daemon+0x234c4) (BuildId: d1bd727f339baca8b516bb61902742768c5c4a6b)

SUMMARY: AddressSanitizer: heap-buffer-overflow ../../../../src/libsanitizer/sanitizer_common/sanitizer_common_interceptors_memintrinsics.inc:115 in memcpy
Shadow bytes around the buggy address:
  0x507000000080: fa fa 00 00 00 00 00 00 00 00 00 fa fa fa fa fa
  0x507000000100: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fd fd
  0x507000000180: fd fd fd fd fd fd fd fd fa fa fa fa 00 00 00 00
  0x507000000200: 00 00 00 00 00 fa fa fa fa fa 00 00 00 00 00 00
  0x507000000280: 00 00 00 fa fa fa fa fa 00 00 00 00 00 00 00 00
=>0x507000000300: 00 06 fa fa fa[fa]fa fa fa fa fa fa fa fa fa fa
  0x507000000380: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x507000000400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x507000000480: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x507000000500: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x507000000580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
==50273==ABORTING
Aborted
```

```
$ dlt-example-user -n 1 "AAAAAAAAAAAAAAAAAAAAAAAAAAAA"
```

```
[1120328.941926]~DLT~50274~NOTICE   ~Starting DLT Daemon; DLT Package Version: 3.0.1 STABLE, Package Revision: v3.0.0_20_gb84dbc0, build on Jul 16 2026 02:13:45
-SYSTEMD -SYSTEMD_WATCHDOG -TEST -SHM

[1120328.941966]~DLT~50274~INFO     ~DLT protocol version: 1 (DLTv1)
[1120328.942219]~DLT~50274~INFO     ~FIFO size: 65536
[1120328.942281]~DLT~50274~WARNING  ~Unable to set send timeout Socket operation on non-socket.
[1120328.942304]~DLT~50274~INFO     ~Activate connection type: 5
[1120328.942345]~DLT~50274~INFO     ~dlt_daemon_socket_open: Socket created
[1120328.942383]~DLT~50274~INFO     ~dlt_daemon_socket_open: Listening on ip 0.0.0.0 and port: 3490
[1120328.942403]~DLT~50274~INFO     ~dlt_daemon_socket_open: Socket send queue size: 16384
[1120328.942460]~DLT~50274~INFO     ~Activate connection type: 1
[1120328.942525]~DLT~50274~INFO     ~[dlt_daemon_udp_socket_open:149] Socket created - socket_family:10 socket_type:2, protocol:17
[1120328.942561]~DLT~50274~INFO     ~UDP fd creation success
[1120328.942716]~DLT~50274~INFO     ~Activate connection type: 9
[1120328.942769]~DLT~50274~INFO     ~Cannot open configuration file: /tmp/dlt-runtime.cfg
[1120328.942793]~DLT~50274~INFO     ~Ringbuffer configuration: 500000/10000000/500000
[1120328.943759]~DLT~50274~NOTICE   ~Failed to open ECU Software version file.
[1120328.943831]~DLT~50274~WARNING  ~Unable to set send timeout Socket operation on non-socket.
[1120328.943855]~DLT~50274~INFO     ~Activate connection type: 6
[1120328.943877]~DLT~50274~INFO     ~Switched to buffer state for socket connections.
[1120328.943902]~DLT~50274~WARNING  ~dlt_daemon_applications_load: cannot open file /tmp/dlt-runtime-application.cfg: No such file or directory
malloc(): corrupted top size
Aborted (core dumped)
```

```
malloc(): corrupted top size
Program received signal SIGABRT, Aborted.
__pthread_kill_implementation (no_tid=0, signo=6, threadid=<optimized out>) at ./nptl/pthread_kill.c:44
warning: 44     ./nptl/pthread_kill.c: No such file or directory
(gdb) backtrace
#0  __pthread_kill_implementation (no_tid=0, signo=6, threadid=<optimized out>) at ./nptl/pthread_kill.c:44
#1  __pthread_kill_internal (signo=6, threadid=<optimized out>) at ./nptl/pthread_kill.c:78
#2  __GI___pthread_kill (threadid=<optimized out>, signo=signo@entry=6) at ./nptl/pthread_kill.c:89
#3  0x00007ffff7de927e in __GI_raise (sig=sig@entry=6) at ../sysdeps/posix/raise.c:26
#4  0x00007ffff7dcc8ff in __GI_abort () at ./stdlib/abort.c:79
#5  0x00007ffff7dcd7b6 in __libc_message_impl (fmt=fmt@entry=0x7ffff7f728d7 "%s\n") at ../sysdeps/posix/libc_fatal.c:134
#6  0x00007ffff7e4cff5 in malloc_printerr (str=str@entry=0x7ffff7f706f7 "malloc(): corrupted top size") at ./malloc/malloc.c:5775
#7  0x00007ffff7e502fc in _int_malloc (av=av@entry=0x7ffff7fa7ac0 <main_arena>, bytes=bytes@entry=72000) at ./malloc/malloc.c:4447
#8  0x00007ffff7e52951 in __libc_calloc (n=<optimized out>, elem_size=<optimized out>) at ./malloc/malloc.c:3754
#9  0x000055555557425b in dlt_daemon_context_add (daemon=0x7fffffffae50, apid=0x7fffffff7df0 "LOG", ctid=0x7fffffff7df4 "TEST", log_level=-1 '\377',
    trace_status=-1 '\377', log_level_pos=0, user_handle=8, description=0x7fffffff80b0 "Test Context for Logging", ecu=0x7fffffffae68 "ECU1\004ECU1",
    verbose=0) at /root/normal/dlt-daemon/src/daemon/dlt_daemon_common.c:1681
#10 0x00005555555621d2 in dlt_daemon_process_user_message_register_context (daemon=0x7fffffffae50, daemon_local=0x7fffffff84e0, rec=0x5555555c5950, verbose=0)
    at /root/normal/dlt-daemon/src/daemon/dlt-daemon.c:4609
#11 0x0000555555560153 in dlt_daemon_process_user_messages (daemon=0x7fffffffae50, daemon_local=0x7fffffff84e0, receiver=0x5555555c5950, verbose=0)
    at /root/normal/dlt-daemon/src/daemon/dlt-daemon.c:3838
#12 0x0000555555578c84 in dlt_daemon_handle_event (pEvent=0x7fffffffa2b8, daemon=0x7fffffffae50, daemon_local=0x7fffffff84e0)
    at /root/normal/dlt-daemon/src/daemon/dlt_daemon_event_handler.c:264
#13 0x000055555555b956 in main (argc=1, argv=0x7fffffffe508) at /root/normal/dlt-daemon/src/daemon/dlt-daemon.c:1684
```


