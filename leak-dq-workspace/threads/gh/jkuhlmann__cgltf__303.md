# [Bug] Memory leak in cgltf_write_file() when fopen() fails

- URL: https://github.com/jkuhlmann/cgltf/issues/303
- Repo: jkuhlmann/cgltf (language: C)
- State: open; created 2026-08-27T03:25:31Z; status ok; passes main

## Issue body

reporter (NONE) · trustqq · 2026-08-27T03:25:31Z · https://github.com/jkuhlmann/cgltf/issues/303

## Summary

`cgltf_write_file()` allocates a buffer, serializes the entire document into it, and then — if the output file cannot be opened — returns `cgltf_result_file_not_found` without freeing the buffer. The buffer holds the fully serialized output (as large as the file itself would be), so every failed call leaks that amount of memory.

## Affected code

`cgltf_write.h`, function `cgltf_write_file()`
(verified on master @ `85cd62382dfea638278962690cf515023f33ed00`)

## Details

The allocation and serialization happen before the file is opened:

```c
/* cgltf_write.h:1247-1249 */
cgltf_size expected = cgltf_write(options, NULL, 0, data);
char* buffer = (char*) malloc(expected);
cgltf_size actual = cgltf_write(options, buffer, expected, data);
```

The error path then returns without freeing `buffer`:

```c
/* cgltf_write.h:1253-1257 */
FILE* file = fopen(path, "wb");
if (!file)
{
    return cgltf_result_file_not_found;   /* buffer leaks here */
}
```

The success path frees the buffer at line 1266 (`free(buffer);`), so only this error path is missing the `free()`.

## Steps to reproduce

```c
cgltf_options options = {0};
/* data: any valid cgltf_data */

/* Output directory does not exist (or path is not writable): */
cgltf_result res = cgltf_write_file(&options, "/nonexistent_dir/out.gltf", data);
/* res == cgltf_result_file_not_found; `expected` bytes leaked */
```

No OOM is involved — any unopenable output path (missing directory, no write permission) triggers the leak. Because the leaked amount equals the size of the fully serialized file, a long-running application that retries saving can accumulate significant memory.

## Suggested fix

```c
FILE* file = fopen(path, "wb");
if (!file)
{
    free(buffer);   /* add this line */
    return cgltf_result_file_not_found;
}
```

## Metadata

- Detector: static analysis (MemLeak)
- CWE: CWE-401 (Missing Release of Memory after Effective Lifetime)
- Severity: MEDIUM

