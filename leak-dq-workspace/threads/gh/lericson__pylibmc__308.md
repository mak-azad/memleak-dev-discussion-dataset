# `key_prefix` leaks in `_PylibMC_IncrMulti()`

- URL: https://github.com/lericson/pylibmc/issues/308
- Repo: lericson/pylibmc (language: C)
- State: open; created 2026-08-02T12:58:17Z; status ok; passes offcwe

## Issue body

reporter (NONE) · K-ANOY · 2026-08-02T12:58:17Z · https://github.com/lericson/pylibmc/issues/308

I found two possible reference leaks around `key_prefix` in `_PylibMC_IncrMulti()`: the empty-prefix case overwrites the only pointer with
`NULL`, and the `keys_tmp` allocation-failure path returns without releasing a non-empty prefix.

File: `src/_pylibmcmodule.c`

Function: `_PylibMC_IncrMulti`

Relevant code:

```c
if (key_prefix_raw != NULL) {
    key_prefix = PyBytes_FromStringAndSize(key_prefix_raw, key_prefix_len);

    if (key_prefix != NULL && PyBytes_Size(key_prefix) == 0)
        key_prefix = NULL;              // (1) overwrites the only reference
}

keys_tmp = PyList_New(nkeys);
if (keys_tmp == NULL)
    return NULL;                        // (2) bypasses cleanup, leaks key_prefix
```

with the cleanup block:

```c
cleanup:
    if (incrs != NULL)
        PyMem_Free(incrs);
    Py_XDECREF(key_prefix);
    Py_DECREF(keys_tmp);
    Py_XDECREF(iterator);
    return retval;
```

1. When an empty prefix is supplied (`key_prefix_raw != NULL`, length 0), `PyBytes_FromStringAndSize()` returns an owned reference, then
   `key_prefix = NULL` overwrites the only pointer without `Py_DECREF()`. The later `Py_XDECREF(key_prefix)` sees `NULL` and cannot release it. (The value is the empty-bytes object, so this is a refcount imbalance on a shared singleton rather than growing memory, but the missing decref is still a bug.)

2. If a non-empty `key_prefix` was created and `PyList_New(nkeys)` then fails, `return NULL` bypasses the `cleanup` block, leaking `key_prefix`. This
   requires an allocation failure.

Suggested fix:

```c
if (key_prefix_raw != NULL) {
    key_prefix = PyBytes_FromStringAndSize(key_prefix_raw, key_prefix_len);
    if (key_prefix == NULL)
        return NULL;
    if (PyBytes_Size(key_prefix) == 0) {
        Py_DECREF(key_prefix);
        key_prefix = NULL;
    }
}

keys_tmp = PyList_New(nkeys);
if (keys_tmp == NULL) {
    Py_XDECREF(key_prefix);
    return NULL;
}
```

