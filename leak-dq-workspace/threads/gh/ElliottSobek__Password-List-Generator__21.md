# Memory Leak on Tearing Down PThreads

- URL: https://github.com/ElliottSobek/Password-List-Generator/issues/21
- Repo: ElliottSobek/Password-List-Generator (language: C)
- State: open; created 2017-11-10T09:25:45Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · ElliottSobek · 2017-11-10T09:25:45Z · https://github.com/ElliottSobek/Password-List-Generator/issues/21

When canceling the threads and trying to join them back there is a memory leak in the cancel phase.
