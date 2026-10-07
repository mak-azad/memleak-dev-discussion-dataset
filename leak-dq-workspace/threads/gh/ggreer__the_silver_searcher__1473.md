# Error: pointer being freed was not allocated when specifying bogus amount of context

- URL: https://github.com/ggreer/the_silver_searcher/issues/1473
- Repo: ggreer/the_silver_searcher (language: C)
- State: open; created 2022-01-03T15:35:11Z; status ok; passes main

## Issue body

reporter (NONE) · papandreou · 2022-01-03T15:35:11Z · https://github.com/ggreer/the_silver_searcher/issues/1473

I "accidentally" tried setting a negative amount of before context and got:

```
$ ag foo . -B-1
ag(31443,0x70000c51c000) malloc: *** error for object 0xf000000000000000: pointer being freed was not allocated
ag(31443,0x70000c393000) malloc: *** error for object 0x7274732065737527: pointer being freed was not allocated
ag(31443,0x70000c51c000) malloc: *** set a breakpoint in malloc_error_break to debug
ag(31443,0x70000c393000) malloc: *** set a breakpoint in malloc_error_break to debug
Abort trap: 6
```

I'm using ag version 2.2.0 on OSX 11.6.1 (20G224), installed using homebrew.
