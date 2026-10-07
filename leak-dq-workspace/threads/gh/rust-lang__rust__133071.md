# Mismatched new/delete alignment alloc value: 8 dealloc value: default-aligned

- URL: https://github.com/rust-lang/rust/issues/133071
- Repo: rust-lang/rust (language: Rust)
- State: open; created 2024-11-15T12:16:38Z; status ok; passes main

## Issue body

reporter (MEMBER) · GuillaumeGomez · 2024-11-15T12:16:38Z · https://github.com/rust-lang/rust/issues/133071

When compiling https://github.com/GuillaumeGomez/mdBook/tree/bug-rustc, I got a segfault. When running under valgrind I get:

```
==563011== Thread 3 rustc:
==563011== Mismatched new/delete alignment alloc value: 8 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x1155C5F6: llvm::PassRegistry::registerPass(llvm::PassInfo const&, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x119FB7D2: initializeReachingDefAnalysisPassOnce(llvm::PassRegistry&) [clone .llvm.14788713002572353718] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11A8CBA8: initializeX86ExecutionDomainFixPassOnce(llvm::PassRegistry&) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11B38BC6: LLVMInitializeX86Target (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xA04714E: rustc_llvm::initialize_available_targets (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0xA046A74: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::init (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BB45: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==  Address 0x12eabac0 is 0 bytes inside a block of size 1,024 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x1155F814: llvm::DenseMap<void const*, llvm::PassInfo const*, llvm::DenseMapInfo<void const*, void>, llvm::detail::DenseMapPair<void const*, llvm::PassInfo const*> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x1155C5F6: llvm::PassRegistry::registerPass(llvm::PassInfo const&, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11A28606: _GLOBAL__sub_I_Debugify.cpp (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x4004556: call_init (dl-init.c:74)
==563011==    by 0x4004556: call_init (dl-init.c:26)
==563011==    by 0x400464C: _dl_init (dl-init.c:121)
==563011==    by 0x401CEDF: ??? (in /usr/lib64/ld-linux-x86-64.so.2)
==563011==    by 0x59: ???
==563011==    by 0x1FFEFFF262: ???
==563011==    by 0x1FFEFFF2AD: ???
==563011==    by 0x1FFEFFF2BA: ???
==563011==    by 0x1FFEFFF2C1: ???
==563011== 
==563011== Mismatched new/delete alignment alloc value: 8 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x1155C5F6: llvm::PassRegistry::registerPass(llvm::PassInfo const&, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x119FA87B: initializeAArch64BranchTargetsPassOnce(llvm::PassRegistry&) [clone .llvm.4105488490841716021] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11B36414: LLVMInitializeAArch64Target (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xA04718A: rustc_llvm::initialize_available_targets (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0xA046A74: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::init (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BB45: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==  Address 0x13105a70 is 0 bytes inside a block of size 2,048 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x1155F814: llvm::DenseMap<void const*, llvm::PassInfo const*, llvm::DenseMapInfo<void const*, void>, llvm::detail::DenseMapPair<void const*, llvm::PassInfo const*> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x1155C5F6: llvm::PassRegistry::registerPass(llvm::PassInfo const&, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x119FB7D2: initializeReachingDefAnalysisPassOnce(llvm::PassRegistry&) [clone .llvm.14788713002572353718] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11A8CBA8: initializeX86ExecutionDomainFixPassOnce(llvm::PassRegistry&) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11B38BC6: LLVMInitializeX86Target (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xA04714E: rustc_llvm::initialize_available_targets (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0xA046A74: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::init (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched new/delete alignment alloc value: 8 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x1155C5F6: llvm::PassRegistry::registerPass(llvm::PassInfo const&, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11A903A4: initializeRISCVCodeGenPreparePassOnce(llvm::PassRegistry&) [clone .llvm.3021935745327874363] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11B382DE: LLVMInitializeRISCVTarget (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xA047298: rustc_llvm::initialize_available_targets (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0xA046A74: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::init (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BB45: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==  Address 0x13109c30 is 0 bytes inside a block of size 4,096 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x1155F814: llvm::DenseMap<void const*, llvm::PassInfo const*, llvm::DenseMapInfo<void const*, void>, llvm::detail::DenseMapPair<void const*, llvm::PassInfo const*> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x1155C5F6: llvm::PassRegistry::registerPass(llvm::PassInfo const&, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x119FA87B: initializeAArch64BranchTargetsPassOnce(llvm::PassRegistry&) [clone .llvm.4105488490841716021] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xB3F7B0A: __pthread_once_slow.isra.0 (in /usr/lib64/libc.so.6)
==563011==    by 0xB3F7B78: pthread_once@@GLIBC_2.34 (in /usr/lib64/libc.so.6)
==563011==    by 0x11B36414: LLVMInitializeAArch64Target (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0xA04718A: rustc_llvm::initialize_available_targets (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0xA046A74: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::init (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BB45: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched free() / delete / delete []
==563011==    at 0x4844B83: free (vg_replace_malloc.c:989)
==563011==    by 0x9F7CFB5: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==    by 0xB3F2796: start_thread (in /usr/lib64/libc.so.6)
==563011==  Address 0x1313b060 is 0 bytes inside a block of size 31 alloc'd
==563011==    at 0x4841FEC: operator new(unsigned long) (vg_replace_malloc.c:487)
==563011==    by 0x114338E4: std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::reserve(unsigned long) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x1143382C: std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > llvm::detail::join_impl<llvm::StringRef*>(llvm::StringRef*, llvm::StringRef*, llvm::StringRef, std::forward_iterator_tag) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x1143372E: llvm::Triple::normalize[abi:cxx11](llvm::StringRef) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7CF7A: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched new/delete alignment alloc value: 4 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x11986EF1: llvm::X86_MC::initLLVMToSEHAndCVRegMapping(llvm::MCRegisterInfo*) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EB5: createX86MCRegisterInfo(llvm::Triple const&) [clone .llvm.4329284753645362384] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432658: llvm::LLVMTargetMachine::initAsmInfo() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11987DD3: llvm::RegisterTargetMachine<llvm::X86TargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOptLevel, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D5CD: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==  Address 0x1313e2b0 is 0 bytes inside a block of size 512 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x11987193: llvm::DenseMap<llvm::MCRegister, int, llvm::DenseMapInfo<llvm::MCRegister, void>, llvm::detail::DenseMapPair<llvm::MCRegister, int> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EF1: llvm::X86_MC::initLLVMToSEHAndCVRegMapping(llvm::MCRegisterInfo*) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EB5: createX86MCRegisterInfo(llvm::Triple const&) [clone .llvm.4329284753645362384] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432658: llvm::LLVMTargetMachine::initAsmInfo() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11987DD3: llvm::RegisterTargetMachine<llvm::X86TargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOptLevel, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D5CD: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched new/delete alignment alloc value: 4 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x11986FEE: llvm::X86_MC::initLLVMToSEHAndCVRegMapping(llvm::MCRegisterInfo*) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EB5: createX86MCRegisterInfo(llvm::Triple const&) [clone .llvm.4329284753645362384] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432658: llvm::LLVMTargetMachine::initAsmInfo() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11987DD3: llvm::RegisterTargetMachine<llvm::X86TargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOptLevel, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D5CD: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==  Address 0x131421f0 is 0 bytes inside a block of size 512 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x11987193: llvm::DenseMap<llvm::MCRegister, int, llvm::DenseMapInfo<llvm::MCRegister, void>, llvm::detail::DenseMapPair<llvm::MCRegister, int> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986FEE: llvm::X86_MC::initLLVMToSEHAndCVRegMapping(llvm::MCRegisterInfo*) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EB5: createX86MCRegisterInfo(llvm::Triple const&) [clone .llvm.4329284753645362384] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432658: llvm::LLVMTargetMachine::initAsmInfo() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11987DD3: llvm::RegisterTargetMachine<llvm::X86TargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOptLevel, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D5CD: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched free() / delete / delete []
==563011==    at 0x4844B83: free (vg_replace_malloc.c:989)
==563011==    by 0x9F7D5E8: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==    by 0xB3F2796: start_thread (in /usr/lib64/libc.so.6)
==563011==  Address 0x1313d350 is 0 bytes inside a block of size 25 alloc'd
==563011==    at 0x4841FEC: operator new(unsigned long) (vg_replace_malloc.c:487)
==563011==    by 0x112A999D: llvm::Twine::str[abi:cxx11]() const (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432C63: llvm::Triple::Triple(llvm::Twine const&) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D595: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched free() / delete / delete []
==563011==    at 0x4844B83: free (vg_replace_malloc.c:989)
==563011==    by 0x9F7D614: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==    by 0xB3F2796: start_thread (in /usr/lib64/libc.so.6)
==563011==  Address 0x1313b0c0 is 0 bytes inside a block of size 25 alloc'd
==563011==    at 0x4841FEC: operator new(unsigned long) (vg_replace_malloc.c:487)
==563011==    by 0x112A9A39: llvm::Twine::str[abi:cxx11]() const (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432C63: llvm::Triple::Triple(llvm::Twine const&) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7CFA1: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched new/delete alignment alloc value: 4 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x11980C89: llvm::TargetMachine::~TargetMachine() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11980DC8: llvm::X86TargetMachine::~X86TargetMachine() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D854: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==    by 0xB3F2796: start_thread (in /usr/lib64/libc.so.6)
==563011==    by 0xB476593: clone (in /usr/lib64/libc.so.6)
==563011==  Address 0x131430b0 is 0 bytes inside a block of size 4,096 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x11987193: llvm::DenseMap<llvm::MCRegister, int, llvm::DenseMapInfo<llvm::MCRegister, void>, llvm::detail::DenseMapPair<llvm::MCRegister, int> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986FEE: llvm::X86_MC::initLLVMToSEHAndCVRegMapping(llvm::MCRegisterInfo*) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EB5: createX86MCRegisterInfo(llvm::Triple const&) [clone .llvm.4329284753645362384] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432658: llvm::LLVMTargetMachine::initAsmInfo() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11987DD3: llvm::RegisterTargetMachine<llvm::X86TargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOptLevel, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D5CD: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== Mismatched new/delete alignment alloc value: 4 dealloc value: default-aligned
==563011==    at 0x484565F: operator delete(void*) (vg_replace_malloc.c:1131)
==563011==    by 0x11980C9A: llvm::TargetMachine::~TargetMachine() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11980DC8: llvm::X86TargetMachine::~X86TargetMachine() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D854: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F2BBC4: rustc_interface::interface::run_compiler::<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E7395A: std::sys::backtrace::__rust_begin_short_backtrace::<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>> (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9E73729: <<std::thread::Builder>::spawn_unchecked_<rustc_interface::util::run_in_thread_with_globals<rustc_interface::interface::run_compiler<core::result::Result<(), rustc_span::ErrorGuaranteed>, rustc_driver_impl::run_compiler::{closure#0}>::{closure#1}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#0}::{closure#0}, core::result::Result<(), rustc_span::ErrorGuaranteed>>::{closure#1} as core::ops::function::FnOnce<()>>::call_once::{shim:vtable#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x49235FA: call_once<(), dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: call_once<(), alloc::boxed::Box<dyn core::ops::function::FnOnce<(), Output=()>, alloc::alloc::Global>, alloc::alloc::Global> (boxed.rs:2070)
==563011==    by 0x49235FA: std::sys::pal::unix::thread::Thread::new::thread_start (thread.rs:108)
==563011==    by 0xB3F2796: start_thread (in /usr/lib64/libc.so.6)
==563011==    by 0xB476593: clone (in /usr/lib64/libc.so.6)
==563011==  Address 0x131401b0 is 0 bytes inside a block of size 8,192 alloc'd
==563011==    at 0x4842722: operator new(unsigned long, std::align_val_t) (vg_replace_malloc.c:547)
==563011==    by 0x11987193: llvm::DenseMap<llvm::MCRegister, int, llvm::DenseMapInfo<llvm::MCRegister, void>, llvm::detail::DenseMapPair<llvm::MCRegister, int> >::grow(unsigned int) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EF1: llvm::X86_MC::initLLVMToSEHAndCVRegMapping(llvm::MCRegisterInfo*) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11986EB5: createX86MCRegisterInfo(llvm::Triple const&) [clone .llvm.4329284753645362384] (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11432658: llvm::LLVMTargetMachine::initAsmInfo() (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x11987DD3: llvm::RegisterTargetMachine<llvm::X86TargetMachine>::Allocator(llvm::Target const&, llvm::Triple const&, llvm::StringRef, llvm::StringRef, llvm::TargetOptions const&, std::optional<llvm::Reloc::Model>, std::optional<llvm::CodeModel::Model>, llvm::CodeGenOptLevel, bool) (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/libLLVM.so.18.1-rust-1.81.0-stable)
==563011==    by 0x9F7D5CD: LLVMRustCreateTargetMachine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7CBD6: rustc_codegen_llvm::back::write::target_machine_factory::{closure#0} (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7B578: rustc_codegen_llvm::back::write::create_informational_target_machine (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D764: rustc_codegen_llvm::llvm_util::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F7D71E: <rustc_codegen_llvm::LlvmCodegenBackend as rustc_codegen_ssa::traits::backend::CodegenBackend>::target_features (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011==    by 0x9F52D6F: rustc_interface::util::add_configuration (in /home/imperio/.rustup/toolchains/stable-x86_64-unknown-linux-gnu/lib/librustc_driver-3f4ebb066deec3c0.so)
==563011== 
==563011== 
==563011== Process terminating with default action of signal 11 (SIGSEGV): dumping core
==563011==  Bad permissions for mapped region at address 0x4990F68
==563011==    at 0x4007DE8: _dl_map_object (dl-load.c:1903)
==563011== 
==563011== HEAP SUMMARY:
==563011==     in use at exit: 23,891,557 bytes in 104,588 blocks
==563011==   total heap usage: 486,459 allocs, 381,871 frees, 72,591,238 bytes allocated
==563011== 
==563011== LEAK SUMMARY:
==563011==    definitely lost: 67,584 bytes in 1 blocks
==563011==    indirectly lost: 0 bytes in 0 blocks
==563011==      possibly lost: 2,673,093 bytes in 4,808 blocks
==563011==    still reachable: 21,150,384 bytes in 99,777 blocks
==563011==         suppressed: 496 bytes in 2 blocks
==563011== Rerun with --leak-check=full to see details of leaked memory
==563011== 
==563011== For lists of detected and suppressed errors, rerun with: -s
==563011== ERROR SUMMARY: 27 errors from 10 contexts (suppressed: 0 from 0)
Segmentation fault (core dumped)
```

I tried with `rustc 1.81.0 (eeb90cda1 2024-09-04)` and with `rustc 1.83.0-nightly (3ae715c8c 2024-10-07)`. The bug occurs in both cases.

## Comment 2478730288

maintainer (MEMBER) · matthiaskrgr · 2024-11-15T12:42:22Z · https://github.com/rust-lang/rust/issues/133071#issuecomment-2478730288


hm, build failure with  nightly-2023-09-01
stack overflow since nightly-2023-10-01

might be a case that never compiled successfully actually 

## Comment 2478823285

reporter (MEMBER) · GuillaumeGomez · 2024-11-15T13:32:26Z · https://github.com/rust-lang/rust/issues/133071#issuecomment-2478823285

There is indeed a wrong recursion in the template. However I expect the compiler to tell me what I did wrong, not to segfault. ;)
