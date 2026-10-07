# Memory leak on thread exiting

- URL: https://github.com/gramineproject/graphene/issues/1030
- Repo: gramineproject/graphene (language: C)
- State: open; created 2019-09-26T05:20:22Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · yamahata · 2019-09-26T05:20:22Z · https://github.com/gramineproject/graphene/issues/1030

_DkThreadExit() leaks PAL_HANDLE for thread.
shim_async.c also leaks struct shim_thread.

## Comment 535341562

reporter (CONTRIBUTOR) · yamahata · 2019-09-26T05:22:05Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-535341562

Due to subtle memory refernce, probably those memory can not easily freed by the exiting thread itself. Somehow remember it and free(or reuse) it later. Probably on the next thread creation.

## Comment 535354080

other (NONE) · dimakuv · 2019-09-26T06:12:28Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-535354080

+1 for re-using/freeing on the next-thread creation.

## Comment 539879860

other (CONTRIBUTOR) · boryspoplawski · 2019-10-09T07:41:10Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-539879860

@yamahata Could you point where exactly `struct shim_thread` leaks in `shim_async.c` ?

## Comment 540149920

reporter (CONTRIBUTOR) · yamahata · 2019-10-09T19:19:40Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-540149920

It's not LibOS, but Pal/Linux.
_DkThreadExit().
free(handle->thread.stack) is actually nop.
handle isn't freed.

## Comment 540733009

other (CONTRIBUTOR) · boryspoplawski · 2019-10-10T19:07:35Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-540733009

Yeah, I agree on that one, but what about 

>  shim_async.c also leaks struct shim_thread.

## Comment 541136641

reporter (CONTRIBUTOR) · yamahata · 2019-10-11T16:37:58Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-541136641

my bad, I scratch it. I missed put_thread() at the  end of shim_async_helper().


## Comment 561973870

other (NONE) · dimakuv · 2019-12-05T05:20:03Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-561973870

Just a note: `shim_thread` objects were leaked for "normal" threads. Even though these threads went through cleanup in LibOS's `thread_exit()` and their stacks were removed in PAL's `DkThreadExit()`, their `shim_thread`s still leaked.

My PR https://github.com/oscarlab/graphene/pull/1199 removes this leak.

## Comment 879950108

other (NONE) · dimakuv · 2021-07-14T14:38:51Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-879950108

It looks like  the memory leak of PAL handle in `_DkThreadExit()` is still there.

This is how it is created in both PALs:
- https://github.com/oscarlab/graphene/blob/af2f7809b36945382a535f95c2af7a2b32a2059a/Pal/src/host/Linux-SGX/db_threading.c#L97
- https://github.com/oscarlab/graphene/blob/4f0927ff993c9e34aa20d6bad93fad47e2daa2ef/Pal/src/host/Linux/db_threading.c#L147

And there is no free of the PAL handle on thread exit:
- https://github.com/oscarlab/graphene/blob/af2f7809b36945382a535f95c2af7a2b32a2059a/Pal/src/host/Linux-SGX/db_threading.c#L151
- https://github.com/oscarlab/graphene/blob/4f0927ff993c9e34aa20d6bad93fad47e2daa2ef/Pal/src/host/Linux/db_threading.c#L191

## Comment 879950816

other (NONE) · dimakuv · 2021-07-14T14:39:40Z · https://github.com/gramineproject/graphene/issues/1030#issuecomment-879950816

This is a very small memory leak (hundred bytes for each thread?), so the priority is low.
