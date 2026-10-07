# cpu_engine: scaled/rotated Picture is drawn 0.5–3 px off its transform

- URL: https://github.com/thorvg/thorvg/issues/4874
- Repo: thorvg/thorvg (language: C++)
- State: open; created 2026-09-28T10:52:04Z; status ok; passes main

## Issue body

reporter (NONE) · ponzifex · 2026-09-28T10:52:04Z · https://github.com/thorvg/thorvg/issues/4874

Hi,

While comparing rotated images I found that a transformed `Picture` isn't drawn where its transform puts it. A `Shape` with the same transform is exact. Rotation and scale triggers it. This is current `main` (cc3ecf5)

#### Repro

A 16x16 checker as a `Picture`, and the same checker as a `Shape` (`appendRect` per square), both with the same matrix: `translate(64, 64) * rotate(a) * scale(s) * translate(-8, -8)`. Each is drawn alone into a 128x128 `SwCanvas`, ARGB8888, CPU engine, no loaders. They should cover the same pixels.

<img width="1534" height="788" alt="Image" src="https://github.com/user-attachments/assets/8391413e-0996-4877-ac38-f78cb8a3f320" />

Offset of the `Picture` from its exact position. The `Shape` is within 0.01 px in every case.

| rotation | scale | content offset (px) | footprint offset (px) |
|---|---|---|---|
| 0° | 1 | 0.00, 0.00 | 0.00, 0.00 |
| 0.1° | 1 | −1.00, −1.00 | −0.52, −0.53 |
| 30° | 1 | −0.68, −1.18 | −0.50, −0.52 |
| 180° | 1 | +0.50, +0.50 | +0.50, +0.50 |
| 0° | 1.5 | +0.48, +0.48 | 0.00, 0.00 |
| 0° | 2 | +0.48, +0.48 | 0.00, 0.00 |
| 0.1° | 2 | −1.50, −1.50 | −0.53, −0.53 |
| 30° | 2 | −0.86, −1.88 | −0.50, −0.54 |
| 90° | 2 | +0.50, −1.50 | 0.00, −0.50 |
| 180.1° | 2 | +0.50, +0.50 | −0.45, −0.45 |
| 30° | 3.5 | −1.14, −2.90 | −0.51, −0.56 |
| 30°, partly above the canvas | 2 | −0.86, −2.04 | −0.62, −0.74 |

- **content offset:** the rendered checker fitted against an exact bilinear rendering of the texture, inside the image only
- **footprint offset:** centroid of a solid 16x16 `Picture` minus that of a solid 16x16 `Shape`

Going from 0° to 0.1° moves the image content by about 2 px in each direction at scale 2, and the error grows with the scale.

#### Cause

With pixel `x` covering `x .. x+1`, a pixel should be sampled at `x + 0.5`, and texel `i` has its center at `i + 0.5`. Three places don't do that:

1. **Axis-aligned path** ([tvgSwRaster.cpp#L558](https://github.com/thorvg/thorvg/blob/cc3ecf52c3abf41f353cf88377443ded6e85159f/src/renderer/cpu_engine/tvgSwRaster.cpp#L558), [#L569](https://github.com/thorvg/thorvg/blob/cc3ecf52c3abf41f353cf88377443ded6e85159f/src/renderer/cpu_engine/tvgSwRaster.cpp#L569)) samples at the pixel's corner: `sx = x * e11 + e13 - 0.49f`.
2. **Texmap** samples at the far corner (`x + 1`, `y + 1`): `dx = 1 - (_xa - x1)` ([#L109](https://github.com/thorvg/thorvg/blob/cc3ecf52c3abf41f353cf88377443ded6e85159f/src/renderer/cpu_engine/tvgSwRasterTexmap.h#L109)) and `dy = 1.0f - (y[0] - yi[0])` ([#L423](https://github.com/thorvg/thorvg/blob/cc3ecf52c3abf41f353cf88377443ded6e85159f/src/renderer/cpu_engine/tvgSwRasterTexmap.h#L423)). It also uses `u, v` directly as texel indices (UVs start at `{0, 0}`, [#L544](https://github.com/thorvg/thorvg/blob/cc3ecf52c3abf41f353cf88377443ded6e85159f/src/renderer/cpu_engine/tvgSwRasterTexmap.h#L544)), so the texel side is off by another half texel. Together: −0.5 − 0.5·scale px, which is the −1.0 at scale 1 and −1.5 at scale 2 above. `_feathering()` measures the edge coverage from the same far corner, so the image border is uneven too.
3. **Rows skipped under a clip** are counted from the vertex, not the row: `off_y = y[0] < bbox.min.y ? (bbox.min.y - y[0]) : 0` ([#L430](https://github.com/thorvg/thorvg/blob/cc3ecf52c3abf41f353cf88377443ded6e85159f/src/renderer/cpu_engine/tvgSwRasterTexmap.h#L430)). It adds up to one row of error when the image starts above the clip (last table row).

Points 1 and 2 disagree with each other, which is why a 0.1° turn switches from one error to the other.

#### Possible fix

The attached patch (`thorvg-image-sampling.patch` in the zip, against cc3ecf5, 2 files, +137 −132) does this:

- **Axis-aligned path:** samples at the pixel center. Nearest and the down-scaler take the same position and convert it to their own texel convention.
- **Texmap:**
  - samples at the pixel center, and draws a pixel when its center is inside, so the two triangles share the diagonal without gaps or overlap
  - looks up texels at `u - 0.5` with edge clamping. The two copies of the bilinear lookup become one `_texel()` helper, and the out-of-range `continue` (which skipped the UV step) goes away.
  - `_feathering()` computes the border coverage from the distance of the pixel center to the image border. To reach the partly covered border pixels, the mesh grows by half a pixel.
  - counts skipped rows from `yi`

Same repro with the patch: content offset 0.00 px and footprint offset ≤ 0.01 px in every case of the table.

<img width="1534" height="1512" alt="Image" src="https://github.com/user-attachments/assets/e3f24ba4-4254-4d01-b02c-da49e8a09499" />

Checked:
- **Unit tests:** `tvgUnitTests` passes, 91 cases, 13904 assertions (same as `main`).
- **Sanitizers:** ASan + UBSan, 5000 random transforms (rotation, scale down to 0.05, skew, mirroring, off-canvas) through the plain, blending, matting, nearest and picture-as-mask (8-bit) paths. No errors.
- **Speed**, 512x512 image into 1024x1024, release build, ms/frame:

| case | main | patch |
|---|---|---|
| rotate 30°, scale 1.3 (texmap) | 3.26 | 3.46 |
| rotate 7°, scale 0.8 (texmap) | 1.29 | 1.38 |
| scale 1.7 (scaled) | 6.00 | 5.83 |
| scale 0.3 (scaled, down-scaler) | 0.26 | 0.26 |

The texmap is about 6% slower, from the edge-clamped lookup and the distance-based coverage. The scaled path is about 3% faster.

Feel free to take any part of it or do it differently. The repro, stress test and benchmark are single .cpp files against the public API; the offsets come from a small Python script.

[thorvg-image-sampling.zip](https://github.com/user-attachments/files/32740161/thorvg-image-sampling.zip)

Side note, unrelated to this: ASan reports an alloc-dealloc mismatch (malloc vs `operator delete`) in `LoaderMgr::retrieve()` when a raw-data `Picture` is freed.

