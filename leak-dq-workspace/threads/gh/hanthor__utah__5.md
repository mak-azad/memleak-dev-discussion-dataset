# Bluefin parity: multimedia codec stack is not installed

- URL: https://github.com/hanthor/utah/issues/5
- Repo: hanthor/utah (language: None)
- State: open; created 2026-08-29T05:53:12Z; status ok; passes main

## Issue body

reporter (OWNER) · hanthor · 2026-08-29T05:53:12Z · https://github.com/hanthor/utah/issues/5

## Summary

Bluefin installs a full codec stack alongside its `[fedora]` list. Utah installs none of it, so a Utah desktop cannot play the media a Bluefin desktop can.

From `build_files/base/03-packages.sh` in projectbluefin/bluefin:

```sh
dnf5 -y install \
    --enablerepo='tailscale-stable' \
    --enablerepo='fedora-multimedia' \
    -x PackageKit* \
    "${FEDORA_PACKAGES[@]}" \
    tailscale \
    ffmpeg{,-libs} libavcodec @multimedia gstreamer1-plugins-{bad-free,bad-free-libs,good,base} lame{,-libs} libfdk-aac libjxl ffmpegthumbnailer
```

Missing from Utah:

- `ffmpeg`, `ffmpeg-libs`, `libavcodec`
- the `@multimedia` group
- `gstreamer1-plugins-bad-free`, `-bad-free-libs`, `-good`, `-base`
- `lame`, `lame-libs`
- `libfdk-aac`, `libjxl`
- `ffmpegthumbnailer`

## Rawhide complication

Bluefin pulls these from negativo17 `fedora-multimedia`, which publishes no Rawhide branch (see #4). Fedora's own `ffmpeg` is now shipped in the main repos, so most of this should resolve from Rawhide directly — but `libfdk-aac` and the unstripped `ffmpeg` builds need checking before we claim parity.

## On Flatpaks

Flathub does not offer an app substitute here — these are host codecs. Flatpak *apps* get their codecs from the `org.freedesktop.Platform.ffmpeg-full` runtime extension independently of the host, so this gap mainly affects host-native applications (Nautilus thumbnailing, GNOME video preview, anything from `brew`). Worth confirming `ffmpeg-full` is preinstalled for the Flatpak side regardless.

## Acceptance

- Each package above is either installed from Rawhide or documented under `[unavailable]` in `packages/utah.toml` with a rationale.
- `just check-rawhide` passes with the additions.
- Media playback verified on a booted image.
