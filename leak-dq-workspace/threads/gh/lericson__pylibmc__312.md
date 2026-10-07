# temporary-string leaks in `_make_behavior_consts()` (non-stealing append)

- URL: https://github.com/lericson/pylibmc/issues/312
- Repo: lericson/pylibmc (language: C)
- State: open; created 2026-08-02T13:03:43Z; status ok; passes offcwe

## Issue body

reporter (NONE) · K-ANOY · 2026-08-02T13:03:43Z · https://github.com/lericson/pylibmc/issues/312

There is a reference leak in `_make_behavior_consts()`. New references from `PyUnicode_FromString()` are passed to `PyList_Append()`, which does not steal, and are never released.

File: `src/_pylibmcmodule.c`

Function: `_make_behavior_consts`

Relevant code:

```c
for (b = PylibMC_callbacks; b->name != NULL; b++) {
    sprintf(name, "callback_%s", b->name);
    PyModule_AddIntConstant(mod, name, b->flag);
    PyList_Append(names, PyUnicode_FromString(b->name));
}
...
for (b = PylibMC_behaviors; b->name != NULL; b++) {
    PyList_Append(names, PyUnicode_FromString(b->name));
}
```

`PyUnicode_FromString()` returns a new reference, and `PyList_Append()` creates its own reference without stealing the caller's, so each temporary string is leaked — once per callback and once per behavior.

This runs once at import, so the practical impact is a small, one-time leak per process, but the missing `Py_DECREF()`s are unambiguous.

Suggested fix: store the string in a local, append, then decref:

```c
PyObject *s = PyUnicode_FromString(b->name);
if (s != NULL) {
    PyList_Append(names, s);
    Py_DECREF(s);
}
```

