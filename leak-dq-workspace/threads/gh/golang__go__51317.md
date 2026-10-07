# proposal: arena:  new package providing memory arenas

- URL: https://github.com/golang/go/issues/51317
- Repo: golang/go (language: Go)
- State: open; created 2022-02-22T16:11:10Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · danscales · 2022-02-22T16:11:10Z · https://github.com/golang/go/issues/51317

**Note, 2023-01-17**. This proposal is on hold indefinitely due to serious API concerns. The GOEXPERIMENT=arena code may be changed incompatibly or removed at any time, and we do not recommend its use in production.

- - -

# Proposal: arena: new package providing memory arenas

Author(s): Dan Scales (with input from many others)

Last updated: 2022-2-22

Discussion at https://golang.org/issue/51317

## Abstract

We propose implementing memory arenas for Go. An arena is a way to allocate a set of memory objects all from a contiguous region of memory, with the advantage that the allocation of the objects from the arena is typically more efficient than general memory allocation, and more importantly, the objects in the arena can all be freed at once with minimal memory management or garbage collection overhead. Arenas are not typically implemented for garbage-collected languages, because their operation for explicitly freeing the memory of the arena is not safe and so does not fit with the garbage collection semantics. However, our proposed implementation uses dynamic checks to ensure that an arena free operation is safe. The implementation guarantees that, if an arena free operation is unsafe, the program will be terminated before any incorrect behavior happens. We have implemented arenas at Google, and have shown savings of up to 15% in CPU and memory usage for a number of large applications, mainly due to reduction in garbage collection CPU time and heap memory usage.

## Background

Go is a garbage-collected language. Application code does not ever explicitly free allocated objects. The Go runtime automatically runs a garbage-collection algorithm that frees allocated objects some time after they become unreachable by the application code. The automatic memory management simplifies the writing of Go applications and ensures memory safety.

However, large Go applications spend a significant amount of CPU time doing garbage collection. In addition, the average heap size is often significantly larger than necessary, in order to reduce the frequency at which the garbage collector needs to run.

Non-garbage-collected languages also have significant memory allocation and de-allocation overhead. In order to deal with complex applications where objects have widely varying lifetimes, non-garbage-collected languages must have a general-purpose heap allocator. Because of the differing sizes and lifetimes of the objects being allocated, such an allocator must have fairly complex code for finding memory for a new object and dealing with memory fragmentation.

One approach to reducing the allocation overhead for non-garbage-collected languages is [region-based memory management](https://en.wikipedia.org/wiki/Region-based_memory_management), also known as arenas. The idea is that applications sometimes follow a pattern where a code segment allocates a large number of objects, manipulates those objects for a while, but then is completely done with those objects, and so frees all (or almost all) of the objects at roughly the same time. The code segment may be allocating all the objects to compute a result or provide a service, but has no need for any of the objects (except possibly a few result objects) when the computation is done.

In such cases, region-based memory allocation using an arena is useful.  The idea is to allocate a large region of memory called an arena at the beginning of the code segment.  The arena is typically a contiguous region, but may be extensible in large chunk sizes.  Then all the objects can be allocated very efficiently from the arena. Typically, the objects are just allocated consecutively in the arena.  Then at the end of the code segment, all of the allocated objects can be freed with very low overhead by just freeing the arena.  Any result object that is intended to be longer-lived and last past the end of the code segment should not be allocated from the arena or should be fully copied before the arena is freed.

Arenas have been found to be useful for a number of common programming patterns, and when applicable, can reduce memory management overhead in non-garbage collected languages.  For instance, for a server serving memory-heavy requests, each request is likely independent, so most or all of the objects allocated while serving a particular request can be freed when the request has been fulfilled.  Therefore, all the objects allocated during the request can be allocated in an arena, and then freed all at once at the completion of the request.

In a related vein, arenas have been useful for protocol buffer processing, especially when unmarshalling the wire format into the in-memory protocol message object. Unmarshalling a message's wire format to memory can create many large objects, strings, arrays, etc., because of the complexity of messages and the frequent nesting of sub-messages inside other messages.  A program may often unmarshal one or more messages, make use of the in-memory objects for a period of time, and then be done with those objects. In this case, all of the objects created while unmarshalling the message(s) can be allocated from an arena and freed all at once. The C++ protocol buffer documentation provides [an example of using arenas](https://developers.google.com/protocol-buffers/docs/reference/arenas). Arenas may similarly be useful for other kinds of protocol processing, such as decoding JSON.

We would like to get some of the benefits of arenas in the Go language.  In the next section, we propose a design of arenas that fits with the Go language and allows for significant performance benefits, while still ensuring memory safety.

Note that there are many applications where arenas will not be useful, including applications that don't do allocation of large amounts of data, and applications whose allocated objects have widely varying lifetimes that don't fit the arena allocation pattern. Arenas are intended as a targeted optimization for situations where object lifetimes are very clear.


## Proposal

We propose the addition of a new `arena` package to the Go standard library. The arena package will allow the allocation of any number of arenas. Objects of arbitrary type can be allocated from the memory of the arena, and an arena automatically grows in size as needed. When all objects in an arena are no longer in use, the arena can be explicitly freed to reclaim its memory efficiently without general garbage collection. We require that the implementation provide safety checks, such that, if an arena free operation is unsafe, the program will be terminated before any incorrect behavior happens.

For maximum flexibility, we would like the API to be able to allocate objects and slices of any type, including types that can be generated at run-time via reflection.

We propose the following API:

```go
package arena

type Arena struct {
	// contains filtered or unexported fields
}

// New allocates a new arena.
func New() *Arena

// Free frees the arena (and all objects allocated from the arena) so that
// memory backing the arena can be reused fairly quickly without garbage
// collection overhead.  Applications must not call any method on this
// arena after it has been freed.
func (a *Arena) Free()

// New allocates an object from arena a.  If the concrete type of objPtr is
// a pointer to a pointer to type T (**T), New allocates an object of type
// T and stores a pointer to the object in *objPtr.  The object must not
// be accessed after arena a is freed.
func (a *Arena) New(objPtr interface{})

// NewSlice allocates a slice from arena a.  If the concrete type of slicePtr
// is *[]T, NewSlice creates a slice of element type T with the specified
// capacity whose backing store is from the arena a and stores it in
// *slicePtr. The length of the slice is set to the capacity.  The slice must
// not be accessed after arena a is freed.
func (a *Arena) NewSlice(slicePtr interface{}, cap int)
```

The application can create an arbitrary number of arenas using `arena.New`, each with a different lifetime.  An object with a specified type can be allocated in a particular arena using `a.New`, where `a` is an arena.  Similarly, a slice with a specified element type and capacity can be allocated from an arena using `a.NewSlice`. Because the object and slice pointers are passed via an empty interface, any type can be allocated.  This includes types that are generated at run-time via the `reflect` library, since a `reflect.Value` can be converted easily to an empty interface.

The application explicitly frees an arena and all the objects allocated from the arena using `a.Free`. After this call, the application should not access the arena again or dereference a pointer to any object allocated from this arena. The implementation is required to cause a run-time erro and terminate the Go program if the application accesses any object whose memory has already been freed. The associated error message should indicate that the termination is due to access to an object in a freed arena. In addition, the implementation must cause a panic or terminate the Go program if `a.New` or `a.NewSlice` is called after `a.Free` is called.  `a.New` and `a.NewSlice` should also cause a panic if they are called with an argument which is not the correct form (`**T` for `a.New` and `*[]T` for `a.NewSlice`).

Here is some sample code as an example of arena usage:

```go
import (
	“arena”
	…
)

type T struct {
	val int
}

func main() {
	a := arena.New()
	var ptrT *T
	a.New(&ptrT)
	ptrT.val = 1

	var sliceT []T
	a.NewSlice(&sliceT, 100)
	sliceT[99] .val = 4

	a.Free()
}
```

There may be an implementation-defined limit, such that if the object or slice requested by calls to `a.New` or `a.NewSlice` is too large, the object cannot be allocated from the arena.  In this case, the object or slice is allocated from the heap. If there is such an implementation-defined limit, we may want to have a way to expose the limit.  We’ve listed it as  one of the possible metrics mentioned in the “Open Issues” section.  An alternate API would be to not allocate the object or slice if it is too large and instead leave the pointer arguments unchanged.  This alternate API seems like it would be more likely to lead to programming mistakes, where the pointer arguments are not properly checked before being accessed or copied elsewhere. 

For optimization purposes, the implementation is allowed to delay actually freeing an arena or its contents. If this optimization is used, the application is allowed to proceed normally if an object is accessed after the arena containing it is freed, as long as the memory of the object is still available and correct (i.e. there is no chance for incorrect behavior). In this case, the improper usage of `arena.Free` will not be detected, but the application will run correctly, and the improper usage may be detected during a different run.

The above four functions are the basic API, and may be sufficient for most cases. There are two other API calls related to strings that are fairly useful. Strings in Go are special, because they are similar to slices, but are read-only and must be initialized with their content as they are created. Therefore, the `NewSlice` call cannot be used for creating strings. `NewString` below allocates a string in the arena, initializes it with the contents of a byte slice, and returns the string header.

```go
// NewString allocates a new string in arena a which is a copy of b, and
// returns the new string.
func (a *Arena) NewString(b []byte) string
```

In addition, a common mistake with using arenas in Go is to use a string that was allocated from an arena in some global data structure, such as a cache, which that can lead to a run-time exception when the string is accessed after its arena is freed. This mistake is understandable, because strings are immutable and so often considered separate from memory allocation. To deal with the situation of a string whose allocation method is unknown, `HeapString` makes a copy of a string using heap memory only if the passed-in string (more correctly, its backing array of bytes) is allocated from an arena. If the string is already allocated from the heap, then it is returned unchanged. Therefore, the returned string is always usable for data structures that might outlast the current arenas.

```go
// HeapString returns a copy of the input string, and the returned copy
// is allocated from the heap, not from any arena. If s is already allocated
// from the heap, then the implementation may return exactly s.  This function
// is useful in some situations where the application code is unsure if s
// is allocated from an arena.
func HeapString(s string) string
```

Of course, this issue of mistakenly using an object from an arena in a global data structure may happen for other types besides strings, but strings are a very common case for being shared across data structures.

We describe an efficient implementation of this API (with safety checks) in the "Implementation" section. Note that the above arena API may be implemented without actually implementing arenas, but instead just using the standard Go memory allocation primitives. We may implement the API this way for compatibility on some architectures for which a true arena implementation (including safety checks) cannot be implemented efficiently.


## Rationale

There are a number of possible alternatives to the above API.  We discuss a few alternatives, partly as a way to justify our above choice of API.

### Removing Arena Free

One simple adjustment to the above API would be to eliminate the arena `Free` operation. In this case, an arena would be freed automatically only by the garbage collector, once there were no longer any pointers to the arena itself or to any objects contained inside the arena. The big problem with not having a `Free` operation is that arenas derive most of their performance benefit from more prompt reuse of memory. Though the allocation of objects in the arena would be slightly faster, memory usage would likely greatly increase, because these large arena objects could not be collected until the next garbage collection after they were no longer in use. This would be especially problematic, since the arenas are large chunks of memory that are often only partially full, hence increasing fragmentation. We did prototype this approach where arenas are not explicitly freed, and were not able to get a noticeable performance benefit for real applications. An explicit `Free` operation allows the memory of an arena to be reused almost immediately. In addition, if an application is able to use arenas for almost all of its allocations, then garbage collection may be mostly unneeded and therefore may be delayed for quite a long time.

### APIs that directly return the allocated objects/slices

An alternate API with similar functionality, but different feel, would replace `(*Arena).New` and `(*Arena).NewSlice` with the following:

```go
// New allocates an object of the given type from the arena and returns a
// pointer to that object.
func (a *Arena) New(typ reflect.Type) interface{}

// NewSlice allocates a slice of the given element type and capacity from the
// arena and returns the slice as an interface. The length of the slice is
// set to the capacity.
func (a *Arena) NewSlice(typ reflect.Type, cap int) interface{}
```

An example of usage would be:

```go
a := arena.New()
floatPtr := a.New(reflect.TypeOf(float64(0))).(*float64)
byteSlice := a.NewSlice(reflect.TypeOf(byte(0)), 100).([]byte)
```

This API potentially seems simpler, since it returns the allocated object or slice directly, rather than requiring that a pointer be passed in to indicate where the result should be stored. This allows convenient use of Go’s idiomatic short variable declaration, but does require type assertions to convert the return value to the correct type.  This alternate API specifies the types to be allocated using `reflect.Type`, rather than by passing in an interface value that contains a pointer to the required allocation type. For applications and libraries that already work on many different types and use reflection, specifying the type using `reflect.Type` may be convenient. However, for many applications, it may seem more convenient to just pass in a pointer to the type that is required.

There is an efficiency distinction in the `NewSlice` call with the two choices. In the `NewSlice` API described in the "Proposal" section, the slice header object is already allocated in the caller, and only the backing element array of the slice needs to be allocated. This may be all that is needed in many cases, and hence more efficient. In the new API in this section, the `Slice` call must allocate the slice object as well in order to return it in the interface, which causes extra heap or arena allocation when they are often not needed.

Another alternative for `a.New` is to pass in a pointer to type T and return a pointer to
type T (both as empty interfaces):

```go
// New, given that the concrete type of objPtr is a pointer to type T,
// allocates an object of type T from the arena a, and returns a pointer to the
// object.
func (a *Arena) New(objPtr interface{}) interface{}
```
An example use of this API call would be:  `intPtr := a.New((*int)(nil)).(*int)`.  Although this also allows the use of short variable declarations and doesn’t require the use of reflection, the rest of the usage is fairly clunky.

### Simple API using type parameterization (generics)

We could have an optional addition to the API that uses type parameterization to express the type to be allocated in a concise and direct way.  For example, we could have generic `NewOf` and `NewSliceOf` functions:

```go
// NewOf returns a pointer to an object of type T that is allocated from
// arena a.
func arena.NewOf[T any](a *Arena) *T
```

```go
// NewSliceOf returns a slice with element type T and capacity cap
// allocated from arena a
func arena.NewSliceOf[T any](a *Arena, cap int) []T
```

Then we could allocate objects from the arena via code such as:

```go
intPtr := arena.NewOf[int](a)
```

We don’t think these generic variants of the API can completely replace the suggested methods above, for two reasons.  First, the `NewOf` function can only allocate objects whose type is specified at compile-time.  So, it cannot satisfy our goal to support allocation of objects whose type is computed at run-time (typically via the `reflect` library).  Second, generics in Go are just arriving in Go 1.18, so we don’t want to force users to make use of generics before they are ready.

## Compatibility

Since this API is new, there is no issue with Go compatibility.

## Implementation

In order to fit with the Go language, we require that the semantics of arenas in Go be fully safe.  However, our proposed API has an explicit arena free operation, which could be used incorrectly.  The application may free an arena A while pointers to objects allocated from A are still available, and then sometime later attempt to access an object allocated from A.

Therefore, we require that any implementation of arenas must prevent improper accesses without causing any incorrect behavior or data corruption. Our current implementation of the API gives a memory fault (and terminates the Go program) if an object is ever accessed that has already been freed because of an arena free operation.

Our current implementation performs well and provides memory allocation and GC overhead savings on the Linux amd64 64-bit architecture for a number of large applications.  It is not clear if a similar approach can work for 32-bit architectures, where the address space is much more limited.

The basic ideas for the implementation are as follows:
 * Each arena `A` uses a distinct range in the 64-bit virtual address space
 * `A.Free` unmaps the virtual address range for arena `A`
 * The physical pages for the arena can then be reused by the operating system for other arenas.
 * If a pointer to an object in arena `A` still exists and is dereferenced, it will get a memory access fault, which will cause the Go program to terminate.  Because the implementation knows the address ranges of arenas, it can give an arena-specific error message during the termination.

So, we are ensuring safety by always using a new range of addresses for each arena, in order that we can always detect an improper access to an object that was allocated in a now-freed arena.

The actual implementation is slightly different from the ideas above, because arenas grow dynamically if needed. In our implementation, each arena starts as a large-size "chunk", and grows incrementally as needed by the addition of another chunk of the same size. The size of all chunks is chosen specifically to be 64 MB (megabytes) for the current Go runtime on 64-bit architectures, in order to make it possible to recycle heap meta-data efficiently with no memory leaks and to avoid fragmentation.

The address range of these chunks do not need to be contiguous.  Therefore, when we said above that each arena A uses a distinct range of addresses, we really meant that each chunk uses a distinct range of addresses.

Each chunk and all the objects that it contains fully participate in GC mark/sweep until the chunk is freed. In particular, as long as a chunk is part of an arena that has not been freed, it is reachable, and the garbage collector will follow all pointers for each object contained in the chunk. Pointers that refer to other objects contained in the chunk will be handled very efficiently, while pointers to objects outside the chunk will be followed and marked normally.

The implementation calls `SetFinalizer(A, f)` on each arena A as it is allocated, where `f` calls `A.Free`.  This ensures that an arena and the objects allocated from it will eventually be freed if there are no remaining references to the arena.  The intent though is that every arena should be explicitly freed before its pointer is dropped.

Because unmapping memory is relatively expensive, the implementation may continue to use a chunk for consecutively allocated/freed arenas until it is nearly full. When an arena is freed, all of its chunks that are filled up are immediately freed and unmapped. However, the remaining part of the current unfilled chunk may be used for the next arena that is allocated. This batching improves performance significantly.

Because of the large 64-bit address space, our prototype implementation has not required reusing the virtual addresses for any arena chunks, even for quite large and long-running applications. However, the virtual addresses of most chunks can eventually be reused, since there will almost always be no more reachable pointers to anywhere in the chunk. Since the garbage collector sees all reachable pointers, it can determine when an address range can be reused.

The implementation described above demonstrates that it is possible to implement the Arena API for 64-bit architectures with full safety, while still providing performance benefits. Many other implementations are possible, and some may be tuned for other types of usage. In particular, because of the 64 MB chunk size, the above implementation may not be useful for applications that need to create a large number of arenas that are live at the same time (possibly because of many concurrent threads). It is probably most appropriate that there should only be a few to 10's of arenas in use at any one time. Also, it is not intended that arenas be shared across goroutines. Each arena has a lock to protect against simultaneous allocations by multiple goroutines, but it would be very inefficient to actually use the same arena for multiple goroutines.  Of course, that would rarely make sense anyway, since the lifetimes of objects allocated in different goroutines are likely to be quite different.

## Open issues

Another possibility in the design space is to implement the API described in the "Proposal" section, but without the safety checks, or with an option to disable the safety checks. The idea here is that the performance savings from the use of arenas can be increased by doing an implementation that doesn't have safety guarantees. As compared to the implementation described above, we can avoid the mapping and unmapping overhead, and reuse the memory of an arena much more quickly (and without OS involvement) when it is freed. We have done a prototype of such an implementation, which we call "unsafe arenas". We have seen an additional 5-10% improvement in performance in some cases when using unsafe arenas rather than our safe arena implementation. However, we feel very strongly that arenas in Go need to be safe. We do not want the use of arenas to lead to memory bugs that may be very hard to detect and debug, and may silently lead to data corruption. We think that it is better to continue to optimize the implementation of safe arenas, rather than trying to support unsafe arenas.

It would be useful to have some run-time metrics associated with arenas.  The desired metrics will depend somewhat on the final API, so we have not yet tried to decide the exact metrics that will cover the application needs.  However, here are some metrics which might be useful:

 * the number of arena created and freed
 * the number of current arenas and the maximum number of arenas that have been active at one time
 * the total number of bytes allocated via arenas, and the average number of bytes allocated per arena
 * the (constant) limit on the largest-size object or slice that can be allocated from an arena

Another open issue is whether arenas can be used for allocating the elements of a map.  This is
possible, but it is not clear what a good API would be.  Also, there might be unusual cases if the arena used for the main map object is different from the arena used to allocate new elements of the map.   With generics arriving in Go 1.18, generic maps (or hash tables) can now be implemented in user libraries.  So, there could be a user-defined generic map implementation that allows optionally specifying an arena for use in allocating new elements.  This might be the best solution, since that would allow for greater flexibility than adjusting the semantics of the built-in `map` type.

## Protobuf unmarshalling overheads

As noted above, arenas are often quite useful for reducing the allocation and GC overhead associated with the objects that are created as a protobuf message is being unmarshaled. We have prototyped changes to the [protobuf package](https://pkg.go.dev/google.golang.org/protobuf) which allow for providing an arena as the allocation option for objects created during unmarshalling. This arrangement makes it quite easy to use arenas to reduce the allocation and GC overhead in applications that make heavy use of protobufs (especially unmarshalling of large protobufs). If the arena proposal is accepted and implemented in Go, then it would make sense to extend the protobuf package to provide such an arena allocation option.


## Comment 1048177275

other (NONE) · hherman1 · 2022-02-22T20:18:49Z · https://github.com/golang/go/issues/51317#issuecomment-1048177275

What is the reason to add this to the standard library as opposed to building a third party package?

## Comment 1048190367

other (NONE) · clausecker · 2022-02-22T20:36:29Z · https://github.com/golang/go/issues/51317#issuecomment-1048190367

Your specification says:

 > The application explicitly frees an arena and all the objects allocated from the arena using a.Free. After this call, the application should not access the arena again or dereference a pointer to any object allocated from this arena. The implementation is required to cause a run-time erro and terminate the Go program if the application accesses any object whose memory has already been freed.

If I read it correctly, this means that it is permitted to keep pointers into a released arena (i.e. stray pointers) as long as you do not explicitly dereference them.  However, this means that the compiler must now be careful not to dereference any pointer it knows not to be `nil` unless user code explicitly does so, lest it be a pointer into a released `arena`. This seems like it would significantly reduce the potential for optimisation as otherwise, the compiler seems to be allowed to perform such accesses, knowing that each reachable object can also be dereferenced safely.

If the rules were tightened to say that you have to erase all pointers into an `arena` before calling `Free`, not only would these optimisations be enabled, but there would also be a way to reclaim the address space occupied by the arena: the garbage collector could be programmed to check if any pointers into the arena address space remain and if there aren't any, it could allow the address space to be reclaimed.  If it finds a stray pointer, it could likewise abort the program in much the same manner as when you dereference a stray pointer.

Another benefit is that it's less likely to have tricky edge cases where stray pointers could remain in some data structures (e.g. as the result of some string manipulation or `append` operations which may only some times return a pointer to one of their arguments), causing them to be dereferenced later only under specific, hard to reconstruct circumstances.  By prohibiting the presence of any stray pointers after a call to `Free`, this kind of error would be much easier to find.

With this issue addressed, I'm very interested in this proposal.  It will be very useful for complex temporary data structures that need to be built step by step and deallocated all at once.

## Comment 1048202600

other (NONE) · quenbyako · 2022-02-22T20:54:06Z · https://github.com/golang/go/issues/51317#issuecomment-1048202600

@hherman1 as far as i understood this proposal, there are a lot of troubles for example in appending to slices, e.g. the code could be more readable if you just use `append`, without calling arena-specific methods.

Even though, the idea to manualy handle memory freeing sounds great for me, cause there are a lot of specific cases, when you don't want to hope on the garbage collector

## Comment 1048216229

other (NONE) · tarndt · 2022-02-22T21:12:30Z · https://github.com/golang/go/issues/51317#issuecomment-1048216229

I'd be curious to understand the problems that an arena solves that can't be solved by either using sync.Pool, allocating a slice of a given type (for example a binary tree allocating a slice of nodes), or a combination of both techniques. It seems to me that Go provides idiomatic ways of addressing at least the specific protobuf use-case mentioned here.

In addition to the above, doesn't the Go allocator already have sizes classes? If the proposal does proceed, I think we need to see a prototype outperform the runtimes allocator and is enough gain to justify the ecosystem complexity.

## Comment 1048267472

other (CONTRIBUTOR) · komuw · 2022-02-22T22:20:25Z · https://github.com/golang/go/issues/51317#issuecomment-1048267472

> We don’t think these generic variants of the API can completely replace ....

> First, the NewOf function can only allocate objects whose type is specified at compile-time. So, it cannot satisfy our goal to support allocation of objects whose type is computed at run-time (typically via the reflect library). 

What's the main usecase for wanting to allocate types created via reflect in arenas? Marshalling & unmarshall? 
Are those usecases compelling enough? Honest question.

> Second, generics in Go are just arriving in Go 1.18, so we don’t want to force users to make use of generics before they are ready.

Is there a hurry in adding arenas? It can always wait one or two release cycles before been added so that people are ready with generics. 
In other words, if hypothetically speaking, the arena-generics design was the better API; we shouldn't shelve it just because generics aren't ready yet. 




## Comment 1048278549

other (NONE) · frioux · 2022-02-22T22:37:33Z · https://github.com/golang/go/issues/51317#issuecomment-1048278549

This proposal sounds really good to me from a user's perspective, but one detail causes concern: wouldn't something like all code eventually end up needing arena support?  For example, imagine I have a web service where I want to allocate an arena for each web request.  This sounds like a great use case for this, but I'd need `encoding/json` to have an Arena mode, and maybe `text/template`/`html/template` to have Arena modes so their working sets can use the Arena.  Probably same for various clients (SQL, http, etc.)  Is that what you see as the path forward or am I missing something?

## Comment 1048301788

other (CONTRIBUTOR) · ianlancetaylor · 2022-02-22T23:16:29Z · https://github.com/golang/go/issues/51317#issuecomment-1048301788

@hherman1

> What is the reason to add this to the standard library as opposed to building a third party package?

It's hard to do this safely in a third party package.  Consider a struct allocated in the arena that contains pointers to memory allocated outside the arena.  The GC must be aware of those pointers, or it may incorrectly free ordinary-memory objects that are still referenced by arena objects.  A third party package would have to somehow make the garbage collector aware of those pointers, including as the pointer values change, which is either hard or inefficient.

## Comment 1048303898

other (CONTRIBUTOR) · ianlancetaylor · 2022-02-22T23:20:10Z · https://github.com/golang/go/issues/51317#issuecomment-1048303898

@clausecker 

> However, this means that the compiler must now be careful not to dereference any pointer it knows not to be nil unless user code explicitly does so

That is already true.  Go code can use pointers that point to memory that was allocated by C, or that was allocated by `syscall.Mmap`.  The compiler already can't casually dereference a pointer.

> the garbage collector could be programmed to check if any pointers into the arena address space remain and if there aren't any, it could allow the address space to be reclaimed

I believe that we can already do that.  If the garbage collector sees a pointer to a freed arena, it can crash the program.  If we have two complete GC cycles after an arena is freed, we can know for sure that there are no remaining pointers into that address space, and we can reclaim the addresses.  However, I don't know if the current patches implement that.

## Comment 1048306511

other (CONTRIBUTOR) · ianlancetaylor · 2022-02-22T23:24:36Z · https://github.com/golang/go/issues/51317#issuecomment-1048306511

@tarndt 

> I'd be curious to understand the problems that an arena solves that can't be solved by either using sync.Pool, allocating a slice of a given type (for example a binary tree allocating a slice of nodes), or a combination of both techniques. It seems to me that Go provides idiomatic ways of addressing at least the specific protobuf use-case mentioned here.

As you note, `sync.Pool` only permits allocating a specific type.  It's reasonable to use if all allocations are the same type.  An arena is when most allocations are different types.  That is the case for protobuf allocations: each protobuf is implemented as a different Go struct.  It's also the case for many uses of, for example, JSON.

> In addition to the above, doesn't the Go allocator already have sizes classes? If the proposal does proceed, I think we need to see a prototype outperform the runtimes allocator and is enough gain to justify the ecosystem complexity.

I'm not sure how size classes are related.

As @danscales mentions, there is already an implementation, which is in use internally at Google.  It does overall outperform the runtime allocator for cases like RPC servers that transmit data as protobufs.

## Comment 1048306725

other (CONTRIBUTOR) · Merovius · 2022-02-22T23:24:57Z · https://github.com/golang/go/issues/51317#issuecomment-1048306725

First, I feel this should live in the `runtime` package, or at least in `runtime/arena`, as it seems fairly runtime specific. Which is my main concern with this, that other implementations might not support it and then packages using it would not be usable on those implementations.

Also, a question for clarification:

> It is probably most appropriate that there should only be a few to 10's of arenas in use at any one time.

One of the main usecases mentioned is protobuf decoding. ISTM that, if every call to `proto.Unmarshal` creates an arena, used until that message is done with, we would very quickly outpace 10's of arenas by orders of magnitude on a loaded gRPC server.

@quenbyako 

> as far as i understood this proposal, there are a lot of troubles for example in appending to slices, e.g. the code could be more readable if you just use append, without calling arena-specific methods.

AIUI the proposal would not interoperate with `append`, i.e. you'd indeed have to use arena-specific methods.

## Comment 1048307660

other (CONTRIBUTOR) · ianlancetaylor · 2022-02-22T23:26:39Z · https://github.com/golang/go/issues/51317#issuecomment-1048307660

@komuw 

> What's the main usecase for wanting to allocate types created via reflect in arenas? Marshalling & unmarshall?
Are those usecases compelling enough? Honest question.

Yes, marshaling and unmarshaling.  These cases are compelling for, for example, network RPC servers that must serialize and unserialize data for every request.

## Comment 1048311568

maintainer (MEMBER) · adonovan · 2022-02-22T23:33:31Z · https://github.com/golang/go/issues/51317#issuecomment-1048311568

One implementation caveat: a 64-bit address space isn't quite the inexhaustible vastness it first seems because many environments impose tighter restrictions. (I recently used a 4GB mmap as an [optimization](https://github.com/google/starlark-go/pull/280) but found [OpenBSD's default ulimit is 1.5GB](https://github.com/google/starlark-go/issues/382) and [some users seem to impose their own limits](https://github.com/google/starlark-go/issues/394).)

## Comment 1048315914

other (CONTRIBUTOR) · Merovius · 2022-02-22T23:42:11Z · https://github.com/golang/go/issues/51317#issuecomment-1048315914

Which reminds me:

> It is not clear if a similar approach can work for 32-bit architectures, where the address space is much more limited.

Does this mean this package would use build-tags to limit itself to 64-bit architectures? And would programs using this then not run on 32-bit platforms, unless they specifically code around that? Also, this seems all the more reason to put this into `runtime`, to make clear that it's platform dependent.

## Comment 1048318877

maintainer (MEMBER) · thepudds · 2022-02-22T23:48:08Z · https://github.com/golang/go/issues/51317#issuecomment-1048318877

Hi @Merovius, my interpretation was that the API could be implemented everywhere, but it would not increase efficiency everywhere:

> Note that the above arena API may be implemented without actually implementing arenas, but instead just using the standard Go memory allocation primitives. We may implement the API this way for compatibility on some architectures for which a true arena implementation (including safety checks) cannot be implemented efficiently.

## Comment 1048328340

other (CONTRIBUTOR) · Merovius · 2022-02-23T00:06:09Z · https://github.com/golang/go/issues/51317#issuecomment-1048328340

@thepudds ah thank you, I missed that, alleviates my concerns around portability. Though I'd find it a bit confusing to provide the API without actual arenas. But, fair enough.

## Comment 1048333104

maintainer (MEMBER) · thepudds · 2022-02-23T00:14:58Z · https://github.com/golang/go/issues/51317#issuecomment-1048333104

@Merovius raises an interesting question, though, around what the overhead of the non-arena implementation of the arena api would be…

## Comment 1048337731

other (NONE) · tarndt · 2022-02-23T00:23:23Z · https://github.com/golang/go/issues/51317#issuecomment-1048337731

@ianlancetaylor 

>As you note, sync.Pool only permits allocating a specific type. It's reasonable to use if all allocations are the same type. An arena is when most allocations are different types. That is the case for protobuf allocations: each protobuf is implemented as a different Go struct. It's also the case for many uses of, for example, JSON.

Assuming the problem with protobufs is the actual objects and not some internal buffer, here is how I would naively use `sync.Pool`.

Today you might see code like this:
```go
book := &pb.AddressBook{}
```
Rather I would suggest the generated `AddressBook` code includes a constructor function:
```go
book := NewAddressBook()
```
The protoc _generated code_ in its package would look something like this:
```go

var addressBookPool sync.Pool = sync.Pool{
	New: func() interface{} {
		return new(AddressBook)
	},
}

func NewAddressBook() *AddressBook {
    return addressBookPool.Get().(*AddressBook)
}

func (ab *AddressBook) Close() error { 
    *ab = AddressBook{}
     addressBookPool.Put(ab)
     return nil
}
```
*I assume if arena existed similar changes to have a constructor that uses it would need to happen as well? If not that burden would fall to the object creator which is in fact how I use sync.Pool with protobufs today (when needed)*

Now maybe more is needed say:
```go
func (ab *AddressBook) Close() error {
    ab.closeOnce.Do(func() {
        *ab = AddressBook{}
         addressBookPool.Put(ab)
    })
    return nil
}
```
Or maybe we need to also generate and use pools/constructors of `*structs` referenced in `AddressBook` (or do what some pkgs like gogoproto optionally do and not use pointers for objects nested in proto structs). Lots of nuance that is besides the point of this discussion-

But I would like to understand why the arena approach is better.  I'd also be curious to bench an arena prototype against `sync.Pool` and an approach like the above.

## Comment 1048342613

reporter (CONTRIBUTOR) · danscales · 2022-02-23T00:32:10Z · https://github.com/golang/go/issues/51317#issuecomment-1048342613

> If the rules were tightened to say that you have to erase all pointers into an `arena` before calling `Free`, not only would these optimisations be enabled, but there would also be a way to reclaim the address space occupied by the arena: the garbage collector could be programmed to check if any pointers into the arena address space remain and if there aren't any, it could allow the address space to be reclaimed. If it finds a stray pointer, it could likewise abort the program in much the same manner as when you dereference a stray pointer.

In addition to what Ian already said about the compiler not dereferencing stray pointers:

One reason that we would like to able to deal with pointers to objects in the arena staying around after it  freed (as long as they are not used) is because it may be quite tricky and disruptive to have to remove them from the stack.  A pointer to an object in the arena could have been passed around as an arg and is still on the stack as an argument or local variable, but will not be used again.  It would be good to ensure that the programmer does not have to nil out these pointers on the stack just to satisfy arenas, when they will naturally go away later.




## Comment 1048344834

reporter (CONTRIBUTOR) · danscales · 2022-02-23T00:36:12Z · https://github.com/golang/go/issues/51317#issuecomment-1048344834

> > We don’t think these generic variants of the API can completely replace ....

> > Second, generics in Go are just arriving in Go 1.18, so we don’t want to force users to make use of generics before they are ready.
> 
> Is there a hurry in adding arenas? It can always wait one or two release cycles before been added so that people are ready with generics. In other words, if hypothetically speaking, the arena-generics design was the better API; we shouldn't shelve it just because generics aren't ready yet.

Yes, I agree.  There's no rush to figure out and add arenas, so it may be worth waiting to use the generics API if there's consensus on it being a better API.  The first point does remain - which is that we would prefer to have some API that allows for allocating a type that is created/calculated at runtime.  However, the generics API could become the main API, and the one that allows for dynamic types could be the secondary API.


## Comment 1048347735

reporter (CONTRIBUTOR) · danscales · 2022-02-23T00:41:27Z · https://github.com/golang/go/issues/51317#issuecomment-1048347735

> This proposal sounds really good to me from a user's perspective, but one detail causes concern: wouldn't something like all code eventually end up needing arena support? For example, imagine I have a web service where I want to allocate an arena for each web request. This sounds like a great use case for this, but I'd need `encoding/json` to have an Arena mode, and maybe `text/template`/`html/template` to have Arena modes so their working sets can use the Arena. Probably same for various clients (SQL, http, etc.) Is that what you see as the path forward or am I missing something?

Yes, that's a good point.  If we have a package that is allocating lots of memory (often by doing decoding of wire format) and we want to use arenas with it, then we will have to plumb in a way to send down an optional allocator function that it should use if enabled (in our case, the allocator function would use an arena).  That's what we have prototyped for the protobuf unmarshaling library calls (see last section).  I don't see any easy way to make packages use arenas, but open to suggestions.



## Comment 1048350175

maintainer (MEMBER) · thepudds · 2022-02-23T00:45:38Z · https://github.com/golang/go/issues/51317#issuecomment-1048350175

Hi @danscales

>  If we have a package that is allocating lots of memory (often by doing decoding of wire format) and we want to use arenas with it, then we will have to plumb in a way to send down an optional allocator function that it should use if enabled (in our case, the allocator function would use an arena).

Is there a rough estimate of how many new APIs this might translate to in the standard library, for example?

## Comment 1048351173

reporter (CONTRIBUTOR) · danscales · 2022-02-23T00:47:23Z · https://github.com/golang/go/issues/51317#issuecomment-1048351173


> Also, a question for clarification:
> 
> > It is probably most appropriate that there should only be a few to 10's of arenas in use at any one time.
> 
> One of the main usecases mentioned is protobuf decoding. ISTM that, if every call to `proto.Unmarshal` creates an arena, used until that message is done with, we would very quickly outpace 10's of arenas by orders of magnitude on a loaded gRPC server.
> 

Yes, that is true.  It is possible there is another implementation that could deal with that many arenas simultaneously.  But I will note that if you have 100s of requests in flight at one time, then they may not be allocating that much new data while serving each individual request, so arenas may not really be required in that case.    Arenas are really more useful/appropriate for unmarshalling large data objects for which you may do a lot of processing.  sync.Pool may be more appropriate if the allocated data per request is small (since there may also be only a limited number of known object types).




## Comment 1048362417

other (NONE) · CannibalVox · 2022-02-23T01:06:39Z · https://github.com/golang/go/issues/51317#issuecomment-1048362417

> Yes, I agree. There's no rush to figure out and add arenas, so it may be worth waiting to use the generics API if there's consensus on it being a better API. The first point does remain - which is that we would prefer to have some API that allows for allocating a type that is created/calculated at runtime. However, the generics API could become the main API, and the one that allows for dynamic types could be the secondary API.

Is there any idea of (A) what is the net cost of doing this with reflection and (B) will it be possible to not do it with reflection when using the generics API?

> Yes, that is true. It is possible there is another implementation that could deal with that many arenas simultaneously. But I will note that if you have 100s of requests in flight at one time, then they may not be allocating that much new data while serving each individual request, so arenas may not really be required in that case. Arenas are really more useful/appropriate for unmarshalling large data objects for which you may do a lot of processing. sync.Pool may be more appropriate if the allocated data per request is small (since there may also be only a limited number of known object types).

What message sizes/throughputs was the prototype tested at? Many small requests/responses is certainly the norm in my background, but I know google was looking hard (I believe?) a Vitess blog post that mainly dealt with very large data replication messages. Certainly if proto performance gets worse than status quo at high throughput levels, many people wouldn't be thrilled with that.

## Comment 1048366038

other (NONE) · CannibalVox · 2022-02-23T01:13:52Z · https://github.com/golang/go/issues/51317#issuecomment-1048366038

> > This proposal sounds really good to me from a user's perspective, but one detail causes concern: wouldn't something like all code eventually end up needing arena support? For example, imagine I have a web service where I want to allocate an arena for each web request. This sounds like a great use case for this, but I'd need `encoding/json` to have an Arena mode, and maybe `text/template`/`html/template` to have Arena modes so their working sets can use the Arena. Probably same for various clients (SQL, http, etc.) Is that what you see as the path forward or am I missing something?
> 
> Yes, that's a good point. If we have a package that is allocating lots of memory (often by doing decoding of wire format) and we want to use arenas with it, then we will have to plumb in a way to send down an optional allocator function that it should use if enabled (in our case, the allocator function would use an arena). That's what we have prototyped for the protobuf unmarshaling library calls (see last section). I don't see any easy way to make packages use arenas, but open to suggestions.

Add memory allocator to context? It seems really silly but doing a second round of "context-aware" updates to add context in more places seems better to me than doing a second round of "context-aware" updates that adds an entirely new type of object that ends up needing to be sent everywhere.

## Comment 1048369149

other (CONTRIBUTOR) · evanphx · 2022-02-23T01:21:03Z · https://github.com/golang/go/issues/51317#issuecomment-1048369149

Hi all,

One quick thought: could you utilize the write barrier that is currently used by the compiler/GC to detect writes to arena allocated memory outside of the arena. Then on .Free, copy the values that are referenced out to the main heap?

This would let you effectively use an arena as a large scratch area, with the GC assisting in figuring out which values are not just scratch.

## Comment 1048386788

other (CONTRIBUTOR) · schmichael · 2022-02-23T02:04:03Z · https://github.com/golang/go/issues/51317#issuecomment-1048386788

Is the code for the experimental protobuf implementation published? The scope of code that needs changing in order to take advantage of per-request arenas seems huge, but I'm eager to see a real world example in hopes I'm wrong!

## Comment 1048466742

other (CONTRIBUTOR) · ianlancetaylor · 2022-02-23T05:47:02Z · https://github.com/golang/go/issues/51317#issuecomment-1048466742

@tarndt A protobuf message can include many different messages (as they are called) arranged in a complex memory layout.  This is all relatively seamless for the program but it means that unmarshaling a protobuf isn't just a matter of allocating a single object type, it can involve dozens of different types.  So you would need dozens of different `sync.Pool` structures.  And in order to use the pools effectively you would need a complicated piece of code to release all the data back to the appropriate pools, which is much more complicated, and slower, than releasing an arena.

Frankly an arena sounds a lot simpler.  And let's not forget that an arena lets you notify the runtime exactly when the memory is no longer needed.  A pool will stick around in a much less predictable fashion.

## Comment 1048467006

other (CONTRIBUTOR) · ianlancetaylor · 2022-02-23T05:47:46Z · https://github.com/golang/go/issues/51317#issuecomment-1048467006

@evanphx I think that would require enabling the write barrier at all times, which would be quite a bit slower than the current approach.

## Comment 1048478158

other (CONTRIBUTOR) · kylelemons · 2022-02-23T06:16:52Z · https://github.com/golang/go/issues/51317#issuecomment-1048478158

I'm in favor of this.  Getting pooling and other allocation-related performance bits correct has been a challenge for us with Thrift as well, so the advantages can go beyond protobuf.  I think arenas would simplify things considerably, both in terms of implementation and in ease of ensuring correctness.

## Comment 1048585297

other (NONE) · vmg · 2022-02-23T09:22:40Z · https://github.com/golang/go/issues/51317#issuecomment-1048585297

@danscales: since you already have a proposed implementation for the feature, I think it would make discussing the proposal as a whole much easier if you shared its CL. Cheers!

## Comment 1048586953

other (NONE) · YuriyNasretdinov · 2022-02-23T09:24:41Z · https://github.com/golang/go/issues/51317#issuecomment-1048586953

I like the general idea. I think in some places like e.g. creating an AST when parsing files the performance benefits can be literally tenfold.

## Comment 1048595120

maintainer (MEMBER) · mvdan · 2022-02-23T09:34:17Z · https://github.com/golang/go/issues/51317#issuecomment-1048595120

> However, the generics API could become the main API, and the one that allows for dynamic types could be the secondary API.

As I was reading the original proposal, this was definitely the main idea that came to mind. Using generics feels more natural and easier for the majority of cases, so it should be the main API, I think. I also believe that adding a generic std API in Go 1.19 would be completely fine, for example - especially given how the use of generics here would be fairly simple.

## Comment 1048597705

maintainer (MEMBER) · mvdan · 2022-02-23T09:37:42Z · https://github.com/golang/go/issues/51317#issuecomment-1048597705

> I don't see any easy way to make packages use arenas, but open to suggestions.

I don't have a good solution for you here, but I think it's worth noting that we've been in a very similar situation before: contexts. Some APIs fixed this by adding a second `FooContext` function, while others added a context field to a struct.

There's always the option of an existing API taking an arena via `context.WithValue`, though I seem to recall that each call to `WithValue` incurs an allocation of its own. Passing an arena as part of a context could still be a worthwhile idea to experiment on, though, as it could make adoption a lot easier for a significant portion of existing stable libraries.

## Comment 1048633962

other (CONTRIBUTOR) · Merovius · 2022-02-23T10:21:53Z · https://github.com/golang/go/issues/51317#issuecomment-1048633962

Personally, I don't very much like the idea of passing around allocators, context or not. I don't feel that traversing the context-chain on every allocation is a very good idea. I also don't want to have to add `context.Context` arguments to any call to data-structures which might need to allocate - `heap.Insert(ctx, v)` feels wrong. `context.Context` has a definite connotation with cancellation and network-traversal to me.

IMO this should ~always be treated as an implementation detail by packages who know that they would benefit from it. For example, it might be possible for `proto.Unmarshal` to transparently use an arena if it is willing to rely on a Finalizer to call `Free`. The API of the `proto` package would then not change at all. The top-level message to pass to `proto.Unmarshal` would still have to be allocated on the heap, but at least all the nested sub-messages could be allocated in the arena when the `proto` package recurses. You'd get most of the benefit without having to plumb allocators.

And even if we're not willing to do that, the way to go would IMO be for the proto package to expose a `UnmarshalArena[M Message](a *arena.Arena, b []byte) *M` function, which is then called by the gRPC server (for example), which directly allocates the arena in `grpc.NewServer` - without giving the ability to plumb it further than that.

i.e. IMO the level of plumbing should be kept to an absolute minimum. In particular, I don't see a reason why protobuf generated code would need to mention arenas at all, FWIW.

If we *do* plumb, I'd argue that yes, we should add `Allocator` fields/arguments to any data structure/type/function which would benefit (combined with a `type allocator.Heap struct{}` which uses `new` and `make`). Making it explicit would serve as an incentive to keep the plumbing depth shallow anyways.

## Comment 1048635532

other (CONTRIBUTOR) · Merovius · 2022-02-23T10:23:50Z · https://github.com/golang/go/issues/51317#issuecomment-1048635532

Maybe the best way to put it is that I see arenas as very much alike to `sync.Pool`. We don't pass those around across API boundaries either.

## Comment 1048639457

other (NONE) · CannibalVox · 2022-02-23T10:28:23Z · https://github.com/golang/go/issues/51317#issuecomment-1048639457

I think that that would cause problems in cases where you need to, for instance, unmarshal a large corpus of different small json files. Some arena is better than none, probably, but it stings to be just incapable of using this stdlib feature with other parts of the stdlib in a use case it was clearly intended for.

## Comment 1048717664

other (NONE) · muscar · 2022-02-23T12:09:58Z · https://github.com/golang/go/issues/51317#issuecomment-1048717664

@danscales can you share more details on the applications you tested the arena protoype implementation with? What kind of applications are they, how much data do they process, what are their performance requirements?

One of the things I find a bit unclear about this proposal is exactly who it's supposed to benefit. You note that:

>  It is probably most appropriate that there should only be a few to 10's of arenas in use at any one time. 

and

> [I]f you have 100s of requests in flight at one time, then they may not be allocating that much new data while serving each individual request, so arenas may not really be required in that case. Arenas are really more useful/appropriate for unmarshalling large data objects for which you may do a lot of processing.

This seems to restrict the subset of apps that would benefit from this incarnation of arenas somewhat significantly. The added focus on protobufs makes me think that the authors have a very specific set of applications in mind.

Is such an intrusive change worth the 15% speed gain for a subset of apps of unknown size?

## Comment 1048730100

other (CONTRIBUTOR) · Merovius · 2022-02-23T12:25:01Z · https://github.com/golang/go/issues/51317#issuecomment-1048730100

@CannibalVox ~~For json specifically, `json.NewDecoder` could allocate an arena, which would allow you to pipe the concatenated JSON data in. More generally, there are often ways to write APIs which allow you to take advantage of arenas without actually mentioning arenas in your API.~~ sorry, just realized this is pretty much nonsense. As the objects might outlast the Decoder, the lifetime of the arena can't be tied to it - and in general, whenever an arena outlasts a function call, the caller probably needs to be aware of it. My bad.

## Comment 1048760630

other (NONE) · tommie · 2022-02-23T13:04:12Z · https://github.com/golang/go/issues/51317#issuecomment-1048760630

>  a common mistake with using arenas in Go is to use a string that was allocated from an arena in some global data structure, such as a cache, which that can lead to a run-time exception when the string is accessed after its arena is freed. This mistake is understandable, because strings are immutable and so often considered separate from memory allocation.

Could this be encoded as a separate type instead? With generics, at least the language has the expressivity of `Arena[string]`, which would also work for non-strings. But if this proposal requires tying in with the compiler/runtime, perhaps the string case should be a completely separate type that the compiler treats like a `string` in most contexts?

## Comment 1048761756

other (NONE) · muscar · 2022-02-23T13:05:34Z · https://github.com/golang/go/issues/51317#issuecomment-1048761756

On @Merovius's point

> and in general, whenever an arena outlasts a function call, the caller probably needs to be aware of it. 

Wouldn't arenas open a can of worms where any API method could potentially be returning an arena pointer that you need to be aware of?

## Comment 1048793039

other (CONTRIBUTOR) · zephyrtronium · 2022-02-23T13:40:20Z · https://github.com/golang/go/issues/51317#issuecomment-1048793039

One line I like to use to explain how Go differs from C and C++ is, "in Go, every pointer is either valid or nil." That line has caveats for unsafe, cgo, syscalls, and any other ways to work outside the type system, of course.

The proposed mechanism here provides a "safe" way to obtain pointers to dead objects, which may or may not terminate the program upon dereference. If it is accepted, then my line instead becomes, "in Go, every pointer is either valid or nil, except those that came from an arena, which you have no way to detect in general." This is a different sense of "memory safety" than what we have now.

## Comment 1048809041

other (NONE) · YuriyNasretdinov · 2022-02-23T13:58:41Z · https://github.com/golang/go/issues/51317#issuecomment-1048809041

I also agree that in Go code we must be explicit when some code is not memory-safe (or at least dangerous), and arenas seem like such a thing to me.

Otherwise it opens up a lot of possibilities for subtle errors that were not possible previously: e.g. if we have a transparent arena allocation on every web request for protobuf, for example, it would also mean that all fields in structs that are unmarshalled using protobuf are also not memory-safe, including `string`s. This would mean that if by any chance someone wants to have e.g. a global cache of some structs keyed by an object id, they would probably think about cloning the struct itself that was allocated on the arena, but I doubt that it is obvious that e.g. a key inside that struct, such as an `ID string` field would also not be safe to be used in a map.

So, with transparent arena-allocated structs you could very easily write (incorrect) code like the following (mutexes removed for brevity):

```go

var globalCache map[string]*someObject

...

func handleWebRequest(obj *someObject) {
globalCache[obj.ID] = proto.Clone(obj) // obj.ID is also arena-allocated, so it's not safe to use it as a map key
}
```

Of course, even with explicit arenas as arguments everywhere it would be easy to make such a mistake, but similar to how Go handles errors, it at least makes you think about the implications of using an arena more and that's a good thing.

## Comment 1048814813

other (CONTRIBUTOR) · Merovius · 2022-02-23T14:04:55Z · https://github.com/golang/go/issues/51317#issuecomment-1048814813

@zephyrtronium ISTM that means you have to add arenas to the list "unsafe, cgo, syscalls and any other way to work outside the type system". Also, race conditions.

But honestly, I feel like "every pointer is either nil or invalid" is already overly simplistic. For example, consider this:

```go
type X struct { m map[int]string }

func (x *X) F(a int, b string) { x.m[a] = b }
```

`new(X)` is a non-nil pointer. But is it "valid"? Calling its method will panic. I'd argue that makes it invalid. The Go typesystem just doesn't encode that invariant.

But yes, arenas definitely are a thing that should be considered with care. And we should discourage APIs which are easy to misuse.

## Comment 1048818944

other (CONTRIBUTOR) · Merovius · 2022-02-23T14:09:12Z · https://github.com/golang/go/issues/51317#issuecomment-1048818944

Hm. I think this discussion begs the question:

> The implementation calls SetFinalizer(A, f) on each arena A as it is allocated, where f calls A.Free. This ensures that an arena and the objects allocated from it will eventually be freed if there are no remaining references to the arena. The intent though is that every arena should be explicitly freed before its pointer is dropped.

Why is that the intent? ISTM an arena does not represent a resource beyond memory, so ISTM that they are exactly what finalizers are useful for. A lot of the discussion about safety could be solved by relying on finalizers and the GC to call Free, instead of expecting the programmer to do it and expose a source of mistakes. So why don't we?

## Comment 1048821353

other (NONE) · muscar · 2022-02-23T14:11:47Z · https://github.com/golang/go/issues/51317#issuecomment-1048821353

> new(X) is a non-nil pointer. But is it "valid"? Calling its method will panic. I'd argue that makes it invalid. The Go typesystem just doesn't encode that invariant.

@Merovius I'd argue that that's a slightly different form of validity. The pointer returned by `new(X)` is a valid pointer. It's just that when you call the method on it, the object is not properly constructed/initialised.

## Comment 1048821529

other (CONTRIBUTOR) · zephyrtronium · 2022-02-23T14:11:58Z · https://github.com/golang/go/issues/51317#issuecomment-1048821529

It might be reasonable to make the difference in "memory safety" more concrete, now that we have generics. We could have arenas work with an `arena.Pointer[T]` type instead of plain pointers, with only a `Deref() T` method (and maybe a `HeapCopy() *T`). This makes it much clearer where arena pointers are used, and it makes documentation on the dangers more accessible. Similar types would make sense for slices and strings.

## Comment 1048825784

other (CONTRIBUTOR) · bcmills · 2022-02-23T14:16:19Z · https://github.com/golang/go/issues/51317#issuecomment-1048825784

> To deal with the situation of a string whose allocation method is unknown, `HeapString` makes a copy of a string using heap memory only if the passed-in string (more correctly, its backing array of bytes) is allocated from an arena.

Existing Go programs — and, especially, existing Go libraries — have been written with Go's “immutable string” semantics in mind. _No_ existing packages written against mainline Go call `HeapString` (because it doesn't exist yet), so with that approach, in order for a program that uses arenas to be memory-safe it must call `HeapString` on _every_ string passed (even indirectly) to any non-arena-aware package.

I believe that that approach makes arena-allocated `string` values much too error-prone. They would appear to be safe to pass as type `string`, but the type `string` would now refer to two types that are fundamentally different:

1. Ordinary, immutable, heap-allocated `string` values, which are garbage-collected and safe to use ~everywhere.

    * Storing a short fragment of a `string` in a global data structure today may over-retain a larger backing allocation, but that allocation will show up on memory profiles and — crucially! — will not cause the program to crash or produce corrupted output or undefined behavior.

2. Arena-allocated `string` values, which are functionally more like slices: they are no longer safe to read after a call returns, and not guaranteed to have stable contents over time.

To me, those factors imply that the “arena-allocated contiguous slice of bytes” type should be `[]byte` or some newly-defined “unsafe string” type, not `string` proper. The argument I could see in favor of `string` is that some APIs operate on type `string` instead of `[]byte` — but wasn't part of the point of adding generics so that we could abstract over the differences between immutable strings and ephemeral slices for APIs that don't care about those differences?

## Comment 1048831618

other (CONTRIBUTOR) · bcmills · 2022-02-23T14:22:18Z · https://github.com/golang/go/issues/51317#issuecomment-1048831618

To draw from existing experience in other languages: because Java objects tend to be mutable, Java programs are often littered with [defensive copying](https://dev.to/kylec32/effective-java-make-defensive-copies-when-necessary-4bd6), which not only makes them more difficult to reason about, but also adds a lot of allocation and copying overhead _that would not be needed_ in a program that distinguishes between mutable and immutable values (as Go programs do today).

## Comment 1048832797

other (CONTRIBUTOR) · zephyrtronium · 2022-02-23T14:23:27Z · https://github.com/golang/go/issues/51317#issuecomment-1048832797

@Merovius 
> @zephyrtronium ISTM that means you have to add arenas to the list "unsafe, cgo, syscalls and any other way to work outside the type system". Also, race conditions.

I think you missed my point. Arenas as proposed look like plain, normal types that give plain, normal pointers. They are not. They work outside the existing Go rules, requiring direct support from the runtime per https://github.com/golang/go/issues/51317#issuecomment-1048301788. Unsafe, cgo, and syscalls *explicitly indicate* that they are not Go. Race conditions are not part of the Go language. Does it make sense to just say that this new package is not part of Go?

> But honestly, I feel like "every pointer is either nil or invalid" is already overly simplistic.

Sure, I could be more specific and say that "there are no dangling pointers in Go," which is still a condition violated by this proposal. I consider `new(X)` in your example to be a valid pointer to an object containing a nil pointer, as @muscar said, but that would be an argument about what "valid" means, and I think off-topic here.

## Comment 1048843159

other (CONTRIBUTOR) · zephyrtronium · 2022-02-23T14:33:08Z · https://github.com/golang/go/issues/51317#issuecomment-1048843159

Is the proposed Arena type meant to be safe for concurrent use?

## Comment 1048861017

maintainer (MEMBER) · thepudds · 2022-02-23T14:47:56Z · https://github.com/golang/go/issues/51317#issuecomment-1048861017

Hi @zephyrtronium, the proposal includes:

> Also, it is not intended that arenas be shared across goroutines. Each arena has a lock to protect against simultaneous allocations by multiple goroutines, but it would be very inefficient to actually use the same arena for multiple goroutines. Of course, that would rarely make sense anyway, since the lifetimes of objects allocated in different goroutines are likely to be quite different.

## Comment 1048867157

other (CONTRIBUTOR) · Merovius · 2022-02-23T14:53:58Z · https://github.com/golang/go/issues/51317#issuecomment-1048867157

@zephyrtronium I think you missed my point as well :) The pointers returned by arenas as proposed might seem special. But they are not *that* special, really. There are plenty of examples in the Go language where functions return pointers with caveats on when and how they can be used, lest your program panics, be it that they can't be modified, the pointed to values can't be copied or that they can't be retained after a callback returns. All of these conditions are error-prone, but we live with them just fine.

They are also set apart from the other examples you mention (unsafe, cgo and syscall) in that they are still *safe*. Your program might panic, if you violate their invariants, but it won't have undefined effects.

> It might be reasonable to make the difference in "memory safety" more concrete, now that we have generics. We could have arenas work with an `arena.Pointer[T]` type instead of plain pointers, with only a `Deref() T` method (and maybe a `HeapCopy()` *T). This makes it much clearer where arena pointers are used, and it makes documentation on the dangers more accessible.

IMO that is a bad idea. It would make it all but impossible to use them without polluting your API with arena usage. For example, the flagship use-case of protobuf encoding would now require all nested messages to be this new, special pointer type. As I said above, I don't think we should, generally, let arena usage cross API boundaries.

## Comment 1048871437

other (CONTRIBUTOR) · bcmills · 2022-02-23T14:58:03Z · https://github.com/golang/go/issues/51317#issuecomment-1048871437

> There are plenty of examples in the Go language where functions return pointers with caveats on when and how they can be used

For a specific example, consider [`io.Reader`](https://pkg.go.dev/io#Reader) and [`io.Writer`](https://pkg.go.dev/io#Writer). The `Read` and `Write` methods are explicitly not allowed to retain the argument slice after the call has returned, because the caller may mutate it concurrently and any access would be racy.

## Comment 1048886971

other (NONE) · muscar · 2022-02-23T15:12:43Z · https://github.com/golang/go/issues/51317#issuecomment-1048886971

> All of these conditions are error-prone, but we live with them just fine.

That's not a reason to add even more edge cases to the language :).

> Your program might panic, if you violate their invariants, but it won't have undefined effects.

That's technically true. But it makes reasoning about pointer lifetimes trickier. One of the appeals of GC'd languages if that you don't have to worry about lifetimes most of the time. This sounds like a decision that shouldn't be made lightly.

> It would make it all but impossible to use them without polluting your API with arena usage.

That is not necessarily bad. Unsafe pointers are special, and they are marked as such. Arena pointers are special, and they should be marked as such if arenas make it into the language. But again, the proposal as it stands sounds like a heavy price to pay for the gains outlined.

## Comment 1048900803

other (CONTRIBUTOR) · bcmills · 2022-02-23T15:26:16Z · https://github.com/golang/go/issues/51317#issuecomment-1048900803

> One of the appeals of GC'd languages if that you don't have to worry about lifetimes most of the time.

I don't think that's actually true, especially given mutability and concurrency. Go programmers do have to worry about lifetimes today, because they have to worry about aliasing bugs, data races, and memory leaks (especially via goroutine leaks and global variables).

The major question for me is: how much _additional_ worry about lifetimes would this proposal introduce? For types other than `string`, I think the answer is almost none: a Go library that today is free of data races, aliasing bugs, and memory leaks, would still be free of those classes of bugs if passed arena-allocated arguments.

## Comment 1048919528

other (NONE) · YuriyNasretdinov · 2022-02-23T15:43:32Z · https://github.com/golang/go/issues/51317#issuecomment-1048919528

Should runtime (or compiler / go vet when possible to deduce statically) then just outright panic when using arena-allocated `string` in `map`s that are heap-allocated? If so it would solve the main issue I personally have with arena allocation being transparent for users.

There is still a question about e.g. how `append` would work (even if arena usage is transparent) given that it reallocates underlying data every time the slice grows. There is a lot of code that doesn't expect `append` without initial capacity to be very expensive. Not sure how big of a deal it is, but it might be in some cases.

## Comment 1048923498

other (NONE) · muscar · 2022-02-23T15:47:28Z · https://github.com/golang/go/issues/51317#issuecomment-1048923498

> I don't think that's actually true, especially given mutability and concurrency. Go programmers do have to worry about lifetimes today, because they have to worry about aliasing bugs, data races, and memory leaks (especially via goroutine leaks and global variables).

Fair point, mixing concurrency and mutability is one of the areas where you do have to worry about lifetimes. And memory leaks do happen in GC'd languages. But these are somewhat "special" scenarios: programmers have been admonished over and over not to mix mutable state and concurrency. Mutable global variables are a smell which most people know about. But making arena pointers just regular values adds a whole new area of uncertainty. *Any* pointer dereference could now theoretically panic.

> [A] Go library that today is free of data races, aliasing bugs, and memory leaks, would still be free of those classes of bugs if passed arena-allocated arguments.

Yes, it will still be free of those classes of bugs, but prone to a whole new class: use after free on arena pointer that it doesn't know about.

## Comment 1048929072

other (CONTRIBUTOR) · bcmills · 2022-02-23T15:52:47Z · https://github.com/golang/go/issues/51317#issuecomment-1048929072

> Yes, it will still be free of those classes of bugs, but prone to a whole new class: use after free on arena pointer that it doesn't know about.

How so? As far as I can see, essentially every use-after-free bug that would occur with arenas has a corresponding (existing) aliasing bug or data race without arenas.

In both cases, the bug is caused by either unexpectedly accessing data retained after a call, or accessing data unexpectedly mutated during a call.

## Comment 1048933651

other (CONTRIBUTOR) · seebs · 2022-02-23T15:57:15Z · https://github.com/golang/go/issues/51317#issuecomment-1048933651

So, we already have this, sort of! It's called `mmap` and using the mmapped space as backing store (usually via unsafe). And we do indeed have to do defensive copying of things accessed through such a thing, and it's a pain. That said, it can still be better than not having that.

I am having vague thoughts that this design might want to be changed in some way if we had immutability as a trait we could express in the type system.

## Comment 1048934062

other (NONE) · muscar · 2022-02-23T15:57:38Z · https://github.com/golang/go/issues/51317#issuecomment-1048934062

@bcmills say you implement a global cache where you store pointers to arenas (nevermind if that's a good idea or not). Is it not possible to accidentaly pass an entry from the cache to a library function after the backing arena has been freed? And would that not result in a panic where it wouldn't have before? Or am I missing the point you are trying to make?

## Comment 1048944178

other (CONTRIBUTOR) · bcmills · 2022-02-23T16:07:05Z · https://github.com/golang/go/issues/51317#issuecomment-1048944178

@muscar, a global cache of pointers to arenas has the same failure modes as a global cache of, say, heap-allocated `[]byte`.

If you do a map lookup like:
```go
func lookup(b []byte) {
	v, ok := m[string(b)]
	…
}
```
then your program can panic or even crash if `b` is mutated during the map access.

Similarly, if you have a function like this:
```go
type S struct{ b []byte }

func deref(s *S, f func()) int {
	if len(s.b) > 0 {
		f()
		return s.b[0]
	}
	return 0
}
```
then your program can panic if `f` mutates the struct pointed to by `s`.

A race on freeing an arena is conceptually not that different from any other data race.

A use-after-free bug with an arena is conceptually not that different from any other aliasing bug. (It has an especially deep connection to the aliasing bugs that arise with `sync.Pool` today!)

## Comment 1048975310

other (NONE) · muscar · 2022-02-23T16:36:10Z · https://github.com/golang/go/issues/51317#issuecomment-1048975310

Thanks for the examples @bcmills. I see what you mean, and I agree with the point you made. My example was indeed an instance of an aliasing bug.

One of the things that makes me uneasy about this proposal is the potential for this kind of problems to become more pervasive. The examples you provided are well chosen, and they illustrate the current problems well.

Both of them involve `[]byte` which is different from a pointer, at least from the type system's perspective. A Go programmer who sees `[]byte` will hopefully be more vigilant. Yes, it's a somewhat weak argument. But at least the language gives you a sort of heads up that things could get tricky. 

But making arena pointers indistinguishable from GC'd pointers could get hairy because now you have to be extra careful when you see pointers because you don't know where they come from. That's why marking them, e.g. like C#'s `Memory<T>` type, has some benefits. In addition to it being an explicit marker that the programmer is dealing with non GC'd memory, it also collaborates with the GC, e.g. by `Pin()`-ing objects.

## Comment 1048992020

other (NONE) · CannibalVox · 2022-02-23T16:53:05Z · https://github.com/golang/go/issues/51317#issuecomment-1048992020

> But making arena pointers indistinguishable from GC'd pointers could get hairy because now you have to be extra careful when you see pointers because you don't know where they come from. That's why marking them, e.g. like C#'s Memory<T> type, has some benefits. In addition to it being an explicit marker that the programmer is dealing with non GC'd memory, it also collaborates with the GC, e.g. by Pin()-ing objects.

I believe that these concerns are unnecessary. One of the key benefits of the arena pattern is how easy it is to avoid the sorts of problems you're describing. Imagine you are the engineer writing the code that creates & frees the arena- what sorts of mistakes would you have to make for another engineer's actions to cause freed memory to be dereferenced? Given that you are in a position to know what data is being allocated from the arena, and also to control the flow of that data, how would such a thing even be possible if you act correctly?

The problem, then, is that **the engineer who creates the arena must be in the driver's seat**, and that does require arenas to be accepted from callers in most situations. As Merovius observed above- the json/encoding library can't use arenas "under the hood" because the caller has to be the one who creates & frees the arena so that there's no "magic" silently producing transient pointers.  (That said, @Merovius I think you're right that you can just make the arena an optional property of the decoder and not even have to pass the arena in for any particular method.)

## Comment 1049014432

other (NONE) · muscar · 2022-02-23T17:14:25Z · https://github.com/golang/go/issues/51317#issuecomment-1049014432

@CannibalVox 

>  Imagine you are the engineer writing the code that creates & frees the arena- what sorts of mistakes would you have to make for another engineer's actions to cause freed memory to be dereferenced? 

This exercise in itself is interesting. The burden of this exercise will now lie on the shoulders of implementers who use arenas to some extent: "How can the users of my library misues it? What do I have to warn them about? What do I have to document?" And this last point, relying on docs instead of automated checks is key. Computers are good at following rules. Humans not so much. How did documenting ownership and lifetime details work for C or C++?

> Given that you are in a position to know what data is being allocated from the arena, and also to control the flow of that data

Am I? If so then that somewhat circumscribes and restricts what can be done with arenas. If you want to use them as an internal implementation detail of a serialisation library or something similar then fine. You have control over a lot of it, and you don't have to even expose that you're using arenas to your library's clients. But that begs the question if such a change is worth the runtime and language support.

> how would such a thing even be possible if you act correctly?

That's a pretty big assumption to make, and I'm happy for whatever help compilers can give me to help me act correctly.

> The problem, then, is that the engineer who creates the arena must be in the driver's seat, and that does require arenas to be accepted from callers in most situations. As Merovius observed above- the json/encoding library can't use arenas "under the hood" because the caller has to be the one who creates & frees the arena so that there's no "magic" silently producing transient pointers. 

Cool. So we come back to the point of arenas being used in a very specific case, as a performance optimisation. If the measurements support it then by all means go for an arena. But again, the changes it would require from the runtime, and the language would open the door to some nastier issues in my view.

## Comment 1049023050

other (NONE) · CannibalVox · 2022-02-23T17:23:02Z · https://github.com/golang/go/issues/51317#issuecomment-1049023050

> This exercise in itself is interesting. The burden of this exercise will now lie on the shoulders of implementers who use arenas to some extent: "How can the users of my library misues it? What do I have to warn them about? What do I have to document?" And this last point, relying on docs instead of automated checks is key. Computers are good at following rules. Humans not so much. How did documenting ownership and lifetime details work for C or C++?

Arenas were developed as a pattern in C & C++ to deal with the exact problem you're describing **because** they don't have those issues.  The correct usage of a memory arenas is ultimately that it's allocated at the start of a method, it's always freed at the end of that same method, and all allocations made between those two points happen in the arena. Arenas are not intended for long-lived objects, or really any objects that escape that method at all.

> If so then that somewhat circumscribes and restricts what can be done with arenas.

Yes, absolutely! Arenas are an allocation pattern intended for a strict subset of use cases that, in C, dramatically improves allocation performance & reduces bookkeeping in those use cases. It does **increase** bookkeeping for us, because we normally use garbage collection, but it also improves performance by even more than usual. This is not **intended**, I don't think, for every use case. There's a specific hole in go's memory performance story, and it's not exactly arena-shaped, but arenas do fill most of the space, I think.

## Comment 1049032288

other (CONTRIBUTOR) · zephyrtronium · 2022-02-23T17:32:22Z · https://github.com/golang/go/issues/51317#issuecomment-1049032288

I don't see/ctrl+f any proposed behavior for the zero Arena value. It seems to me that having a nil Arena always allocate from the heap would make opt-in usage very easy.

## Comment 1049160908

other (CONTRIBUTOR) · rsc · 2022-02-23T19:59:45Z · https://github.com/golang/go/issues/51317#issuecomment-1049160908


This proposal has been added to the [active column](https://golang.org/s/proposal-status#active) of the proposals project
and will now be reviewed at the weekly proposal review meetings.
— rsc for the proposal review group


## Comment 1049165143

other (NONE) · muscar · 2022-02-23T20:04:32Z · https://github.com/golang/go/issues/51317#issuecomment-1049165143

@CannibalVox I know what arenas are. And how they are used in C or C++. What I was getting at (in a very roundabout way) is that they are a very specific pattern only useful in some scenarios. We seem to agree on that point :).

The point I was trying to make is that going straight to adding language level support for a very specific pattern seems a bit rushed. Once you add something to a language it's hard to go back. And you have to write docs for it, make sure newcomers to the language don't misuse it, etc.

That's why a good strategy is to try to implement it as a library. You can always add features to the language later, when you understand the use cases better, if it's warranted.

Also, extending the language in the proposed way would only benefit this one specific case. If you really need language support it makes sense to add smaller, more generic features that other users could use, independently of the one specific use case that prompted them. In this case you could add raw memory handles that the language and GC know about. Allow the memory region to be pinned, and let the GC know that. This would serve as a base for the arena library as well as other scenarios.

What is the cost benefit analysis on making this change to the language? You get a 15%-20% speedup on some very specific scenarios on x86-64 linux at the cost of added complexity for every user of the language irrespective of them using the feature or not.

## Comment 1049195570

reporter (CONTRIBUTOR) · danscales · 2022-02-23T20:40:00Z · https://github.com/golang/go/issues/51317#issuecomment-1049195570

> Hi @danscales
> 
> > If we have a package that is allocating lots of memory (often by doing decoding of wire format) and we want to use arenas with it, then we will have to plumb in a way to send down an optional allocator function that it should use if enabled (in our case, the allocator function would use an arena).
> 
> Is there a rough estimate of how many new APIs this might translate to in the standard library, for example?

No, there is no estimate, since this is just a proposal and its possible use would be completely optional for any packages, of course.   I expect there would be lots of consideration and experimentation before deciding that it may be worth adding optional support for arenas in a particular package.  (Maybe a little similar to being very cautious and slowly gaining experience before adding adding any generic APIs to existing packages, now that generics is just arriving)


## Comment 1049198734

other (NONE) · creker · 2022-02-23T20:42:49Z · https://github.com/golang/go/issues/51317#issuecomment-1049198734

I’m generally in fair of this but have two concerns.

“If this optimization is used, the application is allowed to proceed normally if an object is accessed after the arena containing it is freed, as long as the memory of the object is still available and correct“
I feel like this will only make things worse by hiding genuine errors. Why do we need this? I feel like much better is to immediately panic after free is called regardless of whether arena is really freed or not. 

Second is the fact that this library would return regular Go objects. Go is very much about reducing cognitive load and as others already pointed out arena allocations will force developers to always keep in mind that some memory might be arena allocated and they can’t simply store it for later use. Given Go lacks immutability developers already has to think about that all the time and hope documentation covers that. We don’t need to add more cognitive load. 

Given that arena allocation is very niche usecase why don’t we also make it very explicit. Let API return special object that returns empty interface and has to be type asserted every time you need to access the underlying object. At least that way we are very explicit about arena allocation and developers will think twice when trying to store underlying object somewhere else.

## Comment 1049198847

other (CONTRIBUTOR) · Merovius · 2022-02-23T20:42:59Z · https://github.com/golang/go/issues/51317#issuecomment-1049198847

> The point I was trying to make is that going straight to adding language level support for a very specific pattern seems a bit rushed.

That is not the plan. The plan is to add a new package. That's a library-change, not a language change.

> What is the cost benefit analysis on making this change to the language? You get a 15%-20% speedup on some very specific scenarios on x86-64 linux

I don't think the scenarios are *that* specific. Approximately every request-based server could benefit from it without too much intrusiveness. i.e. ~every HTTP or (g)RPC server. That's a large slice of the Go ecosystem.

They are, however, specific enough to IMO justify that the problems aren't *that* likely. It is relatively easy to document "the Handler is not allowed to retain the request message" and keeping to that - and detecting if you don't via tests.

## Comment 1049200235

reporter (CONTRIBUTOR) · danscales · 2022-02-23T20:44:57Z · https://github.com/golang/go/issues/51317#issuecomment-1049200235

> > Yes, that is true. It is possible there is another implementation that could deal with that many arenas simultaneously. But I will note that if you have 100s of requests in flight at one time, then they may not be allocating that much new data while serving each individual request, so arenas may not really be required in that case. Arenas are really more useful/appropriate for unmarshalling large data objects for which you may do a lot of processing. sync.Pool may be more appropriate if the allocated data per request is small (since there may also be only a limited number of known object types).
> 
> What message sizes/throughputs was the prototype tested at? Many small requests/responses is certainly the norm in my background, but I know google was looking hard (I believe?) a Vitess blog post that mainly dealt with very large data replication messages. Certainly if proto performance gets worse than status quo at high throughput levels, many people wouldn't be thrilled with that.

As mentioned, the performance gains are expected for dealing with large messages that are being unmarshaled or building large data structures during processing that can all be freed at once.  Even if a package (such as protobuf) adds support for an arena allocator, its use is entirely optional.  For a program that is dealing with all small requests and message sizes, the program would just not specify an arena allocator when unmarshaling, so the normal heap allocation be used, so there would be no reduction in performance.  Arenas would only be used after experimentation to determine if they are noticeably improving performance.



## Comment 1049200818

other (CONTRIBUTOR) · Merovius · 2022-02-23T20:45:42Z · https://github.com/golang/go/issues/51317#issuecomment-1049200818

@creker 

> as others already pointed out arena allocations will force developers to always keep in mind that some memory might be arena allocated and they can’t simply store it for later use.

As others have pointed out as well, you *already* have to keep that in mind. It is very common to have requirements like this. It is simply not true that you can assume that any pointer is safe to store in a global data-structure or otherwise to retain (which is the main concern).

## Comment 1049208195

other (NONE) · CannibalVox · 2022-02-23T20:55:46Z · https://github.com/golang/go/issues/51317#issuecomment-1049208195

This discussion does make me consider one serious concern: **strings**.

In the above proposal, downstream code that is not aware of the arena (or may have been written before the existence of arenas!) seems to need to be aware that arenas may exist in order to avoid doing completely normal things with arena-allocated strings.

All of this goes back to my understanding of how arenas *should* work, which is that the user who allocates the arena is responsible for controlling what downstreams they send them to. The string thing seems like such a huge surprise though that I don't think you'll be able to adequately prepare anybody for that behavior even if the arena author is aware of their repsonsibilities.

It may be that there does need to be some language-level support. An `ArenaPointer[T]` type that the compiler considers interchangeable with T- that is, you can call all the same methods and access all the same fields as T, but there is a type-safe check that everyone understands what is going on, and an `ArenaString` that is unambiguously different.  Methods to convert a pointer to a heap copy and an `unsafe` method that will give you the underlying T/string. That seems like a howitzer compared to the proposal, but the string thing really does spook me. That seems like it is going to cause unexpected problems almost constantly.

## Comment 1049209708

reporter (CONTRIBUTOR) · danscales · 2022-02-23T20:57:52Z · https://github.com/golang/go/issues/51317#issuecomment-1049209708

> > [I]f you have 100s of requests in flight at one time, then they may not be allocating that much new data while serving each individual request, so arenas may not really be required in that case. Arenas are really more useful/appropriate for unmarshalling large data objects for which you may do a lot of processing.
> 
> This seems to restrict the subset of apps that would benefit from this incarnation of arenas somewhat significantly. The added focus on protobufs makes me think that the authors have a very specific set of applications in mind.
> 
> Is such an intrusive change worth the 15% speed gain for a subset of apps of unknown size?

It's definitely reasonable to question how useful arenas will be vs how "intrusive".  Their use is entirely  optional, and the only user-visible change would likely be the appearance of a new arena package with its API (no language change).   So, for most users they shouldn't be "intrusive".  But it is good to discuss if arenas puts a burden on package/library writers, and/or if there are rules about usage of arenas that can minimize that burden.




## Comment 1049211413

other (NONE) · CannibalVox · 2022-02-23T21:00:14Z · https://github.com/golang/go/issues/51317#issuecomment-1049211413

> What is the cost benefit analysis on making this change to the language? You get a 15%-20% speedup on some very specific scenarios on x86-64 linux at the cost of added complexity for every user of the language irrespective of them using the feature or not.

My argument is that a (properly implemented) arena only increases complexity for those who choose to use it. There's a lot of stdlib features I've never personally interacted with that exist for situational use. I think that there's a strong argument that arenas CANNOT be satisfactorily implemented outside golang/go and it's very much a "put it here or not at all" thing.

## Comment 1049219278

other (NONE) · creker · 2022-02-23T21:10:37Z · https://github.com/golang/go/issues/51317#issuecomment-1049219278

@Merovius it’s true that you can’t assume any pointer is safe to store but it is in most cases unless documented otherwise which is quiet rare in my practice. Arena essentially puts a huge burden on library writers. Either they have to painstakingly document every function or make sure any public API returns non arena allocated copies. Without arena allocation that’s relatively easy - you just forget the object and let it go. With arena you have to carefully examine whole execution path to find where the object come from and whether it’s arena allocated. Yes, you can imagine using special naming scheme for arena allocated variables or cases where even letting go of some object is dangerous because some internal structure might still retain it. But it still feels like arena allocation makes it even more complex and dangerous for no good reason. And at least with wrappers there’s some additional barrier. Either that or get rid of Free and let GC worry about when arena is safe to deallocated. But then the question is, will it be performant enough to warrant the complexity.

## Comment 1049223269

other (NONE) · AndrewHarrisSPU · 2022-02-23T21:15:54Z · https://github.com/golang/go/issues/51317#issuecomment-1049223269

> and/or if there are rules about usage of arenas that can minimize that burden.

I'm wondering if there's an opportunity to provide a (separately packaged?) complementary API that nudges towards the less pathological patterns of concurrency using arenas. Is this something where 80% or 90% of the use cases are going to be solving the same problems?

## Comment 1049224212

other (NONE) · CannibalVox · 2022-02-23T21:17:11Z · https://github.com/golang/go/issues/51317#issuecomment-1049224212

> Either they have to painstakingly document every function or **make sure any public API returns non arena allocated copies.**

I would describe this as the correct use of arenas to begin with. Arenas should not last beyond the stack they're allocated in, and stuff allocated via the arena should not escape the call graph beneath that function.

Maybe that's the answer? Require arena allocation on the stack, if an arena pointer escapes a method where the arena that allocated it is on the stack, move it to the heap, ban assigning arena pointers to anything on the heap (or auto-heapify it if you try to assign it to something on the heap)

## Comment 1049230653

maintainer (MEMBER) · jimmyfrasche · 2022-02-23T21:25:55Z · https://github.com/golang/go/issues/51317#issuecomment-1049230653

Would this provide as significant an improvement with a generational GC? I'm sure it would still be faster, but would it still be enough to be worth it?

## Comment 1049235551

other (NONE) · creker · 2022-02-23T21:32:58Z · https://github.com/golang/go/issues/51317#issuecomment-1049235551

@CannibalVox yes but the point I’m getting at, who’s gonna enforce it? Or is it another case of “assume developers understand all the caveats”. There’s already too many cases of that in Go and this adds another. That’s why I feel like there needs to be either some barrier in convenience or make it smarter so that incorrect usage is simply impossible. Automatically making objects escape sounds like a great idea.

## Comment 1049237565

other (NONE) · CannibalVox · 2022-02-23T21:35:52Z · https://github.com/golang/go/issues/51317#issuecomment-1049237565

> @CannibalVox yes but the point I’m getting at, who’s gonna enforce it? Or is it another case of “assume developers understand all the caveats”. There’s already too many cases of that in Go and this adds another. That’s why I feel like there needs to be either some barrier in convenience or make it smarter so that incorrect usage is simply impossible. Automatically making objects escape sounds like a great idea.

I would like the auto-escape, I feel like the compiler already understands the situations where an arena object need to evaluate whether it needs to move to the heap, so hopefully that's possible.

However, I don't think "don't return objects that you, personally, have just freed on the previous line of code" is that tough of a sell. I'm definitely more concerned with situations where an engineer did not expect arena pointers to be persisted, like basically anything involving strings.

## Comment 1049254420

other (CONTRIBUTOR) · Merovius · 2022-02-23T21:58:36Z · https://github.com/golang/go/issues/51317#issuecomment-1049254420

@creker I get the impression you are overestimating how common usages of arenas are going to be. There are a handful of use-cases for them and you are only affected by them, as a library author, if you decide to do so. And even then, their use will be limited to a couple of places.

I think it's instructive to look at a concrete use-case: An RPC server. In that case, the documentation will be "a handler might not retain a pointer to the request message". And the pointer to keep track of (for the framework author) will be that single request message. That's not a huge burden.

Apart from that, yes, as a library *user* you need to read documentation that says "don't retain such and such pointers", but again, it's fairly common that you have to do that anyways.

FWIW I've been trying to come up with places where I might use arenas. I can't think of any. And that's not for lack of worry about doing lots of small allocations - it's that arenas are just not the right tool for the jobs I have that problem with.

## Comment 1049264155

other (NONE) · creker · 2022-02-23T22:11:30Z · https://github.com/golang/go/issues/51317#issuecomment-1049264155

@Merovius that’s only if we assume that developers themselves understand that they should almost never use arenas. But if we look at sync.Pool which is everywhere I don’t think that would hold true. Especially if people are coming from other languages where arenas are very popular like C++. Eventually arenas would get into many packages regardless of actual need for it and Go ecosystem would suffer if arenas are as fragile as proposed. The notion that allocations are a bane of existence of every Go developer is very much popular. 

## Comment 1049264350

other (NONE) · hakihet · 2022-02-23T22:11:46Z · https://github.com/golang/go/issues/51317#issuecomment-1049264350

seems like a hassle with little benefit. where is the simplicity? the line between spec and implementation is blurring. Where is the CL?

## Comment 1049274064

other (CONTRIBUTOR) · Merovius · 2022-02-23T22:25:35Z · https://github.com/golang/go/issues/51317#issuecomment-1049274064

@creker Your concern was "it places a huge burden on library authors". ISTM that you are now saying that burden is mostly self-inflicted by people using it where they shouldn't. So, maybe that burden is a bug, not a feature of the design.

FWIW that there are a couple APIs that interact with the GC, which are similarly dangerous. `runtime.SetFinalizer`, for example. Or the [accepted proposal for pointer-pinning](https://github.com/golang/go/issues/46787#issuecomment-959789582). And `sync.Map` also tends to be abused by people (but TBF is rarely ever harmful). I don't think we should necessarily let us deter from adding useful APIs, to protect people from themselves.

## Comment 1049316607

other (CONTRIBUTOR) · Merovius · 2022-02-23T23:21:44Z · https://github.com/golang/go/issues/51317#issuecomment-1049316607

@danscales In case you missed it, I would like to [push my earlier question](https://github.com/golang/go/issues/51317#issuecomment-1048818944): Why does the design rely on the intent for users to call `Free`? I think if we can rely on finalizers, a lot of the pushback in this issue would be resolved, as most usages can be made fully transparent. That also would make them more generally useful, as the need to call `Free` makes them prohibitive for many applications.

## Comment 1049335054

other (NONE) · CannibalVox · 2022-02-23T23:39:18Z · https://github.com/golang/go/issues/51317#issuecomment-1049335054

> @danscales In case you missed it, I would like to [push my earlier question](https://github.com/golang/go/issues/51317#issuecomment-1048818944): Why does the design rely on the intent for users to call `Free`? I think if we can rely on finalizers, a lot of the pushback in this issue would be resolved, as most usages can be made fully transparent. That also would make them more generally useful, as the need to call `Free` makes them prohibitive for many applications.

The design does include a finalizer for arenas, but I don't see how that changes anything: there are plenty of situations where the arena can be GC'd but its allocations are glued to something.

## Comment 1049337738

reporter (CONTRIBUTOR) · danscales · 2022-02-23T23:44:33Z · https://github.com/golang/go/issues/51317#issuecomment-1049337738

@Merovius See the section in the proposal "Removing arena free" in the "Rationale" section.  We find that arenas do not give any improvement in performance on (and can make things worse) if arenas don't have an explicit `arena.Free` and instead are only freed when the garbage collectors notices that there are no more pointers to the arena or the objects in the arena.  One of the big wins of arenas (where they can be applied) is that the memory can be almost immediately reused at the point of the arena free, rather than waiting for a complete GC cycle.  And, if most memory is allocated and freed via arenas, you may actually decrease how often the garbage collector needs to be called. 


## Comment 1049370745

other (NONE) · apg · 2022-02-24T00:46:50Z · https://github.com/golang/go/issues/51317#issuecomment-1049370745

The conversation seems to be going back and forth between:

1. "Arenas aren't generally useful and puts too much burden on the programmer to ensure no heap objects point into an arena allocation."
2. "Arenas are really useful for specific use cases, and in those use cases there's no need to have heap objects point into an arena allocation, therefore there's no problem."

Maybe there's a compromise here where the API is designed in such a way as to indicate that it's a temporary workspace. Some languages have a `with` or `with-x-y-z` pattern that takes a block, or lambda and cleans up the managed thing afterwards (transaction, file, etc):

```
var (
   result Something
   err error
)
arena.With(func(a arena.Page) {
   var ptrT *T
   a.New(&ptrT)
   ... go about your business
})
```

Yes, it allocates a closure. But, we're already used to the semantics of calling functions and having the stack space be cleaned up. That's essentially what we're trying to achieve with arenas. Perhaps unfortunately, the fact that Go does escape analysis for stack allocations won't work the same for arena allocations, and there will certainly be bugs associated with it. But maybe that's lintable?

## Comment 1049377886

other (NONE) · CannibalVox · 2022-02-24T00:59:18Z · https://github.com/golang/go/issues/51317#issuecomment-1049377886

> The conversation seems to be going back and forth between:
> 
> 1. "Arenas aren't generally useful and puts too much burden on the programmer to ensure no heap objects point into an arena allocation."
> 2. "Arenas are really useful for specific use cases, and in those use cases there's no need to have heap objects point into an arena allocation, therefore there's no problem."
> 
> Maybe there's a compromise here where the API is designed in such a way as to indicate that it's a temporary workspace. Some languages have a `with` or `with-x-y-z` pattern that takes a block, or lambda and cleans up the managed thing afterwards (transaction, file, etc):
> 
> ```
> var (
>    result Something
>    err error
> )
> arena.With(func(a arena.Page) {
>    var ptrT *T
>    a.New(&ptrT)
>    ... go about your business
> })
> ```
> 
> Yes, it allocates a closure. But, we're already used to the semantics of calling functions and having the stack space be cleaned up. That's essentially what we're trying to achieve with arenas. Perhaps unfortunately, the fact that Go does escape analysis for stack allocations won't work the same for arena allocations, and there will certainly be bugs associated with it. But maybe that's lintable?

Two things:

1. Do we actually, really, truly, foresee engineers not being able to wrap their minds around what an arena is and what it does? I understand that you personally are not taking a position on this question in your comment here, but a lot of the discussion around the difficulty of using arenas seems to focus on the idea that somebody might just not really understand that when they call arena.Free(), the memory they have allocated by the arena... will be freed. That seems completely incredible to me. 
2. This idea does not actually prevent anyone from escaping arena-allocated data, nor does it make it especially harder to do so by accident. I assume that in any case where there was a problem, there's still a problem.

## Comment 1049381156

other (CONTRIBUTOR) · randall77 · 2022-02-24T01:04:59Z · https://github.com/golang/go/issues/51317#issuecomment-1049381156

Just to clarify, @bcmills said

> Arena-allocated string values, which are functionally more like slices: they are no longer safe to read after a call returns, and not guaranteed to have stable contents over time.

They *are* guaranteed to have stable contents over time. They either have their originally allocated contents, or they crash the program when accessed. In no situation would they successfully look like a different string than their original contents.

Similarly, arenas are better than the `sync.Pool` allocation scheme that some have proposed as an alternative. If you use a `sync.Pool` to do allocation, you run the risk of use-after-free bugs ("free" = return to pool) that are undetectable. With arenas, a use-after-free either still gives you the correct contents, or crashes the program. In no case will you mistakenly read (or be otherwise aliased to) the contents of some unrelated allocation as you would with a `sync.Pool` implementation.


## Comment 1049404042

other (NONE) · apg · 2022-02-24T01:29:01Z · https://github.com/golang/go/issues/51317#issuecomment-1049404042



> On Feb 23, 2022, at 16:59, Stephen Baynham ***@***.***> wrote:
> Do we actually, really, truly, foresee engineers not being able to wrap their minds around what an arena is and what it does? I understand that you personally are not taking a position on this question in your comment here, but a lot of the discussion around the difficulty of using arenas seems to focus on the idea that somebody might just not really understand that when they call arena.Free(), the memory they have allocated by the arena... will be freed. That seems completely incredible to me.
Mind boggling, I know! 


> This idea does not actually prevent anyone from escaping arena-allocated data, nor does it make it especially harder to do so by accident. I assume that in any case where there was a problem, there's still a

Yup! Fully acknowledged that there are problems with this idea. The obvious advantage is the isomorphism with stack allocation. But, with this being a library, and not, say, a new type of language level construct, is there actually a way to prevent these types of problems? I think a defensive API and clear documentation are the best bets.




## Comment 1049405166

other (NONE) · apg · 2022-02-24T01:31:23Z · https://github.com/golang/go/issues/51317#issuecomment-1049405166



> On Feb 23, 2022, at 17:05, Keith Randall ***@***.***> wrote:
> 
> With arenas, a use-after-free either still gives you the correct contents, or crashes the program.

Arguably, `Free` should zero the underlying memory to ensure a crash as early as possible…

## Comment 1049411766

other (CONTRIBUTOR) · randall77 · 2022-02-24T01:46:29Z · https://github.com/golang/go/issues/51317#issuecomment-1049411766

> Arguably, `Free` should zero the underlying memory to ensure a crash as early as possible…

The proposal uses unmapping as the mechanism to ensure crashes. Because unmapping is somewhat expensive, the proposal batches them up to lower overhead, but that of course leaves a window where an object is freed but still accessible. Perhaps there should be a debug mode where unmapping is immediate. (Maybe when running with `-race`? That's kind of the grab-bag that we throw expensive debugging things into, but it might be appropriate here.)

I don't think just zeroing is a good idea. It may cause quick crashes on pointer data, but may just cause incorrect computation (especially on nonpointer data, but potentially on pointer data as well).



## Comment 1049411860

other (CONTRIBUTOR) · zephyrtronium · 2022-02-24T01:46:41Z · https://github.com/golang/go/issues/51317#issuecomment-1049411860

@CannibalVox 
> ... a lot of the discussion around the difficulty of using arenas seems to focus on the idea that somebody might just not really understand that when they call arena.Free(), the memory they have allocated by the arena... will be freed. That seems completely incredible to me.

Speaking as someone who spends a fair amount of time teaching new Go programmers, I don't think that's particularly incredible at all. Ideally, nothing in Go makes you think about memory being freed. That's a C concept. In Go, Java, Python, &c. it only applies in edge cases, and then only as an implementation detail. Hence, my reservations about this proposal come from the pedagogical perspective.

## Comment 1049423459

other (CONTRIBUTOR) · bcmills · 2022-02-24T02:09:29Z · https://github.com/golang/go/issues/51317#issuecomment-1049423459

> [Arena-allocated strings] are guaranteed to have stable contents over time. They either have their originally allocated contents, or they crash the program when accessed. In no situation would they successfully look like a different string than their original contents.

That's better than it could be, but I still wouldn't describe a thing that decays into a poison-pill that crashes your program as “stable contents”. 😅

## Comment 1049511657

other (NONE) · reusee · 2022-02-24T05:36:30Z · https://github.com/golang/go/issues/51317#issuecomment-1049511657

> Also, it is not intended that arenas be shared across goroutines. Each arena has a lock to protect against simultaneous allocations by multiple goroutines, but it would be very inefficient to actually use the same arena for multiple goroutines. Of course, that would rarely make sense anyway, since the lifetimes of objects allocated in different goroutines are likely to be quite different.

We can just add heap-less functions that allocate all objects on stacks and panic on heap-escaping since arenas are bounded to goroutines.

## Comment 1049616510

other (CONTRIBUTOR) · Merovius · 2022-02-24T08:40:07Z · https://github.com/golang/go/issues/51317#issuecomment-1049616510

@danscales Darn, don't know how I overlooked that. That makes me feel a lot worse about this proposal, as it really requires exposing arenas in the API to be useful. I feel like performance optimizations like this should be implementation details of packages. But okay, that's that, then.

## Comment 1049994101

other (NONE) · CannibalVox · 2022-02-24T15:47:41Z · https://github.com/golang/go/issues/51317#issuecomment-1049994101

> > Also, it is not intended that arenas be shared across goroutines. Each arena has a lock to protect against simultaneous allocations by multiple goroutines, but it would be very inefficient to actually use the same arena for multiple goroutines. Of course, that would rarely make sense anyway, since the lifetimes of objects allocated in different goroutines are likely to be quite different.
> 
> We can just add heap-less functions that allocate all objects on stacks and panic on heap-escaping since arenas are bounded to goroutines.

Arena allocated objects need to be able to be returned back to the arena root without issue which is escape from the method that allocated it (and anyway, prevents it from living on the stack)

## Comment 1050029713

other (NONE) · CannibalVox · 2022-02-24T16:23:56Z · https://github.com/golang/go/issues/51317#issuecomment-1050029713

I went back and re-read the vitess blog post that started this whole thing (https://vitess.io/blog/2021-06-03-a-new-protobuf-generator-for-go/) and I couldn't help but notice a couple things:

A) First of all, their results from using a sync.Pool were much better than 15%. I'm like 90% sure that's because of the honking huge messages they're passing around, but it does make me very curious about the prototype being discussed here.
B) Second of all, they were not syncpooling strings. I'm pretty sure all their strings are still coming off the heap, and their grpc requests for this case surely contain more strings than the average implementation. What would the results of the prototype be if strings were exempted from the arena? If putting strings on the heap does not change the outcome substantially, I think there's a strong argument for exempting them.

E: Also what would the results be of syncpooling arenas instead of generating brand new ones? I use this strategy with a cgo library I built (free "excessive" allocations, wipe out the bookkeeping in the remaining pages, and return the arena to a syncpool) and the performance is quite an improvement.  Obviously this would make the consequences of holding freed pointers even more baffling, but I would like to know what the performance cost of that clarity is.

## Comment 1050148853

other (CONTRIBUTOR) · timothy-king · 2022-02-24T18:39:57Z · https://github.com/golang/go/issues/51317#issuecomment-1050148853

@danscales Thank you for the well put together proposal. (I am not sure I am in favor of it or not yet but I do appreciate it.)

1. Are there any cases studies you can share with how usage of the proposed API has played out in practice? My worry is that understanding the implications of the lifetimes bleeds into APIs clients are putting together. Tell tale signs would be comments on exposed functions that describe the lifetimes of return values or something similar, such as `func Foo(ctx context.Context) string // do not keep string alive longer than ctx as it is in an arena`. The question is how much this impacts API design. Case studies would maybe clarify this. If we do not have case studies, does it make sense for such an arenas package to be made available outside of the standard library while data is being gathered?

2. I am struggling to reconcile when the "free" of an object happens based on two different sections. My understanding of the following is that semantically it is a bug to use-after-free any "freed" object.
> After this call, the application should not access the arena again or dereference a pointer to any object allocated from this arena. The implementation is required to cause a run-time erro and terminate the Go program if the application accesses any object whose memory has already been freed

My understanding of this second section is that the "free" of an object happens at some point after Free but at the discretion of the runtime.

> For optimization purposes, the implementation is allowed to delay actually freeing an arena or its contents. If this optimization is used, the application is allowed to proceed normally if an object is accessed after the arena containing it is freed, as long as the memory of the object is still available and correct (i.e. there is no chance for incorrect behavior). In this case, the improper usage of arena.Free will not be detected, but the application will run correctly, and the improper usage may be detected during a different run.

The first section heavily suggests to me that using an object after `Free` for the allocating arena is called is a bug. It also states the user is promised a crash. The second section says there is some other internal decision for an object is actually freed by the runtime (based on some kinda vague criteria). Reading from these values may be a 'correct behavior' (e.g. not a bug). Can we spell out in more detail what users can expect for when the true "free" happens and when it is a bug to access the object?

3. [Very minor point for tool developers] Do we know which plain Go expressions (only go, no unsafe, no races, etc.) transition from cannot panic to may panic? Is it just operations on strings or are there more?

## Comment 1050155746

other (CONTRIBUTOR) · Merovius · 2022-02-24T18:48:58Z · https://github.com/golang/go/issues/51317#issuecomment-1050155746

@timothy-king 

> Can we spell out in more detail what users can expect for when the true "free" happens and when it is a bug to access the object?

AIUI "at some point after `Free` is called, determined by the runtime". Accessing a pointer into the arena after `Free` is called is always a bug, but it might not panic. But the runtime *is* required to make it panic, if it could cause unsafe behavior (i.e. if it actually released the memory of the arena for re-use).

That is, your interpretation

> Reading from these values may be a 'correct behavior' (e.g. not a bug).

is incorrect. It might not panic, but it *is* a bug.

## Comment 1050157554

other (CONTRIBUTOR) · zeebo · 2022-02-24T18:51:22Z · https://github.com/golang/go/issues/51317#issuecomment-1050157554

> Perhaps there should be a debug mode where unmapping is immediate. (Maybe when running with `-race`? That's kind of the grab-bag that we throw expensive debugging things into, but it might be appropriate here.)

I agree with this. Having some mechanism, even if it's not `-race`, to tickle out the use-after-free bugs as soon as possible I think is very important.

Some questions:

1. The doc string on the `Free` method says
> Applications must not call any method on this after it has been freed.

Does that mean that calling `Free` twice fails in some way? If so, how? Also, I'd suggest that allowing `Free` to be called multiple times would be helpful.

2. The implementation calls `SetFinalizer` on the arena. What happens if a user also calls `SetFinalizer`? If it's anything problematic, maybe that should be called out in documentation.

## Comment 1050173826

other (CONTRIBUTOR) · timothy-king · 2022-02-24T19:12:29Z · https://github.com/golang/go/issues/51317#issuecomment-1050173826

@Merovius

> AIUI "at some point after Free is called, determined by the runtime". Accessing a pointer into the arena after Free is called is always a bug, but it might not panic. But the runtime is required to make it panic, if it could cause unsafe behavior (i.e. if it actually released the memory of the arena for re-use).

That makes sense to me. I am just not sure it is what the proposal is saying.

> It might not panic, but it is a bug.

The proposal currently describes this as "the application will run correctly". It is possible I am reading too much into the word "correctly".

(My guess is your interpretation is correct, but the proposal may need to be edited.)

## Comment 1050182899

other (CONTRIBUTOR) · Merovius · 2022-02-24T19:20:07Z · https://github.com/golang/go/issues/51317#issuecomment-1050182899

@timothy-king A buggy program might, occasionally, run correctly.

Compare that to a program containing a data-race. The race will not always actually cause incorrect values to be written and the program will not always run incorrectly. Most of the time it will run just fine. But it is still a buggy program.

I think the proposal describes what's intended to be happening pretty unambiguously. The point it's trying to make is that under an implementation of this proposal, even a program containing a use-after-free bug should always either a) panic or b) run correctly - it should never cause undefined behavior.

## Comment 1050228464

reporter (CONTRIBUTOR) · danscales · 2022-02-24T20:20:11Z · https://github.com/golang/go/issues/51317#issuecomment-1050228464

> @timothy-king
> 
> > Can we spell out in more detail what users can expect for when the true "free" happens and when it is a bug to access the object?
> 
> AIUI "at some point after `Free` is called, determined by the runtime". Accessing a pointer into the arena after `Free` is called is always a bug, but it might not panic. But the runtime _is_ required to make it panic, if it could cause unsafe behavior (i.e. if it actually released the memory of the arena for re-use).
> 
> That is, your interpretation
> 
> > Reading from these values may be a 'correct behavior' (e.g. not a bug).
> 
> is incorrect. It might not panic, but it _is_ a bug.

Yes, @Merovius , that is a good explanation.  It is considered a use-after-free bug if an object allocated from an arena is accessed after the arena is freed.   The implementation will often panic at the buggy access, but it is allowed to not panic if it can provide completely correct behavior (because the object is still accessible with correct contents).  The program is guaranteed to have completely correct, defined behavior up to completion or to a panic (maybe because of another buggy access).

It definitely may make sense to have a debug mode where arenas are always immediately freed/unmapped, so that such buggy accesses are always caught (with a panic) if they occur in the debug mode.


## Comment 1050234193

other (NONE) · creker · 2022-02-24T20:27:29Z · https://github.com/golang/go/issues/51317#issuecomment-1050234193

@danscales why don't we panic immediatelly after Free is called? Why do we need debug mode or allow any access after Free regardless of whether contents are still valid or not? If it is a bug, which we all seem to agree, then why allow it to go unnoticed. I suspect that would require less efficient implementation but I feel like it's a worthy tradeof.

## Comment 1050237991

maintainer (MEMBER) · thepudds · 2022-02-24T20:32:46Z · https://github.com/golang/go/issues/51317#issuecomment-1050237991

Perhaps the default mode could immediately unmap the virtual address range with some low probability immediately upon Free, in order to help trigger failure during testing. The probability could be low enough that it doesn’t materially impact performance. 

## Comment 1050245170

maintainer (MEMBER) · thepudds · 2022-02-24T20:42:13Z · https://github.com/golang/go/issues/51317#issuecomment-1050245170

Hi @creker

> why don't we panic immediatelly after Free is called?

FWIW, the proposal says the performance benefit of batching is significant:

> Because unmapping memory is relatively expensive, the implementation may continue to use a chunk for consecutively allocated/freed arenas until it is nearly full. When an arena is freed, all of its chunks that are filled up are immediately freed and unmapped. However, the remaining part of the current unfilled chunk may be used for the next arena that is allocated. This batching improves performance significantly.

## Comment 1050245256

other (CONTRIBUTOR) · Merovius · 2022-02-24T20:42:19Z · https://github.com/golang/go/issues/51317#issuecomment-1050245256

@creker 

> why don't we panic immediatelly after Free is called?

As a potential performance optimization. It requires unmapping and unmapping is expensive. OTOH, by allowing the runtime to delay it, there are situations where unmapping can be avoided - if the GC determines that no pointer into the arena remains, it is safe to re-use the memory for a new arena, without unmapping it. And even if it can't be *avoided*, the runtime might benefit from the flexibility to delay and do it in the background, when it has extra cycles.

@thepudds Personally, I feel that there is no super material difference between "panic with a low probability, because we throw a weighted dice" and "panic with a low probability, because the runtime might sometimes immediately unmap". Personally, I don't like tests which occasionally fail.

## Comment 1050248212

other (CONTRIBUTOR) · Merovius · 2022-02-24T20:46:16Z · https://github.com/golang/go/issues/51317#issuecomment-1050248212

@creker FWIW, the comparison to data races might again be helpful. If a data race is always a bug and we have a tool to detect them with high confidence (the race detector), why don't we always use that tool? Well, because it has a hugely negative performance impact.

## Comment 1050257967

other (NONE) · creker · 2022-02-24T20:58:30Z · https://github.com/golang/go/issues/51317#issuecomment-1050257967

@Merovius I was thinking about some way to flag arena allocated objects as "invalid" but it's not obvious how this can be done without affecting every object access. Essentially it would mean permanent "barrier" of sorts on every object access even if it's not arena allocated.

## Comment 1050293704

other (CONTRIBUTOR) · Merovius · 2022-02-24T21:42:21Z · https://github.com/golang/go/issues/51317#issuecomment-1050293704

@creker The most efficient way to do it is the way the design does it - unmapping the pages, so the hardware does the checking for you. But while it's the most efficient way, it still has an appreciable cost.

## Comment 1051042326

other (CONTRIBUTOR) · extemporalgenome · 2022-02-25T17:19:26Z · https://github.com/golang/go/issues/51317#issuecomment-1051042326

> > why don't we panic immediatelly after Free is called?
> 
> As a potential performance optimization. It requires unmapping and unmapping is expensive.

@creker @Merovius perhaps then the implementation should force some frees to be immediate, based on some pseudorandom roll, and if the runtime has instrumentation for it, immediately unmap the first arena free called from a given code location. This would retain the optimization in nearly all cases, but like random map iteration and random case handling in select, would uncover buggy behavior quickly.

## Comment 1051063895

other (CONTRIBUTOR) · Merovius · 2022-02-25T17:46:42Z · https://github.com/golang/go/issues/51317#issuecomment-1051063895

@extemporalgenome To have no noticeable performance impact, I'd guess the pseudo-random rate would have to be on the order of single-digit percentages of `Free` operations. In other words, low enough that you just end up with frustratingly flaky tests and unreproducible panics happening in production, but not enough to actually rely on for CI.

But, I'm not super opposed to the idea of pseudo-random immediate unmapping - as long as we *also* [make it happen on `-race` or an equivalent catch-all flag for these kinds of debugging](https://github.com/golang/go/issues/51317#issuecomment-1049411766). So those of us who prefer their tests to be as reliable as possible can use that. And those who observe panics in production can reproduce them reliably.

## Comment 1051125627

other (CONTRIBUTOR) · RLH · 2022-02-25T19:17:25Z · https://github.com/golang/go/issues/51317#issuecomment-1051125627

Use of finalizers to free arenas should be a programming choice not a promise of the arena implementation. There is tension between memory management using an arena approach and one using a GC approach. The arena API should enforce that an arena is created and freed under explicit program control. The program needs to be architected so that the Free point is explicit and can be reasoned about. The arena implementation’s use of a finalizer to free an unreachable arena is at its heart a GC wart that could lead to variations in performance that would be hard to diagnose.

In support of avoiding finalizers one can point to the successful use of arenas in languages without GC so any use case needing finalizers would seem to be new and unique to Go. One can also point to the deprecation of finalizers in Java as a warning about the construct in general. Finally, if a finalizer is really needed it can be added to the program as an aid to code reviewers and not maintained as legacy in the arena implementation.


## Comment 1051138132

other (NONE) · CannibalVox · 2022-02-25T19:35:57Z · https://github.com/golang/go/issues/51317#issuecomment-1051138132

> Use of finalizers to free arenas should be a programming choice not a promise of the arena implementation. There is tension between memory management using an arena approach and one using a GC approach. The arena API should enforce that an arena is created and freed under explicit program control. The program needs to be architected so that the Free point is explicit and can be reasoned about. The arena implementation’s use of a finalizer to free an unreachable arena is at its heart a GC wart that could lead to variations in performance that would be hard to diagnose.
> 
> In support of avoiding finalizers one can point to the successful use of arenas in languages without GC so any use case needing finalizers would seem to be new and unique to Go. One can also point to the deprecation of finalizers in Java as a warning about the construct in general. Finally, if a finalizer is really needed it can be added to the program as an aid to code reviewers and not maintained as legacy in the arena implementation.

I agree with this specifically, but maybe more generally, I think the proposal needs to decide on a level of danger and stick with it. Arenas as-proposed are rather dangerous to use so the finalizer definitely stands out as an unusual component of the proposal. By contrast, if changes were made to the proposal to make it much safer, the finalizer aspect would be of a piece with that. It doesn't make sense to me to guarantee that the arena memory will be garbage collected, even if drastically misused, if we are not guaranteeing that arena memory will not panic if moderately misused.

On the other hand, it could be that the Finalizer exists specifically to allow GC in cases of a recovered panic.  In that case, I would argue that @apg 's suggestion of using a closure would be a better way to achieve the same result.

## Comment 1051286712

reporter (CONTRIBUTOR) · danscales · 2022-02-25T21:32:12Z · https://github.com/golang/go/issues/51317#issuecomment-1051286712

> Use of finalizers to free arenas should be a programming choice not a promise of the arena implementation. There is tension between memory management using an arena approach and one using a GC approach. The arena API should enforce that an arena is created and freed under explicit program control. The program needs to be architected so that the Free point is explicit and can be reasoned about. The arena implementation’s use of a finalizer to free an unreachable arena is at its heart a GC wart that could lead to variations in performance that would be hard to diagnose.
> 
> In support of avoiding finalizers one can point to the successful use of arenas in languages without GC so any use case needing finalizers would seem to be new and unique to Go. One can also point to the deprecation of finalizers in Java as a warning about the construct in general. Finally, if a finalizer is really needed it can be added to the program as an aid to code reviewers and not maintained as legacy in the arena implementation.

The comments about not having the arena finalizer make sense, especially that it could hide the fact that an `arena.Free` is missing that the programmer meant to add, or, as you say, "lead to variations in performance that would be hard to diagnose".   I included it in the proposal as a possibility for the implementation and for completeness, but it could certainly be eliminated.

Separately, the intent was not to deal with panics via the finalizer - the `arena.Free` calls should already usually be in a defer in order to deal with panics.  (But I note that this is not suggested anywhere in the proposal.)




## Comment 1051383238

other (NONE) · CannibalVox · 2022-02-26T00:02:42Z · https://github.com/golang/go/issues/51317#issuecomment-1051383238

@danscales 
> The comments about not having the arena finalizer make sense, especially that it could hide the fact that an `arena.Free` is missing that the programmer meant to add, or, as you say, "lead to variations in performance that would be hard to diagnose". I included it in the proposal as a possibility for the implementation and for completeness, but it could certainly be eliminated.
> 
> Separately, the intent was not to deal with panics via the finalizer - the `arena.Free` calls should already usually be in a defer in order to deal with panics. (But I note that this is not suggested anywhere in the proposal.)

Thank you for the clarification. Over the past few hours, I've fallen very deeply into the line of thinking I mentioned earlier, that the level of safety in this proposal seems inconsistent. I can't help but feel that there is a general discomfort with putting a feature expected to be used by protobuf into unsafe/runtime, and that is driving some  of the decisions.

If this was, for instance, a subpackage of `unsafe` that gave general access to allocate and deallocate non-garbage-collected memory pages, I believe this proposal would have gotten less pushback than it has, despite being even less safe, because `unsafe` is the appropriate place to put things that can cause the sorts of issues this proposal can.

Obviously there is some discomfort with importing unsafe from grpc, a piece of code that is in almost every deployment running go, it doesn't seem like what the unsafe package is "for".  However, this is still "unsafe" code, whether or not it's in the package. We would ostensibly expect the same level of "knowing what you are doing" from someone who works with these arenas as we would from someone who starts doing pointer arithmetic with unsafe.Pointer.

So I promise I'll pipe down after I say: I think this proposal would be better if it chose a direction.  Either it should find a way to bring the danger into line with something like "sync.Pool" which can mess up your program if you use it wrong but not in the same sort of C++-like way, or it should move to unsafe and take the safeties off completely. Personally, I'd love to see what the latter looks like, but I understand that you have a goal you're trying to achieve here and that may not help you achieve it. 

Thank you for being so patient with all of us as we digest this proposal. It's clearly very well thought out, and I think the final impact is going to be really strong!

## Comment 1051390312

other (NONE) · creker · 2022-02-26T00:17:27Z · https://github.com/golang/go/issues/51317#issuecomment-1051390312

@CannibalVox given the proliferation of JSON packages that use unsafe, I wouldn't say it would be that strange for grpc to use unsafe. On the contrary. Given how important it is it might be worth it to use any ways necessary to increase performance.

## Comment 1051665198

other (CONTRIBUTOR) · Merovius · 2022-02-26T06:16:06Z · https://github.com/golang/go/issues/51317#issuecomment-1051665198

@CannibalVox

> I think this proposal would be better if it chose a direction. Either it should find a way to bring the danger into line with something like "sync.Pool" which can mess up your program if you use it wrong but not in the same sort of C++-like way

Arenas as proposed *are* safe. They can make your program panic, but lots of code can do that. But they can't corrupt your memory and they can't lead to undefined behavior "in the same sort of C++-like way". No offense, but if that's causing the discussion, then people should simply clarify to themselves that the proposal is in fact safe. Their level of safety is comparable with e.g. `strings.Builder`, which can *also* make your program panic, if used incorrectly. [edit] FWIW the one exception is the problem with strings. That seems to be unique to arenas and only possible with `unsafe` otherwise [/edit]

I do think, personally, that `runtime` is the right place for them, because they fundamentally are in the same class of feature as `SetFinalizer`. I feel that analogy is pretty obvious.

## Comment 1052594738

other (CONTRIBUTOR) · martin-sucha · 2022-02-26T20:49:12Z · https://github.com/golang/go/issues/51317#issuecomment-1052594738

> ```go
> // HeapString returns a copy of the input string, and the returned copy
> // is allocated from the heap, not from any arena. If s is already allocated
> // from the heap, then the implementation may return exactly s.  This function
> // is useful in some situations where the application code is unsure if s
> // is allocated from an arena.
> func HeapString(s string) string
> ```
> Of course, this issue of mistakenly using an object from an arena in a global data structure may happen for other types besides strings, but strings are a very common case for being shared across data structures.

What does `HeapString` do if it is passed a string that is not allocated in an arena or on the heap? For example if it is a string literal or if it is allocated on the stack. We should probably update the documentation to mention this case as the current wording suggests HeapString returns a copy while it should probably just return `s`. Should we call the function something different, for example ExtractString?

What are the cases when the application code is unsure if a value is allocated from an arena? It seems that in order to use arenas correctly, the application code must be aware of arenas and know the lifecycle of the objects at all times. Why is a function that conditionally copies better than a function that always copies?

On the other hand, if we want to have something like `HeapString`, why limit it to strings only? It seems we could have a generic version instead.

```go
> // Heap returns a shallow copy of the input, and the returned copy
> // is allocated from the heap, not from any arena. If input is already allocated
> // from the heap, then the implementation may return exactly input.  This function
> // is useful in some situations where the application code is unsure if input
> // is allocated from an arena.
> func Heap[T any](input *T) *T
```

Do we want to allow user code to determine if a value is allocated in an arena? This might be useful if someone wanted to implement a deep copy.

```go
// IsAllocated reports whether v is allocated in an arena.
func IsAllocated[T any](v *T) bool
```

## Comment 1055392320

other (NONE) · dongmu101 · 2022-03-01T12:27:17Z · https://github.com/golang/go/issues/51317#issuecomment-1055392320

I hope I can do better

## Comment 1055831752

reporter (CONTRIBUTOR) · danscales · 2022-03-01T20:29:48Z · https://github.com/golang/go/issues/51317#issuecomment-1055831752

I have uploaded a prototype implementation of Go arenas at https://go-review.googlesource.com/c/go/+/387975 .  This is a functioning, fairly complete implementation, but it is not well tested in its current form for open-source, so it may have bugs, etc.  The implementation is roughly as described in the "Implementation" section of the proposal.  It should be useful for showing what a real implementation could look like, including the size of the change overall and the extent of the integration needed with the Go runtime.



## Comment 1055871325

maintainer (MEMBER) · thepudds · 2022-03-01T21:23:44Z · https://github.com/golang/go/issues/51317#issuecomment-1055871325

Hi @danscales, does the current prototype CL implement this portion from the proposal?

> Pointers that refer to other objects contained in the chunk will be handled very efficiently, while pointers to objects outside the chunk will be followed and marked normally.

And is that expected to be a significant savings in GC CPU time? 

Earlier, I think you said the majority of arena performance benefit stems from more prompt reuse of memory, but part of the reason I am asking the questions above is I am curious if there would be additional use cases such as using an arena for a related set of long-lived objects (for example, memory that will be alive until program end). 

That said, perhaps the mark savings are modest, and the fact that those savings would be just for pointers to objects in the same chunk (and not the same arena) might limit the benefit to using an arena for many long-lived objects.

## Comment 1056637872

maintainer (MEMBER) · rasky · 2022-03-02T09:11:12Z · https://github.com/golang/go/issues/51317#issuecomment-1056637872

The current API worries me in that it makes it explicit that you want some specific allocations to happen in an arena. This can match some use cases where a library wants to internally use Arenas, while leaving its public API unchanged and its users unaware of it. On the other hand, I can think of endless cases where it is not a clear cut whether a family of allocations made by a library during the creation of an object tree should go in an arena or not; it might depend on how the library is *used* instead. This would mean that those libraries might start getting feature requests to enhance their API to be Arena-aware, that is optionally accepting an Arena pointer to use. They would then have to duplicate internally their code paths for both the Arena and the non-Arena case, and their API would now become more polluted.

This recalls me of how context percolates APIs. I don't think we have a better solution for that, but I think most people will agree that purely from a language design perspective, context is not pretty. I'm afraid we are going down the same road here.

Has a call-stack based API been evaluated instead?

```
package arena

// Run calls f. All allocations performed by this gorutine while f is running will happen in a memory arena,
// which is automatically reclaimed when f exits. Objects allocated by f will not valid anymore after f
// exits and must not be accessed
func Run(f func())
```




## Comment 1056898018

maintainer (MEMBER) · sbinet · 2022-03-02T12:53:49Z · https://github.com/golang/go/issues/51317#issuecomment-1056898018

> They would then have to duplicate internally their code paths for both the Arena and the non-Arena case

why do you think that would be the case?
wouldn't it be possible for those libraries to devise a `MemoryAllocator` interface, use that interface in their code base and have two implementations, one w/ the `Arena` and the other with the regular Go allocator?

actually, that's what we did in the Go implementation of the [Apache Arrow](https://github.com/apache/arrow) library:
- https://pkg.go.dev/github.com/apache/arrow/go/arrow@v0.0.0-20211112161151-bc219186db40/memory#Allocator
- https://pkg.go.dev/github.com/apache/arrow/go/arrow@v0.0.0-20211112161151-bc219186db40/memory#GoAllocator

_wrt_ your call-stack based API: I guess that could be as easily (and more explicitly) achieved with a `defer arena.Free()`?
couldn't it?

## Comment 1057185706

maintainer (MEMBER) · adonovan · 2022-03-02T17:24:52Z · https://github.com/golang/go/issues/51317#issuecomment-1057185706

To the question of whether this is a library or a language change: the arena package is fundamentally no different to "unsafe", which also has the potential to create non-nil pointers that explode when dereferenced. Perhaps naming the package "unsafe/arena" would help convey this risk.

But whereas the use of "unsafe" is typically encapsulated within a single data type or function, the arena package seems to demand broader use in other packages' APIs, and may require the plumbing of arena values down the call tree. 

The potentially "viral" aspect of arenas reminds me of C++'s std::allocator; yet fiddly though std::allocator is, it does at least catch certain mistakes during type checking. Previous type systems for arenas such as [Cyclone](https://www.cs.umd.edu/projects/cyclone/papers/cyclone-regions.pdf) led to rather unwieldy programs, though the examples are not so far removed from the kind of type annotations successfully used in Rust. Rust and Go are both more pleasant to use than C++ in large part because they abolish use-after-free mistakes: one statically, by borrow checking, the other dynamically, by garbage collection. We must not give that up.

For me, the viability of this proposal rests on the question of whether it can deliver real optimization benefits while allowing its users to encapsulate local violations of type safety. I would love to see how extensive the required changes were to the protocol buffer API.

## Comment 1057186995

other (NONE) · CannibalVox · 2022-03-02T17:26:19Z · https://github.com/golang/go/issues/51317#issuecomment-1057186995

> I have uploaded a prototype implementation of Go arenas at https://go-review.googlesource.com/c/go/+/387975 . This is a functioning, fairly complete implementation, but it is not well tested in its current form for open-source, so it may have bugs, etc. The implementation is roughly as described in the "Implementation" section of the proposal. It should be useful for showing what a real implementation could look like, including the size of the change overall and the extent of the integration needed with the Go runtime.

This is good stuff- I don't suppose you have the grpc proof of concept available?

## Comment 1057608700

other (NONE) · huskar-t · 2022-03-03T02:40:47Z · https://github.com/golang/go/issues/51317#issuecomment-1057608700

This proposal I think is a good start and a very necessary feature for big data processing, even though using buffer can solve some needs, it would be a very elegant way to optimize memory if you could manually release large memory blocks immediately instead of waiting for gc.

## Comment 1058028053

other (NONE) · mrosenc · 2022-03-03T13:12:12Z · https://github.com/golang/go/issues/51317#issuecomment-1058028053

I don't see how you can avoid attaching this thing to the context. If you don't many other APIs will feel pressure to add arena arguments. If you attempt to keep it as an internal detail in a library, then the library API will instead have to add some kind of Free method, which seems no better than taking an arena argument.  This is different then sync.Pool which can be used for temporary objects, it seems to me that the reason for using arenas and not pools is because you need to tie the scope of many allocated objects to some external thing (request lifetime).

Also to the point of accessing the context on every allocation, I think that is a bit of a straw-man. Libraries will only be interested in using arenas if they are doing a lot of allocations. I imagine they'd pull it out of the context at the top of their call stack and pass it as a normal argument internally.

Context is already viral, and while it's not ideal, it's what we have. It would be better to define methods in the arena package for attaching this to the context so there is a standard that different APIs can use to find it.

## Comment 1058043845

other (NONE) · creker · 2022-03-03T13:31:14Z · https://github.com/golang/go/issues/51317#issuecomment-1058043845

@sbinet 

> I guess that could be as easily (and more explicitly) achieved with a defer arena.Free()?
> couldn't it?

The problem with that approach is that it's just one of many ways of doing it. Call-stack based API forces very specific semantics that would make using arenas much safer. It forces any usage to be finished at the end of the function with no other option. You can launch multiple goroutines with however much nested calls you want but you will always be forced to stop using arena allocated objects at the end of the function. It also limits the possiblity of arenas leaking into public API because you can no longer simply keep arena alive forever. Any arena allocated object you would want to retain would have to be copied. The question is, how well these limitations fit the use cases this proposal is aimed at?

I personally prefer @rasky suggestion. It looks very similar to key erasure proposal which bears some similarities around incorrect usage.

## Comment 1058087197

other (CONTRIBUTOR) · bcmills · 2022-03-03T14:18:21Z · https://github.com/golang/go/issues/51317#issuecomment-1058087197

@mrosenc
> This is different then sync.Pool which can be used for temporary objects, it seems to me that the reason for using arenas and not pools is because you need to tie the scope of many allocated objects to some external thing (request lifetime).

1. I believe that the proposed arenas are strictly safer than `sync.Pool`. With a `sync.Pool`, a use-after-`Put` becomes an aliasing bug, which may or may not be detected during testing. With an arena, a use-after-`Free` becomes a diagnosable panic.

2. As I understand it, the reasons for using arenas and not pools are efficiency and heterogeneity. Arenas can bump-allocate and can free backing memory (RSS) immediately, whereas pooled objects must be garbage-collected; arenas can allocate many differently-sized objects, whereas pools must have a separate pool for each size class.

## Comment 1058320330

other (NONE) · CannibalVox · 2022-03-03T17:50:48Z · https://github.com/golang/go/issues/51317#issuecomment-1058320330

> @mrosenc
> 
> > This is different then sync.Pool which can be used for temporary objects, it seems to me that the reason for using arenas and not pools is because you need to tie the scope of many allocated objects to some external thing (request lifetime).
> 
> 1. I believe that the proposed arenas are strictly safer than `sync.Pool`. With a `sync.Pool`, a use-after-`Put` becomes an aliasing bug, which may or may not be detected during testing. With an arena, a use-after-`Free` becomes a diagnosable panic.
> 2. As I understand it, the reasons for using arenas and not pools are efficiency and heterogeneity. Arenas can bump-allocate and can free backing memory (RSS) immediately, whereas pooled objects must be garbage-collected; arenas can allocate many differently-sized objects, whereas pools must have a separate pool for each size class.

I think it would be insanely easy to write tests that didn't catch, for instance, a use-after-free on a string key applied to a long-lived map. If the diagnostic solution was based on detecting writing outside of the "clean memory" (writing pointer to heap, escaping from the section of the stack that contains the arena) that would improve things somewhat. There are always going to be units that accept arena pointers at runtime but aren't tested for that, though, for the exact same reason they weren't set up to handle arena strings properly in the first place.

I also wouldn't feel comfortable doing with sync.Pool what is being discussed doing with arenas- the vitess sync pool implementation only uses pooling on the client side, not the server side, because relying on endpoint implementors to use request pointers in a particular way would be completely crazy. The current arena proposal is fine when a single code site is creating the arena, doing the allocations, and deciding what to do with the allocated pointers. They're not a good fit for frameworks as designed, I don't think, and you wouldn't be able to easily use them for HTTP or GRPC endpoints without that specific idiom. I can't figure out how I would ensure that random grpc endpoint implementors would not make mistakes that would cause runtime panics, or how to make sure that testing used arena-allocated pointers so we would catch these issues at development time.

e: also sync.Pool doesn't have the string alloc problem, which still seems like a huge deal to me

## Comment 1058329234

other (NONE) · CannibalVox · 2022-03-03T18:00:05Z · https://github.com/golang/go/issues/51317#issuecomment-1058329234

I think it's all fun and games to say "mistakes can cause panics with any library" but consider the following

```go
func WriteToMetrics(metricName string, key string, data interface{}) {
   metricChan <- &struct{MetricName: metricName, DataKey: key, DataValue: data}
 }
 ```
 
 Sending any part of a request body to WriteToMetrics() will cause a panic... someday. Sometimes. Maybe.  This is not an expected way for go to act currently.

## Comment 1058767184

other (NONE) · caochaovkey · 2022-03-04T02:34:34Z · https://github.com/golang/go/issues/51317#issuecomment-1058767184

I think it's very terrible.  freeing memory manually in C++ causes many problems。 such as forget ''free"， repeat “free” ， free “free” early， why does "go" make complicated?

## Comment 1059613052

maintainer (MEMBER) · rasky · 2022-03-05T00:00:17Z · https://github.com/golang/go/issues/51317#issuecomment-1059613052

@sbinet 

> > They would then have to duplicate internally their code paths for both the Arena and the non-Arena case
> 
> why do you think that would be the case? wouldn't it be possible for those libraries to devise a `MemoryAllocator` interface, use that interface in their code base and have two implementations, one w/ the `Arena` and the other with the regular Go allocator?

To clarify, this is what I meant by "duplicating code paths". You now have two allocators, you introduced a new interface, and you need to use the interface everywhere you want to allocate objects that might be "arena compatible". That's a cognitive overload compared to standard Go code where you can simply use `new` or even `&Type{}`.

> actually, that's what we did in the Go implementation of the [Apache Arrow](https://github.com/apache/arrow) library:
> 
> * https://pkg.go.dev/github.com/apache/arrow/go/arrow@v0.0.0-20211112161151-bc219186db40/memory#Allocator
> * https://pkg.go.dev/github.com/apache/arrow/go/arrow@v0.0.0-20211112161151-bc219186db40/memory#GoAllocator

I see that Arena is now in the API of the linked package, which is exactly what I was worried of. Libraries will now begin to expose optional Arena support in their APIs.

> _wrt_ your call-stack based API: I guess that could be as easily (and more explicitly) achieved with a `defer arena.Free()`? couldn't it?

My API proposal is meant to be the full API of the package, not an addition.

## Comment 1059629731

other (NONE) · mrosenc · 2022-03-05T00:48:44Z · https://github.com/golang/go/issues/51317#issuecomment-1059629731

> 2. As I understand it, the reasons for using arenas and not pools are efficiency and heterogeneity. Arenas can bump-allocate and can free backing memory (RSS) immediately, whereas pooled objects must be garbage-collected; arenas can allocate many differently-sized objects, whereas pools must have a separate pool for each size class.

What I meant was that sync.Pool is often not used for objects returned from library APIs because the library would have to ensure that users can't possibly hold on to references of those objects (of course it can be done, but not usually). Normally they are just used to allocate temporary buffers that are used within the scope of a function call or something.

Arenas are different, for example the protocol buffer APIs are going to return to you objects allocated on an arena, and so you have to supply the arena to the protocol buffer library because otherwise how would we ensure that the arena lived long enough. In fact if you take an arena argument, you sort of only want to use it to allocate objects you return, since it would be unsafe to hold on to objects that are allocated on an arena you don't control.

It is unfortunate that lots of APIs will grow arena variant methods. It seemed to me that it's almost inevitable that arenas would be attached to contexts because otherwise all those APIs will have two mandatory parameters to thread everywhere.

## Comment 1059631274

other (NONE) · mrosenc · 2022-03-05T00:54:25Z · https://github.com/golang/go/issues/51317#issuecomment-1059631274

@rasky

Unfortunately I don't see how your proposal can work. Any function that allocates memory and stashes it away would be unsafe to call with your Run. Even if it worked today any code change deep in a library that suddenly started caching things would cause programs to crash.

Perhaps if go had some kind of const like thing in its type system that allowed you to express that your function didn't have that property it could work?

## Comment 1060445089

other (NONE) · creker · 2022-03-07T10:22:17Z · https://github.com/golang/go/issues/51317#issuecomment-1060445089

@mrosenc I see that as a plus. The fact that arena allocated objects can't be used outside of Run forces developers to fit everything into Run call and properly guard everything outside from it. This very clearly delineates arena and non-arena code. With the current proposal there's nothing of that. Arena lifetime can be arbitrary long and that's exactly why this is more dangerous when it comes to caching. Current proposal already limits arenas to single goroutine. I don't think it's that big of a stretch to further limit it with Run.

The only problem is, proposal cites C++ as an example. If we take that as an example then Run() would probably be impossible to fit into that use case. It explicitly requires passing arena from outside. Using arenas only internally during parsing and then copying resulting message onto heap would probably defeat the purpose of the proposal. At least when it comes to protobufs.

## Comment 1063354775

other (NONE) · mrosenc · 2022-03-09T20:45:02Z · https://github.com/golang/go/issues/51317#issuecomment-1063354775

@creker It seems too harsh. The function in Run basically can't call any library unless that library markets itself as 'run safe' and the type system does nothing to help you prove that your code is run safe. Even standard library functions wouldn't be safe to call, who knows if they use some kind of cache underneath. I think that direction will lead to arena's either being not used, or used unsafely (hope that the libraries you use don't cache anything).

## Comment 1063373517

other (NONE) · creker · 2022-03-09T21:09:55Z · https://github.com/golang/go/issues/51317#issuecomment-1063373517

@mrosenc maybe we can relax it a bit more like so
```go
func Run(f func(arena *Arena))
```

Arena object would lack Free() method basically forcing the same semantics (everything in the arena is deallocated upon return. Whether it's delayed or not is implementation defined) but would allow safely calling into other parts of the code.

## Comment 1063420318

maintainer (MEMBER) · rasky · 2022-03-09T22:05:56Z · https://github.com/golang/go/issues/51317#issuecomment-1063420318

> Even standard library functions wouldn't be safe to call, who knows if they use some kind of cache underneath. 

Obviously we need to enhance the `Run` proposal to add a way to force-allocate on the heap. I don't want to bikeshed on the exact syntax here, so let's revisit the counter-proposal with:

```go
package arena

// Run calls f. All allocations performed by this gorutine while f is running will happen in a memory arena,
// which is automatically reclaimed when f exits. Objects allocated by f will not valid anymore after f
// exits and must not be accessed
func Run(f func())

// HeapNew allocates a T on the heap. It is equivalent to the new keyword, but always allocate T on the heap
// even if it is being called within a Run.
func HeapNew[T any]() *T
```

> The function in Run basically can't call any library unless that library markets itself as 'run safe' and the type system does nothing to help you prove that your code is run safe.

None of the existing code is "arena ready" today. The original proposal is proposing to ask package authors to change the API of all existing Go packages to duplicate the entrypoints adding an arena-ready version next to the existing APIs, while sorting out internally how to reduce code duplication. 

My counter-proposal with `Run` and `HeapNew` allows to make a package arena ready without modifying its public API, without percolating Arena pointers everywhere like Context, and simply by calling `arena.HeapNew` in specific places where required. There might be more implementation details here (eg: I guess resizing an existing heap slice should keep it in the heap even in the Run context), but nobody said this was going to be easy on the runtime team :)

I would also like to put forward a different argument against the original proposal as it stands. It has been discussed and rejected multiple times the proposal to add an `inline` keyword to the language. I've been bitten by its absence a lot. The bullet I had to bit is that we don't want to start adding "compiler/runtime implementation details" to the Go language itself; if the compiler is supposed to figure it out by itself, then it will, eventually. If it doesn't today, I should just wait multiple years until it catches up, and meanwhile stick with the resulting low performance or manually inline the code.

I'm not sure why Arena should get an exemption from this approach. Arena as proposed is extremely more viral and impactful on the design of Go's APIs than inline, and would have a ripple effect on many Go packages that will be forced to change their APIs to adapt to it. It would change the way many Go APIs will present to users including beginners, and will force them to learn what an Arena is very early. It will be a much more visible change compared to inline. And we would do this "just because" the compiler cannot figure it out by itself how to optimize the lifetime of those memory allocations.

This is exactly the same situation of the inline keyword, and we should probably reject this proposal on the same basis. Or if we don't, I think the proposal team should give a clear answer on whether their position on inline should be changed as well.

## Comment 1063434467

other (CONTRIBUTOR) · Merovius · 2022-03-09T22:26:29Z · https://github.com/golang/go/issues/51317#issuecomment-1063434467

> Obviously we need to enhance the Run proposal to add a way to force-allocate on the heap.

That's certainly not the right approach. Arena usage should be opt-in, not opt-out. Simply calling `new` should never allocate in an arena - even if we ignore that `new` isn't the only way to allocate memory, there's also closures, `make`, pointer literals or sometimes simply passing an argument. It is impossible to know if a given function allocates without carefully reading its code, probably compiling it with `-gcflags=-m` and repeating that for every Go version you want to use. That's simply unacceptable.

Passing `*arena.Arena` around is the safe variant. It is a way for code to opt-in into arena support where it makes sense and it's a way to make it explicit which code allocates into an arena and which will never allocate into an arena.

We can discuss whether passing around an `*arena.Arena` happens via `a := arena.New(); defer a.Free(); f(a)` or whether it happens via `arena.Run(f)`, sure. But it absolutely has to happen explicitly.

## Comment 1063443027

other (CONTRIBUTOR) · Merovius · 2022-03-09T22:34:47Z · https://github.com/golang/go/issues/51317#issuecomment-1063443027

> Arena as proposed is extremely more viral and impactful on the design of Go's APIs than inline, and would have a ripple effect on many Go packages that will be forced to change their APIs to adapt to it. It would change the way many Go APIs will present to users including beginners, and will force them to learn what an Arena is very early. It will be a much more visible change compared to inline. And we would do this "just because" the compiler cannot figure it out by itself how to optimize the lifetime of those memory allocations.

FWIW I had a similar thought, recently. A couple of years back, there was talk about a new GC algorithm for Go called a [Request Oriented Collector](https://imkira.com/assets/files/golang-gc-paper.pdf) which, if you squint at it a bit, seems to be exactly that. It supposes that many Go programs allocate a bunch of memory in independent "requests" and can free it again in bulk, once the request is done and builds a GC algorithm out of that. That's *kinda sorta* heuristic, transparent arenas. At least as I understand it.

I believe at the time, the conclusion was that this doesn't seem to actually create a big benefit in practice, so it wasn't ultimately added to Go. But I'm not sure about that. I can't find a definitive answer and I might misremember. But I'm curious if a) I'm misunderstanding and the analogy is actually very wrong and b) if not, how those learnings translate to this proposal.

## Comment 1063455741

maintainer (MEMBER) · rasky · 2022-03-09T22:46:02Z · https://github.com/golang/go/issues/51317#issuecomment-1063455741

> It is impossible to know if a given function allocates without carefully reading its code, probably compiling it with -gcflags=-m and repeating that for every Go version you want to use.

Yes, and this is exactly why you do *not* want to go catching all those allocations one by one and explicitly opt them in into an Arena. Nor you want them to go into the heap, if they are executed in the context of a situation where you want to just extract one data.

Let's make an example:

```go
func protoReadStatus(conn *myprotocol.Conn) int {
   pkt := myprotocol.ReadPacket(conn)
   data := myprotocol.Deserialize(pkt)
   return data.status
}
```

This function reads a packet from the network, deserializes it, and then extract a single integer field from it, a status code. Assuming one want to limit the lifetime of allocations of this function, using my proposal you would change the function to:

```go
func protoReadStatus(conn *myprotocol.Conn) int {
   var status int
   arena.Run(func() {
      pkt := myprotocol.ReadPacket(conn)
      data := myprotocol.Deserialize(pkt)
      status = data.status
   })
   return status
}
```

This means that *everything that is allocated within the myprotocol library functions is redirected to an arena pool and automatically reclaimed*. You don't need to go catch all single makes, closures, strings, slices, news, or whatever. *Everything* is intended to be a "temporary" allocation whose purpose is finished when the Run function ends. The function takes a connection and extracts an integer: everything that is allocated in-between is an intermediate object, and is immediately deallocated. Once you get the int you were looking for, you don't need all those intermediate objects anymore.

Now, will this always work on existing Go code as-is? Of course not. It might be possible that `myprotocol.ReadPacket` or `myprotocol.Deserialize` allocate something that is supposed to survive, even if it's not immediately visible from their API that they need to (the "internal cache" example is probably the easiest to reason around). So in this case, `myprotocol` will have to be made arena-safe by just changing *those* allocations to `arena.HeapNew`: only those related the internal cache. Everything else can go to the temporary arena. And of course, this behavior can then be fixed with a test that verifies that it doesn't regress in the future, and the documentation can confirm that the package has been tested to be arena-safe.

## Comment 1063463208

other (NONE) · beoran · 2022-03-09T22:57:10Z · https://github.com/golang/go/issues/51317#issuecomment-1063463208

Maybe a silly suggestion but in stead of  arenas, I  think a tree allocator with node results would be easier to use and free  after.

## Comment 1063486794

other (CONTRIBUTOR) · ianlancetaylor · 2022-03-09T23:35:48Z · https://github.com/golang/go/issues/51317#issuecomment-1063486794

@rasky I see arenas as being significantly different from an inline keyword.  Arenas change the run-time behavior, inline changes the compile-time behavior.  An inline keyword changes the language.  Arenas do not change the language.

I would say that arenas are similar to `sync.Pool`.  Both `sync.Pool` and arenas requires to explicitly release memory.  Both `sync.Pool` and arenas are unsafe, in that if you use the memory after releasing, bad things will happen (in fact, arenas are better than `sync.Pool` here, in that for arenas the bad thing is a program crash and for `sync.Pool` the bad thing is memory aliasing leading to unexpected corruption).

## Comment 1063488218

other (CONTRIBUTOR) · Merovius · 2022-03-09T23:38:42Z · https://github.com/golang/go/issues/51317#issuecomment-1063488218

@rasky Currently, changing a function from

```go
func Foo(args Args) *Val { return expensiveComputation(args) }
```

to

```go
var (
    mu sync.Mutex
    m = make(map[Args]*Val)
)

func Foo(args Args) *Val {
    mu.Lock()
    defer mu.Unlock()
    v, ok := m[args]
    if !ok {
        v = expensiveComputation(args)
        m[args] = v
    }
    return v
}
```

is a safe, backwards compatible change. Under your proposal, it is not. `Foo` might be called in `arena.Run` and the allocations it does would happen in an arena, causing the program to panic at some point in the future. That's not acceptable. Arena allocations must not be transparent.

## Comment 1063489884

other (CONTRIBUTOR) · ianlancetaylor · 2022-03-09T23:42:15Z · https://github.com/golang/go/issues/51317#issuecomment-1063489884

@Merovius Arenas can indeed be seen as another iteration of the Request Oriented Collector.  The problem with the Request Oriented Collector was that despite quite a lot of work nobody was able to measure any performance improvements on real programs.  With arenas, by comparison, the implementers measured significant performance improvements for real programs.  As the proposal says: "savings of up to 15% in CPU and memory usage for a number of large applications, mainly due to reduction in garbage collection CPU time and heap memory usage."

This isn't to say that arenas are perfect or that we should necessarily adopt this proposal.  It's obviously troublesome that user programs have to be rewritten to get any benefit from arenas.  I think the hope is that most of the rewriting would be focused on a couple of packages (protobuf, JSON) and that once that is done the advantages of arenas are available for about as much work as is required to use `sync.Pool`.

## Comment 1063491815

other (CONTRIBUTOR) · josharian · 2022-03-09T23:45:55Z · https://github.com/golang/go/issues/51317#issuecomment-1063491815

@ianlancetaylor that's an apt analogy, but I'm not sure how far it goes.

In practice, sync.Pools get used only in places where lifetimes are short and obvious. Part of the reason for that is that sync.Pools hold individual objects.

The use case for arenas is rather more sweeping, so there's a stronger temptation/need to pass them around.

If, like sync.Pool, I was confident that I would ~never see an arena in a non-internal package's API, I'd feel a lot more comfortable about this proposal. But I think the use case lends itself to viral function signature changes and spooky-panic-at-a-distance a lot more than sync.Pool does.


## Comment 1063500496

other (CONTRIBUTOR) · ianlancetaylor · 2022-03-10T00:02:33Z · https://github.com/golang/go/issues/51317#issuecomment-1063500496

Yes, arenas are definitely more sweeping, and they will definitely be passed around.  And they will definitely appear in the API of packages like protobufs and encoding/json.  I don't think there would be much benefit to them if that were not true.

So it's possible that for some programs there would be viral signature changes.  I don't see why that would _necessarily_ happen, but it could happen.  The kinds of programs that benefit from arenas are those for which there is a very clear lifetime to certain kinds of memory use.  That is, server programs that perform requests on behalf of clients.  The memory use of the action performed for the client does not have a clear lifetime.  But the memory used to unmarshal client requests and marshal server responses does have a clear lifetime.  So that is where arenas would be used.  I don't know why they would escape beyond that.  But, of course, I am often surprised.

When arenas are used for marshaling and unmarshaling, then the program has to be aware of the risks of memory aliasing when using unmarshaled data.  That is where there is a potential for spooky panics.

So the big problem with arenas is that they can indeed be misused.  And the question for the proposal is: do the benefits they provide outweigh the potential for abuse?  Are they an attractive nuisance, or are they worth the chance of error?  We had similar discussions about `sync.Pool` back in the day.

## Comment 1063501138

other (NONE) · CannibalVox · 2022-03-10T00:03:36Z · https://github.com/golang/go/issues/51317#issuecomment-1063501138

> This isn't to say that arenas are perfect or that we should necessarily adopt this proposal. It's obviously troublesome that user programs have to be rewritten to get any benefit from arenas. I think the hope is that most of the rewriting would be focused on a couple of packages (protobuf, JSON) and that once that is done the advantages of arenas are available for about as much work as is required to use `sync.Pool`.

I'm curious what a JSON arena would actually look like in practice. As I said previously, nobody would ever use sync.Pool in such a way that you hand a user a pile of pooled objects at the root of an endpoint handler and expect that every layer of a piece of code would remember not to persist any part of the request body. I'm not even sure it would be possible.

I can think of a few valuable uses of arenas, as written- basically anytime you can seal the allocated memory away from the consumer and you don't have to worry about what's going to be done with it, arenas can potentially be a valuable ally.  Any memory-heavy algorithm that produces a reduced result that can be allocated from heap will be a big win. However, the suggested uses, which all seem to involve handing allocated data to the consumer at the root of a deep call stack, seem tremendously dangerous. And if the overarching goal was to come up with a solution to proto allocation costs, I don't know if this is a viable plan.

e:

> When arenas are used for marshaling and unmarshaling, then the program has to be aware of the risks of memory aliasing when using unmarshaled data. That is where there is a potential for spooky panics.

I don't know how this could even be physically possible.

## Comment 1063616047

other (NONE) · mrosenc · 2022-03-10T03:30:37Z · https://github.com/golang/go/issues/51317#issuecomment-1063616047

@ianlancetaylor If you look at a lot of Google backends you will see code that allocates protos deep inside call stacks, for example to call the backends backends. This would be especially problematic in the case where there is a wide fanout and every shard has a slightly different request object. In addition I can remember many cases where we chased down allocations of large arrays or other temporary data structures deep in a servers request call stack to move onto Arenas.

It seems to me many of these function chains would end up growing arena parameters. That said, maybe a lot of the benefit of arenas can be had when not allowing arenas to be shared quite so broadly, instead using many different arenas during a single backend request. I'm not sure how much use you would have to make of a single arena for it to pay off.

## Comment 1064419774

other (CONTRIBUTOR) · akshayjshah · 2022-03-10T19:33:39Z · https://github.com/golang/go/issues/51317#issuecomment-1064419774

As a community, we digested `context` years ago and are beginning to explore how generics change idiomatic Go. Are arenas, with their attendant changes to API design, the only solution to the underlying problem?

The motivating use case seems to be protobuf performance at Google, and the prototype implementation makes marshaling and unmarshaling ~15% faster. That's great! But putting aside its many options to customize the generated code, `gogoproto` is **[~50% faster](https://github.com/alecthomas/go_serialization_benchmarks)** using today's Go. The performance improvements alone led many teams, including Kubernetes, to adopt it. Why not add an opt-in flag to `protoc-gen-go` to enable `gogoproto`'s optimizations, get a much larger performance improvement, and let the community adapt to generics first?

We may still feel that the additional complexity of arenas is worthwhile. Personally, I'd be happy to use arenas with APIs that are otherwise carefully optimized. In this case, though, it seems like there's plenty of space to improve performance using today's Go.

## Comment 1064440063

other (NONE) · CannibalVox · 2022-03-10T19:50:53Z · https://github.com/golang/go/issues/51317#issuecomment-1064440063

> The motivating use case seems to be protobuf performance at Google, and the prototype implementation makes marshaling and unmarshaling ~15% faster. That's great!

I'm not sure this is correct- the implication seemed to be that the service's total CPU usage was 15% lower. This seems to imply that the marshal/unmarshal impact would be somewhat higher. I think the issue is that since the impact is largely garbage collection, it's difficult to measure it other than holistically.

## Comment 1064440715

other (CONTRIBUTOR) · Merovius · 2022-03-10T19:51:14Z · https://github.com/golang/go/issues/51317#issuecomment-1064440715

> The motivating use case seems to be protobuf performance at Google, and the prototype implementation makes marshaling and unmarshaling ~15% faster.

This seems to have two misunderstandings (or I misunderstood things): 1. This doesn't just affect Google, but *any* user of gRPC. That's a *lot*. And 2. it's not "marshaling and unmarshaling got ~15% faster", but "the total CPU and memory requirements of the service got reduced by ~15%".

## Comment 1064454814

other (NONE) · CannibalVox · 2022-03-10T20:04:19Z · https://github.com/golang/go/issues/51317#issuecomment-1064454814

You know, anybody who logs requests isn't even going to be able to use this: nobody can guarantee their logging framework doesn't now or won't in the future persist the values sent to it, at least a few moments beyond the lifetime of the request.

## Comment 1064457823

other (CONTRIBUTOR) · Merovius · 2022-03-10T20:08:05Z · https://github.com/golang/go/issues/51317#issuecomment-1064457823

@CannibalVox I think doing that is a bad idea for a logging library regardless of whether or not arenas exist. Code like

```go
log.Printf("%v", req)
req.SomeField = SomeValue
```

can already exist and would be racey and/or create unusable logs.

## Comment 1064459603

other (NONE) · CannibalVox · 2022-03-10T20:10:20Z · https://github.com/golang/go/issues/51317#issuecomment-1064459603

I think logging inbound requests is somewhat more common than modifying the contents of a request in the endpoint code that handles it.

## Comment 1064468687

other (CONTRIBUTOR) · Merovius · 2022-03-10T20:21:24Z · https://github.com/golang/go/issues/51317#issuecomment-1064468687

Whether that's common or not doesn't change the fact that it's a very bad idea for a logging library to persist its arguments beyond the call. As a user I would most definitely not expect it to. And I would be pretty ticked off if my service breaks because of the data-race it causes.

## Comment 1064471870

other (NONE) · CannibalVox · 2022-03-10T20:25:24Z · https://github.com/golang/go/issues/51317#issuecomment-1064471870

> Whether that's common or not doesn't change the fact that it's a very bad idea for a logging library to persist its arguments beyond the call. As a user I would most definitely not expect it to. And I would be pretty ticked off if my service breaks because of the data-race it causes.

open telemetry does - https://github.com/open-telemetry/opentelemetry-go/blob/0d0a7320e6eab18df12e2542b4ea000ced32d5bb/sdk/trace/span.go#L451

Use a string from your request as an event name and you've bought yourself a one-way ticket to panic town

## Comment 1064474163

other (NONE) · jfesler · 2022-03-10T20:28:18Z · https://github.com/golang/go/issues/51317#issuecomment-1064474163

I like the idea, but I fear people rushing to use these arenas.  I don't trust everyone's code quite so equally.  I'm likely to write a scanner to look for libraries that use this proposed feature, and red flag them.  I am quite concerned about pointers to arena objects getting returned outside their scope, and this not being caught either at compile or lint time.  Catching them at runtime is much too late.

## Comment 1064520845

other (CONTRIBUTOR) · Merovius · 2022-03-10T21:28:27Z · https://github.com/golang/go/issues/51317#issuecomment-1064520845

@CannibalVox Yes, I agree that strings are the exception, in terms of what makes this proposal problematic.

## Comment 1064539352

other (NONE) · CannibalVox · 2022-03-10T21:53:16Z · https://github.com/golang/go/issues/51317#issuecomment-1064539352

How about slices?

https://github.com/DataDog/datadog-go/blob/bebc8687148d0d66357729f1ce11015470cf6888/statsd/statsd.go#L544

Apply tags from request to a metric = panic

## Comment 1064558091

other (CONTRIBUTOR) · Merovius · 2022-03-10T22:11:21Z · https://github.com/golang/go/issues/51317#issuecomment-1064558091

You seem to be making arguments for filing bugs against these libraries.
If they break if you pass an arena-allocated value to them, they'll break if you modify the value after passing it. I don't see why one would be materially more likely than the other.
You won't allocate slices of `attribute.KeyValue` in an arena and you won't allocate the slice of string-tags you send to datadog in an arena.

And yes, to be clear, the handling of string-values itself is a notable exception to that. I think it's totally reasonable to assume that one of those strings used might be derived from request data which *would* be allocated in an arena.

## Comment 1064572859

other (CONTRIBUTOR) · akshayjshah · 2022-03-10T22:29:59Z · https://github.com/golang/go/issues/51317#issuecomment-1064572859

> 2. it's not "marshaling and unmarshaling got ~15% faster", but "the total CPU and memory requirements of the service got reduced by ~15%".

You're right (as is @CannibalVox) - I misread the performance benefit. Totally my fault, and the effect of arenas was more pronounced than I'd realized. The broader point I'm trying to make perhaps still stands, though: this is a finicky, potentially difficult-to-debug optimization that requires all packages to agree out-of-band on the lifetime of any exchanged data, _even strings_. Outside a closed monorepo, how long will it take us to flush out all the places we need to call `HeapString`? Could we capture a significant fraction of these gains more safely by optimizing a few widely-used packages, even if requires a v2 with new APIs?

(I also overlooked the fact that the serialization benchmarks I referenced are using proto2 and `github.com/golang/protobuf`. 🤦🏽‍♂️ `google.golang.org/protobuf` and proto3 likely do better already.)

> 1. This doesn't just affect Google, but any user of gRPC. That's a lot.

Absolutely. If we're widely adopting a notion of request-lifetime data, I assume arenas would also get integrated into net/http somehow - the audience is indeed very large.

## Comment 1064615277

other (CONTRIBUTOR) · Merovius · 2022-03-10T23:22:37Z · https://github.com/golang/go/issues/51317#issuecomment-1064615277

@akshayjshah

> this is a finicky, potentially difficult-to-debug optimization that requires all packages to agree out-of-band on the lifetime of any exchanged data, *even strings*.

FWIW, I've personally fully come around to believe strings should never be allocated in an arena and we shouldn't provide an API to do so - and if the benefits of arenas are too small under that constraint, we probably shouldn't do it.

The discussion above convinced me that the actual practice around strings is incompatible with arenas. `HeapString` IMO does not solve those problems, because it's unreasonable to expect any code which lets a string escape to call it. Normal Go programmers shouldn't have to know about arenas - the only code that should be aware of arenas at all is the code which actively interacts with it. Which would likely put it so close to the in-arena-allocation, that you might as well allocate the string on the heap to begin with.

But that's just my opinion.

## Comment 1064754724

other (NONE) · reusee · 2022-03-11T04:13:39Z · https://github.com/golang/go/issues/51317#issuecomment-1064754724

How about adding lifetimes to the type system?
```
func main() {
	begin Span
	var ptrT *T/Span
	ptrT.val = 1

        sliceT := make([]T/Span, 100)
	sliceT[99] .val = 4

        end Span
}
```
and generic params can take lifetimes
```
func foo[T any/Span]() []T {
    slice := make([]T, 100)
    slice[99] = 42
    return slice
}
```


## Comment 1068144696

other (NONE) · CannibalVox · 2022-03-15T15:47:16Z · https://github.com/golang/go/issues/51317#issuecomment-1068144696

Hello- this morning I was spending a moment thinking about what I'd like to happen with large, parsed objects, in order to avoid heap allocations. It occurred to me that what I'd **really** like to happen is for my request body to be allocated to the stack. This would basically cause everything to work how I'd want it to work, because we'd avoid the heap allocation, the object would be freed at the end of the request as I'd hope, and attempts to use the object elsewhere would cause an escape and heap allocation seamlessly.

Obviously, allocating to stack a potentially-large object returned from a large, complicated unmarshalling method isn't usually something that's possible.  But it occurred to me that if there was an arena method to move arena memory into the stack, it would perhaps be possible. This would allow the usage pattern of these arenas to match more traditional arenas, where the blast radius of using an arena is much more limited.

```go
allocator := arena.New()
unsafeReq := unmarshalWithArena(ctx, allocator)
req := arena.ToStack(unsafeReq)
allocator.Free()
handler(ctx, req)
```

I think that probably large request objects being bounced onto the stack has downsides, so maybe this isn't as good as it appears at first glance (and I don't know what the gc characteristics of this would actually be), but this does match my expectation of how request objects ought to act generally.

## Comment 1068239295

other (CONTRIBUTOR) · Merovius · 2022-03-15T17:10:44Z · https://github.com/golang/go/issues/51317#issuecomment-1068239295

@CannibalVox ISTM that the compiler would have to assume that `handler` would let `req` escape, given that it'll usually be a dynamic call (i.e. an interface). So, ISTM that this would just leave `req` on the heap anyways.

## Comment 1068243071

other (NONE) · CannibalVox · 2022-03-15T17:14:39Z · https://github.com/golang/go/issues/51317#issuecomment-1068243071

This wouldn't be the case for grpc handlers, would it? Maybe with the interceptor stack it would be. HTTP handlers/json wouldn't necessarily be an issue since the above process would take place within the handler itself, but otoh would logging the req count as an escape as well?

## Comment 1068298469

other (CONTRIBUTOR) · Merovius · 2022-03-15T18:07:42Z · https://github.com/golang/go/issues/51317#issuecomment-1068298469

> This wouldn't be the case for grpc handlers, would it?

gRPC service handlers are [interface implementations](https://grpc.io/docs/languages/go/generated-code/#methods-on-generated-server-interfaces). And it's [stored in the server as an `interface{}`](https://github.com/grpc/grpc-go/blob/v1.45.0/server.go#L104), so I highly doubt the compiler can de-virtualize it either.

In general, it should likely be preferred for the relevant arena code to happen in whatever framework is used, as its an expert feature and should be centralized as much as possible. So I would assume it's almost universal that this framework then calls into user-code via some sort of interface. HTTP is an exception insofar as it doesn't provide typed access to the body data anyways, but presumably any HTTP framework (like Buffalo or whatever) which does would have exactly the same pattern.

## Comment 1068314848

other (NONE) · CannibalVox · 2022-03-15T18:22:05Z · https://github.com/golang/go/issues/51317#issuecomment-1068314848

> gRPC service handlers are [interface implementations](https://grpc.io/docs/languages/go/generated-code/#methods-on-generated-server-interfaces). And it's [stored in the server as an interface{}](https://github.com/grpc/grpc-go/blob/v1.45.0/server.go#L104), so I highly doubt the compiler can de-virtualize it either.

~~I might be misunderstanding you, but I believe it's the request itself that needs to be devirtualized to avoid escapes, not the server being called into. The request unmarshalling takes place in strongly-typed code, where the arena could be added with no escapes.  The process of calling into an endpoint shouldn't count as an escape. There is of course a long list of things an endpoint author could do with a request that would force it onto the heap, though, it seems.~~

~~As example:~~

```go
package main

import (
	"fmt"
)

type RequestType struct {
	Value int
}

type Service interface {
	Handler(req RequestType) error
}

type ServiceImpl struct{}

func NewService() Service {
	return &ServiceImpl{}
}

func (s *ServiceImpl) Handler(req RequestType) error {
	fmt.Println("wow!")

	return nil
}

func main() {
	service := NewService()

	request := RequestType{Value: 5}

	_ = service.Handler(request)
}
```

```sh
$ go build -gcflags '-m -l' ./...
# testslice
.\main.go:18:9: &ServiceImpl{} escapes to heap
.\main.go:21:7: s does not escape
.\main.go:22:13: ... argument does not escape
.\main.go:22:14: "wow!" escapes to heap
```

E: scratch this, pointers would escape to the heap, which would be an unavoidable problem with proto

## Comment 1068350739

other (CONTRIBUTOR) · Merovius · 2022-03-15T18:59:41Z · https://github.com/golang/go/issues/51317#issuecomment-1068350739

@CannibalVox Your example is not illustrative, as the compiler can devirtualize `ServiceImpl`, preventing the argument from escaping. This code demonstrates the problem better:

```go
package main

type RequestType struct{ Value int }

type Service interface{ Handler(req *RequestType) }

type ServiceImpl struct{}

func NewService() Service { return &ServiceImpl{} }

func (s *ServiceImpl) Handler(req *RequestType) {}

func main() {
	m := map[string]Service{
		"x": NewService(),
	}
	request := &RequestType{Value: 5}
	m["x"].Handler(request)
}
```

And sure enough

```
mero@hix ~/tmp/x$ go build -gcflags=-m x.go
# command-line-arguments
./x.go:9:6: can inline NewService
./x.go:11:6: can inline (*ServiceImpl).Handler
./x.go:15:18: inlining call to NewService
./x.go:9:36: &ServiceImpl{} escapes to heap
./x.go:11:7: s does not escape
./x.go:11:31: req does not escape
./x.go:14:25: map[string]Service{...} does not escape
./x.go:15:18: &ServiceImpl{} escapes to heap
./x.go:17:13: &RequestType{...} escapes to heap
```

The crucial part here is preventing the compiler from devirtualizing the interface-call - if you replace `main()` with `NewHandler().Handler(&RequestType{Value: 5})`, the request no longer escapes.

This demonstrates that this isn't actually specific to protobuf at all. *Any* framework will have a separation between framework code and user-code, the latter being called via some sort of dynamic dispatch. And generally, that dynamic dispatch can't be avoided, as what handler is to be called will depend on the request data. And when the framework is being compiled, the service implementations are not known, so they can't be analyzed for whether or not their arguments escape. So, as I said, I think this problem is near-universal.

FWIW, I don't think there is any need for an explicit method call to move an arena to the stack anyways. If escape-analysis determines that data allocated from an arena does not escape, it could just transparently allocate the arena on the stack. But if that can be proved we wouldn't need arenas - you could just allocate the request on the stack in the first place.

## Comment 1068397994

other (NONE) · CannibalVox · 2022-03-15T19:45:05Z · https://github.com/golang/go/issues/51317#issuecomment-1068397994

> @CannibalVox Your example is not illustrative, as the compiler can devirtualize `ServiceImpl`, preventing the argument from escaping. This code demonstrates the problem better:

No, the escape analyzer calls out devirtualization, the issue was that I was passing a value. Not great for a scenario where optional values are vital.

> FWIW, I don't think there is any need for an explicit method call to move an arena to the stack anyways. If escape-analysis determines that data allocated from an arena does not escape, it could just transparently allocate the arena on the stack. But if that can be proved we wouldn't need arenas - you could just allocate the request on the stack in the first place.

Sending the data out of unmarshalling code is itself an escape, so this isn't necessarily true. Regardless, I agree that this isn't really viable at all.

## Comment 1068458173

other (CONTRIBUTOR) · Merovius · 2022-03-15T20:47:40Z · https://github.com/golang/go/issues/51317#issuecomment-1068458173

> No, the escape analyzer calls out devirtualization, the issue was that I was passing a value. Not great for a scenario where optional values are vital.

Indeed it does. For [your example](https://github.com/golang/go/issues/51317#issuecomment-1068314848), go 1.18 prints (among other things):

> ./x.go:32:21: devirtualizing service.Handler to *ServiceImpl

[If you change the arguments to pointers](https://go.dev/play/p/LeaVi7PJA9z), it prints (among other things):

> ./x.go:32:21: devirtualizing service.Handler to *ServiceImpl
> ./x.go:30:13: &RequestType{...} does not escape

[And if you put the `Service` in a map](https://go.dev/play/p/2JzgYdX73GF), it no longer prints the devirtualization message and prints:

> ./x.go:32:13: &RequestType{...} escapes to heap

You are correct that using pointers is a necessary condition for the request to end on the heap. But it's not a sufficient one. The real issue is that the compiler can't do escape analysis through dynamic calls, unless it can devirtualize them - which it can't, in most use-cases for arenas.

## Comment 1070261882

other (NONE) · hhstore · 2022-03-17T03:48:26Z · https://github.com/golang/go/issues/51317#issuecomment-1070261882

## Is it really necessary to add `Manual GC` to the Go language?

- Do these users really care about performance? If they do, why not use `C/C++/Rust`?
- Do these users really care about performance? If they do, why not use `C/C++/Rust`?
- Do these users really care about performance? If they do, why not use `C/C++/Rust`?


Introducing gc in go, will the performance be better than rust? If not. Is it necessary?

Why should the needs of the few affect everyone? 

Just because it's a proposal from someone from an internal team at Google?

What about the `CGo` in the past?


## Why don't these users use Rust?

- Wouldn't `Rust without GC` be a better option?


## Is it a smart move to turn Go into Rust?

- really?



## Who are the users who need this feature?

- `Rust Users`?
- Why do `Rust users` write Go?


## Has the official really listened to the community's opinion?

- Or just tell everyone to `accept` it and `shut up`?
- Seriously, does Go have a real community?  `Googler's go` or the `community's go`?
    - what about `generic design: <> vs []`?
    - what about `dep` vs `go module`?
    - what about `cgo`?










## Comment 1070354093

other (NONE) · hhstore · 2022-03-17T05:57:47Z · https://github.com/golang/go/issues/51317#issuecomment-1070354093

## Don't just point at the emoticon.

- Use your arguments to refute me item by item. 
- Use your arguments to refute me item by item. 
- Use your arguments to refute me item by item. 


> This proposal is contagious. Same as `generics`. 

- Once a large number of base libraries are implemented based on it, it will force everyone to use it. 
- It seems that others may choose not to use it, but in fact, there is no choice at all.

## Comment 1070371858

other (CONTRIBUTOR) · Merovius · 2022-03-17T06:32:11Z · https://github.com/golang/go/issues/51317#issuecomment-1070371858

> Do these users really care about performance? If they do, why not use C/C++/Rust?

Because it is possible to care about more than one thing. Go is a different language than those, with different strengths and weaknesses. Most people who work actively on Go and contribute to it like it, probably. And so want to use it.

> Has the official really listened to the community's opinion?

This is an old discussion. It has happened in a lot of places already. I think [the best response to this question is still this post by @ianlancetaylor](https://groups.google.com/g/golang-nuts/c/6dKNSN0M_kg/m/EUzcym2FBAAJ). But this is decidedly not the place to have it again.

In the meantime, note that while I'm skeptical about this proposal and have thus downvoted it, the emoji upvotes still outweigh the downvotes. And that it has not been accepted, so far.

> Don't just point at the emoticon. It's cowardly.

Please note that [the Go community Code of Conduct](https://go.dev/conduct) is in effect here. Calling people "cowardly" is not only unkind and inflammatory, it also is not pragmatic. Your confrontational, inflammatory posts makes it hard to engage constructively and easy to ignore your concerns. So if your goal is to not have this proposal accepted, your posts are actually counterproductive for the achievement of that goal.

## Comment 1070751811

other (NONE) · hhstore · 2022-03-17T10:14:46Z · https://github.com/golang/go/issues/51317#issuecomment-1070751811

> > Do these users really care about performance? If they do, why not use C/C++/Rust?
> 
> Because it is possible to care about more than one thing. Go is a different language than those, with different strengths and weaknesses. Most people who work actively on Go and contribute to it like it, probably. And so want to use it.
> 
> > Has the official really listened to the community's opinion?
> 
> This is an old discussion. It has happened in a lot of places already. I think [the best response to this question is still this post by @ianlancetaylor](https://groups.google.com/g/golang-nuts/c/6dKNSN0M_kg/m/EUzcym2FBAAJ). But this is decidedly not the place to have it again.
> 
> In the meantime, note that while I'm skeptical about this proposal and have thus downvoted it, the emoji upvotes still outweigh the downvotes. And that it has not been accepted, so far.
> 
> > Don't just point at the emoticon. It's cowardly.
> 
> Please note that [the Go community Code of Conduct](https://go.dev/conduct) is in effect here. Calling people "cowardly" is not only unkind and inflammatory, it also is not pragmatic. Your confrontational, inflammatory posts makes it hard to engage constructively and easy to ignore your concerns. So if your goal is to not have this proposal accepted, your posts are actually counterproductive for the achievement of that goal.


I deleted `cowardly`.  This word is indeed inappropriate. (But these people who clicked on the emoticon, did not stand up to discuss the proposal)

I'm well aware: this proposal will most likely pass. 


https://groups.google.com/g/golang-nuts/c/6dKNSN0M_kg/m/EUzcym2FBAAJ?pli=1

The content of this link, does not explain anything. 


> When I say go is Google's go, I mean: 

- In fact, go's design decisions are made almost exclusively by the Google's internal development team
- contrary to the opinion of the Google's development team, it is basically ignored. 
- exactly means is: Go belongs to Google employees, not the community.

## Comment 1070764760

other (NONE) · hhstore · 2022-03-17T10:29:28Z · https://github.com/golang/go/issues/51317#issuecomment-1070764760

- In fact, I would like to say: a large number of users of go, because they are not native English speakers, or pay less attention to community development. Their opinions and voices, are ignored. 
- The reasons given in this proposal are very unconvincing.
- And the proponents of this proposal, no one came out to answer my questions: `Is this proposal really  necessary?`
- As I said, If you (the Google's team) think you can do whatever you want, there's no need to fake a proposal. 
- You guys decide internally. Does voting make sense? Anyway, it's all for everyone to accept.


## Comment 1070778848

other (CONTRIBUTOR) · Merovius · 2022-03-17T10:45:47Z · https://github.com/golang/go/issues/51317#issuecomment-1070778848

@hhstore Again, this issue is not the right place to argue about the governance of the Go project. Please keep the discussion to the proposal at hand. If you want to discuss the Go project's governance, [golang-nuts](https://groups.google.com/g/golang-nuts) (or the [Go subreddit](https://www.reddit.com/r/golang/), the [Go slack](https://invite.slack.golangbridge.org), the [Go twitter community](https://twitter.com/i/communities/1493637136502960134) or any number of other discussion platforms) would be a more appropriate forum.

> The reasons given in this proposal are very unconvincing.

Can you be more specific? As far as I'm aware, the main argument in favor seems to be "it saves around 15% of memory and CPU time savings for some gRPC servers we tested", which, on its own, seem to be a pretty convincing argument in favor. Those savings would be significant in the extreme.

> And the proponents of this proposal, no one came out to answer my questions: `Is this proposal really necessary?`

The answer to that is, I believe, a strong "no". It is not necessary, but it does have benefits. It also has downsides and I don't think anyone is denying that either. All of this is, FTR, true for the overwhelming majority of proposals. The only exception I could think of are proposals directly addressing bugs.

This issue is to weigh the benefits against the downsides. Do you have anything to add about that? i.e. do you have data to suggest that the benefits are lower than claimed, or that the costs are higher than expected?

## Comment 1070782872

other (NONE) · hhstore · 2022-03-17T10:50:25Z · https://github.com/golang/go/issues/51317#issuecomment-1070782872

> What is the reason to add this to the standard library as opposed to building a third party package?

- I support this view. 
- The value of this proposal, more suitable as a third-party library. not the standard library.


> about the governance of the Go project.

- I don't want to talk too much about go's community governance. 
- Go official behavior over the past few years, how the facts are, everybody knows exactly what's going on.

## Comment 1070784669

maintainer (MEMBER) · thepudds · 2022-03-17T10:52:22Z · https://github.com/golang/go/issues/51317#issuecomment-1070784669

> The value of this proposal, more suitable as a third-party library. And not the standard library.

FWIW, Ian commented on that here:

https://github.com/golang/go/issues/51317#issuecomment-1048301788

## Comment 1070787067

other (NONE) · hhstore · 2022-03-17T10:54:53Z · https://github.com/golang/go/issues/51317#issuecomment-1070787067

@Merovius @thepudds 


- https://github.com/heiyeluren/XMM
- You can take a look at the work done by this project. 
- XMM is a high performance third party memory manager for Go environments that is not affected by GC and guarantees high performance.




## Comment 1070789993

other (NONE) · creker · 2022-03-17T10:58:12Z · https://github.com/golang/go/issues/51317#issuecomment-1070789993

I would say the arguments are not convincing enough why this specific proposal should pass (apart from "someone from  Google needs it"). Saving 15% of memory and CPU is obviously convincing argument that something should be done. The question is, what exactly. Arena allocator doesn't seem to be good enough solution to outweight its usability problems that countless people already pointed out here. If Google employees want arena allocator that much they can easily maintain their own fork of Go and don't force everyone to deal with the conciquences of their decisions. In the end, arena allocation is trying to fix a deficiency in the GC. Why don't we instead talk about how we can improve GC/escape analysis/memory allocator?

## Comment 1070792484

other (NONE) · hhstore · 2022-03-17T11:01:16Z · https://github.com/golang/go/issues/51317#issuecomment-1070792484

> I would say the arguments are not convincing enough why this specific proposal should pass (apart from "someone from Google needs it"). Saving 15% of memory and CPU is obviously convincing argument that something should be done. The question is, what exactly. Arena allocator doesn't seem to be good enough solution to outweight its usability problems that countless people already pointed out here. If Google employees want arena allocator that much they can easily maintain their own fork of Go and don't force everyone to deal with the conciquences of their decisions. In the end, arena allocation is trying to fix a deficiency in the GC. Why don't we instead talk about how we can improve GC/escape analysis/memory allocator?

- Very well said.
- The Google's team wants arenas, which can fork themselves. And not imposed on everyone.
- Go should learn from Java and improve GC performance. Instead of discussing arena.



## Comment 1070805249

other (CONTRIBUTOR) · Merovius · 2022-03-17T11:16:45Z · https://github.com/golang/go/issues/51317#issuecomment-1070805249

@creker

> Saving 15% of memory and CPU is obviously convincing argument that something should be done. The question is, what exactly.

Feel free to suggest something else. The issue already contains a couple of such suggestions and their respective pros and cons.

> Arena allocator doesn't seem to be good enough solution to outweight its usability problems that countless people already pointed out here. 

Which is why this proposal is marked as "discussion ongoing", not "likely accept". We are still discussing the relative merits and issues of this proposal.

To repeat myself: If you don't want this proposal to get accepted, the best way is to continue that discussion and bring up new arguments. Instead of focussing on the assumption that it will be accepted anyways. Drawing out and complaining about that hypothetical does not help anyone. Indeed, it hurts, because it makes it harder for the proponents to find and address and potentially yield to the arguments against it.

As far as I can tell, the proponents of this proposal are following the discussion and have seen the concerns we've brought up about it. I have no reason to expect that they will not be addressed in some way, before a decision on it is made.

> If Google employees want arena allocator that much they can easily maintain their own fork of Go and don't force everyone to deal with the conciquences of their decisions.

I strongly object to painting this as an "Google against the rest of the community" issue. I do not work at Google, but we do use gRPC in production where I work. We would benefit from and welcome the savings, if they can be achieved in a non-intrusive way. Likewise, several Google employees have criticized and brought up issues with this proposal in this discussion.

The divide between Google employees and the rest of the community is, as far as I can tell, non-existent. And it's not helpful to draw it, because again, the helpful thing is to focus on the arguments for and against the design.

> In the end, arena allocation is trying to fix a deficiency in the GC. Why don't we instead talk about how we can improve GC/escape analysis/memory allocator?

We are. For example, [I brought up a previous attempt at solving this on the GC side here](https://github.com/golang/go/issues/51317#issuecomment-1063443027). Ian [responded to that comment here](https://github.com/golang/go/issues/51317#issuecomment-1063489884). It is simply false to imply that we are not talking about this.

## Comment 1070811983

other (CONTRIBUTOR) · Merovius · 2022-03-17T11:25:33Z · https://github.com/golang/go/issues/51317#issuecomment-1070811983

@hhstore 

> https://github.com/heiyeluren/XMM
> You can take a look at the work done by this project.
> XMM is a high performance third party memory manager for Go environments that is not affected by GC and guarantees high performance.

I don't speak chinese, so I can't read most of the documentation. Looking at [the API](https://pkg.go.dev/github.com/heiyeluren/XMM), I can't find a way to allocate Go types using it, or how it could be used to address the issues arenas are set out to solve. From what I can tell, the primary purpose of this package is to provide a high-performance Red-Black-Tree. Which is fair enough, but doesn't help with the allocations made by the protobuf package, for example.

I'm not doubting that it side-steps the garbage collector. Doing so is easy enough. But side-stepping the garbage collector is not the only thing arenas are about. For example, arena-allocated memory would be able to safely contain pointers to heap-allocated Go data. This, AFAIK, is impossible to do without co-operation from the GC. And it would be a necessity to solve the issues brought up around string values in this proposal - namely, you might have a proto-message, which contains a `string` field and we might want to `string` contents to be allocated on the heap, so that it can be safely used as a map-key.

## Comment 1070816680

other (NONE) · creker · 2022-03-17T11:31:03Z · https://github.com/golang/go/issues/51317#issuecomment-1070816680

@Merovius 

> We are. For example, https://github.com/golang/go/issues/51317#issuecomment-1063443027. Ian https://github.com/golang/go/issues/51317#issuecomment-1063489884. It is simply false to imply that we are not talking about this.

We aren't, I said "instead". The expectation is that counter-proposals not merely brough up but instead this specific proposal is rejected on the grounds that it tries to cover something that should be properly fixed in GC. I remember proposals when Go team straight up closed proposals on the same grounds - we don't do workarounds for GC issues, we fix them. Not only because it's just proper way of dealing with such issues. But also becase GC improvements benefit every single one of us. I would be glad if the same thing happened here but I have my suspicions. I probably wouldn't even comment here if I didn't.

## Comment 1070819251

other (NONE) · hhstore · 2022-03-17T11:34:16Z · https://github.com/golang/go/issues/51317#issuecomment-1070819251

@Merovius


https://github.com/gogo/protobuf

about the performance of gRPC, this library(gogoproto) can be used to alleviate the pain.


- Even so. I still don't think it's necessary to add it to the standard library. 
- This is like discussing the poor performance of Python, whether to remove the GC or not. 
- When struggling with poor performance, you should change the language such as: `Rust`. (I don't believe Google's engineers can't learn rust? Just kidding.)
- Instead of trying to turn `Python and Go` into `Rust`.


> The fundamental contradiction here remains: 

- This is the need of a few, not the majority.
- Most `Python users` don't care about the performance improvement at all. The same goes for `Go users`.
- Most `Python users` don't care about the performance improvement at all. The same goes for `Go users`.
- Most `Python users` don't care about the performance improvement at all. The same goes for `Go users`.

> The performance of Go is good enough for most people.
- Those who really care about `GC performance` have already chosen `Rust`.
- Choose to use Go to solve the problem that is suitable for Go. That's enough. 
- Each language has its own advantages, changing itself to someone else, just self-defeating.

## Comment 1070827324

other (NONE) · aierui · 2022-03-17T11:45:00Z · https://github.com/golang/go/issues/51317#issuecomment-1070827324

In TiDB, it similar implementation https://github.com/pingcap/tidb/blob/master/util/chunk/alloc.go#L51 and https://github.com/pingcap/tidb/blob/master/util/arena/arena.go
It looks like it cloud be replaced with arena.

## Comment 1070832576

other (CONTRIBUTOR) · Merovius · 2022-03-17T11:52:05Z · https://github.com/golang/go/issues/51317#issuecomment-1070832576

@creker 

> The expectation is that counter-proposals not merely brough up but instead this specific proposal is rejected on the grounds that it tries to cover something that should be properly fixed in GC.

From what I can tell, the best counter-proposal and attempt to properly fix this in GC failed, because it didn't manifest the expected savings. If you have a better solution, again, I strongly urge you to file a proposal to that effect. But "this should just be done by the GC" in and off itself is not a good argument, if *as best as we know right now* the GC can't solve this issue.

Specifically, the "Removing Arena Free" section of the proposal covers why the GC in its current form does not help - the main benefit from arenas seem to be the prompt and explicit freeing of arenas. The [Request Oriented Collector](https://github.com/golang/go/issues/51317#issuecomment-1063443027) was designed specifically to transparently get that benefit, but it empirically didn't pan out.

So, as far as I can tell, we tried the most obvious ways to "properly fix this in GC". What's left are non-obvious ways, but I don't think it is fair to accuse anyone of ignoring them, without making concrete suggestions of what they are. There has been pretty significant work done by the runtime team, to actually implement and test ROC. So I believe it is unfair to accuse them of not trying to solve this in the GC as much as they can.

And, to be repeat: **It is premature to make any assumptions about the outcome of this proposal**. At this point in time, it is just as likely that it will be rejected for lack of consensus, as it is to be accepted. So, please, at least wait until it gets marked as "likely accept" without addressing the problems brought up, before accusing anyone of pushing this through.

@hhstore Gogoproto [has been brought up](https://github.com/golang/go/issues/51317#issuecomment-1064419774). See the comment below that for a refutation that it gives the same benefits as arenas. For the rest of your comment [see the first paragraph here](https://github.com/golang/go/issues/51317#issuecomment-1070371858).

## Comment 1070846809

maintainer (MEMBER) · thepudds · 2022-03-17T12:10:35Z · https://github.com/golang/go/issues/51317#issuecomment-1070846809

>> https://github.com/heiyeluren/XMM
> 
> [...]
> But side-stepping the garbage collector is not the only thing arenas are about. For example, arena-allocated memory would be able to safely contain pointers to heap-allocated Go data. This, AFAIK, is impossible to do without co-operation from the GC. 

From quick look at the code, it appears to be memory unsafe even without pointers to heap-allocated Go data. It appears to allow memory corruption even if the memory is all XMM-managed.

FWIW, "it can panic with misuse" is a different category of saftey than "memory unsafe", which can open the door to credential stealing, remote code execution, Heartbleed-like excitement, and so on.

This proposal stays memory safe. See some of the comments above from @bcmills for some additional commentary on the saftey properties of this proposal.

In other words, I don't think anyone is suggesting it is not possible to do various forms of memory management in Go outside of the standard library (via a hand-rolled object pool, or mmap, or C malloc, or ____. For example, search pkg.go.dev for 'arena' or 'slab' or 'offheap'). 

Rather, I think the suggestion is it is not possible do to it outside of the standard library with similar safety and performance properties as this proposal. Whether or not it is worth it is of course the question and is an example of why the Go project has a proposals process in the first place, as @Merovius said.

## Comment 1070848780

other (NONE) · hhstore · 2022-03-17T12:12:57Z · https://github.com/golang/go/issues/51317#issuecomment-1070848780

What I want to express has been made clear. 

This is not a discussion of whether the implementation as a third-party library is difficult, whether to add it, or the question of who wants to add it. 


- Similar appeals from others in the past were directly rejected by Go officials.
- But here the Google employee's proposal is encouraged to discuss (pretend to discuss, the facts have decided to adopt?)
- It's ridiculous to pretend that this assumption doesn't hold up. 
- Community users aren't so stupid either. 


I will follow the outcome of this proposal. As predicted in my first response, if the "fake community" continues like this, then I won't pay any more attention to any of go's proposals. 

(Seriously, I hope the official finally proves that my prediction is wrong. although I am pessimistic about the final result.)


It's ridiculous to waste time pretending to participate in a discussion.

Probably for many people, it's time to learn some other programming languages.


## Some interesting screenshots:

- Note the `timeline` for `status changes` for this proposal
- https://github.com/golang/go/issues/51317#issuecomment-1049160908
    - Russ Cox changed the status of the proposal.
> Proposal creation time:

<img width="936" alt="image" src="https://user-images.githubusercontent.com/3252130/158926406-2bf250e5-f046-41ff-83e8-ef85e72ff26e.png">

> Status change time:( 1 day is enough?)

<img width="1045" alt="image" src="https://user-images.githubusercontent.com/3252130/158926304-8168d316-066e-4b2e-8c22-ca1689e1111b.png">


## Some similar closed proposals:

- https://github.com/golang/go/issues/43810



> Proposal creation time:

<img width="621" alt="image" src="https://user-images.githubusercontent.com/3252130/158927183-edb264c5-b910-4745-ac07-2ce7574a4dc7.png">

> Status change time: (It took 7 days to change the status)
<img width="734" alt="image" src="https://user-images.githubusercontent.com/3252130/158927443-27a5b90a-ce83-43d6-85ac-1d2713201c16.png">


## Has anyone told me the difference in response speed? 

- Is it a coincidence?




## Comment 1070898453

other (NONE) · beoran · 2022-03-17T13:00:44Z · https://github.com/golang/go/issues/51317#issuecomment-1070898453

What this proposal boils down to is to add a form of manually managed, non garbage collected memory to the Go standard library. I am convinced this increases performance and convenient for loading and unloading graphics in games and Gui applications. 

However, manual memory management was already possible in Go by using cgo, allocating memory using system calls, etc. Admitted, using manual memory management like this can be risky. We cannot store pointers to garbage collected memory in memory manually allocated like this.

What the current proposal  could add, by using the Go garbage collector, but actually does NOT add is memory safety. It only has a HeapString function, but if one stores a pointer to a heap object in the arena, the object can get inadvertantly garbage collected if the pointer in the arena is the only reamaining reference to it. This is the first example of the "spooky action at a distance " of this proposal as currently stated.

Or, if one keeps a pointer to an arena object in the heap, a panic can occur if that pointer is deferred. This has the effect that now, these pointers also have a "spooky action at a distance". 

So I fully understand that many people are opposed to this proposal, as it would make Go significantly more difficult to use. With arenas in the standard library, we would have to be very careful not to store pointers in the arena nor to refer to arena memory through pointers. Since arena pointers are identical to normal garbage collected pointers, they are easy to mix up.

Therefore I would propose that theis proposal should be modified to give more memory safety guarantees. For example the Arena.Free function could run a GC sweep on the arena to detect any pointers to heap in it, and conversely look up in the GC's structures if there are any pointers pointing into the arena. In both cases the Free should fail and return an error. A second modification could be to add arena.Pointer and arena.Slice to the package and return these on allocation, so the difference with normal pointers is preserved. I think other memory safety enhancements wich prevent spooky action at a distance are likely possible and should urgently be discussed.

## Comment 1070958119

other (CONTRIBUTOR) · Merovius · 2022-03-17T14:01:33Z · https://github.com/golang/go/issues/51317#issuecomment-1070958119

@beoran

> What the current proposal could add, by using the Go garbage collector, but actually does NOT add is memory safety.

This claim has been repeated a bunch of times above, but it just does not seem true, to me. At least not in the way I understand "memory safety" as in "it is impossible to accidentally read/write arbitrary memory". In particular, that's the thing famously lacking from `cgo`, `unsafe` and `syscall` and which leads to so many exploitable security holes in C software.

Arenas do not allow you to read/write arbitrary memory, so they are memory safe. It is simply wrong to lump them into the same category as `unsafe` et al. It would certainly preferable if arenas provided *more* safeties (all things being equal), in particular if they also provided type-safety (as it stands, they violate safety invariants of `string` and arguably pointer types). But it should be possible to disagree with the proposal and criticize its deficiencies, without exaggerating them.

> if one stores a pointer to a heap object in the arena, the object can get inadvertantly garbage collected if the pointer in the arena is the only reamaining reference to it.

Is that so? The proposal says:

> Each chunk and all the objects that it contains fully participate in GC mark/sweep until the chunk is freed. In particular, as long as a chunk is part of an arena that has not been freed, it is reachable, and the garbage collector will follow all pointers for each object contained in the chunk. Pointers that refer to other objects contained in the chunk will be handled very efficiently, while pointers to objects outside the chunk will be followed and marked normally.

This seems to directly contradict that claim.

> In both cases the Free should fail and return an error.

What would the user be expected to do with such an error? Try again? Crash? Log? It doesn't seem an actionable error, given that the respective code likely has little control over what references are causing it.

## Comment 1070970651

other (NONE) · beoran · 2022-03-17T14:40:23Z · https://github.com/golang/go/issues/51317#issuecomment-1070970651

@hhstore It is true that apart from sync.Pool, there were several issues related to manual memory management that were rejected, like #43810, #50418, #43810, ... Also, often knobs on the Garbage Collector were rejected as well and have in stead the GC was improved. So I feel I understand your point of view.

But, more importantly: even proposals by the go team members can and do get rejected, see #22624, #21161... So if you are opposed to this proposal, then it is definitely useful to keep on explaining just why.

@Merovius 

I can agreein that this proposal offers better memory safety than CGO/unsafe/syscall memory allocation. But getting my program terminated because some library called Arena.Free when I happen to defer a pointer pointing into the Arena, even indirectly, will make Go significantly harder to use. In other words, it is a bit better than manual memory management in Go right now, but not by much.

Before this proposal, I could be sure that a non nil pointer, non unsafe.Pointer, could be deferred safely without having to think about memory management. With this proposal this important property of Go is gone. 

This indicates to me that we need to add at least an arena.Pointer type to segregate arena memory from normal memory. Basically, it should not be allowed to have any normal pointers pointing into the arena at all, in order to keep the normal pointers in Go working as they do now.

Sorry, i forgot to to add on calling Free, in my part about GC/heap pointers stored in an arena. Whap happens if the arena is freed with sole  pointers to heap objects?

What is most scary about the proposal is the "implementation" part:

"In order to fit with the Go language, we require that the semantics of arenas in Go be fully safe. However, our proposed API has an explicit arena free operation, which could be used incorrectly. The application may free an arena A while pointers to objects allocated from A are still available, and then sometime later attempt to access an object allocated from A.

Therefore, we require that any implementation of arenas must prevent improper accesses without causing any incorrect behavior or data corruption. Our current implementation of the API gives a memory fault (and terminates the Go program) if an object is ever accessed that has already been freed because of an arena free operation."

This is a serious burden on us Go programmers, whom if this proposal is accepted, must now carefully avoid making or returning any pointers to anything inside an arena, lest their programs panic mysteriously when Arena.Free is called in some remote  library. Anything in an arena that needs to be kept on the GC/heap will have to be copied out. This is what I mean by spooky action at a distance. Without more stringent memory safety for this feature, such as specific area pointers, I would rather have this proposal rejected.

As for the error return, the library using Arena can allocate a new arena copy everything over from the old one into the new arena if necessary,  and signal the problem to the user of the library. Seems actionable enough to me. By the way, arena allocations should probably also return an error in case no suitable slab of memory can be allocated. The library could then still try to use GC/heap memory in stead.

## Comment 1071146988

other (CONTRIBUTOR) · Merovius · 2022-03-17T17:51:22Z · https://github.com/golang/go/issues/51317#issuecomment-1071146988

> Before this proposal, I could be sure that a non nil pointer, non unsafe.Pointer, could be deferred safely without having to think about memory management.

I don't think this is as true as you might think. Dereferencing a pointer can lead to a data-race, if the pointee is concurrently modified. Which means that, in full generality, dereferencing a pointer might not be memory safe.

This might seem like a nitpick. But the specific case people are worried about is code being passed an arena-pointer, retaining that and later dereferencing it. That *exactly* the same bug if, for example, the gRPC framework would store proto messages in `sync.Pool`s for later re-use. Except that with arenas, that bug will lead to a debuggable and safe panic, whereas with `sync.Pool` it would (potentially) lead to a data-race and loss of memory safety.

Point is, we already rely quite a lot on outside of the typesystem restrictions such as "don't concurrently modify data" or "don't retain data after returning", which doesn't seem to present that much of a problem, in practice.

> This indicates to me that we need to add at least an arena.Pointer type to segregate arena memory from normal memory.

Maybe. To me, if that's the price we need to pay for arenas, it's not worth paying. One of the main concerns with arenas is that their usage would pollute and "infect" APIs. Special pointer/string/slice types would make this problem significantly worse.

For example, for protobuf to then take advantage of arenas, the generated protobuf code would have to use these special arena-pointers *everywhere*. So every usage of protobuf would now have to deal with arena-specific types. Or we'd have to generate two separate types for every proto-message, one using arenas and one without.

Same, of course, with `encoding/json`. Except there, it is even *more* common to just pass your normal struct types to `json` and use them as-is.

IMO that would be unacceptable.

There's also a question of how this would look, in practice:

- Making it `type Pointer[T any] *T` would be useless, as [`*Pointer[T]` would then be assignable to `*T`](https://go.dev/play/p/3p-LEtnBgOF). So it would lose any "safety" anyways.
- We could make it `type Pointer[T any] struct { p *T }` with methods for getting/setting the value. But then it would no longer implement any of `*T`'s methods and wouldn't satisfy any interfaces.
- We could make it `type Pointer[T any] struct { P *T }`, but then people can just access the field and get a plain pointer to arena-memory
- And in any case - if it's possible to call a method on `*T` (which we probably want to allow), then that method can get a plain pointer via its receiver.

I don't think a special pointer type is really practical, TBQH.

> As for the error return, the library using Arena can allocate a new arena copy everything over from the old one into the new arena if necessary, and signal the problem to the user of the library. Seems actionable enough to me.

And not `Free` the original arena, leaking a large chunk of memory?

> By the way, arena allocations should probably also return an error in case no suitable slab of memory can be allocated

The proposal says about this:

> There may be an implementation-defined limit, such that if the object or slice requested by calls to `a.New` or `a.NewSlice` is too large, the object cannot be allocated from the arena. **In this case, the object or slice is allocated from the heap.**

Which seems like a reasonable way to deal with this problem. In particular, it allows us to transparently use heap-allocations on platforms without arena-support, while the application code just has to use one set of APIs.

Note that allocations in Go generally do not return errors and allocation failures are not recoverable. So Go has a pretty well-established to prefer simple allocation patterns without a need to check the result.

## Comment 1071457238

other (NONE) · CannibalVox · 2022-03-17T20:54:13Z · https://github.com/golang/go/issues/51317#issuecomment-1071457238

@Merovius 

> This might seem like a nitpick. But the specific case people are worried about is code being passed an arena-pointer, retaining that and later dereferencing it. That exactly the same bug if, for example, the gRPC framework would store proto messages in sync.Pools for later re-use. Except that with arenas, that bug will lead to a debuggable and safe panic, whereas with sync.Pool it would (potentially) lead to a data-race and loss of memory safety.

It's very difficult to assess the proposal, because this is, I think, objectively true, that arenas are no less safe than sync pools, and like sync pools, I can think of several use cases that don't particularly scare me (outside the string thing that you & I have talked to death). However, as I've stated, I would never use sync pools to retrieve & store inbound request objects. And I certainly wouldn't use sync pools for every single level of an inbound request object, such that I could never safely store any pointer from anywhere in the request. 

This latter part is not explicitly part of the proposal, though. But on the other hand, would this proposal's acceptance be seen as clearing the way for that feature? If that feature was proposed separately and rejected by the community, would this be seen as a waste?

I would like to see arenas accepted (probably with just heap-allocating all strings as a simple shim), and I would like to see better performance for request & response marshalling. I don't think I would like to see the former used as a solution for the latter without more serious changes. 

Sync pools are frequently used as solutions in somewhat self-contained systems. It would be unreasonable to create a framework that presses large amounts of backend code to service ensuring the sync pool is respected. I think it would be even more unreasonable to do it as a change to an existing backend framework.


e: 
> I don't think a special pointer type is really practical, TBQH.

I think it would have to be something much more invasive like a key word. `arena *T` can be passed to `arena *T` but not `*T` and `*T` can be passed to both. I suspect that wouldn't fly, but I think it's the only way to make arenas type safe.

## Comment 1071519009

other (NONE) · creker · 2022-03-17T21:31:59Z · https://github.com/golang/go/issues/51317#issuecomment-1071519009

@Merovius 

> Maybe. To me, if that's the price we need to pay for arenas, it's not worth paying. One of the main concerns with arenas is that their usage would pollute and "infect" APIs. Special pointer/string/slice types would make this problem significantly worse.

We need to remember the context in which that concern was brough up - the inherent unsafety of arena allocated pointers. Infection of APIs is probably inevitable if arenas were to be accepted but if we require special types then we at least have clear distinction as to which pointers are safe and which aren't. It would actually help alleviate the "infection" problem. The real problem with special pointers is they don't offer any real guarantees without the help from type system. They're merely self-documenting way of delineating potentially unsafe objects.

> For example, for protobuf to then take advantage of arenas, the generated protobuf code would have to use these special arena-pointers everywhere. So every usage of protobuf would now have to deal with arena-specific types. Or we'd have to generate two separate types for every proto-message, one using arenas and one without.

The more I think about protobuf example the more I think the real problem is not with Go not having arena allocation or some other efficient way of allocation but the design of protobuf. I don't use them much but it looks like the current protobuf project uses pointers everywhere. Obviously this would force insane amount of allocations. Instead of arena allocation protobuf should switch to values everywhere and solve pretty much all GC problems that way. Why it isn't that way (it looks like older implementation did use values) I don't know. Then the question would be, do arenas still give any performance benefits when used internally without ever exposing them to the public API? 

So if we ignore protobuf example where arenas have to be visible in public API, what other examples where arena allocation can improve performance? Is there many of them? Do they really need it to be in the standard library or third-party implementation would suffice? I think another reason people are suspicious is due to lack of clear examples apart from protobuf which again is Google's creation. Protobuf is important and all but it's just one use-case. I would think barrier for inclusion in the standard library is much higher than that.

## Comment 1071538133

other (NONE) · CannibalVox · 2022-03-17T21:39:31Z · https://github.com/golang/go/issues/51317#issuecomment-1071538133

I would expect people to want to use arenas or something like them for any case in which you are unmarshalling request data for inbound requests or constructing outbound requests. That includes protobuf, but also json or any number of other things.

As for protobuf's propensity for pointers, fields have to be optional in protobuf. Using pointers to indicate the presence or absence of a field isn't the only way to do things, but it is a common and convenient way.

## Comment 1071546179

other (CONTRIBUTOR) · Merovius · 2022-03-17T21:42:29Z · https://github.com/golang/go/issues/51317#issuecomment-1071546179

@CannibalVox `sync.Pool` was just an example, FWIW. As we mentioned above, the situation isn't really any different from `io.Reader/Writer` or any number of APIs which make assumptions about the validity and lifetime of values passed by or returned from them. My point was that our feelings about what is "safe" are often misleading. Even the most basic operations, like dereferencing a pointer, accessing a map or using `append` are only safe as long as we keep to a set of frankly complicated and often implicit rules about the lifetime and access patterns of values we use them with.

> I would expect people to want to use arenas or something like them for any case in which you are unmarshalling request data for inbound requests or constructing outbound requests.

I don't think outbound requests are really a concern. They are far too unergonomic for that use-case.

@creker 

> Infection of APIs is probably inevitable if arenas were to be accepted but if we require special types then we at least have clear distinction as to which pointers are safe and which aren't.

I think there is very much a difference in quantity which becomes a difference in quality. For example, I don't really see a reason why a gRPC service implementation would have to ever know anything about arenas. It is apparently unavoidable that the protobuf API adds one function to unmarshal using an arena - but after that, the gRPC framework can make arenas fully transparent (except for the documentation that requests can't be retained after the request handler returns).

That's a *very different* situation from every user of gRPC being exposed to the concept.

Also, at the danger of sounding like a broken record: Arenas are memory safe. It is tiring to repeatedly having to refute the claim that they aren't.

> Instead of arena allocation protobuf should switch to values everywhere and solve pretty much all GC problems that way. Why it isn't that way (it looks like older implementation did use values) I don't know.

Then let me introduce you to [Chesterton's Fence](https://en.wikipedia.org/wiki/G._K._Chesterton#Chesterton's_fence). The way protobuf generated code uses pointers is forced by constraints of what the format requires. It wasn't done by chance.

> Do they really need it to be in the standard library or third-party implementation would suffice? 

Please stop bringing this up. It has been mentioned a couple of times, even very recently, why this can't be done in a 3rd party library. Arenas have to live in the standard library, or not exist at all.

## Comment 1071565608

other (NONE) · CannibalVox · 2022-03-17T21:50:18Z · https://github.com/golang/go/issues/51317#issuecomment-1071565608

> As we mentioned above, the situation isn't really any different from io.Reader/Writer or any number of APIs which make assumptions about the validity and lifetime of values passed by or returned from them.

I don't think io.Reader/Write is a very good example but I'm probably misunderstanding.  The Reader/Writer itself may not be valid after storage due to some nonsense done to the underlying object, but that fact is implicit to the Reader/Writer types- if you receive a Reader, you understand that you are largely intended to read from it and throw it away. By contrast, a random pointer *UserInfo may reasonably be considered safe to store today, but the fact that secretly that object is in a sync pool, or was allocated from an arena makes it unsafe.

> I don't think outbound requests are really a concern. They are far too unergonomic for that use-case.

On the contrary, this was the primary use case of gogoproto's sync pool implementation, the performance results were very good, and there is no concern about people up the call stack holding the request in that case. It's a great use case for arenas without any of the baggage that we've been talking about.



## Comment 1071587933

other (NONE) · creker · 2022-03-17T21:59:41Z · https://github.com/golang/go/issues/51317#issuecomment-1071587933

@Merovius 

> Arenas are memory safe. It is tiring to repeatedly having to refute the claim that they aren't.

People keep bringing unsafety because we have different opinions on what unsafety is. For me the possibility of a panic just because I access some object I shouldn't have is unsafety. It's not unsafe in the sense it would corrupt or leak something. It's unsafe in that it violates the guarantees that GC gives and the advantages it brings - the ability to completely forget about lifetimes. Yes, sync pools do already violate it. That doesn't change anything. Sync pools probably were a mistake also but that train already left. We can still stop arenas.

> The way protobuf generated code uses pointers is forced by constraints of what the format requires. It wasn't done by chance.

That's clearly false. Anything that is conveyed by pointers can be implemented through additional metadata fields (again, without additional allocations) that indicate optional fields or whatever you need. Pointers are convenient but they're not required, at all. If they're please describe something that can't be implemented any other way.

## Comment 1071604306

other (NONE) · CannibalVox · 2022-03-17T22:06:40Z · https://github.com/golang/go/issues/51317#issuecomment-1071604306

> That's clearly false. Anything that is conveyed by pointers can be implemented through additional metadata fields (again, without additional allocations) that indicate optional fields or whatever you need. Pointers are convenient but they're not required, at all. If they're please describe something that can't be implemented any other way.

FWIW google does this with some internal protobuf implementations (not go, but my point is that this is not out of the question). This reduces the allocation count, though, but not the throughput (and in fact increases the throughput) so I'm not convinced it's a substantial improvement.

Most of the improvements around unmarshalling code I've seen have centered around eliminating reflection from the picture. Gogoproto generates unrolled marshalling/unmarshalling code, there are json libraries that generate JIT. I'm curious how the arena stacks up to gogoproto.

I do take issue with this, though (which is why I'm sanguine on the proposal if not the use case):

> Sync pools probably were a mistake also but that train already left. We can still stop arenas.

Sync pools have been a valuable tool for many, including myself. Properly managed, they can be very powerful and very safe.  It's all about blast radius. The truth is, I doubt that you have actually been bitten by sync pools, because there aren't very many opportunities to encounter a bare pool you didn't write. Most of the time, I doubt you realize that they exist. Arenas **could** be like that, and provide a powerful tool. If everyone has to be aware of the lifetime of their objects anytime they write a grpc service, they will **not** be like that, though.

## Comment 1071653098

other (NONE) · creker · 2022-03-17T22:25:50Z · https://github.com/golang/go/issues/51317#issuecomment-1071653098

@CannibalVox I agree, sync pools are very valuable but I've seen cases where they made things worse and in some cases forced developers to remove them. In those cases users are affected indirectly. For example, through memory usage suddenly ballooning and subsequent OOM. Arenas would suffer the same fate, I fear. People will start shoving them into every corner of their libraries.

## Comment 1071717695

other (CONTRIBUTOR) · Merovius · 2022-03-17T22:46:44Z · https://github.com/golang/go/issues/51317#issuecomment-1071717695

@creker

> For me the possibility of a panic just because I access some object I shouldn't have is unsafety.

According to this definition, almost no operation in Go is safe. That's not a practical way to use the word.

> If they're please describe something that can't be implemented any other way.

```proto
message M { M x = 1; }
```

Again, the generated code is done that way for a reason. [If you can't see that reason, you should sit down and think about the reasons, before claiming it's unnecessary](https://en.wikipedia.org/wiki/G._K._Chesterton#Chesterton's_fence).

@CannibalVox 

> On the contrary, this was the primary use case of gogoproto's sync pool implementation

I'll take you at your word. Personally, I find the thought unbearable, having to do `var x *Message; a.New(&a)` for every nested message, when constructing a response - not to mention passing around the arena in the first place. Most people already found it unbearable having to type `proto.String("foo")` (before proto3 made that unnecessary).

## Comment 1071720399

other (CONTRIBUTOR) · Merovius · 2022-03-17T22:47:52Z · https://github.com/golang/go/issues/51317#issuecomment-1071720399

@CannibalVox 

> I don't think io.Reader/Write is a very good example but I'm probably misunderstanding. The `Reader/Writer` itself may not be valid […]
 
It's not about the `io.Reader/Writer`, but about the arguments passed to their methods.

## Comment 1072020434

reporter (CONTRIBUTOR) · danscales · 2022-03-18T04:27:33Z · https://github.com/golang/go/issues/51317#issuecomment-1072020434

> but if one stores a pointer to a heap object in the arena, the object can get inadvertantly garbage collected if the pointer in the arena is the only reamaining reference to it. This is the first example of the "spooky action at a distance " of this proposal as currently stated.

Just want to clarify - the objects in an arena must (and do) fully participate in garbage collection until the arena is freed.  Therefore, a heap object will not be freed inadvertently because the only remaining pointer to it is from an object in an arena.  No pointers to heap objects can ever become invalid or point to incorrect data because of the use of arenas (and no incorrect data can happen at all with arenas).  As we have said, the only "unexpected" thing that can happen is that the use of a pointer to an object in a freed arena can lead to a panic/exception.  (@Merovius  responded about this question as well, but just want to make sure this was clear.)


## Comment 1072051419

other (NONE) · typeless · 2022-03-18T05:39:33Z · https://github.com/golang/go/issues/51317#issuecomment-1072051419

Regarding the potentially viral API changes, it seems arenas should be embedded into structs rather than being passed around through the call stack. So, instead of `json.UnmarshalWithArena(arena, buf, &myobj)`, this would probably be cleaner: 
```
dec := json.NewDecoder(r)
dec.Allocator = arena.New()  // When dec.Allocator is nil, it will use the global heap by default.
err := dec.Unmarshal(buf, &myobj)
``` 


## Comment 1072062808

other (CONTRIBUTOR) · Merovius · 2022-03-18T06:09:47Z · https://github.com/golang/go/issues/51317#issuecomment-1072062808

@typeless Personally, I think passing them as an argument is cleanear and clearer. Because it makes it obvious that they are not supposed to be long-lived values to be kept around.

## Comment 1072112827

other (NONE) · beoran · 2022-03-18T07:54:11Z · https://github.com/golang/go/issues/51317#issuecomment-1072112827

@creker Agreed, this is what I am getting at. Memory safety in Go is not a yes/no issue, there are different "levels" so to speak. But the current proposal's Arena seems to be at the same level as sync.Pool or perhaps worse. Seeing how troublesome sync.Pool can be, I would prefer this proposal to be improved so it provides a lot better memory safety than sync.Pool.

@Merovius , sorry, but race conditions are orthogonal to memory management, so yes, to me they are a nitpick in this discussion. OTOH sync.Pool is relevant though, but mostly if an example of an API i would like to improve on. The arena.Pointer could only be an advisory wrapper, without loss of convenience for the users of Arenas. That would help to set them apart from normal pointers and could also help with later vet checks on abuses of Arenas.

As for making arenas a third party library, that would be possible if the Go garbage collector had a few more knobs available. I could definitely implement arenas in Ruby or Mruby since their garbage collectors have a wide API that allows to mark GC roots, sweep areas, etc. But addi g these GC knobs is likely to be even more controversial than arenas are.

@danscales Thanks for making that very clear. I admit my first "spooky action" was my misunderstanding of this proposal. But not the second one. As you admit, the only unexpected thing that can happen is that the use of a pointer to an object in a freed arena can lead to a panic/exception. But that is a very inconvenient "only", as I and many others here are trying to explain here.

To be very clear. I do like the idea of manual memory management in Go. This would be useful for my use cases such as gaming and GUI. But I don't agree with the current proposal because I think we can do better. For example, apart from separate pointers, a tree allocator in stead of a slab allocator also has additional memory safety benefits. Let us discuss other ways in which we can improve this proposal.

## Comment 1072180437

other (NONE) · creker · 2022-03-18T08:39:42Z · https://github.com/golang/go/issues/51317#issuecomment-1072180437

@Merovius 

> According to this definition, almost no operation in Go is safe. That's not a practical way to use the word.

It is. If I have a pointer to a struct and I don't do anything with it (or any other part of my application) I know for a fact that in correct race free code it will stay that way forever. That's one of the most basic safety features of GC and Go in general. With arenas this is no longer true. Pointers are detached from arenas. I call free on arena and suddenly some object somewhere in the program becomes invalid and triggers panic. This is why I and others suggesting some way to better "attach" pointers to arenas. Maybe through special wrapper type. Maybe by getting rid of Free and doing it completely automatic. But something to make them safe (-er) in that specific sense.

> Again, the generated code is done that way for a reason.

ok, fair enough, recursive messages can be problematic, not only in protobuf. But I don't see how that one exception should mean "everything is a pointer". There're ways to solve that and keep GC happy (the simplest of which is to use pointers where there's recursion). So although your example is problematic it's in no way proves to me that current design is the only way to do it and was forced on developers. Developer chose that design and now suffering the consiquences. Trying to fix that design with dangerous additions to std lib seems backwards.


## Comment 1072237888

other (CONTRIBUTOR) · Merovius · 2022-03-18T09:37:24Z · https://github.com/golang/go/issues/51317#issuecomment-1072237888

@beoran

> sorry, but race conditions are orthogonal to memory management, so yes, to me they are a nitpick in this discussion.

To me, this implies that your objection is not about the actual guarantees provided by the language, what kind of code is or is not safe and how hard it is to write correct code. But about semantics and what to call problems, when they occur. I don't think that's how we should evaluate proposals.

> But I don't see how that one exception should mean "everything is a pointer".

The point is that I am not going to argue with you about a design which a bunch of intelligent and thoughtful engineers have spent weeks or even months scrutinizing when you are not willing to spend even a couple of minutes thinking about their reasoning.

I'm not even saying that the generated code couldn't use *fewer* pointers, if it was willing to pay for it in other regards. After all, the point of Chesterton's Fence isn't that the fence should *never* be torn down. It's just that it should only be torn down after you have shown that you considered the consequences of doing so, by understanding why it was put there in the first place.

## Comment 1072280196

other (NONE) · beoran · 2022-03-18T10:32:47Z · https://github.com/golang/go/issues/51317#issuecomment-1072280196

@Merovius Please do not put words in my mouth. I imply nothing of the sort. I say what I say, please answer only to that. Of course, preventing race conditions is important. But it is a tangent to this discussion. Unless if arenas were to lessen the chance for race conditions somehow, which does not seem the case.

@hhstore I read your translated angry blog post. Although it could do without the swear words I can see how some people could think that proposals from Google employees seem privileged. I think it is a bad sign when people start rage quitting a programming language. I saw it for Ruby before and it definitely contributed to the decline of that language... For the future of Go, I  think we should make sure that all proposals are treated even handedly.

@creker Thanks for (re)stating my ideas better. I think we are in full agreement.

## Comment 1072286671

other (NONE) · creker · 2022-03-18T10:41:15Z · https://github.com/golang/go/issues/51317#issuecomment-1072286671

@Merovius it's useless for me to think about reasoning of other people. For all I know, protobuf developers just though, the heck with it, let's use pointers everywhere. The only practical way of dealing with design issues is to ask, why things were designed that way. That's why I'm asking because you seem to imply you know the reasoning but keep deflecting my questions with wiki articles I don't care about. Either stop being so agressive and just ignore my questions when you already told everyone that you're not Google employee and not affiliated with them (so, why you even care?). Or let's have reasonable discussion about design of protobuf. After all, this proposal is only concerned with that, looking at how it lacks any other meaningful examples.

## Comment 1072406254

other (NONE) · tooolbox · 2022-03-18T13:23:15Z · https://github.com/golang/go/issues/51317#issuecomment-1072406254

I've been following this thread loosely and I just re-read most of it, couple of comments.

1. There's obviously some contentious points here because the proposal deals with the balance between performance and safety of the language. I think it would be good for everyone to put renewed effort into keeping the discussion analytical and amicable.
2. My opinion is that it's not useful to discuss the design of the Protobuf library (pointers, no pointers) because we can find other scenarios that involve many allocations and could therefore benefit from an arena.  So I suggest the conversation focuses on arenas themselves as much as possible, despite Protobuf being the motivation of and example used in the proposal.
3. I see the draw of arenas from a performance perspective.
4. I am...not super concerned...about safety issues. Maybe I should be. I think it would help to have realistic sample programs showing how a Go dev could "get arenas wrong" and cause panics. All this talk of relative safety and guarantees is highly theoretical.
5. Would it be accurate to say that, in practice, one should never *return* an Arena? It's created, work is done, it's freed, typically in the same scope even.
6. My current biggest concern is the proliferation of Arenas in function signatures, similar to Context. I also don't think hiding the Arena in a Context or other struct is the key. I'm curious what other alternatives could be explored, maybe slightly more runtime magic would be acceptable given that this whole thing is a tradeoff of safety for performance and one must Know What One Is Doing.


## Comment 1072421187

other (CONTRIBUTOR) · Merovius · 2022-03-18T13:39:48Z · https://github.com/golang/go/issues/51317#issuecomment-1072421187

@toolbox

> Would it be accurate to say that, in practice, one should never return an Arena? It's created, work is done, it's freed, typically in the same scope even.

I would agree with that recommendation.

> My current biggest concern is the proliferation of Arenas in function signatures, similar to Context. I also don't think hiding the Arena in a Context or other struct is the key. I'm curious what other alternatives could be explored, maybe slightly more runtime magic would be acceptable given that this whole thing is a tradeoff of safety for performance and one must Know What One Is Doing.

What are you imagining? [I've argued before](https://github.com/golang/go/issues/51317#issuecomment-1063434467) (and [also here](https://github.com/golang/go/issues/51317#issuecomment-1063488218)) that I don't think arena-allocation should ever happen implicitly. And I think it is very likely that a non-trivial depth of calls need to use the same arena. I can't really imagine a solution to this which does not involve explicitly passing an arena.

## Comment 1072443515

other (CONTRIBUTOR) · bcmills · 2022-03-18T14:04:29Z · https://github.com/golang/go/issues/51317#issuecomment-1072443515

@creker
> It's unsafe in that it violates the guarantees that GC gives and the advantages it brings - the ability to completely forget about lifetimes.

That's not what a GC gives you. The GC [simulates infinite memory](https://devblogs.microsoft.com/oldnewthing/20100809-00/?p=13203), and it allows you to avoid writing about lifetime properties that are trivial or obvious in the code. If you “completely forget about lifetimes”, then your program will be prone to data races, aliasing bugs, and/or memory leaks.

Arenas don't violate the principles of the GC: they don't cause it to stop simulating infinite memory, and they don't cause you to have to write down lifetime properties that are otherwise obvious.

## Comment 1072490989

maintainer (MEMBER) · adonovan · 2022-03-18T14:56:52Z · https://github.com/golang/go/issues/51317#issuecomment-1072490989

> Arenas don't violate the principles of the GC: they don't cause it to stop simulating infinite memory, and they don't cause you to have to write down lifetime properties that are otherwise obvious.

I think that depends exactly how you define the principles of GC. If your program avoids the unsafe package, or uses it only in ways that are completely encapsulated, then the GC guarantees that `if p != nil { x = *p }` will not crash, even if the value of x is completely unspecified. Arenas violate this guarantee. This argues for arenas to belong in the unsafe package, but by design, arenas are unlikely to be used in ways that completely encapsulate their unsafe behavior, so programmers will need to think about a new class of lifetime properties.


## Comment 1072499984

other (NONE) · tooolbox · 2022-03-18T15:06:07Z · https://github.com/golang/go/issues/51317#issuecomment-1072499984

> What are you imagining? https://github.com/golang/go/issues/51317#issuecomment-1063434467 (and https://github.com/golang/go/issues/51317#issuecomment-1063488218) that I don't think arena-allocation should ever happen implicitly. And I think it is very likely that a non-trivial depth of calls need to use the same arena. I can't really imagine a solution to this which does not involve explicitly passing an arena.

I fully concur that arena allocations should not happen implicitly, rest easy there.

Don't laugh, but my initial thought was similar to the `arena.Run()` concept except with package-level `arena.Allocate()` functions that use whatever Arena is active and fall back to the normal allocation strategies if there isn't one. That way packages like `json` or `sql` could opt into using one transparently if the caller has one active.

```go
import "runtime/arena"

func Decode() {
    arena.Run(func() {
        Process()
    }) // anything allocated with arena.Allocate() is freed at this point
}

func Process() {
    obj := arena.Allocate[int]() // uses Arena
    obj2 := &MyStruct{} // does not use Arena
    // ...
}
```

*(If we don't like the closure, this could be done with just `arena.New()` and `arena.Free()` and vet could warn if you don't call `arena.Free()` before exiting the scope where you called `arena.New()`.)*
    
This is essentially: keeping the Arena out of signatures by storing the reference to it in the stack/goroutine/runtime. Nested `arena.Run()` calls could be allowed, however it wouldn't work for a scenario where any given portion of a call stack cared about allocating into more than one Arena at a time.

This concept makes things less explicit, and I do value explicitness highly, but I'm bothered enough by proliferating `*arena.Arena` to bring this up. Probably the fact that Go's base case is abstracting away memory management makes it less icky to me, as well.

I had another idea but I realized it was not safe for concurrent use of a package, so I won't bother detailing it here :)

## Comment 1072514732

other (CONTRIBUTOR) · Merovius · 2022-03-18T15:21:34Z · https://github.com/golang/go/issues/51317#issuecomment-1072514732

@toolbox

> Don't laugh, but my initial thought was similar to the arena.Run() concept except with package-level arena.Allocate() functions that use whatever Arena is active and fall back to the normal allocation strategies if there isn't one. 

I don't think this would work. The situation is made up, but:

```go

var X struct { X *int }

func B() {
    json.Unmarshal([]byte(`{X:42}`), &X)
}

func A() {
    arena.Run(B)
    if X.X != nil {
        fmt.Println(*X.X) // boom
    }
}
```

Assuming `json.Unmarshal` would transparently use arenas this way and `B` does not know about arenas, this code would crash.

If arenas must be passed explicitly, then `B` wouldn't pass an arena, so the memory for `X.X` would be heap-allocated and everything is fine.

## Comment 1072518049

other (CONTRIBUTOR) · bcmills · 2022-03-18T15:25:05Z · https://github.com/golang/go/issues/51317#issuecomment-1072518049

@adonovan

>  If your program avoids the unsafe package, or uses it only in ways that are completely encapsulated, then the GC guarantees that `if p != nil { x = *p }` will not crash, even if the value of x is completely unspecified. Arenas violate this guarantee.

It makes no such guarantee today. To wit: https://go.dev/play/p/mwkOix5VzSV.

## Comment 1072538570

other (NONE) · tooolbox · 2022-03-18T15:48:14Z · https://github.com/golang/go/issues/51317#issuecomment-1072538570

> I don't think this would work. The situation is made up, but:

I admire your ability to concoct edge cases :)

However, I'm not sure that's a valid criticism of what I'm suggesting. And don't get me wrong, I don't want to die on a hill over this, but let me rewrite your example back into the current proposed syntax:

```go
var X struct { X *int }

func B(a *arena.Arena) {
    json.UnmarshalArena(a, []byte(`{X:42}`), &X)
}

func A() {
    a := arena.New()
    B(a)
    a.Free()
    if X.X != nil {
        fmt.Println(*X.X) // boom
    }
}
```

Your example seems more like an illustration of the dangers of accessing an Arena after it's been freed, no?

## Comment 1072549865

other (CONTRIBUTOR) · Merovius · 2022-03-18T15:59:11Z · https://github.com/golang/go/issues/51317#issuecomment-1072549865

@toolbox But in that code, `B` *has to know* about the arena. So it can decide whether or not `X` should be allocated in an arena or not.

The point I was trying to make is that your idea does not allow to allocate *some* json-values into an arena and *some* not. An RPC server might both allocate the request data into an arena *and* lazily load some config or store other state resulting from interacting with a backend service. The `json` package, unless you explicitly tell it which you want, can't tell the difference, because both happen down-stack from `arena.Run`.

So to be explicit: I said that `B` doesn't know about the arena, so the actual rewrite would be

```go
var X struct { X *int }

func B() {
    json.Unmarshal([]byte(`{X:42}`), &X)
}

func A() {
    a := arena.New()
    defer a.Free()
    B()
    if X.X != nil {
        fmt.Println(*X.X) // 42
    }
}
```

Which is, of course, totally fine.

## Comment 1072575162

other (NONE) · CannibalVox · 2022-03-18T16:23:37Z · https://github.com/golang/go/issues/51317#issuecomment-1072575162

> @toolbox But in that code, `B` _has to know_ about the arena. So it can decide whether or not `X` should be allocated in an arena or not.

This seems like the other side of the coin of concerns other people have raised about accessing these pointers. If there's no need to provide notification or safety to accessors of arena pointers, surely there's no reason to provide notification or safety to allocators of arena pointers?

e: at the very least, for the allocators, the owner of the arena is in much more control over the operation. It's more difficult to say the same about where every pointer you pass to a library ends up.

## Comment 1072598823

other (NONE) · beoran · 2022-03-18T16:52:08Z · https://github.com/golang/go/issues/51317#issuecomment-1072598823

@bcmills That example looks like a race condition to me, which as I stated above seems lIke a tangent to memory safety to me.

I hate to repeat myself, but a hierarchical allocator similar to this one for C, could help ensure that memory gets allocated and freed at the right place in the call stack : https://github.com/esneider/talloc. 

## Comment 1072622918

other (NONE) · tooolbox · 2022-03-18T17:20:29Z · https://github.com/golang/go/issues/51317#issuecomment-1072622918

Firstly, I do see your point, but I'm going to split hairs for a second. I'll swap your latest example back to the `Run()` syntax:

```go
var X struct { X *int }

func B() {
    json.Unmarshal([]byte(`{X:42}`), &X)
}

func A() {
    arena.Run(func(){})
    B()
    if X.X != nil {
        fmt.Println(*X.X) // 42
    }
}
```

Yes, totally fine :)

But yes, joking aside, I see your point and here is an equally contrived but more thorough example where you can really see it:

```go
type Message struct {
    Header, Body, Footer *string
}

var GlobalConfig struct { Level *int }

func Serve(method string, data []byte) {
    area.Run(func() {
        switch method {
            case "message":
                ProcessMessage(data)
        }
    })
}

func ProcessMessage(data []byte) {
    if GlobalConfig.Level == nil {
        viper.LoadConfig("config", &GlobalConfig) // loads config.json
    }
    var m Message
    json.Unmarshal(data, &m)
    logPrintf("Level %d message: %s, %s, %s", GlobalConfig.Level, m.Header, m.Body, m.Footer)
}
```

In this example, the 2nd ProcessMessage call will blow up because the `Level` property now points to data freed by the Arena after the 1st call. There's no way to tell the Viper package you want *that* unmarshalling to eschew the Arena. I believe this is what you're talking about in terms of lazy-loading config.

I could make the argument that the `arena.Run()` call should be made in the method rather than in the server, which would solve that problem, but I see how this is spooky action at a distance. Generally, you can't know at face value which packages would transparently use Arena allocations, which will lead to subtle bugs.  Imagine the above example of using Viper, which scans for `config.json`, `config.yaml`, `config.xml` and so on, and only the JSON package has Arena support. The RPC server would work fine with YAML/XML configs and blow up with a JSON config. Hooray.

I suppose you could do some fancy work to ensure that no Arena-allocated pointer exits `arena.Run()` including being set into a variable that lives higher up the stack than that call, or on the heap, but that's probably impossible to do at compile time and doesn't solve this problem.

So yeah, back to passing around Arenas. I guess the fundamental point is if you want to manually free a batch of references, you need a way to refer to the batch and a way to specify which allocations go into that batch instead of normal GC space. If you also want concurrency and traversing package boundaries...well, you need an object and you need to thread it around throughout your code. There's not really a way for the runtime to make that more magical.

For the record, it's not clear to me how a hierarchical allocator is materially different, but I'm curious to know.

## Comment 1072769909

other (NONE) · creker · 2022-03-18T20:21:17Z · https://github.com/golang/go/issues/51317#issuecomment-1072769909

@bcmills your article is questionable at best but that besides the point. As already mentioned, data races and other invalid programs is not what I or other people are talking about here. We're talking about correct programs that do everything by the book (no data races, that's silly), don't use CGO, unsafe or other things that might do "spooky action at a distance". If I hold a reference and I know it's valid it will stay valid no matter how long a program runs or what it does. It might become invalid only when my code modifies that reference. That is, there's a direct connection between a piece of code and the effect it produces. That means, for example, those aliasing examples do not violate that property. That's basic memory safety that GC achieves by tracking references and never releasing something that's still in use. Arenas violate that property. `Free` will deallocate memory regardless of anything else and cause panics. I didn't do anything to my reference, why suddenly it should produce panics? If that's not a violation of basic principles of memory safe languages then I don't know anymore. Maybe we're talking about two completely different languages.

What would not violate that property is getting rid of `Free` and allowing GC to automatically determine when arena is safe to deallocate. 

## Comment 1072779174

other (CONTRIBUTOR) · Merovius · 2022-03-18T20:37:10Z · https://github.com/golang/go/issues/51317#issuecomment-1072779174

@creker

> As already mentioned, data races and other invalid programs is not what I or other people are talking about here.

"Bugfree programs don't have bugs" is a tautology. So much so, that a bugfree program will never experience a panic due to a use-after-free with arenas. That's because if someone hands you a pointer with a documented lifetime and you retain it beyond that, your program is illegal.

So, as a corollary, for there to be something to talk about, we must *not* be talking about bugfree programs. We are talking about how likely it is for arenas to make it easier or harder to write bugfree programs and how bad the consequences are in the presence of such bugs.

The people you are arguing with are taking the position that the mistakes being made are exactly the same in both cases, therefore arenas don't increase the likelihood of mistakes being made. But that the consequences are, if anything, milder for arenas.

However, whenever someone tries to tell you that, you declare that we should assume one class of bugs impossible, purely because it's called a race, whether or not the actual *code* causing that bug changed at all from one case to the other. That's very frustrating, TBQH.

## Comment 1072782687

other (CONTRIBUTOR) · josharian · 2022-03-18T20:43:15Z · https://github.com/golang/go/issues/51317#issuecomment-1072782687

> programmers will need to think about a new class of lifetime properties

sync.Pool already brought us into this world. Arenas are marginally better than sync.Pool on this front. If you mess up sync.Pool lifetimes, you get data corruption. If you mess up arena lifetimes, you get a panic. (Although I'm still -1/-0 on the proposal.)


## Comment 1072783224

other (CONTRIBUTOR) · josharian · 2022-03-18T20:44:11Z · https://github.com/golang/go/issues/51317#issuecomment-1072783224

@danscales is the prototype available anywhere? I'd kind of like to see what it's like to integrate into a program: The impact on the structure of the program, the performance benefits, how many bugs I introduce.

## Comment 1072786677

other (CONTRIBUTOR) · ianlancetaylor · 2022-03-18T20:50:29Z · https://github.com/golang/go/issues/51317#issuecomment-1072786677

@josharian https://go.dev/cl/387975

## Comment 1072815033

other (CONTRIBUTOR) · bcmills · 2022-03-18T21:22:10Z · https://github.com/golang/go/issues/51317#issuecomment-1072815033

> The people you are arguing with are taking the position that the mistakes being made are exactly the same in both cases, therefore arenas don't increase the likelihood of mistakes being made.

To be clear, I'm taking the position that the _only_ class of new mistakes is due to `string` values, which today are always safe to retain in the absence of `unsafe` (but may bloat a program's memory footprint).

However, even that impact could be easily eliminated by dropping `NewString` and `HeapString` from the proposal. (Then the classes of mistakes really would be exactly the same with or without arenas!)

## Comment 1072836269

maintainer (MEMBER) · thepudds · 2022-03-18T21:39:51Z · https://github.com/golang/go/issues/51317#issuecomment-1072836269

For anyone less familiar with how to try a CL -- it is fairly easy to try out the prototype, and I encourage people to do so if they are curious about this proposal:

```
 $ go install golang.org/dl/gotip@latest
 $ gotip download 387975
```
-----
Regarding the performance comment from @josharian, FWIW, I took the prototype for a spin and looked at some performance with a write-up of the results in a separate issue https://github.com/golang/go/issues/51667.

Related to that, the proposal has:

> In particular, because of the 64 MB chunk size, the above implementation may not be useful for applications that need to create a large number of arenas that are live at the same time (possibly because of many concurrent threads). It is probably most appropriate that there should only be a few to 10's of arenas in use at any one time.

My guess (which might be wrong! ;-) based on what I saw in #51667 is that if arenas are adopted and there is a full implementation, it might be plausible to use 100s or perhaps even 1000s of them concurrently rather than "few to 10s", though of course it would likely depend on how much RAM you have, how much benefit you are getting, and especially at the upper end it might come down to CPU vs. RAM tradeoffs.

If it ends up being 100s or 1000s concurrently, that would of course have some implications for how widely they are used, how viral they are in terms of APIs, and so on.

One API implication of wanting to use more arenas concurrently is that there might be some benefit to allowing a user to control or hint the batching size or chunk size. That said, that might not be worthwhile if the chunk size and/or batch size is "small enough" or perhaps auto-tuned. Also, the API could possibly allow getting a snapshot of how many allocations have been done by an arena instance. That could be helpful for things like testing and monitoring, and could allow a user to more conveniently decide to re-use an arena instance or not, although a user could in theory track themselves. All of that might not be worth doing if the benefit is small compared to cost of increasing the API size, but wanted to mention these while the API is being evaluated.

## Comment 1072849542

maintainer (MEMBER) · thepudds · 2022-03-18T22:05:53Z · https://github.com/golang/go/issues/51317#issuecomment-1072849542

One other quick comment about the prototype CL -- I believe it is Linux only at this point. (At least, the tests say so, and it crashed for me on a non-Linux platform but worked well on Linux, so personally I am not about to argue with the tests 😅 ).

## Comment 1072863951

maintainer (MEMBER) · rasky · 2022-03-18T22:26:07Z · https://github.com/golang/go/issues/51317#issuecomment-1072863951

@Merovius 

> But in that code, B has to know about the arena. So it can decide whether or not X should be allocated in an arena or not.

This is exactly what is wrong in this proposal. The fact that B has to know about the arena means that all Go code will have to know about the arena, and will have to provide an arena-allocated version of everything (`json.Unmarshal` vs `json.UmarshalArena`). Then, continuing on the same example packages, what if I want to load a viper configuration in an arena so that I can quickly dispose it later? Should I call a new function `viper.LoadConfigArena()`?

Languages that allow to use custom allocators like slabs provide a different allocation function, but the memory allocated by them can then be used with existing code without that code to ever know that the custom allocator was used. This proposal fails to make existing code work with the custom allocator, and propose we duplicate the Go API of all existing packages to provide an Arena-enabled version. 

@tooolbox 
> I suppose you could do some fancy work to ensure that no Arena-allocated pointer exits arena.Run() including being set into a variable that lives higher up the stack than that call, or on the heap, but that's probably impossible to do at compile time and doesn't solve this problem.

I suggest we focus on the best possible solution for the language and the ecosystem, and if it requires lots of work on the compiler, so be it. The best possible solution for inlining is not to have any language keyword, and we are still waiting for the compiler to provide good inlining support. If the best possible solution for providing an arena allocation requires a much more powerful escape analysis, I guess we could wait for it to happen.

## Comment 1072871250

other (NONE) · beoran · 2022-03-18T22:46:04Z · https://github.com/golang/go/issues/51317#issuecomment-1072871250

@josharian That is exactly one if the problems with this proposal. I do not want a second sync.Pool, nor anything that has similar problems. 

@Merovius Yes there are already similar ways in which Go can be memory unsafe when making mistakes. Similar does not mean equal. Adding yet another way in which Go can be memory unsafe increases the risk for the Go programmer to make mistakes. Seeing how arenas might end up being in many places much like context.Context, this means the risk is significantly increased compared to the current situation. Therefore,  this risk must be mitigated somehow.

@rasky I agree. Since this proposal already is embedded in the run time, it could leverage the garbage collector to avoid dangling pointers to objects inside the arena. For  example,if Go had a moving Gc, then the Free function could be more of a free request, after which the Gc looks for those dangling pointers and copies the pointed to objects over from the arena to the GC heap before actually freeing the slab. 

## Comment 1072874846

other (NONE) · CannibalVox · 2022-03-18T22:56:39Z · https://github.com/golang/go/issues/51317#issuecomment-1072874846

> @rasky I agree. Since this proposal already is embedded in the run time, it could leverage the garbage collector to avoid dangling pointers to objects inside the arena. For example,if Go had a moving Gc, then the Free function could be more of a free request, after which the Gc looks for those dangling pointers and copies the pointed to objects over from the arena to the GC heap before actually freeing the slab.

As has been mentioned upthread, waiting for the GC eliminates most or all of the savings of this proposal. That doesn't mean that this is an impossible solution, but it does mean that it needs to be able to happen on demand, not when the GC is ready for it.

e: FWIW this would allow strings to remain arena-allocated, so it does have my vote

double e: I'm curious what we would do about "minor" references, such as a heap-allocated interface header that is ready to be GC'd but still points to the arena space

## Comment 1072884148

other (CONTRIBUTOR) · Merovius · 2022-03-18T23:23:15Z · https://github.com/golang/go/issues/51317#issuecomment-1072884148

@rasky

> Then, continuing on the same example packages, what if I want to load a viper configuration in an arena so that I can quickly dispose it later? Should I call a new function `viper.LoadConfigArena()`?

ISTM that this is a decision the viper-authors need have to make. That is, if the community doesn't want arenas to spread, there is a simple way to not have them spread - don't expose APIs for them.

Personally, I find the idea of a configuration parser using arenas sufficiently outlandish to not be worried.

> Languages that allow to use custom allocators like slabs provide a different allocation function, but the memory allocated by them can then be used with existing code without that code to ever know that the custom allocator was used.

Arena-allocated memory can be used without knowing about arenas with this proposal just as well¹. It is just that if code wants to allocate into an arena itself, it needs to know about it.

From what I know, the most common approach to custom allocators seems to be to add an optional type-parameter for the allocator to use, FWIW. That seems largely identical to this proposal in both the virality of API and practical usage.

@beoran 

> Yes there are already similar ways in which Go can be memory unsafe when making mistakes. Similar does not mean equal. 

The argument is that *the bug causing the misbehavior is exactly the same*. The class of bug this triggers is different. But if you retain a pointer past its lifetime, that's exactly the same programming mistake - whether that pointer was allocated on the heap (triggering a race condition) or allocated in an arena (triggering a panic). That is, the bug is not "a racing write" or "a panic". The bug is "retaining a pointer after its lifetime".

The argument is that thus, the likelihood of making that mistake is exactly the same.

---

[1] As long as we don't incorporate the [IMO impractical](https://github.com/golang/go/issues/51317#issuecomment-1071146988) idea of a custom pointer type.

## Comment 1072905681

other (NONE) · beoran · 2022-03-19T00:43:43Z · https://github.com/golang/go/issues/51317#issuecomment-1072905681

@CannibalVox yes, a Free should instruct the  GC to check and fix up and if pisdible free  the area as soon as possible. If we had a runtime.Free function, this could be used similarly even for GC memory...

@Merovius Even if the kind of bug to be careful of is the same, areas as per this proposal increase thr likeliness of making this bug because the list of things to keep in mind becomes longer. It was the same whrn sync.Pool was introduced. In Go 1.1 the list was: be careful with unsafe.Pointer and race conditions. When pools were introdiced it took a while before we realized but they are now on the list as well. I would rather not add yet anotger item to that list. 

## Comment 1072907079

other (CONTRIBUTOR) · kylelemons · 2022-03-19T00:52:16Z · https://github.com/golang/go/issues/51317#issuecomment-1072907079

As I've been following along with this proposal, it seems like the largest beneficiaries would be wire protocol libraries / encoding schemes.  Apologies if I'm missing another large, motivating use-case here.  I have been thinking about ways to kick the can down the road a bit by finding a way to fill the gap between these wire protocols' optionality and the Go type system--the gap that is currently filled by using e.g. `*int` to mean "an optional `int`".

The question I have is this: if we had a new common way to specify an "optional" field that didn't _also_ carry with it the burden of a pointer to a separately-allocated value (along with language / builtin / stdlib constructs to make it about as heavy as today's `nil` checks / allocation calls in associated code), how much would that buy us?  Maybe we wouldn't get the 15% improvement, since the objects themselves (rather than the objects _and_ their fields) are still subject to normal GC, but it might be interesting if it could get something like 10% back.

@danscales Do you have any insight into how much of the reduction in GC overhead of protobuf decoding is a result of optional primitive types (strings, integers, etc) vs the sheer number of message values?  Or, put another way, does proto2 (whose generated code has many more pointers to primitives) benefit substantially more than proto3?  If so, something like this would potentially allow proto2 to allocate closer to once per message than once per field.

## Comment 1072910789

other (NONE) · beoran · 2022-03-19T01:14:36Z · https://github.com/golang/go/issues/51317#issuecomment-1072910789

@kylelemons Manual memory management is useful for other use cases as well. For example, in a game or game engine like ebiten, it  would be convenient to be able to have a memory area for storing image or sound data which can be passed to the OS or to C libraries as is, and which could be  immediately freed after a quick GC safety scan when not needed anymore. After reading the prototype PR, am not sure if the proposed arenas can really be used for that, though. 

Your remark on optional types is very interesting. Now in Go we have to use either a pointer, or like sql does, a struct with a bool and the actual value. But a pointer creates more work for the gc  while a struct with a bool wastes space. If he had a built in way, perhaps a built in generic optional[T], then the GC could be taught to not scan these optional values in the most common cases and improve performance like that. 




## Comment 1072916109

other (CONTRIBUTOR) · zephyrtronium · 2022-03-19T01:51:41Z · https://github.com/golang/go/issues/51317#issuecomment-1072916109

At this point, I am convinced that @Merovius's argument is correct, specifically in the sense that arenas do not introduce any error conditions that sync.Pool does not. I disagree that they are memory safe in the same sense as properly typed Go, but I think the difference isn't important.

There has been a lot of speculation about how different details about arenas would affect or "pollute" APIs. By now, I think it's worthwhile to try it and see. In particular, I'm curious about the impacts of arenas as proposed on decoders and encoders for wire transmission, `New(args) *T` constructor functions, and situations like managing resources for games like @beoran mentions (which was also my first thought on seeing this proposal!). I'd also like to see the impact of making the nil Arena always allocate from the heap, so that instead of `NewWithArena` we might have `SetArena` methods – although I'm not sure whether that's better or worse. I think it isn't particularly viable particularly where pointers exist inside allocated objects, but I'm also curious about an `arena.Pointer[T]` type that does not expose the allocated address.

## Comment 1072921267

other (NONE) · beoran · 2022-03-19T02:22:28Z · https://github.com/golang/go/issues/51317#issuecomment-1072921267

@zephyrtronium I think i said it before, while it is true that arenas as proposed here are equally risky as sync.Pool is, that is not what we should  be aiming at. I think we can do significantly better than sync.Pool on the level of safety, use in games, selecting the size of the allocated area, etc.

But I actually agree that it would be good if we could try it out for at least one year in x/exp/arenas as to be not bound by the Go compatibility promise. 

## Comment 1076141617

other (CONTRIBUTOR) · cuishuang · 2022-03-23T09:26:28Z · https://github.com/golang/go/issues/51317#issuecomment-1076141617

It sounds strange to a GC language  also have a backdoor to manage memory manually. Worried about being abused. It is recommended to have a description or measure like the `unsafe` package

## Comment 1076157429

other (NONE) · beoran · 2022-03-23T09:42:13Z · https://github.com/golang/go/issues/51317#issuecomment-1076157429

@cuishuang. Go would not be the first language to do this. The D language is normally garbage collected but it has a whole panoply of features for manual memory management as well. https://news.digitalmars.com/d/2.0/memory.html

## Comment 1078795900

other (NONE) · fzhedu · 2022-03-25T08:55:44Z · https://github.com/golang/go/issues/51317#issuecomment-1078795900

```
func A() {
    a := arena.New()
    B(a)
    a.Free()
}
```
do you propose a smart point way to prevent from forgetting deleting arena, like the unique/share_ptr in C++?
```
func A() {
   smartPoint a := arena.New()
    B(a)
    /// a.Free()
}
```

## Comment 1078803524

other (CONTRIBUTOR) · Merovius · 2022-03-25T09:06:00Z · https://github.com/golang/go/issues/51317#issuecomment-1078803524

@fzhedu I think the recommendation will be

```go
func A() {
    a := arena.New()
    defer a.Free()
    B(a)
}
```

Go doesn't have a way to do something when a value falls out of scope, i.e. it doesn't have destructors. So, the best approximation of what you suggest are finalizers. The proposal text talks about those.

## Comment 1078831722

other (NONE) · fzhedu · 2022-03-25T09:39:41Z · https://github.com/golang/go/issues/51317#issuecomment-1078831722

@[Merovius](https://github.com/Merovius)
that would also be dangerous, some programmers, especially new guys often forget writing the `defer xxx`. Does Go have a similar way to destruct objects like `try-with-resources` of Java?


## Comment 1078843154

other (CONTRIBUTOR) · Merovius · 2022-03-25T09:53:43Z · https://github.com/golang/go/issues/51317#issuecomment-1078843154

@fzhedu Please consult the proposal text:

> The implementation calls `SetFinalizer(A, f)` on each arena A as it is allocated, where f calls A.Free. This ensures that an arena and the objects allocated from it will eventually be freed if there are no remaining references to the arena. The intent though is that every arena should be explicitly freed before its pointer is dropped.

And the section titled "Removing Arena Free", for making finalizers the primary mechanism.

> Does Go have a similar way to destruct objects like `try-with-resources` of Java?

The closest it has is writing something like

```go
func WithResource(f func(*Resource)) {
    r := acquireResource()
    defer r.Close() // Free, whatever
    f(r)
}
```

which is [the same as the thing we are talking about](https://github.com/golang/go/issues/51317#issuecomment-1078803524).

It would certainly be possible to make the API `func WithArena(func(*Arena))` in this manner, instead of `NewArena() *Arena`. There is a bit of discussion about this above as well.


## Comment 1083421630

other (CONTRIBUTOR) · rsc · 2022-03-30T17:30:14Z · https://github.com/golang/go/issues/51317#issuecomment-1083421630

This discussion seems not to be converging. I think the Go runtime team would like to be able to experiment with this code in the main tree to learn more. I suggest that we add the code behind GOEXPERIMENT=arena and then put this proposal on hold until we have more experience. Having it as a GOEXPERIMENT should make it easier for others to try too, but it will avoid any of the "API invasiveness" concerns of directly adopting the proposal.



## Comment 1083550529

other (CONTRIBUTOR) · zephyrtronium · 2022-03-30T19:39:56Z · https://github.com/golang/go/issues/51317#issuecomment-1083550529

A use case that isn't unmarshaling: I expect that arenas could substantially improve the performance of certain uses of math/big. For example, [this implementation of pi to arbitrary precision](https://github.com/ALTree/bigfloat/blob/38c8b72a99243062fe71a04c8c456fc7f9d35121/misc.go#L62) requires several temporary variables with predictable lifetimes. If I translate that code to use an arena as proposed, and assuming that `*big.Float` gets a new `SetArena(*arena.Arena) *big.Float` method, I get:

```go
func pi(arena *Arena, prec uint) *big.Float {
	var half, two, a, b, t, x, y, lim *big.Float
	arena.New(&half)
	arena.New(&two)
	arena.New(&a)
	arena.New(&b)
	arena.New(&t)
	arena.New(&x)
	arena.New(&y)
	arena.New(&lim)
	half.SetArena(arena).SetFloat64(0.5)
	two.SetArena(arena).SetFloat64(2).SetPrec(prec + 64)
	a.SetArena(arena).SetFloat64(1).SetPrec(prec + 64)
	b.SetArena(arena)
	b.Mul(b.Sqrt(b), half)
	t.SetArena(arena).SetFloat64(0.25).SetPrec(prec + 64)
	x.SetArena(arena).SetFloat64(1).SetPrec(prec + 64)
	y.SetArena(arena)
	lim.SetArena(arena).SetMantExp(x, -int(prec+1))
	for y.Sub(a, b).Cmp(lim) != -1 {
		y.Copy(a)
		a.Add(a, b).Mul(a, half)
		b.Sqrt(b.Mul(b, y))
		y.Sub(a, y)
		y.Mul(y, y).Mul(y, x)
		t.Sub(t, y)
		x.Mul(x, two)
	}
	a.Mul(a, a).Quo(a, t)
	return a.SetPrec(prec)
}

func Pi(prec uint) *big.Float {
	arena := arena.New()
	defer arena.Free()
	return new(big.Float).Copy(pi(arena, prec))
}
```

Using the arena accounts for about half of the code here. If the arena API were `Arena.New(...any)` instead of `Arena.New(any)`, half of the arena code would disappear. If `Arena.New` would check whether the arguments have a `SetArena(*arena.Arena)` method and automatically call it, then the other half could disappear. If the function taking the arena is exposed such that the arena argument could be nil, and a nil `Arena.New` does not implicitly allocate from the heap, then the sequence of calls to `New` must be doubled with `half = new(big.Float)` &c. in an `if arena == nil` branch.

If @ALTree wants to support using a single arena for pi and other calculations, then he must choose between exposing an arena argument on all functions, having arena and non-arena variants (possibly in separate packages to avoid API pollution), using an arena global, or making all operations methods of some wrapper type with its own `SetArena` (which also lends itself to non-arena package-level variants, reminiscent of flag's and math/rand's functions versus methods).

It is not straightforward to use the `Arena.Run(func())` variant that people have mentioned for this problem, because the way to have a `*big.Float` definitely copy a result to heap memory is non-obvious: one must manipulate the precision outside the Run function to ensure that Copy/Set doesn't allocate. All types which own memory would have to provide such mechanisms, so it seems like it wouldn't solve the API pollution problem. It would instead introduce APIs to support arenas but which don't mention arenas in their signatures.

## Comment 1083658895

other (NONE) · CannibalVox · 2022-03-30T21:49:48Z · https://github.com/golang/go/issues/51317#issuecomment-1083658895

@zephyrtronium This is a great use case, and definitely the sort of thing that makes me interested in the proposal. Although it would be replaceable with object pooling, I think. I think unmarshalling would be a really bad use case.

## Comment 1083873096

other (CONTRIBUTOR) · gopherbot · 2022-03-31T00:43:11Z · https://github.com/golang/go/issues/51317#issuecomment-1083873096

Change https://go.dev/cl/397034 mentions this issue: `arena: have nil arenas allocate from the heap`

## Comment 1083873121

other (CONTRIBUTOR) · gopherbot · 2022-03-31T00:43:12Z · https://github.com/golang/go/issues/51317#issuecomment-1083873121

Change https://go.dev/cl/397035 mentions this issue: `math/big: use arenas for Float`

## Comment 1083880270

other (CONTRIBUTOR) · zephyrtronium · 2022-03-31T00:48:14Z · https://github.com/golang/go/issues/51317#issuecomment-1083880270

CL 397035 is an experiment to test the API and performance changes associated with having operations on big.Float use arenas. A quick summary is that having nil arenas handle allocation from the heap appears to cause up to a 200% slowdown (although I don't have time to profile and verify that that is indeed the source of the problem), and actually trying to use an arena in a benchmark to compute pi as I demonstrated in my previous comment causes the benchmark to hang at 53 bits of precision on my machine. I don't know the cause of that issue.

## Comment 1086464826

other (CONTRIBUTOR) · zephyrtronium · 2022-04-02T01:34:51Z · https://github.com/golang/go/issues/51317#issuecomment-1086464826

I've had some time to try more changes with arena in math/big and find more findings and feedback.

- Even undoing the change to allow nil arenas to handle heap allocations, the geometric mean for execution time of the big.Float benchmarks with internal changes for arenas is +51%, with a peak of +166%. runtime.mallocgc appears substantially higher in profiles now, and I note that the benchmarks now perform dramatically more heap allocations, including going from 0 to 2 per op for BenchmarkFloat{Add,Sub}. I think this is because of the way I wrote some parts of code to use arenas, but it may be the case that the interface-based arena API is inhibiting escape analysis.
- I thought before that my arena-using benchmark would hang at 53 bits of precision, but it actually hangs on whatever is the second benchmark function to use arenas. This is to say, it hangs on the second iteration of the first such benchmark if I pass `-count=2`. I have been able to find nothing which would indicate the cause of this, and the only information that I have is that stack traces seem to suggest that the benchmark goroutine is spending its time in a system stack.
- I find that I do wish we had generic variants of Arena.New and Arena.Slice, for no reason other than to serve as documentation of exactly the right thing to provide to those functions.
- In cases like formatting big.Float to a decimal string where it is difficult to predict the size of the result, it is awkward to use an arena to allocate a slice for appending. It would be nice to have a dedicated arena method to replace `append`. An alternative would be an API to suggest a capacity to allocate when growing a slice, so that I could follow size classes. A worse alternative would be to naïvely double the length of the slice when it needs to grow.

## Comment 1086630131

maintainer (MEMBER) · thepudds · 2022-04-02T12:30:02Z · https://github.com/golang/go/issues/51317#issuecomment-1086630131

Hi @zephyrtronium.  FWIW, I also initially saw heavy `interface{}` related allocations from arenas, and for what I was testing, adding arenas initially made it ~4x slower.

The first thing I did was modify the arena implementation to add a generics API:

https://github.com/thepudds/go119/commit/3c3094dc8d5cc3ee00978c64ad7d69903a1e195e#diff-2018f445bcf0c48965fd7accc508a0fa2a8ce02b0ed0db7cf2d6928f42fd4795R46-R60

It reuses most of the existing machinery, but it avoided any `interface{}` related allocs for what I was testing. That change eliminated about 40% of the wall clock overhead of arenas. 

(Another reason I added the generics API was I was more interested in getting the feel of it given there's a decent chance that would become the primary API if adopted).

Arenas were still about ~2.5x slower than no arenas, so I poked at it a bit more and tweaked the runtime a bit to get some better performance (at least for my case), which ultimately ended up with arenas being ~2x faster than the original and also used ~40% less RAM. I put a longer writeup into #51667 with details (with some additional comments [above](https://github.com/golang/go/issues/51317#issuecomment-1072836269) on potential API implications). YMMV.

I could send a CL with the generics API, but it is also something anyone can patch in themselves. (Also, I think a lower-level implementation of the proposed generics API would likely squeeze out a bit more performance, including there were hints that a different generics API might be faster, but my simple first cut seemed to help enough that I moved on to other performance areas).

Finally, thanks for the detailed analysis & experiments -- very interesting!

## Comment 1090551915

other (CONTRIBUTOR) · rsc · 2022-04-06T17:44:53Z · https://github.com/golang/go/issues/51317#issuecomment-1090551915

I'm definitely concerned about the follow-on API effects, such as the proposal to add Arenas to math/big.

Given the positive responses to https://github.com/golang/go/issues/51317#issuecomment-1083421630, let's put this proposal on hold, land the code behind GOEXPERIMENT for now, and see how things look down the road.


## Comment 1098317293

other (CONTRIBUTOR) · rsc · 2022-04-13T17:40:56Z · https://github.com/golang/go/issues/51317#issuecomment-1098317293

Given the reactions to my last comment, let's put this on hold. Runtime team, it's OK to land this behind GOEXPERIMENT=arena if you like.


## Comment 1098333447

other (CONTRIBUTOR) · rsc · 2022-04-13T18:00:39Z · https://github.com/golang/go/issues/51317#issuecomment-1098333447


**[Placed on hold](https://golang.org/s/proposal-status#hold)**.
— rsc for the proposal review group


## Comment 1105945855

other (NONE) · fzhedu · 2022-04-22T02:40:31Z · https://github.com/golang/go/issues/51317#issuecomment-1105945855

we look forward to the arena useful to mitigate OOM in [TiDB](https://github.com/pingcap/tidb) in terms of the following three cases:
1. Unmarshaling json or grpc protobuf packets uses a lot of memory, and the memory useage cannot be estimated in advance. From some cases, unmarshaling uses more than 10GB memory, causing OOM. This case is worse when many goroutines unmarshal packets at the same time;

2. Heap size is often significantly larger than necessary for  some structures, like table stats, hash table in hash agg or join. we cannot exactly count the memory usage of these general structures, causing OOM;

4. The used memory cannot be released in time. we cannot exactly know the free memory at runtime, causing OOM.

## Comment 1106525566

other (NONE) · burdiyan · 2022-04-22T13:38:26Z · https://github.com/golang/go/issues/51317#issuecomment-1106525566

I'm very excited about this proposal. Strongly believe that having manual memory management "hooks" in Go could expand its usefulness for so many different areas where a more granular control of the memory is required.

People from [Dgraph](https://dgraph.io) wrote a [blog post about manual memory management using jemalloc](https://dgraph.io/blog/post/manual-memory-management-golang-jemalloc/?repost=1/). Their allocator approach sounds similar to the use case of this proposal.

[Zig](https://ziglang.org) also has an interesting approach of explicitly passing Allocator object to places where memory needs to be managed manually. Go code that needs to manage memory manually could similarly take Allocator as an argument, which clearly conveys the idea of manual memory management, in a similar way that a function taking a Context conveys that it could block and get canceled.



## Comment 1113353387

other (NONE) · traetox · 2022-04-29T14:05:29Z · https://github.com/golang/go/issues/51317#issuecomment-1113353387

I admittedly haven't dug too deep into the Golang slab allocator, but could it be possible to hand in a custom slab allocator to the `arena.New()` function and still get GC sweeps on the allocations?  That would allow some very interesting use cases with file backed allocations and custom "swap."  It would also allow for users to manually define arenas that can be offloaded to disk in very high resource contention.

It is an admitted rabbit hole in terms of additional fault potential, but if the internal slab allocator for the arena is accessible there are some very cool custom application potentials.

## Comment 1126677422

other (NONE) · hauntedness · 2022-05-14T09:15:17Z · https://github.com/golang/go/issues/51317#issuecomment-1126677422

I would suggest to have a Reset() or Clone() to deal with some infinite loops.
```go
arena := arena.New()
for {
    doSomething(arena)
    arena.Reset()
}
```


## Comment 1179552770

other (CONTRIBUTOR) · soypat · 2022-07-09T14:21:31Z · https://github.com/golang/go/issues/51317#issuecomment-1179552770

Way late to this discussion, but I'd like to chip in two cents on package design. 
**Disclaimer**: I have never managed memory manually in a program. My experience is with Matlab and Python. All I know on memory management and hardware efficency comes from watching CppCon talks on youtube. 

That said, I'd like to mention two talks from CppCon 2014 that covered memory management for real-time/safety-critical applications:
* "Data-Oriented Design and C++" Mike Acton ([10:46](https://youtu.be/rX0ItVEVjHc?t=645))
* "C++ on Mars" Mark Maimone ([40:20](https://youtu.be/3SdSKZFoUa8?t=2421))

From listening to these talks it seems common to need different type of allocators from one case to the next depending on the data one is dealing with. Given this, does it not make sense to have a top level `alloc` package that contains this functionality? i.e.
* `alloc.HeapString` as detailed by this proposal
* `alloc.HeapNew` if decided is needed (from [this comment](https://github.com/golang/go/issues/51317#issuecomment-1063420318))
* `alloc.Allocator` interface, if it is decided is needed (from this [comment](https://github.com/golang/go/issues/51317#issuecomment-1106525566))
* `arena` package contained inside `alloc`, as well as any other future custom/manual allocator.

## Comment 1179625835

other (NONE) · beoran · 2022-07-10T00:16:27Z · https://github.com/golang/go/issues/51317#issuecomment-1179625835

@soypat Something like that does seem like a better design, yes.

## Comment 1185784018

other (NONE) · hherman1 · 2022-07-15T18:12:29Z · https://github.com/golang/go/issues/51317#issuecomment-1185784018

Instead of arenas being a discrete feature that allows users to manage memory, and leads to downstream surprises when an object is deallocated, could arenas be a GC hint?

e.g

```
arena.Call(myFunction)
```

Maybe this could tell the GC that we expect all memory in this function call to be deallocated together when the function exits, and so the runtime could allocate it in such a fashion that it would be easier to mark/sweep it all at once?

This might be dumb, I don't know too much about how these things work.

If this isn't dumb the advantages are potentially:

1. more efficient GC use for HTTP requests, though not as efficient as an actual arena
2. No surprises. The GC still does its thing before freeing objects

## Comment 1185806045

other (NONE) · beoran · 2022-07-15T18:35:19Z · https://github.com/golang/go/issues/51317#issuecomment-1185806045

@hherman1 This could actually be a good idea. In stead of arena, it would likely become something like runtime.FreeMemory() and when called this will cause all memory allocated thus far but not in use anymore to be freed, as a limited form of runtime.GC(). Normally runtime.FreeMemory could be used in conjunction with defer.

## Comment 1189328785

other (NONE) · kris-watts-gravwell · 2022-07-19T16:52:07Z · https://github.com/golang/go/issues/51317#issuecomment-1189328785

Distilling an arena down to GC hints on a memory group would simplify the design but also remove some useful things like the ability to have custom memory regions (mmap, GPU shared memory, etc...).

I also get that providing the ability to yank the rug out from under the GC manual RE memory arenas is also basically a bucket of grenades for bugs.

If it was possible to get new, free, gc_sweep, etc.. over a manually managed arena it would allow for some very cool functionality.

I also acknowledge that this might not be something that should be in the stdlib.  A library that is just a golang implementation of dlmalloc might be the right choice 99.99% of the time for those that want it..

## Comment 1221336700

maintainer (MEMBER) · mvdan · 2022-08-20T15:40:51Z · https://github.com/golang/go/issues/51317#issuecomment-1221336700

The sudden surge of comments adds very little to this discussion and does not follow https://go.dev/conduct. It is fine to disagree with the proposal, but only by being respectful and giving technical reasons for it. I am going to hide the comments and lock the thread for a few days to prevent further comments; I imagine this thread got shared in some external community with negative context.

## Comment 1279582594

other (CONTRIBUTOR) · rsc · 2022-10-14T23:17:34Z · https://github.com/golang/go/issues/51317#issuecomment-1279582594

For the record if we ever do take arenas off hold: in #56234, @dsnet suggests renaming reflect.ArenaNew to reflect.NewFrom. Closed that issue as a duplicate of this one.


## Comment 1279603480

other (CONTRIBUTOR) · mknyszek · 2022-10-15T00:06:10Z · https://github.com/golang/go/issues/51317#issuecomment-1279603480

@dsnet also suggested the following API for allocating maps with arenas:

```
// MakeMap creates a new map[K]V with the provided capacity.
// The map[K]V must not be used after the arena is freed.
// Accessing the underlying storage of the map after free may result in a fault,
// but this fault is also not guaranteed.
func MakeMap[K comparable, V any](a *Arena, cap int) map[K]V { ... }
```

The basic idea is the created map uses the arena as its underlying allocator.

## Comment 1279675552

other (CONTRIBUTOR) · gopherbot · 2022-10-15T06:34:55Z · https://github.com/golang/go/issues/51317#issuecomment-1279675552

Change https://go.dev/cl/423361 mentions this issue: `arena: add experimental arena package`

## Comment 1279675557

other (CONTRIBUTOR) · gopherbot · 2022-10-15T06:34:56Z · https://github.com/golang/go/issues/51317#issuecomment-1279675557

Change https://go.dev/cl/431955 mentions this issue: `misc/cgo/test: add asan and msan arena tests`

## Comment 1279675561

other (CONTRIBUTOR) · gopherbot · 2022-10-15T06:34:57Z · https://github.com/golang/go/issues/51317#issuecomment-1279675561

Change https://go.dev/cl/423359 mentions this issue: `runtime: add safe arena support to the runtime`

## Comment 1279675562

other (CONTRIBUTOR) · gopherbot · 2022-10-15T06:34:58Z · https://github.com/golang/go/issues/51317#issuecomment-1279675562

Change https://go.dev/cl/432078 mentions this issue: `runtime: make (*mheap).sysAlloc more general`

## Comment 1279675564

other (CONTRIBUTOR) · gopherbot · 2022-10-15T06:34:59Z · https://github.com/golang/go/issues/51317#issuecomment-1279675564

Change https://go.dev/cl/423365 mentions this issue: `runtime: factor out GC assist credit accounting`

## Comment 1279675567

other (CONTRIBUTOR) · gopherbot · 2022-10-15T06:35:00Z · https://github.com/golang/go/issues/51317#issuecomment-1279675567

Change https://go.dev/cl/423364 mentions this issue: `runtime: factor out mheap span initialization`

## Comment 1298439268

other (NONE) · phenpessoa · 2022-11-01T12:28:22Z · https://github.com/golang/go/issues/51317#issuecomment-1298439268

Is this package going to be testable by the public in Go 1.20 by using GOEXPERIMENT=arena?

## Comment 1298558428

other (CONTRIBUTOR) · mknyszek · 2022-11-01T14:03:13Z · https://github.com/golang/go/issues/51317#issuecomment-1298558428

@Pedro-Pessoa Yes. Sorry, I forgot to update this issue: the API and implementation landed behind GOEXPERIMENT. Note that the API and implementation that landed departs a little bit from the proposal but in ways I believe are  uncontroversial. Namely:
- The API uses generics (e.g. `arena.New[int](myArena)`).
- The chunk size is 8 MiB instead of 64 MiB (just seems to provide better performance in more cases).
- The MSAN and ASAN modes can be used to identify use-after-free errors that wouldn't cause a crash (memory corruption should still not be possible). Note that normally these modes do little for Go programs that are not cgo; arenas are the exception.

## Comment 1298753516

other (CONTRIBUTOR) · Merovius · 2022-11-01T15:58:31Z · https://github.com/golang/go/issues/51317#issuecomment-1298753516

> The API uses generics (e.g. `arena.New[int](myArena)`).

Just noting that this means you can't have an `Allocator` interface. So code-paths for arena/non-arena code must be pretty separate. I guess you could use the `reflect` API…

## Comment 1298772948

other (CONTRIBUTOR) · mknyszek · 2022-11-01T16:13:26Z · https://github.com/golang/go/issues/51317#issuecomment-1298772948

That's true, you can only do it by wrapping the reflect API. FWIW, I don't expect there to be any meaningful performance difference from using the reflect API in the current implementation.

## Comment 1300211695

other (NONE) · LeGamerDc · 2022-11-02T11:56:12Z · https://github.com/golang/go/issues/51317#issuecomment-1300211695

will arena support alloc reflect.Value and interface? we want to support alloc object in arena for protobuf/json/bson etc, which most memory footprint is reflect.Value and interface?

## Comment 1325225058

other (NONE) · ddkwork · 2022-11-23T15:09:07Z · https://github.com/golang/go/issues/51317#issuecomment-1325225058

any info for use package arena build Windows kernel driver？ set main as driverentry etc.

## Comment 1326248810

other (NONE) · dosgo · 2022-11-24T10:23:00Z · https://github.com/golang/go/issues/51317#issuecomment-1326248810

Why does the performance of using arena under windows seem to be worse?

## Comment 1326832161

other (CONTRIBUTOR) · mknyszek · 2022-11-24T21:02:14Z · https://github.com/golang/go/issues/51317#issuecomment-1326832161

> Why does the performance of using arena under windows seem to be worse?

Please file a new issue with details and how to reproduce the behavior.

## Comment 1326832890

other (CONTRIBUTOR) · mknyszek · 2022-11-24T21:03:43Z · https://github.com/golang/go/issues/51317#issuecomment-1326832890

> will arena support alloc reflect.Value and interface? we want to support alloc object in arena for protobuf/json/bson etc, which most memory footprint is reflect.Value and interface?

@LeGamerDc The arena API that landed in Go 1.20 (behind `GOEXPERIMENT=arenas`) allow you to do this via an interface in the `reflect` package.

## Comment 1326833542

other (CONTRIBUTOR) · mknyszek · 2022-11-24T21:04:58Z · https://github.com/golang/go/issues/51317#issuecomment-1326833542

> any info for use package arena build Windows kernel driver？ set main as driverentry etc.

I don't think Go has any specific support for running as a Windows kernel driver (though I may be misunderstanding what you mean). I'm not certain how arenas helps you with that.

## Comment 1328502278

other (NONE) · dosgo · 2022-11-28T03:56:04Z · https://github.com/golang/go/issues/51317#issuecomment-1328502278

> > Why does the performance of using arena under windows seem to be worse?
> 
> Please file a new issue with details and how to reproduce the behavior.

@mknyszek  I'm not sure if arena is suitable for the scene of binary tree calculation.

## Comment 1329244830

other (CONTRIBUTOR) · mknyszek · 2022-11-28T14:54:53Z · https://github.com/golang/go/issues/51317#issuecomment-1329244830

@dosgo It can in some circumstances. See #51667 for an example of how it's used in a binary tree benchmark (the optimizations in that issue will be included in the Go 1.20 release of arenas, behind `GOEXPERIMENT`).

## Comment 1341819198

other (NONE) · hherman1 · 2022-12-08T00:55:17Z · https://github.com/golang/go/issues/51317#issuecomment-1341819198

It appears Java 20 is adding support for arenas. Might be interesting to contrast this proposal with their design: http://minborgsjavapot.blogspot.com/2022/12/java-20-sneak-peek-on-panama-ffm-api.html 

## Comment 1354600057

other (CONTRIBUTOR) · DmitriyMV · 2022-12-16T11:34:16Z · https://github.com/golang/go/issues/51317#issuecomment-1354600057

Just a note - can arena be adjusted to work with CGo where [pinner](https://github.com/golang/go/issues/46787) would be required? That is - is it safe and valid to pass a pointer to arena allocated memory which only contains non-pointers or pointers to the memory in that same arena?

## Comment 1358290434

other (CONTRIBUTOR) · mknyszek · 2022-12-19T20:37:12Z · https://github.com/golang/go/issues/51317#issuecomment-1358290434

That's a great question; I don't think precise cgo interactions have been considered yet.

Enforcing that guarantee is difficult to do efficiently. We could have one of the `cgocheck` modes enforce it I suppose.

## Comment 1367681317

other (NONE) · bvk · 2022-12-30T01:57:55Z · https://github.com/golang/go/issues/51317#issuecomment-1367681317

Is there a mechanism to create sub-arenas from a larger arena?

## Comment 1369859846

other (CONTRIBUTOR) · mknyszek · 2023-01-03T14:54:47Z · https://github.com/golang/go/issues/51317#issuecomment-1369859846

I'm not sure what you mean by "sub-arena," but I think the answer is no. What are the semantics of what you're asking about and what's the use-case?

## Comment 1370537217

other (NONE) · bvk · 2023-01-04T06:36:21Z · https://github.com/golang/go/issues/51317#issuecomment-1370537217

@mknyszek By sub-arena, I meant a nested, child arena whose scope is limited by the parent arena. Sub-arena gets free-ed when the parent-arena gets freed automatically, however, users can free a sub-arena to reclaim storage without invalidating the parent-arena.

I typically unmarshal multiple json blobs into Go objects as part of handling a single request. Should I create a single arena and share it in all multiple json-unmarshal operations (along with other non-marshaling ops) or should I create a new arena for  unmarshal operations?

Once a json blob is unmarshaled into a Go object, the memory used for unmarshaling is a waste. I wish there is a way to quickly reclaim the short-lived memory used for unmarshaling instead of waiting for GC. I assume we would want to create one arena per request and use a short-lived sub-arena which is freed immediately after the unmarshaling operation, thus consuming as less address space as possible.

I don't see the need for multiple sub-arenas, so at max one child sub-arena seems to be good enough for my use-case.

## Comment 1374838604

other (NONE) · assemblaj · 2023-01-08T13:39:17Z · https://github.com/golang/go/issues/51317#issuecomment-1374838604

Hello, I'm from the [IKEMEN-Go](https://github.com/ikemen-engine/Ikemen-GO) development team, a next generation engine written in Go that utilizes [M.U.G.E.N](https://en.wikipedia.org/wiki/Mugen_(game_engine)) resources. I'm in the process of implementing [rollback netcode](https://en.wikipedia.org/wiki/GGPO) and have a [rollback library](https://github.com/assemblaj/ggpo) written, but I've had some issues optimizing the [snapshotting](https://i.ibb.co/HrdmF9m/pprofbad.png) due to the immense amount of heap allocations necessary.  I've tried utilizing pools and my own slab allocator with varying degrees of success, but I'm really glad this is being added to the language as it can do thing with regards to the runtime that I cannot do on my own.  I think our project would be the perfect demonstration for the use of Go Arenas and I look forward to updating you all with questions and results. 

## Comment 1376865248

other (NONE) · assemblaj · 2023-01-10T08:00:43Z · https://github.com/golang/go/issues/51317#issuecomment-1376865248

How can I track allocations made using the arena in pprof? The `alloc_objects` section shows no objects allocated with the arena at all.  [Here ](https://pbs.twimg.com/media/FmDMKTBWYBUyk8j?format=png&name=900x900)is what I'm used to and [here ](https://pbs.twimg.com/media/FmEBCl1XoAIDAG6?format=png&name=900x900)is what I'm seeing when using the Arena's for a few critical objects (`CommandList`, `Command`).  Is this normal for prerelease features? 

## Comment 1382734869

other (NONE) · assemblaj · 2023-01-14T13:11:22Z · https://github.com/golang/go/issues/51317#issuecomment-1382734869

Loving the arenas so far, have helped a lot with performance, will do a write up when all is said and done.  Is support for maps a possibility? 

Also, I've noticed that Arenas seem to use way more memory on slower machines, (see [here ](https://twitter.com/intandemwith/status/1613580583942197273)vs [here](https://twitter.com/intandemwith/status/1613600082837884929)), why might that be? 

## Comment 1382821965

other (NONE) · hherman1 · 2023-01-14T15:24:43Z · https://github.com/golang/go/issues/51317#issuecomment-1382821965

@assemblaj github won’t let me react to comments for some reason but wanted to say I’m excited to see your write up/results!

## Comment 1382965670

other (NONE) · CannibalVox · 2023-01-14T23:44:43Z · https://github.com/golang/go/issues/51317#issuecomment-1382965670

> Also, I've noticed that Arenas seem to use way more memory on slower machines, (see [here ](https://twitter.com/intandemwith/status/1613580583942197273)vs [here](https://twitter.com/intandemwith/status/1613600082837884929)), why might that be?

Just a guess, but bear in mind that arenas are not freed immediately when Free is called- they are freed when the runtime gets around to them. So it's a possibility that on slower systems there are more arenas waiting to be cleaned up on than on faster ones. 

## Comment 1385476920

other (CONTRIBUTOR) · mknyszek · 2023-01-17T14:05:16Z · https://github.com/golang/go/issues/51317#issuecomment-1385476920

> Just a guess, but bear in mind that arenas are not freed immediately when Free is called- they are freed when the runtime gets around to them. So it's a possibility that on slower systems there are more arenas waiting to be cleaned up on than on faster ones.

That's not quite true in the current implementation. In most cases the physical memory for an arena is indeed freed immediately, just the address space is not. There is one exception, which is if the arena is freed while the GC is in the mark phase (in most applications, this represents a relatively small fraction of wall time in each GC cycle; there are of course exceptions). In that case, freeing the arena is delayed until the next sweep phase.

RE: using more memory on slower machines, I think it really depends on what part of the system is "slower." For example, a "slower" machine could still have more arenas queued up if the parts of system performance the mark phase relies upon are disproportionately slower than other parts of the system, resulting in a longer mark phase overall and delaying arena frees.

This seems like a relatively easy question to answer with an ad-hoc trace of the state of every arena chunk, and which list its sitting on. I don't plan to look into this any time soon, but `println` instrumentation in the runtime that's parsed after the fact should be sufficient. (If `println` is interfering with performance too much, there's `src/runtime/debuglog.go`.)

## Comment 1385525078

other (NONE) · assemblaj · 2023-01-17T14:38:05Z · https://github.com/golang/go/issues/51317#issuecomment-1385525078

Hey everyone, I appreciate all of the replies to my inquiries. Right now I'm working on finalizing a build for the IKEMEN Go rollback public alpha scheduled for Friday. Perhaps this will be the first use of Golang arenas on many consumer systems for a desktop application? Anyway, I'll have a lot to update when all is said and done. Talk to you soon! 

Edit: see message below

## Comment 1385566724

other (CONTRIBUTOR) · gopherbot · 2023-01-17T15:04:58Z · https://github.com/golang/go/issues/51317#issuecomment-1385566724

Change https://go.dev/cl/462355 mentions this issue: `doc/go1.20: remove mention of arena goexperiment`

## Comment 1385623024

other (CONTRIBUTOR) · mknyszek · 2023-01-17T15:42:51Z · https://github.com/golang/go/issues/51317#issuecomment-1385623024

@assemblaj and everyone else currently following this issue:

Arena support behind the `GOEXPERIMENT` has landed, but I want to be absolutely clear that `GOEXPERIMENT` means a true experiment. The API and implementation is completely unsupported and we make no guarantees about compatibility or whether it will even continue to exist in any future release. We do not recommend using it in production for this reason, though we appreciate any hands-on ideas and feedback, especially about the API. Apologies for not communicating this more clearly earlier.

I think it's clear to us that there are serious concerns with respect to the existing API: it's infectious. While the performance benefit in some cases can be great, it comes at a high cost to the ecosystem. These problems need to be resolved before we can even start to consider making it an supported API.

In sum, please take the current arenas API and implementation for what it is: an experiment.

## Comment 1385679701

other (NONE) · assemblaj · 2023-01-17T16:20:28Z · https://github.com/golang/go/issues/51317#issuecomment-1385679701

Gotcha. Thanks for the clarification. As per that statement, I won't be using arenas for my public alpha and as such won't be able to make a writeup on it.  I really wanted to be at the forefront of sharing this very powerful feature with the world but am still hopeful that this will become possible in the future. 

## Comment 1399194607

other (NONE) · CannibalVox · 2023-01-21T06:55:54Z · https://github.com/golang/go/issues/51317#issuecomment-1399194607

I've been working with some performance-intensive code recently, and it has occurred to me that the inability to signal to other engineers that a pointer in a particular method needs to not escape is a maintainability issue if you're trying to keep allocations at zero in a section of code, and I think arenas are also suffering from the same problem. 

I think it might be valuable if go had the concept of a "sealed reference", a type of reference that can only be used as locals, params, or return types, can't be converted into a bare pointer except maybe with something in unsafe package, and therefore has be copied by value for any use that would result in an escape (although returning a sealed reference would still result in an escape). This would also clear up the issues with arenas: arenas return sealed references, which would be entirely safe to use.

The main oddball case would be that arena'd data would potentially need to be castable to an interface, which would both provide a path to persisting the data, cause undesirable escapes, and put us right back where we started in terms of nobody knowing that this particular variable needs to not escape.

## Comment 1399238299

maintainer (MEMBER) · thepudds · 2023-01-21T12:03:25Z · https://github.com/golang/go/issues/51317#issuecomment-1399238299

> signal to other engineers [...] if you're trying to keep allocations at zero in a section of code,

I know this is not your main point , but FWIW, tests are one way to keep allocations at zero. Random example from stdlib:
https://github.com/golang/go/blob/go1.19.5/src/crypto/ed25519/ed25519_test.go#L196-L206

## Comment 1399322333

other (NONE) · CannibalVox · 2023-01-21T19:59:40Z · https://github.com/golang/go/issues/51317#issuecomment-1399322333

> I know this is not your main point , but FWIW, tests are one way to keep allocations at zero. Random example from stdlib: https://github.com/golang/go/blob/go1.19.5/src/crypto/ed25519/ed25519_test.go#L196-L206

That's still super valuable to know, thank you!

## Comment 1402273046

other (NONE) · LeGamerDc · 2023-01-24T16:56:40Z · https://github.com/golang/go/issues/51317#issuecomment-1402273046

> I've been working with some performance-intensive code recently, and it has occurred to me that the inability to signal to other engineers that a pointer in a particular method needs to not escape is a maintainability issue if you're trying to keep allocations at zero in a section of code, and I think arenas are also suffering from the same problem.
> 
> I think it might be valuable if go had the concept of a "sealed reference", a type of reference that can only be used as locals, params, or return types, can't be converted into a bare pointer except maybe with something in unsafe package, and therefore has be copied by value for any use that would result in an escape (although returning a sealed reference would still result in an escape). This would also clear up the issues with arenas: arenas return sealed references, which would be entirely safe to use.
> 
> The main oddball case would be that arena'd data would potentially need to be castable to an interface, which would both provide a path to persisting the data, cause undesirable escapes, and put us right back where we started in terms of nobody knowing that this particular variable needs to not escape.

you can do trick with uintptr, if you are so urge with the performance...

```
func main() {
	var p = &Cat{
		name: "mimi",
		age:  21,
	}
	pp := uintptr(unsafe.Pointer(p))
	//DoWithAnimal(p) // will make p escape
	DoWithAnimal((*Cat)(unsafe.Pointer(pp)))
	_ = p
}

//go:noinline
func DoWithAnimal(a Animal) {
	a.Walk()
}
```

## Comment 1405229351

other (NONE) · assemblaj · 2023-01-26T16:01:02Z · https://github.com/golang/go/issues/51317#issuecomment-1405229351

I decided to follow through with my [experiment](https://github.com/assemblaj/Ikemen-GO/releases/tag/0.0.0).  I am aware that arenas may not always be around, and I accept that risk, I have other options in the case that they are removed. So far things are going well.  There was something that needed to be moved off of arenas due to unpredictable lifetimes, but other than that I've had no issues. I've not heard complaints about performance (and this is an application with a very high data throughput with very tight performance requirements).  I will be writing an article about arenas, but more broadly the struggles of optimizing IKEMEN Rollback in Go very soon.  IKEMEM Go is a great project and I look forward to sharing our efforts with the broader Golang community. 

## Comment 1414292896

other (NONE) · petethepig · 2023-02-02T19:59:42Z · https://github.com/golang/go/issues/51317#issuecomment-1414292896

Hi everyone, we've experimented with arenas at Pyroscope and [I wrote a blog post about it](https://pyroscope.io/blog/go-1-20-memory-arenas/).

TL;DR:
* we were able to cut 8% of CPU utilization on an already highly optimized service. We think that there's much more potential for less optimized services. We see arenas as a powerful tool when it comes to reducing performance impact of allocations
* we found arenas to be easier to implement compared to `sync.Pool` optimizations or other optimizations we've done, like writing custom allocation-free protobuf parsers
* concerns regarding the implicitly of the lifecycle of pointers to objects allocated on arenas are fair, but we think that arenas use-case is very narrow and therefore this won't be a big issue. And so basically the pros outweigh the cons
* this can be further mitigated by discouraging the use of arenas, similar to how the use of `unsafe`, `reflect` or `cgo` is discouraged


## Comment 1414447298

other (NONE) · beoran · 2023-02-02T22:15:50Z · https://github.com/golang/go/issues/51317#issuecomment-1414447298

@petethepig Interesting. It seems that in practice the problems I for saw with arenas seem to be less of a concern than they seem in theory if not overused. Then, I will support adding them to Go.

## Comment 1416078511

other (NONE) · hherman1 · 2023-02-03T16:06:48Z · https://github.com/golang/go/issues/51317#issuecomment-1416078511

What if arenas lived in the unsafe package? That way it was obvious at every interaction that you were off roading. Specifically I mean “unsafe.NewArena” as opposed to “arena.NewArena”

## Comment 1416080625

other (NONE) · beoran · 2023-02-03T16:08:31Z · https://github.com/golang/go/issues/51317#issuecomment-1416080625

@hherman1 Or even better, in "unsafe/arena", if we are bikeshedding.

## Comment 1416087072

other (NONE) · hherman1 · 2023-02-03T16:13:59Z · https://github.com/golang/go/issues/51317#issuecomment-1416087072

@beoran “Unsafe/arena” only indicates the unsafety at import, not when you actually use the methods.

## Comment 1416181947

other (CONTRIBUTOR) · ianlancetaylor · 2023-02-03T17:30:11Z · https://github.com/golang/go/issues/51317#issuecomment-1416181947

@hherman1 Putting arenas in unsafe doesn't address a major concern: if arenas are adopted, people will want to start using them, and that will lead to a series of requests for adding arenas to existing APIs and for adding arenas when designing new APIs.  Arenas will tend to spread everywhere, making everything more complicated.  At least, that is the fear.

## Comment 1416209542

other (NONE) · DeedleFake · 2023-02-03T17:55:05Z · https://github.com/golang/go/issues/51317#issuecomment-1416209542

@ianlancetaylor That's been the fear with a number of things, but thus far it hasn't materialized too much, with the exception of `context.Context` which was explicitly _designed_ to spread everywhere. People don't pass `unsafe.Pointer`s all over the place or try to re-implement synchronization primitives manually with `sync/atomic`. I think a stern warning or two in a few comments and an obvious relation to the `unsafe` package would probably be enough.

The [potential performance improvements](https://gist.github.com/DeedleFake/b0f23672cc38dfe3b1e8b8e923b3ad6c) would be really nice to have.

## Comment 1416283503

other (NONE) · assemblaj · 2023-02-03T19:07:15Z · https://github.com/golang/go/issues/51317#issuecomment-1416283503

The potential runtime errors which crash the program without warning will be enough to prevent people from overly adopting arenas.  Arenas are more convenient than every alternative (given certain conditions are met), but they're not that easy.  I can say from experience that repurposing  algorithms that were built with garbage collection in mind to utilize  arenas isn't easy.  As a huge proponent of arenas I personally wouldn't be quick to trust that an external package would use them properly as I've seen how difficult some of these errors are to replicate, diagnose and debug. This is not a knock against arenas, just that I feel that there's already a fair amount of obstacles inherent to using them. There might be calls to rewrite or reimagine packages with arenas but I don't see that actually working out well unless they were a good fit for arenas in the first place. I expect there will be large amounts of enthusiasm for arenas initially but most Go programmers will be deterred by how careful you need to be with them.

I left a note in [this](https://supercombo.gg/2023/02/02/from-rollback-with-love-ikemen-go/)  article about arenas.  I also have an article of my own that I'm currently editing about arenas. I will try to focus on some of the hardships of using arenas so that people don't get the idea that they're "plug and play", because they aren't. 

## Comment 1416353469

other (CONTRIBUTOR) · ianlancetaylor · 2023-02-03T20:12:53Z · https://github.com/golang/go/issues/51317#issuecomment-1416353469

@DeedleFake I do think the issue here is a bit different.  Let's say we want to use an arena to handle per-request memory allocation for some HTTP server.  And let's say that the HTTP requests use JSON, as is common.  It's straightforward to use the arena to handle the program's memory allocation, but it turns out that most of the allocation for a specific request is actually unmarshalling the JSON.  So now we need to design a way to pass the arena into the encoding/json API, so that the JSON unmarshalling will allocate memory in the way that we want.  That doesn't seem at all unlikely to me.  And that's just one example of arenas spreading into unrelated APIs.

## Comment 1416736348

other (NONE) · burdiyan · 2023-02-04T12:11:47Z · https://github.com/golang/go/issues/51317#issuecomment-1416736348

Go has a lot of things that are meant for “grownups”, like closing file handles, HTTP response bodies, assumption that a library shouldn’t panic unless explicitly documented and justified, and many-many things like that. I believe that properly documenting concerns of using arenas should be enough for most “grownup” Go users. 

## Comment 1416868003

other (NONE) · hherman1 · 2023-02-04T22:48:45Z · https://github.com/golang/go/issues/51317#issuecomment-1416868003

@ianlancetaylor hm, I’m not sure what made me come off as though I don’t agree with you about that, but I do. My suggestion was more of an added caution. Some way to try and constrict their spread, and discourage adoption. 

## Comment 1416870503

other (NONE) · assemblaj · 2023-02-04T23:00:31Z · https://github.com/golang/go/issues/51317#issuecomment-1416870503

[Here's](https://medium.com/@assemblaj/arenas-for-ikemen-go-rollback-17a5ab2a9a64) a draft for my article on arenas. I feel like it's important to get feedback here before spreading it into the wild.  The basic gist of it is: 

- Arenas present a great reduction in code complexity compared to other options for my usecase 
- Arena's performance is similar to using custom preallocators without the large memory footprint or the requirement to know how much data is needed ahead of time 
- A tradeoff when using arenas is the potential of runtime errors 
- Memory usage on low end machines is unpredictable

Suggestions 
- Maps 
- Improve syntax (though this doesn't really matter) 

More code examples can be found [here](https://github.com/assemblaj/Ikemen-GO/blob/Rollback-Public-Alpha/src/state_clone.go) . 

I would like to see arenas become a part of the language. I feel like this could be revolutionary for Go game development. 

## Comment 1416876829

other (NONE) · hherman1 · 2023-02-04T23:36:53Z · https://github.com/golang/go/issues/51317#issuecomment-1416876829

Suppose the api were instead:

`unsafe.InArena(f func())`

All allocations in the current goroutine in f() would happen in an arena that is freed when f completes.

the downsides:

* what if f, indirectly, tries to save memory off to the side?
* How do you return a value from f e.g parsed json?
* Hooks into allocations in a function in a weird way. Maybe it’s hard to implement?


The upsides:

* 0% infectious api. There is no need to be arena aware anywhere in the callstack except the call site.
* Good enough for the main use case in this thread, deserializing protobufs.
* Easier to use than custom allocation methods.

I want to emphasize that this seems risky, but also still good enough, and the risk is entirely in the hands of the user of the method.

## Comment 1416878221

other (CONTRIBUTOR) · zephyrtronium · 2023-02-04T23:48:20Z · https://github.com/golang/go/issues/51317#issuecomment-1416878221

@hherman1 That kind of API was suggested before in https://github.com/golang/go/issues/51317#issuecomment-1056637872. Per https://github.com/golang/go/issues/51317#issuecomment-1083550529, it would make crossing the boundary between arena and non-arena code extremely subtle and still would lead to arena-focused APIs that simply don't indicate they're arena-focused.

## Comment 1416882918

other (NONE) · DeedleFake · 2023-02-05T00:16:26Z · https://github.com/golang/go/issues/51317#issuecomment-1416882918

From my understanding, the majority of performance gains of arenas comes from the way in which allocations are performed, not in that they essentially bypass the garbage collector, correct? How feasible would it be to remove, or maybe somehow restrict, manual freeing of arenas and instead prevent an arena from being collected until all references to all allocations from that arena are ready, not just the arena reference itself? That would drastically improve their safety, though it could lead to some potential memory leaks instead of use-after-free bugs.

In other words, something like

```go
var v1, v2 int
{
  a := arena.NewArena()
  v1 = arena.New[int](a)
  v2 = arena.New[int](a)
}
// a is no longer referenced, but won't be freed until v1 and v2 can both be.
// ...
```

## Comment 1416885076

other (NONE) · hherman1 · 2023-02-05T00:25:19Z · https://github.com/golang/go/issues/51317#issuecomment-1416885076

@zephyrtronium thanks, navigating this thread is getting difficult. You wrote

> the way to have a *big.Float definitely copy a result to heap memory is non-obvious: one must manipulate the precision outside the Run function to ensure that Copy/Set doesn't allocate.

I didn’t understand why you need to ensure the *big.Float escapes to heap? Is this as a result type? Would the api

`arena.Call[T](f func(out *T))`

Where out is guaranteed to escape the arena to heap resolve your concern?

## Comment 1416885756

other (CONTRIBUTOR) · zephyrtronium · 2023-02-05T00:28:07Z · https://github.com/golang/go/issues/51317#issuecomment-1416885756

@DeedleFake Free() is the very thing that can make arenas efficient. See the proposal text:
> The big problem with not having a Free operation is that arenas derive most of their performance benefit from more prompt reuse of memory. Though the allocation of objects in the arena would be slightly faster, memory usage would likely greatly increase, because these large arena objects could not be collected until the next garbage collection after they were no longer in use. This would be especially problematic, since the arenas are large chunks of memory that are often only partially full, hence increasing fragmentation. We did prototype this approach where arenas are not explicitly freed, and were not able to get a noticeable performance benefit for real applications. An explicit Free operation allows the memory of an arena to be reused almost immediately. In addition, if an application is able to use arenas for almost all of its allocations, then garbage collection may be mostly unneeded and therefore may be delayed for quite a long time.

## Comment 1416886363

other (NONE) · DeedleFake · 2023-02-05T00:31:57Z · https://github.com/golang/go/issues/51317#issuecomment-1416886363

@zephyrtronium Ah, O.K. Thanks for the clarification. That makes sense. I know allocation is more efficient with arenas so I was hoping that was the primary benefit but yeah, that makes sense. Since arenas require large amounts of memory, delayed collection would definitely be a potential issue.

## Comment 1416887771

other (CONTRIBUTOR) · zephyrtronium · 2023-02-05T00:41:14Z · https://github.com/golang/go/issues/51317#issuecomment-1416887771

@hherman1 
> I didn’t understand why you need to ensure the *big.Float escapes to heap? Is this as a result type?

The slice inside the *big.Float needs to be allocated from the arena for there to be any benefit. If I try to copy the result inside the Run/Call function, then the destination needs to allocate a new slice to hold that copy, and that slice would be in the arena, so it is invalid once the call returns. If I don't, then the result to copy from is invalid once the call returns, and I never have an opportunity to copy it.

In general, that kind of API requires that every type which internally *contains* allocated memory provide ways to predict the amount of memory required and to copy that internal memory out to another object. If either is impossible, then that type can never be used inside an arena call.

## Comment 1416893900

other (NONE) · CannibalVox · 2023-02-05T01:22:04Z · https://github.com/golang/go/issues/51317#issuecomment-1416893900

I agree with the concern/worry about rolling out arenas and would like to make the following concrete declarations:

* The largest source of allocation CPU for the largest portion of go customers comes from request & response allocation for some class of web services
* Arenas are the first thing that has been added to Go that can address this (which is why object pool has not had the same implications), and on the performance side, they seem to do it well
* Arenas, as implemented now, are poorly suited to address this because complex objects that were previously safe to use for all purposes now are not

Effectively, arenas represent an "attractive nuisance" because they are extremely valuable for a common "low-skill" use case but require intermediate-level knowledge (and, depending on how your organization uses request & response objects, may require bizarre tribal knowledge to know you can't do X with Y variable, miles away from where the arena is actually used).  Object Pools were not demanded for encoding/json because Object Pools could not be **used**, really, in encoding/json. Arenas can, and anyone who has a Go HTTP surface running at high scale could measure the value of doing so in the tens of thousands of dollars, and potentially a lot more.

My hope is that arenas aren't just put to work on whatever bespoke google use case drove the desire to implement them and set aside, because I think that this experiment has revealed (A) that go's tools for avoiding allocations are very thin on the ground for a language that chose to up-front garbage collector costs, and that (B) the reason for that is deep in the language and requires some attention. Taking an ambitious approach on delivering arenas could have major positive implications for go performance far beyond the narrow scope of arenas.

## Comment 1416910033

other (NONE) · hherman1 · 2023-02-05T03:06:34Z · https://github.com/golang/go/issues/51317#issuecomment-1416910033

@zephyrtronium 

>In general, that kind of API requires that every type which internally contains allocated memory provide ways to predict the amount of memory required and to copy that internal memory out to another object. If either is impossible, then that type can never be used inside an arena call.

This makes sense to me and does seem like a problem.

>The slice inside the *big.Float needs to be allocated from the arena for there to be any benefit. If I try to copy the result inside the Run/Call function, then the destination needs to allocate a new slice to hold that copy, and that slice would be in the arena, so it is invalid once the call returns. If I don't, then the result to copy from is invalid once the call returns, and I never have an opportunity to copy it.

This is what my alternate API was meant to address. If perhaps there was some way to flag the result, and everything used to compose the result, must not be allocated in the arena, and everything else should be. That way you can have the single thing, the deserialized protobuf or what have you, which is reusable once the arena closes, and all other temporary memory is released. 

## Comment 1416914347

other (CONTRIBUTOR) · randall77 · 2023-02-05T03:43:14Z · https://github.com/golang/go/issues/51317#issuecomment-1416914347

> This is what my alternate API was meant to address. If perhaps there was some way to flag the result, and everything used to compose the result, must not be allocated in the arena, and everything else should be. That way you can have the single thing, the deserialized protobuf or what have you, which is reusable once the arena closes, and all other temporary memory is released.

My understand of the proto decoder is that *all* of the allocations done during deserialization are things reachable from the return value. It only allocates things it needs to return; there are no temporary allocations.
That may differ for different deserializers, of course. But solving the problem only for the temporary allocations isn't going to solve the whole problem.

## Comment 1418888597

other (NONE) · LeGamerDc · 2023-02-06T10:56:02Z · https://github.com/golang/go/issues/51317#issuecomment-1418888597

> Suppose the api were instead:
> 
> `unsafe.InArena(f func())`
> 
> All allocations in the current goroutine in f() would happen in an arena that is freed when f completes.
> 
> the downsides:
> 
> * what if f, indirectly, tries to save memory off to the side?
> * How do you return a value from f e.g parsed json?
> * Hooks into allocations in a function in a weird way. Maybe it’s hard to implement?
> 
> The upsides:
> 
> * 0% infectious api. There is no need to be arena aware anywhere in the callstack except the call site.
> * Good enough for the main use case in this thread, deserializing protobufs.
> * Easier to use than custom allocation methods.
> 
> I want to emphasize that this seems risky, but also still good enough, and the risk is entirely in the hands of the user of the method.

if some object are very sure be allocate.use.free in one function, then it should obviously be allocated in stack.

## Comment 1419295568

other (NONE) · paxostv · 2023-02-06T15:44:19Z · https://github.com/golang/go/issues/51317#issuecomment-1419295568

I'd like to suggest an improvement to a potentially common case, where arenas are used in the preamble to request processing, e.g. when deserializing an incoming request:

```
func handler(...) {
	a := arena.New()
	defer a.Free()
	req := ... // Use `a`
	a.Freeze() // <--- Proposed, indicates the arena's new allocations are done
	process(req)
}
```

Here the arena lives for the duration of handling the request which could, in certain contexts, take hundreds of ms, even though allocation from the arena completes within in a fraction of the total time. This means that the partial block the arena is holding cannot be reused until completion, despite there being no need to retain the unallocated memory from it. It's proposed that calling `Freeze()` would return the partial block to the reuse list and cause panic on any subsequent allocations from the arena.

This has a couple benefits, albeit admittedly minor. First, it reduces the total number of active partial blocks, especially in cases where the total allocation amounts are small per request. This means the footprint would be marginally smaller, which may have benefits in certain contexts.

Second, it may actually improve GC overhead--despite the number of arena memory allocations remaining the same--when dealing with a bursty workloads. Since the partial blocks will be rotated more quickly, the total number of new block allocations should be reduced. If the workload processes the burst and returns to a lower steady state, we again see fewer active blocks.

The existing implementation would require a change to the current tracking of partial blocks by adding a reference count, and a boolean to indicate when they are "full".

## Comment 1419326141

other (NONE) · DeedleFake · 2023-02-06T16:03:07Z · https://github.com/golang/go/issues/51317#issuecomment-1419326141

> Suppose the api were instead:
> 
> `unsafe.InArena(f func())`
> 
> All allocations in the current goroutine in f() would happen in an arena that is freed when f completes.
> 
> the downsides:
> 
> * what if f, indirectly, tries to save memory off to the side?
> * How do you return a value from f e.g parsed json?
> * Hooks into allocations in a function in a weird way. Maybe it’s hard to implement?
> 
> 
> The upsides:
> 
> * 0% infectious api. There is no need to be arena aware anywhere in the callstack except the call site.
> * Good enough for the main use case in this thread, deserializing protobufs.
> * Easier to use than custom allocation methods.
> 
> I want to emphasize that this seems risky, but also still good enough, and the risk is entirely in the hands of the user of the method.

Maybe I'm way off-base here, but it seems to me that a cross between the two could solve some of those issues. For example,

```go
package unsafe

type Arena ...

func NewArena() *Arena
func (a *Arena) Free()
func (a *Arena) Use(f func())
```

`Use()` causes what would otherwise be heap allocations during the execution of `f` to instead allocate in `a`. With this API, existing code using `arena.New[Node](a)` would instead become `var n *Node; a.Use(func() { n = new(Node) })`.

This would allow, for example, easy usage with `big.Int` as mentioned before without causing weird subtleties from automatically freeing at the end of the function because the caller would still have total control over that. Even if something saved memory off somewhere else, it would be up to the caller to free it. This pattern would now be primarily geared towards the originally intended usage. It also fixes the `append()` issue because it could guarantee that the new slice is also in the arena.

Edit: ~~It probably makes sense to make the `Arena` type opaque so as to prevent accidental copying. I've changed the above code to reflect that.~~ Edit 2: Never mind, upon further reflection that has the undesirable side-effect of making a zero-value hard to distinguish from a valid arena due to the lack of nilability.

Should also be noted that a top-level function, if not provided, could easily be written by a user to simplify the common case:

```go
func FromArena[T any](a *unsafe.Arena, f func() T) (v T) {
  a.Use(func() { v = f() })
  return
}
```

I don't think a function like that makes sense clogging up `unsafe`, but it's so easy to write that I also don't see the need. It also would make it look like only the thing returned is in the arena, which is wrong.

Edit 3: It occurs to me that the use-arenas-in-a-function approach could also potentially fix the issue of usage of an arena internally to something. It would remove the need to pass an arena to something because the system could just see when `unsafe.NewArena()` is called that it's already operating inside of an arena and either re-use that with a special caveat in `Free()` to prevent it from being freed early or create a sub-arena. For example, let's say that `big.Int` allocated with an arena internally. If you call `var v *big.Int; a.Use(func() { v = big.NewInt(...) })`, then when `big.NewInt()` calls `unsafe.NewArena()` it would automatically just return an `*unsafe.Arena` that actually uses `a` because it was being called inside of `Use()`. The only difference between that arena and the actual `a` is that the inner one would not actually be freed when `Free()` is called on it, since that free should actually happen at the outermost usage.

## Comment 1422505043

other (NONE) · assemblaj · 2023-02-08T12:17:27Z · https://github.com/golang/go/issues/51317#issuecomment-1422505043

Edit: this comment was rude and out of line. I apologize to all involved and am now removing myself from the conversation.

## Comment 1423004791

other (NONE) · CannibalVox · 2023-02-08T17:43:29Z · https://github.com/golang/go/issues/51317#issuecomment-1423004791

The problem with arena.Use is the problem with arenas more generally. If I make code that receives a pointer and does [thing] it's impossible for me to know that the pointer is allocated on an arena and can't be safely held somewhere. People forgetting to free arenas isn't a problem IMO and explicitly choosing an allocator and passing it as a parameter (perhaps via Context or something) is more in line with existing Go standards.

On the converse, I don't think that prioritizing use cases where someone wants to hold arena-allocated objects long term is a good idea since that is contrary to the concept of an arena, whose lifetime is supposed to be limited by scope. I acknowledge that rolling snapshot storage of arbitrary key/value pairs probably requires something like that in order to be tenable, though. Maybe an unsafe method could be used to allow long-term storage of arena-allocated objects, but a  TLSF or Ring Buffer allocator that itself has a long lifetime and whose objects are only permitted to be stored in or around itself might be a better fit than an arena for this use case.

This is kind of what I mean about us needing to open a path to more types of allocation-avoiding tools.

EDIT: What I mean by the above is, we finally get a single square peg and people are trying to cram it into round holes because it's the only peg we have.

## Comment 1423032521

other (NONE) · CannibalVox · 2023-02-08T18:05:13Z · https://github.com/golang/go/issues/51317#issuecomment-1423032521

Perhaps the answer would be to simply have the danger of handling one of these pointers be signaled by the type system. Some sort of indicator that can only be removed by the `unsafe` package and otherwise must be present on any value you assign it to.

## Comment 1423066761

other (CONTRIBUTOR) · Merovius · 2023-02-08T18:32:40Z · https://github.com/golang/go/issues/51317#issuecomment-1423066761

FWIW that seems extremely close to the idea of Rust lifetimes and it seems fraught to me, to special case that into the type system for arenas.

## Comment 1423082870

other (NONE) · CannibalVox · 2023-02-08T18:47:00Z · https://github.com/golang/go/issues/51317#issuecomment-1423082870

It would be a massive pain in the ass, but the alternative seems to be "allocations are largely unavoidable in our language that pays all GC fees up front" which doesn't seem very good either.

## Comment 1424046066

other (NONE) · hauntedness · 2023-02-09T11:35:29Z · https://github.com/golang/go/issues/51317#issuecomment-1424046066

> FWIW that seems extremely close to the idea of Rust lifetimes and it seems fraught to me, to special case that into the type system for arenas.

it is really cool if go compiler can support to check lifetimes and further delete short lived objects.
we can add a new pointer type or some hint to the variable with mentioning that this variable should not be managed by gc, I assume it is predictable and short term lived.
the compiler check and report failure: No!! Please remove the hint, let it live in gc managed memory, I found danger reference....

## Comment 1424503770

other (CONTRIBUTOR) · mknyszek · 2023-02-09T16:51:56Z · https://github.com/golang/go/issues/51317#issuecomment-1424503770

> it is really cool if go compiler can support to check lifetimes and further delete short lived objects.
we can add a new pointer type or some hint to the variable with mentioning that this variable should not be managed by gc, I assume it is predictable and short term lived.

This is more or less what escape analysis allows for, and the Go compiler already does it. In other words, if the compiler can determine that a value doesn't escape the stack frame it was created in, it gets to be allocated on the stack (for the most part), and it is never managed by the GC[1]. Of course, escape analysis has room for improvement, and such improvements are another direction we could pursue in the space of designs to reuse memory more efficiently.

[1] Stacks still need to be scanned, but only when a GC's mark phase is active. By putting values on the stack instead of the heap, however, the GC's mark phase happens less frequently.

## Comment 1425716972

other (NONE) · hauntedness · 2023-02-10T12:03:22Z · https://github.com/golang/go/issues/51317#issuecomment-1425716972

@mknyszek 
Escape analysis is excellent to me, while I hope its craftsmanship would not be abandoned by arena. Escape analysis works in the way right before convenient. It is transparent to newer gopher, the user never need to worry about their memory safety. 

While from what I saw in this arena proposal, the New function return a regular go pointer. 
  1. the arena's pointer is actually different to gc's, it could be used after free. 
  2. the arena still invovles in a lot of gc works(at least the marker phase? I am not 100% sure, please correct me if any mistake). So it could be more efficient.

I suppose a new pointer type or hint could improve both above concens. Let me call it weak ref. 
  1. This weak ref is discriminated to regular pointer, so the compiler can take better effort on safety. And even for user, they don't worry about a regular pointer might come from unexpected arena. It also make user harder to misuse pointer as it is not only * on the variable. 
  2. Escape analysis is only adapted for those objects on stack frame, while this weak ref can be coordinated with compiler for heap objects. 
  3. This weak ref also benefit garbage collector as gc can somehow scan less object. 

## Comment 1426641871

other (NONE) · beoran · 2023-02-11T07:04:48Z · https://github.com/golang/go/issues/51317#issuecomment-1426641871

@hauntedness Honest question: in what ways would this new  weak pointer be different from unsafe.Pointer? Could we perhaps require the use of unsafe.Pointer for arenas?

## Comment 1426657618

other (NONE) · atdiar · 2023-02-11T08:17:35Z · https://github.com/golang/go/issues/51317#issuecomment-1426657618

@beoran not OP but from what I understand of their suggestion, an unsafe.Pointer is not typed.

What they seem to suggest is that pointers into an Arena should keep that information with them so that their scope/lifetime (which merges with the scope/lifetime of the objects these pointers are a part of) can be tracked (probably conservatively because of branching statements such as defer, goto, if etc).

Also, by indirection, taking a reference to such arena pointing objects could/would extend their lifetime?

It seems it would be a bit of a similar logic to definite assignment or typestate tracking where a variable of a given type has additional implicit/hidden mutable information/state that one may want to track (if relevant and possible).



## Comment 1426660779

other (NONE) · pat3icki · 2023-02-11T08:29:41Z · https://github.com/golang/go/issues/51317#issuecomment-1426660779

From the comments I think the Go team is worried about the abuse of `Arena` since it’s well known that developers are trying to match up with the likes of C or Cpp honestly some developers will definitely abuse it, there’re way to solve this and the one I think of,  the `unsafe` word has been the line of those who want it and those who really need it
The Go libraries is a very delicate matter but when it comes to libraries the Go community can handle that I wouldn’t recommend it in the standard lib, the standard libraries is too generic some people can use JSON for very small data while other really Big data and arena allocating small data each time can do more harm than good, `arena` (tho would prefer it if `unsafe` were to be attached) I wouldn’t be worried But there’re are people who definitely need this and that’s more valuable than those who want it 

## Comment 1426696065

other (NONE) · beoran · 2023-02-11T10:48:57Z · https://github.com/golang/go/issues/51317#issuecomment-1426696065

@atdiar I see. Then, I think we could probably add a generic type arena.Pointer[T any] that does this. Perhaps with some compiler assistance.

## Comment 1426804622

other (CONTRIBUTOR) · zephyrtronium · 2023-02-11T15:47:01Z · https://github.com/golang/go/issues/51317#issuecomment-1426804622

I think there is a misunderstanding about the concern with arenas. A substantial chunk of the "load more" bin is a discussion about whether arenas would change the memory safety properties of the language. The conclusion is that arenas are *less unsafe* than sync.Pool: they have the same failure modes, but misuse of arenas tends to fail loudly.

At this point, the concern is about how often arenas will appear in APIs that otherwise don't seem to need to care. This means the arena.Pointer[T] idea only exacerbates the problem. You'd need to use it wherever you use any pointer, because that memory might have originally come from an arena. Otherwise you don't have arena support.

## Comment 1426805583

other (NONE) · atdiar · 2023-02-11T15:52:30Z · https://github.com/golang/go/issues/51317#issuecomment-1426805583

@beoran just like @zephyrtronium indicates, I think that it shouldn't be visible to the end user here (that would complicate assignment rules too much otherwise, perhaps, although that could possibly be one solution with subtyping extended to non-interface types).
This would simply allow the compiler to find out where it is safe to call Free().

So more similar to escape analysis 
This is all speculative anyway. 

## Comment 1426983293

other (NONE) · hauntedness · 2023-02-12T09:22:30Z · https://github.com/golang/go/issues/51317#issuecomment-1426983293

> I think there is a misunderstanding about the concern with arenas. A substantial chunk of the "load more" bin is a discussion about whether arenas would change the memory safety properties of the language. The conclusion is that arenas are *less unsafe* than sync.Pool: they have the same failure modes, but misuse of arenas tends to fail loudly.
> 
> At this point, the concern is about how often arenas will appear in APIs that otherwise don't seem to need to care. This means the arena.Pointer[T] idea only exacerbates the problem. You'd need to use it wherever you use any pointer, because that memory might have originally come from an arena. Otherwise you don't have arena support.

I can not agree with the idea that it is not appeared often so we don't need to care. If it is not that often why bring this arena to go? API is not a lighthouse in language. we can't rely on common sense about how to use arena. Also, current situation is people looking at arena for performant usage. What they really need are avoid gc for performance and strong type system for safety and convenience. 

## Comment 1427053667

other (CONTRIBUTOR) · zephyrtronium · 2023-02-12T14:56:42Z · https://github.com/golang/go/issues/51317#issuecomment-1427053667

@hauntedness I think you misunderstood me. I did not mean that arenas will be rare. Exactly the opposite, in fact: I meant that arenas may be too common. APIs will need to add support for them so that users can tie those APIs' resources to the arenas they want for performance, even in places where those APIs don't themselves care.

## Comment 1444981692

other (NONE) · introspection3 · 2023-02-25T04:01:04Z · https://github.com/golang/go/issues/51317#issuecomment-1444981692

sir,please tell us the detail about "This proposal is on hold indefinitely due to serious API concerns. " 
and how to write a safe code with arena ("but without safe check")
@danscales 


## Comment 1536177566

other (CONTRIBUTOR) · choleraehyq · 2023-05-05T12:20:26Z · https://github.com/golang/go/issues/51317#issuecomment-1536177566

Is there any plan to make this feature stable or deprecated? 

## Comment 1536904580

other (CONTRIBUTOR) · ianlancetaylor · 2023-05-05T23:34:19Z · https://github.com/golang/go/issues/51317#issuecomment-1536904580

@choleraehyq Any decision will be mentioned here.  No decision has been made, nor is any likely to be made any time soon.

## Comment 1576256555

other (NONE) · lesismal · 2023-06-05T07:49:35Z · https://github.com/golang/go/issues/51317#issuecomment-1576256555

I think we also need `Append` for `Slice`, but it seems `Append` make it much more difficult cause that demands a real allocator.

## Comment 1576663003

other (CONTRIBUTOR) · soypat · 2023-06-05T12:05:37Z · https://github.com/golang/go/issues/51317#issuecomment-1576663003

What are the opinions on renaming the `arena.Clone` to something a bit more representative of what it's doing, the heapification?
- `arena.ToHeap`: Reads like english, from arena to the heap


## Comment 1635519094

other (NONE) · glycerine · 2023-07-14T08:45:22Z · https://github.com/golang/go/issues/51317#issuecomment-1635519094

I have use case for which the current arena experiment would seem to be a 95% fit.

The bottom line up front is that it would be very useful to me to be able to allocate all Go structures and pointers together, compactly, to a compact chunk of memory that is loaded from disk (or shared memory) via memory mapping, and never free-ed, simply to avoid slow deserialization (parsing of bytes into Go struct) overhead.

My specific example: I have a custom embedded database index that is about 2GB compressed on disk and needs to be parsed and deserialized into memory on startup of any program using the embedded database. It takes about 30 seconds to startup any client program at present, because of parsing overhead, which is painful.  The garbage collector spends time scanning this index structure, which is wasted time since it never changes once loaded at startup. The data consists of many hash maps and red-black trees that tell the database program where the data is located in files on the disk. To be concrete, and yet minimal and simplified, it looks something like this:

~~~
type CustomDBIndex struct {
    HashByName    map[string]*IndexElem
    HashByCode    map[int64]*IndexElem
    RedBlackTreeByDate  *RedBlackTree[time.Time, *IndexElem]
    RedBlackTreeByUser  *RedBlackTree[string, *IndexElem]
}

type  IndexElem struct {
   PathToDataOnDisk string
   OtherMetaInfo    []int
   LastWritten      time.Time
}
~~~

Since this index data is immutable, but large-ish (8 million IndexElem) it would be super useful to create it once, in a compact arena, and save it to disk. Then on startup, my program could just memory map that file and run. Without the parsing overhead, this would be very fast. And, for instance, even the read-from-disk time could be alleviated if I could have my Go program simply share via shared memory the memory chunk that holds the CustomDBIndex (and everything it directly points to) from an existing process that had already loaded it from disk.  Super speedy!

Anyway, it sounds like the current arena proposal would *almost* enable this. It would be great if the proposal could be extended to make this use case viable.  Thus I would need to have:

+ all the memory related to the CustomDBIndex would absolutely 100% have to be allocated within the arena, with no corner case exceptions.  The current arena experiment does not provide this:

"That means a valid implementation of this package is to just
allocate all memory the way the runtime normally would, and in fact, it
reserves the right to occasionally do so for some Go values." -- line 25 of https://go.dev/src/arena/arena.go

+ more than one go routine must be allowed to read the immutable data in my memory mapped arena. Oddly, the current arena wants to forbid this:

"An Arena must never be used concurrently by multiple goroutines." here: line 43 of https://go.dev/src/arena/arena.go

[edit:]
+ A simple way to enable this would be to provide a utility function that copies a struct and all of its dependencies into an arena. Thus any arbitrary Go struct with pointers and strings could be "compactified" into a memory mapped file and that could be saved to disk.  It would be great to allocate an arena that is in a memory mapped region, and get back a ptrToArena, and then be able to call `CopyRecursivelyToArena(prtToArena, ptrCustomDBIndex)`.

[comment to downvoters]: The point is, if Go is going to have a means to optimize for very short object lifetimes (such as with arenas), then the API (when redesigned) could as readily enable the programmer to provide information about very long lifetimes too. And maybe medium long lifetimes (but known precisely to the programmer) could also adopt the same API. Design a general API, and get speed wins in lots of places!

## Comment 1635974755

other (CONTRIBUTOR) · randall77 · 2023-07-14T14:48:42Z · https://github.com/golang/go/issues/51317#issuecomment-1635974755

> "An Arena must never be used concurrently by multiple goroutines." here: line 43 of https://go.dev/src/arena/arena.go

This only applies to the `Arena` type and calling methods on it. It does not apply to the allocated objects themselves.


## Comment 1638457235

other (CONTRIBUTOR) · seebs · 2023-07-17T16:15:41Z · https://github.com/golang/go/issues/51317#issuecomment-1638457235

i think it's impossible to do nested data structures as actual pointers in a thing to be mmapped, but there's a fair bit of prior art for doing nested data structures by storing "pointers" as memory-address-offsets within a block. I think capnproto does something like that.

## Comment 1676329163

other (NONE) · kolinfluence · 2023-08-13T11:32:06Z · https://github.com/golang/go/issues/51317#issuecomment-1676329163

When is this going to be standard and not experimental?

## Comment 1676334535

other (NONE) · gophun · 2023-08-13T11:48:37Z · https://github.com/golang/go/issues/51317#issuecomment-1676334535

> When is this going to be standard and not experimental?

@kolinfluence
Likely never: _"This proposal is on hold indefinitely due to serious API concerns."_

## Comment 1676422739

other (NONE) · joaoeinride · 2023-08-13T17:47:17Z · https://github.com/golang/go/issues/51317#issuecomment-1676422739

Could this API or a similar one be added as an experimental library with the documented limitations, until a safer design is found?

## Comment 1676423853

other (NONE) · gophun · 2023-08-13T17:53:07Z · https://github.com/golang/go/issues/51317#issuecomment-1676423853

@joaoeinride It has been available via GOEXPERIMENT=arena since Go 1.20, but please note, it

>  may be changed incompatibly or removed at any time, and we do not recommend its use in production.

## Comment 1676427059

other (NONE) · joaoeinride · 2023-08-13T18:08:26Z · https://github.com/golang/go/issues/51317#issuecomment-1676427059

Thanks for the prompt reply. I am aware but was curious if it could be released like "https://pkg.go.dev/golang.org/x/exp/arenas"

## Comment 1676428737

other (CONTRIBUTOR) · Merovius · 2023-08-13T18:16:57Z · https://github.com/golang/go/issues/51317#issuecomment-1676428737

@joaoeinride I believe we specifically *don't* want to do that, because it means people would use it and would have to leak it into their API to do so - which is specifically what we want to avoid. Also, FWIW, it is implemented in the runtime, so it's somewhat awkward to put into `x/exp`.

If you are only using it in internal software, you can add the `GOEXPERIMENT` to your CI system and get the same effect. If you want to use it in open source code and find this setup too painful, that's basically WAI.

At least, that's my understanding.

## Comment 1676431373

other (NONE) · gophun · 2023-08-13T18:30:36Z · https://github.com/golang/go/issues/51317#issuecomment-1676431373

Also, there was some recent drama, because several people ignored the warnings and used x/exp/slices in production, and then a function signature changed: https://github.com/golang/go/issues/61374#issuecomment-1673213058
(I personally don't want to hear any complaints in case the arena experiment is removed - you all have been warned)

## Comment 1684396314

other (NONE) · hherman1 · 2023-08-18T20:20:19Z · https://github.com/golang/go/issues/51317#issuecomment-1684396314

Is there a version of this proposal where arenas aren’t added to the standard library, but instead some important unsafe function is which enables devs to implement something like arenas? Because that would probably satisfy the initial use case and push some of the API experimentation work onto the community 

## Comment 1684425525

other (CONTRIBUTOR) · ianlancetaylor · 2023-08-18T20:53:19Z · https://github.com/golang/go/issues/51317#issuecomment-1684425525

For full efficiency arenas need to be tied into the garbage collector.  That's not something that can reasonably be exposed to user code.

Of course it's feasible to implement arenas less efficiently using direct calls to `syscall.Mmap`.  That might suffice for API experimentation work.  But the key issue here isn't so much the arena API itself.  It's the fact that if arenas are adopted then they kind of seep into a lot of other code that allocates memory.  That doesn't seem quite right.  It also seems hard to avoid.

## Comment 1684452719

other (CONTRIBUTOR) · Merovius · 2023-08-18T21:27:59Z · https://github.com/golang/go/issues/51317#issuecomment-1684452719

> Of course it's feasible to implement arenas less efficiently using direct calls to `syscall.Mmap`.

I find that surprising. I would expect this to create trouble if the types allocated from the arena themselves contain pointers.

## Comment 1684468111

other (CONTRIBUTOR) · ianlancetaylor · 2023-08-18T21:49:34Z · https://github.com/golang/go/issues/51317#issuecomment-1684468111

Sorry, you're quite right.  I wasn't thinking clearly.

## Comment 1684732453

other (CONTRIBUTOR) · zigo101 · 2023-08-19T03:22:32Z · https://github.com/golang/go/issues/51317#issuecomment-1684732453

@hherman1 No that unsafe functionalities provided. Personally, I indeed hope the "unsafe" package could provide `alloc` and `free` functions to let users manage memory themselves, so that they don't need to use cgo to do this.

## Comment 1700477535

other (NONE) · someview · 2023-08-31T07:04:12Z · https://github.com/golang/go/issues/51317#issuecomment-1700477535

Is there some plan to add this  feature to the release version

## Comment 1701848443

other (CONTRIBUTOR) · ianlancetaylor · 2023-08-31T22:10:50Z · https://github.com/golang/go/issues/51317#issuecomment-1701848443

@someview At present there are no plans for putting this into a Go release.

## Comment 1720487128

other (NONE) · gptlang · 2023-09-15T04:03:03Z · https://github.com/golang/go/issues/51317#issuecomment-1720487128

> Personally, I indeed hope the "unsafe" package could provide alloc and free functions to let users manage memory themselves, so that they don't need to use cgo to do this.

Are there any current proposals for something similar? There are a few hot paths where this could be very useful

## Comment 1721733487

other (CONTRIBUTOR) · ianlancetaylor · 2023-09-15T19:18:55Z · https://github.com/golang/go/issues/51317#issuecomment-1721733487

It is exceptionally unlikely that we would ever add functionality for freeing memory.

The discussion is also off-topic on this proposal, so please discuss in some other forum.  Thanks.

## Comment 1902634257

maintainer (MEMBER) · qiulaidongfeng · 2024-01-21T13:45:09Z · https://github.com/golang/go/issues/51317#issuecomment-1902634257

I recently studied this issue.
Based on my understanding of the proposal, and what the non-standard library can do.
I created https://gitee.com/qiulaidongfeng/arena
It Features
- It can be used in multiple goroutines at the same time
- It can be used in versions younger than go1.20 (>=go1.18)
- not happen use-after-free

Performance is also good, with 32.18n sec/op on a 16-thread benchmark.
```
goos: windows
goarch: amd64
pkg: gitee.com/qiulaidongfeng/arena
cpu: AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
                │      n      │
                │   sec/op    │
Alloc_int_P1-16   11.41n ± 1%
Alloc_int-16      32.18n ± 3%
geomean           19.17n

                │      n       │
                │     B/s      │
Alloc_int_P1-16   751.9Mi ± 1%
Alloc_int-16      266.7Mi ± 3%
geomean           447.8Mi

                │     n      │
                │    B/op    │
Alloc_int_P1-16   8.000 ± 0%
Alloc_int-16      49.00 ± 8%
geomean           19.80

                │      n       │
                │  allocs/op   │
Alloc_int_P1-16   0.000 ± 0%
Alloc_int-16      0.000 ± 0%
geomean
```
Although third-party implementations of arena perform well.
But considering that it depends on such as https://github.com/golang/go/issues/62483#issuecomment-1800913220 the idea here will not become a reality, and the other is no guarantee that do not change the existing implementation details.
An arane addition to the standard library is worthwhile.

> This proposal is on hold indefinitely due to serious API concerns

If the concerns is use-after-free , See #63671 Adding implicit alloc and free is probably not a good idea.
Even if use-after-free can occur in the standard library arena, it can be avoided by the structured allocation I describe here
https://github.com/golang/go/issues/63671#issuecomment-1774222675
It is I assume that the program has not started to use memory at a certain time node, called A1; At a certain time node, called A2, memory is used; At a certain time node, called A3, the program no longer uses memory.
So if you do NewArena before A2 and Free after A3, use-after-free doesn't happen.
Because using Arena need to explicitly call New, also avoid the https://github.com/golang/go/issues/63671#issuecomment-1774225418 said, is not convenient to come to the conclusion that when the free memory is safe.

If #18802 is completed later, there may be a way to make the arena perform equally on single goroutine and multi-Goroutine, although since it is not possible to merge the two arenas, Need https://github.com/golang/go/issues/18802#issuecomment-1888490890 description by using the dynamic pool to manage indices into the static pool, but I believe that performance is better when there are multiple cores because they are not competing for atomic operations on the same piece of memory.

I have noticed that the scene of multi-Goroutine using arena may be rare but there are some.
For example, when creating a new programming language with go, different nodes of the syntax tree can often be free at the same time.

## Comment 1903162654

maintainer (MEMBER) · qiulaidongfeng · 2024-01-22T03:59:52Z · https://github.com/golang/go/issues/51317#issuecomment-1903162654

As I review the discussion of this proposal, it appears that the arguments preventing its acceptance center on two points.

1. this introduces the possibility of use-after-free in languages with GC.

There are many solutions, as follows:

1. Such as https://gitee.com/qiulaidongfeng/arena, Arena.Free semantics is to write code mark here Arena allocated memory life cycle is over. True free exists after the GC determines that there are no references.
2. As with go:linkname, you must import unsafe to use it. Its security is similar to that of the C languages malloc and free.
3. Check memory ownership regardless of compilation speed, as rust does.
4. **Default behavior after Arena.Free call, free memory after GC confirms no reference. free memory directly after opt-in Arena.Free call. I think such a scheme can even be implemented in go1.23.**
5. Restrict the use of arena in the API, and the API cannot pass Pointers outward.
For example:
```go
// compile pass , because not return Pointer
func New()int{
a:=arena.NewArena()
b:=arena.New[int](a)
a.Free()
return b
}
// compile not pass , because return Pointer
func New()*int{
a:=arena.NewArena()
b:=arena.New[*int](a)
return b
}
```

2. arena's API is highly contagious.

See #63671 , Implicit modify some heap allocation behavior is not a good idea, the most important objection in the https://github.com/golang/go/issues/63671#issuecomment-1774225418

If arena is to be used explicitly, it does not necessarily mean infectivity.
See https://github.com/golang/go/issues/51317#issuecomment-1902634257  what I said about structured allocation .
One way to implement this idea is to put the arena in the field of the struct and use the arena in the struct's methods (without giving the memory allocated from the arena to the outside world).
The caller is then explicitly told that the behavior of using this struct and its methods is undefined from the time a method of the struct, such as Close, is called.
In this way, the user does not need to know about the arena, and if someone uses the structure and its methods after the structure's Close method is called, it only shows that the code is inherently wrong, regardless of whether there is an arena.

## Comment 1905287203

other (CONTRIBUTOR) · mknyszek · 2024-01-23T04:48:34Z · https://github.com/golang/go/issues/51317#issuecomment-1905287203

> There are many solutions, as follows:
> 
> 1. Such as https://gitee.com/qiulaidongfeng/arena, Arena.Free semantics is to write code mark here Arena allocated memory life cycle is over. True free exists after the GC determines that there are no references.

The resource wins of arenas come almost entirely from releasing memory early so it doesn't count against the GC, and the frequency of GC cycles goes down. If you have to wait until the GC determines there are no references, this is not much better than just regular heap allocation.

Actually, I'm not sure I really understand what https://gitee.com/qiulaidongfeng/arena does to help improve performance. I see it doesn't free memory in a way that allows for immediate reuse. It appears to group memory by type in 8 MiB blocks and bump-pointer allocates into the blocks. The existing memory allocator in the runtime already allocates in size classes, in P-local buffers, without any map lookups or synchronization on the fast path (except for the publication barrier on weak memory architectures). I don't see how this would be faster. Perhaps writing out heap metadata for pointer-ful allocations in bulk earlier is helpful? The gains seem marginal at best though.

(Bump-pointer allocation is an interesting direction to explore, but I suspect it's unlikely to be worth it if additional synchronization is required. The allocator's fast path is already usually [pretty fast](https://cs.opensource.google/go/go/+/master:src/runtime/malloc.go;l=911?q=nextFreeFast&sq=&ss=go%2Fgo).)

(Note: Be careful when comparing with microbenchmarks. By allocating 8 MiB up-front, the minimum total heap size you're going to get is 16 MiB. If you compare this to a microbenchmark that heap-allocates the same type with no ballast or anything, the heap will be, at most, 4 MiB in total size. That means it's not an good comparison because the latter is using half the memory and is going through twice as many GC cycles.)

> 2. As with go:linkname, you must import unsafe to use it. Its security is similar to that of the C languages malloc and free.

Compromising memory safety really feels like a very last resort, and I think we're very far from exhausting all our options.

> 3. Check memory ownership regardless of compilation speed, as rust does.

This is an interesting direction, but has a similar kind of virality as `const`.

> 4. Default behavior after Arena.Free call, free memory after GC confirms no reference. free memory directly after opt-in Arena.Free call. I think such a scheme can even be implemented in go1.23.

I do not know what you mean by this. A direct memory free without any protections means use-after-free bugs resulting in memory corruption. The implementation currently in the runtime ensures that memory corruption never occurs (only a possible immediate crash) on use-after-free.

> 5. Restrict the use of arena in the API, and the API cannot pass Pointers outward.

If your point is to bind arenas to the stack frame in which the arena is created, this is basically already what the compiler's escape analysis pass already does automatically. The general idea of emitting a compilation error if a value escapes its stack frame is interesting, but the weird part is that the compilation error depends on how sophisticated the compiler's escape analysis is. Encoding that in the spec is going to be very limiting and changing the analysis algorithm will be hard. I'm no expert on language design, but my impression is that language really has to be designed from the ground up for this sort of thing, like Rust. (Even then, Rust has been steadily expanding in sophistication to allow more flexibility, IIUC.)

> If arena is to be used explicitly, it does not necessarily mean infectivity.

Using an arena explicitly at all means that it is going to be infectious to some degree. Lots of packages cannot make use of arena allocation without changing their API to accept an arena. A common example of this is serialization packages like `encoding/json`. Another example is most tree data structures. `math/big` could accept an arena. Changing all of these packages' APIs to accept arenas as an option does not seem like the best path forward.

> One way to implement this idea is to put the arena in the field of the struct and use the arena in the struct's methods

I do not see how this helps in general. Sure, you can pass around a struct as part of an API that hides the arena, but that's not really that different from just passing around the arena.

## Comment 1905386844

maintainer (MEMBER) · qiulaidongfeng · 2024-01-23T06:47:29Z · https://github.com/golang/go/issues/51317#issuecomment-1905386844

https://gitee.com/qiulaidongfeng/arena is mainly used to explain the arena if implemented with third-party libraries, the question is how to interact with GC.
One way to do this is to use syscall.Mmap, but then the problem is to make sure the GC knows that there are go Pointers on the non-Go heap. Any solution depends on the GC implementation.
An alternative approach that does not rely on the GC implementation is to use runtime.mallocgc, but without an API like unsafe.Free, it waits for GC to free the memory.
So implementing arena in the standard library is a better choice.

>> 4. Default behavior after Arena.Free call, free memory after GC confirms no reference. free memory directly after opt-in 
>> Arena.Free call. I think such a scheme can even be implemented in go1.23.

> I do not know what you mean by this. A direct memory free without any protections means use-after-free bugs resulting in 
> memory corruption. The implementation currently in the runtime ensures that memory corruption never occurs (only a possible > immediate crash) on use-after-free.

I mean the meaning of Arena.Free is
The default free memory occurs after the GC determines that no pointer references the memory allocated from the arena. The purpose of this is to ensure that arena can be used without the risk of use-after-free.
With options like GODEBUG=arenafreenow=1, arena is allowed with the risk of use-after-free for higher performance.
free memory simply means that memory allocated from arena via the return pointer should not be dereferenced again. The runtime can do anything with this memory, including existing implementations.

>> 5. Restrict the use of arena in the API, and the API cannot pass Pointers outward.

> If your point is to bind arenas to the stack frame in which the arena is created, this is basically already what the compiler's escape analysis pass already does automatically. The general idea of emitting a compilation error if a value escapes its stack frame is interesting, but the weird part is that the compilation error depends on how sophisticated the compiler's escape analysis is. Encoding that in the spec is going to be very limiting and changing the analysis algorithm will be hard. I'm no expert on language design, but my impression is that language really has to be designed from the ground up for this sort of thing, like Rust. (Even then, Rust has been steadily expanding in sophistication to allow more flexibility, IIUC.)

What I mean specifically is that for functions that use arena, there is no possibility that a pointer created inside the function will survive the return of the function. For structs that use arena in their methods, a pointer created in any way through the struct is not allowed to survive after the struct object is reclaimed by GC.
In this way, although functions cannot write to arguments of type **int32, arena is transparent to callers. As long as Arena.Free is called before the end of the function call or Arena.Free is called with a finalizer before the struct is GC, there will be no use-after-free because subsequent program execution has no pointer to the memory allocated from the Arena.
This is backwards compatible with code that does not use arena.

> One way to implement this idea is to put the arena in the field of the struct and use the arena in the struct's methods

> I do not see how this helps in general. Sure, you can pass around a struct as part of an API that hides the arena, but that's not really that different from just passing around the arena.

Tie the lifecycle and structure of Arena together. This way, as long as there is no pointer obtained from the struct, it can still be accessed after the structure is GC. The caller does not need to know arena.

## Comment 1905560437

maintainer (MEMBER) · qiulaidongfeng · 2024-01-23T08:38:13Z · https://github.com/golang/go/issues/51317#issuecomment-1905560437

>Actually, I'm not sure I really understand what https://gitee.com/qiulaidongfeng/arena does to help improve performance. I see it doesn't free memory in a way that allows for immediate reuse. It appears to group memory by type in 8 MiB blocks and bump-pointer allocates into the blocks. The existing memory allocator in the runtime already allocates in size classes, in P-local buffers, without any map lookups or synchronization on the fast path (except for the publication barrier on weak memory architectures). I don't see how this would be faster. Perhaps writing out heap metadata for pointer-ful allocations in bulk earlier is helpful? The gains seem marginal at best though.
>(Bump-pointer allocation is an interesting direction to explore, but I suspect it's unlikely to be worth it if additional synchronization is required. The allocator's fast path is already usually [pretty fast](https://cs.opensource.google/go/go/+/master:src/runtime/malloc.go;l=911?q=nextFreeFast&sq=&ss=go%2Fgo).)

https://gitee.com/qiulaidongfeng/arena It is possible to free memory before GC determines that there is no reference.
As long as there is a risk of  use-after-free, reusing 8 MiB sized blocks through sync.Pool can be achieved.
For the caller, this is indeed free memory.This gives it better Free performance than GC.
Much of its current overhead comes from atomic operations that are used synchronously.
Just by dropping support for multiple goroutine, or using the check-out/check-in model shown in #18802 but with static size and no need to merge the sync.ShardedValue of the method, eliminate synchronization such as atomic manipulation , I believe its Alloc performance can exceed that of calling new. (On my computer, the performance of new(int) is 7+ns, it is 10+ns)
https://gitee.com/qiulaidongfeng/arena performance improvement potential mainly from it using //go:linkname runtime_mallocgc runtime.mallocgc, can customize the behavior of Alloc and Free.
Ways to improve performance that are not implemented:
1. The above mentioned methods to improve Alloc and Free performance.
2. Reduce the overhead of setting to zero value by setting the needzero parameter of runtime.mallocgc to false when zero value is not required.

>> If arena is to be used explicitly, it does not necessarily mean infectivity.

> Using an arena explicitly at all means that it is going to be infectious to some degree. Lots of packages cannot make use of arena allocation without changing their API to accept an arena. A common example of this is serialization packages like encoding/json. Another example is most tree data structures. math/big could accept an arena. Changing all of these packages' APIs to accept arenas as an option does not seem like the best path forward.

What I mean is that requiring explicit use of Arena does not mean that the caller must know Arena.
**I want this sentence to be expressed along with my other words, by hiding the use of arena within a function or within a method of a structure, so that the memory allocated through arena cannot be accessed outside of the function or structure and its methods. Use arena to be transparent to the caller.**

## Comment 1909811485

maintainer (MEMBER) · qiulaidongfeng · 2024-01-25T10:09:26Z · https://github.com/golang/go/issues/51317#issuecomment-1909811485

I noticed this benchmark after these two commits（https://gitee.com/qiulaidongfeng/arena/compare/v0.4.0...v0.5.0 ）
```
set GOEXPERIMENT=arenas
go test -bench=^*  -benchtime=2s
UseAfterFree(false)
goos: windows
goarch: amd64
pkg: gitee.com/qiulaidongfeng/arena
cpu: AMD Ryzen 7 7840HS w/ Radeon 780M Graphics
BenchmarkAlloc_int_P1-16                273490933                9.637 ns/op     933.90 MB/s           8 B/op          0 allocs/op
BenchmarkAlloc_int-16                   62029608                35.58 ns/op      252.93 MB/s          69 B/op          0 allocs/op
BenchmarkAlloc_int_new-16               281095550                8.432 ns/op    1067.37 MB/s           8 B/op          1 allocs/op
BenchmarkAlloc_intAndFree-16                5997            402418 ns/op           0.02 MB/s     8389042 B/op          7 allocs/op
BenchmarkAlloc_int_stdArena-16          210657051               11.27 ns/op      798.29 MB/s           7 B/op          0 allocs/op
BenchmarkAlloc_intAndFree_arena-16       1825330              1279 ns/op           7.04 MB/s         856 B/op          2 allocs/op
PASS
UseAfterFree(true)
BenchmarkAlloc_int_P1-16                205623828               11.61 ns/op      775.45 MB/s           8 B/op          0 allocs/op
BenchmarkAlloc_int-16                   58220772                36.24 ns/op      248.35 MB/s          50 B/op          0 allocs/op
BenchmarkAlloc_int_new-16               291649136                8.087 ns/op    1112.94 MB/s           8 B/op          1 allocs/op
BenchmarkAlloc_intAndFree-16             2008635              1169 ns/op           7.70 MB/s         511 B/op          6 allocs/op
BenchmarkAlloc_int_stdArena-16          214101681               11.28 ns/op      797.78 MB/s           7 B/op          0 allocs/op
BenchmarkAlloc_intAndFree_arena-16       1847961              1279 ns/op           7.04 MB/s         855 B/op          2 allocs/op
PASS
ok      gitee.com/qiulaidongfeng/arena  40.705s
```

It seems that the arena implemented outside my standard library supports multi-Goroutine, supports the choice of whether the use-after-free situation can occur, and can be further optimized when #18802 is completed. Scenarios in which int is allocated and 100 ints are allocated Free are comparable to the standard library's arena performance.(need UseAfterFree(true))

**It seems that the biggest advantage of the standard library experimental arena is that it doesn't keep use-after-free silent.**

I think that many packages, such as encoding/json packages, cannot use arena allocation without changing the API, which is basically unsolved in cases requiring explicit use of arena.

> Changing all of these packages' APIs to accept arenas as an option does not seem like the best path forward.

But seems no better way.
After all, it's unlikely that go will ever have an interface like this in the future to decouple where alloc's memory comes from.
```go
type Alloc[T any] interface{
Alloc(*T)
}
```
Then let the user use gls or something to pick up such an allocator for heap allocation.
This is done without changing the API, but the work becomes code rewriting that the compiler can do.
But as shown in the https://github.com/golang/go/issues/63671#issuecomment-1774225418, any change implicit heap allocation can use this reason to oppose.（ you would have to deeply inspect its code (and the code of its transitive dependencies) to draw any conclusion about when it is safe to free the memory. And you would have to repeat this exhaustive exercise any time you upgrade anything.）

## Comment 1914682477

other (NONE) · sprappcom · 2024-01-29T13:19:42Z · https://github.com/golang/go/issues/51317#issuecomment-1914682477

please do not remove arena as a feature and pls make it from experimental into standard library.
just read here which says will be removed in future. 
https://www.reddit.com/r/golang/comments/174g9b3/are_arenas_usable/

please dont.

## Comment 2465765650

other (CONTRIBUTOR) · mknyszek · 2024-11-08T21:18:39Z · https://github.com/golang/go/issues/51317#issuecomment-2465765650

https://github.com/golang/go/discussions/70257 is a discussion that is relevant to this issue.

## Comment 2855420655

other (NONE) · heavymetalmixer · 2025-05-06T17:44:11Z · https://github.com/golang/go/issues/51317#issuecomment-2855420655

Still no progress on adding arenas to Go? No offense, but it seems like that would scare away potential future Go devs in other programming branches besides Web Dev (Game dev is one that instantly cmes to mind).

## Comment 3448983467

other (CONTRIBUTOR) · gopherbot · 2025-10-26T22:47:27Z · https://github.com/golang/go/issues/51317#issuecomment-3448983467

Change https://go.dev/cl/715080 mentions this issue: `runtime: skip tests for GOEXPERIMENT=arenas that do not handle clobberfree=1`
