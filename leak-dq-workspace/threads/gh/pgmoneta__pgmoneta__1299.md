# heap-use-after-free when a server with backups is followed by a server without

- URL: https://github.com/pgmoneta/pgmoneta/issues/1299
- Repo: pgmoneta/pgmoneta (language: C)
- State: open; created 2026-09-11T17:32:06Z; status ok; passes offcwe

## Issue body

reporter (CONTRIBUTOR) · LoayTarek5 · 2026-09-11T17:32:06Z · https://github.com/pgmoneta/pgmoneta/issues/1299

**Describe the bug**

I noticed that `pgmoneta-cli status details` reads freed memory when a server with at least one backup is followed by a server with no backups.
 
i tried to investigate, i see that `status.c` always emits the `Backups` key, but for a server with no backups the object is still `JSONUnknown` (it renders as `Backups: {}`), and `pgmoneta_json_iterator_create()` rejects that object in `json.c` file and returns `1` without assigning `*iter`. also in `translate_json_object()` the return value is unchecked in `cli.c` file, and `backup_it` is declared outside the server loop in `cli.c`, so i think it still points at the iterator destroyed in cli.c at around 3349 line for the previous server, then dereferences it.
 
so i think, if i understand it correctly that reversing the server order avoids it, since `backup_it` is still `NULL` at that point.
 

**To Reproduce**

One PostgreSQL cluster is enough, the second server never needs to be reachable.
 
1-Configure two servers in this order: a working one, and a throwaway one on a port where nothing listens (see Configuration). The throwaway section still needs a `wal_slot`
2-ofcourse start pgmoneta.
3-`pgmoneta-cli -c pgmoneta_cli.conf backup primary`
4-`pgmoneta-cli -c pgmoneta_cli.conf status details`

but the step 4 reads freed memory, also before step 3, with both servers at zero backups, it completes normally.


**Version**

0.22.0, main

**PostgreSQL**

17.11

**libev**

1:4.33-2.1build1

**OpenSSL**

3.0.13

**OS**

Pop!_OS 24.04 LTS

**Configuration**
 
* pgmoneta.conf
```
[pgmoneta]
host = localhost
metrics = 0
 
base_dir = /path/to/backup
 
compression = zstd
retention = 7
 
log_type = file
log_level = info
log_path = /path/to/pgmoneta.log
 
unix_socket_dir = /path/to/sock/
 
[primary]
host = localhost
port = 5432
user = repl
wal_slot = repl
create_slot = yes
 
[foo]
host = localhost
port = 5999
user = repl
wal_slot = foo
```
 
**Debug logs**
 
The fault is in `pgmoneta-cli` after the response is received, so the server side logs nothing unusual. AddressSanitizer report from step 4:
 
```
==10405==ERROR: AddressSanitizer: heap-use-after-free on address 0x503000001ae0
READ of size 8 at 0x503000001ae0 thread T0
    #0 pgmoneta_json_iterator_next  src/libpgmoneta/json.c:577:30
    #1 translate_json_object        src/cli.c:3344:26
    #2 process_result               src/cli.c:2056:7
    #3 details                      src/cli.c:1581:8
    #4 main                         src/cli.c:984:19
 
0x503000001ae0 is located 0 bytes inside of 32-byte region [0x503000001ae0,0x503000001b00)
 
freed by thread T0 here:
    #0 free
    #1 pgmoneta_json_iterator_destroy  src/libpgmoneta/json.c:570:4
    #2 translate_json_object           src/cli.c:3349:19
    #3 process_result                  src/cli.c:2056:7
    #4 details                         src/cli.c:1581:8
    #5 main                            src/cli.c:984:19
 
previously allocated by thread T0 here:
    #0 malloc
    #1 pgmoneta_json_iterator_create  src/libpgmoneta/json.c:540:8
    #2 translate_json_object          src/cli.c:3343:19
    #3 process_result                 src/cli.c:2056:7
    #4 details                        src/cli.c:1581:8
    #5 main                           src/cli.c:984:19
 
SUMMARY: AddressSanitizer: heap-use-after-free src/libpgmoneta/json.c:577:30 in pgmoneta_json_iterator_next
```
 
also libc frames and shadow bytes trimmed, full report available if useful.

I can work on it, if it is ok
