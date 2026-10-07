# JNI local reference leak in TskAutoDbJava::addFile during image ingest

- URL: https://github.com/sleuthkit/sleuthkit/issues/3552
- Repo: sleuthkit/sleuthkit (language: C)
- State: open; created 2026-09-09T09:14:09Z; status ok; passes offcwe

## Issue body

reporter (NONE) · QiuYucheng2003 · 2026-09-09T09:14:09Z · https://github.com/sleuthkit/sleuthkit/issues/3552

## problem

`TskAutoDbJava` 在一次 JNI native 调用中遍历整张镜像并逐文件回调 Java。`addFile` 通过 `createJString` 创建的 `jstring` 在 `CallLongMethod` 之后没有 `DeleteLocalRef`。

Java 入口 `runOpenAndAddImgNat` / `runAddImgNat` 会调用 `startAddImage()` → `findFilesInImg()`。该 native 方法返回前，本次调用里创建的局部引用都不会被 JVM 自动回收。镜像文件数量很大时，局部引用表会持续增长，存在 overflow 或长时间占用大量 local ref 的风险。

## location

`bindings/java/jni/auto_db_java.cpp`

- `createJString`：`NewString` / `NewStringUTF` 后把引用交给调用方
- `addFile`：每个文件至少创建 `namej`、`pathj`、`extj`，有 SID / slack 时还会再创建；调用 `addFile` Java 方法后未释放
- `addFileWithLayoutRange`、`addImageInfo` 中 `SetObjectArrayElement` 的循环同样有临时 `jstring` 未删，但主路径是 `addFile`

`bindings/java/jni/dataModel_SleuthkitJNI.cpp`

- `initializeAddImgPasswordNat` 里 `initializeJni` 缓存 `JNIEnv*`
- `runOpenAndAddImgNat` 在同一次 native 调用中跑完整盘 ingest

## suggestion

在 `CallLongMethod` 返回后立即 `DeleteLocalRef`（`namej` / `pathj` / `extj` / `sidj` 以及 slack 相关字符串）。循环里创建、再塞进 `jobjectArray` 的临时 `jstring` 同样需要删。也可以在 `addFile` 入口 `PushLocalFrame`、出口 `PopLocalFrame`。
