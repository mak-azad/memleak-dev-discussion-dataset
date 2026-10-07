# ld v. 1.1.0: `ld(56401) malloc: *** error for object 0xa0430754: pointer being freed was not allocated` (powerpc 32-bit)

- URL: https://github.com/iains/darwin-xtools/issues/11
- Repo: iains/darwin-xtools (language: C)
- State: open; created 2025-01-09T02:09:20Z; status ok; passes main

## Issue body

reporter (NONE) · barracuda156 · 2025-01-09T02:09:20Z · https://github.com/iains/darwin-xtools/issues/11

@iains Could you say why `ld` issues all these `malloc` errors? This is the build from 1.1.0 branch, no patches applied to the source:

```
Sergey-Fedorovs-Mac:xtools_build svacchanda\$ /opt/svacchanda/xtools/bin/ld -v
ld(56401) malloc: *** error for object 0xa0430754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(56401) malloc: *** error for object 0xa04307c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
xtools-1.1.0 ld (unpackaged)
Based on Apple Inc. ld64-253.9 
configured to support archs: ppc ppc64 i386 x86_64 x86_64h armv6 armv6m armv7 armv7s armv7m armv7em arm64
```

Script I used:
```
# Install to here.
SET(CMAKE_INSTALL_PREFIX /opt/svacchanda/xtools CACHE PATH "put it here")
SET(CMAKE_BUILD_TYPE MinSizeRel CACHE STRING "build style")

SET(CMAKE_OSX_DEPLOYMENT_TARGET "10.6" CACHE STRING "OS X Version")

# Default install place, change if you put it somehwere different.
set(SDK_BASE /Developer/SDKs)
SET(CMAKE_OSX_SYSROOT ${SDK_BASE}/MacOSX10.6.sdk CACHE PATH "system SDK")
SET(LLVM_DEFAULT_TARGET_TRIPLE powerpc-apple-darwin10 CACHE STRING "system triple")

SET(compilers /opt/local/bin)
SET(CMAKE_C_COMPILER   ${compilers}/gcc-mp-14 CACHE PATH "C")
SET(CMAKE_CXX_COMPILER ${compilers}/g++-mp-14 CACHE PATH "C++")

SET(CMAKE_C_FLAGS    "-mmacosx-version-min=10.6 -pipe" CACHE STRING "c flags")
SET(CMAKE_CXX_FLAGS  "-mmacosx-version-min=10.6 -pipe" CACHE STRING "cxx flags")

# This leaves assertions on.
SET(CMAKE_C_FLAGS_MINSIZEREL  "-Os" CACHE STRING "c   opt flags")
SET(CMAKE_CXX_FLAGS_MINSIZEREL "-Os" CACHE STRING "cxx opt flags")

# If we're building with my GCC, then avoid carrying around a shared lib.
set(CMAKE_EXE_LINKER_FLAGS "-static-libstdc++ -static-libgcc " CACHE STRING "toolchain exe ldflags")
set(CMAKE_SHARED_LINKER_FLAGS "-static-libstdc++ -static-libgcc " CACHE STRING "toolchain shlib ldflags")

# If your host is 64b.
set(XTOOLS_HOST_IS_64B NO CACHE BOOL "host native bitwidth")

# Do not link to libc++ based on support for stdlib_flag
set(XTOOLS_CXX_HAS_STDLIB_FLAG NO CACHE BOOL "link to libc++ instead of libstdc++")

set(XTOOLS_BUGURL "https://githb.com/iains/darwin-xtools/issues" CACHE STRING "bug url")
```

P. S. I also tried via MacPorts port (dropping existing patches and using 1.1.0 branch) with the same result. I also tried using `gcc10-bootstrap` as the compiler, with the same result.
Other tools do not output `malloc` errors.


## Comment 2579035836

reporter (NONE) · barracuda156 · 2025-01-09T02:11:31Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579035836

Linking looks okay:
```
$ otool -L  /opt/svacchanda/xtools/bin/ld
/opt/svacchanda/xtools/bin/ld:
	/usr/lib/libxar.1.dylib (compatibility version 1.0.0, current version 1.0.0)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 125.2.0)
```

## Comment 2579297756

reporter (NONE) · barracuda156 · 2025-01-09T06:53:58Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579297756

Despite these malloc complaints, it actually works fine, apparently. I.e., same output during linking, but nothing fails so far.
```
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/_virtualenv/bin/python /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/config/expandlibs_exec.py --uselist --  /opt/local/bin/g++-mp-14 -std=gnu++14 -o js -I/opt/local/include -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2 -Wall -Wempty-body -Wignored-qualifiers -Woverloaded-virtual -Wpointer-arith -Wsign-compare -Wtype-limits -Wunreachable-code -Wwrite-strings -Wno-invalid-offsetof -Wc++1z-compat -Wduplicated-cond -Wimplicit-fallthrough -Wno-error=maybe-uninitialized -Wno-error=deprecated-declarations -Wno-error=array-bounds -Wno-error=free-nonheap-object -Wformat -Wformat-overflow=2 -Wno-noexcept-type -fno-sized-deallocation -pipe -Os -mone-byte-bool -D_GLIBCXX_USE_CXX11_ABI=0 -arch ppc -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2 -fno-common -fno-rtti -ffunction-sections -fdata-sections -fno-exceptions -fno-math-errno -pipe -g -O3 -fno-stack-protector -fomit-frame-pointer  Unified_cpp_js_src_shell0.o   -L/opt/local/lib -Wl,-headerpad_max_install_names -arch ppc -lobjc -framework ExceptionHandling -Wl,-executable_path,/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/bin -Wl,-dead_strip   ../../../js/src/editline/libeditline.a ../../../js/src/build/libjs_static.a  ../../../mozglue/build/libmozglue.dylib -lm  -L/opt/local/lib/nspr -lplds4 -lplc4 -lnspr4 -L/opt/local/lib -lz -latomic -lm
In member function 'void JS::Rooted<T>::registerWithRootLists(JS::RootedListHeads&) [with T = JSObject*]',
    inlined from 'JS::Rooted<T>::Rooted(const RootingContext&, S&&) [with RootingContext = JSContext*; S = JSObject*; T = JSObject*]' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:948:26,
    inlined from 'virtual bool cls_testPromise_NewPromise::run(JS::HandleObject)' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:36:45:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:926:12: warning: storing the address of local variable 'promise' in '((JS::Rooted<void*>**)MEM[(struct JSContext * const &)this_9(D) + 8])[4]' [-Wdangling-pointer=]
  926 |     *stack = reinterpret_cast<Rooted<void*>*>(this);
      |     ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/js/src/jsapi-tests/Unified_cpp_js_src_jsapi-tests4.cpp:74:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp: In member function 'virtual bool cls_testPromise_NewPromise::run(JS::HandleObject)':
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:36:16: note: 'promise' declared here
   36 |   RootedObject promise(cx, CreatePromise(cx));
      |                ^~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/tests.h:338:47: note: 'this' declared here
  338 |     virtual bool run(JS::HandleObject global) override
      |                                               ^~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:35:1: note: in expansion of macro 'BEGIN_TEST'
   35 | BEGIN_TEST(testPromise_NewPromise) {
      | ^~~~~~~~~~
In member function 'void JS::Rooted<T>::registerWithRootLists(JS::RootedListHeads&) [with T = JSObject*]',
    inlined from 'JS::Rooted<T>::Rooted(const RootingContext&, S&&) [with RootingContext = JSContext*; S = JSObject*; T = JSObject*]' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:948:26,
    inlined from 'virtual bool cls_testPromise_GetPromiseState::run(JS::HandleObject)' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:45:45:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:926:12: warning: storing the address of local variable 'promise' in '((JS::Rooted<void*>**)MEM[(struct JSContext * const &)this_8(D) + 8])[4]' [-Wdangling-pointer=]
  926 |     *stack = reinterpret_cast<Rooted<void*>*>(this);
      |     ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp: In member function 'virtual bool cls_testPromise_GetPromiseState::run(JS::HandleObject)':
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:45:16: note: 'promise' declared here
   45 |   RootedObject promise(cx, CreatePromise(cx));
      |                ^~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/tests.h:338:47: note: 'this' declared here
  338 |     virtual bool run(JS::HandleObject global) override
      |                                               ^~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:44:1: note: in expansion of macro 'BEGIN_TEST'
   44 | BEGIN_TEST(testPromise_GetPromiseState) {
      | ^~~~~~~~~~
In member function 'void JS::Rooted<T>::registerWithRootLists(JS::RootedListHeads&) [with T = JSObject*]',
    inlined from 'JS::Rooted<T>::Rooted(const RootingContext&, S&&) [with RootingContext = JSContext*; S = JSObject*; T = JSObject*]' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:948:26,
    inlined from 'virtual bool cls_testPromise_ResolvePromise::run(JS::HandleObject)' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:55:45:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:926:12: warning: storing the address of local variable 'promise' in '((JS::Rooted<void*>**)MEM[(struct JSContext * const &)this_10(D) + 8])[4]' [-Wdangling-pointer=]
  926 |     *stack = reinterpret_cast<Rooted<void*>*>(this);
      |     ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp: In member function 'virtual bool cls_testPromise_ResolvePromise::run(JS::HandleObject)':
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:55:16: note: 'promise' declared here
   55 |   RootedObject promise(cx, CreatePromise(cx));
      |                ^~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/tests.h:338:47: note: 'this' declared here
  338 |     virtual bool run(JS::HandleObject global) override
      |                                               ^~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:54:1: note: in expansion of macro 'BEGIN_TEST'
   54 | BEGIN_TEST(testPromise_ResolvePromise) {
      | ^~~~~~~~~~
In member function 'void JS::Rooted<T>::registerWithRootLists(JS::RootedListHeads&) [with T = JSObject*]',
    inlined from 'JS::Rooted<T>::Rooted(const RootingContext&, S&&) [with RootingContext = JSContext*; S = JSObject*; T = JSObject*]' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:948:26,
    inlined from 'virtual bool cls_testPromise_RejectPromise::run(JS::HandleObject)' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:69:45:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:926:12: warning: storing the address of local variable 'promise' in '((JS::Rooted<void*>**)MEM[(struct JSContext * const &)this_10(D) + 8])[4]' [-Wdangling-pointer=]
  926 |     *stack = reinterpret_cast<Rooted<void*>*>(this);
      |     ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp: In member function 'virtual bool cls_testPromise_RejectPromise::run(JS::HandleObject)':
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:69:16: note: 'promise' declared here
   69 |   RootedObject promise(cx, CreatePromise(cx));
      |                ^~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/tests.h:338:47: note: 'this' declared here
  338 |     virtual bool run(JS::HandleObject global) override
      |                                               ^~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:68:1: note: in expansion of macro 'BEGIN_TEST'
   68 | BEGIN_TEST(testPromise_RejectPromise) {
      | ^~~~~~~~~~
In member function 'void JS::Rooted<T>::registerWithRootLists(JS::RootedListHeads&) [with T = JSObject*]',
    inlined from 'JS::Rooted<T>::Rooted(const RootingContext&, S&&) [with RootingContext = JSContext*; S = JSObject*; T = JSObject*]' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:948:26,
    inlined from 'virtual bool cls_testPromise_PromiseThen::run(JS::HandleObject)' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:107:45:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:926:12: warning: storing the address of local variable 'promise' in '((JS::Rooted<void*>**)MEM[(struct JSContext * const &)this_20(D) + 8])[4]' [-Wdangling-pointer=]
  926 |     *stack = reinterpret_cast<Rooted<void*>*>(this);
      |     ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp: In member function 'virtual bool cls_testPromise_PromiseThen::run(JS::HandleObject)':
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:107:16: note: 'promise' declared here
  107 |   RootedObject promise(cx, CreatePromise(cx));
      |                ^~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/tests.h:338:47: note: 'this' declared here
  338 |     virtual bool run(JS::HandleObject global) override
      |                                               ^~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:106:1: note: in expansion of macro 'BEGIN_TEST'
  106 | BEGIN_TEST(testPromise_PromiseThen) {
      | ^~~~~~~~~~
In member function 'void JS::Rooted<T>::registerWithRootLists(JS::RootedListHeads&) [with T = JSObject*]',
    inlined from 'JS::Rooted<T>::Rooted(const RootingContext&, S&&) [with RootingContext = JSContext*; S = JSObject*; T = JSObject*]' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:948:26,
    inlined from 'virtual bool cls_testPromise_PromiseCatch::run(JS::HandleObject)' at /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:130:45:
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/dist/include/js/RootingAPI.h:926:12: warning: storing the address of local variable 'promise' in '((JS::Rooted<void*>**)MEM[(struct JSContext * const &)this_20(D) + 8])[4]' [-Wdangling-pointer=]
  926 |     *stack = reinterpret_cast<Rooted<void*>*>(this);
      |     ~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp: In member function 'virtual bool cls_testPromise_PromiseCatch::run(JS::HandleObject)':
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:130:16: note: 'promise' declared here
  130 |   RootedObject promise(cx, CreatePromise(cx));
      |                ^~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/tests.h:338:47: note: 'this' declared here
  338 |     virtual bool run(JS::HandleObject global) override
      |                                               ^~~~~~~~
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/jsapi-tests/testPromise.cpp:129:1: note: in expansion of macro 'BEGIN_TEST'
  129 | BEGIN_TEST(testPromise_PromiseCatch) {
      | ^~~~~~~~~~
ld(59562) malloc: *** error for object 0xa0430754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(59562) malloc: *** error for object 0xa04307c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/_virtualenv/bin/python -m mozbuild.action.check_binary --target js
../../../config/nsinstall -L /opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/js/src/shell -m 755 'js' '../../../dist/bin'
make[3]: Leaving directory `/opt/local/var/macports/build/_opt_PPCSnowLeopardPorts_lang_mozjs60/mozjs60/work/mozjs-60.8.0/js/src/obj/js/src/shell'
```

## Comment 2579349677

other (NONE) · cooljeanius · 2025-01-09T07:36:53Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579349677

Did you try the "`set a breakpoint in malloc_error_break to debug`" suggestion it printed? 

## Comment 2579385283

maintainer (OWNER) · iains · 2025-01-09T08:01:03Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579385283

it is possible that the symbols from the statically-linked libstdc++ in ld are being exported - and then clashing with  symbols in /usr/lib/libstdc++.6.dylib linked into some other /usr/lib/...  this is unfortunately tricky to fix without versioning libstdc++ (an on-going process both upstream and locally to darwin)..  You might also check the libLTO.dylib?



## Comment 2579520558

reporter (NONE) · barracuda156 · 2025-01-09T09:05:03Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579520558

@iains I have built without LTO first and then also with LTO:
![image](https://github.com/user-attachments/assets/756f408c-0ee4-46c2-9bcb-ba94659ab6dc)

I tried a number of ways to tweak the build just to see if something gets rid of these, but no. With gcc10-bootstrap it was worse (more malloc errors), with gcc14 down to two, but I could not figure out what to try further.

However, looks like both llas and ld work. I did not have much time today after I finally sorted the build, but rebuilding xtools with llas worked and building mozjs with both worked either.

## Comment 2579528120

reporter (NONE) · barracuda156 · 2025-01-09T09:07:17Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579528120

@cooljeanius I will check how to do that.

## Comment 2579866277

other (NONE) · cooljeanius · 2025-01-09T11:09:30Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579866277

> @cooljeanius I will check how to do that.

Well, step 1 is attaching your debugger... are you using `gdb` or `lldb`?

## Comment 2579873723

reporter (NONE) · barracuda156 · 2025-01-09T11:12:56Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579873723

@cooljeanius I think only GDB is available for PowerPC, so I have that. If I run the same command to `ld` with GDB, it just spits out same malloc errors and exits normally. So a usual `bt` does not apply. How do I set a breakpoint in this case to prevent it from exiting?

## Comment 2579890085

maintainer (OWNER) · iains · 2025-01-09T11:21:11Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579890085

@cooljeanius, @barracuda156   - IIRC this is a hard problem to debug - and I have some doubts as to whether gdb-6 (apple's last version) is up to it - you might do better by using `DYLD_PRINT_LIBRARIES=1 and DYLD_PRINT_BINDINGS=1` and looking to see if new and delete are mismatched (i.e. coming from different DSOs).   As said, it's not easy to debug - because the problem is occurring during program start-up (i.e. before main() has even been reached) in general.

## Comment 2579915279

reporter (NONE) · barracuda156 · 2025-01-09T11:29:58Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579915279

@iains I have seen a similar behavior with some other software, which also appears otherwise working normally (at least from a user perspective).

(Often these malloc errors, especially those which actually crash a binary on launch, are solvable via pointing DYLD_LIBRARY_PATH to libgcc directory, but sometimes they still remain or happen in a scenario where libstdc++ should not even be involved.)

## Comment 2579938349

maintainer (OWNER) · iains · 2025-01-09T11:38:47Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579938349

> @iains I have seen a similar behavior with some other software, which also appears otherwise working normally (at least from a user perspective).
> 
> (Often these malloc errors, especially those which actually crash a binary on launch, are solvable via pointing DYLD_LIBRARY_PATH to libgcc directory, but sometimes they still remain or happen in a scenario where libstdc++ should not even be involved.)

Yes, using DYLD_LIBRARY_PATH works on 10.5 - actually after 10.6 AFAIR dyld properly honours the different paths for the two copies of libstdc++ and we do not have a problem.   The pending update to `xtools` allows building a bootstrap toolchain that only uses /usr/lib/libstdc++ (of course, you will still potentially run into the issue with any c++11+ program that uses system libraries linked against /usr/lib/libstdc++).  As said. the only long-term solution is to support a hidden namespace versioned libstdc++ that deals with the c++11 std::string changes ... and that's not fully completed upstream - so not yet a back-port option.


## Comment 2579956112

reporter (NONE) · barracuda156 · 2025-01-09T11:47:39Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579956112

@iains By the way is there some reason to keep compatibility with the system libstdc++ and not just build everything with modern gcc and against its runtime libs? Wouldn’t that address the issue?
MacPorts uses libc++ on 10.6 x86, but that is not a great option on ppc, perhaps, since libc++ that we have (from llvm 7) is way older than libstdc++ of modern gcc, so switching to libc++ would likely kill support for C++17 and later. But we could just leave the system libstdc++ alone and use Xcode compilers exclusively to bootstrap the initial toolchain.
Or there are some problems here which I am unaware of? (I mean in principle; of course in practice something may not build with modern gcc, especially very old software.)

## Comment 2579967529

maintainer (OWNER) · iains · 2025-01-09T11:53:14Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579967529

I suspect libc++  not an option with fewer headaches - setting up the use of libc++ with GCC is not (yet) automated (because there are so many permutations of self-built and system ones).  As always, it's a judgement on where to spend time - every problem is solvable with enough effort - but making Sequoia work is currently a higher priority than Leopard ;)


## Comment 2579976892

reporter (NONE) · barracuda156 · 2025-01-09T11:57:37Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579976892

@iains Yeah, what I was rather thinking of is to use only one libstdc++, which is provided by modern gcc (and then no need for old C++ ABI). And do not use Xcode gcc and its libs for anything besides toolchain bootstrap.

## Comment 2579987687

maintainer (OWNER) · iains · 2025-01-09T12:02:53Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2579987687

> @iains Yeah, what I was rather thinking of is to use only one libstdc++, which is provided by modern gcc (and then no need for old C++ ABI). And do not use Xcode gcc and its libs for anything besides toolchain bootstrap.

IFF you are the system controller **_and_** you are happy to do so then, indeed replacing the /usr/lib/libstdc++.6.dylib with the current GCC one is an option.  I could say that you have such an unusual and already-modified configuration that  that's probably an easy route (although my advice would be to rename and keep the apple one in case you need to undo the action) **AND NOTE THAT A MISTAKE COULD MAKE THE SYSTEM UNBOOTABLE** - so you better have a way to boot it up and restore the original config :D .

However, I cannot recommend this action for the general end-user ... 


## Comment 2580029704

reporter (NONE) · barracuda156 · 2025-01-09T12:24:48Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2580029704

Yeah, I always have several installations, so that I can reboot into a working OS if something goes wrong and also have a reference to source components from.
(Also since my pre-built ports are now rsynced to a server, I can get back to the current state in a matter of couple of hours even if the main system is wiped out.)

A bit on a side note, but of practical relevance at the moment: is there a reproducible and documented procedure to build Apple CLI tools of Xcode 3.2.6? The problem is that release does not have ppc slices in many crucial components, and Darwinbuild, while kinda works, is not a reproducible build system (nothing builds without manual tweaks, dependencies are not tracked correctly, etc.). I could probably reimplement everything via MacPorts build system (simply because I know it better), but if there exists a solution, I rather not reinvent a bicycle.
The context of the question: potential users of 10.6.8 on powerpc (however few of them) should have a straightforward way to install essential Unix tools, so that my MacPorts fork (or mainstream one) can be used. I.e. either it is needed to make a standalone distribution of CLI tools with ppc slices or at least an archive of binaries to replace manually (plus a reproducible procedure to build those). Otherwise there is a disconnect between ”here is the OS image to install” and ”here is PPCPorts which can supply pre-built toolchain or build from source w/e needed”.

P. S. And for this we need standard Apple tools; a decision to switch to some newer implementation (whether xtools, MacPorts’ cctools or something else) is to be left to an end-user.

## Comment 2580731136

maintainer (OWNER) · iains · 2025-01-09T16:26:05Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2580731136


> A bit on a side note, but of practical relevance at the moment: is there a reproducible and documented procedure to build Apple CLI tools of Xcode 3.2.6? 

I don't think that this is even possible - since some of the content (e.g. dsymutil and the other dwarfutils) sources are not present - I'd suppose that darwinbuild would build everything that was available as source.

The reason that `xtools` is a composite is because of needing to add things in from different places .

## Comment 2580763285

maintainer (OWNER) · iains · 2025-01-09T16:36:16Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2580763285

note: for the (as yet unreleased, sorry) `xtools-0.7.0` which is specifically targeting the OS versions [10.4..10.8] that use `/usr/lib/libstdc++.6.dylib` as their c++ library - I have made a sequence that starts with Apple-4.2.1 and does not require anything else to bootstrap to gcc-10.  This might well be suitable for your needs, since it _only_ requires a (non-apple) pre-built GCC if you want to build Ada.


## Comment 2581919250

reporter (NONE) · barracuda156 · 2025-01-10T06:57:48Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2581919250

> I don't think that this is even possible - since some of the content (e.g. dsymutil and the other dwarfutils) sources are not present - I'd suppose that darwinbuild would build everything that was available as source.

The minimum set of utils to get the setup working is not huge: as, ar, flex, gm4, gnumake, ld, libtool, lipo, nm, nmedit, otool. So mostly cctools, but I wanted to get exactly 3.2.6 versions in this case (to replace Apple binaries).
gcc-4.2 also lacks ppc slices in its ld, as a remember, so that should be rebuilt.
The rest either has ppc slices so can be used as is after installing standard 3.2.6 or not essential (once it suffices to build something, we are good to go; for debugging newer tools can be used).
There are some proprietary Xcode components for which no sources exist like `ibtool`, so those can only be grabbed from earlier builds of Xcode, which mostly works, but not always, so some Cocoa GUI ports will need to be cross-compiled for ppc on x86 (iTerm2 as a recent example, but there are very few of such, and nothing essential to development).

Darwinbuild as is in MacPorts or its upstream is just broken and does not even build itself on 10.6 for ppc. Once fixed, it fails to build stuff for ppc. Also, Apple repos are dead, so it cannot fetch anything.
I got all these sorted out, so now it actually can build stuff for ppc (both natively and from 10.6.8 x86), but some components fail to build and many complex ones require an undocumented sequence of builds. Unlike MacPorts, there is no mechanism to handle dependencies. So not that it is impossible to do it that way, it just turned out way more painful than “just fix Darwinbuild itself, and you are sorted”.

## Comment 2585119616

reporter (NONE) · barracuda156 · 2025-01-11T06:37:26Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585119616

2.2.4 and 3.3.1 exhibit the same behavior:
```
Sergey-Fedorovs-Mac:~ svacchanda\$ ld --version
ld(17415) malloc: *** error for object 0xa0430754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(17415) malloc: *** error for object 0xa04307c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
xtools-3.3.1 ld (macos-powerpc)
Based on Apple Inc. ld64-351.8 (with LLVM LTO support)
configured to support archs: ppc ppc64 i386 x86_64 x86_64h armv6 armv6m armv7 armv7s armv7m armv7em arm64
LTO support using: LLVM version 7.1.1 (static support for 22, runtime is 22)
TAPI support using: MacOS PowerPC TAPI version 2.0.0
```
```
Sergey-Fedorovs-Mac:~ svacchanda\$ otool -L /opt/local/bin/ld
/opt/local/bin/ld:
	/usr/lib/libxar.1.dylib (compatibility version 1.0.0, current version 1.0.0)
	/opt/local/libexec/llvm-7.1.1/lib/libLTO.dylib (compatibility version 1.0.0, current version 7.1.1)
	/opt/local/lib/libtapi.dylib (compatibility version 1.0.0, current version 7.1.1)
	/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 125.2.11)
```

## Comment 2585122234

reporter (NONE) · barracuda156 · 2025-01-11T06:47:33Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585122234

@iains The output with those two variables enabled in environment is huge, 26k LoC. Is it sequential? If yes, then this occurs before `malloc` errors:
```
dyld: bind indirect sym: ld:___cxa_atexit$lazy_ptr = libSystem.B.dylib:___cxa_atexit, *0x0024c174 = 0x9259eca8
dyld: bind indirect sym: ld:__ZN2ld4tool13DSOHandleAtomC4EPKcNS_4Atom5ScopeENS4_20SymbolTableInclusionERNS_7SectionE$lazy_ptr = ld:__ZN2ld4tool13DSOHandleAtomC4EPKcNS_4Atom5ScopeENS4_20SymbolTableInclusionERNS_7SectionE, *0x00249408 = 0x0001fd18
dyld: bind indirect sym: ld:_strcmp$lazy_ptr = libSystem.B.dylib:_strcmp, *0x0024c330 = 0x9259f1a0
dyld: bind indirect sym: ld:_pthread_once$lazy_ptr = libSystem.B.dylib:_pthread_once, *0x0024c2d4 = 0x92554d14
dyld: bind indirect sym: ld:_memset$lazy_ptr = libSystem.B.dylib:_memset, *0x0024c260 = 0x924b67a0
dyld: bind indirect sym: ld:__ZNKSt6locale5facet16_M_add_referenceEv$lazy_ptr = ld:__ZNKSt6locale5facet16_M_add_referenceEv, *0x0024ab7c = 0x0013b840
dyld: bind indirect sym: ld:__ZNSt7__cxx118messagesIcEC4Em$lazy_ptr = ld:__ZNSt7__cxx118messagesIcEC4Em, *0x0024b138 = 0x00156a0c
dyld: bind indirect sym: ld:_wctob$lazy_ptr = libSystem.B.dylib:_wctob, *0x0024c3d4 = 0x92532700
dyld: bind indirect sym: ld:_btowc$lazy_ptr = libSystem.B.dylib:_btowc, *0x0024c1a0 = 0x92520564
dyld: bind indirect sym: ld:__ZNSt7__cxx118messagesIwEC4Em$lazy_ptr = ld:__ZNSt7__cxx118messagesIwEC4Em, *0x0024b32c = 0x0016362c
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8numpunctIcEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8numpunctIcEEEvPT_, *0x0024abc0 = 0x001431fc
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt7collateIcEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt7collateIcEEEvPT_, *0x0024abb0 = 0x00143248
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIcLb0EEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIcLb0EEEEvPT_, *0x0024aba0 = 0x00143294
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIcLb1EEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIcLb1EEEEvPT_, *0x0024aba4 = 0x001432e0
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_getIcSt19istreambuf_iteratorIcSt11char_traitsIcEEEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_getIcSt19istreambuf_iteratorIcSt11char_traitsIcEEEEEvPT_, *0x0024abd0 = 0x0014332c
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_putIcSt19ostreambuf_iteratorIcSt11char_traitsIcEEEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_putIcSt19ostreambuf_iteratorIcSt11char_traitsIcEEEEEvPT_, *0x0024abd8 = 0x00143378
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8time_getIcSt19istreambuf_iteratorIcSt11char_traitsIcEEEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8time_getIcSt19istreambuf_iteratorIcSt11char_traitsIcEEEEEvPT_, *0x0024abc8 = 0x001433c4
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8messagesIcEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8messagesIcEEEvPT_, *0x0024abb8 = 0x00143410
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8numpunctIwEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8numpunctIwEEEvPT_, *0x0024abc4 = 0x0014345c
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt7collateIwEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt7collateIwEEEvPT_, *0x0024abb4 = 0x001434a8
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIwLb0EEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIwLb0EEEEvPT_, *0x0024aba8 = 0x001434f4
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIwLb1EEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt10moneypunctIwLb1EEEEvPT_, *0x0024abac = 0x00143540
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_getIwSt19istreambuf_iteratorIwSt11char_traitsIwEEEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_getIwSt19istreambuf_iteratorIwSt11char_traitsIwEEEEEvPT_, *0x0024abd4 = 0x0014358c
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_putIwSt19ostreambuf_iteratorIwSt11char_traitsIwEEEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt9money_putIwSt19ostreambuf_iteratorIwSt11char_traitsIwEEEEEvPT_, *0x0024abdc = 0x001435d8
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8time_getIwSt19istreambuf_iteratorIwSt11char_traitsIwEEEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8time_getIwSt19istreambuf_iteratorIwSt11char_traitsIwEEEEEvPT_, *0x0024abcc = 0x00143624
dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8messagesIwEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8messagesIwEEEvPT_, *0x0024abbc = 0x00143670
ld(18516) malloc: *** error for object 0xa0430754: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
ld(18516) malloc: *** error for object 0xa04307c4: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
dyld: bind indirect sym: ld:__ZNSt15_Rb_tree_headerC4Ev$lazy_ptr = ld:__ZNSt15_Rb_tree_headerC4Ev, *0x00249974 = 0x00049b30
dyld: bind indirect sym: ld:_getenv$lazy_ptr = libSystem.B.dylib:_getenv, *0x0024c21c = 0x924b8890
dyld: bind indirect sym: ld:_pthread_key_create$lazy_ptr = libSystem.B.dylib:_pthread_key_create, *0x0024c2b4 = 0x92552364
dyld: bind indirect sym: ld:_mach_absolute_time$lazy_ptr = libSystem.B.dylib:_mach_absolute_time, *0x0024c23c = 0x924da720
dyld: bind indirect sym: ld:__ZN7Options16SetWithWildcardsC4Ev$lazy_ptr = ld:__ZN7Options16SetWithWildcardsC4Ev, *0x00249320 = 0x00015444
dyld: bind indirect sym: ld:_strlcat$lazy_ptr = libSystem.B.dylib:_strlcat, *0x0024c34c = 0x9254b080
dyld: bind indirect sym: ld:__ZNSt6vectorIPKcSaIS1_EE9push_backERKS1_$lazy_ptr = ld:__ZNSt6vectorIPKcSaIS1_EE9push_backERKS1_, *0x00249394 = 0x00016040
dyld: bind indirect sym: ld:__ZNKSt6vectorIPKcSaIS1_EE12_M_check_lenEmS1_$lazy_ptr = ld:__ZNKSt6vectorIPKcSaIS1_EE12_M_check_lenEmS1_, *0x00249330 = 0x00015fc8
dyld: bind indirect sym: ld:_memcpy$lazy_ptr = libSystem.B.dylib:_memcpy, *0x0024c258 = 0x924b7d40
dyld: bind indirect sym: ld:_fputs$UNIX2003$lazy_ptr = libSystem.B.dylib:_fputs$UNIX2003, *0x0024c1f4 = 0x9251f9c4
xtools-3.3.1 ld (macos-powerpc)
Based on Apple Inc. ld64-351.8 (with LLVM LTO support)
dyld: bind indirect sym: ld:_fprintf$LDBL128$lazy_ptr = libSystem.B.dylib:_fprintf$LDBL128, *0x0024c1ec = 0x9257c58c
configured to support archs: ppc ppc64 i386 x86_64 x86_64h armv6 armv6m armv7 armv7s armv7m armv7em arm64
dyld: bind indirect sym: ld:_pthread_mutex_lock$lazy_ptr = libSystem.B.dylib:_pthread_mutex_lock, *0x0024c2c0 = 0x92552d88
dyld: bind indirect sym: ld:_lto_get_version$lazy_ptr = libLTO.dylib:_lto_get_version, *0x00249224 = 0x00416590
dyld: bind indirect sym: libLTO.dylib:__ZN4llvm16LTOCodeGenerator16getVersionStringEv$lazy_ptr = libLLVM.dylib:__ZN4llvm16LTOCodeGenerator16getVersionStringEv, *0x004241dc = 0x018c42a4
dyld: bind indirect sym: ld:_pthread_mutex_unlock$lazy_ptr = libSystem.B.dylib:_pthread_mutex_unlock, *0x0024c2c4 = 0x92552974
dyld: bind indirect sym: ld:_lto_api_version$lazy_ptr = libLTO.dylib:_lto_api_version, *0x002491d8 = 0x004182d0
LTO support using: LLVM version 7.1.1 (static support for 22, runtime is 22)
dyld: bind indirect sym: ld:__ZN4tapi7Version22getFullVersionAsStringEv$lazy_ptr = libtapi.dylib:__ZN4tapi7Version22getFullVersionAsStringEv, *0x002492c0 = 0x0043fd00
dyld: bind indirect sym: libtapi.dylib:__ZNSs6appendEPKcm$lazy_ptr = libstdc++.6.dylib:__ZNSs6appendEPKcm, *0x0049f19c = 0x9229ede0
TAPI support using: MacOS PowerPC TAPI version 2.0.0
dyld: bind indirect sym: ld:_exit$lazy_ptr = libSystem.B.dylib:_exit, *0x0024c1c8 = 0x9259e87c
dyld: bind indirect sym: ld:_pthread_key_delete$lazy_ptr = libSystem.B.dylib:_pthread_key_delete, *0x0024c2b8 = 0x92552250
dyld: bind indirect sym: libLLVM.dylib:_pthread_mutex_destroy$lazy_ptr = libSystem.B.dylib:_pthread_mutex_destroy, *0x03986c88 = 0x9255289c
dyld: bind indirect sym: libLLVM.dylib:__ZNSs4_Rep10_M_destroyERKSaIcE$lazy_ptr = libstdc++.6.dylib:__ZNSs4_Rep10_M_destroyERKSaIcE, *0x03986970 = 0x9229d9ec
dyld: bind indirect sym: libstdc++.6.dylib:_pthread_key_delete$lazy_ptr = libSystem.B.dylib:_pthread_key_delete, *0x04640ea0 = 0x92552250
```

## Comment 2585202482

maintainer (OWNER) · iains · 2025-01-11T10:55:12Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585202482

> @iains The output with those two variables enabled in environment is huge, 26k LoC. Is it sequential? 

Yes, in the sense that errors triggered by a binding action appear after it.

>If yes, then this occurs before `malloc` errors:
> 
> ```
> dyld: bind indirect sym: ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8messagesIwEEEvPT_$lazy_ptr = ld:__ZNSt6locale5_Impl23_M_init_facet_uncheckedISt8messagesIwEEEvPT_, *0x0024abbc = 0x00143670
> ld(18516) malloc: *** error for object 0xa0430754: pointer being freed was not allocated
> *** set a breakpoint in malloc_error_break to debug
> ld(18516) malloc: *** error for object 0xa04307c4: pointer being freed was not allocated
> *** set a breakpoint in malloc_error_break to debug
> ```

yeah this seems like the familiar issue with facets clashing between the two instances of libstdc++.  

Actually, I would not have expected to see this on 10.6 .. I thought that dyld had been fixed by then - but maybe I misremember and it was not fixed until 10.7.



## Comment 2585203894

reporter (NONE) · barracuda156 · 2025-01-11T11:01:34Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585203894

@iains I will need to check which exactly dyld is that also. If the one in 10.6.8 had no ppc slice, then it has been [hopefully] rebuilt from source or in the worst case borrowed from earlier build. (I think the source code is available, so the last option is not very likely.)

We could perhaps just patch the source, rebuild and replace it in the OS. Is it known what specifically causes this?

## Comment 2585204484

maintainer (OWNER) · iains · 2025-01-11T11:04:09Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585204484

> > I don't think that this is even possible - since some of the content (e.g. dsymutil and the other dwarfutils) sources are not present - I'd suppose that darwinbuild would build everything that was available as source.

Are we talking about your hybrid 10.6 host - or are we talking about backporting newer tools to 10.5?

> The minimum set of utils to get the setup working is not huge: as, ar, flex, gm4, gnumake, ld, libtool, lipo, nm, nmedit, otool. So mostly cctools, but I wanted to get exactly 3.2.6 versions in this case (to replace Apple binaries). 

I am puzzled by "exactly 3.2.6" given that we know there are serious bugs (for PPC) in that toolset (agreed it is better than later or earlier ones, but it still breaks for large PPC executables).

>gcc-4.2 also lacks ppc slices in its ld, as a remember, so that should be rebuilt. 

OK.

>The rest either has ppc slices so can be used as is after installing standard 3.2.6 or not essential (once it suffices to build something, we are good to go; for debugging newer tools can be used). There are some proprietary Xcode components for which no sources exist like `ibtool`, so those can only be grabbed from earlier builds of Xcode, which mostly works, but not always, so some Cocoa GUI ports will need to be cross-compiled for ppc on x86 (iTerm2 as a recent example, but there are very few of such, and nothing essential to development).

For some tools there were open source drafts (possibly available from PureDarwin) - but that might not include ibtool - although ISTR there was an xcodebuild equivalent.

> Darwinbuild as is in MacPorts or its upstream is just broken and does not even build itself on 10.6 for ppc. Once fixed, it fails to build stuff for ppc.

Well .. you are pretty much stuck with fixing 10.6+PPC since it's not a supported configuration anywhere ;)

> Also, Apple repos are dead, so it cannot fetch anything.

AFAIK all the resources were simply moved to a github repo so that the open sourced parts of Darwin are available there.  [There's a separate repo for the developer tools].

> I got all these sorted out, so now it actually can build stuff for ppc (both natively and from 10.6.8 x86), but some components fail to build and many complex ones require an undocumented sequence of builds. Unlike MacPorts, there is no mechanism to handle dependencies. So not that it is impossible to do it that way, it just turned out way more painful than “just fix Darwinbuild itself, and you are sorted”.

understood - IDK what the best solution is - for my part, I did not want to introduce TCL as a dependency (or, so far, Python) - so I've stuck with cmake and autotools.



## Comment 2585205953

maintainer (OWNER) · iains · 2025-01-11T11:10:43Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585205953

> @iains I will need to check which exactly dyld is that also. If the one in 10.6.8 had no ppc slice, then it has been [hopefully] rebuilt from source or in the worst case borrowed from earlier build. 

If you pulled in a 10.5-ish one that would explain this..

>(I think the source code is available, so the last option is not very likely.)

OK - well you'll have to check

> We could perhaps just patch the source, rebuild and replace it in the OS. Is it known what specifically causes this?

IDK exactly - but it would seem that the 10.5 dyld does not see `/usr/lib/stdc++.6.dylib` as different from `/path/to/gcc/install/lib/libstdc++.6.dylib` where (I think) it should honour that they are different because of the two-level namspacing. 

`DYLD_LIBRARY_PATH=/path/to/gcc/install/lib` works because it disables the namespace resolution and forces all refs to use the library there.

TBH I have not explored fixing dyld as a solution - because that then means asking end users to override an Apple install.  There is a solution - to put the new libstdc++ symbols in an inline namespace - it's just not (yet) complete either upstream or locally.


## Comment 2585233137

reporter (NONE) · barracuda156 · 2025-01-11T11:58:30Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585233137

> Are we talking about your hybrid 10.6 host - or are we talking about backporting newer tools to 10.5?

As long as we talk about 32-bit ppc, I honestly see no point in 10.5, since more software works on 10.6 – this was already true for 10a190, but more so for 10.6.8. Of course, it may not work perfectly (but it does not work perfectly on Apple Silicon either), yet the improvement is visible. However, 10.5, with some reservations like lack of dispatch, is relatively close to 10.6, so more or less whatever is fixed for one will work on another, possibly with minor extra fixes for 10.5. (There are exceptions to this, I know.)
ppc64 is where 10.5 is the only option, but a) from my experience it is way more broken than ppc32, so requires more effort and time, and we are already clearly short at least on the latter; b) benefits are conceivable but unlikely proportionate to extra effort and time; c) there is no PowerBook G5, so whatever is achieved for ppc64 but not for ppc32, will be restricted to PowerMacs.

So my priority is 10.6.8, but it makes sense to consider 10.5 as well for anything fundamental like toolchain.

> > The minimum set of utils to get the setup working is not huge: as, ar, flex, gm4, gnumake, ld, libtool, lipo, nm, nmedit, otool. So mostly cctools, but I wanted to get exactly 3.2.6 versions in this case (to replace Apple binaries).
> 
> I am puzzled by "exactly 3.2.6" given that we know there are serious bugs (for PPC) in that toolset (agreed it is better than later or earlier ones, but it still breaks for large PPC executables).

What I had in mind was:
1. Target group of potential users is already small, and not everyone has a developer mindset; it is just easier to advise to install w/e Apple had, just with restored ppc. Then for whomever is interested to have more, there are ways to build and install improved toolchain. But if the latter is made a hard requirement, it may be a stopper for some people. And less users means less IRL testing.
2. Myself I cannot be sure what consequences may be introduced by literally replacing Apple components with much newer ones. I am open to trying that locally, but it is always better to have a “safe” installation to revert to if needed.

> For some tools there were open source drafts (possibly available from PureDarwin) - but that might not include ibtool - although ISTR there was an xcodebuild equivalent.

There are quite a number of Xcode components (nearly all plugins) which are x86-only, not just in 3.2.6, but way back to 10a261. The last properly ppc Xcode is in 10a190, 10a222 retains a lot of ppc, but loses some, everything after that goes down the tubes. But relevance of all these is limited: there are perhaps not many Cocoa apps which are both very important and got no alternatives. Also, cross-compilation from 3.2.6 x86 seems to work fine (XIBs are processed correctly, plugins do not break the build by not being able to load ppc images).
I think we can live without native Xcode GUI and support for XIBs at the level of x86.

> > Darwinbuild as is in MacPorts or its upstream is just broken and does not even build itself on 10.6 for ppc. Once fixed, it fails to build stuff for ppc.
> 
> Well .. you are pretty much stuck with fixing 10.6+PPC since it's not a supported configuration anywhere ;)

GCC supports it! Thanks to your earlier fixes. (gcc on 10a190 needed a minor patch, but on 10.6.8 ppc it works normally, just like on 10.6.8 on Intel.)

But yes, the usual case is that it is broken unless I fix it myself )

> > Also, Apple repos are dead, so it cannot fetch anything.
> 
> AFAIK all the resources were simply moved to a github repo so that the open sourced parts of Darwin are available there. [There's a separate repo for the developer tools].

Some sources got lost (at least two cases which I encountered), but I have moved most of relevant stuff to http://macos-powerpc.org/darwinbuild/Projects and patched `darwinbuild` to use that as a source archive.

> understood - IDK what the best solution is - for my part, I did not want to introduce TCL as a dependency (or, so far, Python) - so I've stuck with cmake and autotools.

If only Apple sources were written for CMake, that would make life much easier. We do not have a CMake recipe to build libSystem, do we?

## Comment 2585238761

reporter (NONE) · barracuda156 · 2025-01-11T12:17:28Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585238761

> > @iains I will need to check which exactly dyld is that also. If the one in 10.6.8 had no ppc slice, then it has been [hopefully] rebuilt from source or in the worst case borrowed from earlier build.
> 
> If you pulled in a 10.5-ish one that would explain this.

Most of the work on the OS itself was carried out by a developer from OpenCore Legacy Patcher, and I did not need to replace any OS components manually, so will need to check once back to the PowerMac. (There is a reference to changed/replaced components, but regardless I can just compare binaries on 10.6.8 Rosetta, 10.6.8 ppc, 10a190 and 10.5.8.)

Source is there: https://github.com/apple-oss-distributions/dyld/tree/dyld-132.13
So should be rebuildable.

## Comment 2585764439

reporter (NONE) · barracuda156 · 2025-01-12T14:51:22Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585764439

@iains I am a bit puzzled, how do I check `dyld` version? It does not seem to allow `-v` or `-version`. `/usr/lib/dyld` just says “Cannot execute binary file” for anything, `update_dyld_shared_cache` does not have arguments to display version. This is true for 10.6.8 x86_64 as well.

However, I can confirm that:

1. `/usr/lib/dyld` is identical between 10.6.8 Intel (i.e. standard release) and 10.6.8 ppc image (same binary size, same date of creation) and has ppc slice.
2. `/usr/bin/update_dyld_shared_cache` is _not_ identical and has no ppc slice in 10.6.8 Intel. So it was probably rebuilt or otherwise borrowed (from 10a190?). I cannot check that based on binary size and date, since it was thinned to have only ppc slice, so will differ regardless. Need to ask about that or check notes.

Building `dyld` from source seems to require building static `libc` first, and that will pull in a lot of stuff, I believe. I can try it, but it may take some time and effort.

## Comment 2585766306

maintainer (OWNER) · iains · 2025-01-12T14:56:25Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585766306

n

> @iains I am a bit puzzled, how do I check `dyld` version? It does not seem to allow `-v` or `-version`. `/usr/lib/dyld` just says “Cannot execute binary file” for anything, `update_dyld_shared_cache` does not have arguments to display version. This is true for 10.6.8 x86_64 as well.
> 
> However, I can confirm that:
> 
> 1. `/usr/lib/dyld` is identical between 10.6.8 Intel (i.e. standard release) and 10.6.8 ppc image (same binary size, same date of creation) and has ppc slice.
> 2. `/usr/bin/update_dyld_shared_cache` is _not_ identical and has no ppc slice in 10.6.8 Intel. So it was probably rebuilt or otherwise borrowed (from 10a190?). I cannot check that based on binary size and date, since it was thinned to have only ppc slice, so will differ regardless. Need to ask about that or check notes.

you might try "strings" on the exe.

> Building `dyld` from source seems to require building static `libc` first, and that will pull in a lot of stuff, I believe. I can try it, but it may take some time and effort.

It's probably not worth the effort - as you say the 10.6.8 dyld has a ppc slice - so I'd expect ppc and i686 to behave the same.



## Comment 2585771735

reporter (NONE) · barracuda156 · 2025-01-12T15:11:08Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585771735

> It's probably not worth the effort - as you say the 10.6.8 dyld has a ppc slice - so I'd expect ppc and i686 to behave the same.

If what matters in the discussed context is `/usr/lib/dyld`, then there is no point indeed, since from what I can see it is the original Apple binary, the same which was shipped in 10.6.8 release. Unless, of course, it is found how to fix the source first.

## Comment 2585773567

maintainer (OWNER) · iains · 2025-01-12T15:16:15Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585773567

> > It's probably not worth the effort - as you say the 10.6.8 dyld has a ppc slice - so I'd expect ppc and i686 to behave the same.
> 
> If what matters in the discussed context is `/usr/lib/dyld`, then there is no point indeed, since from what I can see it is the original Apple binary, the same which was shipped in 10.6.8 release. Unless, of course, it is found how to fix the source first.

Although I am curious about ppc64 - I was under the impression you had that working on 10.6.8 - but then that would require a ppc64 slice for dyld too.


## Comment 2585776230

reporter (NONE) · barracuda156 · 2025-01-12T15:23:56Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2585776230

> I am puzzled by "exactly 3.2.6" given that we know there are serious bugs (for PPC) in that toolset (agreed it is better than later or earlier ones, but it still breaks for large PPC executables).

@iains On a second thought, perhaps those users who cannot trust to install a pre-built binary from me (or someone else) won’t install it regardless of whether its version matches Xcode 3.2.6 release or not. For practical purposes, in such case Xcode 3.2 from 10a190 (which is available from Apple DVD image) will satisfy a need for an initial working toolchain (possibly with a replaced SDK).

Therefore, the question: is it supposed to work fine, if, for example, I install your `xtools` (or abstractly, some newer version of `cctools` and `ld64` than Apple ever had on 10.6.x) directly into `/usr/bin`?
AFAIK, in most cases that is inconsequential for MacPorts builds, since it prefers by default binaries from its prefix to system’s or Xcode ones, so presumably `/opt/local/bin/as` and `/opt/local/bin/ld` are picked as long as respective ports are present and active. It will be consequential in some specific cases, and obviously when bootstrapping basic toolchain components (including MacPorts’ – here I mean any non-Apple version built via MacPorts, not necessarily their port as it is – cctools and ld64). It also will mean that any build without MacPorts will use those tools with Xcode.

> Although I am curious about ppc64 - I was under the impression you had that working on 10.6.8 - but then that would require a ppc64 slice for dyld too.

We can probably build for ppc64 against 10.5 SDK, but it won’t work in the OS itself, unless we restore ppc64 into the system. I do not really know what is the minimum set of components and whether we have sources for all of them.

## Comment 2600122404

reporter (NONE) · barracuda156 · 2025-01-18T21:56:26Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-2600122404

@iains I have tried to install v. 1.1.0 directly into `/usr/bin` on a clean system, replacing Xcode tools:

1. `as` seems to work fine with Apple gcc.
2. `ld` does not, `malloc` errors break configure with it. At least when built with gcc10.

I still should rebuilt `ld` with gcc14 and repeat the test, since they may not behave the same, as `ld` built with gcc14 definitely works with modern gcc. But looks like with Apple gcc it may not be usable. Or have you tried that and confirmed it working?

## Comment 4894310552

maintainer (OWNER) · iains · 2026-07-06T15:03:34Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-4894310552

0.7.0r1 (built with apple-gcc-4.2)  is a better choice for 10.5-10.8 since it is designed to use the system c++98 stdc++ lib (you should not get the conflict between stdc++ libs)


## Comment 4894709269

reporter (NONE) · barracuda156 · 2026-07-06T15:39:12Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-4894709269

Yes, that is what is being done since then. Later ld versions from xtools still seem to work in most cases, but I recall with gcc they did not (last time I tried, which was with gcc14).

## Comment 4914929451

reporter (NONE) · barracuda156 · 2026-07-08T12:48:04Z · https://github.com/iains/darwin-xtools/issues/11#issuecomment-4914929451

@iains We could perhaps link libgcc and libstdc++ statically when building later branches? (Having options is good; I am not talking about switching the default away from 0.7.0, there is no reason to do that.)
