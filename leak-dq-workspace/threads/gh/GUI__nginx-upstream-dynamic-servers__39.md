# slove memory leak when domain name changes very frequently

- URL: https://github.com/GUI/nginx-upstream-dynamic-servers/issues/39
- Repo: GUI/nginx-upstream-dynamic-servers (language: C)
- State: open; created 2024-06-20T03:54:39Z; status ok; passes offcwe

## Issue body

reporter (NONE) · Sunldon · 2024-06-20T03:54:39Z · https://github.com/GUI/nginx-upstream-dynamic-servers/issues/39

1. When using (ngx_parse_url(ngx_cycle->pool, &u) != NGX_OK) to parse URLs, if the domain name changes very frequently, the memory occupied by ngx_cycle->pool will increase continually. This memory is only released when Nginx is reloaded. Creating a new memory pool can solve this issue.
2. There is a memory leak in dynamic_server[i].previous_pool which needs to be checked if it is null. During the first assignment, dynamic_server->previous_pool = dynamic_server->pool, dynamic_server->pool is null. In the second assignment, it is assigned a new value (new_pool), hence the memory allocated for the previous new_pool is not released.

## Comment 2179758220

reporter (NONE) · Sunldon · 2024-06-20T03:55:31Z · https://github.com/GUI/nginx-upstream-dynamic-servers/issues/39#issuecomment-2179758220

#38 
this patch have resolved that problem
