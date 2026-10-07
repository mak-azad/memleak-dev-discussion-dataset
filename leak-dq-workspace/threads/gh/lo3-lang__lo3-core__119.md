# [BUG] String variables crash on cleanup — free() on stack pointer (var_setString missing strdup; regression of #16/#17)

- URL: https://github.com/lo3-lang/lo3-core/issues/119
- Repo: lo3-lang/lo3-core (language: C)
- State: open; created 2026-06-10T21:05:43Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · seesee010 · 2026-06-10T21:05:43Z · https://github.com/lo3-lang/lo3-core/issues/119

## Summary

Any program that uses a **string variable** crashes (heap corruption / abort) at cleanup, because `var_free` / `var_freeAll` call `free()` on a pointer that points into a **stack buffer**, not heap memory. The string value is never copied to the heap: `var_setString` stores the caller's pointer verbatim, and that pointer originates from `pars_resv`, which returns `&type[1]` — an address inside the stack-allocated `arg2[64]` buffer in `pars_file`.

This is the same defect previously tracked in #16 (BUG-03) and #17 (BUG-04), both now **closed**, but the fix is **not present in the current branch** — the code still stores the pointer without `strdup` and still frees it.

## Reproduction

```lo3
#n _s $3
#= _s _Hello
#o %s $0
#0 $0 $0
```

Built with `-fsanitize=address`, this aborts. Even without an explicit `#f`, the crash happens in `var_freeAll` at program exit:

```
==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed
    #1 var_freeAll src/var.c:122
    #2 main        src/main.c:34
Address ... is located in stack of thread T0 ... in frame pars_file src/parsing.c:39
  [256, 320) 'arg2' (line 43) <== Memory access is inside this variable
```

(With `#f _s`, the same bad-free fires earlier at `var_free` `src/var.c:110`.)

## Affected code

`src/var.c` — `var_setString` stores the pointer directly:

```c
void var_setString(const char *name, char *string) {
    ...
    list->array[i]->value.string = string;   // <-- no copy; aliases caller's buffer
}
```

`src/parsing.c` — `pars_resv` (TYPE_string) returns a pointer into the stack `type` buffer:

```c
case TYPE_string:
    result.value.string = &type[1];   // <-- points into stack arg buffer
    result.chooseType = 3;
    break;
```

…and `arg1`/`arg2` are stack arrays in `pars_file`:

```c
char arg1[64] = {0}, arg2[64] = {0};
```

`src/var.c` then frees that stack pointer:

```c
void var_freeAll(void) {
    for (...) {
        if (list->array[i]->type == 3) {
            free(list->array[i]->value.string);   // <-- free() on stack address
        }
        ...
    }
}
```

## What it does

- The stored string aliases `arg2` on `pars_file`'s stack. By the time the value is *read* (`#o %s`) the buffer may already have been overwritten by later `sscanf` calls (dangling read → wrong output), and at cleanup `free()` is called on a non-heap address (undefined behaviour, observed as an abort under ASan and as heap corruption otherwise).
- Net effect: **every program that assigns a string to a variable crashes on exit.**

## What it should do

Own the string on the heap. Have `var_setString` duplicate the input (and free any previous value):

```c
void var_setString(const char *name, char *string) {
    ...
    free(list->array[i]->value.string);        // free old (memset-0 on create makes this safe)
    list->array[i]->value.string = strdup(string);
    if (list->array[i]->value.string == NULL) {
        lo3_error("Out of memory while setting string var", name);
    }
}
```

Then `var_free` / `var_freeAll` free heap-owned memory as intended. (Re-opening / referencing #16 and #17 since the committed fix is missing on this branch.)

## Severity

**Critical** — 100% reproducible crash for any string-variable program; undefined behaviour / heap corruption.

---
*This issue was created by [Claude](https://claude.ai) on behalf of the repository maintainer.*

