# JNI local reference leak in CarbonWriter (sortBy can overflow local ref table)

- URL: https://github.com/apache/carbondata/issues/4402
- Repo: apache/carbondata (language: Scala)
- State: open; created 2026-09-09T08:09:15Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-09T08:09:15Z · https://github.com/apache/carbondata/issues/4402

## Problem

`sdk/CSDK/src/CarbonWriter.cpp` creates JNI local references (`NewStringUTF`, `FindClass`, `NewObjectArray`, `GetObjectClass`, `CallObjectMethodA`) and almost never calls `DeleteLocalRef`.

The C++ SDK embeds a JVM and keeps `JNIEnv` for the whole writer lifetime. These references are **not** released when a C++ function returns. They stay in the local reference table until `DeleteLocalRef`, `PopLocalFrame`, thread detach, or JVM destroy.

`close()` only deletes `carbonWriterBuilderObject`, `carbonWriterObject`, and a *local* `jclass` that shadows the member. Temporary refs from builder APIs are never cleaned up.

## Impact

- `sortBy` allocates one `jstring` per column in a loop and never deletes it after `SetObjectArrayElement`. A large `argc` can overflow the JNI local reference table (`JNI local references: ... exceeded`).
- Other builder methods (`outputPath`, `withHadoopConf`, `withLoadOption`, `withTableProperty`, `writtenBy`, …) leak a few refs per call. They persist until JVM destroy.
- Member fields store local refs without `NewGlobalRef`, which is invalid JNI for objects that must outlive a single native frame.

## Affected code

[`sdk/CSDK/src/CarbonWriter.cpp`](https://github.com/apache/carbondata/blob/f86ac085ddbbd8381b0a5b65658731fe618eff4a/sdk/CSDK/src/CarbonWriter.cpp)

**`sortBy` — leak grows with column count:**

```cpp
jclass objectArrayClass = jniEnv->FindClass("Ljava/lang/String;");
jobjectArray array = jniEnv->NewObjectArray(argc, objectArrayClass, NULL);
for (int i = 0; i < argc; ++i) {
    jstring value = jniEnv->NewStringUTF(argv[i]);
    jniEnv->SetObjectArrayElement(array, i, value);
    // missing: jniEnv->DeleteLocalRef(value);
}
carbonWriterBuilderObject = jniEnv->CallObjectMethodA(carbonWriterBuilderObject, methodID, args);
// missing: DeleteLocalRef(objectArrayClass / array / previous builder / carbonWriterBuilderClass)


Same pattern in outputPath (NewStringUTF + overwrite builder object) and withHadoopConf / withTableProperty / withLoadOption (two NewStringUTF args, never deleted).

close() does not cover these temps, and the member class is not deleted:
jclass carbonWriter = jniEnv->GetObjectClass(carbonWriterObject); // shadows the member
// ...
jniEnv->DeleteLocalRef(carbonWriterBuilderObject);
jniEnv->DeleteLocalRef(carbonWriterObject);
jniEnv->DeleteLocalRef(carbonWriter); // deletes the local jclass, not the FindClass member

Related: FindClass("Ljava/lang/String;") is the wrong name; JNI class names use java/lang/String.

Suggested fix
1. After each use, DeleteLocalRef on temps (jstring, jclass from GetObjectClass/FindClass, jobjectArray). In sortBy, delete value every iteration; delete array / objectArrayClass after the Java call.
2. Before overwriting carbonWriterBuilderObject, delete the previous local ref (or keep one global ref and update it).
3. Promote long-lived members (carbonWriter, carbonWriterBuilderObject, carbonWriterObject) with NewGlobalRef, and DeleteGlobalRef in close().
4. Prefer PushLocalFrame / PopLocalFrame or a small RAII local-ref wrapper so exception / early-return paths cannot skip cleanup.
5. Change FindClass("Ljava/lang/String;") to FindClass("java/lang/String").


## Comment 5944306563

other (CONTRIBUTOR) · chenliang613 · 2026-10-02T02:10:57Z · https://github.com/apache/carbondata/issues/4402#issuecomment-5944306563

great.
can you optimize this issue ? 
