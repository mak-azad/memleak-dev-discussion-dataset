# thread leaks (non-joined) reported by ThreadSanitizer

- URL: https://github.com/parrot/parrot/issues/915
- Repo: parrot/parrot (language: C)
- State: open; created 2013-01-05T17:15:41Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · rurban · 2013-01-05T17:15:41Z · https://github.com/parrot/parrot/issues/915

The alarm thread leaks, is not joined. We might want join it, or suppress these warnings.

Recent clang 3.3 (trunk 171626)

```
clang -o miniparrot frontend/parrot/main.o src/null_config.o src/longopt.o \
    "-Wl,-rpath=/home/rurban/Perl/parrot/test/blib/lib" -L"/home/rurban/Perl/parrot/test/blib/lib" \
    -lparrot -L/usr/lib  -licuuc -licudata  -lnsl -ldl -lm -lcrypt -lutil -lpthread -lrt -lgmp -lreadline  -lffi \
   -pie -fsanitize=undefined -fsanitize=thread -fstack-protector -L/usr/local/lib -Wl,-E    
perl tools/build/gen_version.pl >runtime/parrot/include/parrot_version.pir
./miniparrot -Iruntime/parrot/include config_lib.pir > runtime/parrot/include/config.fpmc
==1687== WARNING: Program is run with unlimited stack size, which wouldn't work with ThreadSanitizer.
==1687== Re-execing with stack size limited to 33554432 bytes.
==================
WARNING: ThreadSanitizer: thread leak (pid=1687)
  Thread T1 (tid=1688, running) created by main thread at:
    #0 pthread_create ??:0 (exe+0x00000002eb8a)
    #1 Parrot_alarm_init /usr/src/parrot/test/src/alarm.c:61 (libparrot.so.4.11.0+0x000000adbd24)
    #2 Parrot_cx_init_scheduler /usr/src/parrot/test/src/scheduler.c:73 (libparrot.so.4.11.0+0x000000da7be3)
    #3 Parrot_interp_initialize_interpreter /usr/src/parrot/test/src/interp/api.c:337 (libparrot.so.4.11.0+0x000000be7239)
    #4 Parrot_api_make_interpreter /usr/src/parrot/test/src/embed/api.c:155 (libparrot.so.4.11.0+0x000000a6e485)
    #5 main /usr/src/parrot/test/frontend/parrot/main.c:178 (exe+0x000000016a84)

==================
ThreadSanitizer: reported 1 warnings
make: *** [runtime/parrot/include/config.fpmc] Error 66
```

`export TSAN_OPTIONS="report_thread_leaks=0"` would suppress this warning. 
See http://code.google.com/p/thread-sanitizer/wiki/Flags 


## Comment 11918275

maintainer (MEMBER) · leto · 2013-01-05T19:15:12Z · https://github.com/parrot/parrot/issues/915#issuecomment-11918275

@rurban Can you explain what "is not joined" means? I don't quite understand the terminology.


## Comment 11921882

reporter (MEMBER) · rurban · 2013-01-05T23:50:08Z · https://github.com/parrot/parrot/issues/915#issuecomment-11921882

On Sat, Jan 5, 2013 at 1:15 PM, leto notifications@github.com wrote:

> @rurban https://github.com/rurban Can you explain what "is not joined"
> means? I don't quite understand the terminology.

A "leaked" thread is a thread created by e.g, pthread_create(),
which was never joined.
See e.g, http://code.google.com/p/thread-sanitizer/wiki/CppManual
or http://stackoverflow.com/questions/10873519/symptoms-of-thread-leak

It's not critical for us, but a common error that one forgets to join
created
threads. And it's a resource leak, cleaned up only by process end.

## 

Reini Urban
http://cpanel.net/   http://www.perl-compiler.org/

