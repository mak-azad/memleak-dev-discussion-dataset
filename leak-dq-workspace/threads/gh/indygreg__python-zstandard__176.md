# Implement `max_length` argument on `ZstdDecompressionObj::decompress()`

- URL: https://github.com/indygreg/python-zstandard/issues/176
- Repo: indygreg/python-zstandard (language: C)
- State: open; created 2022-06-20T19:26:44Z; status ok; passes main

## Issue body

reporter (OWNER) · indygreg · 2022-06-20T19:26:44Z · https://github.com/indygreg/python-zstandard/issues/176

Python 3.6 added an optional `max_length` argument on decompressor's `decompress()` method. e.g. https://docs.python.org/3/library/zlib.html#zlib.Decompress.decompress.

This argument can reduce a lot of (but not all) of the performance badness in the API design of `decompress()` by allowing implementations to allocate a single output buffer of size `max_length` to avoid excessive memory allocations/copies.

We should support this optional argument.
