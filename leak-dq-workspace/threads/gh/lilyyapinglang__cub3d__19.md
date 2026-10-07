# memory leak

- URL: https://github.com/lilyyapinglang/cub3d/issues/19
- Repo: lilyyapinglang/cub3d (language: C)
- State: open; created 2026-07-18T15:09:30Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · lilyyapinglang · 2026-07-18T15:09:30Z · https://github.com/lilyyapinglang/cub3d/issues/19

```
NO ./texture/north64.xpm
SO ./texture/south64.xpm
WE ./texture/west64.xpm
EA ./texture/east64.xpm

FD ./texture/east64.xpm

F 220,100,0
C 225,30,0
        1111111111111111111111111
        1000000000110000000000001
        1011000001110000000000001
        1001000000000000000000001
111111111011000001110000000000001
100000000011000001110111111111111
11110111111111011100000010001
11110111111111011101010010001
11000000110101011100000010001
10000000000000001100000010001
10000000000000001101010010001
11000001110101011111011110N0111
11110111 1110101 101111010001
11111111 1111111 111111111111
```


```
 cub3d-github git:(main) ✗ valgrind --track-origins=yes --leak-check=full --show-leak-kinds=all ./cub3d ./maps/test_complex.cub
==892023== Memcheck, a memory error detector
==892023== Copyright (C) 2002-2024, and GNU GPL'd, by Julian Seward et al.
==892023== Using Valgrind-3.26.0 and LibVEX; rerun with -h for copyright info
==892023== Command: ./cub3d ./maps/test_complex.cub
==892023== 
0 
==892023== Conditional jump or move depends on uninitialised value(s)
==892023==    at 0x4017C5: parse_textures (process_cub_file.c:43)
==892023==    by 0x401125: line_treatement (parse_input.c:40)
==892023==    by 0x4011DA: dispatch_lines (parse_input.c:61)
==892023==    by 0x4013B3: parse_file (parse_input.c:90)
==892023==    by 0x400D1E: main (main.c:114)
==892023==  Uninitialised value was created by a stack allocation
==892023==    at 0x400CD3: main (main.c:109)
==892023== 
==892023== Conditional jump or move depends on uninitialised value(s)
==892023==    at 0x4842DF6: free (vg_replace_malloc.c:990)
==892023==    by 0x4017EF: parse_textures (process_cub_file.c:44)
==892023==    by 0x401125: line_treatement (parse_input.c:40)
==892023==    by 0x4011DA: dispatch_lines (parse_input.c:61)
==892023==    by 0x4013B3: parse_file (parse_input.c:90)
==892023==    by 0x400D1E: main (main.c:114)
==892023==  Uninitialised value was created by a stack allocation
==892023==    at 0x400CD3: main (main.c:109)
==892023== 
==892023== Invalid free() / delete / delete[] / realloc()
==892023==    at 0x4842E43: free (vg_replace_malloc.c:990)
==892023==    by 0x4017EF: parse_textures (process_cub_file.c:44)
==892023==    by 0x401125: line_treatement (parse_input.c:40)
==892023==    by 0x4011DA: dispatch_lines (parse_input.c:61)
==892023==    by 0x4013B3: parse_file (parse_input.c:90)
==892023==    by 0x400D1E: main (main.c:114)
==892023==  Address 0x40163d8 is in the Text segment of /usr/lib64/ld-linux-x86-64.so.2
==892023==    at 0x40163D8: handle_intel.constprop.0 (dl-cacheinfo.h:286)
==892023== 
 1 
 3 
 2 
Error
Invalid character in map
 ==892023== 
==892023== HEAP SUMMARY:
==892023==     in use at exit: 1,662 bytes in 47 blocks
==892023==   total heap usage: 218 allocs, 175 frees, 20,258 bytes allocated
==892023== 
==892023== 26 bytes in 1 blocks are indirectly lost in loss record 1 of 6
==892023==    at 0x483FB26: malloc (vg_replace_malloc.c:447)
==892023==    by 0x40448C: ft_calloc (in /home/ylang/code/cub3d-github/cub3d)
==892023==    by 0x402296: ft_line (utils.c:50)
==892023==    by 0x4024D9: get_next_line (utils.c:112)
==892023==    by 0x40102F: read_file (parse_input.c:25)
==892023==    by 0x401396: parse_file (parse_input.c:88)
==892023==    by 0x400D1E: main (main.c:114)
==892023== 
==892023== 90 bytes in 4 blocks are definitely lost in loss record 2 of 6
==892023==    at 0x483FB26: malloc (vg_replace_malloc.c:447)
==892023==    by 0x4044E3: ft_strdup (in /home/ylang/code/cub3d-github/cub3d)
==892023==    by 0x401777: parse_textures (process_cub_file.c:40)
==892023==    by 0x401125: line_treatement (parse_input.c:40)
==892023==    by 0x4011DA: dispatch_lines (parse_input.c:61)
==892023==    by 0x4013B3: parse_file (parse_input.c:90)
==892023==    by 0x400D1E: main (main.c:114)
==892023== 
==892023== 590 bytes in 22 blocks are indirectly lost in loss record 3 of 6
==892023==    at 0x483FB26: malloc (vg_replace_malloc.c:447)
==892023==    by 0x40448C: ft_calloc (in /home/ylang/code/cub3d-github/cub3d)
==892023==    by 0x402296: ft_line (utils.c:50)
==892023==    by 0x4024D9: get_next_line (utils.c:112)
==892023==    by 0x401069: read_file (parse_input.c:30)
==892023==    by 0x401396: parse_file (parse_input.c:88)
==892023==    by 0x400D1E: main (main.c:114)
==892023== 
==892023== 612 bytes in 18 blocks are indirectly lost in loss record 4 of 6
==892023==    at 0x483FB26: malloc (vg_replace_malloc.c:447)
==892023==    by 0x40448C: ft_calloc (in /home/ylang/code/cub3d-github/cub3d)
==892023==    by 0x401A8E: pad_line (generate_map.c:24)
==892023==    by 0x401BB6: create_map (generate_map.c:48)
==892023==    by 0x4013D6: parse_file (parse_input.c:95)
==892023==    by 0x400D1E: main (main.c:114)
==892023== 
==892023== 764 (152 direct, 612 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 6
==892023==    at 0x483FB26: malloc (vg_replace_malloc.c:447)
==892023==    by 0x40448C: ft_calloc (in /home/ylang/code/cub3d-github/cub3d)
==892023==    by 0x401B3A: create_map (generate_map.c:42)
==892023==    by 0x4013D6: parse_file (parse_input.c:95)
==892023==    by 0x400D1E: main (main.c:114)
==892023== 
==892023== 808 (192 direct, 616 indirect) bytes in 1 blocks are definitely lost in loss record 6 of 6
==892023==    at 0x483FB26: malloc (vg_replace_malloc.c:447)
==892023==    by 0x40448C: ft_calloc (in /home/ylang/code/cub3d-github/cub3d)
==892023==    by 0x401302: parse_file (parse_input.c:81)
==892023==    by 0x400D1E: main (main.c:114)
==892023== 
==892023== LEAK SUMMARY:
==892023==    definitely lost: 434 bytes in 6 blocks
==892023==    indirectly lost: 1,228 bytes in 41 blocks
==892023==      possibly lost: 0 bytes in 0 blocks
==892023==    still reachable: 0 bytes in 0 blocks
==892023==         suppressed: 0 bytes in 0 blocks
==892023== 
==892023== For lists of detected and suppressed errors, rerun with: -s
==892023== ERROR SUMMARY: 15 errors from 6 contexts (suppressed: 0 from 0)
➜  cub3d-github git:(main) ✗ 
```
