# [security] GPAC MP4Box: heap-use-after-free in gf_mx_v

- URL: https://github.com/gpac/gpac/issues/3867
- Repo: gpac/gpac (language: C)
- State: open; created 2026-08-20T15:42:39Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ZIllR0 · 2026-08-20T15:42:39Z · https://github.com/gpac/gpac/issues/3867


## 1. Summary

When `MP4Box -add` is given an input file whose import fails during demuxer setup (e.g. a truncated ISO file), the filter engine tears down the failing filter via `gf_filter_setup_failure_task`, which destroys the filter and its mutex (`gf_filter_del` → `gf_mx_del`). Meanwhile, another scheduler thread may still be inside `gf_filter_process_task` and touch that same mutex through `gf_filter_pck_send_internal` → `gf_mx_v`. The mutex object is freed by the teardown thread before the process thread locks it → **heap-use-after-free**.

The race is triggered reliably when several MP4Box instances run concurrently on the same CPU cores (oversubscription), which widens the scheduling window.


## 2. How to reproduce

### 2.1 Get the source

```bash
git clone https://github.com/gpac/gpac.git
cd gpac
# tested at commit 2fd5a06 (2026-08-20); the issue is present on current master
```

### 2.2 Build with ASan

```bash
./configure --enable-sanitizer
make -j$(nproc)
# binary: bin/gcc/MP4Box
```

### 2.3 PoC input

The PoC is attached as [PoC.zip](https://github.com/user-attachments/files/31270809/PoC.zip). Unzip it to obtain min_input_8B.mp4 — sha256 3b47a05cc0f7b533587c3d898599fbff587465e8e43547090b24e9bdacafcd68.



### 2.4 Run the reproducer

Single invocations crash only with low probability (~<1%); the race window needs scheduling contention. Run 16 MP4Box instances concurrently on a couple of cores — with this the crash reproduces within the first round (seconds):

```bash
# repro.sh — parallel oversubscription reproducer
#!/bin/bash
set -u
IN="${1:?usage: repro.sh <input.mp4> [MP4Box-binary]}"
BIN="${2:-$PWD/MP4Box}"
export ASAN_OPTIONS='detect_leaks=0:abort_on_error=1:symbolize=1'
WK=16
round=0
while true; do
  round=$((round+1))
  for w in $(seq 1 "$WK"); do
    (
      if command -v setarch >/dev/null 2>&1; then
        setarch -R "$BIN" -threads 8 -noprog -add "$IN":dopt: -new /tmp/out_${w}.mp4 >/tmp/out_${w}.log 2>&1
      else
        "$BIN" -threads 8 -noprog -add "$IN":dopt: -new /tmp/out_${w}.mp4 >/tmp/out_${w}.log 2>&1
      fi
      rc=$?
      if [ $rc -eq 134 ] || [ $rc -eq 139 ] || [ $rc -eq 132 ]; then
        echo ">>> Crash in round $round, worker $w (rc=$rc)"
        awk '/ERROR: AddressSanitizer/{p=1} p' /tmp/out_${w}.log
        echo "1" > /tmp/.poc_done_$$
      fi
    ) 2>/dev/null &
  done
  wait
  [ -f /tmp/.poc_done_$$ ] && break
done
rm -f /tmp/.poc_done_$$
```

```bash
bash repro.sh min_input_8B.mp4 ./bin/gcc/MP4Box
```

Expected output (within the first round, ~1-5 s):

```
>>> Crash in round 1, worker 9 (rc=134)
==47987==ERROR: AddressSanitizer: heap-use-after-free ...
```

Notes:
- `setarch -R` disables ASLR; on macOS omit it (the script detects it).
- `-threads 8` is significant: it creates 8+ scheduler threads whose  interleaving exercises the race.
- Parallelism (16 workers on 2 cores) is what makes the race reproducible;  single sequential runs hit it only rarely.

## 3. ASAN report (full)

```
==47987==ERROR: AddressSanitizer: heap-use-after-free on address 0x6060000011f0 at pc 0x7ffff34c6a48 bp 0x7fffffff4e20 sp 0x7fffffff4e10
READ of size 8 at 0x6060000011f0 thread T0
    #0 0x7ffff34c6a47 in gf_mx_v utils/os_thread.c:666
    #1 0x7ffff43c5a6c in gf_filter_pck_send_internal filter_core/filter_pck.c:1359
    #2 0x7ffff44b9a65 in gf_filter_process_task filter_core/filter.c:3225
    #3 0x7ffff448010f in gf_fs_thread_proc filter_core/filter_session.c:2420
    #4 0x7ffff448505e in gf_fs_run filter_core/filter_session.c:2728
    #5 0x7ffff3d6907c in gf_media_import media_tools/media_import.c:1634
    #6 0x5555556770fd in import_file /home/user/work/eval/real-world/gpac/applications/mp4box/fileimport.c:1730
    #7 0x55555562a273 in do_add_cat /home/user/work/eval/real-world/gpac/applications/mp4box/mp4box.c:4633
    #8 0x55555562a273 in mp4box_main /home/user/work/eval/real-world/gpac/applications/mp4box/mp4box.c:6377
    #9 0x7ffff0e6bd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #10 0x7ffff0e6be3f in __libc_start_main_impl ../csu/libc-start.c:392
    #11 0x555555605264 in _start (/home/user/work/eval/real-world/gpac/bin/gcc/MP4Box+0xb1264)

0x6060000011f0 is located 48 bytes inside of 64-byte region [0x6060000011c0,0x606000001200)
freed by thread T2 here:
    #0 0x7ffff7676537 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x7ffff34c5cfa in gf_mx_del utils/os_thread.c:610
    #2 0x7ffff44cd7e4 in gf_filter_del filter_core/filter.c:705
    #3 0x7ffff44cf5f7 in gf_filter_setup_failure_task filter_core/filter.c:3677
    #4 0x7ffff448010f in gf_fs_thread_proc filter_core/filter_session.c:2420
    #5 0x7ffff34c8723 in RunThread utils/os_thread.c:234
    #6 0x7ffff0ed6ac2 in start_thread nptl/pthread_create.c:442

previously allocated by thread T0 here:
    #0 0x7ffff7676887 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x7ffff34c591a in gf_mx_new utils/os_thread.c:531
    #2 0x7ffff44ca6d8 in gf_filter_new filter_core/filter.c:336
    #3 0x7ffff43fb4d3 in gf_filter_pid_resolve_link_internal filter_core/filter_pid.c:4088
    #4 0x7ffff4421454 in gf_filter_pid_resolve_link_check_loaded filter_core/filter_pid.c:4194
    #5 0x7ffff4421454 in gf_filter_pid_init_task filter_core/filter_pid.c:5612
    #6 0x7ffff448010f in gf_fs_thread_proc filter_core/filter_session.c:2420
    #7 0x7ffff448505e in gf_fs_run filter_core/filter_session.c:2728
    #8 0x7ffff3d6907c in gf_media_import media_tools/media_import.c:1634
    #9 0x5555556770fd in import_file /home/user/work/eval/real-world/gpac/applications/mp4box/fileimport.c:1730

SUMMARY: AddressSanitizer: heap-use-after-free utils/os_thread.c:666 in gf_mx_v
==47987==ABORTING
```



## 4. Additional notes
- Tested on Linux x86_64, gcc 11.4, GPAC master 2fd5a06



