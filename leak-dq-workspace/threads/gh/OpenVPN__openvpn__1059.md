# Memory leak in dns_server_addr_parse(): addrinfo not freed when the DNS server address table is full (9th `--dns` address)

- URL: https://github.com/OpenVPN/openvpn/issues/1059
- Repo: OpenVPN/openvpn (language: C)
- State: closed; created 2026-06-20T05:38:09Z; status ok; passes main

## Issue body

reporter (NONE) · OwenSanzas · 2026-06-20T05:38:09Z · https://github.com/OpenVPN/openvpn/issues/1059


## Summary

`dns_server_addr_parse()` in `src/openvpn/dns.c` allocates an `addrinfo`
structure via `openvpn_getaddrinfo()` and then checks whether the per-server
address table (`struct dns_server::addr[8]`, capacity 8) is already full. When
it is full the function returns `false` immediately, **without** calling
`freeaddrinfo()` on the structure it just allocated. Every `--dns server <prio>
address <addr...>` option that supplies a 9th (or later) valid address therefore
leaks one `addrinfo` allocation.

The option is parsed by the normal configuration parser
(`read_config_string()` / `parse_line()` → `add_option()` →
`check_dns_option()` → `dns_server_addr_parse()`), so the leak is reachable both
from a local configuration file and from a `--dns` option pushed by the peer
(`--dns` belongs to the `OPT_P_DHCPDNS` pushable class), i.e. a server can leak
client memory through a crafted `PUSH_REPLY`.

## Root Cause

`src/openvpn/dns.c`, `dns_server_addr_parse()`:

```c
    struct addrinfo *ai = NULL;
    if (openvpn_getaddrinfo(0, addr, NULL, 0, NULL, af, &ai) != 0)   /* line 118: allocates *ai */
    {
        return false;
    }

    if (server->addr_count >= SIZE(server->addr))                    /* line 123: addr[8] is full */
    {
        return false;                                                /* line 125: BUG -- leaks ai */
    }

    /* ... use ai ... */

    server->addr_count += 1;

    freeaddrinfo(ai);                                                /* line 143: only on success */
    return true;
```

`ai` is a local variable. On the `addr_count >= 8` early return at line 125 it is
neither stored anywhere nor freed, so the allocation is unreachable and leaks.
`freeaddrinfo()` is only reached on the success path at line 143.

`check_dns_option()` (`src/openvpn/options.c`) feeds every address token of a
single `--dns server ... address ...` option into this function in a loop, so a
single option line with more than 8 valid addresses triggers the leak:

```c
        if (streq(p[3], "address"))
        {
            for (int i = 4; p[i]; ++i)
            {
                if (!dns_server_addr_parse(server, p[i]))   /* 9th valid addr leaks */
                {
                    msg(msglevel, "--dns server %ld: malformed address or maximum exceeded '%s'",
                        priority, p[i]);
                    return false;
                }
            }
        }
```

## PoC

A single configuration/option line carrying nine valid DNS server addresses
(the first eight fill `addr[0..7]`; the ninth leaks):

```
dns server 5 address 9.9.9.9 2620:: 2620:fe:: 2620:fe::29 2620:fe::fe9 9.9.9.9 2620:: 2620:fe:: 9.9.9.9
```

The same condition is reachable from a peer-pushed option, e.g. a `PUSH_REPLY`
that contains `dns server 5 address <nine or more valid addresses>`.

## Reproduction

Standalone program `dns_repro.c` (full source below) hands the crafted option
line to OpenVPN's own configuration parser `read_config_string()` and then
performs a complete caller-side cleanup (`env_set_destroy()`,
`uninit_options()`). LeakSanitizer still reports the leak, proving the
allocation is lost inside `dns_server_addr_parse()` rather than by the caller.

```c
#include "config.h"
#include "syshead.h"
#include "options.h"
#include "env_set.h"
#include "error.h"

int main(void)
{
    static const char *config =
        "dns server 5 address "
        "9.9.9.9 2620:: 2620:fe:: 2620:fe::29 2620:fe::fe9 "
        "9.9.9.9 2620:: 2620:fe:: 9.9.9.9\n";   /* 9 valid addresses */

    struct options options;
    init_options(&options);
    struct env_set *es = env_set_create(&options.gc);

    uint64_t option_types_found = 0;
    read_config_string("[CONFIG-STRING]", &options, config,
                        M_WARN, OPT_P_DEFAULT, &option_types_found, es);

    env_set_destroy(es);     /* release everything the caller owns */
    uninit_options(&options);
    return 0;
}
```

Build flags (LeakSanitizer is part of AddressSanitizer on Linux):

```
# OpenVPN configured/built with:
CC=clang
CFLAGS="-fsanitize=address -g -O1 -fno-omit-frame-pointer"
LDFLAGS="-fsanitize=address"
./configure --disable-lz4 --disable-plugins --disable-management \
            --disable-dco --disable-systemd --with-crypto-library=openssl
make

# link the reproduction (objects bundled into libopenvpn.a):
clang -fsanitize=address -g -O1 -fno-omit-frame-pointer -DHAVE_CONFIG_H \
  -Isrc/openvpn -Iinclude -Isrc/compat -std=c11 dns_repro.c \
  src/openvpn/libopenvpn.a src/compat/.libs/libcompat.a \
  -lssl -lcrypto -ldl -lnsl -lresolv -lcap-ng -llzo2 -o dns_repro
```

Observed LeakSanitizer output:

```
==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 64 byte(s) in 1 object(s) allocated from:
    #0 ... in malloc
    #1 ... in generate_addrinfo posix/../sysdeps/posix/getaddrinfo.c:1075
    #3 ... in getaddrinfo posix/../sysdeps/posix/getaddrinfo.c:2397
    #5 ... in openvpn_getaddrinfo src/openvpn/socket_util.c:598
    #6 ... in dns_server_addr_parse src/openvpn/dns.c:118
    #7 ... in check_dns_option src/openvpn/options.c:5311
    #8 ... in add_option src/openvpn/options.c:7926
    #9 ... in read_config_string src/openvpn/options_parse.c:440
    #10 ... in main dns_repro.c:63

SUMMARY: AddressSanitizer: 64 byte(s) leaked in 1 allocation(s).
```

## Suggested Fix

Free `ai` before the early `return false` when the address table is full
(or, equivalently, restructure so `freeaddrinfo(ai)` runs on every exit path):

```c
    if (server->addr_count >= SIZE(server->addr))
    {
        freeaddrinfo(ai);   /* fix: release before bailing out */
        return false;
    }
```

## PoC bytes (self-contained)
Self-contained base64 of the crafted option line (decode to a file and feed it
to a build that parses it as a configuration line, or push it inside a
`PUSH_REPLY`):

```
ZG5zIHNlcnZlciA1IGFkZHJlc3MgOS45LjkuOSAyNjIwOjogMjYyMDpmZTo6IDI2MjA6ZmU6OjI5IDI2MjA6ZmU6OmZlOSA5LjkuOS45IDI2MjA6OiAyNjIwOmZlOjogOS45LjkuOQo=
```

One-liner to materialize it:

```
echo 'ZG5zIHNlcnZlciA1IGFkZHJlc3MgOS45LjkuOSAyNjIwOjogMjYyMDpmZTo6IDI2MjA6ZmU6OjI5IDI2MjA6ZmU6OmZlOSA5LjkuOS45IDI2MjA6OiAyNjIwOmZlOjogOS45LjkuOQo=' | base64 -d > dns_poc.txt
```

## Credit

Aisle Research (Ze Sheng (O2Lab & TAMU), Dmitrijs Trizna, Luigino Camastra, Guido Vranken).


## Comment 4757243397

other (CONTRIBUTOR) · cron2 · 2026-06-20T09:56:27Z · https://github.com/OpenVPN/openvpn/issues/1059#issuecomment-4757243397

Seems there is a new generation of AI tools that finds this particular issue...  and just maybe you should run that tool against current master, because we fixed it two days ago.

commit 154e8a520b3bd639fb137c1ba73ce8a80818d08d (master)
Author: saddamr3e <saddamr3e@gmail.com>
Date:   Thu Jun 18 08:18:28 2026 +0200

    dns: Fix memory leak in dns_server_addr_parse

    When the DNS server's address count is already full (exceeds the
    limit of 8), the function returned early without freeing the
    successfully resolved addrinfo struct. Fix this by checking the
    limit before executing the DNS lookup.

    Github: OpenVPN/openvpn#1055

swamping projects' bug trackers with elaborate multipage reports for already-known issues is not helping anything. 
