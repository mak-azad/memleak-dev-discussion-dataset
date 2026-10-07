# New vulnerability

- URL: https://github.com/svanderburg/libilbm/issues/8
- Repo: svanderburg/libilbm (language: C)
- State: open; created 2025-09-24T03:21:10Z; status ok; passes main

## Issue body

reporter (NONE) · zdi-disclosures · 2025-09-24T03:21:10Z · https://github.com/svanderburg/libilbm/issues/8

Hello,

Trend Micro's Zero Day Initiative is a security/vulnerability research organization. We have discovered a vulnerability in  libilbm dependency   and we would like to disclose it responsibly to you. Thank you and best regards,


Kholoud Altookhy
Program Manager, Zero Day Initiative
Trend Micro
[ZDI-DISCLOSURES@trendmicro.com](mailto:ZDI-DISCLOSURES@trendmicro.com)

## Comment 3824318117

other (NONE) · mcatanzaro · 2026-01-30T15:28:18Z · https://github.com/svanderburg/libilbm/issues/8#issuecomment-3824318117

Details here: https://gitlab.gnome.org/GNOME/gimp/-/issues/14817

## Comment 3842434603

reporter (NONE) · zdi-disclosures · 2026-02-03T16:46:30Z · https://github.com/svanderburg/libilbm/issues/8#issuecomment-3842434603

> Details here: https://gitlab.gnome.org/GNOME/gimp/-/issues/14817

Access Denied: error code 178ada60f4be0254.

## Comment 3842572737

other (NONE) · mcatanzaro · 2026-02-03T17:11:53Z · https://github.com/svanderburg/libilbm/issues/8#issuecomment-3842572737

I see you've managed to get past Anubis now, but I've forwarded this to our sysadmins anyway since they like to investigate when it blocks humans.

## Comment 5525082070

other (NONE) · PypeBros · 2026-09-03T11:34:01Z · https://github.com/svanderburg/libilbm/issues/8#issuecomment-5525082070

> When decompressing an IFF/ILBM image file, the function [ILBM_unpackByteRun libilbm/src/libilbm/byterun.c] contains a Heap-based Buffer vulnerability that can lead to remote code execution.

```C
/* Allocate decompressed chunk attributes */

        IFF_Long chunkSize = ILBM_calculateRowSize(image) * image->bitMapHeader->h * image->bitMapHeader->nPlanes;
        IFF_UByte *decompressedChunkData = (IFF_UByte*)malloc(chunkSize * sizeof(IFF_UByte)); 
        // ===  [memory allocation is attacker controlled] ===^^

        /* Perform RLE decompression */

        while(readBytes < body->chunkSize)
        {
             // ...
[1]                    decompressedChunkData[count] = body->chunkData[readBytes]; 
                       // =============================^^ 
                      // [There is no check for the [count] variable against the max buffer
                      // length, So this inner loop can write out of bound]
                    readBytes++;
             // ...
    for(i = 0; i < -byte + 1; i++)
                {
                    decompressedChunkData[count] = ubyte;  // << ============ [Same as above]
                    count++;
                }
          }
```

> on line [1], it doesn't check count is outside of buffer decompressedChunkData or not and keep write to this buffer. This is a heap based buffer overflow.

## Comment 5525095681

other (NONE) · PypeBros · 2026-09-03T11:35:10Z · https://github.com/svanderburg/libilbm/issues/8#issuecomment-5525095681

possibly related: (https://www.cve.org/CVERecord?id=CVE-2026-82324)

> A flaw was found in the file-iff (IFF/ILBM) plugin in GIMP. When processing a specially crafted IFF/ILBM image file, the plugin does not properly validate the HAM row size and improperly handles cases where the number of color planes (nPlanes) is zero. This causes a row size mismatch that bypasses memory bounds checking, resulting in heap out-of-bounds reads. This issue can result in an application crash, leading to a denial of service or a limited information disclosure of heap memory contents.

## Comment 5527365637

other (NONE) · mcatanzaro · 2026-09-03T14:34:54Z · https://github.com/svanderburg/libilbm/issues/8#issuecomment-5527365637

[CVE-2026-82324](https://gitlab.gnome.org/GNOME/gimp/-/work_items/16584) is unrelated.

This issue report corresponds to [CVE-2025-10935](https://gitlab.gnome.org/GNOME/gimp/-/issues/14817).
