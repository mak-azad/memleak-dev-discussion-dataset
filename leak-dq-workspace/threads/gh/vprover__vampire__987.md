# TPTP parser leaks temporary type-declaration nodes

- URL: https://github.com/vprover/vampire/issues/987
- Repo: vprover/vampire (language: C++)
- State: open; created 2026-09-25T10:20:23Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · shalashaska117 · 2026-09-25T10:20:23Z · https://github.com/vprover/vampire/issues/987

A successful TPTP type declaration leaves a temporary type node allocated by `TPTP::simpleType()`.

Tested on Linux x86-64 at production commit `af03e1547d9381cea97c051ed65a7918d07a2b0e`, using GCC 15.2.0, Valgrind 3.26.0 and a Debug build with `CHECK_LEAKS=ON` and Z3 enabled. No production fixes were applied. The commands below assume the repository dependencies are available:

```sh
cmake -S . -B build/memcheck -DCMAKE_BUILD_TYPE=Debug -DCHECK_LEAKS=ON
cmake --build build/memcheck --target vampire vtest -j4
```

Save this as `typed.p`:

```text
tff(a_type,type,a:$i).
cnf(a,axiom,p(a)).
```

```sh
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all \
  --errors-for-leak-kinds=definite,indirect,possible --track-origins=yes \
  --error-exitcode=97 --trace-children=yes \
  build/memcheck/vampire -p off -t 0 typed.p
```

Excerpt from the recorded Valgrind XML, with the stack shortened:

```text
16 bytes in 1 blocks are definitely lost in loss record 6 of 20
  operator new(unsigned long) (vg_replace_malloc.c:488)
  Parse::TPTP::simpleType() (TPTP.cpp:4623)
  Parse::TPTP::parseImpl(Parse::TPTP::State) (TPTP.cpp:299)
  Parse::TPTP::parse() (TPTP.cpp:181)
```

The allocation is at [TPTP::simpleType](https://github.com/vprover/vampire/blob/af03e1547d9381cea97c051ed65a7918d07a2b0e/Parse/TPTP.cpp#L4623). The parser needs to retain ownership of its temporary type nodes through successful declarations and error paths, with child links remaining borrowed.

The 16-byte `simpleType` allocation is separate from the duplicate `OperatorType` candidate records also seen in this run. A historical six-case parser experiment covered atomic, product and polymorphic declarations and parser errors; it is supporting evidence, not a claim that every parser allocation is covered by this minimal current-master reproduction.

## Discovery and test

Found while checking typed TPTP inputs with Valgrind. The minimal declaration below retains a temporary simpleType allocation after a successful parse and solve, separately from OperatorType interning losses.

The campaign, strict Valgrind handling and failure-reporting methods are shared in [testing PR #978](https://github.com/vprover/vampire/pull/978). The input and direct command above reproduce the selected check without that runner.

