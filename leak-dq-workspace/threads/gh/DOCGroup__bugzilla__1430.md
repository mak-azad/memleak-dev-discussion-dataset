# [BZ-1430] Handle Leak

- URL: https://github.com/DOCGroup/bugzilla/issues/1430
- Repo: DOCGroup/bugzilla (language: C++)
- State: open; created 2026-03-27T23:04:08Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · jwillemsen · 2026-03-27T23:04:08Z · https://github.com/DOCGroup/bugzilla/issues/1430

<!-- Migrated from Bugzilla -->

| Field | Value |
| --- | --- |
| **Bugzilla ID** | [1430](http://bugzilla.dre.vanderbilt.edu/show_bug.cgi?id=1430) |
| **Reporter** | Lukas Gruetzmacher |
| **Assigned to** | DOC Center Support List (internal) |
| **Product** | TAO |
| **Component** | ORB |
| **Version** | 1.3 |
| **Platform / OS** | x86 / Windows 2000 |
| **Priority** | P3 |
| **Severity** | normal |
| **Status** | NEW |
| **Resolution** |  |
| **Created** | 2003-01-22 10:54:58 -0600 |

---

_Originally posted by Lukas Gruetzmacher on 2003-01-22 10:54:58 -0600_

---

As already described in Bug 1200 there is a handle leak during high trafic on 
the server.

Reproducable on Win2k with the sample from Bug 1200.
Start the Server.
Start about 10 Clients.

This scenario cause the following behavoir:
Time    Server Handles Threads     Clients Handles Threads
10:33          339     22                  125-136 4-6
11:19          378     22                  125-136 4-6
15:41          415     22                  125-151 4-9

## Comment 4145824827

reporter (MEMBER) · jwillemsen · 2026-03-27T23:04:13Z · https://github.com/DOCGroup/bugzilla/issues/1430#issuecomment-4145824827

_Originally posted by Nanbor Wang on 2003-02-02 08:21:13 -0600_ ([Bugzilla comment 1](http://bugzilla.dre.vanderbilt.edu/show_bug.cgi?id=1430#c1))

---

Assign the bug to me

## Comment 4145825083

reporter (MEMBER) · jwillemsen · 2026-03-27T23:04:19Z · https://github.com/DOCGroup/bugzilla/issues/1430#issuecomment-4145825083

_Originally posted by Nanbor Wang on 2003-02-02 08:21:27 -0600_ ([Bugzilla comment 2](http://bugzilla.dre.vanderbilt.edu/show_bug.cgi?id=1430#c2))

---

Accept the bug

## Comment 4145825387

reporter (MEMBER) · jwillemsen · 2026-03-27T23:04:25Z · https://github.com/DOCGroup/bugzilla/issues/1430#issuecomment-4145825387

_Originally posted by Lukas Gruetzmacher on 2003-03-25 10:26:36 -0600_ ([Bugzilla comment 3](http://bugzilla.dre.vanderbilt.edu/show_bug.cgi?id=1430#c3))

---

Hi Bala,

How about the status of this issue.
The leak seams to become critical for us. Are you able to reproduce the 
behavior ?

## Comment 4145825671

reporter (MEMBER) · jwillemsen · 2026-03-27T23:04:30Z · https://github.com/DOCGroup/bugzilla/issues/1430#issuecomment-4145825671

_Originally posted by Nanbor Wang on 2003-03-25 10:47:03 -0600_ ([Bugzilla comment 4](http://bugzilla.dre.vanderbilt.edu/show_bug.cgi?id=1430#c4))

---

Lukas,
Its in my "todo" list. We are swamped on different projects that we are
committed to deliver for our sponsors. We will get to this whenever we get time.
It would be difficult for us to give you an ETA. If you would like to sponsor
this effort please let us know. Or if you have time to track this down please
let us know your solution and we will integrate your patch happily!

Thanks

## Comment 4145825936

reporter (MEMBER) · jwillemsen · 2026-03-27T23:04:36Z · https://github.com/DOCGroup/bugzilla/issues/1430#issuecomment-4145825936

_Originally posted by @jwillemsen on 2007-09-20 03:09:00 -0500_ ([Bugzilla comment 5](http://bugzilla.dre.vanderbilt.edu/show_bug.cgi?id=1430#c5))

---

to pool
