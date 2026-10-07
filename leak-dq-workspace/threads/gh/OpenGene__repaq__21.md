# munmap_chunk(): invalid pointer

- URL: https://github.com/OpenGene/repaq/issues/21
- Repo: OpenGene/repaq (language: C)
- State: open; created 2024-08-02T11:21:54Z; status ok; passes main

## Issue body

reporter (NONE) · krejciadam · 2024-08-02T11:21:54Z · https://github.com/OpenGene/repaq/issues/21

Hi!
  In very rare cases, I get this error: 
  
```
munmap_chunk(): invalid pointer
Aborted (core dumped)
```

Unfortunately, I can't share the fastq where this happens yet, because it is very large and I didn't manage to get a small portion that would demonstrate this behavior so far. 

This happens for both the 0.3.0 release and the current source code (which I guess is 0.4.0)

Any help appretiated. Thank you!

## Comment 4244947616

other (NONE) · rfm-targa · 2026-04-14T15:03:00Z · https://github.com/OpenGene/repaq/issues/21#issuecomment-4244947616

Hello,

I think I am running into a similar issue with a pair of FASTQ files I want to compress with `repaq`. Trying to compress both files into a single archive with `repaq -c -i 109_R1.fastq.gz -I 109_R2.fastq.gz -o 109.rfq.xz` outputs `Segmentation fault`. It still creates a file but `repaq --compare` returns the following:

```
{
	"result":"failed",
	"msg":"The RFQ file and FASTQ file have different sequence in the 606096 pair. ACCTATTGTTGTAACCAAAAGCTAAANATTAAAAAGCTGAAAACAAACGCCAAAAACCCCTTTAAAGCATCACATAAACCAACTAAGAAGCCTATTTTCAAACCAAAAACACGGATTGAGTTAGAGAGCAGATCGGAAGAGCACACGTCTG | ACCTATTGTTGTAACCAAAAGCTAAAGATTAAAAAGCTGAAAACAAACGCCAAAAACCCCTTTAAAGCATCACATAAACCAACTAAGAAGCCTATTTTCAAACCAAAAACACGGATTGAGTTAGAGAGCAGATCGGAAGAGCACACGTCTG",
	"fastq_reads":1212193,
	"rfq_reads":1212193,
	"fastq_bases":183041143,
	"rfq_bases":183041143
}
```

The sequences differ in a single position, with one sequence having a `G` and the other having an `N`. Here are the sequences with the different base highlighted with `*`:

```
ACCTATTGTTGTAACCAAAAGCTAAA*N*ATTAAAAAGCTGAAAACAAACGCCAAAAACCCCTTTAAAGCATCACATAAACCAACTAAGAAGCCTATTTTCAAACCAAAAACACGGATTGAGTTAGAGAGCAGATCGGAAGAGCACACGTCTG

ACCTATTGTTGTAACCAAAAGCTAAA*G*ATTAAAAAGCTGAAAACAAACGCCAAAAACCCCTTTAAAGCATCACATAAACCAACTAAGAAGCCTATTTTCAAACCAAAAACACGGATTGAGTTAGAGAGCAGATCGGAAGAGCACACGTCTG
```


If I try to compress the files separately it returns different errors for each file:

R1
```
repaq -c -i 109_R1.fastq.gz -o 109_R1.rfq.xz
Segmentation fault
```

R2
```
repaq -c -i 109_R2.fastq.gz -o 109_R2.rfq.xz
munmap_chunk(): invalid pointer
Aborted
```

Any idea about what may be the issue?
Thank you in advance.

Rafael
