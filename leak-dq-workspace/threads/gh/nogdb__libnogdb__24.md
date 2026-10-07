# Aborting in some SQL operation tests with AddressSanitizer on Travis

- URL: https://github.com/nogdb/libnogdb/issues/24
- Repo: nogdb/libnogdb (language: C++)
- State: open; created 2018-06-05T15:58:39Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · pj4dev · 2018-06-05T15:58:39Z · https://github.com/nogdb/libnogdb/issues/24

Environment:
=================================================================
- Linux on Travis (Ubuntu)
- g++ (Ubuntu 4.8.5-4ubuntu8~14.04.2) 4.8.5

Important error logs:
=================================================================
```
==5913==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete []) on 0x6030012980b0
    #0 0x2aaeba106990 in operator delete[](void*) (/usr/lib/x86_64-linux-gnu/libasan.so.3+0xc3990)
    #1 0x8e0a28 in std::enable_if<std::is_convertible<unsigned char (*) [], unsigned char (*) []>::value, void>::type std::default_delete<unsigned char []>::operator()<unsigned char>(unsigned char*) const (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8e0a28)
    #2 0x8df13e in std::unique_ptr<unsigned char [], std::default_delete<unsigned char []> >::~unique_ptr() (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8df13e)
    #3 0x8d8de5 in nogdb::sql_parser::Token::toBytes() const (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8d8de5)
    #4 0x8f93ea in (anonymous namespace)::yypParser::yy_reduce(unsigned int) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8f93ea)
    #5 0x8fad75 in (anonymous namespace)::yypParser::parse(int, nogdb::sql_parser::Token&&) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8fad75)
    #6 0x8dce7b in nogdb::SQL::execute(nogdb::Txn&, std::string const&) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8dce7b)
    #7 0x7bd29c in test_sql_validate_property_type() (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x7bd29c)
    #8 0x46f799 in exec(void (*)(), std::string const&) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x46f799)
    #9 0x4764e6 in main (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x4764e6)
    #10 0x2aaebbc59f44 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21f44)
    #11 0x407398  (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x407398)
0x6030012980b0 is located 0 bytes inside of 17-byte region [0x6030012980b0,0x6030012980c1)
allocated by thread T0 here:
    #0 0x2aaeba105348 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.3+0xc2348)
    #1 0x8d898d in HexToBlob(char const*, int) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8d898d)
    #2 0x8d8d94 in nogdb::sql_parser::Token::toBytes() const (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8d8d94)
    #3 0x8f93ea in (anonymous namespace)::yypParser::yy_reduce(unsigned int) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8f93ea)
    #4 0x8fad75 in (anonymous namespace)::yypParser::parse(int, nogdb::sql_parser::Token&&) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8fad75)
    #5 0x8dce7b in nogdb::SQL::execute(nogdb::Txn&, std::string const&) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x8dce7b)
    #6 0x7bd29c in test_sql_validate_property_type() (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x7bd29c)
    #7 0x46f799 in exec(void (*)(), std::string const&) (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x46f799)
    #8 0x4764e6 in main (/home/travis/build/nogdb/nogdb/runtest_debug_address+0x4764e6)
    #9 0x2aaebbc59f44 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21f44)
SUMMARY: AddressSanitizer: alloc-dealloc-mismatch (/usr/lib/x86_64-linux-gnu/libasan.so.3+0xc3990) in operator delete[](void*)
==5913==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==5913==ABORTING
```
