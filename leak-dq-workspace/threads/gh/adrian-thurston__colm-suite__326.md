# colm: exit inside a loop over a user iterator leaks the iterator's locals

- URL: https://github.com/adrian-thurston/colm-suite/issues/326
- Repo: adrian-thurston/colm-suite (language: C++)
- State: open; created 2026-09-30T23:30:22Z; status ok; passes main

## Issue body

reporter (OWNER) · adrian-thurston · 2026-09-30T23:30:22Z · https://github.com/adrian-thurston/colm-suite/issues/326

<!-- colm-issues-followup pr=315 -->
`test/colm.d/exit6.lm` passes, but it loses one string tree and one head. The harness can't see that (#310). Minimal repro on main at bd7aa2a0:

```
iter i()
{
	S: str = "1"
	yield S
}

for T: any in i() {
	exit( 3 )
}
```

A `-DDEBUG` runtime prints `lost trees: 1` and `lost heads: 1`. A `-DPOOL_MALLOC` runtime under `valgrind --leak-check=full` reports 64 bytes definitely lost, allocated by `construct_string` from `IN_LOAD_STR` (`bytecode.c:844`). That is the iterator's local `S`. When `exit` interrupts the loop, nothing on its path seems to destroy the suspended iterator: neither the `FN_EXIT` unwind (`bytecode.c:4662`) nor the root frame's `downref_locals` in `colm_execute` (`bytecode.c:598`). I haven't traced which step should. Suggested fix: have `exit`'s path destroy any live iterators in the frames it leaves, including the root frame. Then add a DEBUG or valgrind check for `exit6` once #310 gives the harness one.

Found while reviewing #315.

