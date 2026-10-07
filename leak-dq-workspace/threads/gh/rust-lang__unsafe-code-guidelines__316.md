# About "unleaking": what is the required pointer provenance in `dealloc`?

- URL: https://github.com/rust-lang/unsafe-code-guidelines/issues/316
- Repo: rust-lang/unsafe-code-guidelines (language: None)
- State: open; created 2022-01-10T16:06:01Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · danielhenrymantilla · 2022-01-10T16:06:01Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316

Sorry if this is a duplicate, but I like the "keywords" I've showcased in this issue. Other related issues:
  - https://github.com/rust-lang/unsafe-code-guidelines/issues/285
  - https://github.com/rust-lang/unsafe-code-guidelines/issues/287
  - https://github.com/rust-lang/unsafe-code-guidelines/issues/256 <- this is a pervasive instance of that.
  - https://github.com/rust-lang/unsafe-code-guidelines/issues/243
  - https://github.com/rust-lang/unsafe-code-guidelines/issues/134 <- canonical issue?
  - https://github.com/rust-lang/unsafe-code-guidelines/issues/52

Note that the quite loaded term "provenance" is being used here as described mainly in https://github.com/rust-lang/unsafe-code-guidelines/issues/134.

___

## Unleaking

The stdlib libs docs [currently state, regarding `Box::leak`](https://doc.rust-lang.org/1.57.0/std/boxed/struct.Box.html#method.leak):

> Dropping the returned reference \[return value of `Box::leak()`\] will cause a memory leak. If this is not acceptable, the reference should first be wrapped with the `Box::from_raw` function producing a `Box`. This `Box` can then be dropped which will properly destroy `T` and release the allocated memory.

So, even if there is no code snippet, such statement is stating that:

```rust
fn drop_box<T> (boxed: Box<T>)
{
    drop(unsafe { Box::from_raw(Box::leak(boxed)) });
}
```

is sound, no matter the `alloc::Global` backing it.

  - <details><summary>A far-fetched / contrived generalization to any <code>impl Allocator</code></summary>

    ```rust
    fn drop_box_in<T, A : Allocator> (boxed: Box<T, A>)
    {
        let (mut ptr, alloc) = Box::into_raw_with_allocator(x);
        unsafe {
            ptr = &mut *ptr;
            drop(Box::from_raw_in(ptr, alloc));
        }
    }
    ```

    </details>

Which, given `Box`'s implementation, is assuming that if somebody asks an `impl GlobalAlloc` —or an `impl Alloc` if generalizing— memory for a `Layout::new::<T>()` (through `alloc` or `realloc`), and gets back a non-null pointer `ptr`, then it is then legal to give back `ptr` to that `impl Alloc`'s `dealloc` (or `realloc`), but with `ptr`'s provenance having been "shrunk" down to that `T`'s layout (_e.g._, through `ptr = <*mut _>::cast(&mut *ptr.cast::<MaybeUninit<T>>());`).

This, in practice, can be quite problematic for many (most?) `GlobalAlloc` implementations out there, since they do often perform some bookkeeping and whatnot laid out contiguously to the yielded allocation, and such metadata would thus not be accessible from such a returned pointer alone: the allocator would thus need to keep some extra data / state to be able to get back provenance over the user-facing allocation _and_ the contiguous metadata.

### A simplified example

```rust
use ::std::{
    alloc::{self, GlobalAlloc as _, Layout},
    mem::drop as stuff,
    ptr,
};

unsafe trait AllocI32 {
    fn alloc_i32() -> Option<ptr::NonNull<i32>>;

    unsafe
    fn dealloc(_: ptr::NonNull<i32>);
}

struct MyAllocUsingGlobalAllocUnderTheHood;

#[repr(C)]
struct I32AndMeta {
    alloc: i32,
    meta: u8,
}

static SYSTEM_ALLOC: alloc::System = alloc::System;

unsafe impl AllocI32 for MyAllocUsingGlobalAllocUnderTheHood {
    fn alloc_i32() -> Option<ptr::NonNull<i32>> {
        let layout = Layout::new::<I32AndMeta>();
        ptr::NonNull::new(unsafe { SYSTEM_ALLOC.alloc_zeroed(layout) })
            .map(ptr::NonNull::cast)
    }

    unsafe fn dealloc(ptr: ptr::NonNull<i32>) {
        let layout = Layout::new::<I32AndMeta>();
        let meta = ptr.as_ptr().cast::<u8>().add(4).read();
        stuff(meta);
        SYSTEM_ALLOC.dealloc(ptr.as_ptr().cast(), layout);
    }
}
```

The interesting lines here are:

```rust
    unsafe fn dealloc(ptr: ptr::NonNull<i32>) {
        let layout = Layout::new::<I32AndMeta>();
        let meta = ptr.as_ptr().cast::<u8>().add(4).read();
```

if `ptr` were to stem from `&i32` (_e.g._, `let r: &i32 = …; dealloc(r.into());`), even if that `&i32` had originated from an `alloc()`-yielded ptr (`let r: &i32 = alloc().unwrap().as_ref();`), then the operation reading `meta` would not be well-defined: `r.add(4)` would yield an off-by-one pointer, which would not be usable to perform a read-dereference with.

___

### The two possible workarounds

In a world without any abstraction whatsoever, the answer to this problem is easy: keep a pointer with provenance over that allocated `I32AndMeta` around (such as the `ptr` returned by `alloc` itself), and use it to "launder" the received ptr. But since there is this `Alloc` / `GlobalAlloc` boundary, the question remains: who should be responsible for doing this?

  - Would it be the `Alloc`ator, as in:
    
    ```diff
        unsafe fn dealloc(ptr: ptr::NonNull<i32>) {
            let layout = Layout::new::<I32AndMeta>();
            let ptr = ptr.as_ptr().cast::<u8>();
    +       let ptr_with_provenance: *mut u8 = Self::get_ptr_with_provenance(…);
    +       // amend `ptr` so that it points to the same place, but with a fixed provenance
    +       let ptr = <*mut u8>::wrapping_offset(
    +           ptr_with_provenance,
    +           isize::wrapping_sub(
    +               ptr.as_ptr() as _,
    +               ptr_with_provenance as _,
    +           ),
    +       );
            let meta = ptr.add(4).read(); // <- this read is now well-defined!
            stuff(meta);
            SYSTEM_ALLOC.dealloc(ptr.as_ptr().cast(), layout);
        }
    ```

  - or would it be the user of the `Alloc`ator, **by declaring "unleaking" to be a contract violation** / **by requiring that a pointer with the originally-obtained provenance be the only valid input for a `{de,re}alloc` call?**
    
    ```rust
    pub struct MutRefWithOriginalProvenance<'lt, T> {
        ptr: ptr::NonNull<T>,
        _phantom: PhantomData<&'lt mut T>,
    }
    
    impl<T> Deref{,Mut} for … { type Target = T; … }
    impl… MutRefWithOriginalProvenance… {
        pub fn into_raw…
    }
    ```
    
    ```rust
    let mut r: MutRefWithOriginalProvenance<'static, i32> = Box::reversible_leak(Box::new(42));
    *r += 27;
    unsafe {
        drop(Box::from_raw(r.into_raw()));
    }
    ```

This point ought to be clarified, and if going for the latter —or until confirming the former—, then the stdlib docs should be updated to actually disincentivize unleaking.


___

#### My potentially-obvious two cents

It feels like the "legalized unleaking" approach has the drawback of requiring that extra `get_ptr_with_provenance(…)` operation, which could come with a non-negligible cost for _all_ `GlobalAlloc` implementations, only to allow a potentially deemed niche "unleaking" operation.

But it also feels like "forbidden unleaking" approach is quite a footgun, if, for instance, even the stdlib docs have gotten it wrong for such a long time.

So this seems like the classic "let's gauge/measure the performance benefits of 'forbidden unleaking' / the performance cost of 'legalized unleaking'" to compare them against the footguns that forbidding it introduces.

Finally, and this is technically beyond Rust's reach, there is also the question of non-Rust pervasive implementations of `GlobalAlloc`, such as that of `libc` (`malloc`, `calloc`, `realloc`, `free`) and whatnot. Such implementations do use metadata, and according to @chorman0773, the cost of a `get_ptr_with_provenance(…)` operation would be very much non-negligible (and, technically, even more so since Rust cannot go and tweak such an implementation, and would thus have to wrap it in a black-box API kind of fashion).

  - So, _from the looks of it_ / IIUC, the only _practical_ approach _w.r.t._ a legalized unleaking would be to ban `malloc` _& friends_ from being used for `GlobalAlloc` implementations! But I may very well be wrong; I'll let @chorman0773 (and others) chime in and clarify this _hypothetical_ point (although if this were to be true, then I guess there is really no other choice than forbidding unleaking).

      - <sub><sup>This, in turn, could be deemed inconvenient for FFI users which would have chosen a `malloc`-powered `#[global_allocator]` to allow `free`-ing to occur from the C side, but this is yet another topic…</sup></sub>

## Comment 1009264011

other (CONTRIBUTOR) · chorman0773 · 2022-01-10T19:19:35Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1009264011

> So, from the looks of it / IIUC, the only practical approach w.r.t. a legalized unleaking would be to ban malloc & friends from being used for GlobalAlloc implementations!

This is a real kicker, because the easiest implementation for libstd to provide the allocator is either `libc::malloc` or equivalent (in lccc, proc-macro crates uses `xlang_allocate_aligned` so it can pass pointers accross the FFI boundary into `xlangfrontend-rust`, same deal however, as `aligned_alloc(size,align)` or `operator new(size,std::align_val_t{align},std::nothrow)` is a perfectly valid implementation). If we rule out this, then every rust `libstd` would have to implement its own `#[global_allocator]` from scratch. And likely, unless it is very smart, it would run into the same issues as `libc`, assuming it wants to handle large allocation sizes or alignments.

## Comment 1009287018

other (NONE) · Diggsey · 2022-01-10T19:51:16Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1009287018

AIUI, provenance for a pointer tracks (in some unspecified way) how that pointer relates to an underlying allocation. A heap allocation is a call to the [Rust memory interface](https://github.com/rust-lang/unsafe-code-guidelines/blob/master/wip/memory-interface.md).

Therefore, I don't see how it can make sense to talk about the provenance of a pointer on "the other side" of the memory interface: provenance begins when the pointer is returned from `alloc` and ends when its passed back to `dealloc`, so the correctness of the `dealloc` implementation itself cannot depend on the provenance? (Although *which* pointers you can pass to `dealloc` in the first place obviously can)

Maybe there is some layering system, where each allocator must observe the provenance rules of any allocator it defers to, but at some point there must be some "root allocator" that can slice up memory as it sees fit - either by provenance not existing at that level, or all pointers having the same provenance.

In other words, I'm not sure it's really possible to ask questions about what is sound here, when AFAIK we haven't actually specified what rules code on the other side of the memory interface must follow?

## Comment 1009298561

other (CONTRIBUTOR) · chorman0773 · 2022-01-10T20:06:24Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1009298561

>  provenance begins when the pointer is returned from alloc and ends when its passed back to dealloc, so the correctness of the dealloc implementation itself cannot depend on the provenance?

Provenance really doesn't begin or end, it's state attached to a pointer that indicates what allocation it points into and what offset/extent it can access. The allocation itself does, but it makes more sense to say that the allocation's storage duration ends when `deallocate` returns. 

> some point there must be some "root allocator" that can slice up memory as it sees fit - either by provenance not existing at that level, or all pointers having the same provenance.


This implies that you either cannot write the allocator in Rust (or at all in a way that rust requires you to follow its memory model...), that the allocator cannot access any memory via the deallocated pointer, or that the allocator must know the "original provenance" of all pointers it yields. The latter may seem like a good idea, but in practice, it implies that the allocator only pulls memory from a single contiguous range (for example, a static buffer allocator). Many `malloc` implementations use several pools, and even can directly pull memory from the kernel (`mmap`), and thus this fails.

## Comment 1009306151

other (NONE) · Diggsey · 2022-01-10T20:15:54Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1009306151

> Provenance really doesn't begin or end, it's state attached to a pointer that indicates what allocation it points into

Ok, but that state can't exist until the allocation exists (or how could it indicate the allocation...), and the allocation doesn't exist until `alloc` returns.

> This implies that you either cannot write the allocator in Rust

It implies that the rules must work at least slightly differently for code written to implement an allocator. This seems to follow directly from the fact that provenance depends on the concept of an allocation, and for this "root" allocator, there's no such thing as a heap allocation.

AFAIK, what these modified rules might be is still unspecified, hence why it is difficult to discuss answers to the questions in this issue.

## Comment 1009307564

maintainer (MEMBER) · thomcc · 2022-01-10T20:17:53Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1009307564

ISTM like forbidding the use of C memory allocators for the global allocator is a non-starter.

Supporting this is should be considered a design constraint on the set of operations we consider to be well-defined behavior, as not supporting it both retroactively make far too much code UB (far more than forbidding unleaking) — not only would this be a massive breaking change that we don't need to make (which would hurt a great deal going forward[^1]), it would prevent use of Rust from several situations that Rust was designed to be usable in.

So, it's really not an option to forbid use of common allocators. That said, the way that SB forbids these container_of-operations to access allocation metadata feels like another of these SB-specific limitation around not allowing access to memory, even if no other reference covers it. IOW, this is a tooling limitation, and probably would not be a problem for other Rust aliasing or provenance models. So, I'm not sure there's a reason to forbid that in order to make unleaking safe.

But even if so, `#[global_allocator]` being allowed to use malloc seems more important than allowing unleaking, no matter how you look at it.

[^1]: At the moment C is still the de-facto choice for writing a memory allocator (especially one intended to be the global allocator), and there's no evidence that will change anytime soon.

    Even for use within Rust by an author who knows Rust, it's honestly the case Rust is still a less-than-ideal language to use when writing an allocator: poor ergonomics for raw pointers, our sad story around thread locals, how easy it is to accidentally create a reference and invalidate some remote raw pointer into that memory, the fact that our rules are still subject to change, even before you get to concerns like momentum...

    So I don't think we should assume this is likely to change any time soon, no matter how much we might wish for there to be a really good pure rust memory allocator.

## Comment 1010709525

other (NONE) · comex · 2022-01-12T07:09:46Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1010709525

> That said, the way that SB forbids these container_of-operations to access allocation metadata feels like another of these SB-specific limitation around not allowing access to memory, even if no other reference covers it. 

Agreed.  This is a case of #256.

>  the fact that our rules are still subject to change, even before you get to concerns like momentum...

I'll note that the same is true in the C spec, where [container_of has dubious legality](https://stackoverflow.com/questions/25296019/can-a-container-of-macro-ever-be-strictly-conforming), allocators run into issues with [type-based aliasing](https://stackoverflow.com/questions/38515179/is-it-possible-to-write-a-conformant-implementation-of-malloc-in-c), and there is an ongoing effort to totally overhaul the provenance model.  These are mostly theoretical issues rather than a practical ones, as there aren't any common compiler implementations that exploit these cases of (potential) UB.  But you could say the same about Rust.  

It would be unfortunate if these UCG discussions scared people away from writing allocators in Rust, though I'm not convinced they actually are doing so.

## Comment 1011279989

maintainer (MEMBER) · thomcc · 2022-01-12T17:22:51Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1011279989

> I'll note that the same is true in the C spec, where container_of has dubious legality, allocators run into issues with type-based aliasing, and there is an ongoing effort to totally overhaul the provenance model.

The container_of operation being not strictly-conforming because "the standard 'permits an implementation to tailor how it represents pointers to the size of the objects they point at'" is along the lines of them saying `dlsym` isn't conforming, because it requires casts between function and data pointers.

TBAA doesn't cause major problems for allocators if they're carefully written, at least in C where you can follow the effective type rules — in C++ you run into the problems described [here](https://www.youtube.com/watch?v=Djw6aY0VhwI), but realistically I doubt anybody accepts arguments that you can't use memory that comes from mmap because 'the bytes inside it don't constitute objects' or whatever, please[^implicit].

And it's worth pointing out, the proposed provenance models in C are all considerably more forgiving than stacked borrows, and the responsible groups have been considerably more hesitant to declare existing code in the wild UB than SB or this group has been.

[^implicit]: I think recent wording is that objects are implicitly created or some such, which is supposed to solve that. Thankfully I haven't had to pay attention.

> It would be unfortunate if these UCG discussions scared people away from writing allocators in Rust

It's hard to say, I suspect the other concerns are larger, and didn't mention all[^panic] of the reasons it's annoying. But honestly, the ergonomics of raw pointers alone have been mostly enough to prevent from doing anything substantial, despite the fact that I have quite a few that I was very happy with in C++.

[^panic]: For example, I didn't mention the fact that it's very difficult code to write code with any guarantee that it won't panic -- panicing in an allocator is probably undesirable, often UB, and is bad news regardless, because the panic runtime will call into you reentrantly. There are several others too, if you want to write something of production-quality.

That said, it's worth noting... the outcome of "technically might be UB but practically well-supported" in C code is different than in Rust code. In Rust code you'll get an advisory filed (which will likely later be mapped to a CVE with a ludicrously high score[^cve]). The rust community, for better or worse, is very aggressive about these things. This has been [noted before](https://without.boats/blog/vulnerabilities/), but has absolutely had an effect on what libraries get written/published.

[^cve]: "9.8 critical" for soundness holes? Really?

This has probably veered well into the offtopic, though!

## Comment 1014017192

maintainer (MEMBER) · RalfJung · 2022-01-17T01:01:36Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1014017192

I agree there are unanswered questions around how to implement an allocator inside a language with a high-level provenance model. These questions apply to Rust as much as they apply to C -- I do not think it is currently possible to write an allocator and link it into an application all inside the scope of the C spec. As was said above, the allocator is a "language primitive" that performs some amount of "magic" when it comes to provenance. I am not saying that is great but I do not see Rust being at greater risk than C here -- Rust is just a lot more upfront and explicit about its provenance model, making such issues much more obvious. (IOW, there is no Miri for C.)

> Therefore, I don't see how it can make sense to talk about the provenance of a pointer on "the other side" of the memory interface: provenance begins when the pointer is returned from alloc and ends when its passed back to dealloc, so the correctness of the dealloc implementation itself cannot depend on the provenance? (Although which pointers you can pass to dealloc in the first place obviously can)

I would say there are layers here: there is provenance on the side of the allocator impementation, and provenance on the side of the allocator user, but those are basically separate from each other. When the implementation returns a pointer from `alloc`, the user will consider this pointer to have "freshly generated" provenance -- it is that freshness that enables all sorts of useful reasoning principles and optimizations. Currently this happens 'by construction': Miri / the spec will just treat `alloc` as a primitive and imbue it with a fresh provenance (`AllocId` in the case of Miri, plus whatever Stacked Borrows does).

If we consider the allocator implementation to be itself implemented in Rust, then I think we have to say that there is some kind of 'magic' that happens as the pointer crosses the allocator boundary: its provenance is changed, somewhat akin to a Stacked Borrows `Retag`. This is not a new idea, LLVM even has a way to express it: via `noalias` on the return type (which is very different from `noalias` on an argument type, but unfortunately uses the same attribute name). Correspondingly, I think we need a 'magic' primitive operation that un-does this "provenance shift" inside the `dealloc` implementation: when the pointer passes back from the user to the implementation of the allocator, we have to transform its provenance back to what the allocator has expected.

So, we could imagine that when a pointer `p` is returned from an allocation function (in LLVM terms: a function with a `noalias` return type), we do something like this:
- generate a fresh ID (e.g. `AllocId`) representing the provenance of this allocation
- store the previous provenance of `p` in some global table that maps each fresh AllocId to the original provenance of the "root pointer" for that allocation

When a pointer `p` is passed to a deallocation function (which would hence also need some kind of attribute, or we could represent both of these things via intrinsics, or whatever):
- Look up the `AllocId` of this pointer in the aforementioned global table, and use that to restore the provenance that this pointer had when it left the allocator implementation. The 'user-side' `AllocId` of this pointer now becomes invalid and must not be used any more.

I have not fully thought about how this interacts with the more intricate provenance of Stacked Borrows, but I don't see why this would not work there. This might prevent having the same memory region accessed both from inside and outside the allocator implementation, but that seems like a violation of the idea of an allocator anyway: the memory returned from `alloc` is fully owned by the user and must not be accessed by the allocator until the time that `dealloc` is called. (Of course this all can be suitably extended to cover `realloc`.)

## Comment 1166360304

other (CONTRIBUTOR) · CAD97 · 2022-06-25T20:57:40Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1166360304

The concept of "allocation planes" discussed in https://github.com/rust-lang/unsafe-code-guidelines/issues/328 might impact this discussion. For at least `Global`, the pointers it returns are *not* the ones provided by the `#[global_allocator]`; they're pointers to fresh "rust allocated object"s.

So answering the OP: the provenance of the pointer given to global `dealloc` must cover the entire "rust allocated object" allocated by global `alloc`. The implementation magic converting the `#[global_allocator]` provided pointers into fresh rust allocated objects is in charge of mapping between the rust allocated object and the pointers that `#[global_allocator]` deals in.

(For other allocator implementations, c.f. https://github.com/rust-lang/wg-allocators/issues/101.)

## Comment 1191728580

other (CONTRIBUTOR) · CAD97 · 2022-07-21T17:01:17Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1191728580

So, interesting information:

The windows implementation of `alloc::System::alloc` is roughly:

- Round alignment up to `_Alignof(*const T)`
- Allocate `size + align` with `HeapAlloc`
- Align the pointer to `align` (taking the offset pointer in the case it is already sufficiently aligned)
- Write the pointer to the allocated block at `(ptr as *mut win::LPVOID)[-1]`
- Return the aligned pointer

And `alloc::System::dealloc` is roughly:

- Read the block pointer from `(ptr as *mut win::LPVOID)[-1]`
- Give the block pointer to `HeapFree`

This means that so long as `<System as Alloc>`'s implementation is on this side of the magic allocator "rust allocated object" launder barrier, `dealloc` *absolutely does* require the same provenance as returned from `alloc`.

(Away from keyboard atm otherwise I'd try to provoke a UB diagnostic from `miri --target windows`.)

-----

I really need to fully write up my thoughts on overlapping "rust allocated objects" and putting the AM "allocated object" laundering barrier on `impl Alloc`, for multiple reasons now.

## Comment 1191931643

other (NONE) · beepster4096 · 2022-07-21T21:01:44Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1191931643

You can see this happening in https://github.com/rust-lang/miri/issues/2104.

## Comment 4104961727

other (NONE) · VorpalBlade · 2026-03-22T00:02:30Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-4104961727

This issue has not been touched in a long while, and only mentions stacked borrows. Does the newer tree borrows model change anything?

I went digging into this because of https://rust-lang.zulipchat.com/#narrow/channel/136281-t-opsem/topic/Eq.20and.20Ord.20in.20raw.20pointers/near/580851443 (which I suppose is a variation of this issue).

## Comment 4106358838

maintainer (MEMBER) · saethlin · 2026-03-22T14:35:00Z · https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-4106358838

I think Ralf's comment: https://github.com/rust-lang/unsafe-code-guidelines/issues/316#issuecomment-1014017192 is still relevant, you could replace mentions of Stacked Borrows with "Stacked/Tree Borrows".
