# pool: free-list index assertion fires in pool_free — bad or corrupted entry header reaches the allocator

- URL: https://github.com/n00b-lang/n00b/issues/228
- Repo: n00b-lang/n00b (language: C)
- State: open; created 2026-08-27T20:34:14Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · meisenbarth · 2026-08-27T20:34:14Z · https://github.com/n00b-lang/n00b/issues/228

Found while revalidating #185 against `cf3bcab1`. Single occurrence, live gateway, ~1 hour before filing.

## The crash

```
2026-08-27T20:24:23.894Z
Assertion failed: (entry->list_index <= N00B_NUM_FREE_LISTS),
                  function pool_free, file pool.c, line 1348.
n00b: fatal: trap
n00b: crash sig=5   thread id=21  os_tid=9475
```

Host: macOS arm64, installed `crayon-gw` 0.8.44 build 1787796476. The gateway relaunched and has been healthy since (canary 237 → 238, one relaunch, no loop).

## Mechanism

`src/core/pool.c:1346-1348`:

```c
n00b_pool_entry_t *entry = (n00b_pool_entry_t *)((char *)ptr - N00B_ALIGN);
assert(entry->list_index <= N00B_NUM_FREE_LISTS);
```

`N00B_NUM_FREE_LISTS` is 8 (`include/core/pool.h:17`). The assertion reads the 32 bytes preceding `ptr` as a pool entry header and requires `list_index <= 8`. It failed, so one of:

- a pointer that is not a pool allocation was passed to `pool_free`
- a double free, where the header had already been reused
- the entry header was overwritten by an out-of-bounds write to the preceding allocation

The assertion is doing its job — this is a controlled abort, not silent corruption. That is worth stating plainly: the allocator caught a bad free instead of propagating it.

## Grade: P1, not P0

Against `crashappsec/wax` `docs/priority-levels.md` (rev 2), Edge cases → Inherited severity:

- **Half (1) — named downstream blocked in a shipping path:** partially. `crayon-gw` crashed, but launchd relaunched it once and it recovered. One transient fault with automatic recovery is not "blocked."
- **Half (2) — reproduces inside the library boundary:** **fails.** One occurrence, no repro, no test.

Same test that moved #217 and #221 to P1 today. Carrying `needs-repro` for consistency with that pass.

## What would move it

Any second occurrence, or an in-library test that drives a double free or a foreign pointer into `pool_free`. If it turns out to be reachable on the default path rather than a one-off, half (1) strengthens and this is a Gate 1 candidate — a bad free in the allocator is memory-unsafety, and the assertion only covers builds that keep it enabled.

## Related, not asserted as the same defect

Thread 21 here; #217/#218 are the dict reader path and the 2026-08-27 crash loop was thread 13 on the registry load path. **No shared mechanism is being claimed** — treating stale-pointer or bad-free *shape* as evidence of common cause is the error that cost the `wax#669` investigation a day.

The dump for this crash is itself interleaved mid-token (`fault_addr=` doubled, `overflow= overflow=00`), which is #185 reproducing live and is why the frame list could not be recovered.

## Comment 5681916206

reporter (COLLABORATOR) · meisenbarth · 2026-09-15T14:25:38Z · https://github.com/n00b-lang/n00b/issues/228#issuecomment-5681916206

## Second occurrence, with the caller this issue was missing

crashappsec/wax#992 reports the same assertion on a different host and a much later build. This is the "any second occurrence" that this issue says would move it off `needs-repro`.

```
2026-09-14T18:11:22.234Z
Assertion failed: (entry->list_index <= N00B_NUM_FREE_LISTS),
                  function pool_free, file pool.c, line 1404.
n00b: fatal: aborted
n00b: crash sig=6 si_code=0 sender_pid=19168
```

macOS arm64, installed `crayon-gw` **0.8.55 build 1789356761** (first report was 0.8.44 / 1787796476). Line number moved 1348 → 1404; same function, same assertion. Recovered by relaunch, as before.

### The stack, which the first report did not have

Symbolized against the shipped release binary — the pkg's `crayon-gw` carries exactly the crash's UUID `8F15693E-0CA5-305D-9740-BC587608A945`, so this is authoritative:

```
pool_free                            +2908
n00b_free_storage_from_allocator     +516
n00b_free                            +1292
rocs_store_batch_term_append_unique  +652     <- the free
rocs_store_append_key_visitor        +180
rocs_norm_visit_string_key           +372
n00b_store_normalize_text_token_keys +1132
rocs_store_append_text_keys          +432
rocs_store_append_default_search_text +752
rocs_store_collect_search_text       +1716
rocs_store_collect_search_text       +924     <- recursive descent
rocs_store_build_batch_terms         +2184
rocs_store_batch_prepare_job         +304
```

So the bad free is reached from **ROCS batch term preparation**, on the ingest conduit thread: `rocs_store_batch_term_append_unique` releasing storage while de-duplicating search-index terms for a record. That narrows your three candidate mechanisms to whatever that function frees — a duplicate-term path that frees a token it does not own, frees twice, or writes past a token buffer and lands on the next entry's header.

Worth knowing: that exact call path is the one crashappsec/wax#366 profiles as saturating a core in tokenization, and six of the seven shared frame offsets there are identical to these, on a 0.8.17 sample. The path is unchanged across 38 releases and is under continuous heavy load in the field, which is a plausible reason a rare bad free surfaces here rather than anywhere else.

### On grading

Not asserting a new grade — that is yours. But flagging what changed against the two halves in the issue body: this is no longer a single occurrence, and the caller is now named. The gateway still recovered by relaunch on both occasions, so half (1) is unchanged.

No repro and no in-library test yet, so the mechanism remains one of the three you listed.

