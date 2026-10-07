# bin/opj_compress: munmap_chunk(): invalid pointer: 0x00007f3387f42010

- URL: https://github.com/kingofthebongo2008/openjpeg/issues/358
- Repo: kingofthebongo2008/openjpeg (language: C)
- State: open; created 2015-05-15T08:39:21Z; status ok; passes main

## Issue body

reporter (NONE) · GoogleCodeExporter · 2015-05-15T08:39:21Z · https://github.com/kingofthebongo2008/openjpeg/issues/358

```
$ truncate -s 3110400 /tmp/1920x540_i420.raw
$ bin/opj_compress -i /tmp/1920x540_i420.raw -o image.j2k -F 
1920,540,3,8,u@1x1:2x2:2x2

Warning. End of raw file not reached... processing anyway
[INFO] tile number 1 / 1
*** glibc detected *** bin/opj_compress: munmap_chunk(): invalid pointer: 
0x00007f3387f42010 ***

```

Original issue reported on code.google.com by `mathieu.malaterre` on 19 Jun 2014 at 8:46

