# AddressSanitizer: requested allocation size exceeds maximum supported size

- URL: https://github.com/jerryscript-project/jerryscript/issues/5072
- Repo: jerryscript-project/jerryscript (language: C)
- State: open; created 2023-04-19T11:58:01Z; status ok; passes main

## Issue body

reporter (NONE) · Ye0nny · 2023-04-19T11:58:01Z · https://github.com/jerryscript-project/jerryscript/issues/5072

###### JerryScript revision
Commit: https://github.com/jerryscript-project/jerryscript/commit/05dbbd134c3b9e2482998f267857dd3722001cd7
Version: v3.0.0

###### Build platform
Ubuntu 20.04.5 LTS (Linux 5.4.0-144-generic x86_64)

###### Build steps
```sh
python ./tools/build.py --clean --debug --compile-flag=-m32 --compile-flag=-fno-omit-frame-pointer --compile-flag=-fno-common --compile-flag=-fsanitize=address --compile-flag=-g --strip=off --lto=off --error-messages=on --system-allocator=on --logging=on --line-info=on --stack-limit=20
```

###### Test case
<details><summary>testcase</summary>
<p>

```javascript
function func0 ( n , r , t , u ) { if ( n < 0 ) { throw arguments ; } return n + r + t + u ; } function func1 ( n , r , t , u , f ) { return i ( n , r , t , u * f ) ; } function func2 ( n , r ) { return t ( n , ... r ) ; } var e = new Float32Array ( 1 * 1000000.0 * 1000.0 ) . reverse ( ) . filter ( r => r === - r . valueOf ) [ 0 ] ; function func3 ( ) { ; } function func4 ( n ) { return r ( n , n ) ; }
```
</p>
</details>

```javascript
// poc.js
var e = new Float32Array ( 1000000.0 * 1000.0 ) . reverse ( );
```

###### Execution steps & Output
```
$ ./jerryscript/build/bin/jerry poc.js
=================================================================
==2464945==ERROR: AddressSanitizer: requested allocation size 0xee6b2800 (0xee6b3800 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0xc0000000 (thread T0)
    #0 0x80efe65 in malloc (./jerryscript/build/bin/jerry+0x80efe65)
    #1 0x825f11c in jmem_heap_alloc ./jerryscript/jerry-core/jmem/jmem-heap.c:254:10
    #2 0x825f11c in jmem_heap_gc_and_alloc_block ./jerryscript/jerry-core/jmem/jmem-heap.c:291:24
    #3 0x81d5463 in ecma_arraybuffer_allocate_buffer ./jerryscript/jerry-core/ecma/operations/ecma-arraybuffer-object.c:169:28
    #4 0x81c47d1 in ecma_builtin_typedarray_prototype_dispatch_routine ./jerryscript/jerry-core/ecma/builtin-objects/typedarray/ecma-builtin-typedarray-prototype.c:1929:12
    #5 0x81b94a4 in ecma_builtin_dispatch_routine ./jerryscript/jerry-core/ecma/builtin-objects/ecma-builtins.c:1460:10
    #6 0x81b94a4 in ecma_builtin_dispatch_call ./jerryscript/jerry-core/ecma/builtin-objects/ecma-builtins.c:1489:12
    #7 0x81fb6b7 in ecma_op_function_call_native_built_in ./jerryscript/jerry-core/ecma/operations/ecma-function-object.c:1217:5
    #8 0x81fa81c in ecma_op_function_call ./jerryscript/jerry-core/ecma/operations/ecma-function-object.c:1411:16
    #9 0x81fa5ce in ecma_op_function_validated_call ./jerryscript/jerry-core/ecma/operations/ecma-function-object.c:1371:10
    #10 0x82d7630 in opfunc_call ./jerryscript/jerry-core/vm/vm.c:758:5
    #11 0x82d7630 in vm_execute ./jerryscript/jerry-core/vm/vm.c:5217:9
    #12 0x82d4f61 in vm_run ./jerryscript/jerry-core/vm/vm.c:5312:10
    #13 0x82d4c38 in vm_run_global ./jerryscript/jerry-core/vm/vm.c:286:25
    #14 0x812a4e4 in jerry_run ./jerryscript/jerry-core/api/jerryscript.c:548:24
    #15 0x83eac3e in jerryx_source_exec_script ./jerryscript/jerry-ext/util/sources.c:68:14
    #16 0x812162c in main ./jerryscript/jerry-main/main-desktop.c:156:20
    #17 0xf7b9aed4 in __libc_start_main (/lib32/libc.so.6+0x1aed4)

==2464945==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: allocation-size-too-big (./jerryscript/build/bin/jerry+0x80efe65) in malloc
==2464945==ABORTING
```

Credits:
@Ye0nny, @EJueon of the seclab-yonsei.


## Comment 1618057032

other (CONTRIBUTOR) · matetokodi · 2023-07-03T11:45:27Z · https://github.com/jerryscript-project/jerryscript/issues/5072#issuecomment-1618057032

Allocating such large arrays (1 000 000 000 * 4 bytes or nearly 4GB) is not a supported use case of jerryscript.


## Comment 1639358320

maintainer (MEMBER) · zherczeg · 2023-07-18T04:08:33Z · https://github.com/jerryscript-project/jerryscript/issues/5072#issuecomment-1639358320

A low end library does not need to support allocating way too large arrays,
