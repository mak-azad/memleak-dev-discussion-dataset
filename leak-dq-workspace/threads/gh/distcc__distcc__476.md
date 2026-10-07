# `malloc(): corrupted top size` when doing anything on powerpc gentoo

- URL: https://github.com/distcc/distcc/issues/476
- Repo: distcc/distcc (language: C)
- State: open; created 2022-11-22T03:37:15Z; status ok; passes offcwe

## Issue body

reporter (NONE) · Un1q32 · 2022-11-22T03:37:15Z · https://github.com/distcc/distcc/issues/476

On an iMac G4, when i use distcc for anything I get that error.
I can't even compile a hello world.

## Comment 1323072369

reporter (NONE) · Un1q32 · 2022-11-22T05:02:50Z · https://github.com/distcc/distcc/issues/476#issuecomment-1323072369

to be clear, i mean anything related to compiling, running `distcc echo hello` will print hello to the terminal as expected, but running `distcc gcc` gives the error.  I am currently building clang hopefully that fixes it

## Comment 1323794366

other (CONTRIBUTOR) · sourcefrog · 2022-11-22T14:48:35Z · https://github.com/distcc/distcc/issues/476#issuecomment-1323794366

> iMac G4

Nice :)

If updating clang doesn't help can you somehow get a traceback of when this error occurs? Maybe running it under gdb?

## Comment 1324179000

reporter (NONE) · Un1q32 · 2022-11-22T20:03:10Z · https://github.com/distcc/distcc/issues/476#issuecomment-1324179000

gotta compile gdb AND clang, bruh.

I haven't been able to compile clang bc I'm still compiling the linux kernel so I can actually boot from the drive instead of USB.

## Comment 1324179341

reporter (NONE) · Un1q32 · 2022-11-22T20:03:33Z · https://github.com/distcc/distcc/issues/476#issuecomment-1324179341

cross compiling clang isnt working idk why

## Comment 1328142892

reporter (NONE) · Un1q32 · 2022-11-27T00:51:06Z · https://github.com/distcc/distcc/issues/476#issuecomment-1328142892

i gave up cross compiling and now im compiling clang on device, its been about 2 days of compiling and im about 2/3rds done.

## Comment 1329286170

reporter (NONE) · Un1q32 · 2022-11-28T15:20:57Z · https://github.com/distcc/distcc/issues/476#issuecomment-1329286170

it works with clang, still gonna run it in gdb, I've never used gdb before so pls tell me what commands to run

## Comment 1329376203

other (CONTRIBUTOR) · sourcefrog · 2022-11-28T16:22:50Z · https://github.com/distcc/distcc/issues/476#issuecomment-1329376203

Basically

    $ gdb DISTCC_BINARY
    gdb> r ARGS
    (crashes, presumably)
    gdb> bt

## Comment 1329382771

reporter (NONE) · Un1q32 · 2022-11-28T16:28:12Z · https://github.com/distcc/distcc/issues/476#issuecomment-1329382771

oh btw while i was testing i found that emerge could run gcc through distcc without an error, but i still got another error in my distccd log that i dont know how to fix
`distccd[66787] (dcc_execvp) ERROR: failed to exec powerpc-unknown-linux-gnu-gcc: Permission denied`
I have the toolchain in my PATH, and i have a PATH definition setup in /etc/conf.d/distccd, I dont know why its not working

## Comment 1329384853

other (CONTRIBUTOR) · sourcefrog · 2022-11-28T16:29:35Z · https://github.com/distcc/distcc/issues/476#issuecomment-1329384853

Is the file `chmod +x`? Are all its parent directories readable and executable?

## Comment 1329424503

reporter (NONE) · Un1q32 · 2022-11-28T16:51:32Z · https://github.com/distcc/distcc/issues/476#issuecomment-1329424503

> Is the file `chmod +x`? Are all its parent directories readable and executable?

yes, i tested it by building a bunch of stuff with it including bash and llvm+clang (clang didnt work at first but i had to add a line to my cmake toolchain file)

## Comment 1455116866

other (NONE) · thesamesam · 2023-03-05T15:04:39Z · https://github.com/distcc/distcc/issues/476#issuecomment-1455116866

Duplicate of https://github.com/distcc/distcc/issues/472?
