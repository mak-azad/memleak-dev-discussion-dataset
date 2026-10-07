# Fix Python reference leaks in legacy getForces binding

- URL: https://github.com/Electrostatics/apbs/issues/310
- Repo: Electrostatics/apbs (language: C)
- State: open; created 2026-09-13T00:28:25Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · sobolevnrm · 2026-09-13T00:28:25Z · https://github.com/Electrostatics/apbs/issues/310

The legacy SWIG implementation in `tools/python/apbslib.i` creates the `qf`, `db`, and `ib` dictionary-key objects with `PyUnicode_FromString()` and passes them to `PyDict_SetItem()`. `PyDict_SetItem()` does not steal references, so those three local references need `Py_DECREF()` calls after insertion (including appropriate error-path cleanup).

This is pre-existing binding technical debt discovered while fixing #300. It does not block the parser/build compatibility work, but repeated `getForces()` calls in a long-running Python process can leak references.

Acceptance criteria:
- add correct decref/error cleanup for all locally owned objects in `getForces()`
- add a focused repeated-call or reference-count regression test
- verify the generated SWIG module under the supported Python binding CI lane
