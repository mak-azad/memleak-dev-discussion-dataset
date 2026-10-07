# [BUG] Integer range parsing: signed-overflow infinite loop & unbounded allocation

- URL: https://github.com/lucocozz/Argus/issues/59
- Repo: lucocozz/Argus (language: C)
- State: open; created 2026-06-20T12:27:12Z; status ok; passes main

## Issue body

reporter (OWNER) · lucocozz · 2026-06-20T12:27:12Z · https://github.com/lucocozz/Argus/issues/59

## Summary
Parsing an integer **range** from untrusted CLI input can cause a signed-integer-overflow (undefined behavior) **infinite loop** and/or **unbounded heap allocation** (DoS).

## Location
`source/callbacks/handlers/array_int_handler.c` — `add_range_values()` (and `parse_int_range()`).

```c
static void add_range_values(argus_option_t *option, const int_argus_range_t *range)
{
    for (int i = range->start; i <= range->end; i++) {
        adjust_array_size(option);
        option->value.as_array[option->value_count].as_int = i;
        option->value_count++;
    }
}
```

## Mechanism
With an input such as `--nums=1-2147483647`:
- `range->end == INT_MAX`. When `i == INT_MAX`, `i <= end` is true, then `i++` **overflows a signed int → UB** (in practice wraps to `INT_MIN`); the loop never terminates.
- Even without the overflow, a multi-billion-element range attempts to allocate `~range_size * sizeof(argus_value_t)` → memory exhaustion / OOM kill.

Both are reachable from the command line, on the documented range feature (`1-3,5,7-9`).

Related: `parse_int_range()` does `int start = strtol(value, NULL, 10);` with **no `errno`/`INT_MAX` check**, so values above `INT_MAX` are silently truncated on LP64.

## Repro
```sh
./myprog --nums=1-2147483647   # hangs / exhausts memory
```

## Suggested fix
- Cap the number of generated elements (`end - start`) to a sane maximum and raise `ARGUS_ERROR_INVALID_FORMAT` (or a dedicated limit error) above it.
- Iterate with a type/guard that cannot overflow (e.g. `long` loop counter, or check `i == end` before the increment).
- Validate `strtol` via `errno == ERANGE` and bounds-check against `INT_MIN/INT_MAX`.

## Severity
High — untrusted-input DoS + signed-overflow UB on a headline feature.

