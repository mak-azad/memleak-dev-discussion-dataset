#  AddressSanitizer: attempting free on address which was not malloc()-ed

- URL: https://github.com/microsoft/mimalloc/issues/795
- Repo: microsoft/mimalloc (language: C)
- State: closed; created 2023-07-27T22:36:23Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · sergio-nsk · 2023-07-27T22:36:23Z · https://github.com/microsoft/mimalloc/issues/795

When built with  AppleClang 13.1.6 on macOS Monterey 12.4 x86_64 with `-fsanitize=address` and configured with `-DMI_TRACK_ASAN=ON -DMI_OVERRIDE=OFF` and using V8 installed by `brew install v8`, getting the error while my app start:
```
==39100==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x02e41a0f09a0 in thread T0
1:     #0 0x10b1f95cd in wrap__ZdlPv+0x7d (libclang_rt.asan_osx_dynamic.dylib:x86_64h+0x575cd)
1:     #1 0x10d45e2ca in v8::internal::(anonymous namespace)::ComputeFlagListHash()+0x39a (libv8.dylib:x86_64+0x34[32](https://github.com/snxd/client/actions/runs/5685487943/job/15410906961?pr=1464#step:9:33)ca)
1:     #2 0x10d45df24 in v8::internal::FlagList::Hash()+0x14 (libv8.dylib:x86_64+0x342f24)
1:     #3 0x10d5ad69a in v8::internal::V8::Initialize()+0x86a (libv8.dylib:x86_64+0x49269a)
```
It seems to happen in libclang_rt wrap for `operator delete(void*)` in local variable destructors [v8/src/flags/flags.cc:555](https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:v8/src/flags/flags.cc;l=555;drc=714e1e34e823b7b4bc172fa4bdefee5aaf5e5fff).

My app includes `mimalloc-new-delete.h` in one of .cc files.
mimalloc v2.1.2

## Comment 4939727939

other (NONE) · github-actions[bot] · 2026-07-10T21:36:39Z · https://github.com/microsoft/mimalloc/issues/795#issuecomment-4939727939

This issue has been automatically marked as stale because it has not had recent activity. It will be closed if no further activity occurs in the next 14 days. Thank you for your contributions!

## Comment 5074660179

other (NONE) · github-actions[bot] · 2026-07-24T21:37:32Z · https://github.com/microsoft/mimalloc/issues/795#issuecomment-5074660179

This issue was closed because it has been inactive for 14 days since being marked as stale. Please feel free to reopen if this is still an active issue.
