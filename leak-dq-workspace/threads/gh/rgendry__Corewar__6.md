# valgrind

- URL: https://github.com/rgendry/Corewar/issues/6
- Repo: rgendry/Corewar (language: C)
- State: open; created 2020-01-21T16:48:50Z; status ok; passes main

## Issue body

reporter (COLLABORATOR) · sergejij · 2020-01-21T16:48:50Z · https://github.com/rgendry/Corewar/issues/6

#!/bin/bash

ASM="./asm"

for S_FILE in $( find ${1} -type f -name "*.s" ) ; do
  (valgrind ${ASM} ${S_FILE})

# echo `egrep "definitely lost:$" out`
done

