# ckx() leaks the toString() jstring local reference

- URL: https://github.com/s-u/rJava/issues/353
- Repo: s-u/rJava (language: Java)
- State: open; created 2026-09-09T05:36:27Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-09T05:36:27Z · https://github.com/s-u/rJava/issues/353

### Summary

In `ckx()`, the `jstring` returned by `Throwable.toString()` is never released. Nearby local refs (`cname`, `cls`, `x`) are deleted, but `s` is not.

https://github.com/s-u/rJava/blob/534ff33499641619e3ca3ac7d573d953613d0102/src/rJava.c#L78-L114

```c
jstring s = (jstring)(*env)->CallObjectMethod(env, x, mid);
if (s) {
    const char *c = (*env)->GetStringUTFChars(env, s, 0);
    if (c) {
        msg = PROTECT(mkString(c));
        (*env)->ReleaseStringUTFChars(env, s, c);
    }
}
/* cname / cls / x are DeleteLocalRef'd; s is not */
```

`ReleaseStringUTFChars` only releases the UTF-8 buffer. It does not delete the JNI local reference.

### Why it sticks around

`ckx()` runs on the R thread after `AttachCurrentThread` (the `JNIEnv` is cached in `eenv` and is not detached for the session). This is not a Java-to-native JNI entry, so locals are not freed on return to R. `throwR()` then calls `stop()`, which typically does not return.

Each Java exception handled by `ckx()` therefore leaves one extra local ref (`s`) on that attached thread.

### Impact

One leaked local reference per exception. This is a small, persistent leak on a long-lived attached thread. It is unlikely to overflow the local reference table unless many Java exceptions are handled in the same R session.

### Suggested fix

After `ReleaseStringUTFChars` (and on the `s != NULL` path even if `GetStringUTFChars` fails):

```c
(*env)->DeleteLocalRef(env, s);
```
