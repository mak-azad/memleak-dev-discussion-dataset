# Memory leak: Investigate valgrind output after #1073

- URL: https://github.com/jamulussoftware/jamulus/issues/1083
- Repo: jamulussoftware/jamulus (language: C)
- State: open; created 2021-02-21T12:08:24Z; status ok; passes main

## Issue body

reporter (MEMBER) · hoffie · 2021-02-21T12:08:24Z · https://github.com/jamulussoftware/jamulus/issues/1083

**Describe the bug**
<!-- A clear and concise description of what the bug is. -->
Even after #1073, valgrind shows some possible leaks. These should be investigated.

Note: I'm not entirely sure if they are real or relevant leaks. I suppose there may be some ressources which are not destroyed explicitly when Jamlus shuts down. This would be not relevant in the real world, but would probably still be shown as a possible leak by valgrind.

So, I'm not saying that all of the outputs are worth fixing, I'm just proposing to investigate their validity and relevance.

**To Reproduce**
<!-- Steps to reproduce the behavior: -->
```
$ valgrind --leak-check=full ./Jamulus -s -n -p 10001 -e localhost:10000 -l /tmp/log -R /tmp/recordings -o 'Private Server;Stockholm;205' -m /tmp/jam.dat -u 40 -T -w 'Welcome!'

$ for x in {1..12}; do Jamulus -c localhost:10001 --nogui --inifile /tmp/x &; done

# leave running for some minutes
# Ctrl+C and wait for exit (takes a rather long time, possibly due to valgrind overhead + recording finishing?)
```

**Expected behavior**
No leaks.

**Screenshots**
<!-- If applicable, add screenshots to help explain your problem. -->
```
==3121== 
==3121== HEAP SUMMARY:
==3121==     in use at exit: 8,560,244 bytes in 1,231 blocks
==3121==   total heap usage: 11,163,830 allocs, 11,162,599 frees, 3,097,366,260 bytes allocated
==3121== 
==3121== 352 bytes in 1 blocks are possibly lost in loss record 110 of 156
==3121==    at 0x483CB65: calloc (vg_replace_malloc.c:760)
==3121==    by 0x40142EB: _dl_allocate_tls (in /usr/lib/ld-2.32.so)
==3121==    by 0x48C913C: pthread_create@@GLIBC_2.2.5 (in /usr/lib/libpthread-2.32.so)
==3121==    by 0x58D79A2: QThread::start(QThread::Priority) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x15C7D2: CServer::CServer(int, QString const&, unsigned short, QString const&, QString const&, QString const&, QString const&, QString const&, QString const&, QString const&, bool, bool, bool, bool, ELicenceType) (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x13CD8F: main (in /home/christian/Projects/jamulus/Jamulus)
==3121== 
==3121== 352 bytes in 1 blocks are possibly lost in loss record 111 of 156
==3121==    at 0x483CB65: calloc (vg_replace_malloc.c:760)
==3121==    by 0x40142EB: _dl_allocate_tls (in /usr/lib/ld-2.32.so)
==3121==    by 0x48C913C: pthread_create@@GLIBC_2.2.5 (in /usr/lib/libpthread-2.32.so)
==3121==    by 0x58D79A2: QThread::start(QThread::Priority) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x156F4F: CServer::Start() (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x5AEC4BE: QObject::event(QEvent*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5ABFA4F: QCoreApplication::notifyInternal2(QObject*, QEvent*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5AC2572: QCoreApplicationPrivate::sendPostedEvents(QObject*, int, QThreadData*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5B190A3: ??? (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x7147A83: g_main_context_dispatch (in /usr/lib/libglib-2.0.so.0.6600.4)
==3121==    by 0x719B9B0: ??? (in /usr/lib/libglib-2.0.so.0.6600.4)
==3121==    by 0x71462B0: g_main_context_iteration (in /usr/lib/libglib-2.0.so.0.6600.4)
==3121== 
==3121== 1,408 bytes in 4 blocks are possibly lost in loss record 135 of 156
==3121==    at 0x483CB65: calloc (vg_replace_malloc.c:760)
==3121==    by 0x40142EB: _dl_allocate_tls (in /usr/lib/ld-2.32.so)
==3121==    by 0x48C913C: pthread_create@@GLIBC_2.2.5 (in /usr/lib/libpthread-2.32.so)
==3121==    by 0x58D79A2: QThread::start(QThread::Priority) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x58DA754: QThreadPoolPrivate::startThread(QRunnable*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x58DBB13: QThreadPoolPrivate::tryStart(QRunnable*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x58DC327: QThreadPool::start(QRunnable*, int) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x19276F: QFuture<void> QtConcurrent::run<void, CServer, int, int, int, int, int, int>(CServer*, void (CServer::*)(int, int, int), int const&, int const&, int const&) (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x15A393: CServer::OnTimer() (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x5AEC581: QObject::event(QEvent*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5ABFA4F: QCoreApplication::notifyInternal2(QObject*, QEvent*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5AC2572: QCoreApplicationPrivate::sendPostedEvents(QObject*, int, QThreadData*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121== 
==3121== 1,824 (16 direct, 1,808 indirect) bytes in 1 blocks are definitely lost in loss record 138 of 156
==3121==    at 0x483ADEF: operator new(unsigned long) (vg_replace_malloc.c:342)
==3121==    by 0x155F3A: recorder::CJamController::SetRecordingDir(QString, int, bool) (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x15B799: CServer::CServer(int, QString const&, unsigned short, QString const&, QString const&, QString const&, QString const&, QString const&, QString const&, QString const&, bool, bool, bool, bool, ELicenceType) (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x13CD8F: main (in /home/christian/Projects/jamulus/Jamulus)
==3121== 
==3121== 9,504 bytes in 27 blocks are possibly lost in loss record 153 of 156
==3121==    at 0x483CB65: calloc (vg_replace_malloc.c:760)
==3121==    by 0x40142EB: _dl_allocate_tls (in /usr/lib/ld-2.32.so)
==3121==    by 0x48C913C: pthread_create@@GLIBC_2.2.5 (in /usr/lib/libpthread-2.32.so)
==3121==    by 0x58D79A2: QThread::start(QThread::Priority) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x58DA754: QThreadPoolPrivate::startThread(QRunnable*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x58DBB13: QThreadPoolPrivate::tryStart(QRunnable*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x58DC327: QThreadPool::start(QRunnable*, int) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x19276F: QFuture<void> QtConcurrent::run<void, CServer, int, int, int, int, int, int>(CServer*, void (CServer::*)(int, int, int), int const&, int const&, int const&) (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x15A015: CServer::OnTimer() (in /home/christian/Projects/jamulus/Jamulus)
==3121==    by 0x5AEC581: QObject::event(QEvent*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5ABFA4F: QCoreApplication::notifyInternal2(QObject*, QEvent*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121==    by 0x5AC2572: QCoreApplicationPrivate::sendPostedEvents(QObject*, int, QThreadData*) (in /usr/lib/libQt5Core.so.5.15.2)
==3121== 
==3121== LEAK SUMMARY:
==3121==    definitely lost: 16 bytes in 1 blocks
==3121==    indirectly lost: 1,808 bytes in 10 blocks
==3121==      possibly lost: 11,616 bytes in 33 blocks
==3121==    still reachable: 8,546,804 bytes in 1,187 blocks
==3121==         suppressed: 0 bytes in 0 blocks
==3121== Reachable blocks (those to which a pointer was found) are not shown.
```

**Operating system**
<!-- Add the operating system you are running, e.g. Windows 10 Version 20H2, macOS 10.15.5, Ubuntu Linux 20.10. Also add where you got Jamulus from, e.g. if you downloaded it from the internet, if you got it from your Linux distribution or if you built from source. -->
```Linux wuechoo 5.10.9-arch1-1 #1 SMP PREEMPT Tue, 19 Jan 2021 22:06:06 +0000 x86_64 GNU/Linux
```

**Version of Jamulus**
<!-- Get this from the Help > About menu or from the `Jamulus --version` command line -->
3.6.2dev-a26ff711 (= #1073)

@softins Are you already planning to look further into this? I can try my luck, but you seem way more proficient in tracking such things down. :)

## Comment 782849624

maintainer (MEMBER) · softins · 2021-02-21T12:25:16Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-782849624

Yes, I am planning to continue the investigation. I'll look at SetRecordingDir first, as it relates to my active PR. The thread ones appear to be related to the multithreading. Could you repeat the test without -T?

## Comment 782854874

maintainer (MEMBER) · softins · 2021-02-21T13:03:13Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-782854874

> ```
> $ valgrind --leak-check=full ./Jamulus -s -n -p 10001 -e localhost:10000 -l /tmp/log -R /tmp/recordings -o 'Private Server;Stockholm;205' -m /tmp/jam.dat -u 40 -T -w 'Welcome!'
> 
> $ for x in {1..12}; do Jamulus -c localhost:10001 --nogui --inifile /tmp/x &; done
> 
> # leave running for some minutes
> # Ctrl+C and wait for exit (takes a rather long time, possibly due to valgrind overhead + recording finishing?)
> ```

I think it would be better to kill the clients first, then leave a significant time for things to settle before terminating the server. If the server is killed with active sessions, we might get false positives, reporting memory that would have been freed on disconnect.

I think the one in `SetRecordingDir()` might be a case in point.

## Comment 782949760

reporter (MEMBER) · hoffie · 2021-02-21T23:28:57Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-782949760

> I think it would be better to kill the clients first

I think I did, will make sure in my next test tomorrow.

> Could you repeat the test without -T?

Will do.

Independent of valgrind I have run a test with 33 clients and no recording/-T. Memory was stable over hours. When adding multithreading there was a sudden increase after some seconds/minutes, but it then seemed stable. I think some more thorough tests should be done, but it would not be high on my list. I will do the repeated valgrind tests though.

## Comment 817183815

maintainer (MEMBER) · ann0see · 2021-04-10T18:28:50Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-817183815

Is this still in progress?

## Comment 817184540

reporter (MEMBER) · hoffie · 2021-04-10T18:34:09Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-817184540

I did not get around to working on it recently. I still think this should be analyzed properly. Keeping it open, but moving it to Backlog for that reason. Feel free to take over.

## Comment 817203292

maintainer (MEMBER) · ann0see · 2021-04-10T21:16:09Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-817203292

Ok. 

## Comment 819837208

other (CONTRIBUTOR) · genesisproject2020 · 2021-04-14T21:14:23Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-819837208

I have some memory logging on my Jamulus processes and below are three of them from last week. I thought it was a correlation between memory allocation and users. The first one is an open server and the two others are private servers but the config is the same. Something is not ok but I have a hard time to figure out what. I'm running 3.7.0 on the first one and 3.7.0dev-664fd9ed on the other two.

<img width="1399" alt="Skärmavbild 2021-04-14 1" src="https://user-images.githubusercontent.com/7592139/114779217-1f31ef00-9d76-11eb-9080-8d2dc84bd038.png">
<img width="1394" alt="Skärmavbild 2021-04-14 30" src="https://user-images.githubusercontent.com/7592139/114779223-20fbb280-9d76-11eb-868a-2350b7d9292f.png">
<img width="1394" alt="Skärmavbild 2021-04-14 36" src="https://user-images.githubusercontent.com/7592139/114779226-21944900-9d76-11eb-9154-9086173b2db5.png">


## Comment 1616087868

maintainer (MEMBER) · ann0see · 2023-07-01T20:20:05Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-1616087868

Tagging as 3.11.0 just to look at it again.

## Comment 1660829664

maintainer (COLLABORATOR) · pljones · 2023-08-01T18:01:38Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-1660829664

We'll need to validate for each target, too, if we're going to clean up fully.  Maybe break it down per target for actual investigation, as it might need different people working on it - make it easier to target fixes coming into different future releases.

## Comment 1685071061

maintainer (COLLABORATOR) · pljones · 2023-08-19T17:46:37Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-1685071061

@ann0see are you okay to assign yourself to this?

## Comment 1685091160

maintainer (MEMBER) · ann0see · 2023-08-19T19:38:23Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-1685091160

No. I'm not confident enough with the topic. 

## Comment 1685229766

maintainer (COLLABORATOR) · pljones · 2023-08-20T08:58:54Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-1685229766

OK, maybe we could drop it from 3.11.0 unless someone can pick it up -- it's not something I'd be comfortable with, either.

## Comment 5130571023

maintainer (MEMBER) · ann0see · 2026-07-30T12:03:12Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-5130571023

This was closed automatically. If there's still something unfixed, we should re open this. 

## Comment 5134335988

maintainer (COLLABORATOR) · pljones · 2026-07-30T17:48:24Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-5134335988

Can we split it into separate issues if there are multiple problems that need fixing?

## Comment 5739709144

other (CONTRIBUTOR) · mcfnord · 2026-09-19T05:39:25Z · https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-5739709144

**🤖 AI:** One site remains. Re-measured at [`cc40a8a9`](https://github.com/jamulussoftware/jamulus/commit/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba) with the command from the description, 12 headless clients for 180 s, run twice — once with `-T` and once without. Every question on this thread, in the order asked.

> I'm not entirely sure if they are real or relevant leaks.

One is real. The run leaves **864 bytes definitely lost in one block**, plus 1,304 bytes in 10 blocks indirectly through it, against the 8,560,244 bytes in 1,231 blocks recorded in the description after [#1073](https://github.com/jamulussoftware/jamulus/pull/1073). That block is [the recorder](https://github.com/jamulussoftware/jamulus/blob/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba/src/recorder/jamrecorder.h#L174): [`SetRecordingDir` news it](https://github.com/jamulussoftware/jamulus/blob/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba/src/recorder/jamcontroller.cpp#L114) and gives ownership to [`QThread::finished` → `deleteLater`](https://github.com/jamulussoftware/jamulus/blob/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba/src/recorder/jamcontroller.cpp#L147), and [`CJamController`](https://github.com/jamulussoftware/jamulus/blob/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba/src/recorder/jamcontroller.h#L56-L82) has no destructor, so on shutdown the thread is never quit, `finished` never fires and the slot never runs. Eight connection objects and one queued audio frame go with it. Only on a server started with `-R`, once, at construction. The other half of this issue, freeing the same object when `Init()` fails, closed with [#3838](https://github.com/jamulussoftware/jamulus/pull/3838).

> Could you repeat the test without -T?

Done, and the answer is no change. Same site, same single block, and the thread record stays at **352 bytes with `-T` and without it** — so multithreading is not what produces it. Its stack is `_dl_allocate_tls` beneath `pthread_create`: a thread stack's own DTV, not memory allocated here. That is the whole of what remains beyond the recorder.

> I think it would be better to kill the clients first, then leave a significant time for things to settle before terminating the server. [...] I think the one in `SetRecordingDir()` might be a case in point.

The clients are killed first here, and a control settles it independently of timing: in a run where no client ever connected, the same record appears with an identical stack. Not session memory that a disconnect would have freed.

> Something is not ok but I have a hard time to figure out what.

Not answered by this run, and worth saying so. Without valgrind the same 12-client session holds RSS between 66,864 and 67,712 kB across 180 s, flat from t=120 s — but that is 3.12.5dev over minutes, against 3.7.0 over hours in [those graphs](https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-819837208).

> Can we split it into separate issues if there are multiple problems that need fixing?

Not on this evidence: one problem, on one target. Per-target splitting stays open — everything above is Linux/x86-64, and valgrind does not exist on Windows.

Three more questions here were answered when they were asked: [continuing the investigation](https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-782849624) in 2021, [moving it to Backlog](https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-817184540) instead, and [declining the assignment](https://github.com/jamulussoftware/jamulus/issues/1083#issuecomment-1685071061) in 2023.

Two notes for whoever repeats the run. The dump is dominated by a still-reachable block of 4,194,288 bytes with `-T` and 2,097,144 without, posted through `QCoreApplication::postEvent` by [`CHighPrecisionTimer::run()`](https://github.com/jamulussoftware/jamulus/blob/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba/src/util.h#L1344) and [`CSocket::ProtocolMessageReceived`](https://github.com/jamulussoftware/jamulus/blob/cc40a8a9442879a39dd9fda3ee4f61fccde2c2ba/src/socket.h#L150) respectively — that one is valgrind: absent when no client connects, and no such growth exists without the instrumentation. And `-m /tmp/jam.dat` now exits with `Unknown option '-m'`, since [`31800e97`](https://github.com/jamulussoftware/jamulus/commit/31800e97f8aabb2192a64cc2fb0188654b5ffa2f) removed `--htmlstatus`.

