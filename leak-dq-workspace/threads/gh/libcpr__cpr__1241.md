# ASAN Error - CPR 1.11.2

- URL: https://github.com/libcpr/cpr/issues/1241
- Repo: libcpr/cpr (language: C++)
- State: open; created 2025-08-04T22:34:30Z; status ok; passes main

## Issue body

reporter (NONE) · amikhail48 · 2025-08-04T22:34:30Z · https://github.com/libcpr/cpr/issues/1241

### Description

Observing address sanitizer error in `cpr::Session::prepareHeader()`. See ASAN backtrace:

```
=================================================================
==9562==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x0001033dd470 in thread T0
    #0 0x000103d5734d in _ZdlPv+0x7d (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0xad34d)
    #1 0x00010320c7c1 in cpr::Session::prepareHeader()+0x281 (libcpr.1.dylib:x86_64+0x1d7c1)
    #2 0x00010320fc06 in cpr::Session::prepareCommonShared()+0xd6 (libcpr.1.dylib:x86_64+0x20c06)
    #3 0x00010321098f in cpr::Session::prepareCommon()+0x1f (libcpr.1.dylib:x86_64+0x2198f)
    #4 0x00010321b154 in cpr::Session::Post()+0x14 (libcpr.1.dylib:x86_64+0x2c154)
    #5 0x0001021d6e51 in cpr::Response cpr::Post<cpr::Url, std::__1::map<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, cpr::CaseInsensitiveCompare, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>>, cpr::Body, cpr::Timeout>(cpr::Url&&, std::__1::map<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>, cpr::CaseInsensitiveCompare, std::__1::allocator<std::__1::pair<std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>> const, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char>>>>>&&, cpr::Body&&, cpr::Timeout&&)+0x171
```

### Example/How to Reproduce

1. Create a `cpr::Post` request to any URL with `{"Content-Type", "application/json"}` in `cpr::Header`
2. Build with ASAN configuration
`ASAN_OPTIONS=detect_leaks=1 gcc -g -O1 -fsanitize=address -DADDRESS_SANITIZER -fno-omit-frame-pointer <program>`
3. Observe error

### Possible Fix

_No response_

### Where did you get it from?

GitHub (branch e.g. master)

### Additional Context/Your Environment

- OS: macOS
- Version: Sequoia 15.5


## Comment 3824087653

maintainer (MEMBER) · COM8 · 2026-01-30T14:35:16Z · https://github.com/libcpr/cpr/issues/1241#issuecomment-3824087653

@amikhail48 thanks for reporting! Could you please provide a minimal example to reproduce this?
