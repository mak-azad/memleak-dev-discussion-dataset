# Coroutine frame corruption on aarch64 + gcc: reference-captured lambdas cause bad-free / use-after-free

- URL: https://github.com/alibaba/yalantinglibs/issues/1210
- Repo: alibaba/yalantinglibs (language: C++)
- State: open; created 2026-07-27T01:00:23Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · shenxuebing · 2026-07-27T01:00:23Z · https://github.com/alibaba/yalantinglibs/issues/1210

## Summary

async_simple `Lazy` coroutine frames corrupt reference-captured lambda members on **aarch64 + gcc 11**, causing crashes (`bad-free`, `use-after-free`) when the coroutine is resumed from a different thread (e.g., io_context thread processing an RPC response). **x86_64 + gcc is unaffected.**

## Environment

- **CPU architecture**: aarch64 (ARM64)
- **Compiler**: gcc 11.4.0 (also reproduced with gcc 13.3.0)
- **OS**: Kylin Linux Advanced Server V10 (Sword)
- **async_simple**: bundled with yalantinglibs (latest `main` as of 2026-07)
- **Note**: x86_64 + gcc 11/13 **does not** reproduce. clang on aarch64 not tested.

## Reproduction

### Setup

A `client_pool::send_request()` call with a lambda that captures local variables **by reference** and contains `co_await`:

```cpp
// Application thread calls:
syncAwait(client.call<&MyService::myRpc>(req, resp));

// Inside VyrionClient::requestRpc (a Lazy coroutine):
auto ec = co_await pool->send_request(
    [&req, &resp](coro_rpc_client& client) -> Lazy<bool> {
        // This lambda becomes a coroutine. Its reference captures (&req, &resp)
        // are stored as members of the coroutine frame.
        auto result = co_await client.call<&MyService::myRpc>(req);
        // ^^^ coroutine suspends here, waiting for RPC response
        resp = result.value();
        co_return true;
    });
```

### What happens

1. Application thread calls `syncAwait(requestRpc(...))`, blocking.
2. `requestRpc` is a `Lazy` coroutine. It calls `pool->send_request(lambda)`.
3. `send_request` is also a `Lazy` coroutine. It `co_await`s the lambda.
4. The lambda's `co_await client.call<RpcMethod>(req)` sends the RPC request and **suspends**.
5. The **io_context thread** receives the RPC response and resumes the coroutine chain:
   `client.call` → lambda → `send_request` → `requestRpc`.
6. **Crash** during resume at `LazyAwaiterBase::awaitResume()`.

### Crash backtrace (gdb)

```
#0  0x... in raise () from /usr/lib64/libc.so.6
#1  0x... in abort () from /usr/lib64/libc.so.6
#2  0x... in __libc_message () from /usr/lib64/libc.so.6
#3  0x... in munmap_chunk () from /usr/lib64/libc.so.6
#4  0x... in operator delete(void*, unsigned long)
#5  0x... in client_pool<...>::send_request(...)::_Z...Frame*) [clone .actor]
#6  0x... in LazyAwaiterBase<expected<bool, errc>>::awaitResume()
#7  0x... in VyrionClient::requestRpc<...>(...)::_Z...Frame*) [clone .actor]
#8  0x... in FutureState<...>::scheduleContinuation(bool)
#9  0x... in coro_rpc_client::handler_t::operator()(resp_body&&, unsigned char)
#10 0x... in coro_rpc_client::recv(...)::_Z...Frame*) [clone .actor]
#11 0x... in reactive_socket_recv_op<...>::do_complete(...)
#12 0x... in scheduler::do_run_one(...)
#13 0x... in scheduler::run(...)
#14 0x... in io_context_pool::run()::{lambda(...)#1}::operator()()
```

### ASan report

```
==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0xffff90105b80
    #0 operator delete(void*, unsigned long)
    #1 new_allocator<char>::deallocate
    ...
    #7 GenRandomV6Request::~GenRandomV6Request()
    #8 {lambda}::~coro_http_response()
    #9 execute_coroutine_with_timeout

0xffff90105b80 is located 608 bytes inside of 672-byte region [0xffff90105b00,0xffff90105da0)
allocated by thread T22 here:
    #0 operator new[](unsigned long, std::nothrow_t const&)
    #1 PromiseAllocator<void, true>::operator new(unsigned long)

SUMMARY: AddressSanitizer: bad-free
```

Key observation: The freed address is **inside a PromiseAllocator-allocated coroutine frame** (672 bytes, offset 608). The corrupted memory belongs to an SSO string (`requestId`) inside a request struct captured by the lambda.

## Root Cause Analysis

The issue is in how `Lazy` coroutine frames handle **reference members** on aarch64:

1. A lambda capturing `[&req, &resp]` creates reference members inside the lambda object.
2. When this lambda becomes a `Lazy` coroutine (returned by `operator()`), the lambda object is stored in the coroutine frame allocated by `PromiseAllocator`.
3. On **x86_64**, the frame layout and destruction order work correctly.
4. On **aarch64 + gcc**, the frame's reference members appear to be corrupted during `resume()` or `destroy()` — possibly due to different alignment rules, member layout, or destruction order on the aarch64 ABI.

The corruption specifically affects:
- SSO (Small String Optimization) strings inside captured structs — the string's internal length/data pointer gets overwritten with garbage.
- When the coroutine frame is destroyed, the corrupted string attempts to `free()` an address pointing **inside the coroutine frame itself** → `bad-free`.

## Workaround

**Capture local variables by value instead of by reference** in lambdas passed to coroutines:

```cpp
// ❌ Crashes on aarch64
co_await pool->send_request(
    [&req, &resp](auto& client) -> Lazy<bool> {
        co_await client.call<METHOD>(req);
        resp = result;
    });

// ✅ Safe on all platforms
RespType* respPtr = &resp;  // pointer is POD, ABI-stable
co_await pool->send_request(
    [req, respPtr](auto& client) -> Lazy<bool> {
        co_await client.call<METHOD>(req);
        *respPtr = result;
    });
```

This workaround has been verified on aarch64 + gcc 11.4.0 and gcc 13.3.0.

## Why this matters

This is a **silent landmine** for ARM server deployments:
- Code works perfectly on x86_64 development machines.
- Crashes on aarch64 production servers.
- The crash is **deterministic** (every call crashes, not intermittent).
- Developers unfamiliar with coroutine internals will struggle to diagnose it.


## Comment 5118466082

maintainer (COLLABORATOR) · qicosmos · 2026-07-29T13:34:01Z · https://github.com/alibaba/yalantinglibs/issues/1210#issuecomment-5118466082

@shenxuebing 

我看了一下这个 issue 和当前 `main`（`c1cef74057b139944c982d840c09c9940f26e08e`）里的相关路径，结论是：建议先不要把根因锁定为“reference-captured lambda 导致 Lazy coroutine frame crash”。

几点观察：

1. `client_pool::send_request(T op, ...)` 是按值接收 `op`，并在自己的 coroutine 中执行 `co_await op(*client)`。因此这个包装层本身会把 closure 作为 `send_request` coroutine 的状态持有，不能直接等同于典型的 immediately-invoked capturing coroutine lambda 里 closure 已销毁的问题。

2. C++ coroutine lambda 的捕获确实是危险点，CP.51/CP.53 都建议避免捕获型 coroutine lambda、避免 coroutine 参数按引用跨 suspend 使用。但通常问题是 coroutine 挂起后仍访问已经销毁的 closure 或引用对象，而不是“捕获成员被复制进 coroutine frame 后被 aarch64 ABI crash”。这里还需要看到 `requestRpc` 的完整签名和 `req/resp` 的真实生命周期，才能证明 `[&req, &resp]` 是根因。

3. 更可疑的是 yalantinglibs vendored 的 `async_simple` 落后于上游，而且缺少几个和 aarch64/恢复路径高度相关的修复：
   - https://github.com/alibaba/async_simple/commit/ab5ab2edc2970c02cc97ed5571497fb573848efb ，提交信息是 `fix futureAwaiter test failed in aarch64`，在 `FutureAwaiter` 里增加了 ARM 相关 fence。
   - https://github.com/alibaba/async_simple/commit/12c2a726f5112143ea11e0664b2ac7099f5a7d94 ，提交信息是 `try to fix aarch64 memory order`，加强了 `FutureState`/`Signal` 等处的 memory order。
   - https://github.com/alibaba/async_simple/commit/dd30504fca27786c5f17e85c826f64e840888ff6 ，让 lvalue awaiter 不再被无条件拷贝，也建议一起同步。

4. 这个 issue 的 backtrace 正好经过 `FutureState<...>::scheduleContinuation(bool)`，而 `coro_rpc_client` 的响应路径是 `handler_t::operator()` 调 `promise_.setValue(...)`，然后恢复 `co_await std::move(future)` 等待的 coroutine 链。所以缺少上述 aarch64 memory-order/FutureAwaiter 修复，比单纯的 lambda 引用捕获解释更贴近当前调用链。

建议先在 aarch64 + GCC 11/13 环境里 cherry-pick 或同步上游 `async_simple` 的上述提交后复测。如果同步后仍然复现，再提供一个最小 repro（包含 `requestRpc` 签名、`req/resp` 生命周期、是否使用 `LazyLocal`/cancellation slot、编译选项和 ASan 选项），这样才能继续判断是不是 GCC/aarch64 coroutine frame layout 或引用生命周期问题。

## Comment 5126921890

reporter (CONTRIBUTOR) · shenxuebing · 2026-07-30T05:19:52Z · https://github.com/alibaba/yalantinglibs/issues/1210#issuecomment-5126921890

我在CentOS 7.9 + GCC 11.5 的 x86_64 还是崩溃，arm64下测试依然崩溃。

该问题不只出现在 ARM 的引用捕获场景，在 x86_64 + GCC 11.5 下，lambda 按值捕获包含 std::string 的请求对象
  同样会触发 bad-free。ASan 显示非法释放地址位于 async_simple 协程帧内部。将 req、addr 等复杂对象改为仅捕获指针后，ARM
  和 x86_64 均不再崩溃。因此问题可能是 YLT/async_simple 与 GCC C++20 协程在处理非平凡 lambda 捕获对象时的兼容性或生命周
  期缺陷，而不只是引用捕获问题。

  在WSL 环境下测试正常，暂未复现该问题；但在 CentOS 7.9 + GCC 11.5 的 x86_64 和 ARM 环境中，lambda 捕获
  包含 std::string 的对象时出现 bad-free。ASan 显示非法释放地址位于 async_simple 协程帧内部。将 req、addr 等复杂对象改为
  仅捕获指针后，问题消失，初步判断与特定 GCC/YLT/async_simple 组合下的协程帧生命周期处理有关。
