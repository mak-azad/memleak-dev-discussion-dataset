# alloc-dealloc-mismatch-HtmlString-~HtmlString

- URL: https://github.com/dsidavis/pdftohtml/issues/6
- Repo: dsidavis/pdftohtml (language: C++)
- State: open; created 2020-07-10T04:27:14Z; status ok; passes main

## Issue body

reporter (NONE) · Aurorainfinity · 2020-07-10T04:27:14Z · https://github.com/dsidavis/pdftohtml/issues/6

$./pdftohtml 03-alloc-dealloc-mismatch-HtmlString-~HtmlString

	==126277==ERROR: AddressSanitizer: alloc-dealloc-mismatch (malloc vs operator delete) on 0x606000008420
	    #0 0x7f795792cb2a in operator delete(void*) (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x99b2a)
	    #1 0x40380b in HtmlString::~HtmlString() /home/test/pdftohtml_tmp/src/HtmlOutputDev.cc:152
	    #2 0x408206 in HtmlPage::coalesce() /home/test/pdftohtml_tmp/src/HtmlOutputDev.cc:672
	    #3 0x40d943 in HtmlOutputDev::endPage() /home/test/pdftohtml_tmp/src/HtmlOutputDev.cc:1458
	    #4 0x471ab5 in Gfx::~Gfx() /home/test/pdftohtml_tmp/xpdf/Gfx.cc:509
	    #5 0x43ebe5 in Page::displaySlice(OutputDev*, double, double, int, int, int, int, int, int, int, Links*, Catalog*, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/Page.cc:347
	    #6 0x43e1ad in Page::display(OutputDev*, double, double, int, int, int, Links*, Catalog*, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/Page.cc:223
	    #7 0x43fa41 in PDFDoc::displayPage(OutputDev*, int, double, double, int, int, int, int, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/PDFDoc.cc:327
	    #8 0x43fb1c in PDFDoc::displayPages(OutputDev*, int, int, double, double, int, int, int, int, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/PDFDoc.cc:343
	    #9 0x41ce0a in main /home/test/pdftohtml_tmp/src/pdftohtml.cc:300
	    #10 0x7f7956c4883f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)
	    #11 0x4028a8 in _start (/home/test/pdftohtml_tmp/src/pdftohtml+0x4028a8)

	0x606000008420 is located 0 bytes inside of 64-byte region [0x606000008420,0x606000008460)
	allocated by thread T0 here:
	    #0 0x7f795792b602 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98602)
	    #1 0x4a7c4d in grealloc (/home/test/pdftohtml_tmp/src/pdftohtml+0x4a7c4d)
	    #2 0x403a6b in HtmlString::addChar(GfxState*, double, double, double, double, unsigned int) /home/test/pdftohtml_tmp/src/HtmlOutputDev.cc:167
	    #3 0x405646 in HtmlPage::addChar(GfxState*, double, double, double, double, double, double, unsigned int*, int) /home/test/pdftohtml_tmp/src/HtmlOutputDev.cc:361
	    #4 0x40df16 in HtmlOutputDev::drawChar(GfxState*, double, double, double, double, double, double, unsigned int, int, unsigned int*, int) /home/test/pdftohtml_tmp/src/HtmlOutputDev.cc:1513
	    #5 0x47ef30 in Gfx::doShowText(GString*) /home/test/pdftohtml_tmp/xpdf/Gfx.cc:2823
	    #6 0x47df96 in Gfx::opShowSpaceText(Object*, int) /home/test/pdftohtml_tmp/xpdf/Gfx.cc:2681
	    #7 0x47244c in Gfx::execOp(Object*, Object*, int) /home/test/pdftohtml_tmp/xpdf/Gfx.cc:676
	    #8 0x471e7a in Gfx::go(int) /home/test/pdftohtml_tmp/xpdf/Gfx.cc:566
	    #9 0x471c5e in Gfx::display(Object*, int) /home/test/pdftohtml_tmp/xpdf/Gfx.cc:538
	    #10 0x43e9e1 in Page::displaySlice(OutputDev*, double, double, int, int, int, int, int, int, int, Links*, Catalog*, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/Page.cc:317
	    #11 0x43e1ad in Page::display(OutputDev*, double, double, int, int, int, Links*, Catalog*, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/Page.cc:223
	    #12 0x43fa41 in PDFDoc::displayPage(OutputDev*, int, double, double, int, int, int, int, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/PDFDoc.cc:327
	    #13 0x43fb1c in PDFDoc::displayPages(OutputDev*, int, int, double, double, int, int, int, int, int (*)(void*), void*) /home/test/pdftohtml_tmp/xpdf/PDFDoc.cc:343
	    #14 0x41ce0a in main /home/test/pdftohtml_tmp/src/pdftohtml.cc:300
	    #15 0x7f7956c4883f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2083f)

	SUMMARY: AddressSanitizer: alloc-dealloc-mismatch ??:0 operator delete(void*)
	==126277==HINT: if you don't care about these warnings you may set ASAN_OPTIONS=alloc_dealloc_mismatch=0
	==126277==ABORTING

ref:https://github.com/Aurorainfinity/Poc/tree/master/pdftohtml
[03-alloc-dealloc-mismatch-HtmlString-~HtmlString.pdf](https://github.com/dsidavis/pdftohtml/files/4900776/03-alloc-dealloc-mismatch-HtmlString-.HtmlString.pdf)

