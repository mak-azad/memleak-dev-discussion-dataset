# `std::process::exit` is not thread-safe in combination with C code calling `exit`

- URL: https://github.com/rust-lang/rust/issues/126600
- Repo: rust-lang/rust (language: Rust)
- State: open; created 2024-06-17T15:36:23Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · teskje · 2024-06-17T15:36:23Z · https://github.com/rust-lang/rust/issues/126600

Calling `exit` concurrently from Rust and C (or from 2 different copies of the Rust runtime in the same binary) is UB. This is permitted by the C standard, and can actually cause trouble in practice since not all versions of all libc implementations do proper locking when traversing the list of `atexit` functions. For programs only using Rust, we mitigated this by adding a lock, but this only helps when *all* calls to `exit` come from Rust (and they must come from the same Rust runtime). Note that returning from `main` is equivalent to calling `exit` so it can also cause this issue.

### Current status

Mitigation on our end (only covers pure Rust programs): #126606

The current status is that the specification language stems from a time when C did not specify multithreading and the intent was to forbid reentrancy. External discussion indicates that there's intent to fix it both in libc implementations and the specs:

- glibc: https://sourceware.org/bugzilla/show_bug.cgi?id=31997
  - patch: https://sourceware.org/pipermail/libc-alpha/2024-July/158579.html
- POSIX: https://austingroupbugs.net/view.php?id=1845
   - also [a comment](https://austingroupbugs.net/view.php?id=1845#c6853) mentioning taking it to the C committee.
- libc-coord (including musl author): https://www.openwall.com/lists/libc-coord/2024/07/24/4
- musl patch: https://git.musl-libc.org/cgit/musl/commit/?id=8cca79a72cccbdb54726125d690d7d0095fc2409
- freebsd patch: https://reviews.freebsd.org/D46108
- bionic: https://android.googlesource.com/platform/bionic.git/+/089f4d17265480a5ad9311bcbd8890bc9f361801%5E%21/

### Original bugreport (partially outdated)

The current implementation of `std::process::exit` is unsound on Linux and possibly related platforms where it defers to libc's `exit()` function. `exit()` [is documented to be](https://man7.org/linux/man-pages/man3/exit.3.html#ATTRIBUTES) not thread-safe, and hence `std::process::exit` is not thread-safe either, despite being a non-`unsafe` function.

To show that this isn't just a theoretical problem, here is a minimal example that segfaults on my machine (Ubuntu with glibc 2.37):

```rust
use std::thread;

fn main() {
    for _ in 0..32 {
        unsafe { libc::atexit(exit_handler) };
    }
    for _ in 0..2 {
        thread::spawn(|| std::process::exit(0));
    }
}

extern "C" fn exit_handler() {
    thread::sleep_ms(1000);
}
```

The example contains `unsafe` code, but only to install exit handlers. AFAICT nothing about the `libc::atexit` call is unsafe. The UB is introduced by calling `std::process::exit` concurrently afterwards.

If you are curious, https://github.com/MaterializeInc/database-issues/issues/6528 lays out what causes the segfault (it's a use-after-free). That's not terribly relevant though, given that glibc has no obligation to ensure `exit()` is thread safe when it's clearly documented not to be. Instead, Rust should either mark `std::process::exit` as `unsafe` (which is something it could do for the 2024 edition), or introduce locking to ensure only a single thread gets to call `exit()` at a time.



## Comment 2173754455

reporter (CONTRIBUTOR) · teskje · 2024-06-17T15:45:26Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2173754455

This has been discussed previously in https://github.com/rust-lang/rust/issues/83994. There the decision was to not do anything about the concerns with `std::process::exit`, mostly based on the reasoning that `exit()` is thread safe. The above example shows it's clearly not, neither according to the documentation nor in the implementation.

Given that I just spend the better part of a weekend debugging a segfault that was caused by concurrent `std::process::exit` invocations I feel quite strongly that this issue deserves reconsideration.

## Comment 2173781206

maintainer (MEMBER) · ChrisDenton · 2024-06-17T15:56:52Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2173781206

On that thread joshtriplett notes:

> The same arguments apply here as they do with environment handling: some types of unsynchronized changes to the environment from C code could race with an otherwise-synchronized one from Rust on some platforms, but we don't mark the corresponding functions in std::env as unsafe.

We do now mark [`std::env::set_var`](https://doc.rust-lang.org/nightly/std/env/fn.set_var.html) as unsafe so maybe thinking on this has changed. Though I'm not sure how you would mark returning from main as being `unsafe`?

## Comment 2173929351

other (CONTRIBUTOR) · conradludgate · 2024-06-17T17:14:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2173929351

Linux libc documentation does claim that `exit()` is thread-unsafe: "MT-Unsafe race:exit", although the original thread suggests that all libc implementations introduce appropriate locks. Perhaps introducing a `Once` before calling libc::exit is sufficient and not a performance blocker?

## Comment 2174003911

maintainer (MEMBER) · the8472 · 2024-06-17T17:58:35Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174003911

Doesn't solve the problem with exit getting called from non-rust code. And no, an atexit handler won't help since it leaves a race-window and if you're in a situation where threads concurrently call exit you're already racing.

https://github.com/MaterializeInc/database-issues/issues/6528 sounds like it's either a libc bug or the assessment from the previous thread that libc _implementations_ provide the desired behavior - even if the standard language doesn't - needs to be revised.

## Comment 2174042488

maintainer (MEMBER) · ChrisDenton · 2024-06-17T18:17:28Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174042488

I'd guess the safe thing to do is kill all other threads then call `exit`.

## Comment 2174140730

maintainer (MEMBER) · the8472 · 2024-06-17T18:34:20Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174140730

Not sure if serious...

Killing threads would make anything that accesses their stacks UB. Freezing them would work but that's difficult to implement reliably. Libc would be in a position to do it since they control pthreads. But then they might as well fix their locking.

## Comment 2174262000

other (CONTRIBUTOR) · tbu- · 2024-06-17T19:29:46Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174262000

Adding 32 `atexit` handlers seems to be essential to make this segfault on my glibc 2.39+r52+gf8e4623421-1 on Arch Linux. With 31 `atexit` handlers, it doesn't segfault.

## Comment 2174288267

other (CONTRIBUTOR) · tbu- · 2024-06-17T19:42:22Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174288267

I'd say it makes sense to introduce a lock on the Rust side, since pure-Rust code shouldn't be able to cause UB by calling libc's `exit` on different threads.

This also means that Rust cdylibs mustn't call `std::process::exit` since they might not be the only language running, and applications must ensure that no foreign functions call `exit`. The latter should be a bug anyway due to the C standard saying that multiple calls to `exit` are UB.

## Comment 2174312879

reporter (CONTRIBUTOR) · teskje · 2024-06-17T19:56:32Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174312879

> https://github.com/MaterializeInc/database-issues/issues/6528 sounds like it's either a libc bug or the assessment from the previous thread that libc implementations provide the desired behavior - even if the standard language doesn't - needs to be revised.

Based on how the glibc code is set up it very much looks like `exit` isn't intended to be thread safe. It uses a lock, but releases it every time it calls one of the exit handlers. That'd make no sense if it wanted to prevent other threads from modifying the list of exit handlers concurrently. The lock is useful for preventing corruption in the face of other threads calling `atexit` in parallel. There is [a comment](https://github.com/bminor/glibc/blob/f94f6d8a3572840d3ba42ab9ace3ea522c99c0c2/stdlib/exit.h#L70) that says that this is its intended purpose (though admittedly it could be clearer).

I think the previous assumption that glibc's `exit` is thread-safe was a misconception based on the existence of this lock alone.

## Comment 2174321585

reporter (CONTRIBUTOR) · teskje · 2024-06-17T20:01:40Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174321585

> Adding 32 atexit handlers seems to be essential to make this segfault on my glibc 2.39+r52+gf8e4623421-1 on Arch Linux. With 31 atexit handlers, it doesn't segfault.

That's explained by the fact that one block in the list of exit handlers contains 32 entries, and the last block is never freed. So to trigger the use-after-free you need at least two blocks in the list. glibc installs one exit handler on its own, so 32 more need to be installed to add a free-able block to the list.

## Comment 2174323718

maintainer (MEMBER) · jieyouxu · 2024-06-17T20:02:51Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2174323718

Triage: marking this as `I-unsound`, but please readjust the label accordingly.

## Comment 2176480337

maintainer (MEMBER) · ChrisDenton · 2024-06-18T16:10:26Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2176480337

[This comment](https://github.com/rust-lang/rust/issues/83994#issuecomment-821903447) from the main author of musl was pointed out in the libs-api meeting:

> POSIX requires exit be thread-safe; it is not one of the functions listed in the exceptions, and all functions are required to be thread-safe by default. My understanding is that C11 also requires this.

I looked up the spec to confirm and it seems to be correct. https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_09_01

> All functions defined by this volume of POSIX.1-2017 shall be thread-safe, except that the following functions[1](https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_foot_1) need not be thread-safe.

`exit` is not on the list.

## Comment 2176502546

other (CONTRIBUTOR) · tbu- · 2024-06-18T16:22:28Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2176502546

According to the C11 standard, calling `exit` more than once is undefined behavior.

C11 [7.22.4.4p2](https://port70.net/~nsz/c/c11/n1570.html#7.22.4.4p2)

> If a program calls the `exit` function more than once, or calls the `quick_exit` function in addition to the `exit` function, the behavior is undefined. 

Calling it from two threads at the same time is calling it twice. It is thus explicitly thread-unsafe in C11.

## Comment 2176505739

other (CONTRIBUTOR) · tbu- · 2024-06-18T16:24:15Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2176505739

The POSIX description also contains that sentence.

https://pubs.opengroup.org/onlinepubs/009695299/functions/exit.html

> If `exit()` is called more than once, the behavior is undefined.

So the POSIX spec is kind of in conflict with itself?

## Comment 2176538243

other (NONE) · ericlagergren · 2024-06-18T16:42:18Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2176538243

@tbu- See the latter half of https://github.com/rust-lang/rust/issues/83994#issuecomment-1430013574

## Comment 2176552129

other (CONTRIBUTOR) · tbu- · 2024-06-18T16:50:11Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2176552129

> If there's any proper action to be had here, it's on the C side. The text about calling `exit` more than once being UB was written in the absence of threads and was obviously intended to make *recursive* `exit` (via `atexit` handlers) undefined, not to be a constraint on MT programs outside the scope of C. This should just be fixed (at least in POSIX and other more specific implementation specs) to make it so only the recursive case is undefined.

It makes sense to fix this on the C side, too.

Currently, we have `process::exit` causing practical UB on a tier 1 platform, it's not just a hypothetical issue, so I think something like #126606 also makes sense. Basically making sure `exit()` is only called once, and other threads calling `exit` simply going to sleep forever (until they're cleaned up by the OS).

## Comment 2179579210

maintainer (MEMBER) · Amanieu · 2024-06-19T23:42:22Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2179579210

This should probably be reported as a bug to glibc, along with a C program that reproduces the issue.

## Comment 2181988373

other (CONTRIBUTOR) · zachs18 · 2024-06-21T04:42:33Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2181988373

Here is a mostly-one-to-one C11 translation of the program in the OP that reproduces a segfault on my machine (Ubuntu 24.04, gcc 13.2.0-23ubuntu4, glibc 2.39-0ubuntu8.2), if someone wants to use it in a bug report.

<details> <summary>code</summary>

```C
#include <stdlib.h>
#include <threads.h>

void exit_handler(void) {
    thrd_sleep(&(struct timespec){.tv_sec = 1}, NULL);
}

int thread_function(void *arg) {
    (void)arg;
    exit(0);
}

int main(void) {
    for (int i = 0; i < 32; ++i) {
        atexit(exit_handler);
    }

    for (int i = 0; i < 2; ++i) {
        thrd_t thread;
        thrd_create(&thread, thread_function, NULL);
    }
}
```

</details>

## Comment 2182160566

other (CONTRIBUTOR) · carbotaniuman · 2024-06-21T07:22:05Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2182160566

> I'd say it makes sense to introduce a lock on the Rust side, since pure-Rust code shouldn't be able to cause UB by calling libc's `exit` on different threads.

This is definitely the wrong way to go, we just finished the fight with `set_var`, let's not repeat it.

## Comment 2182171354

other (CONTRIBUTOR) · tbu- · 2024-06-21T07:29:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2182171354

> This is definitely the wrong way to go, we just finished the fight with `set_var`, let's not repeat it.

I think this case is different.

Process exiting is something that should fundamentally be thread-safe. I can even see this being adopted into the C standard. Libraries are not supposed to `exit` (but they are expected to `getenv`).

The problem with safe `setenv` was that libraries were expected to `getenv` without taking a lock.

## Comment 2199274364

other (CONTRIBUTOR) · benesch · 2024-07-01T05:34:32Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2199274364

> This should probably be reported as a bug to glibc, along with a C program that reproduces the issue.

I don't think it's exactly a bug in glibc, though, and reporting it that way might get the issue bounced. The [Linux manual page for `exit(3)` says clearly](https://man7.org/linux/man-pages/man3/exit.3.html):

> The exit() function uses a global variable that is not protected, so it is not thread-safe.

So glibc is at least conforming to its own documentation.

As @richfelker said in https://github.com/rust-lang/rust/issues/83994#issuecomment-1430013574, I do think it's worth trying to get this fixed over in the POSIX/C world, but I think that looks like engaging the folks who work on the POSIX and C standards to get this updated in the next version of those standards, and looping the glibc maintainers into those conversations for feedback.

## Comment 2199287956

other (CONTRIBUTOR) · benesch · 2024-07-01T05:47:17Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2199287956

> > This is definitely the wrong way to go, we just finished the fight with `set_var`, let's not repeat it.
> 
> I think this case is different.
> 
> Process exiting is something that should fundamentally be thread-safe. I can even see this being adopted into the C standard. Libraries are not supposed to `exit` (but they are expected to `getenv`).
> 
> The problem with safe `setenv` was that libraries were expected to `getenv` without taking a lock.

I agree. Adding a lock around `std::process::exit` seems like a no downside change. As far as I can tell, doing so entirely eliminates the unsoundness. If it's later determined that there's an error in that reasoning and `std::process::exit` _must_ be marked unsafe, the existence of the lock doesn't make that transition any more difficult. And the happy case is that the POSIX and C folks agree that `exit` should be safe to call from multiple threads simultaneously, and Rust can remove the lock for platforms with `exit` implementations that are known to follow the new spec.

## Comment 2200600538

maintainer (MEMBER) · Amanieu · 2024-07-01T16:39:06Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200600538

I agree that adding a lock is fine and would solve this issue. I am slightly concerned about the possibility of deadlocks but I think it shouldn't cause any.

## Comment 2200608555

maintainer (MEMBER) · the8472 · 2024-07-01T16:44:19Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200608555

😕 How does it _fix_ the issue? Doesn't it suffer from the same problem as the environment lock, that C code can still race?

## Comment 2200627275

maintainer (MEMBER) · bjorn3 · 2024-07-01T16:56:10Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200627275

C code that follows the rules wouldn't call exit in cases where Rust could call it anyway. Only if you have multiple Rust staticlibs/cdylibs which don't share the lock can you still get issues. This is unlike the setenv issue where C code that follows the rules (doesn't call setenv once any thread is spawned) is enough to cause UB when calling setenv from the Rust side. And the setenv issue is fundamentally impossible to make safe due to the guarantees POSIX provides around getenv and the environ global, while exit is trivially to make safe by having libc add a lock.

## Comment 2200645995

maintainer (MEMBER) · the8472 · 2024-07-01T17:07:14Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200645995

I don't expect C code to follow the rules because following the rules isn't reasonable here. Linking python (or java?) and rust code was an example that was brought up in environ discussion and this applies here too.

So imo it's at best a partial bandaid, not a fix.

## Comment 2200685498

other (CONTRIBUTOR) · tbu- · 2024-07-01T17:33:30Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200685498

It's a fix for the Rust side. libc and other libraries don't call `exit` in random places (unlike `getenv`).

It's partial bandaid for the general problem, but theoretically, libraries shouldn't call `exit` anyway (again, unlike `getenv`). I feel like the situation looks *much* better than the env lock.

## Comment 2200727818

other (CONTRIBUTOR) · benesch · 2024-07-01T18:01:52Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200727818

> So imo it's at best a partial bandaid, not a fix.

It is a full fix for _this_ issue. The issue here is that a well behaved Rust program can cause memory unsafety by calling the `std::process::exit` function from multiple threads. This means that `std::process::exit` function is currently unsound. It should not be possible to cause memory unsafety in Rust by calling a safe function.

Adding a lock inside of `std::process::exit` fully fixes _this_ issue, as it will no longer be possible for a well behaved Rust program to cause memory unsafety by calling `std::process::exit`.

The issue is _not_ that C programs can cause memory unsafety by calling the libc `exit` function from multiple threads. POSIX is clear: calling libc's `exit` function twice is undefined behavior. Libraries that call libc's `exit` function **must** only do so if they have arranged to ensure that they are the only thread that will call `exit`. How C libraries (or libraries in other languages that call libc's `exit` function) arrange to do that is out of scope for Rust.

> I don't expect C code to follow the rules because following the rules isn't reasonable here.

I think it's the other way around: the only reasonable approach to writing safe C code is to mandate that C code follows the rules. Safe C code **must not** trigger undefined behavior. Any C library that wants to call `exit` safely needs to somehow ensure that no other thread could possibly cause `exit` to be called after the library calls `exit`. For example, the library could declare itself to be thread-unsafe, or it could clearly document the caller's responsibilities on a function that calls `exit`, like so:

```c
/** Terminates the current process with exit code 0.
 *
 * Calling this function concurrently with another thread that calls `exit`
 * will trigger undefined behavior. If you call this function, you MUST ensure
 * that no other threads can possibly call `exit` after this function is called.
 */
void mylib_terminate(void) {
    printf("mylib requested to exit process\n");
    exit(0);
}
```

It sounds like there is some appetite for adjusting the C standard to allow calling `exit` more than once, but until that happens, I don't think there is a Rust issue here. If C code needs to call` exit`, it must somehow arrange to ensure that `exit` is not called more than once, but how that happens is out of scope for Rust.

## Comment 2200758032

maintainer (MEMBER) · the8472 · 2024-07-01T18:21:42Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200758032

I'll repeat @RalfJung's argument https://github.com/rust-lang/rust/issues/83994#issuecomment-1430358346

This isn't about just C having UB. It's about libc/posix (not C the language) being the foundation on which most other languages build. By necessity, on platforms where raw syscalls are not available. _Safe_ languages still expose means to exit the process that end up calling C's exit(). One of Rust's aims is to be able to interoperate with such languages.

We cannot claim that it's merely some sketchy C programs that are holding it wrong. We are building on a foundation of sand. Libraries that claim to provide safe interop with safe languages are exposing UB.

`process::exit` does not even have a correctness requirement that it should be called from bin crates and not from libraries. Neither do python's or java's `exit()`. And of course zero safety requirements, since it's a safe method.

> It sounds like there is some appetite for adjusting the C standard to allow calling exit more than once, but until that happens, I don't think there is a Rust issue here.

We can't promise UB-free language interop as long as the underlying issue is not fixed.

## Comment 2200776832

other (CONTRIBUTOR) · tbu- · 2024-07-01T18:33:25Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200776832

@the8472 You haven't responded to the statement that this fix makes pure-Rust programs linking glibc on Linux not have UB on parallel `std::process::exit`.

You're correct that we can't fix the ecosystem problem without fixing the C standard and/or POSIX.

## Comment 2200786564

maintainer (MEMBER) · RalfJung · 2024-07-01T18:39:58Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200786564

That fix is a bit like the env lock though -- it's not safe under composition with non-Rust code. For the environment we eventually said the functions should be `unsafe`. So, should we make `exit` `unsafe`? That seems so silly. Even after all the things I have seen C do, I am still surprised about just how programmer-unfriendly that language is.

With the environment, the "implicit contract" that avoids races in concurrent C programs seems to be that the environment is read-only. What is that contract with `exit`? Is there a general expectation that `atexit` and `exit` can only be called on the main thread? Could we have a safe `exit` that checks whether it runs on the main thread? If not, how are C programmers expected to ever correctly call that function?

It is worth filing a bug against glibc to ask them to provide a sane interface, even if POSIX does not require sanity? I would be curious what their thoughts are about how languages built on a C runtime (which is sometimes the only runtime one can build any program on) are supposed to safely exit the process.

Cc @richfelker  for  a libc perspective

## Comment 2200797418

maintainer (MEMBER) · RalfJung · 2024-07-01T18:47:10Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200797418

If libcs cannot provide a reasonably safe `exit`, IMO we should call the syscall directly, and provide an alternative unsafe function one can call instead if one needs the atexit handlers to be run. In a concurrent world, clearly we can't be expected to call `exit`. glibc, by making it non-thread-safe, is basically putting up a big sign saying "please don't call this function in a concurrent program", and we should do as they say. It is unfortunate if that breaks things due to missing out on atexit handlers, but it's the platform that is broken, not Rust -- glibc can fix this, but we cannot.

## Comment 2200799664

other (CONTRIBUTOR) · benesch · 2024-07-01T18:48:33Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200799664

> Safe languages still expose means to exit the process that end up calling C's exit(). One of Rust's aims is to be able to interoperate with such languages.

That is a different issue, IMO. This issue is not about allowing Rust programs to interleave calls to `exit` with non-Rust code that might also call `exit`. It's just about allowing Rust programs to safely call `std::process::exit` from Rust.

> That fix is a bit like the env lock though -- it's not safe under composition with non-Rust code.

I think it's meaningfully different, though. The exit lock allows Rust code that calls `std::process::exit` to be safely composed with non-Rust code that calls `atexit`. That is a meaningful improvement in composability.

> What is that contract with `exit`? Is there a general expectation that `atexit` and `exit` can only be called on the main thread? Could we have a safe `exit` that checks whether it runs on the main thread? If not, how are C programmers expected to ever correctly call that function?

`atexit` is thread safe. You can safely call it from any thread. One reasonable way to write safe multithreaded C code is to adhere to the following rules:

  * `atexit` may be called from any thread.
  * The process can only be exited by returning from `main`. If another thread wants to exit, that thread must signal the main thread to return, rather than calling libc's `exit` function.

## Comment 2200801133

maintainer (MEMBER) · RalfJung · 2024-07-01T18:49:34Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200801133

> I think it's meaningfully different, though. The exit lock allows Rust code that calls std::process::exit to be safely composed with non-Rust code that calls atexit. 

Is that true? There can still be `atexit` calls running concurrently to `exit` iterating through the list of handlers to call. So I think there still is a race condition there.

> One reasonable way to write safe multithreaded C code is to adhere to the following rules:

For some notion of "reasonable". ;)  Basically you are saying that we have to deprecate `exit` without replacement. I think it is fair to say that "being able to exit the process at any moment by calling a specific function" is a requirement generally expected to be supported by all reasonable platforms. As evidence I bring up every single programming language that provides such a function -- they provide them, presumably, because programmers want or need them.

OTOH, there are other functions we could call instead -- [quick_exit](https://en.cppreference.com/w/cpp/utility/program/quick_exit) and [_Exit](https://en.cppreference.com/w/cpp/utility/program/_Exit). Is either of them documented as thread-safe?

## Comment 2200811172

maintainer (MEMBER) · the8472 · 2024-07-01T18:55:29Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200811172

> That is a different issue, IMO. This issue is not about allowing Rust programs to interleave calls to exit with non-Rust code that might also call exit. It's just about allowing Rust programs to safely call std::process::exit from Rust.

Well, we could add the lock and declare this issue as "fixed". But then we'd have to open another issue because the UB is still there, only more difficult to exploit.

## Comment 2200819601

maintainer (MEMBER) · bjorn3 · 2024-07-01T19:00:13Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200819601

> If libcs cannot provide a reasonably safe exit, IMO we should call the syscall directly, and provide an alternative unsafe function one can call instead if one needs the atexit handlers to be run.

`_exit()` and `_Exit()` (both functionally equivalent) skip the atexit handlers. The POSIX specification doesn't state that calling them twice is UB, unlike for `exit()`.

## Comment 2200827453

other (CONTRIBUTOR) · tbu- · 2024-07-01T19:05:27Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200827453

> Is that true? There can still be `atexit` calls running concurrently to `exit` iterating through the list of handlers to call. So I think there still is a race condition there.

Yes, it's thread-safe. `atexit` is documented to be thread-safe. There is no race-condition here. glibc also locks this.

> OTOH, there are other functions we could call instead -- [quick_exit](https://en.cppreference.com/w/cpp/utility/program/quick_exit) and [_Exit](https://en.cppreference.com/w/cpp/utility/program/_Exit). Is either of them documented as thread-safe?

`quick_exit` has the same problems as `exit`. `_Exit` is just a wrapper around the `exit_group` syscall on Linux AFAIK.

## Comment 2200827933

other (CONTRIBUTOR) · benesch · 2024-07-01T19:05:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200827933

> > I think it's meaningfully different, though. The exit lock allows Rust code that calls std::process::exit to be safely composed with non-Rust code that calls atexit.
> 
> Is that true? There can still be `atexit` calls running concurrently to `exit` iterating through the list of handlers to call. So I think there still is a race condition there.

As far as I can tell. See: https://github.com/rust-lang/rust/issues/126600#issuecomment-2174312879. Concurrent calls to `exit` and `atexit` appear to be properly synchronized, and there are comments indicating that concurrent calls to `exit` and `atexit` are meant to be safe:

https://github.com/bminor/glibc/blob/f94f6d8a3572840d3ba42ab9ace3ea522c99c0c2/stdlib/exit.c#L119-L120

See also this glibc bug report about a race during concurrent calls to `atexit` and `exit`, which was accepted and fixed: https://sourceware.org/bugzilla/show_bug.cgi?id=14333

This seems consistent with the POSIX specification, which requires that it is safe to call `atexit` and `exit` simultaneously, but declares calling `exit` more than once to be undefined behavior.

## Comment 2200836553

maintainer (MEMBER) · RalfJung · 2024-07-01T19:09:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200836553

Reading through the old issue, it seems @richfelker is of the [opinion that](https://github.com/rust-lang/rust/issues/83994#issuecomment-820572419)

> exit is thread-safe. Installing atexit handlers which free resources other threads might still be using is not thread-safe and is a bug in whatever code is installing those atexit handlers, and should be fixed there.

That directly contradicts the Linux man page when it says "MT-Unsafe race:exit". The POSIX and C standards state

> If exit() is called more than once, the behavior is undefined.

I guess it is up to interpretation whether two concurrent calls to `exit` count as "called more than once" -- glibc seems to say that yes, it does. I would say that makes `exit` not-thread-safe.   @richfelker either has a different interpretation of "called more than once" or a different definition of "thread-safe".

C also has quick_exit, but the documentation for that says

> If a program calls
the quick_exit function more than once, or calls the exit function in addition to the quick_exit
function, the behavior is undefined.

So `_Exit` seems to be the only well-behaved option.

(Turns out I am just repeating what @bjorn3 and @tbu- also already said above.)

## Comment 2200841145

other (CONTRIBUTOR) · benesch · 2024-07-01T19:11:18Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200841145

> For some notion of "reasonable". ;)

Heh, yeah, C is tricky. That's why y'all invented Rust. ;)

> Basically you are saying that we have to deprecate `exit` without replacement.

I don't think I'm saying that! Adding a lock to `std::process::exit` seems like it leaves Rust in a sound place. Then we can work to shift the ecosystem so that users who want to write a program that links together different languages that each safely call `exit` can do so. But I don't see why Rust needs to be under an obligation to provide a `std::process::exit` call that can be safely interspersed with exit calls from other languages. Of course that's a desirable end state, but it seems impossible to achieve given the current C standard.

> I think it is fair to say that "being able to exit the process at any moment by calling a specific function" is a requirement generally expected to be supported by all reasonable platforms. As evidence I bring up every single programming language that provides such a function -- they provide them, presumably, because programmers want or need them.

I do agree with this! But for me the tension is resolved by splitting this issue into two: what we can do _today_ in Rust to provide composability between `std::process::exit` and `atexit`, and what we can do in the long term by fixing the C standard to allow composability between `std::process::exit` and `exit`.

## Comment 2200858768

maintainer (MEMBER) · RalfJung · 2024-07-01T19:18:56Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200858768

With set_var and remove_var, we decided that we want Rust code to be sound under composition with "well-behaved" C (and other non-Rust) code. For the environment, that meant code which only reads and never mutates the environment. We thus had to make set_var and remove_var unsafe.

For exit, the question then is -- what does "well-behaved" C code look like? Is the answer "code that never calls `exit` ever"? Or "only call `exit` on the main thread"? I guess we can rule out C libraries calling `exit` as obviously being already broken, but what about a C binary using a Rust library calling `exit`? Following the usual practices of the C world, the C binary can expect the Rust library to not call `exit`, and therefore it can safely call `exit` on its main thread (or on a single dedicated thread). Rust providing a safe `exit` breaks this concept, and therefore we cannot provide a safe wrapper around `exit`.

> what we can do today in Rust to provide composability between std::process::exit and atexit

As we have decided when making environment mutation unsafe, this is insufficient. Rust's soundness story demands more.

## Comment 2200890764

other (CONTRIBUTOR) · benesch · 2024-07-01T19:41:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200890764

> That directly contradicts the Linux man page when it says "MT-Unsafe race:exit".

Yeah, this came up in the old thread, too. @richfelker [commented on it here](https://github.com/rust-lang/rust/issues/83994#issuecomment-821931870):

> That's the Linux man page, which seems to be going by a different definition of MT-unsafe or else just wrong.

----

> I guess it is up to interpretation whether two concurrent calls to `exit` count as "called more than once" -- glibc seems to say that yes, it does. I would say that makes `exit` not-thread-safe. @richfelker either has a different interpretation of "called more than once" or a different definition of "thread-safe".

@richfelker had an [explanation for this too](https://github.com/rust-lang/rust/issues/83994#issuecomment-1430013574) in the old thread:

> If there's any proper action to be had here, it's on the C side. The text about calling `exit` more than once being UB was written in the absence of threads and was obviously intended to make recursive `exit` (via `atexit` handlers) undefined, not to be a constraint on MT programs outside the scope of C. This should just be fixed (at least in POSIX and other more specific implementation specs) to make it so only the recursive case is undefined.

The text in the POSIX standard makes a lot more sense to me if you assume threads hadn't been invented when the text was written, as there would be no way to call exit concurrently. The only way to call exit more than once would be to have an `atexit` handler call `exit` recursively.

----

> For exit, the question then is -- what does "well-behaved" C code look like?

C doesn't offer the programmer any assistance in using `exit` safely. In my opinion, a well behaved C binary is one in which the author has audited every line of code that will be linked into that binary (regardless of whether that code is written in C or another language like Rust) and asserts that there is no code path that can allow multiple threads to call libc's `exit` function more than once.

> what about a C binary using a Rust library calling `exit`? Following the usual practices of the C world, the C binary can expect the Rust library to not call `exit`, and therefore it can safely call `exit` on its main thread (or on a single dedicated thread). Rust providing a safe `exit` breaks this concept, and therefore we cannot provide a safe wrapper around `exit`.

This is where I have a different opinion! The C binary _cannot_ expect the Rust library not to call `std::process::exit`. Someone programming in C is responsible for ensuring there is no undefined behavior when linking in libraries written in other languages. It is their responsibility to check whether the Rust library they're linking calls `std::process::exit`, and, if it does, they must somehow arrange to only trigger that call to `std::process::exit` when they can ensure that no other threads running non-Rust code will also trigger a call to libc's `exit`.

In other words: with a C binary, the programmer is responsible for upholding the requirements about not calling `exit` twice, and cannot rely on the Rust runtime to provide that guarantee.

> As we have decided when making environment mutation unsafe, this is insufficient. Rust's soundness story demands more.

It seems subtly different to me! With environment mutation, a well-behaved Rust binary that called `set_env` could call a well behaved C library that called `getenv` and cause memory unsafety. Whereas here, a well-behaved Rust library that calls `std::process::exit` could only cause memory unsafety when linked into a C binary, where it is explicitly the C programmer's responsibility to look for and prevent multiple calls to `exit`. 

That said, my opinion on Rust's soundness story is worth a lot less than yours. :)

> If libcs cannot provide a reasonably safe exit, IMO we should call the syscall directly, and provide an alternative unsafe function one can call instead if one needs the `atexit` handlers to be run.

This take seems reasonable to me, for what it's worth. The one downside I see is that if you add a function like this to the standard library, that change is largely backwards compatible:

```
/// Like `std::process::exit`, but invokes `libc::exit` in order to call
/// any handlers registered with `libc::atexit`.
///
/// Calling this function from multiple threads concurrently or calling
/// this function more than once is undefined behavior.
pub unsafe fn exit_calling_handlers(code: i32) -> !;
```

But if in the future the POSIX and C standards are adjusted to make it safe to call `exit` concurrently from multiple threads, it will be a non-backwards compatible change to make `std::process::exit` call handlers again, and remove `exit_calling_handlers`.

## Comment 2200926838

maintainer (MEMBER) · the8472 · 2024-07-01T20:01:35Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200926838

> I do agree with this! But for me the tension is resolved by splitting this issue into two: what we can do today in Rust to provide composability between std::process::exit and atexit, and what we can do in the long term by fixing the C standard to allow composability between std::process::exit and exit.

From  https://github.com/rust-lang/rust/issues/126600#issuecomment-2200627275:

> [...] Only if you have multiple Rust staticlibs/cdylibs which don't share the lock can you still get issues.

So even with a lock pure rust would still be unsound.

This is consequence of the standard library not aiming to be or require a runtime that has exclusive rights to some parts of the system API. E.g. the hotspot JVM claims ownership of certain signal handlers and they require that you go through them if you want to add hooks.

Rust doesn't do that kind of thing. The consequence is we can't pretend to be able to guard access to `exit()`.

## Comment 2200975072

other (CONTRIBUTOR) · DemiMarie · 2024-07-01T20:35:51Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200975072

> > If a program calls
> > the quick_exit function more than once, or calls the exit function in addition to the quick_exit
> > function, the behavior is undefined.
> 
> So `_Exit` seems to be the only well-behaved option.
> 
> (Turns out I am just repeating what @bjorn3 and @tbu- also already said above.)

Can we preceed that with a call to `fflush(NULL)`?  That _is_ safe, and it should avoid “why didn’t my standard streams get flushed?” complaints.

## Comment 2200990179

other (CONTRIBUTOR) · comex · 2024-07-01T20:46:23Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2200990179

> > [...] Only if you have multiple Rust staticlibs/cdylibs which don't share the lock can you still get issues.
> 
> So even with a lock pure rust would still be unsound.

Sidenote: Just like with `set_env`, it would sure be nice if we had a way for multiple otherwise-independent images within a process to coordinate with each other.  Then we could patch this by 'just' having the standard library coordinate with other copies of itself to share a lock, at least until `exit` is fixed on libc's side.  Unfortunately, as I discovered when investigating this for `set_env`, there aren't any portable libc APIs suitable for such coordination.  The only reasonable one is `dlsym`, but that doesn't work in some configurations.

## Comment 2201078298

other (CONTRIBUTOR) · benesch · 2024-07-01T21:10:03Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2201078298

> > > [...] Only if you have multiple Rust staticlibs/cdylibs which don't share the lock can you still get issues.
> > 
> > 
> > So even with a lock pure rust would still be unsound.
> 
> Sidenote: Just like with `set_env`, it would sure be nice if we had a way for multiple otherwise-independent images within a process to coordinate with each other. Then we could patch this by 'just' having the standard library coordinate with other copies of itself to share a lock, at least until `exit` is fixed on libc's side. Unfortunately, as I discovered when investigating this for `set_env`, there aren't any portable libc APIs suitable for such coordination. The only reasonable one is `dlsym`, but that doesn't work in some configurations.

Oh, interesting! I haven't spent much time working with shared or static libraries in Rust, and naively I'd always assumed that linking together multiple libraries using Rust would result in the runtime sharing some global state between the runtimes.

Is there more written up on what you tried with `set_env`, @comex? I would have expected this to be largely solved by exporting a global symbol containing the env/process lock, but maybe it is not so simple with static libraries.

## Comment 2201097961

maintainer (MEMBER) · bjorn3 · 2024-07-01T21:23:31Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2201097961

For set_env there is no way to force all callers of getenv (including the C ones) to take the environment lock. Getenv is safe to call in multithreaded programs and a fair amount of libc functions in fact call it.

## Comment 2202078307

maintainer (MEMBER) · RalfJung · 2024-07-02T06:46:00Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2202078307

>   The text in the POSIX standard makes a lot more sense to me if you assume threads hadn't been invented when the text was written, as there would be no way to call exit concurrently. The only way to call exit more than once would be to have an atexit handler call exit recursively.

I have seen that argument and find it plausible. But with glibc explicitly documenting `exit` as not-thread-safe, and their implementation evidently being non-thread-safe, it seems like other people have other interpretations of this wording.

For instance, [this list](https://developer.arm.com/documentation/dui0475/m/the-c-and-c---library-functions-reference/thread-safe-c-library-functions) does not have `exit` as a thread-safe function either.

So, @richfelker might be in the minority here with their interpretation. Has anyone tried bringing this up with the glibc folks?

> This is where I have a different opinion! The C binary cannot expect the Rust library not to call std::process::exit. Someone programming in C is responsible for ensuring there is no undefined behavior when linking in libraries written in other languages. It is their responsibility to check whether the Rust library they're linking calls std::process::exit, and, if it does, they must somehow arrange to only trigger that call to std::process::exit when they can ensure that no other threads running non-Rust code will also trigger a call to libc's exit.

That does not seem like a workable approach to me. It does not match precedent e.g. for getenv / setenv, where the answer is "only call getenv if there might be threds"; it is *not* "audit everything to find uses of setenv". A complete audit  also does not match actual practice to my knowledge, so I don't think what you are saying reflects the reality out there. It may reflect what you wish the reality should be, but that's not enough. The question was "how do C programs in practice negotiate the use of `exit`", not "how do you think they should negotiate the use of `exit`".

Now, it is very possible that the answer is "they don't, and it is pure luck that things don't explode all the time".

> It seems subtly different to me! With environment mutation, a well-behaved Rust binary that called set_env could call a well behaved C library that called getenv and cause memory unsafety. Whereas here, a well-behaved Rust library that calls std::process::exit could only cause memory unsafety when linked into a C binary, where it is explicitly the C programmer's responsibility to look for and prevent multiple calls to exit.

Where does it say that it is "explicitly the C programmer's responsibility to look for and prevent multiple calls to exit"? This is just your personal opinion for how C programs should be written, not some official guideline, as far as I know. The official glibc docs just say it's not thread-safe, end of story -- very similar to setenv.

> But if in the future the POSIX and C standards are adjusted to make it safe to call exit concurrently from multiple threads, it will be a non-backwards compatible change to make std::process::exit call handlers again, and remove exit_calling_handlers.

We can just say that `process::exit` calls the handlers if that is possible to do in a thread-safe way. (I assume on Windows similar handlers exist and they do get executed and it is thread-safe to call `exit` concurrently in multiple threads.)

## Comment 2202089376

maintainer (MEMBER) · ChrisDenton · 2024-07-02T06:51:44Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2202089376

> I have seen that argument and find it plausible. But with glibc explicitly documenting `exit` as not-thread-safe, and their implementation evidently being non-thread-safe, it seems like other people have other interpretations of this wording.

Is there any libc, other than glibc, that uses glibc's interpretation?

## Comment 2202314307

other (CONTRIBUTOR) · benesch · 2024-07-02T08:31:22Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2202314307

> I have seen that argument and find it plausible. But with glibc explicitly documenting `exit` as not-thread-safe, and their implementation evidently being non-thread-safe, it seems like other people have other interpretations of this wording.

Yeah, sorry, you and I are on the same page here about the wording being unclear in a way that allows different libc implementations to come up with different interpretations of the wording. I just thought you might not have seen Rich's argument for why he interprets the wording the way that he does. 

> So, @richfelker might be in the minority here with their interpretation. Has anyone tried bringing this up with the glibc folks?

There's a [libc mailing list thread](https://sourceware.org/pipermail/libc-alpha/2015-September/064764.html) where Andreas Schwab (a libc maintainer) posts that `exit` must be thread-safe, which is at odds with the MT-Unsafe designation in the manual. That's all I can find for historical threads on the subject. I agree that it'd be worth starting a new discussion specifically about why the glibc manual does not match the POSIX and C standards.

> The question was "how do C programs in practice negotiate the use of `exit`", not "how do you think they should negotiate the use of `exit`".

Oh, I see. Your question was:

> For exit, the question then is -- what does "well-behaved" C code look like?

and I didn't read the quotes around "well-behaved" as you meant them. For me, the phrase "well-behaved C code" means "C code that does not trigger undefined behavior." I agree there is a difference between "the C code most programmers write" and "C code that strictly adheres to the standard and therefore never triggers UB", and that most C programmers probably call `exit` in multi-threaded contexts without careful locking.

> A complete audit also does not match actual practice to my knowledge, so I don't think what you are saying reflects the reality out there. It may reflect what you wish the reality should be, but that's not enough.

Right, I was talking about responsibility, not actual practice. 

> It does not match precedent e.g. for getenv / setenv, where the answer is "only call getenv if there might be threds"; it is _not_ "audit everything to find uses of setenv".

The equivalent precedent is "don't call `exit`." Standard practice in C libraries is not to call `exit`, because libraries generally shouldn't manipulate the state of the process hosting the library. But if a C library _really_ wants to call `exit`, it could do so safely in a function that is clearly documented as MT-Unsafe.

This seems equivalent to getenv / setenv. Standard practice in C libraries is to call only `getenv` and never call `setenv`, and then hope that everyone else follows the same rule. But a library that _really_ wants to call `setenv` could do so in a function that is clearly documented to be MT-unsafe.

So it seems to me that the answer to the question of "how do C programs in practice negotiate the use of `exit`"  is that C programs in practice don't link libraries that call `exit`.

> Where does it say that it is "explicitly the C programmer's responsibility to look for and prevent multiple calls to exit"? This is just your personal opinion for how C programs should be written, not some official guideline, as far as I know. The official glibc docs just say it's not thread-safe, end of story -- very similar to setenv.

Declaring that calling `exit` more than once is UB is in the [ISO C standard](https://web.archive.org/web/20181230041359if_/http://www.open-std.org/jtc1/sc22/wg14/www/abq/c17_updated_proposed_fdis.pdf):

> If a program calls the `exit` function more than once, or calls the `quick_exit` function in addition to the exit function, the behavior is undefined.

That's not a matter of opinion—that's what the standard says. Where did I miscommunicate? With C code, ultimately someone or something is responsible for ensuring that the code is semantically valid, and part of ensuring that the code is semantically valid is ensuring that `exit` is not called twice.

## Comment 2202341464

other (CONTRIBUTOR) · benesch · 2024-07-02T08:44:47Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2202341464

> So it seems to me that the answer to the question of "how do C programs in practice negotiate the use of `exit`" is that C programs in practice don't link libraries that call `exit`.

I think part of the disagreement here is that there are two schools of thought on how to make Rust compatible with this practice:

  1. Since Rust code might be compiled into a library that gets linked into a C binary, Rust should not provide a way to safely call `libc::exit`, since doing so would violate standard practice in C.
  2. Since C programs in practice don't link libraries that call `exit`, we can rely on C programmers not to link in Rust libraries that call `std::process::exit`. (This is somewhat dangerous, but no more dangerous than what happens any time you link a library in C—you need to either assume or ensure that library doesn't trigger UB.)

## Comment 2202395132

maintainer (MEMBER) · RalfJung · 2024-07-02T09:01:41Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2202395132

> Is there any libc, other than glibc, that uses glibc's interpretation?

I assume musl is thread-safe, given Rich's position.
It would be interesting to know what bionic and the BSDs (including macOS) are doing here. Does anyone know?

@benesch 

> There's a [libc mailing list thread](https://sourceware.org/pipermail/libc-alpha/2015-September/064764.html) where Andreas Schwab (a libc maintainer) posts that exit must be thread-safe, which is at odds with the MT-Unsafe designation in the manual. That's all I can find for historical threads on the subject. I agree that it'd be worth starting a new discussion specifically about why the glibc manual does not match the POSIX and C standards.

Reading through that thread, it looks like they eventually fixed things so that file locks work properly inside `exit`. But no further discussion was had on the question of concurrent calls to `exit`.  Andreas said "exit must be thread-safe, except that calling it more than once is undefined" which I still find unclear -- `exit` is not atomic so a program calling `exit` concurrently is calling it "more than once". OTOH he did clearly say "must be thread-safe".

Once we have some data on other libcs, it seems worth bringing this all up in a bugreport. Looks like Andreas might be an ally for our cause here, which would be good.

> Right, I was talking about responsibility, not actual practice.

Who is responsible for what when multiple libraries of different origin are composed is a practical social question. It doesn't follow mechanically from the C standard, because the C standard unfortunately does not provide guidance for that kind of composition. (That's different in Rust, where we have a much clearer documentation of who is responsible to ensure which property. That's why we keep running into issues like this.)

*You claim* that the usual social expectation is that a programmer must audit everything for calls to `exit`. But I don't see that supported by any outside evidence. There are other possible social contracts here, such as "only the main thread may exit" or "libraries may never exit, only the final binary may do that".

> Declaring that calling exit more than once is UB is in the [ISO C standard](https://web.archive.org/web/20181230041359if_/http://www.open-std.org/jtc1/sc22/wg14/www/abq/c17_updated_proposed_fdis.pdf):

Indeed, but the standard does not say who is responsible for ensuring this requirement when multiple libraries of different origin are composed. Consider setenv as an instructive example for comparison -- the standard just says that data races are UB. The usual social contract is that you just can't call setenv in a concurrent program. That doesn't follow from the standard, that's just an unspoken agreement among programmers.

I was wondering whether there exists a similar agreement for `exit`.

> Since C programs in practice don't link libraries that call exit, we can rely on C programmers not to link in Rust libraries that call std::process::exit. (This is somewhat dangerous, but no more dangerous than what happens any time you link a library in C—you need to either assume or ensure that library doesn't trigger UB.)

That does not sound acceptable to me. What is a Rust programmer supposed to do when writing a library intended for consumption by C? Audit all Rust dependencies for use of `exit`? That's clearly a no-go, `exit` is a safe function so even if a crate you use doesn't call `exit` today, maybe it will do so in its next version.

> The equivalent precedent is "don't call exit." Standard practice in C libraries is not to call exit, because libraries generally shouldn't manipulate the state of the process hosting the library. But if a C library really wants to call exit, it could do so safely in a function that is clearly documented as MT-Unsafe.

In that case Rust cannot provide a safe wrapper around `exit`, since we intend safe Rust code to be safely usable in larger programs that mix C and Rust.

## Comment 2204896819

other (CONTRIBUTOR) · benesch · 2024-07-03T02:02:11Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2204896819

> That's different in Rust, where we have a much clearer documentation of who is responsible to ensure which property. That's why we keep running into issues like this.

Forgive me, but I don't think I'm familiar with this documentation! I'm relatively familiar with the Nomicon's treatment of `unsafe` within Rust programs (e.g., [the soundness principle](https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html) that Safe Rust can't cause Undefined Behavior), but it's not clear to me how to map that principle onto a C program that has linked a Rust library. Is this spelled out in more detail elsewhere?

> Who is responsible for what when multiple libraries of different origin are composed is a practical social question. It doesn't follow mechanically from the C standard, because the C standard unfortunately does not provide guidance for that kind of composition.
>
> _You claim_ that the usual social expectation is that a programmer must audit everything for calls to `exit`. But I don't see that supported by any outside evidence. There are other possible social contracts here, such as "only the main thread may exit" or "libraries may never exit, only the final binary may do that".

In my mind there's a difference between "responsibility" and "social expectations." Responsibility is what's prescribed in standards and documentation, while social norms are what happens in practice. When the C standard labels something as UB, it becomes someone else's responsibility to ensure that UB does not happen. Whether C programmers actually accept that responsibility in practice, or can be trusted to handle that responsibility in practice, is a separate question. I absolutely agree that, in practice, C programmers are not auditing their libraries for calls to `exit`. They are either trusting that their libraries do not call `exit`, or they are unaware that the standard does not take any responsibility for making multiple calls to `exit` safe and they're just getting lucky. But at the end of the day, if no tool takes responsibility for making a program safe, that responsibility _must_ fall to the programmer who chooses to use the tools. Who else could bear responsibility?

I think we just have different working definitions of "responsibility." Maybe there's a better word than "responsibility" that I should be using? Where I think we very much agree is that there should be as little space as possible between what responsibilities the standards prescribe and what responsibilities are accepted in practice. When there _is_ a gap between these two things, either the standards should be adapted to better support what happens in practice, or you have to raise awareness of the gap to try to change programmer behavior (e.g., by writing [blog posts warning about setenv being thread unsafe](http://rachelbythebay.com/w/2017/01/30/env/)).

I think we're talking past each other a bit, though—sorry! Lemme try to make things more concrete. I think Rust would be totally within its rights to declare "responsibilities for programmers linking Rust and C" like so:

> ### Writing Rust code that does not get linked with any C code
>
>  * You cannot cause Undefined Behavior unless you are writing `unsafe` Rust code. The Rust compiler and standard library are responsible for guaranteeing this.
>
> ### Linking a C library into a Rust program
> 
>   * You are responsible for ensuring that the C library does not call `setenv` concurrently with any Rust calls to `std::env::var`, `std::env::var_os`, `std::env::vars`, or `std::env::vars_os`.
>
>     [NON NORMATIVE] Why we feel good about making this your responsibility: it is widely accepted that C libraries that are intended to be used in multithreaded programs should not call `setenv`.
> 
> ### Linking a Rust library into a C program
> 
>   * You are responsible for ensuring that the C code does not call `exit` concurrently with any Rust calls to `std::process::exit`.
>
>     [NON NORMATIVE] Why we feel good about making this your responsibility: in C, it is somewhat well established that libraries should not call `exit`. That said, we don't feel that this is the ideal state of affairs, and we're working to adjust the C standard to allow calling `exit` from multiple threads concurrently.

This brings me back to my earlier question—does something like this already exist? You mentioned that Rust has good documentation on this front. Apologies for not being fully spun up on the current state of the Rust reference. I took a quick look around but didn't see anything like this.

Writing something like this down somewhere in the Rust documentation, if it's not already, seems like it'd be a huge step forward for the ecosystem. Rust would no longer be relying on the unspoken creed that multithreaded C code should not call `setenv`. Instead, the responsibility of C code to not call `setenv` concurrently with `std::env::var` would be clearly specified, along with justification for why we think this is an acceptable responsibility to push onto the end user. If there's appetite for this, I'd be happy to help prepare a PR.

Framed like this, it seems to me that there is a symmetry here. Just like `std::env::var`'s safety would rely on the fact that Rust makes it the end user's responsibility to ensure that `setenv` is never called concurrently, `std::process::exit`'s safety would rely on the fact that Rust makes it the end user's responsibility to ensure that `exit` is never called concurrently. I personally think Rust would be 100% within its rights to push the responsibility to avoid concurrent calls to `exit` onto the end user when linking Rust and C together, as long as it clearly documented that responsibility.

> That does not sound acceptable to me. What is a Rust programmer supposed to do when writing a library intended for consumption by C? Audit all Rust dependencies for use of `exit`? That's clearly a no-go, `exit` is a safe function so even if a crate you use doesn't call `exit` today, maybe it will do so in its next version.

I agree it's kind of miserable, but if Rust were to tell me clearly:

"if you are writing a Rust library that is intended for consumption by C, safe Rust cannot guarantee that the resulting program does not call `libc::exit` concurrently and induce undefined behavior; an easy way to recover this guarantee is to audit all dependencies and ensure none call `std::process::exit`" 

I would accept that responsibility.

It doesn't feel all that different to me than ensuring that when I call a Rust library from C I don't trigger undefined behavior. E.g., if I understand correctly, I can trigger UB in safe Rust from C by calling the following function

```rust
#[no_mangle]
pub extern "C" fn do_ffi(x: bool) {
    println!("{x}");
}
```

with a value that is not 0 or 1:

```c
do_ffi(2);
```

> In that case Rust cannot provide a safe wrapper around `exit`, since we intend safe Rust code to be safely usable in larger programs that mix C and Rust.

Please double check my example above, but it does seem to me that safely calling safe Rust code in programs that mix C and Rust fundamentally requires some amount of "holding it right" to not trigger unsafety (thanks to C's lack of guarantees).

----

All that said, as I sketched out in the [NON NORMATIVE] sections above, I do think responsibilities for `getenv`/`setenv` have different social norms than responsibilities for `exit`. In my experience the "don't call `setenv`" norm is more widely followed than the "don't call `exit` in libraries" norm. So I definitely see the argument here for Rust making `std::process::exit` not call `exit`. It would relieve programmers who mix Rust and C of a fairly tricky responsibility to avoid concurrent calls to `exit`.

Still, it seems like a big hammer to me! We'd be making a marginal improvement to the safety of the rare C program that links a Rust library that calls `std::process::exit` at the expense of a material behavior change to the relatively common Rust program that calls `std::process::exit` and links C libraries.

## Comment 2204908400

other (CONTRIBUTOR) · benesch · 2024-07-03T02:11:14Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2204908400

> > But if in the future the POSIX and C standards are adjusted to make it safe to call exit concurrently from multiple threads, it will be a non-backwards compatible change to make std::process::exit call handlers again, and remove exit_calling_handlers.
> 
> We can just say that `process::exit` calls the handlers if that is possible to do in a thread-safe way. (I assume on Windows similar handlers exist and they do get executed and it is thread-safe to call `exit` concurrently in multiple threads.)

Yeah, I was more worried about ripping out `exit_calling_handlers`, which would have to be done at an edition boundary. Although it just occurred to me that you probably wouldn't need to introduce `exit_calling_handlers`, unless you _really_ needed something in `std` for some reason. The `exit_calling_handlers` function already exists in `libc` as `libc::exit`. 

## Comment 2205234651

maintainer (MEMBER) · RalfJung · 2024-07-03T06:58:56Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2205234651

> Forgive me, but I don't think I'm familiar with this documentation! I'm relatively familiar with the Nomicon's treatment of unsafe within Rust programs (e.g., [the soundness principle](https://doc.rust-lang.org/nomicon/safe-unsafe-meaning.html) that Safe Rust can't cause Undefined Behavior), but it's not clear to me how to map that principle onto a C program that has linked a Rust library. Is this spelled out in more detail elsewhere?

We have the notion of a safe function, which means "calling this in arbitrary ways from safe code cannot cause UB". And for unsafe functions we document what the requirements of the caller are -- *local* requirements that the caller needs to ensure, not "go read the entire source code of everything linked into your binary", which is clearly impractical.

For `env::set_var`, we decided that a safe function needs to be safely callable even in mixed-language situations, as long as all code in all languages follows the rules for whatever is "safe" to do in that language. For the environment specifically, calling `getenv` is considered "safe" (that's something that does not follow from the standard, it is a social norm). It follows that Rust's `set_var` must be unsafe. No special documentation for mixing C and Rust is needed here, it all follows from the fact that Rust code is safe to compose. (Of course you need to be careful to align your function signatures at the boundary, but that's entirely off-topic here.)

For Rust's `exit` to be safe, it hence must be the case that as long as the C code in a mixed-language binary follows the usual expectations for the use of `exit` in C, the entire program must be safe. That's why I was asking about what these expectations are. Global checks covering the entire program are clearly neither scalable nor practical, so what are the local rules that govern use of `exit`?

(There's only so many ways I can ask this question, so at some point I will stop trying to re-phrase it again -- I'm afraid I don't have the time to write a full book deriving this all from first principles.)

> Framed like this, it seems to me that there is a symmetry here. Just like std::env::var's safety would rely on the fact that Rust makes it the end user's responsibility to ensure that setenv is never called concurrently, std::process::exit's safety would rely on the fact that Rust makes it the end user's responsibility to ensure that exit is never called concurrently. I personally think Rust would be 100% within its rights to push the responsibility to avoid concurrent calls to exit onto the end user when linking Rust and C together, as long as it clearly documented that responsibility.

But here you just argued for `exit` to be an unsafe functions, since only unsafe functions are allowed to place extra responsibility on their caller. `var` is safe because `setenv`/`set_var` are unsafe, so the responsibility is on the callers of `setenv`/`set_var` to ensure that there are no concurrent calls to `var`/`getenv` (or other kinds of environment access). So no requirement at all needs to be placed on `var`.

---

Anyway this is all hypothetical since it does not seem unlikely that glibc is just wrong here, and `exit` ought to be safe to call from any thread at any time (except inside an `atexit` handler).

## Comment 2205288675

maintainer (MEMBER) · RalfJung · 2024-07-03T07:29:07Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2205288675

Crucially, the thing that we learned in the environment debacle is that it is a bad idea for the Rust side and the C side of the same API to have different requirements for their caller. Rust was making it so that `set_var` had no requirements on Rust callers, but in doing so it implicitly imposed a requirement on C code to never call `getenv` concurrently with any Rust environment access. That's (a) impolite, who are we to decide what requirements C functions impose on their callers -- remember that people compose C code and Rust code with each other where neither the C nor the Rust author are aware that their code is used together with code from another language -- and (b) impractical, since it's not how C code is written, so people linking C and Rust have no practical way to ensure that no `getenv` ever races with a Rust `set_var`.

Suggesting that `exit` is safe in Rust but C code must do a careful *global* audit is repeating that mistake. We can't externalize this requirement on the rest of the ecosystem, we ought to do our part in ensuring safe composition.

Again, a key point here is locality. Asking people to check the signatures at the boundary is entirely fine. Asking people to check *all the code that runs on both sides of the boundary* is not. It must be possible to take arbitrary safe Rust code, and arbitrary C code that follows the C expectations of what interactions with global state are allowed, and put them together without a full audit. It is pointless to document that people should do a full audit as it's not practically possible to do that.

## Comment 2207506315

other (CONTRIBUTOR) · benesch · 2024-07-03T23:32:14Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2207506315

@RalfJung it sounds like, despite the broader conversation about mixing C and Rust, we may agree on the next steps for this issue?

1. Add a lock to `std::process::exit` on Linux (#126606), since this materially improves the situation.
2. See if we can get glibc and/or the C/POSIX standards to agree that exit must be safe to call concurrently from multiple threads.
3. If (2) fails, restart this conversation and consider changing `std::process::exit` to not call `_exit`.

So I'm happy to set this conversation down here. I want to be sensitive to the fact that it seems like you haven't found it productive!

----

I didn't want to leave your last responses hanging though, so the following sections are a few thoughts in response. 

----

What strikes me as treacherous is that you're saying Rust's soundness story in mixed C and Rust programs depends on following undocumented social norms of "safe" C code. That does not sound fully satisfying to me. As someone who is reasonably comfortable with writing both safe Rust code and "safe" C code, I still find myself uncomfortable mixing C and Rust code, because Rust has not documented what social norms it expects "safe" C code to follow. The nature of norms is that we don't all share the same norms. That is why standards and specifications exist! So that we don't need to rely on norms.

It seems to me that the solution here would be for Rust (or some as yet to be incorporated standards body that governs the safe mixing of C and Rust) to explicitly spell out the specific additional requirements on C code, beyond what the C and POSIX standards mandate, for Rust's soundness guarantees to hold. Specifically, I agree this is a good goal:

> It must be possible to take arbitrary safe Rust code, and arbitrary C code that follows the C expectations of what interactions with global state are allowed, and put them together without a full audit.

But today I don't see how I'm meant to learn what those "C expectations of what interactions with global state are allowed" if those expectations do not flow from the C standard, the POSIX standard, or my libc's man pages.

----

> And for unsafe functions we document what the requirements of the caller are -- _local_ requirements that the caller needs to ensure, not "go read the entire source code of everything linked into your binary", which is clearly impractical.

I agree "go read the entire source code of everything linked into your binary" is impractical, but the forthcoming documentation on the unsafe version of `std::env::set_var` imposes exactly this sort of nonlocal requirement on the caller:

https://github.com/rust-lang/rust/blob/1086affd98ad746e1bb02e187562b9a037e854e3/library/std/src/env.rs#L329-L341

The documentation says that it is only safe to call `set_var` in a single-threaded program. But that is exactly the kind of global requirement that you're saying `unsafe` code must not impose on its caller. The caller of `set_var` cannot locally ensure that the program does not use threads. Determining whether a program uses threads requires a global audit of the program.

So it seems to me that Rust has at least one `unsafe` function that imposes a global requirement on its caller.

> It is pointless to document that people should do a full audit as it's not practically possible to do that.

I disagree that it is pointless to document! It is extremely valuable to document, because it drives home just how hard it is to use the API safely. I for one am very glad that the new documentation for `std::env::set_var` clearly states that safe usage requires a full program audit to ensure the environment is never read concurrently with a call to `std::env::set_var`.

Also, “doesn’t tend to happen in practice” is different from “impossible.” Sufficiently cautious C projects run all sorts of static analyzers and sanitizers on their codebases to find instances of UB that are hard to spot manually. A static analyzer that runs over all C dependencies to flag any usages of `setenv` or `exit` does not sound terribly hard to write. In fact it probably already exists. 

----

> For Rust's `exit` to be safe, it hence must be the case that as long as the C code in a mixed-language binary follows the usual expectations for the use of `exit` in C, the entire program must be safe. That's why I was asking about what these expectations are. Global checks covering the entire program are clearly neither scalable nor practical, so what are the local rules that govern use of `exit`?
> 
> (There's only so many ways I can ask this question, so at some point I will stop trying to re-phrase it again -- I'm afraid I don't have the time to write a full book deriving this all from first principles.)

Similarly, I feel like I've answered each time you've asked this question! This is also the first time you've specified that you are interested in only _local_ rules that govern the safe use of `exit`. 

I agree that there do not seem to be any social norms that one can follow _locally_ to ensure that safe use of `exit` results _globally_. The closest we have to such a norm is that C libraries generally agree not to call `exit`. However, that norm doesn't help programmers of the top level application who want to call `exit` to do so safely.

----

> But here you just argued for `exit` to be an unsafe functions, since only unsafe functions are allowed to place extra responsibility on their caller. `var` is safe because `setenv`/`set_var` are unsafe, so the responsibility is on the callers of `setenv`/`set_var` to ensure that there are no concurrent calls to `var`/`getenv` (or other kinds of environment access). So no requirement at all needs to be placed on `var`.

I'm drawing a distinction between `std::process::exit` (Rust) and `exit` (C). I'll try to use `libc::exit` to refer to the latter going forward to avoid confusion.

So, what I'm saying is that `std::process::exit` can be safe because `libc::exit` is unsafe, so the responsibility is on the callers of `libc::exit` to ensure that `libc::exit` is not called more than once, whether via a direct call to `libc::exit` or via a call to `std::process::exit`. This is a nonlocal requirement to put on the caller of `libc::exit`, but it seems equivalent to the nonlocal requirement we put on the caller of `std::env::set_var`/`libc::setenv`.

Again, I agree that there are social norms in C around avoiding `libc::setenv` that do not exist to the same degree for `libc::exit`. But as I mentioned earlier, I don't think Rust's soundness should depend on undocumented social norms. I think Rust should spell out explicitly what it considers "safe" C code to mix with Rust. And then we can debate whether those expectations are good and reasonable, where a major factor in determining whether an expectation is good and reasonable is if the expectation matches our best understanding of current social norms for "safe" C code.

Part of what is appealing to me about separating out "what is expected" from "what is done in practice" is that what is done in practice can _change_ based on what is expected, to move closer to what is expected! If Rust were to clearly and loudly document "C code that is mixed with Rust cannot safely call `libc::exit`", that might start to _change_ the social norm, and get C programmers to stop calling `libc::exit`.

Of course, in this case, that's unrealistic. `libc::exit` is useful, and _should_ be threadsafe. We have decades of multithreaded C code out there that is using `libc::exit` unsafely. So the best option here is to change the POSIX/C standard to make `libc::exit` threadsafe. But there may be other more subtle cases that we discover in the future where it is easier or better to change the social norm of what is considered "safe modern C" to match Rust's needs than to change the standard. And the best (only?) way to change social norms is to spell out clearly what we want them to be. 

## Comment 2208118346

other (CONTRIBUTOR) · comex · 2024-07-04T04:55:39Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2208118346

> I assume musl is thread-safe, given Rich's position. It would be interesting to know what bionic and the BSDs (including macOS) are doing here. Does anyone know?

From my reading of [macOS's version](https://github.com/apple-oss-distributions/Libc/blob/899a3b2d52d95d75e05fb286a5e64975ec3de757/stdlib/FreeBSD/atexit.c#L236), it's thread-safe.

However…

Checking that reminded me of another issue nobody has mentioned: **C++ static destructors**.

`exit` doesn't only run functions explicitly registered with `atexit`.  It also runs destructors of C++ global variables.

So if there happens to be a thread running C++ code that continuously accesses a global variable of some class type, and another thread calls `exit`, then the first thread will suddenly run into UB.  Quite possibly in the form of use-after-free.  [Example.](https://gcc.godbolt.org/z/axzMsjos6)

And I don't think there's any social norm in C++ against accessing global variables from threads.  While [Google's C++ style guide recommends that global variables have trivially destructible types](https://softwareengineering.stackexchange.com/questions/436502/file-scope-static-variables-with-non-trivial-destructors), most programs don't follow any such rule.

In fact, I've rarely seen the issue discussed at all.  I guess it doesn't often cause problems in practice.  But that doesn't mean it's safe.

## Comment 2208249489

maintainer (MEMBER) · RalfJung · 2024-07-04T06:55:17Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2208249489

@benesch 

> it sounds like, despite the broader conversation about mixing C and Rust, we may agree on the next steps for this issue?

Sounds good. :)

> But today I don't see how I'm meant to learn what those "C expectations of what interactions with global state are allowed" if those expectations do not flow from the C standard, the POSIX standard, or my libc's man pages.

Yeah, the situation in C land is extremely unsatisfying. But it makes no sense for the Rust project to document what C programmers should do. This is something the C community needs to fix. After all, the issue already arises when mixing two C libraries in the same binary, it's not really related to Rust at all.


> The documentation says that it is only safe to call set_var in a single-threaded program. But that is exactly the kind of global requirement that you're saying unsafe code must not impose on its caller. The caller of set_var cannot locally ensure that the program does not use threads. Determining whether a program uses threads requires a global audit of the program.

They can ensure that at the beginning of `main`, and that's about it. The function documentation even says that:

>  All this makes it not practically possible for you to guarantee that no other thread will read the environment, so the only safe option is to not use set_var or remove_var in multi-threaded programs at all.

The expectation is not that anyone does a global audit, the expectation is that people stop using `set_var`. It's pretty much the only way.

> So, what I'm saying is that std::process::exit can be safe because libc::exit is unsafe, so the responsibility is on the callers of libc::exit to ensure that libc::exit is not called more than once, whether via a direct call to libc::exit or via a call to std::process::exit. 

That's equivalent to arguing that std::env::set_var can be safe because every way to access the environment in C is unsafe. It's technically a correct argument but relies on privileging Rust over all other languages in the current binary, saying "we get to make the rues, you have to follow" -- not very cooperative. For environment access we eventually decided this approach is not practical; I don't see why the same would not apply here. We can't privilege Rust; our functions (that work on global state shared with C) have the same safety requirements as the equivalent C functions, except some of these requirements can be discharged via their type signature. This could have ended with `env::var` being unsafe, but common practice in C seems to indicate that `libc::getenv` is safe so we carried that over.

@comex 

> Checking that reminded me of another issue nobody has mentioned: C++ static destructors.

Ugh, that's... "fun" I guess?
That's already broken when just considering C++. So, doesn't seem like it is possible to call `exit` anywhere in a C++ program?

## Comment 2209528988

other (CONTRIBUTOR) · comex · 2024-07-04T20:19:58Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2209528988

> Ugh, that's... "fun" I guess?
That's already broken when just considering C++. So, doesn't seem like it is possible to call `exit` anywhere in a C++ program?

Not unless you can guarantee that all other threads have exited or are in a safe state.

If you're a C++ *application*, you probably can make that guarantee with respect to your own threads.  You still have to assume that the libraries you're using don't spawn any threads themselves.  But most libraries don't spawn their own threads or, if they do, have some way to shut down those threads.  On top of that, most libraries don't use global variables.  Meanwhile, most C++ applications only use a small number of libraries (other than OS-provided libraries which are presumably safe), so it's not too much work to think about thread safety for each library. 
 
If you're a library, you can't make any guarantees.  But that's not the end of the world because libraries usually shouldn't call `exit`.  They are more likely to call `abort` or `std::terminate`, but those functions do not run global destructors.

In Rust's context, though, we consider it safe to spawn threads (which may or may not be tracked by the runtime), and we consider it safe to call into libraries that may happen to be written in C++ and make use of global variables.  With that in mind, I don't know how it can ever be safe to call `exit`.


## Comment 2209536772

maintainer (MEMBER) · the8472 · 2024-07-04T20:30:15Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2209536772

FWIW C++ static destructors came up in the previous thread https://github.com/rust-lang/rust/issues/83994#issuecomment-820646946

## Comment 2209543130

maintainer (MEMBER) · RalfJung · 2024-07-04T20:38:37Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2209543130

So apparently [returning from `main` is unsafe](https://github.com/rust-lang/rust/issues/83994#issuecomment-820759367) with such C++ libraries. I think we can safely call that a bug in these libraries -- C++ libraries that make returning from `main` unsafe when they are used in another thread just cannot be wrapped in a sound Rust API.

## Comment 2209555889

other (CONTRIBUTOR) · DemiMarie · 2024-07-04T20:57:51Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2209555889

It’s certainly a bug in these libraries, but it is apparently a somewhat widespread bug.  I know that RPM had it and IIUC RocksDB did as well.  I’m not sure if that was since fixed.

A workaround would be for Rust’s main to call `_Exit` before returning from `main`, thus preventing the implicit call to `exit`.

## Comment 2209582714

other (CONTRIBUTOR) · comex · 2024-07-04T21:36:44Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2209582714

It is a bug for a C++ library to spawn its own threads that access global data and have no API to shut them down.

It is arguably a bug even if there is an API to shut them down, but YMMV.

But I see two problematic cases where the C++ side definitely does not have a bug.

First, if a C++ library does not spawn its own threads at all, but merely offers APIs that access global data, there's no bug.  But suppose someone then writes safe Rust bindings for those APIs (and let's assume the C++ side handles its own locking, so there are no thread-safety issues aside from exiting).  A safe Rust program might spawn a thread that continually uses the APIs, then have the main thread either call `exit` or return from `main`.

Second, if the C++ side is an *application* and the Rust side is a library, then the application should be entitled to start whatever threads it wants, then stop them before exiting.  It shouldn't have to worry about a library randomly calling `exit`.  This case is a bit trickier because the C++-to-Rust interface is unsafe.  Arguably, instead of making exiting unsafe, you could say that every single Rust function exposed via `extern "C"` is responsible for guaranteeing that neither it nor anything it calls ever uses `exit`.  But I don't think that's practical.

(Which cases do RPM and RocksDB fall into?)

## Comment 2209621988

other (CONTRIBUTOR) · DemiMarie · 2024-07-04T22:46:12Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2209621988

RPM and RocksDB require that a specific cleanup function is called before `exit()`.  I don’t believe that they spawn threads of their own, at least not in this use-case.

## Comment 2210241979

maintainer (MEMBER) · RalfJung · 2024-07-05T06:09:17Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2210241979

> First, if a C++ library does not spawn its own threads at all, but merely offers APIs that access global data, there's no bug. But suppose someone then writes safe Rust bindings for those APIs (and let's assume the C++ side handles its own locking, so there are no thread-safety issues aside from exiting). A safe Rust program might spawn a thread that continually uses the APIs, then have the main thread either call exit or return from main.

That is the case I referred to above -- I don't think I agree that these libraries don't have a bug. At the very least, they must document that they may only be called on the main thread, or otherwise in a way that guarantees that the main thread keeps running while code runs inside the library. It is then a bug for a Rust library to provide a wrapper around this C++ library that does not ensure this soundness composition.

Really, such libraries should use global variables that do not get deallocated on `exit` -- there's anyway no point in doing that since the entire process is going down.

## Comment 2210347423

other (CONTRIBUTOR) · comex · 2024-07-05T07:29:34Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2210347423

> At the very least, they must document that they may only be called on the main thread, or otherwise in a way that guarantees that the main thread keeps running while code runs inside the library. It is then a bug for a Rust library to provide a wrapper around this C++ library that does not ensure this soundness composition.

They should document that you should not exit the process while concurrently using their APIs.  (Incidentally, [here is a concrete example](https://github.com/facebook/rocksdb/issues/11374#issuecomment-1548152282) of such documentation in RocksDB!  Well, except that it's a GitHub issue comment rather than documentation.  But at least it's written down…)

But anyway, from a C++ perspective, a requirement to not concurrently exit doesn't have much to do with the main thread.  After all, calling `exit` and returning from `main` are both equally 'safe' in C++.  (Even in Rust they are equally safe in the implementation today.)

And I'd argue that "you should not exit the process while concurrently using their APIs" should be the default assumption for C++ libraries.  We can't expect your average C++ library to just not use the language feature of global variables (or take pains to make all globals have trivial destructors)… even if some libraries do take that step.

So, to be slightly melodramatic, your approach boils down to: all Rust wrappers for C++ libraries need to lock the main thread around all API calls, unless the library has documented that it *doesn't* use global variables with nontrivial destructors.  That seems kind of unrealistic, from a backwards-compatibility and performance perspective.

I prefer @DemiMarie's suggestion of having the forced `_Exit` call apply to both `std::process::exit` and returns from Rust `main`.

> Really, such libraries should use global variables that do not get deallocated on `exit` -- there's anyway no point in doing that since the entire process is going down.

There are apparently [recent standards and compiler efforts](https://maskray.me/blog/2024-03-17-c++-exit-time-destructors#no_destroy-attribute) to make it easier for C++ code authors to do exactly that. 

But even this has a catch.  Disabling global destructors, as described in the link above, doesn't just prevent them from running on exit; it also prevents them from running if the library is dynamically unloaded (e.g. with `dlclose`).  This is likely to result in a memory leak if the same library is repeatedly loaded and unloaded.

Admittedly, dynamically unloading libraries is not too common, and many libraries already leak memory if you unload them.  Most languages not named C++ don't even have a standardized way to run code on unload.  But dynamic unloading is not unheard-of, so there's definitely some sense in which running destructors is the more-correct behavior.

In my opinion there ought to be a way to make destructors run on dynamic load but *not* on process exit.  But I haven't heard of such a thing.

## Comment 2210511191

maintainer (MEMBER) · RalfJung · 2024-07-05T09:15:27Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2210511191

> We don't support closing the DB while the process is exiting

:exploding_head: 
With libraries like this, you don't need any enemies...

I'm not convinced that it should be Rust's job to deal with poor library design induced by some bad choices C++ made a while ago.

C++ destructors are not run by `quick_exit`, I assume?

> dynamically unloading

I seem to recall that dynamic unloading is fundamentally broken in several ways, so that doesn't seem like a strong motivation to me.

## Comment 2211261194

other (CONTRIBUTOR) · comex · 2024-07-05T18:26:06Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211261194

> C++ destructors are not run by `quick_exit`, I assume?

Correct.

> I seem to recall that dynamic unloading is fundamentally broken in several ways, so that doesn't seem like a strong motivation to me.

'Fundamentally' may be a bit strong.  I think the main issue with it is that libraries not designed for dynamic unloading may leak memory or crash after unload.  But of course that's a chicken-and-egg scenario; it doesn't mean a library shouldn't try to do better.  On the other hand, unloading a library also unloads its dependencies recursively (if there aren't any other references to them), so you can't claim to be truly unload-safe unless you know all your dependencies are also unload-safe.  And a large fraction of the ecosystem isn't unload-safe.  Arguably that renders the existing system fundamentally broken; perhaps unloading should have been opt-in instead of opt-out.

For some concrete data points:

- musl does not support dynamic unloading and [claims that not doing so makes it more robust](https://wiki.musl-libc.org/functional-differences-from-glibc.html#Unloading_libraries).  Of the two reasons given, one has to do with "libraries not designed with `dlclose` in mind", and the other is a point about thread-local storage that in my opinion is misguided.

- Apple once tried to deprecate dynamic unloading, but never followed through.  However, Objective-C and Swift have never supported dynamic unloading.  The dynamic linker has a special case to keep libraries permanently loaded if they contain any Objective-C or Swift code.

## Comment 2211313744

maintainer (MEMBER) · bjorn3 · 2024-07-05T19:19:03Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211313744

On macOS any dynamic library which uses thread local storage (so anything statically linking libstd) doesn't get unloaded when you try to dlclose it. See also https://github.com/rust-lang/rust/issues/28794#issuecomment-368693049 for a quote from WWDC 2017 as well as https://github.com/rust-lang/rust/issues/47974 for an open issue about this.

## Comment 2211409061

other (CONTRIBUTOR) · benesch · 2024-07-05T21:01:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211409061

> Incidentally, [here is a concrete example](https://github.com/facebook/rocksdb/issues/11374#issuecomment-1548152282) of such documentation in RocksDB! Well, except that it's a GitHub issue comment rather than documentation. But at least it's written down…

Ha! Not so incidental, it turns out, as both that issue and this issue were filed as a result of segfaults in Materialize. 🫠 

> I don’t believe that they spawn threads of their own, at least not in this use-case.

RocksDB will certainly spawn threads of its own if you let it: https://github.com/facebook/rocksdb/wiki/Thread-Pool

> I prefer @DemiMarie's suggestion of having the forced `_Exit` call apply to both `std::process::exit` and returns from Rust main.

I'm starting to come around to this viewpoint. For safe composition with C++, it really does seem like the practical options are:

1. Document that it is not possible to write a safe Rust wrapper for a C++ library that uses global variables with non-trivial destructors.
2. Change `std::process::exit` to call `_Exit` instead of `exit`.

And option (1) doesn't feel _terribly_ practical given the widespread use of libraries like rust-rocksdb. Although it does seem like the RocksDB folks have pondered this question in the past (https://github.com/facebook/rocksdb/pull/9958#discussion_r874217571), and maybe they'd be amenable to revisiting whether `PosixEnv` can be marked as `STATIC_AVOID_DESTRUCTION`. 

## Comment 2211416109

maintainer (MEMBER) · RalfJung · 2024-07-05T21:10:04Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211416109

> I'm starting to come around to this viewpoint. For safe composition with C++, it really does seem like the practical options are:

Making `process::exit` call `quick_exit` should be sufficient for this, no?

Though not sure if that provides any practical advantages over `_Exit`.

## Comment 2211421613

other (CONTRIBUTOR) · benesch · 2024-07-05T21:18:06Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211421613

> > I'm starting to come around to this viewpoint. For safe composition with C++, it really does seem like the practical options are:
> 
> Making `process::exit` call `quick_exit` should be sufficient for this, no?
> 
> Though not sure if that provides any practical advantages over `_Exit`.

Yes, I think that would also be sufficient. Though it's worth noting that macOS's libc does not provide `quick_exit`. So on macOS at least you'd need to call `_Exit`.

> And option (1) doesn't feel _terribly_ practical given the widespread use of libraries like rust-rocksdb. Although it does seem like the RocksDB folks have pondered this question in the past ([facebook/rocksdb#9958 (comment)](https://github.com/facebook/rocksdb/pull/9958#discussion_r874217571)), and maybe they'd be amenable to revisiting whether `PosixEnv` can be marked as `STATIC_AVOID_DESTRUCTION`.

Turns out they already did. RocksDB looks to have corrected this in v8.4: https://github.com/facebook/rocksdb/commit/70bf5ef0934d46ec42870ee0869353fce086c12d

## Comment 2211704984

maintainer (MEMBER) · RalfJung · 2024-07-06T08:24:30Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211704984

Is there any way to make `process::exit`  pause the execution of other threads, and therefore avoid such race conditions? Or would that be a problem in itself because `atexit` handler may try to communicate with other threads?

## Comment 2211715746

maintainer (MEMBER) · Amanieu · 2024-07-06T09:12:15Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211715746

> Is there any way to make `process::exit` pause the execution of other threads, and therefore avoid such race conditions? Or would that be a problem in itself because `atexit` handler may try to communicate with other threads?

It's not possible in general, and even if it was, that would deadlock if another thread was in the middle of registering an `atexit` handler (and thus holding the lock for the `atexit` handler list).

----

My opinion is that we should either do nothing and declare this to be C's problem (and get glibc fixed), or just put a lock to protect Rust's use of `exit`.

Changing `std::process::exit` to not call exit handlers is going to be a very surprising change for many users: there are quite a few Rust programs that rely on `atexit` handlers being called on process exit (e.g. restoring the terminal mode) which this would break.

## Comment 2211873133

other (CONTRIBUTOR) · benesch · 2024-07-06T19:10:18Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211873133

> My opinion is that we should either do nothing and declare this to be C's problem (and get glibc fixed), or just put a lock to protect Rust's use of `exit`.

Any objection to doing both? It seems to me that the lock strictly improves the situation in the short term, while we can in parallel start a conversation with the C community about making `exit` threadsafe.

I looked into the process for starting that conversation. It seems that the C standard itself has little to say about thread safety. It's the POSIX standard that imposes the thread safety requirement. That's good news, because it looks much easier for the public to engage with the POSIX standard working group than the C standard working group.

I don't have the time myself, unfortunately, but if someone is so inclined, the [Austin Commons Standard Revision Group](https://www.opengroup.org/austin/) is responsible for maintaining the POSIX standard. Based on what I've read there, they would be amenable to someone joining the mailing list (https://www.opengroup.org/austin/lists.html) and starting a conversation about this defect in the specification of `exit`. 

## Comment 2211946175

other (CONTRIBUTOR) · comex · 2024-07-06T20:09:20Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211946175

> Yes, I think that would also be sufficient. Though it's worth noting that macOS's libc does not provide `quick_exit`. So on macOS at least you'd need to call `_Exit`.

macOS 15 beta does provide it.

## Comment 2211947213

maintainer (MEMBER) · RalfJung · 2024-07-06T20:09:46Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2211947213

C has concurrency since C11, so the C standard absolutely has things to say about thread safety.

## Comment 2218630505

maintainer (MEMBER) · Amanieu · 2024-07-09T20:08:01Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2218630505

We discussed this in the libs-api meeting. The conclusions were:
- We should propose making `exit` thread-safe to the people behind the C & POSIX standards.
- Separately, we should encourage popular libc implementations (e.g. musl, glibc) to make `exit` thread-safe as a QoI issue.
- For targets that don't have a thread-safe `exit`, we should introduce a lock in the standard library so at least Rust code remains safe. This is being done in #126606.
- We should *not* change `std::process::exit` to use `_Exit` or `quick_exit`. These do not execute `atexit` handlers, which will likely break many programs that depend on this behavior.

## Comment 2219490507

other (CONTRIBUTOR) · benesch · 2024-07-10T03:49:53Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2219490507

That plan sounds great to me. Thank you very much for considering this issue again!

> We should propose making exit thread-safe to the people behind the C & POSIX standards.

Do y'all have any connections to the folks behind the C & POSIX standards? Or bandwidth to drive this forward? Or were y'all hoping that someone from the Rust community would pick this up? 

## Comment 2219521780

other (CONTRIBUTOR) · BlackHoleFox · 2024-07-10T04:24:11Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2219521780

Slightly curious: did anyone in the libs-api meeting come to a conclusion about the difference between this and `std::env::set_var` in terms of "just slap a lock on it and talk to ~upstream~ POSIX" being the right way forward? Was it the likelihood of hitting it?

## Comment 2219540809

other (CONTRIBUTOR) · benesch · 2024-07-10T04:44:25Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2219540809

> Slightly curious: did anyone in the libs-api meeting come to a conclusion about the difference between this and `std::env::set_var` in terms of "just slap a lock on it and talk to ~upstream~ POSIX" being the right way forward? Was it the likelihood of hitting it?

Not on the libs-api team, but the significant difference in my mind is that Rich Felker, the maintainer of musl, is on the record as saying that `libc::setenv` _should not_  be made threadsafe ([reference](https://github.com/rust-lang/rust/issues/27970#issuecomment-1003066633)), while `libc::exit` _should_ be made threadsafe ([reference](https://github.com/rust-lang/rust/issues/83994#issuecomment-1430013574)).

So there is substantially more hope that C/POSIX would be willing to declare that `libc::exit` must be made threadsafe, and virtually no hope that that C/POSIX would be willing to declare that `libc::setenv` be made threadsafe.

## Comment 2219624490

maintainer (MEMBER) · Noratrieb · 2024-07-10T05:58:28Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2219624490

Making setenv thread safe is also not really easily possible because of the way the API works, you'd have to leak all environment variables for that to work. While making exit thread safe is incredibly trivial if you know what a lock is.

## Comment 2219662443

maintainer (MEMBER) · RalfJung · 2024-07-10T06:27:43Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2219662443

@Amanieu what about the problems due to not-thread-safe code installed by `atexit` handlers? That seems to be a common pattern at least in C++ libraries. The `exit` docs should at least warn that calling `exit`  (or returning form `main`!) while there is concurrently running C++ code can lead to problems, and maybe clarify that this is considered a bug in those libraries -- i.e., in the Rust ecosystem, libraries are generally expected to be resilient to `exit` being called (and `atexit` handlers invoked) any time.

## Comment 2220915299

maintainer (MEMBER) · Amanieu · 2024-07-10T16:02:02Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2220915299

I would simply argue that those libraries are buggy. We can certainly include this in the docs.

## Comment 2221696048

other (CONTRIBUTOR) · DemiMarie · 2024-07-10T23:24:54Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2221696048

@RalfJung In theory I agree that this should be considered a bug.  In practice, I think there may be too many buggy libraries for it to be feasible to fix them all.

When dealing with a C library with this problem, my solution was to add an `atexit()` handler that just called `_exit()`, so the library’s handler never got to run.

## Comment 2222088671

maintainer (MEMBER) · RalfJung · 2024-07-11T05:50:52Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2222088671

@DemiMarie did you mean `@Amanieu`?

> When dealing with a C library with this problem, my solution was to add an atexit() handler that just called _exit(), so the library’s handler never got to run.

So this relies on `atexit` handlers being called in reverse order of initialization?

## Comment 2223595785

other (CONTRIBUTOR) · DemiMarie · 2024-07-11T18:18:29Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2223595785

> @DemiMarie did you mean `@Amanieu`?

Both you (@RalfJung) and @Amanieu.

> > When dealing with a C library with this problem, my solution was to add an atexit() handler that just called _exit(), so the library’s handler never got to run.
> 
> So this relies on `atexit` handlers being called in reverse order of initialization?

Correct, which is required by the C standard IIUC.

## Comment 2231836657

maintainer (MEMBER) · workingjubilee · 2024-07-16T21:11:53Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2231836657

@DemiMarie wrote:
> In theory I agree that this should be considered a bug. In practice, I think there may be too many buggy libraries for it to be feasible to fix them all.

It'd be great if someone did something like make a programming language that made it easier to write libraries without trivial memory/thread-safety bugs... ah well! I suppose we will just suffer buggy libraries forever. :^)

## Comment 2231911863

other (CONTRIBUTOR) · DemiMarie · 2024-07-16T22:15:41Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2231911863

> @DemiMarie wrote:
> 
> > In theory I agree that this should be considered a bug. In practice, I think there may be too many buggy libraries for it to be feasible to fix them all.
> 
> It'd be great if someone did something like make a programming language that made it easier to write libraries without trivial memory/thread-safety bugs... ah well! I suppose we will just suffer buggy libraries forever. :^)

Sadly, often the existing libraries represent enormous amounts of engineering effort that is competely infeasible to reimplement from scratch.

## Comment 2239434377

maintainer (MEMBER) · RalfJung · 2024-07-19T15:14:04Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2239434377

I have filed this against glibc, let's see what they say: https://sourceware.org/bugzilla/show_bug.cgi?id=31997.

## Comment 2240177977

other (NONE) · ThePhD · 2024-07-19T21:27:31Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2240177977

> Do y'all have any connections to the folks behind the C & POSIX standards? Or bandwidth to drive this forward? Or were y'all hoping that someone from the Rust community would pick this up?

Someone linked me this thread complaining about it so that has, at least, put it on my radar.

As for what the proper fix is, after reading through the thread I'm just going to wait a bit to see what glibc says while also bringing it up in casual conversation with other C Committee members. And then go from there.

## Comment 2240246031

maintainer (MEMBER) · workingjubilee · 2024-07-19T21:42:29Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2240246031

re: C, POSIX, and glibc's bug, my understanding is the relevant standards require at minimum supporting the registration of 32 atexit handlers.

It is obviously nonsense for an implementation to only support 32 and then reserve one of those slots for _itself_. No one can program against that, as then there is no reason for the implementation to not reserve **32** slots, which is essentially just a statement that atexit support is not required.

## Comment 2240254972

maintainer (MEMBER) · ChrisDenton · 2024-07-19T21:47:02Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2240254972

As far as I understand it, according to the C specification `exit` is thread safe because it's not on the list of exceptions to thread-safety (https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_09_01). So either there's a bug in the spec or there's a bug in glibc.

## Comment 2240299565

other (NONE) · richfelker · 2024-07-19T21:56:24Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2240299565

> As far as I understand it, according to the C specification `exit` is thread safe because it's not on the list of exceptions to thread-safety (https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_09_01). So either there's a bug in the spec or there's a bug in glibc.

That link is POSIX, not the C standard. Indeed `exit` is not thread-unsafe; rather it just explicitly has undefined behavior if called more than once. POSIX copies the text from the C standard on this:

> If exit() is called more than once, the behavior is undefined.

This is very unfortunate and almost certainly an error carried over from before C had threads, where the only way `exit` could have come to be called "more than once" is recursively via an `atexit` handler.

We should work to get this fixed at least in POSIX and ideally in the baseline C standard too.


## Comment 2240581199

other (CONTRIBUTOR) · DemiMarie · 2024-07-19T23:10:41Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2240581199

> > As far as I understand it, according to the C specification `exit` is thread safe because it's not on the list of exceptions to thread-safety (https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_09_01). So either there's a bug in the spec or there's a bug in glibc.
> 
> That link is POSIX, not the C standard. Indeed `exit` is not thread-unsafe; rather it just explicitly has undefined behavior if called more than once. POSIX copies the text from the C standard on this:
> 
> > If exit() is called more than once, the behavior is undefined.
> 
> This is very unfortunate and almost certainly an error carried over from before C had threads, where the only way `exit` could have come to be called "more than once" is recursively via an `atexit` handler.
> 
> We should work to get this fixed at least in POSIX and ideally in the baseline C standard too.

Does this mean that concurrent calls to `exit()` do _not_ cause undefined behavior in musl, or at least that you would consider it to be a bug if they do?

## Comment 2243633798

maintainer (MEMBER) · RalfJung · 2024-07-22T19:08:19Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2243633798

I have filed this as an issue with POSIX: https://austingroupbugs.net/view.php?id=1845. Ultimately this will probably have to go via C itself, but I won't pursue that path.

## Comment 2252661685

other (NONE) · codonell · 2024-07-26T12:29:12Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2252661685

@RalfJung I've commented on the POSIX issue and I agree with Rich's wording, and from glibc's perspective I think we need to improve the situation. The bigger question will be how far we can take some of the changes and seeing the impact on the larger body of existing code. Thanks for moving this forward.

## Comment 2252680516

maintainer (MEMBER) · RalfJung · 2024-07-26T12:40:07Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2252680516

Overall there's three external threads now that I am aware of:
- glibc: https://sourceware.org/bugzilla/show_bug.cgi?id=31997
- POSIX: https://austingroupbugs.net/view.php?id=1845
- libc-coord: https://www.openwall.com/lists/libc-coord/2024/07/24/4

@codonell happy to hear that glibc is willing to make exit thread-safe! In Rust we now have our own lock doing basically exactly what the [proposed glibc patch](https://sourceware.org/pipermail/libc-alpha/2024-July/158579.html) would do, but of course it would be better to have this in glibc so that e.g. concurrent calls from a mixed C-Rust binary are working properly.

(I didn't realize "dalias" is Rich. ;)

## Comment 2254573726

other (CONTRIBUTOR) · lolbinarycat · 2024-07-28T16:31:10Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2254573726

> This is definitely the wrong way to go, we just finished the fight with set_var, let's not repeat it.

`set_vat` *does* use a lock though, it's just that lock was deemed insufficient.


## Comment 2256029734

other (NONE) · codonell · 2024-07-29T14:00:54Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2256029734

@RalfJung 100%, we need to do this right, concurrency issues in C need to fixed, we need to be able to parallelize safely to take advantage of modern hardware.

## Comment 2299899664

other (NONE) · nicowilliams · 2024-08-20T22:59:13Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2299899664

I've seen crashes in MIT Kerberos libraries due to `assert()`s in MIT Kerberos that trip because of unloading of loaded shared objects at `exit()` time.  This is because one of the things that happens at `exit()` time is the unloading (as if by last `dlclose()`) of shared objects that have only one reference.  (One can leak shared object handles to prevent those objects being unloaded at exit time, but don't.)  In each case that I've seen this the fix turned out to be to make all worker threads exit first.

Notice that locking in or around `exit()` cannot help: as long as other threads are still active then the process' death can cause them to do bad things.  For example, in a database application/library an `exit()` could cause worker threads that die uncleanly to leave the database in an unclean state -- sure, the DB should be designed with power failures in mind and should be able to recover on startup, but this is a general problem that can only be avoided by _programmers_ or by the programming language providing a way to cleanly shut down threads at `exit()` time.

Every threaded program or library must shutdown its worker threads before `exit()`ing.  Threaded libraries need to provide an API to shut down their worker threads.  Though there is no need if the program is only expected to exit by signal or halt or power failure.

For emergencies, of course, do `_exit()` (and if not in signal handlers or `fork()` children then maybe also flush `stdout`/`stderr`), as at least that will not crash with double-frees or whatever other pathologies.

All of this applies to _all_ programming languages regardless of whether they use the C run-time.  Either `exit()` or equivalent _is_ unsafe and must be documented as such, or the language and its run-time must provide a way to automatically cleanly shut down threads at exit time.

## Comment 2299915350

other (NONE) · richfelker · 2024-08-20T23:16:53Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2299915350

I largely don't disagree with @nicowilliams that, in general, multithreaded programs may need logic to coordinate `exit` such that it's not particularly meaningful for helpful for `exit` itself to be thread-safe. However, this is specific to what the actual program and its threads are doing, and does not always apply. Moreover, one way of achieving such coordination is with an `atexit` handler that calls `pthread_cancel` on any outstanding threads that may have cleanup work to do and waits to join them. If you take that approach, thread-safety for `exit` makes sense. And if you do not have threads managing any state that needs to be preserved, then just letting them terminate asynchronously with the process is fine.


## Comment 2301187682

maintainer (MEMBER) · RalfJung · 2024-08-21T05:53:43Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2301187682

> For example, in a database application/library an exit() could cause worker threads that die uncleanly to leave the database in an unclean state -- sure, the DB should be designed with power failures in mind and should be able to recover on startup, but this is a general problem that can only be avoided by programmers or by the programming language providing a way to cleanly shut down threads at exit() time.

This seems incoherent to me. Indeed a thread talking to a database bust be resilient to SIGKILL and power failure, e.g. using database transasctions if more than on query need to be executed either all together or none at all. So assuming the program is written like that, why isn't it okay to also rudely kill the thread in the same way on process exit?

There's a reason some people are advocating "crash-only software" -- all software must be written in a way that crashes do not corrupt persistent state, and then if crashes are a way to stop the software in a way that leaves the global state consistent, we can just make this the only and expected way to stop the software. That has the huge advantage that the crash code paths get exercises a lot more than they would otherwise, which also makes them a lot more likely to actually behave as intended.

## Comment 2302497872

other (NONE) · nicowilliams · 2024-08-21T16:25:58Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302497872

[Responding a bit out of order.]

> I largely don't disagree with @nicowilliams that, in general, multithreaded programs may need logic to coordinate `exit` such that it's not particularly meaningful for helpful for `exit` itself to be thread-safe.

`exit()` _cannot_ be thread-safe because the _cleanup_ that it does can cause other threads to crash.  Just merely the shared object unloading is enough.  `exit()` could only be thread-safe if it did no cleanup (other than `fflush(stdout)` and `fflush(stderr)`), but since `atexit()`/`onexit()` exist, `exit()` cannot be thread-safe.

`_exit()` is thread-safe in a sense, but since the other threads are killed in the middle of who knows what, it's really only safe is the code the process is running is able to recover from crashes.  Of course, we should all only write code that can recover safely from crashes and power failures...

> However, this is specific to what the actual program and its threads are doing, and does not always apply.

It does always apply, _unless_ you mean never to `exit()` :)

> And if you do not have threads managing any state that needs to be preserved, then just letting them terminate asynchronously with the process is fine.

It's probably fair to assume that the caller of `exit()` is the program.  It's also more than fair to assume that the program and the libraries it uses cannot know whether the other libraries are going to have threads that can be killed safely.

The bottom-line is that all libraries should provide a shutdown function that can be used in an `atexit()` handler _or_ they should just register `atexit()` handlers to call their internal shutdown functions.  Shutdown here means: kill their thread pools under a lock so that `atexit()` handlers do not continue to execute, and hope that no `atexit()` handler running ahead of theirs will cause a crash.  I do believe that shared object unloading comes after the `atexit()` handlers, because the inverse wouldn't make sense, as long as application- and library-supplied handlers don't themselves call `dlclose()` without first exiting their threads.

> Moreover, one way of achieving such coordination is with an `atexit` handler that calls `pthread_cancel` on any outstanding threads that may have cleanup work to do and waits to join them. If you take that approach, thread-safety for `exit` makes sense. And if you do not have threads managing any state that needs to be preserved, then just letting them terminate asynchronously with the process is fine.

There's several problems with this approach:

1) You can't force `atexit()` handler invocation order, so you can't make sure that the handler that cancels all other threads runs before any handler that could crash the process.

2) Making your code cancel-safe is not easy.

   I think of `pthread_cancel()` as a method for interrupting CPU-bound threads, because if they are not CPU-bound then they can use async I/O mechanisms for detecting the need to exit (e.g., a `pthread_cond_signal()` or broadcast on a condition variable, a "broadcast" on an event port/kqueue/epoll/whatever, messages on self-pipes -- whatever can wake your threads into their event loops so they can discover the need to exit and then exit.

   Whereas CPU-bound threads by definition may not be able to respond to exit-required conditions in a timely manner.  If you have a program doing a very expensive computation, you don't want to burden that with extra branches and memory accesses to check a global do-exit sentinel.  `pthread_cancel()` is perfect for this, and the thread can use `pthread_cleanup_push()`/`pthread_cleanup_pop()` to cleanup safely if it has to.

3) If you started detached threads you'll never be able to know when they have exited unless you took steps like making them atomically decrement a live thread count (_and_ signal the thread that wants to `exit()` on a condvar or similar, unless you want to poll).

## Comment 2302519320

other (NONE) · nicowilliams · 2024-08-21T16:37:09Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302519320

> This seems incoherent to me. Indeed a thread talking to a database bust be resilient to SIGKILL and power failure, e.g. using database transasctions if more than on query need to be executed either all together or none at all. So assuming the program is written like that, why isn't it okay to also rudely kill the thread in the same way on process exit?

It _is_ ok to kill them rudely IFF you can assume that the code they run can recover safely from crashes.

What's not ok is to do things that cause the process to _crash_ as opposed to die uncleanly.  A crash comes with a core dump, and it's disruptive because the user may need to investigate why it happened.  Ask me how I know...  Or just let me tell you how I know: when the crashes in MIT Kerberos library assertions have happened to my users I've had to go investigate.  Sure, those crashes were mostly harmless, but I still had to investigate, and that was a) disruptive to my users, b) disruptive to me.  The apps and libraries in question didn't have to shut down cleanly, but dropping cores was not acceptable.

But if you have a modern program with 200+ direct and indirect dependencies, how can you assume that it's safe to `_exit()` without cleaning up?  Will you inspect the documentation for all those dependencies?

It would be better if the program's direct dependencies all either:

 - provide a shutdown function

or

 - add their shutdown function as an `atexit()` handler (and that function should take and hold a lock during shutdown, naturally).

The latter is infinitely easier on developers.

But _Rust_ can't ensure that libraries and programs shutdown safely at `exit()` time, therefore `exit()` is inherently unsafe.

But also you can't really stop the process calling `exit()` -- it has to be able to exit!!  So I think this issue is a bit much-ado-about-nothing-one-can-do-much-about.  Just document the problem and encourage developers to use `atexit()` correctly.

> There's a reason some people are advocating "crash-only software" -- all software must be written in a way that crashes do not corrupt persistent state, and then if crashes are a way to stop the software in a way that leaves the global state consistent, we can just make this the only and expected way to stop the software. That has the huge advantage that the crash code paths get exercises a lot more than they would otherwise, which also makes them a lot more likely to actually behave as intended.

I also advocate crash-only software.  But again, there is a big difference between "just kill all the threads but still exit with status code zero" and "oops, here's a `SIGSEGV` or a `SIGBUS` and a core dump, good luck figuring out if you have to worry about this or not!!".

Crashing to exit is fine; dumping core to exit is not just not fine, it's not acceptable.

To reliably avoid dumping core at exit time you need developers to use `atexit()` correctly.

## Comment 2302522166

maintainer (MEMBER) · RalfJung · 2024-08-21T16:38:39Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302522166

I would say that a library that has threads that cannot be killed safely (killed together with the entire process - this is quite different from killing an individual thread) is buggy. That is also the position at least one libs-api team member took above.

This is not an outlandish position - Java, C#, Python and many other languages let their users safely do a process exit at any moment, thus assuming that if C code was running in other threads in this process, it is safe to kill.

## Comment 2302531388

other (NONE) · richfelker · 2024-08-21T16:43:55Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302531388

> But if you have a modern program with 200+ direct and indirect dependencies

That's not "modern", it's just bad. If you want to argue about the constraints of trying to make bad software vaguely usable, that's fine, but it's not applicable to software that's not doing awful things like that and you can't just assume everyone is going to do that just because it's what an utterly mismanaged and incompetent industry considers "modern". It's meaningful to have safety guarantees, invariants, etc. that well-engineered programs whose code the developers fully understand and take responsibility for can benefit from, even if not all or even not most programs will be of that sort.


## Comment 2302534214

maintainer (MEMBER) · RalfJung · 2024-08-21T16:45:33Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302534214

That point about an implicit `dlclose` on `exit` is new to me and highly concerning. dlclose itself is an extremely unsafe operation (Cc https://github.com/rust-lang/unsafe-code-guidelines/issues/526). I was not able to find documentation about this in the dlclose or exit man pages -- do you have any references for this? To me this sounds like a very buggy libc, if it just unloads a shared object *while other threads are still running*, including possibly threads inside that shared object.

EDIT: to reply to your message below, since we raced:
> Your thread can be trying to execute the next instruction and suddenly the memory where that instruction should have been has been unmapped (because the shared object containing it was unloaded by exit() before it got to _exit() and also before your thread got to the next instruction), and now you have a SIGBUS and dump core.

I don't see how that's not a buggy libc. How can a libc possibly justify just unloading shared objects while there is still code running?!?

It is obviously UB to call `dlclose` while there's still any code running in the library being closed. If libc calls `dlclose` by itself, it is up to libc to ensure that this is safe.

## Comment 2302536120

other (NONE) · nicowilliams · 2024-08-21T16:46:42Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302536120

> I would say that a library that has threads that cannot be killed safely (killed together with the entire process - this is quite different from killing an individual thread) is buggy. That is also the position at least one libs-api team member took above.

Your thread can be trying to execute the next instruction and suddenly the memory where that instruction should have been has been unmapped (because the shared object containing it was unloaded by `exit()` before it got to `_exit()` and also before your thread got to the next instruction), and now you have a `SIGBUS` and dump core.

The only correct fix I know of is to have that library set up an `atexit()` handler so that it can cause all its threads to exit (or cancel them, if that is safe for that library).

> This is not an outlandish position - Java, C#, Python and many other languages let their users safely do a process exit at any moment, thus assuming that if C code was running in other threads in this process, it is safe to kill.

The MIT Kerberos assertion tripping I described happened in C code running in a Java program via JNI.

Seriously, this problem is 100% language-agnostic.

Every programming language will have this problem unless it natively ensures that its `exit()`-like mechanism cannot cause core dumps, but the moment you have an FFI escape to other languages you can no longer enforce that and once again exiting is unsafe.  Or a language could ensure that when exit time comes all threads will exit before any unknown exit handling can cause a core dump, and to do this the language might need to allow developers to set up handlers for "exceptions" or "signals" or "panics" or whatever the language wants to use to represent an asynchronous exit request.

## Comment 2302538783

other (NONE) · nicowilliams · 2024-08-21T16:48:04Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302538783

> > But if you have a modern program with 200+ direct and indirect dependencies
> 
> That's not "modern", it's just bad.

From your lips to developers ears.  It's not a good practice, but it is incredibly common.  I see this in C++, Rust, Java, and Python every day.  It is a reality.

## Comment 2302549533

maintainer (MEMBER) · RalfJung · 2024-08-21T16:53:53Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302549533

Let's please not debate whether 200 dependencies is modern or bad or whatever. Rust is designed to provide safety in a compositional way, where the safety of a 200-component-program directly follows from the safety of each of its pieces. This requires a coherent safety contract that every component agrees on: either all threads may be canceled by process kill any moment, or no part of the system may just call `exit` (including implicitly by returning from `main`). A choice must be made here.

Since it seems bizarre to associate a safety requirement with returning from `main`, my position is that the only reasonable choice is: libraries must tolerate process exit at any moment. If the ecosystem doesn't provide this today, then we should work towards providing this.

Or we can just throw up our hands in despair and declare that it is impossible to improve the state of the art of the industry, I guess.

## Comment 2302558235

other (NONE) · nicowilliams · 2024-08-21T16:58:46Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302558235

> That point about an implicit `dlclose` on `exit` is new to me and highly concerning. dlclose itself is an extremely unsafe operation (Cc [rust-lang/unsafe-code-guidelines#526](https://github.com/rust-lang/unsafe-code-guidelines/issues/526)). I was not able to find documentation about this in the dlclose or exit man pages -- do you have any references for this? To me this sounds like a very buggy libc, if it just unloads a shared object _while other threads are still running_, including possibly threads inside that shared object.

Even if that doesn't/didn't happen, MIT Kerberos has shared object destructors (`.fini`) that run at exit time (because they _are_ `.fini`) to clean up its resources, and among those cleanup tasks it destroys mutexes, and that's what the assertions that trip do: assert that mutex functions succeed, but since the locks have been destroyed they fail.

> EDIT: to reply to your message below, since we raced:
> 
> > Your thread can be trying to execute the next instruction and suddenly the memory where that instruction should have been has been unmapped (because the shared object containing it was unloaded by exit() before it got to _exit() and also before your thread got to the next instruction), and now you have a SIGBUS and dump core.
> 
> I don't see how that's not a buggy libc. How can a libc possibly justify just unload shared objects while there is still code running?!?

I definitely justifies calling the shared objects' `.fini` destructors -- this is a) documented, b) kinda the point of `.fini` destructors.  Yes, one should use `atexit()` handles instead of `.fini` destructors, but `.fini` is the only way to detect possibly-non-exit-time unloading of shared objects.

I know this is all very rude seeming, but really, `exit()`ing is only safe if all thread-spawning code in the process sets `atexit()` handlers (or provides shutdown functions that can be called from the caller's `atexit()` handlers) to prevent all of this.

Note BTW that C++ has `atexit()`, naturally, Java has `Runtime.getRuntime().addShutdownHook()`, Python has `atexit.register()`, Go has `defer` (not great; but see https://pkg.go.dev/github.com/tebeka/atexit).  Rust doesn't seem to have a native form of `atexit()`, but since you can write and call C functions in Rust you can always just use the C `atexit()` and be done.

## Comment 2302570823

other (CONTRIBUTOR) · comex · 2024-08-21T17:05:49Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302570823

> Even if that doesn't/didn't happen, MIT Kerberos has shared object destructors (`.fini`) that run at exit time (because they _are_ `.fini`) to clean up its resources, and among those cleanup tasks it destroys mutexes, and that's what the assertions that trip do: assert that mutex functions succeed, but since the locks have been destroyed they fail.

These are similar to C++ global destructors, discussed earlier in this thread.  They are a real problem, but not quite as bad as the dynamic linker just unmapping code (which isn't something I've heard of).


## Comment 2302572842

other (NONE) · richfelker · 2024-08-21T17:07:00Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302572842

> Let's please not debate whether 200 dependencies is modern or bad or whatever. Rust is designed to provide safety in a compositional way, where the safety of a 200-component-program directly follows from the safety of each of its pieces

I don't think we need to discuss whether it's bad, but "programs which do not have 200 dependencies" (or even 5 dependencies) are a completely valid usage case for a language, and having safety guarantees or invariants that are useful to them is meaningful, even if it might not be useful to some 200-dependency monstrosity.

That being said, the whole "compositional safety" theory is rather bollocks. Sure, you can have compositional memory-safety, thread-safety, etc. in the way you describe, but you do not get *semantic* safety compositionally, because that depends on actual human beings' intents being aligned with what the code actually does, which quickly becomes impossible to guarantee as soon as the number of composed components with different authorships starts to get large.


## Comment 2302573692

other (NONE) · nicowilliams · 2024-08-21T17:07:31Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302573692

> Let's please not debate whether 200 dependencies is modern or bad or whatever.

+1.  I only mentioned it to point out that there is no safe way for a developer to know if calling `exit()` (or returning from main, as you point out) unless it's widely understood and accepted that programs and libraries must use `atexit()` (or similar) to make it safe.  Having more than a handful of dependencies makes it impractical to inspect them all for this, so it just has to be that a) the Rust docs tell you to use `atexit()` judiciously to make `exit()` safe, b) Rust libraries and programs -and their developers- do just that -- a social contract if you wish.

> Rust is designed to provide safety in a compositional way, where the safety of a 200-component-program directly follows from the safety of each of its pieces. This requires a coherent safety contract that every component agrees on: either all threads may be canceled by process kill any moment, or no part of the system may just call `exit` (including implicitly by returning from `main`). A choice must be made here.

Banning `exit()` will definitely not be satisfying.

And making asynchronous exit safe w/o `atexit()` is just not feasible.

But there is third way: a) provide an `atexit()` in Rust, b) every Rust program and every Rust library that needs special exit-time handling (to make exiting safe) _must_ use `atexit()` (or whatever Rust wants to call it).

> Since it seems bizarre to associate a safety requirement with returning from `main`, my position is that the only reasonable choice is: libraries must tolerate process exit at any moment. If the ecosystem doesn't provide this today, then we should work towards providing this. Or we can just throw up our hands in despair and declare that it is impossible to improve the state of the art of the industry, I guess.

This is only feasible if Rust provides an `atexit()` and developers are told to use it.  There is no need to despair.  What works for C, C++, Java, and Python _will_ work for Rust.  This problem is language-agnostic, and the solution (`atexit()` and judicious use of it) is _also_ language-agnostic.

Rust simply _must_ adopt this well-known, universal, and language-agnostic solution.



## Comment 2302576668

other (NONE) · nicowilliams · 2024-08-21T17:09:19Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302576668

> > Even if that doesn't/didn't happen, MIT Kerberos has shared object destructors (`.fini`) that run at exit time (because they _are_ `.fini`) to clean up its resources, and among those cleanup tasks it destroys mutexes, and that's what the assertions that trip do: assert that mutex functions succeed, but since the locks have been destroyed they fail.
> 
> These are similar to C++ global destructors, discussed earlier in this thread. They are a real problem, but not quite as bad as the dynamic linker just unmapping code (which isn't something I've heard of).

They are a real enough problem (I've seen it happen repeatedly, with disparate libraries).  It's enough that the Rust community must accept that it needs an `atexit()`, and it must accept that Rust developers must be told to use `atexit()` when it's needed (and to recognize how to know when it's needed).

## Comment 2302577817

other (NONE) · richfelker · 2024-08-21T17:10:01Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302577817

> Even if that doesn't/didn't happen, MIT Kerberos has shared object destructors (`.fini`) that run at exit time (because they _are_ `.fini`) to clean up its resources, and among those cleanup tasks it destroys mutexes, and that's what the assertions that trip do: assert that mutex functions succeed, but since the locks have been destroyed they fail.

Destroying this kind of singleton is just a programming error (lifetime error). The correct way to make this kind of thing safe is for the dtor (or equivalent) to take a lock on the object and never release it, not to destroy the lock and object it protects. This ensures that there is never an inconsistent state at exit, since no thread but the exiting one is entitled to modify the protected object.


## Comment 2302588650

maintainer (MEMBER) · the8472 · 2024-08-21T17:16:19Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302588650

>> That point about an implicit dlclose on exit is new to me and highly concerning. dlclose itself is an extremely unsafe operation [...]

> Even if that doesn't/didn't happen, MIT Kerberos has shared object destructors (.fini) that run at exit time (because they are .fini) to clean up its resources [...]

Checking, is this a retraction/correction of a previous comment? Is it libraries themselves that run dlclose in atexit? Or is it not dlclose but destructors after all? In those cases that would not be a problem for Rust-C interop but only for Rust interoperating with those specific libraries.

If we can make exit()/atexit() safe *in principle* that would already be a huge step forward, even if individual C libraries then set things on fire again, but that can't be helped, they can do that in a thousand ways.

## Comment 2302600100

other (CONTRIBUTOR) · comex · 2024-08-21T17:23:25Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302600100

> That being said, the whole "compositional safety" theory is rather bollocks. Sure, you can have compositional memory-safety, thread-safety, etc. in the way you describe, but you do not get _semantic_ safety compositionally, because that depends on actual human beings' intents being aligned with what the code actually does, which quickly becomes impossible to guarantee as soon as the number of composed components with different authorships starts to get large.

One of the core motivating ideas of Rust is that not all bugs are created equal.  On average, bugs that violate memory safety are much more likely to result in exploitable vulnerabilities.  From that perspective, what you're describing actually sounds like a pretty good deal.  Not perfect, but better than the alternative of no safety.

## Comment 2302605633

other (NONE) · nicowilliams · 2024-08-21T17:26:44Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302605633

> > > That point about an implicit dlclose on exit is new to me and highly concerning. dlclose itself is an extremely unsafe operation [...]
> 
> > Even if that doesn't/didn't happen, MIT Kerberos has shared object destructors (.fini) that run at exit time (because they are .fini) to clean up its resources [...]
> 
> Checking, is this a retraction/correction of a previous comment? Is it libraries themselves that run dlclose in atexit? Or is it not dlclose but destructors after all? In those cases that would not be a problem for Rust-C interop but only for Rust interoperating with those specific libraries.

I think the unload-at-exit-time thing was a mistake, though it does happen when libraries `dlclose()` when cleaning up (which is why I misremembered).  So a correction.  This is instructive: https://wiki.musl-libc.org/functional-differences-from-glibc.html#Unloading-libraries (Musl libc never unloads shared objects, but _does_ call their destructors at exit time).

> If we can make exit()/atexit() safe _in principle_ that would already be a huge step forward, [...]

You absolutely can make `exit()` safe IFF you provide `atexit()` _and_ developers make use of `atexit()`.  Every major language has been down this path before.

> [...] even if individual C libraries then set things on fire again, but that can't be helped, they can do that in a thousand ways.

Not just C.  Even Rust libraries could cause crashes at exit time if they need-to-but-don't use `atexit()`.

## Comment 2302624800

other (NONE) · nicowilliams · 2024-08-21T17:38:29Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302624800

Checking glibc sources I see that `exit()` [takes a lock while processing the `atexit()` handlers, but drops it while calling each handler so that new handlers can be added while exiting](https://sourceware.org/git/?p=glibc.git;a=blob;f=stdlib/cxa_finalize.c;h=496141d80218bd5f3284a7d316436397f0c22937;hb=HEAD#l48):

```C
  25 /* If D is non-NULL, call all functions registered with `__cxa_atexit'
  26    with the same dso handle.  Otherwise, if D is NULL, call all of the
  27    registered handlers.
  28 
  29    A __cxa_finalize function is declared in the libstdc++ <cxxabi.h>
  30    header, and the libstdc++ implementation calls this function.  GCC
  31    calls the glibc variant directly from its CRT files, from an ELF
  32    destructor.  this call always passes a non-null D argument.  In the
  33    current implementation, the GCC-provided __cxa_finalize call is
  34    responsible for removing the registered __cxa_atexit (C++)
  35    destructors of an object that is undergoing dlclose.  Note that
  36    this is specific to dlclose.  During process termination, glibc
  37    invokes the __run_exit_handlers, which calls registered
  38    __cxa_atexit (C++) destructors in reverse registration order,
  39    across all objects.  The subsequent GCC-provided __cxa_finalize
  40    calls (which are ordered according to ELF object dependencies, not
  41    __cxa_atexit call order, and group destructor calls per object
  42    during dlclose) do not result in further destructor invocations.  */
  43 void
  44 __cxa_finalize (void *d)
  45 {
  46   struct exit_function_list *funcs;
  47 
  48   __libc_lock_lock (__exit_funcs_lock);
  49 
...
  95             /* Unlock the list while we call a foreign function.  */
  96             __libc_lock_unlock (__exit_funcs_lock);
  97             cxafn (cxaarg, 0);
  98             __libc_lock_lock (__exit_funcs_lock);
  99 
 100             /* It is possible that that last exit function registered
 101                more exit functions.  Start the loop over.  */
 102             if (__glibc_unlikely (check != __new_exitfn_called))
 103               goto restart;
 104           }
```

All the commentary there is worth reading:

```C
  62             /* We don't want to run this cleanup more than once.  The Itanium
  63                C++ ABI requires that multiple calls to __cxa_finalize not
  64                result in calling termination functions more than once.  One
  65                potential scenario where that could happen is with a concurrent
  66                dlclose and exit, where the running dlclose must at some point
  67                release the list lock, an exiting thread may acquire it, and
  68                without setting flavor to ef_free, might re-run this destructor
  69                which could result in undefined behaviour.  Therefore we must
  70                set flavor to ef_free to avoid calling this destructor again.
  71                Note that the concurrent exit must also take the dynamic loader
  72                lock (for library finalizer processing) and therefore will
  73                block while dlclose completes the processing of any in-progress
  74                exit functions. Lastly, once we release the list lock for the
  75                entry marked ef_free, we must not read from that entry again
  76                since it may have been reused by the time we take the list lock
  77                again.  Lastly the detection of new registered exit functions is
  78                based on a monotonically incrementing counter, and there is an
  79                ABA if between the unlock to run the exit function and the
  80                re-lock after completion the user registers 2^64 exit functions,
  81                the implementation will not detect this and continue without
  82                executing any more functions.
  83 
  84                One minor issue remains: A registered exit function that is in
  85                progress by a call to dlclose() may not completely finish before
  86                the next registered exit function is run. This may, according to
  87                some readings of POSIX violate the requirement that functions
  88                run in effective LIFO order.  This should probably be fixed in a
  89                future implementation to ensure the functions do not run in
  90                parallel.  */
```

## Comment 2302637802

maintainer (MEMBER) · the8472 · 2024-08-21T17:46:20Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302637802

> You absolutely can make exit() safe IFF you provide atexit() and developers make use of atexit().

> And making asynchronous exit safe w/o atexit() is just not feasible.

Can you elaborate why you think it's a *strict necessity*? ISTM what's really necessary is for exit handlers used by libraries to be thread-safe, i.e. the handlers running must not render other threads unsound.
That confines the safety reasoning to the libraries making use of the handlers, rather imposing a burden on everyone.

> Checking glibc sources I see that exit() takes a lock while processing the atexit() handlers, but drops it while calling each handler so that new handlers can be added while exiting

Yes, this has been discussed upthread already and an issue has been filed.

## Comment 2302668950

other (CONTRIBUTOR) · comex · 2024-08-21T18:04:22Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302668950

> They are a real enough problem (I've seen it happen repeatedly, with disparate libraries). It's enough that the Rust community must accept that it needs an `atexit()`, and it must accept that Rust developers must be told to use `atexit()` when it's needed (and to recognize how to know when it's needed).

Perhaps that is the only path forward.  But for it to achieve Rust's compositional safety goals, there are two limitations:

1. Safe code cannot be required to call `atexit` or anything else for memory safety.

2. Safe code cannot be required to shut down other threads before exiting, even if it created them itself.

Therefore, if a particular C library has problematic global destructors, and is used by Rust code, then:

1. The responsibility to call `atexit` falls on whatever crate is attempting to wrap the underlying unsafe C APIs in a safe Rust API.  It doesn't fall on that crate's clients.

2. The crate's `atexit` handler must do *two* different things:
   a. The handler must shut down any threads created by the C library itself.  This would be done using APIs provided by the library.
   b. Since the handler can't prevent arbitrary other application threads from continuing to exist and continuing to run arbitrary safe Rust code, the handler must somehow block off further access to the C library from safe Rust.  That could be done, say, by having a global `RwLock`, adding a read lock around every call into C in the crate, and then having the `atexit` handler take an exclusive lock and leak it.  (In practice you would probably want an approach with better UX, but that's the basic idea.)

The main problem is that nobody will want to do 2b. because it adds runtime cost to every API call.  Oh well, I guess?

Sidenote:

> To reliably avoid dumping core at exit time you need developers to use `atexit()` correctly.

> The correct way to make this kind of thing safe is for the dtor (or equivalent) to take a lock on the object and never release it, not to destroy the lock and object it protects.

I still wish we didn't have to advocate an approach that fundamentally breaks dynamic unloading.  C libraries that support dynamic unloading ought to create a mechanism to have destructors run during `dlclose` but not at process exit.

## Comment 2302805255

other (NONE) · nicowilliams · 2024-08-21T19:09:29Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302805255

> > And making asynchronous exit safe w/o atexit() is just not feasible.
> 
> Can you elaborate why you think it's a _strict necessity_? ISTM what's really necessary is for exit handlers used by libraries to be thread-safe, i.e. the handlers running must not render other threads unsound. That confines the safety reasoning to the libraries making use of the handlers, rather imposing a burden on everyone.

You're accepting the premise when you say that "exit handlers used by libraries to be thread-safe" is what should be necessary.

BTW, glibc calls each handler no more than once.

> > Checking glibc sources I see that exit() takes a lock while processing the atexit() handlers, but drops it while calling each handler so that new handlers can be added while exiting
> 
> Yes, this has been discussed upthread already and an issue has been filed.

glibc does ensure that no handler is called more than once, but not holding _some_ lock here does mean that glibc cannot enforce LIFO handler execution order like POSIX says it must.  (glibc can't hold _this_ lock because it wants to allow `atexit()` concurrent with `exit()`.

## Comment 2302840223

other (NONE) · nicowilliams · 2024-08-21T19:18:14Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302840223

> Perhaps that is the only path forward. But for it to achieve Rust's compositional safety goals, there are two limitations:
> 
>     1. Safe code cannot be required to call `atexit` or anything else for memory safety.
> 
>     2. Safe code cannot be required to shut down other threads before exiting, even if it created them itself.

What causes (1)?

Why can't safe code send a message to its threads to tell them to exit (2)?

> I still wish we didn't have to advocate an approach that fundamentally breaks dynamic unloading. C libraries that support dynamic unloading ought to create a mechanism to have destructors run during `dlclose` but not at process exit.

I personally think that insisting on full cleanup at exit time is a fetish.  Long long ago I had to deal with a program that hit a knee and what used to take minutes suddenly took hours, and it as because it was freeing a very large data structure in memory almost all of which had been paged out, and the fix was (besides buying more RAM) to not do that, just exit.

However, that does not mean that no cleanup should ever be needed at exit time.  Consider a program that reads a password by turning off echo mode, but you interrupt it and now echo mode is off in your terminal -- that sucks, and it's why such programs try hard to restore the tty's modes if interrupted.  There are lots of cleanup actions of this sort that really should be done, and there are lots of cleanup actions that really should be elided -- developers have to know the difference.  For example, the MIT Kerberos library code should really not destroy mutexes in its destructors -- there is zero value in doing so, and it only ever causes pain!  (@greghudson).

Perhaps Rust could try not calling the C `exit()`, only `_exit()`, though I am pretty sure that you'll find that unsatisfactory.

## Comment 2302878262

other (NONE) · nicowilliams · 2024-08-21T19:39:20Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302878262

> > As far as I understand it, according to the C specification `exit` is thread safe because it's not on the list of exceptions to thread-safety (https://pubs.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_09_01). So either there's a bug in the spec or there's a bug in glibc.
> 
> That link is POSIX, not the C standard. Indeed `exit` is not thread-unsafe; rather it just explicitly has undefined behavior if called more than once. POSIX copies the text from the C standard on this:
> 
> > If exit() is called more than once, the behavior is undefined.
> 
> This is very unfortunate and almost certainly an error carried over from before C had threads, where the only way `exit` could have come to be called "more than once" is recursively via an `atexit` handler.
> 
> We should work to get this fixed at least in POSIX and ideally in the baseline C standard too.

Reminds me of how some implementations tried to stop all threads in the calling process in `vfork()` because the pre-threading docs said that `vfork()` stops the parent.  Very sad.

It should be pretty easy for the C library to make the second, third, .., nth calls to `exit()` just wait for a lock that will never be dropped.

## Comment 2302885177

maintainer (MEMBER) · the8472 · 2024-08-21T19:43:43Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302885177

> What causes (1)?

This is a general principle in Rust. Memory safety must not depend on safe code doing the right thing. If some code is not unconditionally memory-safe then it must be marked as `unsafe fn`, the preconditions must be documented and it is upon the caller (using an `unsafe {}` block) to only call that code if the preconditions are upheld.

The rest in comex' post follows from that.

## Comment 2302885758

other (NONE) · nicowilliams · 2024-08-21T19:44:03Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302885758

> 2\. Safe code cannot be required to shut down other threads before exiting, even if it created them itself.

Oh, because you can share objects on the stack between threads?  Right, yeah, so don't exit the threads, just quiesce them -- make them block until the exit completes.

## Comment 2302896371

other (NONE) · nicowilliams · 2024-08-21T19:50:16Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2302896371

> > What causes (1)?
> 
> This is a general principle in Rust. Memory safety must not depend on safe code doing the right thing. If some code is not unconditionally memory-safe then it must be marked as `unsafe fn`, the preconditions must be documented and it is upon the caller (using an `unsafe {}` block) to only call that code if the preconditions are upheld.
> 
> The rest in comex' post follows from that.

I think (2) comes from the ability to safely share objects on the stack, not from (1), and it has a solution (see above).

I'm not sure you can avoid compromising on (1) for just this one thing.  If you won't require `atexit()` usage then IMO you can't allow `exit()` then you must allow/use `_exit()`, and that will be surprising and unsatisfactory in other ways.  Choose your poison.

And how can you stop ffi C code from calling `exit()`?  Well, hopefully there's no need.

## Comment 2303005502

other (CONTRIBUTOR) · comex · 2024-08-21T21:00:57Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2303005502

> > 2. Safe code cannot be required to shut down other threads before exiting, even if it created them itself.
> 
> Oh, because you can share objects on the stack between threads? Right, yeah, so don't exit the threads, just quiesce them -- make them block until the exit completes.

This is a tricky point.  In principle it could be a reasonable strategy to add some kind of check that all Rust-created threads are quiescent or dead.  Either Rust's `std::process::exit` could perform the check before calling into libc's `exit`, or the check could be done by an atexit handler.  But in practice there are significant difficulties:

- Non-Rust code is allowed to create its own threads and call into Rust code.  (I brought this up earlier in the thread.)  So there may be threads in the process that libstd knows nothing about, yet are currently running safe Rust code.

  Now, because every call from non-Rust into Rust is inherently unsafe, you could theoretically solve this by declaring that every time Rust code defines an `extern "C"` function or callback, that function is responsible for ensuring that neither it nor anything it calls (recursively) is ever going to call into `std::process::exit`.  But that sounds impractical and, well, non-compositional.  It would also be a backwards-incompatible requirement to graft onto existing unsafe Rust code.  To be fair, my suggestion about FFI crates using locks is also backwards-incompatible, but at least it is a bit narrower in scope.

- Even when libstd knows about a thread, how would it quiesce or kill it?  Rust doesn't have a heavyweight runtime like Java; the libstd thread APIs are just wrappers for native thread APIs, mainly pthreads.  So there's no portable way to reach in and pause another thread.

  You could use `pthread_cancel`, but that is likely to end badly.  Most code is not cancel-safe, and yes, there are memory safety issues that arise if stacks get unexpectedly freed.
 
  You could have some kind of Rust-specific cancellation signal that all standard library I/O and concurrency operations check for.  But the thread being quiesced might not perform any I/O or concurrency operations (or it might do so without going through the standard library).

  You could use `pthread_kill` with a signal handler.  But first of all, while registering a global signal handler might be feasible when building an executable, it's not feasible when building a cdylib.  Second, if the signal handler just unconditionally froze the thread, then there'd be a high risk of freezing the thread while it owns e.g. a `malloc` lock, which could later hang the exiting thread.  To do this "properly" you would want the signal handler to walk the call stack and determine whether there are any non-Rust frames (or something like that).  But that would be quite a bit more intrusive than anything the runtime currently does, and potentially impossible, especially on `panic=abort` builds where there is not necessarily unwind info or frame pointers.

  You could sidestep these issues by having the runtime just abort if extra threads exist rather than trying to halt them, but that would be a big backwards compatibility break.

- If the check is done by an atexit handler then there might be ordering issues if C libraries register their own atexit handlers that run before Rust's handler.  If the check is done by `std::process::exit` then, as you mentioned, you have no safety if FFI code calls `exit` directly.  That might not be the end of the world, but it's problematic, especially when considering interop with other safe languages – or even interop with other Rust libraries with their own separate copies of libstd (which is a common situation with cdylibs).


## Comment 2303048656

other (NONE) · nicowilliams · 2024-08-21T21:32:22Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2303048656

> - Even when libstd knows about a thread, how would it quiesce or kill it?

When I write code to do this (in C) I make sure all my threads have an event loop so that sending them a message to exit is enough.  But this is not a general solution because threads might not have event loops.  For example, for the CPU-bound threads case you have to send them a signal (`pthread_kill()`) or cancel them (`pthread_cancel()`, which is typically a wrapper around `pthread_kill()` anyways).

Using `pthread_kill()` to quiesce threads (the handler would signal that it's quiesced then block forever) is an interesting idea, but now you need to camp on a signal (sigh) and you need to block the signal around certain operations (or do the clever stack walking thing you mentioned, but then if the thread can't be quiesced at that moment you need to arrange for it to get the signal again a bit later or for the operation that can't complete now to notice the need to quiesce later (more branches and memory accesses, or maybe modify the `.text` in place to insert a jump to signal-quiesced-and-block-forever code).

I'm not sure this is tractable.  You want to interop with C and other languages, and even without that it's reasonable to want to register exit-time handlers unless you want to mandate crash-only (just no dropping core please).  I'm a fan of crash-only, but I would hesitate at making that the only option in a language like Rust.

## Comment 2306114243

maintainer (MEMBER) · workingjubilee · 2024-08-23T03:31:12Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2306114243

I do not enjoy feeling compelled to silence discussion, even if it runs hot. I invite any of my peers to reverse this lock if they feel a sufficient cooling-off period to have elapsed, or perhaps if the conversation in question has been moved to https://internals.rust-lang.org/ or somewhere else likely. But this issue is not about debating the deeper semantics of Rust, its abstract goals, or whether modern programs have too many dependencies. It is not even about implementing thread-safe programs despite various forms of destructors existing.

It is about a concern about `std::process::exit` that makes **any** multithreaded program that calls `std::process::exit` "simultaneously" on two threads unsound. This fact remains even if we remove `atexit`, finalizers, and the like from the picture. The C Standard and POSIX, that I can see, say that **two calls to `exit` within the lifetime of the same program causes the following behavior to not be defined**. There is no additional caveat or requirement. No "if `atexit` was ever called". Merely a second `exit` will do.

It was previously hypothesized that due to implementation details, this function was actually "thread-safe" (in a *meaningful* sense) on common implementations. Now that we know this to be false, it does not matter whether the second call leads to undefined behavior because of various cleanup functions being called or because the second call is followed, in the implementing libc, by control-flow arriving at a C expression like `*NULL`.

## Comment 2308903902

maintainer (MEMBER) · RalfJung · 2024-08-25T15:52:33Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308903902

> It is about a concern about std::process::exit that makes any multithreaded program that calls std::process::exit "simultaneously" on two threads unsound. This fact remains even if we remove atexit, finalizers, and the like from the picture. The C Standard and POSIX, that I can see, say that two calls to exit within the lifetime of the same program causes the following behavior to not be defined. There is no additional caveat or requirement. No "if atexit was ever called". Merely a second exit will do.

That's what started the discussion, yes. But that part has been mostly resolved, I think:
- We added a lock on the Rust side to ensure that the 2nd `exit` will not happen. This is a work-around, not good enough for when `exit` also gets called by non-Rust code, but it helps.
- We [started](https://github.com/rust-lang/rust/issues/126600#issuecomment-2252680516) the slow process towards having libc's commit to, effectively, carry such a lock themselves. According to information [here](https://sourceware.org/bugzilla/show_bug.cgi?id=31997), glibc 2.41 will have such a lock. FreeBSD libc received a [similar patch](https://reviews.freebsd.org/D46108).

But it is still a valid question, and related to thread safety of `exit`, to ask "whose bug it is" when we have a situation like
- some library's exit handler (via `atexit` or `fini` sections or whatever) destroys a global resource (such as a mutex, in the case mentioned above)
- some code calls `exit`, or returns from `main`
- another thread is still running library code that accesses the mutex that is destroyed by the `atexit` handler

From a Rust perspective, I don't think there is any credible alternative to saying that this is a library bug. We cannot say that it is a bug in the code that calls `exit`, because we cannot make "return from `main`" an unsafe operation. (The only possibility I was able to come up with here is for the standard library to provide a "do not leave main" lock that libraries can acquire to ensure return-from-main blocks until library cleanup was done. That seems terrible.)

No matter whose bug it is, it will be a bunch of extra work for *someone* to deal with this and fix the bug, but at least this choice means we get a credible compositional safety story in return, making it better than the alternative.

Maybe this issue is the wrong place to discuss that question, but it is a question worth discussing. Or rather, since I think we already know the answer we want to give, we should "just" document that, to make it clear that this is an expectation Rust imposes on libraries: https://github.com/rust-lang/rust/pull/129581.

## Comment 2308917133

other (NONE) · richfelker · 2024-08-25T16:33:38Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308917133

We are also re-introducing `exit` locking in musl libc, to be included in version 1.2.6.

I'm pretty much entirely in agreewith with @RalfJung's [above comment](https://github.com/rust-lang/rust/issues/126600#issuecomment-2308903902). Destroying objects that could still be in use from an `atexit` handler is a library bug. Unfortunately this also means the very existence of non-PoD global C++ objects in a library is usually a library bug. There are probably general patterns that can be used to mitigate it, however.

I think we do need better resources for programmers to understand these issues so that they don't keep happening.

Aside from documenting that destroying global objects as part of a dtor/atexit handler is unsafe as far as Rust is concerned, I think most further work on this is outside the scope of the current issue report, which should be considered resolved by adding the Rust-side lock and getting libc implementors and standards on-track for doing locking on our side too.


## Comment 2308917316

other (NONE) · greghudson · 2024-08-25T16:34:11Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308917316

> From a Rust perspective, I don't think there is any credible alternative to saying that this is a library bug

As a C library author, I understand the arguments why Rust cannot reasonably prevent this situation, but I also don't think there's anything I can do, given the state of the ecosystem.

If platforms could ensure that library finalizers run after the end of library usage, then it would be safe to destroy global resources.  But platforms don't, and there's no obvious fix for that.

If platforms did not implement library unloading, then there would be no need to release global memory resources.  But platforms do, and people would (correctly) report bugs against my libraries if they leaked resources on each library unload.  I saw a lot of discussion in this PR which ignored library unloading, or dismissed it as a niche thing that most libraries don't support.  I don't think that is correct.  I would certainly prefer it if (at least by default) libraries remained mapped after all handles to them are closed and their global values persisted for a subsequent open, but that isn't generally the case, and frameworks like PAM can repeatedly open and close libraries.

If portable threads APIs didn't require dynamic mutex initialization and destruction, then the singleton mutexes used to protect global resources could persist after library finalizers.  But that isn't the case.  (I think the story gets better if you decide to rely on common properties of real-world pthreads implementations.  I don't think that's the case for Windows.)

One possible platform improvement would be to refrain from unloading libraries during process exit, and somehow communicate to library finalizers whether the process is exiting.  Then only finalizations affecting resources beyond the process (like flushing I/O buffers or resetting tty state) would need to be run.


## Comment 2308918996

other (NONE) · richfelker · 2024-08-25T16:39:19Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308918996

> As a C library author, I understand the arguments why Rust cannot reasonably prevent this situation, but I also don't think there's anything I can do, given the state of the ecosystem.

You can refrain from having global state in your library at all, and instead have an explicit state object that any user of the library is responsible for requesting and releasing. Parts of this can even then be shared between multiple consumers of the library within the same program; having explicit release ensures that you free things only when the last user is done - which might be never, but which will be before library unloading if the library is going to be unloaded.


## Comment 2308921554

other (NONE) · greghudson · 2024-08-25T16:47:23Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308921554

> You can refrain from having global state in your library at all

That's great if you can manage it.  C libraries frequently have history which precludes it, or are written to an API specification which precludes it.

## Comment 2308922227

other (NONE) · richfelker · 2024-08-25T16:49:15Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308922227

> That's great if you can manage it. C libraries frequently have history which precludes it, or are written to an API specification which precludes it.

Then they can be marked non-unloadable so that `dlopen`/`dlclose` N times does not leak O(N) resources but leaves O(1) resources live for the entire program lifetime. Perfectly acceptable behavior.


## Comment 2308923947

other (NONE) · greghudson · 2024-08-25T16:54:26Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308923947

> Then they can be marked non-unloadable 

If I can mark my libraries as non-unloadable in an even vaguely portable fashion, then I would like to sign up immediately.  I don't think that's a common platform facility.

## Comment 2308931347

other (NONE) · richfelker · 2024-08-25T17:22:39Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308931347

> If I can mark my libraries as non-unloadable in an even vaguely portable fashion, then I would like to sign up immediately. I don't think that's a common platform facility.

For ELF-based platforms, `-Wl,-z,nodelete` does it. If the library knows its own name, `dlopen(myname,RTLD_NOW|RTLD_LOCAL)` and throwing away the result does it at runtime on any platform with `dlopen`. If you want to write code that's compatible with static linking into an environment that might not have `dlopen`, declaring a weak reference to `dlopen` and testing it before calling should work.

```
#include <dlfcn.h>
__typeof__(dlopen) dlopen __attribute__((__weak__));
...
if (dlopen) ...
```

Libtool may have its own abstraction for how to mark libraries non-unloadable; I'm not sure.

None of this is perfectly portable but I think it meets your requirement for "even vaguely portable". At worst you may need to add special cases for Windows and Mac.


## Comment 2308941030

other (CONTRIBUTOR) · DemiMarie · 2024-08-25T17:55:30Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308941030

On Windows I’m not sure if making a library non-unloadable is an always an option, as it leaks the DLL’s handles.  Fortunately, `DllMain` on Windows takes an argument indicating whether it is called due to process termination (in which case cleaning up resources is not safe or needed) or due to DLL unloading (in which case cleaning up is both safe and needed).

## Comment 2308941357

maintainer (MEMBER) · bjorn3 · 2024-08-25T17:56:38Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308941357

On macOS using thread local storage effectively blocks dlclose. (There are several issues on the rust issue tracker about rust dylibs not getting unloaded when using dlclose. This due to rust's standard library using TLS internally and it by default getting statically linked into dylibs.)

## Comment 2308950786

other (CONTRIBUTOR) · comex · 2024-08-25T18:28:00Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308950786

> On macOS using thread local storage effectively blocks dlclose. (There are several issues on the rust issue tracker about rust dylibs not getting unloaded when using dlclose. This due to rust's standard library using TLS internally and it by default getting statically linked into dylibs.)

Indeed.  But on the other hand [there doesn't seem to be any](https://github.com/apple-oss-distributions/dyld/blob/a571176e8e00c47e95b95e3156820ebec0cbd5e6/common/MachOAnalyzer.cpp#L2952) explicit "never unload" flag for macOS.  No *nice* solution.

## Comment 2308964682

maintainer (MEMBER) · RalfJung · 2024-08-25T19:23:51Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2308964682

> As a C library author, I understand the arguments why Rust cannot reasonably prevent this situation, but I also don't think there's anything I can do, given the state of the ecosystem.

So it seems what you need is a function that is called on `dlclose` but not on `exit`? And then for `dlclose`, it is the caller's requirement to ensure that no thread runs library code any more (that's anyway required) so there can't be any conflict with concurrently running code?

Or alternatively, if supporting `dlclose` is not even your intent -- some way to tell libc about that so that it doesn't end up being incorrectly half-unloaded or so?

I am not sure what is the best platform to request features like that -- it'd have to come from libcs, right?

## Comment 2309419369

maintainer (MEMBER) · workingjubilee · 2024-08-26T06:23:13Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2309419369

> We https://github.com/rust-lang/rust/issues/126600#issuecomment-2252680516 the slow process towards having libc's commit to, effectively, carry such a lock themselves. According to information [here](https://sourceware.org/bugzilla/show_bug.cgi?id=31997), glibc 2.41 will have such a lock. FreeBSD libc received a [similar patch](https://reviews.freebsd.org/D46108).

Yes. My main concern is that the best use of this issue is, I think, continuing to coordinate these efforts. A concern that goes far enough afield, like advocacy for Rust adding an explicit API for exit handlers, [is better taken to the actual decision-makers](https://github.com/rust-lang/libs-team/issues/new?assignees=&labels=api-change-proposal%2C+T-libs-api&projects=&template=api-change-proposal.md&title=%28My+API+Change+Proposal%29).

For solving the issue of dynamic libraries having problems with dlclose, it sounds like we would want either something like "if this magic symbol is included in your dylib, it shouldn't be actually-unloaded at `dlclose` time" going on? The appropriate venue for that is probably POSIX, as `dlopen` is not a Standard C function.

## Comment 2309424539

maintainer (MEMBER) · bjorn3 · 2024-08-26T06:26:41Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2309424539

> For solving the issue of dynamic libraries having problems with dlclose, it sounds like we would want either something like "if this magic symbol is included in your dylib, it shouldn't be actually-unloaded at dlclose time" going on? The appropriate venue for that is probably POSIX, as dlopen is not a Standard C function.

For ELF based platforms there is already `-Wl,-z,nodelete` as noted a couple of comments back.

## Comment 2309432933

maintainer (MEMBER) · workingjubilee · 2024-08-26T06:32:17Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2309432933

Doesn't that require the person driving the linker to do it? It's not something the author can assure. And ELF is not under the purview of the Austin Group, I think.

## Comment 2310426573

maintainer (MEMBER) · RalfJung · 2024-08-26T14:59:36Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2310426573

> Yes. My main concern is that the best use of this issue is, I think, continuing to coordinate these efforts.

Fair. I feel like coordinating those efforts is out of scope of Rust, but it'd make sense for us to track progress here, and maybe remove our own `exit` lock once all libc guarantee thread-safe `exit` (but with the rate at which we increment our min glibc version, that will take many years).

Discussing how to write C libraries that can tolerate their exit handlers to be invoked at any time while also not leaking resources on `dlclose` (or somehow declaring they don't support being unloaded on `dlclose`) is also out of scope of Rust, but people are inevitably going to discuss this anyway, so I've created a [forum thread for this](https://users.rust-lang.org/t/how-to-write-a-library-rust-or-c-that-avoids-leaks-on-dlclose-and-races-on-exit/116623).

## Comment 2432716939

other (CONTRIBUTOR) · bstrie · 2024-10-23T15:57:33Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2432716939

This is a rather long thread, can we get a summary of the current status added to the original issue body? What are actionable steps that can be taken to resolve this unsound issue? AFAICT the status appears to be "wait until the rest of the world is fixed", which IMO is tantamount to closing this issue as WONTFIX, given the prospects of that ever happening. And I'm not entirely satisfied by the dismissal of ameliorations on the Rust side (either adding a lock or marking as `unsafe`). If we can do better, then let's do better, even if preventing people from linking to broken C code is out of our power.

## Comment 2432755871

maintainer (MEMBER) · ChrisDenton · 2024-10-23T16:12:58Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2432755871

The pure Rust fix would be to have some Rust API for adding on exit functions. This could side-step the issue entirely so long as you ignore C.

Note that we already have [a lock to mitigate this issue](https://github.com/rust-lang/rust/blob/be01dabfefd2daa4574b974f571c7852085d60cb/library/std/src/sys/exit_guard.rs#L32). However it's by no means a fix.


## Comment 2432772105

maintainer (MEMBER) · the8472 · 2024-10-23T16:18:56Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2432772105

> AFAICT the status appears to be "wait until the rest of the world is fixed", which IMO is tantamount to closing this issue as WONTFIX, given the prospects of that ever happening. 

Things are looking rosier than that. Posix, musl and glibc agreed to improve things and if I read the comments on the posix issue correctly they'll also bring it to the appropriate C committee.

## Comment 2433475177

maintainer (MEMBER) · the8472 · 2024-10-23T21:13:36Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2433475177

I have gathered a short summary and a few links from other comments into the top comment. Edit away if there's anything to correct.

## Comment 2622785286

other (CONTRIBUTOR) · safinaskar · 2025-01-29T20:34:07Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2622785286

Please, document in https://doc.rust-lang.org/nightly/std/process/fn.exit.html , on which platforms `exit` is fully thread-safe (even if some C code calls it), and on which platforms it is not. As well as I understand, `exit` is fully safe on musl. This should be documented on that page.

Also, as well as I understand, musl is shipped with Rust itself. This means nothing prevents us from patching it! So, I suggest patching all remaining similarly unsafe C functions (`setenv`?) in musl implementation we ship. This will allow us fully solve all these remaining Rust unsoundness problems caused by system libc once and for all (at least for system libraries we ship).

Also, we can create alternative target with static glibc. We will patch that glibc however we want, we will fix all `exit`, `setenv`, etc problems there. (Unfortunately, if we really want static glibc, we should build it with `--enable-static-nss`, but this is blocked by https://sourceware.org/bugzilla/show_bug.cgi?id=27959 )

## Comment 2622790647

maintainer (MEMBER) · RalfJung · 2025-01-29T20:36:48Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2622790647

> Please, document in https://doc.rust-lang.org/nightly/std/process/fn.exit.html , on which platforms exit is fully thread-safe (even if some C code calls it), and on which platforms it is not. As well as I understand, exit is fully safe on musl. This should be documented on that page.

That is really something the respective platforms need to document. We shouldn't be in the business of providing a central repository of  all the ways in which various C implementations promise more than the C standard. We track this for our own needs here, but that is not the same as making it part of the official docs.

And we are also not interested in maintaining a patched fork of musl or glibc.

## Comment 2622797337

maintainer (MEMBER) · RalfJung · 2025-01-29T20:40:12Z · https://github.com/rust-lang/rust/issues/126600#issuecomment-2622797337

What we should do, however, is document that it is UB to call this `exit` concurrently with C code calling `exit`.
