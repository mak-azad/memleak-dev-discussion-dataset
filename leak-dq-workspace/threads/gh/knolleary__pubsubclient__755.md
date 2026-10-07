# Memory leak in PubSubClient::setBufferSize

- URL: https://github.com/knolleary/pubsubclient/issues/755
- Repo: knolleary/pubsubclient (language: C++)
- State: open; created 2020-07-02T10:32:27Z; status ok; passes main

## Issue body

reporter (NONE) · gudnimg · 2020-07-02T10:32:27Z · https://github.com/knolleary/pubsubclient/issues/755

There is a memory leak in line 752 in PubSubClient.cpp. I can't say I understand the code but when I use Check feature in PlatformIO, it reports this leak.

```c
boolean PubSubClient::setBufferSize(uint16_t size) {
    if (size == 0) {
        // Cannot set it back to 0
        return false;
    }
    if (this->bufferSize == 0) {
        this->buffer = (uint8_t*)malloc(size);
    } else {
        uint8_t* newBuffer = (uint8_t*)realloc(this->buffer, size);
        if (newBuffer != NULL) {
            this->buffer = newBuffer;
        } else {
            return false; // this is line 752
        }
    }
    this->bufferSize = size;
    return (this->buffer != NULL);
}
```

## Comment 652927965

maintainer (OWNER) · knolleary · 2020-07-02T10:34:00Z · https://github.com/knolleary/pubsubclient/issues/755#issuecomment-652927965

You'll have to give a bit more information then that.

What is the actual message from PlatformIO?

Have you observed an actual leak?

## Comment 652930967

reporter (NONE) · gudnimg · 2020-07-02T10:40:59Z · https://github.com/knolleary/pubsubclient/issues/755#issuecomment-652930967

Message from PlatformIO: _include\PubSubClient.cpp:752: [high:error] Memory leak: newBuffer [memleak]_

No I haven't observed an actual leak, just noticed this message when trying to debug my own code.

![image](https://user-images.githubusercontent.com/8218499/86349312-69ffd180-bc50-11ea-9244-d0b0bca1f102.png)


## Comment 652932012

maintainer (OWNER) · knolleary · 2020-07-02T10:43:16Z · https://github.com/knolleary/pubsubclient/issues/755#issuecomment-652932012

Hmm, I'm not entirely sure how that can leak. We only go to line 752 if `newBuffer` is `NULL`. I don't use PlatformIO, so I don't know what it is doing to analyse the source code. But I *think* its a false positive.

## Comment 652971769

reporter (NONE) · gudnimg · 2020-07-02T12:18:15Z · https://github.com/knolleary/pubsubclient/issues/755#issuecomment-652971769

Interesting if I add `free(newBuffer);` PlatformIO no longer reports a leak. 

```c
boolean PubSubClient::setBufferSize(uint16_t size) {
    if (size == 0) {
        // Cannot set it back to 0
        return false;
    }
    if (this->bufferSize == 0) {
        this->buffer = (uint8_t*)malloc(size);
    } else {
        uint8_t* newBuffer = (uint8_t*)realloc(this->buffer, size);
        if (newBuffer != NULL) {
            this->buffer = newBuffer;
        } else {
            free(newBuffer); // <---
            return false;
        }
    }
    this->bufferSize = size;
    return (this->buffer != NULL);
}
```

As I am trying to undestand this, the documentation at cppreference (https://en.cppreference.com/w/c/memory/realloc) mentions this:

> On failure, returns a null pointer. The original pointer ptr remains valid and **may need to be deallocated with free()** or realloc()

This makes me think that `this->buffer` needs to be freed in the else statement. But PlatformIO will still see the memory leak due to newBuffer.

```c
boolean PubSubClient::setBufferSize(uint16_t size) {
    if (size == 0) {
        // Cannot set it back to 0
        return false;
    }
    if (this->bufferSize == 0) {
        this->buffer = (uint8_t*)malloc(size);
    } else {
        uint8_t* newBuffer = (uint8_t*)realloc(this->buffer, size);
        if (newBuffer != NULL) {
            this->buffer = newBuffer;
        } else {
            free(this->buffer); // <---
            return false;
        }
    }
    this->bufferSize = size;
    return (this->buffer != NULL);
}
```

I am just going to assume this is a false positive as you say :)

## Comment 653752201

other (NONE) · OBorce · 2020-07-04T11:05:50Z · https://github.com/knolleary/pubsubclient/issues/755#issuecomment-653752201

it is a false positive.
