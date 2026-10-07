# co_composed produces mismatched new/delete

- URL: https://github.com/chriskohlhoff/asio/issues/1391
- Repo: chriskohlhoff/asio (language: C++)
- State: open; created 2023-12-05T18:46:11Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · justend29 · 2023-12-05T18:46:11Z · https://github.com/chriskohlhoff/asio/issues/1391

Forward: asio is a gift to humanity.

## Issue

GCC's `-Wmismatched-new-delete` warns on usages of co_composed. Although this may be spurious, it could indicate an intrinsic issue.
The warnings can be reproduced with asio's native tests of co_composed.

## Reproduction

I'm not sure how to compile & run individual tests in asio, but the tests of concern are those in `asio/src/tests/unit/experimental/co_composed.cpp`. Reproducing these warnings was accomplished with GCC 13.2.1 through:

```bash
git clone https://github.com/chriskohlhoff/asio.git
cd asio/asio
./autogen.sh
./configure CXXFLAGS='-std=c++20 -Wmismatche-new-delete'
make check
```

## Sample Warning

```
unit/experimental/co_composed.cpp: In lambda function:
unit/experimental/co_composed.cpp:169:9: warning: ‘static void asio::experimental::detail::co_composed_promise<Execu
tors, Handler, Return>::operator delete(void*, std::size_t) [with Executors = void(asio::io_context::basic_executor_type<std::allocator<void>, 0>); Handler = asio::experimental::detail::co_composed_handler<void(asio::io_context::basic_executor_type<std::allocator<void>, 0>), test_nested_post_loop()::<lambda(int)>, asio::experimental::detail::co_composed_returns<>, void()>; Return = asio::experimental::detail::co_composed_returns<>]’ called on pointer returned from a mismatched allocation function [-Wmismatched-new-delete]
  169 |         [](auto state, asio::io_context& ctx) -> void
      |         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  170 |         {
      |         ~
  171 |           co_await asio::post(ctx, asio::deferred);
      |           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  172 |           co_yield state.complete();
      |           ~~~~~~~~~~~~~~~~~~~~~~~~~~
  173 |         }, ctx), token, std::ref(ctx));
      |         ~
unit/experimental/co_composed.cpp:169:9: note: returned from ‘static void* asio::experimental::detail::co_composed_promise<Executors, Handler, Return>::operator new(std::size_t, C&&, asio::experimental::detail::co_composed_state<Executors, Handler, Return>&, Args&& ...) [with C = const nested_post<const asio::deferred_t&>(asio::io_context&, const asio::deferred_t&)::<lambda(auto:51, asio::io_context&)>&; Args = {asio::io_context&}; Executors = void(asio::io_context::basic_executor_type<std::allocator<void>, 0>); Handler = asio::experimental::detail::co_composed_handler<void(asio::io_context::basic_executor_type<std::allocator<void>, 0>), test_nested_post_loop()::<lambda(int)>, asio::experimental::detail::co_composed_returns<>, void()>; Return = asio::experimental::detail::co_composed_returns<>]’
  169 |         [](auto state, asio::io_context& ctx) -> void
      |         ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  170 |         {
      |         ~
  171 |           co_await asio::post(ctx, asio::deferred);
      |           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  172 |           co_yield state.complete();
      |           ~~~~~~~~~~~~~~~~~~~~~~~~~~
  173 |         }, ctx), token, std::ref(ctx));
      |         ~
```
