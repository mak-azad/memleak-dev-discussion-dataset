# xdo_new to xdo_free leaks

- URL: https://github.com/jordansissel/xdotool/issues/189
- Repo: jordansissel/xdotool (language: C)
- State: open; created 2017-10-01T04:11:22Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · luxe · 2017-10-01T04:11:22Z · https://github.com/jordansissel/xdotool/issues/189

```
extern "C" {
#include <xdo.h>
}

int main(){
    xdo_t *xdo = xdo_new(NULL);
    xdo_free(xdo);
}
```

```
==14950==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 72 byte(s) in 1 object(s) allocated from:
    #0 0x7fb13b18d130 in calloc (/usr/lib/x86_64-linux-gnu/libasan.so.3+0xc7130)
    #1 0x7fb1381338a0 in XkbGetMap (/usr/lib/x86_64-linux-gnu/libX11.so.6+0x8d8a0)

SUMMARY: AddressSanitizer: 72 byte(s) leaked in 1 allocation(s).
```

Seriously?

## Comment 333353499

reporter (CONTRIBUTOR) · luxe · 2017-10-01T04:51:56Z · https://github.com/jordansissel/xdotool/issues/189#issuecomment-333353499

https://github.com/jordansissel/xdotool/pull/190
fixes my leak.  I dunno if its a valid or not.  
stolen from:  
https://github.com/kupferlauncher/keybinder/pull/10/commits/d9f0a1ff32050683300e2b981aeaab18d5d34041

## Comment 473555961

other (CONTRIBUTOR) · frobware · 2019-03-16T16:04:31Z · https://github.com/jordansissel/xdotool/issues/189#issuecomment-473555961

Fixed by PR #242 

## Comment 1732366236

other (NONE) · lucasturci · 2023-09-23T17:06:27Z · https://github.com/jordansissel/xdotool/issues/189#issuecomment-1732366236

Was the fix abandoned?

## Comment 1732563229

other (CONTRIBUTOR) · frobware · 2023-09-24T12:47:46Z · https://github.com/jordansissel/xdotool/issues/189#issuecomment-1732563229

> Was the fix abandoned?

I closed my PR due to lack of interest: https://github.com/jordansissel/xdotool/pull/242#issuecomment-631511187

