# Valgrind reported errors

- URL: https://github.com/OpenVisualCloud/SVT-VP9/issues/122
- Repo: OpenVisualCloud/SVT-VP9 (language: C)
- State: open; created 2020-07-10T16:29:10Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · intelmark · 2020-07-10T16:29:10Z · https://github.com/OpenVisualCloud/SVT-VP9/issues/122

When running valgrind to analyze another VP9 issue, a number of errors were reported.

 Conditional jump or move depends on uninitialised value(s)
Uninitialised value was created by a heap allocation

The command line I ran is:

_valgrind --log-file="valgrind_results.txt" --leak-check=full --show-leak-kinds=all --track-origins=yes --dsymutil=yes /repos/SVT-VP9/Bin/Debug/SvtVp9EncApp -i /testfiles/neighbor_360x360_420p_20frames.yuv -w 360 -h 360 -fps 50 -b output_valgrind.vp9 -asm 0
[valgrind_results.txt](https://github.com/OpenVisualCloud/SVT-VP9/files/4914206/valgrind_results.txt)
_


## Comment 2829199883

other (CONTRIBUTOR) · davidebeatrici · 2025-04-25T01:51:39Z · https://github.com/OpenVisualCloud/SVT-VP9/issues/122#issuecomment-2829199883

I'm unable to reproduce the issue, could you provide the test file?
