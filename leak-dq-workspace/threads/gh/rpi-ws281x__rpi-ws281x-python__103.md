# munmap_chunk(): invalid pointer in ws2811_cleanup

- URL: https://github.com/rpi-ws281x/rpi-ws281x-python/issues/103
- Repo: rpi-ws281x/rpi-ws281x-python (language: C)
- State: open; created 2023-10-11T11:25:47Z; status ok; passes main

## Issue body

reporter (NONE) · godmar · 2023-10-11T11:25:47Z · https://github.com/rpi-ws281x/rpi-ws281x-python/issues/103

I'm using rpi-ws281x 5.0.0 on an RPi 3b with Raspbian GNU/Linux 11. My Python program does not use any other native libraries besides this one. In my app, I'm using 2 PWM channels (GPIO 18 and 19) and one 1 PCM channel (GPIO 21), and the app/hardware basically works.

However, usually when exiting, the program crashes due to an attempt to free an invalid pointer in `ws2811_cleanup`:

```
munmap_chunk(): invalid pointer

Program received signal SIGABRT, Aborted.
__GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
50	../sysdeps/unix/sysv/linux/raise.c: No such file or directory.
(gdb) bt
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
#1  0x76d4a364 in __GI_abort () at abort.c:79
#2  0x76d9be44 in __libc_message (action=action@entry=do_abort, fmt=<optimized out>)
    at ../sysdeps/posix/libc_fatal.c:155
#3  0x76da39fc in malloc_printerr (str=<optimized out>) at malloc.c:5347
#4  0x76da3d40 in munmap_chunk (p=<optimized out>) at malloc.c:2830
#5  0x766b0230 in ws2811_cleanup (ws2811=0x51e7e8) at lib/ws2811.c:623
#6  0x766b54d0 in _wrap_ws2811_fini (self=<optimized out>, args=<optimized out>)
    at rpi_ws281x_wrap.c:4169
#7  0x000b747c in ?? ()
Backtrace stopped: previous frame identical to this frame (corrupt stack?)
(gdb)
```
I'm not sure if this constitutes a problem with the Python wrapper or with `rpi_ws281x` itself.  I haven't been able to collect more information, but I wanted to leave this bug report since this shouldn't happen. 


## Comment 1763673452

reporter (NONE) · godmar · 2023-10-16T03:35:33Z · https://github.com/rpi-ws281x/rpi-ws281x-python/issues/103#issuecomment-1763673452

I found the issue.  [`ws2811_led_set`](https://github.com/rpi-ws281x/rpi-ws281x-python/blob/95a43d61421ffe43f9ed77034df7d5f9c00f27ed/library/rpi_ws281x.i#L78-L88) currently does not check for negative led indices:
```c
    int ws2811_led_set(ws2811_channel_t *channel, int lednum, uint32_t color)
    {
        if (lednum >= channel->count)
        {
            return -1;
        }

        channel->leds[lednum] = color;

        return 0;
    }
```
A negative value for `lednum` will not be caught and leads to memory corruption.

Even though this library is close to the hardware, it would be nice if the Python wrapper were memory safe and would catch this kind of bug in a fail-safe manner.

IMO, it may even be advisable to turn it into an `IndexError` (or implement Python's negative index semantics), rather than returning -1 (which the caller may not check). `PixelStrip` appears to want to act like an array, but doesn't implement negative indices either.

Leaving this open for comment.



