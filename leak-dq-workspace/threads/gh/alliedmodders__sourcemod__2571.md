# [Bug]: Heap corruption / deterministic `free(): invalid pointer` crash in PlayerManager destructor on shutdown (SDK2013 engine target)

- URL: https://github.com/alliedmodders/sourcemod/issues/2571
- Repo: alliedmodders/sourcemod (language: C++)
- State: open; created 2026-09-13T14:52:08Z; status ok; passes main

## Issue body

reporter (NONE) · stive101 · 2026-09-13T14:52:08Z · https://github.com/alliedmodders/sourcemod/issues/2571

### Prerequisites

- [x] I have checked that my issue doesn't exist yet in the [issue tracker](https://github.com/alliedmodders/sourcemod/issues)

### Operating System and Version

Ubuntu 24

### Game / AppID and Version

Source SDK Multiplayer

### SourceMod Version

Newest stable

### Metamod:Source Version

Newest Stable

### Version Verification

- [x] I have updated SourceMod to the [latest version](https://www.sourcemod.net/downloads.php) and the issue persists
- [x] I have updated SourceMod to the [latest snapshot](https://www.sourcemod.net/downloads.php?branch=dev) and the issue persists
- [x] I have updated Metamod:Source to the [latest snapshot](https://sourcemm.net/downloads.php?branch=dev) and the issue persists

### Updated SourceMod Version

1.12 - build 7253

### Updated Metamod:Source Version

.12 - build 1226:

### Description

## SourceMod Version
1.12.0.7253 (stock build, `sourcemod.2.sdk2013.so`)

## Description of the problem
On every clean server shutdown/restart (`quit`, `+restart`), the server deterministically crashes with:

free(): invalid pointer

### Steps to Reproduce

This happens even with **zero third-party plugins loaded** (clean SourceMod install, only Core) and **zero players connected** at the time of shutdown. Reproduced with `MALLOC_CHECK_=3` set, which confirms this is a genuine invalid/corrupted heap pointer, not a random race.

## Backtrace (gdb, no debug symbols but resolved dynamic symbols)

#0 abort () from libc.so.6
#1 ?? () from libc.so.6
#2 ?? () from libc.so.6
#3 ?? () from libc.so.6
#4 free () from libc.so.6
#5 operator delete(void*) () from libstdc++.so.6
#6 operator delete () from libstdc++.so.6
#7 PlayerManager::~PlayerManager () from sourcemod.2.sdk2013.so
#8 __cxa_finalize () from libc.so.6
#9 __do_global_dtors_aux () from sourcemod.2.sdk2013.so
...
#19 UnloadInterface_MMS () from sourcemod_mm_i486.so
#20 Unloader::ReadyToUnload(int) () from metamod.2.sdk2013.so
...
#29 SV_ShutdownGameDLL () from engine_srv.so

The crash occurs on the **second** `delete[]` call inside `PlayerManager::~PlayerManager()` during the global destructor chain triggered by `dlclose()` on module unload.

## Suspected root cause
This looks structurally identical to the historically fixed issue #1107 (unchecked `-1` return of `engine->GetPlayerUserId()` writing out of bounds into `m_UserIdLookUp`, corrupting the heap chunk header, with the crash surfacing much later at `free()`).

That specific instance (in `InvalidatePlayer()`) was fixed in commit 8c380e4 (Oct 2019). However, the **same unchecked pattern still exists** in `PlayerManager::OnClientConnect()`:

```cpp
m_UserIdLookUp[engine->GetPlayerUserId(pEntity)] = client;
```

No bounds/`-1` check is performed here, same as the originally reported bug. Given this reproduces 100% deterministically on a custom SDK2013-based mod (non-standard edict/userid handling), it's plausible this specific engine target hits the `-1` edge case reliably where stock games rarely do.

## Suggested fix
Apply the same guard as in the #1107 fix:
```cpp
int userid = engine->GetPlayerUserId(pEntity);
if (userid >= 0 && userid <= USHRT_MAX)
{
    m_UserIdLookUp[userid] = client;
}
```

## Environment
- Engine target: SDK2013 (custom mod, "sgm_beta")
- OS: Linux (i386/x86 32-bit binaries)
- Reproducible on every shutdown, independent of player count/session activity

### Relevant Log Output

```shell

```

## Comment 5654205457

maintainer (MEMBER) · psychonic · 2026-09-13T15:29:22Z · https://github.com/alliedmodders/sourcemod/issues/2571#issuecomment-5654205457

The suggested change seems fine as a good defensive check, but it may or may not actually fix the issue. The suggested root cause is just speculative, and the part about edict and userid handling doesn't make sense, as mods don't have control over that. It's in the engine

## Comment 5654592414

reporter (NONE) · stive101 · 2026-09-13T16:39:32Z · https://github.com/alliedmodders/sourcemod/issues/2571#issuecomment-5654592414

yeah its just speculative but the only hangup i found ;/

## Comment 5673959615

maintainer (MEMBER) · Kenzzer · 2026-09-15T02:55:01Z · https://github.com/alliedmodders/sourcemod/issues/2571#issuecomment-5673959615

I'm essentially going to repeat what was already said, but here goes.

While userid being potentially -1 made sense in the context of #1107 I don't see it here.

One has to essentially showcase the engine has not assigned a user id to the edict **it provides** under `IServerGameClients::ClientConnect`. It's safe to say that regardless this should be guarded against, but I don't believe this is the source of your specific issue.

## Comment 5674862713

reporter (NONE) · stive101 · 2026-09-15T04:45:01Z · https://github.com/alliedmodders/sourcemod/issues/2571#issuecomment-5674862713

"I think one of the issues is that the mod I play has a cure-time fix where a fake player joins while the server is starting up and leaves afterward.
Maybe the join happens too early during the startup process, and when the fake player leaves, it produces the -1."
