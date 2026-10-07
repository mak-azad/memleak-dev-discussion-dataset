# socket leak on tcpconnect() timeout

- URL: https://github.com/sustrik/libmill/issues/181
- Repo: sustrik/libmill (language: C)
- State: open; created 2018-02-17T13:43:53Z; status ok; passes offcwe

## Issue body

reporter (NONE) · majek · 2018-02-17T13:43:53Z · https://github.com/sustrik/libmill/issues/181

If I read this code right:
https://github.com/sustrik/libmill/blob/2dd13ae8a1e4c9b5b89670f813a185dd51c43a66/tcp.c#L209

```
    int rc = connect(s, (struct sockaddr*)&addr, mill_iplen(addr));
    if(rc != 0) {
        mill_assert(rc == -1);
        if(errno != EINPROGRESS)
            return NULL;
        rc = fdwait(s, FDW_OUT, deadline);
        if(rc == 0) {
            errno = ETIMEDOUT;
            return NULL;
        }
```
On fdwait() timeout, the "s" never gets "closed()".
