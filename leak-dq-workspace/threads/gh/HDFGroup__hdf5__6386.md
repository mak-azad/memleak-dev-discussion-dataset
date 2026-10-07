# Memory leak in H5O__add_cont_msg when opening corrupted object via H5Rdereference

- URL: https://github.com/HDFGroup/hdf5/issues/6386
- Repo: HDFGroup/hdf5 (language: C)
- State: open; created 2026-04-28T19:06:02Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · tbeu · 2026-04-28T19:06:02Z · https://github.com/HDFGroup/hdf5/issues/6386

When reading corrupted HDF5 files, `H5Rdereference2` can trigger object header deserialization (`H5O__chunk_deserialize`) that allocates continuation message buffers via `H5O__add_cont_msg` / `H5FL_blk_malloc`. If the object header is corrupted, these allocations are not freed, causing a memory leak.

This was found by [OSS-Fuzz](https://github.com/google/oss-fuzz) via the [matio](https://github.com/tbeu/matio) project's fuzzer (ClusterFuzz testcase 6294340632117248).

### LeakSanitizer report

\\\
==411==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 56 byte(s) in 1 object(s) allocated from:
    # 0 __interceptor_malloc
    # 1 H5FL__malloc hdf5/src/H5FL.c:203:30
    # 2 H5FL_blk_malloc hdf5/src/H5FL.c:765:48
    # 3 H5O__add_cont_msg hdf5/src/H5Ocache.c:953:26
    # 4 H5O__chunk_deserialize hdf5/src/H5Ocache.c:1429:21
    # 5 H5O__cache_deserialize hdf5/src/H5Ocache.c:300:9
    # 6 H5C__load_entry hdf5/src/H5Centry.c:1193:26
    # 7 H5C_protect hdf5/src/H5Centry.c:3101:30
    # 8 H5AC_protect hdf5/src/H5AC.c:1276:26
    # 9 H5O_protect hdf5/src/H5Oint.c:987:32
    # 10 H5O__obj_class hdf5/src/H5Oint.c:1647:23
    # 11 H5O_open_by_loc hdf5/src/H5Oint.c:716:30
    # 12 H5O__open_by_addr hdf5/src/H5Oint.c:688:30
    # 13 H5VL__native_object_open hdf5/src/H5VLnative_object.c:112:38
    # 14 H5VL__object_open hdf5/src/H5VLcallback.c:5543:30
    # 15 H5VL_object_open hdf5/src/H5VLcallback.c:5575:30
    # 16 H5Rdereference2 hdf5/src/H5Rdeprec.c:639:31
\\\

The leak occurs because `H5O__add_cont_msg` allocates via `H5FL_SEQ_REALLOC` (line 955) to grow the continuation message array, but when subsequent deserialization of the corrupted object header fails, the error cleanup path does not free this allocation.
