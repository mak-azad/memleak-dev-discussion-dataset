# JNI local reference leak in getMetadata / NewStringUTF can overflow the local reference table

- URL: https://github.com/wseemann/ServeStream/issues/17
- Repo: wseemann/ServeStream (language: C)
- State: open; created 2026-09-21T04:37:50Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-21T04:37:50Z · https://github.com/wseemann/ServeStream/issues/17

## Summary

`native_getMetadata` leaks JNI local references on every metadata entry. Files with many tags can overflow the JNI local reference table (default ~512) and abort the process.

**File:** [`app/src/main/jni/metadata/wseemann_media_MediaMetadataRetriever.cpp`](https://github.com/wseemann/ServeStream/blob/3492aeaea54a3fade0e4c6cd4945255a2124177e/app/src/main/jni/metadata/wseemann_media_MediaMetadataRetriever.cpp)

## Problem

### 1. `NewStringUTF` never releases `string_Clazz`

```cpp
jclass string_Clazz = env->FindClass("java/lang/String");
jmethodID string_initMethodID = env->GetMethodID(string_Clazz, "<init>", "([BLjava/lang/String;)V");
jstring utf = env->NewStringUTF("UTF-8");
str = (jstring) env->NewObject(string_Clazz, string_initMethodID, array, utf);

env->DeleteLocalRef(utf);
env->DeleteLocalRef(array);
// string_Clazz is not deleted

This helper is not a JNI entry point. Local refs created here stay alive until the outer native method returns.


2. getMetadata calls it in a loop and drops HashMap.put's return value
for (i = 0; i < metadata->count; i++) {
    jstring jKey = NewStringUTF(env, metadata->elems[i].key);
    jstring jValue = NewStringUTF(env, metadata->elems[i].value);
    (jobject) env->CallObjectMethod(map, gHashMap_putMethodID, jKey, jValue);
    env->DeleteLocalRef(jKey);
    env->DeleteLocalRef(jValue);
}

jKey / jValue are released, but each iteration still leaves 3 local refs:

· 2 × string_Clazz from NewStringUTF
· 1 × unused HashMap.put return value (CallObjectMethod)


Suggested fix

// NewStringUTF: after NewObject
env->DeleteLocalRef(string_Clazz);

// getMetadata loop
jobject prev = env->CallObjectMethod(map, gHashMap_putMethodID, jKey, jValue);
if (prev) {
    env->DeleteLocalRef(prev);
}
env->DeleteLocalRef(jKey);
env->DeleteLocalRef(jValue);

Optionally cache java/lang/String as a global ref instead of calling FindClass on every tag.



