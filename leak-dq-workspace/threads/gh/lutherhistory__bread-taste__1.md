# bug list of `v0.0.1`

- URL: https://github.com/lutherhistory/bread-taste/issues/1
- Repo: lutherhistory/bread-taste (language: C)
- State: open; created 2026-09-19T11:22:33Z; status ok; passes main

## Issue body

reporter (OWNER) · lutherhistory · 2026-09-19T11:22:33Z · https://github.com/lutherhistory/bread-taste/issues/1

# 🍞 Bd Interpreter — Bug List

**Repository:** Bread Taste (Bd)
**Version:** v0.0.1
**Date:** Initial push
**Status:** 🔧 Work in progress

---

## 🔴 Critical Bugs

### 1. Loop Execution Not Implemented
**File:** `main.c` — `can_parse()`
**Severity:** 🔴🔴🔴 Critical

```c
case '[':
    count_of_braces++;
    break;

case ']':
    count_of_braces--;
    break;
```

**Issue:** `[` and `]` only count braces. No actual jump logic.
**Expected:** 
- `[` → if `cell == 0`, jump to matching `]`
- `]` → if `cell != 0`, jump back to matching `[`

**Fix:** Build a jump table during parse phase.

---

### 2. `cell_move_ptr` Realloc Bug
**File:** `main.c` — `cell_move_ptr()`
**Severity:** 🔴🔴🔴 Critical

```c
self->ptr  += dir;
self->size++;
self->capc++;
self->mem = realloc(self->mem, self->size);
```

**Issue:**
- `realloc` called on every pointer movement — extremely slow
- `size` and `capc` always equal — no distinction
- `realloc` return value not checked
- Original pointer lost on `realloc` failure → memory leak

**Fix:** Only realloc when `ptr >= capc`. Double capacity. Check return.

---

### 3. Buffer Overflow in Tape Access
**File:** `main.c` — `can_parse()`
**Severity:** 🔴🔴🔴 Critical

```c
case '+':
    self->mem[*ptr]++;
```

**Issue:** `*ptr` can exceed allocated memory. `cell_move_ptr` increments `size` but `mem` doesn't actually grow correctly.

**Fix:** Validate `ptr < capc` before access. Ensure realloc happens before write.

---

## 🔴 Major Bugs

### 4. `realloc` Failure Not Checked
**File:** `main.c` — `cell_move_ptr()`
**Severity:** 🔴🔴

```c
self->mem = realloc(self->mem, self->size);
```

**Issue:** If `realloc` fails, `self->mem = NULL` → original memory leaked.

**Fix:**
```c
char* tmp = realloc(self->mem, new_size);
if (!tmp) { /* handle error */ }
self->mem = tmp;
```

---

### 5. Memory Leak in `cell_start`
**File:** `main.c` — `cell_start()`
**Severity:** 🔴🔴

```c
cell_type* self = malloc(sizeof(cell_type));
if (!self || !(self->mem = malloc(sizeof(char))))
    return NULL;
```

**Issue:** If `self` succeeds but `mem` fails, `self` is leaked.

**Fix:**
```c
if (!self) return NULL;
self->mem = malloc(sizeof(char));
if (!self->mem) {
    free(self);
    return NULL;
}
```

---

### 6. Potential Segfault in `cell_end`
**File:** `main.c` — `cell_end()`
**Severity:** 🔴🔴

```c
if (self) {
    LOG()   // accesses (*self)->capc
    free((*self)->mem);
    free(*self);
    *self = NULL;
}
```

**Issue:** `self != NULL` but `*self` could be `NULL`. `LOG()` dereferences `*self` → segfault.

**Fix:**
```c
if (self && *self) { ... }
```

---

### 7. Static Variable in `can_parse`
**File:** `main.c` — `can_parse()`
**Severity:** 🔴🔴

```c
static int count_of_braces = 0;
```

**Issue:** `static` persists across calls. Not reset per invocation. State leaks between calls.

**Fix:** Move to struct or make global. Reset explicitly.

---

### 8. Line-by-Line Parsing Breaks Loops
**File:** `main.c` — `main()`
**Severity:** 🔴🔴

```c
while (fgets(buf, sizeof(buf), file))
{
    if (!can_parse(cell, buf))
        break;
}
```

**Issue:** `[` and `]` can span multiple lines. Line-by-line parsing cannot handle cross-line loops.

**Fix:** Read entire file into a single buffer, then parse.

---

### 9. Incorrect Bracket Matching
**File:** `main.c` — `can_parse()`
**Severity:** 🔴🔴

```c
if (count_of_braces != 0)
    return 0;
return 1;
```

**Issue:**
- Checked per-line, not per-program
- `]` before `[` makes count negative — not detected
- Nested loops not validated

**Fix:** Use proper stack-based matching on full program.

---

## 🔴 Medium Bugs

### 10. Unsigned Arithmetic with Negative Direction
**File:** `main.c` — `cell_move_ptr()`
**Severity:** 🔴

```c
enum { LEFT = -1, RIGHT = +1 };
// ...
self->ptr += dir;   // ptr is size_t
```

**Issue:** `size_t` (unsigned) + `-1` → wrap-around to huge value.

**Fix:** Handle `LEFT`/`RIGHT` explicitly with separate branches.

---

### 11. `strlen` Called in Loop Condition
**File:** `main.c` — `can_parse()`
**Severity:** 🟡

```c
for (size_t i=0; i < strlen(buf); i++)
```

**Issue:** `strlen` is O(n), called every iteration → O(n²) total.

**Fix:**
```c
size_t len = strlen(buf);
for (size_t i = 0; i < len; i++)
```

---

### 12. `scanf("%c")` Whitespace Issue
**File:** `main.c` — `can_parse()`
**Severity:** 🟡

```c
case ',':
    scanf("%c", &self->mem[*ptr]);
```

**Issue:** `%c` reads whitespace (spaces, newlines) — unexpected input behavior.

**Fix:** Use `scanf(" %c", ...)` or `getchar()`.

---

### 13. `LOG()` Macro Semicolon Issue
**File:** `main.c` — top of file
**Severity:** 🟡

```c
#define LOG() \
    printf("\n\n"); \
    printf("capc: %zu\n", (*self)->capc); \
    ...
```

**Issue:** Multiple statements without `do { } while(0)` wrapper → dangling-else risk.

**Fix:**
```c
#define LOG() do { \
    printf("\n\n"); \
    ...
} while(0)
```

---

## 🟢 Minor Issues

### 14. Missing Newline in Error Messages
**File:** `main.c` — `command_line()`
**Severity:** 🟢

```c
fprintf(stderr, "%s: not found '%s'", argv[0], argv[i]);
```

**Issue:** No trailing `\n` → shell prompt sticks to error message.

**Fix:** Add `\n`.

---

### 15. `--version` Flag Not Implemented
**File:** `main.c` — `command_line()`
**Severity:** 🟢

```c
"-v, --version\t Show version number and quit\n"
```

**Issue:** Help text mentions `--version` but no handler exists.

**Fix:** Add `--version` case.

---

### 16. `--logs` Flag Does Nothing
**File:** `main.c` — `command_line()`
**Severity:** 🟢

```c
if (strcmp(argv[i], "--logs") == 0)
{
    // Enable logs
}
```

**Issue:** Empty handler. Needs global flag.

---

### 17. Multiple Files Overwrite in `command_line`
**File:** `main.c` — `command_line()`
**Severity:** 🟢

```c
for (int i=1; i < argc; i++)
{
    else if ((*file = fopen(argv[i], "r")) == NULL)
```

**Issue:** Multiple file args → previous `FILE*` leaked, only last one kept.

---

## 📋 Summary Table

| # | Bug | Severity | File |
|---|-----|----------|------|
| 1 | Loop execution not implemented | 🔴🔴🔴 | main.c |
| 2 | `cell_move_ptr` realloc bug | 🔴🔴🔴 | main.c |
| 3 | Buffer overflow in tape | 🔴🔴🔴 | main.c |
| 4 | `realloc` failure unchecked | 🔴🔴 | main.c |
| 5 | Memory leak in `cell_start` | 🔴🔴 | main.c |
| 6 | Segfault in `cell_end` | 🔴🔴 | main.c |
| 7 | Static var in `can_parse` | 🔴🔴 | main.c |
| 8 | Line-by-line parsing | 🔴🔴 | main.c |
| 9 | Bracket matching wrong | 🔴🔴 | main.c |
| 10 | Unsigned arithmetic | 🔴 | main.c |
| 11 | `strlen` in loop | 🟡 | main.c |
| 12 | `scanf %c` whitespace | 🟡 | main.c |
| 13 | `LOG()` macro semicolon | 🟡 | main.c |
| 14 | Missing `\n` in errors | 🟢 | main.c |
| 15 | `--version` missing | 🟢 | main.c |
| 16 | `--logs` empty | 🟢 | main.c |
| 17 | Multiple files overwrite | 🟢 | main.c |

---

## 🎯 Priority Fix Order

1. **Jump table** (fixes #1, #9)
2. **Read full file** (fixes #8)
3. **Tape realloc logic** (fixes #2, #3, #4, #10)
4. **Memory safety** (fixes #5, #6, #7)
5. **Minor cleanups** (#11–#17)

---

## 🍞 Notes

> "The dough is raw. It needs time to rise."
> 
> — Bd Philosophy

**Version:** v0.0.1 — "Dough"
**Next:** v0.0.2 — "First Bake" (loop fixed)

---

**Generated:** Initial push review
**Repo:** Bread Taste (Bd)
**Language:** C
