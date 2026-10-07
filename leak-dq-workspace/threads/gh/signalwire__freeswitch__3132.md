# Memory leak in bridged calls: `switch_channel_get_partner_uuid_copy()` dups `signal_bond` into the session pool on every CNG frame (OOM under sustained queue/MOH load)

- URL: https://github.com/signalwire/freeswitch/issues/3132
- Repo: signalwire/freeswitch (language: C)
- State: open; created 2026-08-24T19:54:49Z; status ok; passes offcwe

## Issue body

reporter (NONE) · era-brdid-developers · 2026-08-24T19:54:49Z · https://github.com/signalwire/freeswitch/issues/3132

In a bridged call, every received **CNG frame** triggers a ~70-byte allocation in the session's memory pool that is only freed at session destruction. Long-lived bridged calls with a silent direction — queue members listening to MOH, bridged+parked legs, trunks doing VAD/DTX (e.g. Opus DTX), hold — therefore grow process memory continuously (~12 MB/hour per silent leg at 50 fps) until the kernel OOM-kills FreeSWITCH under sustained load.

Real-world impact that led us here: a load test with 500 concurrent inbound queue calls per node (each call = 2 channels on the PBX node, B-leg bridged to a queue server, callers in MOH) killed two 8 GB FreeSWITCH nodes by kernel OOM after ~2 hours (~2.5 GB/h growth per node), with CPU ~99% idle throughout.

### Root cause

Call chain, confirmed live with a gdb breakpoint on `switch_core_session_strdup`:

```
audio_bridge_thread
→ switch_core_session_read_frame        (switch_core_io.c ~367, CNG frame handling / partner media-bug check)
→ switch_core_session_get_partner
→ perform_get_partner                   (switch_core_session.c:195)
→ switch_channel_get_partner_uuid_copy  (switch_channel.c:4851)
→ switch_channel_get_variable_dup(channel, SWITCH_SIGNAL_BOND_VARIABLE, SWITCH_TRUE, -1)
→ switch_core_session_strdup            → allocation in the session pool
```

`switch_channel_get_partner_uuid_copy()` passes `dup=SWITCH_TRUE`, which strdups the value into the **session pool**. Session pools only release at hangup, so every call of this function leaks one duplicate of the partner UUID. Because `switch_core_session_read_frame()` consults the partner for every CNG frame of a bridged call, this runs at frame rate (≈50/s) for as long as one direction is silent.

Heap inspection of a live process showed ~25,000 copies of the same partner UUID string accumulated by a single 8-minute call (≈50/s).

Why it only shows up in "silent" scenarios (all verified empirically on the same call path):

- continuous RTP in both directions → no CNG path → memory flat;
- park **without** bridge → no `signal_bond` set → flat;
- **any** sustained bridge with a silent direction → linear growth (sofia or loopback endpoints alike — no network required).

### To reproduce

Minimal, no SIP involved:

1. Dialplan that `bridge`s to a leg which answers and parks (e.g. via loopback).
2. `originate` ~100 loopback calls into it and keep them up.
3. Watch the freeswitch process RSS: linear growth (~12–13 MB/min at 100 calls in our runs) with CPU idle. Memory only drains at hangup — and even then RSS barely regresses because the APR pool allocator keeps freed blocks on its free-list.

### Expected behavior

Flat memory for stable bridged calls, regardless of silence/CNG.

### Package version / git hash

- Reproduced on the `v1.10` branch, tree at `a88d069d6f` (`1.10.12-release`).
- The same code is present in current `master` (checked 2026-08): `switch_channel_get_partner_uuid_copy()` still calls `switch_channel_get_variable_dup()` with `SWITCH_TRUE`.
- Linux x86_64 (Debian), default build.

### Proposed fix (validated under load)

The dup is unnecessary: the function already holds `channel->profile_mutex` across both the lookup and the `strncpy` into the caller's buffer, and the pool pointer never escapes the function (it is overwritten by `buf` before return; the only in-tree call site is `perform_get_partner()` in switch_core_session.c, which consumes the copied string). All variable-mutation paths take the same `profile_mutex` (created with `SWITCH_MUTEX_NESTED`), so reading the live value under the mutex is safe.

```diff
--- a/src/switch_channel.c
+++ b/src/switch_channel.c
@@ -4852,8 +4852,8 @@ SWITCH_DECLARE(const char *) switch_channel_get_partner_uuid_copy(switch_channel
        const char *uuid = NULL;
 
        switch_mutex_lock(channel->profile_mutex);
-       if (!(uuid = switch_channel_get_variable_dup(channel, SWITCH_SIGNAL_BOND_VARIABLE, SWITCH_TRUE, -1))) {
-               uuid = switch_channel_get_variable_dup(channel, SWITCH_ORIGINATE_SIGNAL_BOND_VARIABLE, SWITCH_TRUE, -1);
+       if (!(uuid = switch_channel_get_variable_dup(channel, SWITCH_SIGNAL_BOND_VARIABLE, SWITCH_FALSE, -1))) {
+               uuid = switch_channel_get_variable_dup(channel, SWITCH_ORIGINATE_SIGNAL_BOND_VARIABLE, SWITCH_FALSE, -1);
        }
 
        if (uuid) {
```

Validation:

- Post-patch, the 100-call reproduction above runs **flat** for 9+ minutes (previously ~15–20 MB/min).
- A/B under real load: 1,000 muted bridged calls split round-robin across two identical nodes — the **patched** node froze at ~400 MB with 1,000 channels up; the **unpatched** node grew at **+90 MB/min** until we stopped the test.
- No functional regressions observed (bridge, MOH, teardown, CDR) at ~50 Hz × 1,000 channels over several hours.

### Additional note (possible follow-up)

`switch_channel_get_variable_dup()`'s **global-variable fallback** (`switch_core_get_variable_pdup`) allocates in the session pool regardless of the `dup` flag, so a global variable named `signal_bond` / `originate_signal_bond` would still leak on this path even with the fix above. A more complete fix might honor `dup=SWITCH_FALSE` in that fallback too (or avoid the per-frame partner lookup in `switch_core_session_read_frame`'s CNG path altogether).

Happy to submit this as a PR if preferred, Tom.

## Comment 5468087223

other (NONE) · raselhowlader · 2026-08-30T10:15:59Z · https://github.com/signalwire/freeswitch/issues/3132#issuecomment-5468087223

**The Bug in Simple Terms**
Every time a bridged call has one silent direction (MOH, parked leg, DTX), FreeSWITCH calls switch_channel_get_partner_uuid_copy() ~50 times per second. Each call **duplicates the partner UUID string into the session memory pool** -- which never frees until hangup. Result: ~12 MB/hour per silent leg, OOM kill under load.

**Apply the Patch (Primary Fix)
Step 1 -- Find your FreeSWITCH source**

`find / -name "switch_channel.c" 2>/dev/null`
> [!NOTE]
>  Usually: /usr/src/freeswitch/src/switch_channel.c


**Locate the exact lines**
`grep -n "switch_channel_get_variable_dup" /usr/src/freeswitch/src/switch_channel.c | grep -i "signal_bond"`

**Apply the fix**
`cd /usr/src/freeswitch`
`cp src/switch_channel.c src/switch_channel.c.bak.$(date +%Y%m%d)`

**Edit the file -- find this block around line 4852:**
`grep -n "SIGNAL_BOND_VARIABLE" src/switch_channel.c | grep "variable_dup"`

**Apply the 2-line fix (SWITCH_TRUE → SWITCH_FALSE)**

BEFORE (leaking)
```c
- if (!(uuid = switch_channel_get_variable_dup(channel,
SWITCH_SIGNAL_BOND_VARIABLE, SWITCH_TRUE, -1))) {
- uuid = switch_channel_get_variable_dup(channel,
SWITCH_ORIGINATE_SIGNAL_BOND_VARIABLE, SWITCH_TRUE, -1);
``` 
AFTER (fixed)
```c
+ if (!(uuid = switch_channel_get_variable_dup(channel,
SWITCH_SIGNAL_BOND_VARIABLE, SWITCH_FALSE, -1))) {
+ uuid = switch_channel_get_variable_dup(channel,
SWITCH_ORIGINATE_SIGNAL_BOND_VARIABLE, SWITCH_FALSE, -1);
``` 

After that rebuild and restart hope its will work!



