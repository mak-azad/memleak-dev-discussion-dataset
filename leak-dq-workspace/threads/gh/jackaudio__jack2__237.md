# ASAN: malloc vs delete mismatch

- URL: https://github.com/jackaudio/jack2/issues/237
- Repo: jackaudio/jack2 (language: C++)
- State: open; created 2016-11-13T23:25:39Z; status ok; passes main

## Issue body

reporter (NONE) · abique · 2016-11-13T23:25:39Z · https://github.com/jackaudio/jack2/issues/237

Hi,

I got this issue recently

==27525==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete) on 0x60300004f180
    #0 0x7ffff6f00520 in operator delete(void*) /build/gcc-multilib/src/gcc/libsanitizer/asan/asan_new_delete.cc:92
    #1 0x7ffff5ebbd88  (/usr/lib/libjack.so.0+0x12d88)
    #2 0x7ffff5eb68e9 in jack_port_register (/usr/lib/libjack.so.0+0xd8e9)

Good luck!

## Comment 260290847

maintainer (MEMBER) · sletz · 2016-11-14T09:45:43Z · https://github.com/jackaudio/jack2/issues/237#issuecomment-260290847

Without any more precise log it is just unusable...

> Le 14 nov. 2016 à 00:25, Alexandre Bique notifications@github.com a écrit :
> 
> Hi,
> 
> I got this issue recently
> 
> ==27525==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete) on 0x60300004f180
> #0 0x7ffff6f00520 in operator delete(void*) /build/gcc-multilib/src/gcc/libsanitizer/asan/asan_new_delete.cc:92
> #1 0x7ffff5ebbd88 (/usr/lib/libjack.so.0+0x12d88)
> #2 0x7ffff5eb68e9 in jack_port_register (/usr/lib/libjack.so.0+0xd8e9)
> 
> Good luck!
> 
> —
> You are receiving this because you are subscribed to this thread.
> Reply to this email directly, view it on GitHub, or mute the thread.


## Comment 260292223

reporter (NONE) · abique · 2016-11-14T09:52:09Z · https://github.com/jackaudio/jack2/issues/237#issuecomment-260292223

I believe you could wrap the delete with std::unique_ptr<>? Then you can easily find the mismatch with what is left?
Or use some static analysis?


## Comment 260292507

reporter (NONE) · abique · 2016-11-14T09:53:27Z · https://github.com/jackaudio/jack2/issues/237#issuecomment-260292507

And also the mismatch happens in jack_port_register so I believe that there are not so many things going on there...


## Comment 272830178

other (NONE) · milasudril · 2017-01-16T10:52:39Z · https://github.com/jackaudio/jack2/issues/237#issuecomment-272830178

Do you use overrides for operator new? If so C++14 adds some more entry points to define. See https://github.com/milasudril/snowflake-toolkit/commit/1f4ce0a7bc16e88606a9d2ae07656f27a9a7199b
