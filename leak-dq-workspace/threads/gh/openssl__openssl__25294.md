# Race condition on error strings cleanup?

- URL: https://github.com/openssl/openssl/issues/25294
- Repo: openssl/openssl (language: C)
- State: open; created 2024-08-27T09:48:30Z; status ok; passes main

## Issue body

reporter (MEMBER) · beldmit · 2024-08-27T09:48:30Z · https://github.com/openssl/openssl/issues/25294

This report is inspired by https://github.com/latchset/pkcs11-provider/issues/429#issuecomment-2276242417 and https://github.com/latchset/pkcs11-provider/issues/429#issuecomment-2276265853. This report is based on my understanding of the issue and may not be correct, we didn't manage writing a simple reproducer here and now.

Looks like, when we have a default library context and a non-default one with loaded provider, the lock object is freed on freeing non-default context and attempt to lock it causes crash on exit. 

Looks like it has nothing to do with OpenSSL atexit() handler as the crash is reproduced when we build OpenSSL with `no-atexit`. 

@simo5, @Jakuje and @AdamWill may give some more details.



## Comment 2312107473

maintainer (MEMBER) · t8m · 2024-08-27T10:08:50Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312107473

What I see in the backtrace is that ldap is trying to call OpenSSL when OPENSSL_cleanup() was already called. Who called it or how was the call triggered is not clear. I do not really see a bug in OpenSSL here unless it was OpenSSL itself that called the cleanup. Are you sure about no-atexit being applied properly in the last tests?


## Comment 2312121189

reporter (MEMBER) · beldmit · 2024-08-27T10:15:19Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312121189

We will double-check but I'm sure the build was done with no-atexit. I don't have the env in my disposal :(

## Comment 2312132814

maintainer (MEMBER) · t8m · 2024-08-27T10:20:27Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312132814

We need to find out what calls OPENSSL_cleanup() then. If it is explicitly called by an application, then either this call must be removed or ldap must not do things with OpenSSL in atexit or fini handler.

## Comment 2312248642

other (NONE) · abbra · 2024-08-27T11:08:57Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312248642

This is happening with OpenLDAP 2.6.8 which has the following commit:

```
commit 1d37f7b005163b4cf531da3cb98eeade2bb7b644
Author: Howard Chu <hyc@openldap.org>
Date:   Tue May 7 19:47:35 2024 +0100

    ITS#10209 libldap: only use OPENSSL_INIT_NO_ATEXIT if it's defined
    
    Fake OpenSSL clones like LibreSSL don't support it.
    
    In general we will make no effort to support fake OpenSSL clones.

diff --git a/libraries/libldap/tls_o.c b/libraries/libldap/tls_o.c
index f24158252b..d5861d9339 100644
--- a/libraries/libldap/tls_o.c
+++ b/libraries/libldap/tls_o.c
@@ -225,7 +225,12 @@ tlso_init( void )
        SSL_library_init();
        OpenSSL_add_all_digests();
 #else
-       OPENSSL_init_ssl(OPENSSL_INIT_NO_ATEXIT, NULL);
+#ifdef OPENSSL_INIT_NO_ATEXIT
+#define        OPENSSL_FLAGS   OPENSSL_INIT_NO_ATEXIT
+#else
+#define        OPENSSL_FLAGS   0
+#endif
+       OPENSSL_init_ssl(OPENSSL_FLAGS, NULL);
 #endif
 
        /* FIXME: mod_ssl does this */


```

Even before that, there was the following commit:
```
commit e08b80e8b7534d63080bdd4a2eb2a3d46071aef8
Author: Howard Chu <hyc@openldap.org>
Date:   Sun Feb 18 10:57:07 2024 +0000

    ITS#9952 TLS/OpenSSL: disable use of atexit()
    
    This will only have any effect if libldap is the first caller to
    initialize OpenSSL, but that should be all that matters when libldap
    is part of a dynmically loaded module. It prevents the crash in the
    example cases given.

diff --git a/libraries/libldap/tls_o.c b/libraries/libldap/tls_o.c
index 6847ef33b4..9bd830c196 100644
--- a/libraries/libldap/tls_o.c
+++ b/libraries/libldap/tls_o.c
@@ -225,7 +225,7 @@ tlso_init( void )
        SSL_library_init();
        OpenSSL_add_all_digests();
 #else
-       OPENSSL_init_ssl(0, NULL);
+       OPENSSL_init_ssl(OPENSSL_INIT_NO_ATEXIT, NULL);
 #endif
 
        /* FIXME: mod_ssl does this */

```


## Comment 2312531809

other (CONTRIBUTOR) · simo5 · 2024-08-27T13:14:23Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312531809

While openldap here may be doing something wrong (not certain but they may be trying to free the *default* openssl context which would be a bad idea in a library), this is a race condition in openssl that tries to access a lock after already having nulled it.
That simply should not happen, regardless of whether ldap is doing good or bad thing.
If openssl_cleanup() has already been called there should be a guard that makes it a noop if it is called again.

However this is a different issue than double calling cleanup, this is the code that frees the providers trying to cleanup the default context err_strings to my reading which sound suspicious.



## Comment 2312657976

maintainer (MEMBER) · t8m · 2024-08-27T14:02:56Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312657976

The cleanup done in libldap in the fini handle is not about calling OPENSSL_cleanup() but it is calling into OpenSSL. The problem is something else before that does the OPENSSL_cleanup() call, that must be investigated and the call removed (or postponed after the fini call in libldap).

## Comment 2312717617

other (CONTRIBUTOR) · simo5 · 2024-08-27T14:23:06Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312717617

@t8m if openldap where to instantiate a new libctx, would that prevent an OPENSSL_cleanup() called on the default context from messing up until that other libctx is also freed ?

If not I do not think we can get out of this, because when you have multiple libraries loaded in a process you may not have any control on what is called in what order.

## Comment 2312735678

other (CONTRIBUTOR) · simo5 · 2024-08-27T14:30:24Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312735678

Just to be clear, note that openldap is simply calling SSL_CTX_free() which is the correct thing to do in a library. So if cleanup is proceeding while there are contexts still around I think it is something OpenSSL should deal with.
One way would be to mark the context as freed so that any call into it will not crash but will also be a no-op.
Leaking an allocation for the context structure itself in case the application fails to free the context is preferable to crashes.

## Comment 2312796218

maintainer (MEMBER) · t8m · 2024-08-27T14:55:17Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312796218

OPENSSL_cleanup() is NOT libctx-specific. It should NOT be called from a library. After it is called, OpenSSL must never be used again (except of any other OPENSSL_cleanup() call).

There is no indication that libldap is calling OPENSSL_cleanup() by itself. The cleanup calls you see in the backtrace are not related to an OPENSSL_cleanup() call and they are legitimate.

However, something somewhere must have called OPENSSL_cleanup() before that and that must not be done if any library or the app is still having OpenSSL calls to do. This was always the case and we will not try to patch things around here as a hackish workaround/bug fix.


## Comment 2312811767

maintainer (MEMBER) · t8m · 2024-08-27T15:01:44Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312811767

I have one more thing to add. For the reason that an application might want to call OPENSSL_cleanup() before it terminates to get a clean valgrind output, it is in general a bad idea to call OpenSSL from a library destructor. So actually it is partially a libldap fault, however the best way to resolve this is to simply not call OPENSSL_cleanup() at all. It is not really necessary.


## Comment 2312833287

other (CONTRIBUTOR) · simo5 · 2024-08-27T15:09:41Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312833287

In the end it comes down to ERR_unload_strings() being called after err_string_lock has been NULLed, which happens only in err_cleanup() if I read it right, and err_cleanup() is called only in OPENSSL_cleanup().

The thing here is that I assume python correctly called OPENSSL_cleanup() before exiting but the openldap (also correctly ?) is calling SSL_CTX_free() in its atexit handler, which necessarily comes after python is done.

So either it is illegal to do anything with openssl in atexit handlers, and openldap should just leak those contexts. Or OpenSSL handles gracefully freeing contexts after OPENSSL_cleanup() has been called.

This specific string freeing crash can be worked around by checking if err_string_lock is NULL in ERR_unload_strings(), but it is just trying to swipe the dust under the mat, pretty sure something else will end up blowing up.

This is the sequence as I understand it:

Process calls OPENSSL_cleanup() [which calls err_cleanup() which set err_string_lock = NULL] and then exit().

Atexit() handler kicks in at this point and openldap calls SSL_CTX_free() and this goes down as this sequence of calls:
```
 - SSL_CTX_free()
   - ssl_evp_cipher_free()
     - EVP_CIPHER_free()
       - evp_cipher_free_int()
         - ossl_provider_free()
           ...
           - ERR_unload_strings()
             -  CRYPTO_THREAD_write_lock(err_string_lock)  <- BOOM
```

## Comment 2312841205

other (CONTRIBUTOR) · simo5 · 2024-08-27T15:13:02Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312841205

> However, something somewhere must have called OPENSSL_cleanup() before that and that must not be done if any library or the app is still having OpenSSL calls to do. This was always the case and we will not try to patch things around here as a hackish workaround/bug fix.

I guess the only fix here is to make openldap leak the SSL ctx and not try to free it in an atexit() handler


## Comment 2312843317

maintainer (MEMBER) · t8m · 2024-08-27T15:13:51Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312843317

Yeah, or not call OPENSSL_cleanup() from python.


## Comment 2312862930

other (CONTRIBUTOR) · simo5 · 2024-08-27T15:20:58Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312862930

> Yeah, or not call OPENSSL_cleanup() from python.

This would be ineffective, openldap would blow up in some other application calling OPENSSL_cleanup() ... which is a valid thing to do for an application.

## Comment 2312923971

other (NONE) · AdamWill · 2024-08-27T15:46:16Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312923971

So...is there an openldap bug report?

## Comment 2312936898

other (CONTRIBUTOR) · nhorman · 2024-08-27T15:51:40Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312936898

@simo5 what openssl bindings are being used in your python environment?  I'm looking at the python cryptography package, and while they don't appear to actually call OPENSSL_init_crypto/OPENSSL_cleanup at all (not sure how they avoid all the memory leaks), But it does appear to dynamically load openssl when cryptography is imported/used.  Is it possible that the library version which python loaded differs from the one that you built for openldap?  i.e. I'm wondering if, despite the fact that you built openssl with no-atexit, that python is loading a different version that does have atexit enabled, and the loading of libldap is just resolving the symbols to the former library rather than loading what you expect?

The test would be to run the server and then check /proc/<pid>/maps to see the path that libssl and libcrypto were loaded at.  If its not what you expect, a solution might be to force python to look in a different path for libcrypto/ssl so that you properly get your no-atexit version.

## Comment 2312947041

other (CONTRIBUTOR) · simo5 · 2024-08-27T15:56:00Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312947041

@nhorman I do not think it matters how OPENSSL_cleanup() ends up being called, it is totally legal for an application to call it, and the destructor openldap calls at library unload will blow up regardless of atexit() or not.

This is the issue:
https://github.com/openldap/openldap/blob/c9ab732ec18e32c58643e44a45233a6ed87830b6/libraries/libldap/init.c#L500

## Comment 2312949677

other (CONTRIBUTOR) · simo5 · 2024-08-27T15:57:07Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312949677

It just so happens that if there is a non-default provider loaded this ends up crashing. If there isn't we just do not notice, but it is wrong either way.

## Comment 2312970771

other (CONTRIBUTOR) · nhorman · 2024-08-27T16:05:42Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2312970771

@simo5 an application can absolutely call OPENSSL_cleanup, as long as it is aware of the libraries that its loading, and ensure that any dependent libs are no longer using openssl at the time cleanup is called, or after, but I grant you in this situation those conditions aren't met, and OPENSSL_cleanup shouldn't be called.

that said, I don't see anywhere in pyca/cryptography that happens.  What I'm postulating is that python is loading libcrypto at some point before libldap is loaded, and is doing so from a path that differs from the location that you have your version of openssl which was built with no-atexit (note I have no idea if this is true, its just a hyptohesis).  The result of that may be that:
a) python (ne pyca/cryptography) is loading a version of libcrypto that does have atexit handlers registered, and so is calling OPENSSL_cleanup implicitly when python exits
and 
b) that libldap, when loaded is resolving its libcrypto symbols to the already loaded versions from (a) - i.e. you're not actually using your no-atexit build of openssl

I'm suggesting that, if you can force the library load path of python to use your no-atexit build, you might be able to avoid this problem.  Its still a crappy situation, but if the hypothesis is right, its a reasonable workaround.

## Comment 2313019045

other (NONE) · droideck · 2024-08-27T16:26:59Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2313019045

OpenLDAP bug opened for this issue:
https://bugs.openldap.org/show_bug.cgi?id=10255

## Comment 2313030175

other (CONTRIBUTOR) · simo5 · 2024-08-27T16:32:36Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2313030175

@nhorman you are barking up the wrong tree sorry.

It would be nice to be able to know what libraries you are loading from an application but it is often not possible (people use to load in glibc things like nss_ldap which the application would not be aware of at all, and generally any library that is pluggable ... like openssl with providers makes it so that it is impossible for an application to generically and categorically know all the libraries it loaded).

So given that libldap can be pulled into random applications and applications are allowed to call OPENSSL_cleanup() before exiting, the only sane thing to do is to avoid trying to touch SSL context in ldap destructors, and just let them leak if the application does not explicitly free the ldap context.


## Comment 2313042436

reporter (MEMBER) · beldmit · 2024-08-27T16:38:26Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2313042436

> So given that libldap can be pulled into random applications and applications are allowed to call OPENSSL_cleanup() before exiting, the only sane thing to do is to avoid trying to touch SSL context in ldap destructors, and just let them leak if the application does not explicitly free the ldap context.

It means that for lack of memory leaks an application should be able to provide the context managed by it, not by the library


## Comment 2313173526

other (NONE) · hyc · 2024-08-27T17:47:50Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2313173526

> > So given that libldap can be pulled into random applications and applications are allowed to call OPENSSL_cleanup() before exiting, the only sane thing to do is to avoid trying to touch SSL context in ldap destructors, and just let them leak if the application does not explicitly free the ldap context.
> 
> It means that for lack of memory leaks an application should be able to provide the context managed by it, not by the library

Apps can always provide their own context via `ldap_set_option(.., LDAP_OPT_X_TLS_CTX, ...)` but since most apps don't do this explicitly, libldap will still have to create one itself by default.

Leaking the context should typically be OK but if any app tends to load/unload modules repeatedly during a run it will become a problem. I would expect this is not a normal usage pattern though.

## Comment 2313183525

other (NONE) · hyc · 2024-08-27T17:54:02Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2313183525

As I noted in https://bugs.openldap.org/show_bug.cgi?id=9952#c5 you guys could just fix your damn cleanup functions to check for the context already being NULL before executing.

## Comment 2313261191

reporter (MEMBER) · beldmit · 2024-08-27T18:40:33Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2313261191

> Apps can always provide their own context via `ldap_set_option(.., LDAP_OPT_X_TLS_CTX, ...)` but since most apps don't do this explicitly, libldap will still have to create one itself by default.

Thanks, it's a great design!



## Comment 2390847263

other (CONTRIBUTOR) · nhorman · 2024-10-03T08:40:44Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2390847263

Ok, so from my re-read here, the path forward is for openLDAP to not touch SSL contexts on their cleanup path.  Is there any reason for this to remain open?

## Comment 2391707060

other (NONE) · hyc · 2024-10-03T15:24:33Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2391707060

> Is there any reason for this to remain open?

IMO yes, a library that requires callers to leak memory is a broken library. It's frankly shocking that a debate was needed about whether to fix things properly. Even moreso that the outcome of that debate was "no". I've been developing with this codebase since SSLeay 0.4 but if this is how you guys want to do things I think it's time to abandon this project.



## Comment 2391815903

other (CONTRIBUTOR) · nhorman · 2024-10-03T16:15:28Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2391815903

I'm sorry, but I don't see how you arrive at that conclusion.  To recap my read of this issue:

1) An issue was [reported](https://github.com/openssl/openssl/issues/25294#issue-2488831209).  It is assumed that a crash occurs because a lock (specifically the err_string_lock) is freed on the freeing of one context and then its use is attempted by an other context.

2) @t8m pointed out that the only way that lock gets freed is via a call to OPENSSL_cleanup.  This is observable, as there are only two calls to CRYPTO_THREAD_lock_free(err_string_lock), one in do_err_strings_init() if the a failure occurs, which would present as an unsuable library (init failure), and one in err_cleanup(), which is only called from OPENSSL_cleanup.  As such, something must have called OPENSSL_cleanup.  If not via the atexit handler  ( [disabled by configuration here](https://github.com/openssl/openssl/issues/25294#issuecomment-2312121189) ), then by some other caller, possibly in a different call stack.

3) @simo5 indicated that the solution going forward was to modify the openldap destructor to not touch SSL objects ([allowing them to leak](https://github.com/openssl/openssl/issues/25294#issuecomment-2313030175))

So I don't see how you arrive at the conclusions that openssl mandates memory leakage, or that  the outcome of the debate was "no" (which I think I correctly interpret as your view being that the openssl devs have agreed there is an openssl bug here, and that we're not going to fix it, please correct me if I'm wrong).  I don't see that conclusion at all, rather that the openssl team has presented a counter argument to the assertion of the root cause of the issue, and there doesn't seem to have been any follow up to identifying that alternate root cause.

That said, item (3) in my mind is not a foregone conclusion.  We could absolutely pursue continuing to look for the wayward copy of libcrypto (possibly linked to or loaded by another library component of openldap, or python itself, and find where OPENSSL_cleanup is getting called prior to openldaps destructors.  I'm happy to help out with that, But it sounds like thats not whats going to happen.  And if its not, then the question stands, why is this still open?

## Comment 2391839576

other (NONE) · hyc · 2024-10-03T16:28:32Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2391839576

> That said, item (3) in my mind is not a foregone conclusion. We could absolutely pursue continuing to look for the wayward copy of libcrypto (possibly linked to or loaded by another library component of openldap, or python itself, and find where OPENSSL_cleanup is getting called prior to openldaps destructors. I'm happy to help out with that, But it sounds like thats not whats going to happen. And if its not, then the question stands, why is this still open?

Finding the wayward copy is pointless. It should be obvious that you can't account for all of the possible ways libcrypto gets invoked in an arbitrary process. As such, the only viable course of action is to ensure that it's safe to call OpenSSL_cleanup redundantly. And doing that isn't hard.

## Comment 2392311243

maintainer (MEMBER) · t8m · 2024-10-03T20:51:11Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2392311243

> Finding the wayward copy is pointless. It should be obvious that you can't account for all of the possible ways libcrypto gets invoked in an arbitrary process. As such, the only viable course of action is to ensure that it's safe to call OpenSSL_cleanup redundantly. And doing that isn't hard.

You can call OPENSSL_cleanup() redundantly. That isn't the problem here. What you cannot do is to do any other
OpenSSL calls (apart from those not touching error state or any other global state) after you called OPENSSL_cleanup(). We could add guards here and there but these wouldn't be thread safe and would not really solve the problem as the only thing that such call can do safely is to immediately return failure.

## Comment 2392314577

maintainer (MEMBER) · t8m · 2024-10-03T20:53:06Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2392314577

The best way to fix these problems is to not call OPENSSL_cleanup() at all. The global state does not need to be cleaned up. It should not cause any memory leakage reports as the allocated memory will be linked from the global state.

## Comment 2392549785

other (CONTRIBUTOR) · nhorman · 2024-10-04T00:18:42Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2392549785

@hyc I understand that you think its pointless and it seems @simo5 agrees, let me try explain why I disagree 

We agree that there is A problem in which openssl cleans up it's data structures prior to some components finishing their use, yes?

As I tried to elaborate above, I'm hypothesizing that the environment in question is using two versions of openssl, one that has atexit disabled, and another that does not.  If that is the case and symbol resolution occurs in a "wrong" or "bad" order symbols may get resolved such that the version of OpenSSL_crypti_iniy that gets bound is on that does atexit registration.  In that event you will get exactly the symptom you are seeing 

While I understand you think that it's impossible to know every component that uses openssl, this is in fact the bug here (hypothetically).  That multiple components are using different versions of openssl, and the application is getting bound to the unexpected/wrong version with an incompatible config.  While we can't know all the components that use openssl we can perhaps influence the version that gets selected in such an environment, allowing for the use of an acceptable build time config.

If you don't want to explore that, then I'm back to my original question, why are we still working on this issue?  If you just want the openssl cleanup model changed to support this, that's fine, we have plans to remove at exit in 4.0 (it's going to be abi breaking so it has to wait for a major release).  I'm on my phone now so I can't look it up, but I can post the trackig issue here tomorrow.  At which point this seems like a duplicate to me.

Or you can just follow the proposed solution @simo5 proposed and let the SSL_CTX objects leak.  In my view it seems worthwhile to pursue my hypothesis to avoid that leakage, at least until the atexit code gets removed.

But Its your all's choice.  Let us know what you would like to do.

## Comment 2475307389

other (NONE) · droideck · 2024-11-14T02:53:55Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2475307389

Hello,
I am the OpenLDAP maintainer for Fedora and RHEL.

Could you please provide guidance regarding the final OpenSSL decision on this matter?

If it is determined that OpenSSL expects `SSL_CTX_free` not to be called on the OpenLDAP side, I will work on a solution to exclude calling `ldap_pvt_tls_ctx_free` partially from the `ldap_int_destroy_global_options` destructor.

If I understand correctly, this approach will cause OpenLDAP in Fedora and RHEL to diverge from the upstream implementation in this regard, which I regret. However, I recognize that this may be necessary.

## Comment 2476309141

other (CONTRIBUTOR) · nhorman · 2024-11-14T13:05:07Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476309141

As I noted (here)[https://github.com/openssl/openssl/issues/25294#issuecomment-2392549785], I have a hypothesis for whats going on here, specifically that, while openLDAP builds to link against an openssl version that has atexit use disabled, another linked component (python IIRC), builds and links against an openssl version that still has atexit use enabled, leading to this issue.  A possible solution would be to simply change the python build configuration such that is disables atexit usage in openssl as well, which would solve the problem without having to diverge from upstream.  There doesn't seem to be interest in pursuing that approach however, so you are likely stuck with having to carry a custom patch, at least until we remove atexit usage entirely, which needs to happen on a major release boundary, and all components need to update to it.

## Comment 2476404984

other (CONTRIBUTOR) · simo5 · 2024-11-14T13:49:35Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476404984

@nhorman sorry but your hypothesis is provably wrong as we can reproduce on a system with a single dynamically linked OpenSSL. The analysis is clear that what is happening is that openldap in their destructor calls SSL_CTX_free() on a libctx *after* OPENSSL_cleanup() has already been called. So please let's not keep advancing theories. Let's decide what is the behavior OpenSSL expects so we can move on.

Note that removing atexit() is not sufficient to avoid all cases, because an application *can* be calling OPENSSL_cleanup() before exit() and OpenLdap libraries would then still call SSL_CTX_free() in their library destructor that necessarily executes after exit().

So either OpenSSL wants to make SSL_CTX_free() safe to call after OPENSSL_cleanup() or we must remove any call to OpenSSL functions in any destructor anywhere.

## Comment 2476457307

other (CONTRIBUTOR) · Sashan · 2024-11-14T14:12:26Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476457307

Do I understand right the libldap calls `SSL_CTX_free()` from library `_fini()` (a.k.a. library destructor)?
if it is the case, then this is not a race condition. It's rather matter of unfortunate ordering. If I remember correct the libc calls atexit handlers first (this is where the call to `OPENSSL_cleanup()` happens. Once all registered atexit handlers are done, the libc is going to call library destructors, this is where `SSL_CTX_free()` is coming from. call to `SSL_CTX_free()` comes _after_ call to `OPENSSL_cleanup()` in this case. I've found it while I was trying to replace `atexit()` with library destructors (call `OPENSSL_cleanup()` from `_fini()`). But moving call to `OPENSSL_cleanup()` to library destructor (`_fini()`) invites also it's [problems](https://github.com/openssl/openssl/pull/24148#issuecomment-2139491761). The plan is to leave it as it is in 3.x versions.

In my opinion the only way how to sort it out is not to use atexit to call `OPENSSL_cleanup()` at all. And let application to call it explicitly if wants to do so.

## Comment 2476647460

maintainer (MEMBER) · t8m · 2024-11-14T15:11:00Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476647460

@Sashan @nhorman The problem with OpenLDAP will happen not just if the OPENSSL_cleanup() is called within atexit() but also when OPENSSL_cleanup() is called from an application with OpenLDAP library being still loaded because if the OpenLDAP library unload happens after that, it will only at that point try to call SSL_CTX_free() which is already an invalid call.

So yeah @simo5, for safety reasons OpenLDAP cannot really call SSL_CTX_free() in the library destructor if it is to be used in such apps.

I believe this requires two things to clean this mess up:
1. OpenLDAP should use its own OSSL_LIB_CTX for that SSL_CTX
2. We need to change OPENSSL_cleanup() to be a no-op if there are existing non-default OSSL_LIB_CTX contexts that are not released yet.

Except 2) is not as easy because these contexts might be allocated by a provider loaded into the default context and that would effectively make any OPENSSL_cleanup() a no-op. So perhaps we have to always deinitialize the default context first and only then check if there are still any remaining OSSL_LIB_CTX contexts and do not try to release any global data in such case.


## Comment 2476755577

other (CONTRIBUTOR) · Sashan · 2024-11-14T15:46:29Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476755577

What openldap can do is to opt-out from atexit. Calling `OPENSSL_init_crypto(OPENSSL_INIT_NO_ATEXIT)` at the beginning should prevent libcrypto from arming atexit handler. The openldap then can call `OPENSSL_cleanup()` from its library destructor. This is perhaps the solution which fits best to the current situation.

## Comment 2476783313

maintainer (MEMBER) · t8m · 2024-11-14T15:57:27Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476783313

> What openldap can do is to opt-out from atexit. Calling `OPENSSL_init_crypto(OPENSSL_INIT_NO_ATEXIT)` at the beginning should prevent libcrypto from arming atexit handler. The openldap then can call `OPENSSL_cleanup()` from its library destructor. This is perhaps the solution which fits best to the current situation.

No @Sashan, unfortunately that does not solve anything. As @simo5 and I said the same problem happens if an application calls OPENSSL_cleanup() **explicitly** before OpenLDAP is unloaded. Which can very well happen as OpenLDAP is used for example by the nss_ldap module.

## Comment 2476798685

other (CONTRIBUTOR) · simo5 · 2024-11-14T16:03:09Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476798685

@Sashan it's be nice if you red other messages fully before proposing "solutions".
That last thing libldap should do is call OPENSSL_cleanup() itself and break the other 50% of applications that do not blow up today.

@t8m has provided the only reasonable solutions if libldap for some reason needs to clean up the context.

But libldap should probbaly stop calling SSL_CTX_free() at all.

Libldap has no way to know if other libraries still are using the default context in *their* destructors as well, only a context allocated by the library itself for exclusive use is safe to free in a destructor as a general rule. Any context provided by the application should also *not* bee freed, because the application may still be using it after it calls dlclose() on the ldap library (unless the contract is that the application relinquish all control on the ctx after it gives it to openldap).





## Comment 2476851391

other (CONTRIBUTOR) · Sashan · 2024-11-14T16:20:44Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2476851391

simo5@ sorry I was following my path on how to make sure OPENSSL_cleanup() is not invoked before library destructors. I agree libldap should not be calling `OPENSSL_cleanup()`. I think my suggestion to use `OPENSSL_INIT_NO_ATEXIT` is valid thing, which is worth to try.

edit:
suggestion above won't help if there are more calls to `OPENSSL_init_crypto()`. if single call to `OPENSSL_init_crypto()` from within the application does not use `OPENSSL_INIT_NO_ATEXIT`, then we are back at square one with atexit handle armed. 

## Comment 2477191588

other (NONE) · hyc · 2024-11-14T18:59:27Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2477191588

We already disabled OpenSSL's use of atexit, back in February. Why are we still having this conversation?

https://git.openldap.org/openldap/openldap/-/commit/a5953812f0c03e802e61109ae18e8fed5f3f2df8

As for nss_ldap - that was deprecated over a decade ago. Distros should be using nss-pam-ldapd.

## Comment 2478519695

other (CONTRIBUTOR) · Sashan · 2024-11-15T10:35:49Z · https://github.com/openssl/openssl/issues/25294#issuecomment-2478519695

> We already disabled OpenSSL's use of atexit, back in February. Why are we still having this conversation?
> 
because this works if and only if there is a single call to `OPENSSL_init_crypto()`/`OPENSSL_init_ssl()` from the application. Consider a case where the application depends on more shared libraries (libldap + libwhatever). If those libraries further depend on libcrypto, then we are heading to a situation where libwhatever may override libldap's decision not to arm atexit, by simply calling `OPENSSL_init_crypto()` with its own set of flags.

we are just afraid to change the unfortunate behavior in 3.x release.

## Comment 3617550313

other (CONTRIBUTOR) · nhorman · 2025-12-05T16:16:02Z · https://github.com/openssl/openssl/issues/25294#issuecomment-3617550313

@beldmit @simo5 I know this is somewhat old, and we're investigating approaches to remove atexit() in 4.0.  In that vein wondering if you would mind testing with the tree defined here:
https://github.com/nhorman/openssl/tree/cleanup-experiment

We have another approach, in which we propose using an environment variable to enable atexit() only for memory leak checking, enabled via an environment variable, but that one isn't quite ready yet.

## Comment 3672172683

other (CONTRIBUTOR) · nhorman · 2025-12-18T20:52:25Z · https://github.com/openssl/openssl/issues/25294#issuecomment-3672172683

@simo5 @beldmit actually, scratch the above, could you try this patch to openldap:
```
diff --git a/libraries/libldap/tls_o.c b/libraries/libldap/tls_o.c
index 729b6e9308..6790e63b4a 100644
--- a/libraries/libldap/tls_o.c
+++ b/libraries/libldap/tls_o.c
@@ -230,6 +230,8 @@ tlso_init( void )
        (void) tlso_seed_PRNG( lo->ldo_tls_randfile );
 #endif
 
+    if (!OPENSSL_add_library_user())
+        return -1;
 #if OPENSSL_VERSION_NUMBER < 0x10100000
        SSL_load_error_strings();
        SSL_library_init();
@@ -271,6 +273,7 @@ tlso_destroy( void )
                LDAP_FREE( lo->ldo_tls_randfile );
                lo->ldo_tls_randfile = NULL;
        }
+    OPENSSL_cleanup_ex();
 }
```

Instead.  its meant to be used with this patch:
https://github.com/nhorman/openssl/tree/library-users-rebase-to-noatexit

Which is a summary of work we have been doing for 4.0.  It removes the atexit handler useage from openssl entirely, and replaces it with a global reference counting mechanism.  With it, you should be able to hold data allocated in openssl stable until such time as all participating users are done with it.

