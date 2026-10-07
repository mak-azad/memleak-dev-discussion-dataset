# pointer being freed was not allocated

- URL: https://github.com/haywire/haywire/issues/130
- Repo: haywire/haywire (language: C)
- State: open; created 2017-05-17T16:43:24Z; status ok; passes main

## Issue body

reporter (NONE) · jwoertink · 2017-05-17T16:43:24Z · https://github.com/haywire/haywire/issues/130

Maybe this is related to #129 or possibly #108? I setup a new machine and started fresh, but now I get this error:

```
Added route /
Address: 0.0.0.0
Port: 3000
Threads: 0
Balancer: ipc
Parser: http_parser
TCP No Delay: on
Listen backlog: 128
Maximum request size: 1048576
Listening...
malloc: *** error for object 0x7fff5cb22318: pointer being freed was not allocated
*** set a breakpoint in malloc_error_break to debug
Program received and didn't handle signal IOT (6)
```

This only happens when a client connects to the server. Booting it works fine.
