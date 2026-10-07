# [Tests different vector and block sizes] - ERROR: LeakSanitizer: detected memory leaks

- URL: https://github.com/ZuleykhaPavlichenkova-TomTom/duckdb/issues/252
- Repo: ZuleykhaPavlichenkova-TomTom/duckdb (language: C++)
- State: open; created 2025-08-20T08:32:01Z; status ok; passes main

## Issue body

reporter (OWNER) · ZuleykhaPavlichenkova-TomTom · 2025-08-20T08:32:01Z · https://github.com/ZuleykhaPavlichenkova-TomTom/duckdb/issues/252


**Workflow:** `NightlyTests` (17085251116)
- **Failed job:** [Tests different vector and block sizes](https://github.com/duckdb/duckdb/actions/runs/17085251116/job/48448630504)
- **Branch:** `v1.3-ossivalis` (0663a7142014ac4e21779575634bf35cbfd4cc1b)
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
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf95853a77 in init_text_pool(long, DBGenContext*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/text.cpp:413

Direct leak of 9648 byte(s) in 2 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fcbb3 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:153

Direct leak of 9104 byte(s) in 22 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf9584ab56 in read_dist(char const*, char const*, distribution*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/bm_utils.cpp:287

Direct leak of 4000 byte(s) in 50 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf9580624f in init_params() /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/r_params.cpp:317
#2 0x7faf9580624f in init_params() /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/r_params.cpp:310

Direct leak of 2160 byte(s) in 6 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf9581e76f in makePermutation(int*, int, int) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/permute.cpp:65

Indirect leak of 517588 byte(s) in 130 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fdbcb in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:354
#2 0x7faf957fdbcb in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 444984 byte(s) in 246 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fd39a in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:303
#2 0x7faf957fd39a in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 309784 byte(s) in 216 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fd826 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:326
#2 0x7faf957fd826 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 7280 byte(s) in 130 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fc9d1 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:276
#2 0x7faf957fc9d1 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 6317 byte(s) in 569 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf9584a853 in read_dist(char const*, char const*, distribution*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/bm_utils.cpp:292

Indirect leak of 1968 byte(s) in 130 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fd293 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:298
#2 0x7faf957fd293 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 1728 byte(s) in 130 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fd76a in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:323
#2 0x7faf957fd76a in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 984 byte(s) in 130 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fd2d3 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:299
#2 0x7faf957fd2d3 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 864 byte(s) in 130 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fca38 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:283
#2 0x7faf957fca38 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 724 byte(s) in 12 object(s) allocated from:
#0 0x7fafa40fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7faf957fda7e in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:342
#2 0x7faf957fda7e in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

SUMMARY: AddressSanitizer: 11802994 byte(s) leaked in 1904 allocation(s).
```



**Workflow:** `NightlyTests` (17085251118)
- **Failed job:** [Tests different vector and block sizes](https://github.com/duckdb/duckdb/actions/runs/17085251118/job/48448729218)
- **Branch:** `main` (a8206a211f01652e5109fc05b0a56b3b778dea1d)
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
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a18197 in init_text_pool(long, DBGenContext*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/text.cpp:413

Direct leak of 9648 byte(s) in 2 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a46fb3 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:153

Direct leak of 9104 byte(s) in 22 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a0f276 in read_dist(char const*, char const*, distribution*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/bm_utils.cpp:287

Direct leak of 4000 byte(s) in 50 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a5064f in init_params() /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/r_params.cpp:317
#2 0x7f6ef3a5064f in init_params() /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/r_params.cpp:310

Direct leak of 2160 byte(s) in 6 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a68b6f in makePermutation(int*, int, int) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/permute.cpp:65

Indirect leak of 517588 byte(s) in 130 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a47fcb in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:354
#2 0x7f6ef3a47fcb in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 444984 byte(s) in 246 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a4779a in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:303
#2 0x7f6ef3a4779a in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 309784 byte(s) in 216 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a47c26 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:326
#2 0x7f6ef3a47c26 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 7280 byte(s) in 130 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a46dd1 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:276
#2 0x7f6ef3a46dd1 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 6317 byte(s) in 569 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a0ef73 in read_dist(char const*, char const*, distribution*) /home/runner/work/duckdb/duckdb/extension/tpch/dbgen/bm_utils.cpp:292

Indirect leak of 1968 byte(s) in 130 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a47693 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:298
#2 0x7f6ef3a47693 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 1728 byte(s) in 130 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a47b6a in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:323
#2 0x7f6ef3a47b6a in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 984 byte(s) in 130 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a476d3 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:299
#2 0x7f6ef3a476d3 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 864 byte(s) in 130 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a46e38 in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:283
#2 0x7f6ef3a46e38 in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

Indirect leak of 724 byte(s) in 12 object(s) allocated from:
#0 0x7f6f030fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
#1 0x7f6ef3a47e7e in load_dist /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:342
#2 0x7f6ef3a47e7e in find_dist(char const*) /home/runner/work/duckdb/duckdb/extension/tpcds/dsdgen/dsdgen-c/dist.cpp:236

SUMMARY: AddressSanitizer: 11802994 byte(s) leaked in 1904 allocation(s).
```

