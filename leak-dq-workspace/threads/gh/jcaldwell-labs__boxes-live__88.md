# fix: Memory leak when realloc fails in command_runner.c

- URL: https://github.com/jcaldwell-labs/boxes-live/issues/88
- Repo: jcaldwell-labs/boxes-live (language: C)
- State: open; created 2026-01-19T02:26:08Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · jcaldwell1066 · 2026-01-19T02:26:08Z · https://github.com/jcaldwell-labs/boxes-live/issues/88

## Problem
When `realloc()` fails during dynamic array expansion in command_runner.c:79-83, the original `lines` pointer is lost.

```c
char **new_lines = realloc(lines, sizeof(char *) * capacity);
if (!new_lines) {
    break;  // Memory leak: lines and allocated strings lost
}
```

## Affected Files
- `src/command_runner.c` - Lines 46-91

## Impact
- **Severity**: HIGH  
- Memory leak when allocation fails
- Allocated strings lost without cleanup

## Suggested Fix
```c
char **new_lines = realloc(lines, sizeof(char *) * capacity);
if (!new_lines) {
    // Free allocated lines before breaking
    for (int k = 0; k < line_count; k++) {
        free(lines[k]);
    }
    free(lines);
    break;
}
```

Found during tech debt retrospective (#86)
