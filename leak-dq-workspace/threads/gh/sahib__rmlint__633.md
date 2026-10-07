# error for object 0x...: pointer being freed was not allocated

- URL: https://github.com/sahib/rmlint/issues/633
- Repo: sahib/rmlint (language: C)
- State: open; created 2023-09-30T20:33:11Z; status ok; passes main

## Issue body

reporter (NONE) · dzg · 2023-09-30T20:33:11Z · https://github.com/sahib/rmlint/issues/633

Mac Silicon 
```
rmlint --version
version 2.10.2 compiled: Aug  9 2023 at [08:49:19] "Ludicrous Lemur" (rev unknown)
compiled with: -mounts -nonstripped -fiemap +sha512 +bigfiles +intl +replay -xattr -btrfs-support
```

```
$ rmlint -bgrD --xattr old dupes
Traversing (844848 usable files / 0 + 0 ignored files / folders)
Preprocessing (reduces files to 387549 / found 19211 other lint)
Matching (271075 dupes of 79207 originals; 0 B to scan in 0 files, ETA:  2s)
Merging files into directories (stand by...)

==> In total 844848 files, whereof 271075 are duplicates in 79207 groups.
==> This equals 5.48 GB of duplicates which could be removed.
==> 19211 other suspicious item(s) found, which may vary in size.
==> Scanning took in total  2m 17.947s.

Wrote a sh file to: /Volumes/2TB/rmlint.sh
Wrote a json file to: /Volumes/2TB/rmlint.json
rmlint(47032,0x1f0322080) malloc: *** error for object 0x6000dba34b60: pointer being freed was not allocated
rmlint(47032,0x1f0322080) malloc: *** set a breakpoint in malloc_error_break to debug
Aborting due to a fatal error. (signal received: Abort trap: 6)
Please file a bug report (See rmlint -h)
zsh: abort      rmlint -bgrD --xattr old dupes
```

## Comment 1741869985

other (CONTRIBUTOR) · cebtenzzre · 2023-09-30T22:09:42Z · https://github.com/sahib/rmlint/issues/633#issuecomment-1741869985

Please build rmlint with `CFLAGS='-fsanitize=address' LDFLAGS=$CFLAGS scons GDB=1`, make it crash again, and paste the full ASAN report. I believe this is another case where the same file object is sent to the formatter twice, which causes it to be freed twice. Probably similar to #626

## Comment 5616550597

maintainer (COLLABORATOR) · vassilit · 2026-09-10T09:44:46Z · https://github.com/sahib/rmlint/issues/633#issuecomment-5616550597

`scons SANITISE=address`
