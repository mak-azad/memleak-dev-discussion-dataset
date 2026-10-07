# genmkvpwd max_lvl parameter memory exhaustion

- URL: https://github.com/openwall/john/issues/5798
- Repo: openwall/john (language: C)
- State: open; created 2025-07-03T02:59:36Z; status ok; passes main

## Issue body

reporter (NONE) · momo-trip · 2025-07-03T02:59:36Z · https://github.com/openwall/john/issues/5798

# genmkvpwd max_lvl parameter memory exhaustion

Hi, we have found a memory exhaustion issue and would like to report this.
We're running the proposed fix locally but haven't tested thoroughly. Please make any needed corrections and push.

## Summary
The `max_lvl` argument in genmkpwd can cause excessive memory allocation when an invalid or large value is provided.

## Reproduction
- Operating System: Ubuntu 24.04 LTS
- Architecture: x86_64
- Compiler: GCC 14.2.0

## Reproduction steps
```bash
git clone https://github.com/openwall/john
cd john/src
./configure --enable-asan
make
../run/genmkvpwd  ../run/stats -1
# No crash, but large allocations
# ../run/genmkvpwd  ../run/stats 99999
```

## Output
```
=================================================================
==1014574==ERROR: AddressSanitizer: out of memory: allocator is trying to allocate 0x2160ec0000 bytes
    #0 0x7c1c7f4fd9c7 in malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x5a111f4e4031 in mem_alloc /tmp/john/src/memory.c:92
    #2 0x5a111f4e2069 in main /tmp/john/src/genmkvpwd.c:232
    #3 0x7c1c7f02a1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #4 0x7c1c7f02a28a in __libc_start_main_impl ../csu/libc-start.c:360
    #5 0x5a111f4e07e4 in _start (/tmp/john/run/genmkvpwd+0x47e4) (BuildId: b4e075dafb2127c3f70d28cd97c5c1dcc7034212)
==1014574==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: AddressSanitizer: out-of-memory ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69 in malloc
==1014574==ABORTING
```

## Root Cause Analysis
[[src/genmkvpwd.c:217](https://github.com/openwall/john/blob/5baa3c47dbef1466b106a5894e3096b13a8c22f1/src/genmkvpwd.c#L217)](https://github.com/openwall/john/blob/5baa3c47dbef1466b106a5894e3096b13a8c22f1/src/genmkvpwd.c#L217)
The `max_lvl` value is read from command line arguments using `atoi`.

[[src/genmkvpwd.c:232](https://github.com/openwall/john/blob/5baa3c47dbef1466b106a5894e3096b13a8c22f1/src/genmkvpwd.c#L232)](https://github.com/openwall/john/blob/5baa3c47dbef1466b106a5894e3096b13a8c22f1/src/genmkvpwd.c#L232)
Here, when `max_lvl` is large, excessive memory allocation occurs.
This code path is executed when `max_len` is not provided as an argument or is set to 0.

[[src/genmkvpwd.c:269](https://github.com/openwall/john/blob/5baa3c47dbef1466b106a5894e3096b13a8c22f1/src/genmkvpwd.c#L269)](https://github.com/openwall/john/blob/5baa3c47dbef1466b106a5894e3096b13a8c22f1/src/genmkvpwd.c#L269)
Additional context: When `max_len` is non-zero, it is corrected to be within `MAX_MKV_LVL`.

## Proposed Fix
This issue can be avoided by comparing against `MAX_MKV_LVL`, similar to when `max_len` is non-zero.
Additionally, using `strtol` instead of `atoi` would better prevent invalid input.

```diff
diff --git a/src/genmkvpwd.c b/src/genmkvpwd.c
index de62d0330..4b5e0f5d9 100644
--- a/src/genmkvpwd.c
+++ b/src/genmkvpwd.c
@@ -214,7 +214,17 @@ int main(int argc, char * *argv)
 		return -1;
 	}
 
-	max_lvl = atoi(argv[2]);
+	char *parse_error;
+	long l_max_lvl = strtol(argv[2], &parse_error, 10);
+	if (errno != 0){
+		printf("Usage: %s statfile max_lvl [max_len] [start] [end]\n", argv[0]);
+		return -1;
+	} else if (l_max_lvl > UINT_MAX || l_max_lvl < 0|| parse_error[0] != '\0'){
+		fprintf(stderr, "max_lvl is invalid\n");
+		return -1;
+	}
+
+	max_lvl = l_max_lvl;
 
 	if (argc>3)
 		max_len = atoi(argv[3]);
@@ -227,6 +237,10 @@ int main(int argc, char * *argv)
 
 	if (max_len == 0)
 	{
+		if (max_lvl>MAX_MKV_LVL) {
+			fprintf(stderr, "Warning: Level = %d is too large (max = %d)\n", max_lvl, MAX_MKV_LVL);
+			max_lvl = MAX_MKV_LVL;
+		}
 		for (max_len=6;max_len<20;max_len++)
 		{
 			nbparts = mem_alloc(256*(max_lvl+1)*sizeof(long long)*(max_len+1));
```
