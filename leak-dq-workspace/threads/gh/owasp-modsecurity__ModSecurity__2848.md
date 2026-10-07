# Memory leaks with nginx reload (without restart)

- URL: https://github.com/owasp-modsecurity/ModSecurity/issues/2848
- Repo: owasp-modsecurity/ModSecurity (language: C++)
- State: open; created 2022-12-21T19:05:25Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · martinhsv · 2022-12-21T19:05:25Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848

When, instead of restarting nginx, one performs a ```reload``` of the configuration, memory may leak.

The memory leaks are not large per reload, but if doing so frequently, the free memory reduction will become noticeable. A near-term mitigation is to at least periodically do a true restart.

This issue is being created in lieu of #2502 and others.


## Comment 1404866735

other (NONE) · Volatus · 2023-01-26T11:19:15Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1404866735

@martinhsv Would it be possible to do a small patch release soon that would include the commit e9a7ba4a60be48f761e0328c6dfcc668d70e35a0 ? According to https://github.com/kubernetes/ingress-nginx/issues/8166#issuecomment-1311495548 it did alleviate the leaks that were significant in size and would be very helpful for the users for the time being as other leaks related to reloading get ironed out. Thanks.

## Comment 1410412474

other (NONE) · IanRobertson-wpe · 2023-01-31T14:04:12Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1410412474

Hi @martinhsv, I believe my organization is encountering this issue as well. What is needed in order to address this? Is the root cause already identified?

## Comment 1410504717

reporter (CONTRIBUTOR) · martinhsv · 2023-01-31T14:52:32Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1410504717

Hello @Volatus ,

The ModSecurity project has not had a practice of doing patch releases for single issues that are separate from accumulated changes in v3/master. When the next 3.0.x release appears, it will almost certainly be from v3/master as that branch appears at that time.

The next release of 3.0.x is tentatively planned for the moderately soon period (by which I mean within 8-10 weeks) -- if that is within your definition of 'soon'. If that is problematically long for you, you could always build ModSecurity yourself from a point in time that includes the commit that you have referenced.

I do, understand, of course, that some installations may have a policy of only allowing use of official releases. If that is the case for you, and the aforementioned timeframe is problematic, I could take that into consideration. But that would have to be weighed against some other factors.

Hi @IanRobertson-wpe ,

Perhaps my response to Volatus answers most of what you are asking about as well.

One other thing I'll mention is that there is one (smaller) unresolved leak present with common ModSecurity usage. I have a fix for this for which I'll likely create the PR within a few days.


## Comment 1410517028

other (NONE) · Volatus · 2023-01-31T14:59:15Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1410517028

> Hello @Volatus ,
> 
> The ModSecurity project has not had a practice of doing patch releases for single issues that are separate from accumulated changes in v3/master. When the next 3.0.x release appears, it will almost certainly be from v3/master as that branch appears at that time.
> 
> The next release of 3.0.x is tentatively planned for the moderately soon period (by which I mean within 8-10 weeks) -- if that is within your definition of 'soon'. If that is problematically long for you, you could always build ModSecurity yourself from a point in time that includes the commit that you have referenced.
> 
> I do, understand, of course, that some installations may have a policy of only allowing use of official releases. If that is the case for you, and the aforementioned timeframe is problematic, I could take that into consideration. But that would have to be weighed against some other factors.
> 
> Hi @IanRobertson-wpe ,
> 
> Perhaps my response to Volatus answers most of what you are asking about as well.
> 
> One other thing I'll mention is that there is one (smaller) unresolved leak present with common ModSecurity usage. I have a fix for this for which I'll likely create the PR within a few days.

Thanks for the response. I think we may have a temporary fix that allows us to point to the specific commit that includes the memory leak fix. 8-10 weeks is not bad at all assuming our fix works for the time being.

## Comment 1438606887

reporter (CONTRIBUTOR) · martinhsv · 2023-02-21T14:42:59Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1438606887

There is a pull request available ( https://github.com/SpiderLabs/ModSecurity/pull/2876 ) that resolves the most prominent remaining memory leak issue when doing an nginx reload (rather than restart).

The leak in this case is proportional to the number of '.conf' ModSecurity files being read in by the bison parser.

Users for whom this is a significant nuisance in the immediate period are invited to try out the PR during the period before it is merged.


## Comment 1527608284

reporter (CONTRIBUTOR) · martinhsv · 2023-04-28T13:56:39Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1527608284

Known memory leaks of general application that occur when executing nginx reload have been resolved as of v3.0.9.

I will, however, leave this item open for at least a few weeks to allow for any additional reports.

It is probable that any further memory leaks associated with reload are related to less-commonly used features. Specific information about what sorts of Sec* constructs appear to trigger the effect would be helpful.


## Comment 1546702236

other (NONE) · S0obi · 2023-05-13T16:13:21Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1546702236

Hello @martinhsv, here is a report from our side.

**Configuration** : nginx 1.23.4 with modsecurity 3.0.9 (Ubuntu 20.04.6), coreruleset-3.3.4 with few custom rules. 197 servers blocks in nginx configs with 191 "modsecurity on" directives.

Here are few tests I performed and data I collected :

- Reloading nginx multiple times (systemctl reload nginx) with ModSecurity 3.0.9 will not consume more memory. With modsecurity < 3.0.9, multiple reload will increase the used amount of memory
- I restarted nginx (systemctl restart nginx), after few second the used memory usage will stabilize around 2.53Go. After a first reload, the memory will peak and stabilize at 4.53 Go. Second and third reload after will not change the used memory (I can only a short burst during reload to 4.62Go and then get back to 4.53Go)

However, I am still observing a rampant memory leak over time. Here is a screenshot of the memory usage of our production server (similar to test server):

![Screenshot 2023-05-13 at 17 59 16](https://github.com/SpiderLabs/ModSecurity/assets/4180104/0cbe9a07-8825-4eb8-a0d2-903fb9578e1a)

This situation is not new to modsecurity 3.0.9 but was also noticeable in the previous versions.


## Comment 1570732794

other (NONE) · Zoey2936 · 2023-05-31T18:41:35Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1570732794

> Known memory leaks of general application that occur when executing nginx reload have been resolved as of v3.0.9.

I still get one. Running nginx -s reload makes my server using all 2GB of Ram and 4GB of swap, also cpu goes up to 100% until the server freezes, killing and relaunching instead makes the server use 1,5GB ram and 3GB of swap with the cpu being at nearly 0%. I use CRS and the default modsec configuration. 

## Comment 1586583160

other (NONE) · GNU-Plus-Windows-User · 2023-06-12T05:04:48Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1586583160

I can also confirm the memory leak on reload still exists. personally, I've found the memory leak size is based on the number of ``modsecurity on;`` and ``modsecurity_rules_file /path/to/example.conf;`` directives and the use of ``@pmFromFile``.

## Comment 1587491199

reporter (CONTRIBUTOR) · martinhsv · 2023-06-12T14:43:27Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1587491199

Thanks to all for the ongoing reports

@GNU-Plus-Windows-User : thanks for the specific reference to ```@pmFromFile```.

Interestingly, the suspect functionality seems to have already been noted quite some time ago: https://github.com/SpiderLabs/ModSecurity/blame/b84f32d6f2e2e024cd85d82c6707ce66327eb7d0/src/utils/acmp.cc#L32

... but it had not previously come to my attention.


## Comment 1588485001

other (NONE) · GNU-Plus-Windows-User · 2023-06-13T03:55:13Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1588485001

@martinhsv Awesome, at least you are aware of it now.
I'm happy to test any PRs that may fix this issue.

## Comment 1593438707

other (NONE) · Zoey2936 · 2023-06-15T17:05:38Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1593438707

Will this problem be fixed in the next time?

## Comment 1607471741

reporter (CONTRIBUTOR) · martinhsv · 2023-06-26T13:25:03Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1607471741

Hi @GNU-Plus-Windows-User ,

Regarding your specific reference to ```@pmFromFile```, I have not yet been able to identify a memory leak in that code. (The code comment in acmp.cc that I previously mentioned may be obsolete since at least one correction was made later in time than that comment).

One possibility is that there is a distinctive use case in your file(s) that was not replicated in the tests that I ran with valgrind. Are you able/willing to share yours? ( If there is anything sensitive in the content, you could send them to the address listed here: https://github.com/SpiderLabs/ModSecurity#security-issue , rather than including them here.)

Also: are you using local files for that operator? Or are you using the https: option?



## Comment 1607625743

reporter (CONTRIBUTOR) · martinhsv · 2023-06-26T14:37:27Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1607625743

Hi @GNU-Plus-Windows-User ,

Regarding your observations about ```modsecurity on``` and ```modsecurity_rules_file``` ...

Could you tell me more about your environment? nginx version? ModSecurity version and Connector (ModSecurity-nginx) versions? Are you using PCRE1 or PCRE2?

Part of the reason I ask is that it's possible the leaks are actually related to code in the separate connector project (ModSecurity-nginx). One factor in that code is that there is some more complex memory pool management when PCRE1 is being used.

@S0obi , for the above reason: were you using PCRE1 or PCRE2 (the former is still the default)?


## Comment 1607687027

other (NONE) · S0obi · 2023-06-26T15:09:25Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1607687027

Hey @martinhsv, modsec library has been built with `./configure --with-pcre2` so PCRE2.

## Comment 1608581882

other (NONE) · GNU-Plus-Windows-User · 2023-06-27T01:49:35Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1608581882

@martinhsv I'm running the latest version of both modsec and the connector, my ModSecurity is compiled with pcre2 and pcre-jit for the nginx connector.
I'm using nginx 1.24.0 on ubuntu 22.04 from suvy's repo and I have about 9 server blocks with 9 ``modsecurity on`` and ``modsecurity_rules_file`` directives.
I should note that I'm observing the same/similar patterns with the memory leak as s0obi.

## Comment 1662680232

other (NONE) · S0obi · 2023-08-02T17:40:39Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1662680232

@martinhsv any clue about what can be one or multiple causes of this memory leak ?

## Comment 1716445641

reporter (CONTRIBUTOR) · martinhsv · 2023-09-12T21:10:05Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-1716445641

I have identified some leaks when using the ```--with-lmdb``` option. I will be addressing those shortly.

[Edit: the issue mentioned here was resolved in #2983 . Note that those leaks are not restricted to rule reload but can occur during each transaction.]

## Comment 2715499630

other (NONE) · S0obi · 2025-03-11T19:35:36Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-2715499630

As this is the most complete topic on Modsecurity memory leaks, I will document here some of the findings that may help to find new paths for improving the situation.

## Summary

On reload operation, nginx modsecurity module cleanup functions will be called (ngx_http_modsecurity_cleanup_rules and ngx_http_modsecurity_cleanup_instance) which will free Modsecurity and RuleSet structures. Comparing the number of calls between reload and restart seems to be equivalent. Quick review of [ngx_http_modsecurity_merge_conf ](https://github.com/owasp-modsecurity/ModSecurity-nginx/blob/master/src/ngx_http_modsecurity_module.c#L726)should be done to check if it can have a role with memory leaks.

## How does it work in detail ?

### Starting with documentation

According to [Nginx documentation](https://nginx.org/en/docs/control.html#reconfiguration) :

> In order for nginx to re-read the configuration file, a HUP signal should be sent to the master process. [...] If this succeeds, it starts new worker processes, and sends messages to old worker processes requesting them to shut down gracefully. 

In the [development guide](https://nginx.org/en/docs/dev/development_guide.html#cycle), we have a bit more information about cycle :

> Each time the nginx configuration is reloaded, a new cycle is created from the new nginx configuration; the old cycle is usually deleted after the new one is successfully created. 

On [cleanup mecanism](https://nginx.org/en/docs/dev/development_guide.html#pool) :

> Cleanup handlers can be registered in a pool. A cleanup handler is a callback with an argument which is called when pool is destroyed. A pool is usually tied to a specific nginx object (like an HTTP request) and is destroyed when the object reaches the end of its lifetime. Registering a pool cleanup is a convenient way to release resources, close file descriptors or make final adjustments to the shared data associated with the main object.

### Understanding how nginx handles SIGHUP with code

A source code analysis of nginx will help us understand the documentation better.
The HUP signal is referenced by the [NGX_RECONFIGURE_SIGNAL](https://github.com/nginx/nginx/blob/release-1.27.4/src/core/ngx_config.h#L63) macro and captured with sigaddset() in ngx_master_process_cycle() function.

The important source code controlling nginx behavior on reload is in [ngx_process_cycle.c](https://github.com/nginx/nginx/blob/release-1.27.4/src/os/unix/ngx_process_cycle.c#L74) :

```c
ngx_log_error(NGX_LOG_NOTICE, cycle->log, 0, "reconfiguring");


cycle = ngx_init_cycle(cycle);
if (cycle == NULL) {
    cycle = (ngx_cycle_t *) ngx_cycle;
    continue;
}


ngx_cycle = cycle;
ccf = (ngx_core_conf_t *) ngx_get_conf(cycle->conf_ctx,
                                        ngx_core_module);
ngx_start_worker_processes(cycle, ccf->worker_processes,
                            NGX_PROCESS_JUST_RESPAWN);
ngx_start_cache_manager_processes(cycle, 1);


/* allow new processes to start */
ngx_msleep(100);


live = 1;
ngx_signal_worker_processes(cycle,
                            ngx_signal_value(NGX_SHUTDOWN_SIGNAL));
```

On the reload operation, ngx_destroy_pool() will call the cleanup handler attached to the pool.

### Experimenting with Modsecurity-nginx module

To enable interesting debug logs, we can just uncomment a few lines from [src/ddebug.h](https://github.com/owasp-modsecurity/ModSecurity-nginx/blob/master/src/ddebug.h#L15-L18).

A typical reload operation will call these function (in this specific order) :

1. ngx_http_modsecurity_create_main_conf (once)
2. ngx_http_modsecurity_create_conf (multiple times)
3. ngx_http_modsecurity_merge_conf (multiple times)
4. ngx_http_modsecurity_cleanup_rules (multiple times)
5. ngx_http_modsecurity_cleanup_instance (multiple times)

A comparison between reload and restart is showing the same number of cleanup operations.

**Hypothesis**: is ngx_http_modsecurity_merge_conf doing memory allocations that are not free ? When calling msc_rules_merge, what happens to the previous ruleset ?

**Observation** : after a fresh start, the memory allocated for nginx is normal, after a first reload, we can observe a bump in the allocated memory (+3Go on our test instance). Second and next reload will bump the allocated memory temporarily (that can cause an OOM) and come back to previous level plus a small amount (+10Mo on our test instance after the next reload). Finally, memory allocated will slowly increase over time.

## Comment 2716901762

other (NONE) · wohaiaini · 2025-03-12T07:35:24Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-2716901762

Is it possible that this is caused by memory fragmentation?

## Comment 2717120884

maintainer (MEMBER) · airween · 2025-03-12T08:57:33Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-2717120884

> Is it possible that this is caused by memory fragmentation?

I don't think so. It's definitely there when you have so much free memory.

## Comment 2855166221

other (NONE) · fl0ppy-d1sk · 2025-05-06T16:14:17Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-2855166221

> **Observation** : after a fresh start, the memory allocated for nginx is normal, after a first reload, we can observe a bump in the allocated memory (+3Go on our test instance). Second and next reload will bump the allocated memory temporarily (that can cause an OOM) and come back to previous level plus a small amount (+10Mo on our test instance after the next reload). Finally, memory allocated will slowly increase over time.

I confirm that we have the same behavior. 

## Comment 3561483043

other (NONE) · roshatron2 · 2025-11-21T05:41:47Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3561483043

Hi all, my organisation is also seeing a memory leak while using modsecurity + coreruleset combo. Has anyone observed the same stack trace while using ModSecurity?

==27426== 1 bytes in 1 blocks are possibly lost in loss record 16 of 1,421
==27426==    at 0x482BBB5: operator new(unsigned int) (vg_replace_malloc.c:338)
==27426==    by 0x94EB43A: _M_init_functor (functional:1987)
==27426==    by 0x94EB43A: _M_init_functor (functional:1958)
==27426==    by 0x94EB43A: function<modsecurity::AnchoredSetVariableTranslationProxy::AnchoredSetVariableTranslationProxy(const string&, modsecurity::AnchoredSetVariable*)::__lambda2, void> (functional:2458)
==27426==    by 0x94EB43A: operator=<modsecurity::AnchoredSetVariableTranslationProxy::AnchoredSetVariableTranslationProxy(const string&, modsecurity::AnchoredSetVariable*)::__lambda2> (functional:2336)
==27426==    by 0x94EB43A: AnchoredSetVariableTranslationProxy (anchored_set_variable_translation_proxy.h:58)
==27426==    by 0x94EB43A: modsecurity::TransactionAnchoredVariables::TransactionAnchoredVariables(modsecurity::Transaction*) (transaction.h:210)
==27426==    by 0x94E7805: modsecurity::Transaction::Transaction(modsecurity::ModSecurity*, modsecurity::RulesSet*, void*) (transaction.cc:164)
==27426==    by 0x94E895E: msc_new_transaction (transaction.cc:1917)
==27426==    by 0xB546B6E: ???
==27426==    by 0xB5479E4: ???
==27426==    by 0x165E98: ngx_http_core_rewrite_phase (ngx_http_core_module.c:929)
==27426==    by 0x160ED0: ngx_http_core_run_phases (ngx_http_core_module.c:875)
==27426==    by 0x16E29D: ngx_http_process_request (ngx_http_request.c:2212)
==27426==    by 0x16F158: ngx_http_process_request_headers (ngx_http_request.c:1601)
==27426==    by 0x16F5C0: ngx_http_process_request_line (ngx_http_request.c:1230)
==27426==    by 0x154416: ngx_ssl_handshake_handler (ngx_event_openssl.c:2168)
==27426==    by 0x14EE65: ngx_epoll_process_events (ngx_epoll_module.c:901)
==27426==    by 0x141C81: ngx_process_events_and_timers (ngx_event.c:248)
==27426==    by 0x14C5FF: ngx_worker_process_cycle (ngx_process_cycle.c:721)
==27426==    by 0x14AB69: ngx_spawn_process (ngx_process.c:212)
==27426==    by 0x14C93A: ngx_start_worker_processes (ngx_process_cycle.c:344)
==27426==    by 0x14D86F: ngx_master_process_cycle (ngx_process_cycle.c:130)
==27426==    by 0x11ADAB: main (nginx.c:384)

## Comment 3562032346

maintainer (MEMBER) · airween · 2025-11-21T08:54:43Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3562032346

Hi @roshatron2,

> Hi all, my organisation is also seeing a memory leak while using modsecurity + coreruleset combo. Has anyone observed the same stack trace while using ModSecurity?

could you explain please how did you catch this result? I mean you made an `nginx reload` and during that event you made a valgrind inspection?


## Comment 3562309445

other (NONE) · roshatron2 · 2025-11-21T10:07:20Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3562309445

> Hi [@roshatron2](https://github.com/roshatron2),
> 
> > Hi all, my organisation is also seeing a memory leak while using modsecurity + coreruleset combo. Has anyone observed the same stack trace while using ModSecurity?
> 
> could you explain please how did you catch this result? I mean you made an `nginx reload` and during that event you made a valgrind inspection?

It wasn't an nginx reload, I got this log while running valgrind on normal web traffic, this was the only memory leak thread that was open on github. 

I'm running modsecurity with nginx (modsecurity version is 3.0.12)


==21059== LEAK SUMMARY:
==21059==    definitely lost: 5,602 bytes in 594 blocks
==21059==    indirectly lost: 59,318 bytes in 1,176 blocks
==21059==      possibly lost: 28,811,062 bytes in 1,617 blocks
==21059==    still reachable: 2,198,148 bytes in 655 blocks
==21059==                       of which reachable via heuristic:
==21059==                         stdstring          : 16,953 bytes in 487 blocks
==21059==                         multipleinheritance: 36 bytes in 1 blocks
==21059==         suppressed: 702,506 bytes in 29,612 blocks
==21059== 
==21059== Use --track-origins=yes to see where uninitialised values come from
==21059== For lists of detected and suppressed errors, rerun with: -s
==21059== ERROR SUMMARY: 745 errors from 593 contexts (suppressed: 48 from 48)


## Comment 3562343513

maintainer (MEMBER) · airween · 2025-11-21T10:16:33Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3562343513

Thank @roshatron2,

> It wasn't an nginx reload, I got this log while running valgrind on normal web traffic, this was the only memory leak thread that was open on github.

I see, but this issue is about the `nginx reload` problem. I think the issue you described is a separated problem, and probably more serious. It would have been better to open a separated issue - never mind.

Could you explain how did you run Valgrind and what was the request? Also the used config and CRS would be helpfully.

## Comment 3562508382

other (NONE) · roshatron2 · 2025-11-21T10:58:51Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3562508382

> Thank [@roshatron2](https://github.com/roshatron2),
> 
> > It wasn't an nginx reload, I got this log while running valgrind on normal web traffic, this was the only memory leak thread that was open on github.
> 
> I see, but this issue is about the `nginx reload` problem. I think the issue you described is a separated problem, and probably more serious. It would have been better to open a separated issue - never mind.
> 
> Could you explain how did you run Valgrind and what was the request? Also the used config and CRS would be helpfully.


/usr/bin/valgrind --num-callers=20 --leak-check=full --show-reachable=yes --trace-children=yes --error-limit=no --suppressions=/home/etc/valgrind/valgrind_suppressions --log-file=/home/runtime/cores/nginx-valgrind%p.log /home/ecbuilds/int-rel/sa/22.8/bld16480.1/install/bin/nginx -c /home/ecbuilds/int-rel/sa/22.8/bld16480.1/install/runtime/nginx/config/nginx.conf -e /home/ecbuilds/int-rel/sa/22.8/bld16480.1/install/runtime/nginx/logs/nginx_error.log

This is the valgrind settings

I'm using coreruleset version 4.12.0
The requests start with HTTP requests and then we are RDPing into a windows VM in the browser



## Comment 3562769117

other (NONE) · FireBurn · 2025-11-21T12:15:31Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3562769117

So I ploked all this into Google AI Studio and it came up with:

Based on the Valgrind output and the provided code, the memory leak is located in the **`TransactionAnchoredVariables`** class (which is part of the `Transaction` object).

The stack trace indicates that memory allocated during the construction of `AnchoredSetVariableTranslationProxy` (specifically inside a `std::function` initialization) is never freed.

```text
==27426== 1 bytes in 1 blocks are possibly lost ...
==27426== at 0x482BBB5: operator new(unsigned int) ...
==27426== by 0x94EB43A: ... function<...>::operator= ...
==27426== by 0x94EB43A: AnchoredSetVariableTranslationProxy ...
==27426== by 0x94EB43A: modsecurity::TransactionAnchoredVariables::TransactionAnchoredVariables(modsecurity::Transaction*) ...
```

In `src/transaction.cc`, the `Transaction` constructor initializes `TransactionAnchoredVariables`:

```cpp
Transaction::Transaction(ModSecurity *ms, RulesSet *rules, const char *id,
    void *logCbData, const time_t timestamp)
    : ...
    TransactionAnchoredVariables(this) { // <--- Initialization here
    ...
```

And in `src/variables/variable.h`, the code accesses `m_variableArgsNames` as if it were an object (using `&`), not a pointer:

```cpp
anchoredSetVariableTranslationProxy = &t->m_variableArgsNames;
```

This usage pattern combined with the leak indicates that **`TransactionAnchoredVariables` declares its members (like `m_variableArgsNames`) as references (`&`) but initializes them using `new` in its constructor.**

Because they are references, the `TransactionAnchoredVariables` destructor does not (and cannot) delete the objects they refer to. Consequently, the `AnchoredSetVariableTranslationProxy` objects (and their internal `std::function` members) are leaked when the `Transaction` is destroyed.

**To fix this:**
The members in `TransactionAnchoredVariables` should be changed from references (e.g., `AnchoredSetVariableTranslationProxy &`) to pointers (e.g., `std::unique_ptr<AnchoredSetVariableTranslationProxy>`), or they should be deleted manually in the `TransactionAnchoredVariables` destructor if raw pointers are used. Given the `&t->member` usage, they were likely intended to be value members or references binding to dynamic memory (which is the bug).

## Comment 3562851220

other (NONE) · FireBurn · 2025-11-21T12:36:54Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3562851220

@roshatron2 Are you able to test that MR and see if it fixes things for you

## Comment 3564542399

other (NONE) · roshatron2 · 2025-11-21T20:45:33Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3564542399

> [@roshatron2](https://github.com/roshatron2) Are you able to test that MR and see if it fixes things for you

I'm yet to test this MR yet, I was testing few more scenarios for the feature in my org's product, I see that there is memory leaks coming from RuleRemoveTargetByTag, 



==23905== 53,443 (16 direct, 53,427 indirect) bytes in 1 blocks are definitely lost in loss record 1,450 of 1,467
==23905==    at 0x482BBB5: operator new(unsigned int) (vg_replace_malloc.c:338)
==23905==    by 0x9523231: allocate (new_allocator.h:104)
==23905==    by 0x9523231: _M_get_node (stl_list.h:334)
==23905==    by 0x9523231: _M_create_node<std::pair<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > (stl_list.h:502)
==23905==    by 0x9523231: _M_insert<std::pair<std::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::basic_string<char, std::char_traits<char>, std::allocator<char> > > > (stl_list.h:1561)
==23905==    by 0x9523231: push_back (stl_list.h:1021)
==23905==    by 0x9523231: modsecurity::actions::ctl::RuleRemoveTargetByTag::evaluate(modsecurity::RuleWithActions*, modsecurity::Transaction*) (rule_remove_target_by_tag.cc:49)
==23905==    by 0x951FF5E: modsecurity::actions::Action::evaluate(modsecurity::RuleWithActions*, modsecurity::Transaction*, std::shared_ptr<modsecurity::RuleMessage>) (action.h:82)
==23905==    by 0x95002FD: modsecurity::RuleWithActions::executeAction(modsecurity::Transaction*, bool, std::shared_ptr<modsecurity::RuleMessage>, modsecurity::actions::Action*, bool) (rule_with_actions.cc:299)
==23905==    by 0x950153E: modsecurity::RuleWithActions::executeActionsAfterFullMatch(modsecurity::Transaction*, bool, std::shared_ptr<modsecurity::RuleMessage>) (rule_with_actions.cc:283)
==23905==    by 0x9506BE1: modsecurity::RuleWithOperator::evaluate(modsecurity::Transaction*, std::shared_ptr<modsecurity::RuleMessage>) (rule_with_operator.cc:369)
==23905==    by 0x95025C3: modsecurity::RuleWithActions::evaluate(modsecurity::Transaction*) (rule_with_actions.cc:177)
==23905==    by 0x94F9369: modsecurity::RulesSet::evaluate(int, modsecurity::Transaction*) (rules_set.cc:210)
==23905==    by 0x94DA7B1: modsecurity::Transaction::processRequestHeaders() (transaction.cc:580)
==23905==    by 0x94DA86A: msc_process_request_headers (transaction.cc:1997)
==23905==    by 0xB547E01: ???
==23905==    by 0x165E98: ngx_http_core_rewrite_phase (ngx_http_core_module.c:929)
==23905==    by 0x160ED0: ngx_http_core_run_phases (ngx_http_core_module.c:875)
==23905==    by 0x16E29D: ngx_http_process_request (ngx_http_request.c:2212)

I will get back to you with the results after I test with the MR as soon as possible



## Comment 3569378710

other (NONE) · roshatron2 · 2025-11-24T07:54:03Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3569378710

> [@roshatron2](https://github.com/roshatron2) Are you able to test that MR and see if it fixes things for you

@FireBurn  I've tried your fix, my org is still on CentOS 7(gcc 4.8.5), so make_unique syntax is not supported yet

## Comment 3570169726

other (NONE) · FireBurn · 2025-11-24T11:02:08Z · https://github.com/owasp-modsecurity/ModSecurity/issues/2848#issuecomment-3570169726

Try with devtoolset-9, 8 should also work
