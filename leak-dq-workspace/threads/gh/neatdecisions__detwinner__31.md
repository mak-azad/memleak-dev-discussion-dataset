# free(): invalid pointer

- URL: https://github.com/neatdecisions/detwinner/issues/31
- Repo: neatdecisions/detwinner (language: C++)
- State: open; created 2024-06-03T06:11:13Z; status ok; passes main

## Issue body

reporter (NONE) · Rovano01 · 2024-06-03T06:11:13Z · https://github.com/neatdecisions/detwinner/issues/31

flatpak run --branch=stable --arch=x86_64 --command=detwinner com.neatdecisions.Detwinner
Gtk-Message: 14:16:30.998: Failed to load module "xapp-gtk3-module"
Gtk-Message: 14:16:31.035: Failed to load module "colorreload-gtk-module"
Gtk-Message: 14:16:31.035: Failed to load module "window-decorations-gtk-module"
free(): invalid pointer
Magick: abort due to signal 6 (SIGABRT) "Abort"...

Its version 0.4.2.

How can I help you more with diagnostics?

