# Task 5: Debugging and Memory Investigation

- URL: https://github.com/cablexd/COS214-Prac4/issues/5
- Repo: cablexd/COS214-Prac4 (language: C++)
- State: open; created 2026-09-01T20:16:35Z; status ok; passes main

## Issue body

reporter (OWNER) · cablexd · 2026-09-01T20:16:35Z · https://github.com/cablexd/COS214-Prac4/issues/5

```
Use the debugging tools introduced in the module as part of development, not only after the program is
finished.
Your PDF must contain a short engineering investigation that includes:
• evidence of using GDB on a meaningful part of your program, including breakpoints/stepping and
inspection of relevant program state;
• one genuine bug encountered during development, with its symptom, cause, debugging evidence and
correction; and
• Valgrind evidence for the final application.
The final implementation must not contain definitely-lost memory originating from your own code.
A typical Valgrind command is:
valgrind --leak-check=full --show-leak-kinds=all ./taskforge
```
