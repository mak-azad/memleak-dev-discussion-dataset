# Socket leak in the rpc thread

- URL: https://github.com/davitkalantaryan/xdr_rpc/issues/4
- Repo: davitkalantaryan/xdr_rpc (language: C)
- State: open; created 2023-12-27T21:42:51Z; status ok; passes offcwe

## Issue body

reporter (OWNER) · davitkalantaryan · 2023-12-27T21:42:51Z · https://github.com/davitkalantaryan/xdr_rpc/issues/4

Unfortunately below assumption is not true. Investigations should be continued!!!  
  
Following is the stack of leaking part  
```stack
void svc_getreqset(fd_set * readfds) Line 554 at src\core\for_server\svc.c(554)
void svc_run() Line 120 at src\core\for_server\svc_run.c(120)
```  
  
Condition when there is a socket leak is ``stat==XPRT_IDLE``.  The socket is closed and the resource is cleaned when ``stat==XPRT_DIED``, in case if ``stat == XPRT_MOREREQS`` loop continues and new data is received.   
  
![image](https://github.com/davitkalantaryan/xdr_rpc/assets/22635214/d7283a8c-76f9-4bd4-be3b-b0a77683821f)



## Comment 1870684593

reporter (OWNER) · davitkalantaryan · 2023-12-27T23:13:04Z · https://github.com/davitkalantaryan/xdr_rpc/issues/4#issuecomment-1870684593

```bat
.\ld_postload.exe --libs libanalyze_socket_leak.dll ---pid 3852
```

## Comment 1870840948

reporter (OWNER) · davitkalantaryan · 2023-12-28T05:36:16Z · https://github.com/davitkalantaryan/xdr_rpc/issues/4#issuecomment-1870840948

https://github.com/davitkalantaryan/xdr_rpc/issues/4#issue-2057793902  
Unfortunately not true.  
Investigations should be continued  

## Comment 1903545410

reporter (OWNER) · davitkalantaryan · 2024-01-22T09:07:58Z · https://github.com/davitkalantaryan/xdr_rpc/issues/4#issuecomment-1903545410

fl:svc.c,ln:129,fn:xprt_register => too many connections (1740), compilation constant FD_SETSIZE was only 64  
  
![image](https://github.com/davitkalantaryan/xdr_rpc/assets/22635214/6ccae997-ea31-47cc-9801-ce9619b11960)  

