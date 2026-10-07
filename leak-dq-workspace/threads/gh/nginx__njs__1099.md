# Potential memory leak in njs_fs_fd_read error paths

- URL: https://github.com/nginx/njs/issues/1099
- Repo: nginx/njs (language: C)
- State: open; created 2026-07-14T11:32:37Z; status ok; passes main, offcwe

## Issue body

reporter (NONE) · minami-0213 · 2026-07-14T11:32:37Z · https://github.com/nginx/njs/issues/1099

## Description

`njs_fs_fd_read()` in `external/njs_fs_module.c` can leave its VM-pool buffer allocated when `read()` fails or when a buffer-growth allocation fails. Its caller, `njs_fs_read_file()`, closes the file descriptor on these paths but does not release `data.start`.

The buffer therefore remains allocated until the VM memory pool is destroyed. Repeated failing `readFile` operations in a long-lived VM could accumulate unreleased memory and increase memory consumption.

## Details

Analyzed commit: `e7eac4565bd0933e9ee066098109abbe6ce06650`

Affected locations:

- `external/njs_fs_module.c:247-260` in `njs_flags_table`
- `external/njs_fs_module.c:1843-1849` and `1861-1904` in `njs_fs_read_file()`
- `external/njs_fs_module.c:2852-2907` in `njs_fs_fd_read()`
- `src/njs_vm.c:204-208` in `njs_vm_destroy()`

Relevant code:

`external/njs_fs_module.c:247-260`

```c
static njs_fs_entry_t njs_flags_table[] = {
    { njs_str("a"),   O_APPEND | O_CREAT | O_WRONLY },
    { njs_str("a+"),  O_APPEND | O_CREAT | O_RDWR },
    { njs_str("as"),  O_APPEND | O_CREAT | O_SYNC | O_WRONLY },
    { njs_str("as+"), O_APPEND | O_CREAT | O_RDWR | O_SYNC },
    { njs_str("ax"),  O_APPEND | O_CREAT | O_EXCL | O_WRONLY },
    { njs_str("ax+"), O_APPEND | O_CREAT | O_EXCL | O_RDWR },
    { njs_str("r"),   O_RDONLY },
    { njs_str("r+"),  O_RDWR },
    { njs_str("rs+"), O_RDWR   | O_SYNC },
    { njs_str("w"),   O_CREAT  | O_TRUNC | O_WRONLY },
    { njs_str("w+"),  O_CREAT  | O_TRUNC | O_RDWR },
    { njs_str("wx"),  O_CREAT  | O_TRUNC | O_EXCL | O_WRONLY },
    { njs_str("wx+"), O_CREAT  | O_TRUNC | O_EXCL | O_RDWR },
```

`external/njs_fs_module.c:1843-1849`

```c
        (void) njs_vm_object_prop(vm, options, &string_flag, &flag);

        (void) njs_vm_object_prop(vm, options, &string_encoding, &encode);
    }

    flags = njs_fs_flags(vm, njs_value_arg(&flag), O_RDONLY);
    if (njs_slow_path(flags == -1)) {
```

`external/njs_fs_module.c:1878-1904`

```c
    data.start = NULL;
    data.length = sb.st_size;

    ret = njs_fs_fd_read(vm, fd, &data);
    if (njs_slow_path(ret != NJS_OK)) {
        if (ret == NJS_DECLINED) {
            ret = njs_fs_error(vm, "read", strerror(errno), path, errno,
                               &result);
        }

        goto done;
    }

    if (encoding == NULL) {
        ret = njs_buffer_set(vm, njs_value_arg(&result), data.start,
                             data.length);

    } else {
        ret = encoding->encode(vm, njs_value_arg(&result), &data);
        njs_mp_free(njs_vm_memory_pool(vm), data.start);
    }

done:

    if (fd != -1) {
        (void) close(fd);
```

`external/njs_fs_module.c:2858-2901`

```c
    size = data->length;

    if (size == 0) {
        size = 4096;
    }

    data->start = njs_mp_alloc(njs_vm_memory_pool(vm), size);
    if (data->start == NULL) {
        njs_vm_memory_error(vm);
        return NJS_ERROR;
    }

    p = data->start;
    end = p + size;

    for ( ;; ) {
        n = read(fd, p, end - p);

        if (njs_slow_path(n < 0)) {
            return NJS_DECLINED;
        }

        p += n;

        if (n == 0) {
            break;
        }

        if (end - p < 2048) {
            size *= 2;

            start = njs_mp_alloc(njs_vm_memory_pool(vm), size);
            if (start == NULL) {
                njs_vm_memory_error(vm);
                return NJS_ERROR;
            }

            memcpy(start, data->start, p - data->start);

            njs_mp_free(njs_vm_memory_pool(vm), data->start);

            p = start + (p - data->start);
            end = start + size;
            data->start = start;
```

`njs_fs_read_file()` obtains the requested open flags from the JavaScript options, opens the path, verifies that the descriptor refers to a regular file, initializes `data.length` from `sb.st_size`, and passes the descriptor and `data` to `njs_fs_fd_read()`. The accepted flag table includes write-only modes, so a successfully opened regular file can reach the helper with a descriptor on which `read()` returns an error.

The helper allocates `data.start` from the VM memory pool before its first `read()`. A negative `read()` result returns `NJS_DECLINED` immediately without freeing that allocation. If the file requires the buffer to grow, the helper allocates a doubled buffer and frees the previous buffer only after the new allocation succeeds; failure of the growth allocation returns `NJS_ERROR` while the current `data.start` allocation remains live.

In both cases, ownership remains with the helper's `data.start` pointer and is not transferred to a JavaScript Buffer. `njs_fs_read_file()` branches to `done`, where it closes only the descriptor. The later `njs_mp_free()` applies only to the encoding branch after `njs_fs_fd_read()` succeeds, so it cannot cover either helper error return. On successful unencoded reads, `njs_buffer_set()` instead attaches the allocation to the resulting Buffer.

Because the lost allocation belongs to the VM memory pool, it remains live until `njs_vm_destroy()` destroys that pool. Repeatedly reaching either error path within the same VM can consequently retain additional memory for the remainder of that VM's lifetime.

This behavior is most directly classified as CWE-401: Missing Release of Memory after Effective Lifetime.

