# munmap_chunk(): invalid pointer in any fastq file

- URL: https://github.com/Megagenomics/FastProNGS/issues/2
- Repo: Megagenomics/FastProNGS (language: C)
- State: open; created 2021-01-05T21:45:53Z; status ok; passes main

## Issue body

reporter (NONE) · guilhermesena1 · 2021-01-05T21:45:53Z · https://github.com/Megagenomics/FastProNGS/issues/2

Hello,

I tried running the program on several different fastq files but keep getting the following error:

```
munmap_chunk(): invalid pointer
```

I tried both on Ubuntu 20.04 with gcc 10.2.0 and on CentOS 7 with the same gcc. I compiled according to the README instructions and ran the following:

```
./bin/FastProNGS -x conf/default.xml a.fq
```

One of the examples, containing 100 reads, for which I got this error, is available [here](https://pastebin.com/raw/gQVTGthG). Is this a known issue? Any idea what might be happening?

Thank you so much in advance!
