# Memory Leak

- URL: https://github.com/cameron314/concurrentqueue/issues/364
- Repo: cameron314/concurrentqueue (language: C++)
- State: open; created 2023-10-17T15:02:41Z; status ok; passes main

## Issue body

reporter (NONE) · tolgatanriverdi · 2023-10-17T15:02:41Z · https://github.com/cameron314/concurrentqueue/issues/364

Hi
Sorry for the previous issue(mistakenly opened with a wrong user)

We are using concurrentqueue in our trading application for transfering data between threads, and we are very pleased about the performance of this queue.
However there is a significant memory leak problem in the library, We are transferring all market data from 1 producer to multiple consumers(approx 2-3 consumers) but creating 10,15 different queues and when we do that the memory usage increases 10mb in every 1 seconds, so at the end of the day we are consuming at least 200-300gb of memory.
When we remove the concurrentqueue and replace it with intel tbb concurrent queue library, memory leak dissapears.
Here is how we use the concurrentqueue:  (We also have the same problem on spsc queue)  . I'm also attaching the memory usage of our server when we continously use the concurrentqueue (In the graph at the time 16.00 and 17.00 we restarted the app)



```
#pragma once

#include <memory>
#include "IdGenerator.h"
#include "../Globals/Enumarations.h"
#include "../Containers/concurrentqueue.h"

template<class T = char*, class L = moodycamel::ConcurrentQueue<T>>

class Subscriber: private IdGenerator {
public:
	Subscriber() : id(++idGenerater) {
	}
	virtual ~Subscriber(){
	}

	void add(const T& message) {
		messageList.enqueue(message);
	}
	bool tryPop(T& item) {
		return messageList.try_dequeue(item);
	}
	L& getList() {
		return messageList;
	}
	unsigned short getId()const {
		return id;
	}
	void clear()
	{
	}
protected:
	const short id;
	L messageList;
};

template<class T, class L> using SubscriberPtr = std::shared_ptr<Subscriber<T, L>>;
```


<img width="714" alt="memory" src="https://github.com/cameron314/concurrentqueue/assets/1306155/58228248-fe6b-4bb3-ad4b-36515eae4da1">


## Comment 1766610121

maintainer (OWNER) · cameron314 · 2023-10-17T15:05:18Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-1766610121

Copying my questions here:

Are the consumers keeping up with the producers? Are there many temporary threads enqueueing elements? Is this reproducible with the latest version of the queue?

Also, 100 MB per second is 360 GB per hour, but only 200 GB are in use at the end of the day. Are you sure this is a leak and not just the peak memory usage? (The queue recycles memory internally but never returns it to libc/the OS until destruction).

## Comment 1766613510

maintainer (OWNER) · cameron314 · 2023-10-17T15:06:59Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-1766613510

My SPSC implementation (ReaderWriterQueue) is completely different. The only thing in common is that it reuses memory internally as well, only releasing it on destruction. So that could be the reason?

## Comment 1766626993

reporter (NONE) · tolgatanriverdi · 2023-10-17T15:14:05Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-1766626993

Edited my original post, there were some mistakes in the logic I want to describe.
As you see in the code this is a subscriber class and this instance (with the queue inside of it) created everytime a subscriber is created and generally its between 15-20 instances in our application and that means there are 15-20 concurrentqueues and each of them works as  single producer - multiple consumer

## Comment 1766679873

other (NONE) · erenkal · 2023-10-17T15:40:02Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-1766679873

I have a similar problem,

Here is a sample code. Memory usage is increasing all the time.  


```
#include <iostream>
#include "concurrentqueue.h"

int main() {
  moodycamel::ConcurrentQueue<std::string> queue{1000};
  auto producer = [&queue]() {
    while (true) {
      std::string message = "Hello" + std::to_string(rand()%1000000);
      queue.enqueue(message);
    }
    std::cout << "Producer finished" << std::endl;
  };

  auto consumer = [&queue]() {
    while (true) {
      std::string message;
      if (queue.try_dequeue(message)) {
//        std::cout << message << std::endl;
      }
    }
  };

  std::thread producerThread(producer);
  std::thread consumerThread(consumer);

  producerThread.detach();
  consumerThread.detach();

  while (true)
    std::this_thread::sleep_for(std::chrono::seconds(1));

  return 0;


}
```

## Comment 1766685096

maintainer (OWNER) · cameron314 · 2023-10-17T15:42:27Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-1766685096

@erenkal, there's no backpressure in that example. If enqueueing is even slightly faster than dequeueing on average, the queue's size will grow indefinitely.

## Comment 1766691036

maintainer (OWNER) · cameron314 · 2023-10-17T15:45:39Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-1766691036

@tolgatanriverdi, what are the queues' sizes before shutting down? And how many different threads call add?

## Comment 2212960234

other (NONE) · Toby-Shi-cloud · 2024-07-08T03:56:44Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2212960234

the enqueue operator seems significantly faster than dequeue. Is this true?

## Comment 2212972873

maintainer (OWNER) · cameron314 · 2024-07-08T04:03:42Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2212972873

That depends on a lot of factors, but often yes.

## Comment 2401294270

other (NONE) · 396848385 · 2024-10-09T04:33:24Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2401294270

@cameron314 I have encountered a similar problem, and based on your previous analysis, it is likely due to the fact that consumers' consumption speed cannot keep up with producers' production speed, resulting in infinite growth of elements in the queue and rapidly reaching memory overflow;

From the source code, it can be seen that the capacity passed in when creating a blocking queue is not the fixed capacity of the queue, but only the portion that can be used without allocating memory.

So I would like to ask if there is a way to truly limit the capacity of the queue, such as blocking when the producer's production data reaches the capacity of the queue, instead of performing an unrestricted enqueue operation.

## Comment 2402388030

maintainer (OWNER) · cameron314 · 2024-10-09T13:42:17Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2402388030

You can configure a max sub-queue size in the traits, but there is no blocking-enqueue version. Consider using a semaphore.

## Comment 2403864909

other (NONE) · 396848385 · 2024-10-10T03:28:36Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2403864909

“configure a max sub-queue size in the traits“  If this method reaches the maximum size, the elements will be discarded instead of blocking until they can be enqueued. The scenario we are using does not allow element dropout

## Comment 2403941597

other (NONE) · 396848385 · 2024-10-10T04:24:36Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2403941597

@cameron314 
while(!(channel->try_enqueue(local_data))) {
 continue;
}
Can I achieve a certain degree of blocking the enqueue effect through this method? Will it have a significant overhead on performance or CPU.

## Comment 2403952451

maintainer (OWNER) · cameron314 · 2024-10-10T04:28:47Z · https://github.com/cameron314/concurrentqueue/issues/364#issuecomment-2403952451

That's called spin-waiting, and can make sense in certain cases, but will definitely cost CPU cycles. Only do this if you're certain you have more hardware cores than threads ready to run.
