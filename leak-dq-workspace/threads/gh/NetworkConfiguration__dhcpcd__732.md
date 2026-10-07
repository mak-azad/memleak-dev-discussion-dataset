# dhcpcd/src/if-options.c:1470 allocation-size-too-big in parse_option

- URL: https://github.com/NetworkConfiguration/dhcpcd/issues/732
- Repo: NetworkConfiguration/dhcpcd (language: C)
- State: open; created 2026-09-14T08:41:54Z; status ok; passes main

## Issue body

reporter (NONE) · sigdevel · 2026-09-14T08:41:54Z · https://github.com/NetworkConfiguration/dhcpcd/issues/732

### dhcpcd/src/if-options.c:1470 allocation-size-too-big in parse_option

#### Description:
A crafted conf-file supplied via dhcpcd -f <> can trigger an excessive memory allocation in parse_option() while handling the "whitelist" ('W') option. parse_option() calls "reallocarray(ifo->whitelist, ifo->whitelist_len + 2, sizeof(in_addr_t))" at if-options.c:1470; the element count derived from ifo->whitelist_len reaches an excessively large value, so the requested allocation size (0x3f3f3f3f3f3f8) exceeds the allocator's maximum supported size and AddressSanitizer aborts at if-options.c:1470.

#### To Reproduce

Steps to reproduce the behavior:

```bash
./dhcpcd -f ./6_if-options_c_1470 1> /dev/null
```

#### Output:

asan-build:
<details>
  <summary>show full -click to expand</summary>
  
```bash
unknown option: defiquietnendvendor
=================================================================
==827962==ERROR: AddressSanitizer: requested allocation size 0x3f3f3f3f3f3f8 (0x3f3f3f3f403f8 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)                                              
    #0 0x5614a98f64b0 in reallocarray (/run/media/user/8ed8205b-4114-4c2a-b2d0-e2ad6640262d/dhcpcd/dhcpcd_asan/src/dhcpcd+0xf64b0) (BuildId: b0997b3a3ac7480d192ccade97ea1fd3d69df25f)
    #1 0x5614a996d4a5 in parse_option /run/media/user/8ed8205b-4114-4c2a-b2d0-e2ad6640262d/dhcpcd/dhcpcd_asan/src/if-options.c:1470:11
    #2 0x5614a9963648 in parse_config_line /run/media/user/8ed8205b-4114-4c2a-b2d0-e2ad6640262d/dhcpcd/dhcpcd_asan/src/if-options.c:2680:10
    #3 0x5614a9963648 in read_config /run/media/user/8ed8205b-4114-4c2a-b2d0-e2ad6640262d/dhcpcd/dhcpcd_asan/src/if-options.c:3023:3
    #4 0x5614a994bece in main /run/media/user/8ed8205b-4114-4c2a-b2d0-e2ad6640262d/dhcpcd/dhcpcd_asan/src/dhcpcd.c:2271:8
    #5 0x7f92a0e7cf76 in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #6 0x7bb29ffe01af  (<unknown module>)

==827962==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big (/run/media/user/8ed8205b-4114-4c2a-b2d0-e2ad6640262d/dhcpcd/dhcpcd_asan/src/dhcpcd+0xf64b0) (BuildId: b0997b3a3ac7480d192ccade97ea1fd3d69df25f) in reallocarray
==827962==ABORTING

```

</details>

#### Environment

    OS: tested at 7.1.5-1kali1 (2026-07-29) x86_64 GNU/Linux ;
    Compiler version: Clang 21.1.8 ;
    Build-opts: -g -fno-omit-frame-pointer -fsanitize=address (AFL_USE_ASAN=1; ./configure --enable-debug --without-openssl) ;
    CPU type: x86_64 ;
    dhcpcd - commit hash 42ca579bc7aa6fbc6d1342eeade3eba028101a8b ;
    dhcpcd verison - 10.5.2


#### Additional context

link to the sample (github-url):

[6_if-options_c_1470](https://github.com/sigdevel/pocs/blob/main/res/dhcpcd/6/6_if-options_c_1470)

#### Screenshots

![screen](https://github.com/sigdevel/pocs/blob/main/res/dhcpcd/6/6_asan.png?raw=true "screen")

![screen](https://github.com/sigdevel/pocs/blob/main/res/dhcpcd/6/6_vanilla.png?raw=true "screen")


