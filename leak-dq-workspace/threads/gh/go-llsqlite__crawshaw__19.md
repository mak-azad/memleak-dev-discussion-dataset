# Possible memory leak of `Snapshot.schema` on the error paths of `(*Conn).GetSnapshot`

- URL: https://github.com/go-llsqlite/crawshaw/issues/19
- Repo: go-llsqlite/crawshaw (language: C)
- State: open; created 2026-08-28T02:02:59Z; status ok; passes main

## Issue body

reporter (NONE) · OvOhao · 2026-08-28T02:02:59Z · https://github.com/go-llsqlite/crawshaw/issues/19

# Possible memory leak of `Snapshot.schema` on the error paths of `(*Conn).GetSnapshot`

I found a possible memory leak on the error paths of `(*Conn).GetSnapshot`. The schema name is
allocated with `C.CString` **before** the two operations that can fail, and both failure returns
exit without freeing it. The finalizer that would normally release it is registered only after
those returns, and `Free()`'s own `s.ptr == nil` guard would short-circuit in any case, because
`sqlite3_snapshot_get` leaves `s.ptr` nil on failure. The failing conditions are the ones the
function's own doc comment enumerates (non-WAL schema, open transaction, no committed WAL
transaction yet), and the documented remedy for the last of these is to retry — so a retry loop
leaks once per attempt.

File: `snapshot.go`

Function: `github.com/go-llsqlite/crawshaw.(*Conn).GetSnapshot` (`snapshot.go:83-107`)

```go
func (conn *Conn) GetSnapshot(schema string) (*Snapshot, func(), error) {
	var s Snapshot
	if schema == "" || schema == "main" {
		s.schema = cmain
	} else {
		s.schema = C.CString(schema)
	}

	endRead, err := conn.disableAutoCommitMode()
	if err != nil {
		return nil, nil, err
	}

	res := C.sqlite3_snapshot_get(conn.conn, s.schema, &s.ptr)
	if res != 0 {
		endRead()
		return nil, nil, reserr("Conn.CreateSnapshot", "", "", res)
	}

	runtime.SetFinalizer(&s, func(s *Snapshot) {
		s.Free()
	})

	return &s, endRead, nil
}
```

The intended release, `snapshot.go:120-129` — note both the `s.ptr` guard and the `cmain` sentinel
check:

```go
func (s *Snapshot) Free() {
	if s.ptr == nil {
		return
	}
	C.sqlite3_snapshot_free(s.ptr)
	if s.schema != cmain {
		C.free(unsafe.Pointer(s.schema))
	}
	s.ptr = nil
}
```

1. Application code calls `conn.GetSnapshot(schema)` with a schema name other than `""` or
   `"main"` — e.g. the name of an `ATTACH`ed database.
2. Because the name is not the `main` sentinel, line 88 takes the `C.CString` branch:
   `malloc(len(schema)+1)` plus a copy of the Go string. `s.schema` now holds the only reference.
   `s` is a local `Snapshot` value; no finalizer is attached yet and `s.ptr` is still nil.
3. Line 91 calls `conn.disableAutoCommitMode()`, which can fail (open transaction, non-WAL schema,
   SQL error). Line 96 calls `C.sqlite3_snapshot_get`, which fails whenever SQLite's documented
   preconditions are unmet — precisely the three conditions listed in this function's own doc
   comment at lines 69-80.
4. Lines 93 and 99 return without touching `s.schema`. `s` goes out of scope and the `malloc` block
   becomes unreachable from Go. Both failure returns pass `nil` for the `*Snapshot` and the
   `endRead` closure, so the caller receives no handle and cannot free anything either.
5. The safety net at line 102 has not run yet, so no finalizer exists on these paths — and even if
   one did, `Free()`'s first statement (line 121, `if s.ptr == nil { return }`) would return early,
   because `sqlite3_snapshot_get` leaves `s.ptr` nil on failure. One `malloc` block of
   `len(schema)+1` bytes leaks per failed call.

The `main`/`""` branch is not affected: line 86 assigns the shared `cmain` sentinel
(`blob.go:29`) and allocates nothing. `Free()`'s `s.schema != cmain` test at line 125 shows the
authors already distinguish the two cases correctly on the success path.

Go trigger (if applicable):

```go
conn, _ := sqlite.OpenConn("file:test.db", 0)
defer conn.Close()

// A non-"main" schema name is required so that snapshot.go:88 allocates.
sqlite.Exec(conn, "ATTACH DATABASE 'file:other.db' AS other;", nil)

// "other" is not in WAL mode / has no committed WAL transaction, so
// sqlite3_snapshot_get fails and snapshot.go:99 returns without freeing.
for i := 0; i < 1_000_000; i++ {
	_, _, err := conn.GetSnapshot("other")
	if err == nil {
		panic("expected failure for this trigger")
	}
	// len("other")+1 bytes leaked per iteration
}
```

Any condition that makes `disableAutoCommitMode` or `sqlite3_snapshot_get` fail works. The leak is
synchronous and needs no GC step — and the finalizer that might have helped is never registered on
these paths.

Suggested fix: release on both failure paths with the same `!= cmain` guard used at line 125 — for
example by hoisting a cleanup that runs only when the function returns an error:

```go
	var s Snapshot
	allocated := false
	if schema == "" || schema == "main" {
		s.schema = cmain
	} else {
		s.schema = C.CString(schema)
		allocated = true
	}
	ok := false
	defer func() {
		if !ok && allocated {
			C.free(unsafe.Pointer(s.schema))
		}
	}()
	...
	ok = true
	return &s, endRead, nil
```

