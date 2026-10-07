# File descriptor leak for mmaped files

- URL: https://github.com/containers/fuse-overlayfs/issues/378
- Repo: containers/fuse-overlayfs (language: Rust)
- State: open; created 2022-10-20T18:27:45Z; status ok; passes offcwe

## Issue body

reporter (NONE) · jpalus · 2022-10-20T18:27:45Z · https://github.com/containers/fuse-overlayfs/issues/378

I'm running rootless `podman` container backed by `fuse-overlayfs` within which I'm running process opening many files one by one, each being `mmap()`ed and immediately `close()`d but all `mmap()` are kept (to be specific that's linking https://github.com/rui314/mold/issues/797). Now it all works fine within host system or in `podman` container with `overlay` driver (which I unfortunately cannot use in this particular case) or when files are not `mmap()`ed, but scenario fails with `fuse-overlayfs` due to `-EMFILE (Too many open files)`. It appears that `mmap()` on file results in file descriptor being kept by `fuse-overlayfs` process even though file is `close()`d afterwards.

Is this something that can be avoided or is it perhaps shortcoming of `fuse` filesystems?
