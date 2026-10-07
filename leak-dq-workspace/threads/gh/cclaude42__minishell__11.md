# Issue: Memory leak detected in minishell on exit

- URL: https://github.com/cclaude42/minishell/issues/11
- Repo: cclaude42/minishell (language: C)
- State: open; created 2025-01-25T22:50:09Z; status ok; passes main

## Issue body

reporter (NONE) · iaceene · 2025-01-25T22:50:09Z · https://github.com/cclaude42/minishell/issues/11

When running the minishell project and exiting the shell, Valgrind reports that there are 2 bytes still in use in 1 block of memory. No memory errors or leaks are detected, but a small amount of memory remains allocated when the program exits.

Expected Behavior:
The program should not leave any allocated memory when exiting. All memory should be properly freed to avoid memory leaks.

Steps to Reproduce:
Clone the minishell repository:

git clone https://github.com/42Project/minishell.git
cd minishell
Compile the project:

make
Run the shell with Valgrind to check for memory leaks:

![Image](https://github.com/user-attachments/assets/d44faed7-00c6-4cb4-aa80-b4ab089f14d1)

valgrind --leak-check=full ./minishell
In the minishell prompt, enter the following commands:

echo "the comment should be egnored!" #hi
exit
Observe the output, which shows that there is still 2 bytes of memory in use on exit.

Environment:
OS: (specify OS version)
Valgrind version: 3.18.1
Compiler: (specify compiler version, e.g., GCC, Clang)
minishell repository: (commit hash or branch, e.g., cclaude)
Logs:
==483002== Memcheck, a memory error detector
==483002== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==483002== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==483002== Command: ./minishell
==483002== 
😎 minishell ▸ echo "the comment should be egnored!" #hi
the comment should be egnored! #hi
😎 minishell ▸ exit
exit 💚
==483002== 
==483002== HEAP SUMMARY:
==483002==     in use at exit: 2 bytes in 1 blocks
==483002==   total heap usage: 283 allocs, 282 frees, 10,109 bytes allocated
==483002== 
==483002== LEAK SUMMARY:
==483002==    definitely lost: 0 bytes in 0 blocks
==483002==    indirectly lost: 0 bytes in 0 blocks
==483002==      possibly lost: 0 bytes in 0 blocks
==483002==    still reachable: 2 bytes in 1 blocks
==483002==         suppressed: 0 bytes in 0 blocks
==483002== Reachable blocks (those to which a pointer was found) are not shown.
==483002== To see them, rerun with: --leak-check=full --show-leak-kinds=all
==483002== 
==483002== For lists of detected and suppressed errors, rerun with: -s
==483002== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
Additional Context:
The program does not report any memory errors or leaks directly, but Valgrind indicates that there is still 2 bytes of memory that are not freed upon exit.
This could potentially be an issue in the cleanup code or during the process of terminating the shell session.
Possible Solution (if applicable):
Investigate the code responsible for freeing allocated memory when the program exits. Ensure that all dynamically allocated memory is freed properly to avoid any memory still being "reachable" when the program terminates.

## Comment 4192279334

other (NONE) · yabuawad · 2026-04-06T12:37:16Z · https://github.com/cclaude42/minishell/issues/11#issuecomment-4192279334




> When running the minishell project and exiting the shell, Valgrind reports that there are 2 bytes still in use in 1 block of memory. No memory errors or leaks are detected, but a small amount of memory remains allocated when the program exits.
> 
> Expected Behavior: The program should not leave any allocated memory when exiting. All memory should be properly freed to avoid memory leaks.
> 
> Steps to Reproduce: Clone the minishell repository:
> 
> git clone https://github.com/42Project/minishell.git cd minishell Compile the project:
> 
> make Run the shell with Valgrind to check for memory leaks:
> 
> ![Image](https://github.com/user-attachments/assets/d44faed7-00c6-4cb4-aa80-b4ab089f14d1)
> 
> valgrind --leak-check=full ./minishell In the minishell prompt, enter the following commands:
> 
> echo "the comment should be egnored!" #hi exit Observe the output, which shows that there is still 2 bytes of memory in use on exit.
> 
> Environment: OS: (specify OS version) Valgrind version: 3.18.1 Compiler: (specify compiler version, e.g., GCC, Clang) minishell repository: (commit hash or branch, e.g., cclaude) Logs: ==483002== Memcheck, a memory error detector ==483002== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al. ==483002== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info ==483002== Command: ./minishell ==483002== 😎 minishell ▸ echo "the comment should be egnored!" #hi the comment should be egnored! #hi 😎 minishell ▸ exit exit 💚 ==483002== ==483002== HEAP SUMMARY: ==483002== in use at exit: 2 bytes in 1 blocks ==483002== total heap usage: 283 allocs, 282 frees, 10,109 bytes allocated ==483002== ==483002== LEAK SUMMARY: ==483002== definitely lost: 0 bytes in 0 blocks ==483002== indirectly lost: 0 bytes in 0 blocks ==483002== possibly lost: 0 bytes in 0 blocks ==483002== still reachable: 2 bytes in 1 blocks ==483002== suppressed: 0 bytes in 0 blocks ==483002== Reachable blocks (those to which a pointer was found) are not shown. ==483002== To see them, rerun with: --leak-check=full --show-leak-kinds=all ==483002== ==483002== For lists of detected and suppressed errors, rerun with: -s ==483002== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0) Additional Context: The program does not report any memory errors or leaks directly, but Valgrind indicates that there is still 2 bytes of memory that are not freed upon exit. This could potentially be an issue in the cleanup code or during the process of terminating the shell session. Possible Solution (if applicable): Investigate the code responsible for freeing allocated memory when the program exits. Ensure that all dynamically allocated memory is freed properly to avoid any memory still being "reachable" when the program terminates.


if you use the flag --show-leak-kinds=all with valgrind you can spot the leak location :

2 bytes in 1 blocks are still reachable in loss record 1 of 1
==159338==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==159338==    by 0x407809: stock_trim (in /home/yabuawad/mini/minishell)
==159338==    by 0x407BCB: get_next_line (in /home/yabuawad/mini/minishell)
==159338==    by 0x40456D: parse (in /home/yabuawad/mini/minishell)
==159338==    by 0x403D89: main (in /home/yabuawad/mini/minishell)

if you look up the code inside the function get_next_line.c inside  
	if ((stock = stock_trim(stock)))
		return (-1);
stock_trim() returns a valid allocated string
So stock != NULL  when condition is true
You return -1 immediately
and you never free stock
you fix it like this
stock = stock_trim(stock);
if (!stock)
	return (-1);


