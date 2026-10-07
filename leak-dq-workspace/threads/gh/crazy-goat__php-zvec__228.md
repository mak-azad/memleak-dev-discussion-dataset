# fix(ffi): cross-boundary operator new/delete mismatch between libzvec.so and libzvec_ffi.so

- URL: https://github.com/crazy-goat/php-zvec/issues/228
- Repo: crazy-goat/php-zvec (language: PHP)
- State: open; created 2026-09-28T17:36:24Z; status ok; passes main

## Issue body

reporter (MEMBER) · s2x · 2026-09-28T17:36:24Z · https://github.com/crazy-goat/php-zvec/issues/228

Found while fixing the exit-time SIGABRT in #227. **Not fixed there** — this is a separate finding.

## Problem

valgrind still reports mismatched frees with the prebuilt SDK:

```
Mismatched free() / delete / delete []
   at 0x465EB0D: operator delete(void*, unsigned long)
   by 0x6555FF0: zvec_collection_insert (in ffi/build/libzvec_ffi.so)
 Address 0x12d01d80 is 0 bytes inside a block of size 40 alloc'd
   at 0x465A858: malloc
   by 0x8C200CB: operator new(unsigned long) (in zvec/build/lib/libzvec.so)
```

Same shape via `zvec_schema_free`. Objects are allocated by the `operator new` **inside libzvec.so** and released by the sized `operator delete(void*, unsigned long)` **in libzvec_ffi.so**.

## Why it happens

The SDK ships `operator new` / `operator delete` as **local** symbols (`nm` shows lowercase `t`, 0 exported), so libzvec carries its own libstdc++ allocation routines. `libzvec_ffi.so` exports 6 and therefore uses the dynamic libstdc++ that PHP FFI also uses. The two sides can disagree on the sized/unsized delete variant.

## Impact

Currently benign: both paths end in the same glibc `free()` on a glibc-allocated chunk, so nothing crashes. It is still undefined behaviour and could corrupt the heap if the two implementations diverge (allocator build differences, hardened allocators, jemalloc/tcmalloc preloaded under PHP).

This is **not** the cause of the exit-time SIGABRT in #227 — that was the double-constructed `GlobalConfig` singleton.

## Reproduction

```bash
./build_zvec.sh
valgrind php -n -d extension=ffi.so -r '
require "src/ZVec.php";
ZVec::init(logType: ZVec::LOG_CONSOLE, logLevel: ZVec::LOG_ERROR);
$p = sys_get_temp_dir() . "/zvec_mm_" . uniqid();
$s = new ZVecSchema("mm");
$s->addInt64("id", nullable: false)
  ->addVectorFp32("v", dimension: 4, metricType: ZVecSchema::METRIC_IP);
$c = ZVec::create($p, $s);
$c->insert((new ZVecDoc("a"))->setInt64("id", 1)->setVectorFp32("v", [1.0,0,0,0]));
$c->flush();
'
```

A `Mismatched free()` count is enough to turn this into a regression gate.

## Candidate approaches

1. **Link `libzvec_ffi.so` with `-static-libstdc++`** so the adapter matches the SDK. Cheap to try, but it only helps if the *allocation* also lands in the same copy — worth measuring rather than assuming.
2. **Prefer the unsized delete** in the adapter (`-fno-sized-deallocation`, since sized deallocation is the default) so both sides use the same variant.
3. **Report upstream** and ask for an SDK built against a shared libstdc++, or for the SDK to export its allocation symbols so one implementation wins.
4. **Build zvec from source** (`ZVEC_NO_SDK=1`), which sidesteps it by construction but gives up the build-time win from #227.

## Notes

- Must not regress the #227 singleton rule: no inlined `zvec::` singletons in the adapter.
- Only reproducible with the shared SDK; the static source build does not show it.
- Verified on Linux x86_64 with glibc.

Found during #227.


## Comment 5875287755

reporter (MEMBER) · s2x · 2026-09-28T17:36:31Z · https://github.com/crazy-goat/php-zvec/issues/228#issuecomment-5875287755

Confirmed on **Ubuntu / PHP 8.5.4 / glibc**, libzvec v0.7.0 prebuilt SDK.

A/B measurement for the same realistic workload (create collection, insert, flush, optimize, query, leave the collection open at exit):

| build | exit code | valgrind |
|---|---|---|
| inline  (#227 before) | **134** (SIGABRT) | invalid read in , 4 contexts |
|  via  (#227 after) | **0** | , 4 contexts |

So the singleton fix removed the fatal error but left this second, independent finding in place — which is why it is tracked separately rather than folded into #227.

 confirmation of the split:



Both sides reach the same glibc allocator, which is why it is currently benign rather than a crash. Also worth noting for anyone reproducing: the exact call sites are  and .

## Comment 5875289504

reporter (MEMBER) · s2x · 2026-09-28T17:36:38Z · https://github.com/crazy-goat/php-zvec/issues/228#issuecomment-5875289504

Confirmed on **Ubuntu / PHP 8.5.4 / glibc**, libzvec v0.7.0 prebuilt SDK.

A/B measurement for the same realistic workload (create collection, insert, flush, optimize, query, leave the collection open at exit):

| build | exit code | valgrind |
|---|---|---|
| inline `GlobalConfig::Instance()` (#227 before) | **134** (SIGABRT) | invalid read in `~GlobalConfig()`, 4 contexts |
| `global_config_ptr()` via `dlsym` (#227 after) | **0** | `Mismatched free() / delete`, 4 contexts |

So the singleton fix removed the fatal error but left this second, independent finding in place — which is why it is tracked separately rather than folded into #227.

`nm` confirmation of the split:

```
libzvec.so        operator new/delete: 18 local, 0 exported
libzvec_core.so   operator new/delete: 17 local, 0 exported
libzvec_ailego.so operator new/delete:  8 local, 0 exported
libzvec_ffi.so    operator new/delete:  2 local, 6 exported
```

Both sides reach the same glibc allocator, which is why it is currently benign rather than a crash. Also worth noting for anyone reproducing: the exact call sites are `zvec_collection_insert` and `zvec_schema_free`.


## Comment 5875302884

reporter (MEMBER) · s2x · 2026-09-28T17:37:31Z · https://github.com/crazy-goat/php-zvec/issues/228#issuecomment-5875302884

Context correction: the prebuilt-SDK work and the singleton fix this issue was filed against landed on `main` as e02dc6c, ahead of the PR that originally reported it (#227, now closed as superseded).

So on current `main` the state is:

- `global_config_ptr()` is present and the exit-time SIGABRT is gone (exit 0, suite green).
- This `Mismatched free() / delete` finding is still reproducible on `main` and is not yet addressed.

One correction to carry forward: the e02dc6c commit message and the earlier `tests/repro_ffi_static_libstdc_crash.php` attributed the SIGABRT to a static `libstdc++` in the SDK. That is not the mechanism — `nm` shows the SDK's `operator new` routes to the same `malloc@plt` as the adapter. The fatal cause was the double-constructed `GlobalConfig` singleton (each module constructing the same GNU_UNIQUE object under its own guard). The distinct sized/unsized delete variant mismatch described in this issue is real, but it is a separate and currently non-fatal problem.

`main` also still uses `php run-tests.php -n tests/`, which skips the FFI tests wherever FFI comes from a conf.d ini. Worth fixing separately: `php run-tests.php -n -d extension=ffi.so tests/`.

