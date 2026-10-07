# ==16971==ERROR: LeakSanitizer: detected memory leaks

- URL: https://github.com/owenthewizard/i3lock-next/issues/19
- Repo: owenthewizard/i3lock-next (language: C)
- State: open; created 2018-02-06T02:30:06Z; status ok; passes main

## Issue body

reporter (NONE) · ibrokemypie · 2018-02-06T02:30:06Z · https://github.com/owenthewizard/i3lock-next/issues/19

When running as a post-suspend systemd service I get this in my journalctl every time it wakes from sleep.

```
Feb 06 13:28:44 badhp i3lock-next[16881]: =================================================================
Feb 06 13:28:44 badhp i3lock-next[16881]: ==16971==ERROR: LeakSanitizer: detected memory leaks
Feb 06 13:28:44 badhp i3lock-next[16881]: =================================================================
Feb 06 13:28:44 badhp i3lock-next[16881]: Direct leak of 512 byte(s) in 2 object(s) allocated from:
Feb 06 13:28:44 badhp i3lock-next[16881]: ==16966==ERROR: LeakSanitizer: detected memory leaks
Feb 06 13:28:44 badhp i3lock-next[16881]: Direct leak of 768 byte(s) in 3 object(s) allocated from:
Feb 06 13:28:44 badhp i3lock-next[16881]:     #0 0x563d7797c9a1 in malloc (/usr/bin/i3lock+0xe99a1)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #1 0x7f1a4b5b87ee  (/usr/lib/libfontconfig.so.1+0x1d7ee)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #0 0x563d7797c9a1 in malloc (/usr/bin/i3lock+0xe99a1)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #1 0x7f1a4b5b87ee  (/usr/lib/libfontconfig.so.1+0x1d7ee)
Feb 06 13:28:44 badhp i3lock-next[16881]: Indirect leak of 128 byte(s) in 4 object(s) allocated from:
Feb 06 13:28:44 badhp i3lock-next[16881]:     #0 0x563d7797cbe1 in calloc (/usr/bin/i3lock+0xe9be1)
Feb 06 13:28:44 badhp i3lock-next[16881]: Indirect leak of 224 byte(s) in 7 object(s) allocated from:
Feb 06 13:28:44 badhp i3lock-next[16881]:     #1 0x7f1a4b5b8ed9  (/usr/lib/libfontconfig.so.1+0x1ded9)
Feb 06 13:28:44 badhp i3lock-next[16881]: Indirect leak of 14 byte(s) in 2 object(s) allocated from:
Feb 06 13:28:44 badhp i3lock-next[16881]:     #0 0x563d7797cbe1 in calloc (/usr/bin/i3lock+0xe9be1)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #0 0x563d778d8de1 in __interceptor_strdup (/usr/bin/i3lock+0x45de1)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #1 0x7f1a4b5b8ed9  (/usr/lib/libfontconfig.so.1+0x1ded9)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #1 0x7f1a4b5b81f5 in FcValueSave (/usr/lib/libfontconfig.so.1+0x1d1f5)
Feb 06 13:28:44 badhp i3lock-next[16881]: SUMMARY: AddressSanitizer: 654 byte(s) leaked in 8 allocation(s).
Feb 06 13:28:44 badhp i3lock-next[16881]: Indirect leak of 25 byte(s) in 3 object(s) allocated from:
Feb 06 13:28:44 badhp i3lock-next[16881]:     #0 0x563d778d8de1 in __interceptor_strdup (/usr/bin/i3lock+0x45de1)
Feb 06 13:28:44 badhp i3lock-next[16881]:     #1 0x7f1a4b5b81f5 in FcValueSave (/usr/lib/libfontconfig.so.1+0x1d1
```
