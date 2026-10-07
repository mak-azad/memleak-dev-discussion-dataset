# valgrind shows memry leak

- URL: https://github.com/ankurs/Hash-Table/issues/6
- Repo: ankurs/Hash-Table (language: C)
- State: open; created 2015-08-03T12:00:58Z; status ok; passes main

## Issue body

reporter (NONE) · abbycin · 2015-08-03T12:00:58Z · https://github.com/ankurs/Hash-Table/issues/6

 ~  cd mnt 
 ~/mnt  git clone https://github.com/ankurs/Hash-Table
Cloning into 'Hash-Table'...
remote: Counting objects: 43, done.
remote: Total 43 (delta 0), reused 0 (delta 0), pack-reused 43
Unpacking objects: 100% (43/43), done.
Checking connectivity... done.
 ~/mnt  cd Hash-Table 
 ~/mnt/Hash-Table   master  ls
debug.h  hashtable.c  hashtable.h  LICENSE  main.c  Makefile
 ~/mnt/Hash-Table   master  cc main.c hashtable.c 
 ~/mnt/Hash-Table   master  valgrind --leak-check=full --track-origins=yes ./a.out
//----------------------------------------------------------------------------------------------------------------------------------
==5243== LEAK SUMMARY:
==5243==    definitely lost: 52,712 bytes in 5 blocks
==5243==    indirectly lost: 295,546 bytes in 12,585 blocks
==5243==      possibly lost: 0 bytes in 0 blocks
==5243==    still reachable: 0 bytes in 0 blocks
==5243==         suppressed: 0 bytes in 0 blocks
==5243== 
==5243== For counts of detected and suppressed errors, rerun with: -v
==5243== ERROR SUMMARY: 3 errors from 3 contexts (suppressed: 0 from 0)
Key NOT found 3000
found 3000 keys
j -> 2999 
value is 3097


## Comment 5230317267

other (NONE) · webbrain-one · 2026-08-09T07:15:10Z · https://github.com/ankurs/Hash-Table/issues/6#issuecomment-5230317267

Hi! Thanks for reporting this. I’ve opened a pull request to address the memory leak: #7.

The fix adds proper cleanup logic to free all allocated hash table nodes and the table structure before the program exits, which resolves the `definitely lost` and `indirectly lost` blocks reported by Valgrind. Let me know if you have any questions or feedback! 🛠️✨
