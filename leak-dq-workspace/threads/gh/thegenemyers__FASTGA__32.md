# FastGA crashes with munmap_chunk(): invalid pointer in FAtoGDB — fixed by reverting to commit 13c7c0f2

- URL: https://github.com/thegenemyers/FASTGA/issues/32
- Repo: thegenemyers/FASTGA (language: C)
- State: open; created 2026-09-02T22:05:45Z; status ok; passes main

## Issue body

reporter (NONE) · finn314 · 2026-09-02T22:05:45Z · https://github.com/thegenemyers/FASTGA/issues/32

Hello all, I'm running FastGA through Cactus v3.3.0 (aligning 21 non-eutherian genomes to human), and it crashes every single time it's called — every genome pair I've tried, regardless of genome size, always within a few seconds and ~100MB of memory, so it's clearly not something specific to one assembly. A typical command looks like:

FastGA -pafs -M -P./fgatmp -T8 stickleback_0.f.fa humpbackpufferfish_0.f.fa

and it dies with:

stderr=Segmentation fault (core dumped)

FastGA: Call to FAtoGDB failed

That's the FastGA build Cactus 3.3.0 currently pins (commit 42fd339a7e0600d45265ca5569a76c8dc265597c). I diffed it against the commit Cactus 3.2.1 used (13c7c0f201ba6eef5980c7a7264587f7a394f2b6, which never had this problem), and one change stood out: Uncompress_Read in gene_core.c picked up a new beg offset parameter, and handles it by pointing s0 before the start of the caller's buffer (s0 = s-beg) and writing through it. If the buffer wasn't allocated with headroom before s for that, this looks like a straightforward way to write a few bytes before the start of an allocation and corrupt the neighboring heap chunk — which would explain munmap_chunk complaining later on. There's related churn right nearby too (the moff array shrank from int64 to int, plus some new masking-accounting fields), all in the same soft-masking code path that -M turns on.

I confirmed the fix works end to end: built FastGA from 13c7c0f2 (FastGA, FAtoGDB, GIXmake, GIXrm, ALNtoPAF), swapped it in for the 3.3.0 build, and reran my full 21-genome pipeline from scratch. All 18 genome pairs that failed before — from ~12Gi jobs up to ~120Gi ones — now complete cleanly, no crash, nothing.

One catch for anyone else trying this: the older FastGA doesn't accept -M at all (FastGA: -M is an illegal option) — it soft-masks by default and you turn that off with -N instead. So the fix isn't just the binary swap, you also need to drop -M from wherever you're passing FastGA options (for Cactus users, that's the fastga_params config attribute).

Happy to attach the two smallest input files that reproduce this in a couple seconds, or do a diagnostic build (ASan, etc.) if that'd help pin down the exact write.

## Comment 5541114028

maintainer (COLLABORATOR) · c-zhou · 2026-09-04T13:27:33Z · https://github.com/thegenemyers/FASTGA/issues/32#issuecomment-5541114028

Hello @finn314 and @glennhickey,

We fixed a few bugs related to ANO files back in July, and I have now tagged a new release that includes these fixes: https://github.com/thegenemyers/FASTGA/releases/tag/v1.5.1

I am not sure whether they fully resolve the issues, but could you please give the new release a try and let me know if the problem persists?

Best,
Chenxi

 
