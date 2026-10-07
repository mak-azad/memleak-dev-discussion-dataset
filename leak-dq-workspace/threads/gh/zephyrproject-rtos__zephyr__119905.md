# posix: rwlock: PTHREAD_RWLOCK_INITIALIZER fails with EINVAL and lacks lazy-init synchronization

- URL: https://github.com/zephyrproject-rtos/zephyr/issues/119905
- Repo: zephyrproject-rtos/zephyr (language: C)
- State: open; created 2026-09-22T08:39:48Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · harshitnub077 · 2026-09-22T08:39:48Z · https://github.com/zephyrproject-rtos/zephyr/issues/119905

### Describe the bug

Statically declared read-write locks initialized with `PTHREAD_RWLOCK_INITIALIZER` (`-1`) are unusable at runtime on Zephyr:

1. **Acquisition functions bypass lazy allocation**: `pthread_rwlock_rdlock()`, `pthread_rwlock_wrlock()`, and their `try*` and `timed*` variants in `subsys/portability/posix/options/rwlock.c` call `get_posix_rwlock(*rwlock)` directly rather than routing through `to_posix_rwlock()`. For an unassociated static rwlock (`*rwlock == -1`), `get_posix_rwlock(-1)` checks bit index `0x7fffffff`, bounds-checks out of range, and returns `NULL`. Every acquisition call unconditionally returns `EINVAL`.
2. **Missing primitive initialization**: `to_posix_rwlock()` allocates a bit from `posix_rwlock_bitarray`, but does not initialize the underlying synchronization members (`sys_sem_init(&rwl->wr_sem, 1, 1)`, `sys_sem_init(&rwl->reader_active, 1, 1)`, `atomic_set(&rwl->rd_count, 0)`, and `rwl->wr_owner = NULL`). These initializations were placed inside `pthread_rwlock_init()`. Any slot returned by `to_posix_rwlock()` has zero-count semaphores and immediately deadlocks upon acquisition.
3. **Concurrency race on lazy binding**: `to_posix_rwlock()` calls `sys_bitarray_alloc()` without holding `posix_rwlock_lock`. If two threads concurrently take an unassociated static rwlock, both allocate separate slots. One thread overwrites `*rwlock`, permanently leaking the other slot and causing threads to operate on disjoint rwlock instances.

This should follow the double-checked locking pattern established in `to_posix_mutex()` (`subsys/portability/posix/options/mutex.c`) and `to_posix_cond()` (`subsys/portability/posix/options/cond.c`).


### Regression

- [ ] This is a regression.

### Steps to reproduce

```
#include <zephyr/ztest.h>
#include <zephyr/posix/pthread.h>

static pthread_rwlock_t static_rwlock = PTHREAD_RWLOCK_INITIALIZER;

ZTEST(posix_rw_locks, test_static_initializer)
{
    /* Returns EINVAL (22) instead of 0 */
    zassert_ok(pthread_rwlock_rdlock(&static_rwlock),
               "pthread_rwlock_rdlock failed on static initializer");
    zassert_ok(pthread_rwlock_unlock(&static_rwlock),
               "pthread_rwlock_unlock failed on static initializer");
}
```

### Relevant log output

```shell
Assertion failed at zephyr/tests/subsys/portability/posix/rwlocks/src/main.c:xx:
pthread_rwlock_rdlock(&static_rwlock) (22 == 0): pthread_rwlock_rdlock failed on static initializer
FAIL - test_static_initializer
```

### Impact

Functional Limitation – Some features not working as expected, but system usable.

### Environment

- OS: Linux / macOS
- Toolchain: Zephyr SDK 0.17.x
- Commit SHA: main (0388ef0c424)


### Additional Context

Related upstream commits & references:
- Commit c250c330c6b ("posix: re-introduce PTHREAD_RWLOCK_INITIALIZER") re-introduced the standard macro for external libraries, but runtime association was omitted.
- Commit 2cfaa251d69 ("posix: mutex: remove global lock from the acquisition fast path") and Issue #119672 / commit 78a38b5b048 ("posix: cond: serialize lazy initialization of static condvars") resolve the identical pattern for mutexes and condition variables.

