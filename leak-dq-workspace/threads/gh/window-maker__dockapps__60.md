# wmclockmon-0.8.1

- URL: https://github.com/window-maker/dockapps/issues/60
- Repo: window-maker/dockapps (language: C)
- State: open; created 2024-02-27T17:33:56Z; status ok; passes main

## Issue body

reporter (NONE) · svgol · 2024-02-27T17:33:56Z · https://github.com/window-maker/dockapps/issues/60

It is supplied with a configuration utility wmclockmon-config which crashes on pushing any of two buttons 'Save'.
The cause is it tries to free memory allocated in an external library, namely by gtk_entry_get_text().
The documentation of the function states that its return value

> A pointer to the contents of the widget as a string. This string points to internally allocated storage in the widget and must not be freed, modified or stored.

The attached patch fixes the problem

[fix_crashes_on_free.patch.tgz](https://github.com/window-maker/dockapps/files/14423790/fix_crashes_on_free.patch.tgz)



## Comment 1967406501

maintainer (MEMBER) · d-torrance · 2024-02-27T19:03:32Z · https://github.com/window-maker/dockapps/issues/60#issuecomment-1967406501

Thanks!  Would you be able to send this patch to `wmaker-dev@googlegroups.com`?

## Comment 1968082194

reporter (NONE) · svgol · 2024-02-28T02:36:30Z · https://github.com/window-maker/dockapps/issues/60#issuecomment-1968082194

Sent
