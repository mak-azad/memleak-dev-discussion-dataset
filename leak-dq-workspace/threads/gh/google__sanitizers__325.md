# Leak of size 0 reported as leak of size 1

- URL: https://github.com/google/sanitizers/issues/325
- Repo: google/sanitizers (language: C)
- State: open; created 2015-09-01T00:36:27Z; status ok; passes main

## Issue body

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:36:27Z · https://github.com/google/sanitizers/issues/325

Originally reported on Google Code with ID 325

```
#include <stdlib.h>

int main() {
  void * volatile p = malloc(0);
  return 0;
}

ERROR: LeakSanitizer: detected memory leaks

Direct leak of 1 byte(s) in 1 object(s) allocated from:

This is confusing and may lead debugging down the wrong path.

```

Reported by `eugenis@google.com` on 2014-07-17 08:32:33


## Comment 136537504

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:36:35Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537504

```
This is because malloc(0) actually allocates 1 byte in ASan. The allocator doesn't support
0-byte allocations. Alas we don't have the luxury of an extra metadata bit to distinguish
between 0 and 1 byte blocks.
```

Reported by `earthdok@chromium.org` on 2014-07-17 08:52:24


## Comment 136537517

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:36:44Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537517

```
It's somewhat tempting to mark this as wontfix :) Is there an example of real-world
problem it causes? Even if it is reported as a leak, LSan should provide an allocation
stack trace, so debugging this shouldn't be that hard.
```

Reported by `samsonov@google.com` on 2014-07-17 18:23:07


## Comment 136537530

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:36:52Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537530

```
Isn't it perfectly fine to allocate non-zero amount of memory for malloc(0)? This could
indeed result in a leak in real program.
```

Reported by `tetra2005` on 2014-07-17 19:48:57


## Comment 136537545

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:37:01Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537545

```
See discussion for commit r213120 in cfe ml.
Thinking that allocation size is 1 rather then 0 actually leads report investigation
down the wrong path.

And yes, this could totally be a real memory leak.
```

Reported by `eugenis@google.com` on 2014-07-17 19:51:29


## Comment 136537556

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:37:10Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537556

```
What we could do is have the user_requested_size metadata field always contain the actual
requested size (possibly 0), and have two accessors (one returns user_requested_size
for use in reports, the other returns max(user_requested_size, 1) for internal use).
We just need to go through the code carefully and separate the two use cases.
```

Reported by `earthdok@chromium.org` on 2014-07-18 08:35:15


## Comment 136537572

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:37:18Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537572

Reported by `ramosian.glider` on 2015-07-30 09:05:33
- **Labels added**: ProjectAddressSanitizer


## Comment 136537594

reporter (MEMBER) · ramosian-glider · 2015-09-01T00:37:27Z · https://github.com/google/sanitizers/issues/325#issuecomment-136537594

```
Adding Project:AddressSanitizer as part of GitHub migration.
```

Reported by `ramosian.glider` on 2015-07-30 09:06:57

