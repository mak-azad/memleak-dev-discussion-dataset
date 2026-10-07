# free(): invalid pointer

- URL: https://github.com/GenericMappingTools/gmt/issues/7522
- Repo: GenericMappingTools/gmt (language: C)
- State: open; created 2023-06-12T20:21:27Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · jidanni · 2023-06-12T20:21:27Z · https://github.com/GenericMappingTools/gmt/issues/7522

```
$ echo | gmt xyz2grd /dev/stdin -G/tmp/nn \
-JT-87/41/4c \
-I1M -R-100/100/-100/100
xyz2grd [WARNING]: For a UTM or TM projection, your region -100/100/-100/100 is too large to be in degrees and thus assumed to be in meters
free(): invalid pointer
Aborted
$ gmt --version
6.4.0
```

## Comment 1588034293

other (NONE) · welcome[bot] · 2023-06-12T20:21:29Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588034293

👋 Thanks for opening your first issue here! Please make sure you filled out the template with as much detail as possible. We appreciate that you took the time to contribute!

Please make sure you read our [Contributing Guide](https://github.com/GenericMappingTools/gmt/blob/master/CONTRIBUTING.md) and abide by our [Code of Conduct](https://github.com/GenericMappingTools/.github/blob/main/CODE_OF_CONDUCT.md).


## Comment 1588160765

maintainer (MEMBER) · joa-quim · 2023-06-12T21:58:05Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588160765

Can't reproduce this either (Linux == Windows)
```
echo | xyz2grd -Glixo /dev/stdin -JT-87/41/4c -I1M -R-100/100/-100/100 -V
xyz2grd [WARNING]: For a UTM or TM projection, your region -100/100/-100/100 is too large to be in degrees and thus assumed to be in meters
mapproject [INFORMATION]: Provides 2, expects 2-column binary data
mapproject [INFORMATION]: Processing input table data
mapproject [INFORMATION]: Transform -88/-86/40/42 <- -85394.6196907/85394.6196907/-111044.260899/111547.404647 [m]
mapproject [INFORMATION]: Input 2 columns via binary records using format dd
mapproject [INFORMATION]: Reading Data Table from memory reference supplied by pointer
mapproject [INFORMATION]: Output 2 columns via binary records using format dd
mapproject [INFORMATION]: Writing Data Table to memory reference supplied by pointer
mapproject [INFORMATION]: Projected 2 points
mapproject [INFORMATION]: Input extreme values:  Xmin: -100 Xmax: 100 Ymin: -100 Ymax 100
mapproject [INFORMATION]: Output extreme values: Xmin: -87.0011885472 Xmax: -86.9988114204 Ymin: 40.9990995308 Ymax 41.0009004579
mapproject [INFORMATION]: Mapped 2 x-y pairs [m] to lon-lat pairs
xyz2grd [INFORMATION]: Region selection -R-100/100/-100/100 is replaced by the equivalent geographic region -R-87.0011885472/40.9990995308/-86.9988114204/41.0009004579+r
xyz2grd [ERROR]: Unrecognized option -V
```

And what is that ``/dev/stdin`` doing there?

## Comment 1588171287

maintainer (MEMBER) · Esteban82 · 2023-06-12T22:06:27Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588171287

Hi jidanni!! Thanks for reporting all the issues and suggestions. It is nice to see someone new.

I can reproduce BUT I was using **GMT 6.4**. Maybe the problem was already fix. 

@jidanni try using the dev version. 6.4 is almost one year old. 

## Comment 1588177391

maintainer (MEMBER) · joa-quim · 2023-06-12T22:10:56Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588177391

Tried with an old 6.1.1 and didn't get that message either.

## Comment 1588854199

reporter (CONTRIBUTOR) · jidanni · 2023-06-13T08:58:19Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588854199

I'm using
https://packages.debian.org/sid/gmt
If there is something I should put in
/etc/apt/sources.list.d/
please tell me.
No .debs on
https://www.generic-mapping-tools.org/download/ .

## Comment 1588900789

maintainer (MEMBER) · PaulWessel · 2023-06-13T09:25:09Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588900789

FYI, the /dev/stdin does not cause any trouble but is unnecessary since GMT always reads stdin if no table file is given.

## Comment 1588903027

maintainer (MEMBER) · PaulWessel · 2023-06-13T09:26:38Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588903027

> Tried with an old 6.1.1 and didn't get that message either.

Nothing on macOS either with dev version.

## Comment 1588949195

maintainer (MEMBER) · PaulWessel · 2023-06-13T09:50:47Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588949195

> I'm using
> https://packages.debian.org/sid/gmt
> If there is something I should put in
> /etc/apt/sources.list.d/
> please tell me.
> No .debs on
> https://www.generic-mapping-tools.org/download/ .

I think all the Linux distros do their own GMT version maintenance and since we developers do not work on all of those anyway we do not know what to put in such config recipes.  It is possible this is a real bug that only manifests on some OS and since @Esteban82 can reproduce it perhaps that command can be run in ddd and tell us what line it crashes.

## Comment 1588995143

other (CONTRIBUTOR) · anbj · 2023-06-13T10:15:59Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1588995143

Debian 12 Bookworm, gmt bleeding edge compiled from source:

```
$ gmt --version
6.5.0_3403c89_2023.06.13
```

```
$ echo | gmt xyz2grd /dev/stdin -G/tmp/nn \
-JT-87/41/4c \
-I1M -R-100/100/-100/100
xyz2grd [WARNING]: For a UTM or TM projection, your region -100/100/-100/100 is too large to be in degrees and thus assumed to be in meters
free(): invalid pointer
Aborted
```

Variations:

Remove ``/dev/stdin`` and you get this:

```
$ echo | gmt xyz2grd -G/tmp/nn -JT-87/41/4c -I1M -R-100/100/-100/100
xyz2grd [WARNING]: For a UTM or TM projection, your region -100/100/-100/100 is too large to be in degrees and thus assumed to be in meters
malloc_consolidate(): invalid chunk size
Aborted
```

Remove ``echo |`` and it just hangs (killed with ``^c``)::

```
$ gmt xyz2grd /dev/stdin -G/tmp/nn -JT-87/41/4c -I1M -R-100/100/-100/100
xyz2grd [WARNING]: For a UTM or TM projection, your region -100/100/-100/100 is too large to be in degrees and thus assumed to be in meters
^Cfree(): invalid pointer
Aborted
```

## Comment 1589006661

maintainer (MEMBER) · PaulWessel · 2023-06-13T10:24:24Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1589006661

Thanks @anbj, might you be able to build with debug (See DEBUG in cmake/* files) and run the gmt command in **ddd**?

## Comment 1589066653

maintainer (MEMBER) · PaulWessel · 2023-06-13T10:57:20Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1589066653

Actually, turning malloc guards on in Xcode shows the problem.  Because of confusion on **-I** it first creates a grid that has size 25 (a 1x1 grid since **-R** is (at line 535 in xyz2grd) -87.001188547204534/-86.998811420443928/40.999099530771346/41.000900457940716 but inc is 1 so we get a grid size of 1x1.

Then, when we updated the pad on the grid the wesn is the same but now inc is 0.0023771267606065294,/0.0018009271693699702 and the grid is suddenly 2x2 in size.  With pad that is 36 nodes but only 25 was allocated earlier.  Accessing those nodes beyond 25 yields the SEGV .

Clearly, there are issues with computing _inc_ twice and not properly set the very first time (1) but improved the 2nd time - but that is too late for memory alloc.

Think we need to document clearly what **-R -J** means in **xyz2grd** and then we can probably fix where it fails to live up to that.  Pretty sure this happens because nobody intended any of this to happen or be used as such in **xyz2grd**.

## Comment 1589165669

other (CONTRIBUTOR) · anbj · 2023-06-13T12:02:37Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1589165669

@PaulWessel, so no point for me to run **ddd**?

## Comment 1589173822

maintainer (MEMBER) · PaulWessel · 2023-06-13T12:06:38Z · https://github.com/GenericMappingTools/gmt/issues/7522#issuecomment-1589173822

No, clearly a bug

On 13 June 2023 at 14:02:47, anbj ***@***.***) wrote:

> @PaulWessel
> <https://urldefense.com/v3/__https://github.com/PaulWessel__;!!PvDODwlR4mBZyAb0!ULIHmNMbr36czeiI6vII7kjfvscYalC_Flc7O-3jLXTwj8K9AJpZ7VzPQWHHESjkClsr4secnABn-SsqM5ZDVGLZsw$>,
> so no point for me to run *ddd*?
>
> —
> Reply to this email directly, view it on GitHub
> <https://urldefense.com/v3/__https://github.com/GenericMappingTools/gmt/issues/7522*issuecomment-1589165669__;Iw!!PvDODwlR4mBZyAb0!ULIHmNMbr36czeiI6vII7kjfvscYalC_Flc7O-3jLXTwj8K9AJpZ7VzPQWHHESjkClsr4secnABn-SsqM5aqKYEEdg$>,
> or unsubscribe
> <https://urldefense.com/v3/__https://github.com/notifications/unsubscribe-auth/AGJ7IXYNCRU4M7PVSQSFQHTXLBJGPANCNFSM6AAAAAAZD4DO4I__;!!PvDODwlR4mBZyAb0!ULIHmNMbr36czeiI6vII7kjfvscYalC_Flc7O-3jLXTwj8K9AJpZ7VzPQWHHESjkClsr4secnABn-SsqM5a3CH_9aw$>
> .
> You are receiving this because you were mentioned.Message ID:
> ***@***.***>
>

