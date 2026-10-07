# Possible handle leak: OnHover creates a cgo.Handle per call and nothing deletes it

- URL: https://github.com/bvisness/flowshell/issues/3
- Repo: bvisness/flowshell (language: C++)
- State: open; created 2026-09-20T04:19:28Z; status ok; passes offcwe

## Issue body

reporter (NONE) · OvOhao · 2026-09-20T04:19:28Z · https://github.com/bvisness/flowshell/issues/3

# Possible handle leak: OnHover creates a cgo.Handle per call and nothing deletes it

`OnHover` wraps the callback and its user data in a `cgo.Handle` and passes the
handle value to clay as the C user-data word.

clay/clay.go:1234

```go
func OnHover(f OnHoverFunc, userData any) {
	registeredFuncHandle := cgo.NewHandle(registeredOnHover{
		Func:     f,
		UserData: userData,
	})
	C.Clay_OnHover(C.Clay_OnHoverCallback(C.clayOnHoverCallback_cgo), C.intptr_t(registeredFuncHandle))
}
```

`clayOnHoverCallback` (clay.go:1243) resolves the handle with `.Value()` when
clay dispatches a hover, but does not release it, and the `clay` package contains
no `cgo.Handle.Delete` call at all.

Callers invoke `OnHover` from inside the child closures of an immediate-mode
element declaration, which re-run on every frame: app/ui.go:534 in the node
header, :712 in `UIButton`, :777 in the text field and :917. Each pass allocates
a new handle, and the previous frame's handle stays in the handle table together
with the closure and everything it captured.

`SetMeasureTextFunction` (clay.go:1250) shows the shape that does not accumulate:
it stores the Go callback in a package map keyed by the clay context
(clay.go:1273) rather than minting a handle per call.

Suggested fix: register the hover callback in a map keyed by the element id and
pass that key to `Clay_OnHover`, overwriting the entry on each frame; or delete
the handle at the end of the frame, once clay can no longer dispatch against it.

If you could credit me as a reporter for my contributions to security advisory I will be thankful.

