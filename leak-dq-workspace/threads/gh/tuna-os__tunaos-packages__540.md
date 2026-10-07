# gtk4 is served but uninstallable: nothing provides libgstplay-1.0.so.0 (gstreamer1-plugins-bad-free unbuilt)

- URL: https://github.com/tuna-os/tunaos-packages/issues/540
- Repo: tuna-os/tunaos-packages (language: Python)
- State: open; created 2026-08-26T08:44:01Z; status ok; passes main

## Issue body

reporter (MEMBER) · hanthor · 2026-08-26T08:44:01Z · https://github.com/tuna-os/tunaos-packages/issues/540

`gtk4` is published in the hummingbird prefix and **cannot install**. Everything behind it — the GNOME 51 stack — is blocked on one unbuilt package.

## Measured

Read from the served indexes, not inferred:

```
gtk4       (gtk4-4.22.1-2.fc43.src.rpm)  unmet: gstreamer1-plugins-bad-free-libs(x86-64)
                                                libgstplay-1.0.so.0()(64bit)
gtk4-devel (gtk4-4.22.1-2.fc43.src.rpm)  unmet: libgstplay-1.0.so.0()(64bit)
```

Neither capability is provided by the hummingbird base (`packages.redhat.com/.../public-hummingbird/x86_64/`) nor by anything the factory has published to `repo.tunaos.org/hummingbird/20251124-x86_64/`. `gstreamer1-plugins-bad-free-libs` is not in either index.

**A near miss worth recording**, because it is easy to convince yourself otherwise: a substring search for `libgstplay` in the served provides *does* hit — on `libgstplayback.so()(64bit)`, from `gstreamer1-plugins-base`. That is a different library. `libgstplayback.so` is a playback **plugin** from `-base`; `libgstplay-1.0.so.0` is the **GstPlay library** from `-bad-free`. Match the exact capability string.

## Why it matters

`gstreamer1-plugins-bad-free` sits at **layer-05** of `build-order-hummingbird-desktops.yml`, beside `gstreamer1-plugins-base` and `gtk4` — both of which build and are served. It is one of 103 source packages out of 673 that the chain has not produced. Because `gtk4` is a dependency of essentially the whole desktop, this single package gates the GNOME 51 goal.

## What is NOT the cause

Ruled out rather than assumed:

- **Not unsatisfiable BuildRequires.** `scripts/preflight-buildrequires.py --target hummingbird` reports exactly one package that cannot build across all 673, and it is `SwayNotificationCenter` (`pkgconfig(granite-7)`, a Fedora-wide FTBFS). `gstreamer1-plugins-bad-free` is not blocked at the name or the version level.
- **Not a missing recipe.** It is a `distgit:` entry, so `src/hummingbird/gstreamer1-plugins-bad-free/` is absent on disk by design and materialized at build time.
- **Probably not its `bootstrap: true` key.** A reduced bootstrap build that omits GstPlay would explain a package that succeeds without producing `libgstplay-1.0.so.0`, but nothing in `scripts/build-chain.sh` or `scripts/run-package-factory-cell.sh` reads a per-package `bootstrap` key — `scripts/copr-build-chain.py` filters spec *filenames* containing `bootstrap`, which is a different thing. Recorded as a hypothesis that did not survive checking, not as a finding.

## What would answer it

The chain log for the cell that last attempted layer-05. Job logs return HTTP 404 while a job is running, so this needs a completed run. When reading it, find the package's own `package     : gstreamer1-plugins-bad-free` block rather than the nearest `ERROR:` line — the chain runs `jobs=2` and interleaves output, so a failure routinely prints inside a different package's mock lines.

Two outcomes to distinguish:

1. It **fails to build** — then the error is the work.
2. It **builds but ships no `libgstplay`** — then the packaging is the work, and `gtk4`'s requirement is the thing that is wrong.

## Do not work around it by relaxing gtk4

`gtk4.spec` carries a `%{rhel}` guard that drops the GStreamer dependency, and extending it to hummingbird would make `gtk4` installable immediately. That exemption exists because the dependency is genuinely circular on EL10 — `bad-free-libs` needs gtk3, which EL10 dropped. Hummingbird builds gtk3 and serves it, so the reasoning does not carry over. Taking that shortcut trades GTK4 video playback for build-order convenience.

## Comment 5913105807

reporter (MEMBER) · hanthor · 2026-09-30T14:16:45Z · https://github.com/tuna-os/tunaos-packages/issues/540#issuecomment-5913105807

Following the convergence refactor in #631 (commit `447c37e`), GNOME 51 on Hummingbird is consumed from `projectbluefin/utah-packages` by digest.

Measurement against the live indexes via `scripts/check-hummingbird-installability.py` confirms:
- Consumed `gtk4` (from `utah-packages`) and published `qt6-qtmultimedia` (from `tunaos-hummingbird`) both require `libgstplay-1.0.so.0()(64bit)` provided by `gstreamer1-plugins-bad-free-libs`.
- Neither `public-hummingbird`, `utah-packages`, nor the published `tunaos-hummingbird` repository currently provides `gstreamer1-plugins-bad-free-libs`.
- In `tunaos-packages`, `gstreamer1-plugins-bad-free` is properly declared in `manifests/catalog.yaml` and placed at `layer-14` in `build-order-hummingbird-desktops.yml` as a dist-git package. Rawhide's spec correctly packages `libgstplay-1.0.so.0` in the `-libs` subpackage.

This issue is blocked waiting for the package factory pipeline to build and publish `gstreamer1-plugins-bad-free` (layer-14) to the Hummingbird repository prefix `repo.tunaos.org/hummingbird/20251124-x86_64/` (or for upstream `projectbluefin/utah-packages` to build and publish it).

— hive: backend=agy model=gemini-3.7-flash-high effort=low

---
🐝 **Hive Agent**: `contributor` | **SHA:** `c68ec01`
