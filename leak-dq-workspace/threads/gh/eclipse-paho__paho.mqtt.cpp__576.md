# Memory leak in property::operator= (copy and move)

- URL: https://github.com/eclipse-paho/paho.mqtt.cpp/issues/576
- Repo: eclipse-paho/paho.mqtt.cpp (language: C++)
- State: open; created 2026-07-10T11:43:27Z; status ok; passes main

## Issue body

reporter (NONE) · ErikDervishi03 · 2026-07-10T11:43:27Z · https://github.com/eclipse-paho/paho.mqtt.cpp/issues/576

Both assignment operators of mqtt::property (src/properties.cpp) overwrite the internal MQTTProperty without freeing the heap buffer the object already owns. 
copy() does memcpy then malloc, never freeing the old buffers
move-assign does memcpy + memset, never freeing the old buffers

Confirmed on 1.6.0

```bash
./leak_poc copy

=================================================================
==41539==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 100 byte(s) in 1 object(s) allocated from:
    #0 0x7f60f14b89cf in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7f60f13b464e in mqtt::property::property(mqtt::property::code, mqtt::buffer_ref<char>) (/usr/local/lib/libpaho-mqttpp3.so.1+0x10e64e)
    #2 0x55f963829aaf in leak_via_copy /home/.../mqtt/leak_poc.cpp:24
    #3 0x55f963829e41 in main /home/.../mqtt/leak_poc.cpp:33
    #4 0x7f60f0d65249 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: 100 byte(s) leaked in 1 allocation(s).
```
```bash
./leak_poc move     

=================================================================
==41585==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 100 byte(s) in 1 object(s) allocated from:
    #0 0x7fac8b4b89cf in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7fac8b3b464e in mqtt::property::property(mqtt::property::code, mqtt::buffer_ref<char>) (/usr/local/lib/libpaho-mqttpp3.so.1+0x10e64e)
    #2 0x564b4286f609 in leak_via_move /home/.../mqtt/leak_poc.cpp:17
    #3 0x564b4286fdf9 in main /home/.../leak_poc.cpp:32
    #4 0x7fac8ad65249 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: 100 byte(s) leaked in 1 allocation(s).
```

you can find the poc here https://gist.github.com/ErikDervishi03/7e56e7775b755a79392cf9e6cedc37dc


## Comment 4947605085

other (CONTRIBUTOR) · fpagliughi · 2026-07-11T16:25:14Z · https://github.com/eclipse-paho/paho.mqtt.cpp/issues/576#issuecomment-4947605085

Thanks for the report. I'll have a look.
