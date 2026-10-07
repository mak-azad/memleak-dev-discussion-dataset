# GPU memory leak when using gluon.data.DataLoader with num_workers>0

- URL: https://github.com/apache/mxnet/issues/20959
- Repo: apache/mxnet (language: C++)
- State: open; created 2022-03-14T18:29:39Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ann-qin-lu · 2022-03-14T18:29:39Z · https://github.com/apache/mxnet/issues/20959

## Description
GPU memory leak when using gluon.data.DataLoader after upgrading Cuda-11.1/Cudnn-8.2.x (also tested with latest Cuda11.5+CuDnn8.3.x but still leaking). Minimal code to repro attached below.

No memory leak with older Cuda version (Cuda-10.1 + CuDnn-7.6.5).

### Error Message
gpu memory keeps increasing during training. 

## To Reproduce
(If you developed your own code, please provide a short script that reproduces the error. For existing examples, please provide link.)
```
import mxnet.gluon as gl
import mxnet as mx
import gc

if __name__ == "__main__":
    gpu_ctx = mx.gpu()
    model = gl.nn.Embedding(10, 5)
    model.initialize(ctx=gpu_ctx)
    X = mx.random.uniform(shape=(1000, 3))
    dataset = mx.gluon.data.dataset.ArrayDataset(X)
    num_workers_list = [0, 4, 8]
    for num_workers in num_workers_list:

        for epoch in range(5):
            dataset = mx.gluon.data.dataset.ArrayDataset(X)
            data_loader = gl.data.DataLoader(
                dataset,
                batch_size=1,
                num_workers=num_workers,
            )
            for batch in data_loader:
                # move data to gpu
                data_gpu = batch.copyto(mx.gpu())
                # forward
                l = model(data_gpu)
                # force immediate compute
                l.asnumpy()
            # gc & gpu_ctx.empty_cache
            mx.nd.waitall()
            del dataset
            del data_loader
            gc.collect()
            gpu_ctx.empty_cache()
            mx.nd.waitall()

            a, b = mx.context.gpu_memory_info(0)
            print(f"num_workers: {num_workers} epoch {epoch}: "
                  f"current gpu memory {(b - a) / (1024 * 1024 * 1024)} GB, "
                  f"Total gpu memory {b / (1024 * 1024 * 1024)} GB.")
```

### Steps to reproduce
(Paste the commands you ran that produced the error.)
```
### Output with MXNet-1.9 built with Cuda11.1 CuDnn 8.2.0 (Memory leak when `num_workers` > 0)
  (also tested with the latest Cuda11.5+CuDnn8.3.x)

num_workers: 0 epoch 0: current memory 1.381591796875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 1: current memory 1.381591796875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 2: current memory 1.381591796875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 3: current memory 1.381591796875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 4: current memory 1.381591796875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 0: current memory 1.483154296875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 1: current memory 1.582763671875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 2: current memory 1.683349609375 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 3: current memory 1.782958984375 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 4: current memory 1.880615234375 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 0: current memory 1.980224609375 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 1: current memory 2.080810546875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 2: current memory 2.180419921875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 3: current memory 2.281982421875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 4: current memory 2.380615234375 GB, Total memory 15.78173828125 GB.
  

### Output with MXNet-1.9 built with Cuda10.1 CuDnn 7.6.5 (No memory leak)

num_workers: 0 epoch 0: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 1: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 2: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 3: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 0 epoch 4: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 0: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 1: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 2: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 3: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 4 epoch 4: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 0: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 1: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 2: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 3: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.
num_workers: 8 epoch 4: current memory 1.301513671875 GB, Total memory 15.78173828125 GB.

```


## What have you tried to solve it?

1. python gc clean doesn't help
2. upgrade cuda/cudnn to least version doesn't help

## Environment

***We recommend using our script for collecting the diagnostic information with the following command***
`curl --retry 10 -s https://raw.githubusercontent.com/apache/incubator-mxnet/master/tools/diagnose.py | python3`
<details>
<summary>Environment Information</summary>

```
# Paste the diagnose.py command output here
```

```
----------Python Info----------
Version      : 3.6.14
Compiler     : GCC 7.5.0
Build        : ('default', 'Feb 19 2022 10:06:15')
Arch         : ('64bit', 'ELF')
------------Pip Info-----------
No corresponding pip install for current python.
----------MXNet Info-----------
Version      : 1.9.0
Directory    : /efs-storage/debug_log/test-runtime/lib/python3.6/site-packages/mxnet
Commit hash file "/efs-storage/debug_log/test-runtime/lib/python3.6/site-packages/mxnet/COMMIT_HASH" not found. Not installed from pre-built package or built from source.
Library      : ['/efs-storage/debug_log/test-runtime//lib/libmxnet.so']
Build features:
✔ CUDA
✔ CUDNN
✖ NCCL
✖ CUDA_RTC
✖ TENSORRT
✔ CPU_SSE
✔ CPU_SSE2
✔ CPU_SSE3
✖ CPU_SSE4_1
✖ CPU_SSE4_2
✖ CPU_SSE4A
✖ CPU_AVX
✖ CPU_AVX2
✔ OPENMP
✖ SSE
✖ F16C
✖ JEMALLOC
✔ BLAS_OPEN
✖ BLAS_ATLAS
✖ BLAS_MKL
✖ BLAS_APPLE
✔ LAPACK
✔ MKLDNN
✔ OPENCV
✖ CAFFE
✖ PROFILER
✖ DIST_KVSTORE
✖ CXX14
✖ INT64_TENSOR_SIZE
✔ SIGNAL_HANDLER
✖ DEBUG
✖ TVM_OP
----------System Info----------
Platform     : Linux-4.14.232-177.418.amzn2.x86_64-x86_64-with
system       : Linux
node         : ip-10-0-10-233.ec2.internal
release      : 4.14.232-177.418.amzn2.x86_64
version      : #1 SMP Tue Jun 15 20:57:50 UTC 2021
----------Hardware Info----------
machine      : x86_64
processor    : x86_64
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              64
On-line CPU(s) list: 0-63
Thread(s) per core:  2
Core(s) per socket:  16
Socket(s):           2
NUMA node(s):        2
Vendor ID:           GenuineIntel
CPU family:          6
Model:               79
Model name:          Intel(R) Xeon(R) CPU E5-2686 v4 @ 2.30GHz
Stepping:            1
CPU MHz:             2630.103
CPU max MHz:         3000.0000
CPU min MHz:         1200.0000
BogoMIPS:            4600.04
Hypervisor vendor:   Xen
Virtualization type: full
L1d cache:           32K
L1i cache:           32K
L2 cache:            256K
L3 cache:            46080K
NUMA node0 CPU(s):   0-15,32-47
NUMA node1 CPU(s):   16-31,48-63
Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon rep_good nopl xtopology nonstop_tsc cpuid aperfmperf pni pclmulqdq monitor est ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch cpuid_fault invpcid_single pti fsgsbase bmi1 hle avx2 smep bmi2 erms invpcid rtm rdseed adx xsaveopt ida
```
</details>


## Comment 1067152699

other (NONE) · github-actions[bot] · 2022-03-14T18:30:22Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1067152699

Welcome to Apache MXNet (incubating)! We are on a mission to democratize AI, and we are glad that you are contributing to it by opening this issue.
Please make sure to include all the relevant context, and one of the @apache/mxnet-committers will be here shortly.
If you are interested in contributing to our project, let us know! Also, be sure to check out our guide on [contributing to MXNet](https://mxnet.apache.org/community/contribute) and our [development guides wiki](https://cwiki.apache.org/confluence/display/MXNET/Developments).

## Comment 1067165130

reporter (NONE) · ann-qin-lu · 2022-03-14T18:44:54Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1067165130

Some additional resources I've found:

* This is a similar [issue](https://github.com/apache/incubator-mxnet/pull/19924) for CPU memory leak with the MultiWorker setup in DataLoader. The solution was to add the python gc to clean up the memory, however this solution doesn't work for GPU. 
* The Cudnn release [note](https://docs.nvidia.com/deeplearning/cudnn/release-notes/rel_8.html#rel_8) mentions a new buffer management that might affect the Cuda>=10.2, which seems to be related. And the issue only surfaces after I upgrade Cuda version (tested with Cuda10.2/Cuda11.1/Cuda11.5, and all 3 have memory leak issue).

## Comment 1068589538

other (CONTRIBUTOR) · mseth10 · 2022-03-16T00:11:53Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1068589538

@TristonC 

## Comment 1069231854

reporter (NONE) · ann-qin-lu · 2022-03-16T15:09:00Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1069231854

one additional finding is that the memory leak happens with the default thread_pool option set as False (a.k.a leak when using the [multiprocessing.Pool](https://github.com/apache/incubator-mxnet/blame/master/python/mxnet/gluon/data/dataloader.py#L665)), if I switch to use [ThreadPool](https://github.com/apache/incubator-mxnet/blame/master/python/mxnet/gluon/data/dataloader.py#L659), there is no memory leak any more! This could be a good indicate for the issue in shared memory. 

## Comment 1069279656

other (CONTRIBUTOR) · samskalicky · 2022-03-16T15:46:22Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1069279656

@ptrendx not that its your fault, but you had the most recent commit in the dataloader code: https://github.com/apache/incubator-mxnet/blob/v1.9.x/python/mxnet/gluon/data/dataloader.py#L654-L657 do you have any thoughts here about this memory leak issue?

## Comment 1069387685

other (CONTRIBUTOR) · TristonC · 2022-03-16T17:36:57Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1069387685

We are checking this issue. Thanks for the feedback @ann-qin-lu. It does look like more of multiprocessing package related. 

## Comment 1069830658

other (CONTRIBUTOR) · TristonC · 2022-03-17T01:59:30Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1069830658

@ann-qin-lu  I did repro the same behavior as you mentioned in your comments. We don't have the conclusion now. If you need the workaround, use the thread_pool might be a good choice. Thanks. 

## Comment 1069874455

reporter (NONE) · ann-qin-lu · 2022-03-17T02:17:41Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1069874455

Hi @TristonC, thanks a ton for looking into the issue. I tried with thread_pool option, and it did work without memory leak. However, since the thread_pool option is slow in preparing the data, I do observe the increased E2E latency (mostly increased during validation time). My production use cases are very sensitive to the training time, and we'd still like to explore the option for multiprocess.Pool (assume the memory leak issue can be resolved soon).

Do you have any hunch about what changes in Cuda/Cudnn that might lead to this issue?

## Comment 1071082032

other (CONTRIBUTOR) · TristonC · 2022-03-17T16:55:05Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1071082032

@ann-qin-lu 
Do you have any hunch about what changes in Cuda/Cudnn that might lead to this issue?

Not that I have been aware of. I will seek help from related NVIDIA teams. Stay tuned.

## Comment 1072914204

other (CONTRIBUTOR) · waytrue17 · 2022-03-19T01:37:20Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1072914204

Tested the above script on two mxnet nightly builds:
1. [mxnet_cu112-1.9.0b20220227-py3-none-manylinux2014_x86_64.whl](https://repo.mxnet.io/dist/python/cu112/mxnet_cu112-1.9.0b20220227-py3-none-manylinux2014_x86_64.whl) - no memory issue.
2. [mxnet_cu112-1.9.0b20220301-py3-none-manylinux2014_x86_64.whl](https://repo.mxnet.io/dist/python/cu112/mxnet_cu112-1.9.0b20220301-py3-none-manylinux2014_x86_64.whl) - has memory issue.

This may indicate that the issue was introduced by the commits in between 02/27 to 03/01. Possibly: https://github.com/apache/incubator-mxnet/commit/8041c0da75cd146ebd578c7bee13af25dc231a98 

## Comment 1072926185

reporter (NONE) · ann-qin-lu · 2022-03-19T03:02:28Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1072926185

After more deep dives, this issue is actually not caused by cuda upgrade from 10 to 11, but introduced by this specific [commit: Remove cleanup on side threads](https://github.com/apache/incubator-mxnet/pull/19378), which skips the cuda deinitialization when destructing engine. I've confirmed that after reverting this commit, the memory leak issue is gone.

I'll work with MXNet team to see if this commit should be reverted in both MxNet master and 1.9 branch. (actually another user reported similar memory [issue](https://github.com/apache/incubator-mxnet/issues/19420) when using the multiprocessing and tried to [revert](https://github.com/apache/incubator-mxnet/pull/19432) this commit). Here is the open [issue](https://github.com/apache/incubator-mxnet/issues/19379) for better handling the engine destruction, which needs to be addressed first if the above workaround will be reverted.


## Comment 1072926312

reporter (NONE) · ann-qin-lu · 2022-03-19T03:03:21Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1072926312

@TristonC False alarm on the Cuda version. Thanks a lot for your help!

## Comment 1074140831

other (CONTRIBUTOR) · TristonC · 2022-03-21T16:43:30Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1074140831

Thanks @ann-qin-lu for your update.  I will address issue issue with the MXNet team soon.

## Comment 1074580675

other (CONTRIBUTOR) · TristonC · 2022-03-22T01:10:51Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1074580675

I wonder you might be interested in digger little deeper @ann-qin-lu. It seems current gluon dataloader using fork to start a worker process in multiprocessing.Pool(..) function call (as it is default in Unix-like system). It might be a problem for this issue as the child process inherit everything from its parent process. It might be a good idea to use spawn instead of using fork this function. Unfortunately, I ran into a issue that blocks my test of multiprocessing.get_context('spawn').Pool(...) . 
```bash
Traceback (most recent call last):                                                                                                                                   
File "<string>", line 1, in <module>
File "/usr/lib/python3.8/multiprocessing/spawn.py", line 116, in spawn_main
exitcode = _main(fd, parent_sentinel)                                                                                                                            
File "/usr/lib/python3.8/multiprocessing/spawn.py", line 126, in _main 
self = reduction.pickle.load(from_parent)                                                                                                                       
File "/opt/mxnet/python/mxnet/gluon/data/dataloader.py", line 58, in rebuild_ndarray
return nd.NDArray(nd.ndarray._new_from_shared_mem(pid, fd, shape, dtype))
File "/opt/mxnet/python/mxnet/ndarray/ndarray.py", line 193, in _new_from_shared_mem 
check_call(_LIB.MXNDArrayCreateFromSharedMemEx(                                                                                                                 
File "/opt/mxnet/python/mxnet/base.py", line 246, in check_call  
raise get_last_ffi_error() 
mxnet.base.MXNetError: Traceback (most recent call last):                                                                                                           
File "../src/storage/./cpu_shared_storage_manager.h", line 179 
MXNetError: Check failed: ptr != ((void *) -1) (0xffffffffffffffff vs. 0xffffffffffffffff) : Failed to map shared memory. mmap failed with error Permission denied

## Comment 1079551643

other (CONTRIBUTOR) · waytrue17 · 2022-03-26T01:29:58Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1079551643

It looks like the memory leak in the above script is due to instantiating multiple dataloader objects in the for loop. Having one dataloader object seems to mitigate the issue:
```
import mxnet.gluon as gl
import mxnet as mx
import gc

if __name__ == "__main__":
    gpu_ctx = mx.gpu()
    model = gl.nn.Embedding(10, 5)
    model.initialize(ctx=gpu_ctx)
    X = mx.random.uniform(shape=(1000, 3))
    dataset = mx.gluon.data.dataset.ArrayDataset(X)
    num_workers = 8
    data_loader = gl.data.DataLoader(
                dataset,
                batch_size=1,
                num_workers=num_workers,
            )

    for epoch in range(5):
        for batch in data_loader:
            # move data to gpu
            data_gpu = batch.copyto(mx.gpu())
            # forward
            l = model(data_gpu)
            # force immediate compute
            l.asnumpy()

        mx.nd.waitall()

        a, b = mx.context.gpu_memory_info(0)
        print(f"num_workers: {num_workers} epoch {epoch}: "
              f"current gpu memory {(b - a) / (1024 * 1024 * 1024)} GB, "
              f"Total gpu memory {b / (1024 * 1024 * 1024)} GB.")
        data_loader.refresh()
```

```
num_workers: 8 epoch 0: current gpu memory 1.43017578125 GB, Total gpu memory 15.78192138671875 GB.
num_workers: 8 epoch 1: current gpu memory 1.43017578125 GB, Total gpu memory 15.78192138671875 GB.
num_workers: 8 epoch 2: current gpu memory 1.43017578125 GB, Total gpu memory 15.78192138671875 GB.
num_workers: 8 epoch 3: current gpu memory 1.43017578125 GB, Total gpu memory 15.78192138671875 GB.
num_workers: 8 epoch 4: current gpu memory 1.43017578125 GB, Total gpu memory 15.78192138671875 GB.
```

## Comment 1080014222

reporter (NONE) · ann-qin-lu · 2022-03-27T20:36:12Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1080014222

Hi @waytrue17, thanks for sharing above info. Yep, by skipping recreating dataloader for each epoch does prevent such issue, but in my use case, I need to shard the big dataset into smaller ones in each epoch, and therefore data loader needs to be created multiple times. 
I've seen a few comments (e.g. [issue 1](https://github.com/apache/incubator-mxnet/pull/19378#issuecomment-730078762), [issue 2](https://github.com/apache/incubator-mxnet/issues/19420)) that mentioned memory error with this workaround [commit](https://github.com/apache/incubator-mxnet/pull/19378). Reverting this commit does resolve my accumulated gpu memory issue. 

Side question: Could you share more insights about how this workaround [commit](https://github.com/apache/incubator-mxnet/pull/19378/files), which skips the clean up gpu memory in Naive Engine, affects the usage pattern of dataloader?

## Comment 1080014895

reporter (NONE) · ann-qin-lu · 2022-03-27T20:40:23Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1080014895

@TristonC I think your error is due to the fact that Dataloader uses shared memory to hold the dataset. I am not sure if using `spawn` would require copying shared memory or not. If yes, I am assuming this approach going to increase the total memory usage? 

## Comment 1080969760

maintainer (MEMBER) · ptrendx · 2022-03-28T18:00:04Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1080969760

The workaround skips the clean up for all engines, not just the NaiveEngine. 

So, the general problem here is that when you create the dataloader, it creates a pool of workers by forking the main process, which creates a copy of everything, including the engine and the resources held by it. Then the forked process destroys this copy of the engine to become a much leaner dataloader worker. This would normally destroy the stream engine uses, but with the workaround commit in place, the destruction of the stream does not happen. Now, the problem is that CUDA does not in fact survive forking and the fact that it seems to work is just a lucky coincidence. That is why the spawn method should be used to fix the dataloader - with that the worker processes do not inherit anything from the parent and start from a clean state - with nothing copied to destroy.
In principle in the end it should work the same way as currently, via shared memory so there should be no visible differences compared to the current way of things (if anything, it should actually work slightly faster, since it would not need to spend the time to destroy the copied engine during the dataloader construction). I guess the error that @TristonC encounters means that there is some additional issue in the dataloader that it somehow depends on some copied variable from the parent process in order to initiate the communication channel with the parent. 

## Comment 1081046122

reporter (NONE) · ann-qin-lu · 2022-03-28T19:21:41Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1081046122

Hi @ptrendx, thanks a lot for the explanation! Now I get a much clear picture of what's going wrong. If the actually RC is that "CUDA does not in fact survive forking", does it mean multiprocessing with `fork` method should be avoided from the very beginning?

Just a quick summary for the two approaches we discussed:

* with the workaround that skips the clean up for all engines, it has the issue of lingering gpu resources held by engine, whenever the multiprocess fork method is used. Proposed solution is to use `spawn` in Gluon.DataLoader. @waytrue17 if you can help?
* if we revert the workaround, we will see the non-deterministic segfault issue at exit. This segfault could be resolved if this open Open issue for [Better handling of the engine destruction](https://github.com/apache/incubator-mxnet/issues/19379#) can be resolved first.

## Comment 1087853785

other (CONTRIBUTOR) · TristonC · 2022-04-04T18:02:37Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1087853785

We recommend the first solution that @ann-qin-lu proposed. 

- with the workaround that skips the clean up for all engines, it has the issue of lingering gpu resources held by engine, whenever the multiprocess fork method is used. Proposed solution is to use spawn in Gluon.DataLoader. 

## Comment 1097110719

other (CONTRIBUTOR) · TristonC · 2022-04-12T19:07:08Z · https://github.com/apache/mxnet/issues/20959#issuecomment-1097110719

@DickJC123 will help to follow up this issue.
