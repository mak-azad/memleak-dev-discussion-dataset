# GPU memory leak after using asnumpy()

- URL: https://github.com/apache/mxnet/issues/20315
- Repo: apache/mxnet (language: C++)
- State: open; created 2021-05-27T01:04:49Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · barry-jin · 2021-05-27T01:04:49Z · https://github.com/apache/mxnet/issues/20315

Looks like GPU memory will not be released after using `asnumpy()` method for a large mxnet numpy ndarray with gpu context. 

Code to reproduce:
```python
import mxnet as mx
from mxnet import npx
npx.set_np()

mx.context._current.set(mx.gpu(0))

def test():
    xshape = (16, 128, 256, 256)
    x = mx.np.random.uniform(size=xshape)
    for _ in range(5):
        x.attach_grad()
        a, b = mx.context.gpu_memory_info(0)
        x.asnumpy()
        print("Used memory {} GB, Total memory {} GB.".format((b - a) / (1024 * 1024 * 1024), b / (1024 * 1024 * 1024)))

if __name__ == '__main__':
    test()
``` 

Before comment out `x.asnumpy()` these two lines: 
``` 
Used memory 1.6171875 GB, Total memory 14.755615234375 GB.
Used memory 2.6171875 GB, Total memory 14.755615234375 GB.
Used memory 3.1171875 GB, Total memory 14.755615234375 GB.
Used memory 3.1171875 GB, Total memory 14.755615234375 GB.
Used memory 3.1171875 GB, Total memory 14.755615234375 GB.
``` 

After comment out these two lines:
``` 
Used memory 1.6171875 GB, Total memory 14.755615234375 GB.
Used memory 2.1171875 GB, Total memory 14.755615234375 GB.
Used memory 2.142578125 GB, Total memory 14.755615234375 GB.
Used memory 2.142578125 GB, Total memory 14.755615234375 GB.
Used memory 2.142578125 GB, Total memory 14.755615234375 GB.
``` 

After change xshape to a relatively smaller one (8, 64, 128, 128), the memory usage looks normal.

_Originally posted by @barry-jin in https://github.com/apache/incubator-mxnet/pull/20262#issuecomment-849217284_

## Comment 849737231

other (NONE) · lgg · 2021-05-27T15:39:47Z · https://github.com/apache/mxnet/issues/20315#issuecomment-849737231

@barry-jin what version and platform are you using?

## Comment 849757699

reporter (CONTRIBUTOR) · barry-jin · 2021-05-27T16:07:17Z · https://github.com/apache/mxnet/issues/20315#issuecomment-849757699

> @barry-jin what version and platform are you using?

Hi @lgg The environment information is here

```
----------Python Info----------
Version      : 3.8.8
Compiler     : GCC 7.5.0
Build        : ('default', 'Feb 20 2021 21:09:14')
Arch         : ('64bit', 'ELF')
------------Pip Info-----------
Version      : 21.0.1
Directory    : /home/ubuntu/.local/lib/python3.8/site-packages/pip
----------MXNet Info-----------
Version      : 2.0.0
Directory    : /home/ubuntu/workspace/incubator-mxnet/python/mxnet
Commit hash file "/home/ubuntu/workspace/incubator-mxnet/python/mxnet/COMMIT_HASH" not found. Not installed from pre-built package or built from source.
Library      : ['/home/ubuntu/workspace/incubator-mxnet/python/mxnet/../../build/libmxnet.so']
Build features:
✔ CUDA
✔ CUDNN
✔ NCCL
✖ TENSORRT
✖ CUTENSOR
✔ CPU_SSE
✔ CPU_SSE2
✔ CPU_SSE3
✔ CPU_SSE4_1
✔ CPU_SSE4_2
✖ CPU_SSE4A
✔ CPU_AVX
✖ CPU_AVX2
✔ OPENMP
✖ SSE
✔ F16C
✖ JEMALLOC
✔ BLAS_OPEN
✖ BLAS_ATLAS
✖ BLAS_MKL
✖ BLAS_APPLE
✔ LAPACK
✖ ONEDNN
✔ OPENCV
✔ DIST_KVSTORE
✔ INT64_TENSOR_SIZE
✔ SIGNAL_HANDLER
✖ DEBUG
✖ TVM_OP
----------System Info----------
Platform     : Linux-5.4.0-1047-aws-x86_64-with-glibc2.27
system       : Linux
node         : ip-172-31-10-57
release      : 5.4.0-1047-aws
version      : #49~18.04.1-Ubuntu SMP Wed Apr 28 23:08:58 UTC 2021
----------Hardware Info----------
machine      : x86_64
processor    : x86_64
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
CPU(s):              8
On-line CPU(s) list: 0-7
Thread(s) per core:  2
Core(s) per socket:  4
Socket(s):           1
NUMA node(s):        1
Vendor ID:           GenuineIntel
CPU family:          6
Model:               85
Model name:          Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
Stepping:            7
CPU MHz:             3278.429
BogoMIPS:            4999.99
Hypervisor vendor:   KVM
Virtualization type: full
L1d cache:           32K
L1i cache:           32K
L2 cache:            1024K
L3 cache:            36608K
NUMA node0 CPU(s):   0-7
Flags:               fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single pti fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid mpx avx512f avx512dq rdseed adx smap clflushopt clwb avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves ida arat pku ospke avx512_vnni
----------Network Test----------
Setting timeout: 10
Timing for MXNet: https://github.com/apache/incubator-mxnet, DNS: 0.0016 sec, LOAD: 0.3136 sec.
Timing for Gluon Tutorial(en): http://gluon.mxnet.io, DNS: 0.0902 sec, LOAD: 0.1888 sec.
Error open Gluon Tutorial(cn): https://zh.gluon.ai, <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1125)>, DNS finished in 0.19376182556152344 sec.
Timing for FashionMNIST: https://apache-mxnet.s3-accelerate.dualstack.amazonaws.com/gluon/dataset/fashion-mnist/train-labels-idx1-ubyte.gz, DNS: 0.0104 sec, LOAD: 0.5044 sec.
Timing for PYPI: https://pypi.python.org/pypi/pip, DNS: 0.0013 sec, LOAD: 0.2037 sec.
Error open Conda: https://repo.continuum.io/pkgs/free/, HTTP Error 403: Forbidden, DNS finished in 0.049257516860961914 sec.
----------Environment----------
```
MXNet is 2.0.0 version and built from source with commit hash 978f97e8cd1d486a05aaa0682b209150e1178dfd
The issue is also in MXNet 2.0.0a
