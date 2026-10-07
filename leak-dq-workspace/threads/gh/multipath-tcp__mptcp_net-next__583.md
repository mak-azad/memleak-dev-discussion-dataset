# KMemLeak: from `mptcp_sk_clone_init()`

- URL: https://github.com/multipath-tcp/mptcp_net-next/issues/583
- Repo: multipath-tcp/mptcp_net-next (language: C)
- State: open; created 2025-09-05T11:13:49Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · matttbe · 2025-09-05T11:13:49Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583

Our CI just [reported](https://github.com/multipath-tcp/mptcp_net-next/actions/runs/17484970392) this potential leak:

```
unreferenced object 0xffff888119d90c80 (size 3032):
comm "packetdrill", pid 31258, jiffies 4299819414
hex dump (first 32 bytes):
7f 00 00 06 7f 00 00 06 00 00 00 00 ad 97 90 1f  ................
0a 00 07 41 00 00 00 00 00 00 00 00 00 00 00 00  ...A............
backtrace (crc 890e4443):
kmem_cache_alloc_noprof (mm/slub.c:4190 (discriminator 1)) 
sk_prot_alloc.isra.0 (net/core/sock.c:2233 (discriminator 2)) 
sk_clone_lock (net/core/sock.c:2467) 
mptcp_sk_clone_init (net/mptcp/protocol.c:3269) 
subflow_syn_recv_sock (net/mptcp/subflow.c:880 (discriminator 1)) 
tcp_check_req (net/ipv4/tcp_minisocks.c:873) 
tcp_v6_rcv (net/ipv6/tcp_ipv6.c:1840) 
ip6_protocol_deliver_rcu (net/ipv6/ip6_input.c:440) 
ip6_input_finish (net/ipv6/ip6_input.c:492) 
ip6_input (include/linux/rcupdate.h:869) 
ipv6_rcv (include/net/dst.h:474 (discriminator 3)) 
__netif_receive_skb_one_core (net/core/dev.c:6033) 
netif_receive_skb_internal (net/core/dev.c:6239) 
netif_receive_skb (net/core/dev.c:6298) 
tun_rx_batched.isra.0 (include/linux/bottom_half.h:33 (discriminator 1)) 
tun_get_user (drivers/net/tun.c:1950)
```

Similar issues have been seen on NIPA:
* https://netdev-3.bots.linux.dev/vmksft-mptcp-dbg/results/279881/1-mptcp-join-sh/stdout
* https://netdev-3.bots.linux.dev/vmksft-mptcp-dbg/results/280062/1-mptcp-join-sh/stdout

@cpaasch did you manage to reproduce it? A false positive?

## Comment 3273855247

reporter (MEMBER) · matttbe · 2025-09-10T08:19:37Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583#issuecomment-3273855247

It looks like it happened again recently:
* https://github.com/multipath-tcp/mptcp_net-next/actions/runs/17604568587
* https://github.com/multipath-tcp/mptcp_net-next/actions/runs/17586663636
* https://github.com/multipath-tcp/mptcp_net-next/actions/runs/17608702434

@cpaasch : how did you reproduce it on your side?

## Comment 3275731344

other (CONTRIBUTOR) · cpaasch-oai · 2025-09-10T16:47:30Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583#issuecomment-3275731344

Turned out that when I hit it, it was a different leak.

## Comment 3275739972

reporter (MEMBER) · matttbe · 2025-09-10T16:50:44Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583#issuecomment-3275739972

> Turned out that when I hit it, it was a different leak.

Thank you for your reply! Do you mean you had the same calltrace? Or you had an unrelated KMemLeak?

## Comment 3275909391

other (CONTRIBUTOR) · cpaasch-oai · 2025-09-10T17:37:05Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583#issuecomment-3275909391

Unrelated kmemleak... 

## Comment 3523127851

reporter (MEMBER) · matttbe · 2025-11-12T17:42:05Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583#issuecomment-3523127851

Note: this issue still happens from time to time, e.g. https://github.com/multipath-tcp/mptcp_net-next/actions/runs/19303104996/job/55202821360

If someone has an idea how to reproduce this, or help with the debug, do not hesitate to share that :)

## Comment 3647305525

reporter (MEMBER) · matttbe · 2025-12-12T16:37:10Z · https://github.com/multipath-tcp/mptcp_net-next/issues/583#issuecomment-3647305525

FYI, my syzkaller instances can also reproduce the issue, e.g. on top of `export/20251205T155419`:

```
BUG: memory leak
unreferenced object 0xffff8880396c3000 (size 2928):
  comm "softirq", pid 0, jiffies 4295153189
  hex dump (first 32 bytes):
    ac 14 14 aa ac 14 14 aa 00 00 00 00 dc b0 21 4e  ..............!N
    02 00 07 40 00 00 00 00 00 00 00 00 00 00 00 00  ...@............
  backtrace (crc 1247605b):
    kmemleak_alloc_recursive include/linux/kmemleak.h:44 [inline]
    slab_post_alloc_hook mm/slub.c:4953 [inline]
    slab_alloc_node mm/slub.c:5258 [inline]
    kmem_cache_alloc_noprof+0x489/0x6e0 mm/slub.c:5265
    sk_prot_alloc+0x60/0x290 net/core/sock.c:2239
    sk_clone+0x7f/0x1360 net/core/sock.c:2481
    sk_clone_lock include/net/sock.h:1836 [inline]
    mptcp_sk_clone_init+0x36/0x1730 net/mptcp/protocol.c:3507
    subflow_syn_recv_sock+0xcfd/0x1280 net/mptcp/subflow.c:881
    tcp_check_req+0x78e/0x2470 net/ipv4/tcp_minisocks.c:910
    tcp_v4_rcv+0x178c/0x47a0 net/ipv4/tcp_ipv4.c:2247
    ip_protocol_deliver_rcu+0xb7/0x3e0 net/ipv4/ip_input.c:207
    ip_local_deliver_finish+0x3cd/0x690 net/ipv4/ip_input.c:241
    NF_HOOK include/linux/netfilter.h:318 [inline]
    NF_HOOK include/linux/netfilter.h:312 [inline]
    ip_local_deliver+0x1be/0x560 net/ipv4/ip_input.c:262
    dst_input include/net/dst.h:474 [inline]
    ip_rcv_finish net/ipv4/ip_input.c:453 [inline]
    NF_HOOK include/linux/netfilter.h:318 [inline]
    NF_HOOK include/linux/netfilter.h:312 [inline]
    ip_rcv+0x534/0x840 net/ipv4/ip_input.c:573
    __netif_receive_skb_one_core+0x197/0x1e0 net/core/dev.c:6137
    __netif_receive_skb+0x1f/0x120 net/core/dev.c:6250
    process_backlog+0x362/0x13d0 net/core/dev.c:6602
    __napi_poll.constprop.0+0xb7/0x6c0 net/core/dev.c:7666
    napi_poll net/core/dev.c:7729 [inline]
    net_rx_action+0xafc/0x1070 net/core/dev.c:7881

BUG: memory leak
unreferenced object 0xffff888010b29c00 (size 32):
  comm "softirq", pid 0, jiffies 4295153190
  hex dump (first 32 bytes):
    02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00  ................
  backtrace (crc ea16adaf):
    kmemleak_alloc_recursive include/linux/kmemleak.h:44 [inline]
    slab_post_alloc_hook mm/slub.c:4953 [inline]
    slab_alloc_node mm/slub.c:5258 [inline]
    __do_kmalloc_node mm/slub.c:5651 [inline]
    __kmalloc_noprof+0x4e8/0x7e0 mm/slub.c:5664
    kmalloc_noprof include/linux/slab.h:961 [inline]
    kzalloc_noprof include/linux/slab.h:1094 [inline]
    lsm_blob_alloc+0x68/0x90 security/security.c:192
    lsm_sock_alloc security/security.c:4375 [inline]
    security_sk_alloc+0x2f/0xd0 security/security.c:4391
    sk_prot_alloc+0xab/0x290 net/core/sock.c:2248
    sk_clone+0x7f/0x1360 net/core/sock.c:2481
    sk_clone_lock include/net/sock.h:1836 [inline]
    mptcp_sk_clone_init+0x36/0x1730 net/mptcp/protocol.c:3507
    subflow_syn_recv_sock+0xcfd/0x1280 net/mptcp/subflow.c:881
    tcp_check_req+0x78e/0x2470 net/ipv4/tcp_minisocks.c:910
    tcp_v4_rcv+0x178c/0x47a0 net/ipv4/tcp_ipv4.c:2247
    ip_protocol_deliver_rcu+0xb7/0x3e0 net/ipv4/ip_input.c:207
    ip_local_deliver_finish+0x3cd/0x690 net/ipv4/ip_input.c:241
    NF_HOOK include/linux/netfilter.h:318 [inline]
    NF_HOOK include/linux/netfilter.h:312 [inline]
    ip_local_deliver+0x1be/0x560 net/ipv4/ip_input.c:262
    dst_input include/net/dst.h:474 [inline]
    ip_rcv_finish net/ipv4/ip_input.c:453 [inline]
    NF_HOOK include/linux/netfilter.h:318 [inline]
    NF_HOOK include/linux/netfilter.h:312 [inline]
    ip_rcv+0x534/0x840 net/ipv4/ip_input.c:573
    __netif_receive_skb_one_core+0x197/0x1e0 net/core/dev.c:6137
    __netif_receive_skb+0x1f/0x120 net/core/dev.c:6250
    process_backlog+0x362/0x13d0 net/core/dev.c:6602


<<<<<<<<<<<<<<< tail report >>>>>>>>>>>>>>>

    __netif_receive_skb_one_core+0x197/0x1e0
    __netif_receive_skb+0x1f/0x120
    process_backlog+0x362/0x13d0
    __napi_poll.constprop.0+0xb7/0x6c0
    net_rx_action+0xafc/0x1070
BUG: memory leak
unreferenced object 0xffff888010b29c00 (size 32):
  comm "softirq", pid 0, jiffies 4295153190
  hex dump (first 32 bytes):
    02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    01 00 00 00 00 00 00 00 10 00 00 00 00 00 00 00  ................
  backtrace (crc ea16adaf):
    __kmalloc_noprof+0x4e8/0x7e0
    lsm_blob_alloc+0x68/0x90
    security_sk_alloc+0x2f/0xd0
    sk_prot_alloc+0xab/0x290
    sk_clone+0x7f/0x1360
    mptcp_sk_clone_init+0x36/0x1730
    subflow_syn_recv_sock+0xcfd/0x1280
    tcp_check_req+0x78e/0x2470
    tcp_v4_rcv+0x178c/0x47a0
    ip_protocol_deliver_rcu+0xb7/0x3e0
    ip_local_deliver_finish+0x3cd/0x690
    ip_local_deliver+0x1be/0x560
    ip_rcv+0x534/0x840
    __netif_receive_skb_one_core+0x197/0x1e0
    __netif_receive_skb+0x1f/0x120
    process_backlog+0x362/0x13d0


<<<<<<<<<<<<<<< tail report >>>>>>>>>>>>>>>
```

Note that NIPA also had it when running [`mptcp_connect.sh`](https://netdev-3.bots.linux.dev/vmksft-mptcp-dbg/results/398141/2-mptcp-connect-sh/stdout):

```
ok 1 selftests: net/mptcp: mptcp_connect.sh
make[1]: Leaving directory '/home/virtme/testing/wt-12/tools/testing/selftests/net/mptcp'
make: Leaving directory '/home/virtme/testing/wt-12/tools/testing/selftests'
xx__-> echo $?
0
xx__-> echo scan > /sys/kernel/debug/kmemleak
xx__-> echo scan > /sys/kernel/debug/kmemleak && cat /sys/kernel/debug/kmemleak
unreferenced object 0xffff88800c17b340 (size 3040):
  comm "softirq", pid 0, jiffies 4297185802
  hex dump (first 32 bytes):
    0a 00 01 02 0a 00 01 01 00 00 00 00 95 42 89 27  .............B.'
    0a 00 07 41 00 00 00 00 00 00 00 00 00 00 00 00  ...A............
  backtrace (crc eeaaf340):
    kmem_cache_alloc_noprof+0x441/0x650
    sk_prot_alloc.constprop.0+0x4e/0x1b0
    sk_clone+0x4d/0x1140
    mptcp_sk_clone_init+0x33/0x10d0
    subflow_syn_recv_sock+0x9d1/0x16d0
    tcp_check_req+0x4b9/0x20c0
    tcp_v4_rcv+0x1004/0x30a0
    ip_protocol_deliver_rcu+0x82/0x350
    ip_local_deliver_finish+0x35d/0x620
    ip_local_deliver+0x19c/0x470
    ip_rcv+0xc2/0x370
    __netif_receive_skb_one_core+0x108/0x180
    process_backlog+0x3b8/0x13d0
    __napi_poll.constprop.0+0x9b/0x460
    net_rx_action+0x49c/0xd30
    handle_softirqs+0x215/0x610
xx__-> 
```
