# [CODE REVIEW] A friendly being sent a code review.

- URL: https://github.com/Nemirtingas/ingame_overlay/issues/77
- Repo: Nemirtingas/ingame_overlay (language: C++)
- State: open; created 2026-08-19T07:37:34Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · Nemirtingas · 2026-08-19T07:37:34Z · https://github.com/Nemirtingas/ingame_overlay/issues/77

# Code Review — ingame_overlay

**Date:** 2026-08-19
**Scope:** Core library (`src/`, `include/`, `public/` — ~17k lines, 52 files). Vendored deps (ImGui, mini_detour, glad2, VulkanSDK headers) and test harnesses excluded. Depth: "standard" — all core files read; Windows DX9/11/12, Vulkan, OpenGL, input hooks and X11/Metal/NSView reviewed line by line; DX10 (a close clone of DX11), Linux/macOS OpenGL hooks and the Linux/macOS renderer detectors reviewed by diff/skim against their Windows counterparts.

**Overall impression:** A mature, pragmatic codebase for a hard problem (injecting an ImGui overlay into arbitrary games across 7 renderer APIs and 3 platforms). Architecture is clean: `BaseHook_t` (mini_detour RAII wrapper) → per-renderer singleton hooks → shared `RendererHookInternal_t` resource machinery. The heuristics it relies on (device refcount thresholds, swapchain memory scanning, fake `VK_SUBOPTIMAL_KHR`) are inherently fragile but are known-art in this domain and mostly commented as such. The issues below are ranked by expected real-world impact.

---

## Positive observations

Worth keeping as-is: the RAII unhook via `MiniDetour::Hook_t` vector; the Vyukov MPMC queue for cross-thread input events (correct implementation, and the added `item_count_` is honestly relaxed/approximate); DX9's Reset handling correctly releases `D3DPOOL_DEFAULT` textures before `Reset` with an explanatory comment; deferred texture release keyed to frames-in-flight in DX12/Vulkan/Metal; the batched-upload path (single staging buffer, one fence wait) in DX12/Vulkan; consistent screenshot-failure signaling (`_SendScreenshot(nullptr)`); and the DXVK detection via interop GUIDs, which is neatly isolated.

## Suggested fix order

1. H1 (two-line fix, real crash), H4 (bounded work, crash-on-OOM), H2 (restructure one condition + move fence reset after the bail-out point).
2. H3 (delete or implement the readback branch), H5 (a mutex around `_RenderPass` + retain the descriptor).
3. M1 (doc fix), M2 (forward filters), M9/M10 (null checks in the detector).
4. The rest as opportunity allows; M3/M4 deserve a design think rather than a patch.

## Not covered at this depth (candidates for a deeper pass)

DX10Hook line-by-line (reviewed as DX11-clone only), `DXVKDetector.h` / `SimpleWindowsGamingInput` internals, macOS `RendererDetector.mm` and OpenGL hooks in detail, the Linux `RendererDetector.cpp` beyond diffing, validation of the mini_detour vendored copy, and dynamic verification (building + running the test apps under validation layers / D3D debug layer, which would confirm M3/M4 empirically).


## Comment 5358101602

reporter (OWNER) · Nemirtingas · 2026-08-20T15:31:26Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358101602

### H1. Symbol-load check tests the wrong pointer — never fails (copy-pasted bug)
`src/Windows/WindowsHook.cpp:126` and `src/Linux/X11Hook.cpp:174`

```cpp
*entry.func_ptr = libUser32.GetSymbol<void*>(entry.func_name);
if (entry.func_ptr == nullptr)   // address of member — always non-null
```

Should be `*entry.func_ptr == nullptr`. If any symbol fails to resolve, the error path is dead code and a null pointer is either hooked or later invoked (`_TranslateMessage`, `_DefWindowProcW`, `_XQueryPointer`…) → crash inside the host game. Same pattern in both files.


## Comment 5358102934

reporter (OWNER) · Nemirtingas · 2026-08-20T15:31:32Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358102934

### H2. Vulkan: early-return mid-frame leaves a reset fence and an open command buffer → permanent hang
`src/Windows/VulkanHook.cpp:865-889` (identical in `src/Linux/VulkanHook.cpp:869-893`)

Per swapchain image the code does `vkWaitForFences` → `vkResetFences` → `vkBeginCommandBuffer` → `vkCmdBeginRenderPass`, and only then:

```cpp
if (ImGui_ImplVulkan_NewFrame() && !WindowsHook_t::Inst()->PrepareForOverlay(_MainWindow))
    return;
```

If that returns, the fence was reset but nothing will ever signal it — the next present for the same image index waits on it with timeout `~0ull` and the game freezes. The command buffer is also left in recording state and the render pass unclosed. Additionally the condition is inverted relative to every other backend: if `ImGui_ImplVulkan_NewFrame()` returns *false*, execution *continues* into `ImGui::NewFrame()`/`Render()` with an unready backend (DX11/DX9/GL gate the whole block on `NewFrame() && Prepare()`).


## Comment 5358107758

reporter (OWNER) · Nemirtingas · 2026-08-20T15:31:51Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358107758

### H3. Linux Vulkan detector: `try_to_lock` result never checked — detection state mutated without the mutex
`src/Linux/RendererDetector.cpp:348-361`

```cpp
std::unique_lock<std::recursive_mutex> lk(inst->_RendererMutex, std::try_to_lock);
...
inst->_HookDetected(inst->_VulkanHook);   // runs whether or not the lock was acquired
```

The Windows equivalent takes a blocking `lock_guard`. Here, if the try-lock fails (detection thread holds the mutex), `_HookDetected` still runs: it unhooks `_DetectionHooks` and flips `_DetectionDone` concurrently with `DetectRenderer` iterating and installing hooks on the other thread — data race on the hook list, potential unhook-while-hooking corruption. Either check `lk.owns_lock()` and skip, or use a blocking lock like Windows does.


## Comment 5358109978

reporter (OWNER) · Nemirtingas · 2026-08-20T15:32:00Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358109978

### H4. DX12 screenshot: `goto readback` path dereferences null command list / staging buffer
`src/Windows/DX12Hook.cpp:832-923`

When the back buffer reports `D3D12_HEAP_TYPE_READBACK`, the code jumps to `readback:` before `pCommandList`, `pFence`, `pStaging` are created, then immediately calls `pCommandList->ResourceBarrier(...)` (null) and later `pStaging->Map(...)` (null), with `barrier.Transition.pResource` also unset. Any execution of that branch crashes. It's a rarely-hit path (swapchain buffers are practically never readback heaps), but the code as written can never work — either implement it or remove the branch.



## Comment 5358111025

reporter (OWNER) · Nemirtingas · 2026-08-20T15:32:06Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358111025

### H5. Resource loading asserts instead of handling failure — release-build null derefs
`src/Windows/DX11Hook.cpp:391-404`, `src/Windows/DX10Hook.cpp:355-369`, `src/Windows/DX12Hook.cpp:662-763`, `src/Windows/VulkanHook.cpp:1031-1107`

`CreateTexture2D` / `CreateCommittedResource` / `vkCreateImage` failures are handled with `IM_ASSERT(SUCCEEDED(hr))` (no-op in release) or ignored entirely (Vulkan). On device-removed, OOM, or absurd image sizes supplied by the library user, the follow-up calls (`texture->Release()`, `uploadBuffer->Map()`, `vkGetImageMemoryRequirements(image=NULL)`) crash the host game. DX9 (`DX9Hook.cpp:314-353`) and Metal (`MetalHook.mm:247-253`) do this correctly — check and skip. Bring the other four backends up to that standard.



## Comment 5358113127

reporter (OWNER) · Nemirtingas · 2026-08-20T15:32:14Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358113127

### H6. Metal: `_RenderPass` vector raced across threads
`src/MacOSX/MetalHook.mm:308-352`

`MyMTLCommandBufferRenderCommandEncoderWithDescriptor` (any encoder-creating thread — multithreaded encoding is idiomatic Metal) does `_RenderPass.emplace_back(...)` while `MyMTLCommandBufferPresentDrawable` iterates and `clear()`s it, with no lock. Concurrent `emplace_back` + iteration on a `std::vector` is UB → intermittent crashes in multithreaded games. Also: the stored `MTLRenderPassDescriptor*`/command-buffer ids are held without retain (the file uses MRC — there are explicit `release` calls), so the descriptor can be deallocated by the app before present reads it.



## Comment 5358114723

reporter (OWNER) · Nemirtingas · 2026-08-20T15:32:21Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358114723

### M1. Public API doc for `DetectRenderer` is inverted
`include/InGameOverlay/RendererDetector.h:33` says "True: detection done, False: detection can be called again". The implementation (all three platforms; e.g. `src/Windows/RendererDetector.cpp:1480-1548`) returns **true = keep calling, false = done** — and the shipped example (`tests/overlay_example/library_main.cpp:277`) loops `while (DetectRenderer(...))`. Anyone following the header comment writes an inverted loop. Fix the comment (or the return semantics, but that breaks callers).



## Comment 5358129999

reporter (OWNER) · Nemirtingas · 2026-08-20T15:33:20Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358129999

### M2. `GetMessage`/`PeekMessage` hooks force message filters to 0 unconditionally
`src/Windows/WindowsHook.cpp:514-608`

`wMsgFilterMin/Max` are zeroed on every call (`// Force filters to 0 ?` — the author's own question mark), even when the overlay is closed and inputs aren't hidden. A game calling `GetMessage(&msg, hwnd, WM_TIMER, WM_TIMER)` suddenly receives *all* messages; message loops that rely on range filtering will misbehave in ways that look unrelated to the overlay. Filters should be forwarded untouched, or only widened while `_ApplicationInputsHidden` is actually active.


## Comment 5358131747

reporter (OWNER) · Nemirtingas · 2026-08-20T15:33:26Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358131747

### M3. Vulkan: deliberately returning fake `VK_SUBOPTIMAL_KHR`, and format guess when the game ignores it
`src/Windows/VulkanHook.cpp:1376-1391`

The first present returns a spoofed `VK_SUBOPTIMAL_KHR` to trick the game into recreating its swapchain so the hook can capture the image format in `vkCreateSwapchainKHR`. Games are *allowed* to ignore `VK_SUBOPTIMAL_KHR` — in that case `_VulkanTargetFormat` stays at its default `VK_FORMAT_R8G8B8A8_UNORM` (line 1443), which then mismatches the actual swapchain images (most Windows swapchains are BGRA) in the render pass and image views → validation errors, potential artifacts or driver-dependent failure. Consider capturing the format from `vkGetPhysicalDeviceSurfaceFormatsKHR` or by hooking swapchain creation earlier rather than lying to the app.



## Comment 5358133839

reporter (OWNER) · Nemirtingas · 2026-08-20T15:33:33Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358133839

### M4. Vulkan synchronization shortcuts
`src/Windows/VulkanHook.cpp:918-969`
- The overlay submit waits on `pPresentInfo->pWaitSemaphores` and **re-signals the same semaphores** (lines 962-963) so the subsequent real present can wait on them again. Works on current drivers but is a spec-gray reuse of binary semaphores; the commented-out "correct" version was abandoned due to validation errors — document the invariant, and consider `VK_KHR_timeline_semaphore` where available.
- Only `pWaitSemaphores` of the first swapchain's present are honored; for `swapchainCount > 1`, iteration `i > 0` waits on nothing.
- Screenshot copies from the swapchain image passing `VK_IMAGE_LAYOUT_PRESENT_SRC_KHR` as `srcImageLayout` to `vkCmdCopyImage` (`VulkanHook.cpp:1309-1312`) without transitioning to `TRANSFER_SRC` — invalid per spec, works on forgiving drivers.



## Comment 5358135554

reporter (OWNER) · Nemirtingas · 2026-08-20T15:33:40Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358135554

### M5. Vulkan/DX12: multiple-swapchain indexing can go out of bounds
`src/Windows/VulkanHook.cpp:860-862`: `_OverlayFrames[pPresentInfo->pImageIndices[i]]` — `_OverlayFrames` was built from `pSwapchains[0]` only (line 834); a second swapchain with more images indexes past the vector. `src/Windows/DX12Hook.cpp:547`: same class of assumption. Single-swapchain games are fine; multi-window/multi-swapchain apps crash. At minimum bounds-check and bail.



## Comment 5358137781

reporter (OWNER) · Nemirtingas · 2026-08-20T15:33:50Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358137781

### M6. DX12: `_CommandQueue` captured without synchronization or ownership
`src/Windows/DX12Hook.cpp:1056-1064`

`_MyID3D12CommandQueueExecuteCommandLists` writes `inst->_CommandQueue = _this` from whatever thread the game submits on; Present reads it concurrently (plain non-atomic pointer), and the queue is never AddRef'd — if the game destroys that queue the hook holds a dangling pointer used for screenshot submission (line 912). Make it atomic and take a reference (or re-validate against the swapchain each frame).



## Comment 5358139549

reporter (OWNER) · Nemirtingas · 2026-08-20T15:33:58Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358139549

### M7. Detector/hook singletons: lifetime races with in-flight hooked calls
`src/Windows/RendererDetector.cpp:918-943`, `FreeDetector()` (line 1713), and every hook's `~XxxHook_t`

`FreeDetector()` deletes the detector (unhooking in the destructor) while a game render thread may be *inside* `_MyIDXGISwapChainPresent`, which then calls `Inst()` and re-creates an empty instance whose `_IDXGISwapChainPresent` member is null → call through null member-function-pointer. Not fully solvable with inline patching, but: (a) document "only destroy hooks when no frames are in flight", and (b) don't lazily re-create singletons from within hook callbacks — use `_Instance` directly and bail if null. All `Inst()` lazy-inits are also unsynchronized (benign in practice, trivially fixed with a local static).



## Comment 5358141645

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:07Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358141645

### M8. Renderer-hook destructors delete the input-hook singleton, then immediately recreate and leak it
`src/Windows/DX9Hook.cpp:544-547`, `DX10Hook.cpp`, `DX11Hook.cpp:578-581`, `DX12Hook.cpp:1099-1102`, `OpenGLHook.cpp:291-294`

```cpp
if (_WindowsHooked)
    delete WindowsHook_t::Inst();
_ResetRenderState(OverlayHookState::Removing);   // → WindowsHook_t::Inst()->ResetRenderState(...)
```

`_ResetRenderState(Removing)` calls `WindowsHook_t::Inst()` *after* the singleton was deleted — the lazy `Inst()` allocates a **fresh** `WindowsHook_t` that is never destroyed (leak), and `ResetRenderState` runs on an uninitialized instance. Swap the order (reset first, delete last), as the Metal destructor effectively does.



## Comment 5358143231

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:15Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358143231

### M9. X11: `XQueryTree`/`XGetTextProperty` results leaked on every window enumeration
`src/Linux/X11Hook.cpp:51-68` never calls `XFree(childrenWindows)` (and the early `return` at line 63 makes it structurally awkward); `FindApplicationX11Window` (lines 300-312) never `XFree(data.value)`. Runs on every overlay init. Also `_NET_WM_PID` is a CARDINAL property — for `format == 32` Xlib stores items as `long`, so `*(int32_t*)data.value` is endian/ABI-fragile (works on x86-64 LE today).



## Comment 5358147215

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:35Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358147215

### M10. Detection: unchecked instance/device creation in DX9 and Vulkan drivers
- `src/Windows/RendererDetector.cpp:327-328, 344-345`: `Direct3DCreate9Ex(...)` return ignored, then `pD3D->CreateDeviceEx(...)`; fallback `pD3D = Direct3DCreate9(...)` can be null before `pD3D->CreateDevice(...)`. Crashes detection on systems where D3D9 can't initialize (headless, broken drivers, RDP edge cases).
- `src/Windows/RendererDetector.cpp:752-767` and `src/Linux/RendererDetector.cpp:138-155`: `_vkCreateInstance(...)` result unchecked; `_vkEnumeratePhysicalDevices(_vkInstance /* possibly null */, ...)` follows — loader dereferences a null dispatch handle when no ICD is present.



## Comment 5358147963

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:39Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358147963

### M11. Detector never resets `_DummyWindowHandle` after `_ExitDetection`
`src/Windows/RendererDetector.cpp:1455-1477`

`_ExitDetection()` destroys the dummy window but leaves `_DummyWindowHandle` stale; a subsequent `DetectRenderer(restart=true)` path can call `_ExitDetection` again (line 1491) → `DestroyWindow` on a stale HWND, which can hit an unrelated recycled window handle. Null the handle (and atom) after destruction. Related: `CreateDummyHWND`'s `assert(dummyHwnd && ...)` (line 214) asserts the out-*parameter pointer*, not `*dummyHwnd`, so window-creation failure is never caught even in debug.



## Comment 5358149051

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:45Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358149051

### M12. macOS Metal detection only recognizes Intel, NVIDIA-WebDriver, and M1-era GPU driver classes
`src/MacOSX/RendererDetector.mm:126-130`

Detection swizzles `commit` on hardcoded private classes: `MTLIGAccelCommandBuffer` (Intel), `NVMTLCommandBuffer` (NVIDIA WebDriver — dead since Mojave), `AGXG13XFamilyCommandBuffer` (M1 family only). M2/M3/M4 Macs use `AGXG14X`/`G15X`/`G16X` classes and AMD Macs use `AMDMTL*` classes — on all of those, Metal is silently never detected. Consider swizzling via the class of a real object (`[[device newCommandQueue] commandBuffer]` at detection time) instead of hardcoding driver class names, or at least extend the table and log loudly when no class matches. (Also `RendererDetector.mm:308`: `metalClass = objc_getClass(driverHook.RenderCommandEncoderClass)` is assigned and never used — leftover.)



## Comment 5358149904

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:49Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358149904

### M13. macOS `GetRenderer()` is a stub that always returns nullptr
`src/MacOSX/RendererDetector.mm:505-519` — both switch cases are empty `break`s. The public API (`RendererDetector.h:51`) gives no hint that direct (detection-free) renderer acquisition is unimplemented on macOS. Implement or document.



## Comment 5358150844

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:54Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358150844

### M14. DX12: ImGui SRV alloc/free callbacks assume exactly one ImGui-allocated descriptor
`src/Windows/DX12Hook.cpp:513-525`

`SrvDescriptorAllocFn` stores the allocated slot id in the single `_ImGuiFontTextureId` member and `SrvDescriptorFreeFn` frees that member — ignoring the `cpu_desc_handle` it's given. The codebase enables `ImGuiBackendFlags_RendererHasTextures`-era ImGui (see `ImFontAtlasUpdateNewFrame` calls), under which the backend may allocate *multiple* descriptors over time (dynamic font textures). Each new alloc overwrites the stored id, and each free releases whatever id happens to be stored — descriptor-slot double-free/leak in the bitmap allocator. Map handle→id (the id is derivable from the heap base and increment) instead of caching one.



## Comment 5358151524

reporter (OWNER) · Nemirtingas · 2026-08-20T15:34:57Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358151524

### M15. CMake: first configure fails unless `IMGUI_USER_CONFIG` is passed
`CMakeLists.txt:134` — `if(NOT ${IMGUI_USER_CONFIG} STREQUAL "")` with the variable undefined expands to `if(NOT STREQUAL "")` → hard CMake error ("if given arguments…"). CI always passes `-DIMGUI_USER_CONFIG=...` so it never notices; a plain `cmake -S . -B build` for a new user errors out. Use `if(DEFINED IMGUI_USER_CONFIG AND NOT IMGUI_USER_CONFIG STREQUAL "")` (unexpanded variable name).



## Comment 5358152055

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:00Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358152055

- **L1. `BaseHook_t::HookFuncs` discards `HookFunc`'s bool** (`src/BaseHook.h:47-58`); `WindowsHook_t::StartHook` and `X11Hook_t::StartHook` proceed as "hooked" even if some hooks failed — half-hooked input where e.g. `GetCursorPos` is spoofed but `SetCursorPos` isn't.


## Comment 5358152569

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:03Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358152569

- **L2. WGI raw-controller memset bug** (`src/Windows/WindowsHook.cpp:712`): `memset(axisArray, 0, sizeof(axisArray) * axisArrayLength)` uses pointer size, not `sizeof(*axisArray)` (double). Coincidentally correct on x64 (8==8), wrong on x86 — only half the axis array is cleared.


## Comment 5358153159

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:06Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358153159

- **L3. WGI `Added` handlers not removed in the destructor** (`WindowsHook.cpp:804-815`, commented out) — a controller hot-plugged after the hook is destroyed calls into a freed instance. Related COM hygiene in `SimpleWindowsGamingInput.cpp`: `AddRef`/`Release` return the *previous* refcount (`fetch_add` return) rather than the resulting count, `Release` never destroys (fine for member-lifetime objects, but non-compliant return values), and the `IRawGameControllerStatics`/`IGamepadStatics` factories are never `Release`d (process-lifetime leak).


## Comment 5358153894

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:09Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358153894

- **L4. Device-refcount removal heuristic** (`_UpdateHookDeviceRefCount` in DX9/10/11/12): magic constants including `+1 // ?` tied to exact ImGui backend internals; an ImGui upgrade silently shifts the threshold and the overlay either tears down mid-game or keeps a destroyed device alive. Note this is doubly coupled because the ImGui dependency is a **fork** (`Nemirtingas/ImGui` per `.gitmodules`, with non-upstream backends `imgui_impl_x11`, a win32 backend taking a GetKeyState callback, and `ImFontAtlasUpdateNewFrame`). Pin and re-verify on every bump; a `static_assert` on `IMGUI_VERSION_NUM` would document the coupling. Stock upstream ImGui will not build this project — worth a README note.


## Comment 5358154614

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:13Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358154614

- **L5. DX11/DX9/DX10 vs DX12/Vulkan/Metal release inconsistency**: DX11 `_ReleaseResources` frees SRVs immediately (`DX11Hook.cpp:417-424`; the stored `ReleaseFrame` is unused — same in DX9/DX10); DX12/Vulkan/Metal correctly defer N frames. D3D9/10/11 runtime refcounting makes immediate release safe today, but the asymmetry deserves a comment or unification.


## Comment 5358155268

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:16Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358155268

- **L6. DX12 `initInfo.DSVFormat = sc_desc.BufferDesc.Format`** (`DX12Hook.cpp:510`) — a color format passed as depth-stencil format. Harmless (ImGui uses no depth) but should be `DXGI_FORMAT_UNKNOWN`.


## Comment 5358155811

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:19Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358155811

- **L7. DX12 swapchain scan** (`DX12Hook.cpp:213-224`) reads 1024 bytes past a COM object pointer at byte granularity — can theoretically fault at an allocation boundary and breaks whenever DXGI's internal layout changes (fallback exists, good).


## Comment 5358156479

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:22Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358156479

- **L8. `DX12Frame_t` move constructor drops `CommandList`** (`src/Windows/DX12Hook.h:100-104`): copies `RenderTarget`, `CommandAllocator`, `BackBuffer` but not `CommandList`, then `other.Reset()` nulls the source → the command list leaks and the moved-to frame has none. Currently latent (`_OverlayFrames.resize` happens only while empty), but any future reallocation with populated frames breaks. The move-*assignment* is correct; fix the ctor to match. (`Reset()` also doesn't clear `RenderTarget` — cosmetic.)


## Comment 5358156906

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:24Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358156906

- **L9. OpenGL (Windows/Linux/macOS) leaks GL state and context assumptions**: `glReadBuffer` changed and not restored in `_HandleScreenshot` (`OpenGLHook.cpp:244`); screenshot dimensions come from the current viewport, which need not match the window; `_ResetRenderState` never calls `ImGui::DestroyContext` (commented out) unlike other backends — context leak on teardown. Texture deleters call `glDeleteTextures` (`OpenGLHook.cpp:330-338`) — only valid if a GL context is current, i.e. only when destruction happens inside the SwapBuffers hook; a user calling `resource->Delete()` off the render thread silently leaks or corrupts. Ties into L13.


## Comment 5358160838

reporter (OWNER) · Nemirtingas · 2026-08-20T15:35:42Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358160838

- **L10. Linux OpenGLX hook never resets on window change** (`src/Linux/OpenGLXHook.cpp:_PrepareForOverlay`): the Windows version tears down when `WindowFromDC` changes; the GLX version initializes once and never re-checks the drawable — stale size/input binding if the game recreates its window.


## Comment 5358234505

reporter (OWNER) · Nemirtingas · 2026-08-20T15:41:50Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358234505

- **L11. Linux renderer coverage**: detection looks for `libGLX.so` and `libvulkan.so` literal names only (`src/Linux/RendererDetector.cpp:52-53`) — most processes have `libGLX.so.0`/`libvulkan.so.1` loaded (behavior depends on the System submodule's matching semantics — verify); EGL-based GL (Wayland, GLES) has no hook path at all; the X11 input hook requires the game to pump events via Xlib `XPending`/`XEventsQueued` (pure-XCB or Wayland games never initialize input). Worth documenting as supported-configuration constraints.


## Comment 5358235308

reporter (OWNER) · Nemirtingas · 2026-08-20T15:41:54Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358235308

- **L12. macOS input/API concerns** (`NSViewHook.mm`): `[NSApplication _mainWindow]` (line 266) is a private underscore selector — use `mainWindow`; `GetKeys` (line 31) is deprecated Carbon; the destructor calls `method_setImplementation(..., (IMP)pressedMouseButtons)` and `removeMonitor:` without null guards — crashes if `StartHook` never ran (MetalHook's destructor guards these; copy that); scroll-wheel events are not in `IgnoreEvent`, so the app keeps receiving scroll while app inputs are "hidden".


## Comment 5358235910

reporter (OWNER) · Nemirtingas · 2026-08-20T15:41:57Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358235910

- **L13. Thread-safety contract undocumented**: `_ImageResourcesToLoad`/`_ImageResources` (plain vector/set) are mutated by `RendererResource_t` methods; safe only if the user touches resources exclusively from inside `OverlayProc`. Real but unstated in the public headers.


## Comment 5358236447

reporter (OWNER) · Nemirtingas · 2026-08-20T15:42:00Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5358236447

- **L14. `RendererResource_t` lifetime**: `~RendererResourceInternal_t` → `Unload()` → `_RendererHook->ReleaseImageResource(...)` on a raw back-pointer. The header warns "Don't use it if you recycle the renderer hook", but merely *destroying* a resource after the hook is freed is a UAF. Consider a generation check or nulling back-pointers on teardown.


## Comment 5911284467

reporter (OWNER) · Nemirtingas · 2026-09-30T12:27:06Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5911284467

- **L15. Public API uses `std::function` members across the library boundary** (`RendererHook.h:129-130`) — already marked TODO by the author; ABI hazard across differing runtimes.


## Comment 5911285324

reporter (OWNER) · Nemirtingas · 2026-09-30T12:27:09Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5911285324

- **L16. macOS OpenGL detection edge**: `_HookOpenGL` (`RendererDetector.mm:248-270`) swizzles `NSOpenGLContext flushBuffer` *before* checking `CGLFlushDrawable`; if the CGL symbol were missing, `_OpenGLHook` is never created but the swizzled `_MyNSOpenGLContextFlushBuffer` → `_FoundOpenGLRenderer(true)` → `_OpenGLHook->LoadFunctions(...)` null-derefs. Mostly theoretical (CGL always exports it), but the ordering is free to fix. Metal-side dead code: `MetalHook.mm:336-339` contains `if (renderPass.CommandBuffer != self) continue;` nested inside `if (renderPass.CommandBuffer == self)`.


## Comment 5911286035

reporter (OWNER) · Nemirtingas · 2026-09-30T12:27:12Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5911286035

- **L17. Metal hooks only `presentDrawable:`** — games using `presentDrawable:atTime:`/`afterMinimumDuration:` (common with CAMetalLayer + display link) never trigger the overlay. Metal screenshots are silently unimplemented (`MetalHook.mm:303-306` always reports failure) — document in the public header.


## Comment 5911286968

reporter (OWNER) · Nemirtingas · 2026-09-30T12:27:16Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5911286968

- **L18. Vulkan descriptor allocator ignores allocation failure** (`VulkanHook.cpp:173-175`): `vkAllocateDescriptorSets` result unchecked and `UsedDescriptors++` regardless — a fragmented/free-set pool failure yields a null descriptor set handed to ImGui.


## Comment 5911287763

reporter (OWNER) · Nemirtingas · 2026-09-30T12:27:19Z · https://github.com/Nemirtingas/ingame_overlay/issues/77#issuecomment-5911287763

- **L19. Minor**: `RandomString` uses `int i` vs `size_t length` (`RendererDetector.cpp:146`); `_SendScreenshot` has no `Unknown` case so `PixelSize` is passed to the callback uninitialized when the format isn't recognized (`RendererHookInternal.cpp:48-71` — DX9's 16-bit-float back buffers, for instance, map to `Unknown`); `CMakeLists.txt` force-clears `CMAKE_C(XX)_STANDARD_LIBRARIES` cache-wide, which can surprise parent projects embedding this via `add_subdirectory`.

