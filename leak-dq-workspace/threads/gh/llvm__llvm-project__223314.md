# [libcxx][test] qemu: uncaught target signal 4 (Illegal instruction) - core dumped

- URL: https://github.com/llvm/llvm-project/issues/223314
- Repo: llvm/llvm-project (language: LLVM)
- State: open; created 2026-09-14T06:58:05Z; status ok; passes main

## Issue body

reporter (NONE) · peppergrayxyz · 2026-09-14T06:58:05Z · https://github.com/llvm/llvm-project/issues/223314

Running `libcxx` on qemu-ppc with altivec extensions enabled fails with errors: 


```
********************
FAIL: llvm-libc++-shared.cfg.in :: std/containers/container.adaptors/flat.map/flat.map.modifiers/replace.pass.cpp (3766 of 11321)
******************** TEST 'llvm-libc++-shared.cfg.in :: std/containers/container.adaptors/flat.map/flat.map.modifiers/replace.pass.cpp' FAILED ********************
Exit Code: 252

Command Output (stdout):
--
# COMPILED WITH
/usr/lib/llvm/22/bin/powerpc-unknown-linux-musl-clang++-22 /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/replace.pass.cpp -pthread --target=powerpc-unknown-linux-musl -nostdinc++ -I /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/include/c++/v1 -I /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/include/c++/v1 -I /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/libcxx/test/support -std=c++26 -Werror -Wall -Wctad-maybe-unsupported -Wextra -Wshadow -Wundef -Wunused-template -Wno-unused-command-line-argument -Wno-attributes -Wno-pessimizing-move -Wno-noexcept-type -Wno-atomic-alignment -Wno-reserved-module-identifier -Wdeprecated-copy -Wdeprecated-copy-dtor -Wshift-negative-value -Wno-user-defined-literals -Wno-tautological-compare -Wsign-compare -Wunused-variable -Wunused-parameter -Wunreachable-code -Wno-unused-local-typedef -Wno-local-type-template-args -Wno-c++11-extensions -Wno-unknown-pragmas -Wno-pass-failed -Wno-mismatched-new-delete -Wno-redundant-move -Wno-self-move -Wno-nullability-completeness -flax-vector-conversions=none -D_LIBCPP_HAS_NO_PRAGMA_SYSTEM_HEADER -D_LIBCPP_ENABLE_EXPERIMENTAL -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE -Wuser-defined-warnings  -lc++experimental -nostdlib++ -L /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/lib -Wl,-rpath,/var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/lib -lc++ -o /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/Output/replace.pass.cpp.dir/t.tmp.exe
# executed command: /usr/lib/llvm/22/bin/powerpc-unknown-linux-musl-clang++-22 /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/replace.pass.cpp -pthread --target=powerpc-unknown-linux-musl -nostdinc++ -I /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/include/c++/v1 -I /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/include/c++/v1 -I /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/libcxx/test/support -std=c++26 -Werror -Wall -Wctad-maybe-unsupported -Wextra -Wshadow -Wundef -Wunused-template -Wno-unused-command-line-argument -Wno-attributes -Wno-pessimizing-move -Wno-noexcept-type -Wno-atomic-alignment -Wno-reserved-module-identifier -Wdeprecated-copy -Wdeprecated-copy-dtor -Wshift-negative-value -Wno-user-defined-literals -Wno-tautological-compare -Wsign-compare -Wunused-variable -Wunused-parameter -Wunreachable-code -Wno-unused-local-typedef -Wno-local-type-template-args -Wno-c++11-extensions -Wno-unknown-pragmas -Wno-pass-failed -Wno-mismatched-new-delete -Wno-redundant-move -Wno-self-move -Wno-nullability-completeness -flax-vector-conversions=none -D_LIBCPP_HAS_NO_PRAGMA_SYSTEM_HEADER -D_LIBCPP_ENABLE_EXPERIMENTAL -D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_NONE -Wuser-defined-warnings -lc++experimental -nostdlib++ -L /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/lib -Wl,-rpath,/var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test-suite-install/lib -lc++ -o /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/Output/replace.pass.cpp.dir/t.tmp.exe
# EXECUTED AS
/usr/bin/python3.14 /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/libcxx/utils/run.py --execdir /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/Output/replace.pass.cpp.dir --  /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/Output/replace.pass.cpp.dir/t.tmp.exe
# executed command: /usr/bin/python3.14 /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/libcxx/utils/run.py --execdir /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/Output/replace.pass.cpp.dir -- /var/tmp/portage/llvm-runtimes/libcxx-22.1.8/work/runtimes_build-.ppc/libcxx/test/std/containers/container.adaptors/flat.map/flat.map.modifiers/Output/replace.pass.cpp.dir/t.tmp.exe
# .---command stderr------------
# | qemu: uncaught target signal 4 (Illegal instruction) - core dumped
# `-----------------------------
# error: command failed with exit status: 252

--
```

The issue is caused by `libcxx/utils/run.py` which drops all env vars: 

- `qemu-static` is controlled through `QEMU_*` vars including `QEMU_CPU`.
- `QEMU_CPU` needs to be set to a compatible CPU to support altivec extensions, e.g. `QEMU_CPU=7450`
- When `qemu-static` is called without that information, it uses the default CPU for the target architecture, i.e. with CPU extensions disabled.
- This issue is not ppc specific, but affects all use cases, where CPU extensions are used that are not supported by the baseline.

The script should forward  `QEMU_*` vars to ensure that the env is setup properly to run the test in an emulated environment.


