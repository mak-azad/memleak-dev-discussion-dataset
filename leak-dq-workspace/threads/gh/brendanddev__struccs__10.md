# fix: ll_copy leaks Node + value buffer for every element copied

- URL: https://github.com/brendanddev/struccs/issues/10
- Repo: brendanddev/struccs (language: C)
- State: open; created 2026-09-15T23:04:06Z; status ok; passes main

## Issue body

reporter (OWNER) · brendanddev · 2026-09-15T23:04:06Z · https://github.com/brendanddev/struccs/issues/10

The issue is with the `LinkedList` struct, specifically when it copies via `ll_copy`, which allocates a temporary `Node` via `ll_create_node`, then passes its value into `ll_insert_tail`, which makes its own independent heap copy internally. The temporary node returned by `ll_create_node` is never linked into the copied list and never freed, so it leaks on every iteration of the copy loop.

### Location

`src/linked_list.c`, `ll_copy`:

```c
struct LinkedList* ll_copy(struct LinkedList *orig) {
    struct LinkedList *copy = ll_create();

    for (struct Node *current = orig->head; current != NULL; current = current->next) {
        struct Node *cnode = ll_create_node(current->value, current->item_size);
        ll_insert_tail(copy, cnode->value, cnode->item_size);
        // cnode and its value buffer are never freed or linked in
    }
    return copy;
}
```

### Proof (Valgrind, CI run on ubuntu-latest)

Caught by `test_linkedlist_copy`, which copies a 3-node list:
```
==3879== HEAP SUMMARY:
==3879== in use at exit: 108 bytes in 6 blocks
==3879== total heap usage: 2,123 allocs, 2,117 frees, 42,452 bytes allocated

==3879== 12 bytes in 3 blocks are indirectly lost in loss record 1 of 2
==3879== at 0x4846828: malloc
==3879== by 0x1092F6: ll_create_node
==3879== by 0x109CCF: ll_copy
==3879== by 0x10B9A6: test_linkedlist_copy
==3879== by 0x10A340: main

==3879== 108 (96 direct, 12 indirect) bytes in 3 blocks are definitely lost in loss record 2 of 2
==3879== at 0x4846828: malloc
==3879== by 0x1092A9: ll_create_node
==3879== by 0x109CCF: ll_copy
==3879== by 0x10B9A6: test_linkedlist_copy
==3879== by 0x10A340: main

==3879== LEAK SUMMARY:
==3879== definitely lost: 96 bytes in 3 blocks
==3879== indirectly lost: 12 bytes in 3 blocks
==3879== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```

3 leaked `Node` structs (definitely lost) plus 3 leaked value buffers (indirectly lost), matching the 3 elements inserted by the test.

