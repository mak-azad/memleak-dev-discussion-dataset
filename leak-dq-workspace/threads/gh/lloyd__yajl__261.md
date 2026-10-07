# [Bug]memory leak in yajl_tree_parse on parse-failure path (CWE-401)

- URL: https://github.com/lloyd/yajl/issues/261
- Repo: lloyd/yajl (language: C)
- State: open; created 2026-08-03T07:45:44Z; status ok; passes main

## Issue body

reporter (NONE) · 1820893135-pixel · 2026-08-03T07:45:44Z · https://github.com/lloyd/yajl/issues/261

## Summary

When parsing **fails partway** (e.g. unterminated array/object, syntax error), `yajl_tree_parse()` only calls `yajl_free(handle)` to release the parser handle, but the **partially-built DOM tree already allocated on the heap through the callbacks (`ctx.root` and all its children) is never freed**, and the function returns NULL. The memory allocated by `context_push`/`value_alloc` leaks. Continuously feeding malicious/malformed JSON to a service using `yajl_tree_parse` accumulates memory until the process runs out (measured: ~43,384,151 allocations ≈ 1.2 GB leaked in a 60-second fuzz run), i.e. a **memory-exhaustion DoS**.

- **Affected versions**: YAJL 2.1.1 / HEAD `5e3a785` (2015-09-24)
- **Severity**: Medium (remote DoS, no RCE; can exhaust memory without authentication)
- **CWE**: CWE-401 (Missing Release of Memory after Effective Lifetime)

## Detail

### Affected code

The leak root cause is in `src/yajl_tree.c`. The DOM builder relies on heap allocations in `value_alloc` and `context_push`:

```c
/* src/yajl_tree.c:60-72 */
static yajl_val value_alloc (yajl_type type)
{
    yajl_val v;

    v = malloc (sizeof (*v));          /* heap allocation, must be freed on error path */
    if (v == NULL) return (NULL);
    memset (v, 0, sizeof (*v));
    v->type = type;

    return (v);
}

/* src/yajl_tree.c:113-133 */
static int context_push(context_t *ctx, yajl_val v)
{
    stack_elem_t *stack;

    stack = malloc (sizeof (*stack));  /* heap allocation, must be freed on error path */
    if (stack == NULL)
        RETURN_ERROR (ctx, ENOMEM, "Out of memory");
    memset (stack, 0, sizeof (*stack));

    assert ((ctx->stack == NULL)
            || YAJL_IS_OBJECT (v)
            || YAJL_IS_ARRAY (v));

    stack->value = v;
    stack->next = ctx->stack;
    ctx->stack = stack;

    return (0);
}
```

The error-handling path of `yajl_tree_parse` **only frees the handle, not the built tree**:

```c
/* src/yajl_tree.c:403-445 (excerpt) */
yajl_val yajl_tree_parse (const char *input,
                          char *error_buffer, size_t error_buffer_size)
{
    ...
    context_t ctx = { NULL, NULL, NULL, 0 };
    ...
    handle = yajl_alloc (&callbacks, NULL, &ctx);
    yajl_config(handle, yajl_allow_comments, 1);

    status = yajl_parse(handle,
                        (unsigned char *) input,
                        strlen (input));
    status = yajl_complete_parse (handle);
    if (status != yajl_status_ok) {
        if (error_buffer != NULL && error_buffer_size > 0) {
               internal_err_str = (char *) yajl_get_error(handle, 1,
                     (const unsigned char *) input,
                     strlen(input));
             snprintf(error_buffer, error_buffer_size, "%s", internal_err_str);
             YA_FREE(&(handle->alloc), internal_err_str);
        }
        yajl_free (handle);            /* <-- frees only the handle */
        return NULL;                   /* <-- DOM tree on ctx.root is dropped, leaks */
    }

    yajl_free (handle);
    return (ctx.root);
}
```

`context_t` holds `root` and the parse stack `stack`, but the error path never touches them:

```c
/* src/yajl_tree.c:32-44 */
struct context_s
{
    stack_elem_t *stack;    /* parse stack, contains intermediate pushed nodes */
    yajl_val root;          /* root of the partially-built DOM tree */
    char *errbuf;
    size_t errbuf_size;
};
typedef struct context_s context_t;
```

**Root cause**: the callbacks (`handle_start_array`/`handle_start_map`/`handle_number`, etc.) attach nodes to `ctx` via `value_alloc` + `context_push`, but when `yajl_complete_parse` returns failure, only `yajl_free(handle)` is called — **none of the heap nodes reachable from `ctx.stack` and `ctx.root` are reclaimed**.

`yajl_tree_free` already exists (see below), showing the author knew the tree must be released recursively; the **error path simply forgot to call it**:

```c
/* src/yajl_tree.c:478-503 */
void yajl_tree_free (yajl_val v)
{
    if (v == NULL) return;

    if (YAJL_IS_STRING(v))
    {
        free(v->u.string);
        free(v);
    }
    else if (YAJL_IS_NUMBER(v))
    {
        free(v->u.number.r);
        free(v);
    }
    else if (YAJL_GET_OBJECT(v))
    {
        yajl_object_free(v);
    }
    else if (YAJL_GET_ARRAY(v))
    {
        yajl_array_free(v);
    }
    else
    {
        free(v);
    }
}
```

## POC

Triggering input (7 bytes, cfg 0x40 enables the DOM parser):

```bash
# Input bytes (hex): 40 5b 31 2c 32 2c 33  i.e. @[1,2,3 (unterminated array)
# 0x40 = cfg bit, enables the yajl_tree_parse DOM path

# Repro command (leak detection enabled)
ASAN_OPTIONS=detect_leaks=1 ./yajl_fuzzer -runs=0 verify/repro_tree_parse_leak.bin
```

Repro directly via the `yajl_tree_parse` API:

```c
#include <yajl/yajl_tree.h>
int main(void) {
    for (int i = 0; i < 100000; i++) {
        char *errbuf[200];
        yajl_val v = yajl_tree_parse("[1,2,3", errbuf, sizeof(errbuf));
        /* returns NULL on parse failure, but the partial DOM leaks */
        /* if non-NULL, yajl_tree_free(v) must also be called */
    }
    return 0;
}
```

## Trigger result

```
==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 24 bytes in 1 object(s) allocated from:
    #0 __interceptor_malloc
    #1 context_push  src/yajl_tree.c:117
    #2 handle_start_array  src/yajl_tree.c:233
    #3 ...

Indirect leak of 8 bytes in 1 object(s) allocated from:
    #0 __interceptor_malloc
    #1 value_alloc  src/yajl_tree.c:63
    #2 handle_number  src/yajl_tree.c:298
    ...
```

- Replay exit code: `77` (LSAN fails by default)
- Measured leak scale: ~**43,384,151 allocations ≈ 1.2 GB** leaked in a 60-second fuzz run, blowing through libFuzzer's 2048 MB / 8192 MB RSS limits and triggering an OOM abort

## Suggested fix

1. **Call `yajl_tree_free` in the failure branch of `yajl_tree_parse` to recursively release the built tree**:

```c
if (status != yajl_status_ok) {
    if (error_buffer != NULL && error_buffer_size > 0) {
        internal_err_str = (char *) yajl_get_error(handle, 1,
              (const unsigned char *) input, strlen(input));
        snprintf(error_buffer, error_buffer_size, "%s", internal_err_str);
        YA_FREE(&(handle->alloc), internal_err_str);
    }
    yajl_free (handle);
    yajl_tree_free (ctx.root);        /* <-- new: free the built DOM */
    ctx.root = NULL;
    return NULL;
}
```

2. **Release every `stack_elem_t` still on the parse stack `ctx.stack`** (including its `value`), since those nodes have not yet been linked into `root`:

```c
static void context_stack_free(context_t *ctx) {
    stack_elem_t *cur = ctx->stack;
    while (cur) {
        stack_elem_t *next = cur->next;
        yajl_tree_free(cur->value);
        free(cur);
        cur = next;
    }
    ctx->stack = NULL;
}
```

3. **Walk the stack before `yajl_free(handle)`** — the top of the stack holds partially-built containers, so free them recursively and null out the root:

```c
if (status != yajl_status_ok) {
    ...
    context_stack_free(&ctx);
    yajl_tree_free(ctx.root);
    yajl_free (handle);
    return NULL;
}
```


## Comment 5183728493

other (NONE) · robohack · 2026-08-04T19:35:59Z · https://github.com/lloyd/yajl/issues/261#issuecomment-5183728493

This also looks like AI slop.

There is a related bug in the this original yajl version, #223, but these suggested fixes are all wrong.

See this commit in my version:  https://github.com/robohack/yajl/commit/38220afaffaf4fdf6770cdfad42960e19de164ed

That fix in my version has actually been tested rigorously.


## Comment 5790600689

reporter (NONE) · 1820893135-pixel · 2026-09-23T07:09:21Z · https://github.com/lloyd/yajl/issues/261#issuecomment-5790600689

Fixed in #264 (the failure path now releases the open stack elements and the partially built tree before returning NULL).
