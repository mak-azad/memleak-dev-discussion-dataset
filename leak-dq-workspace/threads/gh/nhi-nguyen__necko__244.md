# 1587534 - ASAN failure: ERROR: AddressSanitizer: requested allocation size 0x7ffaf606e0f0 (0x7ffaf606f0f0 after adjustments for alignment, red zones etc.) exceeds maximum supported size of 0x10000000000

- URL: https://github.com/nhi-nguyen/necko/issues/244
- Repo: nhi-nguyen/necko (language: None)
- State: open; created 2019-10-16T20:22:34Z; status ok; passes main

## Issue body

reporter (OWNER) · nhi-nguyen · 2019-10-16T20:22:34Z · https://github.com/nhi-nguyen/necko/issues/244

https://bugzilla.mozilla.org/show_bug.cgi?id=1587534

https://treeherder.mozilla.org/logviewer.html#/jobs?job_id=270243806&repo=try&lineNumber=11154

Call stack:
```
#0 0x7ffb2aed4610 in malloc Z:\task_1569588313\fetches\llvm-project\llvm\projects\compiler-rt\lib\asan\asan_malloc_win.cc:69
#1 0x7ffaf562a14a in nsIncrementalStreamLoader::OnStartRequest z:\build\build\src\netwerk\base\nsIncrementalStreamLoader.cpp:66
#2 0x7ffaf5fc29d2 in mozilla::net::HttpChannelChild::DoOnStartRequest z:\build\build\src\netwerk\protocol\http\HttpChannelChild.cpp:682
#3 0x7ffaf5fcdca7 in mozilla::net::HttpChannelChild::OnStartRequest z:\build\build\src\netwerk\protocol\http\HttpChannelChild.cpp:607
#4 0x7ffaf607851f in mozilla::net::StartRequestEvent::Run z:\build\build\src\netwerk\protocol\http\HttpChannelChild.cpp:426
#5 0x7ffaf5e770d8 in mozilla::net::ChannelEventQueue::RunOrEnqueue z:\build\build\src\obj-firefox\dist\include\mozilla\net\ChannelEventQueue.h:210
#6 0x7ffaf5fcbe95 in mozilla::net::HttpChannelChild::RecvOnStartRequest z:\build\build\src\netwerk\protocol\http\HttpChannelChild.cpp:488
#7 0x7ffaf6a4bdf4 in mozilla::net::PHttpChannelChild::OnMessageReceived z:\build\build\src\obj-firefox\ipc\ipdl\PHttpChannelChild.cpp:833
#8 0x7ffaf67eccbf in mozilla::dom::PContentChild::OnMessageReceived z:\build\build\src\obj-firefox\ipc\ipdl\PContentChild.cpp:7879
#9 0x7ffaf65bff5a in mozilla::ipc::MessageChannel::DispatchAsyncMessage z:\build\build\src\ipc\glue\MessageChannel.cpp:2185
#10 0x7ffaf65bbafd in mozilla::ipc::MessageChannel::DispatchMessage z:\build\build\src\ipc\glue\MessageChannel.cpp:2109
#11 0x7ffaf65bdc44 in mozilla::ipc::MessageChannel::RunMessage z:\build\build\src\ipc\glue\MessageChannel.cpp:1954
#12 0x7ffaf65be2f5 in mozilla::ipc::MessageChannel::MessageTask::Run z:\build\build\src\ipc\glue\MessageChannel.cpp:1985
#13 0x7ffaf53359a5 in mozilla::SchedulerGroup::Runnable::Run z:\build\build\src\xpcom\threads\SchedulerGroup.cpp:295
#14 0x7ffaf53637e9 in nsThread::ProcessNextEvent z:\build\build\src\xpcom\threads\nsThread.cpp:1225
#15 0x7ffaf536cd48 in NS_ProcessNextEvent z:\build\build\src\xpcom\threads\nsThreadUtils.cpp:486
#16 0x7ffaf65c814f in mozilla::ipc::MessagePump::Run z:\build\build\src\ipc\glue\MessagePump.cpp:88
#17 0x7ffaf65010ae in MessageLoop::RunHandler z:\build\build\src\ipc\chromium\src\base\message_loop.cc:308
#18 0x7ffaf6500e45 in MessageLoop::Run z:\build\build\src\ipc\chromium\src\base\message_loop.cc:290
#19 0x7ffaffeb63ea in nsBaseAppShell::Run z:\build\build\src\widget\nsBaseAppShell.cpp:137
#20 0x7ffb0004dc18 in nsAppShell::Run z:\build\build\src\widget\windows\nsAppShell.cpp:406
#21 0x7ffb041bf1ed in XRE_RunAppShell z:\build\build\src\toolkit\xre\nsEmbedFunctions.cpp:934
#22 0x7ffaf65010ae in MessageLoop::RunHandler z:\build\build\src\ipc\chromium\src\base\message_loop.cc:308
#23 0x7ffaf6500e45 in MessageLoop::Run z:\build\build\src\ipc\chromium\src\base\message_loop.cc:290
#24 0x7ffb041be3d5 in XRE_InitChildProcess z:\build\build\src\toolkit\xre\nsEmbedFunctions.cpp:769
#25 0x7ff60c2020f4 in NS_internal_main z:\build\build\src\browser\app\nsBrowserApp.cpp:273
#26 0x7ff60c2014f2 in wmain z:\build\build\src\toolkit\xre\nsWindowsWMain.cpp:131
#27 0x7ff60c2fc0d7 in __scrt_common_main_seh f:\dd\vctools\crt\vcstartup\src\startup\exe_common.inl:288
#28 0x7ffb433e3033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180013033)
#29 0x7ffb43f31460 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180071460)
```

The scary part to me is that the allocation length looks a lot like a pointer to something on the stack.


