# Possible memory leak

- URL: https://github.com/sddm/sddm/issues/1158
- Repo: sddm/sddm (language: C++)
- State: open; created 2019-04-19T12:52:01Z; status ok; passes offcwe

## Issue body

reporter (NONE) · jerome-laurent-pro · 2019-04-19T12:52:01Z · https://github.com/sddm/sddm/issues/1158

Hi,

My problem in one picture :

![memory_leak_xorg_sddm](https://user-images.githubusercontent.com/12716864/56424749-e1e31580-62b1-11e9-82a1-a08484d01323.png)

The memory usage of xorg as a child process of sddm keeps growing with time.
Everytime I restart my computer, the problem reappears after a few dozens of minutes.
I tried to troubleshoot with the logfile but it seems to be empty.

Do you have any idea ?
Can I give you better information ?
I'm running Kubuntu 18.10.

## Comment 484886850

maintainer (MEMBER) · plfiorini · 2019-04-19T12:54:11Z · https://github.com/sddm/sddm/issues/1158#issuecomment-484886850

That seems a possible memory leak of Xorg not SDDM.

## Comment 484889228

reporter (NONE) · jerome-laurent-pro · 2019-04-19T13:03:01Z · https://github.com/sddm/sddm/issues/1158#issuecomment-484889228

Alright, I'm opening an [issue on stack overflow](https://unix.stackexchange.com/questions/513398/possible-xorg-memory-leak) in that case.
Thank you for your fast answer.
