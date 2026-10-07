# free(): invalid pointer

- URL: https://github.com/intel/lmbench/issues/30
- Repo: intel/lmbench (language: C)
- State: open; created 2024-12-04T08:24:29Z; status ok; passes main

## Issue body

reporter (NONE) · gongchangsui · 2024-12-04T08:24:29Z · https://github.com/intel/lmbench/issues/30

vm OS:  ubuntu 24.04
run：
```./bw_mem -P `nproc --all`  -W 5 -N 5 1024M rdwr```
output： `free(): invalid pointer`
