# [Bug]Unbounded memory allocation in RESP aggregate parsing: a single untrusted MAP/ARRAY header triggers OOM (CWE-770 / CWE-789)

- URL: https://github.com/redis/hiredis/issues/1357
- Repo: redis/hiredis (language: C)
- State: open; created 2026-08-28T00:49:12Z; status ok; passes main

## Issue body

reporter (NONE) · 1820893135-pixel · 2026-08-28T00:49:12Z · https://github.com/redis/hiredis/issues/1357

## Summary

The RESP protocol reader accepts an attacker-controlled element count for aggregate types (ARRAY/MAP/SET/PUSH/ATTR) and passes it almost directly to `hi_calloc(elements, sizeof(redisReply*))`. The only bound is `REDIS_READER_MAX_ARRAY_ELEMENTS = 2^32-1` (`read.h:70`), which still lets a single `MAP` header (`%4294967295`) request `hi_calloc(8589934590, 8)` ≈ **68.7 GB**, and a single `ARRAY` header (`*4294967295`) request `hi_calloc(4294967295, 8)` ≈ **34.4 GB**. Any host immediately runs out of memory. ASan reports `out of memory: allocator is trying to allocate 0xffffffff0 bytes`; a production (non-sanitized) build triggers the OS OOM killer, killing the process. This is a deterministic single-packet denial of service against any program that parses an untrusted RESP stream with hiredis (a Redis client, proxy, or library consumer).

- **Affected versions**: hiredis master `29ea279` (post-v1.5.0)
- **Severity**: High (deterministic single-message resource-exhaustion DoS)
- **CWE**: CWE-770 (Allocation of Resources Without Limits or Throttling) / CWE-789 (Uncontrolled Memory Allocation)

## Detail

### Affected code

`src/read.c` `processAggregateItem` (excerpt, lines 570–613):

```c
if ((p = readLine(r,&len)) != NULL) {
    if (string2ll(p, len, &elements) == REDIS_ERR) {
        __redisReaderSetError(r,REDIS_ERR_PROTOCOL,
                "Bad multi-bulk length");
        return REDIS_ERR;
    }
    ...
    if (elements < -1 || (LLONG_MAX > SIZE_MAX && elements > SIZE_MAX) ||
        (r->maxelements > 0 && elements > r->maxelements))   /* maxelements = 2^32-1 */
    {
        __redisReaderSetError(r,REDIS_ERR_PROTOCOL,
                "Multi-bulk length out of range");
        return REDIS_ERR;
    }
    ...
    if (cur->type == REDIS_REPLY_MAP || cur->type == REDIS_REPLY_ATTR) {
        long long maxelements = LLONG_MAX / 2;
        ...
        elements *= 2;                                    /* MAP/ATTR double the count */
    }

    if (r->fn && r->fn->createArray)
        obj = r->fn->createArray(cur,elements);           /* -> hi_calloc(elements, 8) */
    ...
}
```

`createArrayObject` in `hiredis.c:176` calls:

```c
r->element = hi_calloc(elements,sizeof(redisReply*));     /* hiredis.c:184 */
```

and `hi_calloc` in `alloc.h:62` only guards against `size_t` wraparound, not against huge-but-valid values:

```c
static inline void *hi_calloc(size_t nmemb, size_t size) {
    /* Overflow check as the user can specify any arbitrary allocator */
    if (SIZE_MAX / size < nmemb)    /* passes: SIZE_MAX/8 is far above 2^32-1 */
        return NULL;
    return hiredisAllocFns.callocFn(nmemb, size);         /* requests tens of GB */
}
```

**Root cause**: the element count in a RESP aggregate header is taken verbatim from the untrusted input. The only cap, `REDIS_READER_MAX_ARRAY_ELEMENTS = (1LL<<32)-1` (`read.h:70`), is large enough that `elements * sizeof(redisReply*)` (and `elements * 2 * sizeof(redisReply*)` for MAP/ATTR) reaches 34.4–68.7 GB — far beyond any host's memory. The `hi_calloc` wraparound check does not fire on 64-bit platforms because `SIZE_MAX / 8` is ~2^61.

Call chain:

```
redisReaderFeed (read.c:789)
  └─ redisReaderGetReply (read.c:820)
       └─ processItem (read.c:729)
            └─ processAggregateItem (read.c:553)   reads elements from input
                 └─ createArrayObject (hiredis.c:176)
                      └─ hi_calloc(elements, 8) (alloc.h:62)   -> 34.4–68.7 GB request -> OOM
```

## Build the parser fuzzer

The fuzz target `hiredis_reader_fuzzer` drives `redisReaderFeed` + `redisReaderGetReply` with the full RESP parse tree. Build it as follows:

1. Clone hiredis and check out the affected commit:

   ```bash
   git clone https://github.com/redis/hiredis.git
   cd hiredis
   git checkout 29ea279
   ```

2. Save this harness as `harness.c`:

   ```c
   #include "hiredis.h"
   #include "read.h"
   #include <stdint.h>
   #include <stddef.h>

   int LLVMFuzzerInitialize(int *argc, char ***argv) {
       (void)argc; (void)argv;
       return 0;
   }

   int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
       if (size == 0) return 0;
       redisReader *r = redisReaderCreate();
       if (r == NULL) return 0;
       int rv = redisReaderFeed(r, (const char *)data, size);
       if (rv == REDIS_OK) {
           void *reply = NULL;
           redisReaderGetReply(r, &reply);
           if (reply != NULL) freeReplyObject(reply);
       }
       redisReaderFree(r);
       return 0;
   }
   ```

   and this driver as `driver.c` (reads a file argument and calls it):

   ```c
   #include <stdio.h>
   #include <stdint.h>
   #include <stdlib.h>
   extern int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size);
   int main(int argc, char** argv) {
       if (argc < 2) return 1;
       FILE* f = fopen(argv[1], "rb"); if (!f) return 1;
       fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
       uint8_t* buf = (uint8_t*)malloc((size_t)sz);
       if (!buf) return 1;
       fread(buf, 1, (size_t)sz, f); fclose(f);
       LLVMFuzzerTestOneInput(buf, (size_t)sz);
       free(buf);
       return 0;
   }
   ```

3. Compile with ASan + UBSan:

   ```bash
   clang -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer \
       -I . harness.c driver.c read.c hiredis.c sds.c alloc.c net.c async.c sockcompat.c dict.c \
       -o hiredis_reader_fuzzer
   ```

## POC (tested on the unmodified source)

Save as `poc_map.bin` — a single RESP MAP header with element count `4294967295`:

```text
%4294967295
```

(hex: `25 34 32 39 34 39 36 37 32 39 35 0d 0a` — 12 bytes)

```bash
ASAN_OPTIONS=detect_leaks=0 ./hiredis_reader_fuzzer poc_map.bin
```

An even simpler trigger is the RESP ARRAY header:

```text
*4294967295
```

(hex: `2a 34 32 39 34 39 36 37 32 39 35 0d 0a` — 12 bytes)

## Trigger result

ASan (the MAP case, confirmed on the unmodified source):

```
ERROR: AddressSanitizer: out of memory: allocator is trying to allocate 0xffffffff0 bytes
READ-ALLOC request 68.7GB; stack: __interceptor_calloc <- hi_calloc alloc.h:67 <-
createArrayObject hiredis.c:184 <- processAggregateItem read.c:618 <-
processItem read.c:729 <- redisReaderGetReply read.c:846 <- LLVMFuzzerTestOneInput harness.c:39
```

ASan (the ARRAY case):

```
ERROR: AddressSanitizer: out of memory: allocator is trying to allocate 0x7fffffff8 bytes
ALLOC request 34.4GB; stack: __interceptor_calloc <- hi_calloc alloc.h:67 <-
createArrayObject hiredis.c:184 <- processAggregateItem read.c:618 <- processItem <-
redisReaderGetReply <- LLVMFuzzerTestOneInput harness.c:39
```

- Replay exit code: `1` (ASan abort); under AFL++ the same input raises `sig:06` (SIGABRT)
- Deterministic: yes — the 12-byte `%4294967295\r\n` reproduces reliably, 8 independent crash files all confirm the same root cause

<img width="2272" height="647" alt="Image" src="https://github.com/user-attachments/assets/d77a5014-f81e-4a91-9c48-9cc18dde2963" />

## Suggested fix

Cap the element count to a realistic value before allocation, in `processAggregateItem` (and keep the existing `maxelements` check applied to the *doubled* value for MAP/ATTR):

```c
/* reject aggregate headers whose total allocation would exceed a sane bound,
   e.g. 1M elements (~8 MB of reply pointers) */
if (elements > 1024 * 1024) {
    __redisReaderSetError(r, REDIS_ERR_PROTOCOL, "Multi-bulk length out of range");
    return REDIS_ERR;
}
```

A matching fix should also be applied to `hi_calloc`/`hi_malloc` call sites that derive an allocation size from an untrusted length field, so a huge-but-not-wrapping count cannot request tens of gigabytes.

## Comment 5447571024

maintainer (COLLABORATOR) · michael-grunder · 2026-08-28T02:17:17Z · https://github.com/redis/hiredis/issues/1357#issuecomment-5447571024

I'm slightly skeptical about attacks that require an "evil" Redis server. 

That said lowering the default max elements  is probably fine but `1024 * 1024` is too low and would break real-world applications.

Hiredis on my system had no problem with a `100,000,000` element list (other than it took a long time):
```bash
❯ redis-cli llen biglist; time redis-cli lrange biglist 0 -1 |tail
(integer) 100000000
99999991
99999992
99999993
99999994
99999995
99999996
99999997
99999998
99999999
100000000
redis-cli lrange biglist 0 -1  12.90s user 6.92s system 73% cpu 26.922 total
tail  0.68s user 0.23s system 3% cpu 26.921 total
```

Like I said, I'm not sure what the right value is. maybe `2^28` (~260,000,000)?

## Comment 5447768047

reporter (NONE) · 1820893135-pixel · 2026-08-28T02:47:34Z · https://github.com/redis/hiredis/issues/1357#issuecomment-5447768047

Thanks for the detailed testing — the 100M-element list is a fair point, and a hard 1M cap would indeed break legitimate workloads. Let me reframe the issue and propose a fix that avoids a blunt cap.

**The real problem is amplification, not the absolute count.** A 12-byte input (`*4294967295\r\n`) makes `processAggregateItem` call `hi_calloc(4294967295, 8)` ≈ 34 GB *before any of the claimed elements have actually been received*. Your 100M-list case is safe because the wire data for 100M elements is hundreds of MB, so the allocation stays proportional to real input. The malicious case has no such proportionality — the smallest possible packet produces the largest possible allocation.

**On the threat model:** hiredis isn't only used as `redis-cli` against a trusted server. It's embedded in proxies, gateways, monitoring/test tools, and apps that parse RESP from a network boundary. A single crafted packet is a one-shot DoS there. Even for a direct connection, cluster/sentinel failover or a MITM on the wire gives an attacker one chance to inject this header.

**Suggested fix (no fixed cap needed):** bound the pre-allocation by the data actually buffered. Each RESP element requires at least a few bytes on the wire, so the declared `elements` count is only plausible up to `~r->len`. Something like:

```c
/* in processAggregateItem, before createArrayObject: */
size_t elem_size = sizeof(redisReply*);
if (elements > (long long)(r->len / elem_size) * 64) {
    __redisReaderSetError(r, REDIS_ERR_PROTOCOL, "Multi-bulk length out of range");
    return REDIS_ERR;
}
```

This kills the amplification (a 12-byte input can never claim 4B elements) while leaving genuinely large lists — including your 100M case — completely unaffected, because real lists are backed by proportionally large data. If you'd prefer a numeric cap instead, `2^28` (~268M) seems reasonable. Happy to turn this into a concrete patch.


## Comment 5448696857

maintainer (COLLABORATOR) · michael-grunder · 2026-08-28T05:09:35Z · https://github.com/redis/hiredis/issues/1357#issuecomment-5448696857

> The real problem is amplification, not the absolute count. A 12-byte input (*4294967295\r\n) makes processAggregateItem call hi_calloc(4294967295, 8) ≈ 34 GB before any of the claimed elements have actually been received.

Agreed, it would be easy for malicious input to stall or crash a server with very little effort.

Your wire length heuristic sounds like a good strategy. Another I suppose would be an upper bound to how many elements we allocate at once, then grow in chunks of that size until we've consumed the  data.

The Redis folks have been taking a more active role in the Repo so I'll let them weigh in on their preference.

## Comment 5452589358

reporter (NONE) · 1820893135-pixel · 2026-08-28T12:37:27Z · https://github.com/redis/hiredis/issues/1357#issuecomment-5452589358

Sounds good — I think chunked allocation is the cleaner fix and fully addresses the amplification too. Happy to draft a patch either way; I'll wait for the Redis team's preference.
