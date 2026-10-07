# Memory leak with console.mod and issues in core

- URL: https://github.com/eggheads/eggdrop/issues/1933
- Repo: eggheads/eggdrop (language: C)
- State: closed; created 2026-08-31T13:00:31Z; status ok; passes main

## Issue body

reporter (MEMBER) · michaelortmann · 2026-08-31T13:00:31Z · https://github.com/eggheads/eggdrop/issues/1933

```
.handle foo
.reload
.store
```

```
==301878==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 32 byte(s) in 1 object(s) allocated from:
    #0 0x7f1916d2c0c1 in malloc (/usr/lib/libasan.so.8+0x12c0c1) (BuildId: b8a4241051a1621937fdc46e867ba7ecb56d96ea)
    #1 0x55fa1f217ffb in n_malloc /home/michael/projects/eggdrop/src/mem.c:341
    #2 0x55fa1f2b9ee5 in _user_malloc /home/michael/projects/eggdrop/src/userrec.c:58
    #3 0x7f19149dbd60 in console_store .././console.mod/console.c:317
    #4 0x55fa1f27bfb5 in builtin_dcc /home/michael/projects/eggdrop/src/tclhash.c:693
    #5 0x55fa1f251dda in tcl_call_stringproc_cd /home/michael/projects/eggdrop/src/tcl.c:340
    #6 0x7f1916a7b7e8 in TclNRRunCallbacks /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:4541
    #7 0x7f1916a7d973 in TclEvalEx /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:5409
    #8 0x7f1916a7e31a in Tcl_EvalEx /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:5075
    #9 0x7f1916a7e33a in Tcl_Eval /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:6001
    #10 0x7f1916a7e98f in Tcl_VarEvalVA /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:7001
    #11 0x7f1916a7ea71 in Tcl_VarEval /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:7033
    #12 0x55fa1f27c710 in trigger_bind /home/michael/projects/eggdrop/src/tclhash.c:745
    #13 0x55fa1f27dcf9 in check_tcl_bind /home/michael/projects/eggdrop/src/tclhash.c:941
    #14 0x55fa1f27e559 in check_tcl_dcc /home/michael/projects/eggdrop/src/tclhash.c:973
    #15 0x55fa1f1bf248 in dcc_chat /home/michael/projects/eggdrop/src/dcc.c:1102
    #16 0x55fa1f213a6d in mainloop main.c:803
    #17 0x55fa1f217f16 in main main.c:1234
    #18 0x7f1915627780  (/usr/lib/libc.so.6+0x27780) (BuildId: 503200d7fda94a5dc6058d7e0694e5d1dcb2e372)
    #19 0x7f19156278b8 in __libc_start_main (/usr/lib/libc.so.6+0x278b8) (BuildId: 503200d7fda94a5dc6058d7e0694e5d1dcb2e372)
    #20 0x55fa1f128554 in _start (/home/michael/eggdrop/eggdrop-1.10.2+0x27b554) (BuildId: 53a21df18bc1eab4c18d6e9ed8d33d822b0c246b)

Indirect leak of 9 byte(s) in 1 object(s) allocated from:
    #0 0x7f1916d2c0c1 in malloc (/usr/lib/libasan.so.8+0x12c0c1) (BuildId: b8a4241051a1621937fdc46e867ba7ecb56d96ea)
    #1 0x55fa1f217ffb in n_malloc /home/michael/projects/eggdrop/src/mem.c:341
    #2 0x55fa1f2b9ee5 in _user_malloc /home/michael/projects/eggdrop/src/userrec.c:58
    #3 0x7f19149dc126 in console_store .././console.mod/console.c:322
    #4 0x55fa1f27bfb5 in builtin_dcc /home/michael/projects/eggdrop/src/tclhash.c:693
    #5 0x55fa1f251dda in tcl_call_stringproc_cd /home/michael/projects/eggdrop/src/tcl.c:340
    #6 0x7f1916a7b7e8 in TclNRRunCallbacks /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:4541
    #7 0x7f1916a7d973 in TclEvalEx /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:5409
    #8 0x7f1916a7e31a in Tcl_EvalEx /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:5075
    #9 0x7f1916a7e33a in Tcl_Eval /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:6001
    #10 0x7f1916a7e98f in Tcl_VarEvalVA /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:7001
    #11 0x7f1916a7ea71 in Tcl_VarEval /usr/src/debug/tcl/tcl8.6.16/generic/tclBasic.c:7033
    #12 0x55fa1f27c710 in trigger_bind /home/michael/projects/eggdrop/src/tclhash.c:745
    #13 0x55fa1f27dcf9 in check_tcl_bind /home/michael/projects/eggdrop/src/tclhash.c:941
    #14 0x55fa1f27e559 in check_tcl_dcc /home/michael/projects/eggdrop/src/tclhash.c:973
    #15 0x55fa1f1bf248 in dcc_chat /home/michael/projects/eggdrop/src/dcc.c:1102
    #16 0x55fa1f213a6d in mainloop main.c:803
    #17 0x55fa1f217f16 in main main.c:1234
    #18 0x7f1915627780  (/usr/lib/libc.so.6+0x27780) (BuildId: 503200d7fda94a5dc6058d7e0694e5d1dcb2e372)
    #19 0x7f19156278b8 in __libc_start_main (/usr/lib/libc.so.6+0x278b8) (BuildId: 503200d7fda94a5dc6058d7e0694e5d1dcb2e372)
    #20 0x55fa1f128554 in _start (/home/michael/eggdrop/eggdrop-1.10.2+0x27b554) (BuildId: 53a21df18bc1eab4c18d6e9ed8d33d822b0c246b)

SUMMARY: AddressSanitizer: 41 byte(s) leaked in 2 allocation(s).
```

after `.handle` and `.reload` `dcc[idx].user` becomes `NULL`, so `get_user(&USERENTRY_CONSOLE, u)` becomes `NULL`, a new struct is allocated and the old one rots away, see also:
https://github.com/eggheads/eggdrop/blob/3e2e2877a1d3df51d905904f64367d21d8f85e00/src/mod/console.mod/console.c#L305-L310
Yet, i dont know, if this is an error in `reload()` after a handle change via `.handle`  or in console.mod.




## Comment 5485189295

reporter (MEMBER) · michaelortmann · 2026-08-31T21:53:38Z · https://github.com/eggheads/eggdrop/issues/1933#issuecomment-5485189295

when the `dcc[idx].user` link is lost, checks for `!u` act like an emergency break, so eggdrop wont crash easy on it, but core stuff is broken, stuff related to `dcc[idx].user` stops working, most harmless example is `.info`.

## Comment 5485693897

reporter (MEMBER) · michaelortmann · 2026-08-31T22:35:30Z · https://github.com/eggheads/eggdrop/issues/1933#issuecomment-5485693897

we need a design decision. changing a handle (esp. of a user logged into the bots partyline) and then reloading the userfile (with only the old handle in it) , what exactly is expected to happen in that case? like, should we boot the (ghost-)user?
