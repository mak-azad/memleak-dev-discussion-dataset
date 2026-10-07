# pool collect memory leak

- URL: https://github.com/krakjoe/pthreads/issues/875
- Repo: krakjoe/pthreads (language: C)
- State: open; created 2018-06-07T16:46:52Z; status ok; passes offcwe

## Issue body

reporter (NONE) · BoltUser · 2018-06-07T16:46:52Z · https://github.com/krakjoe/pthreads/issues/875

Hi,
on the following code : 
```
$pool = new Pool(5, Worker::class);
while (true) {
    $i++;
    try {
        $message = new Message($receiver->recv());
        $messages[] = $message;
        if ($i ==5) {
            for ($th = 0; $th < 5; $th++) {
                $pool->submit(new DispatcherQueueWorker($messages[$th]));
            }
            //while ($pool->collect()) ;
            $pool->collect();
            $i = 0;
            unset($messages);
        }
        usleep(1000);
    } catch (ZMQException $e) {
        $pool->shutdown();
        die();
    }

```
the memory increase because in run method on DispatcherQueueWorker i have a simple getmxrr(), if i try to change with :

`while ($pool->collect()) ;`

i dont have memory leaks, but the script wait every time that all worker are finished. 
This is not good for my application, because if a have a worker blocked with 60 seconds of response, all workers are waiting that only 1 or two worker finishing.

is possible to have a situation without memory leaks but with all workers that work indipendently, without waiting others?

## Comment 462940881

other (NONE) · joeyhub · 2019-02-12T21:23:34Z · https://github.com/krakjoe/pthreads/issues/875#issuecomment-462940881

How are you determining that there's a memory leak? You need to enable the gc in php for cyclicle collection.

## Comment 462988671

reporter (NONE) · BoltUser · 2019-02-12T23:41:44Z · https://github.com/krakjoe/pthreads/issues/875#issuecomment-462988671

the GC is already enabled, and the memory leak is on 
stream_socket_client, when you use streams with pthreads you can have 
memory leaks.

At the moment i don't have a solution about this issue.

Il 12/02/2019 21:23, Joey ha scritto:
>
> How are you determining that there's a memory leak? You need to enable 
> the gc in php for cyclicle collection.
>
> —
> You are receiving this because you authored the thread.
> Reply to this email directly, view it on GitHub 
> <https://github.com/krakjoe/pthreads/issues/875#issuecomment-462940881>, 
> or mute the thread 
> <https://github.com/notifications/unsubscribe-auth/AgdL1ZrU7DZKRWwZQ2k3C6233xYlXWdwks5vMzDcgaJpZM4UewuS>.
>


## Comment 463483277

other (NONE) · joeyhub · 2019-02-14T04:18:33Z · https://github.com/krakjoe/pthreads/issues/875#issuecomment-463483277

You might be better of using multiple processes and a more stable async lib instead. I think collect might be an async function. Also that might be old pthreads. I thought collect moved to worker.

## Comment 463484937

other (NONE) · joeyhub · 2019-02-14T04:27:42Z · https://github.com/krakjoe/pthreads/issues/875#issuecomment-463484937

If there's no leak in while then it's just you need to manually gc which is a bit freaky. It doesn't seem like in that case you have a memory leak but you do have much delayed GC. Having it on while will bomb out a CPU core probably. Though it might be worse if your thread fails to fclose. Until collected I'd assume those PHP instances as worker stay open. So if you did fopen but not fclose then that handle will stick around same as in normal PHP.

Additionally do you need Worker here? It looks like instead you can stick to thread. That's not persistent so in theory the php scope should shutdown sooner (though the thread object would want to still be collected I'd guess).

## Comment 463485826

other (NONE) · joeyhub · 2019-02-14T04:33:09Z · https://github.com/krakjoe/pthreads/issues/875#issuecomment-463485826

Move the pool collect somewhere else as well so it runs every second, not every five. You're delaying it worse with that. Also you're wrapping too much with that try catch. Try to only wrap what actually throws the exception. Why even have that? It makes no sense just let the exception propagate up or catch throwable, shutdown the pool then throw it back up. You should almost never use die or exit. Die is the default PHP exception handler so why reimplement that?

## Comment 463597872

reporter (NONE) · BoltUser · 2019-02-14T11:44:53Z · https://github.com/krakjoe/pthreads/issues/875#issuecomment-463597872

Yes in fact at the moment my code is little different, and i have tried with syncronize for some stuff, like update an object shared with other threads (but after 5 minute , the process crash with segfault) for that reason now i have a copy of Data objects for each threads because only one shared object cause a segfault (on update, not on read)!

and all my worker now are in while true, each worker, never die, but the standard streams functions leak with pthreads.

I have tried a new beta implementation of Streams made by @SirSnyder, but i see the same behaviour


Example (Pseudo code)
Main.php:
```php
<?php
$mydataobject = new MyData(); (this object is Volatile!)
$connections= new Connections(); (this object is Volatile!)

$workerPool = new Pool(10,'Worker');
for ($i = 0; $i <= 10; $i++) {
    $workerPool->submit(new DispatcherWorker($mydataobject,$connections));
}
```
------------------------------------------------
DispatcherWorker.php:
```php
<?php
class dispatcherWorker{

private $mydataobject;
private $connections;

public function __construct($mydataobject,$connections){
  $this->mydataobject = $mydataobject;
  $this->connections = $connections;
}

public function run(){
  while(true){
    $this->mydataobject->synchronize(function(){
       $this->mydataobject->updateProperties();
    });

     $slot = $this->getFreeSlot();
     $this->connections[$slot]->connect();
     somestuff...
     $connections[$slot]->disconnect();
     sleep(1);
  }
}
}
```
With this code the syncronize not do lock job, because some times i receive a segfault.

and the streams standard function used on connection, send data, and disconnection leaks.
i think that the problem is on the closing of stream resource, in threads context the stream is not really closed.
