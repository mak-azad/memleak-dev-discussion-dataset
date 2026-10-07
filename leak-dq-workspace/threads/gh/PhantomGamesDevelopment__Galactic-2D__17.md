# Tests Needed: PThread_ContinualThread Deletion

- URL: https://github.com/PhantomGamesDevelopment/Galactic-2D/issues/17
- Repo: PhantomGamesDevelopment/Galactic-2D (language: C)
- State: open; created 2014-08-26T01:20:10Z; status ok; passes offcwe

## Issue body

reporter (NONE) · Phantom139 · 2014-08-26T01:20:10Z · https://github.com/PhantomGamesDevelopment/Galactic-2D/issues/17

As noted with a lovely 4 line block comment in pContinualThread.cpp, we have a potential major issue here when a thread instance is deleted. Since the threading system itself by definition must also have multi-thread support, it is entirely possible that the instance of "this", may be deleted before a call to delete() is actually done, which would lead to access violation crashes.

Now, the notion of checking the this pointer itself, seems to be something that would be valid, however most people think it violates some silly "standard". I honestly have to disagree here since writing safe code has the precedence. However, I'm opening this issue to have a full test of the module to ensure this block of code behaves as intended.

``` C++
                    if(this != NULL) {
                        SendToHell(this);
                    }
                    else {
                        GC_Error("PContinualThread::kill(): Thread kill exception leak blocked...");
                        return false;
                    }
```


## Comment 97819400

reporter (NONE) · Phantom139 · 2015-04-30T14:32:35Z · https://github.com/PhantomGamesDevelopment/Galactic-2D/issues/17#issuecomment-97819400

Some investigations into the manner suggests that the notion of testing the "this" pointer is perfectly safe in this case and it should safeguard the potential crashes. 

I'll leave the investigation label on this as we'll need to get a good test of this before I'll close the issue and that'll require platform support for a PThread platform (Linux, Mac, Etc).

