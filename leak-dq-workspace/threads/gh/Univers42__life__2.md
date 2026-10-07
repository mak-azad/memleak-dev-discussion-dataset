# grid_alloc overwrites teh three grid pointers unconditionally

- URL: https://github.com/Univers42/life/issues/2
- Repo: Univers42/life (language: C)
- State: open; created 2026-09-15T13:39:20Z; status ok; passes main

## Issue body

reporter (MEMBER) · LESdylan · 2026-09-15T13:39:20Z · https://github.com/Univers42/life/issues/2

```bash

╭─ life develop took 3.3s
╰─ ❯ ./life random=8x8:50 --random=9x9:50
life: error: cannot read config file
╭─ life develop ✘1
╰─ ❯ ./life co./life configs/glider.cfg --random=9x9:50 
╭─ life develop took 7.0s
╰─ ❯ make     make                                                                                                                                                                                                        15:36
cc -g3 -fsanitize=address,undefined \
   -Iincludes -Ilibft/includes -Iminilibx \
   srcs/*.c libft/libft.a \
   -Lminilibx -lmlx -lXext -lX11 -lbsd -lm \
   -o life_debug
make: Nothing to be done for 'all'.
╭─ life develop
╰─ ❯ ( unset D^Cunset DISPLAY; ASAN_OPTIONS=detect_leaks=1 ./life_debug --random=8x8:50 --random=9x9:50 )                                                                                                                 15:37
╭─ life develop ✘130
╰─ ❯ ( unset D( unset DISPLAY; ASAN_OPTIONS=detect_leaks=1 ./life_debug --random=8x8:50 --random=9x9:50 )                                                                                                                 15:37
life: error: mlx_init failed

=================================================================
==642119==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 64 byte(s) in 1 object(s) allocated from:
    #0 0x49a4cd in malloc (/home/dlesieur/Documents/life/life_debug+0x49a4cd)
    #1 0x4db5a4 in ft_calloc (/home/dlesieur/Documents/life/life_debug+0x4db5a4)
    #2 0x4cc2d7 in grid_alloc /home/dlesieur/Documents/life/srcs/grid_alloc.c:20:15
    #3 0x4d5c3c in parse_random /home/dlesieur/Documents/life/srcs/parse_random.c:57:2
    #4 0x4d2a1a in apply_flag /home/dlesieur/Documents/life/srcs/parse_args.c:44:3
    #5 0x4d22bf in parse_args /home/dlesieur/Documents/life/srcs/parse_args.c:63:4
    #6 0x4d1801 in main /home/dlesieur/Documents/life/srcs/main.c:40:2
    #7 0x7f4b6b7b0d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 64 byte(s) in 1 object(s) allocated from:
    #0 0x49a4cd in malloc (/home/dlesieur/Documents/life/life_debug+0x49a4cd)
    #1 0x4db5a4 in ft_calloc (/home/dlesieur/Documents/life/life_debug+0x4db5a4)
    #2 0x4cc3e3 in grid_alloc /home/dlesieur/Documents/life/srcs/grid_alloc.c:21:18
    #3 0x4d5c3c in parse_random /home/dlesieur/Documents/life/srcs/parse_random.c:57:2
    #4 0x4d2a1a in apply_flag /home/dlesieur/Documents/life/srcs/parse_args.c:44:3
    #5 0x4d22bf in parse_args /home/dlesieur/Documents/life/srcs/parse_args.c:63:4
    #6 0x4d1801 in main /home/dlesieur/Documents/life/srcs/main.c:40:2
    #7 0x7f4b6b7b0d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

Direct leak of 64 byte(s) in 1 object(s) allocated from:
    #0 0x49a4cd in malloc (/home/dlesieur/Documents/life/life_debug+0x49a4cd)
    #1 0x4db5a4 in ft_calloc (/home/dlesieur/Documents/life/life_debug+0x4db5a4)
    #2 0x4cc1ec in grid_alloc /home/dlesieur/Documents/life/srcs/grid_alloc.c:19:16
    #3 0x4d5c3c in parse_random /home/dlesieur/Documents/life/srcs/parse_random.c:57:2
    #4 0x4d2a1a in apply_flag /home/dlesieur/Documents/life/srcs/parse_args.c:44:3
    #5 0x4d22bf in parse_args /home/dlesieur/Documents/life/srcs/parse_args.c:63:4
    #6 0x4d1801 in main /home/dlesieur/Documents/life/srcs/main.c:40:2
    #7 0x7f4b6b7b0d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16

SUMMARY: AddressSanitizer: 192 byte(s) leaked in 3 allocation(s).
╭─ life develop* ✘1

```
