# OpenGL error when reading texture 1282

- URL: https://github.com/Almamu/linux-wallpaperengine/issues/423
- Repo: Almamu/linux-wallpaperengine (language: C++)
- State: open; created 2025-11-29T16:51:30Z; status ok; passes offcwe

## Issue body

reporter (NONE) · spoiledhangover · 2025-11-29T16:51:30Z · https://github.com/Almamu/linux-wallpaperengine/issues/423

### What are you trying to do, and what's the problem?

above is the error i've been getting whenever i try to apply a wallpaper. i have tried dozens of wallpapers and none have worked. despite some hours of troubleshooting it still wont work so im not sure what i have to do

### What have you tried so far?

try the nvidia fix listed on the home page, dozens of different wallpapers, reinstalling dependencies and installing compatibility software

### Errors or Log Output

<img width="650" height="150" alt="Image" src="https://github.com/user-attachments/assets/9795e044-71e6-4695-9062-9e5dfd50a4f0" />

### OS, Desktop Environment, X11/Wayland

linux mint 22 cinnamon

### Installation Method (e.g., AUR, Flatpak, build from source)

build from source

## Comment 3615451446

other (NONE) · AuroraCrimsonRose · 2025-12-05T06:09:22Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3615451446

Same issue even when running Open GL Thread Optimizations -Linux Mint 22 Cinnamon -Built from Source


## Comment 3642406237

other (NONE) · little-sheepycn · 2025-12-11T15:15:51Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3642406237

same issue on opensuse tumbleweed x11 nvidia-open driver
```
/home/ycn/文档/linux-wallpaperengine/build/output/linux-wallpaperengine  --scaling fill --screen-root DP-0 --bg 3540131827
Running with: /home/ycn/文档/linux-wallpaperengine/build/output/linux-wallpaperengine --scaling fill --screen-root DP-0 --bg 3540131827 
Unknown object type found: {"id":164,"name":"脚本","origin":"960.00000 540.00000 0.00000","visible":{"script":"'use strict';\n\nexport function init() {\n\tconst skeleton1=thisScene.getLayer(\"希罗头发-后\");\n\tconst skeleton2=thisScene.getLayer(\"裙子\");\n\tconst skeleton3=thisScene.getLayer(\"艾玛头发2\");\n\tconst skeleton4=thisScene.getLayer(\"艾玛头发1\");\n\tconst skeleton5=thisScene.getLayer(\"希罗头发\");\n\tconst skeleton6=thisScene.getLayer(\"希罗头发1\");\n\tconst skeleton7=thisScene.getLayer(\"帽子\");\n\tconst skeleton8=thisScene.getLayer(\"叶片\");\n\n\tskeleton1.currentFrame=0;\n\tskeleton2.currentFrame=0;\n\tskeleton3.currentFrame=0;\n\tskeleton4.currentFrame=0;\n\tskeleton5.currentFrame=0;\n\tskeleton6.currentFrame=0;\n\tskeleton7.currentFrame=0;\n\tskeleton8.currentFrame=0;\n}\n","value":true}}
Found requested screen: DP-0 -> 0x0:2560x1440
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Particle '光粒' max particles: 500 (maxCount=500 * countMultiplier=1)
Particle '光粒' texture: particle/光点 | cols=0 rows=0 frames=0 duration=0
OpenGL error when reading texture 1282
OpenGL error when reading texture 1282
```
```/home/ycn/文档/linux-wallpaperengine/build/output/linux-wallpaperengine  3540131827
Running with: /home/ycn/文档/linux-wallpaperengine/build/output/linux-wallpaperengine 3540131827 
Unknown object type found: {"id":164,"name":"脚本","origin":"960.00000 540.00000 0.00000","visible":{"script":"'use strict';\n\nexport function init() {\n\tconst skeleton1=thisScene.getLayer(\"希罗头发-后\");\n\tconst skeleton2=thisScene.getLayer(\"裙子\");\n\tconst skeleton3=thisScene.getLayer(\"艾玛头发2\");\n\tconst skeleton4=thisScene.getLayer(\"艾玛头发1\");\n\tconst skeleton5=thisScene.getLayer(\"希罗头发\");\n\tconst skeleton6=thisScene.getLayer(\"希罗头发1\");\n\tconst skeleton7=thisScene.getLayer(\"帽子\");\n\tconst skeleton8=thisScene.getLayer(\"叶片\");\n\n\tskeleton1.currentFrame=0;\n\tskeleton2.currentFrame=0;\n\tskeleton3.currentFrame=0;\n\tskeleton4.currentFrame=0;\n\tskeleton5.currentFrame=0;\n\tskeleton6.currentFrame=0;\n\tskeleton7.currentFrame=0;\n\tskeleton8.currentFrame=0;\n}\n","value":true}}
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Particle '光粒' max particles: 500 (maxCount=500 * countMultiplier=1)
Particle '光粒' texture: particle/光点 | cols=0 rows=0 frames=0 duration=0
Stop requested by driver
Stopping
INFO: Leaked thread (0x6ff8aa0)
```


## Comment 3648267832

other (CONTRIBUTOR) · beyluta · 2025-12-12T21:53:58Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3648267832

Same issue on a fresh, bare-metal installation of:

Mint 22 Cinnamon (x11)
Mint 22 KDE Plasma (x11)

## Comment 3650029396

other (NONE) · kamythol · 2025-12-14T01:31:32Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3650029396

It's an issue with particles, running with `--disable-particles` works fine since the latest commit

## Comment 3652079792

maintainer (OWNER) · Almamu · 2025-12-14T20:50:36Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3652079792

I've pushed a few changes to include more info on GL errors, can you run the last commit with debug info and see what it shows on the console?

## Comment 3675580387

other (NONE) · little-sheepycn · 2025-12-19T15:55:26Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3675580387

```
~/文档/linux-wallpaperengine/build/output> /home/ycn/文档/linux-wallpaperengine/build/output/linux-wallpaperengine  --scaling fill --screen-root DP-0 --bg 3540131827
Running with: /home/ycn/文档/linux-wallpaperengine/build/output/linux-wallpaperengine --scaling fill --screen-root DP-0 --bg 3540131827 
Unknown object type found: {"id":164,"name":"脚本","origin":"960.00000 540.00000 0.00000","visible":{"script":"'use strict';\n\nexport function init() {\n\tconst skeleton1=thisScene.getLayer(\"希罗头发-后\");\n\tconst skeleton2=thisScene.getLayer(\"裙子\");\n\tconst skeleton3=thisScene.getLayer(\"艾玛头发2\");\n\tconst skeleton4=thisScene.getLayer(\"艾玛头发1\");\n\tconst skeleton5=thisScene.getLayer(\"希罗头发\");\n\tconst skeleton6=thisScene.getLayer(\"希罗头发1\");\n\tconst skeleton7=thisScene.getLayer(\"帽子\");\n\tconst skeleton8=thisScene.getLayer(\"叶片\");\n\n\tskeleton1.currentFrame=0;\n\tskeleton2.currentFrame=0;\n\tskeleton3.currentFrame=0;\n\tskeleton4.currentFrame=0;\n\tskeleton5.currentFrame=0;\n\tskeleton6.currentFrame=0;\n\tskeleton7.currentFrame=0;\n\tskeleton8.currentFrame=0;\n}\n","value":true}}
Found requested screen: DP-0 -> 0x0:2560x1440
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Shader has a require block #require LightingV1
Particle '光粒' max particles: 500 (maxCount=500 * countMultiplier=1)
Particle '光粒' texture: particle/光点 | cols=0 rows=0 frames=0 duration=0
OpenGL error when reading texture 1282
OpenGL error when reading texture 1282
```

## Comment 3774064370

other (NONE) · arnt0r · 2026-01-20T17:21:21Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3774064370

I'm on fedora 43, KDE Plasma, X11. I get this error aswell, and when running " ./linux-wallpaperengine --disable-particles --screen-root DP4 --bg 1831214647 " the program just hangs on "Found requested screen: DP-4 -> 2560x0:2560x1440". My background doesn't change.

Edit: when just running ./linux-wallpaperengine --disable-particles 1831214647 the program doesn't hang but it just opens a new window with the animated picture. Not sure if this is the intended result but it seems pretty weird.


## Comment 3808671819

other (NONE) · Xiron2Bar · 2026-01-28T02:57:08Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3808671819

I'm encountering the same error. I run Mint 22.3, with Cinnamon 6.6.6, X11. When running without the --screen-root argument it just opens a new window with the background running as normal, but when --screen-root is included it throws the OpenGL error when reading texture 1282.

## Comment 3907727030

other (CONTRIBUTOR) · sgtaziz · 2026-02-16T10:40:44Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-3907727030

The new commits pushed have fixed this issue on my side. Can anyone confirm?

## Comment 4422982480

other (CONTRIBUTOR) · Gaiser147 · 2026-05-11T17:06:05Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-4422982480

Had the same issue. 
I fixed it together with some other issues in #561 
Though I'm not sure if it works for you (i tested on fedora 43)

@coderabbitai maybe you can confirm if PR #561 does fix this issue

## Comment 4422992748

other (CONTRIBUTOR) · coderabbitai[bot] · 2026-05-11T17:07:19Z · https://github.com/Almamu/linux-wallpaperengine/issues/423#issuecomment-4422992748

<!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR `#561` details
gh pr view 561 --repo Almamu/linux-wallpaperengine --json title,body,files,state,commits

# Get the list of files changed
gh pr view 561 --repo Almamu/linux-wallpaperengine --json files | jq '.files[].path'
```

Length of output: 8361

---

Let me look at the specific particle and texture-related changes in the PR.

---

🏁 Script executed:
```
#!/bin/bash
# Fetch the diff for relevant files in PR `#561`
gh api repos/Almamu/linux-wallpaperengine/pulls/561/files --paginate | \
  jq '.[] | select(.filename == "src/WallpaperEngine/Render/Objects/CParticle.cpp") | .patch'

echo "=== TextureCache.cpp diff ==="
gh api repos/Almamu/linux-wallpaperengine/pulls/561/files --paginate | \
  jq '.[] | select(.filename == "src/WallpaperEngine/Render/TextureCache.cpp") | .patch'

echo "=== CFBO.cpp diff ==="
gh api repos/Almamu/linux-wallpaperengine/pulls/561/files --paginate | \
  jq '.[] | select(.filename == "src/WallpaperEngine/Render/CFBO.cpp") | .patch'
```

Length of output: 18887

---



</details>

`@Gaiser147`, I reviewed the diffs in PR `#561` against the symptoms reported in this issue. Here's my assessment:

**The specific `OpenGL error when reading texture 1282` (GL_INVALID_OPERATION) from issue `#423` does not appear to be directly addressed by PR `#561`.**

Here's what the relevant changed files actually do:

| File | Changes in PR `#561` | Relevant to `#423`? |
|---|---|---|
| `CParticle.cpp` | Refactors `updateMatrices()` into `applyParallaxToModelMatrix()`, `updateParticleViewProjection()`, `updateParticleRenderVars()`; adds parallax support for particles | ❌ No — parallax/matrix math, not texture loading |
| `TextureCache.cpp` | Adds `$mediaThumbnail` / `$mediaPreviousThumbnail` support via `playerctl`, file URI parsing, and STB image loading | ❌ No — media thumbnail feature, unrelated to particle textures |
| `CFBO.cpp` | Fixes framebuffer clearing to use transparent `(0,0,0,0)` instead of the scene clear color | 🟡 Tangential rendering fix, not the texture read error |

The error in `#423` occurs specifically after:
```
Particle '光粒' texture: particle/光点 | cols=0 rows=0 frames=0 duration=0
OpenGL error when reading texture 1282
```

This GL_INVALID_OPERATION during texture read (likely in `glGetTexImage` or equivalent) with `cols=0 rows=0 frames=0` suggests invalid texture state at upload/bind time — none of the PR `#561` particle changes touch that path.

It's also worth noting that `@sgtaziz`'s comment ("The new commits pushed have fixed this issue on my side") appears to reference commits pushed directly to `main` by `@Almamu`, independent of PR `#561`.

**Recommendation:** PR `#561` is a valuable broad compatibility improvement, but users affected by the GL 1282 particle texture error from this issue should check if the fix is already present in the latest `main` branch commits from `@Almamu`.


<!-- <agentComponentType>chat-answer</agentComponentType> -->

<!-- <rawResChunk><answer><details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
# Get PR `#561` details
gh pr view 561 --repo Almamu/linux-wallpaperengine --json title,body,files,state,commits

# Get the list of files changed
gh pr view 561 --repo Almamu/linux-wallpaperengine --json files | jq '.files[].path'
```

Length of output: 8361

---

Let me look at the specific particle and texture-related changes in the PR.

---

🏁 Script executed:
```
#!/bin/bash
# Fetch the diff for relevant files in PR `#561`
gh api repos/Almamu/linux-wallpaperengine/pulls/561/files --paginate | \
  jq '.[] | select(.filename == "src/WallpaperEngine/Render/Objects/CParticle.cpp") | .patch'

echo "=== TextureCache.cpp diff ==="
gh api repos/Almamu/linux-wallpaperengine/pulls/561/files --paginate | \
  jq '.[] | select(.filename == "src/WallpaperEngine/Render/TextureCache.cpp") | .patch'

echo "=== CFBO.cpp diff ==="
gh api repos/Almamu/linux-wallpaperengine/pulls/561/files --paginate | \
  jq '.[] | select(.filename == "src/WallpaperEngine/Render/CFBO.cpp") | .patch'
```

Length of output: 18887

---



</details>

`@Gaiser147`, I reviewed the diffs in PR `#561` against the symptoms reported in this issue. Here's my assessment:

**The specific `OpenGL error when reading texture 1282` (GL_INVALID_OPERATION) from issue `#423` does not appear to be directly addressed by PR `#561`.**

Here's what the relevant changed files actually do:

| File | Changes in PR `#561` | Relevant to `#423`? |
|---|---|---|
| `CParticle.cpp` | Refactors `updateMatrices()` into `applyParallaxToModelMatrix()`, `updateParticleViewProjection()`, `updateParticleRenderVars()`; adds parallax support for particles | ❌ No — parallax/matrix math, not texture loading |
| `TextureCache.cpp` | Adds `$mediaThumbnail` / `$mediaPreviousThumbnail` support via `playerctl`, file URI parsing, and STB image loading | ❌ No — media thumbnail feature, unrelated to particle textures |
| `CFBO.cpp` | Fixes framebuffer clearing to use transparent `(0,0,0,0)` instead of the scene clear color | 🟡 Tangential rendering fix, not the texture read error |

The error in `#423` occurs specifically after:
```
Particle '光粒' texture: particle/光点 | cols=0 rows=0 frames=0 duration=0
OpenGL error when reading texture 1282
```

This GL_INVALID_OPERATION during texture read (likely in `glGetTexImage` or equivalent) with `cols=0 rows=0 frames=0` suggests invalid texture state at upload/bind time — none of the PR `#561` particle changes touch that path.

It's also worth noting that `@sgtaziz`'s comment ("The new commits pushed have fixed this issue on my side") appears to reference commits pushed directly to `main` by `@Almamu`, independent of PR `#561`.

**Recommendation:** PR `#561` is a valuable broad compatibility improvement, but users affected by the GL 1282 particle texture error from this issue should check if the fix is already present in the latest `main` branch commits from `@Almamu`.</answer></rawResChunk> -->
