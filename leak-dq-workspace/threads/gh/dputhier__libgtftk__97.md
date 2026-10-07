# pointer being freed was not allocated

- URL: https://github.com/dputhier/libgtftk/issues/97
- Repo: dputhier/libgtftk (language: C)
- State: open; created 2019-02-01T09:50:07Z; status ok; passes main

## Issue body

reporter (OWNER) · dputhier · 2019-02-01T09:50:07Z · https://github.com/dputhier/libgtftk/issues/97

Consider the following (in branch **blast_to_gtf of pygtftk**). This branch contains the latest ligtftk release (develop branch).

	from pygtftk.gtf_interface import GTF
	def native_str(x):
		return bytes(x.encode())
	blast = GTF._dll.load_blast(native_str('blastn.blast'))
        blast.size
       [1]    22657 segmentation fault  ipython


NB: in this branch, **blastn.blast** can be found in **pygtftk/data/mini_real_10M/ (as a gzip file)**. This file was obtained by blasting the computed sequence of transcripts (**mini_real_10M_tx_seq.fa**) against the genome region (**chr1_hg38_10M.fa**).

Cheers

## Comment 459666908

reporter (OWNER) · dputhier · 2019-02-01T09:51:23Z · https://github.com/dputhier/libgtftk/issues/97#issuecomment-459666908

I guess this could be a OSX one...
