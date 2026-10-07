# Memory leak in aMule 2.3.3 Debian Bullseye

- URL: https://github.com/amule-project/amule/issues/314
- Repo: amule-project/amule (language: C++)
- State: closed; created 2022-01-29T10:51:41Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · ngosang · 2022-01-29T10:51:41Z · https://github.com/amule-project/amule/issues/314

I have been using aMule 2.3.3 (Debian Bullseye package) for several months and I notice there is an important memory leak. I know this issue does not contain enough information to fix the problem but maybe it keeps all related issues in the same place.

I'm running aMule 24/7 in my server and I notice the RAM memory increases over the time without a reason. aMule is connected to 1 ed2k server and Kad network, just sharing files, not downloading anything. I only use `amuled` and `amuleweb` processes. As you can see in the screenshots below the issue is in `amuled` process.

To fix this issue I configured a cron task that restarts aMule every 2 days, if I don't, the memory keeps growing lineal.
![image](https://user-images.githubusercontent.com/10577978/151658122-830ed07a-91c2-4892-b385-f6ed8b48d0a8.png)

Just after start
![image](https://user-images.githubusercontent.com/10577978/151657937-e689f9a0-2878-4197-aa30-a8451f529c24.png)

After 2 days
![image](https://user-images.githubusercontent.com/10577978/151657824-186ec51d-1e03-4eae-9721-828ff090deb0.png)

The memory leak is not huge, just 28 MB increase of RAM per day (24 hours), but it is meaningful if you are running in a Raspberry Pi with low RAM. It can crash your system eventually. I hope you can run some memory profiler in aMule to find and fix this issue.

## Comment 1109805997

other (NONE) · raidenii · 2022-04-26T13:35:10Z · https://github.com/amule-project/amule/issues/314#issuecomment-1109805997

+1 to this. Logfile says
```
Assertion failed: ../../src/kademlia/kademlia/Entry.cpp:ReCalculateTrustValue:463: Assertion '!m_publishingIPs->empty()' failed. 
Backtrace follows:
[3] wxOnAssert(char const*, int, char const*, char const*, char const*) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6d182d5]
[4] ?? in /usr/bin/amuled[0x564c973eb4ce]
[5] ?? in /usr/bin/amuled[0x564c973eb5c8]
[6] ?? in /usr/bin/amuled[0x564c973f14da]
[7] ?? in /usr/bin/amuled[0x564c973178c6]
[8] ?? in /usr/bin/amuled[0x564c97309378]
[9] ?? in /usr/bin/amuled[0x564c97289453]
[10] ?? in /usr/bin/amuled[0x564c972c9223]
[11] ?? in /usr/bin/amuled[0x564c97288619]
[12] wxEvtHandler::ProcessEventIfMatchesId(wxEventTableEntryBase const&, wxEvtHandler*, wxEvent&) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6e94241]
[13] wxEventHashTable::HandleEvent(wxEvent&, wxEvtHandler*) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6e94333]
[14] wxEvtHandler::TryHereOnly(wxEvent&) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6e9467c]
[15] wxEvtHandler::ProcessEventLocally(wxEvent&) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6e94703]
[16] wxEvtHandler::ProcessEvent(wxEvent&) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6e947a1]
[17] wxEvtHandler::ProcessPendingEvents() in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6e9514e]
[18] wxAppConsoleBase::ProcessPendingEvents() in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6d1af7f]
[19] wxEventLoopManual::ProcessEvents() in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6d53b5c]
[20] wxEventLoopManual::DoRun() in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6d53c2e]
[21] wxEventLoopBase::Run() in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6d5397d]
[22] wxAppConsoleBase::MainLoop() in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6d1c9a6]
[23] wxEntry(int&, wchar_t**) in /lib/x86_64-linux-gnu/libwx_baseu-3.0.so.0[0x7f5db6da4a19]
[24] ?? in /usr/bin/amuled[0x564c97243fe2]
[25] __libc_start_main in /lib/x86_64-linux-gnu/libc.so.6[0x7f5db679cd0a]
[26] ?? in /usr/bin/amuled[0x564c9724b81a]
```

Maybe related? Seems a release failed here.

## Comment 1529554904

other (NONE) · ogarcia · 2023-05-01T10:19:28Z · https://github.com/amule-project/amule/issues/314#issuecomment-1529554904

@ngosang maybe not a problem of the amule, see this: https://github.com/raspberrypi/linux/issues/5395

## Comment 1530955434

reporter (CONTRIBUTOR) · ngosang · 2023-05-02T06:33:58Z · https://github.com/amule-project/amule/issues/314#issuecomment-1530955434

@ogarcia It's not related.
I'm maintaining an Alpine Linux Docker image => https://github.com/ngosang/docker-amule
And I can reproduce the issue in x64 and arm64 servers. Furthermore, I don't have issues with the OOM killer.

## Comment 1988023675

other (NONE) · Aniark · 2024-03-11T09:58:07Z · https://github.com/amule-project/amule/issues/314#issuecomment-1988023675

Another temporary solution: disable obfuscation supported
```
[Obfuscation]
IsClientCryptLayerSupported=0
IsCryptLayerRequested=0
IsClientCryptLayerRequired=0
```

## Comment 4409125325

other (CONTRIBUTOR) · got3nks · 2026-05-08T19:07:09Z · https://github.com/amule-project/amule/issues/314#issuecomment-4409125325

Several relevant changes have landed on master since 2022 that bear on this:

**Memory leak side:**
- `ee5289884 upload: port eMule's CUploadDiskIOThread + ASIO fixes + adaptive chunks` (upload-side memory hot path)
- `402f52788 Fixed socket leak reported by Valgrind`
- `b106e3ac8 PartFile: serialise m_hpartfile access against the hash thread`
- `cdbc34c13 throttler: signal m_newDataCondition on empty→non-empty control-queue transition`
- PR #491 (`8c3dbf84f` / `1ac86f693`) replaced the adaptive throttler whose state accumulated over uptime — exactly the "fine for hours, then RAM climbs" failure mode this issue describes.

**The Kademlia assertion** (`Entry.cpp:ReCalculateTrustValue` `!m_publishingIPs->empty()` from @raidenii's comment, also independently reported in #45) is still present at `src/kademlia/kademlia/Entry.cpp:358` on master — the publishing-IPs invariant violation hasn't been touched. So if the assertion still fires alongside the leak on a master build, that's the lead worth chasing.

**The obfuscation workaround** (@Aniark) points at `EncryptedStreamSocket` / `EncryptedDatagramSocket` buffer lifetimes — that's a separate angle worth a Valgrind run with obfuscation toggled.

@ngosang — could you retest on current master via your `docker-amule` image? `ngosang/docker-amule:latest` rebuilt from `amule-project/amule@master` would tell us whether the broad memory-leak side is closed by the recent reworks. If RAM stays bounded, this can be closed and the residual Kademlia-assertion + obfuscation leads tracked narrowly.

## Comment 4413932498

reporter (CONTRIBUTOR) · ngosang · 2026-05-09T23:19:15Z · https://github.com/amule-project/amule/issues/314#issuecomment-4413932498

I just deployed the commit abfcbb8ad375435fcb8291f0b3973d653def478b in my server. I will monitor the CPU and RAM and I will report back in a week.

## Comment 4427946878

reporter (CONTRIBUTOR) · ngosang · 2026-05-12T06:37:53Z · https://github.com/amule-project/amule/issues/314#issuecomment-4427946878

I have been running abfcbb8ad375435fcb8291f0b3973d653def478b for 2 days and it's looking better but I think the problem is not totally fixed. I'm sharing 7 TB of content so maybe there is no memory leak, just the client queue increasing or something like that.
<img width="1145" height="1182" alt="Image" src="https://github.com/user-attachments/assets/9b2889dd-4ca3-4f68-8402-d09efd9d27d7" />
Zoom
<img width="1144" height="369" alt="Image" src="https://github.com/user-attachments/assets/585ec938-668e-423b-a1ae-40c20cb04b97" />
I'm going to deploy the latest changes in the master branch to see if other issues are fixed. If you give me detailed instructions I can do more tests.

## Comment 4428574108

other (CONTRIBUTOR) · got3nks · 2026-05-12T08:11:56Z · https://github.com/amule-project/amule/issues/314#issuecomment-4428574108

@ngosang two things — and thanks for the patient testing.

**On "deploy latest master"** — yes please. Recent landings worth noticing:

- **Startup**: `known.met` load (#584) and AICH `SaveHashSet` (#581) — both went from O(N²) to O(N log N) / O(N). For libraries in the 100 k+ range the startup gap should drop from minutes to seconds.
- **Shutdown**: `CFile` 64 KB write buffer (#573, plus the #576 race fix) collapses the `known.met` / `server.met` / `ipfilter.dat` save from many-minutes to seconds.
- Plus a pile of correctness fixes (partfile hashing, EC tags, GUI list controls).

If you re-test on latest master, a one-line note on observed startup/shutdown timings vs. the prior build closes the loop on whether those cover your workload.

**On the RAM curve** — it might be normal. amuled tracks every peer it has interacted with in the current session (CClientList), every shared file, every banned IP, every in-flight upload slot. A 7 TB sharer regularly accumulates hundreds of thousands of `CUpDownClient` objects over a day, each a few hundred bytes — RSS rises without any leak being present.

The current slope looks gentler than the original pattern in this thread (consistent with the upload-side fixes closing some specific leaks). Cleanest confirmation is **a longer baseline** — let it run for a week and check whether it plateaus once you've seen the regular peer set, or keeps climbing past that. If it's still climbing linearly a week in, that's a real leak.

**Tooling, if you want to capture data now** — only `heaptrack` is worth your time on a production daemon. Quick contrast:

| | `heaptrack` | `valgrind --tool=memcheck` |
|---|---|---|
| **How it works** | `LD_PRELOAD` shim over malloc/free | full CPU emulation in a VM |
| **Overhead** | ~1.5–2× | 10–30× |
| **What it catches** | live-allocation tracking (leaks by retention) | leaks + use-after-free + uninitialised reads + double-free |
| **Daemon-friendly?** | yes, run for hours | no, designed for short dev runs |

heaptrack is the only realistic option for your setup — valgrind would be so slow amuled would barely publish files. Recipe:

```sh
apt-get install -y heaptrack
heaptrack -p "$(pidof amuled)"
# let it run 30–60 min once RSS is meaningfully above startup, then Ctrl-C.
heaptrack_print --max-num-allocations 10 heaptrack.amuled.<PID>.zst
```

The top-N output shows the call stacks of the biggest still-live allocations — paste it as text and we'll know whether it's a real leak or just normal client-list footprint.

## Comment 4430842547

reporter (CONTRIBUTOR) · ngosang · 2026-05-12T13:14:15Z · https://github.com/amule-project/amule/issues/314#issuecomment-4430842547

Master branch is looking good. I answered here => https://github.com/amule-project/amule/issues/562#issuecomment-4430469023
About the RAM profiling, I'm using Alpine Linux and `heaptrack` is not in the official repository. I have to build it from source code. Meanwhile, could you take a look here?
* https://github.com/ngosang/docker-amule/issues/89
* https://github.com/ngosang/docker-amule/issues/88

## Comment 4471679399

reporter (CONTRIBUTOR) · ngosang · 2026-05-17T17:14:54Z · https://github.com/amule-project/amule/issues/314#issuecomment-4471679399

@got3nks I have been running 82626f2f3a537c1fe71839509da58d8221185f4b for 3 days and I the memory has doubled.
I can't run `heaptrack -p "$(pidof amuled)"` because of this => https://github.com/ngosang/docker-amule/issues/89#issuecomment-4471595021
Do you think it will be useful to run `heaptrack amuled ...` from the start of the process and keep it running for a couple of days or the traces will be hard to review? Anyway, please don't block the release for this.

<img width="1151" height="1137" alt="Image" src="https://github.com/user-attachments/assets/349957bb-2996-413a-b87e-c25396501cdb" />

## Comment 4471918908

other (NONE) · mifritscher2 · 2026-05-17T17:50:39Z · https://github.com/amule-project/amule/issues/314#issuecomment-4471918908

Don't know whether it is usefull^^

<img width="1920" height="1150" alt="Image" src="https://github.com/user-attachments/assets/a24df7ab-bf53-40da-bf0c-df22c43ecdbb" />

<img width="1920" height="1150" alt="Image" src="https://github.com/user-attachments/assets/2af1fe17-cfb6-4f38-ab99-1fef63debe6d" />

<img width="1920" height="1150" alt="Image" src="https://github.com/user-attachments/assets/a8aa6639-e873-45b8-adca-a22fece444ed" />

<img width="1920" height="1150" alt="Image" src="https://github.com/user-attachments/assets/a038c145-743a-438a-91e9-7727933b7aef" />

<img width="1920" height="1150" alt="Image" src="https://github.com/user-attachments/assets/d43fa785-52a6-4468-bb52-920032ae3492" />

<img width="1920" height="1150" alt="Image" src="https://github.com/user-attachments/assets/352f0893-2764-4a30-bc99-0185ed654493" />

## Comment 4472557779

other (CONTRIBUTOR) · got3nks · 2026-05-17T21:24:07Z · https://github.com/amule-project/amule/issues/314#issuecomment-4472557779

@ngosang — noted, release won't be blocked on this. The 3-day memory curve is interesting but not in the "obvious leak" shape yet; could be amuled accumulating peer state for a 7 TB shareset (`CClientList` + ban list + slot state grows monotonically until peer churn stabilises).

**heaptrack-from-start is feasible**, but the trace file grows large over days — easily tens of GB on a busy node. Two ways to keep it tractable:

1. **Time-bounded run.** Launch `heaptrack amuled ...` and Ctrl-C after 12-24 h once RSS has meaningfully grown. `heaptrack_print`'s top-N output on that capture should still pinpoint the dominant retention site — a real leak shows up as the biggest growing bucket regardless of total run length.

2. **Sampled snapshots.** Cheaper alternative if heaptrack-on-Alpine is more work than it's worth: periodic `cat /proc/$(pidof amuled)/smaps_rollup` (or `/proc/PID/status` → `VmRSS`) into a logfile, plus `pmap -x $(pidof amuled)` snapshots every hour. No per-callsite attribution but it tells us *which heap regions* grow — distinguishing a real leak from glibc heap fragmentation. Cheaper signal to decide whether (1) is worth the effort.

---

@mifritscher2 — looks like those are from `heaptrack_gui`. Could you run `heaptrack_print` against the same `.zst` capture and paste the top-N retention output in a ``` ``` ``` fence? Specifically:

```
heaptrack_print --max-num-allocations 20 heaptrack.amuled.<PID>.zst
```

Text output is grep-able, quotable, and means anyone landing on the thread later can read it via search — the GUI screenshots aren't. If the GUI is showing you a specific tab/view that's been informative, let me know which and we can find the equivalent `heaptrack_print` flag.

## Comment 4472702122

other (NONE) · mifritscher2 · 2026-05-17T22:25:46Z · https://github.com/amule-project/amule/issues/314#issuecomment-4472702122

[heaptrack.txt](https://github.com/user-attachments/files/27931932/heaptrack.txt)

My heaptrack_print does not recognize  `--max-num-allocations`...

## Comment 4474503264

reporter (CONTRIBUTOR) · ngosang · 2026-05-18T04:57:13Z · https://github.com/amule-project/amule/issues/314#issuecomment-4474503264

> My heaptrack_print does not recognize --max-num-allocations...

Me neither.

@got3nks this dump is after 6 hours running, when the memory should be stable. I just run the command for 20 min. If you need more just tell me. I have the tools ready.

[heaptrack.amuled.218.gz](https://github.com/user-attachments/files/27944794/heaptrack.amuled.218.gz)

## Comment 4475841863

other (CONTRIBUTOR) · got3nks · 2026-05-18T08:33:20Z · https://github.com/amule-project/amule/issues/314#issuecomment-4475841863

@ngosang the 6 h-warm + 20-min trace nailed it. After filtering out the things that "leak" but are just live working set, the top is overwhelmingly one path:

```
Kademlia::CKademliaUDPListener::Process2PublishKeyRequest
  → CKeyEntry::MergeIPsAndFilenames (Entry.cpp:412)
  → push_back onto m_filenames (sFileNameEntry copy-construct, holds a wxString)
```

Every `OP_KADEMLIA2_PUBLISH_KEY_REQ` packet adds a filename variant for that file's hash, and the per-entry filename list has **no cap** — `Entry.cpp:403-415`. The publishing-IP list right next to it caps at 100 (`:429-432`); the filename list never got the same treatment. A popular shared file can collect hundreds of filename variants (language renames, mirror prefixes, transliterations) and they accumulate forever.

Top-15 "leaks" in your trace, all routed through that path or its `Indexed::AddKeyword` neighbour at `Indexed.cpp:535/552`:

| size | calls | path |
|---|---|---|
| 289.57K | 87497 | `SetFileName → push_front m_filenames` (Entry.cpp:118) |
| 277.43K | 26876 | `Process2PublishKeyRequest → AddKeyword` (KademliaUDPListener.cpp:1126) |
| 260.29K | 18502 | `Process2PublishKeyRequest → MergeIPsAndFilenames` (KademliaUDPListener.cpp:1032) |
| ... | ... | (all same handful of Kad UDP entry points) |

Total leaked in the 20-min window: **2.36 MB**, which extrapolates to ~170 MB/day at this load — consistent with the multi-day slope you originally reported.

Two other useful negatives from the trace: peak heap was only 4.88 MB (so amuled's working set itself is small — the leak is the entire problem), and the 2022 socket/ASIO-side leak hot paths (`CUploadDiskIOThread`, `CClientList`, `EncryptedStreamSocket`) don't show meaningful churn in the leak report. Those fixes seem to have held.

Fix at #652: cap `m_filenames` at 100 (matching the IP cap right below it), popularity-ordered eviction. `GetCommonFileName` already picks the highest-popularity entry, so survivors are exactly the ones search results would have displayed anyway. `CIndexed`'s keyword-to-file map is untouched, so what files match a search and whether amuled answers Kad queries is unchanged. Once that lands, a 24-48 h soak should show RSS plateauing instead of climbing.


## Comment 4477664832

other (NONE) · Stoatwblr · 2026-05-18T12:29:28Z · https://github.com/amule-project/amule/issues/314#issuecomment-4477664832

Good to see this one getting attention. The leak has been there for a very long time.



## Comment 4487460063

reporter (CONTRIBUTOR) · ngosang · 2026-05-19T11:54:40Z · https://github.com/amule-project/amule/issues/314#issuecomment-4487460063

Tested commit a5fb7797d4c4cfb42a60d24588e20d32e637fb30
It's looking very good:
<img width="1966" height="839" alt="Image" src="https://github.com/user-attachments/assets/5201c772-67b7-4566-afc0-4e0bb23eedc8" />
@got3nks here you have another heaptrack dump. If you think it's fine we can close this issue.
[heaptrack.amuled.117.gz](https://github.com/user-attachments/files/28010623/heaptrack.amuled.117.gz)

## Comment 4487530502

other (CONTRIBUTOR) · got3nks · 2026-05-19T12:04:46Z · https://github.com/amule-project/amule/issues/314#issuecomment-4487530502

Trace looks clean for what it captures, @ngosang. Headline numbers from `heaptrack_print`:

| Metric | Value |
|---|---|
| Runtime | ~49 min |
| Allocations | 23.6M (8064/s) |
| Peak heap consumption | **14.87 MB** |
| Peak RSS (incl. heaptrack overhead) | 276 MB |
| "Leaked" at trace end | 13.66 MB |

(The trace header confirms `heaptrack amuled ...` — i.e. heaptrack launched amuled rather than attaching, so the 49 min is the full process lifetime, not a sampling window of a longer-running amuled.)

The "leaked" 13.66 MB is all normal working state, not leaks in the bug sense — it's allocations still tied to active sessions when the trace stopped:

- **5.35 MB / 217k allocations** from `CPacket::CPacket(CMemFile, ...)` via `CUploadDiskIOThread::CreateStandardPackets` / `CreatePackedPackets` — upload packets currently in the disk-IO → socket-send pipeline. ~25 bytes each (`CPacket` header; payload separately allocated). Freed when the packet is sent.
- **2.1 MB / 117 allocations** from `CAsioSocketImpl::DispatchBackgroundRead` — outstanding boost::asio `async_read` handlers, one per currently-active socket. Freed when the read completes or the socket closes.
- **~1 MB across `CUpDownClient::ProcessRequestPartsPacket` / `ProcessExtPacket`** — per-peer receive-packet allocations.

Peak app heap is 15 MB. Nothing here points at a leak — and the previous offender (`CKeyEntry::m_filenames` growing without bound, fixed in #652) is conspicuously absent from the leak set, which is the strongest direct signal that the cap is doing its job.

**One caveat on the trace duration**: your original failure mode was "memory doubled in 3 days", which is a slow growth that a 49-min trace can't conclusively rule out. So this trace is *consistent with* the leak being fixed, but not a proof of long-uptime flatness. Combined with the memory chart you posted (qualitative stability on `a5fb7797d4`), I'd call this enough to close. If the long-uptime curve regresses on extended runtime, a fresh issue with a longer heaptrack capture is the right next step.

Agreed on closing — the Kad filenames cap in #652 was the real culprit; everything else in this thread was either upstream fixes for adjacent regressions or normal peer-list accumulation.

Thanks for the rigorous testing through this one.

## Comment 4487718748

reporter (CONTRIBUTOR) · ngosang · 2026-05-19T12:29:14Z · https://github.com/amule-project/amule/issues/314#issuecomment-4487718748

@got3nks the amuled process has been running for 19h. I attached heaptrack to the running process for 49 min (the same as the other dump). In the grapth you see the combined RSS memory of all the process in the container. Including amuled, amuleweb and heaptrack.
<img width="1966" height="446" alt="Image" src="https://github.com/user-attachments/assets/e926eef3-027b-4d24-8162-62df22d90507" />

## Comment 4487786418

other (CONTRIBUTOR) · got3nks · 2026-05-19T12:37:44Z · https://github.com/amule-project/amule/issues/314#issuecomment-4487786418

Quick correction to my previous analysis — I misread the trace header and thought heaptrack was launched-from-start, but you attached to an already-running amuled. So the 14.87 MB peak / 13.66 MB leaked numbers only cover allocations made *during the 49-min sampling window*; pre-attach allocations from the first 18 h aren't in the trace at all.

The reason: heaptrack hooks `malloc`/`free` at the moment it attaches. Anything allocated before attach isn't in its tracking table — even if it's gigabytes of leaked memory, it's invisible. Pre-attach `free()` calls are seen but with no matching `malloc` record they're ignored. So heaptrack-attach can only answer "is the leak rate currently ongoing?" — it can't quantify any accumulated pre-attach total. The two ways to see the full picture are `heaptrack <amuled>` from launch (full lifetime, but trace files grow large for long-running daemons), or external RSS observation over time — which is exactly your container chart.

What the trace can still tell us: no significant leak accumulation during those 49 min (~14 MB net at end of window from 23.6M allocations, all attributable to active-session state — `CPacket`s in the upload pipeline, asio read handlers, etc.). Combined with your RSS chart showing the daemon's memory stable on `a5fb7797d4`, the picture is consistent with the leak being fixed: no active leak in the sampled window, and no accumulating total visible in the RSS curve. The conclusion (safe to close, #652 was the real fix) stands.

## Comment 4536862882

other (NONE) · LearZhou · 2026-05-25T19:57:34Z · https://github.com/amule-project/amule/issues/314#issuecomment-4536862882

I would like to say thank you for both ngosang and got3nks for tracking this issue down. As a eMule modder, I have experienced similar ram bloat for 24/7 running emule instance, it's so nice to see this accomplishment.

## Comment 4537109149

reporter (CONTRIBUTOR) · ngosang · 2026-05-25T20:41:21Z · https://github.com/amule-project/amule/issues/314#issuecomment-4537109149

We are still working in more leaks here https://github.com/amule-project/amule/issues/712
