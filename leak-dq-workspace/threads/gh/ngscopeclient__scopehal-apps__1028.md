# Crash in VulkanWindow::SaveWindowPositionAndSize after having reset appearance preferences to default

- URL: https://github.com/ngscopeclient/scopehal-apps/issues/1028
- Repo: ngscopeclient/scopehal-apps (language: C++)
- State: open; created 2026-08-24T04:46:31Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · azonenberg · 2026-08-24T04:46:31Z · https://github.com/ngscopeclient/scopehal-apps/issues/1028

=================================================================
==1471043==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x7fffc3539940 in thread T0
    #0 0x7ffff78f6678 in operator delete(void*, unsigned long) ../../../../src/libsanitizer/asan/asan_new_delete.cpp:164
    #1 0x555559a9c46f in Preference::CleanUp() /ceph/fast/home/azonenberg/code/scopehal-apps/src/ngscopeclient/Preference.cpp:238
    #2 0x555559a9e9be in Preference::SetString(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /ceph/fast/home/azonenberg/code/scopehal-apps/src/ngscopeclient/Preference.cpp:371
    #3 0x555559ff5f59 in VulkanWindow::SaveWindowPositionAndSize() /ceph/fast/home/azonenberg/code/scopehal-apps/src/ngscopeclient/VulkanWindow.cpp:895
    #4 0x55555a1a95e9 in main /ceph/fast/home/azonenberg/code/scopehal-apps/src/ngscopeclient/main.cpp:318
    #5 0x7fffc5c35ca7 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #6 0x7fffc5c35d64 in __libc_start_main_impl ../csu/libc-start.c:360
    #7 0x555558990010 in _start (/ceph/fast/home/azonenberg/code/scopehal-apps/asan-build/src/ngscopeclient/ngscopeclient+0x343c010) (BuildId: 1135b7b805f3356ec538ca96bf74b99fc7bc871f)


