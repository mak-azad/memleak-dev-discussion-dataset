# Client socket leaked in parent process

- URL: https://github.com/tedjp/ish/issues/1
- Repo: tedjp/ish (language: C)
- State: open; created 2018-10-11T23:23:29Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · tedjp · 2018-10-11T23:23:29Z · https://github.com/tedjp/ish/issues/1

The accepted socket is never closed in the parent process. The parent process will eventually run out of file handles.

## Comment 429969904

reporter (OWNER) · tedjp · 2018-10-15T18:46:17Z · https://github.com/tedjp/ish/issues/1#issuecomment-429969904

This might be easier to approach on the [min branch](https://github.com/tedjp/ish/tree/min), which I'm considering merging into `master`. Or it could be solved on both.
