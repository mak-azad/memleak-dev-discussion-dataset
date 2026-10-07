# module compilation file descriptor leak

- URL: https://github.com/wesgarland/gpsee/issues/90
- Repo: wesgarland/gpsee (language: C)
- State: open; created 2015-08-23T12:23:09Z; status ok; passes offcwe

## Issue body

reporter (NONE) · GoogleCodeExporter · 2015-08-23T12:23:09Z · https://github.com/wesgarland/gpsee/issues/90

```
Spotted this doing this something else -- but it looks like we have a file 
descriptor leak of the .jsc file when the script compilation throws:

=1814== Open file descriptor 5: /opt/local/gpsee/libexec/.fs-base.jsc
==1814==    at 0x755C52: open$NOCANCEL$UNIX2003 (in /usr/lib/libSystem.B.dylib)
==1814==    by 0x79879: gpsee_compileScript (in 
/opt/local/gpsee/lib/libgpsee.dylib)
==1814==    by 0x75DDB: loadJSModule (in /opt/local/gpsee/lib/libgpsee.dylib)
==1814==    by 0x767B1: loadDiskModule_inDir (in 
/opt/local/gpsee/lib/libgpsee.dylib)
==1814==    by 0x768DB: loadDiskModule_onPath (in 
/opt/local/gpsee/lib/libgpsee.dylib)
==1814==    by 0x76BDE: loadDiskModule (in /opt/local/gpsee/lib/libgpsee.dylib)
==1814==    by 0x7749A: gpsee_loadModule (in 
/opt/local/gpsee/lib/libgpsee.dylib)

This particular script had a syntax error in it (new was used a variable name).
```

Original issue reported on code.google.com by `wes@page.ca` on 26 Sep 2011 at 2:06

