# Memory leak on realloc failure in iccp_cmd_show.c - 8 identical instances

- URL: https://github.com/sonic-net/sonic-buildimage/issues/28696
- Repo: sonic-net/sonic-buildimage (language: C)
- State: open; created 2026-07-30T01:04:19Z; status ok; passes main

## Issue body

reporter (NONE) · dhruthan · 2026-07-30T01:04:19Z · https://github.com/sonic-net/sonic-buildimage/issues/28696

### Is it platform specific

generic

### Importance or Severity

Medium

### Description of the bug

Eight dump functions in `src/iccpd/src/iccp_cmd_show.c` use the classic unsafe realloc
pattern where the return value of realloc is assigned directly to the same pointer.
If realloc fails and returns NULL, the original pointer is overwritten and the previously
allocated memory is permanently leaked.

Vulnerable pattern (line 138, repeated at 203, 268, 335, 487, 596, 680, 804):
```c
state_buf = (char*)realloc(state_buf, state_buf_size);
if (!state_buf)
    return EXEC_TYPE_FAILED;  // original memory is leaked - no pointer to free it
```

Affected functions:
1. `iccp_mclag_config_dump` (line 138)
2. `iccp_arp_dump` (line 203)
3. `iccp_ndisc_dump` (line 268)
4. `iccp_mac_dump` (line 335)
5. `iccp_local_if_dump` (line 487)
6. `iccp_local_if_dump` unique_ip section (line 596)
7. `iccp_peer_if_dump` (line 680)
8. `iccp_unique_ip_if_dump` (line 804)

Fix for all 8 locations:
```c
char *new_buf = (char*)realloc(state_buf, state_buf_size);
if (!new_buf) {
    free(state_buf);
    return EXEC_TYPE_FAILED;
}
state_buf = new_buf;
```

### Steps to Reproduce

1. Review src/iccpd/src/iccp_cmd_show.c lines 138, 203, 268, 335, 487, 596, 680, 804
2. Each location uses: buf = realloc(buf, new_size) - original pointer lost on failure
3. Run cppcheck: `cppcheck --enable=all -I src/iccpd/include src/iccpd/src/iccp_cmd_show.c`
4. cppcheck reports: "Common realloc mistake: 'state_buf' nulled but not freed upon failure"

### Actual Behavior and Expected Behavior

Actual: If realloc fails under memory pressure (large MCLAG deployments with many
MAC entries), the original buffer pointer is lost and memory is permanently leaked.
Repeated failures cause unbounded memory growth in the iccpd daemon.

Expected: Original buffer should be freed before returning on realloc failure.

### Relevant log output

```shell

```

### Output of `show version`, `show techsupport`

```shell

```

### Attach files (if any)

_No response_

## Comment 5268972167

maintainer (COLLABORATOR) · gechiang · 2026-08-12T15:35:36Z · https://github.com/sonic-net/sonic-buildimage/issues/28696#issuecomment-5268972167

To be reviewed by the new security working group.
