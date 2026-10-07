# Memory leaks, an AI targeting bug and an MP desync source

- URL: https://github.com/LoneGazebo/Community-Patch-DLL/issues/13363
- Repo: LoneGazebo/Community-Patch-DLL (language: C++)
- State: open; created 2026-09-14T19:54:41Z; status ok; passes main

## Issue body

reporter (NONE) · EmptyMonad · 2026-09-14T19:54:41Z · https://github.com/LoneGazebo/Community-Patch-DLL/issues/13363

### 1. Mod version

5.4.6

### 2. Installed Components

Vox Populi with EUI

### 3. Additional mods used

_No response_

### 4. Describe the Issue

Found while maintaining a 4.22-based build; each one was re-checked against master at dcb33a6 (5.4.6 Release). Line links point at that commit.

Leaks
CvMap::uninit misses three map-sized arrays that InitPlots allocates: m_pVisibilityCountThisTurnMax, m_pKnownVisibilityCount ([L611](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvMap.cpp#L611), [L613](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvMap.cpp#L613)) and m_pHumanPlannedRouteState ([L626](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvMap.cpp#L626)). That's teams × plots bytes each (~2 MB on Huge), leaked on every load / new game.

SAFE_DELETE_ARRAY(m_pVisibilityCountThisTurnMax);
SAFE_DELETE_ARRAY(m_pKnownVisibilityCount);
SAFE_DELETE_ARRAY(m_pHumanPlannedRouteState);
CvGame::GetDiploResponse: tempDatabase = new Database::Results() ([L5992](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvGame.cpp#L5992)) is never deleted, so every leader line leaks a prepared statement when NO_RANDOM_TEXT_CIVS is on. A stack Database::Results kQuery; fixes it.

CvPlotManager: AddLayer heap-allocates each CvSparseIDInfoGrid ([L251](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvPlotManager.cpp#L251)) but Uninit only calls m_aLayers.clear() ([L206](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvPlotManager.cpp#L206)), and the destructor is empty. Delete m_pkGrid for each entry in Uninit and call Uninit() from the destructor. Also, ~CvSparseIDInfoGrid's loop for (uint uiIndex = m_uiMaxIndex; --uiIndex;) ([L104](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvPlotManager.cpp#L104)) skips the last entry and underflows when m_uiMaxIndex == 0. Use for (uint i = 0; i < m_uiMaxIndex; ++i).

Flavor type strings: paFlavors = FNEW(CvString[...]) ([L412](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvDllDatabaseUtility.cpp#L412)) runs again on every database reload, and m_paszFlavorTypes is never freed. Add SAFE_DELETE_ARRAY(paFlavors) before the FNEW and SAFE_DELETE_ARRAY(m_paszFlavorTypes) in CvGlobals::deleteInfoArrays.

Memory held longer than needed
CvDangerPlots::Uninit uses m_DangerPlots.clear() ([L55](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvDangerPlots.cpp#L55)). clear() keeps the capacity, so every player slot holds a map-sized grid through the main menu and into the next load, which roughly doubles peak usage while loading. Use vector<CvDangerPlotContents>().swap(m_DangerPlots);. It's also worth releasing it in CvPlayer::setAlive(false), and skipping UpdateDanger for dead players.

Replay data copied by value: const map<CvString, CvPlayer::TurnData> replayData = ...getReplayData(); in CvReplayInfo::createInfo ([L139](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvReplayInfo.cpp#L139)) and CvLuaPlayer::lGetReplayData ([L11244](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/Lua/CvLuaPlayer.cpp#L11244)) copies each player's whole per-turn history, which spikes memory during saves and on the graph screens. Make both const ... &. In createInfo, also fill dataSet[uiDataSet] in place instead of copying a temporary TurnData, and swap dataSet into m_listPlayerDataSets.

AI bug
CvMap::GetPlotsAtRangeX without line of sight, range 2 iterates RING2_PLOTS..RING3_PLOTS ([L3205](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/CvMap.cpp#L3205)), which is the range-3 ring. Callers iterate ring by ring, so aircraft and indirect-fire units never see targets at exactly 2 tiles and see ring 3 twice. It should be RING1_PLOTS..RING2_PLOTS, matching the LoS branch.

Multiplayer desync source
WhosWinningPopup.lua rolls the synchronized RNG from UI code ([L92](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/(2)%20Vox%20Populi/Core%20Files/Overrides/WhosWinningPopup.lua#L92), [L112](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/(2)%20Vox%20Populi/Core%20Files/Overrides/WhosWinningPopup.lua#L112), inherited from the base game), inside a reroll loop. It advances JonRand on the viewing client only. Use math.random(n) - 1. As a general guard, CvLuaGame::lRand ([L1693](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/Lua/CvLuaGame.cpp#L1693)) could return GC.getASyncRand() when !gDLL->IsGameCoreThread(), so no UI mod can desync games through Game.Rand.

Clang builds with newer LLVM
With the VC9 include path ahead of clang's builtin headers, va_start is VC9's &param + sizeof macro. Once clang inlines a variadic function such as CvString::format, that address points into the caller's frame, and the DLL crashes during DllMain (LoadLibrary error 1114), seen with LLVM 23. A forced include (/FI) that redefines va_start, va_arg, va_end and _crt_va_* to the __builtin_va_* versions fixes it.

### 5. Save Game From 1 Turn Before (ALWAYS ATTACH THIS IF POSSIBLE)

_No response_

### 6. Logs (ALWAYS ATTACH THESE IF POSSIBLE)

_No response_

### 7. Crash dump and crashes.log (ALWAYS ATTACH IF REPORTING A CRASH)

_No response_

## Comment 5673397451

maintainer (COLLABORATOR) · azum4roll · 2026-09-15T01:43:34Z · https://github.com/LoneGazebo/Community-Patch-DLL/issues/13363#issuecomment-5673397451

> It's also worth releasing it in CvPlayer::setAlive(false), and skipping UpdateDanger for dead players.

Players can be returned to life in any point of the game, so probably not for the first part. Yes for skipping UpdateDanger.

> Multiplayer desync source
> WhosWinningPopup.lua rolls the synchronized RNG from UI code ([L92](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/(2)%20Vox%20Populi/Core%20Files/Overrides/WhosWinningPopup.lua#L92), [L112](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/(2)%20Vox%20Populi/Core%20Files/Overrides/WhosWinningPopup.lua#L112), inherited from the base game), inside a reroll loop. It advances JonRand on the viewing client only. Use math.random(n) - 1. As a general guard, CvLuaGame::lRand ([L1693](https://github.com/LoneGazebo/Community-Patch-DLL/blob/dcb33a654cd9e8efb038a0733b4025e19cbcd8ba/CvGameCoreDLL_Expansion2/Lua/CvLuaGame.cpp#L1693)) could return GC.getASyncRand() when !gDLL->IsGameCoreThread(), so no UI mod can desync games through Game.Rand.

It's ok. That popup doesn't show up in MP. In the long run, we should change CvLuaGame::lRand to use CvGame::randRangeExclusive and take in a seed parameter.

What did you use to analyze the code?
