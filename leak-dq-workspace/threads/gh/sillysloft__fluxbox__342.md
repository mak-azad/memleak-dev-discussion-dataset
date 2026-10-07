# hang on exit, slit is probable cause

- URL: https://github.com/sillysloft/fluxbox/issues/342
- Repo: sillysloft/fluxbox (language: C++)
- State: open; created 2004-09-03T17:53:46Z; status ok; passes main

## Issue body

reporter (OWNER) · sillysloft · 2004-09-03T17:53:46Z · https://github.com/sillysloft/fluxbox/issues/342

I've seen this in both 0.9.9 and 0.9.10, compiled with
gcc 3.4.1 on x86 - when selecting "exit" from the
fluxbox menu, regular windows close but the slit
contents stay active and fluxbox hangs, using 100% cpu.

At the suggestion of someone on \#fluxbox, I read a
PKGBUILD file that he sent me and tried recompiling
with the slit disabled.  This fixed the problem, but I
still want the slit back.

Thanks for all your hard work, fluxbox is the greatest.


Reported by: realgeek

## Comment 348821370

reporter (OWNER) · sillysloft · 2004-10-22T10:24:37Z · https://github.com/sillysloft/fluxbox/issues/342#issuecomment-348821370

Logged In: NO 

When I "exit" fluxbox-0.9.10, it says
"free\(\): invalid pointer 0xb7e35420\!"
for example.
\(I built fluxbox with gcc-3.4.2.\)

==5939== ERROR SUMMARY: 2527 errors from 36 contexts \(suppressed: 0 from 0\)
==5939== 
==5939== 1 errors in context 1 of 36:
==5939== Invalid free\(\) / delete / delete\[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x809486C: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;Strut\*&gt; &gt;::deallocate\(std::\_List\_node&lt;Strut\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x8093DB7: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;Strut\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x8093927: std::list&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_erase\(std::\_List\_iterator&lt;Strut\*&gt;\) \(stl\_list.h:1172\)
==5939==  Address 0x34A77AF8 is 0 bytes inside a block of size 12 free'd
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x809486C: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;Strut\*&gt; &gt;::deallocate\(std::\_List\_node&lt;Strut\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x8093DB7: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;Strut\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x809271B: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_clear\(\) \(list.tcc:78\)
==5939== 
==5939== 1 errors in context 2 of 36:
==5939== Invalid read of size 4
==5939==    at 0x343D0696: std::\_List\_node\_base::unhook\(\) \(in /usr/lib/libstdc++.so.6.0.2\)
==5939==    by 0x8090DC3: std::list&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::erase\(std::\_List\_iterator&lt;Strut\*&gt;\) \(list.tcc:98\)
==5939==    by 0x808A1CA: BScreen::clearStrut\(Strut\*\) \(Screen.cc:1281\)
==5939==    by 0x809A7E8: Slit::clearStrut\(\) \(Slit.cc:348\)
==5939==  Address 0x34A77AFC is 4 bytes inside a block of size 12 free'd
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x809486C: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;Strut\*&gt; &gt;::deallocate\(std::\_List\_node&lt;Strut\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x8093DB7: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;Strut\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x809271B: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_clear\(\) \(list.tcc:78\)
==5939== 
==5939== 1 errors in context 3 of 36:
==5939== Invalid read of size 4
==5939==    at 0x343D0694: std::\_List\_node\_base::unhook\(\) \(in /usr/lib/libstdc++.so.6.0.2\)
==5939==    by 0x8090DC3: std::list&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::erase\(std::\_List\_iterator&lt;Strut\*&gt;\) \(list.tcc:98\)
==5939==    by 0x808A1CA: BScreen::clearStrut\(Strut\*\) \(Screen.cc:1281\)
==5939==    by 0x809A7E8: Slit::clearStrut\(\) \(Slit.cc:348\)
==5939==  Address 0x34A77AF8 is 0 bytes inside a block of size 12 free'd
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x809486C: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;Strut\*&gt; &gt;::deallocate\(std::\_List\_node&lt;Strut\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x8093DB7: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;Strut\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x809271B: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_clear\(\) \(list.tcc:78\)
==5939== 
==5939== 1 errors in context 4 of 36:
==5939== Invalid read of size 4
==5939==    at 0x8090DAA: std::list&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::erase\(std::\_List\_iterator&lt;Strut\*&gt;\) \(list.tcc:97\)
==5939==    by 0x808A1CA: BScreen::clearStrut\(Strut\*\) \(Screen.cc:1281\)
==5939==    by 0x809A7E8: Slit::clearStrut\(\) \(Slit.cc:348\)
==5939==    by 0x809A378: Slit::~Slit\(\) \(Slit.cc:339\)
==5939==  Address 0x34A77AF8 is 0 bytes inside a block of size 12 free'd
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x809486C: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;Strut\*&gt; &gt;::deallocate\(std::\_List\_node&lt;Strut\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x8093DB7: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;Strut\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x809271B: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_clear\(\) \(list.tcc:78\)
==5939== 
==5939== 1 errors in context 5 of 36:
==5939== Invalid read of size 4
==5939==    at 0x80938C7: std::\_List\_iterator&lt;Strut\*&gt; std::find&lt;std::\_List\_iterator&lt;Strut\*&gt;, Strut\*&gt;\(std::\_List\_iterator&lt;Strut\*&gt;, std::\_List\_iterator&lt;Strut\*&gt;, Strut\* const&, std::input\_iterator\_tag\) \(stl\_algo.h:172\)
==5939==    by 0x8090D74: std::\_List\_iterator&lt;Strut\*&gt; std::find&lt;std::\_List\_iterator&lt;Strut\*&gt;, Strut\*&gt;\(std::\_List\_iterator&lt;Strut\*&gt;, std::\_List\_iterator&lt;Strut\*&gt;, Strut\* const&\) \(stl\_algo.h:314\)
==5939==    by 0x808A17F: BScreen::clearStrut\(Strut\*\) \(Screen.cc:1278\)
==5939==    by 0x809A7E8: Slit::clearStrut\(\) \(Slit.cc:348\)
==5939==  Address 0x34A77B00 is 8 bytes inside a block of size 12 free'd
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x809486C: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;Strut\*&gt; &gt;::deallocate\(std::\_List\_node&lt;Strut\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x8093DB7: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;Strut\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x809271B: std::\_List\_base&lt;Strut\*, std::allocator&lt;Strut\*&gt; &gt;::\_M\_clear\(\) \(list.tcc:78\)
==5939== 
==5939== 1 errors in context 6 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F3129: ClockTool::update\(FbTk::Subject\*\) \(ClockTool.cc:211\)
==5939==    by 0x81377C9: std::mem\_fun1\_t&lt;void, FbTk::Observer, FbTk::Subject\*&gt;::operator\(\)\(FbTk::Observer\*, FbTk::Subject\*\) const \(stl\_function.h:792\)
==5939==  Address 0x34A2FDA0 is 0 bytes inside a block of size 28 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F3129: ClockTool::update\(FbTk::Subject\*\) \(ClockTool.cc:211\)
==5939== 
==5939== 1 errors in context 7 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F31A9: ClockTool::update\(FbTk::Subject\*\) \(ClockTool.cc:213\)
==5939==    by 0x80F2A1C: ClockTool::ClockTool\(FbTk::FbWindow const&, ToolTheme&, BScreen&, FbTk::Menu&\) \(ClockTool.cc:166\)
==5939==  Address 0x34B39F00 is 0 bytes inside a block of size 28 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F31A9: ClockTool::update\(FbTk::Subject\*\) \(ClockTool.cc:213\)
==5939== 
==5939== 1 errors in context 8 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F3129: ClockTool::update\(FbTk::Subject\*\) \(ClockTool.cc:211\)
==5939==    by 0x80F2A1C: ClockTool::ClockTool\(FbTk::FbWindow const&, ToolTheme&, BScreen&, FbTk::Menu&\) \(ClockTool.cc:166\)
==5939==  Address 0x34B39E78 is 0 bytes inside a block of size 28 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F3129: ClockTool::update\(FbTk::Subject\*\) \(ClockTool.cc:211\)
==5939== 
==5939== 1 errors in context 9 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x808D632: BScreen::renderPosWindow\(\) \(Screen.cc:2051\)
==5939==    by 0x80846B2: BScreen::BScreen\(FbTk::ResourceManager&, std::string const&, std::string const&, int, int\) \(Screen.cc:338\)
==5939==  Address 0x34B0D7C0 is 0 bytes inside a block of size 68 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x808D632: BScreen::renderPosWindow\(\) \(Screen.cc:2051\)
==5939== 
==5939== 1 errors in context 10 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x808D2D8: BScreen::renderGeomWindow\(\) \(Screen.cc:2006\)
==5939==    by 0x80845D6: BScreen::BScreen\(FbTk::ResourceManager&, std::string const&, std::string const&, int, int\) \(Screen.cc:329\)
==5939==  Address 0x3562B1B0 is 0 bytes inside a block of size 68 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x808D2D8: BScreen::renderGeomWindow\(\) \(Screen.cc:2006\)
==5939== 
==5939== 1 errors in context 11 of 36:
==5939== Source and destination overlap in memcpy\(0x34AF9028, 0x34AF9028, 200\)
==5939==    at 0x3414886B: memcpy \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x342DB81E: \_bdf\_readstream \(in /usr/lib/libfreetype.so.6.3.3\)
==5939== 
==5939== 2 errors in context 12 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x808D632: BScreen::renderPosWindow\(\) \(Screen.cc:2051\)
==5939==    by 0x8087B96: BScreen::update\(FbTk::Subject\*\) \(Screen.cc:610\)
==5939==  Address 0x34A1FEF8 is 0 bytes inside a block of size 68 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x808D632: BScreen::renderPosWindow\(\) \(Screen.cc:2051\)
==5939== 
==5939== 2 errors in context 13 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x808D2D8: BScreen::renderGeomWindow\(\) \(Screen.cc:2006\)
==5939==    by 0x8087B88: BScreen::update\(FbTk::Subject\*\) \(Screen.cc:609\)
==5939==  Address 0x34A1A720 is 0 bytes inside a block of size 68 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x808D2D8: BScreen::renderGeomWindow\(\) \(Screen.cc:2006\)
==5939== 
==5939== 2 errors in context 14 of 36:
==5939== Invalid read of size 1
==5939==    at 0x341486E6: strcmp \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CE364: \(within /lib/libc-2.3.2.so\)
==5939==    by 0x344CDBD5: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB72: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:164\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 2 errors in context 15 of 36:
==5939== Invalid read of size 1
==5939==    at 0x341486E6: strcmp \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CE34B: \(within /lib/libc-2.3.2.so\)
==5939==    by 0x344CDBD5: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB72: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:164\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 2 errors in context 16 of 36:
==5939== Invalid read of size 1
==5939==    at 0x344CE324: \(within /lib/libc-2.3.2.so\)
==5939==    by 0x344CDBD5: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB72: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:164\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 2 errors in context 17 of 36:
==5939== Invalid read of size 1
==5939==    at 0x344CE313: \(within /lib/libc-2.3.2.so\)
==5939==    by 0x344CDBD5: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB72: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:164\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 2 errors in context 18 of 36:
==5939== Invalid read of size 1
==5939==    at 0x341486E6: strcmp \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDB4E: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB72: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:164\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 3 errors in context 19 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810D162: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:490\)
==5939==    by 0x812F6A6: FbTk::TextButton::drawText\(int, int\) \(TextButton.cc:146\)
==5939==    by 0x80FFD61: IconButton::drawText\(int, int\) \(IconButton.cc:243\)
==5939==  Address 0x3562C150 is 0 bytes inside a block of size 24 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CCE6: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:438\)
==5939==    by 0x812F6A6: FbTk::TextButton::drawText\(int, int\) \(TextButton.cc:146\)
==5939== 
==5939== 4 errors in context 20 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939==    by 0x80F4AE0: WorkspaceNameTool::update\(FbTk::Subject\*\) \(WorkspaceNameTool.cc:73\)
==5939==  Address 0x34A07408 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939== 
==5939== 7 errors in context 21 of 36:
==5939== Invalid read of size 4
==5939==    at 0x812BD55: std::\_List\_iterator&lt;FbTk::Timer\*&gt;::operator--\(int\) \(stl\_list.h:162\)
==5939==    by 0x806A143: Fluxbox::eventLoop\(\) \(fluxbox.cc:708\)
==5939==    by 0x807CDD2: main \(main.cc:254\)
==5939==  Address 0x34B61A8C is 4 bytes inside a block of size 12 free'd
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x812C08E: \_\_gnu\_cxx::new\_allocator&lt;std::\_List\_node&lt;FbTk::Timer\*&gt; &gt;::deallocate\(std::\_List\_node&lt;FbTk::Timer\*&gt;\*, unsigned\) \(new\_allocator.h:86\)
==5939==    by 0x812C025: std::\_List\_base&lt;FbTk::Timer\*, std::allocator&lt;FbTk::Timer\*&gt; &gt;::\_M\_put\_node\(std::\_List\_node&lt;FbTk::Timer\*&gt;\*\) \(stl\_list.h:313\)
==5939==    by 0x812BF6B: std::list&lt;FbTk::Timer\*, std::allocator&lt;FbTk::Timer\*&gt; &gt;::\_M\_erase\(std::\_List\_iterator&lt;FbTk::Timer\*&gt;\) \(stl\_list.h:1172\)
==5939== 
==5939== 8 errors in context 22 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939==    by 0x80ED6DC: Toolbar::rearrangeItems\(\) \(Toolbar.cc:998\)
==5939==  Address 0x3468D7B0 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939== 
==5939== 8 errors in context 23 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939==    by 0x80ED68D: Toolbar::rearrangeItems\(\) \(Toolbar.cc:994\)
==5939==  Address 0x34606D80 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939== 
==5939== 8 errors in context 24 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939==    by 0x80ED304: Toolbar::rearrangeItems\(\) \(Toolbar.cc:930\)
==5939==  Address 0x345F2D90 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939== 
==5939== 14 errors in context 25 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x8120E8E: FbTk::doAlignment\(int, int, FbTk::Justify, FbTk::Font const&, char const\*, unsigned, unsigned&\) \(Text.cc:45\)
==5939==    by 0x812F5C0: FbTk::TextButton::drawText\(int, int\) \(TextButton.cc:136\)
==5939==  Address 0x34B5DFC0 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x8120E8E: FbTk::doAlignment\(int, int, FbTk::Justify, FbTk::Font const&, char const\*, unsigned, unsigned&\) \(Text.cc:45\)
==5939== 
==5939== 16 errors in context 26 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810D162: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:490\)
==5939==    by 0x812F6A6: FbTk::TextButton::drawText\(int, int\) \(TextButton.cc:146\)
==5939==    by 0x812F3C0: FbTk::TextButton::clearArea\(int, int, unsigned, unsigned, bool\) \(TextButton.cc:109\)
==5939==  Address 0x34B5E070 is 0 bytes inside a block of size 4 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CCE6: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:438\)
==5939==    by 0x812F6A6: FbTk::TextButton::drawText\(int, int\) \(TextButton.cc:146\)
==5939== 
==5939== 16 errors in context 27 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939==    by 0x80F4E0A: WorkspaceNameTool::renderTheme\(\) \(WorkspaceNameTool.cc:122\)
==5939==  Address 0x34B5DAD8 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x80F4C56: WorkspaceNameTool::width\(\) const \(WorkspaceNameTool.cc:86\)
==5939== 
==5939== 20 errors in context 28 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810D162: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:490\)
==5939==    by 0x8115E98: FbTk::Menu::redrawTitle\(\) \(Menu.cc:791\)
==5939==    by 0x8117C07: FbTk::Menu::exposeEvent\(XExposeEvent&\) \(Menu.cc:1291\)
==5939==  Address 0x34A96738 is 0 bytes inside a block of size 28 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CCE6: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:438\)
==5939==    by 0x8115E98: FbTk::Menu::redrawTitle\(\) \(Menu.cc:791\)
==5939== 
==5939== 20 errors in context 29 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x8115C3F: FbTk::Menu::redrawTitle\(\) \(Menu.cc:763\)
==5939==    by 0x8117C07: FbTk::Menu::exposeEvent\(XExposeEvent&\) \(Menu.cc:1291\)
==5939==  Address 0x34A7EB98 is 0 bytes inside a block of size 28 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x8115C3F: FbTk::Menu::redrawTitle\(\) \(Menu.cc:763\)
==5939== 
==5939== 20 errors in context 30 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x8120E5A: FbTk::doAlignment\(int, int, FbTk::Justify, FbTk::Font const&, char const\*, unsigned, unsigned&\) \(Text.cc:40\)
==5939==    by 0x812F5C0: FbTk::TextButton::drawText\(int, int\) \(TextButton.cc:136\)
==5939==  Address 0x34B5DF80 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x8120E5A: FbTk::doAlignment\(int, int, FbTk::Justify, FbTk::Font const&, char const\*, unsigned, unsigned&\) \(Text.cc:40\)
==5939== 
==5939== 26 errors in context 31 of 36:
==5939== Invalid read of size 1
==5939==    at 0x341486E6: strcmp \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDB4E: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EDA8: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:210\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 26 errors in context 32 of 36:
==5939== Invalid read of size 1
==5939==    at 0x341486E6: strcmp \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CEC39: \(within /lib/libc-2.3.2.so\)
==5939==    by 0x344CE37F: \(within /lib/libc-2.3.2.so\)
==5939==    by 0x344CDBD5: setlocale \(in /lib/libc-2.3.2.so\)
==5939==  Address 0x345E6568 is 0 bytes inside a block of size 13 free'd
==5939==    at 0x341477F9: free \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344CDC75: setlocale \(in /lib/libc-2.3.2.so\)
==5939==    by 0x813EB30: \(anonymous namespace\)::createFontSet\(char const\*, bool\) \(XmbFontImp.cc:161\)
==5939==    by 0x813F1BA: FbTk::XmbFontImp::load\(std::string const&\) \(XmbFontImp.cc:233\)
==5939== 
==5939== 130 errors in context 33 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x8114700: FbTk::Menu::update\(int\) \(Menu.cc:423\)
==5939==    by 0x80BFC41: FbMenu::update\(int\) \(FbMenu.cc:43\)
==5939==  Address 0x34B0E5D8 is 0 bytes inside a block of size 12 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x8114700: FbTk::Menu::update\(int\) \(Menu.cc:423\)
==5939== 
==5939== 722 errors in context 34 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x811AA9B: FbTk::MenuItem::width\(FbTk::MenuTheme const&\) const \(MenuItem.cc:247\)
==5939==    by 0x81147BA: FbTk::Menu::update\(int\) \(Menu.cc:434\)
==5939==  Address 0x34A7D2C0 is 0 bytes inside a block of size 56 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x811AA9B: FbTk::MenuItem::width\(FbTk::MenuTheme const&\) const \(MenuItem.cc:247\)
==5939== 
==5939== 727 errors in context 35 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810D162: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:490\)
==5939==    by 0x811A312: FbTk::MenuItem::draw\(FbTk::FbDrawable&, FbTk::MenuTheme const&, bool, int, int, unsigned, unsigned\) const \(MenuItem.cc:110\)
==5939==    by 0x8116EA0: FbTk::Menu::drawItem\(unsigned, bool, bool, int, int, unsigned, unsigned\) \(Menu.cc:1001\)
==5939==  Address 0x34A7E730 is 0 bytes inside a block of size 56 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CCE6: FbTk::Font::drawText\(unsigned long, int, \_XGC\*, char const\*, unsigned, int, int, bool\) const \(Font.cc:438\)
==5939==    by 0x811A312: FbTk::MenuItem::draw\(FbTk::FbDrawable&, FbTk::MenuTheme const&, bool, int, int, unsigned, unsigned\) const \(MenuItem.cc:110\)
==5939== 
==5939== 727 errors in context 36 of 36:
==5939== Mismatched free\(\) / delete / delete \[\]
==5939==    at 0x34147997: operator delete\(void\*\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810CBE3: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:406\)
==5939==    by 0x811A1A4: FbTk::MenuItem::draw\(FbTk::FbDrawable&, FbTk::MenuTheme const&, bool, int, int, unsigned, unsigned\) const \(MenuItem.cc:92\)
==5939==    by 0x8116EA0: FbTk::Menu::drawItem\(unsigned, bool, bool, int, int, unsigned, unsigned\) \(Menu.cc:1001\)
==5939==  Address 0x34A7E6C8 is 0 bytes inside a block of size 56 alloc'd
==5939==    at 0x3414768D: operator new\[\]\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x810ADFE: \(anonymous namespace\)::recode\(void\*, char const\*, unsigned\) \(Font.cc:118\)
==5939==    by 0x810CB6A: FbTk::Font::textWidth\(char const\*, unsigned\) const \(Font.cc:401\)
==5939==    by 0x811A1A4: FbTk::MenuItem::draw\(FbTk::FbDrawable&, FbTk::MenuTheme const&, bool, int, int, unsigned, unsigned\) const \(MenuItem.cc:92\)
==5939== IN SUMMARY: 2527 errors from 36 contexts \(suppressed: 0 from 0\)
==5939== 
==5939== malloc/free: in use at exit: 198909 bytes in 1970 blocks.
==5939== malloc/free: 116243 allocs, 114274 frees, 41840838 bytes allocated.
==5939== 
==5939== searching for pointers to 1970 not-freed blocks.
==5939== checked 6425928 bytes.
==5939== 
==5939== 
==5939== 16 bytes in 2 blocks are definitely lost in loss record 17 of 101
==5939==    at 0x34147D42: realloc \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x3422BF3E: \(within /usr/X11R6/lib/libX11.so.6.2\)
==5939== 
==5939== 
==5939== 32 bytes in 2 blocks are definitely lost in loss record 31 of 101
==5939==    at 0x341472D8: malloc \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x342A3957: FcPatternCreate \(in /usr/lib/libfontconfig.so.1.0.4\)
==5939== 
==5939== 
==5939== 276 bytes in 11 blocks are possibly lost in loss record 63 of 101
==5939==    at 0x3414744F: operator new\(unsigned\) \(in /usr/lib/valgrind/vgpreload\_addrcheck.so\)
==5939==    by 0x344137E5: std::string::\_Rep::\_S\_create\(unsigned, unsigned, std::allocator&lt;char&gt; const&\) \(in /usr/lib/libstdc++.so.6.0.2\)
==5939==    by 0x808EEA6: FocusModelMenuItem::FocusModelMenuItem\(char const\*, BScreen&, BScreen::FocusModel, FbTk::RefCount&lt;FbTk::Command&gt;&\) \(FocusModelMenuItem.hh:39\)
==5939==    by 0x808C033: BScreen::setupConfigmenu\(FbTk::Menu&\) \(Screen.cc:1760\)
==5939== 
==5939== LEAK SUMMARY:
==5939==    definitely lost: 48 bytes in 4 blocks.
==5939==    possibly lost:   276 bytes in 11 blocks.
==5939==    still reachable: 198585 bytes in 1955 blocks.
==5939==         suppressed: 0 bytes in 0 blocks.
==5939== Reachable blocks \(those to which a pointer was found\) are not shown.
==5939== To see them, rerun with: --show-reachable=yes
\--5939--     TT/TC: 0 tc sectors discarded.
\--5939--            98552 tt\_fast misses.
\--5939-- translate: new     50339 \(798001 -&gt; 7070105; ratio 88:10\)
\--5939--            discard 99 \(1594 -&gt; 12564; ratio 78:10\).
\--5939-- chainings: 36334 chainings, 0 unchainings.
\--5939--  dispatch: 25850000 jumps \(bb entries\); of them 17313016 \(66%\) unchained.
\--5939--            32350/356204 major/minor sched events.
\--5939-- reg-alloc: 91 t-req-spill, 1342857+244 orig+spill uis,
\--5939--            123710 total-reg-rank
\--5939--    sanity: 31805 cheap, 1273 expensive checks.
\--5939--    ccalls: 298653 C calls, 60% saves+restores avoided \(1057818 bytes\)
\--5939--            298819 args, avg 0.53 setup instrs each \(275106 bytes\)
\--5939--            0% clear the stack \(895959 bytes\)
\--5939--            0 retvals, 100% of reg-reg movs avoided \(0 bytes\)


Original comment by: nobody

## Comment 348821371

reporter (OWNER) · sillysloft · 2004-10-24T13:02:18Z · https://github.com/sillysloft/fluxbox/issues/342#issuecomment-348821371

Logged In: NO 

Slit::saveClientList\(\) is the root of this problem.
My fluxbox seems hanging on std::ofstream
file\(FbTk::StringUtil::expandFilename\(m\_filename\).c\_str\(\)\);


Original comment by: nobody

## Comment 348821372

reporter (OWNER) · sillysloft · 2004-11-11T11:06:21Z · https://github.com/sillysloft/fluxbox/issues/342#issuecomment-348821372

Logged In: NO 

I saw the same problem, and
I rebuilt it with gcc-3.2. Then it works fine\!
Probably this is a bug in gcc-3.4.


Original comment by: nobody

## Comment 348821373

reporter (OWNER) · sillysloft · 2004-11-15T22:08:31Z · https://github.com/sillysloft/fluxbox/issues/342#issuecomment-348821373

Logged In: YES 
user\_id=696996

I bootstrapped gcc,g++ 3.4.3 today and built fluxbox-0.9.10
with it, the problem goes away.  I'll assume this was a
compiler bug and mark this thread closed.  Thanks again for
the input from everyone.


Original comment by: realgeek

## Comment 348821374

reporter (OWNER) · sillysloft · 2004-11-15T22:08:31Z · https://github.com/sillysloft/fluxbox/issues/342#issuecomment-348821374

- **status**: open --> closed

Original comment by: realgeek
