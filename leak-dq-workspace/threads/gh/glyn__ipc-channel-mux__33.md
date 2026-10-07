# cargo test fails intermittently on Windows with STATUS_ACCESS_VIOLATION

- URL: https://github.com/glyn/ipc-channel-mux/issues/33
- Repo: glyn/ipc-channel-mux (language: Rust)
- State: open; created 2026-03-24T16:20:42Z; status ok; passes main

## Issue body

reporter (OWNER) · glyn · 2026-03-24T16:20:42Z · https://github.com/glyn/ipc-channel-mux/issues/33

Since three weeks ago, `cargo test` fails intermittently in Windows CI with the following error:
~~~
  process didn't exit successfully: `D:\a\ipc-channel-mux\ipc-channel-mux\target\x86_64-pc-windows-msvc\debug\deps\ipc_channel_mux-050909b60cc6723b.exe --nocapture`
(exit code: 0xc0000005, STATUS_ACCESS_VIOLATION)
~~~

Examples:

* x86_64-pc-windows-msvc - https://github.com/glyn/ipc-channel-mux/actions/runs/23497610593/job/68383112215
* i686-pc-windows-msvc - https://github.com/glyn/ipc-channel-mux/actions/runs/22722472401/job/65888182914
* x86_64-pc-windows-msvc - https://github.com/glyn/ipc-channel-mux/actions/runs/22746074338/job/65970053633

Note that I have not seen this error on MSRV builds (Rust 1.86).

I have tried setting RUST_MIN_STACK to 16 MB, but this doesn't prevent the failure.

## Comment 4126075804

reporter (OWNER) · glyn · 2026-03-25T12:09:10Z · https://github.com/glyn/ipc-channel-mux/issues/33#issuecomment-4126075804

I added an intermittency workflow to investigate changing some of the settings and this unearthed https://github.com/glyn/ipc-channel-mux/issues/36.

## Comment 4137158791

reporter (OWNER) · glyn · 2026-03-26T18:11:23Z · https://github.com/glyn/ipc-channel-mux/issues/33#issuecomment-4137158791

On the branch 33-windows-ci-access-violation I found that the access violations occur when running various bytes* testcases.

Ref: https://github.com/glyn/ipc-channel-mux/actions/runs/23608566659/job/68757932371?pr=38

## Comment 4161383039

reporter (OWNER) · glyn · 2026-03-31T09:54:28Z · https://github.com/glyn/ipc-channel-mux/issues/33#issuecomment-4161383039

https://github.com/glyn/ipc-channel-mux/pull/40 shows that cargo test fails on Windows around 2-3% of the time.

https://github.com/glyn/ipc-channel-mux/pull/41 which includes Claude Code's putative fix to https://github.com/servo/ipc-channel/issues/450 still fails (actually more frequently than PR 40 - 4-5% of the time).

I had Claude Code write some Windows stress tests for ipc-channel, but these all passed. See https://github.com/servo/ipc-channel/pull/451.

I had Claude Code write some Windows stress tests for ipc-channel based on the usage patterns in ipc-channel-mux, but these all passed (once I had applied the putative fix to https://github.com/servo/ipc-channel/issues/450). See https://github.com/glyn/ipc-channel-mux/pull/43.

## Comment 4162682518

reporter (OWNER) · glyn · 2026-03-31T13:33:10Z · https://github.com/glyn/ipc-channel-mux/issues/33#issuecomment-4162682518

Below is a dump of some investigation into this issue by Claude Code.

---
# Windows CI ACCESS_VIOLATION Investigation

## Issue

Intermittent CI failure on Windows where the test process exits with
`STATUS_ACCESS_VIOLATION` (0xc0000005). See GitHub issue #33, branch
`33-windows-ci-access-violation`, PR #38.

Example failure:
https://github.com/glyn/ipc-channel-mux/actions/runs/23588956079/job/68689035582#step:5:256

## Symptoms

- Test process crashes with exit code 0xc0000005 (`STATUS_ACCESS_VIOLATION`)
- Intermittent — only hits occasionally across 200 matrix runs
- Affects x86_64-pc-windows-msvc (and possibly i686)
- No Rust backtrace or panic message — bypasses the panic handler entirely
- `RUST_MIN_STACK=16777216` (16 MB) is already set
- Tests that surface the ipc-channel PR #449 bug (`try_recv_timeout` message
  loss) are `#[ignore]`d, so this is a separate issue

## Crash Dump Capture Journey

Getting a crash dump was non-trivial. Multiple approaches failed before
succeeding:

### 1. WER Registry (failed)
Configured Windows Error Reporting via registry keys
(`HKLM:\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps`) to
write full dumps. No dumps were produced — WER on GitHub Actions runners
apparently doesn't honour these settings.

### 2. Procdump as JIT Debugger (failed)
Installed Sysinternals `procdump` and registered it as the JIT debugger
(`procdump -accepteula -i <dir>`). No dumps were produced — the Rust
runtime's own exception handling catches the structured exception before
Windows dispatches it to the JIT debugger.

### 3. Procdump -x (succeeded)
Ran the test executable **under** procdump directly:
```
procdump -accepteula -e -ma -x <dump_dir> <test_exe> --nocapture
```
This works because procdump monitors the child process's exceptions
in-process rather than relying on the JIT debugger dispatch.

**Exit code headaches:** procdump exits 1 when no dumps are captured (i.e.
tests pass normally). Fixes required:
- `$PSNativeCommandUseErrorActionPreference = $false` for PowerShell 7.4+
- Explicit `exit 0` at end of script to clear `$LASTEXITCODE`
- Detection logic: check for `.dmp` files to determine crash vs clean pass

### CI Workflow Setup

Both `intermittency.yml` and `main.yml` now:
1. Download and extract procdump
2. Build tests with `cargo test --no-run`
3. Parse test executable paths from build output
4. Run each executable under `procdump -e -ma -x`
5. Check for `.dmp` files after each run (exit 1 if found)
6. Upload crash dumps as artifacts on failure

The intermittency workflow runs 50 iterations per target (x86_64, i686) to
increase the chance of reproducing.

## Crash Dump Analysis

Dump file: `scratch/ipc_channel_mux-e5e6125c0f2cadb5.exe_260326_174321.dmp`
Analysed with `minidump-stackwalk`.

### Key Finding: STATUS_HEAP_CORRUPTION

The actual crash reason is **`STATUS_HEAP_CORRUPTION`** (0xC0000374), not
ACCESS_VIOLATION. Windows surfaces this as exit code 0xc0000005 to the parent
process.

- **Crashing thread:** Thread 4, running `mux_test::bytes_cross_thread`
- **Crash location:** `ntdll.dll` heap management code (RtlpHeapHandleError)
- **Other active test threads at crash time:**
  - Thread 0 (main): waiting
  - Thread 5: `mux_test::bytes_disconnect_all_cloned_senders_dropped`
  - Thread 6: `mux_test::bytes_disconnect_cloned_sender_partial_drop`

### What This Means

Heap corruption means something wrote to freed memory, double-freed, or
overflowed a heap buffer. The corruption happens at one point but the crash
occurs later when the heap detects it during a subsequent allocation or free.
This explains:

1. **Intermittency** — the corruption must be detected by a heap operation,
   which depends on timing and allocation patterns
2. **No Rust backtrace** — the crash is in the Windows heap manager, not in
   Rust code, so the panic handler never runs
3. **The faulting thread may not be the culprit** — `bytes_cross_thread`
   triggered a heap operation that detected corruption caused by a different
   thread or test

### Stack Trace Summary (Thread 4, crashed)

```
 0  ntdll.dll + 0x117aa5          (RtlpHeapHandleError / heap validation)
 3  VCRUNTIME140.dll + 0x55e2     (C runtime free/malloc)
10  ipc_channel_mux + 0x34fbcf    (test executable code)
11  ipc_channel_mux + 0x34f999
...
34  KERNELBASE.dll + 0xf347f
```

Without debug symbols, the exact function names within the test executable
are not resolved. The stack is mostly `ntdll.dll` heap routines interleaved
with test executable frames.

## Known ipc-channel Bug (separate issue)

There is a known bug in ipc-channel 0.21.0 documented in
`scratch/IPC_CHANNEL_BUG.md` where `try_recv_timeout` can silently lose
messages on Windows due to a race between `CancelIoEx` and read completion
in `MessageReader::issue_async_cancel`. This is tracked via ipc-channel
PR #449. Tests that trigger this bug are `#[ignore]`d.

The heap corruption may or may not be related to the same area of
ipc-channel's Windows named pipe handling.

## Potential Root Causes

1. **ipc-channel use-after-free in named pipe handling** — The Windows
   implementation uses `AliasedCell` for overlapped I/O buffers. If a buffer
   is freed while an overlapped operation is still in progress, the kernel
   writes to freed memory → heap corruption.

2. **Double-free in ipc-channel handle management** — `WinHandle` implements
   `Drop` to call `CloseHandle`. If a handle is duplicated incorrectly or
   the same handle value is closed twice, this could corrupt the heap.

3. **Buffer overrun in deserialization** — If ipc-channel's message framing
   is off by one or a message length field is corrupted, deserialization
   could write past the end of a buffer.

## Recommended Next Steps

1. **Enable Page Heap** (`gflags /p /enable ipc_channel_mux*.exe /full`) in
   CI to catch the corruption at the point it happens rather than when the
   heap later detects it. This will give a much more useful stack trace
   pointing to the actual offending code.

2. **Build with debug symbols** and publish a symbol file alongside the dump
   so `minidump-stackwalk` (or WinDbg) can resolve function names.

3. **Run under Address Sanitizer** if MSVC ASan is available in the CI
   toolchain (`-Zsanitizer=address` on nightly).

## Additional Crash Dumps

Three crash dumps have been captured and analysed. All show the same
root cause (`STATUS_HEAP_CORRUPTION`) but the crashing thread varies:

| Dump file | Crashing thread | Test |
|-----------|----------------|------|
| `ipc_channel_mux-e5e6125c0f2cadb5.exe_260326_174321.dmp` | Thread 4 | `bytes_cross_thread` |
| `ipc_channel_mux-e5e6125c0f2cadb5.exe_260326_175138.dmp` | Thread 0 | `main` |
| `ipc_channel_mux-0b408fd255c8b4f7.exe_260330_160714.dmp` | Thread 5 | `receiving_many_subchannels` |

All three dumps share:
- **OS:** Windows NT 10.0.26100 (Windows 11 24H2 / Server 2025) — the
  `windows-latest` runner image
- **Crash reason:** `STATUS_HEAP_CORRUPTION` (0xC0000374)
- **Crash site:** `ntdll.dll + 0x117aa5` (`RtlpHeapHandleError`)
- **Process uptime:** 0–1 seconds

The fact that different threads and different tests trigger the crash
reinforces the theory that the corruption happens earlier and is only
detected when a later heap operation (malloc/free) runs the heap
integrity checks.

## Runner Image Hypothesis

All dumps were captured on `windows-latest`, which currently resolves to
a **Windows Server 2025 / Windows 11 24H2** image (OS build 26100). The
heap manager in this OS version may have stricter validation or different
allocation patterns that surface latent corruption more aggressively than
older images.

As a mitigation, the CI workflows (`main.yml` and `intermittency.yml`)
have been pinned to `windows-2022` (Windows Server 2022, OS build
20348). If the crashes stop on `windows-2022`, that would suggest either:
- The corruption is triggered by a behavioural difference in the newer
  Windows heap/pipe implementation, or
- The newer heap manager detects pre-existing corruption that the older
  one silently tolerates.

Either way, pinning to `windows-2022` buys time while the upstream
ipc-channel issue is investigated.

## Branch History

```
58e8160 Add intermittency workflow
8ffa563 Enable Windows crash dump collection in CI workflows
f94640c Switch from WER to procdump for crash dump collection
e0ee3f6 Create CrashDumps directory before installing procdump
26bed9a Run test executables under procdump instead of using JIT debugger
8b35ec5 Use child process exit code instead of procdump exit code
c0c7117 Fix procdump exit code handling in PowerShell 7.4+
8d743c9 Exit 0 explicitly after procdump loop to clear LASTEXITCODE
ebea73d Re-enable tests
ade7f03 Pin Windows CI runners to windows-2022
```

