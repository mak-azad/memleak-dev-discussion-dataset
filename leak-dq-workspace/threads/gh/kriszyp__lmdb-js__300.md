# Valgrind warnings

- URL: https://github.com/kriszyp/lmdb-js/issues/300
- Repo: kriszyp/lmdb-js (language: JavaScript)
- State: open; created 2024-08-12T00:14:44Z; status ok; passes main

## Issue body

reporter (NONE) · yamadapc · 2024-08-12T00:14:44Z · https://github.com/kriszyp/lmdb-js/issues/300

Running a few tests under valgrind produces the following warnings:

## Conditional jump or move depends on uninitialised value(s)

https://github.com/kriszyp/lmdb-js/blob/89032ed79729c66b175aba1f6ae4366ca9a8f198/src/lmdb-js.h#L354

`lastReaderCheck` has no initialization ; I reckon what it is initialized with is undefined behaviour.

## Mismatched free / delete / delete[]

Warning about free call on:
https://github.com/kriszyp/lmdb-js/blob/89032ed79729c66b175aba1f6ae4366ca9a8f198/src/lmdb-js.h#L320

`openEnvWraps` is a vector allocated with `new` on https://github.com/kriszyp/lmdb-js/blob/89032ed79729c66b175aba1f6ae4366ca9a8f198/src/env.cpp#L390

`free` won't call the destructor so I think this is leaking memory as the vector internals won't be released.
