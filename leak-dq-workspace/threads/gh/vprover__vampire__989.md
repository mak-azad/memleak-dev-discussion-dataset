# SMT datatype parse errors leak allocations before registration

- URL: https://github.com/vprover/vampire/issues/989
- Repo: vprover/vampire (language: C++)
- State: open; created 2026-09-25T10:20:34Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · shalashaska117 · 2026-09-25T10:20:34Z · https://github.com/vprover/vampire/issues/989

SMT datatype rejection paths can lose constructor or algebra allocations before ownership is transferred to the signature. The malformed declarations should be rejected, but the temporary allocations should be released.

Tested on Linux x86-64 at production commit `af03e1547d9381cea97c051ed65a7918d07a2b0e`, using GCC 15.2.0, Valgrind 3.26.0 and a Debug build with `CHECK_LEAKS=ON` and Z3 enabled. No production fixes were applied. The commands below assume the repository dependencies are available:

```sh
cmake -S . -B build/memcheck -DCMAKE_BUILD_TYPE=Debug -DCHECK_LEAKS=ON
cmake --build build/memcheck --target vampire vtest -j4
```

Save this as `datatype-duplicate.smt2`:

```text
(declare-datatype Nat ((zero) (zero)))
```

```sh
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all \
  --errors-for-leak-kinds=definite,indirect,possible --track-origins=yes \
  --error-exitcode=97 --trace-children=yes \
  build/memcheck/vampire --input_syntax smtlib2 -t 0 datatype-duplicate.smt2
```

Excerpt from the recorded Valgrind XML, with the stack shortened:

```text
48 bytes in 1 blocks are definitely lost in loss record 9 of 15
  operator new(unsigned long) (vg_replace_malloc.c:488)
  Parse::SMTLIB2::buildTermAlgebraConstructor(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, Kernel::TermList, Lib::Stack<std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > >, Lib::Stack<Kernel::TermList>) (SMTLIB2.cpp:1139)
  Parse::SMTLIB2::readDeclareDatatype(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, Shell::LispParser::Expression*) (SMTLIB2.cpp:985)
  Parse::SMTLIB2::readBenchmark(Shell::LispParser::Expression*) (SMTLIB2.cpp:185)
```
A second input reaches the same ownership boundary after allocating the algebra:

```smt2
(declare-datatype Nat ((succ (pred Nat))))
```

Its current-master Valgrind output includes:

```text
64 bytes in 1 blocks are definitely lost in loss record 11 of 17
  operator new(unsigned long) (vg_replace_malloc.c:488)
  Parse::SMTLIB2::readDeclareDatatype(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, Shell::LispParser::Expression*) (SMTLIB2.cpp:990)
  Parse::SMTLIB2::readBenchmark(Shell::LispParser::Expression*) (SMTLIB2.cpp:185)
  Parse::SMTLIB2::parse(std::istream&) (SMTLIB2.cpp:82)
```


The constructor allocation is at [buildTermAlgebraConstructor](https://github.com/vprover/vampire/blob/af03e1547d9381cea97c051ed65a7918d07a2b0e/Parse/SMTLIB2.cpp#L1139); the algebra is allocated in [readDeclareDatatype](https://github.com/vprover/vampire/blob/af03e1547d9381cea97c051ed65a7918d07a2b0e/Parse/SMTLIB2.cpp#L990). The empty datatype produces a separate 64-byte definitely-lost algebra record at the latter location. Temporary ownership must survive exceptions until registration succeeds.

The duplicate `OperatorType` interning records in these processes are a separate finding. Cleanup of successfully registered term algebras also needs its own owner; fixing registration cleanup alone does not release allocations rejected before registration.

## Discovery and test

Found by running malformed SMT datatype inputs under Valgrind. The duplicate-constructor and empty-datatype tests below still produce their expected rejection diagnostics but leave allocations made before registration. Successful-registration cleanup and OperatorType interning are separate paths.

The campaign, strict Valgrind handling and failure-reporting methods are shared in [testing PR #978](https://github.com/vprover/vampire/pull/978). The input and direct command above reproduce the selected check without that runner.

