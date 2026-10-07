# [BUG] JNI local reference leak in nativeMoveWindow

- URL: https://github.com/Vera-Firefly/Pojav-Glow-Worm/issues/435
- Repo: Vera-Firefly/Pojav-Glow-Worm (language: C)
- State: open; created 2026-09-21T04:13:28Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-21T04:13:28Z · https://github.com/Vera-Firefly/Pojav-Glow-Worm/issues/435

### Describe the bug

AWTInputBridge.nativeMoveWindow leaks one JNI local reference per AWT Frame on every window move.

In app/src/main/jni/pojav/awt_bridge.c, the loop calls Component.getBounds(Rectangle) via CallObjectMethod and discards the return value. That call still creates a new local reference, even when Java returns the same rectangle object. frame is deleted; the getBounds return is not.

These JNI calls use the cached runtimeJNIEnvPtr_INPUT (JRE VM), which is attached once and never detached. Returning to Android Java only frees local refs on the Android JNIEnv, not on this cached env. Repeated window moves therefore accumulate local refs on the JRE thread and can hit local reference table overflow (max=512).

Code:
app/src/main/jni/pojav/awt_bridge.c

jobject frame = (*runtimeJNIEnvPtr_INPUT)->GetObjectArrayElement(..., frames, i);
(*runtimeJNIEnvPtr_INPUT)->CallObjectMethod(..., frame, method_GetBounds, rectangle); // return value leaked
...
(*runtimeJNIEnvPtr_INPUT)->DeleteLocalRef(..., frame); // only frame is deleted


### The log file and images/videos

N/A. 

This is a source-level JNI defect; it does not require a latestlog.txt from a specific crash. The leak is visible in nativeMoveWindow as written.



### Steps To Reproduce

```markdown
1. Launch a Java GUI / AWT session that uses `AWTInputBridge`.
2. Move the AWT window (this calls `nativeMoveWindow`).
3. Repeat. Each call leaks 1 local ref per Frame on `runtimeJNIEnvPtr_INPUT`.
```

### Expected Behavior

Every local reference created in the loop should be deleted before the next iteration. After getBounds, the returned jobject must be DeleteLocalRef'd. The cached JRE JNIEnv must not grow local refs across window-move calls.



### Platform

```markdown
- Device model: N/A (source-level, not device-specific)
- CPU architecture: N/A
- Android version: N/A
- PojavLauncher version: present in 617c16bb (`app/src/main/jni/pojav/awt_bridge.c`)
```

### Anything else?

Suggested fix:

jobject bounds = (*runtimeJNIEnvPtr_INPUT)->CallObjectMethod(
    runtimeJNIEnvPtr_INPUT, frame, method_GetBounds, rectangle);
(*runtimeJNIEnvPtr_INPUT)->SetIntField(...);
(*runtimeJNIEnvPtr_INPUT)->SetIntField(...);
(*runtimeJNIEnvPtr_INPUT)->CallVoidMethod(..., frame, method_SetBounds, rectangle);
if (bounds)
    (*runtimeJNIEnvPtr_INPUT)->DeleteLocalRef(runtimeJNIEnvPtr_INPUT, bounds);
(*runtimeJNIEnvPtr_INPUT)->DeleteLocalRef(runtimeJNIEnvPtr_INPUT, frame);

bounds and rectangle may be the same Java object, but they are two local-ref slots. Deleting bounds does not invalidate rectangle.
