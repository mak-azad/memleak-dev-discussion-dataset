# Memory Leaks

- URL: https://github.com/chivurazvangabriel/LiminalBlocks/issues/2
- Repo: chivurazvangabriel/LiminalBlocks (language: C++)
- State: open; created 2026-03-25T10:12:59Z; status ok; passes main

## Issue body

reporter (NONE) · iLaurian · 2026-03-25T10:12:59Z · https://github.com/chivurazvangabriel/LiminalBlocks/issues/2

The manual delete calls are inconsistent and incomplete in `main.cpp:188-193`:
- delete postProcessingManager is missing (allocated with new at line 120)
- SubsystemManager is never deleted (it uses static storage)
- WindowManager is not deleted

Static singletons `World::GetOrCreate()` (`World.cpp:150`) and `SubsystemManager::Get()` (`SubsystemManager.cpp:12`) create leaks since they're never destroyed.

Inconsistent Memory Management (`World.cpp`)
- `WorldGenerator` is allocated with `new` but never deleted in destructor
- Chunks are allocated with `new` but never freed

Missing Null Check (`World.cpp:50-52`)
```
void World::SetBlockAtLocation(int x, int y, int z, Block *block) {
    auto chunk = GetChunkAtBlockLocation(x, y, z);  // chunk could be nullptr
    InitializeBlockAtLocation(x, y, z, block);     // crashes if chunk invalid
    OnChunkChanged.Broadcast(chunk, ...);          // nullptr broadcast
}
```
