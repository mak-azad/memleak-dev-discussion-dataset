# Thread Local Storage refcount leak tracking

- URL: https://github.com/nfs-ganesha/nfs-ganesha/issues/630
- Repo: nfs-ganesha/nfs-ganesha (language: C)
- State: open; created 2020-09-01T14:42:35Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · dang · 2020-09-01T14:42:35Z · https://github.com/nfs-ganesha/nfs-ganesha/issues/630

After #624 merges, we can track normal refcount increments and decrements in a TLS variable, and the result should be 0 at the end of the op.  This can help us track leaks.
