# JNI local reference leaks in AndroidFileSystem (Iterate loop + Open)

- URL: https://github.com/openblack/openblack/issues/869
- Repo: openblack/openblack (language: C++)
- State: open; created 2026-09-09T13:39:21Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-09T13:39:21Z · https://github.com/openblack/openblack/issues/869

## Summary

`AndroidFileSystem` obtains `JNIEnv` via `SDL_AndroidGetJNIEnv()` and runs on SDL’s attached Android thread. Local JNI refs on that thread are **not** released when a C++ function returns. Several paths never call `DeleteLocalRef`, so refs accumulate until process exit. The worst case is `Iterate`: one large directory listing can overflow the JNI local reference table.

## Affected file

[`src/FileSystem/AndroidFileSystem.cpp`](https://github.com/openblack/openblack/blob/d804e19201cda0fead4ee226e8b1f9b8059d27a9/src/FileSystem/AndroidFileSystem.cpp)

## 1. `Iterate` — leak in the loop (high)

```cpp
jstring jgamePath = _jniEnv->NewStringUTF(_gamePath.c_str());
jstring jpath = _jniEnv->NewStringUTF(path.c_str());
jobjectArray jfilePaths = (jobjectArray)_jniEnv->CallStaticObjectMethod(...);

for (int i = 0; i < stringCount; i++) {
    jstring filePath = (jstring)(_jniEnv->GetObjectArrayElement(jfilePaths, i));
    const char* rawString = _jniEnv->GetStringUTFChars(filePath, nullptr);
    function(path / rawString);
    _jniEnv->ReleaseStringUTFChars(filePath, rawString);
    // filePath local ref never deleted
}
// jgamePath, jpath, jfilePaths never deleted

ReleaseStringUTFChars only releases the UTF buffer, not the jstring local ref. GetObjectArrayElement creates a new local ref every iteration. Listing a game data directory with hundreds of files can fill the local ref table (default ~512) in a single call.

2. Open — jpath / jgamePath never deleted (high)
jstring jpath = _jniEnv->NewStringUTF(path.c_str());
jstring jgamePath = _jniEnv->NewStringUTF(_gamePath.c_str());
jbyteArray jbytes = (jbyteArray)_jniEnv->CallStaticObjectMethod(...);
// ...
_jniEnv->DeleteLocalRef(jbytes);
return value; // jpath and jgamePath leaked

Only jbytes is deleted. Each file open leaks two jstring refs. Asset loading calls this repeatedly.

3. IsPathValid — leak on early return (low)
jgamePath / jpath are deleted on the success path, but if GetStaticMethodID returns nullptr the function return falses without deleting them.

4. Constructor — FindClass local ref (low)
_jniInteropClass = (jclass)_jniEnv->NewGlobalRef(
    _jniEnv->FindClass("org/openblack/app/FileSystemInterop"));

NewGlobalRef does not consume the FindClass local ref. Destructor only DeleteGlobalRefs _jniInteropClass.

SDL_AndroidGetActivity() is also a local ref stored in _jniActivity without NewGlobalRef. SDL documents that this jobject must be released with DeleteLocalRef (or promoted to a global ref).

Suggested fix
Delete every local ref on all paths, especially inside the Iterate loop:

_jniEnv->ReleaseStringUTFChars(filePath, rawString);
_jniEnv->DeleteLocalRef(filePath);

At the end of Iterate / Open (and the IsPathValid early return):

_jniEnv->DeleteLocalRef(jgamePath);
_jniEnv->DeleteLocalRef(jpath);
_jniEnv->DeleteLocalRef(jfilePaths); // Iterate only

After NewGlobalRef(FindClass(...)), DeleteLocalRef the FindClass result. Prefer a small RAII helper so returns cannot skip cleanup. Promote _jniActivity with NewGlobalRef and DeleteGlobalRef it in the destructor.



