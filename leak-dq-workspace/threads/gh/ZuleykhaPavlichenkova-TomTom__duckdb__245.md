# [Tests different vector and block sizes] - ERROR: LeakSanitizer: detected memory leaks

- URL: https://github.com/ZuleykhaPavlichenkova-TomTom/duckdb/issues/245
- Repo: ZuleykhaPavlichenkova-TomTom/duckdb (language: C++)
- State: open; created 2025-08-19T09:49:22Z; status ok; passes main

## Issue body

reporter (OWNER) · ZuleykhaPavlichenkova-TomTom · 2025-08-19T09:49:22Z · https://github.com/ZuleykhaPavlichenkova-TomTom/duckdb/issues/245


**Workflow:** `NightlyTests` (17056222524)
- **Failed job:** [Tests different vector and block sizes](https://github.com/duckdb/duckdb/actions/runs/17056222524/job/48354961728)
- **Branch:** `v1.3-ossivalis` (3bcf01485639fc272d527456232e47f6694f589c)
- **Failure occurred running following command:**
    `./build/relassert/test/unittest`
<details> <summary>Job env:</summary>

```
    GH_TOKEN: ***
DUCKDB_WASM_VERSION: cf2048bd6d669ffa05c56d7d453e09e99de8b87e
CCACHE_SAVE: false
BASE_BRANCH: main
```
</details>

### **Failure details**:
```
ERROR: LeakSanitizer: detected memory leaks

Direct leak of 10485861 byte(s) in 1 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed626539f7 in init_text_pool(long, DBGenContext*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/text.cpp:413

Direct leak of 9648 byte(s) in 2 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fcb33 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:153

Direct leak of 9104 byte(s) in 22 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed6264aad6 in read_dist(char const*, char const*, distribution*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/bm_utils.cpp:287

Direct leak of 4000 byte(s) in 50 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed626061cf in init_params() /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/r_params.cpp:317
#2 0x7fed626061cf in init_params() /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/r_params.cpp:310

Direct leak of 2160 byte(s) in 6 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed6261e6ef in makePermutation(int*, int, int) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/permute.cpp:65

Indirect leak of 517588 byte(s) in 130 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fdb4b in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:354
#2 0x7fed625fdb4b in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 444984 byte(s) in 246 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fd31a in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:303
#2 0x7fed625fd31a in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 309784 byte(s) in 216 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fd7a6 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:326
#2 0x7fed625fd7a6 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 7280 byte(s) in 130 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fc951 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:276
#2 0x7fed625fc951 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 6317 byte(s) in 569 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed6264a7d3 in read_dist(char const*, char const*, distribution*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/bm_utils.cpp:292

Indirect leak of 1968 byte(s) in 130 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fd213 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:298
#2 0x7fed625fd213 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 1728 byte(s) in 130 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fd6ea in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:323
#2 0x7fed625fd6ea in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 984 byte(s) in 130 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fd253 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:299
#2 0x7fed625fd253 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 864 byte(s) in 130 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fc9b8 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:283
#2 0x7fed625fc9b8 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 724 byte(s) in 12 object(s) allocated from:
#0 0x7fed70efd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7fed625fd9fe in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:342
#2 0x7fed625fd9fe in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

SUMMARY: AddressSanitizer: 11802994 byte(s) leaked in 1904 allocation(s).
```

