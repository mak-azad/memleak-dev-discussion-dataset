# Uninitialised value by a heap allocation within RzStrBuf

- URL: https://github.com/rizinorg/rizin/issues/5509
- Repo: rizinorg/rizin (language: C)
- State: open; created 2025-11-08T04:51:49Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · SSharshunov · 2025-11-08T04:51:49Z · https://github.com/rizinorg/rizin/issues/5509

<!-- This template is meant for bug reports, if you have a feature request, please be as descriptive as possible and delete the template

Make sure you are testing using the latest git version of rizin before submitting any issue.

If you would like to report a bug, please fill the template below
-->

### Work environment

| Questions                                            | Answers
|------------------------------------------------------|--------------------
| OS/arch/bits (mandatory)                             | Ubuntu x64
| File format of the file you reverse (mandatory)      | maybe all
| Architecture/bits of the file (mandatory)            | maybe all
| `rizin -v` full output, **not truncated** (mandatory)  | rizin 0.9.0 @ linux-x86-64, commit: bd9725b0b968577798790f8fc035e9fcaefd3153


### Expected behavior
No leaks
### Actual behavior

```
==760529== Conditional jump or move depends on uninitialised value(s)
==760529==    at 0x4C3CFC9: ???
==760529==    by 0x85FC72E: ???
==760529==  Uninitialised value was created by a heap allocation
==760529==    at 0x483D7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==760529==    by 0x48FB060: rz_strbuf_append_n (strbuf.c:290)
==760529==    by 0x48FABC0: rz_strbuf_append (strbuf.c:211)
==760529==    by 0x48E102D: rz_print_colorize_asm_str (print.c:1452)
==760529==    by 0x5B2CCF1: rz_asm_colorize_asm_str (asm.c:1897)
==760529==    by 0x78E67E5: ds_opstr_try_colorize (disasm.c:892)
==760529==    by 0x78E7345: ds_build_op_str (disasm.c:1034)
==760529==    by 0x78F8A5B: rz_core_print_disasm (disasm.c:5476)
==760529==    by 0x797CBBE: core_disassembly (cmd_print.c:2842)
==760529==    by 0x797CE57: rz_cmd_disassembly_n_instructions_handler (cmd_print.c:2890)
==760529==    by 0x799DDC8: argv_call_cb (cmd_api.c:766)
==760529==    by 0x799DF46: call_cd (cmd_api.c:800)
```
```
==670741== Conditional jump or move depends on uninitialised value(s)
==670741==    at 0x4B7F978: ???
==670741==    by 0x94A366F: ???
==670741==  Uninitialised value was created by a heap allocation
==670741==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==670741==    by 0x48E5234: rz_strbuf_append_n (strbuf.c:231)
==670741==    by 0x48E5234: rz_strbuf_append_n (strbuf.c:214)
==670741==    by 0x48D1ED0: rz_print_colorize_asm_str (print.c:1449)
==670741==    by 0x586706B: rz_asm_colorize_asm_str (asm.c:1898)
==670741==    by 0x727B1B7: ds_opstr_try_colorize (disasm.c:892)
==670741==    by 0x727CFB6: ds_build_op_str (disasm.c:1033)
==670741==    by 0x7286C8A: rz_core_print_disasm.part.0 (disasm.c:5475)
==670741==    by 0x72C7E46: core_disassembly (cmd_print.c:2842)
==670741==    by 0x72E66FC: rz_cmd_disassembly_n_instructions_handler (cmd_print.c:2890)
==670741==    by 0x7305215: argv_call_cb (cmd_api.c:766)
==670741==    by 0x7305215: call_cd (cmd_api.c:800)
==670741==    by 0x7305215: rz_cmd_call_parsed_args (cmd_api.c:813)
==670741==    by 0x72FDE03: handle_ts_arged_stmt_internal (cmd.c:1149)
==670741==    by 0x72FDE03: handle_ts_arged_stmt (cmd.c:1097)
==670741==    by 0x72BDB57: handle_ts_stmt (cmd.c:2684)

```
```
==670741== Invalid read of size 16
==670741==    at 0x4B7F95F: ???
==670741==    by 0x946B59F: ???
==670741==  Address 0x946b5af is 15 bytes inside a block of size 27 alloc'd
==670741==    at 0x483B7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==670741==    by 0x4C3C38E: strdup (strdup.c:42)
==670741==    by 0x48E5CC9: drain (strbuf.c:313)
==670741==    by 0x48E5CC9: rz_strbuf_drain (strbuf.c:325)
==670741==    by 0x727B1DB: ds_opstr_try_colorize (disasm.c:898)
==670741==    by 0x727CFB6: ds_build_op_str (disasm.c:1033)
==670741==    by 0x7286C8A: rz_core_print_disasm.part.0 (disasm.c:5475)
==670741==    by 0x72C7E46: core_disassembly (cmd_print.c:2842)
==670741==    by 0x72E66FC: rz_cmd_disassembly_n_instructions_handler (cmd_print.c:2890)
==670741==    by 0x7305215: argv_call_cb (cmd_api.c:766)
==670741==    by 0x7305215: call_cd (cmd_api.c:800)
==670741==    by 0x7305215: rz_cmd_call_parsed_args (cmd_api.c:813)
==670741==    by 0x72FDE03: handle_ts_arged_stmt_internal (cmd.c:1149)
==670741==    by 0x72FDE03: handle_ts_arged_stmt (cmd.c:1097)
==670741==    by 0x72BDB57: handle_ts_stmt (cmd.c:2684)
==670741==    by 0x72EEE6B: handle_ts_statements_internal (cmd.c:2741)
==670741==    by 0x72EEE6B: handle_ts_statements (cmd.c:2706)
```
```
==744508== 1,344 bytes in 12 blocks are definitely lost in loss record 4 of 5
==744508==    at 0x483D7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==744508==    by 0x49519D6: _pcre2_memctl_malloc_8 (pcre2_context.c:89)
==744508==    by 0x4951BD6: pcre2_match_context_create_8 (pcre2_context.c:190)
==744508==    by 0x48E6AFC: match_first_8 (regex.c:671)
==744508==    by 0x48E7911: match_all_internal_8 (regex.c:1037)
==744508==    by 0x48E7FBB: rz_regex_match_all_multi (regex.c:1251)
==744508==    by 0x7362B83: native_string_find (string_search.c:89)
==744508==    by 0x73634FB: string_find (string_search.c:236)
==744508==    by 0x735B704: search_iterator_io_map_cb (search.c:640)
==744508==    by 0x490B14D: thread_iterate_list_cb (thread_iterators.c:57)
==744508==    by 0x4908880: thread_main_function (thread.c:21)
==744508==    by 0x4FB7608: start_thread (pthread_create.c:477)
==744508== 
==744508== 1,064,448 bytes in 9,504 blocks are definitely lost in loss record 5 of 5
==744508==    at 0x483D7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==744508==    by 0x49519D6: _pcre2_memctl_malloc_8 (pcre2_context.c:89)
==744508==    by 0x4951BD6: pcre2_match_context_create_8 (pcre2_context.c:190)
==744508==    by 0x48E6AFC: match_first_8 (regex.c:671)
==744508==    by 0x48E7987: match_all_internal_8 (regex.c:1043)
==744508==    by 0x48E7FBB: rz_regex_match_all_multi (regex.c:1251)
==744508==    by 0x7362B83: native_string_find (string_search.c:89)
==744508==    by 0x73634FB: string_find (string_search.c:236)
==744508==    by 0x735B704: search_iterator_io_map_cb (search.c:640)
==744508==    by 0x490B14D: thread_iterate_list_cb (thread_iterators.c:57)
==744508==    by 0x4908880: thread_main_function (thread.c:21)
==744508==    by 0x4FB7608: start_thread (pthread_create.c:477)
```
Resolved


## Comment 3506819975

maintainer (MEMBER) · Rot127 · 2025-11-08T19:26:27Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3506819975

What is the command you run?

## Comment 3507474751

reporter (CONTRIBUTOR) · SSharshunov · 2025-11-09T03:18:11Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3507474751

I launched them in my fork, but I think you can find them in other architectures as well.

`valgrind -s --track-origins=yes --leak-check=full --show-leak-kinds=all ./rizin -a c166 -qc 'pd' measure`

## Comment 3519846939

reporter (CONTRIBUTOR) · SSharshunov · 2025-11-12T04:10:44Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3519846939

moved from PR #5515 

There is another problem by the way: if the buffer is less than 32 bytes, a memory access error appears.
For example: mnemonic 0xA5 `diswdt`

---------------------------------------
==3275266== Invalid read of size 16
==3275266==    at 0x4C3CFDF: ???
==3275266==    by 0x8E99F9F: ???
==3275266==  Address 0x8e99faf is 15 bytes inside a block of size 30 alloc'd
==3275266==    at 0x483D7F3: malloc (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==3275266==    by 0x4D0038E: strdup (strdup.c:42)
==3275266==    by 0x48EE419: rz_str_dup (str.c:1112)
==3275266==    by 0x48FB203: drain (strbuf.c:315)
==3275266==    by 0x48FB259: rz_strbuf_drain (strbuf.c:327)
==3275266==    by 0x78E6005: ds_opstr_try_colorize (disasm.c:898)
==3275266==    by 0x78E6B1B: ds_build_op_str (disasm.c:1033)
==3275266==    by 0x78F8231: rz_core_print_disasm (disasm.c:5475)
==3275266==    by 0x797C8D4: core_disassembly (cmd_print.c:2842)
==3275266==    by 0x797CB6D: rz_cmd_disassembly_n_instructions_handler (cmd_print.c:2890)
==3275266==    by 0x799DAFC: argv_call_cb (cmd_api.c:766)
==3275266==    by 0x799DC7A: call_cd (cmd_api.c:800)
==3275266== 
==3275266== Conditional jump or move depends on uninitialised value(s)
==3275266==    at 0x4C3CFC9: ???
==3275266==    by 0x8E99F9F: ???
==3275266== 


## Comment 3525294928

maintainer (MEMBER) · wargio · 2025-11-13T04:31:36Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3525294928

Please add the reproducer binary and commands 

## Comment 3940567888

other (CONTRIBUTOR) · notxvilka · 2026-02-22T09:22:33Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3940567888

@SSharshunov ping on this one

## Comment 3940583353

reporter (CONTRIBUTOR) · SSharshunov · 2026-02-22T09:34:16Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3940583353

https://github.com/SSharshunov/rizin-testbins/blob/omf166/omf/omf166/measure

## Comment 3940583709

reporter (CONTRIBUTOR) · SSharshunov · 2026-02-22T09:34:34Z · https://github.com/rizinorg/rizin/issues/5509#issuecomment-3940583709

> Я запустил их в своей ветке, но думаю, вы сможете найти их и в других архитектурах.
> 
> `valgrind -s --track-origins=yes --leak-check=full --show-leak-kinds=all ./rizin -a c166 -qc 'pd' measure`


