# Validate index_block_size to Prevent Attacker-Controlled Memory Exhaustion

- URL: https://github.com/tuxera/ntfs-3g/issues/215
- Repo: tuxera/ntfs-3g (language: C)
- State: open; created 2026-09-02T06:23:52Z; status ok; passes main

## Issue body

reporter (NONE) · fredrikliliengren · 2026-09-02T06:23:52Z · https://github.com/tuxera/ntfs-3g/issues/215

ntfs-3g 2022.10.3
in patch: https://github.com/tuxera/ntfs-3g/commit/dc1b682e99b6c055b0281ca543a8420b698420d1
For: CVE-42616
ntfsprogs/ntfscat.c:359

block_size comes directly from the on-disk INDEX_ROOT.index_block_size, but this path does not validate or cap it before using it as an allocation size. A crafted index root can therefore request a multi-gigabyte allocation (for example, 0x80000000), replacing the fixed-buffer overflow with an attacker-triggered memory-exhaustion failure. Reject implausible index-record sizes before assigning bufsize.

## Comment 5506513645

maintainer (MEMBER) · unsound · 2026-09-02T08:08:48Z · https://github.com/tuxera/ntfs-3g/issues/215#issuecomment-5506513645

Thanks for the report, it looks like you're right but the impact is limited given that the maximum number of bytes that could be allocated is 2 GiB (anything above that would not be a power of 2 as a 32-bit number) and considering that `malloc` reserves but typically doesn't actually allocate memory pages until the memory is accessed the impact is non-existent on most modern operating systems.

It may be reasonable though to limit the index block size globally to the index block size specified in the boot sector (`clusters_per_index_record`).
@rakeshpandit @jpandre do you have any thoughts? Shouldn't the index block size for all of a volume's indices match the global index block size? I haven't checked known volumes to validate that the index block size is always the same for consistent volumes.
