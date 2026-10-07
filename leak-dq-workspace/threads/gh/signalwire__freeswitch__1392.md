# fs_cli socket leak when FreeSWITCH is restarted

- URL: https://github.com/signalwire/freeswitch/issues/1392
- Repo: signalwire/freeswitch (language: C)
- State: open; created 2021-10-20T13:22:21Z; status ok; passes offcwe

## Issue body

reporter (NONE) · adrien-martin · 2021-10-20T13:22:21Z · https://github.com/signalwire/freeswitch/issues/1392

**Describe the bug**
When FreeSWITCH restarts fs_cli can reconnect with the -R option.
In this case the old sockets are not closed and stay in state CLOSE-WAIT.

**To Reproduce**
1. `fs_cli -R`
2. restart FreeSWITCH
3. `ss -ntp dport = 8021`

**Expected behavior**
Old sockets are closed.

**Package version or git hash**
 - `1.10.6~release~18~1ff9d0a60e~buster-1~buster+1` (from files.freeswitch.org/repo/deb/debian-release/)
