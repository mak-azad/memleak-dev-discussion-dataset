# [SECURITY] CFE_TBL_LoadCmd() file descriptor leak causes denial of service via resource exhaustion

- URL: https://github.com/nasa/cFS/issues/1104
- Repo: nasa/cFS (language: C)
- State: open; created 2026-08-25T16:39:13Z; status ok; passes offcwe

## Issue body

reporter (NONE) · xmin-02 · 2026-08-25T16:39:13Z · https://github.com/nasa/cFS/issues/1104

**Checklist (Please check before submitting)**

- [x] I reviewed the [Contributing Guide](https://github.com/nasa/cFS/blob/main/CONTRIBUTING.md).
- [x] I performed a cursory search to see if the bug report is relevant, not redundant, nor in conflict with other tickets.

**Describe the bug**

CFE_TBL_LoadCmd(), the command handler for loading table configuration files, opens a file descriptor via CFE_TBL_TxnOpenTableLoadFile() but fails to close it before returning. Each successful TBL_LOAD command leaks exactly one file descriptor. An authenticated attacker can repeatedly send well-formed TBL_LOAD commands to exhaust the system's open file descriptor limit (typically 256 on Linux), preventing subsequent file operations and causing denial of service.

The vulnerability is in `cfe/modules/tbl/fsw/src/cfe_tbl_task_cmds.c`, function `CFE_TBL_LoadCmd()` (lines 392-477). At line 418, the function opens a file:

```c
Status = CFE_TBL_TxnOpenTableLoadFile(&Txn, LoadFilename, &FileDescriptor, &Header);
```

At line 443, it reads from the file:

```c
Status = CFE_TBL_LoadContentFromFile(&Txn, FileDescriptor, Header.Tbl.Offset, Header.Tbl.NumBytes);
```

Then at line 452, it calls `CFE_TBL_TxnFinish()`, which only unlocks the registry and does NOT close the file descriptor:

```c
CFE_TBL_TxnFinish(&Txn);
```

The function returns at line 476 without ever calling `OS_close(FileDescriptor)`, leaving the descriptor open indefinitely.

**To Reproduce**

Steps to reproduce the behavior:

1. Build a `native_std` deployment with SBN table service enabled.
2. Start `core-cpu1`.
3. Send 256+ TBL_LOAD commands with valid table files (e.g., via cmd_send or SBN).
4. After OS_MAX_NUM_OPEN_FILES commands, all subsequent file operations fail.
5. Monitor /proc/[core-cpu1-pid]/fd (Linux) to confirm FD count grows: initial 4 → final 34 after 30 load attempts.

The leak is exact: **N TBL_LOAD commands = N leaked file descriptors** (verified by standalone reproduction: 30 open() calls → 30 unclosed fds).

**Expected behavior**

The file descriptor must be closed before CFE_TBL_LoadCmd() returns. All other similar code paths in cfe_tbl_load.c close the descriptor explicitly:

```c
// cfe_tbl_load.c:685-687 (correct pattern)
/* Done with the file now -- must always close the file regardless of what happened */
OS_close(FileDescriptor);
```

CFE_TBL_LoadCmd() has identical file operations but lacks the close call.

**Code snips**

- `cfe/modules/tbl/fsw/src/cfe_tbl_task_cmds.c:418` — opens file descriptor
- `cfe/modules/tbl/fsw/src/cfe_tbl_task_cmds.c:443` — reads from file
- `cfe/modules/tbl/fsw/src/cfe_tbl_task_cmds.c:452` — CFE_TBL_TxnFinish() called (does NOT close fd)
- `cfe/modules/tbl/fsw/src/cfe_tbl_task_cmds.c:476` — returns WITHOUT OS_close()
- `cfe/modules/tbl/fsw/src/cfe_tbl_transaction.c:233-241` — CFE_TBL_TxnFinish() source (only unlocks registry, no fd handling)
- `cfe/modules/tbl/fsw/src/cfe_tbl_load.c:685-687` — correct pattern in other code path (has OS_close)

**System observed on:**

- Hardware: x86-64 (generic)
- OS: Ubuntu 22.04 (Linux 5.x)
- Versions: cFE 7.0 (`dev1`), OSAL/PSP from same bundle, built for `pc-linux` PSP
- Verified with AddressSanitizer and FD monitoring

**Additional context**

Severity (self-assessed): CVSS 3.1 base 7.5 (High), vector `AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`. The leak is triggered by any authenticated sender of TBL_LOAD commands (network reachable via SBN) and causes guaranteed denial of service when the FD limit is exhausted. Attack Vector is Network because SBN TCP is accessible remotely; no local access required.

The vulnerability is distinct from UDP-based table-loading issues. This is a resource-exhaustion (DoS) vector in the command handler path, not a protocol parsing or validation issue. A cursory search of nasa/cFS and nasa/cFE issues did not find this specific fd-leak case (existing TBL tickets address validation logic and transaction semantics, not resource cleanup).

**Fix is straightforward:** Add `OS_close(FileDescriptor);` before the return at line 476, following the pattern from cfe_tbl_load.c.

Attached:
- [real_fd_leak_demo.c](https://github.com/user-attachments/files/31428741/real_fd_leak_demo.c) — standalone C program that reproduces the exact leak pattern (30 open() → 30 leaked fds)
- [EVIDENCE.md](https://github.com/user-attachments/files/31428740/EVIDENCE.md) — detailed static code analysis and design comparison with correct code paths
- [test_fd_leak.c](https://github.com/user-attachments/files/31428739/test_fd_leak.c) — dynamic simulation of CFE_TBL_LoadCmd behavior
- [real_fd_leak_demo_output.txt](https://github.com/user-attachments/files/31428738/real_fd_leak_demo_output.txt) — execution output showing FD leak progression

**Reporter Info**

- Name: xmin
- Organization: YongKK team

## Comment 5413637196

other (CONTRIBUTOR) · dzbaker · 2026-08-25T16:41:40Z · https://github.com/nasa/cFS/issues/1104#issuecomment-5413637196

Tagging @ddstewar for awareness.

## Comment 5415765354

reporter (NONE) · xmin-02 · 2026-08-25T19:41:20Z · https://github.com/nasa/cFS/issues/1104#issuecomment-5415765354

This issue should have been reported to nasa/cFE since it's a cFE core module issue.
I've reported it to the correct repository here: https://github.com/nasa/cFE/issues/2811

Apologies for the confusion!

## Comment 5415790526

other (CONTRIBUTOR) · ddstewar · 2026-08-25T19:43:28Z · https://github.com/nasa/cFS/issues/1104#issuecomment-5415790526

Issues can be transferred. No need to create multiple in the future. I'll be able to give this time tomorrow.
