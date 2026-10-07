# Potential memory leak in tcpdump.c

- URL: https://github.com/the-tcpdump-group/tcpdump/issues/1091
- Repo: the-tcpdump-group/tcpdump (language: C)
- State: open; created 2023-10-14T16:02:41Z; status ok; passes main

## Issue body

reporter (NONE) · icy17 · 2023-10-14T16:02:41Z · https://github.com/the-tcpdump-group/tcpdump/issues/1091

Calling pcap_compile in tcpdump.c line: 2350 and 2753 without releasing the fcode cause memleak.

when pcap_setfilter fails, there is no pcap_freecode. It's better to fix it.


## Comment 1964090117

maintainer (MEMBER) · infrastation · 2024-02-26T12:58:54Z · https://github.com/the-tcpdump-group/tcpdump/issues/1091#issuecomment-1964090117

The first instance is currently at line 2355. Then there is a cleanup block with call to `pcap_freecode()` conditional on `dflag` and a number of calls to `error()`, none of which makes many enough cleanup moves before the exit. The second instance is currently at line 2759. It calls `pcap_freecode()` between the calls to `pcap_compile()`, but not after the last (or the only) call.

This way, there is indeed some amount of resources not explicitly freed before the exit. Given the number of various ways to allocate these, perhaps the best potential way to address this would be to have a separate resource deallocation function that `cleanup()` could explicitly use on a signal exit and all other exit paths could implicitly use via `atexit()`.

Until anybody is willing to implement that, the resources will be freed automatically upon the termination of the process. If you are aware of more severe practical effects, please explain in detail.

## Comment 1966070918

maintainer (MEMBER) · guyharris · 2024-02-27T08:57:22Z · https://github.com/the-tcpdump-group/tcpdump/issues/1091#issuecomment-1966070918

> This way, there is indeed some amount of resources not explicitly freed before the exit.

The `pcap_t` is also not closed.  In some situations closing a `pcap_t` performs some cleanup operations other than freeing memory, such as taking an interface out of monitor mode.  (That's also a problem if the process doing the packet capture terminates abnormally.)
