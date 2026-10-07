# GPU memory leak

- URL: https://github.com/dmlc/decord/issues/27
- Repo: dmlc/decord (language: C++)
- State: open; created 2020-02-28T22:02:19Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ternaus · 2020-02-28T22:02:19Z · https://github.com/dmlc/decord/issues/27

I am decoding a list of videos with:

```
video = VideoReader(str(video_path), ctx=gpu(0))

frame_ids = list(range(300))

frames = video.get_batch(frame_ids).asnumpy()
```

on every iteration, GPU Ram consumption goes up till I get `out of memory` error.


## Comment 592922863

other (CONTRIBUTOR) · leigh-plt · 2020-02-29T09:08:45Z · https://github.com/dmlc/decord/issues/27#issuecomment-592922863

Without .asnumpy() memory leak exist too. 
I use:
`frames = torch.utils.dlpack.from_dlpack(video.get_batch(frame_ids).to_dlpack())`
frames are located on gpu in this case

## Comment 593023894

maintainer (MEMBER) · zhreshold · 2020-03-01T00:43:47Z · https://github.com/dmlc/decord/issues/27#issuecomment-593023894

Can you guys post your cuda version/ decive type?
I have tried on my local machine with 1070ti and cuda 10.1.243, didn't notice any mem leak.
```python
from decord import VideoReader
from decord import cpu, gpu

video_path = '/home/joshua/Dev/decord/examples/flipping_a_pancake.mkv'

video = VideoReader(str(video_path), ctx=gpu(0))

frame_ids = list(range(300))

for i in range(100):
  frames = video.get_batch(frame_ids).asnumpy()
  if i % 10 == 0: 
    print(frames.shape)

```

nvidia-smi record can be viewed here:
https://asciinema.org/a/xgI8tFXNlpAoDcVJdxLgag8eW
GPU mem from 627M to 845M and pretty constant.

## Comment 595033894

other (NONE) · KeremTurgutlu · 2020-03-05T05:18:29Z · https://github.com/dmlc/decord/issues/27#issuecomment-595033894

Thanks @leigh-plt, I modified batch loading seems to be ok in notebook environment of Kaggle after `dl_pack` trick:
```
def get_decord_video_batch(fname, sz, freq=10):
    "get batch tensor for inference, original for cropping and H,W of video"
    video = VideoReader(str(fname), ctx=gpu())
#     data = video.get_batch(range(0, len(video), 10))
    data = from_dlpack(to_dlpack(video.get_batch(range(0, len(video), 10))))
    H,W = data.shape[2:]
    del video; gc.collect()
    return (data, None, (H, W))
```

Although I had one successful run there had been unsuccessful runs after that. How can we fix it?

## Comment 595855074

other (NONE) · akansal1 · 2020-03-06T16:43:36Z · https://github.com/dmlc/decord/issues/27#issuecomment-595855074

facing memory leak issues of CPU, on GPU working fine

## Comment 598780732

other (NONE) · yitang · 2020-03-13T15:30:35Z · https://github.com/dmlc/decord/issues/27#issuecomment-598780732

facing the same issues, neither dl_pack nor asnumpy work for me.

@KeremTurgutlu i'm on the kaggle env as well.  

## Comment 598811477

maintainer (MEMBER) · zhreshold · 2020-03-13T16:38:04Z · https://github.com/dmlc/decord/issues/27#issuecomment-598811477

Can you guys post the kaggle gpu and cuda version?

## Comment 598819964

other (NONE) · yitang · 2020-03-13T16:57:16Z · https://github.com/dmlc/decord/issues/27#issuecomment-598819964

the gpu is  Tesla P100-PCIE-16GB.

cuda is  10.0.130.

this is the traceback:

[16:44:39] /kaggle/working/reader/src/video/nvcodec/cuda_threaded_decoder.cc:55: Kernel module version 418.67, so using our own stream.


  7%|▋         | 27/400 [00:23<03:55,  1.58it/s][16:44:40] /kaggle/working/reader/src/video/nvcodec/cuda_threaded_decoder.cc:35: Using device: Tesla P100-PCIE-16GB

[16:44:40] /kaggle/working/reader/src/video/nvcodec/cuda_threaded_decoder.cc:55: Kernel module version 418.67, so using our own stream.


  7%|▋         | 28/400 [00:24<03:51,  1.61it/s][16:44:41] /kaggle/working/reader/src/video/nvcodec/cuda_threaded_decoder.cc:35: Using device: Tesla P100-PCIE-16GB

[16:44:41] /kaggle/working/reader/src/video/nvcodec/cuda_threaded_decoder.cc:55: Kernel module version 418.67, so using our own stream.

terminate called after throwing an instance of 'dmlc::Error'

  what():  [16:44:41] /kaggle/working/reader/src/video/nvcodec/cuda_threaded_decoder.cc:332: Check failed: arr.defined() 



Stack trace returned 10 entries:

[bt] (0) /kaggle/working/reader/build/libdecord.so(dmlc::StackTrace[abi:cxx11](unsigned long)+0x85) [0x7f15712ee059]

[bt] (1) /kaggle/working/reader/build/libdecord.so(dmlc::LogMessageFatal::~LogMessageFatal()+0x20) [0x7f15712ee334]

[bt] (2) /kaggle/working/reader/build/libdecord.so(decord::cuda::CUThreadedDecoder::ConvertThread()+0x1a5) [0x7f157135d659]

[bt] (3) /kaggle/working/reader/build/libdecord.so(void std::__invoke_impl<void, void (decord::cuda::CUThreadedDecoder::* const&)(), decord::cuda::CUThreadedDecoder*>(std::__invoke_memfun_deref, void (decord::cuda::CUThreadedDecoder::* const&)(), decord::cuda::CUThreadedDecoder*&&)+0x66) [0x7f15713669bc]

[bt] (4) /kaggle/working/reader/build/libdecord.so(std::result_of<void (decord::cuda::CUThreadedDecoder::* const&(decord::cuda::CUThreadedDecoder*&&))()>::type std::__invoke<void (decord::cuda::CUThreadedDecoder::* const&)(), decord::cuda::CUThreadedDecoder*>(void (decord::cuda::CUThreadedDecoder::* const&)(), decord::cuda::CUThreadedDecoder*&&)+0x3f) [0x7f1571366949]

[bt] (5) /kaggle/working/reader/build/libdecord.so(decltype (__invoke((*this)._M_pmf, (forward<decord::cuda::CUThreadedDecoder*>)({parm#1}))) std::_Mem_fn_base<void (decord::cuda::CUThreadedDecoder::*)(), true>::operator()<decord::cuda::CUThreadedDecoder*>(decord::cuda::CUThreadedDecoder*&&) const+0x2e) [0x7f15713668fa]

[bt] (6) /kaggle/working/reader/build/libdecord.so(void std::_Bind_simple<std::_Mem_fn<void (decord::cuda::CUThreadedDecoder::*)()> (decord::cuda::CUThreadedDecoder*)>::_M_invoke<0ul>(std::_Index_tuple<0ul>)+0x43) [0x7f15713668c5]

[bt] (7) /kaggle/working/reader/build/libdecord.so(std::_Bind_simple<std::_Mem_fn<void (decord::cuda::CUThreadedDecoder::*)()> (decord::cuda::CUThreadedDecoder*)>::operator()()+0x1d) [0x7f1571366813]

[bt] (8) /kaggle/working/reader/build/libdecord.so(std::thread::_State_impl<std::_Bind_simple<std::_Mem_fn<void (decord::cuda::CUThreadedDecoder::*)()> (decord::cuda::CUThreadedDecoder*)> >::_M_run()+0x1c) [0x7f15713667f2]

[bt] (9) /opt/conda/lib/python3.6/site-packages/matplotlib/../../../libstdc++.so.6(+0xb8408) [0x7f157222e408]


## Comment 598944817

other (CONTRIBUTOR) · leigh-plt · 2020-03-13T22:08:28Z · https://github.com/dmlc/decord/issues/27#issuecomment-598944817

Ubuntu 19.04 last update drivers, cuda 10.2 have leak too. 730 gtx

Kaggle:
cuda_threaded_decoder.cc:35: Using device: Tesla P100-PCIE-16GB
cuda_threaded_decoder.cc:55: Kernel module version 418.67, so using our own stream.
OS debian  stretch

## Comment 599023568

other (NONE) · KeremTurgutlu · 2020-03-14T07:41:30Z · https://github.com/dmlc/decord/issues/27#issuecomment-599023568

Thanks @leigh-plt this might be helpful for inference in the kernel!

## Comment 599135679

other (NONE) · yitang · 2020-03-14T21:14:32Z · https://github.com/dmlc/decord/issues/27#issuecomment-599135679

@leigh-plt are you writing a kernel on how to using video processing framwork too? 


## Comment 628240190

other (NONE) · anlarro · 2020-05-13T20:53:53Z · https://github.com/dmlc/decord/issues/27#issuecomment-628240190

Any updates on this? I am facing memory leak issues on CPU.

## Comment 688845902

other (NONE) · Black-Hack · 2020-09-08T12:53:13Z · https://github.com/dmlc/decord/issues/27#issuecomment-688845902

It seems that deleting the frame manually avoids the leak:
```python3
vr = VideoReader(video_path)
for frame in vr:
    print(frame.shape)
    del frame
```
Note: I tested it for CPU only, but from the source code it seems that this would be the case for GPU as well.

## Comment 700678177

other (NONE) · huang-ziyuan · 2020-09-29T12:45:30Z · https://github.com/dmlc/decord/issues/27#issuecomment-700678177

> It seems that deleting the frame manually avoids the leak:
> 
> ```python
> vr = VideoReader(video_path)
> for frame in vr:
>     print(frame.shape)
>     del frame
> ```
> 
> Note: I tested it for CPU only, but from the source code it seems that this would be the case for GPU as well.

Same issue with the CPU memory leak. If you deleted the frame, how do you further process this if it is to be applied into a deep learning training framework? 

## Comment 782899608

other (NONE) · Ehsan1997 · 2021-02-21T18:08:59Z · https://github.com/dmlc/decord/issues/27#issuecomment-782899608

> > It seems that deleting the frame manually avoids the leak:
> > ```python
> > vr = VideoReader(video_path)
> > for frame in vr:
> >     print(frame.shape)
> >     del frame
> > ```
> > 
> > 
> > Note: I tested it for CPU only, but from the source code it seems that this would be the case for GPU as well.
> 
> Same issue with the CPU memory leak. If you deleted the frame, how do you further process this if it is to be applied into a deep learning training framework?

Get a bunch of frames, train the model, get the next bunch.
