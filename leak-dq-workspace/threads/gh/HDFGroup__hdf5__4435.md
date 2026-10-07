# allocation-size-too-big error in H5Centry.c

- URL: https://github.com/HDFGroup/hdf5/issues/4435
- Repo: HDFGroup/hdf5 (language: C)
- State: open; created 2024-04-21T16:54:56Z; status ok; passes main

## Issue body

reporter (NONE) · gabe-sherman · 2024-04-21T16:54:56Z · https://github.com/HDFGroup/hdf5/issues/4435

An allocation-size-too-big error occurs in the h5dump program when provided with a malformed input. This behavior occurs at line 1015 in H5Centry.c.
### How to trigger

```LD_PRELOAD=path-to/libhdf5.so h5dump poc```

### POC File
https://github.com/FuturesLab/POC/blob/main/hdf5/poc-10

### Test Environment

Ubuntu 22.04, 64bit
### Version

Latest: 0394b03f66dc45fe96e2c772b7bce293e4316ad2

### Address Sanitizer Output
```
=================================================================
==1440597==ERROR: AddressSanitizer: requested allocation size 0x101010101010158 (0x101010101011158 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000 (thread T0)
    #0 0x5555565cc45e in __interceptor_malloc (/home/gabesherman/harness_test/AutoHarn-Results/hdf5/autoharn-10/harness+0x107845e) (BuildId: 18a7c9ab4a9a69531af3cb99c442f42c242e1103)
    #1 0x55555711b265 in H5C__load_entry /home/gabesherman/harness_test/AutoHarn-Evaluation/hdf5/lib_asan/src/H5Centry.c:1017:37
    #2 0x55555711b265 in H5C_protect /home/gabesherman/harness_test/AutoHarn-Evaluation/hdf5/lib_asan/src/H5Centry.c:3101:30
    #3 0x555556f79dc2 in H5AC_protect /home/gabesherman/harness_test/AutoHarn-Evaluation/hdf5/lib_asan/src/H5AC.c:1276:26

==1440597==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big (/home/gabesherman/harness_test/AutoHarn-Results/hdf5/autoharn-10/harness+0x107845e) (BuildId: 18a7c9ab4a9a69531af3cb99c442f42c242e1103) in __interceptor_malloc
==1440597==ABORTING
```

## Comment 2073496668

reporter (NONE) · gabe-sherman · 2024-04-23T21:34:40Z · https://github.com/HDFGroup/hdf5/issues/4435#issuecomment-2073496668

This is the harness that this crash was discovered with:
```
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdlib.h>
#include <hdf5.h>

int main(int argc, char *argv[])
{
   char *fuzzData = argv[1];

   char H5Gcreate1var0[256];
	sprintf(H5Gcreate1var0, "yhoom");
   char H5Gcreate2var0[256];
	sprintf(H5Gcreate2var0, "7td9h");
   hid_t H5Fopenval1 = H5Fopen(fuzzData, 1, 0);
	if(strcmp(argv[1], fuzzData)){
		fprintf(stderr, "err");
	}
	if(H5Fopenval1 < 0){
		fprintf(stderr, "err");
	}
   hid_t H5Gcreate1val1 = H5Gcreate1(H5Fopenval1, H5Gcreate1var0, 1);
	if(strcmp(argv[1], fuzzData)){
		fprintf(stderr, "err");
	}
	if(H5Gcreate1val1 < 0){
		fprintf(stderr, "err");
	}
   hid_t H5Gcreate2val1 = H5Gcreate2(H5Gcreate1val1, H5Gcreate2var0, 0, 0, 0);
	if(strcmp(argv[1], fuzzData)){
		fprintf(stderr, "err");
	}
	if(H5Gcreate2val1 < 0){
		fprintf(stderr, "err");
	}
   return 0;
}

```

## Comment 5008854962

maintainer (MEMBER) · gheber · 2026-07-18T00:38:22Z · https://github.com/HDFGroup/hdf5/issues/4435#issuecomment-5008854962

`poc-10` is corrupt:
```
 ./tools/h5policy --continue-after-rejection ~/h5/poc-10 
{
  "schema_version": 1,
  "decision": "reject_corrupt",
  "profile": "untrusted_strict",
  "file": "/home/bob/h5/poc-10",
  "mapping_mode": "strict",
  "phase": "0-4",
  "geometry": {
    "physical_bytes": 2873,
    "declared_eoa": 2848,
    "effective_ceiling": 2848,
    "trailing_bytes": 25
  },
  "analysis": {
    "complete": true,
    "walk_started": true,
    "walk_completed": true,
    "stop_reason": "",
    "continue_after_rejection": true,
    "findings_truncated": false
  },
  "boundary": {
    "libhdf5": false,
    "plugins": false,
    "decompression": false,
    "external_file_opens": false,
    "repair": false,
    "writes": false,
    "application_deserialization": false
  },
  "features": {
    "external_links": 0,
    "external_storage": 0,
    "vds": 0,
    "dynamic_filters": [],
    "decode_filters": [],
    "unknown_messages": 0,
    "max_rank_seen": 0,
    "max_logical_dataset_bytes_seen": 0
  },
  "metrics": {
    "metadata_bytes_seen": 680,
    "object_count": 1,
    "attribute_count": 0,
    "object_header_chunk_count": 0,
    "chunk_index_refs": 0,
    "visited_object_headers": 1,
    "visited_continuations": 0,
    "visited_btree_refs": 2,
    "walk_operations": 115
  },
  "findings": [
    {
      "severity": "error",
      "code": "H5_CORRUPT_OFFSET_OUT_OF_FILE",
      "class": "corrupt",
      "has_location": true,
      "offset": 0,
      "object": "superblock",
      "message": "driver-info address is outside the file"
    },
    {
      "severity": "error",
      "code": "H5_CORRUPT_OFFSET_OUT_OF_FILE",
      "class": "corrupt",
      "has_location": true,
      "offset": 120,
      "object": "/",
      "message": "local heap data segment outside file"
    },
    {
      "severity": "error",
      "code": "H5_CORRUPT_BAD_SIGNATURE",
      "class": "corrupt",
      "has_location": true,
      "offset": 1440,
      "object": "/",
      "message": "symbol table node signature mismatch"
    }
  ]
}
```
