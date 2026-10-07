# [Windows] flutter_windows.dll heap corruption (0xC0000005) under heavy Rust→Dart FFI callbacks with Impeller enabled

- URL: https://github.com/flutter/flutter/issues/188635
- Repo: flutter/flutter (language: Dart)
- State: open; created 2026-06-26T15:53:07Z; status ok; passes main

## Issue body

reporter (NONE) · zundaren · 2026-06-26T15:53:07Z · https://github.com/flutter/flutter/issues/188635

### Steps to reproduce

## Steps to reproduce

1. Connect to SSH server via the app (flutter_rust_bridge FFI)
2. Run `tail -f /var/log/some-large-log` to produce continuous high-frequency output
3. While output is streaming, drag the terminal scrollbar repeatedly
4. App crashes within seconds to minutes

## Expected results
App remains stable. The crash does not occur on other machines
without virtual display adapters (e.g. colleagues' PCs).

## Actual results
App crashes with 0xC0000005 access violation inside flutter_windows.dll.
Fault address varies on every crash (different offsets each time),
which is a heap corruption signature, not a deterministic code bug.

Crash dump analysis (parsed via PowerShell minidump reader):
- ExceptionCode: 0xC0000005
- Fault offsets observed: flutter_windows.dll+0x2DFAB6, flutter_windows.dll+0x367274 (varies)
- Stack hit counts: flutter_windows.dll ×145, ntdll ×42, KERNELBASE ×9
- Loaded GPU driver: Intel igd10iumd64.dll (no NVIDIA, no virtual adapter)
- Active threads at crash: ~200

## Environment
- Flutter: 3.44.4
- OS: Windows 11
- GPU: NVIDIA RTX 4060 Laptop + Intel UHD (Optimus)
- Also present: ToDesk Virtual Display Adapter, GameViewer Virtual Display Adapter
- App type: SSH terminal using flutter_rust_bridge (heavy async FFI callbacks)

## Workarounds (all three needed together)

**1. Disable Impeller (most critical):**
```

::SetEnvironmentVariableW(L"FLUTTER_ENGINE_SWITCHES", L"1");
::SetEnvironmentVariableW(L"FLUTTER_ENGINE_SWITCH_1", L"enable-impeller=false");
project.set_gpu_preference(flutter::GpuPreference::LowPowerPreference);
project.set_ui_thread_policy(flutter::UIThreadPolicy::RunOnPlatformThread);

```
All three together completely eliminate the crash. Workaround #3 alone (RunOnPlatformThread) is insufficient when Impeller is enabled. Workaround #1 alone (disable Impeller) also appears insufficient without #3.

Crash does NOT occur on machines without virtual display adapters
Crash is NOT reproducible with the app idle; requires heavy FFI callback load
No Rust panic log, no Dart exception — crash originates in native engine layer
Upgraded Flutter 3.44.2 → 3.44.4: no improvement (same fault offset 0x2DFAB6 persists across engine versions)

### Expected results

<!-- Failed to upload "btshell.exe.33052.dmp" -->

### Actual results

No Crash 

### Code sample

xterm: ^4.0.0
flutter_rust_bridge: ^2.12.0

tail -f  testt.log
ctrl + c
Drag the scroll bar with the mouse

### Screenshots or Video




### Logs

_No response_

### Flutter Doctor output

Doctor summary (to see all details, run flutter doctor -v):
[!] Flutter (Channel [user-branch], 3.44.4, on Microsoft Windows [版本 10.0.26200.8655], locale zh-CN)
    ! Flutter version 3.44.4 on channel [user-branch] at D:\devenv\flutter
      Currently on an unknown channel. Run `flutter channel` to switch to an official channel.
      If that doesn't fix the issue, reinstall Flutter by following instructions at https://flutter.dev/setup.
    ! Upstream repository unknown source is not a standard remote.
      Set environment variable "FLUTTER_GIT_URL" to unknown source to dismiss this error.
[√] Windows Version (Windows 11 or higher, 25H2, 2009)
[X] Android toolchain - develop for Android devices
    X Unable to locate Android SDK.
      Install Android Studio from: https://developer.android.com/studio/index.html
      On first launch it will assist you in installing the Android SDK components.
      (or visit https://flutter.dev/to/windows-android-setup for detailed instructions).
      If the Android SDK has been installed to a custom location, please use
      `flutter config --android-sdk` to update to that location.

[√] Chrome - develop for the web
[√] Visual Studio - develop Windows apps (Visual Studio Community 2022 17.14.35 (June 2026))
[√] Connected device (3 available)



## Comment 4811341218

maintainer (MEMBER) · mbcorona · 2026-06-26T16:14:18Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4811341218

Thanks for the report, routing to the engine team for further investigation.

## Comment 4811343478

other (CONTRIBUTOR) · dcharkes · 2026-06-26T16:14:36Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4811343478

The error is an access violation, so we're trying to dereference an address that is corrupt or has been freed.

The first step is probably to see where in the Flutter engine it is crashing. With arbitrary memory corruption the offset in `flutter_windows.dll` would be changing every crash.

I have no hypothesis yet why the flutter engine would crash with heavy FFI use via Flutter Rust bridge. (If we know the location we could see if it's near an FFI call.) It's interesting that the FFI calls made via FRB are not crashing.

Just to rule out some other possibilities: Are you passing data coming from FRB to be rendered by Flutter? In case you accidentally give Flutter a buffer that you then concurrently free.

Your description smells a bit like a timing issue. E.g. virtual displays might be slower. Doing things on a different thread changes timing. Impeller vs Skia has different timing. So it could be you're passing a pointer to be drawn, and without heavy load the pointer is still valid.

Are there any native pointers in your code that have `NativeFinalizer`s attached? E.g. heavy load could cause the GC to run more eagerly. which would then run the native finalizers earlier. In Dart standalone you can use `--verbose_gc`. In Flutter debug you should be able to use `--dart-flags` with `--verbose_gc`. It would be interesting to know if the crash happens after a GC runs finalizers.

Okay, I'm just theory crafting here. I hope this helps.

> Connect to SSH server via the app (flutter_rust_bridge FFI)

I have no idea what this means. Do you have a minimal reproduction Flutter app somewhere + the flutter command that we need to run + the actions we need to take in the app?

cc @knopp For Windows engine knowledge.

## Comment 4813083067

maintainer (MEMBER) · loic-sharma · 2026-06-26T20:10:33Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4813083067

Yes, please load Flutter's symbols and provide the symbolicated crash call stack:

<details>
<summary>How to load Flutter's symbols in Visual Studio...</summary>

1. Find your **Flutter SDK path** using the terminal: `flutter doctor --verbose`.

   Let's say I have the following output:
   
   ```
   PS C:\> flutter doctor --verbose
   [✓] Flutter (Channel stable, 3.7.0, on Microsoft Windows [Version 10.0.22621.1105], locale en-US)
       • Flutter version 3.7.0 on channel stable at C:\Code\f\flutter
   ...
   ```

   My **Flutter SDK path** is `C:\Code\f\flutter`.

2. Add Flutter's symbols path to Visual Studio's options
    1. Open the Debugging options using `DEBUG` > `Options...`.
    2. Navigate to the `Symbols` pane and use the `+` button to add `<Flutter SDK path>/bin/cache/artifacts/engine/windows-x64`
   as a symbol location:

       ![Pasted image 20230126161935](https://user-images.githubusercontent.com/737941/214984655-353ba5d8-6ca5-4678-bc97-4932c4b3e63e.png)

    3. Close the `Options` window

3. Load Flutter's symbols in Visual Studio
    1. Open the `Modules` window using `DEBUG` > `Windows` > `Modules` (or `Ctrl+Alt+U`):

       ![Pasted image 20230126161915](https://user-images.githubusercontent.com/737941/214985815-ba128e85-b107-4fbf-ae58-7814b840bfaf.png)

    2. In the `Modules` window, right click the `flutter_windows.dll` item and select `Load Symbols`:

       ![Pasted image 20230126162141](https://user-images.githubusercontent.com/737941/214986218-4f53e12c-ccb6-4c8c-8419-ca8772a5e561.png)

    3. The engine's symbols should now be loaded:

       ![Pasted image 20230126162222](https://user-images.githubusercontent.com/737941/214986347-4bd31006-f960-4311-ad7e-9030b32067eb.png)

For more information, see the [How to debug the Flutter engine on Windows guide.](https://gist.github.com/loic-sharma/248f28b3ba4664dde08da68f46b312bd)

</details> 

## Comment 4817605779

reporter (NONE) · zundaren · 2026-06-27T12:53:14Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4817605779

> The error is an access violation, so we're trying to dereference an address that is corrupt or has been freed.
> 
> The first step is probably to see where in the Flutter engine it is crashing. With arbitrary memory corruption the offset in `flutter_windows.dll` would be changing every crash.
> 
> I have no hypothesis yet why the flutter engine would crash with heavy FFI use via Flutter Rust bridge. (If we know the location we could see if it's near an FFI call.) It's interesting that the FFI calls made via FRB are not crashing.
> 
> Just to rule out some other possibilities: Are you passing data coming from FRB to be rendered by Flutter? In case you accidentally give Flutter a buffer that you then concurrently free.
> 
> Your description smells a bit like a timing issue. E.g. virtual displays might be slower. Doing things on a different thread changes timing. Impeller vs Skia has different timing. So it could be you're passing a pointer to be drawn, and without heavy load the pointer is still valid.
> 
> Are there any native pointers in your code that have `NativeFinalizer`s attached? E.g. heavy load could cause the GC to run more eagerly. which would then run the native finalizers earlier. In Dart standalone you can use `--verbose_gc`. In Flutter debug you should be able to use `--dart-flags` with `--verbose_gc`. It would be interesting to know if the crash happens after a GC runs finalizers.
> 
> Okay, I'm just theory crafting here. I hope this helps.
> 
> > Connect to SSH server via the app (flutter_rust_bridge FFI)
> 
> I have no idea what this means. Do you have a minimal reproduction Flutter app somewhere + the flutter command that we need to run + the actions we need to take in the app?
> 
> cc [@knopp](https://github.com/knopp) For Windows engine knowledge.

I'm not very familiar with the lower-level C++ programming. It was all handled by AI for me. I have recorded a video of the code. Could you please help me figure out where the problem is?
```
https://github.com/zundaren/btshellbug
```

https://github.com/user-attachments/assets/09745f24-87ec-47aa-9029-7d98ea1c2ae9

## Comment 4830618069

maintainer (MEMBER) · mraleph · 2026-06-29T08:49:28Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4830618069

>  It was all handled by AI for me. I have recorded a video of the code. Could you please help me figure out where the problem is?

You will have to provide a minimal runnable reproduction. Ain't no one is is going to watch a video and figure out a bug in a pile of LLM generated code. 

## Comment 4830712884

reporter (NONE) · zundaren · 2026-06-29T09:02:05Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4830712884

> > It was all handled by AI for me. I have recorded a video of the code. Could you please help me figure out where the problem is?
> 
> You will have to provide a minimal runnable reproduction. Ain't no one is is going to watch a video and figure out a bug in a pile of LLM generated code.

This is code repository: https://github.com/zundaren/btshellbug
```
Using Rust FRB, Flutter passed a callback to Rust. When there is data on the SSH connection, Rust will call this callback. I asked the AI that it was a problem of thread contention.

Future<ExecResult> startPtyShell({
  required String clientId,
  required FutureOr<void> Function(String) dartCallback,
}) => RustLib.instance.api.crateApiTermSshStartPtyShell(
  clientId: clientId,
  dartCallback: dartCallback,
);
```

## Comment 4889340867

reporter (NONE) · zundaren · 2026-07-06T05:17:10Z · https://github.com/flutter/flutter/issues/188635#issuecomment-4889340867

This issue seems to be related to the Windows system and the CPU model. I changed the system to Win11, 24H2 26100.8737. The CPU remained the same: Intel(R) Core(TM) i9-14900HX (2.20 GHz). Then I installed some of the BIOS drivers from Rog, and the crashes seemed to have decreased, but they still occurred.
