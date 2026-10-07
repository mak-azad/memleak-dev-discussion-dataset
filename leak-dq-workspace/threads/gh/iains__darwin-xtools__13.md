# ld misinterprets `-object_path_lto` flag: `error: unable to open executable 'bject_path_lto'`

- URL: https://github.com/iains/darwin-xtools/issues/13
- Repo: iains/darwin-xtools (language: C)
- State: open; created 2025-04-12T11:34:47Z; status ok; passes main

## Issue body

reporter (NONE) · barracuda156 · 2025-04-12T11:34:47Z · https://github.com/iains/darwin-xtools/issues/13

```
/opt/local/bin/gcc-mp-14 -bundle -undefined dynamic_lookup -L/opt/local/lib -Wl,-headerpad_max_install_names -arch ppc  -flto -Wl,-export_dynamic -Wl,-object_path_lto,"Modules/_[contextvars.cpython-313-darwin.so](http://contextvars.cpython-313-darwin.so/)".lto -g   Modules/_contextvarsmodule.o   -o Modules/_[contextvars.cpython-313-darwin.so](http://contextvars.cpython-313-darwin.so/)
/opt/local/bin/gcc-mp-14 -bundle -undefined dynamic_lookup -L/opt/local/lib -Wl,-headerpad_max_install_names -arch ppc  -flto -Wl,-export_dynamic -Wl,-object_path_lto,"Modules/_[csv.cpython-313-darwin.so](http://csv.cpython-313-darwin.so/)".lto -g   Modules/_csv.o   -o Modules/_[csv.cpython-313-darwin.so](http://csv.cpython-313-darwin.so/)
ld(29920) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29920) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29919) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29919) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29922) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29922) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29915) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29915) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29923) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29923) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29921) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29921) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29953) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29953) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
error: unable to open executable 'bject_path_lto'
collect2: fatal error: /usr/bin/dsymutil returned 1 exit status
compilation terminated.
make: *** [Modules/_[contextvars.cpython-313-darwin.so](http://contextvars.cpython-313-darwin.so/)] Error 1
make: *** Waiting for unfinished jobs....
ld(29957) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29957) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
error: unable to open executable 'bject_path_lto'
collect2: fatal error: /usr/bin/dsymutil returned 1 exit status
compilation terminated.
make: *** [Modules/_[bisect.cpython-313-darwin.so](http://bisect.cpython-313-darwin.so/)] Error 1
ld(29964) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29964) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
error: unable to open executable 'bject_path_lto'
collect2: fatal error: /usr/bin/dsymutil returned 1 exit status
compilation terminated.
make: *** [Modules/_[csv.cpython-313-darwin.so](http://csv.cpython-313-darwin.so/)] Error 1
ld(29969) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29969) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
error: unable to open executable 'bject_path_lto'
collect2: fatal error: /usr/bin/dsymutil returned 1 exit status
compilation terminated.
make: *** [Modules/[array.cpython-313-darwin.so](http://array.cpython-313-darwin.so/)] Error 1
ld(29971) malloc: *** error for object 0xa00a6754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(29971) malloc: *** error for object 0xa00a67c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
error: unable to open executable 'bject_path_lto'
collect2: fatal error: /usr/bin/dsymutil returned 1 exit status
compilation terminated.
make: *** [Modules/_[asyncio.cpython-313-darwin.so](http://asyncio.cpython-313-darwin.so/)] Error 1
```

## Comment 2798802414

maintainer (OWNER) · iains · 2025-04-12T11:56:45Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-2798802414

what OS version?
and what xtools version?

```
error: unable to open executable 'bject_path_lto'
collect2: fatal error: /usr/bin/dsymutil returned 1 exit status
```
seems to suggest that the program reporting the problem is `dsymutil`


## Comment 2798813924

reporter (NONE) · barracuda156 · 2025-04-12T12:30:12Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-2798813924

This is 10.6.8 (ppc, but arch should be irrelevant). Wonder why it uses `dsymutil` from system prefix. I can try using the one from LLVM 7.1.1.
I tried with xtools 1.1.0 and 3.3.0.

## Comment 2798831705

maintainer (OWNER) · iains · 2025-04-12T13:25:30Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-2798831705

`-Wl,-object_path_lto,"Modules/_[contextvars.cpython-313-darwin.so](http://contextvars.cpython-313-darwin.so/)".lto`

looks weird to me - AFAIK that should be a path in your build.

## Comment 2798893009

reporter (NONE) · barracuda156 · 2025-04-12T16:18:36Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-2798893009

> `-Wl,-object_path_lto,"Modules/_[contextvars.cpython-313-darwin.so](http://contextvars.cpython-313-darwin.so/)".lto`
> 
> looks weird to me - AFAIK that should be a path in your build.

I think so, but this is what Python build system does. It is not something I messed with manually. I can check how it looks on x86 with clang.

## Comment 2799876192

maintainer (OWNER) · iains · 2025-04-13T09:23:03Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-2799876192

I have just pushed https://github.com/iains/darwin-xtools/tree/darwin-xtools-0-7-0p0 - prerelease.  I would recommend using that on 10.5 .. 10.8 and strongly recommend using it for any powerpc/powerpc64 stuff.



## Comment 2800081673

reporter (NONE) · barracuda156 · 2025-04-13T19:08:46Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-2800081673

@iains Thank you very much! I will try that and, provided no issues emerge, will switch to this version by default.

## Comment 4894290779

maintainer (OWNER) · iains · 2026-07-06T15:01:30Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-4894290779

any more comments here?


## Comment 4894803609

reporter (NONE) · barracuda156 · 2026-07-06T15:48:56Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-4894803609

I will need to try to build Python without reverting their commits that added black magick into LTO handling. (It was just `-flto` originally, which works fine, but then some “improvement” landed.)

## Comment 5178668566

reporter (NONE) · barracuda156 · 2026-08-04T11:57:44Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-5178668566

@iains Sorry, Iain, what is the current status? Are we supposed to support this flag? `meson` check for `ld` version, and xtools `ld` passes the check, yet the flag is not supported by it, AFAICT.

See:
https://github.com/mesonbuild/meson/issues/15808
https://github.com/knik0/faac/issues/161

```
:info:build FAILED: [code=1] libfaac/libfaac.1.dylib 
:info:build /opt/local/bin/gcc-mp-16  -o libfaac/libfaac.1.dylib libfaac/libfaac.1.dylib.p/bitstream.c.o libfaac/libfaac.1.dylib.p/blockswitch.c.o libfaac/libfaac.1.dylib.p/channels.c.o libfaac/libfaac.1.dylib.p/cpu_compute.c.o libfaac/libfaac.1.dylib.p/faac.c.o libfaac/libfaac.1.dylib.p/filtbank.c.o libfaac/libfaac.1.dylib.p/fft.c.o libfaac/libfaac.1.dylib.p/frame.c.o libfaac/libfaac.1.dylib.p/huff2.c.o libfaac/libfaac.1.dylib.p/huffdata.c.o libfaac/libfaac.1.dylib.p/quantize.c.o libfaac/libfaac.1.dylib.p/sbr.c.o libfaac/libfaac.1.dylib.p/sbr_bitstream.c.o libfaac/libfaac.1.dylib.p/sbr_tables.c.o libfaac/libfaac.1.dylib.p/sbr_analysis.c.o libfaac/libfaac.1.dylib.p/resample.c.o libfaac/libfaac.1.dylib.p/stereo.c.o libfaac/libfaac.1.dylib.p/tns.c.o libfaac/libfaac.1.dylib.p/util.c.o -L/opt/local/lib -I/opt/local/include -flto=auto -Wl,-object_path_lto -Wl,libfaac/libfaac.1.dylib.p/lto.o -Wl,-dead_strip_dylibs -Wl,-headerpad_max_install_names -shared -install_name @rpath/libfaac.1.dylib -compatibility_version 1 -current_version 1 -Wl,-headerpad_max_install_names -arch ppc -pipe -Os -arch ppc -lm
:info:build ld: unknown option: -object_path_lto
```

This is 0.7.0r1.

## Comment 5183654468

maintainer (OWNER) · iains · 2026-08-04T19:28:32Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-5183654468

I've been doing some more work on this - for a r2 release (mostly on the testsuite to try and sort out what is supposed to pass and when).

At present, by default, we build the tools without LTO support - one needs to add in the libLTO.dylib and headers from an LLVM build - I guess 7.1.1 would "work".  

BUT: right now, I don't see the point for PPC because without any LTO in the inputs - which would need a working clang implementation, there's nothing to "lto". 

Perhaps when llvm-11 is ready (and it *is* getting closer) - there is some point  .. but none of this has *ever* been exercised for PPC .. there was never (at least not in public) a ppc llvm implementation.

so .. the short-term solution is to exclude that option on the ppc meson build .. and revisit when we have something working ..  I suppose you could hack in support for the option and just ignore it .. 


## Comment 5184752027

reporter (NONE) · barracuda156 · 2026-08-04T21:19:58Z · https://github.com/iains/darwin-xtools/issues/13#issuecomment-5184752027

@iains For now I disabled this in `meson` for gcc: https://github.com/macos-powerpc/powerpc-ports/commit/f38233ef9d3bf2b225dbd80829fd356b35d382cd
(Clang does not exist on ppc, so gcc is the only real case anyway.)
