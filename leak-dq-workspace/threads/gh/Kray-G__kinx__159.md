# Problems reported by valgrind

- URL: https://github.com/Kray-G/kinx/issues/159
- Repo: Kray-G/kinx (language: C)
- State: open; created 2021-01-16T10:16:03Z; status ok; passes offcwe

## Issue body

reporter (NONE) · mingodad · 2021-01-16T10:16:03Z · https://github.com/Kray-G/kinx/issues/159

Adding `-g` to CFLAGS, building kinx and running it under valgrind we get this output:
```
valgrind --track-origins=yes ../kinx fib.kx 
==2199== Memcheck, a memory error detector
==2199== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==2199== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==2199== Command: /home/mingo/dev/c/A_programming-languages/kinx/kinx fib.kx
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2199==    by 0x108FBA: strncpy (string_fortified.h:106)
==2199==    by 0x108FBA: get_kinx_path (fileutil.c:297)
==2199==    by 0x108CBB: load_kinx_dll (libkinx.h:134)
==2199==    by 0x108CBB: kinx_call_main (libkinx.h:185)
==2199==    by 0x108CBB: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x108F3A: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2199==    by 0x593E5BA: strncpy (string_fortified.h:106)
==2199==    by 0x593E5BA: get_kinx_path (fileutil.c:297)
==2199==    by 0x593E978: kxlib_file_exists_no_current (loadlib.c:112)
==2199==    by 0x593DEBF: load_using_module (lexer.c:100)
==2199==    by 0x593BB5A: process_using (lexer.c:145)
==2199==    by 0x593BB5A: get_keyword_token (lexer.c:250)
==2199==    by 0x593BB5A: kx_yylex (lexer.c:987)
==2199==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2199==    by 0x58F0190: eval (ir_util.c:401)
==2199==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2199==    by 0x594024E: do_main (mainlib.c:306)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x593E53A: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2199==    by 0x834E73A: strncpy (string_fortified.h:106)
==2199==    by 0x834E73A: get_actual_exe_path (fileutil.c:314)
==2199==    by 0x833D765: System_exepath (kxsystem.c:1626)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E6C1: get_actual_exe_path (fileutil.c:307)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2199==    by 0x834E42A: strncpy (string_fortified.h:106)
==2199==    by 0x834E42A: get_kinx_path (fileutil.c:297)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2199==    by 0x834E442: strncpy (string_fortified.h:106)
==2199==    by 0x834E442: setup_actual_exe_path (fileutil.c:51)
==2199==    by 0x834E442: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C34C38: rindex (vg_replace_strmem.c:200)
==2199==    by 0x834E453: setup_actual_exe_path (fileutil.c:59)
==2199==    by 0x834E453: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x834E457: setup_actual_exe_path (fileutil.c:60)
==2199==    by 0x834E457: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Use of uninitialised value of size 8
==2199==    at 0x834E459: setup_actual_exe_path (fileutil.c:60)
==2199==    by 0x834E459: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x834E47E: setup_actual_exe_path (fileutil.c:61)
==2199==    by 0x834E47E: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Use of uninitialised value of size 8
==2199==    at 0x834E4B5: strcpy (string_fortified.h:90)
==2199==    by 0x834E4B5: setup_actual_exe_path (fileutil.c:62)
==2199==    by 0x834E4B5: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Syscall param stat(file_name) points to uninitialised byte(s)
==2199==    at 0x5151845: _xstat (xstat.c:35)
==2199==    by 0x834E329: stat (stat.h:451)
==2199==    by 0x834E329: file_exists (fileutil.c:277)
==2199==    by 0x834E4C3: setup_actual_exe_path (fileutil.c:63)
==2199==    by 0x834E4C3: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Address 0x85aead3 is 51 bytes inside data symbol "exe_full_path.4920"
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Use of uninitialised value of size 8
==2199==    at 0x834E690: strcpy (string_fortified.h:90)
==2199==    by 0x834E690: setup_actual_exe_path (fileutil.c:64)
==2199==    by 0x834E690: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Syscall param stat(file_name) points to uninitialised byte(s)
==2199==    at 0x5151845: _xstat (xstat.c:35)
==2199==    by 0x834E329: stat (stat.h:451)
==2199==    by 0x834E329: file_exists (fileutil.c:277)
==2199==    by 0x834E4D7: setup_actual_exe_path (fileutil.c:67)
==2199==    by 0x834E4D7: get_kinx_path (fileutil.c:298)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Address 0x85aead3 is 51 bytes inside data symbol "exe_full_path.4920"
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C34C38: rindex (vg_replace_strmem.c:200)
==2199==    by 0x834E4EC: get_kinx_path (fileutil.c:299)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x834E4F0: get_kinx_path (fileutil.c:300)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Use of uninitialised value of size 8
==2199==    at 0x834E4F6: get_kinx_path (fileutil.c:300)
==2199==    by 0x833D685: System_kinxpath (kxsystem.c:1614)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C35108: strlen (vg_replace_strmem.c:459)
==2199==    by 0x8351214: ks_append (kstr.c:187)
==2199==    by 0x833D690: System_kinxpath (kxsystem.c:1615)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
==2199== Conditional jump or move depends on uninitialised value(s)
==2199==    at 0x4C34FD8: strncat (vg_replace_strmem.c:349)
==2199==    by 0x83511C4: strncat (string_fortified.h:136)
==2199==    by 0x83511C4: ks_append_n (kstr.c:208)
==2199==    by 0x83511C4: ks_append_n (kstr.c:195)
==2199==    by 0x833D690: System_kinxpath (kxsystem.c:1615)
==2199==    by 0x58E7F43: ir_exec_impl (ir_exec.inl:27)
==2199==    by 0x58EF976: ir_exec (ir_exec.inl:284)
==2199==    by 0x594043A: do_main (mainlib.c:379)
==2199==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2199==    by 0x108C9D: main (main.c:18)
==2199==  Uninitialised value was created by a stack allocation
==2199==    at 0x834E3AA: get_kinx_path (fileutil.c:290)
==2199== 
fib(34) = 9227465
==2199== 
==2199== HEAP SUMMARY:
==2199==     in use at exit: 498,201 bytes in 2,970 blocks
==2199==   total heap usage: 37,100 allocs, 34,130 frees, 37,060,116 bytes allocated
==2199== 
==2199== LEAK SUMMARY:
==2199==    definitely lost: 493,216 bytes in 2,956 blocks
==2199==    indirectly lost: 0 bytes in 0 blocks
==2199==      possibly lost: 0 bytes in 0 blocks
==2199==    still reachable: 4,985 bytes in 14 blocks
==2199==         suppressed: 0 bytes in 0 blocks
==2199== Rerun with --leak-check=full to see details of leaked memory
==2199== 
==2199== For lists of detected and suppressed errors, rerun with: -s
==2199== ERROR SUMMARY: 301 errors from 18 contexts (suppressed: 0 from 0)
```
 

## Comment 761539827

reporter (NONE) · mingodad · 2021-01-16T10:22:44Z · https://github.com/Kray-G/kinx/issues/159#issuecomment-761539827

When trying to execute examples/sample.kx we get a segfault and with valgrind we get this:
```
valgrind ../kinx sample.kx 
==2456== Memcheck, a memory error detector
==2456== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==2456== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==2456== Command: ../kinx sample.kx
==2456== 
==2456== Conditional jump or move depends on uninitialised value(s)
==2456==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2456==    by 0x108FBA: strncpy (string_fortified.h:106)
==2456==    by 0x108FBA: get_kinx_path (fileutil.c:297)
==2456==    by 0x108CBB: load_kinx_dll (libkinx.h:134)
==2456==    by 0x108CBB: kinx_call_main (libkinx.h:185)
==2456==    by 0x108CBB: main (main.c:18)
==2456== 
==2456== Conditional jump or move depends on uninitialised value(s)
==2456==    at 0x4C3571F: __strncpy_sse2_unaligned (vg_replace_strmem.c:553)
==2456==    by 0x593E5BA: strncpy (string_fortified.h:106)
==2456==    by 0x593E5BA: get_kinx_path (fileutil.c:297)
==2456==    by 0x593E978: kxlib_file_exists_no_current (loadlib.c:112)
==2456==    by 0x593DEBF: load_using_module (lexer.c:100)
==2456==    by 0x593BB5A: process_using (lexer.c:145)
==2456==    by 0x593BB5A: get_keyword_token (lexer.c:250)
==2456==    by 0x593BB5A: kx_yylex (lexer.c:987)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
Error: syntax error near the <sample.kx>:5
==2456== Invalid read of size 4
==2456==    at 0x586D710: kx_gen_stmtlist (ast_object.c:210)
==2456==    by 0x594394D: kx_yyparse (kinx.y:171)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456==  Address 0x54b7f68 is 24 bytes before a block of size 16 alloc'd
==2456==    at 0x4C31E83: malloc (vg_replace_malloc.c:307)
==2456==    by 0x58519B8: kx_malloc_impl (alloccore.c:40)
==2456==    by 0x5946617: alloc_string (string.c:10)
==2456==    by 0x59467E0: const_str (string.c:28)
==2456==    by 0x5939C11: kx_yylex (lexer.c:986)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
==2456== Invalid read of size 4
==2456==    at 0x59470AA: opt_ast_constant_folding (opt_cfold.c:26)
==2456==    by 0x59470CB: opt_ast_constant_folding (opt_cfold.c:397)
==2456==    by 0x5947107: opt_ast_constant_folding (opt_cfold.c:390)
==2456==    by 0x59470CB: opt_ast_constant_folding (opt_cfold.c:397)
==2456==    by 0x59470CB: opt_ast_constant_folding (opt_cfold.c:397)
==2456==    by 0x58F01C6: eval (ir_util.c:407)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456==  Address 0x54b7f68 is 24 bytes before a block of size 16 alloc'd
==2456==    at 0x4C31E83: malloc (vg_replace_malloc.c:307)
==2456==    by 0x58519B8: kx_malloc_impl (alloccore.c:40)
==2456==    by 0x5946617: alloc_string (string.c:10)
==2456==    by 0x59467E0: const_str (string.c:28)
==2456==    by 0x5939C11: kx_yylex (lexer.c:986)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
==2456== Invalid read of size 4
==2456==    at 0x58525FA: analyze_ast (ast_analyzer.c:348)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x585369B: analyze_ast (ast_analyzer.c:1089)
==2456==    by 0x5853647: analyze_ast (ast_analyzer.c:1099)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x5855BC9: start_analyze_ast (ast_analyzer.c:1402)
==2456==    by 0x58F01D2: eval (ir_util.c:408)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456==  Address 0x54b7fc0 is 16 bytes before a block of size 7 alloc'd
==2456==    at 0x4C31E83: malloc (vg_replace_malloc.c:307)
==2456==    by 0x50DFAF9: strdup (strdup.c:42)
==2456==    by 0x5851A58: kx_strdup_impl (alloccore.c:75)
==2456==    by 0x5946626: alloc_string (string.c:11)
==2456==    by 0x59467E0: const_str (string.c:28)
==2456==    by 0x5939C11: kx_yylex (lexer.c:986)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
==2456== Invalid read of size 8
==2456==    at 0x5852600: analyze_ast (ast_analyzer.c:348)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x585369B: analyze_ast (ast_analyzer.c:1089)
==2456==    by 0x5853647: analyze_ast (ast_analyzer.c:1099)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x5855BC9: start_analyze_ast (ast_analyzer.c:1402)
==2456==    by 0x58F01D2: eval (ir_util.c:408)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456==  Address 0x54b7fb8 is 24 bytes before a block of size 7 alloc'd
==2456==    at 0x4C31E83: malloc (vg_replace_malloc.c:307)
==2456==    by 0x50DFAF9: strdup (strdup.c:42)
==2456==    by 0x5851A58: kx_strdup_impl (alloccore.c:75)
==2456==    by 0x5946626: alloc_string (string.c:11)
==2456==    by 0x59467E0: const_str (string.c:28)
==2456==    by 0x5939C11: kx_yylex (lexer.c:986)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
==2456== Invalid read of size 4
==2456==    at 0x585260E: analyze_ast (ast_analyzer.c:352)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x585369B: analyze_ast (ast_analyzer.c:1089)
==2456==    by 0x5853647: analyze_ast (ast_analyzer.c:1099)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x5855BC9: start_analyze_ast (ast_analyzer.c:1402)
==2456==    by 0x58F01D2: eval (ir_util.c:408)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456==  Address 0x54b7f68 is 24 bytes before a block of size 16 alloc'd
==2456==    at 0x4C31E83: malloc (vg_replace_malloc.c:307)
==2456==    by 0x58519B8: kx_malloc_impl (alloccore.c:40)
==2456==    by 0x5946617: alloc_string (string.c:10)
==2456==    by 0x59467E0: const_str (string.c:28)
==2456==    by 0x5939C11: kx_yylex (lexer.c:986)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
==2456== Invalid write of size 4
==2456==    at 0x5852620: analyze_ast (ast_analyzer.c:351)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x585369B: analyze_ast (ast_analyzer.c:1089)
==2456==    by 0x5853647: analyze_ast (ast_analyzer.c:1099)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x58536BA: analyze_ast (ast_analyzer.c:1080)
==2456==    by 0x5855BC9: start_analyze_ast (ast_analyzer.c:1402)
==2456==    by 0x58F01D2: eval (ir_util.c:408)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456==  Address 0x54b7f90 is 0 bytes after a block of size 16 alloc'd
==2456==    at 0x4C31E83: malloc (vg_replace_malloc.c:307)
==2456==    by 0x58519B8: kx_malloc_impl (alloccore.c:40)
==2456==    by 0x5946617: alloc_string (string.c:10)
==2456==    by 0x59467E0: const_str (string.c:28)
==2456==    by 0x5939C11: kx_yylex (lexer.c:986)
==2456==    by 0x5941243: kx_yyparse (kmyacc.c.parser:330)
==2456==    by 0x58F0190: eval (ir_util.c:401)
==2456==    by 0x58F4BFF: eval_file (ir_util.c:482)
==2456==    by 0x594024E: do_main (mainlib.c:306)
==2456==    by 0x108C9D: kinx_call_main (libkinx.h:198)
==2456==    by 0x108C9D: main (main.c:18)
==2456== 
==2456== 
==2456== HEAP SUMMARY:
==2456==     in use at exit: 493,056 bytes in 2,952 blocks
==2456==   total heap usage: 27,284 allocs, 24,332 frees, 9,298,874 bytes allocated
==2456== 
==2456== LEAK SUMMARY:
==2456==    definitely lost: 493,056 bytes in 2,952 blocks
==2456==    indirectly lost: 0 bytes in 0 blocks
==2456==      possibly lost: 0 bytes in 0 blocks
==2456==    still reachable: 0 bytes in 0 blocks
==2456==         suppressed: 0 bytes in 0 blocks
==2456== Rerun with --leak-check=full to see details of leaked memory
==2456== 
==2456== Use --track-origins=yes to see where uninitialised values come from
==2456== For lists of detected and suppressed errors, rerun with: -s
==2456== ERROR SUMMARY: 8 errors from 8 contexts (suppressed: 0 from 0)
```


## Comment 761551757

maintainer (OWNER) · Kray-G · 2021-01-16T11:58:27Z · https://github.com/Kray-G/kinx/issues/159#issuecomment-761551757

Thanks for your report.
I will check this.

## Comment 763616162

maintainer (OWNER) · Kray-G · 2021-01-20T13:47:19Z · https://github.com/Kray-G/kinx/issues/159#issuecomment-763616162

I am sorry, I can not use Linux environment now. Just a moment please. I will try to setup another linux on my system.
This is just a progress information.

## Comment 766085612

maintainer (OWNER) · Kray-G · 2021-01-23T14:13:05Z · https://github.com/Kray-G/kinx/issues/159#issuecomment-766085612

In the latest source code, uninitialized values and segfault with sample.kx will be fixed, but memory leak problem is remaining.
I tried valgrind with --leak-check=full option, but the following message will be shown in my system.

```
$ valgrind --leak-check=full ./kinx ../examples/sample.kx

... (omitted)
==4782== 163,840 bytes in 2,048 blocks are definitely lost in loss record 138 of 138
==4782==    at 0x483DD99: calloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==4782==    by 0x4E6D98C: ???
==4782==    by 0x4E6ADFC: ???
==4782==    by 0x4E6B28B: ???
==4782==    by 0x4F5CE92: ???
==4782==    by 0x109331: kinx_call_main (libkinx.h:229)
==4782==    by 0x109331: main (main.c:9)
==4782==
==4782== LEAK SUMMARY:
==4782==    definitely lost: 498,848 bytes in 2,967 blocks
==4782==    indirectly lost: 0 bytes in 0 blocks
==4782==      possibly lost: 0 bytes in 0 blocks
==4782==    still reachable: 5,065 bytes in 14 blocks
==4782==         suppressed: 0 bytes in 0 blocks
```

I do not know why the function name is not displayed.
If you have any messages at your system, please share it with me?

I am also going to try another way to find it cause.

Thanks in advance.


## Comment 766803303

maintainer (OWNER) · Kray-G · 2021-01-25T13:07:12Z · https://github.com/Kray-G/kinx/issues/159#issuecomment-766803303

As I have a limited access to a linux environemnt, so I tried to find it out on Windows with `<crtdbg.h>` of Visual Studio.
Then, I have some memory leak detections and I have fixed those all on Windows.

At least on Windows, there are no errors in SpecTest, REPL, and Isolate library of threading.

If possible, please try the latest source code on Linux.

Thanks in advance.

## Comment 800213542

maintainer (OWNER) · Kray-G · 2021-03-16T12:22:09Z · https://github.com/Kray-G/kinx/issues/159#issuecomment-800213542

It is just a information.

I was going to fix all memory leaks, but it still has remained...
Now only `still reachable: 6,566 bytes in 19 blocks` is remaining, but I feel it is not a big problem so far because it is always same result with any code.

I will fix it when I have time.
