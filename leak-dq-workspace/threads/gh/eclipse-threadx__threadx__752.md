# ThreadX SMP Linux port deadlocks on a lost mutex wake-up, and the regression suite hangs because of it

- URL: https://github.com/eclipse-threadx/threadx/issues/752
- Repo: eclipse-threadx/threadx (language: C)
- State: open; created 2026-09-18T02:44:12Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · fdesbiens · 2026-09-18T02:44:12Z · https://github.com/eclipse-threadx/threadx/issues/752

The ThreadX SMP regression suite hangs intermittently on the Linux simulation port. Measured with ctest's retry disabled, 17.8% of local configuration-runs and 3.6% of hosted-runner ones were not green on the first attempt, across twelve distinct tests. Six of them hang and are killed at the ctest timeout; the rest fail assertions for unrelated reasons. `--repeat until-pass:2` is the only reason the suite has been reporting 108/108.

The hang is a deadlock in `ports_smp/linux/gnu`, not in `common_smp/src`. Four hung processes were captured untraced, across three tests, and all four show the same state:

- a ThreadX thread in `sigsuspend()` inside `_tx_linux_thread_suspend_handler`, sitting on top of `pthread_mutex_lock` inside `_tx_linux_mutex_obtain`, reached from `_tx_thread_smp_protect`;
- the scheduler thread blocked in `pthread_mutex_lock` at `_tx_thread_schedule`;
- `_tx_linux_mutex` reading `__lock = 0, __owner = 0, __nusers = 0`, `tx_linux_mutex_owner = 0`, `tx_linux_mutex_nested_count = 0` — free, with waiters on it;
- the protection held by the port's timer thread, which is waiting on `_tx_linux_isr_semaphore` for a scheduler pass that cannot happen;
- no progress over a ten second control sample, with the simulated clock frozen.

The cause is a lost futex wake-up. The port's suspend handler calls `sigsuspend()` and does not return until the thread is resumed, and the signal can arrive while the thread is parked on `_tx_linux_mutex`. glibc waits for a contended mutex in a loop that re-arms the futex wait after a signal; this handler never returns to that loop. The next release hands its wake-up to the suspended thread, which will not act on it, and every other thread parked on the mutex stays in `futex_wait` on a word that will not change again. On this port that deadlocks the process rather than merely delaying it, because the only thread that can resume the suspended one is the scheduler and the scheduler takes this mutex on every pass.

The port already contains the guard that was meant to prevent this. `_tx_linux_mutex_obtain` sets `tx_thread_linux_mutex_access` immediately before the lock call and clears it immediately after, and in every capture the flag is set on precisely the thread that got suspended. Nothing in the tree reads it: three writes, no reads, the only other mention being its initialisation to `TX_FALSE` in `tx_thread_stack_build.c`.

Reading the flag in `_tx_linux_thread_suspend` and skipping the signal does not work, because every caller of that function holds the mutex, so a thread queued on it cannot make progress while the suspender waits for the handshake. Blocking the suspend signal around the lock call has the same problem. What does work is re-arming the wait: see the pull request below.

The monoprocessor Linux port looks to have the same defect latent in it. `ports/linux/gnu` takes its critical section with a plain `pthread_mutex_lock` through `tx_linux_mutex_lock` and its suspend handler is the same `sigsuspend` that does not return. It has not been observed — the ThreadX suite recorded no first-attempt failures over 105 configuration-runs and 8,640 further test executions — which is consistent with one emulated core and far less suspend and resume traffic rather than with the code being different.


## Comment 5724940416

reporter (CONTRIBUTOR) · fdesbiens · 2026-09-18T03:59:06Z · https://github.com/eclipse-threadx/threadx/issues/752#issuecomment-5724940416

Follow-up, with the first measurement of the fix in #753 against the whole suite rather than one test standalone.

The change closes the mechanism described above and is measurable on its own: standalone, `threadx_smp_random_resume_suspend_exclusion_test` went from 3 hangs in 100 runs and 2 in 55 to **0 in 400**. It does not close the intermittency of the suite. Running the eight build configurations as CI runs them, serially and with ctest's retry disabled, there were **3 timeouts in 54 configuration-runs** after the change, against 6 in 90 before it — in three different tests and three different build configurations, and one more on a hosted runner in `threadx_thread_relinquish_test`.

So there are at least two defects in this emulation, which is what the captures already suggested. The state in the suite-context hangs is not the state this fix addresses:

- `_tx_linux_mutex` is free and nobody is waiting on it;
- `_tx_thread_smp_protection` is not held;
- the scheduler thread is idling in its own two millisecond `sem_timedwait` rather than blocked on the lock, so it wakes, walks the four virtual cores and does nothing;
- `_tx_thread_current_ptr` is null on every core while `_tx_thread_execute_ptr[0]` holds a runnable thread with `tx_thread_linux_suspension_type` of 2 that is waiting on its run semaphore and is never picked up;
- in one capture `_tx_thread_smp_schedule_list` disagrees with both `_tx_thread_current_ptr` and `_tx_thread_execute_ptr`: a schedule was computed and never acted on.

That is a lost wake-up between `_tx_thread_system_return`, `_tx_thread_schedule` and `_tx_thread_context_restore` rather than a lost futex wake-up on the mutex, and `tx_thread_smp_core_control` is the field to read at the moment of the hang: the scheduler skips a core whose `_tx_thread_execute_ptr` entry has it clear, and nothing but the scheduler sets it. It is still being characterised and is not fixed by #753.

Worth recording for anyone reading a capture of this port: the port's globals are defined twice in the test build — once in the library from `ports_smp/linux/gnu/src/tx_initialize_low_level.c` and once in the copy the harness generates into the test tree — and ELF interposition makes the second the live one. A plain `print _tx_linux_mutex` in gdb may resolve either.


## Comment 5733311046

reporter (CONTRIBUTOR) · fdesbiens · 2026-09-18T16:56:10Z · https://github.com/eclipse-threadx/threadx/issues/752#issuecomment-5733311046

Correcting my own follow-up above, now that the capture it asked for exists.

**`tx_thread_smp_core_control` was not the deciding field.** It reads 1 on the waiting execute-pointer thread in every capture taken since, so the scheduler was entitled to pick that thread up and the reason it did not lies elsewhere. My description of the field was also inverted: `_tx_thread_schedule` is the only place that **clears** it, and the paths that take a thread off a core are what **set** it.

**"A schedule was computed and never acted on" does not follow, and I withdraw it.** `_tx_thread_smp_schedule_list` is scratch for the rebalance path — `_tx_thread_smp_rebalance_execute_list` rebuilds it and `_tx_thread_smp_execute_list_setup` copies it into `_tx_thread_execute_ptr` — but `tx_thread_system_resume.c` and `tx_thread_system_suspend.c` both assign `_tx_thread_execute_ptr[i]` directly in their simple paths without touching it. The two disagree routinely, including on a healthy process: a snapshot of a passing run showed the schedule list holding four threads that had already been deleted. A disagreement between those two arrays carries no information about a hang.

**What the suite-context hangs actually are: two further defects, neither of them the one this issue reports.**

The first is in this port: #757, fixed by #759. `_tx_thread_smp_unprotect` takes `_tx_linux_mutex` on entry and releases it twice when the protection names the calling core but only once when it does not, while the matching `_tx_thread_smp_protect` took it once either way. On the timer interrupt thread the leaked nesting level is never drained, so `pthread_mutex_unlock` is never called again and everything waits on a mutex that is held while the tick keeps arriving. Two captures, identical in every participant.

The second is not in the port at all. `_tx_thread_relinquish` in `common_smp/src` sets its `rebalance` flag when the ready-list walk meets a thread it cannot place, then falls into the block that concludes no other thread is ready and sets `finished = TX_TRUE`, which is the flag guarding the rebalance at the end of the function. The rebalance it asked for never runs, and a ready thread behind the obstacle never reaches a core. It is #756, fixed by #758.

So the state I described in that follow-up — mutex free, protection not held, scheduler idling in its two millisecond wait, a runnable thread never picked up — is the second of those, and it is a scheduler defect rather than a port one. The fix in #753 remains correct for the mechanism this issue reports; it was never going to close the rest, and I was wrong to imply the remaining evidence pointed at this port.
