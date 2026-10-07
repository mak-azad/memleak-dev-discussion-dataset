# [ada, oldC]  setjmp/longjmp related memory leaks

- URL: https://github.com/universal-ctags/ctags/issues/90
- Repo: universal-ctags/ctags (language: C)
- State: open; created 2014-10-16T03:33:38Z; status ok; passes offcwe

## Issue body

reporter (MEMBER) · masatake · 2014-10-16T03:33:38Z · https://github.com/universal-ctags/ctags/issues/90

I found setjmp/longjmp are used widely in parsers.
valgrind reports the memory leaks related to them.
I guess longjmp is trigged when reading unexpected EOF.
Incomplete source code may make memory leaks.
These leaks will be a problem when ctags is used as a library in the future.

We have to introduce Trash based destructions in those parsers.


## Comment 59310448

reporter (MEMBER) · masatake · 2014-10-16T03:46:06Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59310448

$ grep -l longjmp *.c
ada.c
c.c
eiffel.c
flex.c
fortran.c
go.c
jscript.c
sql.c
tex.c
verilog.c
vhdl.c


## Comment 59310496

reporter (MEMBER) · masatake · 2014-10-16T03:47:05Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59310496

fuzz target should prepare randomly truncated input files.


## Comment 59310645

reporter (MEMBER) · masatake · 2014-10-16T03:49:43Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59310645

sql is fixed.


## Comment 59368538

maintainer (MEMBER) · b4n · 2014-10-16T14:22:02Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59368538

> I found setjmp/longjmp are used widely in parsers.
> […]
> I guess longjmp is trigged when reading unexpected EOF.

Yes, that's the general use case for it, although IIRC the C parser also uses it when detecting unbalanced preprocessor (though it may be specific to the version we have in Geany).

> These leaks will be a problem when ctags is used as a library in the future.

Indeed.

> We have to introduce Trash based destructions in those parsers.

What about trying to get rid of `longjump()` instead?  To be honest I hate it, and believe it makes the code almost impossible to really follow.  Getting rid of it should not be too hard in the general case (but quite tedious and probably error-prone), and would only require having proper return values in more places and checking for EOF.  FWIW, the non-trivial parsers that don't use `longjump()` work just fine.


## Comment 59396384

reporter (MEMBER) · masatake · 2014-10-16T17:12:06Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59396384

@b4n, agree with you.
Removing longjmp/setjmp will be not so hard but take amount of time.
Anyway I would like to fix vhdl and fortran because valgrind reports leaks.
 In addition I would like to polish my trash.[ch]  API.

BTW, can we reall free from setjmp/longjmp?
See #62. If we use timer to escape from infinite loop, we may want setjmp/longjmp anyway...


## Comment 59428701

other (CONTRIBUTOR) · vhda · 2014-10-16T20:53:37Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59428701

I don't have access to a computer at the moment. Can you confirm if verilog
parser is really making use of longjmp? I think it only includes it.


## Comment 59433867

maintainer (MEMBER) · ffes · 2014-10-16T21:30:02Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-59433867

@vhda Yes it does.

In vGetc() at lines 184 and 209:
`longjmp (Exception, (int) ExceptionEOF);`


## Comment 60032959

reporter (MEMBER) · masatake · 2014-10-22T03:45:30Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60032959

@vhda, I wonder whether you have an interest to introduce trashBox to vhdl.c.
Comparing to fortran.c vhdl is small. So I hope introducing trashBox is not so difficult.

What I did on sql.c:
87cfcbead6e8c8d1381e4ced1c42d5e282026263
and
8f5140aeebb5133eb6cbae1e4088396993c55cdd

may be a good place to start.
I will work on fortran.c first.


## Comment 60100279

maintainer (MEMBER) · dtikhonov · 2014-10-22T15:10:18Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60100279

Another approach is to have a memory pool associated with each parser invocation for a file, which is then destroyed when the file has been parsed.  This would, of course, be a much larger change.


## Comment 60104457

maintainer (MEMBER) · b4n · 2014-10-22T15:34:40Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60104457

> BTW, can we reall free from setjmp/longjmp?
> See #62. If we use timer to escape from infinite loop, we may want setjmp/longjmp anyway...

I'm not quite sure `longjmp()` (in parsers) would help here, as it still has to be triggered explicitly.
The only use I would see for it would be to `setjmp()` before calling in a parser, register a `SIGALARM` (or alike) handler that would `longjmp()` when triggered, call `alarm()`, and then run the parser.  Of course when the parser has finished you remove the handler.

However, I'm not quite sure it's the most sensible approach to escape infinite loops, maybe using a worker thread or forking might be better.


## Comment 60123919

reporter (MEMBER) · masatake · 2014-10-22T17:37:49Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60123919

In my understanding trashbox is similar to what @dtikhonov  wrote. 

@b4n, I'm not quite sure, too:)

We don't have to be afraid of larger change. Howerver, we have to make more than two larger changes;
1) sharing the code with geany, 2) running a parser in sandbox(this issue, using longjmp/setjmp or multi-threading). I wonder which one should be solved first...

I think we should solve the 1) first. 


## Comment 60155669

other (CONTRIBUTOR) · vhda · 2014-10-22T21:08:07Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60155669

@masatake I've just submitted a pull request for what you requested.
In the meanwhile I'm working on a similar change for verilog.


## Comment 60190187

maintainer (MEMBER) · dtikhonov · 2014-10-23T04:03:20Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60190187

> In my understanding trashbox is similar to what @dtikhonov wrote.

@masatake, no, a memory pool is simpler to use.  With the trashbox, you have to do two things:
1. allocate an object and
2. register it with the trashbox

With a memory pool, you'd allocate memory from a pool in a single function call.  The registration is unnecessary -- the memory is freed when the pool is destroyed.


## Comment 60389568

maintainer (MEMBER) · b4n · 2014-10-24T13:54:15Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60389568

> What I did [to port to TrashBox] on sql.c:
> 87cfcbe
> and
> 8f5140a

I must say that I don't like not explicitly freeing the memory, like [on line 983](/fishman/ctags/commit/87cfcbead6e8c8d1381e4ced1c42d5e282026263#diff-b828f3336f0d8cb668e3ed9c88e1ff24L984) (and may other places).  Couldn't there be a way to still free the memory explicitly when it's not needed?  Not doing so means the parser will use as much memory as it allocates as a whole, even if it doesn't actually need it all at the same time and the could possibly re-use the same memory.  I'm afraid this could explode memory consumption for large inputs and complex parsers.

If keeping the trash approach, something like `trashBoxFree(trash_box, ptr)`.

---

> Another approach is to have a memory pool associated with each parser invocation for a file […]

I think I like the memory pool approach better indeed, because it's simpler to use and a more common approach.


## Comment 60392104

reporter (MEMBER) · masatake · 2014-10-24T14:13:10Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60392104

@b4n, I have a question.
Could you tell me the relationship between the issue of trashBox you pointed out and memory pool.
In my understanding memory pool is more implicit approach.  About the issue, trashBox is better, I think because trashbox provides more explicit interface and trashbox can be nested; you can put a trashbox to another. In addition trashBoxTakeback prepares more control. 

Let's use both vhdl.c and sql.c as testbed for this issue.


## Comment 60393055

maintainer (MEMBER) · b4n · 2014-10-24T14:20:07Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60393055

> Could you tell me the relationship between the issue of trashBox you pointed out and memory pool.

None, sorry if it was confusing.  I just posted once answering two separated points.  Edited to add a ruler for clarity.

> In my understanding memory pool is more implicit approach. About the issue, trashBox is better, I think because trashbox provides more explicit interface and trashbox can be nested; you can put a trashbox to another.

I don't think it changes much in the feature side, apart that if the memory pool was global to the whole parser it could be used implicitly by e.g. #define-ing `pool_alloc_item` to `malloc` and `pool_free_item` to `free`.

Otherwise it's basically the same thing as if the TrashBox did the allocation itself, like this:

``` C
void *trashBoxAlloc(TrashBox *b, size_t size) {
    void *ptr = eMalloc(size);
    trashBoxPut(b, ptr, eFree);
    return ptr;
}
```


## Comment 60649721

reporter (MEMBER) · masatake · 2014-10-27T18:58:01Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60649721

Could you look at the latest comit?

I have not introduced things discussed here: trashBoxAlloc(== mempool) and trashBoxFree yet.
I introduce new interface between parser.c and each parser; I lift up setjmp and trashBoxNew code to parser.c from vhdl.c and sql.c.


## Comment 60820938

reporter (MEMBER) · masatake · 2014-10-28T19:57:55Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-60820938

I applied the new interface fortran.c. The memory leak reported by valgrind is gone. 
However, the interface doesn't well fit to fortran.c. jmp_buf passed from upper layer is
not used in fortran.c. fortran.c is assumed in design to manage jmp_buf in fortran.c.

The interface is not enough good but I pushed to our repository because it fixes the memory leak.

Feel free to try improving the interface; vhdl.c, sql.c and fortran.c can be used as target to evaluate your API.


## Comment 64133720

other (CONTRIBUTOR) · vhda · 2014-11-23T20:42:09Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-64133720

Created new PR #138 to remove trashbox use from SQL parser.
At the moment only the Fortran parser requires the existence of a garbage collector in ctags.


## Comment 457140015

reporter (MEMBER) · masatake · 2019-01-24T10:05:52Z · https://github.com/universal-ctags/ctags/issues/90#issuecomment-457140015

Ada still uses longjmp.

