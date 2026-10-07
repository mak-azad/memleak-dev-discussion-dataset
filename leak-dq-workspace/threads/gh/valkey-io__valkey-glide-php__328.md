# CI: flaky Valgrind 9.0 job from glide-core global 'possibly lost' allocations (OTel init + client-registry DashMap)

- URL: https://github.com/valkey-io/valkey-glide-php/issues/328
- Repo: valkey-io/valkey-glide-php (language: PHP)
- State: open; created 2026-08-28T06:11:51Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · prateek-kumar-improving · 2026-08-28T06:11:51Z · https://github.com/valkey-io/valkey-glide-php/issues/328

## Summary

The **PHP Valgrind Tests (EngineVersion 9.0)** CI job intermittently fails with
`possibly lost` memory reported against glide-core global allocations, even when
all tests pass. The failure signature and error count fluctuate run-to-run
(e.g. `ERROR SUMMARY: 2 errors from 2 contexts` on one run, `3 errors from 3
contexts` on the next), which points at timing-dependent thread-teardown
behavior rather than a real leak.

These allocations are **process-lifetime globals in the Rust glide-core** that
are freed at process teardown, not per-connection. They are not caused by the
PHP/C extension code. As a stopgap, `valgrind.supp` suppressions were added in
PR #321 so the flaky gate stops blocking unrelated PRs. This issue tracks the
proper fix.

## Affected allocations (observed loss records)

1. **OpenTelemetry resource init** — `opentelemetry::common::Value::clone`
   (`Box<[u8]>`) → `opentelemetry_sdk::resource::Resource::from_detectors`,
   during one-time `GlideOpenTelemetry::initialise` (`once_cell`). ~22 bytes.

2. **glide-core client registry** — `glide_core::scope::register_client`
   inserting into `DashMap<u64, glide_core::client::Client>`; the `hashbrown`
   `RawTable::reserve_rehash` grows the backing table and valgrind marks the
   pre-rehash table `possibly lost`. Reached via the normal `connect()` path for
   both standalone (`create_glide_client`) and cluster
   (`create_glide_cluster_client`) clients. ~2.2–2.6 KB across 15–16 blocks.

## Why the existing suppressions don't catch these

`valgrind.supp` already has `opentelemetry_resource_from_detectors`, but it only
matches the `hashbrown ... insert → from_detectors` frame chain. The observed
record takes the `Value::clone` path instead, so it isn't matched.

## Stopgap applied in PR #321

Added two tolerant suppressions to `valgrind.supp`:
- `opentelemetry_resource_value_clone_from_detectors`
- `glide_core_scope_register_client_dashmap_rehash`

## Proper fix (this issue)

- Investigate whether `glide_core::scope::register_client` /
  `GlideOpenTelemetry::initialise` can be given deterministic teardown (or
  pre-sized to avoid rehash) so valgrind no longer reports `possibly lost`.
- Reassess the CI gate: `possibly lost > 0` on process-lifetime globals is a
  weak signal; consider gating only on `definitely lost` / `indirectly lost`,
  or on the delta vs a baseline, to reduce false positives.
- Once addressed upstream, remove the stopgap suppressions.

## Acceptance criteria

- [ ] The Valgrind 9.0 job passes deterministically across repeated runs.
- [ ] Root cause fixed in glide-core (or CI gate hardened) rather than relying
      solely on suppressions.
- [ ] Stopgap suppressions removed if no longer needed.

## Confirmed pre-existing on `main`

To rule out PR #321 (mTLS) as the cause, the same `PHP CI` workflow was run via
`workflow_dispatch` against `main` (which contains none of the mTLS changes):

- Run: https://github.com/valkey-io/valkey-glide-php/actions/runs/33147818473
- Valgrind 9.0 job: https://github.com/valkey-io/valkey-glide-php/actions/runs/33147818473/job/98772700807

Result on `main`: the Valgrind 9.0 job **also fails** with no test failure —
`possibly lost: 2,506 bytes in 16 blocks`, `ERROR SUMMARY: 3 errors from 3
contexts`. The three `possibly lost` records are identical in origin to those
seen on the PR:

- OpenTelemetry `Resource::from_detectors` init (~22 bytes)
- `glide_core::scope::register_client` DashMap rehash via `create_glide_client`
  (standalone, ~2.2 KB)
- `glide_core::scope::register_client` DashMap rehash via
  `create_glide_cluster_client` (cluster, ~280 bytes)

Byte/block counts jitter slightly run-to-run (e.g. 2,506 vs 2,522 bytes; 14 vs
15 blocks), which is the DashMap-rehash timing variance that also makes the error
count flicker (2 ↔ 3) and the gate flaky. This confirms the issue is pre-existing
in glide-core and independent of PR #321.


---

> [!IMPORTANT]
> **Blocked by / fix first: #330.** The Valgrind job is currently not triggered
> on `valkey-glide` submodule bumps (path-filter gap in `php.yml`), which is how
> this regression landed unexercised. #330 must be fixed first so CI actually
> runs the Valgrind job on glide-core bumps; otherwise regressions like this will
> continue to slip through regardless of the work here.

