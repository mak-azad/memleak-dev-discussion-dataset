# Sony a6400 Interval capture Image crash with pointer being freed was not allocated

- URL: https://github.com/gphoto/libgphoto2/issues/865
- Repo: gphoto/libgphoto2 (language: C)
- State: open; created 2022-11-10T03:01:17Z; status ok; passes main

## Issue body

reporter (NONE) · Yogayu · 2022-11-10T03:01:17Z · https://github.com/gphoto/libgphoto2/issues/865

**Describe the bug**
Hi， when using gphoto2 command line to capture multiple photos, I came to a crash:

```
gphoto2 --capture-image-and-download -F 5 -I 3 --force-overwrite

Time-lapse mode enabled (interval: 3s).
Capturing frame #1/5...
New file is in location /capt0000.jpg on the camera
Saving file as capt0000.jpg
Deleting file /capt0000.jpg on the camera
Waiting for next capture slot 2 seconds...
gphoto2(26024,0x111bf3600) malloc: *** error for object 0x7ff7b7984840: pointer being freed was not allocated
gphoto2(26024,0x111bf3600) malloc: *** set a breakpoint in malloc_error_break to debug
[1]    26024 abort      gphoto2 --capture-image-and-download -F 5 -I 3 --force-overwrite

```

**Name the camera**

gphoto2 --auto-detect or USB IDs
Model                          Port
Sony ILCE-6400 (PC Control)    usb:020,005
Apple iPhone 5 (PTP mode)      usb:020,002
*** Error (-1: 'Unspecified error') ***


**libgphoto2 and gphoto2 version**

gphoto2 2.5.27

**To Reproduce**

gphoto2 --capture-image-and-download -F 5 -I 3 --force-overwrite

Here is the log:
[my-logfile.txt](https://github.com/gphoto/libgphoto2/files/9976934/my-logfile.txt)

