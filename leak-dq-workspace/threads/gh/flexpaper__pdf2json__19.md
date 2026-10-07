# Alloc_dealloc_mismatch in function ~HtmlString

- URL: https://github.com/flexpaper/pdf2json/issues/19
- Repo: flexpaper/pdf2json (language: C++)
- State: open; created 2018-07-23T11:08:54Z; status ok; passes main

## Issue body

reporter (NONE) · fouzhe · 2018-07-23T11:08:54Z · https://github.com/flexpaper/pdf2json/issues/19

I use **Clang 6.0 and AddressSanitizer**  to build **pdf2json v0.69**, this [file](https://github.com/fouzhe/security/blob/master/pdf2json/alloc_dealloc_mismatch_~HtmlString.pdf) can cause alloc-dealloc-mismatch with the following command:



```shell
./pdf2json alloc_dealloc_mismatch_~HtmlString.pdf 1.json
```



This is the ASAN information:

```shell
=================================================================
==22708==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete) on 0x606000004580
    #0 0x517bd0 in operator delete(void*) /home/fouzhe/llvm/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cc:149
    #1 0x51c1ec in HtmlString::~HtmlString() /home/fouzhe/my_fuzz/pdf2json/src/ImgOutputDev.cc:118:3
    #2 0x52282c in HtmlPage::coalesce() /home/fouzhe/my_fuzz/pdf2json/src/ImgOutputDev.cc:558:10
    #3 0x52a41c in ImgOutputDev::endPage() /home/fouzhe/my_fuzz/pdf2json/src/ImgOutputDev.cc:978:10
    #4 0x78c975 in Gfx::~Gfx() /home/fouzhe/my_fuzz/pdf2json/xpdf/Gfx.cc:530:10
    #5 0x60aa91 in Page::displaySlice(OutputDev*, double, double, int, int, int, int, int, int, int, Links*, int, Catalog*, int (*)(void*), void*) /home/fouzhe/my_fuzz/pdf2json/xpdf/Page.cc:359:3
    #6 0x609810 in Page::display(OutputDev*, double, double, int, int, int, Links*, int, Catalog*, int (*)(void*), void*) /home/fouzhe/my_fuzz/pdf2json/xpdf/Page.cc:265:3
    #7 0x60feb5 in PDFDoc::displayPage(OutputDev*, int, double, double, int, int, int, int, int (*)(void*), void*) /home/fouzhe/my_fuzz/pdf2json/xpdf/PDFDoc.cc:319:27
    #8 0x60feb5 in PDFDoc::displayPages(OutputDev*, int, int, double, double, int, int, int, int, int (*)(void*), void*) /home/fouzhe/my_fuzz/pdf2json/xpdf/PDFDoc.cc:332
    #9 0x53c946 in main /home/fouzhe/my_fuzz/pdf2json/src/pdf2json.cc:275:10
    #10 0x7f1f071e482f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
    #11 0x41b198 in _start (/home/fouzhe/my_fuzz/pdf2json/src/pdf2json+0x41b198)

0x606000004580 is located 0 bytes inside of 64-byte region [0x606000004580,0x6060000045c0)
allocated by thread T0 here:
    #0 0x4df3c8 in __interceptor_malloc /home/fouzhe/llvm/llvm/projects/compiler-rt/lib/asan/asan_malloc_linux.cc:88
    #1 0x8dcbc3 in grealloc /home/fouzhe/my_fuzz/pdf2json/goo/gmem.cc:143:9

SUMMARY: AddressSanitizer: alloc-dealloc-mismatch /home/fouzhe/llvm/llvm/projects/compiler-rt/lib/asan/asan_new_delete.cc:149 in operator delete(void*)
==22708==HINT: if you don't care about these errors you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
==22708==ABORTING
```





# 
