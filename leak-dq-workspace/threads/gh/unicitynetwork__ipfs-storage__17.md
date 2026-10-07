# fix(nostr-pinner): eliminate Python memory leak via architectural redesign

- URL: https://github.com/unicitynetwork/ipfs-storage/issues/17
- Repo: unicitynetwork/ipfs-storage (language: Python)
- State: open; created 2026-06-15T13:10:51Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · vrogojin · 2026-06-15T13:10:51Z · https://github.com/unicitynetwork/ipfs-storage/issues/17

## Problem

The nostr_pinner Python service leaks memory at ~250 MB/min under production load (~43 req/sec). Despite multiple mitigation patches (shared httpx client, response.aclose(), bounded task concurrency, gc.collect + malloc_trim, MALLOC_ARENA_MAX=2), the leak persists due to **Python heap fragmentation** from high-throughput JSON parsing.

### Root Cause (confirmed via tracemalloc)

| Allocator | Memory | Objects | What |
|-----------|--------|---------|------|
| `json/decoder.py` | 713 MB | 7,189,108 | Parsed JSON dicts from IPFS API responses |
| `aiohttp/compression_utils.py` | 115 MB | 6,187 | HTTP response compression buffers |
| `httpx/_models.py` | 27 MB | 2,702 | httpx response objects |

CPython's pymalloc allocates small objects in 256 KB arenas. Under high JSON throughput, these arenas become fragmented — partially empty but unable to be returned to the OS. `malloc_trim()` helps but cannot reclaim pymalloc-internal fragmentation.

### Current State

- Growth rate: ~250 MB/min (down from ~400 MB/min pre-patches)
- Temporary mitigation: graceful self-restart at 4 GB RSS (`MAX_RSS_MB` env var)
- Self-restart cycle: ~15-20 min under current load
- Container hard cap: 10 GB

## Proposed Architectural Fix

### Option A: Move hot path to nginx + lua/njs (Recommended)

The `/routing-get` endpoint (the hot path) does:
1. SQLite query → get `marshalled_record` 
2. Base64-encode it
3. Wrap in `{"Extra": "...", "Type": 5}` JSON
4. Return as HTTP response

This can be done entirely in **nginx njs** (JavaScript module) or **OpenResty/lua**:
- nginx njs can read SQLite via a small FFI binding or a shared-memory key-value store
- Eliminates all Python object allocation for the hot path
- Python pinner only handles writes (IPNS intercept, Nostr events, chain validation)

**Estimated impact**: Eliminates ~80% of request-path JSON allocations.

### Option B: Redis/memcached response cache in front of Python

- Cache serialized JSON responses for `/routing-get` in Redis
- Set TTL = `STALE_THRESHOLD_SECONDS` (currently 120s)
- nginx `proxy_cache` or a tiny Go/Rust sidecar serves cached responses
- Python only handles cache misses and writes

**Estimated impact**: Reduces Python request rate by ~90% for repeated IPNS names.

### Option C: Rewrite hot path in Go/Rust sidecar

- Small Go or Rust binary handles `/routing-get` reads from SQLite
- Python pinner handles only Nostr subscriptions, chain validation, pinning
- Communicate via SQLite (already shared) or Unix socket

**Estimated impact**: Eliminates Python heap fragmentation entirely for reads.

### Option D: orjson + object pooling (minimal change)

- Replace `json.loads/dumps` with `orjson` (C-based, returns bytes, avoids intermediate Python objects)
- Pre-allocate response templates instead of building dicts per request
- Use `__slots__` on hot-path dataclasses

**Estimated impact**: Reduces JSON allocation by ~50%, may not fully solve fragmentation.

## Implementation Checklist

- [ ] Choose approach (A/B/C/D or hybrid)
- [ ] Benchmark: measure exact request rate per endpoint to quantify which paths matter
- [ ] Prototype chosen approach
- [ ] Load test: verify memory stays flat over 1+ hour under production load
- [ ] Remove temporary `MAX_RSS_MB` self-restart once leak is eliminated
- [ ] Update monitoring/alerting for new architecture

## Context

- PR #16 contains the current mitigation patches
- Production metrics: 99,728 IPNS records in SQLite, 1.3 GB database
- Request breakdown: ~43 req/sec total, ~15/sec IPNS-related (routing-get, ipns-intercept, ws/ipns)
- IPFS Kubo daemon is healthy (300 MB, 63 peers) — the leak is entirely in the Python pinner process
- `STALE_THRESHOLD_SECONDS` raised from 15→120 to reduce background DHT refresh volume

## Files

- `nostr-pinner/nostr_pinner.py` — main service (3000+ lines)
- `config/supervisord.conf` — process management
- `config/nginx.conf.template` — nginx routing (would change for Option A/B)

## Comment 4708737787

reporter (CONTRIBUTOR) · vrogojin · 2026-06-15T14:04:23Z · https://github.com/unicitynetwork/ipfs-storage/issues/17#issuecomment-4708737787

## PR #18 merged — Phase 1+2 complete

Merged [#18](https://github.com/unicitynetwork/ipfs-storage/pull/18) with three read-path optimizations:

1. **nginx `proxy_cache`** for `/api/v0/routing/get` — caches responses keyed on `?arg=` for 30s, including POST requests. Serves `X-Routing-Cache: HIT` for repeated same-name lookups without touching Python.
2. **Pre-serialized `response_cache` column** — JSON response body computed once on write, returned as raw bytes on read. Zero per-request `base64`/`json.dumps` allocation.
3. **Regex-based `Extra` extraction** on DHT refresh path — avoids `response.json()` full parse tree on all three kubo DHT response consumers.

### Production results

| Metric | Before | After PR #18 |
|--------|--------|--------------|
| Read-path allocation per request | ~5 Python objects (dict, base64 str, json str) | ~0 (raw bytes from SQLite) |
| Repeated same-name lookups | Hit Python every time | Served from nginx cache (verified HIT) |
| DHT response parsing | `json.loads()` → full dict tree | Regex on raw bytes → single string |

### What remains: background DHT refresh still fragments pymalloc

Post-restart memory growth (all 99k records stale at 15s threshold):

| Time | RSS | Growth/min |
|------|-----|------------|
| T+0m | 104 MB | baseline |
| T+1m | 1,929 MB | +1,825 (stale burst) |
| T+2m | 2,385 MB | +456 |
| T+3m | 2,783 MB | +398 |
| T+4m | 3,059 MB | +276 |
| T+5m | 3,437 MB | +378 |
| T+6m | 4,005 MB | +568 |

The `_refresh_and_push` background tasks make HTTP requests to kubo and allocate `bytes` objects for response bodies + `base64.b64decode` output. Even without `json.loads()`, CPython's pymalloc arenas fragment from any high-throughput short-lived allocation pattern. `malloc_trim()` cannot reclaim pymalloc-internal fragmentation. **This is a fundamental CPython limitation, not a code bug.**

---

## Follow-up: Option C — Go read/refresh sidecar

The definitive fix is moving the hot read path AND the DHT refresh path out of Python into a compiled language. Go is the natural choice (SQLite support via `mattn/go-sqlite3`, no GC fragmentation at this scale, trivial HTTP server).

### Architecture

```
                          ┌──────────────────────────────────┐
                          │         Go sidecar binary        │
Browser ──nginx───────────┤  /routing-get  (SQLite read)     │
                          │  DHT refresh   (kubo HTTP call)  │
                          │  /ws/ipns      (WebSocket push)  │
                          └──────────┬─────────────────────────┘
                                     │ SQLite WAL (shared)
                          ┌──────────┴─────────────────────────┐
                          │      Python nostr_pinner           │
                          │  Nostr subscriptions               │
                          │  Chain validation                  │
                          │  IPNS record writes (store_record) │
                          │  Pin management                    │
                          └──────────────────────────────────────┘
```

### Scope

The Go binary handles:
1. **`/routing-get`** — read `response_cache` from SQLite, return raw bytes. ~20 lines of Go.
2. **Background DHT refresh** — for stale records, POST to kubo `/api/v0/routing/get`, extract `Extra` field, write to `ipns_records` if sequence is newer. ~50 lines.
3. **`/ws/ipns`** — WebSocket subscription push when records update. ~40 lines.

Python pinner retains:
- Nostr relay subscriptions (websockets library, complex reconnection logic)
- Chain validation (`validate_version_chain` — fetches CID content, checks `_meta.lastCid`)
- `store_record` with optimistic locking (write path, low volume)
- `/ipns-intercept` (mirror from nginx, write path)
- Sidecar cache (instant pin cache for blob content)
- Metrics, health, reannounce endpoints

### SQLite sharing

Both processes share the same SQLite database via WAL mode (already enabled). Go reads with `PRAGMA journal_mode=wal` and `PRAGMA busy_timeout=5000`. Python writes exclusively. No locking conflicts — WAL supports concurrent readers + single writer.

### Implementation plan

1. Create `go-sidecar/` directory with `main.go`, `go.mod`
2. Implement `/routing-get` handler: open SQLite read-only, `SELECT response_cache FROM ipns_records WHERE ipns_name=?`, return bytes
3. Implement DHT refresh: periodic scan for stale records, POST to kubo, regex-extract Extra, UPDATE if newer sequence
4. Implement `/ws/ipns`: goroutine watches SQLite for changes (polling or inotify), pushes to connected clients
5. Add to `supervisord.conf` as a new process
6. Update nginx upstream `sidecar` to point to Go binary
7. Remove `/routing-get`, `_refresh_and_push`, `/ws/ipns` from Python pinner
8. Load test: verify flat memory over 1+ hour under production load
9. Remove `MAX_RSS_MB` self-restart mechanism

### Expected impact

- Go binary: ~20-30 MB RSS, flat indefinitely
- Python pinner: ~100-200 MB RSS (Nostr + chain validation only), flat
- Total: ~150-250 MB vs current ~4 GB cycling
