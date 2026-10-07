# A fifth simultaneously deferred device close is dropped (handle leaked)

- URL: https://github.com/hardcoreerik/esp-rtl-sdr/issues/35
- Repo: hardcoreerik/esp-rtl-sdr (language: C++)
- State: open; created 2026-09-29T03:00:03Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · hardcoreerik · 2026-09-29T03:00:03Z · https://github.com/hardcoreerik/esp-rtl-sdr/issues/35

**Where:** `defer_device_close()` in `src/esp_rtl_sdr.cpp`; `kMaxDeferredClose = 4`.

**What happens:** when a control transfer never completes, the device close is parked in a 4-slot list and retried by the client task. If a fifth close is parked while all four slots are still occupied, the code logs `device close deferred list full: handle leaked` and drops it.

**Verified:** yes, by reading the code. It needs five stuck closes at once, so it is very unlikely in practice.

**Suggested fix:** grow the list (or make it a queue) and log the high-water mark.

Found by CodeRabbit's automated review of #29 and triaged while preparing 0.9.1. Deferred from 0.9.1 because the fix changes runtime behaviour on V4/V4L hardware and needs a hardware retest first.

