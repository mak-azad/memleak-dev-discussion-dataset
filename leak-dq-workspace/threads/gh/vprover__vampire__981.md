# OperatorType interning leaks duplicate candidate allocations

- URL: https://github.com/vprover/vampire/issues/981
- Repo: vprover/vampire (language: C++)
- State: open; created 2026-09-25T10:19:32Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · shalashaska117 · 2026-09-25T10:19:32Z · https://github.com/vprover/vampire/issues/981

`OperatorType::getTypeFromKey()` allocates a candidate before looking it up. When an equivalent type already exists, `find(resultType, resultType)` replaces the candidate pointer with the shared result. The key is released, but the candidate object is lost.

Tested on Linux x86-64 at production commit `af03e1547d9381cea97c051ed65a7918d07a2b0e`, using GCC 15.2.0, Valgrind 3.26.0 and a Debug build with `CHECK_LEAKS=ON` and Z3 enabled. No production fixes were applied. The commands below assume the repository dependencies are available:

```sh
cmake -S . -B build/memcheck -DCMAKE_BUILD_TYPE=Debug -DCHECK_LEAKS=ON
cmake --build build/memcheck --target vampire vtest -j4
```

Save this as `true.p`:

```text
cnf(a,axiom,$true).
```

```sh
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all \
  --errors-for-leak-kinds=definite,indirect,possible --track-origins=yes \
  --error-exitcode=97 --trace-children=yes \
  build/memcheck/vampire -p off -t 0 true.p
```

Excerpt from the recorded Valgrind XML, with the stack shortened:

```text
16 bytes in 1 blocks are definitely lost in loss record 2 of 15
  operator new(unsigned long) (vg_replace_malloc.c:488)
  Kernel::OperatorType::getTypeFromKey(Lib::Vector<Kernel::TermList>*, unsigned int) (OperatorType.cpp:66)
  Kernel::OperatorType::getFunctionTypeUniformRange(unsigned int, Kernel::TermList, Kernel::TermList, unsigned int) (OperatorType.hpp:136)
  Kernel::OperatorType::getTypeConType(unsigned int) (OperatorType.hpp:151)
```

The source path is [OperatorType::getTypeFromKey](https://github.com/vprover/vampire/blob/af03e1547d9381cea97c051ed65a7918d07a2b0e/Kernel/OperatorType.cpp#L57). The minimal solve produces four 16-byte definitely-lost records from startup sort registration; repeated interning also exercises the same allocation path. The expected behavior is to release an unused candidate while retaining pointer sharing and the existing key ownership rules.

These records are separate from the cached `Property` leak and timer shutdown reads also present in this process. The total number of leak records is not a count of distinct bugs.

## Discovery and test

Found while grouping repeated Valgrind allocation records from the cleanup-enabled campaign. The true-only solve below retains the four startup records, and inspection of the interning lookup identifies the discarded candidate. The other leak groups are kept separate.

The campaign, strict Valgrind handling and failure-reporting methods are shared in [testing PR #978](https://github.com/vprover/vampire/pull/978). The input and direct command above reproduce the selected check without that runner.

