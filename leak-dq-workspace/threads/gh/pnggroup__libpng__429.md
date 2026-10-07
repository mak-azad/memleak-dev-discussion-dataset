# Exceptions when linking release libpng (1.6.38) against debug application build in MSVC 2019

- URL: https://github.com/pnggroup/libpng/issues/429
- Repo: pnggroup/libpng (language: C)
- State: open; created 2022-08-26T11:40:39Z; status ok; passes main

## Issue body

reporter (NONE) · mystery-keeper · 2022-08-26T11:40:39Z · https://github.com/pnggroup/libpng/issues/429

When I link the release version of libpng to debug build of my application and try to write a file - I get runtime heap-related asserts and exceptions.

It only happens after the png_write_info() call. If if comment it - I get a malformed file, but no runtime errors.
When I fclose() - I get "Debug assertion failed: _CrtIsValidHeapPointer(block)"
And if I comment fclose() - I get an exception when application calls fcloseall() on completion.

Linking debug against debug or release against release works fine.

## Comment 1233440666

other (NONE) · SamB · 2022-08-31T21:29:52Z · https://github.com/pnggroup/libpng/issues/429#issuecomment-1233440666

I think you should read [Allocating and freeing memory across module boundaries](https://devblogs.microsoft.com/oldnewthing/20060915-04/?p=29723), and note that even if both modules are using the same CRT DLL, [debug builds will end up calling different heap functions](https://docs.microsoft.com/en-us/visualstudio/debugger/debug-versions-of-heap-allocation-functions?view=vs-2022).

<https://docs.microsoft.com/en-us/cpp/c-runtime-library/potential-errors-passing-crt-objects-across-dll-boundaries> may also be relevant, especially since you also mention `fclose()`.

<s>However, I'm a bit puzzled as the libz/libpng APIs were designed with this kind of issue in mind</s> ... oh wait, are you using the `png_image_write_to_stdio()` function? That'll totally cause such issues.

P.S. Looking at the README in <https://github.com/glennrp/libpng/tree/libpng16/projects/vstudio>, it seems that debug builds aren't particularly well-supported.

TL;DR: don't try to mix-and-match Release and Debug builds unless you know what you're doing.

## Comment 1233448503

reporter (NONE) · mystery-keeper · 2022-08-31T21:41:15Z · https://github.com/pnggroup/libpng/issues/429#issuecomment-1233448503

> oh wait, are you using the `png_image_write_to_stdio()` function? That'll totally cause such issues.

Not explicitly. But I do use `png_init_io(pPngStruct, a_pFile);`
So, it's using FILE * across runtimes that's causing the problem?

## Comment 1329153824

other (CONTRIBUTOR) · jbowler · 2022-11-28T13:58:40Z · https://github.com/pnggroup/libpng/issues/429#issuecomment-1329153824

> Not explicitly. But I do use `png_init_io(pPngStruct, a_pFile);`
> So, it's using FILE * across runtimes that's causing the problem?

IRC that's a crasher; msvcrt.dll and msvcrtd.dll (or whatever they are called) have very different FILE structures.  You need to implement your own memory and IO callbacks so that the same runtime DLL is used to create, destroy and, in the case of files reads/write the memory and file.

You also need to implement your own longjmp callback, or an error handler to avoid longjmp.

Or you could just build everything for release; that's what I always did, I don't see the point of special debug builds.

## Comment 2381008566

other (CONTRIBUTOR) · jbowler · 2024-09-28T22:13:31Z · https://github.com/pnggroup/libpng/issues/429#issuecomment-2381008566

@ctruta: one of the [libpng18] FILE* issues (i.e. one of several issues that report the same problem.)

Fix is easy with an ABI change, as discussed in another issue... somewhere.
