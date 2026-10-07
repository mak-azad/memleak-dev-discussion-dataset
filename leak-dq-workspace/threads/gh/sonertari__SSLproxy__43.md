# FD leak in passthrough mode

- URL: https://github.com/sonertari/SSLproxy/issues/43
- Repo: sonertari/SSLproxy (language: C)
- State: open; created 2022-05-30T16:27:04Z; status ok; passes offcwe

## Issue body

reporter (NONE) · rakeshbansod · 2022-05-30T16:27:04Z · https://github.com/sonertari/SSLproxy/issues/43

I added a few URLs in the passthrough mode.
I am noticing that when there is more traffic on the passthrough sites, the open fd count for SSLProxy process keep on increasing rapidly and a time comes when the system is out of file descriptors.
Internet stops working until the SSLProxy process is restarted.
I am using SSLProxy on openWRT.
Anyone else facing this issue?

## Comment 1141410548

maintainer (OWNER) · sonertari · 2022-05-30T18:46:40Z · https://github.com/sonertari/SSLproxy/issues/43#issuecomment-1141410548

This might as well be a bug in sslproxy. But we close the file descriptors of the original protocol in  protopassthrough_engage(). And the fds of the passthrough connection is closed when it is being terminated. I have checked memory leaks using valgrind, but I am not sure about fds now.

So I think it may be something else. For example, it may be due to the URLs being connected, which may be using persistent connections.

Can you enable the DEBUG_PROXY switch in Mk/main.mk, recompile, and start sslproxy with the `-D4` option, which will cause sslproxy to print very verbose debug logs. Perhaps this can help you understand the reason for this issue. You can post those logs here if you want.
