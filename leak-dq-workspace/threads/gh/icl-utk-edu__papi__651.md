# [Issue]: Leaks in PAPI_event_name_to_code() when called concurrently from multiple threads

- URL: https://github.com/icl-utk-edu/papi/issues/651
- Repo: icl-utk-edu/papi (language: C)
- State: open; created 2026-08-28T12:17:55Z; status ok; passes offcwe

## Issue body

reporter (NONE) · Abel-Breaker · 2026-08-28T12:17:55Z · https://github.com/icl-utk-edu/papi/issues/651

### Issue Description

When trying to measure hardware counters from multiple pthreads,  AddressSanitizer/LeakSanitizer intermittently (some executions show leaks, others don't) reports memory leaks from `PAPI_event_name_to_code()` function, originated inside `libpapi.so.7.1`.

### Operating System

Ubuntu 24.04.4 LTS (Noble Numbat)

### Architecture

x86_64

### CPU Architecture

AMD Ryzen 7 4800H with Radeon Graphics

### Compiler

gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0

### PAPI Version

7.1.0.0 (7.1.0-5build1)

### Component

_No response_

### Steps to Reproduce

### Minimal reproducible example

```
#include <papi.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 2

void *worker(void *arg)
{
	(void)arg;

	int EventSet = PAPI_NULL;
	int event_code;

	int ret = PAPI_create_eventset(&EventSet);
	if (ret != PAPI_OK) {
		fprintf(stderr, "PAPI_create_eventset failed (%s)\n", PAPI_strerror(ret));
		return NULL;
	}

	/* LEAK */
	ret = PAPI_event_name_to_code("perf::PERF_COUNT_HW_CPU_CYCLES", &event_code);
	if (ret != PAPI_OK) {
		fprintf(stderr, "PAPI_event_name_to_code failed (%s)\n", PAPI_strerror(ret));
		return NULL;
	}

	ret = PAPI_add_event(EventSet, event_code);
	if (ret != PAPI_OK) {
		fprintf(stderr, "PAPI_add_event failed (%s)\n", PAPI_strerror(ret));
		return NULL;
	}

	ret = PAPI_start(EventSet);
	if (ret != PAPI_OK) {
		fprintf(stderr, "PAPI_start failed (%s)\n", PAPI_strerror(ret));
		return NULL;
	}

	volatile double sum = 0.0;
	for (int i = 0; i < 10000000; i++) {
		sum += i * 1.5;
	}

	long long value;
	PAPI_stop(EventSet, &value);
	PAPI_cleanup_eventset(EventSet);
	PAPI_destroy_eventset(&EventSet);

	PAPI_unregister_thread();

	return NULL;
}

int main(void)
{
	int ret = PAPI_library_init(PAPI_VER_CURRENT);
	if (ret != PAPI_VER_CURRENT) {
		fprintf(stderr, "PAPI_library_init failed (%s)\n", PAPI_strerror(ret));
		return EXIT_FAILURE;
	}

	ret = PAPI_thread_init((unsigned long (*)(void))pthread_self);
	if (ret != PAPI_OK) {
		fprintf(stderr, "PAPI_thread_init failed (%s)\n", PAPI_strerror(ret));
		return EXIT_FAILURE;
	}

	pthread_t threads[NUM_THREADS];

	for (int i = 0; i < NUM_THREADS; i++) {
		pthread_create(&threads[i], NULL, worker, NULL);
	}

	for (int i = 0; i < NUM_THREADS; i++) {
		pthread_join(threads[i], NULL);
	}

	PAPI_shutdown();

	return EXIT_SUCCESS;
}
```

Compiled with:

```
gcc main.c -o program -Wall -Wextra -pthread -lpapi -fsanitize=address,undefined,leak
```

### Output

```
=================================================================
==21961==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa202c  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a02c) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

Direct leak of 30 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa206a  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a06a) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

Direct leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa23b7  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a3b7) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

Direct leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa205e  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a05e) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

Direct leak of 14 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa207e  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a07e) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

Direct leak of 10 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa203f  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a03f) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

Direct leak of 5 byte(s) in 1 object(s) allocated from:
    #0 0x7ee0960f74e8 in strdup ../../../../src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0x7ee095fa1f01  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x29f01) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #2 0x7ee095fa2569  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x2a569) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #3 0x7ee095f8de26  (/lib/x86_64-linux-gnu/libpapi.so.7.1+0x15e26) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #4 0x7ee095f85649 in PAPI_event_name_to_code (/lib/x86_64-linux-gnu/libpapi.so.7.1+0xd649) (BuildId: 63fbb30879b5e4a7907b76a16735449b748be2d7)
    #5 0x5baa3677767a in worker (/home/user/StackOverflowQuestions/PAPI_memory_leak/program+0x267a) (BuildId: 412cf49a8f32dba4026b3a18c03cfb94f31f2d40)
    #6 0x7ee09605ea41 in asan_thread_start ../../../../src/libsanitizer/asan/asan_interceptors.cpp:234
    #7 0x7ee09549cb83 in start_thread nptl/pthread_create.c:447

SUMMARY: AddressSanitizer: 147 byte(s) leaked in 7 allocation(s).
```

### Additional Information

Things I've observed:

- It only occurs when using more than 1 thread.

- It occurs when compiling with both clang (18.1.3) and gcc.

- It only occurs with native events (not with \`PAPI\_\`-prefixed preset events).

- If I put a \`sleep()\` between thread creations, the leak never appears, so **I suspect this is a race condition**.

I also compiled and tested the latest version of PAPI (7.2.0) from source, and the behavior is practically identical, the leak still occurs.

## Comment 5527795639

other (CONTRIBUTOR) · dbarry9 · 2026-09-03T15:09:15Z · https://github.com/icl-utk-edu/papi/issues/651#issuecomment-5527795639

I have reproduced this issue on a system with the following:
- ARM Neoverse-V2 
- NVIDIA GH200 480GB
- CUDA 13.3.1
- GCC 14.0.1

Please note the full error log from the reproducer with which I am testing:
```
=================================================================
==2409188==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 31 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb6508 in allocate_native_event components/perf_event/pe_libpfm4_events.c:321
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

Direct leak of 31 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb63cc in allocate_native_event components/perf_event/pe_libpfm4_events.c:316
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

Direct leak of 25 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb65e0 in allocate_native_event components/perf_event/pe_libpfm4_events.c:323
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

Direct leak of 25 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb64cc in allocate_native_event components/perf_event/pe_libpfm4_events.c:320
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

Direct leak of 5 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb51dc in allocate_native_event components/perf_event/pe_libpfm4_events.c:244
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

Direct leak of 1 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb8098 in allocate_native_event components/perf_event/pe_libpfm4_events.c:422
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

Direct leak of 1 byte(s) in 1 object(s) allocated from:
    #0 0xffff9005eb58 in strdup /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:578
    #1 0xffff8fdb6404 in allocate_native_event components/perf_event/pe_libpfm4_events.c:317
    #2 0xffff8fdbaf04 in _pe_libpfm4_ntv_name_to_code components/perf_event/pe_libpfm4_events.c:607
    #3 0xffff8fdacb20 in _pe_ntv_name_to_code components/perf_event/perf_event.c:1886
    #4 0xffff8fd26bf0 in _papi_hwi_native_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi_internal.c:2818
    #5 0xffff8fcc9b3c in PAPI_event_name_to_code /storage/users/dbarry/src/papi-aaronmerey/src/papi.c:1717
    #6 0x4014a0 in worker /home/users/dbarry/src/papi-aaronmerey/src/repro/test1.c:22
    #7 0xffff8ffeb984 in asan_thread_start /tmp/sameer/spack-stage/spack-stage-gcc-master-kzmttphzb6lq4qeqy6mpzbefmagckwp4/spack-src/libsanitizer/asan/asan_interceptors.cpp:234
    #8 0xffff8f531898 in thread_start (/lib64/libc.so.6+0xeb898) (BuildId: f49b931266355f1ed4a0e555b4ba8e819deb8587)

SUMMARY: AddressSanitizer: 119 byte(s) leaked in 7 allocation(s).
```

These leaks are still occurring in master.

## Comment 5858226615

reporter (NONE) · Abel-Breaker · 2026-09-27T17:43:49Z · https://github.com/icl-utk-edu/papi/issues/651#issuecomment-5858226615

How is this going? 

## Comment 5877758966

other (CONTRIBUTOR) · dbarry9 · 2026-09-28T20:19:40Z · https://github.com/icl-utk-edu/papi/issues/651#issuecomment-5877758966

Hi @Abel-Breaker, I have found the root cause of this issue, and I am in the process of creating a PR for it. I will keep you posted.

## Comment 5879159899

other (CONTRIBUTOR) · dbarry9 · 2026-09-28T21:34:14Z · https://github.com/icl-utk-edu/papi/issues/651#issuecomment-5879159899

@Abel-Breaker I have opened PR #690. Could you please checkout this PR and let me know if it resolves the issue on your end?

## Comment 5887879086

reporter (NONE) · Abel-Breaker · 2026-09-29T09:55:46Z · https://github.com/icl-utk-edu/papi/issues/651#issuecomment-5887879086

It works fine for me and resolves the issue.

Tested on:
**Operating System**: Ubuntu 24.04.4 LTS (Noble Numbat)
**Architecture**: x86_64
**CPU**: AMD Ryzen 7 4800H with Radeon Graphics
**Compiler**: gcc (Ubuntu 13.3.0-6ubuntu2~24.04.1) 13.3.0
