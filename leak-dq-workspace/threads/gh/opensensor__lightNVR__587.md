# [0.41.x / 0.42.4] Heap corruption (malloc(): corrupted top size) causes SIGABRT/core dump and container restart

- URL: https://github.com/opensensor/lightNVR/issues/587
- Repo: opensensor/lightNVR (language: C)
- State: open; created 2026-09-03T19:17:38Z; status ok; passes offcwe

## Issue body

reporter (NONE) · DevlTz · 2026-09-03T19:17:38Z · https://github.com/opensensor/lightNVR/issues/587

## Summary

Hi @matteius!

After upgrading my Docker deployment to **LightNVR 0.41.4**, I started noticing occasional web UI stalls where refreshing the page would remain on the loading screen for an unusually long time.

Initially, I thought this was only a frontend/web issue. However, after checking the Docker state, LightNVR logs, and systemd coredumps, I confirmed that the **main LightNVR process is actually aborting and being restarted by Docker**.

The most relevant error is:

```text
malloc(): corrupted top size
```

followed by:

```text
Aborted (core dumped) /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
```

A preserved systemd core dump confirms that LightNVR terminated with **SIGABRT (signal 6)**.

---

## Environment

- **LightNVR:** `0.41.4`
- **Build date reported by LightNVR:** `2026-09-02`
- **Deployment:** Docker
- **Docker restart policy:** `unless-stopped`
- Approximately **54 configured streams**
- `max_streams=60`
- API/object detection enabled
- Detection interval: mostly `40s`
- External detection API configured

Docker reported:

```text
Status=running
Running=true
Restarting=false
ExitCode=0
OOMKilled=false
RestartCount=1
```

System resources were also checked after the incident:

```text
LightNVR memory usage: ~1.67 GiB
Container memory limit: 64 GiB
Host available memory: ~74 GiB
Root filesystem usage: ~43%
Recording/data filesystem usage: ~42%
```

The following command returned no OOM, killed-process, or kernel segfault events:

```bash
dmesg -T | grep -Ei 'oom|out of memory|killed process|segfault'
```

So this does **not currently appear to be caused by OOM or disk exhaustion**.

---

## Observed sequence before the crash

Shortly before the process aborted, LightNVR started reporting that its own health endpoint was becoming slow:

```text
[2026-09-03 14:07:05.863] [ERROR] [HealthCheck] Health check curl failed: Timeout was reached
[2026-09-03 14:07:05.881] [WARN] [HealthCheck] Health check failed (consecutive failures: 4)
[2026-09-03 14:07:05.881] [WARN] [HealthCheck] Health endpoint remains slow but the web event loop is alive; leaving the listener intact and retrying without an in-process restart
```

This matches what I was seeing from the browser: occasionally an `F5`/reload would remain on the LightNVR loading screen for much longer than usual.

Detection activity continued during this period.

For example:

```text
[2026-09-03 14:07:10.077] [INFO] [Detection] Running detection (interval=40s, elapsed=100s, model=api-detection)

[2026-09-03 14:07:10.296] [WARN] [Detection] API Detection (snapshot): Failed to get snapshot from go2rtc for stream [redacted]

[2026-09-03 14:07:10.296] [INFO] [Detection] go2rtc snapshot unavailable, falling back to frame decode

[2026-09-03 14:07:10.296] [ERROR] [Detection] CURL request failed for snapshot: Timeout was reached
```

A few moments later, the following appeared:

```text
malloc(): corrupted top size
```

The main LightNVR process then aborted:

```text
/bin/start.sh: line 10: 58 Aborted (core dumped) /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
Cleaning up processes...
```

Immediately afterwards, container initialization started again.

---

## Docker restart behavior

The container uses the following restart policy:

```text
RestartPolicy={"Name":"unless-stopped","MaximumRetryCount":0}
```

Because of this, Docker automatically starts LightNVR again after the process aborts.

This initially made the problem appear to be only a temporary web UI outage.

The observed behavior from the operator side is approximately:

1. Web UI becomes slow.
2. Page refresh remains on the loading screen.
3. Web UI becomes temporarily unavailable.
4. LightNVR process aborts.
5. Docker restarts the container.
6. LightNVR eventually becomes available again.

---

## Core dump confirmation

The host is configured to use `systemd-coredump`, and the crash was successfully preserved.

`coredumpctl info` reports:

```text
PID: 1387032 (lightnvr)
UID: 0 (root)
GID: 0 (root)
Signal: 6 (ABRT)
Timestamp: Thu 2026-09-03 14:07:11 -03
Command Line: /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
Executable: /usr/bin/lightnvr
Message: Process 1387032 (lightnvr) of user 0 dumped core.
```

The basic stack trace currently provided by `coredumpctl` is:

```text
Stack trace of thread 165:
#0  0x00007f2928fbffac n/a (/usr/lib/x86_64-linux-gnu/libc.so.6)
#1  0x0000000000000000 n/a (n/a)
```

The actual core dump has been preserved locally.

I am intentionally **not attaching the raw core dump publicly**, since process memory may contain RTSP URLs, camera credentials, internal addresses, configuration data, or other sensitive information.

I can provide a sanitized GDB backtrace if that would help investigate the issue.

---

## Another crash on the same day

There is also another preserved LightNVR SIGABRT core dump from earlier on the same day:

```text
PID: 3428740 (lightnvr)
Signal: 6 (ABRT)
Timestamp: Thu 2026-09-03 09:03:31 -03
Command Line: /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
Executable: /usr/bin/lightnvr
```

I cannot yet confirm whether this earlier crash has the same root cause, so I am mentioning it only as additional context.

The host also contains historical LightNVR coredump entries from older deployments, mostly **SIGABRT (signal 6)** with a few **SIGSEGV (signal 11)** occurrences.

Because of that, I do **not** want to assume that the underlying memory issue necessarily originated in `0.41.4`.

However, the crash described in this issue definitely occurred while running **LightNVR 0.41.4**, and the log explicitly reported:

```text
malloc(): corrupted top size
```

---

## Actual behavior

During normal operation, the LightNVR process eventually reaches:

```text
malloc(): corrupted top size
```

and terminates with:

```text
SIGABRT / core dump
```

Docker then automatically restarts the entire LightNVR container.

---

## Expected behavior

Failures such as:

- slow or unavailable cameras;
- go2rtc snapshot timeouts;
- detection API timeouts;
- slow health endpoints;
- detection worker delays;

should be isolated and handled gracefully without corrupting the LightNVR process heap or terminating the complete NVR process.

---

## Impact

The crash affects the **entire LightNVR process**, rather than only the individual camera, stream, detection request, or worker experiencing a problem.

For an NVR deployment, this causes temporary service interruption.

Because Docker automatically restarts the container with `restart: unless-stopped`, the underlying native process crash can easily be hidden from the operator.

Without checking the logs, `RestartCount`, or system coredumps, the incident initially looks like a temporary web UI/loading problem.

---

## Additional observations

Around the same period, some detection jobs configured with a `40s` interval were executing with considerably larger elapsed times.

Examples:

```text
interval=40s, elapsed=80s
interval=40s, elapsed=88s
interval=40s, elapsed=100s
```

There were also occasional go2rtc snapshot timeouts:

```text
[ERROR] [Detection] CURL request failed for snapshot: Timeout was reached

[WARN] [Detection] API Detection (snapshot): Failed to get snapshot from go2rtc

[INFO] [Detection] go2rtc snapshot unavailable, falling back to frame decode
```

The fallback mechanism usually continued working correctly.

I don't know whether these conditions are related to the heap corruption, but I am including them because they were occurring shortly before the crash.

---

## Reproduction

I do not yet have a deterministic minimal reproducer.

The issue occurred during normal operation of a relatively large deployment with approximately **54 configured streams** and API detection enabled.

The observed sequence was:

```text
Normal operation
        ↓
Web / health endpoint becomes slow
        ↓
Multiple health check timeouts
        ↓
Concurrent detection activity
        ↓
Some go2rtc snapshot timeouts
        ↓
malloc(): corrupted top size
        ↓
SIGABRT + core dump
        ↓
Docker restarts LightNVR
        ↓
Service becomes available again
```

I will continue monitoring the deployment and can provide additional logs, another crash occurrence, or a sanitized GDB backtrace if useful.

## Comment 5531101910

other (CONTRIBUTOR) · matteius · 2026-09-03T19:36:48Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5531101910

Thanks for preserving both cores and for not uploading raw process memory. The log timing narrows the workload, but `malloc(): corrupted top size` is emitted when glibc later detects an earlier write, so the two-frame libc trace cannot identify the corrupting LightNVR path.

Could you collect an argument-redacted all-thread trace for both PIDs?

```gdb
sudo coredumpctl debug 1387032
set pagination off
set print frame-arguments none
thread apply all bt
info sharedlibrary
quit

sudo coredumpctl debug 3428740
set pagination off
set print frame-arguments none
thread apply all bt
info sharedlibrary
quit
```

`set print frame-arguments none` suppresses function argument values that could contain URLs or credentials. Please also share the non-memory metadata from `sudo coredumpctl info 1387032` and `sudo coredumpctl info 3428740`, particularly the core size/storage and whether either core was truncated.

If GDB cannot find LightNVR symbols, extract the matching 0.41.4 executable first and open the dumped core with it:

```bash
docker create --name lightnvr-debug ghcr.io/opensensor/lightnvr:0.41.4
docker cp lightnvr-debug:/bin/lightnvr ./lightnvr-0.41.4
docker rm lightnvr-debug
sudo coredumpctl dump 1387032 --output=lightnvr-1387032.core
gdb ./lightnvr-0.41.4 ./lightnvr-1387032.core
```

Please continue to keep the raw cores private. We are keeping this issue open pending those traces; the observed health/snapshot timeouts alone are not enough to claim a heap-corruption fix.


## Comment 5531559479

reporter (NONE) · DevlTz · 2026-09-03T20:15:11Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5531559479

### Update: requested all-thread traces and core metadata

Thanks! I collected the requested argument-redacted all-thread traces for both preserved SIGABRT cores.

The direct `coredumpctl debug` approach could not locate the LightNVR executable on the host, so I extracted the matching executable from:

```text
ghcr.io/opensensor/lightnvr:0.41.4
```

The extracted executable is:

```text
ELF 64-bit LSB, x86-64, dynamically linked
BuildID: bc386c0e0c9c6cd3505f8286a5f59552b8992542
not stripped
```

I then opened each dumped core with that executable and collected:

```gdb
set pagination off
set print frame-arguments none
thread apply all bt
info sharedlibrary
```

The LightNVR symbols are resolving in both traces.

I reviewed both traces before attaching them and did not find obvious RTSP/HTTP URLs, credentials, internal camera identifiers, or private IPv4 addresses in the output.

---

## PID 1387032

```text
Signal: SIGABRT (6)
Timestamp: 2026-09-03 14:07:11 -03
Command Line: /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
Executable: /usr/bin/lightnvr
Current thread: LWP 165
Exported core size: ~1.6 GiB
Stored compressed core size: 251 MiB
Storage: /var/lib/systemd/coredump/core.lightnvr.[redacted].1387032.[redacted].lz4
```

`systemd-coredump` did not report this preserved core as truncated.

---

## PID 3428740

```text
Signal: SIGABRT (6)
Timestamp: 2026-09-03 09:03:31 -03
Command Line: /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
Executable: /usr/bin/lightnvr
Current thread: LWP 141
Exported core size: ~1.7 GiB
Stored compressed core size: 294 MiB
Storage: /var/lib/systemd/coredump/core.lightnvr.[redacted].3428740.[redacted].lz4
```

`systemd-coredump` did not report this preserved core as truncated.

---

## Shared libraries

The matching LightNVR executable symbols resolve, but GDB cannot load symbols for the container's shared libraries from the host environment:

```text
warning: Could not load shared library symbols for 160 libraries
```

The requested `info sharedlibrary` output is included in both attached traces.

I have not attempted to reconstruct the container filesystem as a GDB sysroot yet, since the requested LightNVR all-thread traces are resolving. I can do that as a follow-up if useful.

---

## Attached

- `lightnvr-1387032-gdb.txt`
- `lightnvr-3428740-gdb.txt`

The raw core dumps remain private as requested.

[lightnvr-1387032-gdb.txt](https://github.com/user-attachments/files/31809170/lightnvr-1387032-gdb.txt)
[lightnvr-3428740-gdb.txt](https://github.com/user-attachments/files/31809169/lightnvr-3428740-gdb.txt)

## Comment 5531722495

other (CONTRIBUTOR) · matteius · 2026-09-03T20:29:24Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5531722495

Thanks — these traces materially narrowed this down.

Both cores show the same high-concurrency workload: many API detection workers are simultaneously inside `detect_objects_api_snapshot`, `store_detections_with_source`, and `filter_detections_by_stream_objects`, with other workers encoding JPEG snapshots.

That review exposed a real thread-safety defect in the label-filter path. `filter_detections_by_stream_objects` used `strtok()` from many worker threads. Because `strtok()` keeps shared parsing state, one worker could replace another worker's cursor; the first worker could then continue tokenizing—and writing delimiters into—the second worker's stack buffer. Unrelated `strtok()` calls elsewhere could interfere in the same way.

I replaced every remaining `strtok()` call in `src/` with per-call `strtok_r()` state and added an eight-thread regression that repeatedly filters two different camera label lists in parallel:

- commit: https://github.com/opensensor/lightNVR/commit/36c6233b
- focused parallel regression: passes
- complete native suite: 125/125 passes

This is a confirmed undefined-behavior bug in exactly the concurrent path visible in both cores, but the current traces stop in libc at `abort()`; they do not prove it caused these two heap-corruption aborts. I am therefore keeping this issue open for caller-trace and deployment validation.

A sysroot-backed current-thread trace from each existing core would tell us whether glibc can unwind through the aborting allocation. The raw cores should remain private. One safe way to supply the matching container libraries is:

```bash
debug_root=$(mktemp -d)
debug_container=$(docker create ghcr.io/opensensor/lightnvr:0.41.4)
docker export "$debug_container" | tar -C "$debug_root" -xf -
docker rm "$debug_container"
printf '%s\n' "$debug_root"
```

Then, for each core:

```gdb
gdb ./lightnvr-0.41.4 ./lightnvr-CORE.core
set pagination off
set print frame-arguments none
set sysroot /absolute/path/printed/above
set solib-search-path /absolute/path/printed/above/lib/x86_64-linux-gnu:/absolute/path/printed/above/usr/lib/x86_64-linux-gnu:/absolute/path/printed/above/lib:/absolute/path/printed/above/usr/lib
thread 1
bt
info sharedlibrary
quit
```

Please review the output before attaching it, as before. `set print frame-arguments none` keeps argument values out of the backtrace.

## Comment 5532108810

other (CONTRIBUTOR) · matteius · 2026-09-03T21:03:50Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5532108810

Please try `0.41.6` @DevlTz 

## Comment 5544640283

reporter (NONE) · DevlTz · 2026-09-04T18:11:50Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5544640283

Thanks! I tested the newer builds in the production deployment and got two different behaviors.

## `0.41.7`

I first updated the deployment to:

```text
ghcr.io/opensensor/lightnvr:0.41.7
```

The container itself remained running and did not crash:

```text
Status=running
RestartCount=0
OOMKilled=false
```

However, LightNVR did not become operational.

The Docker healthcheck repeatedly failed with:

```text
curl: (7) Failed to connect to localhost:8080 after 0 ms:
Could not connect to server
```

There was no listener on the expected LightNVR/go2rtc ports while the startup was stalled.

The startup sequence completed an initial read-only database initialization, but when the main LightNVR process started, it stopped progressing after:

```text
Initializing database at path: /var/lib/lightnvr/data/database/lightnvr.db
Backup path set to: /var/lib/lightnvr/data/database/lightnvr.db.bak
Database file already exists
```

The main process remained alive for several minutes without opening the web listener.

While investigating the live process, I confirmed that it was performing heavy reads against the SQLite database:

```text
FD 5 -> /var/lib/lightnvr/data/database/lightnvr.db
Database size: ~1.4 GiB
```

At one point the process was observed in `D` state inside the XFS read path:

```text
generic_file_buffered_read
xfs_file_buffered_read
xfs_file_read_iter
new_sync_read
vfs_read
ksys_pread64
```

Further sampling showed that the process was not permanently stuck on one specific read; the database read counters continued advancing heavily.

Because this is a production camera deployment and the web service had remained unavailable for too long, I rolled back rather than leaving the cameras inaccessible.

---

## Rollback to `0.41.6`

After downgrading to:

```text
ghcr.io/opensensor/lightnvr:0.41.6
```

the system came up quickly and initially became healthy:

```text
Image=ghcr.io/opensensor/lightnvr:0.41.6
Status=running
Health=healthy
RestartCount=0
OOMKilled=false
```

API detection and recording also resumed normally.

However, after several minutes under the normal production workload, the web service became completely unresponsive again.

The container stayed alive:

```text
Image=ghcr.io/opensensor/lightnvr:0.41.6
Status=running
Health=unhealthy
RestartCount=0
OOMKilled=false
```

This was **not** another SIGABRT/core dump.

I tested the HTTP service directly from inside the LightNVR container, so the external browser/reverse-proxy path was bypassed.

All three endpoints accepted the TCP connection immediately but returned no HTTP response before a 15-second timeout:

```text
GET /
connect=0.000231s
TTFB=none
total=15.001964s
HTTP=000
0 bytes received

GET /api/health
connect=0.000215s
TTFB=none
total=15.001662s
HTTP=000
0 bytes received

GET /api/streams
connect=0.000259s
TTFB=none
total=15.001509s
HTTP=000
0 bytes received
```

So the TCP listener was still accepting connections, but the application was not producing an HTTP response.

- The logs show that `/api/health` was still responding successfully shortly before the stall:

```text
15:01:40  Health check handled successfully
```

Then the system started degrading:

```text
15:01:41  API detection snapshot timeout
15:01:45  API detection snapshot timeout
15:01:53  API detection snapshot timeout
15:01:55  first health-check timeout
```

After that, the health endpoint did not recover and reached at least 15 consecutive failures:

```text
Health check curl failed: Timeout was reached
Health check failed (consecutive failures: ...)
Health endpoint remains slow but the web event loop is alive;
leaving the listener intact and retrying without an in-process restart
```

One additional observation: while the web service was stalled, the container process list showed multiple simultaneous Docker healthcheck processes:

```text
curl -f http://localhost:8080/
```

with older instances still alive for several minutes.

They appeared approximately one healthcheck interval apart, so timed-out healthcheck curls may be accumulating during the stall. I am treating this as a possible secondary effect rather than assuming it is the original cause.

Resource usage at the stalled state was approximately:

```text
LightNVR memory: ~802 MiB / 64 GiB
RestartCount: 0
OOMKilled: false
Container block I/O: ~157 GB read / 25.9 GB written
```

The high block-I/O figure also stood out.

Because the web interface had become unavailable in production, I restarted the container after collecting the stalled-state information.

I preserved the relevant logs locally.

At this point:

- `0.41.7` did not become operational during the observed startup window and remained stuck in heavy database initialization/read activity.
- `0.41.6` started normally, but reproduced the web-unresponsiveness symptom after several minutes under the normal workload.
- I have **not** observed another `malloc(): corrupted top size` / SIGABRT/core dump yet on these validation runs.

So I am treating the current `0.41.6` result as a reproduction of the **web-unresponsiveness** issue, not yet as proof that the original heap-corruption failure has reproduced.

## Comment 5544868082

reporter (NONE) · DevlTz · 2026-09-04T18:31:13Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5544868082

### Additional `0.41.6` database startup data

I captured the main process while the second database initialization was still not progressing past:

```text
Initializing database at path: /var/lib/lightnvr/data/database/lightnvr.db
Backup path set to: /var/lib/lightnvr/data/database/lightnvr.db.bak
Database file already exists
```

After approximately 4 minutes 40 seconds, the process was still in `D` state:

```text
PID      STATE  ELAPSED
1594631  D      04:40
```

At that instant, `/proc/<pid>/syscall` showed:

```text
17 0x5 ... 0x1000 0x3fe5f000 ...
```

On this x86-64 host, syscall 17 is `pread64()`, so the thread was blocked in a 4096-byte read from fd 5 at approximately the 1022 MiB offset.

fd 5 had already been confirmed as:

```text
/var/lib/lightnvr/data/database/lightnvr.db
```

The process I/O counters at that point were:

```text
rchar: 182799136
syscr: 44779
read_bytes: 86892544
```

I also inspected the SQLite file itself to better understand what the startup path is dealing with.

```text
page_size:      4096
page_count:     364281
freelist_count: 162561
auto_vacuum:    0
```

That corresponds to approximately:

```text
database file:  ~1423 MiB
freelist:       ~635 MiB
free pages:     ~44.6%
```

The AUTOINCREMENT high-water marks are:

```text
detections:    2777484
recordings:     786414
audit_events:   572528
streams:            75
```

These are historical sequence values, not current row counts.

I then ran `dbstat` to see where the allocated database space is concentrated. The largest objects were:

```text
audit_events                              280.21 MiB
idx_audit_events_target                    53.36 MiB
idx_audit_events_action_outcome            34.36 MiB
sqlite_autoindex_audit_events_1             27.60 MiB
idx_audit_events_occurred                   18.53 MiB
idx_audit_events_principal                  16.28 MiB

detections                                  93.36 MiB
idx_detections_camera_label_time_id         30.88 MiB
idx_detections_camera_source_time_id        28.00 MiB
idx_detections_camera_time_id               26.52 MiB
idx_detections_external_interval            22.82 MiB
idx_detections_stream_timestamp             20.10 MiB
idx_detections_stream_label                 19.48 MiB
idx_detections_stream                       16.79 MiB
```

Among the top `dbstat` entries, the `audit_events` table and its indexes account for roughly 430 MiB, while `detections` and its listed indexes account for roughly 296 MiB.

So the database size does not appear to be driven mainly by the 56 current stream configurations or by recording rows themselves. A significant portion is historical audit/detection data and their indexes, with another ~635 MiB currently on SQLite's freelist.

I am not assuming that any of those tables are the cause of the startup delay, but this gives a more concrete place to profile: whatever runs immediately after `Database file already exists`, especially if that path performs schema/index checks, cleanup, consistency work, or queries over `audit_events` / `detections`.

If useful, I can test an instrumented build here. Adding timing logs around each database initialization stage would let me report exactly which operation is consuming the startup time on this production-sized database.

## Comment 5544890338

other (CONTRIBUTOR) · matteius · 2026-09-04T18:33:03Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5544890338

Thanks, this additional data narrows this down substantially. I inspected both supplied all-thread traces and the relevant 0.41.4 through 0.41.7 code paths. I believe the ticket currently contains two separate failure modes.

### 1. Original heap corruption

The concurrent detection label filters were using non-thread-safe strtok(). One worker could resume tokenizing another worker buffer, which is undefined behavior and can plausibly cause the observed heap damage. Commit 36c6233b changes these paths to strtok_r() and adds a multithreaded regression test; it is included in 0.41.6 and 0.41.7.

The abort stacks cannot prove where the corrupting write occurred, so I would still like a meaningful 0.41.6+ burn-in before considering the SIGABRT resolved.

### 2. Startup delay and later web unresponsiveness

The startup data now identifies the first part quite clearly. Immediately after the Database file already exists message, the main initialization performs a synchronous PRAGMA quick_check before the HTTP listener is bound. There is no progress log before sqlite3_step(), so a long check looks exactly like this. The D state, pread64 against the database, and advancing reads are direct confirmation. This code is identical in 0.41.6 and 0.41.7.

For an immediate test/workaround:

    [database]
    startup_check = off

That skips the automatic boot check; a controlled offline PRAGMA quick_check can still be run separately.

The runtime web stall has another strong amplification path:

- Every visible player creates its own 30-second telemetry timer.
- A 54-stream live grid therefore emits bursts of roughly 54 POST /api/telemetry/player requests.
- Each request repeats authentication, camera lookup, and authorization work, then persists an allowed live.view authorization audit event.
- Audit and detection writes share the global database mutex.
- HTTP handlers are all submitted to the shared libuv worker pool, so a database lock convoy can make TCP connects succeed while normal pages and health endpoints receive no response.

One open 54-camera dashboard can generate about 155,520 allowed telemetry audit rows per day. The new dbstat result showing roughly 430 MiB allocated to audit_events plus its indexes confirms that this traffic is material, while the 635 MiB freelist explains why deleting history did not shrink the file or make the startup scan cheap.

The supplied cores also support high contention: 91 of 112 threads in one and 103 of 112 in the other were waiting at the same low-level lock, with many callers in database, authorization, telemetry, and detection paths. That does not by itself prove the later live hang, since those cores came from the aborts, but it is consistent with the same bottleneck.

Useful next validation:

1. Run 0.41.6 or 0.41.7 with startup_check = off.
2. Keep the 54-camera live dashboard closed for a comparison run, or temporarily disable player telemetry.
3. If the web service stalls again, capture a live thread apply all bt before restarting it.
4. Query audit counts grouped by action and outcome; I expect live.view / allowed to be prominent.

The likely code fixes are to batch or jitter player telemetry, avoid durable per-sample auditing of successful high-frequency telemetry authorization, bound or partition HTTP work, provide a database-independent liveness path, and reduce use of the single shared SQLite handle/mutex. The Docker health check should also use exec form with explicit curl connect and total timeouts so timed-out checks cannot accumulate.

## Comment 5545202970

reporter (NONE) · DevlTz · 2026-09-04T19:02:01Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5545202970

>SIGBUS: fault address resolves to the primary SQLite SHM mapping

I resolved the current-thread trace and the faulting address from the core.

The faulting thread was running:

```text
#0  walFindFrame()
#1  sqlite3WalFindFrame()
#2  readDbPage()
#3  getPageNormal()
#4  sqlite3PagerGet()
#5  getAndInitPage()
#6  moveToChild()
#7  sqlite3BtreeTableMoveto()
#8  sqlite3VdbeFinishMoveto()
#9  sqlite3VdbeExec()
#10 sqlite3Step()
#11 sqlite3_step()
#12 sqlite3_step()
#13 db_storage_lifecycle_reconcile()
#14 migration_worker_main()
```

The signal information from the core is:

```text
SIGBUS
si_code = 2
si_addr = 0x7f06e157b53e
```

`si_code=2` is `BUS_ADRERR`.

I then checked the core mappings. The fault address resolves directly inside the primary SQLite shared-memory mapping:

```text
0x7f06e1575000 - 0x7f06e157d000
/var/lib/lightnvr/data/database/lightnvr.db-shm
```

The fault address:

```text
0x7f06e157b53e
```

is at offset `0x653e` inside that 32 KiB mapping.

So this SIGBUS occurred while `db_storage_lifecycle_reconcile()` was stepping a query, SQLite was in `walFindFrame()`, and the actual faulting address was inside the mapped `lightnvr.db-shm`.

There is another potentially relevant timing detail.

A scheduled database backup had started earlier in the same process at:

```text
15:38:24.578  Starting scheduled database backup cycle
15:38:24.879  Starting database backup from
               /var/lib/lightnvr/data/database/lightnvr.db
               to
               /var/lib/lightnvr/data/database/lightnvr.db.backups/20260904T183824Z.sqlite3
```

The SIGBUS occurred at approximately `15:41:42`.

The core mappings still contain both:

```text
0x7f06e156d000 - 0x7f06e1575000
.../lightnvr.db.backups/20260904T183824Z.sqlite3.tmp-shm

0x7f06e1575000 - 0x7f06e157d000
.../lightnvr.db-shm
```

The actual fault address is in the **primary `lightnvr.db-shm` mapping**, not the backup `.tmp-shm`.

I am not concluding that the backup caused the SIGBUS, but given the `BUS_ADRERR` inside SQLite's WAL-index mapping, the overlap between the storage lifecycle worker and an active backup seems worth checking for any path that can replace, truncate, unlink, or otherwise invalidate the primary SHM/WAL mapping while another thread is using it.

The core is preserved locally if another targeted GDB query would help.

### Additional validation: audit traffic

I also ran the audit aggregation you suggested against the current database:

```text
live.view|allowed|572190
recordings.replay|allowed|177
live.view|denied|105
system.admin|allowed|93
storage.configure|allowed|43
events.configure|denied|27
auth.login|success|26
system.admin|denied|24
users.manage|allowed|16
auth.login|denied|8
camera.configure|allowed|6
camera.configure|success|6
storage.configure|success|2
system.admin|success|2
authorization.policy.update|success|1
live.view|failure|1
```

So `live.view / allowed` currently accounts for approximately **99.9%** of the audit rows represented by this aggregation (`572,190` rows).

This probably confirms that successful live-view authorization auditing is by far the dominant source of audit traffic.

It does not by itself prove that the telemetry/audit path caused the runtime web stall, but it confirms that the traffic volume on that path is material and consistent with the contention mechanism you described.

For the next comparison run I can keep the full live dashboard closed initially, then open the 54-camera grid and compare health latency and the `live.view / allowed` growth rate. Given the new SIGBUS, I have not intentionally forced that load again yet.

## Comment 5545327863

other (CONTRIBUTOR) · matteius · 2026-09-04T19:13:04Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5545327863

Two updates from this new evidence.

### Independent startup reproduction

I also deployed the new version at matteius.lightnvr.com. The proxy was still returning HTTP 503 with no available server at 19:10:12 UTC. By 19:12:17 UTC, both / and /api/health returned HTTP 200; the health response reported 99 seconds of process uptime at 19:12:25 UTC.

So this second instance eventually started, but only after an extended no-listener window. That independently supports the synchronous startup consistency check being very slow rather than permanently deadlocked. We should treat the current startup behavior as unsuitable for production-sized databases even when it eventually completes.

### SIGBUS and scheduled backup overlap

The resolved SIGBUS is important and distinct from the original heap abort. BUS_ADRERR in walFindFrame(), at an address inside the primary 32 KiB db-shm mapping, most commonly means that the mmap backing file was truncated below the accessed page or that the filesystem could not service the mapped I/O.

I do not see application code in the scheduled backup path directly unlinking or truncating the primary db-shm or db-wal files. The backup destination uses a separate .tmp path. However, the backup implementation introduced by eefaa1da is now a strong suspect for the surrounding I/O pressure and WAL lifetime:

- It starts with PRAGMA wal_checkpoint(FULL).
- It opens a second read-only connection to the live WAL database.
- It pins one read transaction across the complete copy and keeps that source connection and transaction open while a full integrity_check scans the destination.
- It calls fdatasync after every 4096-page, approximately 16 MiB destination batch.
- It repeatedly applies POSIX_FADV_DONTNEED to the live source database. The page cache is shared by inode, so this can evict pages needed by the main LightNVR connection; it is not private to the backup file descriptor.

On a 1.4 GiB database under continuous audit and detection writes, that combination can create several minutes of heavy I/O, prevent WAL reset while the snapshot is pinned, and amplify the web/database contention already observed. The fact that both the primary and destination temporary SHM mappings remain in the core confirms that the backup was still active, although it does not yet prove that the backup truncated the primary SHM mapping.

For the next safe run I recommend disabling both expensive paths temporarily:

    [database]
    startup_check = off
    backup_interval_minutes = 0

I would also keep the full live grid closed initially. Given the SIGBUS, I would not intentionally reapply the 54-camera telemetry burst until scheduled backups are disabled.

Could you collect these targeted details from the SIGBUS incident?

1. The image version, PID, and coredumpctl info for this specific core, to distinguish it from the two earlier SIGABRT cores.
2. The post-crash size and inode of lightnvr.db-shm and lightnvr.db-wal. A zero-byte SHM file would be especially significant.
3. Kernel messages around 15:41:42 for XFS, I/O, ENOSPC, or block-device errors.
4. An argument-redacted all-thread backtrace from this SIGBUS core. In particular, a thread in backup_database will show whether it was copying, syncing, or verifying the destination.
5. Whether any external process, host backup job, SQLite CLI, or configured post-backup script could touch the database, WAL, or SHM files.

The code changes I would make next are: stop evicting the live database page cache, release the source snapshot immediately after sqlite3_backup_finish(), move or rate-limit destination verification, add timing/progress logs, and remove the mandatory pre-listener startup scan from the normal container boot path.

## Comment 5545500173

reporter (NONE) · DevlTz · 2026-09-04T19:29:25Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5545500173

I collected the five details you requested for the `0.41.6` SIGBUS incident.

#### 1. Image / PID / core identity

```text
Image=ghcr.io/opensensor/lightnvr:0.41.6
RestartCount=1
OOMKilled=false

PID: 1613933
Signal: 7 (SIGBUS)
Timestamp: 2026-09-04 15:41:42 -03
Core: present
```

This is therefore the new `0.41.6` SIGBUS core, distinct from the two earlier `0.41.4` SIGABRT cores.

#### 2. Current post-restart DB / SHM / WAL state

```text
lightnvr.db
size=1492094976
inode=21474837697

lightnvr.db-shm
size=32768
inode=21474837708

lightnvr.db-wal
size=4783352
inode=21474837707
```

The SHM file is currently 32 KiB, not zero bytes.

These sizes/inodes are from the post-crash, post-restart state, so I do not assume they necessarily match the exact filesystem state at the instant of the SIGBUS.

The core itself shows that the fault address was inside a 32 KiB mapping of the primary `lightnvr.db-shm`.

#### 3. Kernel messages around the crash

I checked the kernel journal from `15:40:30` through `15:42:30`.

```text
-- No entries --
```

There were therefore no XFS, block-device, ENOSPC, or I/O error messages recorded in the kernel journal for that crash window.

#### 4. Backup thread state in the SIGBUS core

The all-thread trace confirms that the scheduled backup was still actively running at the instant of the SIGBUS.

A separate thread was here:

```text
Thread 5 (LWP 223):

#3  pread64()
#4  seekAndRead()
#5  unixRead()
#6  sqlite3OsRead()
#7  readDbPage()
#8  getPageNormal()
#9  sqlite3PagerGet()
#10 btreeGetPage()
#11 checkTreePage()
#12 checkTreePage()
#13 checkTreePage()
#14 sqlite3BtreeIntegrityCheck()
#15 sqlite3VdbeExec()
#16 sqlite3Step()
#17 sqlite3_step()
#18 sqlite3_step()
#19 run_integrity_check()
#20 backup_database()
#21 perform_database_backup_cycle.constprop()
#22 maybe_run_scheduled_database_backup()
#23 main()
```

So the backup had not completed by the time of the crash; it was inside `run_integrity_check()` and actively reading database pages.

This is consistent with the destination verification phase you described, although the argument-redacted trace does not identify the database path directly.

At the same instant, the faulting thread was:

```text
migration_worker_main()
→ db_storage_lifecycle_reconcile()
→ sqlite3_step()
→ walFindFrame()
→ SIGBUS
```

and another detection worker was waiting in `pthread_mutex_lock()` from:

```text
store_detections_with_source()
→ store_detections_in_db()
→ detect_objects_api_snapshot()
```

I am still treating these as concurrent observations rather than proof that the backup caused the SIGBUS.

#### 5. External database access / post-backup hook

Current configuration:

```text
[database]
startup_check = off
backup_interval_minutes = 360
post_backup_script =
```

`post_backup_script` is empty.

I also checked for relevant systemd timers, cron jobs, and currently running external backup/SQLite processes:

```text
systemd timer search: no matches
cron search: no matches
rsync/borg/restic/sqlite3 process search: no matches
```

So I am not currently aware of any external process or configured post-backup hook that would be touching the LightNVR database, WAL, or SHM files.

For the next validation run I will use:

```ini
[database]
startup_check = off
backup_interval_minutes = 0
```

and keep the full live grid closed initially, as suggested.

## Comment 5546228666

other (CONTRIBUTOR) · matteius · 2026-09-04T20:43:14Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5546228666

Thanks — this all-thread trace materially strengthens the backup correlation and exposes a concrete locking defect in the old backup preflight.

At the time of the SIGBUS, `0.41.6` was specifically in the destination `integrity_check`, while the old implementation still kept its second read-only source connection and transaction attached to the primary WAL database. The faulting storage-lifecycle query was concurrently reading the primary WAL index. The lack of XFS/block/ENOSPC messages and the absence of an external SQLite/backup process remove two major alternative explanations, while still not making the timing alone proof of causation.

There is, however, a direct repository bug immediately before that backup begins: `flush_database_to_disk()` calls `sync_path_if_exists()` on the live main database, WAL, and SHM paths. That helper performs a raw `open()` / `fsync()` / `close()` on each path while SQLite connections remain live.

On POSIX, closing any descriptor for an inode can release that process's advisory locks on the inode, including locks held through different descriptors. SQLite's Unix VFS explicitly warns about locks being erroneously deleted by `close(open(DATABASE_PATHNAME))` and has internal deferred-close machinery to avoid that problem. LightNVR's raw descriptors bypass that machinery. Closing the raw primary DB and SHM descriptors can therefore remove the process-level database and WAL-index locks while SQLite's in-memory lock state and 32 KiB SHM mapping remain active. That is directly relevant to a later `BUS_ADRERR` in `walFindFrame()`.

I now have repository fixes that:

- remove the pre-backup `FULL` checkpoint and all raw open/fsync/close operations on the live DB/WAL/SHM files;
- never open a raw cache-control descriptor for the live source database;
- enable persistent WAL sidecars on the primary and independent read connections;
- release the backup source snapshot immediately after `sqlite3_backup_finish()`, before destination verification;
- keep the private backup destination in exclusive locking mode, convert it to `journal_mode=DELETE`, and verify it without a `.tmp-shm` mapping;
- remove stale WAL/SHM/journal sidecars when publishing backups or restoring, and make restore staged/verified/atomic;
- keep the database mutex alive for process lifetime and never close the global SQLite handle without acquiring it.

The backup regression now checks, from a separate child process, that both the primary database lock and SHM lock remain present before and after backup. It also checks that the live SHM inode/size are unchanged, no backup sidecars survive, and stale sidecars cannot be paired with a restored main file. The full build and all 28 database/storage tests pass.

Your proposed A/B run with both `startup_check = off` and `backup_interval_minutes = 0` is the safest useful next step. If that remains stable beyond the previous six-hour backup boundary, it will add strong operational evidence for this path without deliberately reproducing the risky load. Please do not force another scheduled backup on `0.41.6`; that image still contains the raw-descriptor lock bug.


## Comment 5590623473

reporter (NONE) · DevlTz · 2026-09-08T19:26:35Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5590623473

Thanks for all the help investigating this.

I've now tested `0.41.12`, and the original `malloc(): corrupted top size` / heap-corruption issue has not reproduced. The instance is running normally on the fixed release, so I'm closing this as resolved.

Really appreciate the detailed debugging, core analysis, and fixes throughout this investigation.

## Comment 5782700267

reporter (NONE) · DevlTz · 2026-09-22T19:31:57Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5782700267

## Update: still reproducible on 0.42.4

I upgraded the same deployment from `0.41.12` to `0.42.4` and continued monitoring the issue.

Unfortunately, the same heap corruption is still reproducible on `0.42.4`.

### Current 0.42.4 state

After the upgrade, the container initially started normally:

```text
Image=ghcr.io/opensensor/lightnvr:0.42.4
RestartCount=0
OOMKilled=false
Health=healthy
```

Since then, LightNVR has crashed twice.

Current state:

```text
Image=ghcr.io/opensensor/lightnvr:0.42.4
RestartCount=2
OOMKilled=false
Status=running
Health=healthy
```

There are exactly two post-upgrade LightNVR coredumps:

```text
Tue 2026-09-22 00:37:34 -03  Signal 6 (SIGABRT)
Tue 2026-09-22 12:46:32 -03  Signal 6 (SIGABRT)
```

Both crashes contain the same allocator error:

```text
malloc(): corrupted top size
```

followed by:

```text
/bin/start.sh: line 10: 57 Aborted (core dumped) /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
```

and on the second occurrence:

```text
/bin/start.sh: line 10: 58 Aborted (core dumped) /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
```

### Crash #1

Heap corruption was detected at approximately:

```text
2026-09-22 00:36:51 -03
```

Immediately before it, LightNVR was actively processing multiple detection requests.

There were also snapshot timeouts and fallback-to-frame-decode events:

```text
[ERROR] [Detection] CURL request failed for snapshot: Timeout was reached
[WARN] [Detection] API Detection (snapshot): Failed to get snapshot from go2rtc
[INFO] [Detection] go2rtc snapshot unavailable, falling back to frame decode
```

The final activity immediately before the allocator error included detection requests such as:

```text
[INFO] [Detection] API Detection (snapshot): Sending request to http://localhost:9001/api/v1/detect?backend=onnx&confidence_threshold=0.60&return_image=false
malloc(): corrupted top size
```

### Crash #2

The second occurrence happened at approximately:

```text
2026-09-22 12:43:50 -03
```

Again:

```text
malloc(): corrupted top size
```

The process subsequently terminated with `SIGABRT` and Docker restarted the container.

There was significant detection/go2rtc activity immediately before this occurrence as well, including:

```text
[ERROR] [Detection] CURL request failed for snapshot: Timeout was reached
[WARN] [Detection] API Detection (snapshot): Failed to get snapshot from go2rtc
[INFO] [Detection] go2rtc snapshot unavailable, falling back to frame decode
```

There was also a health check timeout:

```text
[ERROR] [HealthCheck] Health check curl failed: Timeout was reached
[WARN] [HealthCheck] Health check failed (consecutive failures: 1)
```

Some unavailable RTSP streams were being retried at the same time.

One HLS writer had reached:

```text
attempt 815
attempt 816
```

and another unavailable detection stream was at:

```text
State: CONNECTING (attempt 732)
```

I am **not claiming that go2rtc/detection activity is necessarily the root cause**, but both observed crashes on `0.42.4` occurred while detection processing and snapshot fallback activity were happening.

### Core dump preserved

I exported the most recent core dump.

```text
PID: 3835667
Signal: 6 (ABRT)
Command Line: /bin/lightnvr -c /etc/lightnvr/lightnvr.ini
Executable: /usr/bin/lightnvr
```

Current stack trace available from systemd-coredump:

```text
Stack trace of thread 99:
#0  0x00007fd9ae6f1d0c n/a (/usr/lib/x86_64-linux-gnu/libc.so.6)
#1  0x0000000000000000 n/a (n/a)
```

I also preserved:

- the ~2 GB raw core dump from the second `0.42.4` crash
- the exact `/bin/lightnvr` binary from the `0.42.4` container
- SHA256 of that binary
- coredump metadata for both crashes
- logs surrounding both crashes
- the previous `0.41.12` evidence

I am not uploading the raw core publicly because process memory may contain RTSP URLs, credentials, internal addresses or other sensitive data.

### Comparison

```text
0.41.12:
- RestartCount: 26
- recurring LightNVR coredumps
- malloc(): corrupted top size
- SIGABRT/core dumps

0.42.4:
- RestartCount: 2 so far
- 2 LightNVR coredumps
- malloc(): corrupted top size
- SIGABRT/core dumps
- OOMKilled=false
```

So the same heap corruption appears to still be present in `0.42.4`.

If useful, I can run a debug/ASan build or provide additional sanitized GDB output from the preserved core.

## Comment 5783108598

reporter (NONE) · DevlTz · 2026-09-22T19:56:08Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5783108598

## Additional observation from a third reproduction

The issue reproduced a third time on `0.42.4` (`RestartCount=3`, `OOMKilled=false`, `SIGABRT`).

One potentially useful pattern from this occurrence is the activity immediately before the heap corruption.

In the few seconds before the crash, several snapshot requests timed out and LightNVR fell back to frame decoding:

```text
[Detection] CURL request failed for snapshot: Timeout was reached
[Detection] API Detection (snapshot): Failed to get snapshot from go2rtc
[Detection] go2rtc snapshot unavailable, falling back to frame decode
```

Immediately afterward, multiple API detection operations started almost simultaneously:

```text
16:37:42.058  API Detection: Starting detection
16:37:42.475  API Detection: Starting detection
16:37:42.477  API Detection: Starting detection
16:37:42.700  malloc(): corrupted top size
```

So in this reproduction, the allocator detected heap corruption roughly 223 ms after the last of several near-concurrent detection operations started.

This does not prove that detection concurrency or the fallback path is the root cause, but it may help narrow down the code path worth inspecting.

The third coredump was also preserved locally.

## Comment 5833404469

other (CONTRIBUTOR) · matteius · 2026-09-25T13:42:33Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5833404469

Found it, and it explains every detail in your reports. The frame-decode fallback (the path that runs right after "go2rtc snapshot unavailable, falling back to frame decode") converts the decoded frame to packed RGB24 into a buffer sized exactly width×height×3. libswscale's x86 SSSE3 yuv420p→rgb24 converter processes 16 pixels per iteration but only checks that the width rounded up to 8 fits the stride, so for any camera whose width mod 16 is 8 or more (1080-wide portrait doorbells, 856, 1000, 1512, 1944, ...) the last row is written up to 24 bytes past the end of the buffer. Its rgb24→yuv420p readers, used when the JPEG for the detector is encoded, also read up to 64 bytes past the end. This is present in FFmpeg 4.3 through 8.1, including the 8.1.2 shipped in the 0.41.4 and 0.42.4 images, where we reproduced the 24-byte overrun inside the container.

For those widths, width×height×3 is a multiple of 16, so glibc leaves 8 bytes of slack and the overrun lands squarely on the next chunk's size field. That is exactly what `malloc(): corrupted top size` reports, it is raised by the *next* allocation in that arena (which is why the abort follows "API Detection: Starting detection" from another worker within a few hundred milliseconds), and it is why the strtok fix did not help and why an ASan build would look clean (libswscale is not instrumented; the overrun lands silently in ASan's redzone).

You can confirm the exposure on your database: `SELECT name, width, height FROM streams WHERE width % 16 >= 8;` should list the cameras involved.

On main the conversion buffers carry 128 bytes of tail slack (packed stride unchanged) and a guard-page regression test proves the padding covers both directions. Please try the next release; on 0.42.4 the only mitigations are keeping go2rtc snapshots reliable enough that the fallback rarely runs, or avoiding those widths.


## Comment 5915935801

other (CONTRIBUTOR) · matteius · 2026-09-30T17:03:01Z · https://github.com/opensensor/lightNVR/issues/587#issuecomment-5915935801

The fix above shipped in 0.42.5; the current release is 0.42.8. On any of those builds the `malloc(): corrupted top size` abort from the frame-decode fallback should be gone. Please retest and post the container's restart count after a comparable period.

