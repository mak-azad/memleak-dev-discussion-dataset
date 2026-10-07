#  Memory leaks in instrument ownership model

- URL: https://github.com/musescore/MuseScore/issues/32722
- Repo: musescore/MuseScore (language: C++)
- State: open; created 2026-03-21T00:54:15Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · CubikingChill · 2026-03-21T00:54:15Z · https://github.com/musescore/MuseScore/issues/32722

## Multiple memory leaks and crashes exist in instrument management:

Memory leaks: Part destructor missing, instruments never freed
Double-free risk: InstrumentChange deletes shared pointers
Use-after-free: setInstruments({}) after shallow-copy leaves dangling pointers
EID assertion: No idempotent registration check causes crashes on memory reuse
Thread-safety: Parallel excerpt serialization races on MIDI mapping

## Root cause: 
No ownership model for Instrument pointers shared between InstrumentChange and Part::m_instruments.

### Checklist

- [x] This report follows the [guidelines](https://github.com/musescore/MuseScore/wiki/Reporting-bugs-and-issues) for reporting bugs and issues
- [x] I have verified that this issue has not been logged before, by searching the [issue tracker](https://github.com/musescore/MuseScore/issues) for similar issues
- [x] I have attached all requested files and information to this report
- [x] I have attempted to identify the root problem as concisely as possible, and have used minimal reproducible examples where possible
