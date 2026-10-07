# Memory leaks

- URL: https://github.com/awmc000/readability/issues/1
- Repo: awmc000/readability (language: C)
- State: open; created 2023-08-25T05:13:55Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · awmc000 · 2023-08-25T05:13:55Z · https://github.com/awmc000/readability/issues/1

There are memory leaks in the program. In particular it appears that line buffers and words in word lists (represented by hash tables) are not being freed. I have fixed a couple of the leaks but most including the biggest remain. When testing I use a single line of text with 5 words, the minimum data for a readability score.
Note: 5,742 blocks are lost in the biggest leak. This is the exact number of proper nouns on the current list.


Here is the section of the report on the most egregious leak:
```
==311743== 40,095 bytes in 5,742 blocks are definitely lost in loss record 5 of 5
==311743==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==311743==    by 0x10994C: hashtable_load_words_from_file (hash_table.c:169)
==311743==    by 0x10A0E5: get_table_from_list_file (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x10A22C: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
```


Here is the full report:
```
==311743== Memcheck, a memory error detector
==311743== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==311743== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==311743== Command: ./readability testdata/oneline
==311743== 
testdata/oneline
lists/dale-expanded loaded successfully.
lists/proper-nouns loaded successfully.
==311743== Conditional jump or move depends on uninitialised value(s)
==311743==    at 0x48FB18B: getdelim (iogetdelim.c:59)
==311743==    by 0x10A3B4: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== Conditional jump or move depends on uninitialised value(s)
==311743==    at 0x109BB5: hashtable_delete (hash_table.c:232)
==311743==    by 0x10A3D6: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== Use of uninitialised value of size 8
==311743==    at 0x109B6E: hashtable_delete (hash_table.c:234)
==311743==    by 0x10A3D6: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== Use of uninitialised value of size 8
==311743==    at 0x109B88: hashtable_delete (hash_table.c:236)
==311743==    by 0x10A3D6: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
Freed 14921 strings from a ht with 0 elemsand total size 29842.
==311743== Conditional jump or move depends on uninitialised value(s)
==311743==    at 0x109BB5: hashtable_delete (hash_table.c:232)
==311743==    by 0x10A3E2: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
Freed 0 strings from a ht with 5742 elemsand total size 11484.
Dale-Chall score of 0.25
Breakdown: 0 hard of 5 words, 1 sentences.
 avg.  5 words per sentence. 0.00% difficult words.
Easily understood by an average student in 4th grade or lower
Computed score in 228.7554 ms.
==311743== 
==311743== HEAP SUMMARY:
==311743==     in use at exit: 41,335 bytes in 5,746 blocks
==311743==   total heap usage: 20,793 allocs, 15,047 frees, 1,017,780 bytes allocated
==311743== 
==311743== 256 bytes in 1 blocks are definitely lost in loss record 1 of 5
==311743==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==311743==    by 0x10A1CA: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== 256 bytes in 1 blocks are definitely lost in loss record 2 of 5
==311743==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==311743==    by 0x10986C: hashtable_load_words_from_file (hash_table.c:137)
==311743==    by 0x10A0E5: get_table_from_list_file (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x10A214: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== 256 bytes in 1 blocks are definitely lost in loss record 3 of 5
==311743==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==311743==    by 0x10986C: hashtable_load_words_from_file (hash_table.c:137)
==311743==    by 0x10A0E5: get_table_from_list_file (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x10A22C: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== 40,095 bytes in 5,742 blocks are definitely lost in loss record 5 of 5
==311743==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==311743==    by 0x10994C: hashtable_load_words_from_file (hash_table.c:169)
==311743==    by 0x10A0E5: get_table_from_list_file (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x10A22C: assess_readability (in /home/alex/Programming/C/readability/readability)
==311743==    by 0x109421: main (main.c:20)
==311743== 
==311743== LEAK SUMMARY:
==311743==    definitely lost: 40,863 bytes in 5,745 blocks
==311743==    indirectly lost: 0 bytes in 0 blocks
==311743==      possibly lost: 0 bytes in 0 blocks
==311743==    still reachable: 472 bytes in 1 blocks
==311743==         suppressed: 0 bytes in 0 blocks
==311743== Reachable blocks (those to which a pointer was found) are not shown.
==311743== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==311743== 
==311743== Use --track-origins=yes to see where uninitialised values come from
==311743== For lists of detected and suppressed errors, rerun with: -s
==311743== ERROR SUMMARY: 74612 errors from 9 contexts (suppressed: 0 from 0)
```

## Comment 1693628690

reporter (OWNER) · awmc000 · 2023-08-25T16:33:38Z · https://github.com/awmc000/readability/issues/1#issuecomment-1693628690

Regarding the biggest leak:
I call the function to empty out that hash table:
```
    hashtable_delete(proper_nouns);
```
But it doesn't seem to do anything.
```c
void hashtable_delete(struct hash_table *ht)
{
    int freed = 0;
    for (unsigned int i; i < ht->array_size; i++)
    {
        if (ht->strings[i] != NULL)
        {
            free(ht->strings[i]);
            ht->array_elems--;
            freed++;
        }
    }
    printf("Freed %d strings from a ht with %d elems"
        "and total size %d.\n", freed,
        ht->array_elems, ht->array_size);
}
```

Here is the print from that particular hash table.

```
Freed 0 strings from a ht with 5742 elems and total size 11484.
```
It works for the other hash table!

```
Freed 14921 strings from a ht with 0 elems [remaining] and total size 29842.
```

## Comment 1693760369

reporter (OWNER) · awmc000 · 2023-08-25T18:16:51Z · https://github.com/awmc000/readability/issues/1#issuecomment-1693760369

Fixed the biggest leak. `hashtable_delete` had an uninitialized counter `i`. 

```
==2004179== Memcheck, a memory error detector
==2004179== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==2004179== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==2004179== Command: ./readability testdata/oneline
==2004179== 
testdata/oneline
lists/dale-expanded loaded successfully.
lists/proper-nouns loaded successfully.
==2004179== Conditional jump or move depends on uninitialised value(s)
==2004179==    at 0x48FB18B: getdelim (iogetdelim.c:59)
==2004179==    by 0x10A3CB: assess_readability (in /home/alex/Programming/C/readability/readability)
==2004179==    by 0x109421: main (main.c:20)
==2004179== 
Freed 14921 strings from a ht with 0 elemsand total size 29842.
Freed 5742 strings from a ht with 0 elemsand total size 11484.
Dale-Chall score of 0.25
Breakdown: 0 hard of 5 words, 1 sentences.
 avg.  5 words per sentence. 0.00% difficult words.
Easily understood by an average student in 4th grade or lower
Computed score in 212.8100 ms.
==2004179== 
==2004179== HEAP SUMMARY:
==2004179==     in use at exit: 1,240 bytes in 4 blocks
==2004179==   total heap usage: 20,793 allocs, 20,789 frees, 1,017,780 bytes allocated
==2004179== 
==2004179== 256 bytes in 1 blocks are definitely lost in loss record 1 of 4
==2004179==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==2004179==    by 0x10A1E1: assess_readability (in /home/alex/Programming/C/readability/readability)
==2004179==    by 0x109421: main (main.c:20)
==2004179== 
==2004179== 256 bytes in 1 blocks are definitely lost in loss record 2 of 4
==2004179==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==2004179==    by 0x10986C: hashtable_load_words_from_file (hash_table.c:137)
==2004179==    by 0x10A0FC: get_table_from_list_file (in /home/alex/Programming/C/readability/readability)
==2004179==    by 0x10A22B: assess_readability (in /home/alex/Programming/C/readability/readability)
==2004179==    by 0x109421: main (main.c:20)
==2004179== 
==2004179== 256 bytes in 1 blocks are definitely lost in loss record 3 of 4
==2004179==    at 0x484DA83: calloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==2004179==    by 0x10986C: hashtable_load_words_from_file (hash_table.c:137)
==2004179==    by 0x10A0FC: get_table_from_list_file (in /home/alex/Programming/C/readability/readability)
==2004179==    by 0x10A243: assess_readability (in /home/alex/Programming/C/readability/readability)
==2004179==    by 0x109421: main (main.c:20)
==2004179== 
==2004179== LEAK SUMMARY:
==2004179==    definitely lost: 768 bytes in 3 blocks
==2004179==    indirectly lost: 0 bytes in 0 blocks
==2004179==      possibly lost: 0 bytes in 0 blocks
==2004179==    still reachable: 472 bytes in 1 blocks
==2004179==         suppressed: 0 bytes in 0 blocks
==2004179== Reachable blocks (those to which a pointer was found) are not shown.
==2004179== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==2004179== 
==2004179== Use --track-origins=yes to see where uninitialised values come from
==2004179== For lists of detected and suppressed errors, rerun with: -s
==2004179== ERROR SUMMARY: 4 errors from 4 contexts (suppressed: 0 from 0)

```
still need to fix line buffer leaks and possible uninitialized values elsewhere.
