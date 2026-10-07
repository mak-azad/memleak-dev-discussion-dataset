# Memory leak in PolaroidImage when the image has a caption

- URL: https://github.com/ImageMagick/ImageMagick/issues/8994
- Repo: ImageMagick/ImageMagick (language: C)
- State: open; created 2026-10-02T03:28:19Z; status ok; passes main

## Issue body

reporter (NONE) · Watson1978 · 2026-10-02T03:28:19Z · https://github.com/ImageMagick/ImageMagick/issues/8994

### ImageMagick version

7.1.2-32

### Operating system

Linux

### Operating system, version and so on

 CachyOS Linux (rolling), kernel 7.2.8, x86_64. ImageMagick 7.1.2-32 Q16-HDRI. valgrind 3.25.1.

### Description

`PolaroidImage` leaks about 4 KB each time it draws a caption and the gravity is not set.

In `MagickCore/visual-effects.c`, `PolaroidImage` calls `CloneString(&annotate_info->geometry,AcquireString(geometry))`.

https://github.com/ImageMagick/ImageMagick/blob/a879b231b35cbc0655e21632f09ce856dcf7a1fe/MagickCore/visual-effects.c#L1761-L1762

`CloneString` copies its source, so the string that `AcquireString` allocates is never freed. Passing `geometry` directly to `CloneString` would avoid the extra allocation. This line is still on `main` (a879b231b3, line 1761).

ImageMagick 6.9.13-54 has the same code in `magick/visual-effects.c` (line 1769) and leaks the same 4,101 bytes with `convert`.

We found this through the RMagick test suite. Calling `Image#polaroid` on an image with a caption 3000 times grew the RSS by about 85 MB.



### Steps to Reproduce

```sh
valgrind --leak-check=full --show-leak-kinds=definite \
  magick -size 20x20 xc:white -set caption hello -polaroid -5 out.png
```

valgrind reports:

```
4,101 bytes in 1 blocks are definitely lost in loss record 19 of 20
   at 0x488B8D8: malloc (in /usr/lib/valgrind/vgpreload_memcheck-amd64-linux.so)
   by 0x4B9AED3: AcquireString (in /usr/lib/libMagickCore-7.Q16HDRI.so.10.0.3)
   by 0x4BC66BC: PolaroidImage (in /usr/lib/libMagickCore-7.Q16HDRI.so.10.0.3)
   by 0x4E0424B: ??? (in /usr/lib/libMagickWand-7.Q16HDRI.so.10.0.3)
   by 0x4E133D3: CLIOption (in /usr/lib/libMagickWand-7.Q16HDRI.so.10.0.3)
   by 0x4DA2323: ProcessCommandOptions (in /usr/lib/libMagickWand-7.Q16HDRI.so.10.0.3)
   by 0x4DA2713: MagickImageCommand (in /usr/lib/libMagickWand-7.Q16HDRI.so.10.0.3)
   by 0x4D99CA9: MagickCommandGenesis (in /usr/lib/libMagickWand-7.Q16HDRI.so.10.0.3)
   by 0x40015B8: ??? (in /usr/bin/magick)
```

Without `-set caption hello`, or with `-gravity center`, valgrind reports no definite leak.


### Images

No image is needed. The command above uses the built-in `xc:white` image.

## Comment 5950940863

maintainer (MEMBER) · urban-warrior · 2026-10-02T11:02:48Z · https://github.com/ImageMagick/ImageMagick/issues/8994#issuecomment-5950940863

Thank you for reporting the issue. We have successfully reproduced it and are actively working on a patch to resolve the issue. You can expect this patch to be merged into the [main GIT branch](https://github.com/ImageMagick/ImageMagick), later today. Your patience and feedback are greatly appreciated.

## Comment 5951157061

reporter (NONE) · Watson1978 · 2026-10-02T11:16:47Z · https://github.com/ImageMagick/ImageMagick/issues/8994#issuecomment-5951157061

Thanks
