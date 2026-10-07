# ext/snmp: Attempted free on non-malloced address

- URL: https://github.com/php/php-src/issues/23453
- Repo: php/php-src (language: C)
- State: closed; created 2026-08-25T12:20:35Z; status ok; passes main

## Issue body

reporter (MEMBER) · alexandre-daubois · 2026-08-25T12:20:35Z · https://github.com/php/php-src/issues/23453

### Description

Originally reported by @TristanInSec

The following code:

```c
$session = new SNMP(SNMP::VERSION_3, 'localhost', 'user');
$session->setSecurity(
    'authPriv', 'SHA', 'authpassword12345', 'AES', 'privpassword12345',
    'myContext', str_repeat('aa', 33)  // 66 hex chars = 33 bytes > 32-byte buffer
);
```

Produces an ASan error:

```
=================================================================
==41704==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x00010c64d440 in thread T0
    #0 0x000104fb5350 in realloc+0x80 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x41350)
    #1 0x000104855348 in snmp_realloc+0x4c (libnetsnmp.45.dylib:arm64+0x29348)
    #2 0x000104855b38 in netsnmp_hex_to_binary+0xf8 (libnetsnmp.45.dylib:arm64+0x29b38)
    #3 0x0001030f8ebc in snmp_session_set_security snmp.c:1210
    #4 0x0001030f87cc in zim_SNMP_setSecurity snmp.c:1751
    #5 0x000103703830 in ZEND_DO_FCALL_SPEC_RETVAL_UNUSED_TAILCALL_HANDLER zend_vm_execute.h
    #6 0x00010355b034 in execute_ex zend_vm_execute.h:110551
    #7 0x00010355b790 in zend_execute zend_vm_execute.h:115989
    #8 0x00010390a280 in zend_execute_script zend.c:1980
    #9 0x00010331c58c in php_execute_script_ex main.c:2589
    #10 0x00010390f664 in do_cli php_cli.c:933
    #11 0x00010390d08c in do_php_cli php_cli.c:1346
    #12 0x000189c884e0 in start+0x1b4c (dyld:arm64e+0x204e0)

Address 0x00010c64d440 is a wild pointer inside of access range of size 0x000000000001.
SUMMARY: AddressSanitizer: bad-free (libnetsnmp.45.dylib:arm64+0x29348) in snmp_realloc+0x4c
==41704==ABORTING
```

`contextEngineID` is a `SnmpEngineID` type as defined by [RFC 3411](https://datatracker.ietf.org/doc/html/rfc3411#section-5), and its length must be between 5 and 32 bytes. We should process the value gracefully.

### PHP Version

```plain
All maintained versions
```

### Operating System

_No response_
