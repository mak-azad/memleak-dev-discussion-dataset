# [Bug]: Shared emptyString object prevents transferring juce::String across binary boundaries

- URL: https://github.com/juce-framework/JUCE/issues/1565
- Repo: juce-framework/JUCE (language: C++)
- State: open; created 2025-08-20T00:22:53Z; status ok; passes main

## Issue body

reporter (NONE) · kevin-- · 2025-08-20T00:22:53Z · https://github.com/juce-framework/JUCE/issues/1565

### Detailed steps on how to reproduce the bug

This is a bit of an esoteric use case admittedly, but this one is a particular head scratcher.

We have a Host and a Plugin built against the same JUCE version. The Host loads the Plugin via VST3, then we use the custom interface API to establish a "rich API" between the host and plugin.

At this point, there are a couple deep seated API's that return `const juce::String&`. In a handful of cases these are occasionally empty.

What then happens is that when `String::~String` is invoked, the empty string in question fails the `isEmptyString` check because the "empty string" it is pointing to is DIFFERENT than the empty string known to exist by the current binary
```
    static bool isEmptyString (StringHolder* other)
    {
        return other == &emptyString;
    }
```
The code then tries to deallocate the OTHER binary's `emptyString` resulting in a segfault because we are deleting something of the data page that was not malloc'ed.

```
==56507==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x000108496a60 in thread T0
    #0 0x1249d83d0 in _ZdaPv+0x74 (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x643d0)
    #1 0x41c8a27cc in juce::StringHolderUtils::release(juce::StringHolder*)+0x60 (REDACTED.vst3/Contents/MacOS/REDACTED:arm64+0x6367cc)
    #2 0x41c78aa88 in juce::StringHolderUtils::release(juce::CharPointer_UTF8)+0x1b4 (REDACTED.vst3/Contents/MacOS/REDACTED:arm64+0x51ea88)
    #3 0x41c78a83c in juce::String::~String()+0x160 (REDACTED.vst3/Contents/MacOS/REDACTED:arm64+0x51e83c)
    #4 0x41c6f3934 in juce::String::~String()+0x18 (REDACTED.vst3/Contents/MacOS/REDACTED:arm64+0x487934)
```

```
0x000108496a60 is located 0 bytes inside of global variable 'juce::emptyString' defined in 'juce_core/juce_core.mm' (0x108496a60) of size 24
SUMMARY: AddressSanitizer: bad-free (REDACTED.app/Contents/Frameworks/libclang_rt.asan_osx_dynamic.dylib:arm64e+0x643d0) in _ZdaPv+0x74
==56507==ABORTING
```

We previously did not experience this, as we were on JUCE 6.1.4. Now we have upgraded to 8.0.6


I tried to force the string to be replaced by the "correct" `emptyString` but to no avail - it just causes the crash to happen sooner.
```
static juce::String kEmptyString;
juce::String forceRecreateString(const juce::String& r)
{
    if(r.length() == 0) {
        return kEmptyString;
    }
    return std::string(r.toUTF8()).c_str();
}
```

Thoughts?

### What is the expected behaviour?

Ideally we could have an option to link dynamiclly against the JUCE library instead of having to hide symbols between every target.

Barring that, a way to transfer data across binary boundaries would be great.

Really just looking for ideas here. I suppose I can always add a new plain "extern C" API to prevent this

### Operating systems

macOS, Windows

### What versions of the operating systems?

macOS 11.6+, Windows 10+

### Architectures

Arm64/aarch64, x86_64

### Stacktrace

```shell

```

### Plug-in formats (if applicable)

VST3

### Plug-in host applications (DAWs) (if applicable)

Our own JUCE Host

### Testing on the `develop` branch

The bug is present on the `develop` branch

### Code of Conduct

- [x] I agree to follow the Code of Conduct
