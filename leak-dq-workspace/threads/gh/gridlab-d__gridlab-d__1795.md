# JNI local references leak in Java module callbacks (FindClass never deleted)

- URL: https://github.com/gridlab-d/gridlab-d/issues/1795
- Repo: gridlab-d/gridlab-d (language: C++)
- State: open; created 2026-09-09T05:25:33Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-09T05:25:33Z · https://github.com/gridlab-d/gridlab-d/issues/1795

### Summary

C-to-Java callbacks in the Java module create a new local `jclass` with `FindClass` on every call and never release it. These functions are not JNI native entries: they attach the simulation thread and call into Java, so the references are not freed when the C function returns.

Affected code:

- https://github.com/gridlab-d/gridlab-d/blob/e1841e1eebced819e45209f4a899763ce337b177/java/gridlabd_java.cpp#L33-L58
- https://github.com/gridlab-d/gridlab-d/blob/e1841e1eebced819e45209f4a899763ce337b177/java/gridlabd_java.h#L64-L147

### Details

`get_env()` calls `AttachCurrentThread` and never detaches:

```cpp
CDECL JNIEnv *get_env(){
    JNIEnv *env;
    if(jvm == nullptr)
        init_jvm();
    jvm->AttachCurrentThread((void **)&env, nullptr);
    return env;
}
```

`set_obj` then leaks `cls` on both the success path and the `GetMethodID` failure path:

```cpp
jclass cls = jnienv->FindClass("GObject");
if(cls == nullptr)
    return nullptr;

jmethodID mid = jnienv->GetMethodID(cls, "SetObject", "(JJI)V");
if(mid == nullptr)
    return nullptr;   // cls is still live

jnienv->CallVoidMethod(obj, mid, ...);
return nullptr;       // cls is still live
```

The same pattern is in `EXPORT_JAVA_CREATE`, `EXPORT_JAVA_INIT`, `EXPORT_JAVA_SYNC`, and `EXPORT_JAVA_PLC`: `FindClass` → `GetStaticMethodID` → `CallStatic*Method` → `return`, with no `DeleteLocalRef`. `FindClass` returning `NULL` is not itself a leak; the leak is the live `cls` after a successful lookup.

`sync_*` / `plc_*` are intended to run per object, per timestep, so one new local reference is added on every call.

JNI native methods that return `NewStringUTF` to Java (for example `Java_gridlabd_GObject__1GetName`) are not part of this issue.

### Impact

Local references remain until the thread detaches or the JVM is destroyed. Repeated `sync`/`plc` calls can fill the JNI local reference table (`JNI local reference table overflow`) and abort the JVM.

### Suggested fix

After `GetMethodID` / `GetStaticMethodID`, call `jnienv->DeleteLocalRef(cls)` on every path, including early returns.

Better: look up each class once, promote it with `NewGlobalRef`, cache the `jclass` and `jmethodID`, and stop calling `FindClass` in the hot path. Pair that with `PushLocalFrame`/`PopLocalFrame` (or detach when the thread is done) so remaining locals cannot accumulate across timesteps.
