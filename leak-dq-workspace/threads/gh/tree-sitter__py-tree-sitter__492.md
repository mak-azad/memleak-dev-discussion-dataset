# Allocation-failure error paths: one NULL dereference and several resource leaks

- URL: https://github.com/tree-sitter/py-tree-sitter/issues/492
- Repo: tree-sitter/py-tree-sitter (language: C)
- State: open; created 2026-08-02T10:49:18Z; status ok; passes offcwe

## Issue body

reporter (NONE) · K-ANOY · 2026-08-02T10:49:18Z · https://github.com/tree-sitter/py-tree-sitter/issues/492

Four places in the binding code mishandle allocation failure. None of them are reachable from ordinary Python code, they all require an allocation to fail, but one of them crashes the interpreter instead of raising `MemoryError`, and the rest leak objects or `PyMem` buffers on the way out. 

---

## 1. `parser_read_wrapper()`: unchecked `PyTuple_Pack()` result passed to `PyObject_Call()`

File: `tree_sitter/binding/parser.c`, lines 60-74

```c
// Form arguments to callable.
PyObject *byte_offset_obj = PyLong_FromUnsignedLong(byte_offset);
PyObject *position_obj = point_new_internal(wrapper_payload->state, position);
if (!position_obj || !byte_offset_obj) {
    *bytes_read = 0;
    return NULL;                                     // (b) leaks the other object
}

PyObject *args = PyTuple_Pack(2, byte_offset_obj, position_obj);
Py_XDECREF(byte_offset_obj);
Py_XDECREF(position_obj);

// Call callable.
PyObject *rv = PyObject_Call(read_cb, args, NULL);   // (a) args may be NULL
Py_XDECREF(args);
```

**(a) NULL dereference.** `PyTuple_Pack()` returns `NULL` on allocation failure. The C API documentation for `PyObject_Call()` states that `args` must not be `NULL` — an empty tuple must be used when there are no arguments. `PyObject_Call()` only guards this with `assert(PyTuple_Check(args))`, which is compiled out in release builds (`NDEBUG`), so the call proceeds and reads `args->ob_size` / `args->ob_item` off a `NULL` pointer. The result is a segfault rather than a recoverable `MemoryError`.

There is a second contract violation on the same path: when `PyTuple_Pack()` fails it leaves `MemoryError` set, and `PyObject_Call()` must not be invoked with a live exception. In a debug build this trips `assert(!_PyErr_Occurred(tstate))` and aborts.

This callback runs once per read chunk, so for a large source it is invoked repeatedly — a comparatively likely place to be sitting when the process runs out of memory.

**(b) Leak.** If exactly one of `byte_offset_obj` / `position_obj` is allocated successfully, the early return drops the successful one without releasing it.

Suggested fix for both:

```c
PyObject *byte_offset_obj = PyLong_FromUnsignedLong(byte_offset);
PyObject *position_obj = point_new_internal(wrapper_payload->state, position);
if (byte_offset_obj == NULL || position_obj == NULL) {
    Py_XDECREF(byte_offset_obj);
    Py_XDECREF(position_obj);
    *bytes_read = 0;
    return NULL;
}

PyObject *args = PyTuple_Pack(2, byte_offset_obj, position_obj);
Py_DECREF(byte_offset_obj);
Py_DECREF(position_obj);
if (args == NULL) {
    *bytes_read = 0;
    return NULL;
}

PyObject *rv = PyObject_Call(read_cb, args, NULL);
Py_DECREF(args);
```

---

## 2. `tree_changed_ranges()` / `tree_get_included_ranges()`: leaked result list and `TSRange` buffer

File: `tree_sitter/binding/tree.c`, functions `tree_changed_ranges` (line 107) and `tree_get_included_ranges` (line 137). Both have the identical shape:

```c
TSRange *ranges = ts_tree_get_changed_ranges(self->tree, tree, &length);

PyObject *result = PyList_New(length);
if (result == NULL) {
    return NULL;                       // leaks `ranges`
}
for (unsigned i = 0; i < length; ++i) {
    Range *range = PyObject_New(Range, state->range_type);
    if (range == NULL) {
        return NULL;                   // leaks `ranges` and `result`
    }
    range->range = ranges[i];
    PyList_SetItem(result, i, PyObject_Init((PyObject *)range, state->range_type));
}

PyMem_Free(ranges);
return result;
```

Both early returns skip `PyMem_Free(ranges)`; the second also drops the partially-filled `result` list.

Suggested fix:

```c
PyObject *result = PyList_New(length);
if (result == NULL) {
    PyMem_Free(ranges);
    return NULL;
}
for (unsigned i = 0; i < length; ++i) {
    Range *range = PyObject_New(Range, state->range_type);
    if (range == NULL) {
        Py_DECREF(result);
        PyMem_Free(ranges);
        return NULL;
    }
    ...
}
```

---

## 3. `PyInit__binding()`: leaked `enum.IntEnum` reference

File: `tree_sitter/binding/module.c`, lines 133-143

```c
PyObject *int_enum = import_attribute("enum", "IntEnum");
if (int_enum == NULL) {
    goto cleanup;
}
state->log_type_type = (PyTypeObject *)PyObject_CallFunction(
    int_enum, "s{sisi}", "LogType", "PARSE", TSLogTypeParse, "LEX", TSLogTypeLex);
if (state->log_type_type == NULL ||
    PyModule_AddObjectRef(module, "LogType", (PyObject *)state->log_type_type) < 0) {
    goto cleanup;
};
Py_DECREF(int_enum);
```

If `PyObject_CallFunction()` or `PyModule_AddObjectRef()` fails, control jumps to `cleanup` before `Py_DECREF(int_enum)`.

This one is inconsequential in practice — it happens at most once per process, and only on a path where module import fails anyway. Listed for completeness.

Suggested fix: decref before the jump.

```c
state->log_type_type = (PyTypeObject *)PyObject_CallFunction(
    int_enum, "s{sisi}", "LogType", "PARSE", TSLogTypeParse, "LEX", TSLogTypeLex);
Py_DECREF(int_enum);
if (state->log_type_type == NULL ||
    PyModule_AddObjectRef(module, "LogType", (PyObject *)state->log_type_type) < 0) {
    goto cleanup;
}
```

(A shared `cleanup` label with `Py_XDECREF(int_enum)` would also work, but requires hoisting the declaration above the earlier `goto`s.)

