# Enhancement: Add tmt check for kmemleak

- URL: https://github.com/teemtee/tmt/issues/3245
- Repo: teemtee/tmt (language: Python)
- State: open; created 2024-09-26T17:24:55Z; status ok; passes offcwe

## Issue body

reporter (NONE) · sbertramrh · 2024-09-26T17:24:55Z · https://github.com/teemtee/tmt/issues/3245

We are attempting to automate testing on a debug kernel and want to incorporate triggering a kmemleak scan at the end of each test. If there is memleak detected then save the trace `cat /sys/kernel/debug/kmemlek >  $TMT_PLAN_DATA/some_file.log ` or any location tmt decides is best.

After reading about tmt.check functions I thought this would be a great next step.

So for each test, as  with dmesg, we clear at the start:
`echo clear > /sys/kernel/debug/kmemleak`

Scan at the end:
`echo scan > /sys/kernel/debug/kmemleak`  (should happen before capturing dmesg)

Capture contents of kmemleak as mentioned above. This file maybe empty.

See https://www.kernel.org/doc/html/latest/dev-tools/kmemleak.html

It is essential we get this process automated and this tmt module seems like the right fit for it.

cc: @thrix 

## Comment 2377598286

other (NONE) · dennisbrendel · 2024-09-26T17:57:34Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2377598286

Thanks @sbertramrh . I think this makes a lot of sense. I would like to add that before the first test execution of the selected plan there should be a scan followed by a clearing the kmleak report (or possibly store it in a special file), so that we do not include leaks from before actually running the first test.

## Comment 2393041210

maintainer (MEMBER) · psss · 2024-10-04T07:40:36Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2393041210

The check implementation handles two events: `CheckEvent.BEFORE_TEST` and `CheckEvent.AFTER_TEST`:

https://github.com/teemtee/tmt/blob/14d60dc0b985603c171d5558b8df0c26cbf776d7/tmt/checks/dmesg.py#L175-L206

I belive the `before_test` part could be used to clear the kmleak report.

## Comment 2435441210

reporter (NONE) · sbertramrh · 2024-10-24T14:23:44Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2435441210

After some more playing around I realized scan clears the buffer so we may not need to run clear before we scan.

I would also like to enhance this by also adding the capture of /proc/slabinfo, `cat /proc/slabinfo > somefile.txt` after we do a scan.

thanks.

## Comment 2450826543

reporter (NONE) · sbertramrh · 2024-10-31T21:14:13Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2450826543

Actually maybe something like this, so we only capture slabinfo if the kmemleak file is > 0 size.

```
        if [ -e /sys/kernel/debug/kmemleak ]; then
            echo scan > /sys/kernel/debug/kmemleak
            cat /sys/kernel/debug/kmemleak ><test dir>/kmemleak-after.log
            if [ -s <test dir>/kmemleak-after.log ]; then
                cat /proc/slabinfo > <test dir>/slabinfo-after.log
            fi
        fi
```

Also discovered we can make kmemleak verbose and this is something we would like to have but I plan to do some tests to see if it persists on reboots. If it does not then we will need to ask for this to be part of the check, to make sure that it is set to verbose. I guess this will depend on the user so maybe having a flag to set verbose or not.

The difference with verbose is you get the warning and also the trace in the dmesg log.

Update as soon as my investigations are done on whether it is needed. thanks.

To  turn verbose on and off for kmemleak

```
[root@localhost ~]# cat /sys/module/kmemleak/parameters/verbose
N
[root@localhost ~]# echo 1 > /sys/module/kmemleak/parameters/verbose
[root@localhost ~]# cat /sys/module/kmemleak/parameters/verbose
Y
[root@localhost ~]# echo 0 > /sys/module/kmemleak/parameters/verbose
[root@localhost ~]# cat /sys/module/kmemleak/parameters/verbose
N
[root@localhost ~]#
```
EDIT:
So it does reset to N on reboot so we will would like to also add this to the kmemleak check. thanks!

## Comment 2452135293

reporter (NONE) · sbertramrh · 2024-11-01T16:06:46Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2452135293

More, taken from analysis done to try and improve how we use kmemleak:
`Wait for 5 seconds after the test/suite has finished and before the scan is started to make sure the time threshold in unreferenced_object() is satisfied for any leak that may have occurred while the test/suite was still running.`

So we should delay at least 5 secs before issuing the scan.

Also adding this here. This i think should not hold up any of the above if it turns out difficult to implement. I am also still researching it but adding here for completeness.

`For any detected leak, use the "dump=" feature of kmemleak to check if the object is still tracked (hasn't been deallocated) and is still unreferenced. Force a new kmemleak scan before checking all the objects to give the scanner a chance to find references that it has previously missed (e.g. xarray nodes that moved around). Any leak with count==min_count is likely a false positive. Any leak with count<min_count could be a real leak and should be further investigated`

thank you!

## Comment 2457321251

other (NONE) · dennisbrendel · 2024-11-05T14:26:40Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2457321251

Waiting for 5 seconds is quite much, it would add up significantly during the runtime of a test suite. It would be great if this could be configurable, or we do some experiments to find a good enough cool-down period.

As to the other thing you quoted - maybe we don't need it if your proposal here is implemented


## Comment 2479603630

other (NONE) · rrendec · 2024-11-15T17:53:30Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2479603630

@dennisbrendel Unfortunately the 5 seconds threshold is hard-coded in https://elixir.bootlin.com/linux/v6.11/source/mm/kmemleak.c#L110 and _will_ prevent a _real_ leak from being reported if we scan sooner than 5 seconds after the object has been allocated.

I agree that the value is probably too conservative and would also have an impact on the runtime of a test suite. I can think of a few possible options:
- Do the clear/test/wait/scan dance at the test suite level rather than individual tests. Since all objects are internally timestamped upon allocation and the timestamp is included in the `dump=` output, it's relatively easy to tell which test was running at the time when the leak occurred, by correlating the allocation timestamp with the test logs, which are also timestamped. Kmemleak uses jiffies for timestamps, but we already know how to convert that to monotonic time or wall clock time.
- Propose an upstream change to make the threshold configurable through a module parameter. While such a change may be accepted, it will take a long time before it makes it into Linux main and we can backport it.
- Make a downstream change to the threshold value. This is only a theoretical option because practically we have a very strict policy of not making downstream changes unless we have a very strong reason to do so.

## Comment 2800014350

other (CONTRIBUTOR) · happz · 2025-04-13T16:14:10Z · https://github.com/teemtee/tmt/issues/3245#issuecomment-2800014350

Sounds like a good tool. There are some ideas and caveats, and there may be a nice MVP to begin with & improve later.
