# Memory leak in zip_file.cpp

- URL: https://github.com/duckdb/duckdb-excel/issues/96
- Repo: duckdb/duckdb-excel (language: C++)
- State: open; created 2026-09-06T22:26:33Z; status ok; passes main

## Issue body

reporter (NONE) · thomas-0816 · 2026-09-06T22:26:33Z · https://github.com/duckdb/duckdb-excel/issues/96

When testing the excel extension, asan found a leak:

```
010+ =================================================================
011+ ==110744==ERROR: LeakSanitizer: detected memory leaks
012+ 
013+ Direct leak of 288 byte(s) in 3 object(s) allocated from:
014+     #0 0x7f471a9080c1 in operator new(unsigned long) (/usr/lib/llvm-18/lib/clang/18/lib/linux/libclang_rt.asan-x86_64.so+0x1080c1) (BuildId: bf9e3747052c46cd49f7974555b1700dce30b8c0)
015+     #1 0x7f4714951615 in duckdb::LocalFileSystem::OpenFile(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>> const&, duckdb::FileOpenFlags, duckdb::optional_ptr<duckdb::FileOpener, true>) (/home/runner/work/pdo-duckdb-php/pdo-duckdb-php/modules/pdo_duckdb.so+0x1751615) (BuildId: d410e8434a31512ca75868e800c188b51a70ba1d)
016+     #2 0x7f4714903a52 in duckdb::FileSystem::OpenFile(duckdb::OpenFileInfo const&, duckdb::FileOpenFlags, duckdb::optional_ptr<duckdb::FileOpener, true>) (/home/runner/work/pdo-duckdb-php/pdo-duckdb-php/modules/pdo_duckdb.so+0x1703a52) (BuildId: d410e8434a31512ca75868e800c188b51a70ba1d)
017+ 
018+ SUMMARY: AddressSanitizer: 288 byte(s) leaked in 3 allocation(s).

(full output, see https://github.com/thomas-0816/pdo-duckdb-php/actions/runs/34059786123/job/101558130750)
```

Suggested diff from the llm:

```
diff --git a/src/excel/xlsx/zip_file.cpp b/src/excel/xlsx/zip_file.cpp
index 8640ee4..bb3e906 100644
--- a/src/excel/xlsx/zip_file.cpp
+++ b/src/excel/xlsx/zip_file.cpp
@@ -54,7 +54,7 @@ int32_t mz_stream_duckdb_open(void *stream, const char *path, int32_t mode) {
 
        if (self.handle) {
                self.handle->Close();
-               self.handle->~FileHandle();
+               delete self.handle;
                self.handle = nullptr;
                self.last_error.clear();
        }
@@ -135,7 +135,7 @@ int32_t mz_stream_duckdb_seek(void *stream, int64_t offset, int32_t origin) {
 int32_t mz_stream_duckdb_close(void *stream) {
        auto &self = *reinterpret_cast<mz_stream_duckdb *>(stream);
        self.handle->Close();
-       self.handle->~FileHandle();
+       delete self.handle;
        self.handle = nullptr;
        self.last_error.clear();
        return MZ_OK;
@@ -160,7 +160,7 @@ void mz_stream_duckdb_delete(void **stream) {
        auto &self = *reinterpret_cast<mz_stream_duckdb *>(*stream);
        if (self.handle) {
                self.handle->Close();
-               self.handle->~FileHandle();
+               delete self.handle;
                self.handle = nullptr;
                self.last_error.clear();
        }
```

Explanation from the llm:

The `mz_stream_duckdb` wrapper takes ownership of a raw `FileHandle *` returned by `FileSystem::OpenFile` (which allocates it with `operator new` inside `LocalFileSystem::OpenFile`), but releases it by calling only `~FileHandle()`, the destructor. Calling a destructor directly never invokes `operator delete`, so the object's memory is never freed—only the destructor body runs. Every opened xlsx file (the `COPY TO` writer stream and the `ZipFileReader` stream used by `SELECT * FROM <xlsx>`) therefore leaks one `FileHandle*` and any buffers it owns, which is exactly the "288 bytes in 3 objects allocated from duckdb::LocalFileSystem::OpenFile" LeakSanitizer report. The correct deallocation is `delete self.handle`, which runs the destructor and frees the allocation.

DuckDB v1.5.5
excel extension_version: f4c72b5
OS: Linux

cc @Maxxen 
