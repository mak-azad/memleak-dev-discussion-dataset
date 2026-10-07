# Socket leak

- URL: https://github.com/westes/flex/issues/705
- Repo: westes/flex (language: C)
- State: open; created 2025-05-17T10:17:24Z; status ok; passes offcwe

## Issue body

reporter (NONE) · doublex · 2025-05-17T10:17:24Z · https://github.com/westes/flex/issues/705

Include files are not closed in `yylex_destroy()`, e.g.:
````c
while (cfg_include_stack_ptr > 0) {
    --cfg_include_stack_ptr;
    fclose(cfg_include_stack[cfg_include_stack_ptr].fp);
}
````

And `cfg_include_stack_ptr = 0;` is not reseted in `yy_init_globals()`.

Best wishes!

