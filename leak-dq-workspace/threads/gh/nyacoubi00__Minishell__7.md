# fd leak on heredoc

- URL: https://github.com/nyacoubi00/Minishell/issues/7
- Repo: nyacoubi00/Minishell (language: C)
- State: open; created 2024-06-03T11:56:26Z; status ok; passes offcwe

## Issue body

reporter (COLLABORATOR) · Isxfiane · 2024-06-03T11:56:26Z · https://github.com/nyacoubi00/Minishell/issues/7

```
eheheh << 0
0
eheheh: command not found
==268351== 
==268351== FILE DESCRIPTORS: 4 open (3 std) at exit.
==268351== Open file descriptor 3: .___tmpfile
==268351==    at 0x49DA53B: open (open64.c:41)
==268351==    by 0x404D59: set_stdin (exec_utils.c:102)
==268351==    by 0x40470D: last_cmd (handle_process.c:97)
==268351==    by 0x404339: cmd_loop (exec_cmd.c:47)
==268351==    by 0x406CA3: main (parsing.c:129)
```

