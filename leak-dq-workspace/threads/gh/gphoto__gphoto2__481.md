# Fuji X-T2 munmap_chunk(): invalid pointer

- URL: https://github.com/gphoto/gphoto2/issues/481
- Repo: gphoto/gphoto2 (language: C)
- State: open; created 2022-01-19T15:20:28Z; status ok; passes main

## Issue body

reporter (NONE) · nikarc · 2022-01-19T15:20:28Z · https://github.com/gphoto/gphoto2/issues/481

Hello,

I've lately been getting an `invalid pointer` error when trying to use `--capture-movie` with my Fuji X-T2.

I had been using gphoto2 for a while now, to pipe stdout to ffmpeg and use as my webcam, but it recently stopped working. Not sure if this is a problem on my end.

Here is my system info:
![image](https://user-images.githubusercontent.com/3580396/150159020-2df23a11-89ab-420c-870e-d5842242f234.png)


Here is the output when i run it through `gdb`:
```bash
GNU gdb (GDB) 11.1
Copyright (C) 2021 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-pc-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from gphoto2...
(No debugging symbols found in gphoto2)
(gdb) run
Starting program: /usr/bin/gphoto2 --capture-movie --stdout
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/libthread_db.so.1".
[New Thread 0x7ffff7726640 (LWP 35763)]
[Thread 0x7ffff7726640 (LWP 35763) exited]
[New Thread 0x7ffff7726640 (LWP 35764)]
[Thread 0x7ffff7726640 (LWP 35764) exited]
[New Thread 0x7ffff7726640 (LWP 35765)]
[Thread 0x7ffff7726640 (LWP 35765) exited]
[New Thread 0x7ffff7726640 (LWP 35766)]
[Thread 0x7ffff7726640 (LWP 35766) exited]
[New Thread 0x7ffff7726640 (LWP 35767)]
[Thread 0x7ffff7726640 (LWP 35767) exited]
[New Thread 0x7ffff7726640 (LWP 35768)]
[Thread 0x7ffff7726640 (LWP 35768) exited]
[New Thread 0x7ffff7726640 (LWP 35770)]
Capturing preview frames as movie to 'stdout'. Press Ctrl-C to abort.
munmap_chunk(): invalid pointer

Thread 1 "gphoto2" received signal SIGABRT, Aborted.
0x00007ffff7c7ad22 in raise () from /usr/lib/libc.so.6
```
Here is `--version`:
```bash
gphoto2 2.5.28

Copyright (c) 2000-2021 Marcus Meissner and others

gphoto2 comes with NO WARRANTY, to the extent permitted by law. You may
redistribute copies of gphoto2 under the terms of the GNU General Public
License. For more information about these matters, see the files named COPYING.

This version of gphoto2 is using the following software versions and options:
gphoto2         2.5.28         gcc, popt(m), exif, no cdk, no aa, jpeg, readline
libgphoto2      2.5.28         standard camlibs, gcc, no ltdl, EXIF
libgphoto2_port 0.12.0         iolibs: disk ptpip serial usb1 usbdiskdirect usbscsi, gcc, no ltdl, EXIF, USB, serial without locking
```

Here is `--abilities` output:
```bash
gphoto2 --abilities
Abilities for camera             : Fuji Fujifilm X-T2
Serial port support              : no
USB support                      : yes
Capture choices                  :
                                 : Image
                                 : Preview
Configuration support            : yes
Delete selected files on camera  : yes
Delete all files on camera       : no
File preview (thumbnail) support : yes
File upload support              : yes
```
And here is `--summary`:
```bash
Camera summary:
Manufacturer: FUJIFILM
Model: X-T2
  Version: 3.00
  Serial Number: 593533313032170626784020217266
Vendor Extension ID: 0xe (1.0)
Vendor Extension Description: fujifilm.co.jp: 1.0; 

Capture Formats: Defined Type JPEG Unknown(b103)
Display Formats: Defined Type, JPEG, Unknown(b103)

Device Capabilities:
	File Download, File Deletion, No File Upload
	Generic Image Capture, Open Capture, No vendor specific capture

Storage Devices Summary:
store_10000001:
	StorageDescription: Still
	VolumeLabel: 1593533313032170626784020217266
	Storage Type: Builtin RAM
	Filesystemtype: Generic Hierarchical
	Access Capability: Read Only with Object deletion
	Maximum Capability: 18446744073709551615 (17592186044415 MB)
	Free Space (Bytes): 18446744073709551615 (17592186044415 MB)
	Free Space (Images): -1
store_10000002:
	StorageDescription: Live
	VolumeLabel: 2593533313032170626784020217266
	Storage Type: Builtin RAM
	Filesystemtype: Generic Hierarchical
	Access Capability: Read Only with Object deletion
	Maximum Capability: 18446744073709551615 (17592186044415 MB)
	Free Space (Bytes): 18446744073709551615 (17592186044415 MB)
	Free Space (Images): -1

Device Property Summary:
Battery Level(0x5001): error 200a on query.
Image Size(0x5003):(readwrite) (type=0xffff) Enumeration [
	'3008x2000',
	'3008x1688',
	'2000x2000',
	'4240x2832',
	'4240x2384',
	'2832x2832',
	'6000x4000',
	'6000x3376',
	'4000x4000'
	] value: '6000x4000'
White Balance(0x5005):(readwrite) (type=0x4) Enumeration [2,4,6,8,32769,32770,32771,32774,32775,32776,32777,32778] value: Automatic (2)
Focus Mode(0x500a):(readwrite) (type=0x4) Enumeration [1,32769,32770] value: Manual Focus (1)
Exposure Metering Mode(0x500b):(readwrite) (type=0x4) Enumeration [1,2,3,4] value: Multi-spot (3)
Flash Mode(0x500c): error 200a on query.
Exposure Program Mode(0x500e):(readwrite) (type=0x4) Enumeration [1,3,4,6] value: A (3)
Exposure Index (film speed ISO)(0x500f):(readwrite) (type=0x5) Enumeration [100,125,160,200,250,320,400,500,640,800,1000,1250,1600,2000,2500,3200,4000,5000,6400,8000,10000,12800,25600,51200,-1,-2,-3] value: ISO -1 (-1)
Date & Time(0x5011):(readwrite) (type=0xffff) '20220119T102500'
Pre-Capture Delay(0x5012):(readwrite) (type=0x4) Enumeration [10000,2000,0] value: 0.0s (0)
Sharpness(0x5015):(readwrite) (type=0x3) Range [-40 - 40, step 10] value: 10
Burst Number(0x5018): error 200a on query.
Burst Interval(0x5019): error 200a on query.
Focus Metering Mode(0x501c):(readwrite) (type=0x4) Enumeration [32769,32770,32771] value: 32769
Film Simulation(0xd001):(readwrite) (type=0x4) Enumeration [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15] value: 11
FilmSimulationTune(0xd002): error 200a on query.
Property 0xd003: error 200a on query.
Property 0xd004: error 200a on query.
Property 0xd005: error 200a on query.
DRangeMode(0xd007):(readwrite) (type=0x4) Enumeration [65535,100,200,400] value: 200
ColorMode(0xd008):(readwrite) (type=0x3) Range [-40 - 40, step 10] value: -10
Property 0xd009: error 200a on query.
ColorSpace(0xd00a):(readwrite) (type=0x4) Enumeration [1,2] value: 1
WhitebalanceTune1(0xd00b):(readwrite) (type=0x3) Range [-9 - 9, step 1] value: 3
WhitebalanceTune2(0xd00c):(readwrite) (type=0x3) Range [-9 - 9, step 1] value: -4
Property 0xd00d: error 200a on query.
Property 0xd00e: error 200a on query.
Property 0xd00f: error 200a on query.
Property 0xd010: error 200a on query.
Property 0xd011: error 200a on query.
Property 0xd012: error 200a on query.
Property 0xd013: error 200a on query.
Property 0xd014: error 200a on query.
Property 0xd015: error 200a on query.
Property 0xd016: error 200a on query.
Color Temperature(0xd017):(readwrite) (type=0x4) Enumeration [2500,2550,2650,2700,2800,2850,2950,3000,3100,3200,3300,3400,3600,3700,3800,4000,4200,4300,4500,4800,5000,5300,5600,5900,6300,6700,7100,7700,8300,9100,10000] value: 10000
Quality(0xd018):(readwrite) (type=0x4) Enumeration [1,2,3,4,5] value: 4
RecMode(0xd019): error 200a on query.
LiveViewBrightness(0xd01a): error 200a on query.
ThroughImageZoom(0xd01b):(readwrite) (type=0x4) Enumeration [1,2,3] value: 1
NoiseReduction(0xd01c):(readwrite) (type=0x4) Enumeration [0,4096,8192,12288,16384,20480,24576,28672,32768] value: 28672
Comment(0xd100):(readwrite) (type=0xffff) ''
SerialMode(0xd101): error 200a on query.
ExposureDelay(0xd102): error 200a on query.
PreviewTime(0xd103): error 200a on query.
BlackImageTone(0xd104): error 200a on query.
Illumination(0xd105): error 200a on query.
FrameGuideMode(0xd106):(readwrite) (type=0x4) Enumeration [1,2,3] value: 1
ViewfinderWarning(0xd107): error 200a on query.
AutoImageRotation(0xd108): error 200a on query.
DetectImageRotation(0xd109): error 200a on query.
ShutterPriorityMode1(0xd10a):(readwrite) (type=0x4) Enumeration [1,2] value: 1
ShutterPriorityMode2(0xd10b):(readwrite) (type=0x4) Enumeration [1,2] value: 1
Property 0xd10c: error 200a on query.
Property 0xd10d: error 200a on query.
Property 0xd10e: error 200a on query.
Property 0xd10f: error 200a on query.
Property 0xd110: error 200a on query.
Property 0xd111: error 200a on query.
AFIlluminator(0xd112):(readwrite) (type=0x4) Enumeration [1,2] value: 1
Beep(0xd113): error 200a on query.
AELock(0xd114): error 200a on query.
ISOAutoSetting1(0xd115): error 200a on query.
ISOAutoSetting2(0xd116): error 200a on query.
ISOAutoSetting3(0xd117): error 200a on query.
ExposureStep(0xd118): error 200a on query.
CompensationStep(0xd119): error 200a on query.
ExposureSimpleSet(0xd11a): error 200a on query.
CenterPhotometryRange(0xd11b): error 200a on query.
PhotometryLevel1(0xd11c): error 200a on query.
PhotometryLevel2(0xd11d): error 200a on query.
PhotometryLevel3(0xd11e): error 200a on query.
FlashTuneSpeed(0xd11f): error 200a on query.
FlashShutterLimit(0xd120): error 200a on query.
BuiltinFlashMode(0xd121): error 200a on query.
FlashManualMode(0xd122): error 200a on query.
FlashRepeatingMode1(0xd123): error 200a on query.
FlashRepeatingMode2(0xd124): error 200a on query.
FlashRepeatingMode3(0xd125): error 200a on query.
FlashCommanderMode1(0xd126): error 200a on query.
FlashCommanderMode2(0xd127): error 200a on query.
FlashCommanderMode3(0xd128): error 200a on query.
FlashCommanderMode4(0xd129): error 200a on query.
FlashCommanderMode5(0xd12a): error 200a on query.
FlashCommanderMode6(0xd12b): error 200a on query.
FlashCommanderMode7(0xd12c): error 200a on query.
ModelingFlash(0xd12d): error 200a on query.
Property 0xd12e: error 200a on query.
BKTChange(0xd12f): error 200a on query.
BKTOrder(0xd130): error 200a on query.
BKTSelection(0xd131): error 200a on query.
AEAFLockButton(0xd132): error 200a on query.
CenterButton(0xd133): error 200a on query.
MultiSelectorButton(0xd134): error 200a on query.
Property 0xd135: error 200a on query.
FunctionLock(0xd136):(readwrite) (type=0x4) Enumeration [1,2,3] value: 1
Property 0xd137: error 200a on query.
Property 0xd138: error 200a on query.
Property 0xd139: error 200a on query.
Property 0xd13a: error 200a on query.
Property 0xd13b: error 200a on query.
Property 0xd13c: error 200a on query.
Property 0xd13d: error 200a on query.
Property 0xd13e: error 200a on query.
Property 0xd13f: error 200a on query.
Property 0xd140: error 200a on query.
Property 0xd141: error 200a on query.
Property 0xd142: error 200a on query.
Property 0xd143: error 200a on query.
Property 0xd144: error 200a on query.
Password(0xd145):(readwrite) (type=0xffff) '0000'
ChangePassword(0xd146): error 200a on query.
CommandDialSetting1(0xd147): error 200a on query.
CommandDialSetting2(0xd148): error 200a on query.
CommandDialSetting3(0xd149): error 200a on query.
CommandDialSetting4(0xd14a): error 200a on query.
ButtonsAndDials(0xd14b): error 200a on query.
NonCPULensData(0xd14c): error 200a on query.
Property 0xd14d: error 200a on query.
MBD200Batteries(0xd14e): error 200a on query.
AFOnForMBD200Batteries(0xd14f): error 200a on query.
Property 0xd150: error 200a on query.
Property 0xd151: error 200a on query.
Property 0xd152: error 200a on query.
FirmwareVersion(0xd153):(read only) (type=0x4) 768
ShotCount(0xd154):(read only) (type=0x6) 806158336
ShutterExchangeCount(0xd155):(read only) (type=0x6) 0
WorldClock(0xd157): error 200a on query.
TimeDifference1(0xd158): error 200a on query.
TimeDifference2(0xd159): error 200a on query.
Language(0xd15a): error 200a on query.
FrameNumberSequence(0xd15b): error 200a on query.
VideoMode(0xd15c): error 200a on query.
SetUSBMode(0xd15d): error 200a on query.
Property 0xd15e: error 200a on query.
Property 0xd15f: error 200a on query.
Property 0xd160: error 200a on query.
CommentWriteSetting(0xd161): error 200a on query.
LightTune(0xd200): error 200a on query.
ReleaseMode(0xd201):(readwrite) (type=0x4) Enumeration [4] value: 4
BKTFrame1(0xd202): error 200a on query.
BKTFrame2(0xd203): error 200a on query.
BKTStep(0xd204): error 200a on query.
ProgramShift(0xd205): error 200a on query.
FocusAreas(0xd206): error 200a on query.
PriorityMode(0xd207):(readwrite) (type=0x4) Enumeration [1,2] value: 2
Property 0xd208:(readwrite) (type=0x4) Enumeration [260,512,4,772,1280,12,40960,6,36864,2,37120,1,37632,5] value: 772
AFStatus(0xd209):(read only) (type=0x4) Enumeration [1,2,3,4] value: 1
Property 0xd20a: error 200a on query.
DeviceName(0xd20b):(readwrite) (type=0xffff) ''
MediaRecord(0xd20c):(readwrite) (type=0x4) Enumeration [1,2,3,4] value: 4
MediaCapacity(0xd20d):(read only) (type=0xffff) '0,14,2537536,9,0,13,9843136,9'
FreeSDRAMImages(0xd20e):(read only) (type=0x4) Range [0 - 1, step 1] value: 19
Property 0xd20f: error 200a on query.
Property 0xd210: error 200a on query.
MediaStatus(0xd211):(read only) (type=0x4) Range [0 - 65535, step 1] value: 257
CurrentState(0xd212): error 201b on query.
Property 0xd213: error 200a on query.
Property 0xd214: error 200a on query.
Copyright(0xd215):(readwrite) (type=0xffff) ''
Copyright2(0xd216):(readwrite) (type=0xffff) ''
Property 0xd217: error 200a on query.
Aperture(0xd218): error 200a on query.
ShutterSpeed(0xd219): error 200a on query.
Property 0xd21a: error 200a on query.
DeviceError(0xd21b): error 200a on query.
Property 0xd406:(readwrite) (type=0xffff) ''
Property 0xd407:(read only) (type=0x6) 1
Exposure Time(0x500d):(readwrite) (type=0x6) Enumeration [] value: 0.16 sec (15625)
F-Number(0x5007):(readwrite) (type=0x4) Enumeration [120,140,160,180,200,220,250,280,320,360,400,450,500,560,640,710,800,900,1000,1100,1300,1400,1600,1800,2000,2200] value: f/0 (0)
LensZoomPosCaps(0xd38c):(readwrite) (type=0x4) Range [1 - 1, step 1] value: 1
FocusPosition(0xd171):(readwrite) (type=0x3) Enumeration [0,0,0,0,0,0] value: 0
Property 0xd21c:(readwrite) (type=0x4) Enumeration [0,1,2,3,4,5,6,7,8,9,10,11] value: 3
Focus Point(0xd347): error 201b on query.
LensZoomPos(0xd170):(read only) (type=0x4) Range [1 - 1, step 1] value: 1
BatteryLevel(0xd242): error 200a on query.
LiveViewImageSize(0xd174):(readwrite) (type=0x4) Enumeration [1,2,3] value: 2
VideoOutOnOff(0xd168): error 200a on query.
LiveViewImageQuality(0xd173):(readwrite) (type=0x4) Enumeration [1,3] value: 1
ForceMode(0xd230):(readwrite) (type=0x4) Enumeration [1] value: 1
Property 0xd16e: error 200a on query.
FocusArea1(0xd372): error 201b on query.
FaceDetectionMode(0xd020):(readwrite) (type=0x4) Enumeration [1,2] value: 2
RawCompression(0xd022):(readwrite) (type=0x4) Enumeration [1,2] value: 1
GrainEffect(0xd023):(readwrite) (type=0x4) Enumeration [1,2,3] value: 2
SetEyeAFMode(0xd024):(readwrite) (type=0x4) Enumeration [1,2,3,4] value: 1
FocusPoints(0xd025):(readwrite) (type=0x4) Enumeration [1,2] value: 2
MFAssistMode(0xd026):(readwrite) (type=0x4) Enumeration [1,2,3,4,5,6,7,8,9] value: 1
InterlockAEAFArea(0xd027):(readwrite) (type=0x4) Enumeration [1,2] value: 1
Shadowing(0xd029): error 200a on query.
CropMode(0xd16f): error 200a on query.
TNumber(0xd02f): error 200a on query.
FocusArea4(0xd395): error 201b on query.
HighLightTone(0xd320):(readwrite) (type=0x3) Range [-20 - 40, step 10] value: 10
ShadowTone(0xd321):(readwrite) (type=0x3) Range [-20 - 40, step 10] value: 20
LongExposureNR(0xd322):(readwrite) (type=0x4) Enumeration [1,2] value: 1
FullTimeManualFocus(0xd323):(readwrite) (type=0x4) Enumeration [1,2] value: 2
LensISSwitch(0xd346):(readwrite) (type=0x4) Enumeration [1,2] value: 2
InstantAFMode(0xd34a):(readwrite) (type=0x4) Enumeration [1,2] value: 1
PreAFMode(0xd34b):(readwrite) (type=0x4) Enumeration [1,2] value: 2
LMOMode(0xd34d):(readwrite) (type=0x4) Enumeration [1,2] value: 2
ISMode(0xd351):(readwrite) (type=0x4) Enumeration [1,2,3] value: 3
FocusCheckMode(0xd35e):(readwrite) (type=0x4) Enumeration [1,2] value: 2
LiveViewImageQuality(0xd173):(readwrite) (type=0x4) Enumeration [1,3] value: 1
FileNamePrefix1(0xd365):(readwrite) (type=0xffff) 'DSCF'
FileNamePrefix2(0xd366):(readwrite) (type=0xffff) 'DSF'
FocusArea3(0xd374): error 201b on query.
TotalShotCount(0xd310):(read only) (type=0x6) 806158336
ExposurePreview(0xd359):(readwrite) (type=0x4) Enumeration [1,2,3] value: 1
FrameGuideGridInfo1(0xd375):(readwrite) (type=0xffff) '0,0,0,0,850,0,0,0,0,850,0,0,0,0,'
FrameGuideGridInfo2(0xd376):(readwrite) (type=0xffff) '0,0,0,0,850,0,0,0,0,850,0,0,0,0,'
CustomDispInfo(0xd36e): error 200a on query.
ViewMode1(0xd33f):(readwrite) (type=0x4) Enumeration [1,2,3,4,5] value: 5
CustomAutoPowerOff(0xd364):(readwrite) (type=0x4) Range [0 - 255, step 1] value: 0
LockButtonMode(0xd34e):(readwrite) (type=0x4) Enumeration [1,2] value: 1
WideDynamicRange(0xd02e): error 200a on query.
LensNameAndSerial(0xd36d):(read only) (type=0xffff) ',,'
LensUnknownData(0xd38a):(read only) (type=0x4) Enumeration [1,2,3,4,5] value: 1
BatteryInfo1(0xd36a):(read only) (type=0x6) Range [0 - 16777215, step 1] value: 12
BatteryInfo2(0xd36b):(read only) (type=0xffff) '92,0,0'
FunctionLockCategory1(0xd36f):(readwrite) (type=0x6) 65536
FunctionLockCategory2(0xd370):(readwrite) (type=0x6) 65536
SensitivityFineTune1(0xd222):(readwrite) (type=0x4) Range [0 - 65535, step 1] value: 8192
SensitivityFineTune2(0xd223):(readwrite) (type=0x4) Range [0 - 65535, step 1] value: 8192
LensZoomPosCaps(0xd38c):(readwrite) (type=0x4) Range [1 - 1, step 1] value: 1
LensFNumberList(0xd38d):(read only) (type=0xffff) ''
LensFocalLengthList(0xd38e):(read only) (type=0xffff) '0,0'
Property 0xd17b:(readwrite) (type=0x4) Enumeration [1] value: 1
```


## Comment 1016574191

other (CONTRIBUTOR) · msmeissn · 2022-01-19T15:21:51Z · https://github.com/gphoto/gphoto2/issues/481#issuecomment-1016574191

a regression in 2.5.28 caused by me, sorry ... see https://github.com/gphoto/gphoto2/issues/480                                                                                                                                                   
... i just fixed it in libgphoto2 GIT. Need to consider a new incremental release...

