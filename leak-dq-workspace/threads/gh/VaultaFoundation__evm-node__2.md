# GCC reports mismatched-new-delete in some cases

- URL: https://github.com/VaultaFoundation/evm-node/issues/2
- Repo: VaultaFoundation/evm-node (language: Python)
- State: open; created 2023-07-11T10:26:30Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · yarkinwho · 2023-07-11T10:26:30Z · https://github.com/VaultaFoundation/evm-node/issues/2

Got the following compiler error in a ubuntu 22 VM on Mac M2 with gcc 11.3.0 

Not seen on other machines so the effect is minor. But we record the issue here just in case some other settings result in the same error.

Might related to when awaitable function becomes too large certain config makes it go into different alloc/free routine. Reducing the function size by take out some logics to another function seems help.

```
error: ‘static void boost::asio::detail::awaitable_frame_base<Executor>::operator delete(void*, std::size_t) [with Executor = boost::asio::any_io_executor]’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
  365 | }
      | ^
In file included from /home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/detail/handler_alloc_helpers.hpp:19,
                 from /home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/detail/executor_function.hpp:19,
                 from /home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/execution/any_executor.hpp:24,
                 from /home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/execution.hpp:19,
                 from /home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/any_io_executor.hpp:22,
                 from /home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/awaitable.hpp:29,
                 from /home/parallels/code/evm_repos/eos-evm-node/external/silkworm/silkworm/silkrpc/commands/ots_api.hpp:21,
                 from /home/parallels/code/evm_repos/eos-evm-node/external/silkworm/silkworm/silkrpc/commands/ots_api.cpp:17:
/home/parallels/.conan/data/boost/1.81.0/_/_/package/8899ea1c41c19e5e9e9ef65936e1bad21e84df83/include/boost/asio/detail/memory.hpp:120:33: note: returned from ‘void* aligned_alloc(size_t, size_t)’
  120 |   void* ptr = std::aligned_alloc(align, size);
      |               ~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~
```
