# [SECURITY] Uninitialized stack memory leaked into cue-point names via short 'labl' subchunk (CWE-457)

- URL: https://github.com/libsndfile/libsndfile/issues/1169
- Repo: libsndfile/libsndfile (language: C)
- State: open; created 2026-09-25T08:21:44Z; status ok; passes offcwe

## Issue body

reporter (NONE) · suywang · 2026-09-25T08:21:44Z · https://github.com/libsndfile/libsndfile/issues/1169

## Summary

When parsing a WAV file containing a `LIST`/`adtl` chunk, the `labl` subchunk handler in `wavlike_subchunk_parse()` reads only `chunk_size` bytes into a 2048-byte stack buffer, but then copies a fixed **256 bytes** (`sizeof (SF_CUE_POINT.name)`) out of that buffer into the cue-point name. A short `labl` subchunk therefore copies up to ~253 bytes of **uninitialized stack memory** into the cue name, and any application can read those bytes back through the public API (`sf_command (SFC_GET_CUE)`). In long-lived processes the leaked bytes are residual stack data (return addresses, saved registers, stdio internals), so this is an information disclosure issue: CWE-457(Use of Uninitialized Variable) leading to CWE-200 (Exposure of Sensitive Information).

## Affected Version

- libsndfile **1.2.2** (current release)
- git master, tested at commit `b9103bd`
- Vulnerable code: `src/wavlike.c`, `case labl_MARKER:` in `wavlike_subchunk_parse()` (lines 1042–1071)
- The issue may also affect earlier versions; a full version-range analysis has not been  performed yet.

## Root Cause

`src/wavlike.c`:

```c
char buffer [2048];
...
case labl_MARKER :
    bytesread += psf_binheader_readf (psf, "44", &chunk_size, &mark_id) ;  // line 1044
    chunk_size -= 4 ;                                                      // line 1046
    chunk_size += (chunk_size & 1) ;
    if (chunk_size < 1 || chunk_size >= SIGNED_SIZEOF (buffer) || ...)     // line 1048: too-big guard only
        goto cleanup_subchunk_parse ;
    bytesread += psf_binheader_readf (psf, "b", buffer, chunk_size) ;      // line 1053: initializes ONLY chunk_size bytes
    buffer [chunk_size] = 0 ;
    ...
    if (psf->cues)
        ...
        memcpy (psf->cues->cue_points [i].name, buffer,
                sizeof (psf->cues->cue_points [i].name)) ;                 // line 1069: ALWAYS 256 bytes
```

A labl subchunk with a declared size of 5 (4-byte mark_id + 1 name byte) passes the guard. After subtracting 4 and applying even-padding, chunk_size becomes 2, so the parser reads 2 bytes from the file into buffer and then sets buffer[2] = 0. Thus only buffer[0..2] are initialized. Nevertheless, the memcpy at line 1069 copies all 256 bytes of SF_CUE_POINT.name. Bytes 3..255 of the cue name are therefore whatever previous stack frames left behind.

Everything needed to reach this point is attacker-controlled: the `cue ` chunk (allocates `psf->cues` with an attacker-chosen cue id), the `LIST`/`adtl` chunk, and the `labl` subchunk size.


## Impact

- Information disclosure: residual stack memory is exposed to whoever can read the cue-point names. In long-lived processes (audio editors, media servers, transcoding pipelines, telephony stacks) the leaked bytes will typically include code/library pointers.
- The amount of leaked data is attacker-tunable via `chunk_size`:   a smaller chunk leaks more, down to 2 file-supplied bytes plus 1 explicit NUL byte,  leaving up to 253 bytes of uninitialized stack memory copied into the cue-point name  .

## Reproduction

```bash
# 1. Build libsndfile (any build works; sanitizer not required — the defect
#    is an uninitialized read within a valid stack buffer)
cmake -B build -DBUILD_SHARED_LIBS=OFF -DBUILD_PROGRAMS=OFF \
      -DBUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF -DENABLE_EXTERNAL_LIBS=OFF
cmake --build build -j

# 2. Build the reader harness (attached: c7_harness_noprime.c)
gcc -g -O0 -Iinclude c7_harness_noprime.c build/libsndfile.a -lm -o c7_harness

# 3a. Direct observation: run on the attached PoC file
./c7_harness poc_c7_labl_leak.wav

# 3b. Under valgrind memcheck with origin tracking (static link recommended
#     to avoid ld.so redirection issues)
gcc -g -O0 -static -Iinclude c7_harness_noprime.c build/libsndfile.a -lm -o c7_harness_static
valgrind --tool=memcheck --track-origins=yes ./c7_harness_static poc_c7_labl_leak.wav
```

Two primed variants are also attached: `c7_harness.c` (pre-fills 16 KiB of
stack with 0x41, makes the leak visible to the naked eye) and
`c7_harness_pattern.c` (fill character given on the command line, for the
control experiment below).


## Error Log

Valgrind memcheck report (valgrind 3.27.1, `--track-origins=yes`), taken with
the unprimed harness. The origin frame is the `char buffer[2048]` stack
allocation in `wavlike_subchunk_parse` (`wavlike.c:956`); the use points are
the application printing the cue name it just got back from `SFC_GET_CUE`:

```
==114947== Use of uninitialised value of size 8
==114947==    at 0x4D918A: _itoa_word (in c7_harness_static)
==114947==    by 0x46D420: __vfprintf_internal (in c7_harness_static)
==114947==    by 0x460EAB: printf (in c7_harness_static)
==114947==    by 0x402064: main (c7_harness_noprime.c:18)
==114947==  Uninitialised value was created by a stack allocation
==114947==    at 0x41C1CA: wavlike_subchunk_parse (wavlike.c:956)
==114947==
==114947== Conditional jump or move depends on uninitialised value(s)
==114947==    at 0x4D919C: _itoa_word (in c7_harness_static)
==114947==    by 0x46D420: __vfprintf_internal (in c7_harness_static)
==114947==    by 0x460EAB: printf (in c7_harness_static)
==114947==    by 0x402064: main (c7_harness_noprime.c:18)
==114947==  Uninitialised value was created by a stack allocation
==114947==    at 0x41C1CA: wavlike_subchunk_parse (wavlike.c:956)
==114947==
==114947== Conditional jump or move depends on uninitialised value(s)
==114947==    at 0x46DC98: __vfprintf_internal (in c7_harness_static)
==114947==    by 0x460EAB: printf (in c7_harness_static)
==114947==    by 0x402064: main (c7_harness_noprime.c:18)
==114947==  Uninitialised value was created by a stack allocation
==114947==    at 0x41C1CA: wavlike_subchunk_parse (wavlike.c:956)
```

(The same report repeats for the remaining name bytes; the full unabridged
log is in the PoC package as `c7_valgrind_notes.txt`, together with the exact
build/run commands.)

Direct observation with the stack primed with 0x41, no tooling required:

```
cue_count=1
SFC_GET_CUE rc=1
cue[0] name as string: 'X'
cue[0] name hex[0..32]: 58 00 00 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41
```

The file supplies exactly one name byte (0x58 = 'X'). The parser reads that byte plus one padding byte and then writes one explicit NUL byte, so only the first three bytes of the cue-point name are initialized. Every byte from offset 3 onward is uninitialized stack memory copied by the 256-byte memcpy at wavlike.c:1069. In a freshly started process whose stack pages have not been reused, the same bytes may read as 00, which is consistent with the source being uninitialized stack residue rather than file content.

Control experiment with different fill bytes (`c7_harness_pattern.c`, fill
character passed as an argument; same PoC file in all runs):

```
fill=0x41 -> cue[0] name hex[0..16]: 58 00 00 41 41 41 41 41 41 41 41 41 41 41 41 41
fill=0x42 -> cue[0] name hex[0..16]: 58 00 00 42 42 42 42 42 42 42 42 42 42 42 42 42
fill=0x5a -> cue[0] name hex[0..16]: 58 00 00 5a 5a 5a 5a 5a 5a 5a 5a 5a 5a 5a 5a 5a
fill=0x30 -> cue[0] name hex[0..16]: 58 00 00 30 30 30 30 30 30 30 30 30 30 30 30 30
```

The leaked tail tracks the prior stack contents exactly, while the first three bytes stay constant (`58 00 00`, from the file), so the exposed bytes come from stale stack memory, not from anything the parser generates. The priming is only there to make this visible; the valgrind log above was taken with the unprimed harness, so the finding does not rely on it.

One more thing worth stressing: the leaked bytes come back through the
documented public API (`sf_command(SFC_GET_CUE)`), the harness simply prints
what the library hands it. No debugger, no `/proc`, no peeking at process
memory. That is what makes this a CWE-457 → CWE-200 disclosure chain rather
than just an uninitialized-read observation.

## Suggested Fix

Copy only the bytes actually read (and NUL-terminate), e.g.:

```c
size_t n = (size_t) chunk_size + 1 ;              /* initialized bytes incl. NUL */
if (n > sizeof (psf->cues->cue_points [i].name))
    n = sizeof (psf->cues->cue_points [i].name) ;
memcpy (psf->cues->cue_points [i].name, buffer, n) ;
```


## PoC

[poc_c7_libsndfile.tar.gz](https://github.com/user-attachments/files/32644077/poc_c7_libsndfile.tar.gz) contains:

- `poc_c7_labl_leak.wav` — 106-byte PoC WAVE file
- `c7_harness_noprime.c` — minimal reader harness (used for the valgrind log)
- `c7_harness.c` — primed variant (stack pre-filled with 0x41 for direct visual confirmation without tooling)
- `c7_harness_pattern.c` — fill-switch variant used in the control experiment
- `gen_poc_c7.py` — generator script that produces the PoC file byte-for-byte
- `c7_valgrind_notes.txt` — exact build/run commands and the full raw valgrind log
