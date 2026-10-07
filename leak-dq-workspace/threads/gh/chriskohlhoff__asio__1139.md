# asio/detail/config.hpp is unreliable in boost:asio

- URL: https://github.com/chriskohlhoff/asio/issues/1139
- Repo: chriskohlhoff/asio (language: C++)
- State: open; created 2022-10-11T15:04:41Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · reddwarf69 · 2022-10-11T15:04:41Z · https://github.com/chriskohlhoff/asio/issues/1139

Edit: Long story short, boost::asio seems to lack https://github.com/chriskohlhoff/asio/commit/6d51490576ef219f3bc6dda3baecc3a9efe49dd5, I guess because of https://github.com/chriskohlhoff/asio/blob/147f7225a96d45a2807a64e443177f621844e51c/asio/include/asio/detail/config.hpp#L38.


Given the following cmake project
[asio_config_test.tar.gz](https://github.com/chriskohlhoff/asio/files/9757276/asio_config_test.tar.gz)
we may end up with asio::aligned_new() behaviour not matching asio::aligned_delete().

```
bash-5.1# rm -rf build*; for CPPFLAGS in '-DASIO_SEPARATE_STDIO' '-DMAIN_STDIO' '-DASIO_SEPARATE_STDIO -DMAIN_STDIO' ''; do CXXFLAGS="${CPPFLAGS} -g -O1 -fsanitize=address" cmake -B "build_${CPPFLAGS}" -DBoost_ROOT=/home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost-build/stage; cmake --build "build_${CPPFLAGS}"; done &>/dev/null
bash-5.1# build_/test 
bash-5.1# build_-DASIO_SEPARATE_STDIO\ -DMAIN_STDIO/test 
bash-5.1# build_-DASIO_SEPARATE_STDIO/test               
=================================================================
==82484==ERROR: AddressSanitizer: alloc-dealloc-mismatch (operator new vs free) on 0x6110000002c0
    #0 0x7f20f25d1368 in __interceptor_free.part.0 (/lib64/libasan.so.8+0xb9368)
    #1 0x4568dd in boost::asio::aligned_delete(void*) /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/memory.hpp:138
    #2 0x4568dd in boost::asio::detail::thread_info_base::~thread_info_base() /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/thread_info_base.hpp:116
    #3 0x4568dd in boost::asio::detail::scheduler_thread_info::~scheduler_thread_info() /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/scheduler_thread_info.hpp:30
    #4 0x4568dd in boost::asio::detail::scheduler::poll(boost::system::error_code&) /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/impl/scheduler.ipp:281
    #5 0x45c228 in boost::asio::io_context::poll() /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/impl/io_context.ipp:93
    #6 0x40629d in main /cmake/main.cpp:14
    #7 0x7f20f200d54f in __libc_start_call_main (/lib64/libc.so.6+0x2954f)
    #8 0x7f20f200d608 in __libc_start_main@@GLIBC_2.34 (/lib64/libc.so.6+0x29608)
    #9 0x405b94 in _start (/cmake/build_-DASIO_SEPARATE_STDIO/test+0x405b94)

0x6110000002c0 is located 0 bytes inside of 201-byte region [0x6110000002c0,0x611000000389)
allocated by thread T0 here:
    #0 0x7f20f25d3188 in operator new(unsigned long) (/lib64/libasan.so.8+0xbb188)
    #1 0x40d785 in void boost::asio::detail::reactive_socket_service_base::async_send<boost::asio::const_buffer, boost::asio::detail::write_op<boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>, boost::asio::const_buffer, boost::asio::const_buffer const*, boost::asio::detail::transfer_all_t, boost::asio::detail::detached_handler>, boost::asio::any_io_executor>(boost::asio::detail::reactive_socket_service_base::base_implementation_type&, boost::asio::const_buffer const&, int, boost::asio::detail::write_op<boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>, boost::asio::const_buffer, boost::asio::const_buffer const*, boost::asio::detail::transfer_all_t, boost::asio::detail::detached_handler>&, boost::asio::any_io_executor const&) (/cmake/build_-DASIO_SEPARATE_STDIO/test+0x40d785)
    #2 0x40e840 in auto boost::asio::async_write<boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>, boost::asio::const_buffer, boost::asio::detached_t const&>(boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>&, boost::asio::const_buffer const&, boost::asio::detached_t const&, boost::asio::constraint<boost::asio::is_const_buffer_sequence<boost::asio::const_buffer>::value, int>::type) (/cmake/build_-DASIO_SEPARATE_STDIO/test+0x40e840)
    #3 0x4724bf  (/cmake/build_-DASIO_SEPARATE_STDIO/test+0x4724bf)

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch (/lib64/libasan.so.8+0xb9368) in __interceptor_free.part.0
==82484==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==82484==ABORTING
bash-5.1# build_-DMAIN_STDIO/test          
=================================================================
==82503==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete) on 0x6110000002c0
    #0 0x7fa6c41fabc8 in operator delete(void*) (/lib64/libasan.so.8+0xbbbc8)
    #1 0x4567f9 in boost::asio::aligned_delete(void*) /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/memory.hpp:144
    #2 0x4567f9 in boost::asio::detail::thread_info_base::~thread_info_base() /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/thread_info_base.hpp:116
    #3 0x4567f9 in boost::asio::detail::scheduler_thread_info::~scheduler_thread_info() /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/scheduler_thread_info.hpp:30
    #4 0x4567f9 in boost::asio::detail::scheduler::poll(boost::system::error_code&) /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/detail/impl/scheduler.ipp:281
    #5 0x45cf00 in boost::asio::io_context::poll() /home/skcristian/git/router_agent_build/servers/full/dependencies/src/boost/external-boost-prefix/src/external-boost/boost/asio/impl/io_context.ipp:93
    #6 0x40629d in main /cmake/main.cpp:14
    #7 0x7fa6c3c3454f in __libc_start_call_main (/lib64/libc.so.6+0x2954f)
    #8 0x7fa6c3c34608 in __libc_start_main@@GLIBC_2.34 (/lib64/libc.so.6+0x29608)
    #9 0x405b94 in _start (/cmake/build_-DMAIN_STDIO/test+0x405b94)

0x6110000002c0 is located 0 bytes inside of 208-byte region [0x6110000002c0,0x611000000390)
allocated by thread T0 here:
    #0 0x7fa6c41f8b28 in aligned_alloc (/lib64/libasan.so.8+0xb9b28)
    #1 0x40d7e4 in void boost::asio::detail::reactive_socket_service_base::async_send<boost::asio::const_buffer, boost::asio::detail::write_op<boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>, boost::asio::const_buffer, boost::asio::const_buffer const*, boost::asio::detail::transfer_all_t, boost::asio::detail::detached_handler>, boost::asio::any_io_executor>(boost::asio::detail::reactive_socket_service_base::base_implementation_type&, boost::asio::const_buffer const&, int, boost::asio::detail::write_op<boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>, boost::asio::const_buffer, boost::asio::const_buffer const*, boost::asio::detail::transfer_all_t, boost::asio::detail::detached_handler>&, boost::asio::any_io_executor const&) (/cmake/build_-DMAIN_STDIO/test+0x40d7e4)
    #2 0x40e8dd in auto boost::asio::async_write<boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>, boost::asio::const_buffer, boost::asio::detached_t const&>(boost::asio::basic_stream_socket<boost::asio::ip::tcp, boost::asio::any_io_executor>&, boost::asio::const_buffer const&, boost::asio::detached_t const&, boost::asio::constraint<boost::asio::is_const_buffer_sequence<boost::asio::const_buffer>::value, int>::type) (/cmake/build_-DMAIN_STDIO/test+0x40e8dd)
    #3 0x4724cf  (/cmake/build_-DMAIN_STDIO/test+0x4724cf)

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch (/lib64/libasan.so.8+0xbbbc8) in operator delete(void*)
==82503==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==82503==ABORTING
bash-5.1#
```

The problem being that https://github.com/chriskohlhoff/asio/blob/147f7225a96d45a2807a64e443177f621844e51c/asio/include/asio/detail/config.hpp#L694 depends on variables like _GLIBCXX_HAVE_ALIGNED_ALLOC, which are defined in libstdc++ in headers that are not included in asio/detail/config.hpp.

In this specific example, asio/detail/memory.hpp #includes cstdlib (https://github.com/chriskohlhoff/asio/blob/147f7225a96d45a2807a64e443177f621844e51c/asio/include/asio/detail/memory.hpp#L20) **after** asio/detail/config.hpp (https://github.com/chriskohlhoff/asio/blob/147f7225a96d45a2807a64e443177f621844e51c/asio/include/asio/detail/memory.hpp#L18). So you can't blame libstdc++ for this.

Not sure what the best solution is. I guess #including a cheap libstdc++ header in asio/detail/config.hpp would do the trick.
