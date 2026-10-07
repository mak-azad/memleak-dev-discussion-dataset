# JNICustomFilter leaks local references on every DCT block row

- URL: https://github.com/mozilla/mozjpeg/issues/460
- Repo: mozilla/mozjpeg (language: C)
- State: open; created 2026-09-09T06:16:12Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-09T06:16:12Z · https://github.com/mozilla/mozjpeg/issues/460

### Summary

`JNICustomFilter` creates several JNI local references per call and never releases them. It is a C callback invoked from `tj3Transform`, so returning from the callback does not pop the JNI local frame. The surrounding `TJTransformer.transform` native method keeps running until the whole image is processed.

https://github.com/mozilla/mozjpeg/blob/08265790774cd0714832c9e675522acbe5581437/turbojpeg-jni.c#L1074-L1130

Each invocation typically leaves locals from:

- `NewDirectByteBuffer`
- `FindClass("java/nio/ByteOrder")`
- `ByteOrder.nativeOrder()`
- `GetObjectClass` / `asShortBuffer()` (the previous `bufobj` is overwritten without deletion)
- the discarded return value of `ByteBuffer.order()`
- `FindClass("java/awt/Rectangle")` and two `AllocObject` results

There is no `DeleteLocalRef` or `PushLocalFrame`/`PopLocalFrame` in this file.

### Why it accumulates

In `turbojpeg.c`, `customFilter` is called for every component and every 8-pixel-high DCT block row:

```c
for (ci = 0; ci < cinfo->num_components; ci++) {
  ...
  for (by = 0; by < compptr->height_in_blocks; by += compptr->v_samp_factor) {
    ...
    for (y = 0; y < compptr->v_samp_factor; y++) {
      t[i].customFilter(...);
```

A 1080p 4:2:0 image is on the order of ~270 callbacks. At ~8–10 locals each, a single `transform()` call can create well over a thousand local references. JNI only guarantees 16 without `EnsureLocalCapacity`/`PushLocalFrame`; many VMs cap the table around 512. This can fail with `JNI local reference table overflow` when a Java `TJCustomFilter` is installed.

The `GetObjectArrayElement` loops in `transform()` itself scale with the number of transforms (`n`), which is usually small. `THROW`/`THROW_TJ` run on error paths that return from the native method and are not the main issue.

### Suggested fix

At the start of `JNICustomFilter`, push a local frame and pop it on every return path:

```c
if ((*env)->PushLocalFrame(env, 16) < 0)
  return -1;
/* ... existing JNI calls ... */
(*env)->PopLocalFrame(env, NULL);
return 0;
```

Cache `jclass`/`jmethodID`/`jfieldID` across callbacks instead of calling `FindClass`/`GetMethodID` every block row.
