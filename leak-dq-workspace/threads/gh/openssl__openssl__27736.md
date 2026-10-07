# Horrible `d2i_TYPE{,_bio,_fp}()` reuse behavior can lead to crashes on error

- URL: https://github.com/openssl/openssl/issues/27736
- Repo: openssl/openssl (language: C)
- State: open; created 2025-05-31T20:41:20Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · DDvO · 2025-05-31T20:41:20Z · https://github.com/openssl/openssl/issues/27736

`d2i_X509_ALGOR()` etc. behave badly as explained in `doc/man3/d2i_X509.pod`:

> In some versions of OpenSSL the "reuse" behaviour of d2i_TYPE() when *a is valid is broken and some parts of
       the reused structure may persist if they are not present in the new one. Additionally, in versions of
       OpenSSL prior to 1.1.0, when the "reuse" behaviour is used and an error occurs the behaviour is
       inconsistent. Some functions behaved as described here, while some did not free *a on error and did not set *a to NULL.
> 
> As a result of the above issues the "reuse" behaviour is strongly discouraged**

> If the "reuse" capability has been used with a valid structure being passed in via I<a>, then the object is
freed in the event of error and I<*a> is set to NULL.

BTW, the initial sentences referring to old OpenSSL versions appear outdated and presumably can be removed.

Unfortunately, `ASN1_item_sign_ctx()` and friends anyway use the "reuse" behaviour of `d2i_X509_ALGOR()`.
This has nasty effect on `d2i_X509_ALGOR()` failure, e.g., in case a provider yields bad DER encoding of `X509_ALGOR`:
any non-NULL `algor1` and `algor2`  is deallocated by `d2i_X509_ALGOR()`, 
and `0` is returned to signal an error.

When the caller then deallocates `algor1` or `algor2` that it had allocated, a double free occurs.
Since on getting `0` the caller does not know what the exact reason of the failure is, it cannot even be sure whether to apply a workaround such as assigning NULL to `algor1` or `algor2`.

Even worse, if the caller had used for `algor1` or `algor2` a pointer to a sub-part of a larger ASN.1 structure,
as done for certs, PKCS#10 CSRs, and CRLs in `crypto/x509/x_all.c`, e.g.:
```
    return ASN1_item_sign_ctx(ASN1_ITEM_rptr(X509_CINF),
                              &x->cert_info.signature,
                              &x->sig_alg, &x->signature, &x->cert_info, ctx);
```
on `d2i_X509_ALGOR()` failure, an attempt is made to free an address which was not allocated,
namely a sub-portion of the ASN.1 structure containing an `X509_ALGOR`, like in this strack trace:
```
==74611==ERROR: AddressSanitizer: attempting free on address which was not malloc()-ed: 0x6130000003e0 in thread T0
    #0 0x000105cf5480 in free+0x7c (libclang_rt.asan_osx_dynamic.dylib:arm64e+0x3d480)
    #1 0x000108741f34 in CRYPTO_free mem.c:353
    #2 0x000107f228e0 in ossl_asn1_item_embed_free tasn_fre.c:119
    #3 0x000107f22990 in ASN1_item_ex_free tasn_fre.c:25
    #4 0x000107f0fedc in asn1_item_ex_d2i_intern tasn_dec.c:121
    #5 0x000107f100c0 in ASN1_item_d2i_ex tasn_dec.c:144
    #6 0x000107f10250 in ASN1_item_d2i tasn_dec.c:154
    #7 0x000107f3322c in d2i_X509_ALGOR x_algor.c:27
    #8 0x000107ebc3d8 in ASN1_item_sign_ctx a_sign.c:236
    #9 0x000108c6db34 in X509_sign_ctx x_all.c:115
    #10 0x0001044eeaf4 in do_X509_sign apps.c:2406
    #11 0x0001044d5c44 in x509_main x509.c:970
    #12 0x0001043eb388 in do_cmd openssl.c:428
    #13 0x0001043ea6c4 in main openssl.c:309
    #14 0x00018cef2b48  (<unknown module>)
```
Here I see no chance for the caller to prevent the crash.

Can `ASN1_item_sign_ctx()` be changed not to use that bad "reuse" behaviour?
So far, it does 
```
        if (algor1 != NULL) {
            const unsigned char *pp = aid;

            if (d2i_X509_ALGOR(&algor1, &pp, aid_len) == NULL) {
                ERR_raise(ERR_LIB_ASN1, ERR_R_INTERNAL_ERROR);
                goto err;
            }
        }

        if (algor2 != NULL) {
            const unsigned char *pp = aid;

            if (d2i_X509_ALGOR(&algor2, &pp, aid_len) == NULL) {
                ERR_raise(ERR_LIB_ASN1, ERR_R_INTERNAL_ERROR);
                goto err;
            }
        }
```

## Comment 2930709060

maintainer (MEMBER) · kroeckx · 2025-06-02T13:23:59Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2930709060

I think the problem you're describing comes down to who the owner of the pointer is, and when the ownership changes. There are some options:
- It always transfers.
- The transfer happens at some random point, but we're not telling when.
- It's only transferred when the function returns success.

We need to pick a behavior and document it. My preference would be that on failure the ownership has not been transferred.

For objects that can be reused, the error path becomes much harder than it needs to be. The easiest is probably to free the old values on entry, and set the pointers to NULL on failure.

## Comment 2931867411

reporter (CONTRIBUTOR) · DDvO · 2025-06-02T18:08:57Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2931867411

Thank you for your comment.
Yes, ownership of the up to two `X509_ALGOR` pointers should not be transferred.
This is what happens when no error occurs - the structures just gets new contents.

Yet on failure of `d2i_X509_ALGOR()`, when applying its "reuse" behaviour, the structures are attempted to be freed,
which either leads to a double free by the caller (who cannot be sure whether a `d2i_X509_ALGOR()` failure or some other error occurred), or to attempts to free a pointer that was not even allocated (in case it points inside a larger structure).

So, as a workaround, `ASN1_item_sign_ctx()` should not apply the "reuse" behaviour but instead call `d2i_X509_ALGOR()` with its first argument being NULL, while still implementing the needed replacement of `X509_ALGOR` contents.
I do so in #27737 ~, but so far I did not find a way of doing so without partially getting a memory leak.~

## Comment 2937162706

reporter (CONTRIBUTOR) · DDvO · 2025-06-03T20:53:58Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2937162706

Initially, I had failed to point out exactly what is the horrible thing about the "reuse" capability of `d2i_*(a, ...)`:
On success, ownership of `a` stays with the caller, but on failure `a` is freed!

This is the code causing the issue in `crypto/asn1/tasn_dec.c` lines 120 and 121:
```
     if (rv <= 0)
         ASN1_item_ex_free(pval, it);
```
from commit f93ad22f6ad  of 2015-10-03 17:15:15 +0100

## Comment 2939070986

maintainer (MEMBER) · kroeckx · 2025-06-04T08:17:11Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939070986

So is this the underlying problem?
``
d2i_TYPE(), d2i_TYPE_bio() and d2i_TYPE_fp() return a valid TYPE structure or NULL if an error occurs. If the "reuse" capability has been used with a valid structure being passed in via a, then the object is freed in the event of error and *a is set to NULL.
``

If you look at the example in the ASN1_item_sign_ctx() manpage, you will pass a valid X509_ALGOR as part of some structure, and the d2i_X509_ALGOR() called by ASN1_item_sign_ctx() shouldn't be deleting this, it was not allocated in the first place.

Your workaround seems to be to temporary allocate some memory, and then on success copy the content.

## Comment 2939482941

reporter (CONTRIBUTOR) · DDvO · 2025-06-04T10:28:21Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939482941

> So is this the underlying problem? `d2i_TYPE(), d2i_TYPE_bio() and d2i_TYPE_fp() return a valid TYPE structure or NULL if an error occurs. If the "reuse" capability has been used with a valid structure being passed in via a, then the object is freed in the event of error and *a is set to NULL.`

Yes, a non-NULL pointer argument is freed on error, while on success ownership stays with the caller.

> If you look at the example in the ASN1_item_sign_ctx() manpage, you will pass a valid X509_ALGOR as part of some structure, and the d2i_X509_ALGOR() called by ASN1_item_sign_ctx() shouldn't be deleting this, it was not allocated in the first place.

Yes. (This example is exactly the situation as when self-signing a PKCS#10-formatted CSR, where `ASN1_item_sign_ctx()` replaces the preliminary contents of the X509_ALGOR sub-structure, while for X.509 certs, there are two such sub-structures.)

So far, as long as `X509_ALGOR` was constructed internally by libcrypto (or since 3.0 by the default provider), the chance of an error was very low (essentially just on out of memory), while with external providers, which anyway can have a hard time setting up `X509_ALGOR` as explained in #22932, risk of errors is much higher, such as a bad DER encoding.

> Your workaround seems to be to temporary allocate some memory, and then on success copy the content.

Exactly.

## Comment 2939488996

reporter (CONTRIBUTOR) · DDvO · 2025-06-04T10:30:34Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939488996

_[Copying over a comment I had originally made [there](https://github.com/openssl/openssl/pull/27737#issuecomment-2926692554), which actually fits better here:]_

libcrypto still contains many others  of those [strongly discouraged](https://docs.openssl.org/master/man3/d2i_X509/) uses of the "reuse" capability `d2i_<TYPE>()` with non-NULL first argument, at least part of which should be replaced.

For instance, in `crypto/store/store_result.c`:
```
        if (d2i_X509_AUX(&cert, (const unsigned char **)&data->octet_data,
                         data->octet_data_size) == NULL
            && (!ignore_trusted
                || d2i_X509(&cert, (const unsigned char **)&data->octet_data,
                            data->octet_data_size) == NULL)) {
            X509_free(cert);
            cert = NULL;
        }
```
strongly smells like double free on `d2i_X509{_AUX,}()` failure.

## Comment 2939536809

reporter (CONTRIBUTOR) · DDvO · 2025-06-04T10:47:57Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939536809

How about confirming this as a bug?

## Comment 2939745769

maintainer (MEMBER) · kroeckx · 2025-06-04T11:52:54Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939745769

I think that d2i behavior is really annoying, it should not free something it didn't allocate. I would prefer changing it over your solution to allocate something temporary. But I expect that changing that is going to break other things.

## Comment 2939798603

reporter (CONTRIBUTOR) · DDvO · 2025-06-04T12:11:34Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939798603

Yeah, fixing the behavior at its source might break some things and at least would violate documented behavior.
That's why I instead took the bumpy path of a non-trivial workaround, which can be done right away without such risk.

I think the best (at least, most clean) option would be to add variants of `d2i_TYPE*()` that keep the ownership also on error.

## Comment 2939992295

maintainer (MEMBER) · t8m · 2025-06-04T13:12:47Z · https://github.com/openssl/openssl/issues/27736#issuecomment-2939992295

We cannot change the semantics of d2i and I am not sure adding new variants of d2i with different semantics makes much sense.


## Comment 3974876483

other (CONTRIBUTOR) · fwh-dc · 2026-02-27T20:10:58Z · https://github.com/openssl/openssl/issues/27736#issuecomment-3974876483

@DDvO did #27737 resolve this or only partially?

## Comment 3975482659

reporter (CONTRIBUTOR) · DDvO · 2026-02-27T22:26:12Z · https://github.com/openssl/openssl/issues/27736#issuecomment-3975482659

As stated in #27737, it provides a workaround for the use of `d2i_X509_ALGOR()` by `ASN1_item_sign_ctx()` and friends. 
Yet it does not cure `d2i_TYPE*()` themselves.

## Comment 3976435453

other (CONTRIBUTOR) · fwh-dc · 2026-02-28T05:33:02Z · https://github.com/openssl/openssl/issues/27736#issuecomment-3976435453

Ah okay, so to sum up the discussions so far this issue can be resolved by adding variants of d2i*(). But are these functions not deprecated? I see a migration guideline describing how to avoid its use. So effectively the safe variants do exist?

## Comment 3979155729

reporter (CONTRIBUTOR) · DDvO · 2026-03-01T05:29:19Z · https://github.com/openssl/openssl/issues/27736#issuecomment-3979155729

Which migration guidelines do you see as potentially applicable here?
The "migration paths" mentioned in `doc/man3/d2i_RSAPrivateKey.pod` are on a different aspect.
To avoid potential confusion, I've just adapted the title to refer to `d2i_TYPE{,_bio,_fp}()`.

## Comment 3979157191

reporter (CONTRIBUTOR) · DDvO · 2026-03-01T05:30:18Z · https://github.com/openssl/openssl/issues/27736#issuecomment-3979157191

So the issue is about the functions documented in `doc/man3/d2i_X509.pod`.
All these functions are not deprecated.

Their problematic "reuse" behaviour, which is the topic of this issue, is mentioned in the BUGS section there.
It is strongly discouraged to use it, i.e., providing a non-NULL value to the `TYPE *a` parameter should be avoided.
This is what I have done in #27737 for some two specific uses of `d2i_X509_ALGOR`,
but there are many other places that still use a non-NULL `a` argument.

BTW, also the BUGS section of should be cleaned up, in particular its mention of outdated and unclear OpenSSL versions.

## Comment 3983665633

other (CONTRIBUTOR) · fwh-dc · 2026-03-02T11:00:44Z · https://github.com/openssl/openssl/issues/27736#issuecomment-3983665633

Thanks for the summary and clarification! Makes more sense now.
