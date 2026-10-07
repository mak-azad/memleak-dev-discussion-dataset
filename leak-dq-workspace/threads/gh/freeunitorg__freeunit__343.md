# port: an abandoned fragment stream leaks its descriptor and pool memory

- URL: https://github.com/freeunitorg/freeunit/issues/343
- Repo: freeunitorg/freeunit (language: C)
- State: open; created 2026-09-13T12:28:16Z; status ok; passes offcwe

## Issue body

reporter (NONE) · andypost · 2026-09-13T12:28:16Z · https://github.com/freeunitorg/freeunit/issues/343

## Summary

A fragmented port message whose first fragment arrives and whose remaining fragments never do leaks both a file descriptor and pool memory, permanently, with no bound on how many such streams a peer may leave outstanding.

## Mechanism

A message with `nf=0, mf=1` and a `(stream, pid)` key not already present starts a fragment stream: `nxt_port_frag_start()` copies the message — descriptors included — into an `fmsg` held in `port->frags`, and the original's `fd[]` is cleared so nothing else reclaims them.

Nothing ever completes it. `port->frags` is referenced nowhere outside `src/nxt_port_socket.c`, so `nxt_port_close()` does not walk it either; the descriptors and the ~100 bytes of pool memory per pending stream live as long as the port does.

The `nf`/`mf` bits are two bits of a 16-byte header the sender chooses, and an application holds the write end of the router's main port (`src/nxt_application.c:1719`), so a compromised application can open one such stream per message and never complete any of them.

This is adjacent to the descriptor leak fixed in #342 but was deliberately left out of it: that fix closes what nothing takes ownership of, whereas here `fmsg` *does* take ownership and simply never gives it up. Closing on this path would be wrong — the descriptors legitimately belong to a stream that may still complete.

## What a fix needs

A decision rather than a close:

1. **A cap on outstanding fragment streams per port.** Exceeding it should route to `fmsg_failed`, which now closes descriptors correctly. The number needs choosing, and it should be checked first whether any legitimate fragmented message carries a descriptor at all — if none does, refusing descriptors on a fragment start is a stronger and simpler rule than a cap.
2. **Teardown of `port->frags` in `nxt_port_close()`**, closing descriptors and freeing the pool allocations for streams that were never completed. This is needed regardless of the cap, since a port can close with legitimate fragments in flight.

A time-based expiry is a third option but adds a timer to a hot structure; a cap plus teardown is likely enough.

## Note

Also worth confirming while in here: `msg->cancelled` is only ever set to 0 (`src/nxt_port_socket.c` and `src/nxt_port_rpc.c`), so every `cancelled` branch in the dispatcher is dead code. If that is intentional the branches can go; if something was meant to set it, that is its own bug.

