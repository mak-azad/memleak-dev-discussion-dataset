# regex_remap AuTest is flaky: LeakSanitizer leak in ConfigReloadTask::start_progress_checker

- URL: https://github.com/apache/trafficserver/issues/13662
- Repo: apache/trafficserver (language: C++)
- State: open; created 2026-09-09T22:57:39Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · bryancall · 2026-09-09T22:57:39Z · https://github.com/apache/trafficserver/issues/13662

## Summary

The `regex_remap` AuTest fails nondeterministically on master. The test assertions all
pass; what fails is the `traffic_server` exit code, because LeakSanitizer reports a
leak during shutdown. The leak is in the config reload machinery and has nothing to do
with the test that surfaces it.

## Rate

Five runs of `regex_remap` on an unmodified `dev-asan` build of `7ed34a3d3c`, same
machine, same settings:

```
pass=1 fail=4 out of 5
```

## The report

```
==3136398==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 104 byte(s) in 1 object(s) allocated from:
    #0 operator new(unsigned long)
    #1 ConfigReloadTask::start_progress_checker()  src/mgmt/config/ConfigReloadTrace.cc:394
    #2 ReloadCoordinator::create_main_config_task(...)  src/mgmt/config/ReloadCoordinator.cc:77
    #3 ReloadCoordinator::prepare_reload(...)  src/mgmt/config/ReloadCoordinator.cc:67
    #4 rpc::handlers::config::reload_config(...)  src/mgmt/rpc/handlers/config/Configuration.cc:366
```

The failing check in the AuTest report is:

```
Process: ts: Failed
  Test : Checking that ReturnCode == 0 - Failed
     Reason: Returned Value 1 != 0
```

with every `diags.log` content assertion passing in the same run.

## Why this test surfaces it

`regex_remap.test.py` rewrites the shared rule file and reloads `remap.config` to
verify that a new shared rule generation is compiled. That reload is what allocates
the progress checker. Whether the allocation is still reachable at shutdown appears to
be timing dependent, which is why the failure is intermittent rather than constant.
Any AuTest that reloads config is a candidate to hit the same thing.

## Notes

There is no entry for this in `ci/asan_leak_suppression/`, and suppressing it would be
the wrong fix if the object is genuinely leaked rather than merely unreachable at exit.

Found while testing https://github.com/apache/trafficserver/pull/13661, which is
unrelated to config reload. That branch shows the same flake, so it is not introduced
there.

