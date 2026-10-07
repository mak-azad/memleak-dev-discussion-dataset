# Socket Leak

- URL: https://github.com/sassanp/pynetinfo/issues/1
- Repo: sassanp/pynetinfo (language: C)
- State: open; created 2012-02-15T05:16:35Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ZachGoldberg · 2012-02-15T05:16:35Z · https://github.com/sassanp/pynetinfo/issues/1

Everytime I call netinfo.list_active_devs() approximately 15 sockets are leaked.  I call list_active_devs once every couple of seconds and therefore this causes my application to crash after a few minutes.

```
    devs = netinfo.list_active_devs()
```

Exception: (24, 'Too many open files')
Error in sys.excepthook:
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/apport_python_hook.py", line 59, in apport_excepthook
ImportError: No module named fileutils


## Comment 3975175

reporter (NONE) · ZachGoldberg · 2012-02-15T05:18:06Z · https://github.com/sassanp/pynetinfo/issues/1#issuecomment-3975175

Correction, other netinfo calls also leak sockets.  get_broadcast() being the largest offender I've identified thus far.


## Comment 4546299

reporter (NONE) · ZachGoldberg · 2012-03-16T19:18:21Z · https://github.com/sassanp/pynetinfo/issues/1#issuecomment-4546299

I wrote the following decorator for use around functions that call netinfo (and preferably only netinfo) to cleanup the leaked FDs.

```
def ensure_no_leaked_fds(function):
    def wrapper(*args, **kwargs):
        original_fds = [int(i) for i in os.listdir(
                "/proc/%s/fd/" % os.getpid()) if int(i) > 10]
        retval = function(*args, **kwargs)  
        post_fds = [int(i) for i in os.listdir(
                "/proc/%s/fd/" % os.getpid()) if int(i) > 10]
        new_fds = set(post_fds) - set(original_fds)
        for fd in new_fds:
            try:
                f = os.fdopen(fd)
                f.close()
            except:
                pass
        return retval
    return wrapper
```


## Comment 5060077

maintainer (OWNER) · sassanp · 2012-04-11T00:55:30Z · https://github.com/sassanp/pynetinfo/issues/1#issuecomment-5060077

Hi Zach,

Thanks for your report, sorry it has taken so long for me to attend to it.
I will hopefully have some time to deal with the issue over the next couple of days.

Thanks
Sassan

