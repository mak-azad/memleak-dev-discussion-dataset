# Add zero-copy camera pipeline sample using NDK Camera2 and OpenGL ES

- URL: https://github.com/android/ndk-samples/issues/1172
- Repo: android/ndk-samples (language: C++)
- State: open; created 2026-09-13T20:26:12Z; status ok; passes offcwe

## Issue body

reporter (NONE) · MohammadNouri5700 · 2026-09-13T20:26:12Z · https://github.com/android/ndk-samples/issues/1172

Hi NDK Team,

I would like to propose adding a new sample demonstrating a high-performance, zero-copy camera rendering pipeline using the NDK camera2 APIs, AImageReader, and OpenGL ES.

**Motivation**
While the existing camera sample effectively demonstrates basic Native Camera2 usage, developers frequently face bottlenecks when attempting low-latency preview rendering, zero-copy frame processing, and synchronization between camera capture streams and the rendering thread.

**What the Sample Demonstrates**

- Zero-Copy Architecture: Leveraging native buffers (AHardwareBuffer / AImageReader) with OpenGL ES external textures (GL_OES_EGL_image_external) to avoid CPU-memory copy overhead.
- 
- Low-Latency Rendering: Clean separation of camera capture threads and rendering loops using standard Android NDK synchronization primitives.
- 
- Modern Best Practices: Minimal overhead, leak-free buffer recycling, and lifecycle-aware lifecycle management purely in C++ and NDK.

I have already implemented a working prototype in a standalone repository:

[https://github.com/MohammadNouri5700/zerostallcam](https://github.com/MohammadNouri5700/zerostallcam)

**Question**
Would the maintainers be open to accepting this as a new standalone sample in android/ndk-samples?

If so, I am ready to refactor the project to strictly align with this repository's structure, Gradle/CMake conventions, documentation style, and Google CLA requirements before submitting a Pull Request.

**Thank you for your time and feedback!**
