# stb_truetype.h: heap-use-after-free in ttUSHORT via stbtt__GetGlyphShapeTT

- URL: https://github.com/nothings/stb/issues/2002
- Repo: nothings/stb (language: C)
- State: open; created 2026-09-10T22:39:54Z; status ok; passes offcwe

## Issue body

reporter (NONE) · KhaledAlsaqabi · 2026-09-10T22:39:54Z · https://github.com/nothings/stb/issues/2002

Title:
stb_truetype.h: heap-use-after-free in ttUSHORT via stbtt__GetGlyphShapeTT

Description:
## Summary

A heap-use-after-free vulnerability was discovered in `stb_truetype.h` v1.26
(commit `2c980bb`) through coverage-guided fuzzing with AFL++ using
ASAN/UBSAN/CMPLOG instrumentation.

This is a **different vulnerability class** from the heap-buffer-overflow
reported in #1905. This is a **use-after-free (CWE-416)**, not an OOB read.

## Details

`stbtt__rasterize()` frees a heap buffer at line 3544. A subsequent call to
`stbtt__GetGlyphShapeTT()` reads from the freed memory region via `ttUSHORT()`
at line 1286.

**Impact:** Crash (DoS). Potential code execution if freed memory is
reallocated with attacker-controlled data.

## ASAN Output

ERROR: AddressSanitizer: heap-use-after-free on address 0x6ef4bb5e8318
READ of size 1 at 0x6ef4bb5e8318 thread T0
    #0 ttUSHORT stb_truetype.h:1286:55
    #1 stbtt__GetGlyphShapeTT stb_truetype.h:1695:13
    #2 stbtt_GetGlyphShape stb_truetype.h:2300:14
    #3 stbtt_GetGlyphBitmapSubpixel stb_truetype.h:3718:20
    #4 stbtt_GetGlyphBitmap stb_truetype.h:3755:11

freed by thread T0 here:
    #0 free
    #1 stbtt__rasterize stb_truetype.h:3544:4
    #2 stbtt_Rasterize stb_truetype.h:3702:7
    #3 stbtt_GetGlyphBitmapSubpixel stb_truetype.h:3746:10

previously allocated here:
    #0 malloc
    #1 stbtt__GetGlyphShapeTT stb_truetype.h:1680:51

## Reproduction

```c
#define STB_TRUETYPE_IMPLEMENTATION
#include "stb_truetype.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char *data = malloc(sz);
    fread(data, 1, sz, f);
    fclose(f);
    stbtt_fontinfo font;
    if (stbtt_InitFont(&font, data, 0)) {
        float scale = stbtt_ScaleForPixelHeight(&font, 32.0f);
        for (int g = 0; g < 64 && g < font.numGlyphs; g++) {
            int w, h, xo, yo;
            unsigned char *bmp = stbtt_GetGlyphBitmap(&font, scale, scale, g, &w, &h, &xo, &yo);
            if (bmp) stbtt_FreeBitmap(bmp, NULL);
        }
    }
    free(data);
}

clang -fsanitize=address,undefined -g -O1 test.c -lm -o test
./test bug1_uaf.ttf

Environment

- stb_truetype.h v1.26 (commit 2c980bb59875b0d32144a71867fbdebb2f77cd20)
- clang 21.1.8, Linux x86_64
- AFL++ 5.03a with ASAN + UBSAN + CMPLOG

PoC

See attached: bug1_uaf.ttf (22964 bytes)

---

[bug1_uaf.ttf.gz](https://github.com/user-attachments/files/32079199/bug1_uaf.ttf.gz)
