# bin/opj_compress: munmap_chunk(): invalid pointer: 0x00007f3387f42010

- URL: https://github.com/dprahut/openjpeg/issues/358
- Repo: dprahut/openjpeg (language: C)
- State: open; created 2016-03-11T18:16:59Z; status ok; passes main

## Issue body

reporter (NONE) · GoogleCodeExporter · 2016-03-11T18:16:59Z · https://github.com/dprahut/openjpeg/issues/358

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


## Comment 195485735

reporter (NONE) · GoogleCodeExporter · 2016-03-11T18:17:00Z · https://github.com/dprahut/openjpeg/issues/358#issuecomment-195485735

```
I have found the the solution to the problem, but the result is also wrong.
https://code.google.com/p/openjpeg/issues/detail?id=357
```

Original comment by `dhz6...@gmail.com` on 20 Jun 2014 at 4:48

Attachments:
- [opj_compress.png](https://storage.googleapis.com/google-code-attachments/openjpeg/issue-358/comment-1/opj_compress.png)

