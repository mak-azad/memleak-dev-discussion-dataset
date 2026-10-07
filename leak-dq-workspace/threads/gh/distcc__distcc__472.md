# malloc(): corrupted top size on PowerPC (32-bit) but not x86

- URL: https://github.com/distcc/distcc/issues/472
- Repo: distcc/distcc (language: C)
- State: open; created 2022-09-28T05:50:06Z; status ok; passes offcwe

## Issue body

reporter (NONE) · vbvr · 2022-09-28T05:50:06Z · https://github.com/distcc/distcc/issues/472

The error shows up when I compile this basic source code in plain mode, on my Power Mac G4 computer, but not on my Compaq running a Pentium III.
```c
#include <stdio.h>

int main() {
    printf("Hello distcc!\n");
    return 0;
}
```
These are the errors I get when I compile from the PowerPC. I tried with and without specifying the compiler.
```bash
ppcsys ~ #  uname -primo
5.15.41-gentoo ppc 7400, altivec supported PowerMac3,1 GNU/Linux

ppcsys ~ #  distcc --version
distcc 3.4 powerpc-unknown-linux-gnu
  (protocols 1, 2 and 3) (default port 3632)
  built Sep 22 2022 23:35:04
Copyright (C) 2002, 2003, 2004 by Martin Pool.
Includes miniLZO (C) 1996-2002 by Markus Franz Xaver Johannes Oberhumer.
Portions Copyright (C) 2007-2008 Google.

distcc comes with ABSOLUTELY NO WARRANTY.  distcc is free software, and
you may use, modify and redistribute it under the terms of the GNU
General Public License version 2 or later.

Please report bugs to distcc@lists.samba.org

ppcsys ~ #  DISTCC_VERBOSE=1 distcc gcc -c test.c -o test.o
distcc[28610] (dcc_trace_version) distcc 3.4 powerpc-unknown-linux-gnu; built Sep 22 2022 23:35:04
distcc[28610] (dcc_recursion_safeguard) safeguard level=0
distcc[28610] (main) compiler name is "distcc"
distcc[28610] (dcc_scan_args) scanning arguments: gcc -c test.c -o test.o
distcc[28610] (dcc_scan_args) found input file "test.c"
distcc[28610] (dcc_scan_args) found object/output file "test.o"
distcc[28610] compile from test.c to test.o
distcc[28610] (dcc_gcc_rewrite_fqn) Re-writing call to 'gcc' to 'powerpc-unknown-linux-gnu-gcc' to support cross-compilation.
malloc(): corrupted top size
Aborted

ppcsys ~ #  DISTCC_VERBOSE=1 distcc -c test.c -o test.o
distcc[28611] (dcc_trace_version) distcc 3.4 powerpc-unknown-linux-gnu; built Sep 22 2022 23:35:04
distcc[28611] (dcc_recursion_safeguard) safeguard level=0
distcc[28611] (main) compiler name is "distcc"
distcc[28611] (dcc_scan_args) scanning arguments: cc -c test.c -o test.o
distcc[28611] (dcc_scan_args) found input file "test.c"
distcc[28611] (dcc_scan_args) found object/output file "test.o"
distcc[28611] compile from test.c to test.o
distcc[28611] (dcc_rewrite_generic_compiler) Rewriting 'cc' to 'gcc'
distcc[28611] (dcc_gcc_rewrite_fqn) Re-writing call to 'gcc' to 'powerpc-unknown-linux-gnu-gcc' to support cross-compilation.
malloc(): corrupted top size
Aborted
```
And this is on x86 (no output to indicate no errors)
```bash
x86sys ~ #  uname -primo
5.15.41-gentoo i686 Pentium III (Coppermine) GenuineIntel GNU/Linux

x86sys ~#  distcc --version
distcc 3.4 i686-pc-linux-gnu
  (protocols 1, 2 and 3) (default port 3632)
  built Aug 15 2022 12:59:25
Copyright (C) 2002, 2003, 2004 by Martin Pool.
Includes miniLZO (C) 1996-2002 by Markus Franz Xaver Johannes Oberhumer.
Portions Copyright (C) 2007-2008 Google.

distcc comes with ABSOLUTELY NO WARRANTY.  distcc is free software, and
you may use, modify and redistribute it under the terms of the GNU
General Public License version 2 or later.

Please report bugs to distcc@lists.samba.org

x86sys ~ #  distcc gcc -m32 -c test.c -o test.o
x86sys ~ #

x86sys ~ #  distcc -m32 -c test.c -o test.o
x86sys ~ #

x86sys ~ #  distcc gcc -c test.c -o test.o
x86sys ~ #

x86sys ~ #  distcc -c test.c -o test.o
x86sys ~ #
```
 
I rolled back my PowerPC's installation to 3.3.3. I get the error on this version as well, but _only_ if I do not specify a compiler.

```bash
ppcsys ~ #  distcc --version
distcc 3.3.3 powerpc-unknown-linux-gnu
  (protocols 1, 2 and 3) (default port 3632)
  built Sep 23 2022 00:55:34
Copyright (C) 2002, 2003, 2004 by Martin Pool.
Includes miniLZO (C) 1996-2002 by Markus Franz Xaver Johannes Oberhumer.
Portions Copyright (C) 2007-2008 Google.

distcc comes with ABSOLUTELY NO WARRANTY.  distcc is free software, and
you may use, modify and redistribute it under the terms of the GNU
General Public License version 2 or later.

Please report bugs to distcc@lists.samba.org

ppcsys ~ #  distcc -c test.c -o test.o
malloc(): corrupted top size
Aborted

ppcsys ~ #  DISTCC_VERBOSE=1 distcc -c test.c -o test.o
distcc[24621] (dcc_trace_version) distcc 3.3.3 powerpc-unknown-linux-gnu; built Sep 23 2022 00:55:34
distcc[24621] (dcc_recursion_safeguard) safeguard level=0
distcc[24621] (main) compiler name is "distcc"
distcc[24621] (dcc_scan_args) scanning arguments: cc -c test.c -o test.o
distcc[24621] (dcc_scan_args) found input file "test.c"
distcc[24621] (dcc_scan_args) found object/output file "test.o"
distcc[24621] compile from test.c to test.o
distcc[24621] (dcc_rewrite_generic_compiler) Rewriting 'cc' to 'gcc'
distcc[24621] (dcc_gcc_rewrite_fqn) Re-writing call to 'gcc' to 'powerpc-unknown-linux-gnu-gcc' to support cross-compilation.
malloc(): corrupted top size
Aborted

ppcsys ~ #  distcc gcc -c test.c -o test.o
ppcsys ~ #
```

