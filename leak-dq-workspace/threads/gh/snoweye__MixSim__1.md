# CRAN packages using uninitialised values

- URL: https://github.com/snoweye/MixSim/issues/1
- Repo: snoweye/MixSim (language: C)
- State: open; created 2021-03-08T14:40:55Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · snoweye · 2021-03-08T14:40:55Z · https://github.com/snoweye/MixSim/issues/1

From Prof Brian Ripley on Mar 7, 2021:

All of these are from within the package and using values which were
never initialized or already freed.  Some are showing other issues which
look a consequence of this.

Please correct as soon as possible and before Apr 7 to safely retain the
package on CRAN.


==3787827== Memcheck, a memory error detector
==3787827== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==3787827== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==3787827== Command: /data/blackswan/ripley/R/R-devel-vg/bin/exec/R --vanilla
==3787827== 

R Under development (unstable) (2021-03-03 r80061) -- "Unsuffered Consequences"
Copyright (C) 2021 The R Foundation for Statistical Computing
Platform: x86_64-pc-linux-gnu (64-bit)

> ### ** Examples
> 
> # Simulate parameters of a mixture model
> A <- MixSim(BarOmega = 0.01, MaxOmega = 0.10, K = 10, p = 5)
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x1194DDD2: dlansy_ (svn/R-devel/src/modules/lapack/dlapack.f:61725)
==3787827==    by 0x119951B7: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134295)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x1194DDF8: dlansy_ (svn/R-devel/src/modules/lapack/dlapack.f:61725)
==3787827==    by 0x119951B7: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134295)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x484D23C: dnrm2_ (svn/R-devel/src/extra/blas/blas.f:1263)
==3787827==    by 0x1194F83E: dlarfg_ (svn/R-devel/src/modules/lapack/dlapack.f:72233)
==3787827==    by 0x11950731: dsytd2_ (svn/R-devel/src/modules/lapack/dlapack.f:139307)
==3787827==    by 0x1198D140: dsytrd_ (svn/R-devel/src/modules/lapack/dlapack.f:140323)
==3787827==    by 0x119952A2: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134314)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x484D242: dnrm2_ (svn/R-devel/src/extra/blas/blas.f:1263)
==3787827==    by 0x1194F83E: dlarfg_ (svn/R-devel/src/modules/lapack/dlapack.f:72233)
==3787827==    by 0x11950731: dsytd2_ (svn/R-devel/src/modules/lapack/dlapack.f:139307)
==3787827==    by 0x1198D140: dsytrd_ (svn/R-devel/src/modules/lapack/dlapack.f:140323)
==3787827==    by 0x119952A2: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134314)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x1194F84D: dlarfg_ (svn/R-devel/src/modules/lapack/dlapack.f:72235)
==3787827==    by 0x11950731: dsytd2_ (svn/R-devel/src/modules/lapack/dlapack.f:139307)
==3787827==    by 0x1198D140: dsytrd_ (svn/R-devel/src/modules/lapack/dlapack.f:140323)
==3787827==    by 0x119952A2: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134314)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x1195CA1B: dsteqr_ (svn/R-devel/src/modules/lapack/dlapack.f:130781)
==3787827==    by 0x11995475: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134325)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 
==3787827== Conditional jump or move depends on uninitialised value(s)
==3787827==    at 0x1195CA1D: dsteqr_ (svn/R-devel/src/modules/lapack/dlapack.f:130781)
==3787827==    by 0x11995475: dsyev_ (svn/R-devel/src/modules/lapack/dlapack.f:134325)
==3787827==    by 0x48BCFF9: EigValDec (packages/tests-vg/MixSim/src/libEVD_LAPACK.c:36)
==3787827==    by 0x48C4B67: GetEigOmega (packages/tests-vg/MixSim/src/libOverlap.c:622)
==3787827==    by 0x48C6C23: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1052)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==  Uninitialised value was created by a heap allocation
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48C1257: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:136)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827==    by 0x52125C: Rf_ReplIteration (svn/R-devel/src/main/main.c:264)
==3787827==    by 0x5215A7: R_ReplConsole (svn/R-devel/src/main/main.c:314)
==3787827== 


==3787827== HEAP SUMMARY:
==3787827==     in use at exit: 56,909,143 bytes in 10,638 blocks
==3787827==   total heap usage: 50,320 allocs, 39,682 frees, 140,685,866 bytes allocated
==3787827== 
==3787827== 80 bytes in 2 blocks are definitely lost in loss record 33 of 1,520
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48BD4E6: genSigmaEcc (packages/tests-vg/MixSim/src/libGenPars.c:88)
==3787827==    by 0x48C5CB2: OmegaClust (packages/tests-vg/MixSim/src/libOverlap.c:906)
==3787827==    by 0x48C0B00: runOmegaClust (packages/tests-vg/MixSim/src/libMixSim.c:90)
==3787827==    by 0x49F825: do_dotCode (svn/R-devel/src/main/dotcode.c:1899)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827== 
==3787827== 200 bytes in 5 blocks are definitely lost in loss record 61 of 1,520
==3787827==    at 0x483A809: malloc (/builddir/build/BUILD/valgrind-3.16.1/coregrind/m_replacemalloc/vg_replace_malloc.c:307)
==3787827==    by 0x48BD4E6: genSigmaEcc (packages/tests-vg/MixSim/src/libGenPars.c:88)
==3787827==    by 0x48C6D50: OmegaBarOmegaMax (packages/tests-vg/MixSim/src/libOverlap.c:1079)
==3787827==    by 0x48C133C: runOmegaBarOmegaMax (packages/tests-vg/MixSim/src/libMixSim.c:151)
==3787827==    by 0x49F703: do_dotCode (svn/R-devel/src/main/dotcode.c:1874)
==3787827==    by 0x4D3566: bcEval (svn/R-devel/src/main/eval.c:7115)
==3787827==    by 0x4F0077: Rf_eval (svn/R-devel/src/main/eval.c:727)
==3787827==    by 0x4F1A8D: R_execClosure (svn/R-devel/src/main/eval.c:1897)
==3787827==    by 0x4F2783: Rf_applyClosure (svn/R-devel/src/main/eval.c:1823)
==3787827==    by 0x4F0243: Rf_eval (svn/R-devel/src/main/eval.c:850)
==3787827==    by 0x4F4299: do_set (svn/R-devel/src/main/eval.c:2969)
==3787827==    by 0x4F04C4: Rf_eval (svn/R-devel/src/main/eval.c:802)
==3787827== 
==3787827== LEAK SUMMARY:
==3787827==    definitely lost: 280 bytes in 7 blocks
==3787827==    indirectly lost: 0 bytes in 0 blocks
==3787827==      possibly lost: 0 bytes in 0 blocks
==3787827==    still reachable: 56,908,863 bytes in 10,631 blocks
==3787827==         suppressed: 0 bytes in 0 blocks
==3787827== Reachable blocks (those to which a pointer was found) are not shown.
==3787827== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==3787827== 
==3787827== For lists of detected and suppressed errors, rerun with: -s
==3787827== ERROR SUMMARY: 268 errors from 71 contexts (suppressed: 0 from 0)



## Comment 793195268

reporter (OWNER) · snoweye · 2021-03-09T00:20:39Z · https://github.com/snoweye/MixSim/issues/1#issuecomment-793195268

MAKE_MATRIX may not initial nor allocate consecutive memory at once. [This](consecutive) seems to resolve the issues caught by valgrind. 
