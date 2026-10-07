# Possible handle leak: ImageElementConfig.C creates a cgo.Handle for every image declaration and nothing deletes it

- URL: https://github.com/bvisness/flowshell/issues/2
- Repo: bvisness/flowshell (language: C++)
- State: open; created 2026-09-20T04:19:26Z; status ok; passes offcwe

## Issue body

reporter (NONE) · OvOhao · 2026-09-20T04:19:26Z · https://github.com/bvisness/flowshell/issues/2

# Possible handle leak: ImageElementConfig.C creates a cgo.Handle for every image declaration and nothing deletes it

`ImageElementConfig.C` mints a fresh `cgo.Handle` each time an element
declaration is converted for clay.

clay/clay.go:527

```go
func (r ImageElementConfig) C() C.Clay_ImageElementConfig {
	var imageHandlePtr unsafe.Pointer
	if r.ImageData != nil {
		imageHandle := cgo.NewHandle(r.ImageData)
		imageHandlePtr = unsafe.Pointer(&imageHandle)
	}
	// pinner.Pin(imageHandlePtr)

	return C.Clay_ImageElementConfig{
		imageData: imageHandlePtr,
	}
}
```

`ElementDeclaration.C` calls it for every element it converts (clay.go:1071),
`CLAY` feeds the result to `Clay__ConfigureOpenElement` (clay.go:1311), and the
handle is read back on the render side by `ImageRenderData2Go` with `.Value()`
(clay.go:843). No path releases it: the `clay` package contains no
`cgo.Handle.Delete` call at all.

The layout API is immediate mode, so the conversion runs once per element per
frame. `UIImage` (app/ui.go:941) rebuilds `clay.ImageElementConfig{ImageData: img}`
on every call, so the handle table grows by one entry per image per frame for as
long as the UI is running, and each entry keeps the image value alive.

`SetMeasureTextFunction` (clay.go:1250) shows the shape that does not accumulate:
it stores the Go callback in a package map keyed by the clay context
(clay.go:1273) rather than minting a handle per call.

Suggested fix: keep the image payload in a registry keyed by something stable,
such as the element id, and pass that key through `imageData`; or delete the
handle once the frame's render commands have been consumed.

If you could credit me as a reporter for my contributions to security advisory I will be thankful.

