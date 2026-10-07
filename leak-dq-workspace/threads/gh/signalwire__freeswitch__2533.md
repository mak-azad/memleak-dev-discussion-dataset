# switch_core_speech_open memory leak when speech_open return false

- URL: https://github.com/signalwire/freeswitch/issues/2533
- Repo: signalwire/freeswitch (language: C)
- State: open; created 2024-07-17T03:49:25Z; status ok; passes offcwe

## Issue body

reporter (NONE) · MasonLuo918 · 2024-07-17T03:49:25Z · https://github.com/signalwire/freeswitch/issues/2533

**Describe the bug**

1. The switch_core_speech_open function, regardless of the request condition, will always create a memory pool, when use speak function.
![image](https://github.com/user-attachments/assets/7b7a51a8-5037-4f68-82d4-6b6638c1588d)
2. The switch_core_speech_close function will destroy then memory pool when return normal.
![image](https://github.com/user-attachments/assets/c693bbe9-f9d3-447c-937b-aabc345bc5ef)
3. But when switch_core_speech_open return false, the code will never reach the switch_core_speech_close method
![image](https://github.com/user-attachments/assets/a71255ba-ebad-4a73-88d4-119b93126b62)

When the custom module's speech_open method returns false, the memory pool is never released.

**To Reproduce**

Write a speech_interface, speech_open alway return false.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Package version or git hash**
 - Version [1.10.7]


