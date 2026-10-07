# free(): invalid pointer

- URL: https://github.com/Atterratio/obs-gphoto/issues/23
- Repo: Atterratio/obs-gphoto (language: C)
- State: open; created 2021-04-02T19:02:05Z; status ok; passes main

## Issue body

reporter (NONE) · samwho · 2021-04-02T19:02:05Z · https://github.com/Atterratio/obs-gphoto/issues/23

If I set up a scene that uses the obs-gphoto plugin to display my Canon EOS 80D, and another scene that does not have the gphoto source in it, when I switch from the scene with the gphoto plugin to the one without and back again, OBS crashes and in the logs it says `free(): invalid pointer`.

The same happens even if I just toggle visibility of the gphoto source.
