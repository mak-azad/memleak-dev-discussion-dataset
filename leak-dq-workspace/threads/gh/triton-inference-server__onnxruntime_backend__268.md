# load_model fail cause gpu memory leak

- URL: https://github.com/triton-inference-server/onnxruntime_backend/issues/268
- Repo: triton-inference-server/onnxruntime_backend (language: C++)
- State: open; created 2024-08-27T02:01:12Z; status ok; passes offcwe

## Issue body

reporter (NONE) · zjd1988 · 2024-08-27T02:01:12Z · https://github.com/triton-inference-server/onnxruntime_backend/issues/268

**Description**
onnxruntime backend load model fail will cause gpu memory leak

**Triton Information**
r23.12 and r24.07

Are you using the Triton container or did you build it yourself?
use nvcr.io/nvidia/tritonserver:r23.12-py3

**To Reproduce**
use densenet_onnx model and change config.pbtxt output shape(from 1000 -> 1001),
start tritonser with explicit
```
tritonserver --model-control-mode=explicit --model-repository=/models
```

then call python grpc client load_model api, output log as follows:
```
+----------------------------------+----------------------------------------------------------------------------------------------------+
| Option                           | Value                                                                                              |
+----------------------------------+----------------------------------------------------------------------------------------------------+
| server_id                        | triton                                                                                             |
| server_version                   | 2.41.0                                                                                             |
| server_extensions                | classification sequence model_repository model_repository(unload_dependents) schedule_policy model |
|                                  | _configuration system_shared_memory cuda_shared_memory binary_tensor_data parameters statistics tr |
|                                  | ace logging                                                                                        |
| model_repository_path[0]         | /workspace/triton_bug_models/load_bug_models/                                                      |
| model_control_mode               | MODE_EXPLICIT                                                                                      |
| strict_model_config              | 0                                                                                                  |
| rate_limit                       | OFF                                                                                                |
| pinned_memory_pool_byte_size     | 268435456                                                                                          |
| cuda_memory_pool_byte_size{0}    | 67108864                                                                                           |
| min_supported_compute_capability | 6.0                                                                                                |
| strict_readiness                 | 1                                                                                                  |
| exit_timeout                     | 30                                                                                                 |
| cache_enabled                    | 0                                                                                                  |
+----------------------------------+----------------------------------------------------------------------------------------------------+

I0827 01:49:08.461295 459 grpc_server.cc:2495] Started GRPCInferenceService at 0.0.0.0:8001
I0827 01:49:08.461547 459 http_server.cc:4619] Started HTTPService at 0.0.0.0:8000
I0827 01:49:08.502527 459 http_server.cc:282] Started Metrics Service at 0.0.0.0:8002
I0827 01:50:19.324972 459 model_lifecycle.cc:461] loading: densenet_onnx:1
I0827 01:50:19.327742 459 onnxruntime.cc:2608] TRITONBACKEND_Initialize: onnxruntime
I0827 01:50:19.327772 459 onnxruntime.cc:2618] Triton TRITONBACKEND API version: 1.17
I0827 01:50:19.327781 459 onnxruntime.cc:2624] 'onnxruntime' TRITONBACKEND API version: 1.17
I0827 01:50:19.327786 459 onnxruntime.cc:2654] backend configuration:
{"cmdline":{"auto-complete-config":"true","backend-directory":"/opt/tritonserver/backends","min-compute-capability":"6.000000","default-max-batch-size":"4"}}
I0827 01:50:19.347738 459 onnxruntime.cc:2719] TRITONBACKEND_ModelInitialize: densenet_onnx (version 1)
I0827 01:50:19.348521 459 onnxruntime.cc:692] skipping model configuration auto-complete for 'densenet_onnx': inputs and outputs already specified
I0827 01:50:19.360188 459 onnxruntime.cc:2784] TRITONBACKEND_ModelInstanceInitialize: densenet_onnx_0_0 (GPU device 0)
I0827 01:50:19.658303 459 onnxruntime.cc:2836] TRITONBACKEND_ModelInstanceFinalize: delete instance state
E0827 01:50:19.658470 459 backend_model.cc:635] ERROR: Failed to create instance: model 'densenet_onnx', tensor 'fc6_1': the model expects 4 dimensions (shape [1,1000,1,1]) but the model configuration specifies 1 dimensions (shape [1001])
I0827 01:50:19.658504 459 onnxruntime.cc:2760] TRITONBACKEND_ModelFinalize: delete model state
E0827 01:50:19.658544 459 model_lifecycle.cc:621] failed to load 'densenet_onnx' version 1: Invalid argument: model 'densenet_onnx', tensor 'fc6_1': the model expects 4 dimensions (shape [1,1000,1,1]) but the model configuration specifies 1 dimensions (shape [1001])
I0827 01:50:19.658573 459 model_lifecycle.cc:756] failed to load 'densenet_onnx'
I0827 01:50:29.020538 459 model_lifecycle.cc:461] loading: densenet_onnx:1
I0827 01:50:29.023708 459 onnxruntime.cc:2719] TRITONBACKEND_ModelInitialize: densenet_onnx (version 1)
I0827 01:50:29.024254 459 onnxruntime.cc:692] skipping model configuration auto-complete for 'densenet_onnx': inputs and outputs already specified
I0827 01:50:29.099367 459 onnxruntime.cc:2784] TRITONBACKEND_ModelInstanceInitialize: densenet_onnx_0_0 (GPU device 0)
I0827 01:50:29.297239 459 onnxruntime.cc:2836] TRITONBACKEND_ModelInstanceFinalize: delete instance state
E0827 01:50:29.297383 459 backend_model.cc:635] ERROR: Failed to create instance: model 'densenet_onnx', tensor 'fc6_1': the model expects 4 dimensions (shape [1,1000,1,1]) but the model configuration specifies 1 dimensions (shape [1001])
I0827 01:50:29.297415 459 onnxruntime.cc:2760] TRITONBACKEND_ModelFinalize: delete model state
E0827 01:50:29.297465 459 model_lifecycle.cc:621] failed to load 'densenet_onnx' version 1: Invalid argument: model 'densenet_onnx', tensor 'fc6_1': the model expects 4 dimensions (shape [1,1000,1,1]) but the model configuration specifies 1 dimensions (shape [1001])
I0827 01:50:29.297480 459 model_lifecycle.cc:756] failed to load 'densenet_onnx'
``` 

config file:
```
name: "densenet_onnx"
platform: "onnxruntime_onnx"
max_batch_size : 0
input [
  {
    name: "data_0"
    data_type: TYPE_FP32
    format: FORMAT_NCHW
    dims: [ 3, 224, 224 ]
    reshape { shape: [ 1, 3, 224, 224 ] }
  }
]
output [
  {
    name: "fc6_1"
    data_type: TYPE_FP32
    dims: [ 1001 ]
  }
]

instance_group [ 
  { 
    count: 1
    kind: KIND_GPU
    gpus: [ 0 ]
  }
]
```

before call python
![企业微信截图_17247243623995](https://github.com/user-attachments/assets/c1a5a4a1-10a8-4352-8ecd-a6230ec5a8ba)


after call 5 times load_model
![企业微信截图_17247243735112](https://github.com/user-attachments/assets/6623e304-4eee-4380-97c1-4506bd44f9b2)


after call 10 times load_model
![企业微信截图_17247243882564](https://github.com/user-attachments/assets/2aa2450c-280a-4f93-a68b-40f08810a201)


**Expected behavior**
no gpu memory increase

