# unix: Memory leak

- URL: https://github.com/libui-ng/libui-ng/issues/156
- Repo: libui-ng/libui-ng (language: C)
- State: open; created 2022-12-04T14:35:54Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · szanni · 2022-12-04T14:35:54Z · https://github.com/libui-ng/libui-ng/issues/156

The library seems to leak memory on unix, as soon as you add a `uiControl`. You can test this by either running one of the examples through `valgrind` or configure with asan `CFLAGS="-fsanitize=address -fno-omit-frame-pointer" meson setup --buildtype=debug build`.

Running the `hello-world` example compiled with asan will result in:
```sh
=================================================================
==3031672==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 2560 byte(s) in 4 object(s) allocated from:
    #0 0x7f2fb3b1f7ea in __interceptor_realloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7f2fb25c4fdb  (/usr/lib/libfontconfig.so.1+0x20fdb)

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x7f2fb3b20a89 in __interceptor_malloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7f2fb25c4f25  (/usr/lib/libfontconfig.so.1+0x20f25)

Indirect leak of 7104 byte(s) in 222 object(s) allocated from:
    #0 0x7f2fb3b20a89 in __interceptor_malloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7f2fb25b0a60  (/usr/lib/libfontconfig.so.1+0xca60)

Indirect leak of 2752 byte(s) in 214 object(s) allocated from:
    #0 0x7f2fb3ad3faa in __interceptor_strdup /usr/src/debug/gcc/libsanitizer/asan/asan_interceptors.cpp:439
    #1 0x7f2fb25b01c3  (/usr/lib/libfontconfig.so.1+0xc1c3)

Indirect leak of 2368 byte(s) in 74 object(s) allocated from:
    #0 0x7f2fb3b20411 in __interceptor_calloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7f2fb25c911d  (/usr/lib/libfontconfig.so.1+0x2511d)

Indirect leak of 1664 byte(s) in 52 object(s) allocated from:
    #0 0x7f2fb3b20411 in __interceptor_calloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7f2fb25c49dc  (/usr/lib/libfontconfig.so.1+0x209dc)

Indirect leak of 453 byte(s) in 46 object(s) allocated from:
    #0 0x7f2fb3ad3faa in __interceptor_strdup /usr/src/debug/gcc/libsanitizer/asan/asan_interceptors.cpp:439
    #1 0x7f2fb25c47d8 in FcValueSave (/usr/lib/libfontconfig.so.1+0x207d8)

Indirect leak of 384 byte(s) in 12 object(s) allocated from:
    #0 0x7f2fb3b20411 in __interceptor_calloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7f2fb25c4890  (/usr/lib/libfontconfig.so.1+0x20890)

Indirect leak of 96 byte(s) in 2 object(s) allocated from:
    #0 0x7f2fb3b20a89 in __interceptor_malloc /usr/src/debug/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7f2fb25bac08 in FcLangSetCopy (/usr/lib/libfontconfig.so.1+0x16c08)

SUMMARY: AddressSanitizer: 17637 byte(s) leaked in 627 allocation(s).
```

Interestingly enough this does _not_ happen for the `window` example.

My first though was this was an upstream DONT CARE/WONT FIX issue, as this used to be very common from the glib/gtk folks, but this seems to be unlikely!?

The (essentially) equivalent program here for example does not leak any memory, leading me to believe this is actually a libui-ng bug.

```c
/**
 * CFLAGS="-Wall -Wextra -pedantic -std=c99 -fsanitize=address -fno-omit-frame-pointer" gcc `pkg-config --cflags --libs gtk+-3.0 ` label.c -o label
 */
#include <gtk/gtk.h>

int
main (int argc, char **argv)
{
	gtk_init(&argc, &argv);

	GtkWidget *w = gtk_window_new(GTK_WINDOW_TOPLEVEL);
	g_signal_connect(G_OBJECT(w), "destroy", gtk_main_quit, NULL);

	GtkWidget *b = gtk_label_new("Text");
	gtk_container_add(GTK_CONTAINER(w), b);

	gtk_widget_show_all(w);
	gtk_main();

	return 0;
}
```

This is highly annoying when building programs that link against libui-ng as it makes it hard to figure out if the program in question leaks memory or not.
