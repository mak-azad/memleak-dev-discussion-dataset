# LeakSanitizer: detected memory leaks

- URL: https://github.com/FairRootGroup/FairMQ/issues/463
- Repo: FairRootGroup/FairMQ (language: C++)
- State: open; created 2023-02-24T12:58:45Z; status ok; passes main

## Issue body

reporter (MEMBER) · dennisklein · 2023-02-24T12:58:45Z · https://github.com/FairRootGroup/FairMQ/issues/463

We often get this on device shutdown, investigate, if this is an issue in our code:
```
Direct leak of 75 byte(s) in 1 object(s) allocated from:
    #0 0x7fa56832d68f in __interceptor_malloc (/lib64/libasan.so.8+0xba68f)
    #1 0x7fa566e801f0 in zmq_msg_init_size (/lib64/libzmq.so.5+0x651f0)
```
examples:
* https://cdash.gsi.de/testDetails.php?test=13584238&build=373072
* https://cdash.gsi.de/viewTest.php?onlyfailed&buildid=373152
* https://cdash.gsi.de/testDetails.php?test=13588357&build=373152
* https://cdash.gsi.de/testDetails.php?test=13588372&build=373152
