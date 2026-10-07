# Define application lifecycle and graceful shutdown behavior

- URL: https://github.com/L0932/ForgeSim/issues/17
- Repo: L0932/ForgeSim (language: C++)
- State: closed; created 2026-10-02T17:29:16Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · L0932 · 2026-10-02T17:29:16Z · https://github.com/L0932/ForgeSim/issues/17

## Objective

Define predictable application initialization and shutdown behavior for the interactive 3D Sandbox, including safe ownership and destruction of graphics resources.

## Current Context

Phase 2 introduces concrete OpenGL resources such as shader programs, vertex buffers, index buffers, and potentially textures.

`main()` currently handles top-level exception handling and exit status. `SandboxApplication` owns the window and coordinates the interactive loop.

The lifecycle contract should ensure that application and graphics resources are initialized and destroyed in a valid order without introducing a general subsystem-management framework.

## Implementation Notes

- Establish clear initialization, execution, and shutdown phases.
- Define ownership of window, context, rendering, scene, and application-level resources.
- Ensure OpenGL resources are destroyed while a valid OpenGL context still exists.
- Preserve top-level exception handling in `main()`.
- Handle partial initialization failures without leaking resources.
- Define behavior when `Run()` is called more than once.
- Prefer RAII and explicit ownership over global managers.
- Keep GLFW-specific lifecycle work inside the platform boundary where practical.

## Acceptance Criteria

- [x] Application initialization responsibilities are clearly defined
- [x] The interactive loop cannot be entered more than once per application instance
- [x] Normal window closure produces an orderly shutdown
- [x] Initialization failures return a failure exit status
- [x] Partially initialized resources are released safely
- [x] Graphics-resource ownership is explicit
- [x] OpenGL resources are destroyed before the OpenGL context
- [x] The window and GLFW state are destroyed in a valid order
- [x] Resource destruction order is deterministic
- [x] Normal shutdown, repeated `Run()` rejection, and initialization-failure cleanup are manually verified
- [x] Existing headless automated tests continue to pass
- [x] Clean Debug and Release builds succeed
- [x] Debug and Release tests pass
- [x] Changes are committed and pushed

## Out of Scope

- A global subsystem manager
- Dependency-injection infrastructure
- Multiple windows or contexts
- Application restart within the same process
- Graphics-resource hot reloading
- Multithreaded initialization or shutdown
- Complete editor lifecycle behavior

## Comment 6019025861

reporter (OWNER) · L0932 · 2026-10-06T14:58:12Z · https://github.com/L0932/ForgeSim/issues/17#issuecomment-6019025861

## Completion Summary

Application lifecycle and graceful shutdown behavior have been clarified and hardened.

### Changes

- Replaced the Debug-only `Run()` assertion with a `std::logic_error`, enforcing the single-run contract in Debug and Release.
- Made `SandboxApplication` explicitly non-copyable and non-movable.
- Corrected GLFW initialization so `glfwInit()` occurs before window hints are configured.
- Preserved cleanup for window-creation and OpenGL-loading failures.
- Documented application ownership, initialization, execution, shutdown, and graphics-resource destruction order.
- Documented that graphics resources must be destroyed before the window and OpenGL context.
- Deferred a general subsystem manager and dedicated Runtime lifecycle coordinator until concrete reuse requirements emerge.

### Validation

- Confirmed normal Sandbox startup and window closure.
- Confirmed repeated `Run()` attempts report an error.
- Confirmed window-creation failure is caught by `main()` and returns a failure exit status.
- Confirmed partially initialized GLFW state is released.
- Confirmed Debug and Release builds run successfully.
- Confirmed existing automated tests continue to pass.

Application restart within the same process, multiple windows, and graphics-resource hot reloading remain out of scope.
```
