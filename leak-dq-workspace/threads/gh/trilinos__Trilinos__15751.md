# ShyLU: Memory leaks

- URL: https://github.com/trilinos/Trilinos/issues/15751
- Repo: trilinos/Trilinos (language: C++)
- State: open; created 2026-10-03T20:31:33Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · cgcgcg · 2026-10-03T20:31:33Z · https://github.com/trilinos/Trilinos/issues/15751

## Bug Report

https://my.cdash.org/builds/4222502/tests?filters=%7B%22all%22%3A%5B%7B%22eq%22%3A%7B%22status%22%3A%22FAILED%22%7D%7D%5D%7D
shows memory leaks in a few ShyLU tests.

ShyLU_NodeBasker_basker_amesos2_coverage_test_14
ShyLU_NodeBasker_basker_amesos_test_1
```
Direct leak of 2308080 byte(s) in 1 object(s) allocated from:
    #0 0x563c32e1d98d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x563c32e235d5 in void readMatrix<long, double>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, long&, long&, long&, long**, long**, double**) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/test_util.hpp:78:18
    #2 0x563c32e2037e in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp:52:3
    #3 0x7fd7ac43560f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 2308080 byte(s) in 1 object(s) allocated from:
    #0 0x563c32e1d98d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x563c32e23585 in void readMatrix<long, double>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, long&, long&, long&, long**, long**, double**) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/test_util.hpp:77:18
    #2 0x563c32e2037e in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp:52:3
    #3 0x7fd7ac43560f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 472568 byte(s) in 1 object(s) allocated from:
    #0 0x563c32e1d98d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x563c32e2352e in void readMatrix<long, double>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, long&, long&, long&, long**, long**, double**) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/test_util.hpp:76:18
    #2 0x563c32e2037e in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp:52:3
    #3 0x7fd7ac43560f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 472560 byte(s) in 1 object(s) allocated from:
    #0 0x563c32e1d98d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x563c32e218f2 in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp:167:19
    #2 0x7fd7ac43560f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)
```

ShyLU_NodeBasker_basker_test_4	
ShyLU_NodeBasker_basker_test_1	
```
Direct leak of 2308080 byte(s) in 1 object(s) allocated from:
    #0 0x561b3f1b059d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x561b3f1b37f1 in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/basker_test.cpp:112:15
    #2 0x7f20c1e2260f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 2308080 byte(s) in 1 object(s) allocated from:
    #0 0x561b3f1b059d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x561b3f1b382b in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/basker_test.cpp:115:12
    #2 0x7f20c1e2260f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 472568 byte(s) in 1 object(s) allocated from:
    #0 0x561b3f1b059d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x561b3f1b37b7 in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/basker_test.cpp:109:15
    #2 0x7f20c1e2260f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 472560 byte(s) in 1 object(s) allocated from:
    #0 0x561b3f1b059d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x561b3f1b3b90 in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/basker_test.cpp:161:14
    #2 0x7f20c1e2260f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 472560 byte(s) in 1 object(s) allocated from:
    #0 0x561b3f1b059d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x561b3f1b3bac in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/basker_test.cpp:162:14
    #2 0x7f20c1e2260f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)

Direct leak of 472560 byte(s) in 1 object(s) allocated from:
    #0 0x561b3f1b059d in operator new[](unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:89:3
    #1 0x561b3f1d2558 in BaskerNS::Basker<long, double, Kokkos::Serial>::GetPerm(long**, long**) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/src/shylubasker_def.hpp:2109:13
    #2 0x561b3f1b425b in main /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/basker/test/basker_test.cpp:199:12
    #3 0x7f20c1e2260f in __libc_start_call_main (/lib64/libc.so.6+0x2a60f) (BuildId: 07d89210779b8a108b40c1f58cb0a0e1cb22ee00)
```
ShyLU_NodeTacho_Tacho_TestSolver.x_MPI_1
```
Direct leak of 304 byte(s) in 1 object(s) allocated from:
    #0 0x55a15899599d in operator new(unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x7f3cf9ab29a1 in Tacho::NumericToolsLevelSet<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>, 3>::NumericToolsLevelSet(int, int, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, int, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&, Kokkos::View<int*, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>> const&) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_LevelSet.hpp:748:15
    #2 0x7f3cf9a85002 in Tacho::NumericToolsFactory<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>::createObject(Tacho::NumericToolsBase<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>*&) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_Factory.hpp:162:5
    #3 0x7f3cf9a833db in Tacho::Driver<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>::initialize() /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp:451:13
    #4 0x55a1589b93ef in int driver<double>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, int, int, bool, bool, bool, bool, bool, bool) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/unit-test/Tacho_TestSolver.cpp:180:24
    #5 0x55a1589a1ca5 in Solver_LU_Test::TestBody() /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/unit-test/Tacho_TestSolver.cpp:361:3
    #6 0x7f3cf98489c8 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/home/runner/spack/opt/spack/linux-x86_64/googletest-1.17.0-n6dsw6xh7uprlz66jgsxd2zbawsmf6wz/lib64/libgtest.so.1.17.0+0x5d9c8)

Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x55a15899599d in operator new(unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x7f3cf9b8d976 in __gnu_cxx::new_allocator<Kokkos::Serial>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/ext/new_allocator.h:127:27
    #2 0x7f3cf9b8d976 in std::allocator<Kokkos::Serial>::allocate(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/allocator.h:185:32
    #3 0x7f3cf9b8d976 in std::allocator_traits<std::allocator<Kokkos::Serial>>::allocate(std::allocator<Kokkos::Serial>&, unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/alloc_traits.h:464:20
    #4 0x7f3cf9b8d976 in std::_Vector_base<Kokkos::Serial, std::allocator<Kokkos::Serial>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/stl_vector.h:346:20
    #5 0x7f3cf9b8d976 in std::vector<Kokkos::Serial, std::allocator<Kokkos::Serial>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/vector.tcc:635:34
    #6 0x7f3cf9cdacec in std::vector<Kokkos::Serial, std::allocator<Kokkos::Serial>>::resize(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/stl_vector.h:940:4
    #7 0x7f3cf9cdacec in Tacho::NumericToolsLevelSet<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>, 3>::createStream(int, int) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_LevelSet.hpp:854:21
    #8 0x7f3cf9ab7a24 in Tacho::NumericToolsLevelSet<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>, 3>::initialize(int, int, int, int, bool, bool, int) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_LevelSet.hpp:646:5
    #9 0x7f3cf9a85145 in Tacho::NumericToolsFactory<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>::createObject(Tacho::NumericToolsBase<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>*&) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_Factory.hpp:162:5
    #10 0x7f3cf9a833db in Tacho::Driver<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>::initialize() /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp:451:13
    #11 0x55a1589b93ef in int driver<double>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, int, int, bool, bool, bool, bool, bool, bool) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/unit-test/Tacho_TestSolver.cpp:180:24
    #12 0x55a1589a1ca5 in Solver_LU_Test::TestBody() /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/unit-test/Tacho_TestSolver.cpp:361:3
    #13 0x7f3cf98489c8 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/home/runner/spack/opt/spack/linux-x86_64/googletest-1.17.0-n6dsw6xh7uprlz66jgsxd2zbawsmf6wz/lib64/libgtest.so.1.17.0+0x5d9c8)

Direct leak of 4 byte(s) in 1 object(s) allocated from:
    #0 0x55a15899599d in operator new(unsigned long) /tmp/runner/spack-stage/spack-stage-llvm-19.1.7-qtsgqxi6wza5uklztrmz3fbnyjsbp6v3/spack-src/compiler-rt/lib/asan/asan_new_delete.cpp:86:3
    #1 0x7f3cf9b8d695 in __gnu_cxx::new_allocator<int>::allocate(unsigned long, void const*) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/ext/new_allocator.h:127:27
    #2 0x7f3cf9b8d695 in std::allocator<int>::allocate(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/allocator.h:185:32
    #3 0x7f3cf9b8d695 in std::allocator_traits<std::allocator<int>>::allocate(std::allocator<int>&, unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/alloc_traits.h:464:20
    #4 0x7f3cf9b8d695 in std::_Vector_base<int, std::allocator<int>>::_M_allocate(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/stl_vector.h:346:20
    #5 0x7f3cf9b8d695 in std::vector<int, std::allocator<int>>::_M_default_append(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/vector.tcc:635:34
    #6 0x7f3cf9cdaba4 in std::vector<int, std::allocator<int>>::resize(unsigned long) /usr/lib/gcc/x86_64-redhat-linux/11/../../../../include/c++/11/bits/stl_vector.h:940:4
    #7 0x7f3cf9cdaba4 in Tacho::NumericToolsLevelSet<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>, 3>::createStream(int, int) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_LevelSet.hpp:850:14
    #8 0x7f3cf9ab7a24 in Tacho::NumericToolsLevelSet<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>, 3>::initialize(int, int, int, int, bool, bool, int) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_LevelSet.hpp:646:5
    #9 0x7f3cf9a85145 in Tacho::NumericToolsFactory<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>::createObject(Tacho::NumericToolsBase<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>*&) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_NumericTools_Factory.hpp:162:5
    #10 0x7f3cf9a833db in Tacho::Driver<double, Kokkos::Device<Kokkos::Serial, Kokkos::HostSpace>>::initialize() /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp:451:13
    #11 0x55a1589b93ef in int driver<double>(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char>>, int, int, bool, bool, bool, bool, bool, bool) /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/unit-test/Tacho_TestSolver.cpp:180:24
    #12 0x55a1589a1ca5 in Solver_LU_Test::TestBody() /home/Trilinos/build/../../runner/_work/Trilinos/Trilinos/packages/shylu/shylu_node/tacho/unit-test/Tacho_TestSolver.cpp:361:3
    #13 0x7f3cf98489c8 in void testing::internal::HandleExceptionsInMethodIfSupported<testing::Test, void>(testing::Test*, void (testing::Test::*)(), char const*) (/home/runner/spack/opt/spack/linux-x86_64/googletest-1.17.0-n6dsw6xh7uprlz66jgsxd2zbawsmf6wz/lib64/libgtest.so.1.17.0+0x5d9c8)
```

## Comment 5973263218

other (NONE) · trilinos-bot[bot] · 2026-10-03T20:37:50Z · https://github.com/trilinos/Trilinos/issues/15751#issuecomment-5973263218

# ShyLU Memory Leaks Investigation

## Summary
ASAN reports direct leaks in three ShyLU test suites:

1. `ShyLU_NodeBasker_basker_amesos2_coverage_test_14` / `ShyLU_NodeBasker_basker_amesos_test_1`
2. `ShyLU_NodeBasker_basker_test_4` / `ShyLU_NodeBasker_basker_test_1`
3. `ShyLU_NodeTacho_Tacho_TestSolver.x_MPI_1`

## Root Causes

### Basker Amesos2 interface test
`packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp`
- `readMatrix` allocates `col_ptr`, `row_idx`, `val` with `new[]` in `test_util.hpp:76-78` and never frees them.
- `yt` is allocated with `new Entry[m]()` at line 167 for transpose solve and is never deleted. The same pattern exists for the copy-transpose path.
- `x`, `xhat`, `y` are freed but matrix arrays are not.

### Basker test
`packages/shylu/shylu_node/basker/test/basker_test.cpp`
- Matrix arrays `col_ptr`, `row_idx`, `vals` allocated at lines 109,112,115 are never freed.
- RHS arrays `y` and `x` allocated at lines 161-162 are never freed.
- `GetPerm` allocates `lperm`/`rperm` with `new Int[gn]` in `shylubasker_def.hpp:2109-2110`. The caller never deletes them.

### Tacho TestSolver
`packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp`
- `Driver::initialize` calls `factory.createObject(_N)`. The factory macro reuses an existing `_N` pointer with placement new without destroying the previous object first.
- When the test performs multiple setups, `initialize` is called repeatedly. The previous `NumericToolsLevelSet` instance is overwritten, leaking its resources, e.g. `_spmv = new SpMV_type(...)` at `Tacho_NumericTools_LevelSet.hpp:748`, and `std::vector` members used in `createStream`.
- The destructor and `release` are never invoked for the replaced object.

## Fixes Applied
- Add `delete[]` for matrix and temporary arrays in both Basker tests.
- Delete permutation arrays returned by `GetPerm`.
- Make `Driver::initialize` release and delete an existing `_N` before creating a new numeric tools object.

These changes eliminate the ASAN direct leaks reported in the CDash builds.


# Suggested changes

```diff
diff --git a/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp b/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp
index be2ca7de5b2..47fd2235504 100644
--- a/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp
+++ b/packages/shylu/shylu_node/basker/test/amesos2_interface_test.cpp
@@ -206,6 +206,7 @@ int main(int argc, char* argv[])
       std::cout << "   Matrix: " << mname << "(" << m << "x" << n << ")"
         << std::endl;
       delete [] e;
+      delete [] yt;
 
     }
     mybasker.Finalize();
@@ -271,6 +272,9 @@ int main(int argc, char* argv[])
   delete [] y;
   delete [] x;
   delete [] xhat;
+  delete [] col_ptr;
+  delete [] row_idx;
+  delete [] val;
   
   Kokkos::finalize();
 
diff --git a/packages/shylu/shylu_node/basker/test/basker_test.cpp b/packages/shylu/shylu_node/basker/test/basker_test.cpp
index e10783e2041..c01db4ad75c 100644
--- a/packages/shylu/shylu_node/basker/test/basker_test.cpp
+++ b/packages/shylu/shylu_node/basker/test/basker_test.cpp
@@ -199,6 +199,13 @@ int main(int argc, char* argv[])
   mybasker.GetPerm(&lperm, &rperm);
   mybasker.Finalize();
   cout << "--------------Called Finalize-----------------"<<endl;
+  delete [] lperm;
+  delete [] rperm;
+  delete [] col_ptr;
+  delete [] row_idx;
+  delete [] vals;
+  delete [] y;
+  delete [] x;
  
   //}//After
   //Kokkos::fence();
diff --git a/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp b/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp
index 755d3f5fbd6..da06ed297c4 100644
--- a/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp
+++ b/packages/shylu/shylu_node/tacho/src/impl/Tacho_Driver_Impl.hpp
@@ -440,6 +440,11 @@ template <typename VT, typename DT> int Driver<VT, DT>::initialize() {
     ///
     /// create numeric tools serial for host space
     ///
+    if (_N != nullptr) {
+      _N->release(_verbose);
+      delete _N;
+      _N = nullptr;
+    }
     NumericToolsFactory<VT, DT> factory;
     factory.setBaseMember(_method, _m, _ap, _aj, _perm, _peri, _nsupernodes, _supernodes, _gid_super_panel_ptr,
                           _gid_super_panel_colidx, _sid_super_panel_ptr, _sid_super_panel_colidx,

```

The patch can be applied by running
```bash

commonTools/patchFromComment/getPatchFromComment.sh apply trilinos/Trilinos/issue/15751#issuecomment-5973263218

```


---

These suggestions were made by a bot.

<details>
<summary>Instructions for triggering LLM actions</summary>

Member of the [Pretest-Inspectors team](https://github.com/orgs/trilinos/teams/pretest-inspectors) can trigger an LLM action by adding one of the following labels to an open PR:

- `Automated review requested`: Review the PR.
- `Automated fix requested`: Attempt to fix build errors observed in the CI builds.
- `Automated documentation requested`: Improve the documentation of the code that was changed in the PR.

No code changes will be made directly to the PR branch. Instead, a message will be posted with suggestions and instructions for applying them to a local checkout.

</details>

## Comment 6026231821

other (CONTRIBUTOR) · iyamazaki · 2026-10-06T21:59:54Z · https://github.com/trilinos/Trilinos/issues/15751#issuecomment-6026231821

Thank you for the report, @cgcgcg. Please let me know if this did not get fixed by https://github.com/trilinos/Trilinos/pull/15757.

## Comment 6026733817

reporter (CONTRIBUTOR) · cgcgcg · 2026-10-06T22:38:04Z · https://github.com/trilinos/Trilinos/issues/15751#issuecomment-6026733817

Thanks! The ASAN build will post fresh results tomorrow.
