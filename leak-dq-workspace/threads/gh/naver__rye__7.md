# fix valgrind

- URL: https://github.com/naver/rye/issues/7
- Repo: naver/rye (language: C)
- State: open; created 2017-10-20T07:02:02Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · iamksseo · 2017-10-20T07:02:02Z · https://github.com/naver/rye/issues/7

repro: v1.0.0

```
************ MASTER *************
rye_server
​
==14296== Thread 1:
==14296==
==14296== 8 bytes in 8 blocks are definitely lost in loss record 1 of 21
==14296==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14296==    by 0x4E05502: mr_readval_varbit_internal (object_primitive.c:6786)
==14296==    by 0x4E05054: mr_data_readval_varbit (object_primitive.c:6646)
==14296==    by 0x4DD3D72: qdata_finalize_aggregate_list (query_opfunc.c:1722)
==14296==    by 0x4DB9E50: qexec_end_buildvalueblock_iterations (query_executor.c:6506)
==14296==    by 0x4DBA79E: qexec_end_mainblock_iterations (query_executor.c:6696)
==14296==    by 0x4DBC3F0: qexec_execute_mainblock_internal (query_executor.c:7283)
==14296==    by 0x4DBAE54: qexec_execute_mainblock (query_executor.c:6863)
==14296==    by 0x4DC1919: qexec_execute_query (query_executor.c:8735)
==14296==    by 0x4D55212: qmgr_process_query (query_manager.c:1517)
==14296==    by 0x4D55CC1: xqmgr_execute_query (query_manager.c:1776)
==14296==    by 0x4D0273F: sqmgr_execute_query (network_interface_sr.c:3348)
==14296==    by 0x4D0C702: net_server_request (network_sr.c:804)
==14296==    by 0x4CF2160: css_internal_request_handler (server_support.c:1217)
==14296==    by 0x4C84B5C: thread_worker (thread.c:2419)
==14296==    by 0x3D5D80683C: start_thread (in /lib64/libpthread-2.5.so)
==14296==    by 0x3D5D0D4FCC: clone (in /lib64/libc-2.5.so)
==14296==
==14296==
==14296== 12 bytes in 12 blocks are definitely lost in loss record 2 of 21
==14296==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14296==    by 0x4E04CE5: mr_setval_varbit (object_primitive.c:6580)
==14296==    by 0x4DCEF70: qdata_copy_db_value (query_opfunc.c:164)
==14296==    by 0x4D3DF5B: fetch_copy_dbval (fetch.c:3313)
==14296==    by 0x4DD259F: qdata_evaluate_aggregate_list (query_opfunc.c:1268)
==14296==    by 0x4DAACC4: qexec_end_one_iteration (query_executor.c:1202)
==14296==    by 0x4DB2F83: qexec_intprt_fnc (query_executor.c:4430)
==14296==    by 0x4DBC245: qexec_execute_mainblock_internal (query_executor.c:7255)
==14296==    by 0x4DBAE54: qexec_execute_mainblock (query_executor.c:6863)
==14296==    by 0x4DC1919: qexec_execute_query (query_executor.c:8735)
==14296==    by 0x4D55212: qmgr_process_query (query_manager.c:1517)
==14296==    by 0x4D55CC1: xqmgr_execute_query (query_manager.c:1776)
==14296==    by 0x4D0273F: sqmgr_execute_query (network_interface_sr.c:3348)
==14296==    by 0x4D0C702: net_server_request (network_sr.c:804)
==14296==    by 0x4CF2160: css_internal_request_handler (server_support.c:1217)
==14296==    by 0x4C84B5C: thread_worker (thread.c:2419)
==14296==    by 0x3D5D80683C: start_thread (in /lib64/libpthread-2.5.so)
==14296==    by 0x3D5D0D4FCC: clone (in /lib64/libc-2.5.so)
==14296==
==14296==
==14296== 12 bytes in 2 blocks are definitely lost in loss record 3 of 21
==14296==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14296==    by 0x4E03713: mr_readval_string_internal (object_primitive.c:6050)
==14296==    by 0x4E031B8: mr_data_readval_string (object_primitive.c:5895)
==14296==    by 0x4DF6248: or_get_value (object_representation.c:5398)
==14296==    by 0x4DF7724: or_unpack_db_value (object_representation.c:5819)
==14296==    by 0x4DE1CA7: stx_build_db_value (stream_to_xasl.c:3624)
==14296==    by 0x4DE164E: stx_unpack_regu_variable_value (stream_to_xasl.c:3472)
==14296==    by 0x4DE1508: stx_build_regu_variable (stream_to_xasl.c:3450)
==14296==    by 0x4DDABBE: stx_restore_regu_variable_list (stream_to_xasl.c:1055)
==14296==    by 0x4DE2888: stx_build_function_type (stream_to_xasl.c:3896)
==14296==    by 0x4DD965C: stx_restore_function_type (stream_to_xasl.c:521)
==14296==    by 0x4DE181D: stx_unpack_regu_variable_value (stream_to_xasl.c:3521)
==14296==    by 0x4DE1508: stx_build_regu_variable (stream_to_xasl.c:3450)
==14296==    by 0x4DD9F98: stx_restore_regu_variable (stream_to_xasl.c:718)
==14296==    by 0x4DDAE08: stx_restore_key_range_array (stream_to_xasl.c:1106)
==14296==    by 0x4DE01C6: stx_build_key_info (stream_to_xasl.c:3015)
==14296==    by 0x4DDFEB8: stx_build_indx_info (stream_to_xasl.c:2954)
==14296==    by 0x4DD9AFA: stx_restore_indx_info (stream_to_xasl.c:620)
==14296==    by 0x4DDFA22: stx_build_access_spec_type (stream_to_xasl.c:2850)
==14296==    by 0x4DDB0E9: stx_restore_access_spec_type (stream_to_xasl.c:1167)
==14296==    by 0x4DDBACB: stx_build_xasl_node (stream_to_xasl.c:1387)
==14296==    by 0x4DDA5C0: stx_restore_xasl_node (stream_to_xasl.c:846)
==14296==    by 0x4DE14B9: stx_build_regu_variable (stream_to_xasl.c:3441)
==14296==    by 0x4DDABBE: stx_restore_regu_variable_list (stream_to_xasl.c:1055)
==14296==    by 0x4DDE7B1: stx_build_outptr_list (stream_to_xasl.c:2405)
==14296==    by 0x4DD9C84: stx_restore_outptr_list (stream_to_xasl.c:653)
==14296==    by 0x4DDE629: stx_build_insert_proc (stream_to_xasl.c:2369)
==14296==    by 0x4DDC333: stx_build_xasl_node (stream_to_xasl.c:1563)
==14296==    by 0x4DDA5C0: stx_restore_xasl_node (stream_to_xasl.c:846)
==14296==    by 0x4DD8E80: stx_map_stream_to_xasl (stream_to_xasl.c:335)
==14296==
==14296==
==14296== 64 bytes in 1 blocks are definitely lost in loss record 10 of 21
==14296==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14296==    by 0x4C98AF2: er_init (error_manager.c:849)
==14296==    by 0x4D0CEF9: net_server_start (network_sr.c:1032)
==14296==    by 0x401DB2: main (server.c:211)
==14296==
==14296==
==14296== 1,368 bytes in 3 blocks are possibly lost in loss record 18 of 21
==14296==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14296==    by 0x4CB9E57: fi_thread_init (fault_injection.c:194)
==14296==    by 0x4C82553: thread_initialize_entry (thread.c:1228)
==14296==    by 0x4C7F86E: thread_initialize_manager (thread.c:431)
==14296==    by 0x4D0CDD3: net_server_start (network_sr.c:1020)
==14296==    by 0x401DB2: main (server.c:211)
==14296==
==14296==
==14296== 4,639,800 bytes in 10,175 blocks are definitely lost in loss record 21 of 21
==14296==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14296==    by 0x4CB9E57: fi_thread_init (fault_injection.c:194)
==14296==    by 0x4C82553: thread_initialize_entry (thread.c:1228)
==14296==    by 0x4C7F86E: thread_initialize_manager (thread.c:431)
==14296==    by 0x4D0CDD3: net_server_start (network_sr.c:1020)
==14296==    by 0x401DB2: main (server.c:211)
==14296==
==14296== LEAK SUMMARY:
==14296==    definitely lost: 4,639,896 bytes in 10,198 blocks.
==14296==      possibly lost: 1,368 bytes in 3 blocks.
==14296==    still reachable: 68,830 bytes in 1,218 blocks.
==14296==         suppressed: 0 bytes in 0 blocks.
==14296== Reachable blocks (those to which a pointer was found) are not shown.
==14296== To see them, rerun with: --leak-check=full --show-reachable=yes
​
​
rye_repl
==14297== Thread 1:
==14297==
==14297== 64 bytes in 1 blocks are definitely lost in loss record 6 of 26
==14297==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14297==    by 0x4D1B125: hb_thread_master_reader (heartbeat.c:214)
==14297==    by 0x3D5D80683C: start_thread (in /lib64/libpthread-2.5.so)
==14297==    by 0x3D5D0D4FCC: clone (in /lib64/libc-2.5.so)
==14297==
==14297==
==14297== 208 bytes in 11 blocks are definitely lost in loss record 13 of 26
==14297==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14297==    by 0x4CD2409: er_vsprintf (error_manager.c:3116)
==14297==    by 0x4CCDCE1: er_set_internal (error_manager.c:1367)
==14297==    by 0x4CCD11C: er_set (error_manager.c:1084)
==14297==    by 0x41C47C: log_copier_main (repl_writer.c:1858)
==14297==    by 0x3D5D80683C: start_thread (in /lib64/libpthread-2.5.so)
==14297==    by 0x3D5D0D4FCC: clone (in /lib64/libc-2.5.so)
==14297==
==14297==
==14297== 288 bytes in 1 blocks are possibly lost in loss record 14 of 26
==14297==    at 0x4A050CC: calloc (vg_replace_malloc.c:397)
==14297==    by 0x3D5CC10162: _dl_allocate_tls (in /lib64/ld-2.5.so)
==14297==    by 0x3D5D806FA2: pthread_create@@GLIBC_2.2.5 (in /lib64/libpthread-2.5.so)
==14297==    by 0x5455EB2: hm_create_health_check_th (cci_handle_mng.c:775)
==14297==    by 0x5435B9D: cci_connect_internal (cas_cci.c:335)
==14297==    by 0x54360C1: cci_connect (cas_cci.c:406)
==14297==    by 0x4312B5: cirp_get_cci_connection (repl.c:714)
==14297==    by 0x42F429: main (repl.c:240)
==14297==
==14297==
==14297== 586 bytes in 11 blocks are definitely lost in loss record 18 of 26
==14297==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14297==    by 0x4CD20FC: er_make_room (error_manager.c:3032)
==14297==    by 0x4CCDC9F: er_set_internal (error_manager.c:1360)
==14297==    by 0x4CCD11C: er_set (error_manager.c:1084)
==14297==    by 0x41C47C: log_copier_main (repl_writer.c:1858)
==14297==    by 0x3D5D80683C: start_thread (in /lib64/libpthread-2.5.so)
==14297==    by 0x3D5D0D4FCC: clone (in /lib64/libc-2.5.so)
==14297==
==14297==
==14297== 33,556 (3,968 direct, 29,588 indirect) bytes in 26 blocks are definitely lost in loss record 22 of 26
==14297==    at 0x4A05FBB: malloc (vg_replace_malloc.c:207)
==14297==    by 0x4F3FE12: db_ws_alloc (quick_fit.c:72)
==14297==    by 0x4F14858: classobj_make_class (class_object.c:2788)
==14297==    by 0x4F45D29: disk_to_class (transform_cl.c:2851)
==14297==    by 0x4F46BF2: tf_disk_to_class (transform_cl.c:3112)
==14297==    by 0x4F6913B: locator_cache_object_class (locator_cl.c:1906)
==14297==    by 0x4F696B5: locator_cache_have_object (locator_cl.c:2078)
==14297==    by 0x4F69B4D: locator_cache (locator_cl.c:2208)
==14297==    by 0x4F668A1: locator_lock (locator_cl.c:669)
==14297==    by 0x4F68D6A: locator_find_class_by_oid (locator_cl.c:1767)
==14297==    by 0x4F68F07: locator_find_class (locator_cl.c:1832)
==14297==    by 0x4F182A1: sm_find_class (schema_manager.c:1894)
==14297==    by 0x4EFC614: au_start (authenticate.c:3469)
==14297==    by 0x4F5DE04: boot_restart_client (boot_cl.c:1025)
==14297==    by 0x4CA3797: db_restart (db_admin.c:610)
==14297==    by 0x432211: cirp_connect_copylogdb (repl.c:916)
==14297==    by 0x42F355: main (repl.c:233)
==14297==
==14297== LEAK SUMMARY:
==14297==    definitely lost: 4,826 bytes in 49 blocks.
==14297==    indirectly lost: 29,588 bytes in 364 blocks.
==14297==      possibly lost: 288 bytes in 1 blocks.
==14297==    still reachable: 92,930 bytes in 1,216 blocks.
==14297==         suppressed: 0 bytes in 0 blocks.
==14297== Reachable blocks (those to which a pointer was found) are not shown.
==14297== To see them, rerun with: --leak-check=full --show-reachable=yes
​
​
​
*************** SLAVE ************
rye_server
​
==22756== Thread 1:
==22756== 64 bytes in 1 blocks are definitely lost in loss record 12 of 26
==22756==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22756==    by 0x4C9CAF2: er_init (error_manager.c:849)
==22756==    by 0x4D10EF9: net_server_start (network_sr.c:1032)
==22756==    by 0x401DB2: main (server.c:211)
==22756==
==22756== 456 bytes in 1 blocks are definitely lost in loss record 16 of 26
==22756==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22756==    by 0x4CBDE57: fi_thread_init (fault_injection.c:194)
==22756==    by 0x4C86553: thread_initialize_entry (thread.c:1228)
==22756==    by 0x4C837A3: thread_initialize_manager (thread.c:413)
==22756==    by 0x4D10DD3: net_server_start (network_sr.c:1020)
==22756==    by 0x401DB2: main (server.c:211)
==22756==
==22756== 456 bytes in 1 blocks are definitely lost in loss record 17 of 26
==22756==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22756==    by 0x4CBDE57: fi_thread_init (fault_injection.c:194)
==22756==    by 0x4C86553: thread_initialize_entry (thread.c:1228)
==22756==    by 0x4C837A3: thread_initialize_manager (thread.c:413)
==22756==    by 0x4E1C458: boot_restart_server (boot_sr.c:2825)
==22756==    by 0x4D11060: net_server_start (network_sr.c:1050)
==22756==    by 0x401DB2: main (server.c:211)
==22756==
==22756== 912 bytes in 2 blocks are possibly lost in loss record 23 of 26
==22756==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22756==    by 0x4CBDE57: fi_thread_init (fault_injection.c:194)
==22756==    by 0x4C86553: thread_initialize_entry (thread.c:1228)
==22756==    by 0x4C8386E: thread_initialize_manager (thread.c:431)
==22756==    by 0x4D10DD3: net_server_start (network_sr.c:1020)
==22756==    by 0x401DB2: main (server.c:211)
==22756==
==22756== 64,752 bytes in 142 blocks are definitely lost in loss record 25 of 26
==22756==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22756==    by 0x4CBDE57: fi_thread_init (fault_injection.c:194)
==22756==    by 0x4C86553: thread_initialize_entry (thread.c:1228)
==22756==    by 0x4C8386E: thread_initialize_manager (thread.c:431)
==22756==    by 0x4E1C458: boot_restart_server (boot_sr.c:2825)
==22756==    by 0x4D11060: net_server_start (network_sr.c:1050)
==22756==    by 0x401DB2: main (server.c:211)
==22756==
==22756== 4,574,592 bytes in 10,032 blocks are definitely lost in loss record 26 of 26
==22756==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22756==    by 0x4CBDE57: fi_thread_init (fault_injection.c:194)
==22756==    by 0x4C86553: thread_initialize_entry (thread.c:1228)
==22756==    by 0x4C8386E: thread_initialize_manager (thread.c:431)
==22756==    by 0x4D10DD3: net_server_start (network_sr.c:1020)
==22756==    by 0x401DB2: main (server.c:211)
==22756==
==22756== LEAK SUMMARY:
==22756==    definitely lost: 4,640,320 bytes in 10,177 blocks
==22756==    indirectly lost: 0 bytes in 0 blocks
==22756==      possibly lost: 912 bytes in 2 blocks
==22756==    still reachable: 68,310 bytes in 1,201 blocks
==22756==         suppressed: 0 bytes in 0 blocks
==22756== Reachable blocks (those to which a pointer was found) are not shown.
==22756== To see them, rerun with: --leak-check=full --show-reachable=yes
==22756==
==22756== For counts of detected and suppressed errors, rerun with: -v
==22756== Use --track-origins=yes to see where uninitialised values come from
==22756== ERROR SUMMARY: 10000006 errors from 64 contexts (suppressed: 6 from 6)
​
​
rye_repl​
​
==22910== Thread 1:
==22910== 16 bytes in 1 blocks are definitely lost in loss record 5 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD6409: er_vsprintf (error_manager.c:3116)
==22910==    by 0x4CD1CE1: er_set_internal (error_manager.c:1367)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x406E5E: cirp_change_state (repl_analyzer.c:402)
==22910==    by 0x40C1AF: analyzer_main (repl_analyzer.c:1785)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 26 (16 direct, 10 indirect) bytes in 1 blocks are definitely lost in loss record 8 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4F43E12: db_ws_alloc (quick_fit.c:72)
==22910==    by 0x4F09E04: obj_alloc (object_accessor.c:1172)
==22910==    by 0x4F44CDF: get_current (transform_cl.c:553)
==22910==    by 0x4F45369: tf_disk_to_mem (transform_cl.c:979)
==22910==    by 0x4F6D384: locator_cache_object_instance (locator_cl.c:1990)
==22910==    by 0x4F6D99E: locator_cache_have_object (locator_cl.c:2141)
==22910==    by 0x4F6DB4D: locator_cache (locator_cl.c:2208)
==22910==    by 0x4F6C92B: locator_fun_get_all_mops (locator_cl.c:1536)
==22910==    by 0x4F6CAC1: locator_get_all_mops (locator_cl.c:1573)
==22910==    by 0x4F1A87A: sm_fetch_all_objects (schema_manager.c:722)
==22910==    by 0x4F007C9: au_start (authenticate.c:3501)
==22910==    by 0x4F61E04: boot_restart_client (boot_cl.c:1025)
==22910==    by 0x4CA7797: db_restart (db_admin.c:610)
==22910==    by 0x432211: cirp_connect_copylogdb (repl.c:916)
==22910==    by 0x42F355: main (repl.c:233)
==22910==
==22910== 32 bytes in 1 blocks are definitely lost in loss record 10 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD6409: er_vsprintf (error_manager.c:3116)
==22910==    by 0x4CD1CE1: er_set_internal (error_manager.c:1367)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x4D1AE37: css_client_init (client_support.c:150)
==22910==    by 0x4D31DC2: net_client_init (network_cl.c:1719)
==22910==    by 0x4F62C37: boot_client_initialize_css (boot_cl.c:1383)
==22910==    by 0x4F6180E: boot_restart_client (boot_cl.c:905)
==22910==    by 0x4CA7797: db_restart (db_admin.c:610)
==22910==    by 0x432211: cirp_connect_copylogdb (repl.c:916)
==22910==    by 0x41BF2B: log_copier_main (repl_writer.c:1767)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 48 bytes in 1 blocks are definitely lost in loss record 17 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD6409: er_vsprintf (error_manager.c:3116)
==22910==    by 0x4CD1CE1: er_set_internal (error_manager.c:1367)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x41ADBC: cirpwr_archive_active_log (repl_writer.c:1478)
==22910==    by 0x41B427: cirpwr_write_log_pages (repl_writer.c:1578)
==22910==    by 0x41DC42: net_client_cirpwr_get_next_log_pages (repl_writer.c:2371)
==22910==    by 0x41C935: log_writer_main (repl_writer.c:1940)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 64 bytes in 1 blocks are definitely lost in loss record 20 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4D1F125: hb_thread_master_reader (heartbeat.c:214)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 67 (48 direct, 19 indirect) bytes in 2 blocks are definitely lost in loss record 21 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4F43E12: db_ws_alloc (quick_fit.c:72)
==22910==    by 0x4F09E04: obj_alloc (object_accessor.c:1172)
==22910==    by 0x4F44CDF: get_current (transform_cl.c:553)
==22910==    by 0x4F45369: tf_disk_to_mem (transform_cl.c:979)
==22910==    by 0x4F6D384: locator_cache_object_instance (locator_cl.c:1990)
==22910==    by 0x4F6D99E: locator_cache_have_object (locator_cl.c:2141)
==22910==    by 0x4F6DB4D: locator_cache (locator_cl.c:2208)
==22910==    by 0x4F6A8A1: locator_lock (locator_cl.c:669)
==22910==    by 0x4F6BECC: locator_fetch_instance (locator_cl.c:1265)
==22910==    by 0x4EFF862: fetch_instance (authenticate.c:3072)
==22910==    by 0x4EFFCA0: au_fetch_instance_force (authenticate.c:3188)
==22910==    by 0x4F0A870: find_unique (object_accessor.c:1536)
==22910==    by 0x4F0ABCF: obj_find_unique (object_accessor.c:1647)
==22910==    by 0x4EFA8BE: au_find_user (authenticate.c:1111)
==22910==    by 0x4F008BF: au_start (authenticate.c:3523)
==22910==    by 0x4F61E04: boot_restart_client (boot_cl.c:1025)
==22910==    by 0x4CA7797: db_restart (db_admin.c:610)
==22910==    by 0x432211: cirp_connect_copylogdb (repl.c:916)
==22910==    by 0x42F355: main (repl.c:233)
==22910==
==22910== 98 bytes in 1 blocks are definitely lost in loss record 23 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD60FC: er_make_room (error_manager.c:3032)
==22910==    by 0x4CD1C9F: er_set_internal (error_manager.c:1360)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x406E5E: cirp_change_state (repl_analyzer.c:402)
==22910==    by 0x40C1AF: analyzer_main (repl_analyzer.c:1785)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 113 bytes in 1 blocks are definitely lost in loss record 26 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD60FC: er_make_room (error_manager.c:3032)
==22910==    by 0x4CD1C9F: er_set_internal (error_manager.c:1360)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x4F63215: boot_client_initialize_css (boot_cl.c:1460)
==22910==    by 0x4F6180E: boot_restart_client (boot_cl.c:905)
==22910==    by 0x4CA7797: db_restart (db_admin.c:610)
==22910==    by 0x432211: cirp_connect_copylogdb (repl.c:916)
==22910==    by 0x41BF2B: log_copier_main (repl_writer.c:1767)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 125 bytes in 1 blocks are definitely lost in loss record 29 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD60FC: er_make_room (error_manager.c:3032)
==22910==    by 0x4CD1C9F: er_set_internal (error_manager.c:1360)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x41ADBC: cirpwr_archive_active_log (repl_writer.c:1478)
==22910==    by 0x41B427: cirpwr_write_log_pages (repl_writer.c:1578)
==22910==    by 0x41DC42: net_client_cirpwr_get_next_log_pages (repl_writer.c:2371)
==22910==    by 0x41C935: log_writer_main (repl_writer.c:1940)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 128 bytes in 8 blocks are definitely lost in loss record 30 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD6409: er_vsprintf (error_manager.c:3116)
==22910==    by 0x4CD1CE1: er_set_internal (error_manager.c:1367)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x4152F0: applier_main (repl_applier.c:1874)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 288 bytes in 1 blocks are possibly lost in loss record 35 of 53
==22910==    at 0x4A057BB: calloc (vg_replace_malloc.c:593)
==22910==    by 0x3FFF411952: _dl_allocate_tls (in /lib64/ld-2.12.so)
==22910==    by 0x30000071E8: pthread_create@@GLIBC_2.2.5 (in /lib64/libpthread-2.12.so)
==22910==    by 0x5459EB2: hm_create_health_check_th (cci_handle_mng.c:775)
==22910==    by 0x5439B9D: cci_connect_internal (cas_cci.c:335)
==22910==    by 0x543A0C1: cci_connect (cas_cci.c:406)
==22910==    by 0x4312B5: cirp_get_cci_connection (repl.c:714)
==22910==    by 0x42F429: main (repl.c:240)
==22910==
==22910== 336 bytes in 8 blocks are definitely lost in loss record 38 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4CD60FC: er_make_room (error_manager.c:3032)
==22910==    by 0x4CD1C9F: er_set_internal (error_manager.c:1360)
==22910==    by 0x4CD111C: er_set (error_manager.c:1084)
==22910==    by 0x4152F0: applier_main (repl_applier.c:1874)
==22910==    by 0x30000079D0: start_thread (in /lib64/libpthread-2.12.so)
==22910==    by 0x3FFFCE88FC: clone (in /lib64/libc-2.12.so)
==22910==
==22910== 16,685 (1,920 direct, 14,765 indirect) bytes in 10 blocks are definitely lost in loss record 52 of 53
==22910==    at 0x4A06A2E: malloc (vg_replace_malloc.c:270)
==22910==    by 0x4F43E12: db_ws_alloc (quick_fit.c:72)
==22910==    by 0x4F18858: classobj_make_class (class_object.c:2788)
==22910==    by 0x4F49D29: disk_to_class (transform_cl.c:2851)
==22910==    by 0x4F4ABF2: tf_disk_to_class (transform_cl.c:3112)
==22910==    by 0x4F6D13B: locator_cache_object_class (locator_cl.c:1906)
==22910==    by 0x4F6D6B5: locator_cache_have_object (locator_cl.c:2078)
==22910==    by 0x4F6DB4D: locator_cache (locator_cl.c:2208)
==22910==    by 0x4F6A8A1: locator_lock (locator_cl.c:669)
==22910==    by 0x4F6CD6A: locator_find_class_by_oid (locator_cl.c:1767)
==22910==    by 0x4F6CF07: locator_find_class (locator_cl.c:1832)
==22910==    by 0x4F1C2A1: sm_find_class (schema_manager.c:1894)
==22910==    by 0x4F00614: au_start (authenticate.c:3469)
==22910==    by 0x4F61E04: boot_restart_client (boot_cl.c:1025)
==22910==    by 0x4CA7797: db_restart (db_admin.c:610)
==22910==    by 0x432211: cirp_connect_copylogdb (repl.c:916)
==22910==    by 0x42F355: main (repl.c:233)
==22910==
==22910== LEAK SUMMARY:
==22910==    definitely lost: 2,944 bytes in 36 blocks
==22910==    indirectly lost: 14,794 bytes in 182 blocks
==22910==      possibly lost: 288 bytes in 1 blocks
==22910==    still reachable: 92,952 bytes in 1,217 blocks
==22910==         suppressed: 0 bytes in 0 blocks
==22910== Reachable blocks (those to which a pointer was found) are not shown.
==22910== To see them, rerun with: --leak-check=full --show-reachable=yes
==22910==
==22910== For counts of detected and suppressed errors, rerun with: -v
==22910== Use --track-origins=yes to see where uninitialised values come from
==22910== ERROR SUMMARY: 470934 errors from 17 contexts (suppressed: 6 from 6)
​
​```
