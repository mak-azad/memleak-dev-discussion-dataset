# [DEV BUG] Memory leak in libprojectM (master branch) renderer arrays during manual playlist switches on Windows

- URL: https://github.com/projectM-visualizer/projectm/issues/1000
- Repo: projectM-visualizer/projectm (language: C++)
- State: open; created 2026-05-15T12:30:28Z; status ok; passes main

## Issue body

reporter (NONE) · HiroyukiHirohata · 2026-05-15T12:30:28Z · https://github.com/projectM-visualizer/projectm/issues/1000

### Please confirm the following points:

- [x] This report is NOT about the Android apps in the Play Store
- [x] I have [searched the project page](https://github.com/search?q=org%3AprojectM-visualizer+type%3Aissue+&type=issues) to check if the issue was already reported

### Affected Project

libprojectM (including the playlist library)

### Affected Version

4.1.6

### Operating Systems and Architectures

Windows (x64)

### Build Tools

Compiler: Microsoft Windows SDK

### Additional Project, OS and Toolset Details

_No response_

### Type of Defect

Specific bug in projectM code (please link the code in question)

### Log Output

```shell

```

### Describe the Issue

Summary
Memory leak identified in libprojectM 4.1.6 during continuous playlist-driven preset transitions on Windows. Memory usage climbs linearly from an 80MB baseline to over 1.2GB within a 7-8 hour window.
Environment
Library Version: libprojectM v4.1.6 Core Release
Operating System: Windows 11 x64
IDE / Toolchain: Visual Studio 2026 / MSVC Compiler

How to Reproduce
The leak occurs when disabling projectM's internal auto-transitioning and driving preset switches authoritatively from the application layer using a Win32 timer:

Instantiate the engine and immediately lock preset switching:
projectm_set_preset_locked(m_pProjectM, true);

Set up a standard Win32 WM_TIMER callback.
Every interval (e.g., matching preset durations), manually call:
projectm_playlist_play_next(m_pProjectM, false);

Observe memory usage over time via Task Manager or Diagnostic Tools.

Visual Studio Diagnostic Profiler Evidence
A heap snapshot differential taken between preset transition cycles reveals that while parent container structures are torn down, primitive array allocations inside the renderer namespace accumulate indefinitely on the process heap.
Here is the raw data dump from the Visual Studio 2026 Memory Profiler Diff (sorted by size impact):

void	4094	93016
projectM-4d.dll!libprojectM::Renderer::Color[]	10	84811
projectM-4d.dll!libprojectM::Renderer::Point[]	18	52042
char[]	172	20327
unsigned int[]	4	16007
projectM-4d.dll!libprojectM::MilkdropPreset::MilkdropPreset	1	15632
projectM-4d.dll!M4::HLSLTree::NodePage	2	8208
projectM-4d.dll!libprojectM::Renderer::TextureUV[]	3	6255
projectM-4d.dll!libprojectM::MilkdropPreset::CustomShape	4	5920
projectM-4d.dll!libprojectM::MilkdropPreset::CustomWaveform	4	5440
projectM-4d.dll!std::_Container_proxy	173	2768
projectM-4d.dll!libprojectM::MilkdropPreset::MilkdropShader	2	1840
char *[]	1	1464
projectM-4d.dll!std::_Ref_count_obj2<libprojectM::Renderer::Texture>	11	1056
projectM-4d.dll!M4::HLSLMacro *[]	1	736
projectM-4d.dll!std::_Tree_node<std::pair<unsigned int const ,std::shared_ptr<libprojectM::Renderer::TextureAttachment> >,void *>	8	448
projectM-4d.dll!std::_Tree_node<std::pair<int const ,std::map<unsigned int,std::shared_ptr<libprojectM::Renderer::TextureAttachment>,std::less<unsigned int>,std::allocator<std::pair<unsigned int const ,std::shared_ptr<libprojectM::Renderer::TextureAttachment> > > > >,void *>	7	448
projectM-4d.dll!std::_Tree_node<std::basic_string<char,std::char_traits<char>,std::allocator<char> >,void *>	4	288
projectM-4d.dll!std::_Ref_count_obj2<libprojectM::Renderer::TextureAttachment>	5	280
projectM-4d.dll!libprojectM::Renderer::TextureSamplerDescriptor	2	240
projectM-4d.dll!std::_Tree_node<std::pair<int const ,libprojectM::Renderer::TextureSamplerDescriptor>,void *>	1	160
projectM-4d.dll!std::_Tree_node<std::pair<M4::matrixCtor const ,std::basic_string<char,std::char_traits<char>,std::allocator<char> > >,void *>	1	112
projectM-4d.dll!std::_Ref_count_obj2<libprojectM::Renderer::Sampler>	2	64
bool *[]	1	64
projectM-4-playlistd.dll!std::_List_node<unsigned int,void *>	1	24
projectM-4-playlistd.dll!std::_Container_proxy	1	16
bool[]	1	16
unsigned int	2	8
char	1	1

Technical Observation
The numbers indicate a clear structural correlation. For every single new MilkdropPreset initialized, the system accumulates a matching set of CustomShape (+4) and CustomWaveform (+4) allocations.
Crucially, the raw vertex-drawing arrays associated with them (Color[] and Point[]) are left abandoned on the heap with positive count deltas. This confirms that while the parent objects are tracked, their low-level heap arrays lack a matching delete[] invocation during the transition sequence.
Technical Analysis
Since ~CustomShape() inside CustomShape.hpp is properly declared as a defaulted virtual destructor (virtual ~CustomShape() = default;), the parent wrapper object drops correctly.
However, the raw coordinate and color arrays (Color[], Point[]) used to instantiate the meshes for waveforms and shape elements are persisting on the system heap. This suggests that during a manual track change, the rendering pipeline misses an explicit array deallocation step (delete[]) or drops pointers before freeing the underlying memory boundaries of the active shader canvas elements.

## Comment 4461593772

maintainer (MEMBER) · kblaschke · 2026-05-15T16:44:25Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-4461593772

This has already been fixed in the main development branch by completely outsourcing vertex buffers into separate management classes which properly allocate & destroy the buffers.

I'll have a look into this leak though, as it's definitely not a great situation. Will fix it and then release projectM 4.1.7.

## Comment 4467692941

maintainer (MEMBER) · kblaschke · 2026-05-16T18:01:39Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-4467692941

There are no classes `Renderer::Color` or ` Renderer::TextureUV` in libprojectM release 4.1.6 - are you absolutely sure you're using the correct code base? These classes only exist in the master branch as of now.

Could you please download the actual release TGZ below and re-run the memory profiler on this?

https://github.com/projectM-visualizer/projectm/releases/download/v4.1.6/libprojectM-4.1.6.tar.gz

Alternatively, you can check out commit https://github.com/projectM-visualizer/projectm/commit/3158ee615eaafd93a8912b5f6dd84a9c47b2e00a.

## Comment 4476758135

reporter (NONE) · HiroyukiHirohata · 2026-05-18T10:28:38Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-4476758135

thanks for the response,
I downloaded the source code from the following URL
In Assets section on the page https://github.com/projectM-visualizer/projectm/releases
"Source Code (zip)" link, that is,
https://github.com/projectM-visualizer/projectm/archive/refs/tags/v4.1.6.zip

I will download the package you mentioned instead and recompile, then re-run the profiler.


## Comment 4517613705

maintainer (MEMBER) · kblaschke · 2026-05-22T09:50:24Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-4517613705

Any new findings yet?

## Comment 4523530248

reporter (NONE) · HiroyukiHirohata · 2026-05-23T00:30:03Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-4523530248

No, no progress.
struggling with unresolved openGL API with 4.1.6
I think, glew32 and some initialization code is needed.
IMHO, I want to deploy the master (4.2 ?) instead, that is working ok except for a leak.


## Comment 4561588014

maintainer (MEMBER) · kblaschke · 2026-05-28T07:09:18Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-4561588014

In 4.1.6, you have to call `glewInit()` once on Windows in your application before creating the projectM instance. Additionally, the application also needs to link against the same glew library as projectM.

The master branch no longer uses glew, but glad instead and thus doesn't require additional init code. It'll dynamically load opengl32.dll and resolve the required functions.

So I understand the leak is actually in the master branch, not in the stable release?

## Comment 5971651721

reporter (NONE) · HiroyukiHirohata · 2026-10-03T17:27:48Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-5971651721

took long since the last comment you gave. Am sorry
yes, the version number I mentioned in my initial report was wrong. Seems I was using the code of 4.2 master(dev) , not 4.1.6
Snippet of core.h header I compiled below

`/**
 * @brief Creates a new projectM instance using the given function to resolve GL api functions.
 *
 * The load_proc function accepts a function name and a user data pointer.
 * If this function returns NULL, in most cases the OpenGL context is not initialized, not made
 * current or insufficient to render projectM visuals.
 *
 * The OpenGL resolver is initialized on the first call to either projectm_create() or projectm_create_with_opengl_load_proc().
 * All projectM instances share the same resolver, and subsequent calls ignore the provided load_proc.
 *
 * @param load_proc Callback function used to resolve OpenGL function pointers. Optional, may be NULL.
 * @param user_data Custom user data pointer to pass along to the load_proc call, e.g. context information. Optional, may be NULL.
 * @return A projectM handle for the newly created instance that must be used in subsequent API calls.
 *         NULL if the instance could not be created successfully.
 * @since 4.2.0
 */
PROJECTM_EXPORT projectm_handle projectm_create_with_opengl_load_proc(projectm_load_proc load_proc, void* user_data);`

## Comment 5993232845

maintainer (MEMBER) · kblaschke · 2026-10-05T11:09:01Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-5993232845

Thanks for getting back on the issue! I've changed the issue title to say it's master that is affected, which more closely matches the report.

I've not yet run the new rendering code through valgrind as my local OS uses some modern CPU instructions valgrind can't properly emulate yet, but I'll check the code manually and see if I can find the problem.

## Comment 5997314643

maintainer (MEMBER) · kblaschke · 2026-10-05T15:12:18Z · https://github.com/projectM-visualizer/projectm/issues/1000#issuecomment-5997314643

Sorry, but I can't find any clue in the code that even matches your initial bug description:
> Technical Observation
> The numbers indicate a clear structural correlation. For every single new MilkdropPreset initialized, the system accumulates a matching set of CustomShape (+4) and CustomWaveform (+4) allocations.
Crucially, the raw vertex-drawing arrays associated with them (Color[] and Point[]) are left abandoned on the heap with positive count deltas. This confirms that while the parent objects are tracked, their low-level heap arrays lack a matching delete[] invocation during the transition sequence.
> Technical Analysis
> Since ~CustomShape() inside CustomShape.hpp is properly declared as a defaulted virtual destructor (virtual ~CustomShape() = default;), the parent wrapper object drops correctly.
However, the raw coordinate and color arrays (Color[], Point[]) used to instantiate the meshes for waveforms and shape elements are persisting on the system heap. This suggests that during a manual track change, the rendering pipeline misses an explicit array deallocation step (delete[]) or drops pointers before freeing the underlying memory boundaries of the active shader canvas elements.

The first thing that I can't find in both the 4.1 release and in master is that there are _no_ "raw vertex-drawing arrays" being used anywhere. since you're saying you've used code from master, the only instances of these classes are part of the VertexBuffer template specializations, and declared as `std::vector<Point>` and `std::vector<Color>`, respectively - thus, no raw array, but a proper STL container. Which in turn means that if the class is destroyed, the instances stored in the vector will also be cleaned automatically. Note that the vertex buffers are members of the `Mesh` class being used in both the `CustomWave` and `CustomShape` classes. Again, no raw arrays/pointers (with `new`) being used in the whole class hierarchy.
Then you again say "low-level heap arrays" - I can't find any in these classes.

Under "Technical Analysis", you again say " the raw ... arrays ... used to instantiate the meshes" - which I can't find either. The mesh is initialized via the `Mesh` members of both [`CustomShape`](https://github.com/projectM-visualizer/projectm/blob/dd89dfba0852c0c7e0c4e668929118d91ec3a3f0/src/libprojectM/MilkdropPreset/CustomShape.cpp#L13-L26) and [`CustomWaveform`](https://github.com/projectM-visualizer/projectm/blob/dd89dfba0852c0c7e0c4e668929118d91ec3a3f0/src/libprojectM/MilkdropPreset/CustomWaveform.cpp#L16-L28), which is basically a call to `std::vector::resize()`. Again - no raw arrays and no direct call to `new` is involved here.

Additionally, a manual preset change uses the _exact same function_ in libprojectM as an automatic change, because the library itself _isn't able to automatically load a new preset_. libprojectM will inform the application (or the projectM playlist library) that it _wants_ to change the preset, and then the application (or playlist library) will call the respective preset load function with either a file name or the preset contents. A preset switch can then be done immediately ("hard cut"), which will skip the transition shader, or with a transition, which will play both presets for a short duration. In both cases, after the transition is finished, the old preset will be destroyed.

### TL;DR:

I'll keep the bug open for now, and see if I can run this in Valgrind so see if there are any leaks being reported. I can't totally dismiss that, since memory profilers rarely give false positives (may happen in certain static allocation and shared library loading scenarios), so this might be a real thing.

If you could re-run your initial profiling with the current master branch, and actually pinpoint the allocation locations of the lost memory to specific lines of code, that would be really helpful. If Valgrind doesn't show anything, I'd rather consider this a fluke and close the issue in this case.
