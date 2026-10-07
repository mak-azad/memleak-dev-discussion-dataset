# Audit by claude opus 5 from feat/cache branch

- URL: https://github.com/Mitotow/c-http-server/issues/1
- Repo: Mitotow/c-http-server (language: C)
- State: open; created 2026-09-07T11:37:55Z; status ok; passes main

## Issue body

reporter (OWNER) · Mitotow · 2026-09-07T11:37:55Z · https://github.com/Mitotow/c-http-server/issues/1

# Security & performance audit — 4 remote crashes, memory corruption, no build system

**Branch audited:** `feat/cache` @ `c747b72` (cross-checked against `main` and `dev`)
**Scope:** all 1383 lines of C in the repo
**Labels:** `security` `bug` `performance` `good first issue (P4 only)`

---

## Summary

Full audit of the server. The module split (`server` / `http` / `lib` / `utils`) is sound — the
epoll rewrite in P3 reuses `createRequest` / `handleRequest` almost unchanged because of it.
The problems are all in memory lifetime and input validation.

**There are four ways to crash the server remotely, one of which corrupts the stack.**

Two things to know before reading:

1. **`feat/cache` is currently *more* broken than `main`.** The cache introduced a double-free,
   and `HEAD` requests segfault on it 100% of the time.
2. **Nearly every finding is one of three repeated patterns:**
   - *Who owns this pointer?* — structs whose fields point into other structs, then both get freed
     (leaks, double-frees, use-after-free)
   - *Is this input trusted?* — attacker-controlled strings copied into fixed buffers; fields
     dereferenced without a NULL check
   - *Is this function thread-safe?* — threads calling libc functions with hidden global state

---

## P0 — Remotely triggerable crashes and memory corruption

- [x] ### P0.1 — A 9-byte request kills the entire server

  `http/response.c` → `addDefaultHeadersResponse()`

  ```c
  char *connection = req->connection;
  if (connection == NULL) {
    if (strcmp(req->httpVersion, HTTP_1_0)) {   // <-- req->httpVersion can be NULL
  ```

  `isValidRequest()` correctly rejects a request with no HTTP version — but `handleClient()` then
  calls `createResponse(req, BAD_REQUEST)` on that same invalid request, which walks straight into
  this `strcmp`. `GET /\r\n\r\n` (no version, no `Host`) leaves both `httpVersion` and `connection`
  NULL → segfault. Threads share one address space, so one thread crashing takes the process down.

  **Fix:** don't trust `req` here. Treat a NULL version as HTTP/1.0 and force `Connection: close`
  on error responses:

  ```c
  const char *version = req->httpVersion ? req->httpVersion : HTTP_DEFAULT_VERSION;
  ```

  > "I validated it upstream" is not protection if the error path still dereferences it. Error
  > paths handle the *most* malformed input, so they need the *most* defensive code.

- [ ] ### P0.2 — Stack buffer overflow + stack memory disclosure in `sendResponse`

  `http/response.c` → `sendResponse()`

  ```c
  char header[RESPONSE_HEADER_SIZE];      // 512 bytes
  char *cur = header;
  char *const end = header + sizeof(header);
  cur += snprintf(cur, end - cur, "%s %d %s\r\n", res->httpVersion, ...);
  cur += snprintf(cur, end - cur, "Date: %s\r\n", res->date);
  ```

  `snprintf` returns **the length it *would* have written**, not what it wrote. Both
  `res->httpVersion` and `res->connection` are `strdup`'d straight from the request and can be
  ~4000 bytes long.

  - Request line `GET / <3000 bytes>` → first `snprintf` returns ~3000 → `cur = header + 3000`,
    past `end`.
  - `end - cur` is now **negative**, and `snprintf`'s size parameter is `size_t` (unsigned) → it
    becomes ~18 quintillion → the next `snprintf` writes out of bounds. **Stack smash.**
  - Then `send(client_socket, header, cur - header, 0)` sends 3000 bytes out of a 512-byte stack
    buffer → **leaks stack contents to the attacker**, including saved return addresses.

  **Fix (both parts needed):**

  1. Never let `cur` pass `end`:
     ```c
     static bool hdr_append(char **cur, char *end, const char *fmt, ...) {
       int n = vsnprintf(*cur, end - *cur, fmt, ap);
       if (n < 0 || n >= end - *cur) return false;   // truncated: bail out
       *cur += n;
       return true;
     }
     ```
     If any append fails, send a fixed `500` instead.
  2. **Cap the inputs at parse time** — a request-line token over 64 bytes, or a header value over
     `HTTP_MAX_HEADER_SIZE`, is a `400`. Never reflect unbounded client data into a fixed buffer.

  > `snprintf` is safe about *writing* but its *return value* is a trap. This is a well-known CVE
  > class. `cur += snprintf(...)` is only correct with the bounds check.

- [ ] ### P0.3 — `strtok` in a multithreaded server is a data race

  `http/request.c` → `readRequest()` uses `strtok(rest, HTTP_DELIMITER)`. `strtok` keeps its parse
  position in a **single global variable**. Two threads parsing concurrently scribble over each
  other's state → garbage routes, NULL fields, and crashes that only appear under load.

  **Fix:** `strtok_r` with a local `char *saveptr`. (Already used correctly in `strutils.c` and
  `readHeader` — this one was just missed.)

  **`getDate()` has the same bug**: `gmtime()` returns a pointer to a static struct → `gmtime_r`.

  > In a threaded program, any libc function with hidden state is off limits: `strtok`, `gmtime`,
  > `localtime`, `asctime`, `strerror`, `getenv`+`setenv`.

- [ ] ### P0.4 — The cache hands out pointers it then frees (double-free / use-after-free)

  `server.c` → `handleGet()`, cache-hit path:

  ```c
  if (!isHead) content = entry->content;   // borrowed pointer, owned by the cache
  ...
  res = createContentResponse(req, contentType, content, contentSize);
  ```

  and `destroyResponse()` does `FREE_ALL(res->date, res->content, res)`.

  Every cache **hit** frees the cache's own buffer. The entry is left holding a dangling pointer;
  the next hit is a **use-after-free**, the one after a **double-free**. Two requests for the same
  file is all it takes.

  Worse: `get_cache_entry_by_path()` unlocks the mutex *before* returning the pointer, so another
  thread can evict and free the entry while you're reading it.

  **Fix:** make ownership explicit.

  ```c
  typedef struct {
    ...
    char *content;
    bool owns_content;   // true = destroyResponse frees it; false = borrowed
  } response_t;
  ```

  Cache hits set `owns_content = false`. Long term, refcount entries (`entry->refs++` under the
  lock, release after send) so eviction can't free a buffer that's in flight.

- [ ] ### P0.5 — Every `HEAD` request crashes the cache branch

  Same function, cache-miss path: when `isHead` is true, `content` stays `NULL` but `contentSize`
  is set from `getFileSizeFromPath()`. Then:

  ```c
  if (contentSize > 0) {
    if (!entry) {
      char *content_cp = malloc(contentSize);
      memcpy(content_cp, content, contentSize);   // content is NULL -> segfault
  ```

  **Fix:** skip the cache-fill entirely when `content == NULL`. `dev` had this right with an early
  `return res;` in the HEAD branch — that early return was lost in the cache merge.

- [ ] ### P0.6 — The cache's linked list is structurally broken

  `lib/cache.c`, independent of P0.4:

  - `add_cache_entry()` never sets `entry->prev` on the tail-append path → `rm_cache_entry()`'s
    `entry->prev->next` is a NULL deref.
  - `rm_cache_entry()` does `entry->next->prev = ...` without checking `entry->next` — NULL for the
    tail. Another NULL deref.
  - The `is_full()` eviction branch does `tmp->prev->next = entry` (NULL deref when evicting the
    head), never unlinks or frees the evicted entry, never updates `tail`, and still increments
    `current_entries` — so the cache grows past `max_entries` forever.
  - `destroy_cache()`: `FREE_ALL(tmp->filepath, tmp->content, tmp); tmp = tmp->next;` reads
    `tmp->next` **after freeing `tmp`** — use-after-free. Save `next` first.
  - `clean_cache()` unlocks, calls `rm_cache_entry` (which relocks), then reads `tmp->prev` on a
    node that may already be gone.
  - `hash_table` is declared, set to NULL in `init_file_cache`, and never used — every lookup is an
    O(n) linear scan under a global mutex.

  **Fix:** rewrite `lib/cache.c` as one coherent unit rather than patching six spots. A real hash
  table on `filepath` for lookup + an intrusive doubly-linked LRU list, with `_locked` internal
  helpers that assume the caller holds the mutex. Add `st_mtime`/`st_size` per entry and revalidate
  on hit so edited files aren't served stale.

  > The lock/unlock/relock pattern in `add_cache_entry` and `clean_cache` is the tell: public
  > functions calling public functions. **One public function = one lock acquisition**, and it
  > calls only `_locked` helpers.

- [ ] ### P0.7 — A client disconnecting mid-download kills the server

  `send()` on a socket the peer closed raises `SIGPIPE`, which terminates the process by default.
  Any client that requests a large PNG and hangs up takes the server down — `curl ... | head -c 1`
  does it by accident.

  **Fix:** `signal(SIGPIPE, SIG_IGN);` at startup **and** `MSG_NOSIGNAL` on every `send()`.

- [ ] ### P0.8 — `stopServer` double-frees every route

  `stopServer()` calls `destroyRouter(ctx->router)` then `destroyConfig(ctx->config)`. But
  `initRouter()` stores the config's array by pointer (`router->routes = routes`), so both free the
  same `route_t` objects and the same array. Ctrl-C reliably double-frees.

  **Fix:** the router **borrows**, it does not own. `destroyRouter` frees only the `router_t`;
  `destroyConfig` stays the sole owner of routes.

  Also: `destroyRouter` does `FREE_ALL(router, router->routes)` — safe only because the macro's
  array initializer evaluates both pointers before freeing anything. Don't rely on that.

- [ ] ### P0.9 — Unbounded thread creation

  `handleConnections()` calls `pthread_create` per connection with no limit. Each thread reserves
  8 MB of virtual address space; a few thousand idle connections exhausts the process.
  `KEEP_ALIVE_MAX 100` is advertised in response headers but **never enforced** — `handleClient`'s
  loop has no counter, so a connection can hold a thread forever.

  Addressed by P3.

---

## P1 — Memory leaks and lifetime bugs

- [ ] `getAbsolutePath()` (`lib/filesystem.c`) leaks `strcp` on the `realpath` failure path
      (`return NULL` before `free(strcp)`). Runs on **every 404**, so it's a leak an attacker can
      drive. It also `malloc`s a full `PATH_MAX` (4 KB) per call — use a stack buffer and `strdup`
      the result, or pass `NULL` to `realpath` and let it allocate exactly.
- [ ] `parseLine()` leaks `key` and `value` on every successful line (`strdup`'d by `strkeyval`,
      never freed). Startup-only, but it's the same ownership blind spot.
- [ ] `config->base_href` is a string literal from `initConfig()` until a config file overwrites it
      with a `malloc`'d path. `destroyConfig` never frees it — and if it did, it would crash when no
      config file exists. **Fix:** always `strdup(DEFAULT_BASEHREF)` so ownership is uniform.
      *Never mix "sometimes a literal, sometimes heap" in one field.*
- [ ] `readFile()` never checks `malloc`'s return before `fread`, and has **no size limit** — a 1 GB
      file in `public/` becomes a 1 GB allocation per concurrent request. Add `MAX_STATIC_FILE_SIZE`
      and return 500 above it. (P3's `sendfile()` replaces this entirely.)
- [ ] `response_t.httpVersion` / `.connection` alias `request_t`'s buffers, but `.connection` can
      *also* be a string literal (`CONN_CLOSE`) from `addDefaultHeadersResponse`. Nothing frees them
      so it works by accident. `strdup` them or document the borrow — but pick one.

---

## P2 — HTTP correctness (each is also a security boundary)

- [ ] **No check that the request is complete.** `handleClient` does one `recv()` into a 4096-byte
      buffer and parses whatever arrived. A request split across two TCP segments parses as two
      broken requests; a request over 4095 bytes is truncated and its tail is parsed as a *new*
      request on the next loop iteration. That is the shape of **HTTP request smuggling**.
      **Fix:** accumulate into a per-connection buffer until `\r\n\r\n`; `400` and close if it
      exceeds `HTTP_MAX_REQUEST_SIZE`. P3 requires this anyway.
- [ ] **No query-string handling.** `GET /index.html?v=2` looks for a file literally named
      `index.html?v=2` → 404. Truncate the route at the first `?`.
- [ ] **No percent-decoding.** `/images/my%20file.png` fails. When you add decoding, decode
      **before** the traversal check, never after — decoding after validation is the classic
      path-traversal bypass.
- [ ] **`getExtension()`** uses `strrchr(path, '.')` over the whole path. For `/a.b/index` it
      returns `"b/index"`. Search only after the last `/`.
- [ ] **The HTTP/1.0 keep-alive test is inverted.** `if (strcmp(req->httpVersion, HTTP_1_0))` is
      *true* when the version is **not** 1.0 — so HTTP/1.1 gets `close` and HTTP/1.0 gets
      `keep-alive`, exactly backwards. This is likely why the server feels slow in a browser: every
      1.1 request reopens a TCP connection.
- [ ] **Bodyless responses (404/400/403) send no `Content-Length`.** With `Connection: keep-alive`
      the client can't tell the response ended and hangs until timeout. Always emit
      `Content-Length: 0`.
- [ ] **`405 Method Not Allowed`**, not `400`, for POST/PUT/DELETE — plus an `Allow: GET, HEAD`
      header. Add 405 to the `status[]` table.
- [ ] **Partial `send()` is ignored.** `send()` may write fewer bytes than asked for large files;
      the remainder is never sent, so big images silently truncate. Loop until fully written (or let
      epoll drive it in P3).
- [ ] **`is_valid_path()` prefix check has no boundary.** It compares `base_href_length` bytes but
      doesn't require the next character to be `/`, so base `/srv/public` would also accept
      `/srv/public-backup/secrets`. Check `ptr[base_href_length] == '/'`.
- [ ] **Add security headers** to every response: `X-Content-Type-Options: nosniff`,
      `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`.
- [ ] **Typo:** `http/http.h` — `#define CTYPE_XML "test/xml"` should be `"text/xml"`.

---

## P3 — Rewrite to an epoll event loop

Replaces P0.9 and is the single biggest performance change: from ~1 thread (8 MB VM) per connection
to one `epoll_wait` loop handling tens of thousands of connections, with `sendfile()` doing
zero-copy file transfer in the kernel.

**Design — one new file, `lib/eventloop.c` / `.h`:**

```c
typedef enum { CONN_READING, CONN_WRITING_HEADER, CONN_WRITING_BODY, CONN_CLOSING } conn_state_t;

typedef struct {
  int fd;
  conn_state_t state;
  char  *inbuf;  size_t in_len, in_cap;            // accumulates until \r\n\r\n
  char  *outbuf; size_t out_len, out_sent;         // response header
  int    file_fd; off_t file_offset, file_size;    // body, sent via sendfile()
  time_t last_activity;
  int    requests_served;                          // enforces KEEP_ALIVE_MAX at last
} connection_t;
```

**Steps:**

- [ ] `setNonBlocking(fd)` helper (`fcntl` + `O_NONBLOCK`) — apply to the listener and every
      accepted socket. **A blocking `read` in an event loop stalls every other connection.**
- [ ] Replace `handleConnections` with `epoll_create1` + `epoll_ctl(ADD)` on the listener.
      Level-triggered to start (edge-triggered requires draining every fd to `EAGAIN`).
- [ ] Accept loop: `accept4(..., SOCK_NONBLOCK)` in a `while` until `EAGAIN`; allocate a
      `connection_t`; store it in `ev.data.ptr` so no fd→connection lookup is needed.
- [ ] `EPOLLIN`: `read()` into `inbuf` (growing, capped at `HTTP_MAX_REQUEST_SIZE`). Only once
      `\r\n\r\n` is present call the existing `createRequest()` / `handleRequest()` — those stay
      almost unchanged, which is the payoff of the module split.
- [ ] `EPOLLOUT`: `send()` the header from `outbuf` honouring partial writes, then
      `sendfile(fd, file_fd, &offset, remaining)` for the body until `EAGAIN`. **`sendfile` never
      copies the file into userspace** — this deletes the entire `readFile` malloc/free per request.
- [ ] Idle timeouts: a `timerfd` ticking every second, sweeping connections whose `last_activity` is
      older than `KEEP_ALIVE_TIMEOUT`, plus a hard `requests_served >= KEEP_ALIVE_MAX` cap.
- [ ] **Scale out later, not now:** once single-threaded epoll works, add N worker processes each
      with `SO_REUSEPORT` on its own listener — the kernel load-balances and you need no locks at
      all. Much easier path to multicore than threads + mutexes.

**Impact on the cache (P0.4 / P0.6):** with `sendfile()`, the cache should hold **open file
descriptors + stat metadata**, not file contents. That sidesteps the whole content-ownership
problem, uses far less memory, and is what nginx does.

**Also fix while in `createServer`:**

- [ ] `if ((server_fd = socket(...)) == 0)` — `socket()` returns **-1** on error; fd 0 is valid.
      Use `< 0`.
- [ ] Add `SO_REUSEADDR` (and `SO_REUSEPORT` for the last step) so restarts don't fail with
      "Address already in use" during `TIME_WAIT`.
- [ ] `accept(ctx->server_fd, &ctx->address, &ctx->addrlen)` writes the **peer** address into the
      shared server context — a data race across threads today, and it clobbers the bind address.
      Use a local `struct sockaddr_storage`.
- [ ] `ctx->address` is a `struct sockaddr` (16 bytes). It happens to fit `sockaddr_in`, but it will
      silently truncate the day IPv6 is added. Use `struct sockaddr_storage`.
- [ ] Move the `bind()` out of `setRouter()` — binding a socket is not part of setting a router, and
      the hidden coupling means route setup must happen before listen for non-obvious reasons.

**Logging is on the hot path:**

- [ ] `writeLog(LOG_DEBUG, ...)` runs several times per request and does `vsnprintf` twice +
      `malloc` + `memmove` + `printf`, with **no level filter at all** despite `#define DEBUG true`
      existing and being unused. Add a runtime `log_level` check as the *first line* of `writeLog`
      so debug logging costs one comparison in release.
- [ ] `print()` uses `perror()` for ERROR/FATAL, which appends `strerror(errno)` even when `errno`
      is stale and unrelated. Use `fprintf(stderr, ...)` and pass errno explicitly when you mean it.
- [ ] `static const status[]` and `content_types[]` live in `http/http.h`, so **every .c file that
      includes it gets a private copy**. Make them `extern` in the header, define once in `http.c`.
- [ ] `#include <asm-generic/errno-base.h>` / `<bits/pthreadtypes.h>` (added on `dev`/`cache`) are
      internal glibc headers — use `<errno.h>` and `<pthread.h>`.

---

## P4 — Build system and sanitizers

There is currently **no build system**. `build.sh` was deleted in `5dec606`, and it was
`gcc *.c -o bin/server`, which never compiled `http/`, `lib/` or `utils/` anyway.

- [ ] New `Makefile` at the repo root:

  ```make
  CC      := gcc
  CFLAGS  := -std=c11 -D_GNU_SOURCE -Wall -Wextra -Wshadow -Wconversion \
             -Wstrict-prototypes -Wpointer-arith -Wwrite-strings
  SRC     := $(wildcard *.c http/*.c lib/*.c utils/*.c)

  release: CFLAGS += -O2 -DNDEBUG -fstack-protector-strong -D_FORTIFY_SOURCE=2
  debug:   CFLAGS += -O0 -g3 -fsanitize=address,undefined -fno-omit-frame-pointer
  tsan:    CFLAGS += -O1 -g  -fsanitize=thread
  ```

**Use the `make debug` binary for all development.** AddressSanitizer catches P0.2, P0.4, P0.5, P0.6
and every leak in P1 on the first request — the single highest-value change in this whole issue.
`make tsan` catches P0.3.

Existing compiler warnings that are real bugs, not noise:

- [ ] `server.c` — `size_t bytes_sent; if (... < 0)` is **always false** (unsigned), so the response
      error path is dead code. Use `ssize_t`.
- [ ] `lib/conf.c` — `realloc(config->routes, sizeof(router_t) * length)` sizes by the **wrong type**
      (`router_t`, 16 bytes, vs `route_t *`, 8). It over-allocates so it isn't unsafe *today*, but
      it will bite when `router_t` shrinks.
- [ ] `lib/conf.c` — `parseRoutes` uses `uint8_t tmp` as an offset into a line up to
      `CONFIG_LINE_BUFF` (256) bytes. Off-by-one from overflow. Use `size_t`.
- [ ] `utils/strutils.c` — `strcpyft(str, from, to)` writes `to-from+1` chars into a `to-from+1`
      buffer then overwrites the last with `\0`, silently **dropping the final character**. It
      currently "works" only because that character is the `\n` from `fgets`.
- [ ] `utils/strutils.c` — `str_to_uint16` uses `strtoul` (unsigned) into a `long`, so `"-1"` becomes
      port 65535 instead of an error. Reject a leading `-`.
- [ ] `server.c` (dev/cache) — the "SLOW REQUEST" timer uses `clock()`, which measures **CPU** time,
      not wall-clock, and on glibc aggregates across all threads. Use
      `clock_gettime(CLOCK_MONOTONIC, ...)`.
- [ ] Various `for (int i = 0; i < router->routes_size; i++)` signed/unsigned comparisons — use
      `size_t`.

---

## Suggested order of work

Each step is independently testable. Don't batch them.

1. **P4 first** — Makefile + ASan. The tooling is needed to verify everything else.
2. **P0.1, P0.2, P0.3, P0.7** — the four remote crashes. Small, surgical, highest value.
3. **P0.4, P0.5, P0.6** — rewrite `lib/cache.c` cleanly. Consider reverting the cache to a
   known-good state and rebuilding rather than patching.
4. **P0.8, P1** — ownership pass: for every `malloc`, write down who frees it.
5. **P2** — HTTP correctness. Cheap, and makes the server behave properly in a browser.
6. **P3** — the epoll rewrite. Last, on its own branch, with everything else green.

---

## Verification

**Build:** `make debug && ./bin/server` (with `config.example` copied to `config`).

**Crash reproduction — each must return a proper response, not a segfault:**

```sh
printf 'GET /\r\n\r\n'                        | nc -q1 localhost 8080  # P0.1
printf "GET / HTTP/$(head -c 3000 /dev/zero | tr '\0' 'A')\r\nHost: x\r\n\r\n" \
                                              | nc -q1 localhost 8080  # P0.2
curl -sI localhost:8080/index.html                                     # P0.5 (HEAD)
curl -s localhost:8080/index.html >/dev/null; curl -s localhost:8080/index.html  # P0.4 (2nd hit)
curl -s localhost:8080/images/cethiel-desert-edit.png | head -c 1      # P0.7 (SIGPIPE)
curl -s 'localhost:8080/index.html?v=2'                                # P2 query string
curl -s localhost:8080/../../../etc/passwd                             # must be 403/404
```

**Leaks:** `valgrind --leak-check=full --show-leak-kinds=all ./bin/server`, run the requests above,
then Ctrl-C. Target: zero definitely-lost bytes. (ASan reports leaks on exit too.)

**Races:** `make tsan`, then `for i in $(seq 200); do curl -s localhost:8080/ & done; wait`.
TSan must report clean — this is what proves P0.3 and the cache locking are fixed.

**Correctness:** `curl -v` and confirm HTTP/1.1 gets `Connection: keep-alive`, every response has a
`Content-Length` (including 404s), `HEAD` returns headers with **no body**, and a POST returns `405`
with an `Allow` header.

**Performance (before/after P3):** `wrk -t4 -c400 -d30s http://localhost:8080/index.html` — record
requests/sec and peak RSS before the epoll rewrite and after.

**Large-file integrity (P2 partial-send):**
`curl -s localhost:8080/images/victory-dance0015.png | cmp - public/images/victory-dance0015.png`
