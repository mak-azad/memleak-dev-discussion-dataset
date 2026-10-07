# socket leak with local nginx proxy used by listener_add

- URL: https://github.com/karlheyes/icecast-kh/issues/444
- Repo: karlheyes/icecast-kh (language: C)
- State: open; created 2024-01-25T09:44:26Z; status ok; passes offcwe

## Issue body

reporter (NONE) · joulaud · 2024-01-25T09:44:26Z · https://github.com/karlheyes/icecast-kh/issues/444

With icecast-kh22 we observed that the metrics global.clients goes up and does not come back to initial value when listeners are disconnecting. This happens only when the activity is high (hundreds of new connections per second). At some point all new connections are (correctly) refused with a 403 (`connection/_handle_get_request server client limit reached`).

Thinking it was perhaps a problem with the counter global.clients tried to workaround by increasing the limit "clients" to an arbitrary insanely high value but this caused some system saturation of fd and caused more problems.

We observed in this case a big discrepancy between the count of TCP alloc (which climbs insanely high) and of TCP inuse (which stays near what we could expect), reinforcing the idea that some leak in socket management occurs in icecast-kh.

Configuration includes something like
```
  <mount>
    <mount-name>/*.mpeg3</mount-name>
    <authentication type="url">
      <option name="listener_add" value="http://localhost/proxyurl"/>
      <option name="timeout" value="99"/>
      <option name="presume_innocent" value="yes"/>
    </authentication>
  </mount>
  ```

We did not reproduce the problem without this configuration.

The same configuration with icecast-kh15 does not seem to have the same problem.
