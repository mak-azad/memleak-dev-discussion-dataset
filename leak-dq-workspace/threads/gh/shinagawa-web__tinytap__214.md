# testing: multi-hour soak run for map, memory, and fd leaks

- URL: https://github.com/shinagawa-web/tinytap/issues/214
- Repo: shinagawa-web/tinytap (language: C)
- State: open; created 2026-08-01T03:23:32Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · shinagawa-web · 2026-08-01T03:23:32Z · https://github.com/shinagawa-web/tinytap/issues/214

Part of v0.7.0 real-hardware bring-up (#198).

## Scope

Every test tinytap has today is short: unit tests, `scripts/test-e2e.sh`, the demo in `scripts/demo.sh`, the CI integration runs. Nothing has ever left tinytap attached for hours. A tool people are asked to run alongside their actual work will be left running for hours, and the failure modes that appear on that timescale are structurally different from the ones a smoke test finds.

Specific things with a plausible long-run failure mode:

- The kernel-side state maps are fixed-size hash maps: `max_entries 10240` at `bpf/tinytap.bpf.c:270` and `:281`, `bpf/tinytap_kprobe.bpf.c:94`, `bpf/tinytap_uprobe.bpf.c:41`. If entries leak — a connection whose `close` is never observed, a tid whose exit tracepoint doesn't fire — the map fills over hours and then quietly stops recording new state. Nothing currently reports map occupancy.
- Userspace parser state has the same shape: per-connection HTTP parser state that is only released on close.
- The TUI already bounds its row count and body budget (`internal/output/tui/model.go:17,66-68`), so that path is designed for it — but designed-for isn't measured.
- `sslWatcher` dynamically attaches uprobes to processes as they appear. Over hours on a busy machine that's a lot of attach/detach churn, and leaked links or fds would accumulate.

## Suggested direction

- Run tinytap for several hours against continuous traffic (a load generator at modest steady rate, plus normal machine activity) and sample over time: RSS, fd count, goroutine count, occupancy of each BPF map, and dropped-event counters if #210 has landed.
- Include connection churn deliberately — many short-lived connections is the pattern most likely to leak map entries, and it's the opposite of what a long-lived-connection load test produces.
- Do it on real hardware, alongside the compatibility-matrix work, not only on the dev VM.
- Decide what tinytap should *do* when a map is full, rather than only measuring that it happens: currently the insert just fails and that state is lost silently.
- Per the project's existing testing convention, report and stop on failure rather than auto-remediating.

## Done when

- A multi-hour run's memory, fd, goroutine, and BPF-map occupancy curves are documented and flat (or the growth is explained).
- Any leak found has its own issue.

## Sub-issues

- #320
- #321
- #322
- #323

Related: #198, #210, #213

## Comment 5312834708

reporter (OWNER) · shinagawa-web · 2026-08-17T06:56:22Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5312834708

## Resources to monitor

Four metrics to sample on a timed interval:

| Metric | What it catches | Source |
|---|---|---|
| RSS | userspace state leak (parser , pairer ) |  |
| fd count | BPF object / uprobe link leak | `ls /proc/PID/fd \| wc -l` |
| `incoming_pending_map` entries | BPF-side per-tid state not cleaned up on close | bpftool |
| `drop_counters` (ringbuf + map_full) | ring buffer overflow; state map insert failures (E2BIG) | bpftool PERCPU_ARRAY, sum across CPUs |

Notes:
- Goroutine count is not reachable without a pprof endpoint; OS thread count (`Threads:` in /proc status) is not a useful proxy.
- The sslWatcher `seen`/`probes`/`payloadProbes` maps accumulate per-pid with no per-process cleanup, but this only matters under TLS traffic — out of scope for a plaintext HTTP soak.
- Drop counts are also reported at shutdown via `reportDrops`, but sampling them periodically during the run shows *when* drops started, not just whether they happened.

## Comment 5312865500

reporter (OWNER) · shinagawa-web · 2026-08-17T07:00:14Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5312865500

## Soak scenarios (CI matrix)

Run each as a separate matrix job (~15 min each, all parallel):

| Scenario | Load generator | Primary resource under test |
|---|---|---|
| `churn` | N parallel curl loops, `--no-keepalive` | `incoming_pending_map` cleanup on close; RSS (parser.streams) |
| `keepalive` | Single persistent connection, many requests | parser `pendingMethods` per-request cleanup on a reused fd |
| `burst` | `ab` / `hey` at high concurrency | `DROP_RINGBUF` — does the ring buffer overflow under load? |
| `large-payload` | Go sendfile server returning multi-MB files | DROP_RINGBUF under per-event payload pressure; iov[0] 2 KiB budget |
| `multi-proc` | Repeatedly start/kill short-lived HTTP server processes | pid-indexed state accumulation (`sslWatcher.seen`; fd count) |

All scenarios sample the same four metrics every 60 s: RSS, fd count, `incoming_pending_map` entries, `drop_counters` (ringbuf + map_full), and upload a TSV artifact at the end.

## Comment 5312883403

reporter (OWNER) · shinagawa-web · 2026-08-17T07:02:18Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5312883403

## Processing paths and resources to monitor

### Kernel-side (BPF)

| Path | Intermediate map (created → deleted) | Ring buffer written |
|---|---|---|
| `accept4` | — | `events` |
| `read` / `recvfrom` / `recvmsg` / `readv` enter | `incoming_pending_map` (tid key, created) | — |
| `read` / `recvfrom` / `recvmsg` / `readv` exit | `incoming_pending_map` (deleted) | `events` |
| `write` / `sendto` / `sendmsg` / `writev` | — | `events` |
| `close` | `incoming_pending_map` (deleted) | `events` |
| `sendfile64` enter | `sendfile_sample_map` (tid key, created) | — |
| `fentry/tcp_sendmsg_locked` | reads `sendfile_sample_map`, writes payload | — |
| `sendfile64` exit | `sendfile_sample_map` (deleted) | `events` |
| `uprobe/ssl_set_fd` | `ssl_fd_map` (pid+ssl key, created) | — |
| `uprobe/ssl_free` | `ssl_fd_map` (deleted) | — |
| `uprobe/ssl_write` / `ssl_write_ex` | — | `ssl_events` |
| `uprobe/ssl_read` enter | `ssl_read_pending_map` (tid key, created) | — |
| `uretprobe/ssl_read` | `ssl_read_pending_map` (deleted) | `ssl_events` |
| `uprobe/ssl_read_ex` enter | `ssl_read_ex_pending_map` (tid key, created) | — |
| `uretprobe/ssl_read_ex` | `ssl_read_ex_pending_map` (deleted) | `ssl_events` |

### Userspace

| State | Lifetime | Cleaned up by |
|---|---|---|
| `Parser.streams` (per connKey) | first data → close event | `Parser.Close(pid, fd)` |
| `Parser.pendingMethods` (per pid+fd) | request line seen → close | `Parser.Close(pid, fd)` |
| `Pairer.pending` (per pid+fd+ssl) | request → paired response or sweep timeout | `Pairer.Close` / `Pairer.Sweep` |
| `sslWatcher.seen` (per pid) | first TLS event → **never** | no per-process cleanup |
| `sslWatcher.probes` (per pid) | uprobe attached → **shutdown only** | `sslWatcher.Close()` |
| `sslWatcher.payloadProbes` (per pid) | uprobe attached → **shutdown only** | `sslWatcher.Close()` |

### What to sample

| Metric | Paths it covers |
|---|---|
| `incoming_pending_map` entry count | read/recvfrom/recvmsg/readv — entry must be 0 after every paired close |
| `ssl_fd_map` entry count | ssl_set_fd/ssl_free balance |
| `ssl_read_pending_map` + `ssl_read_ex_pending_map` entry count | ssl_read enter/uretprobe balance |
| `drop_counters[DROP_RINGBUF]` | `events` and `ssl_events` overflow |
| `drop_counters[DROP_MAP_FULL]` | any hash map hitting max_entries (10240) |
| RSS | `Parser.streams` / `Pairer.pending` growth |
| fd count | `sslWatcher.probes` / `payloadProbes` not released between process exits |

Gaps: `sslWatcher.seen` / `probes` / `payloadProbes` accumulate for the lifetime of tinytap with no per-process cleanup — only observable as fd count and RSS growth under TLS traffic with process churn. Goroutine count is not reachable without a pprof endpoint.

## Comment 5312903717

reporter (OWNER) · shinagawa-web · 2026-08-17T07:04:48Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5312903717

Addendum to the previous comment: the process-level metrics for tinytap itself are missing from the table.

| Metric | Source | What growth means |
|---|---|---|
| RSS | `/proc/PID/status VmRSS` | userspace state accumulation |
| CPU% | `/proc/PID/stat` (utime+stime delta) | capture loop or parser falling behind |
| fd count | `ls /proc/PID/fd \| wc -l` | BPF object / uprobe link leak |

These are the baseline health check for the tinytap process itself, independent of BPF map occupancy. CPU growing over a flat-traffic run would indicate the capture pipeline is not keeping up with the event rate — a separate problem from map leaks but equally important to catch in a soak.

## Comment 5312979944

reporter (OWNER) · shinagawa-web · 2026-08-17T07:13:49Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5312979944

## How to measure whether tinytap is actually working

CPU and RSS tell you something is wrong after the fact; they don't confirm tinytap is capturing correctly. The direct measure is whether output matches input:

| Metric | How to measure |
|---|---|
| Requests sent | count on the load generator side |
| Paired events output | count JSONL lines on tinytap stdout |
| Drops | `drop_counters[DROP_RINGBUF]` + `drop_counters[DROP_MAP_FULL]` |

If requests sent ≈ pairs output and drops = 0, tinytap is working. If pairs output drops while requests keep flowing, something in the pipeline has failed — drops, parser stuck, pairer not flushing — regardless of what CPU and RSS show.

CPU% and fd count are diagnostic inputs, not health signals on their own.

## Comment 5312993337

reporter (OWNER) · shinagawa-web · 2026-08-17T07:15:20Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5312993337

## Server and client for each scenario

**Server**

| Scenario | Server | Reason |
|---|---|---|
| churn / keepalive / burst | `python3 -m http.server` | already used in e2e; no extra CI setup |
| large-payload | Go `http.ServeFile` (already in e2e) | needed to exercise the sendfile path |
| multi-proc | `python3 -m http.server`, killed and restarted in a loop | content doesn't matter; process churn is the point |

**Client (load generator)**

| Scenario | Client | Reason |
|---|---|---|
| churn | `curl --no-keepalive` in a loop, N workers in parallel | each invocation opens a fresh TCP connection |
| keepalive | `curl` default (keepalive on) in a loop | many requests over a single persistent connection |
| burst | `ab` (`apache2-utils`, installable via apt) | higher throughput than a curl loop; no extra download |
| large-payload | `curl` | sufficient for file fetches |
| multi-proc | `curl` | sufficient |

Pair count on the tinytap side is read from stdout JSONL line count, making it straightforward to compare against the request count from each client.

## Comment 5313015509

reporter (OWNER) · shinagawa-web · 2026-08-17T07:17:51Z · https://github.com/shinagawa-web/tinytap/issues/214#issuecomment-5313015509

## System-level overhead

tinytap fires a BPF program on every relevant syscall in the monitored process. Two things to check that are separate from tinytap's own resource usage:

**OS CPU**

Compare total CPU usage (from `/proc/stat`) with and without tinytap running. tinytap's tracepoints add overhead on every `read`, `write`, `close`, etc. — if the machine is under sustained load this overhead is visible system-wide, not just in tinytap's own CPU%.

**Server response latency**

Measure the HTTP server's response time with tinytap attached vs without. If the tracepoints are adding measurable latency per syscall, it shows up here first. A simple proxy: record `curl`'s `time_total` for each request from the load generator and track the distribution over the soak run.

Both should be flat relative to the baseline (tinytap not running). Growth or elevated baseline is a correctness problem for the tool, not just a resource leak.
