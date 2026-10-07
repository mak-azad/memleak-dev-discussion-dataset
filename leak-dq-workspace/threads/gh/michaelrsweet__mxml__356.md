# Memory leak of unlinked text nodes

- URL: https://github.com/michaelrsweet/mxml/issues/356
- Repo: michaelrsweet/mxml (language: C)
- State: closed; created 2026-09-01T06:32:42Z; status ok; passes main

## Issue body

reporter (NONE) · 1820893135-pixel · 2026-09-01T06:32:42Z · https://github.com/michaelrsweet/mxml/issues/356

## Summary

`mxml_load_data` (mxml-file.c) allocates text nodes inside its main loop and, on a parse error, jumps to a cleanup path that cannot reclaim nodes that were allocated but never linked into the returned tree. A 37-byte malformed XML (`<xml verser=21.0"=2rser=21.0"'/>tmei `) deterministically leaks **93 bytes per parse entry point** (88-B node + 5-B string); an application using both `mxmlLoadIO` and `mxmlLoadString` leaks **186 bytes per request**. LeakSanitizer reports `SUMMARY: AddressSanitizer: 186 byte(s) leaked in 4 allocation(s).` with every run.

Crucially, this is **still present after upstream's Issue #354 fix** (commit `a173d01`, "Fix potential memory leak when loading bad XML"): `mxml-file.c` in v4.0.5 and in `master` are byte-identical, and the POC below leaks on both. The #354 fix added `if (node && node != first) mxmlDelete(node);` to the `error:` path, but the leak we reproduce goes through text nodes created by `mxmlNewText(parent, whitespace, buffer)` that never become `first`, so the added check does not reach them.

- **Affected versions**: Mini-XML v4.0.5 and `master` (verified identical `mxml-file.c`; leak reproduces on both)
- **Severity**: Medium (deterministic per-request memory leak → resource exhaustion / DoS on any long-running parser)
- **CWE**: CWE-401 (Missing Release of Memory after an Effective Lifetime)

## Detail

### Affected code

`mxml-file.c` `mxml_load_data` main loop (v4.0.5 `:888`):

```c
        case MXML_TYPE_TEXT :
            node = mxmlNewText(parent, whitespace, buffer);   /* line 888: calloc 88-B node + strdup text */
            break;
```

`mxmlNewText` (`mxml-node.c:692/695/931`):

```c
mxml_node_t *mxmlNewText(mxml_node_t *parent, int whitespace, const char *string)
{
    mxml_node_t *node = mxml_new(MXML_TYPE_TEXT);      /* 931: calloc(1, sizeof(mxml_node_t)) = 88 bytes */
    ...
    node->value.text.whitespace = whitespace;
    node->value.text.string = _mxml_strcopy(string);   /* 695: strdup(text) */
    ...
```

and the `error:` cleanup path (v4.0.5 `:1438`, i.e. already containing the #354 fix):

```c
  // Common error return...
  error:

  if (node && node != first)
    mxmlDelete(node);

  mxmlDelete(first);

  free(buffer);

  return (NULL);
```

**Root cause**: when the input is malformed (here the attribute syntax `verser=21.0"=2rser=21.0"'/>` is invalid), `mxml_load_data` has already called `mxmlNewText(parent, whitespace, buffer)` and allocated a node, but parsing fails before that node is linked into the returned tree and control jumps to the `error:` label. The cleanup path deletes `node` (if it is not `first`) and `first`, but text nodes that were allocated by `mxmlNewText` in the loop and never assigned to `first` (e.g. the whitespace-only text node path at `:925` `node = mxmlNewText(parent, whitespace, "");` and the accumulated-text path at `:888`) are orphaned and leak. Each leaked node carries a `strdup`'d string (indirect leak). No harness involvement: the harness correctly `mxmlDelete()`s every non-NULL returned tree, so all leaked allocations are inside the library.

Call chain (each of the two entry points leaks once):

```
mxmlLoadIO   (mxml-file.c:202) ─┐
                                 ├─ mxml_load_data (mxml-file.c:888) ─ mxmlNewText (mxml-node.c:692)
mxmlLoadString (mxml-file.c:239)┘                                             └─ mxml_new (mxml-node.c:931)  calloc 88 B
                                                                               └─ _mxml_strcopy (mxml-node.c:695) strdup 5 B
```

## Build the reproducer

1. Check out Mini-XML v4.0.5 (or `master`):

   ```bash
   git clone --depth 1 --branch v4.0.5 https://github.com/michaelrsweet/mxml.git mxml
   cd mxml && ./configure >/dev/null && cd ..
   ```

2. Save this self-contained reproducer as `min_repro.c` (feeds the malformed XML through both public entry points):

   ```c
   /* minimal reproducer: mxml_load_data leaks an unlinked text node on parse failure */
   #include <stdio.h>
   #include <stdlib.h>
   #include "mxml.h"

   static size_t io_cb(void *cbdata, void *buffer, size_t bytes)
   {
     const unsigned char **src = (const unsigned char **)cbdata;
     const unsigned char  *s = src[0];
     size_t n = 0;
     while (n < bytes && s[n]) { ((unsigned char *)buffer)[n] = s[n]; n++; }
     src[0] = s + n;
     return n;
   }

   int main(int argc, char **argv)
   {
     mxml_node_t    *tree;
     mxml_options_t *options;
     const char     *input = "<xml verser=21.0\"=2rser=21.0\"'/>tmei ";
     const unsigned char *p;

     options = mxmlOptionsNew();

     /* path 1: mxmlLoadIO streaming parse */
     p = (const unsigned char *)input;
     tree = mxmlLoadIO(NULL, options, io_cb, &p);
     mxmlDelete(tree);

     /* path 2: mxmlLoadString in-memory parse */
     tree = mxmlLoadString(NULL, options, input);
     mxmlDelete(tree);

     mxmlOptionsDelete(options);
     return 0;
   }
   ```

3. Compile with ASan (LeakSanitizer is enabled by default under `-fsanitize=address`):

   ```bash
   gcc -O1 -g -fsanitize=address -fno-omit-frame-pointer \
     -D_THREAD_SAFE -D_REENTRANT -D__USE_MISC -D_GNU_SOURCE \
     -Imxml min_repro.c \
     mxml/mxml-attr.c mxml/mxml-file.c mxml/mxml-get.c mxml/mxml-index.c \
     mxml/mxml-node.c mxml/mxml-options.c mxml/mxml-private.c \
     mxml/mxml-search.c mxml/mxml-set.c \
     -lpthread -lm -o min_repro
   ```

## POC (tested on the unmodified source)

The 37-byte malformed XML:

```text
<xml verser=21.0"=2rser=21.0"'/>tmei 
```

(hex: `3c 78 6d 6c 20 76 65 72 73 65 72 3d 32 31 2e 30 22 3d 32 72 73 65 72 3d 32 31 2e 30 22 27 2f 3e 74 6d 65 69 20`)

Run:

```bash
./min_repro
echo "exit=$?"
```

## Trigger result

Verified on the unmodified source (LeakSanitizer, exit code 1):

```
==3360605==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 88 byte(s) in 1 object(s) allocated from:
    #0 ... in __interceptor_calloc .../asan_malloc_linux.cpp:154
    #1 ... in mxml_new mxml-node.c:931
    #2 ... in mxmlNewText mxml-node.c:692
    #3 ... in mxml_load_data mxml-file.c:888
    #4 ... in mxmlLoadString mxml-file.c:239
    #5 ... in main min_repro.c:31

Direct leak of 88 byte(s) in 1 object(s) allocated from:
    #0 ... in __interceptor_calloc .../asan_malloc_linux.cpp:154
    #1 ... in mxml_new mxml-node.c:931
    #2 ... in mxmlNewText mxml-node.c:692
    #3 ... in mxml_load_data mxml-file.c:888
    #4 ... in mxmlLoadIO mxml-file.c:202
    #5 ... in main min_repro.c:27

Indirect leak of 5 byte(s) in 1 object(s) allocated from:
    #0 ... in __interceptor_strdup .../asan_interceptors.cpp:454
    #1 ... in _mxml_strcopy mxml-private.c:99
    #2 ... in mxmlNewText mxml-node.c:695
    #3 ... in mxml_load_data mxml-file.c:888
    #4 ... in mxmlLoadString mxml-file.c:239

Indirect leak of 5 byte(s) in 1 object(s) allocated from:
    #0 ... in __interceptor_strdup .../asan_interceptors.cpp:454
    #1 ... in _mxml_strcopy mxml-private.c:99
    #2 ... in mxmlNewText mxml-node.c:695
    #3 ... in mxml_load_data mxml-file.c:888
    #4 ... in mxmlLoadIO mxml-file.c:202

SUMMARY: AddressSanitizer: 186 byte(s) leaked in 4 allocation(s).
```

- Replay exit code: `1` (LSan leak report)
- Deterministic: yes — 2/2 independent runs report the identical 186-byte / 4-allocation leak; the POC reproduces on both `mxmlLoadIO` and `mxmlLoadString` paths

<img width="2297" height="1297" alt="Image" src="https://github.com/user-attachments/assets/9d764ed9-32b2-4313-8fdc-06af421233ed" />

<img width="2277" height="1375" alt="Image" src="https://github.com/user-attachments/assets/e4579452-24dd-4425-a176-e7b0a5712408" />

## Suggested fix

1. **Core fix**: make the `error:` cleanup path reclaim every node created during parsing but not linked into the returned tree. Keep a temporary allocation list, or link each node into the `first` chain immediately after creation and walk the whole chain with `mxmlDelete` on error.

2. **Handle `parent==NULL` orphans**: nodes created by `mxmlNewText(parent, ...)` with a NULL parent are not referenced by any tree and must be freed by the error path.

3. **Regression test**: add this POC to the CI corpus, build with `-fsanitize=address` and run with leak detection enabled (`detect_leaks=1`); in OSS-Fuzz, add a dedicated leak-detection job separate from the main `detect_leaks=0` fuzz job.

This is a follow-up to upstream's own issue #354 — the fix commit `a173d01` did not cover this residual path, which is byte-identical between v4.0.5 and `master`.

## Comment 5497797475

maintainer (OWNER) · michaelrsweet · 2026-09-01T17:26:57Z · https://github.com/michaelrsweet/mxml/issues/356#issuecomment-5497797475

OK, I'm going to do some digging here but if "parent" is `NULL` then we shouldn't be even trying to parse more because the XML is invalid.

## Comment 5498908906

maintainer (OWNER) · michaelrsweet · 2026-09-01T18:59:40Z · https://github.com/michaelrsweet/mxml/issues/356#issuecomment-5498908906

I've pushed changes that will catch this as invalid XML, with proper cleanup:

[master 83ef80a] More memory leak fixes/error checking (Issue #356)


## Comment 5506071618

reporter (NONE) · 1820893135-pixel · 2026-09-02T07:29:56Z · https://github.com/michaelrsweet/mxml/issues/356#issuecomment-5506071618

Thanks for the quick fix.
