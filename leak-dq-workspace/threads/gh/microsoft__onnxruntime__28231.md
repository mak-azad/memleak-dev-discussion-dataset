# [Performance] [CPU EP][Apple Silicon][MLAS/KleidiAI] Process phys_footprint grows continuously with fresh changing inputs on M5 Pro

- URL: https://github.com/microsoft/onnxruntime/issues/28231
- Repo: microsoft/onnxruntime (language: C++)
- State: closed; created 2026-04-26T05:50:38Z; status ok; passes offcwe

## Issue body

reporter (NONE) · hiugiak · 2026-04-26T05:50:38Z · https://github.com/microsoft/onnxruntime/issues/28231

### Describe the issue

Hi, I observed sustained RSS / dirty memory growth on Apple Silicon when repeatedly running an object detection model with the CPU Execution Provider.

I am not familiar with ONNX Runtime internals, MLAS, or KleidiAI. I am only reporting what I observed while using ONNX Runtime to run a model.

The issue reproduces on:

- Apple M5 Pro
- 48 GB memory
- macOS Tahoe 26.4.1

I did **not** observe the same issue on another machine:

- Apple M1 Pro
- 16 GB memory
- macOS Tahoe 26.4.1

### To reproduce

Minimal Rust repro: https://github.com/hiugiak/ort-cpu-ep-memory-repro

```sh
git clone https://github.com/hiugiak/ort-cpu-ep-memory-repro.git
cd ort-cpu-ep-memory-repro
./scripts/download-yolov8n.sh

cargo run --release -- \
  /path/to/libonnxruntime.dylib \
  models/yolov8n.onnx \
  1 \
  20
```

Arguments:

```sh
ort-cpu-ep-memory-repro <libonnxruntime.dylib> <model.onnx> [intra_threads] [print_every]
```

The repro is intentionally minimal:

- load ONNX Runtime dynamically
- register CPU Execution Provider
- load a public YOLOv8n ONNX model
- generate a fresh random `[1, 3, 640, 640]` `f32` input tensor every iteration
- call `Session::run` repeatedly
- extract the first output tensor
- print RSS periodically

With fresh changing inputs, RSS / dirty memory keeps growing on the M5 Pro machine. In Instruments, the growing allocations appear under the CPU EP / MLAS / KleidiAI convolution path.

In my original application, switching to CoreML Execution Provider first, with CPU as fallback, stopped the memory growth.

I am not sure whether this is a leak, an unbounded cache, or expected MLAS/KleidiAI workspace behavior, but I would not expect memory to keep growing because only input tensor values change while the model shape remains fixed.

### Urgency

Not blocking production because I can work around it by using CoreML Execution Provider first on Apple Silicon, with CPU as fallback.

However, I would like to understand whether the CPU EP behavior is expected, a known cache behavior, or a bug.

### Platform

Mac

### OS Version

macOS Tahoe 26.4.1

### ONNX Runtime Installation

Released Package

### ONNX Runtime Version or Commit ID

1.24.4

### ONNX Runtime API

Other / Unknown

### Architecture

ARM64

### Execution Provider

Default CPU

### Execution Provider Library Version

_No response_

### Model File

Public YOLOv8n ONNX model.

The repro script downloads:

```sh
https://huggingface.co/webml/yolov8n/resolve/main/onnx/yolov8n.onnx
```

### Is this a quantized model?

No

## Comment 4347942731

maintainer (MEMBER) · hariharans29 · 2026-04-29T22:19:22Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4347942731

Do you see the same behavior with previous versions of ORT ? KleidiAI is a newer component, so it'd help if you could please try 1.22-1.25 (also worth trying the latest 1.25 release, I see that you're on 1.24.4) to narrow it down to KleidiAI.

Alternatively, we have an option for the user to opt out of using KleidiAI with a simple session option (`mlas.disable_kleidiai`). Please see https://github.com/microsoft/onnxruntime/pull/27136. if you see the behavior going away with that, it is tied to KleidiAI

I ll pass this information along to the KleidiAI team just in case. CC: @damdoo01-arm @Colm-in-Arm


## Comment 4356497756

other (CONTRIBUTOR) · Colm-in-Arm · 2026-04-30T22:07:39Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4356497756

Hello @hiugiak

I didn't try your reproducer yet but I did a quick run using onnxruntime_perf_test on an M4. Initially up to 1000 iterations I could see a gentle increase in RSS memory usage. However, at that point it started to plateau. Continuing up to 10,000 iterations there were more increases in usage but I didn't detect a strong correlation to the number of inferences being executed.

If you could try @hariharans29 suggestion of using a session parameter to disable KleidiAI and trying again.

Colm.

## Comment 4379723551

other (CONTRIBUTOR) · JonathanC-ARM · 2026-05-05T13:30:45Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4379723551

Hi @hiugiak,

I was able to reproduce behavior similar to what you described above. I tracked it down to an issue in how we were caching LHS values, and I’ve opened PR #28363 to address it:


Could you try the proposed fix from the PR and let me know whether it resolves the issue on your end?

Best regards,
Jonathan

## Comment 4387473521

reporter (NONE) · hiugiak · 2026-05-06T11:24:53Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4387473521

Hi @JonathanC-ARM,

 I'd like to help, but I don’t know how to try the proposed fix. Compile the dynamic library by myself?

## Comment 4387636320

reporter (NONE) · hiugiak · 2026-05-06T11:51:50Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4387636320

Hi @hariharans29 @Colm-in-Arm , sorry for missing your replies. 

In my original description I said that RSS keeps growing continuously. After adding an additional macOS memory metric to the repro, I need to correct that wording.

The repro now prints both:

- `rss`: `mach_task_basic_info.resident_size`
- `footprint`: `proc_pid_rusage(..., RUSAGE_INFO_V4, ...).ri_phys_footprint`

With the same CPU EP repro, `rss` grows rapidly at first, but later starts to plateau. However, `phys_footprint` continues to grow almost linearly and matches what Activity Monitor shows in the "Memory" column.

Example:

```text
iter=1200, rss=23174.1 MB, footprint=22832.6 MB
iter=1300, rss=24087.0 MB, footprint=24747.1 MB
iter=1400, rss=22747.2 MB, footprint=26664.8 MB
iter=1800, rss=18824.3 MB, footprint=34346.2 MB
iter=2200, rss=14394.1 MB, footprint=41694.7 MB
iter=2600, rss=10424.6 MB, footprint=49367.9 MB
...
```

I also tried the latest release, and the issue still reproduces.

## Comment 4395604001

other (CONTRIBUTOR) · JonathanC-ARM · 2026-05-07T08:49:35Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4395604001

> Hi [@JonathanC-ARM](https://github.com/JonathanC-ARM),
> 
> I'd like to help, but I don’t know how to try the proposed fix. Compile the dynamic library by myself?

Hi @hiugiak,

Unfortunately the only way to test this would be to compile the dylib locally and test with your script that is until this is merged and makes it into a release.

To compile the lib on MacOS the following command would do, that should create a build folder at the root of the onnxruntime repo under which there will be a .dylib for the that particular version of onnxruntime, latest that I checked this morning shows up as `libonnxruntime.1.27.0.dylib`. 
`./build.sh --config Release --build_shared_lib --parallel --skip_tests`

In terms of getting the code to test you would need to clone my fork of the repo and checkout to this branch, or add my fork as an additional remote in your git config within an onnxruntime repo https://github.com/JonathanC-ARM/onnxruntime/tree/jonclo01/gh_issue_28231_repro or of course manually copy over the changes from the PR specifically the convolve_kleidiai.cpp changes

However saying that I've tested this issue locally using both my own method and your reproduction repo
This was the observed behavior before the fix with your reproduction repo
```
ort_library=../libonnxruntime.1.27.0.dylib
model=models/yolov8n.onnx
input=noise: fresh random tensor per iteration
intra_threads=1
print_every=100
rss_start_mb=40.2
footprint_start_mb=23.7
iter=100, elapsed=4.1s, rss=2217.5 MB, footprint=1701.8 MB
iter=200, elapsed=8.2s, rss=2522.1 MB, footprint=3879.9 MB
iter=300, elapsed=12.1s, rss=2933.2 MB, footprint=6017.3 MB
iter=400, elapsed=16.2s, rss=3382.0 MB, footprint=7975.9 MB
iter=500, elapsed=20.0s, rss=5310.0 MB, footprint=9915.3 MB
iter=600, elapsed=24.0s, rss=5272.7 MB, footprint=11868.3 MB
```
This is the behavior after the fix

```
ort_library=../libonnxruntime.1.27.0.dylib
model=models/yolov8n.onnx
input=noise: fresh random tensor per iteration
intra_threads=1
print_every=100
rss_start_mb=40.4
footprint_start_mb=23.8
iter=100, elapsed=5.1s, rss=380.9 MB, footprint=52.9 MB
iter=200, elapsed=10.2s, rss=380.9 MB, footprint=52.9 MB
iter=300, elapsed=15.3s, rss=380.9 MB, footprint=52.9 MB
iter=400, elapsed=20.4s, rss=380.9 MB, footprint=52.9 MB
iter=500, elapsed=25.5s, rss=380.9 MB, footprint=52.9 MB
iter=600, elapsed=30.5s, rss=380.9 MB, footprint=52.9 MB
iter=700, elapsed=35.5s, rss=380.9 MB, footprint=52.9 MB
iter=800, elapsed=40.4s, rss=380.9 MB, footprint=52.9 MB
iter=900, elapsed=45.5s, rss=380.9 MB, footprint=52.9 MB
iter=1000, elapsed=50.7s, rss=380.9 MB, footprint=52.9 MB
iter=1100, elapsed=55.7s, rss=380.9 MB, footprint=52.9 MB
iter=1200, elapsed=60.8s, rss=380.9 MB, footprint=52.9 MB
iter=1300, elapsed=66.0s, rss=381.8 MB, footprint=53.8 MB
iter=1400, elapsed=70.8s, rss=381.8 MB, footprint=53.8 MB
iter=1500, elapsed=75.2s, rss=381.8 MB, footprint=53.8 MB
iter=1600, elapsed=79.4s, rss=381.8 MB, footprint=53.8 MB
```

So it does look like this fix indeed addresses the issue in question.

Best Regards,
Jonathan

## Comment 4395661495

reporter (NONE) · hiugiak · 2026-05-07T08:58:05Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4395661495

@JonathanC-ARM that looks good. Then I guess I don't need to test.

## Comment 4423501175

maintainer (MEMBER) · hariharans29 · 2026-05-11T18:13:36Z · https://github.com/microsoft/onnxruntime/issues/28231#issuecomment-4423501175

Closing this as fix https://github.com/microsoft/onnxruntime/pull/28363 is merged. Please re-open in case the issue is unresolved.
