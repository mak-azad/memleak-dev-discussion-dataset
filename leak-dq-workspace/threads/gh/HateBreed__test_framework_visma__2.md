# Memory leaks must be fixed

- URL: https://github.com/HateBreed/test_framework_visma/issues/2
- Repo: HateBreed/test_framework_visma (language: C)
- State: open; created 2016-01-23T13:06:04Z; status ok; passes main

## Issue body

reporter (OWNER) · HateBreed · 2016-01-23T13:06:04Z · https://github.com/HateBreed/test_framework_visma/issues/2

There are memory leaks. Some might be because of agile coding and hurry, others may be false positives reported by valgrind because glib utilizes memory slicing not well understood by valgrind.

