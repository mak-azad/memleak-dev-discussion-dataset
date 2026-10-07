# malloc() corrupted topsize when trying to install current release

- URL: https://github.com/open-watcom/open-watcom-v2/issues/1557
- Repo: open-watcom/open-watcom-v2 (language: C)
- State: open; created 2025-12-20T09:08:58Z; status ok; passes offcwe

## Issue body

reporter (NONE) · angrypig555 · 2025-12-20T09:08:58Z · https://github.com/open-watcom/open-watcom-v2/issues/1557

I made the  open-watcom-2_0-c-linux-x64  executable with chmod +x and when i try to run it i get this in the terminal:

<img width="2092" height="368" alt="Image" src="https://github.com/user-attachments/assets/d3219ad4-b587-4645-b02b-1f7377c8ff1f" />

This is inside the ubuntu WSL2 on windows 11

## Comment 3677638696

reporter (NONE) · angrypig555 · 2025-12-20T09:13:11Z · https://github.com/open-watcom/open-watcom-v2/issues/1557#issuecomment-3677638696

Using the x86 installer, the installer starts but then theres an internal error and segmentation faults, then the random garbage appears in the terminal

## Comment 3677640684

reporter (NONE) · angrypig555 · 2025-12-20T09:16:23Z · https://github.com/open-watcom/open-watcom-v2/issues/1557#issuecomment-3677640684

Running it in an external terminal (64 bit version) will cause it to reach the file copying part where it will crash due to segmentation fault error

## Comment 3677753649

maintainer (MEMBER) · jmalak · 2025-12-20T11:39:43Z · https://github.com/open-watcom/open-watcom-v2/issues/1557#issuecomment-3677753649

It is known problem (not fixed yet), as workaround you can use Linux 32-bit installer which has same functionality as 64-bit installer.
