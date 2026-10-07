# GL shadow map creation failure leaks a texture + FBO every frame

- URL: https://github.com/CanReader/SleakEngine/issues/157
- Repo: CanReader/SleakEngine (language: C++)
- State: open; created 2026-09-04T14:16:11Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · CanReader · 2026-09-04T14:16:11Z · https://github.com/CanReader/SleakEngine/issues/157

`src/Graphics/OpenGL/OpenGLRenderer.cpp:714-718`, retried at `:732-734`; same pattern at `:849-853`

`CreateShadowMapResources` returns false at :714-718 **without** calling `glDelete*` on what it already
created and **without** setting `m_shadowMapCreated`. The caller retries unconditionally every frame
(:732-734).

At 2048x2048 D32F that is roughly **16 MB leaked per frame**, unbounded: the process is OOM within seconds
of the first failure.

`CreateGBufferResources` has the same missing cleanup at :849-853. Both are inconsistent with the two
shader-failure branches immediately below (:860-864, :871-875), which *do* call `CleanupGBufferResources()`
confirming the omission is an oversight.

Severity: **leak** (catastrophic rate).

Found by a full audit of the graphics layer. Assessed severity: leak: unbounded, per-frame.
