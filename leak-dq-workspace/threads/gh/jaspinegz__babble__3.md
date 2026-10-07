# Memory leaks

- URL: https://github.com/jaspinegz/babble/issues/3
- Repo: jaspinegz/babble (language: C)
- State: open; created 2020-02-27T11:10:25Z; status ok; passes main

## Issue body

reporter (OWNER) · jaspinegz · 2020-02-27T11:10:25Z · https://github.com/jaspinegz/babble/issues/3

A big problem with the library is the concept of caching. Discord bot libraries are expected to cache everything it is reasonable to cache - guilds, channels, messages, etc. Caching is hard, but even without considering the implementation there are immediate problems with respect to when these objects are freed.

Assume an event handler exists...
```c
 void on_message(message_t* message) {
  //do something with message
}
```
...who is responsible for freeing this `message_t` struct?
- Is it the user? It's quite easy to assert that the user can't be responsible because there can be multiple handlers to one event. If the pointer to `message_t` is freed here, any subsequent handler executions may cause a seg. fault. The library also can't cache this message.
- Is it the library? If the library is responsible, then what if the user wants to keep hold of this `message_t` pointer i.e. store a `last_message` global variable. The user can't safely use this pointer since the library's caching implementation may choose to free it at any arbitrary time in the future. With that in mind, how can the user even use this `message` pointer during the execution of the handler, given the caching implementation could reasonably be running on a separate thread to the ws event handler?

**Partial solution:** During the execution of a handler function, the cache is locked.

This is only relevant if the cache is on a different thread to websocket handlers. But what about if the user wants to keep the pointer? I've considered the concept of allowing the user to "steal" the pointer from the library:

```c
message_t* last_message;

void on_message(message_t* message) {
  take_entity_ownership(message);
  last_message = message;
}
```

However, now the user has the capacity to free the pointer before it is given to subsequent handlers _and_ the library loses the ability to cache this message. Instead, I think this is most reasonable:

```c
void on_message(const message_t* message) {
  last_message = clone_message(message);
}
// some time later ...
free_message(last_message);
```

Both `clone_message` and `free_message`have to be implemented in the same way as `parse_message` and `compose_message` (private functions in `json.c`) because both require handling each attribute of `message_t`. In this case the user is trusted to not `free(message)` for performance (don't copy `message` if unnecessary). They are responsible for freeing any pointer returned by a `clone_*` function call.
