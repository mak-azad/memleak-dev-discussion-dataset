# Implement a smart pointer strategy for SUMO

- URL: https://github.com/eclipse-sumo/sumo/issues/6825
- Repo: eclipse-sumo/sumo (language: Python)
- State: open; created 2020-03-20T08:15:13Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · behrisch · 2020-03-20T08:15:13Z · https://github.com/eclipse-sumo/sumo/issues/6825

The idea is to do this step by step maybe first for the things where clang reports memleaks or where we already have our own reference counting (netedit, MSRoute) but we need to have a common picture first. This is my proposal (more or less copied from https://stackoverflow.com/questions/8338570/c11-replace-all-non-owning-raw-pointers-with-stdshared-ptr), please discuss:

- unique_ptrs are for sole ownership (this is probably the main replacement, objects which have members they own exclusively).
- shared_ptrs are for shared ownership (things where we did manual reference counting before).
- functions should take or return references instead of pointers whenever possible (only use a pointer when you transfer ownership or need the possibility to pass a nullptr)
- raw pointers should only be used to keep the interface simple and readable and when the receiving function can guarantee that it will not store the pointer as a member (or pass it to another function which might do so).


## Comment 601587338

reporter (CONTRIBUTOR) · behrisch · 2020-03-20T08:36:26Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601587338

@namdre @palvarezlopez @RobertHilbrich @schwamborn @lbieker @angelobanse Comments are welcome!

## Comment 601609035

other (CONTRIBUTOR) · namdre · 2020-03-20T09:36:26Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601609035

I agree that we should start by replacing our own reference counting with shared_ptrs.
Regarding replacement of other pointers, I'm less sure. We often return nullptrs to signify 'failure' which would be harder to do with references.

## Comment 601613393

maintainer (MEMBER) · palvarezlopez · 2020-03-20T09:48:06Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601613393

I agree also with the replacing **only** the reference counter.

## Comment 601648706

reporter (CONTRIBUTOR) · behrisch · 2020-03-20T11:17:24Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601648706

@namdre When we need a nullptr, even just to signify error, we can still use pointers (that was the remark in the brackets above).

## Comment 601649416

reporter (CONTRIBUTOR) · behrisch · 2020-03-20T11:19:11Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601649416

> I agree also with the replacing **only** the reference counter.

Why not the other pointers? My main reason for doing so is to make memory management easier. Don't you think it is worth it?

## Comment 601664527

other (CONTRIBUTOR) · namdre · 2020-03-20T12:00:27Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601664527

I'm not against replacing others. I'm just suggesting that we start with the pointers thathelp us the most. Regarding the possibility of replacing pointers with references in function returns I'm in favor of keeping pointers (though I'm not sure which of the above brackets are in favor of this).

## Comment 601921759

other (CONTRIBUTOR) · namdre · 2020-03-20T21:39:40Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601921759

it's hard to figure out what happens in [4bddcb8d3bf94142b933ba1491c01fef216736e3] due to the thousands of changed files but I noticed that there are unique_ptr things in the diff. 
Is your intention still to do shared_ptrs first or am I misunderstanding you?

To be honest, after seeing this in the diff:
```
    - myCrossings.push_back(c);
    + myCrossings.push_back(std::unique_ptr<Crossing>(c));
```

I'm a bit worried about the sentence   "_raw pointers should only be used to keep the interface simple and readable'_". 
Taken together, the diff and the sentence suggest that smart pointers may make the code less readable.


## Comment 601925406

reporter (CONTRIBUTOR) · behrisch · 2020-03-20T21:51:10Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-601925406

Sorry about that, it was not meant to be committed this way. Just a simple test balloon to see how unique_ptrs could work and at the same time fixing a memory leak. Yes, smart pointers may make the code less readable but they also convey more information and unfortunately make_unique is not available in c++11. The line you spotted is the only place where a unique_ptr is created and yes it is ugly. Maybe we add it as a point to the discussion :-). We can roll it back although I like the way it fixes the memory leak without the need to look every where for missing deletes.

## Comment 602445173

maintainer (MEMBER) · palvarezlopez · 2020-03-23T08:10:00Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-602445173

@behrisch It's true that smart pointer can solve memory leak problems. But the point is, that if there is memory leak problem, then there is an **implementation** problem. Therefore I'm against using them, because hide underlying problems.

## Comment 602449735

reporter (CONTRIBUTOR) · behrisch · 2020-03-23T08:21:37Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-602449735

I agree that a memory leak is an implementation problem but sometimes it is even a design problem because it is hard and sometimes needs a lot of changes to keep track of who is responsible for freeing allocated memory. Here smart pointers do not hide but solve the problem in an elegant way and make the code more readable. Just think of all the cases where we need to catch exceptions just to free memory and rethrow.
Also with more people using netedit to build their scenarios the topic of memory leaks gets more relevance because the GUI needs to do the proper cleanup and cannot rely on the OS to do that as the command line utilities.

## Comment 602560305

other (NONE) · obrusvit · 2020-03-23T12:27:26Z · https://github.com/eclipse-sumo/sumo/issues/6825#issuecomment-602560305

With the risk of suggesting something you already know, I highly recommend reading C++ Core Guidelines, maintained by the creator himself, Bjarne Stroustrup, and another influential guy from the C++ standard, Herb Sutter. https://github.com/isocpp/CppCoreGuidelines/blob/master/CppCoreGuidelines.md

Especially section "R: Resource management" might help you.

My take is this, smart pointers are intended to explicitly specify the ownership in the code. You should take smart pointers as parameters only if the function implements lifetime semantics of the object (R.30). Otherwise, accept raw pointer. You can always get raw pointer from smart pointer with the get method. Smart pointers are merely just handles of the object pointed to. 

I certainly disagree with the idea that smart pointers hide underlying design problems. The more you use `unique_ptr`, `shared_ptr` in combination with `make_unique` and `make_shared`, the better. 
