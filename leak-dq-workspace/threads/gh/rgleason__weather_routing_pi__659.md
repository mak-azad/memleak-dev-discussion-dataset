# xWeather Windows Trial

- URL: https://github.com/rgleason/weather_routing_pi/issues/659
- Repo: rgleason/weather_routing_pi (language: C++)
- State: closed; created 2026-09-11T01:47:47Z; status ok; passes main

## Issue body

reporter (OWNER) · rgleason · 2026-09-11T01:47:47Z · https://github.com/rgleason/weather_routing_pi/issues/659

The plugin does build and complete.
When run in VS 2022 in normal relwithdebinfo mode with Opencpn 5.15 
it runs and is somewhat functional but is very slow and  does not render  satisfactorily and the routing is disrupted.

<img width="1200" height="745" alt="Image" src="https://github.com/user-attachments/assets/96144f4b-4204-4035-ae16-e3ef7cf45eeb" />

<html><body>
<!--StartFragment--><p>=================</p>
<p>Then using <b>Opencpn 5.14 RELEASE,  VS </b>in admin mode, and attaching opencpn.exe release version, with the opencpn.pdb (65 mb) also freshly downloaded and installed from the website. The since pob220 build plugin refuses to load when dll and pdb are copied into the %localappdata%/opencpn/plugins  directory, I then open  Opencpn 5.14 Release "opencpn.exe" by hitting VS DEBUG F5 and opencpn eventually loads.  Then I navigation to Settings &gt; Plugins and pick Load Tarball and pick the Xweather tarball.<br>
The plugin fails immediately and  that is what is described below, and what is referenced all the way down to the bottom here.</p>
<p>=================<br>
  <br>
-----------------------<br>
</p>
<h3>Opencpn 14.0   "C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\opencpn.exe"<br>
Weather_routing  from Pob220   </h3>
<p>==============<br>
Weather_routing_pi.cpp  Line 104<br>
extern "C" DECL_EXP void destroy_pi(opencpn_plugin* p) { delete p; }<br>
Exception thrown at 0x6D0DCC2A (msvcp140.dll) in opencpn.exe: 0xC0000005: Access violation reading location 0x00000000.<br>
  <br>
-----------------------------------------<br>
msvcp140.dll!6d0dcc2a()<br>
[Frames below may be incorrect and/or missing, no symbols loaded for msvcp140.dll]<br>
weather_routingpi.dll!destroy_pi(opencpn_plugin * p=0x2818e260) Line 104<br>
    at C:\Users\fcgle\source\wr-pob-xweather\src\weather_routing_pi.cpp(104)<br>
opencpn.exe!PluginLoader::LoadPluginCandidate(const wxString &amp; file_name={...}, bool load_enabled=false) Line 679<br>
    at N:\model\src\plugin_loader.cpp(679)<br>
opencpn.exe!PluginLoader::LoadPlugInDirectory(const wxString &amp; plugin_dir={...}, bool load_enabled=false) Line 774<br>
    at N:\model\src\plugin_loader.cpp(774)<br>
opencpn.exe!PluginLoader::LoadAllPlugIns(bool load_enabled=false, bool keep_orphans=true) Line 486<br>
    at N:\model\src\plugin_loader.cpp(486)<br>
opencpn.exe!LoadAllPlugIns(bool load_enabled=false, bool keep_orphans=true) Line 490<br>
    at N:\gui\src\pluginmanager.cpp(490)<br>
opencpn.exe!CatalogMgrPanel::OnTarballButton(wxCommandEvent &amp; event={...}) Line 2431<br>
    at N:\gui\src\pluginmanager.cpp(2431)<br>
wxbase32u_vc14x.dll!6e3868d0()<br>
wxbase32u_vc14x.dll!6e384ee7()<br>
wxbase32u_vc14x.dll!6e485da1()<br>
wxbase32u_vc14x.dll!6e486654()<br>
wxbase32u_vc14x.dll!6e486970()<br>
wxbase32u_vc14x.dll!6e485d1a()<br>
wxbase32u_vc14x.dll!6e48657a()<br>
wxmsw32u_core_vc14x.dll!6d8fddc9()<br>
wxbase32u_vc14x.dll!6e486946()<br>
user32.dll!76239283()<br>
wxmsw32u_core_vc14x.dll!6d9050c1()<br>
user32.dll!76239283()<br>
user32.dll!7622846d()<br>
wxmsw32u_core_vc14x.dll!6d909779()<br>
ntdll.dll!773a9c66()<br>
ig9icd32.dll!6c0e34eb()<br>
user32.dll!762331f9()<br>
ntdll.dll!773abe86()<br>
win32u.dll!771f11ec()<br>
user32.dll!762297b2()<br>
user32.dll!76240938()<br>
user32.dll!76227c36()<br>
comctl32.dll!70b54e57()<br>
comctl32.dll!70b54e13()<br>
comctl32.dll!70b6a58c()<br>
user32.dll!76239283()<br>
user32.dll!7622846d()<br>
user32.dll!76227bda()<br>
wxmsw32u_core_vc14x.dll!6d901aec()<br>
wxmsw32u_core_vc14x.dll!6d9050db()<br>
wxmsw32u_core_vc14x.dll!6d941fd4()<br>
wxmsw32u_core_vc14x.dll!6d944741()<br>
user32.dll!76239283()<br>
user32.dll!7622846d()<br>
user32.dll!76233c29()<br>
wxmsw32u_core_vc14x.dll!6d9046ee()<br>
wxmsw32u_core_vc14x.dll!6d928aaf()<br>
wxbase32u_vc14x.dll!6e3ad189()<br>
wxbase32u_vc14x.dll!6e3ad24f()<br>
wxbase32u_vc14x.dll!6e3872ff()<br>
wxbase32u_vc14x.dll!6e3e10d7()<br>
wxbase32u_vc14x.dll!6e48b2b3()<br>
wxmsw32u_core_vc14x.dll!6d889280()<br>
opencpn.exe!WinMain(HINSTANCE__ * hInstance=0x003a0043, HINSTANCE__ * hPrevInstance=0x0050005c, char * lpCmdLine=0x006f0072, int nCmdShow=0x00720067) Line 439<br>
    at N:\gui\src\ocpn_app.cpp(439)<br>
-------------------------------------------------</p>

  | Name | Value | Type
-- | -- | -- | --
◢ | p | 0x2818e260 {m_panelBitmap={...} m_boat_lat=0.0000000000000000 m_boat_lon=-5.450649249848e-312#DEN ...} | opencpn_plugin * {weather_routing_pi}
  | ◢ [weather_routing_pi] | {m_panelBitmap={...} m_boat_lat=0.0000000000000000 m_boat_lon=-5.450649249848e-312#DEN ...} | weather_routing_pi
  | ▶ wxEvtHandler | {m_nextHandler=0x00000000 <NULL> m_previousHandler=0x00000000 <NULL> m_dynamicEvents=0x00000000 <NULL> ...} | wxEvtHandler
  | ▶ wxEventFilter | {m_next=0x00000000 <NULL> } | wxEventFilter
  | ▶ opencpn_plugin_121 | {...} | opencpn_plugin_121
  | ▶ m_panelBitmap | {...} | wxBitmap
  | m_boat_lat | 0.0000000000000000 | double
  | m_boat_lon | -5.450649249848e-312#DEN | double
  | m_cursor_lat | 2.0575948291209624e-81 | double
  | m_cursor_lon | 7.4713990213907021e-90 | double
  | b_in_boundary_reply | false | bool
  | m_use_persistent_chart_safe_cache | true | bool
  | m_chart_safety_ram_cache_mib | 0x00000000 | int
  | m_chart_safety_atlas_enabled | false | bool
  | m_chart_safety_atlas_max_disk_mib | 0x00000800 | int
  | m_chart_safety_atlas_all_charts | true | bool
  | ▶ m_chart_safety_atlas_selected_paths | { size=0x00000000 } | std::set<std::string,std::less<std::string>,std::allocator<std::string>>
  | ▶ m_chart_safety_atlas_completed_identity | "" | std::string
  | ▶ m_chart_safety_atlas_plan_identity | "" | std::string
  | ▶ m_chart_safety_atlas_coverage_tiles | { size=0x00000000 } | std::vector<std::pair<long,long>,std::allocator<std::pair<long,long>>>
  | ▶ m_chart_safety_atlas_tiles | { size=0x00000000 } | std::vector<std::pair<long,long>,std::allocator<std::pair<long,long>>>
  | m_chart_safety_atlas_cursor | 0x00000000 | unsigned int
  | m_chart_safety_atlas_metadata_attempts | 0x00000000 | int
  | m_chart_safety_atlas_batch_retries | 0x00000000 | int
  | m_chart_safety_atlas_failed_batches | 0x00000000 | unsigned int
  | m_chart_safety_atlas_logged_route_pause | false | bool
  | m_chart_safety_atlas_logged_user_pause | false | bool
  | m_chart_safety_atlas_plan_ready | false | bool
  | m_chart_safety_atlas_filter_installed | false | bool
  | m_chart_safety_atlas_batch_limit | 0x00000001 | unsigned int
  | m_chart_safety_atlas_selected_charts | 0x00000000 | unsigned int
  | m_chart_safety_atlas_estimate_mib | 0.0000000000000000 | double
  | ▶ m_chart_safety_atlas_last_input_ms | 0x000000000109c690 | std::atomic<__int64>
  | ▶ m_chart_safety_atlas_inspection | empty | std::future<weather_routing::ChartSafetyAtlasCacheStatus>
  | ▶ m_chart_safety_cache | {mutex_=unlocked path_="" identity_="" ...} | weather_routing::ChartSafetyCache
  | ▶ m_external_planning_provider | empty | std::unique_ptr<ExternalPlanningProvider,std::default_delete<ExternalPlanningProvider>>
  | ▶ m_pconfig | 0x2f2f3a73 {m_linesHead=??? m_linesTail=??? m_fnLocalFile={m_volume={m_impl={...} m_convertedToChar=...} ...} ...} | wxFileConfig *
  | ▶ m_parent_window | wxmsw32u_aui_vc14x.dll!0x6e65706f (load symbols for additional information) {m_hWnd=0xdc34d834 {unused=...} ...} | wxWindow *
  | ▶ m_pWeather_Routing | 0x00000000 <NULL> | WeatherRouting *
  | ▶ m_GribTime | {m_time={m_ll=0x8000000000000000 } } | wxDateTime
  | m_display_width | 0x68746967 | int
  | m_display_height | 0x692e6275 | int
  | m_leftclick_tool_id | 0x616d2f6f | int
  | m_position_menu_id | 0x702f6e69 | int
  | m_waypoint_menu_id | 0x6c697079 | int
  | m_route_menu_id | 0x692f746f | int
  | m_route_multileg_menu_id | 0x7865646e | int
  | ▶ m_tCursorLatLon | {m_impl=0x1b039bb0 {...} } | wxTimer
  | ▶ m_chart_safety_atlas_timer | {m_impl=0x1b039980 {...} } | wxTimer
  | ▶ m_addressSpaceMonitor | {alertDismissed=false thresholdPercent=80.000000000000000 m_isValid=false ...} | AddressSpaceMonitor
  | ▶ m_addressSpaceTimer | {m_impl=0x1b039a20 {...} } | wxTimer
  | ◢ __vfptr | 0x64f3237c {weather_routing_pi.dll!void(* weather_routing_pi::`vftable'[55])()} {0x64a041d8 {weather_routing_pi.dll![thunk]:weather_routing_pi::`vector deleting destructor'`adjustor{72}' (unsigned int)}, ...} | void * *
  | [0x00000000] | 0x64a041d8 {weather_routing_pi.dll![thunk]:weather_routing_pi::`vector deleting destructor'`adjustor{72}' (unsigned int)} | void *
  | [0x00000001] | 0x64a0df44 {weather_routing_pi.dll!weather_routing_pi::Init(void)} | void *
  | [0x00000002] | 0x64a01ab9 {weather_routing_pi.dll!weather_routing_pi::DeInit(void)} | void *
  | [0x00000003] | 0x64a09322 {weather_routing_pi.dll!weather_routing_pi::GetAPIVersionMajor(void)} | void *
  | [0x00000004] | 0x64a08fbc {weather_routing_pi.dll!weather_routing_pi::GetAPIVersionMinor(void)} | void *
  | [0x00000005] | 0x64a06a7d {weather_routing_pi.dll!weather_routing_pi::GetPlugInVersionMajor(void)} | void *
  | [0x00000006] | 0x64a011d1 {weather_routing_pi.dll!weather_routing_pi::GetPlugInVersionMinor(void)} | void *
  | [0x00000007] | 0x64a17530 {weather_routing_pi.dll!weather_routing_pi::GetPlugInBitmap(void)} | void *
  | [0x00000008] | 0x64a0f245 {weather_routing_pi.dll!weather_routing_pi::GetCommonName(void)} | void *
  | [0x00000009] | 0x64a0b3f7 {weather_routing_pi.dll!weather_routing_pi::GetShortDescription(void)} | void *
  | [0x0000000a] | 0x64a1195f {weather_routing_pi.dll!weather_routing_pi::GetLongDescription(void)} | void *
  | [0x0000000b] | 0x64a0f885 {weather_routing_pi.dll!weather_routing_pi::SetDefaults(void)} | void *
  | [0x0000000c] | 0x64a15712 {weather_routing_pi.dll!weather_routing_pi::GetToolbarToolCount(void)} | void *
  | [0x0000000d] | 0x64e35ec3 {weather_routing_pi.dll!opencpn_plugin::GetToolboxPanelCount(void)} | void *
  | [0x0000000e] | 0x64e35ec9 {weather_routing_pi.dll!opencpn_plugin::SetupToolboxPanel(int,class wxNotebook *)} | void *
  | [0x0000000f] | 0x64e35ecf {weather_routing_pi.dll!opencpn_plugin::OnCloseToolboxPanel(int,int)} | void *
  | [0x00000010] | 0x64a01d9d {weather_routing_pi.dll!weather_routing_pi::ShowPreferencesDialog(class wxWindow *)} | void *
  | [0x00000011] | 0x64e35edb {weather_routing_pi.dll!opencpn_plugin::RenderOverlay(class wxMemoryDC *,class PlugIn_ViewPort *)} | void *
  | [0x00000012] | 0x64a11036 {weather_routing_pi.dll!weather_routing_pi::SetCursorLatLon(double,double)} | void *
  | [0x00000013] | 0x64e35ee7 {weather_routing_pi.dll!opencpn_plugin::SetCurrentViewPort(class PlugIn_ViewPort &)} | void *
  | [0x00000014] | 0x64e35eed {weather_routing_pi.dll!opencpn_plugin::SetPositionFix(class PlugIn_Position_Fix &)} | void *
  | [0x00000015] | 0x64e35ef3 {weather_routing_pi.dll!opencpn_plugin::SetNMEASentence(class wxString &)} | void *
  | [0x00000016] | 0x64e35ef9 {weather_routing_pi.dll!opencpn_plugin::SetAISSentence(class wxString &)} | void *
  | [0x00000017] | 0x64e35eff {weather_routing_pi.dll!opencpn_plugin::ProcessParentResize(int,int)} | void *
  | [0x00000018] | 0x64a021d0 {weather_routing_pi.dll!weather_routing_pi::SetColorScheme(enum PI_ColorScheme)} | void *
  | [0x00000019] | 0x64a140f6 {weather_routing_pi.dll!weather_routing_pi::OnToolbarToolCallback(int)} | void *
  | [0x0000001a] | 0x64a01a00 {weather_routing_pi.dll!weather_routing_pi::OnContextMenuItemCallback(int)} | void *
  | [0x0000001b] | 0x64e35f17 {weather_routing_pi.dll!opencpn_plugin::UpdateAuiStatus(void)} | void *
  | [0x0000001c] | 0x64e35f1d {weather_routing_pi.dll!opencpn_plugin::GetDynamicChartClassNameArray(void)} | void *



<p><br>
======================</p>
<p><br>
  <b>Concise diagnosis<br>
  </b>- Crash is heap corruption (access violation in msvcp140) triggered while executing `delete p` in `destroy_pi`.<br>
- Root cause very likely double-free of a shared/global resource: `_img_WeatherRouting` is deleted in each plugin instance destructor while it is a shared/global image created by `initialize_images()`. The second (or later) destructor frees already-freed memory, corrupting heap and causing the CRT to crash.<br>
  <br>
  <b>Why this happens (≤200 words)</b><br>
The plugin constructor calls `initialize_images()` which allocates a module-global image. The destructor unconditionally `delete _img_WeatherRouting`. When OpenCPN probes plugin candidates it may create/destroy plugin instances multiple times. The first destructor frees the global image; subsequent destructors delete the same pointer again (or free memory allocated by a different CRT), producing heap corruption and an access violation inside the runtime. Mismatched runtime heaps (different CRTs between host/plugin) can amplify the problem, but the visible pattern and your code point to incorrect ownership of a global resource (double-delete).<br>
  <br>
  <b>Recommended fixes (concrete, minimal and robust)</b><br>
  <br>
1) Minimal quick guard (temporary):<br>
- In the plugin destructor, guard-delete and null the global pointer to prevent repeated deletes.<br>
  <br>
</p>
<blockquote>
  <p><font size="2">```<br>
// weather_routing_pi.cpp (in ~weather_routing_pi())<br>
if (_img_WeatherRouting) {<br>
    delete _img_WeatherRouting;<br>
    _img_WeatherRouting = nullptr;<br>
}<br>
```</font><br>
  </p>
</blockquote>
<br>
2) Preferred robust fix — centralize ownership with smart pointer:<br>
- Change `_img_WeatherRouting` to a module-level `std::unique_ptr&lt;wxBitmap&gt;` and manage it in `initialize_images()`/`cleanup_images()`.<br>
<br>
<b>icons.h:</b><br>
<blockquote>
  <p>```<br>
// icons.h<br>
#pragma once<br>
#include &lt;memory&gt;<br>
#include &lt;wx/bitmap.h&gt;<br>
    <br>
extern std::unique_ptr&lt;wxBitmap&gt; _img_WeatherRouting;<br>
void initialize_images();<br>
void cleanup_images();<br>
```<br>
  </p>
</blockquote>
<b>icons.cpp:</b><br>
<br>
<blockquote>
  <p><font size="2">```<br>
#include "icons.h"<br>
      <br>
std::unique_ptr&lt;wxBitmap&gt; _img_WeatherRouting;<br>
      <br>
void initialize_images() {<br>
    if (!_img_WeatherRouting) {<br>
        _img_WeatherRouting = std::make_unique&lt;wxBitmap&gt;(/*...load bitmap...*/);<br>
    }<br>
}<br>
      <br>
void cleanup_images() {<br>
    _img_WeatherRouting.reset(); // single, thread-safe-ish destroy<br>
}<br>
```</font><br>
  </p>
</blockquote>
<b>plugin destructor:</b><br>
```<br>
weather_routing_pi::~weather_routing_pi() {<br>
    // ... other cleanup ...<br>
    cleanup_images(); // single place that frees the module resource<br>
}<br>
```<br>
<br>
3) Best practice: do NOT free module-shared assets from every instance. Create them once (lazy init) and free them in a single module-level shutdown or when the process exits.<br>
<br>
<b>Verification and further checks</b><br>
- Run with CRT debug heap enabled (_CRTDBG_MAP_ALLOC) or Application Verifier to confirm double-free.<br>
- If host and plugin were built against different CRTs, rebuild both with the same dynamic CRT runtime (matching MSVC runtime) — mismatched CRTs can cause similar crash patterns.<br>
- If you want, paste `icons.cpp` / `initialize_images()` implementation and I will produce a patch to convert to `unique_ptr` and a safe module-level lifecycle.<br>
<br>
<b>Possible improvements (readability/performance)</b><br>
- Replace raw globals with `std::unique_ptr` or `std::shared_ptr`; centralize resource init/cleanup.<br>
- Add RAII wrappers for module resources and document ownership in `icons.h`.<br>
- Add unit or integration tests exercising load/unload sequences to detect lifecycle issues early.
<p>==============================<br>
  <br>
  <b>Copied  icons.cpp  into Copilot as requested.</b><br>
  <br>
===========================<br>
  <br>
  <b>Summary</b><br>
- Root cause: module-global `_img_WeatherRouting` is allocated in `initialize_images()` but freed unconditionally by every plugin instance destructor. Multiple create/destroy cycles cause a double-delete / heap corruption and the crash in msvcp140.dll.<br>
- Minimal safe fix: make allocation idempotent and make per-instance destruction guard the delete and null the pointer.<br>
- Better fix: use a single owner (module-level `std::unique_ptr`) or a module cleanup function called once.<br>
  <br>
  <b>Concrete code changes</b><br>
  <br>
1) Make `initialize_images()` idempotent (icons.cpp)<br>
- Add a guard so you only allocate when the global is null.<br>
  <br>
</p>
<blockquote>
  <p><font size="2">```<br>
// icons.cpp<br>
void initialize_images(void) {<br>
  if (_img_WeatherRouting) return; // &lt;-- guard added<br>
      <br>
  {<br>
    wxMemoryInputStream sm( /* ... existing PNG data ... */ , 2901);<br>
    _img_WeatherRouting = new wxBitmap(wxImage(sm));<br>
  }<br>
      <br>
  // ... existing SVG logic ...<br>
}<br>
```</font><br>
  </p>
</blockquote>
<br>
2) Make destructor free safely (weather_routing_pi.cpp)<br>
- Replace the unconditional `delete _img_WeatherRouting;` with guarded delete + nulling.<br>
<br>
<blockquote><font size="2">```<br>
// weather_routing_pi::~weather_routing_pi()<br>
weather_routing_pi::~weather_routing_pi() {<br>
  // ... other cleanup ...<br>
    <br>
  if (_img_WeatherRouting) {<br>
      delete _img_WeatherRouting;<br>
      _img_WeatherRouting = nullptr;<br>
  }<br>
}<br>
```</font><br>
</blockquote>
<br>
<b>Alternative (recommended) — single-owner pattern</b><br>
- Change `icons.h` and `icons.cpp` to use a `std::unique_ptr&lt;wxBitmap&gt;` and provide `initialize_images()` and `cleanup_images()`:<br>
<br>
<b>icons.h:</b><br>
<blockquote>```<br>
#include &lt;memory&gt;<br>
extern std::unique_ptr&lt;wxBitmap&gt; _img_WeatherRouting;<br>
void initialize_images();<br>
void cleanup_images();<br>
```<br>
</blockquote>
<b>icons.cpp:</b>
<blockquote><font size="2">```<br>
std::unique_ptr&lt;wxBitmap&gt; _img_WeatherRouting;<br>
    <br>
void initialize_images() {<br>
  if (!_img_WeatherRouting) {<br>
    wxMemoryInputStream sm(/*...*/);<br>
    _img_WeatherRouting = std::make_unique&lt;wxBitmap&gt;(wxImage(sm));<br>
  }<br>
}<br>
    <br>
void cleanup_images() {<br>
  _img_WeatherRouting.reset();<br>
}<br>
```</font><br>
</blockquote>
Then call `<b>cleanup_images()</b>` once from a single place (not every plugin instance destructor). If you keep per-instance cleanup, calling `cleanup_images()` there is safe because `unique_ptr::reset()` is idempotent.<br>
<br>
<b>Verification &amp; next steps</b><br>
- Rebuild and run under the debug CRT or enable _CRTDBG_ to confirm heap no longer corrupted.<br>
- If host and plugin use different MSVC runtimes, rebuild them with the same dynamic CRT; mismatched CRTs can cause heap/free issues.<br>
- I can generate a patch (diff) for these changes or modify to use `std::unique_ptr` across files if you want.<br>
<br>
<br>
dumpbin /headers weather_routing_pi.dll | findstr Runtime<br>
<br>
<br>
<p><br>
</p>
<p>=================<br>
  <br>
C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo&gt;dumpbin /dependents weather_routing_pi.dll<br>
Microsoft (R) COFF/PE Dumper Version 14.44.35228.0<br>
Copyright (C) Microsoft Corporation.  All rights reserved.<br>
  <br>
  <b><font size="4">Dump of file weather_routing_pi.dll</font></b><br>
  <br>
File Type: DLL<br>
  <br>
  Image has the following dependencies:<br>
  <br>
    wxbase32u_vc14x.dll<br>
    wxmsw32u_core_vc14x.dll<br>
    wxmsw32u_html_vc14x.dll<br>
    wxmsw32u_aui_vc14x.dll<br>
    OPENGL32.dll<br>
    KERNEL32.dll<br>
    opencpn.exe<br>
    GLU32.dll<br>
    zlib1.dll<br>
    MSVCP140.dll<br>
    MSVCP140_ATOMIC_WAIT.dll<br>
    VCRUNTIME140.dll<br>
    api-ms-win-crt-runtime-l1-1-0.dll<br>
    api-ms-win-crt-stdio-l1-1-0.dll<br>
    api-ms-win-crt-filesystem-l1-1-0.dll<br>
    api-ms-win-crt-heap-l1-1-0.dll<br>
    api-ms-win-crt-math-l1-1-0.dll<br>
    api-ms-win-crt-environment-l1-1-0.dll<br>
    api-ms-win-crt-convert-l1-1-0.dll<br>
    api-ms-win-crt-string-l1-1-0.dll<br>
    api-ms-win-crt-time-l1-1-0.dll<br>
    api-ms-win-crt-utility-l1-1-0.dll<br>
    api-ms-win-crt-locale-l1-1-0.dll<br>
  <br>
  Summary<br>
  <br>
        1000 .00cfg<br>
        F000 .data<br>
       26000 .idata<br>
       D6000 .rdata<br>
       58000 .reloc<br>
        1000 .rsrc<br>
      52B000 .text<br>
        1000 .tls<br>
  <br>
</p>
C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo&gt;wmic datafile where name="C:\\Windows\\System32\\msvcp140.dll" get Version<br>
Version<br>
14.51.36247.0<br>
<br>
<pre style=""><div style="position: absolute; left: -9999px;">dumpbin /headers climatology_pi.dll | findstr Runtime</div></pre>
=================<br>
<br>
PS C:\WINDOWS\system32&gt; cd C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo<br>
PS C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo&gt;<br>
PS C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo&gt; Get-ChildItem "C:\Windows\System32","C:\Windows\SysWOW64" -Filter "msvc*.dll" |<br>
&gt;&gt;     Select-Object Name, @{n="Version";e={(Get-Item $_.FullName).VersionInfo.FileVersion}} |<br>
&gt;&gt;     Sort-Object Version<br>
<br>
Name                      Version<br>
----                      -------<br>
msvcp110_win.dll          10.0.26100.7019 (WinBuild.160101.0800)<br>
msvcp110_win.dll          10.0.26100.7019 (WinBuild.160101.0800)<br>
msvcrt40.dll              10.0.26100.8246 (WinBuild.160101.0800)<br>
msvcp_win.dll             10.0.26100.8875 (WinBuild.160101.0800)<br>
msvcp_win.dll             10.0.26100.8875 (WinBuild.160101.0800)<br>
msvcrt20.dll              10.0.26100.8972 (WinBuild.160101.0800)<br>
msvcp100.dll              10.00.40219.325<br>
msvcr100.dll              10.00.40219.325<br>
msvcr100.dll              10.00.40219.325<br>
msvcp100.dll              10.00.40219.325<br>
msvcr120.dll              12.00.40649.5 built by: VSULDR<br>
msvcp120.dll              12.00.40649.5 built by: VSULDR<br>
msvcr120_clr0400.dll      12.00.52519.0 built by: VSWINSERVICING<br>
msvcp120_clr0400.dll      12.00.52519.0 built by: VSWINSERVICING<br>
msvcp120_clr0400.dll      12.00.52519.0 built by: VSWINSERVICING<br>
msvcr120_clr0400.dll      12.00.52519.0 built by: VSWINSERVICING<br>
msvcp140_clr0400.dll      14.29.30154.0 built by: cloudtest<br>
msvcp140_clr0400.dll      14.29.30154.0 built by: cloudtest<br>
msvcp140d_atomic_wait.dll 14.51.36247.0<br>
msvcp140_1d.dll           14.51.36247.0<br>
msvcp140d_codecvt_ids.dll 14.51.36247.0<br>
msvcp140_1.dll            14.51.36247.0<br>
msvcp140_2.dll            14.51.36247.0<br>
msvcp140_2.dll            14.51.36247.0<br>
msvcp140_1d.dll           14.51.36247.0<br>
msvcp140_codecvt_ids.dll  14.51.36247.0<br>
msvcp140_2d.dll           14.51.36247.0<br>
msvcp140_atomic_wait.dll  14.51.36247.0<br>
msvcp140.dll              14.51.36247.0     &lt;====================================<br>
msvcp140_1.dll            14.51.36247.0<br>
msvcp140d.dll             14.51.36247.0  <br>
msvcp140d_codecvt_ids.dll 14.51.36247.0<br>
msvcp140d_atomic_wait.dll 14.51.36247.0<br>
msvcp140d.dll             14.51.36247.0<br>
msvcp140.dll              14.51.36247.0<br>
msvcp140_2d.dll           14.51.36247.0<br>
msvcp140_codecvt_ids.dll  14.51.36247.0<br>
msvcp140_atomic_wait.dll  14.51.36247.0<br>
msvcr100_clr0400.dll      14.8.9221.0 built by: NET481REL1LAST_25H2<br>
msvcr100_clr0400.dll      14.8.9221.0 built by: NET481REL1LAST_25H2<br>
msvcrtd.dll               6.00.9782.0<br>
msvcp60.dll               7.0.26100.1 (WinBuild.160101.0800)<br>
msvcp60.dll               7.0.26100.1 (WinBuild.160101.0800)<br>
msvcirt.dll               7.0.26100.3323 (WinBuild.160101.0800)<br>
msvcirt.dll               7.0.26100.3323 (WinBuild.160101.0800)<br>
msvcrt.dll                7.0.26100.8875 (WinBuild.160101.0800)<br>
msvcrt.dll                7.0.26100.8875 (WinBuild.160101.0800)<br>
<br>
<br>
PS C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo&gt;<br>
<br>
<pre style=""><div style="position: absolute; left: -9999px;">dumpbin /headers climatology_pi.dll | findstr Runtime</div></pre>
===============================<br>
<b>Get-Process OpenCPN</b><br>
<br>
PS C:\Users\fcgle\source\wr-pob-xweather\build\relwithdebinfo&gt; Get-Process OpenCPN<br>
<br>
Handles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName<br>
-------  ------    -----      -----     ------     --  -- -----------<br>
   1005     472   236248     321044      69.33  25972   1 opencpn<br>
<br>
<br>
Get-Process -Id 25972.Id |<br>
    Select-Object -ExpandProperty Modules |<br>
    Where-Object { $_.ModuleName -match "msvc|vcruntime|concrt" } |<br>
    Select-Object ModuleName, FileVersion<br>
<br>
-------------------------------<br>
<p>Windows PowerShell<br>
Copyright (C) Microsoft Corporation. All rights reserved.<br>
  <br>
PS C:\WINDOWS\system32&gt; Get-Process -Id (Get-Process opencpn).Id |<br>
&gt;&gt;     Select-Object -ExpandProperty Modules |<br>
&gt;&gt;     Where-Object {<br>
&gt;&gt;         $_.ModuleName -match "msv|vc|ucrt" -or<br>
&gt;&gt;         $_.FileName   -match "msv|vc|ucrt"<br>
&gt;&gt;     } |<br>
&gt;&gt;     Select-Object ModuleName, FileVersion, FileName<br>
  <br>
</p>
<p>------------------------------</p>
Windows PowerShell<br>
Copyright (C) Microsoft Corporation. All rights reserved.<br>
<br>
PS C:\WINDOWS\system32&gt; Get-Process -Id (Get-Process opencpn).Id |<br>
&gt;&gt;     Select-Object -ExpandProperty Modules |<br>
&gt;&gt;     Where-Object {<br>
&gt;&gt;         $_.ModuleName -match "msv|vc|ucrt" -or<br>
&gt;&gt;         $_.FileName   -match "msv|vc|ucrt"<br>
&gt;&gt;     } |<br>
&gt;&gt;     Select-Object ModuleName, FileVersion, FileName<br>
<br>
ModuleName                  FileVersion                            FileName<br>
----------                  -----------                            --------<br>
msvcrt.dll                  7.0.26100.8875 (WinBuild.160101.0800)  C:\WINDOWS\System32\msvcrt.dll<br>
wxmsw32u_gl_vc14x.dll       3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
ucrtbase.dll                10.0.26100.8875 (WinBuild.160101.0800) C:\WINDOWS\System32\ucrtbase.dll<br>
msvcp_win.dll               10.0.26100.8875 (WinBuild.160101.0800) C:\WINDOWS\System32\msvcp_win.dll<br>
wxbase32u_net_vc14x.dll     3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxbase32u_xml_vc14x.dll     3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxmsw32u_html_vc14x.dll     3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxmsw32u_aui_vc14x.dll      3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxmsw32u_core_vc14x.dll     3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxbase32u_vc14x.dll         3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxmsw32u_richtext_vc14x.dll 3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
wxmsw32u_webview_vc14x.dll  3.2.9                                  C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\w...<br>
MSVCP140.dll                <b>14.12.25810.0 </b>built by: VCTOOLSREL     C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\M...<br>
VCRUNTIME140.dll            14.12.25810.0 built by: VCTOOLSREL     C:\Program Files (x86)\OpenCPN 5.14.0-0+91f3b67\V...<br>
dhcpcsvc6.DLL               10.0.26100.1 (WinBuild.160101.0800)    C:\WINDOWS\SYSTEM32\dhcpcsvc6.DLL<br>
dhcpcsvc.DLL                10.0.26100.1 (WinBuild.160101.0800)    C:\WINDOWS\SYSTEM32\dhcpcsvc.DLL<br>
srvcli.dll                  10.0.26100.1 (WinBuild.160101.0800)    C:\WINDOWS\SYSTEM32\srvcli.dll<br>
davclnt.dll                 10.0.26100.1 (WinBuild.160101.0800)    C:\WINDOWS\System32\davclnt.dll<br>
MSVCP140_ATOMIC_WAIT.dll    <b>14.51.36247.</b>0                          C:\WINDOWS\SYSTEM32\MSVCP140_ATOMIC_WAIT.dll<br>
<br>
PS C:\WINDOWS\system32&gt;<br>
<br>
===========================================================<br>
<br>
<b>Summary</b><br>
- Root cause: module-global `_img_WeatherRouting` is allocated in `initialize_images()` but freed unconditionally by every plugin instance destructor. Multiple create/destroy cycles cause a double-delete / heap corruption and the crash in msvcp140.dll.<br>
- Minimal safe fix: make allocation idempotent and make per-instance destruction guard the delete and null the pointer.<br>
- Better fix: use a single owner (module-level `std::unique_ptr`) or a module cleanup function called once.<br>
<b><br>
</b>Concrete code changes<br>
<br>
1) Make `initialize_images()` idempotent (icons.cpp)<br>
- Add a guard so you only allocate when the global is null.<br>
<br>
<blockquote><font size="2">```<br>
// icons.cpp<br>
void initialize_images(void) {<br>
  if (_img_WeatherRouting) return; // &lt;-- guard added<br>
    <br>
  {<br>
    wxMemoryInputStream sm( /* ... existing PNG data ... */ , 2901);<br>
    _img_WeatherRouting = new wxBitmap(wxImage(sm));<br>
  }<br>
    <br>
  // ... existing SVG logic ...<br>
}<br>
```</font><br>
</blockquote>
<br>
2) Make destructor free safely (weather_routing_pi.cpp)<br>
- Replace the unconditional `delete _img_WeatherRouting;` with guarded delete + nulling.<br>
<br>
<blockquote><font size="2">```<br>
// weather_routing_pi::~weather_routing_pi()<br>
weather_routing_pi::~weather_routing_pi() {<br>
  // ... other cleanup ...<br>
    <br>
  if (_img_WeatherRouting) {<br>
      delete _img_WeatherRouting;<br>
      _img_WeatherRouting = nullptr;<br>
  }<br>
}<br>
```</font><br>
</blockquote>
<br>
<b>Alternative (recommended) — single-owner pattern</b><br>
- Change `icons.h` and `icons.cpp` to use a `std::unique_ptr&lt;wxBitmap&gt;` and provide `initialize_images()` and `cleanup_images()`:<br>
<br>
<b>icons.h:</b><br>
<blockquote><font size="2">``'<br>
#include &lt;memory&gt;<br>
extern std::unique_ptr&lt;wxBitmap&gt; _img_WeatherRouting;<br>
void initialize_images();<br>
void cleanup_images();<br>
```</font><br>
</blockquote>
<br>
<b>icons.cpp:</b><br>
<br>
<blockquote><font size="2">```<br>
std::unique_ptr&lt;wxBitmap&gt; _img_WeatherRouting;<br>
    <br>
void initialize_images() {<br>
  if (!_img_WeatherRouting) {<br>
    wxMemoryInputStream sm(/*...*/);<br>
    _img_WeatherRouting = std::make_unique&lt;wxBitmap&gt;(wxImage(sm));<br>
  }<br>
}<br>
    <br>
void cleanup_images() {<br>
  _img_WeatherRouting.reset();<br>
}<br>
```</font><br>
</blockquote>
<br>
Then c<i>all `cleanup_images()`</i> once from a single place (not every plugin instance destructor). If you keep per-instance cleanup, calling `cleanup_images()` there is safe because `unique_ptr::reset()` is idempotent.<br>
<br>
<b>Verification &amp; next steps</b><br>
- Rebuild and run under the debug CRT or enable _CRTDBG_ to confirm heap no longer corrupted.<br>
- If host and plugin use different MSVC runtimes, rebuild them with the same dynamic CRT; mismatched CRTs can cause heap/free issues.<br>
- I can generate a patch (diff) for these changes or modify to use `std::unique_ptr` across files if you want.<br>
<!--EndFragment-->
</body>
</html>

## Comment 5628238739

reporter (OWNER) · rgleason · 2026-09-11T01:53:26Z · https://github.com/rgleason/weather_routing_pi/issues/659#issuecomment-5628238739

These are older but related issues.
https://github.com/rgleason/weather_routing_pi/issues/655
https://github.com/rgleason/weather_routing_pi/issues/656
https://github.com/rgleason/weather_routing_pi/issues/657
https://github.com/rgleason/weather_routing_pi/issues/654



## Comment 5640952857

reporter (OWNER) · rgleason · 2026-09-11T21:40:51Z · https://github.com/rgleason/weather_routing_pi/issues/659#issuecomment-5640952857

Had a bad environment with old DLL's.  Copilot helped to isolate the bad dlls and I removed them. I also had to delete old dlls indentified by help from copilot, from Opencpn Release v5.14. Then did a VS Installer, selected  VS Community 2022 and  Removed old files and Updated.  It basically rebuilt VS eliminating my settings too. 

Then rebooted and finally after re build of my pob220 local version and copying to Opencpn Release 5.14, then some fiddling. I finally got a small routing to build with enough detail that I could recognize that it was building properly.  Some of the secondary info is not available but the routing itself shows.

<img width="1200" height="736" alt="Image" src="https://github.com/user-attachments/assets/ac5ba982-d35f-4eff-9a86-5e49083e0449" />

Closing now. 

Will try xweather_routing  in the alpha catalog next.

