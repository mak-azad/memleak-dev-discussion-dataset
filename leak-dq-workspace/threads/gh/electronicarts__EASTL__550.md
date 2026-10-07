# Mismatched free() / delete / delete [] when using EAWebKit

- URL: https://github.com/electronicarts/EASTL/issues/550
- Repo: electronicarts/EASTL (language: C++)
- State: open; created 2025-01-03T21:50:31Z; status ok; passes main

## Issue body

reporter (NONE) · TornadoCookie · 2025-01-03T21:50:31Z · https://github.com/electronicarts/EASTL/issues/550


Allocating a string uses the EAWebKit allocator, but deallocating it uses the system allocator. This seems to mess up the stack.
Version: EASTL 3.16.05 (EAWebKit 16.4.2.0.0)

Section of valgrind log:
==689759== Mismatched free() / delete / delete []
==689759==    at 0x484BFA4: operator delete[](void*) (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==689759==    by 0x6A86EEF: deallocate (allocator.h:292)
==689759==    by 0x6A86EEF: DoFree (string.h:3281)
==689759==    by 0x6A86EEF: eastl::basic_string<char, eastl::allocator>::DeallocateSelf() (string.h:3349)
==689759==    by 0x6DA2030: ~basic_string (string.h:995)
==689759==    by 0x6DA2030: EA::WebKit::DebugLogCallback(eastl::basic_string<char, eastl::allocator> const&, bool) (EAWebKit.cpp:632)
==689759==    by 0x6DA3D29: EA::WebKit::DebugLogCallbackInternal(bool, char const*, __va_list_tag*) (EAWebKit.cpp:638)
==689759==    by 0x74C14DB: vprintf_stderr_common (Assertions.cpp:152)
==689759==    by 0x74C1834: printf_stderr_common (Assertions.cpp:235)
==689759==    by 0x74C18D4: WTFReportAssertionFailure (Assertions.cpp:267)
==689759==    by 0x6DA4C52: EA::WebKit::GetAllocator() (EAWebKitAllocator.cpp:353)
==689759==    by 0x6DA1A6B: EA::WebKit::Init(EA::WebKit::AppCallbacks*, EA::WebKit::AppSystems*) (EAWebKit.cpp:676)
==689759==    by 0x6DA1C1E: EA::WebKit::EAWebKitLib::Init(EA::WebKit::AppCallbacks*, EA::WebKit::AppSystems*) (EAWebKit.cpp:196)
==689759==    by 0x10A49F: main (main.cpp:98)
==689759==  Address 0x9598910 is 0 bytes inside a block of size 52 alloc'd
==689759==    at 0x4846828: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==689759==    by 0x6DA557D: EA::WebKit::DefaultAllocator::Malloc(unsigned long, int, char const*) (EAWebKitAllocator.cpp:98)
==689759==    by 0x6DB40EA: operator new[](unsigned long, char const*, int, unsigned int, char const*, int) (EAWebKitNewDelete.cpp:173)
==689759==    by 0x63F4F81: eastl::allocator::allocate(unsigned long, int) (allocator.h:245)
==689759==    by 0x6DA431B: DoAllocate (string.h:3273)
==689759==    by 0x6DA431B: eastl::basic_string<char, eastl::allocator>::append(char const*, char const*) (string.h:1720)
==689759==    by 0x6DA440F: eastl::basic_string<char, eastl::allocator>::append(eastl::basic_string<char, eastl::allocator> const&) (string.h:1612)
==689759==    by 0x6DA1F8A: operator+= (string.h:1590)
==689759==    by 0x6DA1F8A: EA::WebKit::DebugLogCallback(eastl::basic_string<char, eastl::allocator> const&, bool) (EAWebKit.cpp:608)
==689759==    by 0x6DA3D29: EA::WebKit::DebugLogCallbackInternal(bool, char const*, __va_list_tag*) (EAWebKit.cpp:638)
==689759==    by 0x74C14DB: vprintf_stderr_common (Assertions.cpp:152)
==689759==    by 0x74C1834: printf_stderr_common (Assertions.cpp:235)
==689759==    by 0x74C18D4: WTFReportAssertionFailure (Assertions.cpp:267)
==689759==    by 0x6DA4C52: EA::WebKit::GetAllocator() (EAWebKitAllocator.cpp:353)



## Comment 2574403980

reporter (NONE) · TornadoCookie · 2025-01-07T05:08:58Z · https://github.com/electronicarts/EASTL/issues/550#issuecomment-2574403980

Upon further investigation it does not mess up the stack, but it is still odd that it is present.
