# Memory leaks

- URL: https://github.com/BRCode4Fun/Python-Interpreter/issues/2
- Repo: BRCode4Fun/Python-Interpreter (language: C++)
- State: open; created 2025-02-26T22:42:40Z; status ok; passes main

## Issue body

reporter (NONE) · sten-code · 2025-02-26T22:42:40Z · https://github.com/BRCode4Fun/Python-Interpreter/issues/2

You probably already know this, but in the case that you don't. This program is full of memory leaks. I've looked through this code. Everytime you do a heap allocation you don't delete it anywhere. If you do a simple while loop:
```py
while True:
    print("Hello, World!")
```
This will eventually crash, because inside the visit nodes you return `new PyNone()` and never clean them up. Inside the while loop visit you evaluate the condition, but never delete the condition object.

## Comment 2795203812

maintainer (MEMBER) · tonisidneimc · 2025-04-10T21:26:25Z · https://github.com/BRCode4Fun/Python-Interpreter/issues/2#issuecomment-2795203812

I’ve just seen the data leak issue you reported two months ago, and I want to prioritize fixing it in the next release. While I’ve been preparing some new features, I recognize that this memory leak is more critical and will focus on resolving it first. I’ve been working alone on the project recently, so I apologize for the delay. Do you have any suggestions on how to approach this problem directly?

## Comment 2795593042

reporter (NONE) · sten-code · 2025-04-11T01:28:25Z · https://github.com/BRCode4Fun/Python-Interpreter/issues/2#issuecomment-2795593042

Fixing this would be really hard and time consuming, because these allocations happen everywhere throughout the project. 

I would recommend using `shared_ptr` and/or `unique_ptr`. It's basically a wrapper around a raw pointer, but it will clean itself up when no references exist to itself anymore. Use `unique_ptr` wherever you can because it's faster than `shared_ptr`.

If you don't want to use smart pointers, you could probably delete the memory from the destructors.

Feel free to ask anything if you need any help.

## Comment 4612821761

maintainer (MEMBER) · tonisidneimc · 2026-06-03T13:28:05Z · https://github.com/BRCode4Fun/Python-Interpreter/issues/2#issuecomment-4612821761

@sten-code  Thanks for the suggestions. They helped me work toward a fix.

I didn’t move every PyObject to shared_ptr, but I did tighten ownership: unique_ptr for scopes, manual refcounts on bindings, singletons for None/bools, and a small GC that deletes temporaries when their refcount hits zero. The while loop now releases the previous condition before re-evaluating it.

Your example (while True: print("Hello, World!")) should no longer grow memory without bound on current main. It’s still a simple refcount sweep, not full cycle GC, but the cases you reported are covered.

If anything still leaks on your build, tell me the commit and I’ll check. Thanks again.



