# No OpenGL resource management

- URL: https://github.com/pmartz/jag-3d/issues/3
- Repo: pmartz/jag-3d (language: C++)
- State: open; created 2015-03-14T21:51:47Z; status ok; passes offcwe

## Issue body

reporter (NONE) · GoogleCodeExporter · 2015-03-14T21:51:47Z · https://github.com/pmartz/jag-3d/issues/3

```
Currently Jag3D makes no attempt to track and delete unused OpenGL resources 
(texture IDs, buffer IDs, etc). These resources are simply leaked. Code needs 
to be written to support intelligent management of these resources.
```

Original issue reported on code.google.com by `SkewMat...@gmail.com` on 16 Apr 2013 at 6:19

