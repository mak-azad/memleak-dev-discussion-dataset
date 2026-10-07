# Android os_shell_execute leaks JNI local references on attached native threads

- URL: https://github.com/GaijinEntertainment/DagorEngine/issues/210
- Repo: GaijinEntertainment/DagorEngine (language: C++)
- State: open; created 2026-09-15T11:09:56Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-15T11:09:56Z · https://github.com/GaijinEntertainment/DagorEngine/issues/210

## Summary

Android `os_shell_execute` attaches the current thread to the JavaVM, creates several JNI local references, then returns without `DeleteLocalRef` or `DetachCurrentThread`.

## Location

[`prog/engine/osApiWrappers/shellExecute.cpp`](https://github.com/GaijinEntertainment/DagorEngine/blob/75723669297e48e200a0dc67b18c1629e0975daf/prog/engine/osApiWrappers/shellExecute.cpp) (`_TARGET_ANDROID`)

```cpp
jint result = android::attach_current_thread(javaVM, &jniEnv, NULL);
jclass jcls_Activity = jniEnv->FindClass("android/app/Activity");
jclass jcls_Intent = jniEnv->FindClass("android/content/Intent");
jclass jcls_Uri = jniEnv->FindClass("android/net/Uri");
jstring jstr = jniEnv->NewStringUTF(file);
jobject uriObj = jniEnv->CallStaticObjectMethod(/* Uri.parse */, jstr);
jobject intentObj = jniEnv->NewObject(/* Intent(String) */,
    jniEnv->NewStringUTF("android.intent.action.VIEW"));
jniEnv->CallObjectMethod(intentObj, /* setData */, uriObj); // return value discarded
jniEnv->CallVoidMethod(/* activity */, /* startActivity */, intentObj);
// no DeleteLocalRef, no DetachCurrentThread


Why this leaks
This is a C++ engine API, not a JNI native method. Returning from C++ does not free JNI local references.

android::attach_current_thread leaves the thread attached. Game / android_main threads typically stay attached for the process lifetime, so these refs remain until the thread detaches or dies.

Each call leaves about 8–9 local refs:

· 3× FindClass (Activity, Intent, Uri)
· NewStringUTF(file)
· Uri.parse result
· temporary NewStringUTF("android.intent.action.VIEW")
· NewObject Intent
· unused Intent.setData return value

Repeated os_shell_execute on the same thread (open URL / store / etc.) accumulates entries in that thread’s local reference table (Android default ~512) and can lead to JNI ERROR: local reference table overflow (max=512).

Suggested fix
Wrap the JNI block in PushLocalFrame / PopLocalFrame, or DeleteLocalRef each temporary after use. Cache jclass / jmethodID as global refs if this path is hot.

Do not rely on C++ function return to recycle these refs while the thread stays attached.
