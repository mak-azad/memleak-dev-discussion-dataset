# Avoid frequent memory allocation/deallocation by memory pool

- URL: https://github.com/DLTcollab/dcurl/issues/20
- Repo: DLTcollab/dcurl (language: C)
- State: open; created 2018-03-18T20:46:42Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · jserv · 2018-03-18T20:46:42Z · https://github.com/DLTcollab/dcurl/issues/20

Current PoW internals consist of various `malloc` and `free`, which are called frequently. It is bad for performance considerations. Using [memory pool](https://en.wikipedia.org/wiki/Memory_pool) is a common technique to speed up and ensure consistent execution time.

I have done preliminary memory pool: https://github.com/jserv/dcurl/tree/memory-pool
NOTE: we might have to manipulate with thread-safe issues, and check out existing implementations such as [philip-wernersbach/memory-pool-allocator](https://github.com/philip-wernersbach/memory-pool-allocator).

## Comment 374059137

reporter (MEMBER) · jserv · 2018-03-18T22:33:31Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-374059137

After applying [enable-rdtsc.patch](https://github.com/chenwei-tw/dcurl/files/1823210/enable-rdtsc.txt), I got the following [time-stamp](https://c9x.me/x86/html/file_module_x86_id_278.html) numbers:
```shell
*** Validating build/test_trinary ***
=== trits_from_trytes: 42320 ===
=== trytes_from_trits: 5103 ===

*** Validating build/test_curl ***
=== trits_from_trytes: 220208 ===
=== trytes_from_trits: 3171 ===

*** Validating build/test_pow_sse ***
=== trits_from_trytes: 76903 ===
=== trits_from_trytes: 32099 ===
=== trytes_from_trits: 2245 ===
=== trits_from_trytes: 33132 ===
=== trytes_from_trits: 2674 ===
=== trits_from_trytes: 2651 ===
```

## Comment 374192776

reporter (MEMBER) · jserv · 2018-03-19T12:18:31Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-374192776

To illustrate the memory impact, [TCMalloc](http://goog-perftools.sourceforge.net/doc/tcmalloc.html) is used for comparisons. The following environment is Intel Xeon E5 class server with Ubuntu Linux `17.04`.

First, prepare TCMalloc: `$ sudo apt install libtcmalloc-minimal4`.

* without TCMalloc
```shell
$ make check
*** Validating build/test_trinary ***
=== trits_from_trytes: 5460 ===
=== trytes_from_trits: 4286 ===

*** Validating build/test_curl ***
=== trits_from_trytes: 120820 ===
=== trytes_from_trits: 3940 ===

*** Validating build/test_pow_sse ***
=== trits_from_trytes: 68535 ===
=== trits_from_trytes: 61490 ===
=== trytes_from_trits: 1221 ===
=== trits_from_trytes: 31277 ===
=== trytes_from_trits: 1617 ===
=== trits_from_trytes: 2668 ===
```

* with TCMalloc
```shell
$ LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4 make check
*** Validating build/test_trinary ***
=== trits_from_trytes: 29244 ===
=== trytes_from_trits: 3920 ===

*** Validating build/test_curl ***
=== trits_from_trytes: 108290 ===
=== trytes_from_trits: 2940 ===

*** Validating build/test_pow_sse ***
=== trits_from_trytes: 79500 ===
=== trits_from_trytes: 57566 ===
=== trytes_from_trits: 3028 ===
=== trits_from_trytes: 31777 ===
=== trytes_from_trits: 1654 ===
=== trits_from_trytes: 1980 ===
```

`dcurl` would benefit from the use of pre-allocated memory pool especially when its size is tweaked for trytes/trits representations.


## Comment 374329352

maintainer (MEMBER) · furuame · 2018-03-19T19:02:32Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-374329352

It is worth mentioning that heap memory which every PoW task allocates is ***fixed***. Maybe we can implement a special memory pool for allocating trytes & trits.

## Comment 411097910

maintainer (MEMBER) · furuame · 2018-08-07T15:28:46Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-411097910

In our scenario, the memory usage every PoW task (thread) uses is "fixed" and the variables can be reused. I think we can declare all the variables in advance rather than allocating it from memory pool every time.

## Comment 429183099

maintainer (COLLABORATOR) · marktwtn · 2018-10-12T02:27:34Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-429183099

The tool [heaptrack](https://github.com/KDE/heaptrack) can show the information of the dynamic memory allocation.
Such as:

- allocation times
- allocation bytes
- memory leak

![2018-10-12 10-08-27](https://user-images.githubusercontent.com/6748200/46844103-32138380-ce08-11e8-941d-7030309ffebd.png)

The information gives us the blueprint of the memory pool design.
It helps us determine the size of the memory pool.

## Comment 429551816

reporter (MEMBER) · jserv · 2018-10-13T15:42:54Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-429551816

Dynamic memory allocation tends to be non-deterministic, and is it possible to elininate existing dynamic allocation inside dcurl?

## Comment 429697557

maintainer (COLLABORATOR) · marktwtn · 2018-10-15T03:27:03Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-429697557

> Dynamic memory allocation tends to be non-deterministic, and is it possible to elininate existing dynamic allocation inside dcurl?

Yes, we can eliminate the dynamic allocation to once or even use a declared char array as a memory pool.

## Comment 431746020

maintainer (COLLABORATOR) · marktwtn · 2018-10-22T05:54:56Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-431746020

I have implemented a memory pool mechanism and integrated it into the `dcurl - SSE`.

Here are the problems:

1. Experiment result
I run the `test-pow` with executing the `PoW` 100 times.
The execution time does not have much difference.
The time stamp difference of allocating a memory in `trits_from_trytes` and `trytes_from_trits` functions may even worse.

    To solve the problem
    (1) Use `perf` or `gprof` to analyze the memory pool code and improve the performance.
    (2) Run the program multiple times to see the execution time distribution.

2. Allocation size
Take `SSE` as an example.
Most allocation size is fixed.
However, there are some allocation sizes which are related to the maximum thread number and maximum core number.
I leave these memory allocation unchanged.

## Comment 432877906

maintainer (COLLABORATOR) · marktwtn · 2018-10-25T01:04:00Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-432877906

1. Experiment result
Forget about the execution time. It is not related to the memory pool.
I use `rdtsc` to read the time stamp counter difference of each memory allocation.

    0 ~ 150 sample point
    ![timestamp0-150](https://user-images.githubusercontent.com/6748200/47469101-b535d000-d831-11e8-887a-d1f1325d2b25.png)

    2000 ~ 2150 sample point
    ![timestamp2000-2150](https://user-images.githubusercontent.com/6748200/47469103-b830c080-d831-11e8-9274-017d19a613ff.png)

    The graphs show the time stamp difference of allocating a memory with `malloc` function and `memory pool` by running `PoW` 100 times.
    The memory pool looks better than the dynamic memory allocation.
    However, there is a strange peak in memory pool.
    It happens when allocating a 16B memory right after the `PoW` is finished.
Still looking for the reason of the weird behavior.

    The previous comment says the result is worse, that is caused by getting the time stamp counter value at the wrong line of the source code.

2. Allocation size
Based on the previous comment. there are some allocation which are related to the maximum `thread` and `core` number.
If these numbers can be determined, then there would be no problems at all.

## Comment 432941953

reporter (MEMBER) · jserv · 2018-10-25T07:20:33Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-432941953

`rdtsc` is not accurate for SMP. 

## Comment 432989585

maintainer (COLLABORATOR) · marktwtn · 2018-10-25T09:54:45Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-432989585

> `rdtsc` is not accurate for SMP.

However, even if I use `clock_gettime` function to acquire the time difference, the result is still the same.

## Comment 435306316

maintainer (COLLABORATOR) · marktwtn · 2018-11-02T08:29:00Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-435306316

When I was using the analysis tool such as `perf`, I found out that the `PoW` part took the most of the calculation.
Therefore, it was hard to see the behaviour of the other functions such as memory pool allocation.

However, the suggestion to empty the `PoW` function did not work properly.
Since the time stamp counter difference of each memory allocation is somehow affected by the `PoW` function.

## Comment 435335450

reporter (MEMBER) · jserv · 2018-11-02T10:26:51Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-435335450

Ouch! It is a pity. I look forward to the migration to other memory allocators.

## Comment 436723654

maintainer (COLLABORATOR) · marktwtn · 2018-11-07T18:15:40Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-436723654

Since `rdtsc` can be afftected by out-of-order execution and variable CPU clock frequency,
the measurement is replaced with the function `clock_gettime`.

The following charts come up with running on different hardware and commenting the specific function `transfromXXX()` or not.

- My desktop
with `transformXXX()`
![cpu-desktop-nano](https://user-images.githubusercontent.com/6748200/48149874-355f3980-e2f8-11e8-89c6-36b8ad13c7b3.png)
without `transformXXX()`
![cpu-desktop-nano-notrans](https://user-images.githubusercontent.com/6748200/48149922-4b6cfa00-e2f8-11e8-8d6e-71e38834c69c.png)

- My laptop
with `transformXXX()`
![cpu-laptop-nano](https://user-images.githubusercontent.com/6748200/48150303-3a70b880-e2f9-11e8-8c36-18e8cb89831e.png)
without `transformXXX()`
![cpu-laptop-nano-notrans](https://user-images.githubusercontent.com/6748200/48150312-40669980-e2f9-11e8-9060-48580099e2ef.png)

- node.deviceproof.org (with DCURL_CPU_NUM=3)
with `transformXXX()`
![cpu-device-nano-3core](https://user-images.githubusercontent.com/6748200/48150168-e960c480-e2f8-11e8-98c5-09d2a80f0325.png)
without `transformXXX()`
![cpu-device-nano-notrans-3core](https://user-images.githubusercontent.com/6748200/48150188-f2ea2c80-e2f8-11e8-9e96-337c6f777963.png)

**The question and conclusion:**
Comment out the important function `transfromXXX()` in PoW do reduce the impact on memory allocation.
However, the reason is not cleared. (I guess it is caused by the cache.)
And the memory allocation time is not stabilized, which means the memory allocator is not good enough or there are other impacts in `dcurl`.

Keep investigating.

## Comment 459230208

reporter (MEMBER) · jserv · 2019-01-31T06:21:11Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-459230208

After #95 is resolved, we can continue memory pool engagement.

## Comment 549443061

reporter (MEMBER) · jserv · 2019-11-04T16:47:09Z · https://github.com/DLTcollab/dcurl/issues/20#issuecomment-549443061

Cc. @JulianATA 
