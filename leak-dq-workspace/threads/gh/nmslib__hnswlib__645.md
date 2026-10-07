# LeakSanitizer detects alloc-dealloc-mismatch (operator new [] vs operator delete)

- URL: https://github.com/nmslib/hnswlib/issues/645
- Repo: nmslib/hnswlib (language: C++)
- State: open; created 2026-02-09T12:05:39Z; status ok; passes main

## Issue body

reporter (NONE) · yushan107 · 2026-02-09T12:05:39Z · https://github.com/nmslib/hnswlib/issues/645

### Bug report

**Bug description**
LeakSanitizer detects alloc-dealloc-mismatch (operator new [] vs operator delete) when hnswlib.cpython-311-aarch64-linux-gnu.so is called.

**Used compilation parameters in setup.py**
`enable_asan = os.environ.get("HNSWLIB_ASAN", "0") == "1"
    if enable_asan:
        print("=== Enabling ASAN collection ===")
        c_opts['unix'].extend(['-fsanitize=leak', '-fno-stack-protector', '-fno-omit-frame-pointer', '-fsanitize=address', '-fsanitize-recover=address,all'])
        link_opts['unix'].extend(['-lasan'])`

**build**
`HNSWLIB_GCOV=1 python setup.py build_ext` 

**Run**
`export PYTHONPATH=build/lib.linux-aarch64-cpython-311/`
`LD_PRELOAD=/usr/lib64/libasan.so.8.0.0 python example.py`

`env`
python: Python 3.11.6
platform:Linux

**Log**:

> ==718453==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new [] vs operator delete) on 0xffffaeaa8400
>     #0 0xffffb78a6fc4 in operator delete(void*) (/usr/lib64/libasan.so.8.0.0+0xb6fc4)
>     #1 0xffffae6c853c in pybind11::capsule::initialize_with_void_ptr_destructor(void const*, char const*, void (*)(void*))::{lambda(_object*)#1}::_FUN(_object*) (/build/lib.linux-aarch64-cpython-311/hnswlib.cpython-311-aarch64-linux-gnu.so+0x6853c)
>     #2 0xffffb7359f08  (/usr/lib64/libpython3.11.so.1.0+0x109f08)
>     #3 0xffffadfdad44 in array_dealloc (/usr/local/lib64/python3.11/site-packages/numpy/core/_multiarray_umath.cpython-311-aarch64-linux-gnu.so+0x12ad44)
>     #4 0xffffb73ea170  (/usr/lib64/libpython3.11.so.1.0+0x19a170)
>     #5 0xffffb7354058 in _PyEval_EvalFrameDefault (/usr/lib64/libpython3.11.so.1.0+0x104058)
>     #6 0xffffb750ce98  (/usr/lib64/libpython3.11.so.1.0+0x2bce98)
>     #7 0xffffb750cf3c in PyEval_EvalCode (/usr/lib64/libpython3.11.so.1.0+0x2bcf3c)
>     #8 0xffffb750d8f8  (/usr/lib64/libpython3.11.so.1.0+0x2bd8f8)
>     #9 0xffffb750d9f0  (/usr/lib64/libpython3.11.so.1.0+0x2bd9f0)
>     #10 0xffffb750db14  (/usr/lib64/libpython3.11.so.1.0+0x2bdb14)
>     #11 0xffffb7513b44 in _PyRun_SimpleFileObject (/usr/lib64/libpython3.11.so.1.0+0x2c3b44)
>     #12 0xffffb7514080 in _PyRun_AnyFileObject (/usr/lib64/libpython3.11.so.1.0+0x2c4080)
>     #13 0xffffb7514fb8 in Py_RunMain (/usr/lib64/libpython3.11.so.1.0+0x2c4fb8)
>     #14 0xffffb754ad4c in Py_BytesMain (/usr/lib64/libpython3.11.so.1.0+0x2fad4c)
>     #15 0xffffb70276c0 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
>     #16 0xffffb70277a4 in __libc_start_main_impl ../csu/libc-start.c:360
>     #17 0xaaaab25008ac in _start (/usr/bin/python3.11+0x8ac)
> 
> 0xffffaeaa8400 is located 0 bytes inside of 40000-byte region [0xffffaeaa8400,0xffffaeab2040)
> allocated by thread T0 here:
>     #0 0xffffb78a65cc in operator new[](unsigned long) (/usr/lib64/libasan.so.8.0.0+0xb65cc)
>     #1 0xffffae73b6e4 in Index<float, float>::knnQuery_return_numpy(pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&) (/build/lib.linux-aarch64-cpython-311/hnswlib.cpython-311-aarch64-linux-gnu.so+0xdb6e4)
>     #2 0xffffae77e0a0 in pybind11::cpp_function::initialize<pybind11::cpp_function::initialize<pybind11::object, Index<float, float>, pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&, pybind11::name, pybind11::is_method, pybind11::sibling, pybind11::arg, pybind11::arg_v, pybind11::arg_v, pybind11::arg_v>(pybind11::object (Index<float, float>::*)(pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&), pybind11::name const&, pybind11::is_method const&, pybind11::sibling const&, pybind11::arg const&, pybind11::arg_v const&, pybind11::arg_v const&, pybind11::arg_v const&)::{lambda(Index<float, float>*, pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&)#1}, pybind11::object, Index<float, float>*, pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&, pybind11::name, pybind11::is_method, pybind11::sibling, pybind11::arg, pybind11::arg_v, pybind11::arg_v, pybind11::arg_v>(pybind11::cpp_function::initialize<pybind11::object, Index<float, float>, pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&, pybind11::name, pybind11::is_method, pybind11::sibling, pybind11::arg, pybind11::arg_v, pybind11::arg_v, pybind11::arg_v>(pybind11::object (Index<float, float>::*)(pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&), pybind11::name const&, pybind11::is_method const&, pybind11::sibling const&, pybind11::arg const&, pybind11::arg_v const&, pybind11::arg_v const&, pybind11::arg_v const&)::{lambda(Index<float, float>*, pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&)#1}&&, pybind11::object (*)(Index<float, float>*, pybind11::object, unsigned long, int, std::function<bool (unsigned long)> const&), pybind11::name const&, pybind11::is_method const&, pybind11::sibling const&, pybind11::arg const&, pybind11::arg_v const&, pybind11::arg_v const&, pybind11::arg_v const&)::{lambda(pybind11::detail::function_call&)#3}::_FUN(pybind11::detail::function_call&) (/build/lib.linux-aarch64-cpython-311/hnswlib.cpython-311-aarch64-linux-gnu.so+0x11e0a0)
>     #3 0xffffae716fec in pybind11::cpp_function::dispatcher(_object*, _object*, _object*) (/build/lib.linux-aarch64-cpython-311/hnswlib.cpython-311-aarch64-linux-gnu.so+0xb6fec)
>     #4 0xffffb740e2fc  (/usr/lib64/libpython3.11.so.1.0+0x1be2fc)
>     #5 0xffffb740e08c in _PyObject_MakeTpCall (/usr/lib64/libpython3.11.so.1.0+0x1be08c)
>     #6 0xffffb7353be8 in _PyEval_EvalFrameDefault (/usr/lib64/libpython3.11.so.1.0+0x103be8)
>     #7 0xffffb750ce98  (/usr/lib64/libpython3.11.so.1.0+0x2bce98)
>     #8 0xffffb750cf3c in PyEval_EvalCode (/usr/lib64/libpython3.11.so.1.0+0x2bcf3c)
>     #9 0xffffb750d8f8  (/usr/lib64/libpython3.11.so.1.0+0x2bd8f8)
>     #10 0xffffb750d9f0  (/usr/lib64/libpython3.11.so.1.0+0x2bd9f0)
>     #11 0xffffb750db14  (/usr/lib64/libpython3.11.so.1.0+0x2bdb14)
>     #12 0xffffb7513b44 in _PyRun_SimpleFileObject (/usr/lib64/libpython3.11.so.1.0+0x2c3b44)
>     #13 0xffffb7514080 in _PyRun_AnyFileObject (/usr/lib64/libpython3.11.so.1.0+0x2c4080)
>     #14 0xffffb7514fb8 in Py_RunMain (/usr/lib64/libpython3.11.so.1.0+0x2c4fb8)
>     #15 0xffffb754ad4c in Py_BytesMain (/usr/lib64/libpython3.11.so.1.0+0x2fad4c)
>     #16 0xffffb70276c0 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
>     #17 0xffffb70277a4 in __libc_start_main_impl ../csu/libc-start.c:360
>     #18 0xaaaab25008ac in _start (/usr/bin/python3.11+0x8ac)
> 
> SUMMARY: AddressSanitizer: alloc-dealloc-mismatch (/usr/lib64/libasan.so.8.0.0+0xb6fc4) in operator delete(void*)
> ==718453==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
> ==718453==ABORTING




## Comment 4062861167

other (NONE) · Anarion-zuo · 2026-03-15T12:05:37Z · https://github.com/nmslib/hnswlib/issues/645#issuecomment-4062861167

We ran into a similar issue. Fixed this in https://github.com/nmslib/hnswlib/pull/650.
