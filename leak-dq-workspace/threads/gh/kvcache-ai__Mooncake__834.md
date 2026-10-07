# [Bug]: mooncake_master potential memory leaking

- URL: https://github.com/kvcache-ai/Mooncake/issues/834
- Repo: kvcache-ai/Mooncake (language: C++)
- State: closed; created 2025-09-12T08:05:23Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · nickyc975 · 2025-09-12T08:05:23Z · https://github.com/kvcache-ai/Mooncake/issues/834

### Bug Report

We observed that mooncake_master's memory usage keeps growing up when running stress_cluster_benchmark.py in prefill mode multiple times. Here is a simple script to demonstrate our operations:

```bash
#!/bin/bash

# Start mooncake_master in advance and use its pid as the first argument.
master_pid=$1
# Specify the file path to store the result.
output_file=$2

top -b -p $master_pid -n 1 | grep $master_pid >> $output_file
for ((i=0; i<10; i++)); do
    python3 mooncake-store/tests/stress_cluster_benchmark.py \
        --role=prefill --protocol=rdma \
        --device-name=mlx5_bond_0 --local-hostname=127.0.0.1:8081 \
        --local-buffer-size=1024 --global-segment-size=32768 \
        --max-requests=33554432 --value-length=1024 --batch-size=4096 \
        --wait-time=0
    # Sleep for a while to let master calm down.
    sleep 30
    top -b -p $master_pid -n 1 | grep $master_pid >> $output_file
done
```

Running the test against the latest version of Mooncake produced the following result:

```
1311706 root      20   0  526228  37480  10832 S   0.0   0.0   0:00.03 moonca+
1311706 root      20   0   11.2g  10.5g  10960 S   0.0   4.2   2:39.36 moonca+
1311706 root      20   0   20.0g  19.2g  10960 S   0.0   7.6   5:03.04 moonca+
1311706 root      20   0   29.2g  28.3g  10960 S   0.0  11.3   7:22.89 moonca+
1311706 root      20   0   39.2g  38.3g  10960 S   0.0  15.2   9:43.54 moonca+
1311706 root      20   0   39.1g  38.2g  10960 S   0.0  15.2  11:59.55 moonca+
1311706 root      20   0   40.0g  39.0g  10960 S   0.0  15.5  14:18.33 moonca+
1311706 root      20   0   40.9g  39.9g  10960 S   0.0  15.9  16:27.42 moonca+
1311706 root      20   0   40.9g  39.9g  10960 S   0.0  15.9  18:41.46 moonca+
1311706 root      20   0   40.9g  39.9g  10960 S   0.0  15.9  20:52.79 moonca+
1311706 root      20   0   40.9g  39.9g  10960 S   0.0  15.9  23:12.31 moonca+

```

As we can see, mooncake_master's memory usage keeps growing dramatically in the first 4 tests, and finally reaches as high as 39.9g. The problem is that, the memory usage may increase after the first test, but should not increase to that much in following tests.

### Before submitting...

- [x] Ensure you searched for relevant issues and read the [documentation]

## Comment 3284763520

maintainer (COLLABORATOR) · ykwd · 2025-09-12T10:40:45Z · https://github.com/kvcache-ai/Mooncake/issues/834#issuecomment-3284763520

Thanks for reporting this. We will try to find out what happened.

## Comment 3290618367

maintainer (COLLABORATOR) · xiaguan · 2025-09-15T06:07:54Z · https://github.com/kvcache-ai/Mooncake/issues/834#issuecomment-3290618367

Thanks for reporting this.

Quick summary: This is not a memory leak, but expected behavior.

The stress test generates too many small keys, which are frequently inserted into the `std::unordered_map`. Even though we call `erase()` later, the `unordered_map` doesn't immediately shrink or release memory.

As a workaround, try increasing the value size during testing. We might also look into more efficient index structures in the future.

## Comment 3290633570

maintainer (COLLABORATOR) · xiaguan · 2025-09-15T06:15:37Z · https://github.com/kvcache-ai/Mooncake/issues/834#issuecomment-3290633570

reproduce

```cpp
#include <bits/stdc++.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <unistd.h>
#include <dlfcn.h>

// ==== Container switch ======================================================
// Default: std::unordered_map. Build with -DUSE_ABSL to use absl::flat_hash_map.
#ifdef USE_ABSL
  #include "absl/container/flat_hash_map.h"
  template <typename K, typename V>
  using HashMap = absl::flat_hash_map<K, V>;
#else
  template <typename K, typename V>
  using HashMap = std::unordered_map<K, V>;
#endif

using namespace std;

// ---- helpers to read memory stats from /proc ----
struct MemStat {
    long rss_kb = -1;             // Resident Set Size
    long pss_kb = -1;             // Proportional Set Size (kernel estimate)
    long priv_dirty_kb = -1;      // Private_Dirty
    long shared_clean_kb = -1;    // Shared_Clean
};

static MemStat read_smaps_rollup() {
    MemStat ms;
    FILE* f = fopen("/proc/self/smaps_rollup", "r");
    if (!f) return ms;
    char line[512];
    while (fgets(line, sizeof(line), f)) {
        if (sscanf(line, "Rss: %ld kB", &ms.rss_kb) == 1) continue;
        if (sscanf(line, "Pss: %ld kB", &ms.pss_kb) == 1) continue;
        if (sscanf(line, "Private_Dirty: %ld kB", &ms.priv_dirty_kb) == 1) continue;
        if (sscanf(line, "Shared_Clean: %ld kB", &ms.shared_clean_kb) == 1) continue;
    }
    fclose(f);
    return ms;
}

static string human_mb(long kb) {
    if (kb < 0) return "?";
    char buf[64];
    snprintf(buf, sizeof(buf), "%.2f MB", kb / 1024.0);
    return string(buf);
}

static void print_mem(const string& tag) {
    MemStat ms = read_smaps_rollup();
    cerr << fixed << setprecision(2);
    cerr << "[MEM] " << tag
         << " | Rss=" << human_mb(ms.rss_kb)
         << " Pss=" << human_mb(ms.pss_kb)
         << " PrivDirty=" << human_mb(ms.priv_dirty_kb)
         << " SharedClean=" << human_mb(ms.shared_clean_kb)
         << "\n";
}

// ---- optional jemalloc purge (runtime, no hard link dependency) ----
using mallctl_fn = int (*)(const char*, void*, size_t*, void*, size_t);

static void jemalloc_epoch() {
    void* sym = dlsym(RTLD_DEFAULT, "mallctl");
    if (!sym) return; // not jemalloc
    mallctl_fn mallctl_p = reinterpret_cast<mallctl_fn>(sym);
    size_t epoch = 1; size_t sz = sizeof(epoch);
    (void)mallctl_p("epoch", &epoch, &sz, nullptr, 0);
}

static void jemalloc_purge_all() {
    void* sym = dlsym(RTLD_DEFAULT, "mallctl");
    if (!sym) return; // not jemalloc
    mallctl_fn mallctl_p = reinterpret_cast<mallctl_fn>(sym);
    jemalloc_epoch();
    (void)mallctl_p("arenas.purge", nullptr, nullptr, nullptr, 0);
    jemalloc_epoch();
}

#ifdef __GLIBC__
  #include <malloc.h>
  static void glibc_tune_and_trim_once() {
      mallopt(M_TRIM_THRESHOLD, 128 * 1024);
      mallopt(M_MMAP_THRESHOLD, 64 * 1024);
      malloc_trim(0);
  }
#else
  static void glibc_tune_and_trim_once() {}
#endif

// ---- workload ----
int main(int argc, char** argv) {
    ios::sync_with_stdio(false);

    // Parameters
    size_t N = 10'000'000;       // default: 1e7
    bool do_reserve = true;
    size_t reserve_buckets = 0;  // 0 -> let implementation decide

    // parse args: --n=, --no-reserve, --reserve=, --sleep_ms=, --rounds=
    int sleep_ms = 500;  // small pause between phases
    int rounds = 1;      // repeat whole experiment
    for (int i = 1; i < argc; ++i) {
        string a = argv[i];
        if (a.rfind("--n=",0)==0) N = stoull(a.substr(4));
        else if (a == "--no-reserve") do_reserve = false;
        else if (a.rfind("--reserve=",0)==0) { reserve_buckets = stoull(a.substr(10)); do_reserve=true; }
        else if (a.rfind("--sleep_ms=",0)==0) sleep_ms = stoi(a.substr(11));
        else if (a.rfind("--rounds=",0)==0) rounds = stoi(a.substr(9));
    }

    cerr << "Config: N=" << N
         << " do_reserve=" << (do_reserve?"true":"false")
         << " reserve_buckets=" << reserve_buckets
         << " rounds=" << rounds
#ifdef USE_ABSL
         << " container=absl::flat_hash_map"
#else
         << " container=std::unordered_map"
#endif
         << "\n";

    if (N >= 100'000'000ULL) {
        cerr << "[WARN] N is very large for hash maps. Ensure you have enough RAM.\n";
    }

    for (int r = 0; r < rounds; ++r) {
        cerr << "\n=== Round " << r << " ===\n";
        print_mem("start");

        HashMap<uint64_t, uint64_t> m;
        if (do_reserve) {
#ifdef USE_ABSL
            // absl::flat_hash_map::rehash expects #buckets; reserve() expects elements.
            if (reserve_buckets) m.rehash(reserve_buckets);
            else m.reserve(N);
#else
            if (reserve_buckets) m.rehash(reserve_buckets);
            else m.reserve(N);
#endif
        }

        // INSERT
        {
            auto t0 = chrono::steady_clock::now();
            for (uint64_t i = 0; i < N; ++i) {
                m.emplace(i, i);
            }
            auto t1 = chrono::steady_clock::now();
            print_mem("after insert");
            cerr << "insert time: "
                 << chrono::duration_cast<chrono::milliseconds>(t1-t0).count()
                 << " ms\n";
        }

        this_thread::sleep_for(chrono::milliseconds(sleep_ms));
        print_mem("steady after insert");

        // ERASE ALL (erase/clear will not necessarily shrink capacity)
        {
            auto t0 = chrono::steady_clock::now();
            m.clear();
            auto t1 = chrono::steady_clock::now();
            print_mem("after clear (no shrink)");
            cerr << "clear time: "
                 << chrono::duration_cast<chrono::milliseconds>(t1-t0).count()
                 << " ms\n";
        }

        this_thread::sleep_for(chrono::milliseconds(sleep_ms));
        print_mem("steady after clear (still high due to capacity/retained)");

        // SHRINK buckets: rehash(0) where supported
        {
            auto t0 = chrono::steady_clock::now();
            m.rehash(0);
            auto t1 = chrono::steady_clock::now();
            print_mem("after rehash(0) (buckets shrunk)");
            cerr << "rehash(0) time: "
                 << chrono::duration_cast<chrono::milliseconds>(t1-t0).count()
                 << " ms\n";
        }

        this_thread::sleep_for(chrono::milliseconds(sleep_ms));
        print_mem("steady after rehash(0)");

        // SWAP trick
        {
            auto t0 = chrono::steady_clock::now();
            HashMap<uint64_t, uint64_t> tmp;
            tmp.swap(m);
            auto t1 = chrono::steady_clock::now();
            print_mem("after swap-to-empty (capacity released to allocator)");
            cerr << "swap-to-empty time: "
                 << chrono::duration_cast<chrono::milliseconds>(t1-t0).count()
                 << " ms\n";
        }

        // jemalloc purge (if present) and/or glibc trim
        jemalloc_purge_all();
        glibc_tune_and_trim_once();
        this_thread::sleep_for(chrono::milliseconds(sleep_ms));
        print_mem("after purge/trim");
    }

    cerr << "\nDone.\n";
    return 0;
}
```

result
```
./umap_rss_demo_absl 
Config: N=10000000 do_reserve=true reserve_buckets=0 rounds=1 container=absl::flat_hash_map

=== Round 0 ===
[MEM] start | Rss=4.07 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.31 MB
[MEM] after insert | Rss=276.38 MB Pss=272.85 MB PrivDirty=272.45 MB SharedClean=3.62 MB
insert time: 1716 ms
[MEM] steady after insert | Rss=276.44 MB Pss=272.85 MB PrivDirty=272.45 MB SharedClean=3.69 MB
[MEM] after clear (no shrink) | Rss=4.44 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.69 MB
clear time: 25 ms
[MEM] steady after clear (still high due to capacity/retained) | Rss=4.44 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.69 MB
[MEM] after rehash(0) (buckets shrunk) | Rss=4.44 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.69 MB
rehash(0) time: 0 ms
[MEM] steady after rehash(0) | Rss=4.44 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.69 MB
[MEM] after swap-to-empty (capacity released to allocator) | Rss=4.44 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.69 MB
swap-to-empty time: 0 ms
[MEM] after purge/trim | Rss=4.44 MB Pss=0.85 MB PrivDirty=0.45 MB SharedClean=3.69 MB

Done.

        
Config: N=10000000 do_reserve=true reserve_buckets=0 rounds=1 container=std::unordered_map

=== Round 0 ===
[MEM] start | Rss=3.45 MB Pss=0.30 MB PrivDirty=0.22 MB SharedClean=3.20 MB
[MEM] after insert | Rss=387.93 MB Pss=384.46 MB PrivDirty=384.39 MB SharedClean=3.52 MB
insert time: 423 ms
[MEM] steady after insert | Rss=387.99 MB Pss=384.46 MB PrivDirty=384.39 MB SharedClean=3.58 MB
[MEM] after clear (no shrink) | Rss=387.99 MB Pss=384.46 MB PrivDirty=384.39 MB SharedClean=3.58 MB
clear time: 88 ms
[MEM] steady after clear (still high due to capacity/retained) | Rss=387.99 MB Pss=384.46 MB PrivDirty=384.39 MB SharedClean=3.58 MB
[MEM] after rehash(0) (buckets shrunk) | Rss=309.00 MB Pss=305.47 MB PrivDirty=305.40 MB SharedClean=3.58 MB
rehash(0) time: 7 ms
[MEM] steady after rehash(0) | Rss=309.00 MB Pss=305.47 MB PrivDirty=305.40 MB SharedClean=3.58 MB
[MEM] after swap-to-empty (capacity released to allocator) | Rss=309.00 MB Pss=305.47 MB PrivDirty=305.40 MB SharedClean=3.58 MB
swap-to-empty time: 0 ms
[MEM] after purge/trim | Rss=3.83 MB Pss=0.30 MB PrivDirty=0.23 MB SharedClean=3.58 MB

Done.
```

## Comment 3301642933

maintainer (COLLABORATOR) · xiaguan · 2025-09-17T07:21:21Z · https://github.com/kvcache-ai/Mooncake/issues/834#issuecomment-3301642933

close this issue since it's not a bug.
