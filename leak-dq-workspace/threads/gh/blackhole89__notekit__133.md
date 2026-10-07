# free(): invalid pointer

- URL: https://github.com/blackhole89/notekit/issues/133
- Repo: blackhole89/notekit (language: C++)
- State: open; created 2022-09-11T14:56:20Z; status ok; passes main

## Issue body

reporter (NONE) · asakura42 · 2022-09-11T14:56:20Z · https://github.com/blackhole89/notekit/issues/133

```
== This is notekit, built at Sun Sep 11 17:49:27 2022. ==
Detected paths:
Config: /home/asakura/.config/notekit
Active notes path: /home/asakura/.local/share/notekit
Default notes path: /home/asakura/.local/share/notekit
Resource path: /usr/share/notekit

free(): invalid pointer
zsh: IOT instruction (core dumped)  notekit
```

Built from AUR today.

## Comment 1242983972

other (CONTRIBUTOR) · sp1ritCS · 2022-09-11T15:05:14Z · https://github.com/blackhole89/notekit/issues/133#issuecomment-1242983972

might be a known clatexmath bug. try unsetting XDG_DATA_HOME
