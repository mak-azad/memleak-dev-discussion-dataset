# There is a memory leak vulnerability

- URL: https://github.com/cloudwu/cstring/issues/6
- Repo: cloudwu/cstring (language: C)
- State: open; created 2018-05-14T06:58:46Z; status ok; passes main

## Issue body

reporter (NONE) · fCorleone · 2018-05-14T06:58:46Z · https://github.com/cloudwu/cstring/issues/6

=================================================================
==24927==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 1058 byte(s) in 1 object(s) allocated from:
    #0 0x4b9808  (/home/ubuntu/fuzz/cstring/app+0x4b9808)
    #1 0x4f13a0  (/home/ubuntu/fuzz/cstring/app+0x4f13a0)

SUMMARY: AddressSanitizer: 1058 byte(s) leaked in 1 allocation(s).
