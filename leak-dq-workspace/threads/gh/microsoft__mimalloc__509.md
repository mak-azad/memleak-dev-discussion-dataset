# Difference between mimalloc's freed report and valgrind --leak-check=full

- URL: https://github.com/microsoft/mimalloc/issues/509
- Repo: microsoft/mimalloc (language: C)
- State: open; created 2021-12-21T11:42:11Z; status ok; passes main

## Issue body

reporter (NONE) · MasterDuke17 · 2021-12-21T11:42:11Z · https://github.com/microsoft/mimalloc/issues/509

I have been investigating whether we should use mimalloc for [MoarVM](https://github.com/MoarVM/MoarVM) (the primary backend for the [Rakudo](https://github.com/rakudo/rakudo) Raku compiler) and initial results are very promising. However, am wondering about a difference I see between the stats reported when I use `MIMALLOC_SHOW_STATS=1` with `LD_PRELOAD=/path/to/libmimalloc-debug.so` compared to `valgrind --leak-check=full`. For a minimal test case `MIMALLOC_SHOW_STATS=1 LD_PRELOAD=/path/to/libmimalloc-debug.so raku --full-cleanup -e ''` (where the `--full-cleanup` flag to `raku` tells the VM to free every thing on exit instead of just letting the OS cleanup), mimalloc reports 1.2 MiB total for `current`. However, for `valgrind --leak-check=full raku --full-cleanup -e ''`, valgrind reports `All heap blocks were freed -- no leaks are possible`. Is this just an artifact of using dynamic loading? Or could there be some other reason?

## Comment 1001712579

maintainer (COLLABORATOR) · daanx · 2021-12-27T19:29:20Z · https://github.com/microsoft/mimalloc/issues/509#issuecomment-1001712579

Hi @MasterDuke17, very interesting -- hope mimalloc can work well for the MoarVM :-) (feel free to contact me if you have further questions or need help).

The statistics of mimalloc indeed report any allocation while valgrind usually has a list of exceptions where the "leak" is expected; for example when the loader allocates thread local storage dynamically which is never released (or locale's etc). I think that is the case here too (although 1.2MiB seems a bit much). 

One thing you can do is to call `mi_stats_reset()` at the start of `main()` and `mi_stats_print(NULL)` at the end of `main` (or any reasonable block) which avoids counting at least any of the C runtime allocations.

## Comment 1011039537

reporter (NONE) · MasterDuke17 · 2022-01-12T13:21:21Z · https://github.com/microsoft/mimalloc/issues/509#issuecomment-1011039537

We're now using mimalloc in MoarVM via the single static file and using the `mi_*` functions (implemented in https://github.com/MoarVM/MoarVM/pull/1638). However, I'm now seeing even odder stats. `MIMALLOC_SHOW_STATS=1 ./install/bin/raku --full-cleanup -e ''` reports:
```
heap stats:    peak       total        freed    current       unit      count   
  reserved:  128.0 MiB  128.0 MiB    8.0 KiB  128.0 MiB                        not all freed!
 committed:  128.0 MiB  128.0 MiB    8.0 KiB  128.0 MiB                        not all freed!
```
I just tried adding `mi_stats_reset()` at the beginning of `main()` and `mi_stats_print(NULL)` at the end of `main()`, but it still printed almost exactly the same stats.

## Comment 1011624436

maintainer (COLLABORATOR) · daanx · 2022-01-13T01:16:29Z · https://github.com/microsoft/mimalloc/issues/509#issuecomment-1011624436

Ah, yes that is confusing :-(.  I just tried myself and get the same -- I will look into improving this when using `mi_stats_reset`.  

The statistics are adjusted at the lowest level (in order to be correct) but this also means that for a stand alone program you may never see the reserved/committed memory for the main thread go away -- leading to the "not all freed!" message. This is technically true but can also be ignored.  

When building in debug mode, the individual allocation bucket statistics are more useful and these will report more as expected (except for some never freed allocations related to the CRT locale's, TLS , etc). 

The last line of the statistics, starting with process does report the actual OS reported stats which are better than mimallocs "reserved" and "committed" as these are virtual ranges. The `rss` in particular shows the peak physical touched memory. 

I think your goal is to see if any memory was leaked? (is that right?) and this is unfortunately hard to see from the mimalloc stats. In the [Koka](http://koka-lang.org) language I disable mimalloc and use address sanitizer or valgrind to track leaks. It would be nice though if mimalloc could support his scenario better though. 



## Comment 1011931518

reporter (NONE) · MasterDuke17 · 2022-01-13T09:02:10Z · https://github.com/microsoft/mimalloc/issues/509#issuecomment-1011931518

> I think your goal is to see if any memory was leaked? (is that right?) and this is unfortunately hard to see from the mimalloc stats.

Yeah. I was just experimenting to see what the numbers look like. We can also conditionally build MoarVM without mimalloc, so for now at least I'll just do that when I want to use valgrind or heaptrack to check for leaks.

Thanks for following up, feel free to close this if you'd like.
