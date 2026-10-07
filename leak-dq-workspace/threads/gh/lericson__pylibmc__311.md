# temporary-object leaks in `_make_excs()` (non-stealing appends/set-attr)

- URL: https://github.com/lericson/pylibmc/issues/311
- Repo: lericson/pylibmc (language: C)
- State: open; created 2026-08-02T13:02:30Z; status ok; passes offcwe

## Issue body

reporter (NONE) · K-ANOY · 2026-08-02T13:02:30Z · https://github.com/lericson/pylibmc/issues/311

I found possible reference leaks in `_make_excs()`. New references from `Py_BuildValue()` and `PyLong_FromLong()` are passed to `PyList_Append()` and `PyObject_SetAttrString()`, which do not steal, and are never released.

File: `src/_pylibmcmodule.c`

Function: `_make_excs`

Relevant code:

```c
PyList_Append(exc_objs,
              Py_BuildValue("sO", "Error", (PyObject *)PylibMCExc_Error));
PyList_Append(exc_objs,
              Py_BuildValue("sO", "CacheMiss", (PyObject *)PylibMCExc_CacheMiss));

for (err = PylibMCExc_mc_errs; err->name != NULL; err++) {
    ...
    PyObject_SetAttrString(err->exc, "retcode", PyLong_FromLong(err->rc));
    ...
    PyList_Append(exc_objs,
                  Py_BuildValue("sO", err->name, (PyObject *)err->exc));
}
```

`Py_BuildValue()` and `PyLong_FromLong()` each return a new reference. `PyList_Append()` and `PyObject_SetAttrString()` create their own references and do not steal the caller's, so every one of these temporaries is leaked (the per-error ones inside the loop leak once per registered error code).

This runs once at import, so the practical impact is a small, one-time leak per process, but the missing `Py_DECREF()`s are unambiguous.

Suggested fix: store each temporary in a local, check it, append/set, then decref:

```c
PyObject *item = Py_BuildValue("sO", "Error", (PyObject *)PylibMCExc_Error);
if (item != NULL) {
    PyList_Append(exc_objs, item);
    Py_DECREF(item);
}
...
PyObject *rc_obj = PyLong_FromLong(err->rc);
if (rc_obj != NULL) {
    PyObject_SetAttrString(err->exc, "retcode", rc_obj);
    Py_DECREF(rc_obj);
}
```

