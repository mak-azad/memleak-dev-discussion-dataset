# GPU memory leak with high load for ONNX model

- URL: https://github.com/triton-inference-server/onnxruntime_backend/issues/198
- Repo: triton-inference-server/onnxruntime_backend (language: C++)
- State: open; created 2023-06-14T20:10:31Z; status ok; passes offcwe

## Issue body

reporter (NONE) · junwang-wish · 2023-06-14T20:10:31Z · https://github.com/triton-inference-server/onnxruntime_backend/issues/198

**Description**
GPU memory leak with high load, GPU memory usage goes up and never come down when high load requests stop coming (memory never released)

**Triton Information**
What version of Triton are you using? 

23.02

Are you using the Triton container or did you build it yourself?

Triton container

**To Reproduce**
Any ONNX model under high load would result in monotonically increasing GPU memory usage

**Expected behavior**
When requests stop coming, GPU memory should be released


## Comment 1603411566

other (CONTRIBUTOR) · kthui · 2023-06-20T19:41:34Z · https://github.com/triton-inference-server/onnxruntime_backend/issues/198#issuecomment-1603411566

I wonder if the memory usage would come down if the model is unloaded (i.e. via the unload API).

cc @tanmayv25 if the memory usage is expected.

## Comment 1603411568

reporter (NONE) · junwang-wish · 2023-06-20T20:06:11Z · https://github.com/triton-inference-server/onnxruntime_backend/issues/198#issuecomment-1603411568

Thx @kthui , so I don't want to unload the model, since it is used but on a unfrequent basis, ideally if a model is unused for a prolonged period of time (say 2 hours) the GPU memory would be freed

## Comment 1603411571

other (CONTRIBUTOR) · tanmayv25 · 2023-06-22T22:56:38Z · https://github.com/triton-inference-server/onnxruntime_backend/issues/198#issuecomment-1603411571

@[junwang-wish](https://github.com/junwang-wish) which execution provider in ORT are you using? Are you using TRT or CUDA?
Is your model having dynamic shaped inputs?
I am transferring the issue to ORT backend team as it seems to be an issue with ORT.
