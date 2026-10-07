# RAM Leak while Bitsum checkin'

- URL: https://github.com/qbittorrent/qBittorrent/issues/16442
- Repo: qbittorrent/qBittorrent (language: C++)
- State: closed; created 2022-02-14T03:18:00Z; status ok; passes offcwe

## Issue body

reporter (NONE) · backskin · 2022-02-14T03:18:00Z · https://github.com/qbittorrent/qBittorrent/issues/16442

### qBittorrent & operating system versions

qBittorrent: 4.4.0 x64
Operating system: Windows10 Pro 21H2/19044.1526

### What is the problem?

RAM is leaking when it is checking the bitsum of a torrent download.
My memory is full. 

### Steps to reproduce

1. Try to download a torrent with a lot of files in it (mine got 76.1 GB, ~5000x16 Mb pieces)
2. Press "Force Recheck" button
3. Open up your Task Manager and see how your RAM is getting low

### Additional context

_No response_

### Log(s) & preferences file(s)

![image](https://user-images.githubusercontent.com/49398278/153794414-d5b12714-cb42-4c1e-9345-1b519dac20f8.png)


## Comment 1038608132

maintainer (MEMBER) · glassez · 2022-02-14T03:57:52Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038608132

Using a large amount of memory does not necessarily mean a memory leak. Unfortunately, many people use the term "memory leak" without understanding its true meaning.

## Comment 1038849172

other (NONE) · Legendarion · 2022-02-14T09:24:10Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038849172

@glassez: So 'Space Leak' would be the right term, right? :)

https://en.wikipedia.org/wiki/Memory_leak

## Comment 1038894663

maintainer (MEMBER) · glassez · 2022-02-14T10:09:20Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038894663

> @glassez: So 'Space Leak' would be the right term, right? :)

According to article you linked to above:
>A **space leak** occurs when a computer program **uses more memory than necessary**. 
In contrast to memory leaks, where the leaked memory is never released, the memory consumed by a space leak is released, but later than expected

I don't think this is the case since you're talking about checking 76GB of data. It just uses as much memory as available.
@arvidn?

## Comment 1038925098

other (CONTRIBUTOR) · arvidn · 2022-02-14T10:37:31Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038925098

I don't believe there is a leak. but more interestingly, is there a problem?

## Comment 1038937873

maintainer (MEMBER) · glassez · 2022-02-14T10:51:55Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038937873

>more interestingly, is there a problem?

It seems that many users install a large amount of RAM just to see most of it never used.

## Comment 1038965432

maintainer (MEMBER) · jagannatharjun · 2022-02-14T11:19:55Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038965432

as I pointed out here https://github.com/arvidn/libtorrent/pull/6703#issuecomment-1030573308 this kind of memory allocation does seem to cause some performance problems in different apps, plus libtorrent don't need that much allocation, the memory usage will become normal if you open one of the files from checking torrent.

## Comment 1038966809

maintainer (MEMBER) · xavier2k6 · 2022-02-14T11:21:17Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038966809

IMO - to me it's depending on the users interpretation of memory use/memory leak.

With libtorrent 2.x - I understand that it's going to use as much ram that's available/needed & this is a change in behaviour as compared to what users have been used to during libtorrent 1.x series. (It'll take time for users to adjust to this)

>is there a problem?

Yes!

Since the use of libtorrent 2.x, rechecking large torrents 70/80GB+ even with an `SSD` causes mouse lag/stuttering......Task Manager will show read speed of `SSD` for a small period of time at top end of range ~550MB/s & will be hugely sporadic for a long period of time while still checking with drops as low as ~25MB/s & only seem to manage a top speed of ~300MB/s it will then recover close to the end of rechecking.........say with ~25% to go & reach full top speed again of ~550MB/s

CPU/RAM usage hits 99% too & machine sounds like a jet engine!

If I recheck torrents less than 70+GB it seems to maintain full ~550MB/s speed throughout without stuttering/mouse lag etc.

## Comment 1038968496

other (CONTRIBUTOR) · arvidn · 2022-02-14T11:22:56Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038968496

@jagannatharjun 
> as I pointed out here https://github.com/arvidn/libtorrent/pull/6703#issuecomment-1030573308 this kind of memory allocation does seem to cause some performance problems in different apps, plus libtorrent don't need that much allocation, the memory usage will become normal if you open one of the files from checking torrent.

Are you running that patch?

## Comment 1038969721

other (CONTRIBUTOR) · arvidn · 2022-02-14T11:24:13Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1038969721

@xavier2k6 I'm aware of those reports. If you're suggesting this is a duplicate, it should probably be closed referring to one of the existing ones. But I think it would be good to have the original poster acknowledge this first.

## Comment 1039001660

maintainer (MEMBER) · glassez · 2022-02-14T12:00:46Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1039001660

>Since the use of libtorrent 2.x, rechecking large torrents 70/80GB+ even with an SSD causes mouse lag/stuttering....

Well, if that's the case, then that's really a problem.

## Comment 1039018978

maintainer (MEMBER) · jagannatharjun · 2022-02-14T12:17:03Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1039018978

> Are you running that patch?

Yes, at the time of the screenshot

## Comment 1039083092

other (CONTRIBUTOR) · arvidn · 2022-02-14T13:23:39Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1039083092

> Yes, at the time of the screenshot

Ok, great! Do you experience any problems, apart from task manager showing all your memory being used?

Actually, I would prefer we could have this conversation on that PR itself

## Comment 1039096896

other (CONTRIBUTOR) · arvidn · 2022-02-14T13:36:29Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1039096896

@jagannatharjun actually, that patch is about the write-cache (downloading) The patch attempting to address the checking of files on windows is here: https://github.com/arvidn/libtorrent/pull/6711

## Comment 1039597291

other (NONE) · DCxDemo · 2022-02-14T21:42:58Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1039597291

qbittorrent 4.4.0 just regularly eats up all ram available, i have 1000+ files torrents and ram usage just keeps growing, the process says it's 300mb, but it's Process Working Set that grows.

when all ram is used it affects system performance in a negative way, rendering it unresponsive (which is typical out of ram symptom). i actually had to revert to 4.3.9 and it doesn't happen there. memory usage looks more like a "saw", releasing resources appropriately. i also think it wasn't an issue in 4.4.0rc1 as i was using it since the sorting bug for a long time and that didn't have such issue. so it's something introduced in between.

from what it looks like, it accesses a lot of different files, but like leaves file handles open and it just keeps growing. pausing torrent and running again flushes memory usage instantly, but it starts over again.

## Comment 1077828537

other (NONE) · ghost · 2022-03-24T16:47:33Z · https://github.com/qbittorrent/qBittorrent/issues/16442#issuecomment-1077828537

Fixed by https://github.com/qbittorrent/qBittorrent/pull/16617 and https://github.com/qbittorrent/qBittorrent/pull/16700 on Windows systems. Will be included in next release(4.4.2).
