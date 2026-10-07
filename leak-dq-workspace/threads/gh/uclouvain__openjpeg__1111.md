# Excessive memory allocation

- URL: https://github.com/uclouvain/openjpeg/issues/1111
- Repo: uclouvain/openjpeg (language: C)
- State: open; created 2018-04-07T16:37:33Z; status ok; passes main

## Issue body

reporter (NONE) · dlemstra · 2018-04-07T16:37:33Z · https://github.com/uclouvain/openjpeg/issues/1111

The @ImageMagick project is using https://github.com/google/oss-fuzz to find bugs in our own library and in libraries that we use. Attached is a test file that will result in an excessive memory allocation due to this line: https://github.com/uclouvain/openjpeg/blob/98cfdd31340509895f3e2a36f667f66bb3cf1ff2/src/lib/openjp2/j2k.c#L2320

Adn this makes `l_nb_tiles = 1337 * 48 = 64176`. We don't know enough about the format but we suspect that a check could be added to do an early exit instead of allocation below

```c
    l_cp->tcps = (opj_tcp_t*) opj_calloc(l_nb_tiles, sizeof(opj_tcp_t));
```

and the allocations inside the loop

```c
    l_current_tile_param = l_cp->tcps;
    for (i = 0; i < l_nb_tiles; ++i) {
```

Test file: [magick-5304QxxxLsVTCFtl.zip](https://github.com/uclouvain/openjpeg/files/1886544/magick-5304QxxxLsVTCFtl.zip)

<!-- 7457 -->

## Comment 379483762

maintainer (COLLABORATOR) · rouault · 2018-04-07T16:56:54Z · https://github.com/uclouvain/openjpeg/issues/1111#issuecomment-379483762

The file cannot be read with the master version due to stricter checks. 
```
===========================================
The extension of this file is incorrect.
FOUND CFtl. SHOULD BE .j2k or .jpc or .j2c
===========================================

[INFO] Start to read j2k main header (0).
[WARNING] Unknown marker
[WARNING] Cannot take in charge mct data within multiple MCT records
[WARNING] Unknown marker
[INFO] Stream reached its end !
[ERROR] Stream too short
ERROR -> opj_dump: failed to read the header
```

That said the underlying problem still exist. OpenJPEG does validate that the number of tiles does not exceed the maximum allowed of 65535 ( https://github.com/uclouvain/openjpeg/blob/98cfdd31340509895f3e2a36f667f66bb3cf1ff2/src/lib/openjp2/j2k.c#L2314 ) , but that still involve significant memory allocations. Not sure there is an easy fix for that

## Comment 379492000

reporter (NONE) · dlemstra · 2018-04-07T19:08:11Z · https://github.com/uclouvain/openjpeg/issues/1111#issuecomment-379492000

Sorry for not mentioning but we are using a clone of the master on a daily basis.

I was wondering if it would be possible to know the minimum size of a tile and check if the input data is long enough.

## Comment 379494794

maintainer (COLLABORATOR) · rouault · 2018-04-07T19:51:08Z · https://github.com/uclouvain/openjpeg/issues/1111#issuecomment-379494794

> I was wondering if it would be possible to know the minimum size of a tile and check if the input data is long enough.

I've managed to create a file of 65535x1 pixels with tiles of size 1x1, so 65535 tiles. Its size is just 3.6 MB, so this is not an effective way of avoiding the issue.

## Comment 379538556

reporter (NONE) · dlemstra · 2018-04-08T10:16:56Z · https://github.com/uclouvain/openjpeg/issues/1111#issuecomment-379538556

Our file is only 244 bytes and I was wondering the allocation could be moved to `opj_jp2_read_header_procedure` and do the allocation right before the `return OPJ_TRUE;`. And before the allocation you could even check if the stream is at least 64176 * number of bytes required for single tile.
