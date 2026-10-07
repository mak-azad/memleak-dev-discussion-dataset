# [Bug]: chroma_stft (via estimate_tuning/piptrack) leaves unreturned memory in the glibc arena, growing RSS across repeated calls

- URL: https://github.com/librosa/librosa/issues/2076
- Repo: librosa/librosa (language: Python)
- State: open; created 2026-07-13T21:57:42Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · imrulhuda · 2026-07-13T21:57:42Z · https://github.com/librosa/librosa/issues/2076

### Bug summary

Repeated calls to `librosa.feature.chroma_stft()` cause process RSS (resident memory) to grow over time in a long-lived process, especially when input length varies call-to-call (as real audio files typically do). This is not a Python object leak or a growing cache — `chroma_stft` internally calls `estimate_tuning()` → `piptrack()`, which allocates ~6 full-spectrogram-sized temporary arrays (including a redundant `np.abs(S)` copy, since the input power spectrogram is already non-negative) to compute a single scalar tuning offset. These are freed correctly at the Python level every call, but glibc's malloc does not return the freed memory to the OS under this allocation pattern. A single `ctypes` call to `malloc_trim(0)` reliably reclaims the excess, confirming this is arena fragmentation rather than a reference leak.

### Code for reproduction

```python
import ctypes
import numpy as np
import librosa

libc = ctypes.CDLL("libc.so.6")

def vmrss_mb():
    with open("/proc/self/status") as f:
        for line in f:
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) / 1024

sr = 16000
rng = np.random.default_rng(0)
base_len = 3_964_032  # ~248s at 16kHz

# Fixed-length input: RSS should plateau quickly if this is just one-time setup cost.
y0 = rng.standard_normal(base_len).astype(np.float32)
librosa.feature.chroma_stft(y=y0, sr=sr, hop_length=256)  # warmup
print(f"[fixed length] warmup: {vmrss_mb():.1f} MB")
for i in range(1, 11):
    librosa.feature.chroma_stft(y=y0, sr=sr, hop_length=256)
    print(f"[fixed length] call {i}: {vmrss_mb():.1f} MB")

libc.malloc_trim(0)
print(f"[fixed length] after malloc_trim(0): {vmrss_mb():.1f} MB")

# Varying-length input, closer to real-world usage (real files are rarely identical length):
print()
for i in range(1, 21):
    length = base_len + rng.integers(-500_000, 500_000)
    y = rng.standard_normal(length).astype(np.float32)
    librosa.feature.chroma_stft(y=y, sr=sr, hop_length=256)
    print(f"[varying length] call {i} (len={length}): {vmrss_mb():.1f} MB")

libc.malloc_trim(0)
print(f"[varying length] after malloc_trim(0): {vmrss_mb():.1f} MB")
```

### Actual outcome

Real output from the exact script above, on our machine:

```
[fixed length] warmup: 323.8 MB
[fixed length] call 1: 323.9 MB
[fixed length] call 2: 323.9 MB
...
[fixed length] call 10: 323.7 MB
[fixed length] after malloc_trim(0): 268.1 MB

[varying length] call 1 (len=3747151): 329.1 MB
[varying length] call 2 (len=4134037): 342.3 MB
[varying length] call 3 (len=4226114): 359.9 MB
...
[varying length] call 16 (len=4129722): 360.1 MB
[varying length] call 20 (len=4082139): 342.3 MB
[varying length] after malloc_trim(0): 285.2 MB
```

Fixed-length calls plateau almost immediately (~323.7–323.9 MB), yet `malloc_trim(0)` still recovers 55.6 MB that accumulated invisibly during warmup. Varying-length calls push the ceiling meaningfully higher (up to ~360 MB) before `malloc_trim(0)` recovers most of it. In both cases, none of this memory is referenced by Python — it's sitting in glibc's arena.

### Expected outcome

RSS should stay close to a stable baseline across repeated calls, without requiring an explicit `malloc_trim(0)` to reclaim tens of megabytes — especially for a function whose actual return value here is a single scalar float per call. At minimum, we'd expect the growth to be negligible relative to the ~63MB scratch arrays being churned, not a meaningful fraction of it.

### Additional information

Traced via bisection: isolated `chroma_stft`'s four internal steps (STFT, `estimate_tuning`, `filters.chroma` filterbank lookup, final `einsum` contraction) — only `estimate_tuning` (via `piptrack`) shows this behavior; the others are flat. `piptrack`'s implementation (`librosa/core/pitch.py`) computes `S = np.abs(S)` (redundant when `S` is already a non-negative power spectrogram), then allocates `pitches = np.zeros_like(S)`, `mags = np.zeros_like(S)`, `avg = np.gradient(S, axis=-2)`, `shift = _parabolic_interpolation(S, axis=-2)`, and `dskew = 0.5 * avg * shift` — 6 full-size temporary arrays just to return a scalar tuning estimate via `estimate_tuning`.

A possible fix: skip the redundant `np.abs(S)` copy when the caller can guarantee non-negative input (e.g. a `power=2` spectrogram), and/or give `estimate_tuning`/`chroma_stft` a lighter-weight path that doesn't require full pitch/magnitude maps when only a scalar tuning value is needed. Happy to help prototype either approach if a maintainer can weigh in on which direction is preferred — didn't want to open a PR for a behavior/design change like this without checking first.

This may be related to #1286, which reported a similar RSS-growth pattern in `librosa.load()` — that thread concluded librosa's own code holds no cross-call state, consistent with what we found here: it's not a logic bug, it's an allocator-interaction side effect of allocating more scratch memory than the task strictly needs.

### Operating system

Linux (Ubuntu-based, WSL2) — `Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39`

### software versions

```
python: 3.12.13 | packaged by conda-forge | (main, Mar  5 2026, 16:50:00) [GCC 14.3.0]
librosa: 0.11.0
numpy: 2.2.6
scipy: 1.18.0
numba: 0.66.0
soundfile: 0.14.0
joblib: 1.5.3
```

### Installation

conda

## Comment 4964858649

maintainer (MEMBER) · bmcfee · 2026-07-14T02:34:53Z · https://github.com/librosa/librosa/issues/2076#issuecomment-4964858649

Thanks for the deep dive on this.  If I can simplify / summarize a bit here:

1. The problem isn't anything to do with `chroma_stft`, it's just `estimate_tuning`.
2. `estimate_tuning` is not directly to blame, as it's really just a wrapper around piptrack and pitch_tuning.  (This being an expedient way to implement a simple tuning estimator.)
3. The entire problem with piptrack boils down to intermediate array allocations.

In short, this is the kind of thing that is likely to happen when you port matlab code to python. 😬

Anyway, to your proposed solutions:



> skip the redundant `np.abs(S)` copy when the caller can guarantee non-negative input (e.g. a `power=2` spectrogram),

Sure.  In general we don't really trust the user that much on these things, and it's better to just guard it with an `if S.min() <= 0: ...` but yeah this would save one allocation.



> or give `estimate_tuning`/`chroma_stft` a lighter-weight path that doesn't require full pitch/magnitude maps when only a scalar tuning value is needed.

I'm definitely open to suggestions on how to improve this algorithm, as I've always been rather suspicious of it.  If for no reason other than it's going to leak information from high-energy partials that may tell you nothing about the actual intonation of f0s.  

That said, I don't see a direct way to do this without doing something of comparable complexity here.  Really what it should be doing is some kind of mulitple f0 estimation and then run pitch_tuning on *those* outputs.  But I really don't want to put a multi-f0 estimator in the critical path here either, since that's a real chicken-and-egg problem if our entire goal is to produce chroma features (ie, octave-reduced multi-f0s).

A third option, which you didn't mention, is just to streamline the piptrack implementation.  It could be done much more efficiently with a vectorized numba stencil.  In fact, we have almost all of this already written in the `_parabolic_interpolation` helper used by yin/pyin elsewhere in the same module.

The downside to this approach is that it will not port over to array-api very nicely, so we'd probably end up just re-implementing the existing version in a separate code path when we get to #1743 .
