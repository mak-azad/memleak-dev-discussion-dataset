# gcc-asan doesn't work on android/arm32

- URL: https://github.com/ramosian-glider/address-sanitizer/issues/407
- Repo: ramosian-glider/address-sanitizer (language: Python)
- State: open; created 2015-08-24T13:08:35Z; status ok; passes main

## Issue body

reporter (NONE) · GoogleCodeExporter · 2015-08-24T13:08:35Z · https://github.com/ramosian-glider/address-sanitizer/issues/407

```
What steps will reproduce the problem?
1.built the testcase invalid-free.cc with cross-compile toolchain gcc-asan

2.upload libasan.so and binary
sudo adb root
sudo adb remount
sudo adb push libasan.so.2 /system/lib
sudo adb push invalid-free /data/local

3.running the invalid-free on Android Phone
sudo adb shell
/data/local/invalid-free

What is the expected output? What do you see instead?

the expected output should be:

running case 1:  ./TestCases/x86_binary/invalid-free 

=================================================================
==14369==ERROR: AddressSanitizer: attempting free on address which was not 
malloc()-ed: 0x60200000eff5 in thread T0
    #0 0x43be57 in __interceptor_free /tmp/AOSP-toolchain/build/../gcc/gcc-4.9.2/libsanitizer/asan/asan_malloc_linux.cc:62
    #1 0x444a00 in main (TestCases/x86_binary/invalid-free+0x4
44a00)
    #2 0x7f45f75ce76c in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2176c)
    #3 0x408c18 (TestCases/x86_binary/invalid-free+0x408c18)

0x60200000eff5 is located 5 bytes inside of 10-byte region 
[0x60200000eff0,0x60200000effa)
allocated by thread T0 here:
    #0 0x43c01f in __interceptor_malloc /tmp/AOSP-toolchain/build/../gcc/gcc-4.9.2/libsanitizer/asan/asan_malloc_linux.cc:72
    #1 0x44491f in main (TestCases/x86_binary/invalid-free+0x4
4491f)   
    #2 0x7f45f75ce76c in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2176c)

SUMMARY: AddressSanitizer: bad-free 
/tmp/AOSP-toolchain/build/../gcc/gcc-4.9.2/libsanitizer/asan/asan_malloc_linux.c
c:62 __intercept
or_free
==14369==ABORTING

when running the testcase on android, the testcase will SEGV as following:


[1m[31m==3909==ERROR: AddressSanitizer: SEGV on unknown address 0x369a00fe (pc 
0xb6f51662 bp 0xbeb58a1c sp 0xbeb589e0 T0)
[1m[0m    #0 0xb6f51661 in main TestCases/invalid-free.cc:14
    #1 0xb69c0e09  (/system/lib/libc.so+0x12e09)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV TestCases/invalid-free.cc:14 main
==3909==ABORTING


What version of the product are you using? On what operating system?

Android 5.0

Please provide any additional information below.

made a gcc-based cross-compile toolchain for Android 5.0 with AddressSanitizer 
feature enabled; then use the customzied toolchain to built the testcase in 
external/compiler-rt/test/asan/TestCases, and running the testcase on Android 
phone.

this bug had been fixed and validated with gcc4.9.2 and gcc5.2.0 in our 
development environment:


1.
modify function 

static unsigned HOST_WIDE_INT arm_asan_shadow_offset(void) 

in the gcc-4.9.2/config/arm/arm.c  

from 

static unsigned HOST_WIDE_INT
 arm_asan_shadow_offset (void)
{
 return (unsigned HOST_WIDE_INT) 1 << 29;
}

to

static unsigned HOST_WIDE_INT
 arm_asan_shadow_offset (void)
{
#ifdef TARGET_ANDROID
 return 0;
#else
 return (unsigned HOST_WIDE_INT) 1 << 29;
#endif
}

 because the process's memory layout in Android is different in x86. so the shadow offset should be zero in Android when instrument the check code.

2.disable -Os optimization options in Android build system; becase the asan 
pass   
should be called in the GCC's internal to handle GENERIC/GIMPLY 
transformation,otherwise the check code wouldn't be instrumented during compile 
stage.
```

Original issue reported on code.google.com by `zhouweig...@gmail.com` on 21 Aug 2015 at 8:41

Attachments:
- [gcc-asan_ut-on-android-after-fixbug.log](https://storage.googleapis.com/google-code-attachments/address-sanitizer/issue-407/comment-0/gcc-asan_ut-on-android-after-fixbug.log)

