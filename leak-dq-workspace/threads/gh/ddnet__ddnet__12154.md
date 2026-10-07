# Cppcheck: possible memory leak on realloc failure

- URL: https://github.com/ddnet/ddnet/issues/12154
- Repo: ddnet/ddnet (language: C++)
- State: open; created 2026-05-08T11:53:03Z; status ok; passes main

## Issue body

reporter (NONE) · OliviaDavidescu · 2026-05-08T11:53:03Z · https://github.com/ddnet/ddnet/issues/12154

Cppcheck reports several instances of unsafe realloc usage where the return value is assigned directly to the original pointer.

Affected locations include:

src/base/io.cpp
src/engine/shared/http.cpp

Example pattern:

buffer = (char *)realloc(buffer, new_size);

If realloc fails, it returns nullptr and the original allocation is lost, which may lead to a memory leak and potential null dereference later in execution.

Suggested fix is to store the result in a temporary pointer before overwriting the original pointer.

I found this while performing static analysis on DDNet using Cppcheck for a university project. I can also submit a PR with fixes if this issue is considered valid.

## Comment 4407027965

maintainer (MEMBER) · heinrich5991 · 2026-05-08T14:05:20Z · https://github.com/ddnet/ddnet/issues/12154#issuecomment-4407027965

Hi, thanks for your interest in looking at DDNet code.

In DDNet, we generally don't really handle allocation (or reallocation) failure. The subsequent crash is currently intended or at least tolerated. We basically just pretend that there's always going to be enough RAM.

## Comment 4412181359

maintainer (MEMBER) · Robyt3 · 2026-05-09T09:36:55Z · https://github.com/ddnet/ddnet/issues/12154#issuecomment-4412181359

> The subsequent crash is currently intended or at least tolerated. We basically just pretend that there's always going to be enough RAM.

We could consider adding a wrapper `mem_realloc` that `dbg_assert`s if the allocation failed to make it clear that we accept the crash due to insufficient RAM. But I agree that we generally can't handle memory allocation failure. (I'd only like to properly handle allocation failures in parser code, e.g. #9886.)

## Comment 4412264392

maintainer (MEMBER) · heinrich5991 · 2026-05-09T10:14:43Z · https://github.com/ddnet/ddnet/issues/12154#issuecomment-4412264392

> We could consider adding a wrapper `mem_realloc` that `dbg_assert`s if the allocation failed to make it clear that we accept the crash due to insufficient RAM.

We'd need to also add a wrapper for `malloc`. I wonder if it's theoretically allowed to use `#define`s to override standard library's malloc/realloc so we don't have to go over the whole source. @Learath2 Do you know?

## Comment 4485548606

other (CONTRIBUTOR) · AssassinTee · 2026-05-19T07:47:43Z · https://github.com/ddnet/ddnet/issues/12154#issuecomment-4485548606

I am in favor of robyts proposal, creating memory functions in order to fail gracefully. I'd prefer going over the whole source as this makes clear, that we are using our own memory functions then

## Comment 4487350056

maintainer (MEMBER) · heinrich5991 · 2026-05-19T11:38:57Z · https://github.com/ddnet/ddnet/issues/12154#issuecomment-4487350056

> I am in favor of robyts proposal, creating memory functions in order to fail gracefully. I'd prefer going over the whole source as this makes clear, that we are using our own memory functions then

Sounds good. :)
