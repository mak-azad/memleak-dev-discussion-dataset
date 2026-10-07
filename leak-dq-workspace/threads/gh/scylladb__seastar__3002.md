# tls_test: LeakSanitizer: detected memory leaks

- URL: https://github.com/scylladb/seastar/issues/3002
- Repo: scylladb/seastar (language: C++)
- State: open; created 2025-09-30T13:35:00Z; status ok; passes main

## Issue body

reporter (MEMBER) · bhalevy · 2025-09-30T13:35:00Z · https://github.com/scylladb/seastar/issues/3002

Found using `ctest --test-dir build/debug --output-on-failure -j2`
In a branch off of 5446cbab

```
83/83 Test #68: Seastar.unit.tls ..............................***Failed   78.07 sec
[0/1] cd /home/bhalevy/dev/seastar/build/debug && /usr/bin/cmake -E env ASAN_OPTIONS=disable_coredump=0:abort_on_error=1:detect_stack_use_after_return=1 UBSAN_OPTIONS=halt_on_error=1:abort_on_error=1 BOOST_TEST_CATCH_SYSTEM_ERRORS=no /home/bhalevy/dev/seastar/build/debug/tests/unit/tls_test -- -c 2
Running 46 test cases...
INFO  2025-09-30 16:30:39,628 seastar - Reactor backend: linux-aio
INFO  2025-09-30 16:30:39,628 seastar - Perf-based stall detector creation failed (EACCESS), try setting /proc/sys/kernel/perf_event_paranoid to 1 or less to enable kernel backtraces: falling back to posix timer.
INFO  2025-09-30 16:30:39,630 [shard 0:main] seastar - IO queue was unable to find a suitable maximum request length, the search was cut-off early at: 16MB
INFO  2025-09-30 16:30:39,630 [shard 0:main] seastar - IO queue was unable to find a suitable maximum request length, the search was cut-off early at: 16MB
random-seed=1990572726
==1992587==WARNING: ASan doesn't fully support makecontext/swapcontext functions and may produce false positives in some cases!
Reactor stalled for 133 ms on shard 0, in scheduling group main. Backtrace: 0x44dde9 0x99728a 0x996505 0x7a13f1 0x79ba4b 0x79b377 0x79bff9 0x7a3124 0x1a06f 0x7be530a0d8d0 0x7be530a0f8ad 0x7be530a1180a 0x7be530a1a27f 0x7be530a1acff 0x7be530a1b3bb 0x7be530a15484 0x7be530a17596 0x7be530a22997 0x7be530a22b61 0x7be530a2311a 0x7be530a1b90e 0xeed8 0x80f07 0x82d18 0x83b5a 0x83ca6 0x11be43 0x425a0 0x12f2a82 0x12f29ec 0x12f298c 0x12f2930 0x12f28d2 0x12f2801 0x12f26c5 0x12f2504 0x7927ef 0xc6ccd2
Reactor stalled for 34 ms on shard 0, in scheduling group main. Backtrace: 0x44dde9 0x99728a 0x996505 0x7a13f1 0x79ba4b 0x79b377 0x79bff9 0x7a3124 0x1a06f 0x4d8548 0x4b4ed0 0x4a839b 0x7be530a16d7c 0x7be530a1bf79 0x7be530a1fbb7 0x7be530a14f66 0x7dee 0x82d2c 0x85207 0x108ed8 0x11ae56 0x60d5a 0x618cd 0x1349eaf 0x13faf13 0x16ae2 0xe71c 0x1adcd 0x1348e83 0x134bf61 0x134be6f 0x134bdff 0x134bd93 0x134bcf7 0x68fbf2 0x68fab2 0x68fa42 0x68f9d2 0x68f956 0x68f8de 0x68f6f2 0x68f505 0x68ef5a 0x7d6145 0x7e2bfc 0x7e23c3 0x7e792f 0x7e5b76 0x2fc275 0x2f9720 0x1a763 0x1a12c 0x1a02c 0x19b14 0x35b48d 0x5a6cf4 0x4a5f0a 0x71f53 0xf532b
Established connection
Killing server side
Got expected exception

*** No errors detected

=================================================================
==1992587==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 184 byte(s) in 1 object(s) allocated from:
    #0 0x0000004a85e8 in malloc (/home/bhalevy/dev/seastar/build/debug/tests/unit/tls_test+0x4a85e8) (BuildId: f804e03165e1cd7d121bd87c4a4c7e437b56ea13)
    #1 0x7be530a034a4 in SCardEstablishContext (/lib64/libpcsclite_real.so.1+0x24a4) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #2 0x7be52c95a234  (/lib64/libopensc.so.12+0x43234) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #3 0x7be52c91e12e in sc_ctx_detect_readers (/lib64/libopensc.so.12+0x712e) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #4 0x7be52c9241e8 in sc_context_create (/lib64/libopensc.so.12+0xd1e8) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #5 0x7be52f6854f5 in C_Initialize (/usr/lib64/pkcs11/opensc-pkcs11.so+0xd4f5) (BuildId: 658355f52551bfe6042a53376fd473665bbada0e)
    #6 0x7fe531aa9719  (/lib64/libp11-kit.so.0+0x7719) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #7 0x7fe531aa98cf  (/lib64/libp11-kit.so.0+0x78cf) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #8 0x7fe531aae331 in p11_kit_modules_initialize (/lib64/libp11-kit.so.0+0xc331) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #9 0x7fe531aaeaef in p11_kit_modules_load_and_initialize (/lib64/libp11-kit.so.0+0xcaef) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #10 0x7fe53207c372  (/lib64/libgnutls.so.30+0x7c372) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #11 0x7fe53207debe in gnutls_pkcs11_init (/lib64/libgnutls.so.30+0x7debe) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #12 0x7fe53207e087  (/lib64/libgnutls.so.30+0x7e087) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #13 0x7fe5320858e2  (/lib64/libgnutls.so.30+0x858e2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #14 0x7fe532108eab  (/lib64/libgnutls.so.30+0x108eab) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #15 0x7fe53211ae56 in gnutls_x509_trust_list_verify_crt2 (/lib64/libgnutls.so.30+0x11ae56) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #16 0x7fe532060d5a  (/lib64/libgnutls.so.30+0x60d5a) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #17 0x7fe5320618cd in gnutls_certificate_verify_peers3 (/lib64/libgnutls.so.30+0x618cd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #18 0x7fe533d49eaf in seastar::tls::session::verify() /home/bhalevy/dev/seastar/src/net/tls.cc:1400:20
    #19 0x7fe533dfaf13 in seastar::tls::session::verify_wrapper(gnutls_session_int*) /home/bhalevy/dev/seastar/src/net/tls.cc:1380:63
    #20 0x7fe532016ae2  (/lib64/libgnutls.so.30+0x16ae2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #21 0x7fe53200e71c  (/lib64/libgnutls.so.30+0xe71c) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #22 0x7fe53201adcd in gnutls_handshake (/lib64/libgnutls.so.30+0x1adcd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #23 0x7fe533d48e83 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*)) /home/bhalevy/dev/seastar/src/net/tls.cc:1253:24
    #24 0x7fe533d4bf61 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()::operator()() const /home/bhalevy/dev/seastar/src/net/tls.cc:1268:36
    #25 0x7fe533d4be6f in seastar::future<void> seastar::futurize<seastar::future<void>>::invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1960:20
    #26 0x7fe533d4bdff in auto seastar::futurize_invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1991:12
    #27 0x7fe533d4bd93 in auto seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)::operator()<>(auto&&...) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1369:24
    #28 0x7fe533d4bcf7 in seastar::noncopyable_function<seastar::future<void> ()>::direct_vtable_for<seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)>::call(seastar::noncopyable_function<seastar::future<void> ()> const*) /home/bhalevy/dev/seastar/include/seastar/util/noncopyable_function.hh:138:20
    #29 0x00000068fbf2 in seastar::noncopyable_function<seastar::future<void> ()>::operator()() const /home/bhalevy/dev/seastar/include/seastar/util/noncopyable_function.hh:224:16

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x0000004a85e8 in malloc (/home/bhalevy/dev/seastar/build/debug/tests/unit/tls_test+0x4a85e8) (BuildId: f804e03165e1cd7d121bd87c4a4c7e437b56ea13)
    #1 0x7be530a02b33  (/lib64/libpcsclite_real.so.1+0x1b33) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #2 0x7be530a0350c in SCardEstablishContext (/lib64/libpcsclite_real.so.1+0x250c) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #3 0x7be52c95a234  (/lib64/libopensc.so.12+0x43234) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #4 0x7be52c91e12e in sc_ctx_detect_readers (/lib64/libopensc.so.12+0x712e) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #5 0x7be52c9241e8 in sc_context_create (/lib64/libopensc.so.12+0xd1e8) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #6 0x7be52f6854f5 in C_Initialize (/usr/lib64/pkcs11/opensc-pkcs11.so+0xd4f5) (BuildId: 658355f52551bfe6042a53376fd473665bbada0e)
    #7 0x7fe531aa9719  (/lib64/libp11-kit.so.0+0x7719) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #8 0x7fe531aa98cf  (/lib64/libp11-kit.so.0+0x78cf) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #9 0x7fe531aae331 in p11_kit_modules_initialize (/lib64/libp11-kit.so.0+0xc331) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #10 0x7fe531aaeaef in p11_kit_modules_load_and_initialize (/lib64/libp11-kit.so.0+0xcaef) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #11 0x7fe53207c372  (/lib64/libgnutls.so.30+0x7c372) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #12 0x7fe53207debe in gnutls_pkcs11_init (/lib64/libgnutls.so.30+0x7debe) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #13 0x7fe53207e087  (/lib64/libgnutls.so.30+0x7e087) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #14 0x7fe5320858e2  (/lib64/libgnutls.so.30+0x858e2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #15 0x7fe532108eab  (/lib64/libgnutls.so.30+0x108eab) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #16 0x7fe53211ae56 in gnutls_x509_trust_list_verify_crt2 (/lib64/libgnutls.so.30+0x11ae56) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #17 0x7fe532060d5a  (/lib64/libgnutls.so.30+0x60d5a) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #18 0x7fe5320618cd in gnutls_certificate_verify_peers3 (/lib64/libgnutls.so.30+0x618cd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #19 0x7fe533d49eaf in seastar::tls::session::verify() /home/bhalevy/dev/seastar/src/net/tls.cc:1400:20
    #20 0x7fe533dfaf13 in seastar::tls::session::verify_wrapper(gnutls_session_int*) /home/bhalevy/dev/seastar/src/net/tls.cc:1380:63
    #21 0x7fe532016ae2  (/lib64/libgnutls.so.30+0x16ae2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #22 0x7fe53200e71c  (/lib64/libgnutls.so.30+0xe71c) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #23 0x7fe53201adcd in gnutls_handshake (/lib64/libgnutls.so.30+0x1adcd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #24 0x7fe533d48e83 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*)) /home/bhalevy/dev/seastar/src/net/tls.cc:1253:24
    #25 0x7fe533d4bf61 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()::operator()() const /home/bhalevy/dev/seastar/src/net/tls.cc:1268:36
    #26 0x7fe533d4be6f in seastar::future<void> seastar::futurize<seastar::future<void>>::invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1960:20
    #27 0x7fe533d4bdff in auto seastar::futurize_invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1991:12
    #28 0x7fe533d4bd93 in auto seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)::operator()<>(auto&&...) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1369:24
    #29 0x7fe533d4bcf7 in seastar::noncopyable_function<seastar::future<void> ()>::direct_vtable_for<seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)>::call(seastar::noncopyable_function<seastar::future<void> ()> const*) /home/bhalevy/dev/seastar/include/seastar/util/noncopyable_function.hh:138:20

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0000004a85e8 in malloc (/home/bhalevy/dev/seastar/build/debug/tests/unit/tls_test+0x4a85e8) (BuildId: f804e03165e1cd7d121bd87c4a4c7e437b56ea13)
    #1 0x7be530a02afa  (/lib64/libpcsclite_real.so.1+0x1afa) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #2 0x7be530a0350c in SCardEstablishContext (/lib64/libpcsclite_real.so.1+0x250c) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #3 0x7be52c95a234  (/lib64/libopensc.so.12+0x43234) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #4 0x7be52c91e12e in sc_ctx_detect_readers (/lib64/libopensc.so.12+0x712e) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #5 0x7be52c9241e8 in sc_context_create (/lib64/libopensc.so.12+0xd1e8) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #6 0x7be52f6854f5 in C_Initialize (/usr/lib64/pkcs11/opensc-pkcs11.so+0xd4f5) (BuildId: 658355f52551bfe6042a53376fd473665bbada0e)
    #7 0x7fe531aa9719  (/lib64/libp11-kit.so.0+0x7719) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #8 0x7fe531aa98cf  (/lib64/libp11-kit.so.0+0x78cf) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #9 0x7fe531aae331 in p11_kit_modules_initialize (/lib64/libp11-kit.so.0+0xc331) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #10 0x7fe531aaeaef in p11_kit_modules_load_and_initialize (/lib64/libp11-kit.so.0+0xcaef) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #11 0x7fe53207c372  (/lib64/libgnutls.so.30+0x7c372) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #12 0x7fe53207debe in gnutls_pkcs11_init (/lib64/libgnutls.so.30+0x7debe) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #13 0x7fe53207e087  (/lib64/libgnutls.so.30+0x7e087) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #14 0x7fe5320858e2  (/lib64/libgnutls.so.30+0x858e2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #15 0x7fe532108eab  (/lib64/libgnutls.so.30+0x108eab) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #16 0x7fe53211ae56 in gnutls_x509_trust_list_verify_crt2 (/lib64/libgnutls.so.30+0x11ae56) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #17 0x7fe532060d5a  (/lib64/libgnutls.so.30+0x60d5a) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #18 0x7fe5320618cd in gnutls_certificate_verify_peers3 (/lib64/libgnutls.so.30+0x618cd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #19 0x7fe533d49eaf in seastar::tls::session::verify() /home/bhalevy/dev/seastar/src/net/tls.cc:1400:20
    #20 0x7fe533dfaf13 in seastar::tls::session::verify_wrapper(gnutls_session_int*) /home/bhalevy/dev/seastar/src/net/tls.cc:1380:63
    #21 0x7fe532016ae2  (/lib64/libgnutls.so.30+0x16ae2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #22 0x7fe53200e71c  (/lib64/libgnutls.so.30+0xe71c) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #23 0x7fe53201adcd in gnutls_handshake (/lib64/libgnutls.so.30+0x1adcd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #24 0x7fe533d48e83 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*)) /home/bhalevy/dev/seastar/src/net/tls.cc:1253:24
    #25 0x7fe533d4bf61 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()::operator()() const /home/bhalevy/dev/seastar/src/net/tls.cc:1268:36
    #26 0x7fe533d4be6f in seastar::future<void> seastar::futurize<seastar::future<void>>::invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1960:20
    #27 0x7fe533d4bdff in auto seastar::futurize_invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1991:12
    #28 0x7fe533d4bd93 in auto seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)::operator()<>(auto&&...) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1369:24
    #29 0x7fe533d4bcf7 in seastar::noncopyable_function<seastar::future<void> ()>::direct_vtable_for<seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)>::call(seastar::noncopyable_function<seastar::future<void> ()> const*) /home/bhalevy/dev/seastar/include/seastar/util/noncopyable_function.hh:138:20

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x0000004a85e8 in malloc (/home/bhalevy/dev/seastar/build/debug/tests/unit/tls_test+0x4a85e8) (BuildId: f804e03165e1cd7d121bd87c4a4c7e437b56ea13)
    #1 0x7be530a02aea  (/lib64/libpcsclite_real.so.1+0x1aea) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #2 0x7be530a0350c in SCardEstablishContext (/lib64/libpcsclite_real.so.1+0x250c) (BuildId: cbb69c952fb918cb6adb21577a026d80b63a46f2)
    #3 0x7be52c95a234  (/lib64/libopensc.so.12+0x43234) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #4 0x7be52c91e12e in sc_ctx_detect_readers (/lib64/libopensc.so.12+0x712e) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #5 0x7be52c9241e8 in sc_context_create (/lib64/libopensc.so.12+0xd1e8) (BuildId: f9339e9b8d93e821fa15b6ca175151fa312e542c)
    #6 0x7be52f6854f5 in C_Initialize (/usr/lib64/pkcs11/opensc-pkcs11.so+0xd4f5) (BuildId: 658355f52551bfe6042a53376fd473665bbada0e)
    #7 0x7fe531aa9719  (/lib64/libp11-kit.so.0+0x7719) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #8 0x7fe531aa98cf  (/lib64/libp11-kit.so.0+0x78cf) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #9 0x7fe531aae331 in p11_kit_modules_initialize (/lib64/libp11-kit.so.0+0xc331) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #10 0x7fe531aaeaef in p11_kit_modules_load_and_initialize (/lib64/libp11-kit.so.0+0xcaef) (BuildId: 12074fc0e3b0d977d8b254b19280bb629a79c5f2)
    #11 0x7fe53207c372  (/lib64/libgnutls.so.30+0x7c372) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #12 0x7fe53207debe in gnutls_pkcs11_init (/lib64/libgnutls.so.30+0x7debe) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #13 0x7fe53207e087  (/lib64/libgnutls.so.30+0x7e087) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #14 0x7fe5320858e2  (/lib64/libgnutls.so.30+0x858e2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #15 0x7fe532108eab  (/lib64/libgnutls.so.30+0x108eab) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #16 0x7fe53211ae56 in gnutls_x509_trust_list_verify_crt2 (/lib64/libgnutls.so.30+0x11ae56) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #17 0x7fe532060d5a  (/lib64/libgnutls.so.30+0x60d5a) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #18 0x7fe5320618cd in gnutls_certificate_verify_peers3 (/lib64/libgnutls.so.30+0x618cd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #19 0x7fe533d49eaf in seastar::tls::session::verify() /home/bhalevy/dev/seastar/src/net/tls.cc:1400:20
    #20 0x7fe533dfaf13 in seastar::tls::session::verify_wrapper(gnutls_session_int*) /home/bhalevy/dev/seastar/src/net/tls.cc:1380:63
    #21 0x7fe532016ae2  (/lib64/libgnutls.so.30+0x16ae2) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #22 0x7fe53200e71c  (/lib64/libgnutls.so.30+0xe71c) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #23 0x7fe53201adcd in gnutls_handshake (/lib64/libgnutls.so.30+0x1adcd) (BuildId: e0496c86e1ffb3b4b8ed15dc2fa44da980dee42f)
    #24 0x7fe533d48e83 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*)) /home/bhalevy/dev/seastar/src/net/tls.cc:1253:24
    #25 0x7fe533d4bf61 in seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()::operator()() const /home/bhalevy/dev/seastar/src/net/tls.cc:1268:36
    #26 0x7fe533d4be6f in seastar::future<void> seastar::futurize<seastar::future<void>>::invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1960:20
    #27 0x7fe533d4bdff in auto seastar::futurize_invoke<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&>(seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'()&) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1991:12
    #28 0x7fe533d4bd93 in auto seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)::operator()<>(auto&&...) /home/bhalevy/dev/seastar/include/seastar/core/future.hh:1369:24
    #29 0x7fe533d4bcf7 in seastar::noncopyable_function<seastar::future<void> ()>::direct_vtable_for<seastar::future<void> seastar::future<void>::then<seastar::tls::session::do_handshake_invoke(int (*)(gnutls_session_int*))::'lambda'()::operator()() const::'lambda'(), seastar::future<void>>(T&&)::'lambda'(auto&&...)>::call(seastar::noncopyable_function<seastar::future<void> ()> const*) /home/bhalevy/dev/seastar/include/seastar/util/noncopyable_function.hh:138:20

SUMMARY: AddressSanitizer: 272 byte(s) leaked in 4 allocation(s).
Subprocess aborted
FAILED: tests/unit/CMakeFiles/test_unit_tls_run /home/bhalevy/dev/seastar/build/debug/tests/unit/CMakeFiles/test_unit_tls_run 
cd /home/bhalevy/dev/seastar/build/debug && /usr/bin/cmake -E env ASAN_OPTIONS=disable_coredump=0:abort_on_error=1:detect_stack_use_after_return=1 UBSAN_OPTIONS=halt_on_error=1:abort_on_error=1 BOOST_TEST_CATCH_SYSTEM_ERRORS=no /home/bhalevy/dev/seastar/build/debug/tests/unit/tls_test -- -c 2
ninja: build stopped: subcommand failed.


99% tests passed, 1 tests failed out of 83

Total Test time (real) = 171.27 sec

The following tests FAILED:
         68 - Seastar.unit.tls (Failed)
Errors while running CTest
```


## Comment 3352207902

reporter (MEMBER) · bhalevy · 2025-09-30T13:35:35Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3352207902

@elcallio please look into this

## Comment 3352745903

other (CONTRIBUTOR) · elcallio · 2025-09-30T15:27:26Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3352745903

Cannot reproduce on seastar master (which includes the above mentioned patch)

## Comment 3352989386

reporter (MEMBER) · bhalevy · 2025-09-30T16:37:09Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3352989386

> Cannot reproduce on seastar master (which includes the above mentioned patch)

Hmm, I've just reproduced locally at change 9c07020a.
```
./configure.py --compiler=clang++ --c++-standard=23

clang version 20.1.8 (Fedora 20.1.8-4.fc42)
```


## Comment 3353000895

reporter (MEMBER) · bhalevy · 2025-09-30T16:40:51Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3353000895

The leaks seem to come from the libraries: `/lib64/libgnutls -> /lib64/libp11-kit -> /lib64/libopensc` 
So the question is if we need to do something on our side to delete those resources?

## Comment 3353061065

other (CONTRIBUTOR) · elcallio · 2025-09-30T17:00:07Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3353061065

No repro for me at same hash. Same fedora 42 + clang 20.1.8. Any quirks about your TLS setup on the machine? 

I very much doubt there is anything on our end. You could try to pinpoint which of the test cases causes the alert on your machine. I am guessing/hoping it is a module-wide allocation, not a context one...

## Comment 3355045847

reporter (MEMBER) · bhalevy · 2025-10-01T07:14:51Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3355045847

I rebuilt from scratch and ran each test case independently using:
```
$ for in in `build/debug/tests/unit/tls_test --list_content |& sed 's/\*$//'`; do build/debug/tests/unit/tls_test -t $i -- -c 2 >& /tmp/$i.out; done
```

```
bhalevy@ws seastar$ grep Leak /tmp/*.out
/tmp/test_alpn_client_negotiate_h2_with_google.out:==2061919==ERROR: LeakSanitizer: detected memory leaks
/tmp/test_tls_cipher_suite_and_protocol_version.out:==2062212==ERROR: LeakSanitizer: detected memory leaks
/tmp/test_x509_client_with_builder_system_trust_multiple.out:==2061856==ERROR: LeakSanitizer: detected memory leaks
/tmp/test_x509_client_with_builder_system_trust.out:==2061837==ERROR: LeakSanitizer: detected memory leaks
/tmp/test_x509_client_with_system_trust_and_priority_strings.out:==2061868==ERROR: LeakSanitizer: detected memory leaks
/tmp/test_x509_client_with_system_trust.out:==2061816==ERROR: LeakSanitizer: detected memory leaks
```

[leaks.tar.gz](https://github.com/user-attachments/files/22632625/leaks.tar.gz)

## Comment 3370416924

other (CONTRIBUTOR) · elcallio · 2025-10-06T08:12:21Z · https://github.com/scylladb/seastar/issues/3002#issuecomment-3370416924

(Sorry, this comment was not sent last week:) So on your system, building the system trust chain results in a leak.
Next question; If you run the test with _two_ of the leak inducing cases, do you still only get one leak? If so, this is a module-level quirk on your system.
