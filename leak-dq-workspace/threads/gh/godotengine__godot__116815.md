# Texture2DRD causes a memory leak

- URL: https://github.com/godotengine/godot/issues/116815
- Repo: godotengine/godot (language: C++)
- State: open; created 2026-02-26T17:49:11Z; status ok; passes main

## Issue body

reporter (NONE) · SNAKFRIEN · 2026-02-26T17:49:11Z · https://github.com/godotengine/godot/issues/116815

### Tested versions

Reproducible in
- 4.5.1.stable
- 4.6.stable
- https://github.com/godotengine/godot/commit/2327a823578a30f09068f97272598521896d5633

### System information

I tested 2 systems:

Godot v4.6.stable - Windows 11 (build 26200) - Multi-window, 1 monitor - Direct3D 12 (Forward+) - dedicated NVIDIA GeForce RTX 5070 Ti (NVIDIA; 32.0.15.9186) - Intel(R) Core(TM) i9-14900KF (32 threads) - 31.79 GiB memory

Godot v4.6.stable - Windows 11 (build 26100) - Multi-window, 1 monitor - Direct3D 12 (Forward+) - dedicated NVIDIA GeForce GTX 1650 with Max-Q Design (NVIDIA; 31.0.15.3892) - Intel(R) Core(TM) i7-1065G7 CPU @ 1.30GHz (8 threads) - 15.59 GiB memory

### Issue description

When creating a Texture2DRD from within a tool script, its texture RID is never freed. I don't know how to test whether the same bug occurs when running the game (as opposed to the editor).

When the editor exits, the following warning appears in the console:
```
WARNING: 1 RID of type "Texture" was leaked.
     at: finalize (servers/rendering/rendering_device.cpp:7503)
```

I originally found the bug while working on a GDExtension using C++. I did some testing with a custom build of the engine, and when printing the RID from within the source code for Texture2DRD, I got a different result than the RID I received in my GDExtension code when calling ```get_texture_rd_rid```. In other words, it's almost as if Texture2DRD stores and frees a different RID than the one I created in my code.

Perhaps this is only an issue in the editor, but I wouldn't know, because I'm not getting any memory leak warnings when running the game, even when I deliberately leak a texture RID...

### Steps to reproduce

This tool script will create a Texture2DRD when you toggle "test_texture_free" from the inspector. From my understanding, the texture should go out of scope after the function runs, and free the texture RID. 

However, when I close the editor, the console shows that the Texture RID has leaked.

```gdscript
@tool
extends Node

@export var test_texture_free : bool:
	set(v):
		TestTextureFree()
		test_texture_free = false

func TestTextureFree():
	print("GDScript: Testing Texture Free...")
	
	var width = 32
	var height = 32
	
	var mainRd = RenderingServer.get_rendering_device()
	
	var fmt = RDTextureFormat.new()
	fmt.format = RenderingDevice.DATA_FORMAT_R32G32B32A32_SFLOAT
	fmt.texture_type = RenderingDevice.TEXTURE_TYPE_2D
	fmt.width = width
	fmt.height = height
	fmt.depth = 1
	fmt.array_layers = 1
	fmt.mipmaps = 1
	fmt.usage_bits = \
		RenderingDevice.TEXTURE_USAGE_SAMPLING_BIT + \
		RenderingDevice.TEXTURE_USAGE_STORAGE_BIT + \
		RenderingDevice.TEXTURE_USAGE_CAN_COPY_TO_BIT + \
		RenderingDevice.TEXTURE_USAGE_CAN_COPY_FROM_BIT
	
	var rid = mainRd.texture_create(fmt, RDTextureView.new())
	print("Texture RID is ", rid)
	var tex = Texture2DRD.new()
	tex.set_texture_rd_rid(rid)
```

### Minimal reproduction project (MRP)

[texture-leak.zip](https://github.com/user-attachments/files/25583322/texture-leak.zip)

## Comment 3969355162

other (CONTRIBUTOR) · sockeye-d · 2026-02-26T21:32:59Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3969355162

I don't think it can be freed because the rid of the texture is never freed. What happens if you free rid? Does tex ever get destructed?

## Comment 3969391133

reporter (NONE) · SNAKFRIEN · 2026-02-26T21:40:45Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3969391133

@sockeye-d I can manually free the RID of the texture, but from my understanding, Texture2DRD is supposed to do that automatically. Texture2DRD  should take ownership of the RID passed into set_texture_rd_rid, and its destructor then frees the RID when Texture2DRD goes out of scope.
I would also assume that tex gets destroyed automatically after ```TestTextureFree()```, because it's a local variable in that function.

## Comment 3969705601

other (CONTRIBUTOR) · NoctemCat · 2026-02-26T22:53:02Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3969705601

Looks like it won't free underlying texture, it uses `texture_rd_create` inside `set_texture_rd_rid`. And it does free returned from it rid, but docs mentions that you will need to free the underlying texture yourself https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#class-renderingserver-method-texture-rd-create , the destructor also doesn't touch passed texture


## Comment 3969817826

reporter (NONE) · SNAKFRIEN · 2026-02-26T23:21:13Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3969817826

@NoctemCat Thanks for looking into this. Looking at the source code, I think you may be right

@AThousandShips Perhaps you want to weigh in. I noticed you liked sockeye-d's comment, but you also recently contributed to this pull requests which states that you should not manually free the RID after passing it to Texture2DRD: https://github.com/godotengine/godot/pull/116671

## Comment 3971795674

maintainer (MEMBER) · AThousandShips · 2026-02-27T09:29:54Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3971795674

I'll take a closer look today, might depend on how quickly the texture resource is freed, it *should* own it, but it might depend, it might also not be *that* texture that leaks, it might be some other texture in that chain 

## Comment 3972322487

reporter (NONE) · SNAKFRIEN · 2026-02-27T11:13:51Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3972322487

@AThousandShips I appreciate it!

As NoctemCat said, the current behavior does not free the RID you pass into set_texture_rd_rid. The code is a bit confusing to read, because Texture2DRD stores both a texture_rid as well as a texture_rd_rid (that threw me off anyway).

So either the current behavior is correct, and Texture2DRD _should not_ own the RID passed into set_texture_rd_rid, or the current behavior is incorrect, and it _should_ own the RID. Either way, the documentation should probably reflect that, once we figure this out.

## Comment 3985509106

other (NONE) · RemiPKFX · 2026-03-02T16:41:46Z · https://github.com/godotengine/godot/issues/116815#issuecomment-3985509106

> this pull requests which states that you should not manually free the RID after passing it to Texture2DRD: [#116671](https://github.com/godotengine/godot/pull/116671)

Hey! Since I made the issue for the PR you mentionned, I thought I'd pop in and add some of the things I've observed.

I'm using `Texture2DRD` as a makeshift buffer for reading in gdshaders, so my code needs to reallocate the rd_rid quite often when the buffer changes size.

What lead me to believe that `set_texture_rd_rid` took ownership of the rd_rid it was given, is that if the current rd_rid is freed before creating a new one and setting it, an error is logged: "Attempted to free invalid ID". The implementation of that method is indeed quite confusing to read and debug, so at a glance it looked like something might be freeing my rd_rid.

I've dug quite a bit into it today, and here's what I concluded:
- Internally, `Texture2DRD` creates quite a few RIDs for textures, shared textures and texture views. These are all taken care of and freed internally, but one of them uses `RenderingDevice::_add_dependency` to link itself to the rd_rid given to `set_texture_rd_rid`
- When I freed my rd_rid, its dependencies were freed as well (including that internal shared texture)
- Later, when `set_texture_rd_rid` was called again with a new rd_rid, `Texture2DRD` tried to free its internal resources and threw the invalid ID error because the shared texture was already freed

TL;DR: Currently `Texture2DRD` doesn't take ownership of the RID given in `set_texture_rd_rid`: it must be freed manually. ***However***, if the RID is still referenced in `Texture2DRD`, it must first be replaced by a new one, or by an invalid RID.
