# Integer overflow in pixel buffer allocation with large dimensions

- URL: https://github.com/vallentin/LoadBMP/issues/10
- Repo: vallentin/LoadBMP (language: C)
- State: open; created 2026-02-17T13:46:31Z; status ok; passes main

## Issue body

reporter (NONE) · ByamB4 · 2026-02-17T13:46:31Z · https://github.com/vallentin/LoadBMP/issues/10

Hey! I was fuzzing some image loaders and ran into a heap overflow in `loadbmp_decode_file()` caused by an integer overflow in the buffer allocation.

## The problem

In `loadbmp.h` around line 145, the pixel buffer is allocated like this:

```c
w = (bmp_info_header[4] + (bmp_info_header[5] << 8) + ...);
h = (bmp_info_header[8] + (bmp_info_header[9] << 8) + ...);

if ((w > 0) && (h > 0))
{
    data = (unsigned char*)malloc(w * h * components);
```

Since `w`, `h`, and `components` are all `unsigned int`, the multiplication can silently wrap around on 32-bit. A crafted BMP with large dimensions (say `w=65536, h=32768`) makes `w * h * 3` overflow to about 2.1 GB instead of the actual 6.4 GB needed. `malloc` allocates the smaller wrapped value, and then the pixel-reading loop at lines 153-182 writes way past the end of that buffer.

Even more extreme: `w=65536, h=65536` makes `w * h` wrap to exactly 0, so `malloc(0)` either returns NULL (caught by the check) or a tiny allocation (not caught), with the loop then writing into essentially nothing.

## Suggested fix

An overflow check before the allocation would catch this:

```c
if (w > 0 && h > 0) {
    if (w > SIZE_MAX / components / h) {
        fclose(f);
        return LOADBMP_OUT_OF_MEMORY;
    }
    data = (unsigned char*)malloc((size_t)w * h * components);
```

I also noticed that for 32-bit BMPs (bitsPerPixel == 32), the code only reads 3 bytes per pixel on line 159 instead of 4, which causes the rows to get misaligned. But that's a separate issue.

Found this while fuzzing with AddressSanitizer — happy to share a PoC BMP if needed.
