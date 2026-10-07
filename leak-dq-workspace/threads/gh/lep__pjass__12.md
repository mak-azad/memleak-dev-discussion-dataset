# Add warnings for initialization of global variables with CreateRegion and too long string literals

- URL: https://github.com/lep/pjass/issues/12
- Repo: lep/pjass (language: C)
- State: open; created 2024-12-23T00:59:59Z; status ok; passes main

## Issue body

reporter (NONE) · tdauth · 2024-12-23T00:59:59Z · https://github.com/lep/pjass/issues/12

Could you add warnings for two issues with JASS and Reforged/TFT: https://www.hiveworkshop.com/threads/list-of-warcraft-iii-crashes.194706/page-4#post-3637812

The first one is this:

```
globals
    region r = CreateRegion()
endglobals
```

which is valid syntax but leads to the game crashing when saving it.


The second one is:

```
return "hhgiuqvycdmnndtyhcjyvngtwjeykxtngnzfwndeeiytcgduquhdghfhvkguujibvqhpbrnfuqxqrctivvgmwtigpdxgdvaxubtmbievdkbmjmmmibawhbawkwdiyjnpjfgthutaykhzgyipmzecbpzqrtbhpkhuhiyjemptjpypyjdkkxjqcmejenpeajabvbkfufiyzvizgvqxyztutjrfxqrhvtueqccfkvbvqpvfxckumwiqjmzjyypuuugnkrbjtjjvzidavcxzntpnayufkqjirivaakutxmxcvjvyvgzdqjqtmkwvkqyjmjvpfciizgdrbnzwmqcjkqedepuvptfagtfvnuxtycefqhqfqjnvdecazzgnwyrniwmzpdnerxpqwwiwwwwfnefhgxpczuudxahafjpxgzmpdtpdwgruqtbmiqiumxdaevnbqifhafghdyjwhycmhygudfptvbjbqtnkvcryhqffqyxjvucjzmawmfieaztkikrmehvygynrkwmwgupgwhffwarvyfvejncwydwkfbeygvrzfazzdbzqxgpzpppqwbpunwmcxigfudfacfvwbjipgdedwyfqidrriwvyvtfgcfwarwtdrqzffivxudqnqrrtipnuvjuvbnnggxdcaderxbvzfbprkmamxzgivwrabdajqhkexdrqttfqebmbrejdpxkubwuxnthraukyrrfjjzmwnaiddamcbhfnrxqxznmvcrjhpybbhcnxdiymiyjgivendvenbajfmfvmrxepbevcqvujvzirgjmpucbuhyebfywiitqxkehqmtqypjtzyfwmvhqbwicgaygzvqrnzfzevgjrgdgzzdzhnatyxdmdgrpghnkimffigpmxazqkbvahdrzetzzemvwakpruqxyunukjvbztyzefgwjfehweubeijbvzynfurfyqprhagkrfkgfwardfjwdyxnicfvzccrijmtecghzyrfixhxggzqvmujnuzdpixgyqmrem"
```

which made the old World Editor crash according to https://www.hiveworkshop.com/threads/documentation-string-type.240473/ but not anymore and leads to save games crashing.
Any string literal should not be longer than 1023 characters.

I am sure there are more issues like this and warnings would be quite useful.

## Comment 2560236677

maintainer (OWNER) · lep · 2024-12-23T20:03:34Z · https://github.com/lep/pjass/issues/12#issuecomment-2560236677

I'll take your word on these.
e8cb077c59ec5da631cb43b6c5ece27245dc4ab4

## Comment 2561295709

reporter (NONE) · tdauth · 2024-12-24T17:06:01Z · https://github.com/lep/pjass/issues/12#issuecomment-2561295709

"String literals over 1023 chars long crash the game upon saving." not on saving but loading the save game (with Reforged).

It crashed the World Editor on saving in TFT but not Reforged.

## Comment 2629130923

reporter (NONE) · tdauth · 2025-02-01T21:54:00Z · https://github.com/lep/pjass/issues/12#issuecomment-2629130923

Can you create a new release wit the added stuff? Maybe a release on GitHub adding the .exe file and using a tag.

## Comment 2629319760

maintainer (OWNER) · lep · 2025-02-02T09:41:46Z · https://github.com/lep/pjass/issues/12#issuecomment-2629319760

I publish my builds [here](https://lep.duckdns.org/ci/project/pjass). Unfortunately not automatically at this moment.
I get the appeal of letting github build your project, but i don't want to pollute my repo with .github files and also not rely on github. I know, that this is distinct from doing a release on github. But i also don't really want to do releases, as i don't really version my software. Just take whatever master is pointing at and go compile it.
By the way, if you want to, you can fork this repo and add CI in your fork.

## Comment 4198787878

reporter (NONE) · tdauth · 2026-04-07T12:00:34Z · https://github.com/lep/pjass/issues/12#issuecomment-4198787878

The link does not work for me. It would be much easier to release Linux and Windows binaries on GitHub. you can use GitHub actions.

## Comment 4198964716

maintainer (OWNER) · lep · 2026-04-07T12:32:38Z · https://github.com/lep/pjass/issues/12#issuecomment-4198964716

Yes, that site is gone. But i did do a [github release](https://github.com/lep/pjass/releases/tag/release-2025-10-05).
Personally i dislike polluting my git with github (or any other forge) specific files but you're free to make your own repo and have it build pjass like [wurst does over here for jassdoc](https://github.com/wurstscript/wurst-jassdoc-build).
