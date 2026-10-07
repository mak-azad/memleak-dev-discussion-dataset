# Two Deque unit tests leak their heap-allocated containers

- URL: https://github.com/vprover/vampire/issues/990
- Repo: vprover/vampire (language: C++)
- State: open; created 2026-09-25T10:20:39Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · shalashaska117 · 2026-09-25T10:20:39Z · https://github.com/vprover/vampire/issues/990

Two existing `Deque` unit tests leave their outer container allocation behind. This is test-fixture cleanup, not evidence that the production `Deque` implementation leaks during solver use.

Tested on Linux x86-64 at production commit `af03e1547d9381cea97c051ed65a7918d07a2b0e`, using GCC 15.2.0, Valgrind 3.26.0 and a Debug build with `CHECK_LEAKS=ON` and Z3 enabled. No production fixes were applied. The commands below assume the repository dependencies are available:

```sh
cmake -S . -B build/memcheck -DCMAKE_BUILD_TYPE=Debug -DCHECK_LEAKS=ON
cmake --build build/memcheck --target vampire vtest -j4
```
```sh
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all \
  --errors-for-leak-kinds=definite,indirect,possible --track-origins=yes \
  --error-exitcode=97 --trace-children=yes \
  build/memcheck/vtest run Deque
```


The current-master run records a 40-byte definitely-lost container allocation for each test. One excerpt is:

```text
40 bytes in 1 blocks are definitely lost in loss record 68 of 182
  operator new(unsigned long) (vg_replace_malloc.c:488)
  __testFn__Deque__push_front_pop_back_expand() (tDeque.cpp:17)
  Test::TestUnit::spawnTest(void (*)()) (UnitTesting.cpp:194)
  Test::TestUnit::runTestsWithNameSubstring(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, std::ostream&) (UnitTesting.cpp:144)
```

[push_front_pop_back_expand](https://github.com/vprover/vampire/blob/af03e1547d9381cea97c051ed65a7918d07a2b0e/UnitTests/tDeque.cpp#L15) allocates `a_deque` and does not destroy it. [size_reset_desctructor](https://github.com/vprover/vampire/blob/af03e1547d9381cea97c051ed65a7918d07a2b0e/UnitTests/tDeque.cpp#L29) explicitly calls `~Deque()` but does not free the outer allocation. Normal scoped lifetime or `delete` would release both the contents and object storage while retaining the intended assertions.

The startup `OperatorType` records are separate and should not be attributed to these fixtures.

## Discovery and test

Found by running the existing `Deque` unit suite under Valgrind. The allocation stacks lead directly to `push_front_pop_back_expand` and `size_reset_desctructor`; source inspection confirms the missing outer-object deallocation in each fixture.

The campaign, strict Valgrind handling and failure-reporting methods are shared in [testing PR #978](https://github.com/vprover/vampire/pull/978). The input and direct command above reproduce the selected check without that runner.

