# Make gcs valgrind proof

- URL: https://github.com/TauLabs/TauLabs/issues/174
- Repo: TauLabs/TauLabs (language: C)
- State: open; created 2013-01-13T09:48:53Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · lilvinz · 2013-01-13T09:48:53Z · https://github.com/TauLabs/TauLabs/issues/174

In a first test, valgrind throws numerous errors when running gcs. Fix the errors and make a valgrind suppressions file for those that are invalid.

Things to check and fix:
- memcheck errors (fixed)
- memcheck leaks
- massif leaks
- helgrind thread errors

For each of those tasks there should be a startup.sh as well as a
suppressions.sup file put into ./ground/gcs/projects/valgrind/


## Comment 12202194

other (CONTRIBUTOR) · elafargue · 2013-01-13T23:01:19Z · https://github.com/TauLabs/TauLabs/issues/174#issuecomment-12202194

Can you describe in more details ?


## Comment 12234525

other (CONTRIBUTOR) · peabody124 · 2013-01-14T19:15:45Z · https://github.com/TauLabs/TauLabs/issues/174#issuecomment-12234525

Also can you describe the methods to use valgrind or link to an article?  I'm fairly unfamiliar with it and just running valgrind /path/to/binary on OSX just produced a crash.

http://www.developer.nokia.com/Community/Wiki/Using_valgrind_with_Qt_Creator seems to have some relevant information.  It might be that this can only be done (robustly) on linux.


## Comment 12263664

reporter (CONTRIBUTOR) · lilvinz · 2013-01-15T12:01:41Z · https://github.com/TauLabs/TauLabs/issues/174#issuecomment-12263664

As far as i know there is no valgrind for windows and maybe some half working valgrind for osx, so i propose to just get through this on linux. There should not be too much platform dependent code.
Valgrind is kind of an instrumentation framework which can be used with several different tool for error checking.
The most interesting ones in this case are:
- memcheck: used to find memory leaks and memory mis usage like writing beyond a buffer or using uninitialized memory
- helgrind and DRD: used to find errors in multi threaded programs like accessing the same resource from more than one thread without usage of synchronization primitives or situations which could possibly lead to a deadlock
- massif: is a heap profiler, used to track down growing memory leaks e.g. when a program runs for a long time and the used memory grows continuously but is being freed on exit so memcheck doesn't complain

In my past experience valgrind always found numerous programing errors when run first on a software project.
It is a good thing to improve overall stability and quality and even helps tracking down and eliminating very subtle bugs.

Goal of this issue is to have a valgrind suppressions file for each of the used tools which gets rid of all library caused errors as well as false positives and being able to run gcs under all three tools without throwing any error anymore.

Further information on valgrind can be found here: http://valgrind.org/info/tools.html


## Comment 12279516

other (CONTRIBUTOR) · elafargue · 2013-01-15T17:42:20Z · https://github.com/TauLabs/TauLabs/issues/174#issuecomment-12279516

Vinz, maybe we could run a session together, you share your screen and you walk us through your findings, we pick the most pressing issues and create relevant issues in github to fix ?


## Comment 12284473

reporter (CONTRIBUTOR) · lilvinz · 2013-01-15T19:26:33Z · https://github.com/TauLabs/TauLabs/issues/174#issuecomment-12284473

For the eclipse users among us there is a plug-in for valgrind: http://www.eclipse.org/linuxtools/projectPages/valgrind/


## Comment 142196039

other (CONTRIBUTOR) · mlyle · 2015-09-22T06:52:41Z · https://github.com/TauLabs/TauLabs/issues/174#issuecomment-142196039

Want to get at least one low-numbered bug in the next release, and this seems like a nice one to target.

