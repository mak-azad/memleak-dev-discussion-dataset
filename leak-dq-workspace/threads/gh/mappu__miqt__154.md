# Memory leak with callback return values

- URL: https://github.com/mappu/miqt/issues/154
- Repo: mappu/miqt (language: Go)
- State: open; created 2025-01-29T15:57:16Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · arnetheduck · 2025-01-29T15:57:16Z · https://github.com/mappu/miqt/issues/154

https://github.com/mappu/miqt/blob/7ee91701fc9d86233ec3d6d42a781e693f94888f/qt/gen_qabstractitemview.cpp#L977

In this callback handler, the `miqt_array` is allocated on the go side but never freed. Ditto for other, similar conversions.


## Comment 2623524681

maintainer (OWNER) · mappu · 2025-01-30T05:02:07Z · https://github.com/mappu/miqt/issues/154#issuecomment-2623524681

The `modelview` example with `QAbstractListModel_OnData` is susceptible to this - it has to return a pointer to QVariant, because that is all that can traverse the ABI, but the Qt C++ method presumes a pass by value.

Probably, any callbacks that return a type by value (and the C ABI has to project as a pass by value) will need to destruct the value.

Currently, the destructors are embedded directly in the emitgo functions (e.g. `emitParameterGo2CABIForwarding` does a lot of `defer C.free(...)`). They'll need to be split out to separate functions and called more intelligently.

This is the dual of the problem in #86. A complete solution would fix both problems.

## Comment 2624007273

reporter (CONTRIBUTOR) · arnetheduck · 2025-01-30T09:50:06Z · https://github.com/mappu/miqt/issues/154#issuecomment-2624007273

This bug is more about `miqt_array.data` which `miqt_exec_callback_QAbstractItemView_SelectedIndexes` allocates - after the generated code has finished iterating over the items and adding them to the list, it could free `data`. Ditto other similar converters (`miqt_string` to `QString` etc).

## Comment 2678039251

reporter (CONTRIBUTOR) · arnetheduck · 2025-02-24T10:45:33Z · https://github.com/mappu/miqt/issues/154#issuecomment-2678039251

https://github.com/seaqt/seaqt-gen/commit/eb9711ff3ca1aebc6fa10848c2899ceeb163b322 provides some relief to this issue
