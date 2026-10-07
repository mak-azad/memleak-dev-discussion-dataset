# Misc. bug: Memory leak (ggml_cuda_pool_vmm) during prompt prefill with MTP and quantized KV cache

- URL: https://github.com/ggml-org/llama.cpp/issues/23635
- Repo: ggml-org/llama.cpp (language: C++)
- State: closed; created 2026-05-25T01:32:09Z; status ok; passes offcwe

## Issue body

reporter (NONE) · dsenchankau · 2026-05-25T01:32:09Z · https://github.com/ggml-org/llama.cpp/issues/23635

### Name and Version

llama-server --version
version: 9307 (549b9d843)
built with GNU 13.3.0 for Linux x86_64

### Operating systems

Linux

### Which llama.cpp modules do you know to be affected?

llama-server

### Command line

```shell
# MTP + Q8 KV cache + Q8 MTP cache
numactl --physcpubind=0-15 llama-server -m Qwen3.6-27B-uncensored-heretic-v2-Native-MTP-Preserved-Q5_K_S_llmfan46.gguf -ngl 999 --ctx-size 150000 --mlock --no-mmap -np 1 -b 5120 -ub 256 -t 8 -tb 16 -fa on -ctk q8_0 -ctv q8_0 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 --reasoning-budget -1 --chat-template-kwargs '{"preserve_thinking":true}' --cache-reuse 256 -ngld 999 -ctkd q8_0 -ctvd q8_0 --spec-type draft-mtp --spec-draft-n-max 4 --no-mmproj --jinja --rpc 192.168.0.200:50052 --tensor-split 45,55

# MTP + Q8 KV cache + F16 MTP cache
numactl --physcpubind=0-15 llama-server -m ~/pcie3_970evo/Llama_Models/coding/Qwen3.6-27B-uncensored-heretic-v2-Native-MTP-Preserved-Q5_K_S_llmfan46.gguf -ngl 999 --ctx-size 150000 --mlock --no-mmap -np 1 -b 5120 -ub 256 -t 8 -tb 16 -fa on -ctk q8_0 -ctv q8_0 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 --reasoning-budget -1 --chat-template-kwargs '{"preserve_thinking":true}' --cache-reuse 256 -ngld 999 -ctkd f16 -ctvd f16 --spec-type draft-mtp --spec-draft-n-max 4 --no-mmproj --jinja --rpc 192.168.0.200:50052 --tensor-split 45,55

# MTP + F16 KV cache + F16 MTP cache
numactl --physcpubind=0-15 llama-server -m Qwen3.6-27B-uncensored-heretic-v2-Native-MTP-Preserved-Q5_K_S_llmfan46.gguf -ngl 999 --ctx-size 80000 --mlock --no-mmap -np 1 -b 5120 -ub 256 -t 8 -tb 16 -fa on -ctk f16 -ctv f16 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 --reasoning-budget -1 --chat-template-kwargs '{"preserve_thinking":true}' --cache-reuse 256 -ngld 999 -ctkd f16 -ctvd f16 --spec-type draft-mtp --spec-draft-n-max 4 --no-mmproj --jinja --rpc 192.168.0.200:50052 --tensor-split 45,55

# non-MTP + Q8 KV cache
numactl --physcpubind=0-15 llama-server -m Qwen3.6-27B-uncensored-heretic-v2-Q5_K_S_llmfan46.gguf -ngl 999 --ctx-size 150000 --mlock --no-mmap -np 1 -b 5120 -ub 256 -t 8 -tb 16 -fa on -ctk q8_0 -ctv q8_0 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 --reasoning-budget -1 --chat-template-kwargs '{"preserve_thinking":true}' --cache-reuse 256 --no-mmproj --jinja --rpc 192.168.0.200:50052 --tensor-split 45,55

# non-MTP + F16 KV cache
numactl --physcpubind=0-15 llama-server -m Qwen3.6-27B-uncensored-heretic-v2-Q5_K_S_llmfan46.gguf -ngl 999 --ctx-size 80000 --mlock --no-mmap -np 1 -b 5120 -ub 256 -t 8 -tb 16 -fa on -ctk f16 -ctv f16 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 --reasoning-budget -1 --chat-template-kwargs '{"preserve_thinking":true}' --cache-reuse 256 --no-mmproj --jinja --rpc 192.168.0.200:50052 --tensor-split 45,55
```

### Problem description & steps to reproduce

I've come across a memory leak connected to CUDA memory pool when I was using MTP and quantized KV cache (does not matter if its Q8, Q4 or something else).

Llama-server memory usage keeps growing as it's working on the prompt prefill.

This uncontrolled dynamic memory allocation does not happen if I keep the KV cache unquantized (f16).

It does not matter which quantization is selected for MTP (-ctkd -ctvd), only the KV cache quantization causes the memory leak.

I tested this on Qwen3.6-27B (Q5_K_S for both MTP and non-MTP) with a 64053 token prefill.

Hardware is RTX 4080 Super (primary PC) + RTX 4070 Super (RPC PC) both running Ubuntu 24.04 and the latest llama.cpp master pulled and built locally.

I believe the exact model and quant level does not matter but here are the ones I used
* https://huggingface.co/llmfan46/Qwen3.6-27B-uncensored-heretic-v2-GGUF
* https://huggingface.co/llmfan46/Qwen3.6-27B-uncensored-heretic-v2-Native-MTP-Preserved-GGUF

I also reproduced it with a smaller Q3 quant of the same Qwen3.6-27B model on the main PC (RTX 4080) without RPC. The behavior did not change, so it has nothing to do with RPC or quant level.

I tried various combinations of llama-server parameters such as -b, -ub, -cram, --ctx-checkpoints, --fit off, dropping as much supplied parameters as possible, different quantization levels - nothing changed the memory behavior

My llama.cpp build
```code
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_COMPILER=/usr/local/cuda-13.1/bin/nvcc -DGGML_CUDA_FA_ALL_QUANTS=ON -DCMAKE_CUDA_ARCHITECTURES=89 -DGGML_CUDA_F16=ON -DGGML_NATIVE=ON -DGGML_CUDA_GRAPHS=ON -DGGML_RPC=ON -DCMAKE_BUILD_TYPE=Release
```
While troubleshooting I also reproduced it with a minimal build
```code
cmake -B build -DGGML_CUDA=ON -DCMAKE_CUDA_COMPILER=/usr/local/cuda-13.1/bin/nvcc -DCMAKE_CUDA_ARCHITECTURES=89 -DGGML_RPC=ON
```

I used a 64053 tokens prefill to test and reproduce this issue but I believe the prompt length does not matter. OOM is just a question of how much free VRAM is available and whether the prompt is long enough to fill it up.

Memory usage observations:
```code
Notation is
# process-name memory-after-load -> memory after prefill (or before OOM)

MTP + Q8 KV cache + Q8 MTP cache
# llama-server 14276 -> 15042 -> OOM
# rpc-server   10910 -> 10910

MTP + Q8 KV cache + F16 MTP cache
# llama-server 14276 -> 15042 -> OOM
# rpc-server   10910 -> 10910

MTP + F16 KV cache + F16 MTP cache
# llama-server 14220 -> 14484
# rpc-server   10822 -> 10822

non-MTP + Q8 KV cache
# llama-server 13002 -> 13262
# rpc-server   10528 -> 10528

non-MTP + F16 KV cache
# llama-server 12954 -> 12964
# rpc-server   10430 -> 10430
```

### First Bad Commit

9b996f0

(Not entirely sure but I believe it was there from the moment MTP logic was merged into master)


### Relevant log output

<details>
<summary>Logs</summary>
<!-- Copy-pasted short logs go into the "console" area here -->

```console
2.26.274.638 E CUDA error: out of memory
2.26.274.641 E   current device: 0, in function alloc at /home/USER_NAME/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:527
2.26.274.641 E   cuMemCreate(&handle, reserve_size, &prop, 0)
/home/USER_NAME/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:102: CUDA error
[New LWP 496272]
[New LWP 496271]
[New LWP 496270]
[New LWP 496269]
[New LWP 496268]
[New LWP 496267]
[New LWP 496266]
[New LWP 496265]
[New LWP 496264]
[New LWP 496263]
[New LWP 496262]
[New LWP 496261]
[New LWP 496260]
[New LWP 496259]
[New LWP 496258]
[New LWP 496257]
[New LWP 496256]
[New LWP 496255]
[New LWP 496254]
[New LWP 496253]
[New LWP 496252]
[New LWP 496251]
[New LWP 496250]
[New LWP 496249]
[New LWP 496248]
[New LWP 496247]
[New LWP 496246]
[New LWP 496242]
[New LWP 496241]

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.ubuntu.com>
Enable debuginfod for this session? (y or [n]) [answered N; input not from terminal]
Debuginfod has been disabled.
To make this setting permanent, add 'set debuginfod enabled off' to .gdbinit.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
0x00007e9b09b10813 in __GI___wait4 (pid=498807, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
warning: 30	../sysdeps/unix/sysv/linux/wait4.c: No such file or directory
#0  0x00007e9b09b10813 in __GI___wait4 (pid=498807, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
30	in ../sysdeps/unix/sysv/linux/wait4.c
#1  0x00007e9b0a158293 in ggml_print_backtrace () from /home/USER_NAME/llama.cpp/build/bin/libggml-base.so.0
#2  0x00007e9b0a15843b in ggml_abort () from /home/USER_NAME/llama.cpp/build/bin/libggml-base.so.0
#3  0x00007e9b04247bf7 in ggml_cuda_error(char const*, char const*, char const*, int, char const*) () from /home/USER_NAME/llama.cpp/build/bin/libggml-cuda.so.0
#4  0x00007e9b04262a50 in ggml_cuda_pool_vmm::alloc(unsigned long, unsigned long*) () from /home/USER_NAME/llama.cpp/build/bin/libggml-cuda.so.0
#5  0x00007e9b0465bcb9 in void launch_fattn<256, 8, 8>(ggml_backend_cuda_context&, ggml_tensor*, void (*)(char const*, char const*, char const*, char const*, char const*, int const*, float*, float2*, float, float, float, float, unsigned int, float, int, uint3, int, int, int, int, int, int, int, int, int, int, int, long, int, int, long, int, int, int, int, int, long), int, unsigned long, int, bool, bool, bool, int) () from /home/USER_NAME/llama.cpp/build/bin/libggml-cuda.so.0
#6  0x00007e9b0465d0bd in void ggml_cuda_flash_attn_ext_mma_f16_case<256, 256, 8, 8>(ggml_backend_cuda_context&, ggml_tensor*) () from /home/USER_NAME/llama.cpp/build/bin/libggml-cuda.so.0
#7  0x00007e9b04260d21 in ggml_backend_cuda_graph_compute(ggml_backend*, ggml_cgraph*) () from /home/USER_NAME/llama.cpp/build/bin/libggml-cuda.so.0
#8  0x00007e9b0a1758e7 in ggml_backend_sched_graph_compute_async () from /home/USER_NAME/llama.cpp/build/bin/libggml-base.so.0
#9  0x00007e9b090d73c1 in llama_context::graph_compute(ggml_cgraph*, bool) () from /home/USER_NAME/llama.cpp/build/bin/libllama.so.0
#10 0x00007e9b090d9b54 in llama_context::process_ubatch(llama_ubatch const&, llm_graph_type, llama_memory_context_i*, ggml_status&) () from /home/USER_NAME/llama.cpp/build/bin/libllama.so.0
#11 0x00007e9b090e1401 in llama_context::decode(llama_batch const&) () from /home/USER_NAME/llama.cpp/build/bin/libllama.so.0
#12 0x00007e9b090e305f in llama_decode () from /home/USER_NAME/llama.cpp/build/bin/libllama.so.0
#13 0x00007e9b096c81cd in common_speculative_impl_draft_mtp::process(llama_batch const&) () from /home/USER_NAME/llama.cpp/build/bin/libllama-common.so.0
#14 0x00007e9b096bfc68 in common_speculative_process(common_speculative*, llama_batch const&) () from /home/USER_NAME/llama.cpp/build/bin/libllama-common.so.0
#15 0x00007e9b0a370f35 in server_context_impl::update_slots() () from /home/USER_NAME/llama.cpp/build/bin/libllama-server-impl.so
#16 0x00007e9b0a4039e1 in server_queue::start_loop(long) () from /home/USER_NAME/llama.cpp/build/bin/libllama-server-impl.so
#17 0x00007e9b0a2d0097 in llama_server(int, char**) () from /home/USER_NAME/llama.cpp/build/bin/libllama-server-impl.so
#18 0x00007e9b09a2a1ca in __libc_start_call_main (main=main@entry=0x5dd391eef270 <main>, argc=argc@entry=59, argv=argv@entry=0x7ffd3377b898) at ../sysdeps/nptl/libc_start_call_main.h:58
warning: 58	../sysdeps/nptl/libc_start_call_main.h: No such file or directory
#19 0x00007e9b09a2a28b in __libc_start_main_impl (main=0x5dd391eef270 <main>, argc=59, argv=0x7ffd3377b898, init=<optimized out>, fini=<optimized out>, rtld_fini=<optimized out>, stack_end=0x7ffd3377b888) at ../csu/libc-start.c:360
warning: 360	../csu/libc-start.c: No such file or directory
#20 0x00005dd391eef2a5 in _start ()
[Inferior 1 (process 496239) detached]
Aborted (core dumped)

```
</details>


## Comment 4531070583

other (CONTRIBUTOR) · am17an · 2026-05-25T02:31:15Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531070583

quantized kv-cache requires extra VRAM for dequantizing for f16 in the FA code. This is expected to grow till the full context size. It is not a leak

## Comment 4531107727

reporter (NONE) · dsenchankau · 2026-05-25T02:43:03Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531107727

I understand that, however there is a significant difference in memory consumption between between MTP and non-MTP versions of the same model.

(in case of MTP model) to the extent where the benefits of cache quantization (memory savings, bigger context window) are completely wiped out and it's does not make sense to use it.

Shouldn't the memory utilisation be more or less identical (i.e. dynamic growth past model load) for the same prompt and parameters for MTP and non-MTP models?

## Comment 4531127692

other (CONTRIBUTOR) · am17an · 2026-05-25T02:49:30Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531127692

> Shouldn't the memory utilisation be more or less identical (i.e. dynamic growth past model load) for the same prompt and parameters for MTP and non-MTP models?

It is identical for f16 cache except the initial device checkpoint.

Re quantized kv-cache - Ideally `-fit` would adjust the safe context to use, I will look into adding that. 

## Comment 4531358292

reporter (NONE) · dsenchankau · 2026-05-25T03:56:22Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531358292

To better illustrate my point, I ran a 159204 token prompt on a Q3 quant of the same model (MTP and non-MTP versions) and here are the results:

```code
# non-MTP + Q8 KV cache -> a total delta of 1260
#   local   10980 -> 11612 ->   a delta of 632
#   rpc     8510 -> 9138 ->     a delta of 628

# MTP + Q8 KV cache + Q8 MTP cache -> a total delta of 1466
#   local   12466 -> 13928 ->   a delta of 1462
#   rpc     9702 -> 9706 ->     a delta of 4
```

so the MTP version dynamically allocates 16.35% more memory than non MTP when processing the same prompt prefill

## Comment 4531375394

other (CONTRIBUTOR) · am17an · 2026-05-25T04:01:53Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531375394

How does it look when you keep F16 MTP cache? 

## Comment 4531661243

reporter (NONE) · dsenchankau · 2026-05-25T05:03:52Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531661243

here it's even worse, ~66.19% more allocation over a non-MTP

```code
# MTP + Q8 KV cache + F16 MTP cache -> a total delta of 2094
#   local   12466 -> 13928  -> a delta of 1462
#   rpc     9074 -> 9706    -> a delta of 632
```

## Comment 4531710680

other (CONTRIBUTOR) · am17an · 2026-05-25T05:16:31Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531710680

The question is whether there is a *memory leak* - I think it's pretty clear that there isn't. Also please note: MTP **requires more VRAM**, you posting deltas with different configurations is not relevant. With that said, currently the grafted on MTP layer does not respect `-spec-draft-cache-type*`, I think that should be fixed with #23646

## Comment 4531801470

reporter (NONE) · dsenchankau · 2026-05-25T05:30:55Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531801470

I mean sure, I understand that as well. That's why I highlight the deltas and not the full memory usage. I thought MTP only affects the model size, is it also expected that it causes more dynamic memory allocation post model load?

The main issue is that with f16 I know the memory cost and footprint upfront with no surprises later on. As opposed to a quantized cache, where it's basically unpredictable.

-fit on also mostly fails to pick the correct context size with MTP, compounding the issue.

## Comment 4531810671

other (CONTRIBUTOR) · am17an · 2026-05-25T05:32:55Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4531810671

Yes as I said earlier 

> quantized kv-cache requires extra VRAM for dequantizing for f16 in the FA code. This is expected to grow till the full context size. It is not a leak

> Re quantized kv-cache - Ideally -fit would adjust the safe context to use, I will look into adding that.


## Comment 4532046072

other (CONTRIBUTOR) · am17an · 2026-05-25T06:26:02Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4532046072

> I mean sure, I understand that as well. That's why I highlight the deltas and not the full memory usage. I thought MTP only affects the model size, is it also expected that it causes more dynamic memory allocation post model load?

Forgot to mention, apart from model size being affected it also has it's own kv-cache. While doing FA over quantized KV-cache, the memory cost to dequantize the KV vectors is amortized via N layers. Qwen MTP has 1 layer, so you would basically just double the cost there. So it may be better to stick with f16 cache. Gemma 4 MTP #23398 shares this kv-cache so overall memory consumption may be lower. 

## Comment 4536080532

reporter (NONE) · dsenchankau · 2026-05-25T17:36:23Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4536080532

Got it, thanks.

And how much would performance suffer if that `q8 -> f16` so to say buffer is not kept in memory after allocation but rather allocated on-the-fly as needed (per-batch or as a sliding window of sort) and then freed? Is that buffer unique for each context token? Each MB of VRAM is precious nowadays I think it makes sense to save it as much as possible.

## Comment 4544881943

other (CONTRIBUTOR) · Kononnable · 2026-05-26T14:11:16Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4544881943

@DzmitryTheStreak  You may want to check if this change would fix the issue. I encountered something similar.

<details>

<summary>Diff</summary>


```
diff --git a/ggml/src/ggml-cuda/common.cuh b/ggml/src/ggml-cuda/common.cuh
index e54ecb293..902354920 100644
--- a/ggml/src/ggml-cuda/common.cuh
+++ b/ggml/src/ggml-cuda/common.cuh
@@ -1495,6 +1495,15 @@ struct ggml_backend_cuda_context {
     ggml_cuda_pool & pool() {
         return pool(device);
     }
+
+    // Persistent conversion buffers for Flash Attention with quantized KV cache.
+    // Allocated once at max size and reused across all micro-batches, avoiding
+    // repeated pool allocations that grow proportionally with n_kv and trigger
+    // periodic OOM flushes.
+    void * persistent_K_f16 = nullptr;
+    size_t persistent_K_f16_ne = 0;
+    void * persistent_V_f16 = nullptr;
+    size_t persistent_V_f16_ne = 0;
 };
 
 struct ggml_cuda_mm_fusion_args_host {
diff --git a/ggml/src/ggml-cuda/fattn-common.cuh b/ggml/src/ggml-cuda/fattn-common.cuh
index debcb6e54..f77b2434b 100644
--- a/ggml/src/ggml-cuda/fattn-common.cuh
+++ b/ggml/src/ggml-cuda/fattn-common.cuh
@@ -952,8 +952,12 @@ void launch_fattn(
     const int cc  = ggml_cuda_info().devices[id].cc;
     const int nsm = ggml_cuda_info().devices[id].nsm;
 
-    ggml_cuda_pool_alloc<half>   K_f16(pool);
-    ggml_cuda_pool_alloc<half>   V_f16(pool);
+    // Persistent conversion buffers for quantized K/V. Allocated once at max
+    // size and reused across micro-batches, avoiding repeated pool allocations
+    // that grow proportionally with n_kv and trigger periodic OOM flushes.
+    half * K_f16_ptr = nullptr;
+    half * V_f16_ptr = nullptr;
+
     ggml_cuda_pool_alloc<int>    KV_max(pool);
     ggml_cuda_pool_alloc<float>  dst_tmp(pool);
     ggml_cuda_pool_alloc<float2> dst_tmp_meta(pool);
@@ -972,10 +976,21 @@ void launch_fattn(
         const size_t bs = ggml_blck_size(K->type);
         const size_t ts = ggml_type_size(K->type);
 
-        K_f16.alloc(ggml_nelements(K));
+        const size_t ne_K = ggml_nelements(K);
+        // Allocate persistent buffer at current size if not yet allocated or too small
+        if (ctx.persistent_K_f16 == nullptr || ctx.persistent_K_f16_ne < ne_K) {
+            if (ctx.persistent_K_f16 != nullptr) {
+                CUDA_CHECK(cudaFree(ctx.persistent_K_f16));
+            }
+            ctx.persistent_K_f16_ne = ne_K;
+            ggml_cuda_set_device(id);
+            CUDA_CHECK(cudaMalloc(&ctx.persistent_K_f16, ne_K * sizeof(half)));
+        }
+        K_f16_ptr = (half *)ctx.persistent_K_f16;
+
         if (ggml_is_contiguously_allocated(K)) {
             to_fp16_cuda_t to_fp16 = ggml_get_to_fp16_cuda(K->type);
-            to_fp16(K_data, K_f16.ptr, ggml_nelements(K), main_stream);
+            to_fp16(K_data, K_f16_ptr, ggml_nelements(K), main_stream);
 
             nb11 = nb11*bs*sizeof(half)/ts;
             nb12 = nb12*bs*sizeof(half)/ts;
@@ -986,13 +1001,13 @@ void launch_fattn(
             const int64_t s01 = nb11 / ts;
             const int64_t s02 = nb12 / ts;
             const int64_t s03 = nb13 / ts;
-            to_fp16(K_data, K_f16.ptr, K->ne[0], K->ne[1], K->ne[2], K->ne[3], s01, s02, s03, main_stream);
+            to_fp16(K_data, K_f16_ptr, K->ne[0], K->ne[1], K->ne[2], K->ne[3], s01, s02, s03, main_stream);
 
             nb11 = K->ne[0] * sizeof(half);
             nb12 = K->ne[1] * nb11;
             nb13 = K->ne[2] * nb12;
         }
-        K_data = (char *) K_f16.ptr;
+        K_data = (const char *) K_f16_ptr;
     }
 
     if (need_f16_V && V->type != GGML_TYPE_F16) {
@@ -1005,11 +1020,22 @@ void launch_fattn(
             const size_t bs = ggml_blck_size(V->type);
             const size_t ts = ggml_type_size(V->type);
 
-            V_f16.alloc(ggml_nelements(V));
+            const size_t ne_V = ggml_nelements(V);
+            // Allocate persistent buffer at current size if not yet allocated or too small
+            if (ctx.persistent_V_f16 == nullptr || ctx.persistent_V_f16_ne < ne_V) {
+                if (ctx.persistent_V_f16 != nullptr) {
+                    CUDA_CHECK(cudaFree(ctx.persistent_V_f16));
+                }
+                ctx.persistent_V_f16_ne = ne_V;
+                ggml_cuda_set_device(id);
+                CUDA_CHECK(cudaMalloc(&ctx.persistent_V_f16, ne_V * sizeof(half)));
+            }
+            V_f16_ptr = (half *)ctx.persistent_V_f16;
+
             if (ggml_is_contiguously_allocated(V)) {
                 to_fp16_cuda_t to_fp16 = ggml_get_to_fp16_cuda(V->type);
-                to_fp16(V_data, V_f16.ptr, ggml_nelements(V), main_stream);
-                V_data = (char *) V_f16.ptr;
+                to_fp16(V_data, V_f16_ptr, ggml_nelements(V), main_stream);
+                V_data = (const char *) V_f16_ptr;
 
                 nb21 = nb21*bs*sizeof(half)/ts;
                 nb22 = nb22*bs*sizeof(half)/ts;
@@ -1020,13 +1046,13 @@ void launch_fattn(
                 const int64_t s01 = nb21 / ts;
                 const int64_t s02 = nb22 / ts;
                 const int64_t s03 = nb23 / ts;
-                to_fp16(V_data, V_f16.ptr, V->ne[0], V->ne[1], V->ne[2], V->ne[3], s01, s02, s03, main_stream);
+                to_fp16(V_data, V_f16_ptr, V->ne[0], V->ne[1], V->ne[2], V->ne[3], s01, s02, s03, main_stream);
 
                 nb21 = V->ne[0] * sizeof(half);
                 nb22 = V->ne[1] * nb21;
                 nb23 = V->ne[2] * nb22;
             }
-            V_data = (char *) V_f16.ptr;
+            V_data = (const char *) V_f16_ptr;
         }
     }
 
diff --git a/ggml/src/ggml-cuda/ggml-cuda.cu b/ggml/src/ggml-cuda/ggml-cuda.cu
index e25be3592..63b41cf1e 100644
--- a/ggml/src/ggml-cuda/ggml-cuda.cu
+++ b/ggml/src/ggml-cuda/ggml-cuda.cu
@@ -616,6 +616,13 @@ ggml_backend_cuda_context::~ggml_backend_cuda_context() {
             CUBLAS_CHECK(cublasDestroy(cublas_handles[i]));
         }
     }
+    // Free persistent Flash Attention conversion buffers
+    if (persistent_K_f16 != nullptr) {
+        CUDA_CHECK(cudaFree(persistent_K_f16));
+    }
+    if (persistent_V_f16 != nullptr) {
+        CUDA_CHECK(cudaFree(persistent_V_f16));
+    }
 }
 ```

</details>

Full disclosure -  code is entirely AI generated, I didn't have time to properly check if it is doing things in the way they're supposed to be done. After applying the change VRAM usage is near constant during prefill of a long prompt.

#23646 slows down vram increase significantly, but even when using MTP's KV-cache in f16 I was able to observe the changes.

## Comment 4581532474

other (NONE) · vmlinuzx · 2026-05-30T03:40:23Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4581532474

Additional data point from a Strix Halo / Vulkan UMA setup, in case it helps triangulate the MTP + KV/cache memory behavior.

System / backend:
- AMD Ryzen AI Max+ 395 / Radeon 8060S, RADV GFX1151, unified memory
- Vulkan backend, llama-server router mode
- Qwen3.6-35B-A3B-MTP-UD-Q4_K_XL
- `--spec-type draft-mtp --spec-draft-n-max 2`
- `ctx-size = 262144`, `parallel = 2`, `batch-size = 2048`, `ubatch-size = 256`
- target KV was `cache-type-k = q8_0`, `cache-type-v = q8_0`

Workload:
- long-running agent/orchestrator workflow with max concurrency 2
- one orchestrator + one worker, with repeated worker context growth/compression and return to orchestrator

Observed behavior with default checkpoint count:
- router/model eventually hit memory pressure / global OOM under the workload
- normal process RSS did not explain the pressure; on this UMA system the missing pressure appeared mostly as GPU/driver-side memory rather than ordinary RSS
- kernel killed the llama-server cgroup; no coredump expected because it was SIGKILL

Non-optimal but effective workaround:
- explicitly clamp context checkpoints for the MTP model:

```ini
ctx-checkpoints = 4
```

After setting `ctx-checkpoints = 4` and rerunning the same brutal workflow, telemetry stayed stable:

```text
MemAvailable min:  ~90.8 GiB
MemFree min:       ~69.0 GiB
SwapFree stable:   ~7.25 GiB
cgroup peak:       ~6.0 GiB
llama RSS peak:    ~21.5 GiB
VRAM used peak:    ~3.9 GiB
GTT used peak:     ~23.7 GiB
cgroup oom events: 0
```

So for us the practical workaround is not ideal for TTFT/cache reuse, but it strongly suggests checkpoint retention/count is part of the memory-pressure trigger. We have not fully isolated whether this is the same leak as CUDA `ggml_cuda_pool_vmm`, but the shape is adjacent: MTP + long prompt/cache/checkpoint traffic causes memory growth that is not obvious from ordinary process RSS.


## Comment 4589168224

other (NONE) · miversen33 · 2026-06-01T02:47:47Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4589168224

I am struggling to reliably reproduce this issue but it has bitten me every time (eventually) when I am using Qwen3.6 27B MTP with Q8 kv cache. Eventually the ram usage spills into system ram and _eventually_ the whole machine just locks up. 

I am seeing this with 128k context, on 3 AMD 7900XTXs. I don't really know how to provide more useful info, except to say I do not see this behavior from the models not using MTP speculative drafting.

Edit:

One thing I notice is that is isn't related to the size of the context itself (which means this isn't directly related to "MTP uses more VRAM") but rather it's related to the number of operations performed (which hints at a memory leak).

I can say this because _after_ my above lockup occurs, once I restart the machine (or docker container in my case), I can continue my work exactly where I left off. Context gets reloaded and all is well until eventually I run out of RAM again

## Comment 4589480643

reporter (NONE) · dsenchankau · 2026-06-01T04:13:06Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4589480643

@am17an

Now I'm 100% certain that there is indeed a memory leak.

It's more apparent on the RPC side because the process can be kept alive indefinitely. But I think the same issue is present in llama-server.

Today I was playing around with `Qwen3.6-27B-MTP-UD-Q4_K_XL_unsloth.gguf` with Q8 main KV cache and Q8 MTP KV cache as well

```code
numactl --physcpubind=0-15 llama-server -m Qwen3.6-27B-MTP-UD-Q4_K_XL_unsloth.gguf -ngl 999 --ctx-size 160000 --mlock --no-mmap -np 1 -b 2560 -ub 128 -t 8 -tb 16 -fa on -ctk q8_0 -ctv q8_0 --temp 0.6 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 0.0 --repeat-penalty 1.0 --reasoning-budget -1 --chat-template-kwargs '{"preserve_thinking":true}' --cache-reuse 256 -cram 16384 -ngld 999 -ctkd q8_0 -ctvd q8_0 --spec-type draft-mtp --spec-draft-n-max 3 --no-mmproj --jinja --rpc 192.168.0.200:50052 --tensor-split 46,54
```

Here is the RPC process memory usage at different stages:

* Fresh RPC server, before the first model load
> 190 MB used

* Llama-server loaded the model
> 224 MB used

* Llama-server loaded the model, llama-server was shut down, llama-server loaded the model again
> 224 MB used

* After a 160K prefill and subsequent manual llama-server shutdown. So no llama-server process running
> 910 MB used

## Comment 4589970084

other (CONTRIBUTOR) · Kononnable · 2026-06-01T06:04:08Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4589970084

You can check if #23907 solves issues on your machines. For me it did.  It's not merged yet, so you'll need to compile it locally or wait for a merge.

## Comment 4590774194

other (NONE) · AbdulrahmanHashem · 2026-06-01T08:17:32Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4590774194

> You can check if [#23907](https://github.com/ggml-org/llama.cpp/pull/23907) solves issues on your machines. For me it did. It's not merged yet, so you'll need to compile it locally or wait for a merge.

this indeed fixes it, i have tested it myself but there's another critical leak which happnes on the first prompt with mtp and it's about 125 mp allocated all at once
and another 35 roughly sometimes allocated when using ngram-mod
and both happen when using both spec methods together.


## Comment 4627677706

other (NONE) · AbdulrahmanHashem · 2026-06-05T02:50:44Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4627677706

@Kononnable @DzmitryTheStreak  #24108 just fixed this issue. 
the only runtime allocations that happen as of 9518 is roughly 100 MB allocation that happens on first prompt PP and then a total of maybe 8 MB that happen after that during TG.

## Comment 4627761888

reporter (NONE) · dsenchankau · 2026-06-05T03:12:47Z · https://github.com/ggml-org/llama.cpp/issues/23635#issuecomment-4627761888

Great news, thanks. I'm closing this issue then
