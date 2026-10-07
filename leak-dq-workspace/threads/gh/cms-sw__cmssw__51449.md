# (Tiny) Memory Leak observed in a particle gun sample

- URL: https://github.com/cms-sw/cmssw/issues/51449
- Repo: cms-sw/cmssw (language: C++)
- State: open; created 2026-07-08T12:58:11Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · DickyChant · 2026-07-08T12:58:11Z · https://github.com/cms-sw/cmssw/issues/51449

Dear experts, 

During a recent production of a particle gun workflow, we experienced a glitch related to memory setup:

- The memory was measured from run tests with hundreds of events, and measured a memory requirement of <~ 4GB at 8 cores
- The task chain was then formed, with 6GB memory consumption, spawning 8 cores, accounting for a certain margin. 
- But the task chain failed in production, with memory consumption exceeding 6GB.

While it is true that we might not want to run workflows with 6GB memory while 8 threads by construction (the improvement is now under discussion), we got interested in why such an issue happens, and here is a summary of what I found:

Basically, this particular workflow shows continuous RSS growth over events that a short 100-event validation completely hides. 
- **At the default validation size (100 events, 1 thread), peak RSS is a flat 1.5 GB;** 
- ** Scaled to a realistic 8 threads / 10,000 events, it climbs to 5.48 GB and is still rising at job end.**

After a full investigation, the growth is not a leak: it is high-water-mark retention of transient Geant4 (g4SimHits) memory, set by the largest EM shower seen so far (and, in this case, driven by the rare high-pT tail of the EE_FlatPT-1to500 (1–500 GeV) flat-pT particle gun). glibc keeps the freed peak pages instead of returning them to the OS, so RSS ratchets upward and slowly decelerates.

The cmsDriver sequence is:

```
cmsDriver.py Configuration/GenProduction/python/HIN-HINPbPbWinter25GSHIMix-00003-fragment.py --pileup HiMixGEN --scenario HeavyIons --era Run3_pp_on_PbPb_2025 --customise Configuration/DataProcessing/Utils.addMonitoring --beamspot MatchHI --step GEN,SIM --geometry DB:Extended --conditions 151X_mcRun3_2025_realistic_HI_v5 --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(100)" --datatier GEN-SIM --eventcontent RAWSIM --python_filename HIN-HINPbPbWinter25GSHIMix-00003_1_cfg.py --fileout file:HIN-HINPbPbWinter25GSHIMix-00003.root --number 100 --number_out 100 --pileup_input "dbs:/Hydjet_Quenched_MinBias_TuneCELLO_5p36TeV_pythia8/HINPbPbWinter25GS-151X_mcRun3_2025_realistic_HI_v4-v2/GEN-SIM" --no_exec --mc || exit $? ;
```
With the fragment shown below:

```
import FWCore.ParameterSet.Config as cms

generator = cms.EDFilter("Pythia8PtGun",
    PGunParameters = cms.PSet(
        MaxPt = cms.double(500.0),
        MinPt = cms.double(1.0),
        ParticleID = cms.vint32(11),
        AddAntiParticle = cms.bool(True),
        MaxEta = cms.double(3.1),
        MaxPhi = cms.double(3.14159265359),
        MinEta = cms.double(-3.1),
        MinPhi = cms.double(-3.14159265359) ## in radians
    ),
    Verbosity = cms.untracked.int32(0), ## set to 1 (or greater)  for printouts
    psethack = cms.string('double electron pt 1.0 to 500'),
    firstRun = cms.untracked.uint32(1),
    PythiaParameters = cms.PSet(parameterSets = cms.vstring())
)
```
Further details:
--------------------
### 1. Peak memory scales with threads and keeps growing with events

| config | events | threads | peak RSS | peak VSIZE | avg RSS | time/event |
|--|--:|--:|--:|--:|--:|--:|
| default validation | 100 | 1 | **1,498 MB** | 2,361 MB | — | 9.27 s |
| realistic | 10,000 | 8 | **5,484 MB** | 9,010 MB | 3,719 MB | 1.61 s |

The 100-event single-thread job looks perfectly flat — the growth is only visible at scale.

### 2. RSS grows continuously; it does not saturate by 10k events

Per-1,000-event window **max RSS** (8 threads, with pileup):

| events | 1–1k | 2–3k | 3–4k | 4–5k | 5–6k | 6–7k | 7–8k | 8–9k | 9–10k |
|--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| max RSS (MB) | 3,249 | 3,412 | 3,736 | 4,075 | 4,308 | 4,506 | 4,969 | 5,233 | 5,484 |

Growth decelerates (~0.33 → ~0.25 MB/event) but never flattens.

### 3. The growth is `g4SimHits` (Geant4), not GenJets or pileup

End-of-job `SimpleMemoryCheck` `ModuleMemoryReport` (average VSIZE increase per module execution):

| module | avg increase (MB/exec) | max (MB) |
|--|--:|--:|
| **`g4SimHits`** | **3.90** | 487 |
| `genParticles` | 0.62 | 324 (early) |
| `ak2HiGenJets` | 0.12 | 80 |
| `ak6HiGenJets` | 0.053 | 64 |
| `RAWSIMoutput` | 0.068 | 56 |
| `mix` (pileup) | 0.047 | 56 |
| `ak1/ak5/ak7HiGenJets` | 0.01–0.035 | 12–32 |

`g4SimHits` dominates by ~30×. GenJets and pileup mixing are negligible.

### 4. It is anonymous heap, not mmapped pileup files

Live `/proc/<pid>/smaps_rollup` on the worker at ~3.7 GB RSS:

- Anonymous / `Private_Dirty`: **3.55 GB (~98% of RSS)**
- `Pss_File` (all mmapped libs + ROOT files combined): **58 MB**
- Open pileup `.root` fds: **9, stable** (opened only at init; none accumulate)

So to me it is not "keep opening/holding pileup files"

### 5. It is not glibc arena fragmentation

A control run with `MALLOC_ARENA_MAX=2` reached the **same ~3.7 GB peak at 4,000 events** as the
default-allocator baseline (3,770 vs 3,736 MB, within ~1%). Capping arenas changed nothing.

### 6. It is pileup-independent (only the baseline depends on pileup)

Creep magnitude over the first 4,000 events, with and without pileup:

| run | config | baseline RSS (~1k ev) | peak RSS @4k | creep |
|--|--|--:|--:|--:|
| with PU | 8t | 3,249 | 3,736 | **+487** |
| with PU, arenas=2 | 8t | 3,182 | 3,770 | **+588** |
| **no PU** | 8t | 1,951 | 2,509 | **+558** |

The slope is the same (~+500–590 MB / 4k events) with or without pileup. 

### 7. Memory jumps correlate with rare high-energy events (the smoking gun)

A single-thread run correlating per-event processing time (a proxy for shower energy) with VSIZE
steps:

- Per-event cost spans **0.13 s → 93 s** (median 6.7 s) — the 1–500 GeV flat-pT spectrum.
- VSIZE steps up on only **~2–3 % of events**, and those events are **~4× slower than median**
  (median 25 s vs 6.7 s) which, to me, is the high-energy showers.

--------------------
I got some hint that we can trim `malloc` harder, but i guess this is not the best "fix" if we ever want one? 


## Comment 4915019989

other (CONTRIBUTOR) · cmsbuild · 2026-07-08T12:58:34Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915019989

cms-bot internal usage<!-- bot cache: {"commits":{},"emoji":{"4915188580":"+1","4915243739":"+1"},"signatures":{}} -->

## Comment 4915020076

other (CONTRIBUTOR) · cmsbuild · 2026-07-08T12:58:34Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915020076

A new Issue was created by  @DickyChant.

@Dr15Jones, @ftenchini, @makortel, @mandrenguyen, @sextonkennedy, @smuzaffar can you please review it and eventually sign/assign? Thanks.

cms-bot commands are listed <a href="http://cms-sw.github.io/cms-bot-cmssw-issues.html">here</a>


## Comment 4915188580

other (CONTRIBUTOR) · Dr15Jones · 2026-07-08T13:17:38Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915188580

assign generators

## Comment 4915191391

other (CONTRIBUTOR) · cmsbuild · 2026-07-08T13:17:56Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915191391

New categories assigned: generators

@lviliani,@mkirsano,@sensrcn,@theofil you have been requested to review this Pull request/Issue and eventually sign? Thanks

## Comment 4915237172

other (CONTRIBUTOR) · Dr15Jones · 2026-07-08T13:23:11Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915237172

Note, cmsRun does not use glibc allocator, it uses jemalloc. You can force the use of glibc by running cmsRunGlibC instead.

## Comment 4915243739

other (CONTRIBUTOR) · Dr15Jones · 2026-07-08T13:23:57Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915243739

assign simulation

## Comment 4915247358

other (CONTRIBUTOR) · cmsbuild · 2026-07-08T13:24:21Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915247358

New categories assigned: simulation

@civanch,@kpedro88,@mdhildreth you have been requested to review this Pull request/Issue and eventually sign? Thanks

## Comment 4915260465

other (CONTRIBUTOR) · Dr15Jones · 2026-07-08T13:25:44Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4915260465

Using ModuleAllocMonitor (or EventModuleAllocMonitor) can directly pin which module is hoarding/leaking memory. See

https://github.com/cms-sw/cmssw/tree/master/PerfTools/AllocMonitor#moduleallocmonitor

## Comment 4969981083

other (CONTRIBUTOR) · makortel · 2026-07-14T13:56:28Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4969981083

> End-of-job `SimpleMemoryCheck` `ModuleMemoryReport` (average VSIZE increase per module execution):

Are these reports from a multithreaded job? If they are, I'm afraid the per-module information from `SimpleMemoryCheck` is unreliable, because the service monitors the global state of the application and the memory increase reported for a "spectator" module can easily be caused by other modules being run in parallel.

## Comment 4969992302

other (CONTRIBUTOR) · makortel · 2026-07-14T13:57:25Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-4969992302

What CMSSW version was used?

## Comment 5032588924

other (CONTRIBUTOR) · civanch · 2026-07-21T09:56:24Z · https://github.com/cms-sw/cmssw/issues/51449#issuecomment-5032588924

Currently in Geant4 developments a tiny problem is identified and fixed. This may increase run time memory, the memory is cleaned end of run. I am not sure if this issue may explain observed problem in this issue, but may backport the fix to CMSSW if it is Ok.
