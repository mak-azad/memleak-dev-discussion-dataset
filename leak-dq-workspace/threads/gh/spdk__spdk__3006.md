# [lvol] questionable lvol_free() in lvol_close_blob_cb() error path

- URL: https://github.com/spdk/spdk/issues/3006
- Repo: spdk/spdk (language: C)
- State: open; created 2023-04-28T21:45:53Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · mgerdts · 2023-04-28T21:45:53Z · https://github.com/spdk/spdk/issues/3006

# Sighting report

While fixing #2998, I noticed a suspicious `lvol_free()` when `lvol_close_blob_cb()` is called with an error.   At this point, `lvol` is still in `lvol->lvol_store->lvols` (or one of the other tailqs declared nearby) and may be referenced by an `spdk_lvs_degraded_lvol_set`.  It is not safe to just free it.

```c
static void
lvol_close_blob_cb(void *cb_arg, int lvolerrno)
{
        struct spdk_lvol_req *req = cb_arg;
        struct spdk_lvol *lvol = req->lvol;

        if (lvolerrno < 0) {
                SPDK_ERRLOG("Could not close blob on lvol\n");
                lvol_free(lvol);
                goto end;
        }
 ...
end:
        req->cb_fn(req->cb_arg, lvolerrno);
        free(req);
}
```

When fixing this, we should figure out what to do about `lvol->blob` (the fix for #2998 may be setting this to NULL).  In the error path, we have no information as to whether `blob->open_ref` is still incremented on behalf of this lvol.  It seem `spdk_blob_close()` needs to communicate this better.

## Expected Behavior

Memory with references that may be used must not be freed.

## Current Behavior

The error path sets us up for a use after free bug later.

## Context (Environment including OS version, SPDK version, etc.)

Observed with spdk master at commit ca0c4dcde8dda4144b8b0fd30badd1b4ffae5bf3.
