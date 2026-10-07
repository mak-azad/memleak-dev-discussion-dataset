# [🐛 bug report] GPU memory leak issue

- URL: https://github.com/mitsuba-renderer/mitsuba2/issues/294
- Repo: mitsuba-renderer/mitsuba2 (language: C++)
- State: open; created 2020-10-16T12:12:35Z; status ok; passes offcwe

## Issue body

reporter (NONE) · diolatzis · 2020-10-16T12:12:35Z · https://github.com/mitsuba-renderer/mitsuba2/issues/294

Hey thanks for the great work on Mitsuba 2 so far!

## Summary

I have an issue of GPU memory leak when rendering using the "gpu_rgb" variant of mitsuba 2. 

## System configuration

Windows 10
Visual Studio 2019
Python 3.7.9
gpu_rgb variant 

## Description

When rendering a scene (the cbox from the documentation) through python in a loop for dataset generation the GPU used memory is slowly increasing. Am I missing something or is there some GPU memory leak?

## Steps to reproduce

To test this I changed the render_scene.py example script to render in a loop and the GPU memory usage is slowly increasing. 

```import os
import numpy as np
import mitsuba

# Set the desired mitsuba variant
mitsuba.set_variant('gpu_rgb')

from mitsuba.core import Bitmap, Struct, Thread
from mitsuba.core.xml import load_file

# Absolute or relative path to the XML file
filename = 'cbox.xml'

# Add the scene directory to the FileResolver's search path
Thread.thread().file_resolver().append(os.path.dirname(filename))

# Load the actual scene
scene = load_file(filename)

while True:
    # Call the scene's integrator to render the loaded scene
    scene.integrator().render(scene, scene.sensors()[0])

# After rendering, the rendered data is stored in the film
film = scene.sensors()[0].film()

# Write out rendering as high dynamic range OpenEXR file
film.set_destination_file('output.exr')
film.develop()

# Write out a tonemapped JPG of the same rendering
bmp = film.bitmap(raw=True)
bmp.convert(Bitmap.PixelFormat.RGB, Struct.Type.UInt8, srgb_gamma=True).write('output.jpg')

# Get linear pixel values as a numpy array for further processing
bmp_linear_rgb = bmp.convert(Bitmap.PixelFormat.RGB, Struct.Type.Float32, srgb_gamma=False)
image_np = np.array(bmp_linear_rgb)
print(image_np.shape)


## Comment 710016725

maintainer (MEMBER) · wjakob · 2020-10-16T12:31:47Z · https://github.com/mitsuba-renderer/mitsuba2/issues/294#issuecomment-710016725

Hi Stavros -- does the leak still happen when you add a `enoki.cuda_malloc_trim()` call to the loop?

## Comment 710025677

reporter (NONE) · diolatzis · 2020-10-16T12:50:58Z · https://github.com/mitsuba-renderer/mitsuba2/issues/294#issuecomment-710025677

Hi Wenzel, adding this make the memory usage fluctuate much more but on average it is still increasing (albeit more slowly).

## Comment 899350910

other (NONE) · f1shel · 2021-08-16T09:07:54Z · https://github.com/mitsuba-renderer/mitsuba2/issues/294#issuecomment-899350910

Same...I use `gpu_rgb` too. Following is my rendering loop:
```
for asset in asset_list:
    for envmap in envmap_list:
        for envrot in range(0,360,10):
            ek.cuda_malloc_trim()
            scene = load_string(build_scene(...))
            scene.integrator().render(scene, scene.sensors()[0])
            film = scene.sensors()[0].film()
            film.set_destination_file(...)
            film.develop()
```
It gives `cuda_check(): runtime API error = 0002 "cudaErrorMemoryAllocation" in ../ext/enoki/src/cuda/horiz.cu:59.`
