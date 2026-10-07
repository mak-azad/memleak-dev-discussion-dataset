# [Sync-src] gzopen: file descriptor leaked when zlib rejects the mode (c, x)

- URL: https://github.com/lacatoire/php-src/issues/2659
- Repo: lacatoire/php-src (language: C)
- State: open; created 2026-09-29T09:07:19Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · lacatoire · 2026-09-29T09:07:19Z · https://github.com/lacatoire/php-src/issues/2659

`gzopen()` leaks one file descriptor each time `gzdopen()` rejects the mode, which happens for the modes `c` and `x` that the plain file wrapper accepts.

**Where**

`ext/zlib/zlib_fopen_wrapper.c:201` — `self->gz_file = gzdopen(dup(fd), mode);`

The descriptor returned by `dup()` is owned by the gzFile only once `gzdopen()` succeeds. zlib returns `NULL` when the mode contains none of `r`, `w` or `a` (and does not close the descriptor it was given), and the failure path of the function (`:218-221`: `efree(self);` then the "gzopen failed" warning, then `php_stream_close(innerstream)`) closes the inner stream but not the duplicated descriptor. PHP's own wrapper accepts `c` and `x`, so the inner open succeeds first.

**Reproduce**

```php
<?php
function fds() { return count(glob("/proc/self/fd/*")); }
file_put_contents("f.gz", gzencode("x"));
$b = fds();
for ($i = 0; $i < 200; $i++) { $h = gzopen("f.gz", "c"); }
var_dump($h);
echo "mode c leaked ", fds() - $b, "\n";
$b = fds();
for ($i = 0; $i < 200; $i++) { @unlink("x.gz"); $h = gzopen("x.gz", "x"); }
echo "mode x leaked ", fds() - $b, " file created: ", var_export(file_exists("x.gz"), true), "\n";
$b = fds();
for ($i = 0; $i < 200; $i++) { $h = gzopen("f.gz", "r"); gzclose($h); }
echo "mode r leaked ", fds() - $b, "\n";
```

Output:
```
bool(false)
mode c leaked 200
mode x leaked 200 file created: true
mode r leaked 0
```

Each failing call leaves one open descriptor for the life of the process (there are no resources left to close), so a loop over such calls ends with `Too many open files`. With mode `x`, the file has also been created by the inner open before zlib refuses the mode. The message is `Warning: gzopen(): gzopen failed`; `ext/zlib/tests/bug61139.phpt` covers a `c` open and its warning, not the descriptor.

**Checked on** php-src PHP-8.5 (`PHP_RELEASE_VERSION 12`), PHP 8.5.4 CLI with ext/zlib, Linux.

