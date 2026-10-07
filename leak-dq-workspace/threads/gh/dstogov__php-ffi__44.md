# free(): invalid pointer

- URL: https://github.com/dstogov/php-ffi/issues/44
- Repo: dstogov/php-ffi (language: C)
- State: open; created 2021-10-22T16:02:40Z; status ok; passes main

## Issue body

reporter (NONE) · Maxsh · 2021-10-22T16:02:40Z · https://github.com/dstogov/php-ffi/issues/44

I have successfully integrated [Salience](https://salience-docs.lexalytics.com/docs/getting-started) vendor shared library for analyzing text version 6.1. Due to deprecation the version, I'm trying to upgrade up to the latest version, but got an error for `FFI::load` the header of this library and immidiately abort
```
free(): invalid pointer
```

Meanwhile the latest version of the library successfully work with C written scripts, SDK Python and Java wrappers.
I suspect the issue is caused by FFI during the loading library. I've glanced a source code of php-ffi, but didn't see a way to grab some logs or additional infomation. Not sure I can find a way to debug the issue.

Also have tried to write a simple wrapper as a shared library as well, but got an error, that function from the original library cannot be loaded due to not loaded original shared library.

Can you please suggest a way to get more information about issue and the possible way to get around the issue?
Unforuneatelly support doesn't support any other excepting C,Python,Java.

PHP versions: 7.4.24, 8.0.12

## Comment 950712843

maintainer (OWNER) · dstogov · 2021-10-25T09:22:59Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-950712843

I hope, you use ext/ffi bundled into PHP-7.4/8.0. (this branch is not supported any more).
To debug the problem, try to run php under debugger and then check the gdb crash backtrace. It's better to use the DEBUG PHP build.

## Comment 951100200

reporter (NONE) · Maxsh · 2021-10-25T16:31:39Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-951100200

Hey @dstogov 

Thanks for your suggestion.

I can't find a core file in the system with that error.

I've build a docker image with enabled debug flag, based on [Generating a gdb backtrace](https://bugs.php.net/bugs-generating-backtrace.php)
Added for `root` to entrypoint 
```
echo '/tmp/core.%h.%e.%t' > /proc/sys/kernel/core_pattern
ulimit -c unlimited
```
and run via docker-compose with `privileged: true`

But, when I trigger the above issue again, `/tmp` directory doesn't have a core file.

Probably, I've missed something. Is it possible the core file isn't created because this isn't a segmentation fault?



## Comment 951124699

maintainer (OWNER) · dstogov · 2021-10-25T17:03:48Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-951124699

Everything is possible....
I would suggest to run PHP under gdb
```
$ gdb --args php your_script.php

(gdb) r
; in case of crash
(gdb) bt
```

## Comment 951645164

reporter (NONE) · Maxsh · 2021-10-26T07:37:40Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-951645164

Hi Dmitry,

Thanks for the above. I've got a backtrace of the entire stack.

```bash
Reading symbols from php...
(No debugging symbols found in php)
(gdb) r
Starting program: /usr/local/bin/php src/Salience/test.php
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
free(): invalid pointer

Program received signal SIGABRT, Aborted.
__GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
50      ../sysdeps/unix/sysv/linux/raise.c: No such file or directory.
(gdb) bt
#0  __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:50
#1  0x00007ffff749a537 in __GI_abort () at abort.c:79
#2  0x00007ffff74f3768 in __libc_message (action=action@entry=do_abort, fmt=fmt@entry=0x7ffff7601e2d "%s\n") at ../sysdeps/posix/libc_fatal.c:155
#3  0x00007ffff74faa5a in malloc_printerr (str=str@entry=0x7ffff760005a "free(): invalid pointer") at malloc.c:5347
#4  0x00007ffff74fbc14 in _int_free (av=<optimized out>, p=<optimized out>, have_lock=0) at malloc.c:4173
#5  0x00007ffff20e8a82 in std::locale::_Impl::_M_install_facet(std::locale::id const*, std::locale::facet const*) () from /usr/lib/libSalience6.so
#6  0x00007ffff20dfb13 in std::locale::_Impl::_Impl(unsigned long) () from /usr/lib/libSalience6.so
#7  0x00007ffff20e0a85 in std::locale::_S_initialize_once() () from /usr/lib/libSalience6.so
#8  0x00007ffff746434f in __pthread_once_slow (once_control=0x7ffff3dfdf58 <std::locale::_S_once>, init_routine=0x7ffff20e0a70 <std::locale::_S_initialize_once()>) at pthread_once.c:116
#9  0x00007ffff20e0ad1 in std::locale::_S_initialize() () from /usr/lib/libSalience6.so
#10 0x00007ffff20e0b13 in std::locale::locale() () from /usr/lib/libSalience6.so
#11 0x00007ffff20e268c in std::ios_base::Init::Init() () from /usr/lib/libSalience6.so
#12 0x00007ffff1629000 in _GLOBAL__sub_I_json_spirit_reader.cpp () from /usr/lib/libSalience6.so
#13 0x00007ffff7fe1fe2 in call_init (l=<optimized out>, argc=argc@entry=2, argv=argv@entry=0x7fffffffe7b8, env=env@entry=0x555556a59e50) at dl-init.c:72
#14 0x00007ffff7fe20e9 in call_init (env=0x555556a59e50, argv=0x7fffffffe7b8, argc=2, l=<optimized out>) at dl-init.c:30
#15 _dl_init (main_map=0x555556c8afa0, argc=2, argv=0x7fffffffe7b8, env=0x555556a59e50) at dl-init.c:119
#16 0x00007ffff75ad2bd in __GI__dl_catch_exception (exception=<optimized out>, operate=<optimized out>, args=<optimized out>) at dl-error-skeleton.c:182
#17 0x00007ffff7fe6364 in dl_open_worker (a=a@entry=0x7fffffffa4c0) at dl-open.c:758
#18 0x00007ffff75ad260 in __GI__dl_catch_exception (exception=0x7fffffffa4a0, operate=0x7ffff7fe5ca0 <dl_open_worker>, args=0x7fffffffa4c0) at dl-error-skeleton.c:208
#19 0x00007ffff7fe58fa in _dl_open (file=0x7ffff4874511 "libSalience6.so", mode=-2147483383, caller_dlopen=0x7ffff4a3b9e7, nsid=-2, argc=2, argv=0x7fffffffa4a0, env=0x555556a59e50) at dl-open.c:837
#20 0x00007ffff7e02258 in dlopen_doit (a=a@entry=0x7fffffffa6e0) at dlopen.c:66
#21 0x00007ffff75ad260 in __GI__dl_catch_exception (exception=exception@entry=0x7fffffffa680, operate=0x7ffff7e02200 <dlopen_doit>, args=0x7fffffffa6e0) at dl-error-skeleton.c:208
#22 0x00007ffff75ad31f in __GI__dl_catch_error (objname=0x555556a6cc90, errstring=0x555556a6cc98, mallocedp=0x555556a6cc88, operate=<optimized out>, args=<optimized out>) at dl-error-skeleton.c:227
#23 0x00007ffff7e02a65 in _dlerror_run (operate=operate@entry=0x7ffff7e02200 <dlopen_doit>, args=args@entry=0x7fffffffa6e0) at dlerror.c:170
#24 0x00007ffff7e022e4 in __dlopen (file=<optimized out>, mode=<optimized out>) at dlopen.c:87
#25 0x00007ffff4a3b9e7 in ?? () from /usr/local/lib/php/extensions/debug-non-zts-20190902/ffi.so
#26 0x00007ffff4a3cacf in zim_FFI_load () from /usr/local/lib/php/extensions/debug-non-zts-20190902/ffi.so
#27 0x0000555555b7f9ae in execute_internal ()
#28 0x00007ffff46b9dcd in xdebug_execute_internal (current_execute_data=0x7ffff48141e0, return_value=0x7ffff48141b0) at /tmp/pear/temp/xdebug/src/base/base.c:897
#29 0x0000555555b862d6 in ?? ()
#30 0x0000555555beff6b in execute_ex ()
#31 0x00007ffff46b9973 in xdebug_execute_ex (execute_data=0x7ffff4814120) at /tmp/pear/temp/xdebug/src/base/base.c:779
#32 0x0000555555b85d4e in ?? ()
#33 0x0000555555beff5b in execute_ex ()
#34 0x00007ffff46b9973 in xdebug_execute_ex (execute_data=0x7ffff4814020) at /tmp/pear/temp/xdebug/src/base/base.c:779
#35 0x0000555555bf404a in zend_execute ()
#36 0x0000555555b11d85 in zend_execute_scripts ()
#37 0x0000555555a70dc9 in php_execute_script ()
#38 0x0000555555bf6c68 in ?? ()
#39 0x0000555555bf7e30 in ?? ()
#40 0x00007ffff749bd0a in __libc_start_main (main=0x555555bf75e0, argc=2, argv=0x7fffffffe7b8, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7fffffffe7a8) at ../csu/libc-start.c:308
#41 0x000055555560494a in _start ()
```

Not sure what the reason, but it looks like it crashes when locale is trying been initialized
Docker image is based on Debian
```bash
root@3659adf77d8a:/var/www# uname -a
Linux 3659adf77d8a 5.11.0-38-generic #42~20.04.1-Ubuntu SMP Tue Sep 28 20:41:07 UTC 2021 x86_64 GNU/Linux
```

Locale is set 
```bash
root@3659adf77d8a:/var/www# locale
LANG=en_US.UTF-8
LANGUAGE=en_US.UTF-8
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=en_US.UTF-8
```

I really appreciate you are looking at the issue. It might probably the reason of the issue rises from the vendor library. I'll post also the above trace to their support.

Thanks.

## Comment 953767255

maintainer (OWNER) · dstogov · 2021-10-28T11:45:53Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-953767255

According to backtrace, there where some error in __dlopen().
May be loader can't find some dependent shared libraries. Try to run ``ldd your_lib.so``, check if all libraries are resolved.
In any case this is not an ext/ffi bug.

## Comment 953796060

reporter (NONE) · Maxsh · 2021-10-28T12:26:39Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-953796060

It doens't seem there are missing libraries:

```
dev@aa87ca38102d:/var/www$ ldd -r /usr/lib/libSalience6.so 
        linux-vdso.so.1 (0x00007fff607ef000)
        libzmq.so.5 => /usr/lib/libzmq.so.5 (0x00007fcbf01f2000)
        librt.so.1 => /lib/x86_64-linux-gnu/librt.so.1 (0x00007fcbf01e7000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007fcbf01e1000)
        libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007fcbf01bf000)
        libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fcbf007b000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fcbefeb6000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fcbf2e53000)
        libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007fcbefce7000)
        libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007fcbefccd000)
```

Anyway, thank you for your efforts.
Probs makes sens to redevelop that integation using Python SDK

## Comment 954496578

maintainer (OWNER) · dstogov · 2021-10-29T07:29:12Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-954496578

It's possible to investigate the failure a bit deeper. In gdb, you may try to go ``down`` to frame ``#22`` and ``print errstring``. 

```
...
#21 0x00007ffff75ad260 in __GI__dl_catch_exception (exception=exception@entry=0x7fffffffa680, operate=0x7ffff7e02200 <dlopen_doit>, args=0x7fffffffa6e0) at dl-error-skeleton.c:208
#22 0x00007ffff75ad31f in __GI__dl_catch_error (objname=0x555556a6cc90, errstring=0x555556a6cc98, mallocedp=0x555556a6cc88, operate=<optimized out>, args=<optimized out>) at dl-error-skeleton.c:227
#23 0x00007ffff7e02a65 in _dlerror_run (operate=operate@entry=0x7ffff7e02200 <dlopen_doit>, args=args@entry=0x7fffffffa6e0) at dlerror.c:170
#24 0x00007ffff7e022e4 in __dlopen (file=<optimized out>, mode=<optimized out>) at dlopen.c:87
```

## Comment 954873539

reporter (NONE) · Maxsh · 2021-10-29T16:16:47Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-954873539

Thanks for the above
```
(gdb) b __GI__dl_catch_error
Function "__GI__dl_catch_error" not defined.
Make breakpoint pending on future shared library load? (y or [n]) y
Breakpoint 1 (__GI__dl_catch_error) pending.
(gdb) r
Starting program: /usr/local/bin/php src/Salience/test.php
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, __GI__dl_catch_error (objname=0x555556667c00, errstring=0x555556667c08, mallocedp=0x555556667bf8, operate=0x7ffff7e02200 <dlopen_doit>, args=0x7fffffffd090) at dl-error-skeleton.c:225
225     dl-error-skeleton.c: No such file or directory.
(gdb) print errstring
$1 = (const char **) 0x555556667c08
(gdb) x /s 0x555556667c08
0x555556667c08: ""
```
It looks like the string is empty. 
Also, have tried to get exception struct details, but nothing useful
```
(gdb) print *exception
$3 = {objname = 0x0, errstring = 0x7ffff74ffed1 <__libc_calloc+129> "I\211\300H\205\300t\fH\213@\370\250\002\017\204", <incomplete sequence \333>, 
  message_buffer = 0xd0 <error: Cannot access memory at address 0xd0>}
```

I got a vendor support answer and it sounds promising:
> It appears that PHP is pulling in one version of the C++ standard library, and a third party library we use (JSON spirit) is pulling in a different one. We have had other issues with JSON spirit, so it's already scheduled for removal from Salience.

## Comment 955976511

maintainer (OWNER) · dstogov · 2021-11-01T06:49:35Z · https://github.com/dstogov/php-ffi/issues/44#issuecomment-955976511

```
print *errstring
```

PHP doesn't use C++ standard library itself. Only sone extensions e.g. ext/intl You may try to rebuild PHP without ext/intl
