# munmap_chunk(): invalid pointer

- URL: https://github.com/hisptoot/BambuSource2Raw/issues/6
- Repo: hisptoot/BambuSource2Raw (language: C)
- State: open; created 2023-07-09T17:54:22Z; status ok; passes main

## Issue body

reporter (NONE) · totalitarian · 2023-07-09T17:54:22Z · https://github.com/hisptoot/BambuSource2Raw/issues/6

Trying to generate the cfg and I get this error, any idea?

```
root@5151c851e8b2:/bambu-bin# ./bambusource2raw gen_cfg -u xxxxx@gmail.com -p xxxxx-r eu -d xxxxx
by hisptoot 2022.12.26
user_name: xxxxx
passwd specified by user
region: eu
dev_id: xxxxx
getting token by login
getting user_id by token
user_id: xxxxx
region: eu user_id: xxxxx dev_id: xxxxx
munmap_chunk(): invalid pointer
Aborted (core dumped)
```

## Comment 1627944764

maintainer (OWNER) · hisptoot · 2023-07-10T01:43:44Z · https://github.com/hisptoot/BambuSource2Raw/issues/6#issuecomment-1627944764

Hello, thank you for reporting the issue.

It seems to be heap corruption or double-free during the final json generation.

If you are familiar with gdb, you can try to compile the program with -g -O0 and run the program with gdb. When the issue happens, run 'bt' cmd in gdb, report the backtrace info to me. 

## Comment 1627969207

maintainer (OWNER) · hisptoot · 2023-07-10T02:10:47Z · https://github.com/hisptoot/BambuSource2Raw/issues/6#issuecomment-1627969207

you can try this linux build (I remove cJSON api from cfg generation).
[bambusource2raw-for-test-2023-07-10.zip](https://github.com/hisptoot/BambuSource2Raw/files/11997091/bambusource2raw-for-test-2023-07-10.zip)


## Comment 1720892058

other (NONE) · skysolf · 2023-09-15T08:34:33Z · https://github.com/hisptoot/BambuSource2Raw/issues/6#issuecomment-1720892058

> you can try this linux build (I remove cJSON api from cfg generation). [bambusource2raw-for-test-2023-07-10.zip](https://github.com/hisptoot/BambuSource2Raw/files/11997091/bambusource2raw-for-test-2023-07-10.zip)

this test file work ok!~!

## Comment 1720939079

other (NONE) · skysolf · 2023-09-15T09:09:01Z · https://github.com/hisptoot/BambuSource2Raw/issues/6#issuecomment-1720939079




> you can try this linux build (I remove cJSON api from cfg generation). [bambusource2raw-for-test-2023-07-10.zip](https://github.com/hisptoot/BambuSource2Raw/files/11997091/bambusource2raw-for-test-2023-07-10.zip)

use this file ,can make a conf file,but also show 
munmap_chunk(): invalid pointer
Aborted (core dumped)

use the conf file run with docker,the log like this:

`<html>
<body>
<!--StartFragment-->

2023/09/15 17:08:15 | stdout | [1;31mfd:: Invalid data found when processing input
-- | -- | --
2023/09/15 17:08:15 | stdout | get_bambu_studio_user_info failed
2023/09/15 17:08:15 | stdout | Parse cfg json failed
2023/09/15 17:08:15 | stdout | getting user info by BambuNetworkEngine.conf
2023/09/15 17:08:15 | stdout | by hisptoot 2022.12.26
2023/09/15 17:08:10 | stdout | wait for 5 seconds
2023/09/15 17:08:10 | stdout | /bambu-bin/cfg /bambu-bin
2023/09/15 17:08:10 | stdout | /bambu-bin /bambu-bin/cfg /bambu-bin
2023/09/15 17:08:10 | stdout | [0mstarting rtsp-simple-server

<!--EndFragment-->
</body>
</html>`

## Comment 1809635461

maintainer (OWNER) · hisptoot · 2023-11-14T06:50:23Z · https://github.com/hisptoot/BambuSource2Raw/issues/6#issuecomment-1809635461

[bambusource2raw-2023-11-14-for-test2.zip](https://github.com/hisptoot/BambuSource2Raw/files/13345422/bambusource2raw-2023-11-14-for-test2.zip)
try this version, check if 'munmap_chunk(): invalid pointer' is fixed

'Parse cfg json failed' is another problem, check if the conf file contains a valid json data.
