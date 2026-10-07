# allocation-size-too-big at H5Centry.c:1018

- URL: https://github.com/HDFGroup/hdf5/issues/5831
- Repo: HDFGroup/hdf5 (language: C)
- State: open; created 2025-09-15T21:30:57Z; status ok; passes main

## Issue body

reporter (NONE) · yangzao · 2025-09-15T21:30:57Z · https://github.com/HDFGroup/hdf5/issues/5831

Hi, I found an allocation-size-too-big bug when testing HDF5 libraries with a fuzzing harness on `x86-64 Ubuntu 22.04`, and it is still reproducible on current commit (`3363183`).

The crash line is the same as #5572 but the stack trace is different.

#### Files:

[1.zip](https://github.com/user-attachments/files/22351623/1.zip)

#### Compiler:
```
Ubuntu clang version 14.0.0-1ubuntu1.1
```
#### Build commands:
```
export CC=clang
export CXX=clang++
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE:STRING=Release -DBUILD_SHARED_LIBS:BOOL=OFF -DBUILD_TESTING:BOOL=ON -DHDF5_BUILD_TOOLS:BOOL=ON -DCMAKE_C_FLAGS="-fsanitize=address -fno-omit-frame-pointer -O1 -g"   -DCMAKE_CXX_FLAGS="-fsanitize=address -fno-omit-frame-pointer -O1 -g"   -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address"   -DCMAKE_SHARED_LINKER_FLAGS="-fsanitize=address"  ..

cmake --build . --config Release

clang -o ./hdf5 ./hdf5.c -fsanitize=address -fno-omit-frame-pointer -O1 -g -I ../src/ -I ../src/H5FDsubfiling -I ./src -L ../src/.libs/ -L ./bin/ -l:libhdf5.a -lz -lm
```


#### Commandline:
```
./hdf5 ./1
```

#### Crash line:
```
    "    1014           if (H5C__verify_len_eoa(f, type, addr, &len, false) < 0)",
    "    1015               HGOTO_ERROR(H5E_CACHE, H5E_BADVALUE, NULL, \"invalid len with respect to EOA\");",
    "    1016   ",
    "    1017       /* Allocate the buffer for reading the on-disk entry image */",
    "--->1018       if (NULL == (image = (uint8_t *)H5MM_malloc(len + H5C_IMAGE_EXTRA_SPACE)))",
    "    1019           HGOTO_ERROR(H5E_CACHE, H5E_CANTALLOC, NULL, \"memory allocation failed for on disk image buffer\");",
    "    1020   #if H5C_DO_MEMORY_SANITY_CHECKS",
    "    1021       H5MM_memcpy(image + len, H5C_IMAGE_SANITY_VALUE, H5C_IMAGE_EXTRA_SPACE);",
    "    1022   #endif /* H5C_DO_MEMORY_SANITY_CHECKS */",
    "    1023   "
```

#### Stacktrace:
```
    "    #0 0x5555557e041e in __interceptor_malloc (hdf5+0x28c41e) (BuildId: bba9551717dcc6a726bcb7141b7bc2e6ca666c47)",
    "    #1 0x555555f429dc in H5C__load_entry hdf_sep15/src/H5Centry.c:1018:37",
    "    #2 0x555555f429dc in H5C_protect hdf_sep15/src/H5Centry.c:3102:30",
    "    #3 0x555555ee9080 in H5AC_protect hdf_sep15/src/H5AC.c:1302:26",
    "    #4 0x555555909c2a in H5HL_protect hdf_sep15/src/H5HL.c:341:40",
    "    #5 0x55555590441e in H5G__stab_valid hdf_sep15/src/H5Gstab.c:998:20",
    "    #6 0x5555558fdb29 in H5G_mkroot hdf_sep15/src/H5Groot.c:235:21",
    "    #7 0x55555583ac89 in H5F_open hdf_sep15/src/H5Fint.c:2139:13",
    "    #8 0x555555e85b1b in H5VL__native_file_open hdf_sep15/src/H5VLnative_file.c:127:9",
    "    #9 0x555555e51d65 in H5VL__file_open hdf_sep15/src/H5VLcallback.c:3714:25",
    "    #10 0x555555e515ba in H5VL_file_open hdf_sep15/src/H5VLcallback.c:3832:30",
    "    #11 0x555555821599 in H5F__open_api_common hdf_sep15/src/H5F.c:780:29",
    "    #12 0x555555820ceb in H5Fopen hdf_sep15/src/H5F.c:820:22",
    "    #13 0x55555581b2f2 in main hdf_sep15/asan_build/./hdf5.c:15:24",
```

Let me know if you need more information!


## Comment 3294112045

maintainer (COLLABORATOR) · jhendersonHDF · 2025-09-15T22:00:42Z · https://github.com/HDFGroup/hdf5/issues/5831#issuecomment-3294112045

It's possible this may be a duplicate of https://github.com/HDFGroup/hdf5/issues/4435

## Comment 3299460326

maintainer (COLLABORATOR) · bmribler · 2025-09-16T16:12:02Z · https://github.com/HDFGroup/hdf5/issues/5831#issuecomment-3299460326

> It's possible this may be a duplicate of [#4435](https://github.com/HDFGroup/hdf5/issues/4435)

And that is the one I used NF's suggestion but got many tests failed.
