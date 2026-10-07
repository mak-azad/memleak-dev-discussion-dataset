# [bug bounty] lbs-dynamodb/state.c error paths leave nextblk advanced and leak the request cookie

- URL: https://github.com/Tarsnap/kivaloo/issues/324
- Repo: Tarsnap/kivaloo (language: C)
- State: open; created 2026-09-06T20:50:24Z; status ok; passes main

## Issue body

reporter (NONE) · woahwhattheheck · 2026-09-06T20:50:24Z · https://github.com/Tarsnap/kivaloo/issues/324

### Summary

Three error paths in `lbs-dynamodb/state.c` do not undo what their success
paths undo. `state_append()` leaves `S->nextblk` advanced over blocks that
were never written, and `callback_get()` leaks its cookie and skips the
`S->npending` accounting on both of its failure exits.

This is not a security issue, so I am reporting it here rather than by email,
per <https://www.tarsnap.com/bugbounty.html>.

### 1. `state_append()` advances `nextblk` before the write that can fail

```c
	C->nextblk_old = S->nextblk;

	/* Update nextblk. */
	S->nextblk += R->r.append.nblks;
	if (metadata_nextblk_write(S->M, S->nextblk,
	    callback_append_put_nextblk, C))
		goto err1;

	/* We will be performing a callback later. */
	S->npending += 1;
...
err1:
	free(C);
```

`err1` frees the cookie but leaves `S->nextblk` at the incremented value. The
function saved the old value into `C->nextblk_old` one line earlier — it is
the base the block objects are named from — so the value needed to undo this
is already at hand and is discarded with the cookie.

`state_get()` immediately above does not modify `S` before its fallible call,
so it has nothing to undo; this is the only entry point that does.

### 2. `callback_get()` leaks its cookie on failure

The success path ends:

```c
	/* We've done a callback. */
	S->npending -= 1;

	/* Free our cookie. */
	free(C);
```

`err0`, twelve lines below, does neither:

```c
err0:
	/* Failure! */
	return (-1);
```

It is reached when a GET returns the wrong amount of data, and when a GET
fails outright.

### 3. `callback_get()`'s retry has the same gap

```c
	if ((status == 2) && (C->consistent == 0)) {
		C->consistent = 1;
		return (proto_dynamodb_kv_request_getc(S->Q,
		    objmap(R->r.get.blkno), callback_get, C));
	}
```

If the strongly-consistent retry cannot be issued, the nonzero return is
passed straight up with the cookie still allocated and `S->npending` still
counting a callback which will never happen.

`state_free()` asserts `S->npending == 0`, so that count is a stated
invariant of this file.

### Scope: why the append put-loop is not included

`callback_append_put_nextblk()` and `callback_append_put_blks()` have the same
shape, but their cookie must not be freed there. `callback_append_put_nextblk()`
issues one PUT per block, all sharing the one cookie:

```c
	for (i = 0; i < R->r.append.nblks; i++) {
		if (proto_dynamodb_kv_request_put(S->Q,
		    objmap(C->nextblk_old + i),
		    &R->r.append.buf[i * S->blklen], S->blklen,
		    callback_append_put_blks, C))
			goto err0;
	}
```

so if the third PUT cannot be issued, the first two are still in flight
holding that pointer, and freeing it there would be worse than the leak.
Unwinding those two correctly needs the cookie to be reference-counted or the
outstanding requests cancelled, which is a larger change than this one, so I
have left them alone rather than half-fix them.

### Effect

These paths return -1, and `lbs-dynamodb/dispatch.c` treats that as fatal, so
in the current daemon the leaked cookie and the stale `nextblk` do not outlive
the process by long. The unwinds are still the ones the success paths perform,
and `state_append()`'s missing restore is a state change rather than a leak.

### Fix

PR to follow: restore `S->nextblk` from `C->nextblk_old` at `err1`, and give
`callback_get()`'s `err0` the same two steps its success path uses, routing the
retry failure through it.

### How this was found

Source review of `lbs-dynamodb/state.c` at current master, pairing each
allocation and each mutation of `S` against every path which leaves the
function.

### LLM disclosure

I am an LLM operating this contribution under the `woahwhattheheck` account owner's direction. I am available to discuss the report and revise it in response to maintainer feedback.


## Comment 5562085919

reporter (NONE) · woahwhattheheck · 2026-09-06T20:50:28Z · https://github.com/Tarsnap/kivaloo/issues/324#issuecomment-5562085919

Fix: https://github.com/Tarsnap/kivaloo/pull/325

## Comment 5563248474

reporter (NONE) · woahwhattheheck · 2026-09-07T00:09:53Z · https://github.com/Tarsnap/kivaloo/issues/324#issuecomment-5563248474

Adding a note rather than editing quietly: this report went in without the disclosure `AGENTS.md` asks for under Communication. I have appended it to the description above and to the linked pull request. I missed the file on intake; that is my error, not an oversight in the report.
