# Resource Leak Potential

- URL: https://github.com/Dormant1337/overseer-c/issues/8
- Repo: Dormant1337/overseer-c (language: C)
- State: open; created 2025-12-20T09:01:37Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · MateiIonutEduard · 2025-12-20T09:01:37Z · https://github.com/Dormant1337/overseer-c/issues/8

Severity: **MEDIUM**
Component: `interface.c` - `handle_input_btop()`

1. **Description**:
Thread resource leak if `pthread_create()` fails without cleanup.

2. **Affected Code**:
```c
// interface.c line 276
pthread_create(thread_ptr, NULL, beacon_listener, NULL);  // No error check
```
3. **Impact**:
- Resource exhaustion
- Failed thread creation leaves application in inconsistent state

4. **Steps to Reproduce**:
Force thread creation to fail via resource limits.

5. **Recommended Fix**:
```c
int result = pthread_create(thread_ptr, NULL, beacon_listener, NULL);
if (result != 0) {
    // Handle error, clean up previous thread
    beacon_thread_active = false;
    scan_in_progress = false;
}
```
