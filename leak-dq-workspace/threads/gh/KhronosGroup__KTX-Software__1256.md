# ktxTexture2_transcodeLzEtc1s leaks firstImages when a slice has no alpha data

- URL: https://github.com/KhronosGroup/KTX-Software/issues/1256
- Repo: KhronosGroup/KTX-Software (language: C++)
- State: open; created 2026-09-29T19:43:18Z; status ok; passes main

## Issue body

reporter (NONE) · armatti · 2026-09-29T19:43:18Z · https://github.com/KhronosGroup/KTX-Software/issues/1256

When the target needs alpha and an image descriptor has `alphaSliceByteOffset` or
`alphaSliceByteLength` 0, `ktxTexture2_transcodeLzEtc1s` returns `KTX_FILE_DATA_ERROR` without
`delete[] firstImages`. Every other error return after the allocation frees it. The leak is
4 × (levels + 1) bytes per malformed file.

Found by fuzzing (libFuzzer, LeakSanitizer). Reproduced with libktx alone.

Attached: `n7_etc1s_alpha_slice_missing.ktx2` (352 bytes, sha256
`05dc8b1d2df9ab6e69584c416e187cbdc528805e89b605f75c5f20ae0b167e56`), run with `repro_n1.c`
(create with image data, then `ktxTexture2_TranscodeBasis`) built with `-fsanitize=address`:

```
ERROR: LeakSanitizer: detected memory leaks
Direct leak of 8 byte(s) in 1 object(s) allocated from:
    #0 in operator new[](unsigned long)
    #1 in ktxTexture2_transcodeLzEtc1s(...)
SUMMARY: AddressSanitizer: 8 byte(s) leaked in 1 allocation(s).
```
[n7_etc1s_alpha_slice_missing.zip](https://github.com/user-attachments/files/32819714/n7_etc1s_alpha_slice_missing.zip)
