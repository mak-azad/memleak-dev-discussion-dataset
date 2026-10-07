# [GPU] Memory leak in Collective Ops (AllGather, etc) when using Command Buffer

- URL: https://github.com/openxla/xla/issues/36487
- Repo: openxla/xla (language: C++)
- State: open; created 2026-01-16T06:02:10Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · apivovarov · 2026-01-16T06:02:10Z · https://github.com/openxla/xla/issues/36487

I faced a memory leak when executing collective operations (specifically Send, Recv, AllGather, etc) inside an XLA Command Buffer (CUDA Graph). The leak is triggered when the Command Buffer is used (second execution of executable)

I recently added a test file to reproduce this behavior: xla/service/gpu/tests/collective_ops_command_buffer_test.cc.

Reproduction Steps:
Run the test SendRecv_Simple or AllGather_Dim1 in collective_ops_command_buffer_test.cc with ASAN enabled.
The test executes the command buffer multiple times to force graph re-recording.

LeakSanitizer detects a leak of approximately 400 bytes per re-recording

I also added test for AllGather op - AllGather_Dim1 - it has memory leak issue too
https://github.com/openxla/xla/pull/36486


```bash
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from CollectiveOpsCommandBufferTest
[ RUN      ] CollectiveOpsCommandBufferTest.AllGather_Dim1
[       OK ] CollectiveOpsCommandBufferTest.AllGather_Dim1 (7948 ms)
[----------] 1 test from CollectiveOpsCommandBufferTest (7949 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (7949 ms total)
[  PASSED  ] 1 test.

=================================================================
==5373==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 400 byte(s) in 2 object(s) allocated from:
    #0 0x56541bdacde4 in malloc llvm/llvm-project/compiler-rt/lib/asan/asan_malloc_linux.cpp:67:3
    #1 0x7bd70849c6cf  (/build/cas/d7a/d7acd173f28755ba0140b0831c03fd6bdcf20690a6964c5e8cdb87491e79e839_02000812eda0/@0x1000+0x29b6cf) (BuildId: 047942dac4b107dd9dd6a865ced25f1acfc6aca6)
    #2 0x7bd7085af00b  (/build/cas/d7a/d7acd173f28755ba0140b0831c03fd6bdcf20690a6964c5e8cdb87491e79e839_02000812eda0/@0x1000+0x3ae00b) (BuildId: 047942dac4b107dd9dd6a865ced25f1acfc6aca6)
    #3 0x7bd7085a05bf  (/build/cas/d7a/d7acd173f28755ba0140b0831c03fd6bdcf20690a6964c5e8cdb87491e79e839_02000812eda0/@0x1000+0x39f5bf) (BuildId: 047942dac4b107dd9dd6a865ced25f1acfc6aca6)
    #4 0x7fddf7ea6fa5 in stream_executor::gpu::CudaCommandBuffer::LaunchGraph(stream_executor::Stream*) /xla/stream_executor/cuda/cuda_command_buffer.cc:674:7
    #5 0x7fddf72737eb in stream_executor::gpu::GpuCommandBuffer::Submit(stream_executor::Stream*) /xla/stream_executor/gpu/gpu_command_buffer.cc:654:10
    #6 0x7fe06a1d2af0 in xla::gpu::CommandBufferThunk::ExecuteOnStream(xla::gpu::Thunk::ExecuteParams const&) /xla/backends/gpu/runtime/command_buffer_thunk.cc:301:38
    #7 0x7fe052efeb97 in xla::gpu::SequentialThunk::ExecuteOnStream(xla::gpu::Thunk::ExecuteParams const&) /xla/backends/gpu/runtime/sequential_thunk.cc:106:31
    #8 0x7fe06c151156 in xla::gpu::(anonymous namespace)::ExecuteThunksImpl(xla::DebugOptions const*, std::__u::basic_string<char, std::__u::char_traits<char>, std::__u::allocator<char>> const&, int, xla::gpu::SequentialThunk&, xla::gpu::Thunk::ExecutableSource, xla::ServiceExecutableRunOptions const*, xla::gpu::BufferAllocations const&, bool, absl::flat_hash_set<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long>, absl::hash_internal::Hash<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long>>, std::__u::equal_to<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long>>, std::__u::allocator<tsl::gtl::IntType<xla::gpu::ExecutionStreamId_tag_, unsigned long>>> const&) /xla/service/gpu/gpu_executable.cc:533:37
    #9 0x7fe06c14c7ff in xla::gpu::GpuExecutable::ExecuteThunks(xla::gpu::BufferAllocations const&, xla::ServiceExecutableRunOptions const*) /xla/service/gpu/gpu_executable.cc:1107:22
    #10 0x7fe06c14a2e2 in xla::gpu::GpuExecutable::ExecuteAsyncOnStreamImpl(xla::ServiceExecutableRunOptions const*, std::__u::variant<absl::Span<xla::ShapedBuffer const* const>, absl::Span<xla::ExecutionInput>>) /xla/service/gpu/gpu_executable.cc:1031:22
    #11 0x7fe06c14b0fe in xla::gpu::GpuExecutable::ExecuteAsyncOnStream(xla::ServiceExecutableRunOptions const*, absl::Span<xla::ShapedBuffer const* const>) /xla/service/gpu/gpu_executable.cc:864:23
    #12 0x7fddc002396b in xla::Executable::ExecuteOnStream(xla::ServiceExecutableRunOptions const*, absl::Span<xla::ShapedBuffer const* const>) /xla/service/executable.cc:82:7
    #13 0x7fe163d3abc1 in operator() /xla/service/hlo_runner.cc:670:43
    #14 0x7fe163d3abc1 in __invoke<(lambda at /xla/service/hlo_runner.cc:669:29) &> /src/libcxx/include/__type_traits/invoke.h:90:27
    #15 0x7fe163d3abc1 in __call<(lambda at /xla/service/hlo_runner.cc:669:29) &> /src/libcxx/include/__type_traits/invoke.h:350:5
    #16 0x7fe163d3abc1 in __invoke_r<void, (lambda at /xla/service/hlo_runner.cc:669:29) &> /src/libcxx/include/__type_traits/invoke.h:356:10
    #17 0x7fe163d3abc1 in void std::__u::__function::__policy_func<void ()>::__call_func<xla::HloRunner::ExecuteReplicated(xla::OpaqueExecutable*, xla::HloRunnerInterface::ReplicatedExecuteOptions const&, xla::DeviceAssignment*, xla::ExecutionProfile*)::$_0::operator()(std::__u::vector<xla::ServiceExecutableRunOptions, std::__u::allocator<xla::ServiceExecutableRunOptions>> const&, std::__u::vector<absl::Span<xla::ShapedBuffer const* const>, std::__u::allocator<absl::Span<xla::ShapedBuffer const* const>>> const&) const::'lambda0'()>(std::__u::__function::__policy_storage const*) /src/libcxx/include/__functional/function.h:443:12
    #18 0x7fdad5b9f44d in operator() /src/libcxx/include/__functional/function.h:502:12
    #19 0x7fdad5b9f44d in operator() /src/libcxx/include/__functional/function.h:754:10
    #20 0x7fdad5b9f44d in tsl::thread::EigenEnvironment::ExecuteTask(tsl::thread::EigenEnvironment::Task const&) /xla/tsl/platform/threadpool.cc:112:5
    #21 0x7fdad5b9e46f in Eigen::ThreadPoolTempl<tsl::thread::EigenEnvironment>::WorkerLoop(int) eigen3/unsupported/Eigen/CXX11/../../../Eigen/src/ThreadPool/NonBlockingThreadPool.h:365:41
    #22 0x7fdad5b9e2c4 in operator() eigen3/unsupported/Eigen/CXX11/../../../Eigen/src/ThreadPool/NonBlockingThreadPool.h:78:68
    #23 0x7fdad5b9e2c4 in __invoke<(lambda at ./eigen3/unsupported/Eigen/CXX11/../../../Eigen/src/ThreadPool/NonBlockingThreadPool.h:78:54) &> /src/libcxx/include/__type_traits/invoke.h:90:27
    #24 0x7fdad5b9e2c4 in __call<(lambda at ./eigen3/unsupported/Eigen/CXX11/../../../Eigen/src/ThreadPool/NonBlockingThreadPool.h:78:54) &> /src/libcxx/include/__type_traits/invoke.h:350:5
    #25 0x7fdad5b9e2c4 in __invoke_r<void, (lambda at ./eigen3/unsupported/Eigen/CXX11/../../../Eigen/src/ThreadPool/NonBlockingThreadPool.h:78:54) &> /src/libcxx/include/__type_traits/invoke.h:356:10
    #26 0x7fdad5b9e2c4 in void std::__u::__function::__policy_func<void ()>::__call_func<Eigen::ThreadPoolTempl<tsl::thread::EigenEnvironment>::ThreadPoolTempl(int, bool, tsl::thread::EigenEnvironment)::'lambda'()>(std::__u::__function::__policy_storage const*) /src/libcxx/include/__functional/function.h:443:12
    #27 0x7fdad5b9e162 in operator() /src/libcxx/include/__functional/function.h:502:12
    #28 0x7fdad5b9e162 in operator() /src/libcxx/include/__functional/function.h:754:10
    #29 0x7fdad5b9e162 in operator() /xla/tsl/platform/threadpool.cc:95:7
    #30 0x7fdad5b9e162 in __invoke<(lambda at /xla/tsl/platform/threadpool.cc:87:51) &> /src/libcxx/include/__type_traits/invoke.h:90:27
    #31 0x7fdad5b9e162 in invoke<(lambda at /xla/tsl/platform/threadpool.cc:87:51) &> /src/libcxx/include/__functional/invoke.h:29:10
    #32 0x7fdad5b9e162 in InvokeR<void, (lambda at /xla/tsl/platform/threadpool.cc:87:51) &> absl/functional/internal/any_invocable.h:121:5
    #33 0x7fdad5b9e162 in void absl::internal_any_invocable::RemoteInvoker<false, void, tsl::thread::EigenEnvironment::CreateThread(std::__u::function<void ()>)::'lambda'()&>(absl::internal_any_invocable::TypeErasedState*) absl/functional/internal/any_invocable.h:338:10
    #34 0x7fdad61d0464 in operator() absl/functional/internal/any_invocable.h:783:1
    #35 0x7fdad61d0464 in tsl::(anonymous namespace)::GoogleThread::FuncThread::Run() /xla/tsl/platform/google/env.cc:264:27
    #36 0x7fd77514525a in Thread::ThreadBody(void*) thread/thread.cc:1442:16
    #37 0x56541bdaa690 in asan_thread_start(void*) llvm/llvm-project/compiler-rt/lib/asan/asan_interceptors.cpp:246:28
    #38 0x7fe08e8347dc in start_thread (/lib64/libpthread.so.0+0xb7dc) (BuildId: 43d6c4d9186e9be3be4d4e41cb03a501)
    #39 0x7fe07dfbab7e in clone (/lib64/libc.so.6+0x13db7e) (BuildId: ca23ec6d935352118622ce674a8bb52d)

SUMMARY: AddressSanitizer: 400 byte(s) leaked in 2 allocation(s). (//xla/service/gpu/tests:collective_ops_command_buffer_test_2gpu)
-- 2026-01-15 21:42:36 PST Forge runner: Test failed with exit code 66 while running on ozeh8.prod.google.com
================================================================================
```


## Comment 3758332538

reporter (CONTRIBUTOR) · apivovarov · 2026-01-16T06:07:14Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758332538

Eugene, Shawn, could you guys take a look and share your thoughts on how to fix this? @ezhulenev  @shawnwang18 

## Comment 3758339331

reporter (CONTRIBUTOR) · apivovarov · 2026-01-16T06:10:26Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758339331

@beckerhe 

## Comment 3758341637

maintainer (MEMBER) · ezhulenev · 2026-01-16T06:11:33Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758341637

This does look like a leak in CUDA, something is getting allocated when graph is executed, and never released back.

## Comment 3758354453

other (CONTRIBUTOR) · shawnwang18 · 2026-01-16T06:17:27Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758354453

The leakage is known cuda bug, and we have a internal bug to work on this. The scenario is that:  the leaked marker is lazily created when a graph with user objects is launched. Subsequent launches will not leak additional markers. 

I think for some of the affected unittest, XLA is intentionally disabling leakage check. 

@apivovarov maybe disable the leakage test for now? 


## Comment 3758391561

reporter (CONTRIBUTOR) · apivovarov · 2026-01-16T06:33:15Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758391561

Got it. Thank you, Shawn! Thank you, Eugene!

## Comment 3758393326

reporter (CONTRIBUTOR) · apivovarov · 2026-01-16T06:34:04Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758393326

Shawn, can you provide cuda bug number?

## Comment 3758424192

other (CONTRIBUTOR) · shawnwang18 · 2026-01-16T06:44:30Z · https://github.com/openxla/xla/issues/36487#issuecomment-3758424192

Cuda internal number? 5519332  
What can you do externally with this number? 



## Comment 3761765714

reporter (CONTRIBUTOR) · apivovarov · 2026-01-16T20:49:24Z · https://github.com/openxla/xla/issues/36487#issuecomment-3761765714

I have not realized that
NVIDIA does not offer a public, searchable bug tracker; instead, they keep bug reports private for confidentiality, accessible only to the filer and NVIDIA personnel, requiring developers to file bugs directly through their support system or forums to get attention and updates.
