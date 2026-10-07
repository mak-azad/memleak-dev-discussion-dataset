# [Bug]: TUI Gateway progressive RSS leak — 8 concurrent sessions, 7.4 GB tui_gateway RSS

- URL: https://github.com/NousResearch/hermes-agent/issues/62743
- Repo: NousResearch/hermes-agent (language: Python)
- State: open; created 2026-07-11T16:28:38Z; status ok; passes offcwe

## Issue body

reporter (NONE) · aider4ryder · 2026-07-11T16:28:38Z · https://github.com/NousResearch/hermes-agent/issues/62743

## TUI Gateway progressive RSS leak — 8 concurrent sessions, 7.4 GB across tui_gateway alone

This is additional extreme-scale evidence for the tracked memory issues (#48287, #58817, #53415, #60385). Filing as a new issue because the evidence points to a **tui_gateway-specific growth pattern** distinct from the gateway agent-cache leak in #48287 and the startup baseline in #53415.

### Environment

- Hermes: git checkout of `main` at `f82c71396` (2026-07-10)
- Python: 3.11.2
- OS: Linux 6.1.0-50-amd64, 32 GB RAM, 15 GB swap
- MCP servers: codegraph, deepwiki, repomix, context7
- state.db: 7.2 GB, 2,729 sessions, 533,439 messages

### Measured RSS growth (tui_gateway.entry)

8 concurrent TUI sessions, each with its own `tui_gateway.entry` process:

| PID | Uptime | RSS (MB) | Threads |
|-----|--------|----------|---------|
| 3003318 | 18h53m | **1,866** | 33 |
| 97207 | 14h39m | **1,830** | 52 |
| 3270692 | 18h08m | **964** | 28 |
| 237474 | 33h57m | **887** | 33 |
| 1342060 | 3h44m | **834** | 30 |
| 22935 | 55h12m | **790** | 26 |
| 3026685 | 18h50m | **718** | 27 |

**Total tui_gateway RSS: 7,889 MB across 7 processes** (8th session is idle/low-RSS).

### smaps_rollup (PID 3003318, largest)

```
Rss:          1,869,664 kB
Pss:          1,857,535 kB
Pss_Anon:     1,856,980 kB   ← 99.97% anonymous
Pss_File:           555 kB   ← almost no file-backed pages
Private_Dirty: 1,856,980 kB  ← all private, never shared
Anonymous:     1,856,980 kB
Swap:                  0 kB  ← not swapped out
```

### /proc status (PID 3003318)

```
VmRSS:    1,866,164 kB
VmSize:   5,651,044 kB
VmHWM:    1,877,356 kB
RssAnon:  1,855,976 kB
RssFile:     10,188 kB
Threads:         33
```

### Observations

1. **RSS grows monotonically with uptime.** The two oldest active sessions (18h+) are at ~1.8 GB; a 3h session is at 834 MB; a fresh session starts at ~700 MB baseline. The growth is ~50–80 MB/hour.

2. **Almost entirely anonymous private pages.** Pss_Anon is 99.97% of Pss — this is Python pymalloc arena retention + growing in-memory data structures, not file cache or shared libraries.

3. **Thread count correlates with RSS.** PID 97207 has 52 threads and 1.8 GB; PID 22935 has 26 threads and 790 MB. Thread stacks and per-thread allocator arenas contribute.

4. **state.db is 7.2 GB** with 2,729 sessions and 533,439 messages. Session enumeration at startup (`SessionDB` operations) triggers large allocations that pymalloc never returns to the OS.

5. **MCP backend multiplication.** Each tui_gateway spawns 4 MCP servers independently. 8 sessions × 4 servers = 32+ MCP backends (~1 GB RSS), plus 39 orphaned backends from reconnect leaks (#60385) = 78 total MCP processes, 2 GB RSS. After manual orphan cleanup, 33 active backends remain at ~1 GB.

6. **No process sharing.** Each TUI session/tab gets its own full Python interpreter with all tool schemas, plugin imports, and MCP connections. There is no shared tui_gateway process model.

7. **Total Hermes memory footprint: 12.1 GB** across 70 processes on a 32 GB system — 38% of physical RAM.

### Distinction from existing issues

| Issue | Focus | This issue adds |
|-------|-------|-----------------|
| #48287 | Gateway `_agent_cache` 50 GB VmSize | tui_gateway RSS (physical, not virtual) growth pattern |
| #58817 | Gateway memory grows ~5x over 20h | tui_gateway-specific data, smaps evidence, thread correlation |
| #53415 | TUI Gateway ~1 GB on startup | Post-startup growth: baseline → 1.8 GB over 18h |
| #60385 | MCP process leak on reconnect | Aggregate impact: 78 MCP backends, 2 GB from multiplication |

### Quick mitigations tried

| Mitigation | Result |
|---|---|
| `hermes sessions optimize` (VACUUM + FTS5 merge) | No effect on RSS; state.db already compact |
| Kill orphaned MCP backends | Reclaimed ~595 MB from 25 orphaned processes; does not address tui_gateway growth |
| `MALLOC_ARENA_MAX=2` | Not yet applied; would reduce glibc arena fragmentation but not pymalloc |

### Suggested investigation areas

1. **`session["history"]` retention** — full conversation transcripts held per-session in `tui_gateway/server.py`. Auto-compression only triggers near context-limit threshold, not by message count or memory budget.

2. **`_session_messages` duplication** — `run_agent.py` maintains a parallel copy of session messages.

3. **pymalloc arena return** — Python 3.11 never calls `malloc_trim(0)`; PR #23675 proposes adding this after tool dispatch, which would help if arenas are the dominant source.

4. **Shared MCP hub** — a single proxy process for all MCP servers would eliminate the N×M multiplication (tracked separately in RyderFreeman4Logos/cli-sub-agent#2679).

5. **Session store lazy loading** — loading metadata for 2,729 sessions at startup causes large transient allocations that pymalloc holds indefinitely.


## Comment 4947982998

other (NONE) · alloevil · 2026-07-11T17:13:05Z · https://github.com/NousResearch/hermes-agent/issues/62743#issuecomment-4947982998

Great data — the smaps_rollup and thread correlation are very telling. I dug into the code to trace the specific mechanisms.

## Code-level findings

**1. Per-process agent cache — no cross-session sharing**

Each `tui_gateway.entry` process creates its own `GatewayRunner` with a separate `_agent_cache` (`gateway/run.py:2855`). The cache cap is `_AGENT_CACHE_MAX_SIZE = 128` (line 66) with `_AGENT_CACHE_IDLE_TTL_SECS = 3600` (line 67). With 8 TUI sessions, you get 8 independent caches, each potentially holding 128 agent instances. That is 1024 agent instances system-wide before any eviction fires.

**2. No `gc.collect()` or `malloc_trim()` in the eviction path**

`_cleanup_agent_resources()` (run.py:5772) shuts down memory providers, closes tool resources, and cleans up stale async clients — but never calls `gc.collect()` or `ctypes.CDLL(None).malloc_trim(0)`. This means Python pymalloc arenas and glibc malloc arenas retain freed memory indefinitely. Your smaps data (Pss_Anon 99.97%) confirms this: the memory is allocated, logically freed, but never returned to the OS.

**3. Thread × arena multiplication**

With 52 threads in the largest process, glibc creates up to 52 × 8 MB = 416 MB of per-thread malloc arenas (default `ARENA_MAX` for 64-bit). Each arena retains its own heap, and Python pymalloc adds another layer of 256 KB pools per thread. Your data showing thread count correlating with RSS (52 threads → 1.8 GB vs 26 threads → 790 MB) maps directly to this.

**4. state.db startup allocation**

7.2 GB / 533k messages → SessionDB operations at startup trigger large sqlite3 result sets. The `sqlite3.Row` factory creates Python objects for every row touched. Even a partial scan of 533k messages could allocate hundreds of MB that pymalloc never releases.

**5. MCP backend multiplication confirmed**

Each TUI session independently spawns MCP connections. 8 sessions × 4 MCP servers = 32 active backends. Combined with #60385 reconnection leaks (39 orphaned), you get 71 total MCP processes. Each MCP stdio process holds a full Python/Node runtime.

## Actionable suggestions

**Quick wins (no architecture change):**

1. Add `gc.collect()` + `malloc_trim(0)` after agent cache eviction in `_cleanup_agent_resources()`:
```python
import gc, ctypes
gc.collect()
try:
    ctypes.CDLL(None).malloc_trim(0)
except Exception:
    pass
```

2. Set `MALLOC_ARENA_MAX=2` (you tried this — did you also set it for the tui_gateway entry process? It must be set *before* Python starts, not after import).

3. Add a periodic full-cache sweep in the memory_monitor callback — every 5 minutes, sweep idle agents *and* force gc+malloc_trim.

**Medium-term:**

4. Share a single tui_gateway process across all TUI sessions (process-per-session → multi-session-single-process). This collapses 8× agent caches, 8× MCP connections, 8× state.db opens into 1.

5. Make SessionDB startup lazy — don't load the full session list at import time. Only load session metadata on first access.

6. Implement MCP connection pooling — share MCP server connections across sessions within the same tui_gateway process.

## Comment 5886909111

other (NONE) · kshitijk4poor · 2026-09-29T08:52:35Z · https://github.com/NousResearch/hermes-agent/issues/62743#issuecomment-5886909111

Linking this to the tracker #127647, which maps the full scope of desktop idle resource burn (renderer CPU/GPU, backend `serve` CPU, memory) and what is fixed versus still open.

This issue is listed under section 3 (memory / RAM): TUI gateway RSS growth (not desktop, same symptom class).

Fixes still land against this issue; the tracker is for scope and cross-reference. If you have new measurements, the tracker's "Measuring" section lists the capture that makes reports comparable.

## Comment 5947050541

other (NONE) · kshitijk4poor · 2026-10-02T06:59:48Z · https://github.com/NousResearch/hermes-agent/issues/62743#issuecomment-5947050541

Soak result from the #127647 memory wave (main `2fa2f42d41`). In-process `tui_gateway` with a real `AIAgent` and a stubbed model (no LLM calls), 10 minutes, macOS. Harness: `rss_soak.py`, runs create session → 2 turns → close in a loop.

| run | sessions | RSS | threads | fds |
|---|---|---|---|---|
| sessions closed each cycle | 949 (3,796 stub calls) | 81.4 → 165.0 (cycle 25) → 195.5 MB | 9–10, flat | 14, flat |
| sessions kept open | 802 | 305.8 MB | 812 | — |

What this shows:
- **Closed sessions:** growth is slow, about 15 surviving objects per cycle. That fits per-session-id dicts that are never pruned (`_replay_next_seq`, `_closed_session_activity`). It does not explain 50–80 MB/h.
- **Open sessions:** each keeps a `tui-notif-poller-<sid>` thread plus memory. Thread count tracks live sessions, which matches your thread-vs-RSS correlation. The driver is that sessions are never evicted while a client is connected. That's the #63551 mechanism and is waiting on a maintainer decision there.
- **Not yet modelled:** your per-turn history size and your 7 GB state.db.

Next evidence: a 6–12 h run with sessions kept open, 50 turns each and 32 KB replies, with and without a large seeded `state.db`. Also `MALLOC_ARENA_MAX=2` versus default on Linux, to separate allocator fragmentation from live objects, and an hourly `tracemalloc` top-20. Related fixes in flight: #108141 (event replay retained outside its budget) and #49756 (agents orphaned during session build).

