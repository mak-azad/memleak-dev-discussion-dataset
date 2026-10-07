# file descriptor leak in WeDoLinux.c

- URL: https://github.com/scratchfoundation/Scratch_1.4/issues/6
- Repo: scratchfoundation/Scratch_1.4 (language: C)
- State: open; created 2016-12-11T18:29:54Z; status ok; passes offcwe

## Issue body

reporter (NONE) · michaelu123 · 2016-12-11T18:29:54Z · https://github.com/scratchfoundation/Scratch_1.4/issues/6

In scanForWeDo() the open succeeds, the ioctl fails, and as a result, squeak opens a new fd for /dev/usb/hiddev0 and hiddev1 every few seconds,

## Comment 266355416

other (NONE) · dmoco · 2016-12-12T06:50:03Z · https://github.com/scratchfoundation/Scratch_1.4/issues/6#issuecomment-266355416

Thanks Michael.
