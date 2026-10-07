# bsdunzip: Heap use-after-free when archive_read_free() returns non-ARCHIVE_OK status

- URL: https://github.com/libarchive/libarchive/issues/3623
- Repo: libarchive/libarchive (language: C)
- State: closed; created 2026-10-05T10:08:24Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · Abhirup0 · 2026-10-05T10:08:24Z · https://github.com/libarchive/libarchive/issues/3623

### Basic Information
* Version of libarchive: master / 3.8.x
* Operating system: All (POSIX and Windows)
* Component: `unzip/bsdunzip.c`

### Description
In `unzip/bsdunzip.c`, the final cleanup of the read archive object at line 1142 is wrapped in the `ac()` macro:

```c
ac(archive_read_free(a));
```

The `ac()` macro (defined at lines 110-115) checks the return code of the wrapped call and dereferences `a` if the return value is not `ARCHIVE_OK`:

```c
#define ac(call)						\
	do {							\
		int acret = (call);				\
		if (acret != ARCHIVE_OK)			\
			errorx("%s", archive_error_string(a));	\
	} while (0)
```

However, `archive_read_free(a)` unconditionally frees the archive structure and its error string buffer before returning:

```c
// libarchive/archive_read.c
archive_string_free(&a->archive.error_string);
...
free(a);
return (r);
```

If closing the archive or tearing down filters/formats during `archive_read_free()` returns a warning or failure (such as `ARCHIVE_WARN`), `acret != ARCHIVE_OK` evaluates to true, and `ac()` calls `errorx("%s", archive_error_string(a));`.

Because `a` was already passed to `free()`, `archive_error_string(a)` dereferences freed heap memory (`a->error_string.s`), resulting in a heap-use-after-free read.

### Proposed Fix
Align `bsdunzip` with the cleanup pattern used in `bsdtar` (`tar/read.c`):
1. Call `archive_read_close(a)` explicitly prior to freeing.
2. Check the return status of `archive_read_close(a)` and print `archive_error_string(a)` while `a` is still allocated.
3. Call `archive_read_free(a)` unconditionally without wrapping it in `ac()`.

```diff
diff --git a/unzip/bsdunzip.c b/unzip/bsdunzip.c
index 28247071..7ec50c76 100644
--- a/unzip/bsdunzip.c
+++ b/unzip/bsdunzip.c
@@ -1139,7 +1139,8 @@ unarchive(const char *fn)
 		}
 	}
 
-	ac(archive_read_free(a));
+	ac(archive_read_close(a));
+	archive_read_free(a);
 
 	if (passphrase_buf != NULL) {
 		memset(passphrase_buf, 0, PPBUFF_SIZE);
```


## Comment 5997596111

other (CONTRIBUTOR) · stoeckmann · 2026-10-05T15:27:43Z · https://github.com/libarchive/libarchive/issues/3623#issuecomment-5997596111

Looks right. Do you want to create a PR for this?

## Comment 5998505998

reporter (CONTRIBUTOR) · Abhirup0 · 2026-10-05T16:19:49Z · https://github.com/libarchive/libarchive/issues/3623#issuecomment-5998505998

Sure! let me write up a pr
