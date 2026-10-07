# Access violation problem on CPU when number of jobs is significantly high

- URL: https://github.com/ispc/ispc/issues/2040
- Repo: ispc/ispc (language: C++)
- State: open; created 2021-03-15T22:54:00Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · aneshlya · 2021-03-15T22:54:00Z · https://github.com/ispc/ispc/issues/2040

Can be reproduced with cpu_examples/mandelbrot_tasks:
--- a/examples/cpu/mandelbrot_tasks/mandelbrot_tasks.cpp
+++ b/examples/cpu/mandelbrot_tasks/mandelbrot_tasks.cpp
@@ -73,8 +73,8 @@ static void usage() {

 int main(int argc, char *argv[]) {
     static unsigned int test_iterations[] = {7, 1};
-    unsigned int width = 1536;
-    unsigned int height = 1024;
+    unsigned int width = 1536*50;
+    unsigned int height = 1024*50;

It does not depend on task system used (the behaviour the same for pthreads, tbb and omp). Reproduced on Windows/Linux.

==362795==ERROR: MemorySanitizer: requested allocation size 0x2a6000000 exceeds maximum supported size of 0x200000000
    <empty stack>
==362795==HINT: if you don't care about these errors you may set allocator_may_return_null=1
SUMMARY: MemorySanitizer: allocation-size-too-big

