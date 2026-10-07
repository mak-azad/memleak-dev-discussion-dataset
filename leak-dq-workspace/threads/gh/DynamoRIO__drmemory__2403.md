# Possible false positives

- URL: https://github.com/DynamoRIO/drmemory/issues/2403
- Repo: DynamoRIO/drmemory (language: C)
- State: open; created 2021-04-17T15:50:27Z; status ok; passes main

## Issue body

reporter (NONE) · giladfrid009 · 2021-04-17T15:50:27Z · https://github.com/DynamoRIO/drmemory/issues/2403

**Describe the bug**
I'm getting possibly false positives for memory leaks (or real leaks, not from my executable).
I've analyzed my exe with valgrind and it did't find any leaks, but with dr. memory i'm leak reports.

**To Reproduce**
Steps to reproduce the behavior:
Precise command line for running the application: `drmemory mtm_buggy.exe`

- The problem goes away when running in light mode (pass `-light` to Dr. Memory)
 - The problem goes away when running with the option `-leaks_only`
 - ERROR #2 goes away when running with the option `-no_count_leaks`
 - **The analysis crashes** when running with the option `-no_track_allocs`
 - Passing `-debug -dr_debug -pause_at_assert`, does not change the outcome (leaks persist)

**Expected behavior**
No memory leaks found.

**Screenshots or Pasted Text**

***Source code:***

```c
int main()
{
	return 0;
}
```

***Build:***
```json
{
	"version": "2.0.0",
	"tasks": [
		{
			"type": "cppbuild",
			"label": "C/C++: gcc.exe build active file",
			"command": "D:\\Program Files\\mingw-w64\\x86_64-8.1.0-posix-seh-rt_v6-rev0\\mingw64\\bin\\gcc.exe",
			"args": [
				"-g",
				"-std=c99",
				"-Wall",
				"-pedantic-errors",
				"-Werror",
				"-ggdb",
				"${file}",
				"-o",
				"${fileDirname}\\${fileBasenameNoExtension}.exe"
			],
			"options": {
				"cwd": "${workspaceFolder}"
			},
			"problemMatcher": [
				"$gcc"
			],
			"group": {
				"kind": "build",
				"isDefault": true
			},
			"detail": "compiler: \"D:\\Program Files\\mingw-w64\\x86_64-8.1.0-posix-seh-rt_v6-rev0\\mingw64\\bin\\gcc.exe\""
		}
	]
}
```

***Dr. Memory output:***
```
Dr. Memory version 2.3.18722 build 0 built on Apr 10 2021 02:45:45
Windows version: WinVer=105;Rel=2009;Build=19042;Edition=Professional
Dr. Memory results for pid 10632: "mtm_buggy.exe"
Application cmdline: "mtm_buggy.exe"
Recorded 124 suppression(s) from default D:\Program Files (x86)\Dr. Memory\bin64\suppress-default.txt

Error #1: UNADDRESSABLE ACCESS beyond top of stack: reading 0x000000000061fb40-0x000000000061fb48 8 byte(s)
# 0 ___chkstk_ms                            [../../../../../src/gcc-8.1.0/libgcc/config/i386/cygwin.S:132]
# 1 _pei386_runtime_relocator               [D:/Users/Gilad Freidkin/Source/university/hw0/mtm_buggy.c:160]
# 2 __tmainCRTStartup
# 3 .l_start     
# 4 KERNEL32.dll!BaseThreadInitThunk       +0x13     (0x00007ffae16b7034 <KERNEL32.dll+0x17034>)
Note: @0:00:00.474 in thread 532
Note: 0x000000000061fb40 refers to 600 byte(s) beyond the top of the stack 0x000000000061fd98
Note: instruction: or     $0x0000000000000000 (%rcx) -> (%rcx)

Error #2: POSSIBLE LEAK 31 direct bytes 0x00000000016701c0-0x00000000016701df + 0 indirect bytes
# 0 replace_malloc                    [d:\a\drmemory\drmemory\common\alloc_replace.c:2580]
# 1 msvcrt.dll!malloc_crt
# 2 msvcrt.dll!_setargv  
# 3 msvcrt.dll!_getmainargs
# 4 pre_cpp_init 
# 5 msvcrt.dll!initterm  
# 6 __tmainCRTStartup
# 7 .l_start     
# 8 KERNEL32.dll!BaseThreadInitThunk +0x13     (0x00007ffae16b7034 <KERNEL32.dll+0x17034>)

===========================================================================
FINAL SUMMARY:

DUPLICATE ERROR COUNTS:
	Error #   1:      2

SUPPRESSIONS USED:

ERRORS FOUND:
      1 unique,     2 total unaddressable access(es)
      0 unique,     0 total uninitialized access(es)
      0 unique,     0 total invalid heap argument(s)
      0 unique,     0 total GDI usage error(s)
      0 unique,     0 total handle leak(s)
      0 unique,     0 total warning(s)
      0 unique,     0 total,      0 byte(s) of leak(s)
      1 unique,     1 total,     31 byte(s) of possible leak(s)
ERRORS IGNORED:
      4 unique,     4 total,   4142 byte(s) of still-reachable allocation(s)
         (re-run with "-show_reachable" for details)
Details: C:\Users\Gilad Freidkin\AppData\Roaming\Dr. Memory\DrMemory-mtm_buggy.exe.10632.000\results.txt
```

**Versions**
 - What version of Dr. Memory are you using? 2.3.18722
- What operating system version are you running on? 
```
  Edition	Windows 10 Pro
  Version	20H2
  Installed on	‎27/‎03/‎2021
  OS build	19042.928
  Experience	Windows Feature Experience Pack 120.2212.551.0
```
- Is your application 32-bit or 64-bit? Don't know.

