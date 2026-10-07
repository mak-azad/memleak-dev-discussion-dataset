# malloc error on macOS Sequoia: pointer being freed was not allocated - crashes on login

- URL: https://github.com/lastpass/lastpass-cli/issues/727
- Repo: lastpass/lastpass-cli (language: C)
- State: open; created 2026-01-03T19:23:20Z; status ok; passes main

## Issue body

reporter (NONE) · motorthings · 2026-01-03T19:23:20Z · https://github.com/lastpass/lastpass-cli/issues/727

**Summary:**
  LastPass CLI crashes immediately on login with a malloc error on macOS Sequoia 15.6.

  **Environment:**
  - **OS:** macOS Sequoia 15.6 (Darwin 24.6.0)
  - **Architecture:** Apple Silicon (arm64)
  - **LastPass CLI version:** 1.6.1_2 (installed via Homebrew)
  - **Installation method:** `brew install lastpass-cli`

  **Steps to Reproduce:**
  1. Install lastpass-cli via Homebrew: `brew install lastpass-cli`
  2. Run: `lpass login <email>`
  3. Observe immediate crash before password prompt

  **Expected Behavior:**
  The command should prompt for the master password and proceed with login.

  **Actual Behavior:**
  The command crashes immediately with a malloc error:
  lpass(78847,0x1fbe220c0) malloc: *** error for object 0x600000000001: pointer being freed was not allocated
  lpass(78847,0x1fbe220c0) malloc: *** set a breakpoint in malloc_error_break to debug
  zsh: abort      lpass login motorthings@gmail.com

  **Additional Context:**
  - The error occurs with both default execution and with `LPASS_DISABLE_PINENTRY=1`
  - All lpass commands appear to trigger the same malloc error
  - The issue prevents any use of the CLI

  **Related Issues:**
  Similar malloc errors have been reported on previous macOS versions:
  - #447 (macOS Mojave)
  - #513 (macOS Catalina)
  - #427 (macOS Mojave Beta)

  This appears to be a continuation of the library compatibility issues on newer macOS versions.

## Comment 3747871403

other (NONE) · jacmacmod · 2026-01-14T05:40:21Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3747871403

I have had the issue many times. Not sure what fixes it but creating new terminal windows seems to help me login but when trying to use tokens I still get that issue so have reverted to saving keys in env variables for now.

## Comment 3805662552

other (NONE) · aclevername · 2026-01-27T14:51:32Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3805662552

Seeing this on Tahoe as well (related: https://github.com/lastpass/lastpass-cli/issues/731)

## Comment 3807842980

other (NONE) · jakegage · 2026-01-27T22:30:27Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3807842980

I can confirm that I've been seeing this for weeks on Sequoia.

## Comment 3854413999

other (NONE) · abaines · 2026-02-05T15:32:29Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3854413999

I'm pretty sure I'm also encountering this issue with the machine:
```
Chip Apple M4 Pro
macOS Sequoia 15.7.3
```
Seems related to https://github.com/lastpass/lastpass-cli/issues/427 and https://github.com/lastpass/lastpass-cli/issues/550 issues.

Hoping for an official LastPass recommended steps to fix this soon.

Thanks! 🤗

## Comment 3881575624

other (NONE) · jdbaudean · 2026-02-11T01:08:11Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3881575624

I'm seeing this too, are there any workarounds?

```
ProductName:		macOS
ProductVersion:		15.7.3
BuildVersion:		24G419
```

## Comment 3890216276

other (NONE) · lhaeger · 2026-02-12T11:04:21Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3890216276

I got exactly this error after upgrading macOS 15.7.3 --> 15.7.4 today. Seems to be related to macOS' `curl` version. I tried compiling `lpass` from source while pointing it at the Homebrew `curl` version (rather than letting it use macOS' curl) and that solved the issue for me:

- `brew uninstall lastpass-cli`
- `brew install curl`
- `git clone https://github.com/lastpass/lastpass-cli.git`
- edit the `Makefile` to begin as follows:
```
# changed to /usr/local
PREFIX ?= /usr/local
MANDIR ?= $(PREFIX)/share/man
BUILDDIR=build
CMAKEMAKE=$(BUILDDIR)/Makefile
# added -DCMAKE_POLICY_VERSION_MINIMUM=3.5
CMAKEOPTS=-DCMAKE_INSTALL_PREFIX:PATH=$(PREFIX) -DCMAKE_INSTALL_MANDIR:PATH=$(MANDIR) -DCMAKE_POLICY_VERSION_MINIMUM=3.5
# added the following lines
LDFLAGS="-L/opt/homebrew/opt/curl/lib"
CPPFLAGS="-I/opt/homebrew/opt/curl/include"
PKG_CONFIG_PATH="/opt/homebrew/opt/curl/lib/pkgconfig"
```
- `make && make install`
- add `/usr/local/bin` to your PATH


## Comment 3899359935

other (NONE) · wfaulk · 2026-02-13T20:43:24Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3899359935

You can do the equivalent thing within homebrew by running `brew edit lastpass-cli`, deleting the line `uses_from_macos 'curl'`, adding the line `depends_on 'curl'` immediately above the `depends_on 'openssl@3'` line, saving that, and then reinstalling with `HOMEBREW_NO_INSTALL_FROM_API=1 brew reinstall --build-from-source lastpass-cli`.

I have submitted [a PR to get this applied within homebrew](https://github.com/Homebrew/homebrew-core/pull/267439).

## Comment 3951327732

other (NONE) · LittaKake · 2026-02-24T12:12:35Z · https://github.com/lastpass/lastpass-cli/issues/727#issuecomment-3951327732

> You can do the equivalent thing within homebrew by running `brew edit lastpass-cli`, deleting the line `uses_from_macos 'curl'`, adding the line `depends_on 'curl'` immediately above the `depends_on 'openssl@3'` line, saving that, and then reinstalling with `HOMEBREW_NO_INSTALL_FROM_API=1 brew reinstall --build-from-source lastpass-cli`.
> 
> I have submitted [a PR to get this applied within homebrew](https://github.com/Homebrew/homebrew-core/pull/267439).

Seems like your PR is merged. I reinstalled lpass cli and everything works as expected now.
