# Memory leak when writing to a fetch request in stream

- URL: https://github.com/cloudflare/workerd/issues/5665
- Repo: cloudflare/workerd (language: C++)
- State: open; created 2025-12-09T18:33:46Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ceifa · 2025-12-09T18:33:46Z · https://github.com/cloudflare/workerd/issues/5665

I'm not sure if should be an issue on this repo or workers-sdk.

### Versions

wrangler 4.53.0, Windows 11

### How to reproduce

Create a worker with the following code on the fetch handler:

```typescript
const { readable, writable } = new TransformStream<Uint8Array>();
const writer = writable.getWriter();

const responsePromise = fetch('https://reqbin.com/echo/post/json', {
	method: 'POST',
	headers: {
		'Content-Type': 'application/json',
		'User-Agent': 'PostmanRuntime/7.49.1',
	},
	body: readable,
});

const encoder = new TextEncoder()

for (let i = 0; i < 1000000000; i++) {
	await writer.ready;
	await writer.write(encoder.encode(JSON.stringify({ hello: 'world' })));
	await new Promise((resolve) => setTimeout(resolve, 1));
}

await writer.close();

const response = await responsePromise;
if (!response.ok) {
	return new Response(`Upstream server responded with ${response.status}`, { status: 502 });
}

return response;
```

I expect it to stream to run clean in terms of memory, keep streaming to network and doesn't hold any value, but what is happening is, after some iterations, it keeps growing in memory, and if I take a heap snapshot I can see a lot of promises created that never resolves. Can that be related to https://github.com/cloudflare/workerd/pull/4344 @danlapid @anonrig ?

It looks like a memory leak on workerd, I cannot reproduce it with node with the exact same code (and duplex: 'half' on fetch init).

## Comment 3639436283

maintainer (COLLABORATOR) · jasnell · 2025-12-11T00:03:07Z · https://github.com/cloudflare/workerd/issues/5665#issuecomment-3639436283

I'm not able to reproduce any memory leak with that code. When taking a heap snapshot before the request, then another after the request completes, this is what I'm seeing locally:

<img width="904" height="563" alt="Image" src="https://github.com/user-attachments/assets/fde84fb4-9f6a-4c39-89c6-fa824952cf6c" />

Note there are no promises retained, and no other objects retained that would indicate a leak. I also took an allocation timeline profile on the same request and it did not reveal a leak.

What I do notice is that after a while, the length of time between GC's grows, which can account for the increase in memory as the loop continues. Because of the differences in when/how exactly we run GC (we don't use multi-threaded GC the way Node.js does) is there may be some heuristic at play within V8 to cause the GC's to become less frequent based on how the code is behaving. That's just a guess tho. We can ask @erikcorry or @dcarney-cf for opinions here on what may be happening.

Overall tho, based on the heap snapshot (which I ran three times to be sure), I'm not seeing a memory leak.

## Comment 3641138031

other (CONTRIBUTOR) · dcarney-cf · 2025-12-11T09:54:43Z · https://github.com/cloudflare/workerd/issues/5665#issuecomment-3641138031

There are a number of heuristics in play here. it's possible that new space grows to accommodate the throughput, which would reduce frequency of scavenges, etc. Also, if objects are leaking into old space it might be growing to accommodate and compacting less frequently but the code doesn't look like it should be doing that unless whatever is reading the bytes from the socket is slowed down somehow and writes are happening but the resulting reads are causing a backup, pushing stuff into old space? It's all just guesswork without a repro.

## Comment 3644712904

reporter (NONE) · ceifa · 2025-12-12T03:08:38Z · https://github.com/cloudflare/workerd/issues/5665#issuecomment-3644712904

After the request completes, memory is collected correctly. The bug only manifests **during** the request lifecycle, so the heap snapshot must be taken before the request finishes.

Below is a comparison screenshot showing:

* **Wrangler (top):** request on worker running for ~1 minute
* **Node.js (bottom):** request on process running for ~3 minutes

<img width="1915" height="528" alt="Image" src="https://github.com/user-attachments/assets/2d274004-22f2-4739-ab85-e98c4326a828" />

In this example, the worker is retaining a large number of promises while the request is still in progress.

Minimal reproducible example:
[https://github.com/ceifa/cf-workers-heap-bug](https://github.com/ceifa/cf-workers-heap-bug)

While the impact is limited in this minimal repro, the issue is significant in my production code, which processes hundreds of thousands of items. In that scenario, the worker frequently hits the **128 MB memory limit** due to retained promises, whereas the same code running on Node.js remains stable at ~40 MB.

Also, @jasnell, how can I generate an allocation timeline profile using wrangler? The chrome inspector only shows option to take the heap snapshot.


## Comment 3655259358

reporter (NONE) · ceifa · 2025-12-15T12:05:08Z · https://github.com/cloudflare/workerd/issues/5665#issuecomment-3655259358

Inspecting more the snapshot I could see that a big part of the promises are coming from `ValueQueue::ReadRequest`.

## Comment 3656873483

maintainer (COLLABORATOR) · jasnell · 2025-12-15T17:46:43Z · https://github.com/cloudflare/workerd/issues/5665#issuecomment-3656873483

Ok, it's not a memory leak then if the memory is getting cleaned up once the request completes. The issue is just that this particular usage is create a large amount of interim promises and associated overhead that causes the memory limit to be exceeded. That's the memory limit enforcement working as designed. 

Given that you're iterating 1,000,000,000 times on the write:

```
for (let i = 0; i < 1000000000; i++) {
	await writer.ready;
	await writer.write(encoder.encode(JSON.stringify({ hello: 'world' })));
	await new Promise((resolve) => setTimeout(resolve, 1));
}
```

Since the default high water mark is 1 for `TransformStream`, this loop is going to create a minimum of 4,000,000,000 individual Promises.

Your loop is generating 17,000,000,000 bytes of data, which is chunked out in 4096 byte chunks by default, which means the read loop is going to generate a minimum of somewhere around 8,300,782 promises at the least (more if we factor in the additional promises created internally by the runtime to operate.

Each individual promise is around 48 bytes in memory. So your sample here, just in terms of promises created, is generating something like 1503x more memory than the 128 MB memory limit allows in total without even considering the data allocations. Obviously these aren't all head in memory at the same time, but it means that the example is going to be constantly pushing or exceeding the memory limit.

Node.js' garbage collection works differently than in workers. Node.js uses multi-threaded GC while workers uses single threaded. The GC runs at different times and in workers objects can pile up a bit more between GC runs, which accounts for the differences you're seeing in the profiles.

It would be a memory leak only if the memory was not being reclaimed. This is a case where memory reclamation is not working as efficiently/effectively due to the single-threaded GC configuration and the other architectural differences of the runtimes. We can/will explore improvements but there's no quick fix.


## Comment 3657252324

reporter (NONE) · ceifa · 2025-12-15T19:29:45Z · https://github.com/cloudflare/workerd/issues/5665#issuecomment-3657252324

Thanks for the detailed explanation, @jasnell, I now understand this is due to the architectural differences between workerd and Node.js's, rather than an actual leak.

To give more context on my use case: I need to fetch large amounts of data from one service and stream it to another service's request body. My initial approach was straightforward streaming, read from the source and pipe to the destination. I assumed this would be memory-efficient since I'm checking for backpressure. Taking heap snapshots (which forces GC) showed retained promises, something that doesn't occur with the same pattern in Node.js, that's why I initially described it as a "memory leak."

That said, I'm still looking for a practical solution. Given these limitations, what would be the recommended approach to reliably handle this streaming pattern in Workers? Increasing the highWaterMark doesn't seem like a viable solution since it would just trade promise overhead for higher memory usage in the buffer.

Are there any other patterns or workarounds you'd suggest for high-throughput streaming scenarios like this?
