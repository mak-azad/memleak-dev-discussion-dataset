# JSON map import silently drops an area with a blank name and leaks its TArea

- URL: https://github.com/Mudlet/Mudlet/issues/10396
- Repo: Mudlet/Mudlet (language: C++)
- State: open; created 2026-09-04T22:07:47Z; status ok; passes main

## Issue body

reporter (MEMBER) · vadi2 · 2026-09-04T22:07:47Z · https://github.com/Mudlet/Mudlet/issues/10396

### Brief summary of the issue

When a JSON map contains an area with a blank name, `loadJsonMap()` silently discards that area and every room in it, reports success, and leaks the `TArea` object.

Two faults on one line, in [`TMap::readJsonMapFile()`](https://github.com/Mudlet/Mudlet/blob/development/src/TMap.cpp#L3737):

```cpp
std::unique_ptr<TArea> pArea = std::make_unique<TArea>(this, pNewRoomDB.get());
auto [id, name] = pArea->readJsonArea(...);
...
pNewRoomDB->addArea(pArea.release(), id, name);
```

`release()` gives up ownership unconditionally, but [`TRoomDB::addArea(TArea*, int, const QString&)`](https://github.com/Mudlet/Mudlet/blob/development/src/TRoomDB.cpp#L608) opens with:

```cpp
if (name.isEmpty()) {
    return false;
}
```

It never stores `pA` and never deletes it. `TArea` is a plain class with no `Q_OBJECT` and no parent, so nothing else cleans it up. The `false` return is also ignored at the call site, which is why the import reports success.

### Steps to reproduce the issue

```lua
openMapWidget()
local path = getMudletHomeDir() .. "/probe.json"
local areaId = addAreaName("ProbeArea")
local roomId = createRoomID()
addRoom(roomId); setRoomArea(roomId, areaId)
saveJsonMap(path)

-- blank out the area's name in the saved file
local f = io.open(path, "rb"); local t = f:read("*a"); f:close()
f = io.open(path, "wb"); f:write((t:gsub('"ProbeArea"', '""'))); f:close()

print("loadJsonMap:", loadJsonMap(path))
for name, id in pairs(getAreaTable()) do print("area:", name, id) end
```

### Error output / provide screenshots of the issue

```
loadJsonMap:	true
area:	Default Area	-1
area:	Unnamed Area	1
```

`ProbeArea` and its room are gone, and the import still returned `true`.

For the leak I ran the same scenario under gdb with breakpoints on `TRoomDB::addArea(TArea*, int, QString const&)` and `TArea::~TArea`:

```
LEAKPROBE_ADDAREA pA=0x55555b01ca70 id=-1 name_len=12
LEAKPROBE_ADDAREA pA=0x55555b023ed0 id=1  name_len=0
...
LEAKPROBE_DTOR this=0x55555b01ca70      <- the named area, destroyed
(no destructor call for 0x55555b023ed0 for the rest of the process)
```

The area whose name was empty is never destroyed; its accepted sibling is. The `TArea` also owns whatever `readJsonArea()` populated into it, so the leak is not just the one object.

### Extra information, such as Mudlet version, operating system and ideas for how to solve / implement

Confirmed on `development` at 35dce0e30, Linux, self-built debug.

Three things want fixing:

1. **Do not `release()` before the callee has accepted.** Check the return of `addArea()` and only release on success, or change `addArea` to take the `unique_ptr` so ownership is explicit.
2. **Do not silently drop the area.** Either give a blank-named imported area a generated name the way `TRoomDB::addArea(int)` does for unnamed areas, or fail the import with a message naming the offending area. Right now a user importing a map from another client can lose whole areas and be told it worked.
3. `readJsonMapFile()` should not ignore `addArea()`'s `bool` return.

Found while writing map specs.


## Comment 5547593897

reporter (MEMBER) · vadi2 · 2026-09-04T23:24:51Z · https://github.com/Mudlet/Mudlet/issues/10396#issuecomment-5547593897

Independently confirmed by CI's LeakSanitizer, which is a stronger witness than the gdb session in the description - different machine, different Qt (6.11.1), no debugger involved.

A spec that imported a JSON map with one blank-named area was enough to turn the `ubuntu / gcc / lua tests + leak detection` job red, with the busted run itself reporting `4087 successes / 0 failures / 0 errors`:

```
==62058==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #1 std::make_unique<TArea, TMap*, TRoomDB*>(TMap*&&, TRoomDB*&&)
    #2 TMap::readJsonMapFile(QString const&, bool) at src/TMap.cpp:3729
    #3 TLuaInterpreter::loadJsonMap(lua_State*) at src/TLuaInterpreterMapper.cpp:2715

Indirect leak of 192 byte(s) in 1 object(s) allocated from:
    #9  QSet<int>::insert(int const&)
    #10 TArea::readJsonArea(QJsonArray const&, int) at src/TArea.cpp:863
    #11 TMap::readJsonMapFile(QString const&, bool) at src/TMap.cpp:3730

SUMMARY: AddressSanitizer: 640 byte(s) leaked in 4 allocation(s).
```

The `TArea` built at `TMap.cpp:3729` is handed to `TRoomDB::addArea(pArea.release(), id, name)`, which returns early on the empty name without storing or deleting it - so the object and the `QSet<int>` members `readJsonArea()` had already filled on the next line are both stranded. 640 bytes per blank-named area in the file.

Practical consequence for the test suite: any spec that exercises this path fails the leak-detection job even when every assertion passes. The spec that found it is parked as `pending` against this issue in #10398 rather than shipped, so it can be un-parked when this is fixed.
