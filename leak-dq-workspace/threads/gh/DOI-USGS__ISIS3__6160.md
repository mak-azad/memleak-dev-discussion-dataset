# Pvl::setFormatTemplate deletes a Pvl through a non-virtual PvlContainer* (mismatched new/delete size)

- URL: https://github.com/DOI-USGS/ISIS3/issues/6160
- Repo: DOI-USGS/ISIS3 (language: C++)
- State: open; created 2026-09-19T10:41:34Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · ljbade · 2026-09-19T10:41:34Z · https://github.com/DOI-USGS/ISIS3/issues/6160

## Summary

`Pvl::setFormatTemplate()` stores a heap-allocated `Pvl` object through a `PvlContainer*` member (`m_formatTemplate`), then later `delete`s it through that same base-class pointer. Neither `PvlContainer` nor `PvlObject` (the two classes between `PvlContainer` and `Pvl` in the hierarchy) declares a destructor, virtual or otherwise -- so `delete`ing a `Pvl` object through a `PvlContainer*` is undefined behaviour: it deallocates using `PvlContainer`'s size instead of the actual `Pvl` object's size, and skips the `Pvl`/`PvlObject`-specific destructor logic entirely. Found via `valgrind`, which flags it directly as "Mismatched new/delete size value".

**Environment**: Built from source, `dev` @ `095c406d5dd5e8a007f8c9d397ae66921cf2a5e9`.

## Root cause

`m_formatTemplate` is declared in the base-most class, `PvlContainer` (`isis/src/core/include/PvlContainer.h:306`):
```cpp
PvlContainer *m_formatTemplate;
```

`Pvl::setFormatTemplate(const QString &file)` allocates a full `Pvl` object but stores it through this base-class pointer (`isis/src/core/src/Pvl.cpp`):
```cpp
void Pvl::setFormatTemplate(const QString &file) {
  if(m_internalTemplate) delete m_formatTemplate;
  m_internalTemplate = true;
  m_formatTemplate = new Isis::Pvl(file);
}
```

`Pvl`'s own destructor later deletes it the same way (`isis/src/core/include/Pvl.h:136-138`):
```cpp
~Pvl() {
  if(m_internalTemplate) delete m_formatTemplate;
};
```

The class hierarchy is `Pvl : public PvlObject`, `PvlObject : public PvlContainer` -- and none of the three declares a destructor with the `virtual` keyword (`PvlContainer` and `PvlObject` don't declare one at all; `Pvl`'s own destructor above is non-virtual too). `delete`ing a `Pvl*` through a `PvlContainer*` (or `PvlObject*`) pointer when there is no virtual destructor anywhere in the chain is classic undefined behaviour: the compiler emits a fixed-size deallocation call based on the **static** type of the pointer (`PvlContainer`), not the object's actual (`Pvl`) type.

## Valgrind output

```
==27989== Mismatched new/delete size value: 128
==27989==    at 0x4848809: operator delete(void*, unsigned long) (vg_replace_malloc.c:1181)
==27989==    by 0x9C34CC5: Isis::Pvl::setFormatTemplate(QString const&) (Pvl.cpp:564)
==27989==    by 0x75E56C2: Isis::Cube::writeLabels() (Cube.cpp:3008)
==27989==    by 0x75E87CD: Isis::Cube::close(bool) (Cube.cpp:274)
==27989==    by 0x75F8A96: Isis::Cube::fromLabel(Isis::FileName const&, Isis::Pvl&, QString) (Cube.cpp:85)
==27989==    by 0x75F8D7D: Isis::Cube::fromIsd(...) (Cube.cpp:100)
==27989==    by 0xEF671B: Isis::DefaultCube::SetUp() (CameraFixtures.cpp:190)
==27989==  Address 0x2ed6bee0 is 0 bytes inside a block of size 176 alloc'd
==27989==    at 0x4844F93: operator new(unsigned long) (vg_replace_malloc.c:487)
==27989==    by 0x9C34CDF: Isis::Pvl::setFormatTemplate(QString const&) (Pvl.cpp:566)
==27989==    by 0x75E56C2: Isis::Cube::writeLabels() (Cube.cpp:3008)
==27989==    by 0x75F45CF: Isis::Cube::create(QString const&) (Cube.cpp:675)
==27989==    by 0x75F8912: Isis::Cube::fromLabel(Isis::FileName const&, Isis::Pvl&, QString) (Cube.cpp:78)
==27989==    by 0x75F8D7D: Isis::Cube::fromIsd(...) (Cube.cpp:100)
==27989==    by 0xEF671B: Isis::DefaultCube::SetUp() (CameraFixtures.cpp:190)

==27989== Mismatched new/delete size value: 128
==27989==    at 0x4848809: operator delete(void*, unsigned long) (vg_replace_malloc.c:1181)
==27989==    by 0x75035D0: Isis::Pvl::~Pvl() (Pvl.h:137)
==27989==    by 0x75AEC9D: Isis::Cube::cleanUp(bool) (Cube.cpp:2448)
==27989==    by 0x75E8790: Isis::Cube::close(bool) (Cube.cpp:276)
==27989==    by 0x75F8A96: Isis::Cube::fromLabel(Isis::FileName const&, Isis::Pvl&, QString) (Cube.cpp:85)
==27989==    by 0x75F8D7D: Isis::Cube::fromIsd(...) (Cube.cpp:100)
==27989==    by 0xEF671B: Isis::DefaultCube::SetUp() (CameraFixtures.cpp:190)
==27989==  Address 0x2eda9840 is 0 bytes inside a block of size 176 alloc'd
==27989==    at 0x4844F93: operator new(unsigned long) (vg_replace_malloc.c:487)
==27989==    by 0x9C34CDF: Isis::Pvl::setFormatTemplate(QString const&) (Pvl.cpp:566)
==27989==    by 0x75E56C2: Isis::Cube::writeLabels() (Cube.cpp:3008)
==27989==    by 0x75E87CD: Isis::Cube::close(bool) (Cube.cpp:274)
```

`sizeof(PvlContainer)` (128 bytes, what the delete call assumes) versus the actual `sizeof(Pvl)` (176 bytes, what was allocated) accounts exactly for the "128" vs the "block of size 176" in Valgrind's report -- concrete confirmation this is the base-vs-derived size mismatch described above, not a different bug with a coincidentally similar message.

This fires every time `Cube::writeLabels()` runs (i.e. on essentially every cube write that involves a format template), so it's a very hot path -- it just doesn't crash in practice because in every case we saw, the "extra" `PvlObject`/`Pvl`-specific state being skipped happens to not matter (no leaked resources with observable side effects in the common case). It's still undefined behaviour per the C++ standard, and the exact consequences (leaked derived-class members, ASan/hardened-allocator aborts, etc.) are implementation-defined and version-dependent -- this is exactly the kind of latent bug that can turn into a real crash after e.g. a toolchain/allocator upgrade, unrelated code changes to `Pvl`/`PvlObject`'s member layout, or a hardened allocator build.

## Suggested fix

Give `PvlContainer` (or at minimum `PvlObject`, the class actually intended to be a polymorphic base within this hierarchy) a `virtual` destructor. This is the standard, minimal fix for "deleting a derived object through a base pointer" -- it makes the deallocation correctly use the object's dynamic type and lets `Pvl`'s and `PvlObject`'s own destructor logic run properly. Given how widely `PvlContainer`/`PvlObject`/`Pvl` are used throughout ISIS, this should be a low-risk, additive change (adding `virtual` to an existing destructor, or adding one where none exists, doesn't change any existing call site's behavior for non-polymorphic use).

---

*Found via `valgrind --track-origins=yes` (Valgrind 3.24.0) while investigating an unrelated test crash, with the assistance of Claude Code (Anthropic's AI coding agent). The Valgrind output above is real tool output from our own build/run (`dev` @ `095c406d5`), and the `sizeof(PvlContainer)`/`sizeof(Pvl)` explanation was confirmed by reading the actual class declarations, not inferred from the Valgrind message alone.*


## Comment 5741201079

reporter (CONTRIBUTOR) · ljbade · 2026-09-19T10:50:30Z · https://github.com/DOI-USGS/ISIS3/issues/6160#issuecomment-5741201079

## Checked other obvious polymorphic base classes -- none reproduce this specific defect

At the reporter's request, I checked whether the same class of bug (a base class with no virtual destructor, used polymorphically via a base-typed pointer that later gets `delete`d) recurs in the other big polymorphic hierarchies used the same way elsewhere in ISIS: `ShapeModel` (via `Target::m_shape`, constructed as `NaifDskShape`/`DemShape`/`EquatorialCylindricalShape`/`EllipsoidShape`/`PlaneShape` etc. through `ShapeModelFactory::create()`), `AtmosModel`, `PhotoModel`, and the five `Camera::Set*Map` base classes (`CameraDistortionMap`, `CameraFocalPlaneMap`, `CameraDetectorMap`, `CameraGroundMap`, `CameraSkyMap` -- see the [comment on #6159](https://github.com/DOI-USGS/ISIS3/issues/6159) for a *different*, unrelated defect found in that family).

All of these correctly declare a `virtual` destructor:

```
isis/src/base/objs/ShapeModel/ShapeModel.h:76:            virtual ~ShapeModel()=0;
isis/src/base/objs/AtmosModel/AtmosModel.h:64:            virtual ~AtmosModel() {};
isis/src/lro/objs/PhotoModel/PhotoModel.h:44:              virtual ~PhotoModel() {};
isis/src/base/objs/CameraDistortionMap/CameraDistortionMap.h:47:  virtual ~CameraDistortionMap();
isis/src/base/objs/CameraGroundMap/CameraGroundMap.h:82:      virtual ~CameraGroundMap() {};
isis/src/base/objs/CameraSkyMap/CameraSkyMap.h:37:        virtual ~CameraSkyMap() {};
isis/src/base/objs/CameraDetectorMap/CameraDetectorMap.h:51:    virtual ~CameraDetectorMap();
isis/src/base/objs/CameraFocalPlaneMap/CameraFocalPlaneMap.h:89:  virtual ~CameraFocalPlaneMap();
```

So this specific bug -- deleting a derived object through a non-virtual-destructor base pointer -- appears to be isolated to the `Pvl` / `PvlObject` / `PvlContainer` hierarchy rather than a systemic pattern across ISIS's other polymorphic model hierarchies. I did not do an exhaustive codebase-wide search for every base-pointer-holding-a-derived-object pattern (that would be a much larger undertaking), just checked the other obvious, similarly-structured "factory constructs one of several subclasses, stores/deletes it via a common base pointer" cases that are structurally closest to this one.

---

*Checked at the reporter's request, with the assistance of Claude Code (Anthropic's AI coding agent).*

