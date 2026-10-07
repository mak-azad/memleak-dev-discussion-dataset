# `val` dict leak in `_PylibMC_AddServerCallback()` when stat keys fetch fails

- URL: https://github.com/lericson/pylibmc/issues/310
- Repo: lericson/pylibmc (language: C)
- State: open; created 2026-08-02T13:00:52Z; status ok; passes offcwe

## Issue body

reporter (NONE) · K-ANOY · 2026-08-02T13:00:52Z · https://github.com/lericson/pylibmc/issues/310

There is reference leak in `_PylibMC_AddServerCallback()`. The `val` dict is created before `memcached_stat_get_keys()`, and the failure path returns without releasing it.

File: `src/_pylibmcmodule.c`

Function: `_PylibMC_AddServerCallback`

Relevant code:

```c
if ((val = PyDict_New()) == NULL)
    return MEMCACHED_FAILURE;

stat_keys = memcached_stat_get_keys(mc, stat, &rc);
if (rc != MEMCACHED_SUCCESS)
    return rc;                  // leaks val
```

`PyDict_New()` returns a new reference. If `memcached_stat_get_keys()` reports a failure, the function returns `rc` directly without `Py_DECREF(val)`, leaking the dict. Unlike allocation-failure paths, this is reachable on an ordinary runtime memcached error (e.g. a server stat request failing), so it can recur.

Suggested fix:

```c
stat_keys = memcached_stat_get_keys(mc, stat, &rc);
if (rc != MEMCACHED_SUCCESS) {
    Py_DECREF(val);
    return rc;
}
```

