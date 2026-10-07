# C++ interface example outputs "double free or corruption (out)"

- URL: https://github.com/bgrimstad/splinter/issues/138
- Repo: bgrimstad/splinter (language: C++)
- State: open; created 2024-04-17T09:46:44Z; status ok; passes main

## Issue body

reporter (NONE) · victor-kowalski-m · 2024-04-17T09:46:44Z · https://github.com/bgrimstad/splinter/issues/138

Hello,

I tried to execute the provided C++ interface example code and it outputs:

```
double free or corruption (out)
Aborted (core dumped)
```

I recompiled the code with the flag -fsanitize=address and re-executed it, it outputs:

```
=================================================================
==31743==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x631000014820 in thread T0
    #0 0x7fe5b26dbdb8 in __interceptor_free (/usr/lib64/libasan.so.4+0xdbdb8)
    #1 0x7fe5b3774616 in Eigen::SparseLU<Eigen::SparseMatrix<double, 0, int>, Eigen::COLAMDOrdering<int> >::factorize(Eigen::SparseMatrix<double, 0, int> const&) (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x55616)
    #2 0x7fe5b3778f05 in SPLINTER::SparseLU<Eigen::Matrix<double, -1, 1, 0, -1, 1> >::doSolve(Eigen::SparseMatrix<double, 0, int> const&, Eigen::Matrix<double, -1, 1, 0, -1, 1> const&, Eigen::Matrix<double, -1, 1, 0, -1, 1>&) const (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x59f05)
    #3 0x7fe5b375fd35 in SPLINTER::BSpline::Builder::computeCoefficients(SPLINTER::BSpline const&) const (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x40d35)
    #4 0x7fe5b3760e8c in SPLINTER::BSpline::Builder::build() const (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x41e8c)
    #5 0x40af8c in main /home/kowa_vi/trajectory_optimization/src/tests/test_splinter.cpp:44
    #6 0x7fe5b21d524c in __libc_start_main (/lib64/libc.so.6+0x3524c)
    #7 0x40a5a9 in _start ../sysdeps/x86_64/start.S:120

0x631000014820 is located 32 bytes inside of 67616-byte region [0x631000014800,0x631000025020)
allocated by thread T0 here:
    #0 0x7fe5b26dc110 in malloc (/usr/lib64/libasan.so.4+0xdc110)
    #1 0x40bcdf in Eigen::internal::handmade_aligned_malloc(unsigned long, unsigned long) /usr/include/eigen3/Eigen/src/Core/util/Memory.h:105
    #2 0x40bdb4 in Eigen::internal::aligned_malloc(unsigned long) /usr/include/eigen3/Eigen/src/Core/util/Memory.h:188
    #3 0x4100eb in void* Eigen::internal::conditional_aligned_malloc<true>(unsigned long) /usr/include/eigen3/Eigen/src/Core/util/Memory.h:241
    #4 0x40f94d in double* Eigen::internal::conditional_aligned_new_auto<double, true>(unsigned long) /usr/include/eigen3/Eigen/src/Core/util/Memory.h:404
    #5 0x7fe5b3773a3d in Eigen::SparseLU<Eigen::SparseMatrix<double, 0, int>, Eigen::COLAMDOrdering<int> >::factorize(Eigen::SparseMatrix<double, 0, int> const&) (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x54a3d)
    #6 0x7fe5b3778f05 in SPLINTER::SparseLU<Eigen::Matrix<double, -1, 1, 0, -1, 1> >::doSolve(Eigen::SparseMatrix<double, 0, int> const&, Eigen::Matrix<double, -1, 1, 0, -1, 1> const&, Eigen::Matrix<double, -1, 1, 0, -1, 1>&) const (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x59f05)
    #7 0x7fe5b375fd35 in SPLINTER::BSpline::Builder::computeCoefficients(SPLINTER::BSpline const&) const (/home/kowa_vi/Downloads/splinter-3.0/build/libsplinter-3-0.so+0x40d35)

SUMMARY: AddressSanitizer: bad-free (/usr/lib64/libasan.so.4+0xdbdb8) in __interceptor_free
==31743==ABORTING
```

The basic C interface example works, but if I create a variable such as an Eigen::Matrix inside the code, the same error occurs. 

I am running it on an openSUSE 5.14.21 system, using gcc as the compiler.

Is there some sort of memory issue?
