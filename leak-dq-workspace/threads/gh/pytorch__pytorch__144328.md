# Debug build fails to compile on x86 with WERROR=1

- URL: https://github.com/pytorch/pytorch/issues/144328
- Repo: pytorch/pytorch (language: Python)
- State: open; created 2025-01-07T15:06:48Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · robert-hardwick · 2025-01-07T15:06:48Z · https://github.com/pytorch/pytorch/issues/144328

### 🐛 Describe the bug

Attempted to build a debug whl on x86 machine in ubuntu docker image 'pytorch-linux-jammy-py3.9-gcc11'

Build passes when DEBUG=0 OR with DEBUG=1 and WERROR=0

`In file included from /var/lib/jenkins/workspace/torch/csrc/jit/tensorexpr/llvm_codegen.cpp:24:
/opt/llvm/include/llvm/IR/IRBuilder.h: In member function ‘llvm::LoadInst* llvm::IRBuilder<T, Inserter>::CreateLoad(llvm::Type*, llvm::Value*, const llvm::Twine&) [with T = llvm::ConstantFolder; Inserter = llvm::IRBuilderDefaultInserter]’:
/opt/llvm/include/llvm/IR/IRBuilder.h:1581:19: error: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
 1581 |     return Insert(new LoadInst(Ty, Ptr), Name);
      |                   ^~~~~~~~~~~~~~~~~~~~~
/opt/llvm/include/llvm/IR/IRBuilder.h:1581:19: note: returned from ‘static void* llvm::UnaryInstruction::operator new(size_t)’
/opt/llvm/include/llvm/IR/IRBuilder.h: In member function ‘llvm::Value* llvm::IRBuilder<T, Inserter>::CreateFCmp(llvm::CmpInst::Predicate, llvm::Value*, llvm::Value*, const llvm::Twine&, llvm::MDNode*) [with T = llvm::ConstantFolder; Inserter = llvm::IRBuilderDefaultInserter]’:
/opt/llvm/include/llvm/IR/IRBuilder.h:2181:30: error: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
 2181 |     return Insert(setFPAttrs(new FCmpInst(P, LHS, RHS), FPMathTag, FMF), Name);
      |                              ^~~~~~~~~~~~~~~~~~~~~~~~~
/opt/llvm/include/llvm/IR/IRBuilder.h:2181:30: note: returned from ‘static void* llvm::CmpInst::operator new(size_t)’
/opt/llvm/include/llvm/IR/IRBuilder.h: In member function ‘llvm::Value* llvm::IRBuilder<T, Inserter>::CreateICmp(llvm::CmpInst::Predicate, llvm::Value*, llvm::Value*, const llvm::Twine&) [with T = llvm::ConstantFolder; Inserter = llvm::IRBuilderDefaultInserter]’:
/opt/llvm/include/llvm/IR/IRBuilder.h:2173:19: error: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
 2173 |     return Insert(new ICmpInst(P, LHS, RHS), Name);
      |                   ^~~~~~~~~~~~~~~~~~~~~~~~~
/opt/llvm/include/llvm/IR/IRBuilder.h:2173:19: note: returned from ‘static void* llvm::CmpInst::operator new(size_t)’
/opt/llvm/include/llvm/IR/IRBuilder.h: In member function ‘llvm::AllocaInst* llvm::IRBuilder<T, Inserter>::CreateAlloca(llvm::Type*, llvm::Value*, const llvm::Twine&) [with T = llvm::ConstantFolder; Inserter = llvm::IRBuilderDefaultInserter]’:
/opt/llvm/include/llvm/IR/IRBuilder.h:1571:19: error: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
 1571 |     return Insert(new AllocaInst(Ty, DL.getAllocaAddrSpace(), ArraySize), Name);
      |                   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/llvm/include/llvm/IR/IRBuilder.h:1571:19: note: returned from ‘static void* llvm::UnaryInstruction::operator new(size_t)’
/opt/llvm/include/llvm/IR/IRBuilder.h: In member function ‘llvm::StoreInst* llvm::IRBuilder<T, Inserter>::CreateStore(llvm::Value*, llvm::Value*, bool) [with T = llvm::ConstantFolder; Inserter = llvm::IRBuilderDefaultInserter]’:
/opt/llvm/include/llvm/IR/IRBuilder.h:1606:19: error: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
 1606 |     return Insert(new StoreInst(Val, Ptr, isVolatile));
      |                   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/llvm/include/llvm/IR/IRBuilder.h:1606:19: note: returned from ‘static void* llvm::StoreInst::operator new(size_t)’
/opt/llvm/include/llvm/IR/IRBuilder.h: In member function ‘llvm::Value* llvm::IRBuilder<T, Inserter>::CreateShuffleVector(llvm::Value*, llvm::Value*, llvm::Value*, const llvm::Twine&) [with T = llvm::ConstantFolder; Inserter = llvm::IRBuilderDefaultInserter]’:
/opt/llvm/include/llvm/IR/IRBuilder.h:2296:19: error: ‘static void llvm::User::operator delete(void*)’ called on pointer returned from a mismatched allocation function [-Werror=mismatched-new-delete]
 2296 |     return Insert(new ShuffleVectorInst(V1, V2, Mask), Name);
      |                   ^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/opt/llvm/include/llvm/IR/IRBuilder.h:2296:19: note: returned from ‘static void* llvm::ShuffleVectorInst::operator new(size_t)’`

### Versions

PyTorch Version = 8d35333498e9433a379611746c177285fa51c8c5

$ lscpu
Architecture:             x86_64
  CPU op-mode(s):         32-bit, 64-bit
  Address sizes:          46 bits physical, 48 bits virtual
  Byte Order:             Little Endian
CPU(s):                   16
  On-line CPU(s) list:    0-15
Vendor ID:                GenuineIntel
  Model name:             Intel(R) Xeon(R) Platinum 8488C
    CPU family:           6
    Model:                143
    Thread(s) per core:   2
    Core(s) per socket:   8
    Socket(s):            1
    Stepping:             8
    BogoMIPS:             4800.00
    Flags:                fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon rep_good nopl xtopology nonstop_tsc cpuid aperfmp
                          erf tsc_known_freq pni pclmulqdq monitor ssse3 fma cx16 pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch ssbd ibrs ibpb stibp ibrs_
                          enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid avx512f avx512dq rdseed adx smap avx512ifma clflushopt clwb avx512cd sha_ni avx512bw avx512vl xsaveopt xsavec xgetbv1 xsaves avx_vnni avx512_bf16
                          wbnoinvd ida arat avx512vbmi umip pku ospke waitpkg avx512_vbmi2 gfni vaes vpclmulqdq avx512_vnni avx512_bitalg tme avx512_vpopcntdq rdpid cldemote movdiri movdir64b md_clear serialize amx_bf16 avx512_fp16 am
                          x_tile amx_int8 flush_l1d arch_capabilities

cc @malfet @seemethere

## Comment 2575573308

maintainer (COLLABORATOR) · malfet · 2025-01-07T15:26:30Z · https://github.com/pytorch/pytorch/issues/144328#issuecomment-2575573308

I suspect this is because you have llvm-dev and it tries to compile TensorExpr. Please disable it and try again. And if you have a PR that fixes the violation, please do not hesitate to submit one
