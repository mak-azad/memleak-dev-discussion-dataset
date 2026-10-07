# Factory build backlog from Utah bare-metal audit (551 Bluefin names in neither repo)

- URL: https://github.com/projectbluefin/utah-packages/issues/308
- Repo: projectbluefin/utah-packages (language: Python)
- State: open; created 2026-09-30T21:48:35Z; status ok; passes main

## Issue body

reporter (MEMBER) · hanthor · 2026-09-30T21:48:35Z · https://github.com/projectbluefin/utah-packages/issues/308

Utah bare-metal audit diffed Bluefin classic (1806 names) against Utah (1053). After removing Hummingbird-available (218, Utah-side manifest work) and already-factory-built (33, Utah-side consume — projectbluefin/utah#382), **551 names are in neither repo**. They need factory builds (or explicit wontfix). By area, suggested priority order:

1. **Codecs/media** (~40): openh264 or gstreamer1-plugin-libav (GStreamer H.264 is entirely missing), ugly-free, plugin-dav1d, ffmpeg-full decision + tail (x264/x265, vvenc/vvdec, svt-vp9, davs2, faad2, LCEVCdec, libde265, libdovi, libplacebo, libbluray…), papers/ffmpeg/gst thumbnailers. (Intel media driver + bad-free already built — Utah consume tracked in utah#382/utah#383.)
2. **Power** (3): tuned, tuned-ppd, thermald — Utah has no laptop power story (utah#388).
3. **VPN** (~13): openvpn, openconnect, vpnc + NetworkManager plugins (utah#389).
4. **Printing/scanning** (~26): hplip, gutenprint, sane-backends, sane-airscan, ipp-usb, system-config-printer, driver tail (utah#390).
5. **GNOME apps** (~20): disk-utility, system-monitor, remote-desktop, color-manager, tour, browser-connector, ptyxis… (utah#391).
6. **Dev tools** (~25): xdg-utils (**no xdg-open at all** — highest single item), rsync, nano, tmux, htop, gamemode, bolt, exfatprogs, f2fs-tools… (utah#392).
7. **Fonts/i18n overflow**: nerd-fonts, jetbrains-mono, symbola, urw-base35, adobe-source-code-pro, ibus engines (anthy/chewing/hangul/libpinyin/typing-booster), m17n, langtable (utah#393; the 113 default-fonts-* come from Hummingbird, no factory work).
8. **ujust deps** (4): fpaste (device-info), glow (changelogs), powerstat (power-draw), gh (report fallback) — all Go/Python-simple (utah#394).
9. **Unblockers**: anaconda-webui + qt6-qtwebengine (would unstick factory-built anaconda-live + slitherer, currently uninstallable).
10. **Long tail** (~300): python3 modules (~50), lang runtimes, netfs clients, virt stack, hw tools, perl/ruby/go pieces, texlive bits. Happy to split per-area issues on request — method: `comm -23 bluefin-rpmqa utah-rpmqa" minus Hummingbird-available minus factory-repo names, verified 2026-09-30 against factory `sha256:0f04cff…".

Note: factory spec dirs already exist (unpublished) for intel-mediasdk, intel-vpl-gpu-rt, libvpl — publishing those closes the Intel encode half.

## Comment 5920578600

reporter (MEMBER) · hanthor · 2026-09-30T22:08:29Z · https://github.com/projectbluefin/utah-packages/issues/308#issuecomment-5920578600

Audit evidence (package partitions + method + input digests): https://gist.github.com/hanthor/b9b1e3a7f13c51376b771f97a7409a30

## Comment 5922670389

other (CONTRIBUTOR) · dtg01100 · 2026-10-01T01:09:15Z · https://github.com/projectbluefin/utah-packages/issues/308#issuecomment-5922670389

The 551-name backlog from this issue is now a tracked artifact: PR #309 (https://github.com/projectbluefin/utah-packages/pull/309) adds the catalog (`config/factory-build-backlog.toml`), the auditor (`tools/factory_build_backlog.py`), the committed snapshot, the unit tests, the Justfile recipe, and the skill doc. Closing each backlog gap is now a two-edit move (remove from the area + add to `[resolved]` or `[wontfix]`); the gate catches every silent shrinkage. CI wiring ships in a follow-up because this contributor's OAuth token lacks the `workflow` scope; a maintainer who has it can land the three prepared files (`Justfile`, `.github/workflows/validate.yml`, `.github/workflows/recalculate-factory-build-backlog.yml`) in one commit.

— hive: backend=omp model=minimax-code/MiniMax-M3

---
🐝 **Hive Agent**: `contributor` | **SHA:** `unknown`
