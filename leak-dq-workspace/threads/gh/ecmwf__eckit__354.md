# eckitlib wheel: process aborts at exit ("free(): invalid pointer") when eccodes is imported before pyproj

- URL: https://github.com/ecmwf/eckit/issues/354
- Repo: ecmwf/eckit (language: C++)
- State: open; created 2026-09-28T03:38:49Z; status ok; passes main

## Issue body

reporter (NONE) · jakeryderv · 2026-09-28T03:38:49Z · https://github.com/ecmwf/eckit/issues/354

On Linux x86_64, a process that imports `eccodes` (with the `eccodeslib`/`eckitlib` wheels) and then `pyproj` aborts at interpreter exit with SIGABRT. The reverse import order exits cleanly.

### Reproduce

In a fresh virtual environment:

```sh
pip install eccodes eccodeslib pyproj
python -c "import eccodes; import pyproj"   # free(): invalid pointer / munmap_chunk(): invalid pointer; exit 134
python -c "import pyproj; import eccodes"   # exit 0
```

No GRIB decoding or PROJ call is needed. The abort happens during process teardown, after all Python code has finished.

### Environment

- Linux 7.1 x86_64, glibc 2.39
- CPython 3.14.7 and 3.12.12 (both reproduce)
- eccodes 2.48.0, eccodeslib 2.49.0.30, eckitlib 2.3.0.30. eccodeslib 2.48.3.28 with eckitlib 2.3.0.28 also reproduces.
- pyproj 3.8.0 (PROJ 9.8.1)

### What appears to happen

- Both wheels bundle their own copy of PROJ: `eckitlib.libs/libproj-*.so.25.9.8.1` and `pyproj.libs/libproj-*.so.25.9.8.1`.
- `python/eckitlib/buildconfig` builds with `-DENABLE_PROJ=1`.
- `pre-compile.sh` already takes care not to leak `PROJ_DATA` into the process "which would interfere with pyproj". But the bundled `libproj` itself also coexists with pyproj's copy in one process.
- When eckitlib's copy is loaded first, teardown frees memory that the other copy owns.
- The two wheels also both bundle `libcurl`, `libsqlite3` and `libnghttp2`, which may be involved.

### Impact

Any Python stack that reads GRIB through eccodes and also uses pyproj (directly, or via xradar, cartopy, geopandas, and so on) exits with status 134. That fails CI jobs and scripts even though the work succeeded.

### Workaround

Import `pyproj` before `eccodes`.

### Possible fixes

- Build eckitlib's PROJ with hidden symbol visibility, or link it statically with symbols not exported, so it can't clash with another copy.
- Or offer an eckitlib wheel variant without PROJ, for users who don't need `eckit_geo`'s projections.


## Comment 5956070323

other (NONE) · xavierabellan · 2026-10-02T15:51:39Z · https://github.com/ecmwf/eckit/issues/354#issuecomment-5956070323

Just for reference, a user reported this issue on JIRA too: https://jira.ecmwf.int/browse/SD-130570
