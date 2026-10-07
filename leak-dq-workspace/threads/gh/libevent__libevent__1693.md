# New security rules (other type)

- URL: https://github.com/libevent/libevent/issues/1693
- Repo: libevent/libevent (language: C)
- State: open; created 2024-07-13T08:02:35Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · icy17 · 2024-07-13T08:02:35Z · https://github.com/libevent/libevent/issues/1693

Similar to issue #1692 , there are additional types of security rules that are missing in the documentation. I believe incorporating these rules could help developers learn how to correctly use APIs and reduce the risk of security issues.

I will provide a table describing the missing security rules:
| API | parameter index (begin with 1) | Security rules |
|:----------:|:----------:|:----------:|
| event_add | 1 | parameter must not be freed/closed before |
| event_base_dispatch | 1 | parameter must not be freed/closed before |
| evhttp_request_get_connection | 1 | parameter must not be freed/closed before |
| event_base_free | 1 | Parameter 1: Do not call `event_base_free()` multiple times for the same `base` parameter. |
| evhttp_request_free | 1 | "Parameter 1: `req` (evhttp_request) - The caller MUST NOT call `evhttp_request_free` multiple times consecutively for the same `evhttp_request` object. |
| evhttp_uri_free | 1 |  The caller of the API must not free the `uri` parameter more than once. |
| evutil_freeaddrinfo | 1 |  The caller MUST NOT call `evutil_freeaddrinfo` multiple times for the same `ai` parameter. |
| evhttp_free | 1 |  The caller of this API must not free the `http` parameter multiple times. |
| evutil_inet_pton | 1 |  Parameter 1: The caller MUST NOT leave the 'af' parameter uninitialized when calling the evutil_inet_pton function |
| evutil_inet_ntop | 1 |  Parameter 1: The caller MUST NOT leave the `af` parameter uninitialized or pass an invalid value to `evutil_inet_ntop` |
| evhttp_uri_free | 1 |  Parameter 1: The caller MUST NOT assign an invalid address or uninitialized variable to the `http` parameter before calling `evhttp_free` |
| evhttp_uri_free | 1 |  Parameter 1 (uri): The caller MUST NOT modify the `uri` parameter after it has been freed by `evhttp_uri_free` function |
