# Fixing Indirect Memory leaks

- URL: https://github.com/Afsan-z47/CHIP-8/issues/13
- Repo: Afsan-z47/CHIP-8 (language: C)
- State: open; created 2025-08-16T08:47:32Z; status ok; passes main

## Issue body

reporter (OWNER) · Afsan-z47 · 2025-08-16T08:47:32Z · https://github.com/Afsan-z47/CHIP-8/issues/13

Compile the CHIP-8 using fsanitize=address for more description.

The problem is not in the audio.c or any thing regarding audio probably, as I have checked by compiling without those.

Its probably related to SDL for display.


## Comment 3254431981

reporter (OWNER) · Afsan-z47 · 2025-09-04T16:05:57Z · https://github.com/Afsan-z47/CHIP-8/issues/13#issuecomment-3254431981

The SDL_destroy functions for window, texture and rendered did not work. Need to submit a bug report.
