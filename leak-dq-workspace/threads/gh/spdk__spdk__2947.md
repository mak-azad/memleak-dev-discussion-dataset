# crypto-autotest: LeakSanitizer: detected memory leaks

- URL: https://github.com/spdk/spdk/issues/2947
- Repo: spdk/spdk (language: C)
- State: open; created 2023-03-15T16:27:52Z; status ok; passes main

## Issue body

reporter (CONTRIBUTOR) · karlatec · 2023-03-15T16:27:52Z · https://github.com/spdk/spdk/issues/2947

# Sighting report

Leak sanitizer detects memory leak in crypto test job.
https://ci.spdk.io/results/autotest-per-patch/builds/100311/archive/crypto-autotest/build.log
https://ci.spdk.io/public_build/autotest-per-patch_100311.html

## Current Behavior

```
00:14:18.393  ************************************
00:14:18.393  START TEST bdev_fio_rw_verify
00:14:18.394  ************************************
00:14:18.394   14:44:04	-- common/autotest_common.sh@1073 -- # xtrace_enable
00:14:18.394   14:44:04	-- common/autotest_common.sh@1074 -- # fio_bdev --ioengine=spdk_bdev --iodepth=8 --bs=4k --runtime=10 /var/jenkins/workspace/crypto-autotest/spdk/test/bdev/bdev.fio --verify_state_save=0 --spdk_json_conf=/var/jenkins/workspace/crypto-autotest/spdk/test/bdev/bdev.json --spdk_mem=0 --aux-path=/var/jenkins/workspace/crypto-autotest/spdk/../output
00:14:18.394   14:44:04	-- common/autotest_common.sh@1311 -- # fio_plugin /var/jenkins/workspace/crypto-autotest/spdk/build/fio/spdk_bdev --ioengine=spdk_bdev --iodepth=8 --bs=4k --runtime=10 /var/jenkins/workspace/crypto-autotest/spdk/test/bdev/bdev.fio --verify_state_save=0 --spdk_json_conf=/var/jenkins/workspace/crypto-autotest/spdk/test/bdev/bdev.json --spdk_mem=0 --aux-path=/var/jenkins/workspace/crypto-autotest/spdk/../output
00:14:18.394   14:44:04	-- common/autotest_common.sh@1286 -- # local fio_dir=/usr/src/fio
00:14:18.394   14:44:04	-- common/autotest_common.sh@1288 -- # sanitizers=('libasan' 'libclang_rt.asan')
00:14:18.394   14:44:04	-- common/autotest_common.sh@1288 -- # local sanitizers
00:14:18.394   14:44:04	-- common/autotest_common.sh@1289 -- # local plugin=/var/jenkins/workspace/crypto-autotest/spdk/build/fio/spdk_bdev
00:14:18.394   14:44:04	-- common/autotest_common.sh@1290 -- # shift
00:14:18.394    14:44:04	-- common/autotest_common.sh@1292 -- # uname -s
00:14:18.394   14:44:04	-- common/autotest_common.sh@1292 -- # [[ Linux != \L\i\n\u\x ]]
00:14:18.394   14:44:04	-- common/autotest_common.sh@1298 -- # local asan_lib=
00:14:18.394   14:44:04	-- common/autotest_common.sh@1299 -- # for sanitizer in "${sanitizers[@]}"
00:14:18.394    14:44:04	-- common/autotest_common.sh@1300 -- # LD_LIBRARY_PATH=:/var/jenkins/workspace/crypto-autotest/spdk/build/lib:/var/jenkins/workspace/crypto-autotest/spdk/dpdk/build/lib:/var/jenkins/workspace/crypto-autotest/spdk/build/libvfio-user/usr/local/lib:/var/jenkins/workspace/crypto-autotest/spdk/build/lib:/var/jenkins/workspace/crypto-autotest/spdk/dpdk/build/lib:/var/jenkins/workspace/crypto-autotest/spdk/build/libvfio-user/usr/local/lib
00:14:18.394    14:44:04	-- common/autotest_common.sh@1300 -- # ldd /var/jenkins/workspace/crypto-autotest/spdk/build/fio/spdk_bdev
00:14:18.394    14:44:04	-- common/autotest_common.sh@1300 -- # grep libasan
00:14:18.394    14:44:04	-- common/autotest_common.sh@1300 -- # awk '{print $3}'
00:14:18.652   14:44:04	-- common/autotest_common.sh@1300 -- # asan_lib=/usr/lib64/libasan.so.8
00:14:18.652   14:44:04	-- common/autotest_common.sh@1301 -- # [[ -n /usr/lib64/libasan.so.8 ]]
00:14:18.652   14:44:04	-- common/autotest_common.sh@1302 -- # break
00:14:18.652   14:44:04	-- common/autotest_common.sh@1307 -- # LD_PRELOAD='/usr/lib64/libasan.so.8 /var/jenkins/workspace/crypto-autotest/spdk/build/fio/spdk_bdev'
00:14:18.652   14:44:04	-- common/autotest_common.sh@1307 -- # /usr/src/fio/fio --ioengine=spdk_bdev --iodepth=8 --bs=4k --runtime=10 /var/jenkins/workspace/crypto-autotest/spdk/test/bdev/bdev.fio --verify_state_save=0 --spdk_json_conf=/var/jenkins/workspace/crypto-autotest/spdk/test/bdev/bdev.json --spdk_mem=0 --aux-path=/var/jenkins/workspace/crypto-autotest/spdk/../output
00:14:18.910  job_crypto_ram: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=spdk_bdev, iodepth=8
00:14:18.910  job_crypto_ram1: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=spdk_bdev, iodepth=8
00:14:18.910  job_crypto_ram2: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=spdk_bdev, iodepth=8
00:14:18.910  job_crypto_ram3: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=spdk_bdev, iodepth=8
00:14:18.910  fio-3.28
00:14:18.910  Starting 4 threads
00:14:18.910  TELEMETRY: No legacy callbacks, legacy socket not created
00:14:33.770  
00:14:33.770  job_crypto_ram: (groupid=0, jobs=4): err= 0: pid=712978: Wed Mar 15 14:44:17 2023
00:14:33.770    read: IOPS=1023k, BW=3996MiB/s (4191MB/s)(935MiB/234msec)
00:14:33.770      slat (usec): min=9, max=111, avg=17.61, stdev= 6.18
00:14:33.770      clat (usec): min=48, max=1956, avg=415.27, stdev=152.20
00:14:33.770       lat (usec): min=65, max=1982, avg=432.89, stdev=154.42
00:14:33.770      clat percentiles (usec):
00:14:33.770       | 50.000th=[  367], 99.000th=[  824], 99.900th=[ 1123], 99.990th=[ 1319],
00:14:33.770       | 99.999th=[ 1745]
00:14:33.770    write: IOPS=26.1k, BW=102MiB/s (107MB/s)(1000MiB/9798msec); 0 zone resets
00:14:33.770      slat (usec): min=38, max=292, avg=70.87, stdev=28.20
00:14:33.770      clat (usec): min=33, max=1716, avg=435.78, stdev=214.53
00:14:33.770       lat (usec): min=102, max=1832, avg=506.65, stdev=227.38
00:14:33.770      clat percentiles (usec):
00:14:33.770       | 50.000th=[  388], 99.000th=[ 1045], 99.900th=[ 1237], 99.990th=[ 1369],
00:14:33.770       | 99.999th=[ 1450]
00:14:33.770     bw (  KiB/s): min=90800, max=114472, per=98.47%, avg=102896.42, stdev=1772.92, samples=76
00:14:33.770     iops        : min=22700, max=28618, avg=25724.11, stdev=443.26, samples=76
00:14:33.770    lat (usec)   : 50=0.01%, 100=0.01%, 250=14.85%, 500=54.74%, 750=24.18%
00:14:33.770    lat (usec)   : 1000=5.29%
00:14:33.770    lat (msec)   : 2=0.93%
00:14:33.770    cpu          : usr=99.22%, sys=0.20%, ctx=83, majf=0, minf=21661
00:14:33.770    IO depths    : 1=2.8%, 2=19.9%, 4=58.4%, 8=18.8%, 16=0.0%, 32=0.0%, >=64=0.0%
00:14:33.770       submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
00:14:33.770       complete  : 0=0.0%, 4=89.6%, 8=10.4%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
00:14:33.770       issued rwts: total=239401,255950,0,0 short=0,0,0,0 dropped=0,0,0,0
00:14:33.770       latency   : target=0, window=0, percentile=100.00%, depth=8
00:14:33.770  
00:14:33.770  Run status group 0 (all jobs):
00:14:33.770     READ: bw=3996MiB/s (4191MB/s), 3996MiB/s-3996MiB/s (4191MB/s-4191MB/s), io=935MiB (981MB), run=234-234msec
00:14:33.770    WRITE: bw=102MiB/s (107MB/s), 102MiB/s-102MiB/s (107MB/s-107MB/s), io=1000MiB (1048MB), run=9798-9798msec
00:14:33.770  
00:14:33.770  =================================================================
00:14:33.770  ==712939==ERROR: LeakSanitizer: detected memory leaks
00:14:33.770  
00:14:33.770  Direct leak of 904 byte(s) in 1 object(s) allocated from:
00:14:33.770      #0 0x7fd272e816af in __interceptor_malloc (/usr/lib64/libasan.so.8+0xba6af)
00:14:33.770      #1 0x7fd26a35b14c in CRYPTO_zalloc (/usr/lib64/libcrypto.so.3+0x1af14c)
00:14:33.770  
00:14:33.770  -----------------------------------------------------
00:14:33.770  Suppressions used:
00:14:33.770    count      bytes template
00:14:33.770        5         53 /usr/src/fio/parse.c
00:14:33.770      567      49896 /usr/src/fio/iolog.c
00:14:33.770        1          8 libtcmalloc_minimal.so
00:14:33.770  -----------------------------------------------------
00:14:33.770  
00:14:33.770  SUMMARY: AddressSanitizer: 904 byte(s) leaked in 1 allocation(s).
```

## Steps to Reproduce

1. Prepare configuration file:
```
SPDK_RUN_FUNCTIONAL_TEST=1                                                                                                                                                                                           
SPDK_TEST_BLOCKDEV=1                                                                                                                                                                                                 
SPDK_TEST_ISAL=1                                                                                                                                                                                                     
SPDK_TEST_CRYPTO=1                                                                                                                                                                                                   
SPDK_TEST_REDUCE=1                                                                                                                                                                                                   
SPDK_TEST_VBDEV_COMPRESS=1                                                                                                                                                                                           
SPDK_RUN_UBSAN=1                                                                                                                                                                                                     
SPDK_RUN_ASAN=1   
```

2. `./autorun.sh ~/autorun.conf`


## Context (Environment including OS version, SPDK version, etc.)

SPDK 7c3c0b663022417e6ebe1a99c21d2e2b52b30968
Linux spdk-GP-03 6.1.14-200.fc37.x86_64 #1 SMP PREEMPT_DYNAMIC Sun Feb 26 00:13:26 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
gcc 12.2.1 "cc (GCC) 12.2.1 20221121 (Red Hat 12.2.1-4)"

ASAN was disabled for this job since "forever". Unfortunately we don't have any comments added neither in spdk scripts nor in CI configuration to explain why. I recall similar ASAN issues in this job in the past, but could not find a Github issue matching this error trace. This issue was detected when working on #2900 

## Comment 1470420028

maintainer (MEMBER) · jimharris · 2023-03-15T17:05:34Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1470420028

This one isn't clear to me how to fix.  The leak is from openssl crypto library, but I don't see yet where the leak could be, or at least how SPDK could be causing it.  Lack of a full backtrace from ASAN doesn't help.

We only include openssl code in SPDK in three places - iscsi/md5, util/uuid, sock/posix.  I don't see how the iscsi or sock code would get executed in a crypto bdev test.  I scrubbed the util/uuid code, and don't see any leaks there either.

Not sure about next steps here - probably one would just be to reproduce this locally.  Maybe run in gdb and break on CRYPTO_zalloc and see where it gets called from.  That might yield some clues.


## Comment 1471501406

reporter (CONTRIBUTOR) · karlatec · 2023-03-16T08:18:37Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1471501406

I found that this also shows up during fio test in SPDK_TEST_RBD suite. Attaching repro steps using RBD tests as these don't require additional hardware (QAT card).

1. Build SPDK
```
./configure --with-iscsi-initiator --enable-asan --enable-debug --with-rbd --with-fio; make -j
```

2. Prepare configuration files
/tmp/bdev.fio
```
[global]
thread=1

group_reporting=1
direct=1
norandommap=1
percentile_list=50:99:99.9:99.99:99.999
time_based=1
ramp_time=0
verify=sha1
verify_backlog=1024
rw=randwrite
serialize_overlap=1
[job_Ceph0]
filename=Ceph0
```

/tmp/bdev.json
```
{                                                                                                                                                                                                          [15/83574]
  "subsystems": [    
    {                       
      "subsystem": "accel",    
      "config": []            
    },                        
    {                                                                                                     
      "subsystem": "bdev",
      "config": [
        {
          "method": "bdev_set_options",    
          "params": {
            "bdev_io_pool_size": 65535,
            "bdev_io_cache_size": 256,
            "bdev_auto_examine": true
          }
        },                                     
        {
          "method": "bdev_nvme_set_options",
          "params": {
            "action_on_timeout": "none",
            "timeout_us": 0,
            "timeout_admin_us": 0,
            "keep_alive_timeout_ms": 10000,
            "transport_retry_count": 4,
            "arbitration_burst": 0,
            "low_priority_weight": 0,
            "medium_priority_weight": 0,
            "high_priority_weight": 0,
            "nvme_adminq_poll_period_us": 10000,
            "nvme_ioq_poll_period_us": 0,
            "io_queue_requests": 0,
            "delay_cmd_submit": true,
            "bdev_retry_count": 3,
            "transport_ack_timeout": 0,
            "ctrlr_loss_timeout_sec": 0,
            "reconnect_delay_sec": 0,
            "fast_io_fail_timeout_sec": 0,
            "generate_uuids": false,
            "transport_tos": 0,
            "io_path_stat": false
          }
        },
        {
          "method": "bdev_nvme_set_hotplug",
          "params": {
            "period_us": 100000,
            "enable": false
          }
        },
        {
          "method": "bdev_iscsi_set_options",
          "params": {
            "timeout_sec": 30
          }
        },
        {
          "method": "bdev_rbd_create",
          "params": {
            "name": "Ceph0",
            "pool_name": "rbd",
            "rbd_name": "foo",
            "block_size": 512,
            "uuid": "82cbafb2-b9d8-466c-a358-80cac9875fe0"
          }
        },
        {
          "method": "bdev_wait_for_examine"
        }
      ]
    }
  ]
}
```

/tmp/asan_suppression/file
```
leak:spdk_fs_alloc_thread_ctx

# Suppress known leaks in fio project
leak:/usr/src/fio/parse.c
leak:/usr/src/fio/iolog.c
leak:/usr/src/fio/init.c
leak:/usr/src/fio/filesetup.c
leak:fio_memalign
leak:spdk_fio_io_u_init
# Suppress leaks in gperftools-libs from fio
leak:libtcmalloc_minimal.so

# Suppress leaks in libiscsi
leak:libiscsi.so
leak:libfuse3.so
```

3. Run the test:
```
[vagrant@fedora37-cloud-1676542281-1707 spdk]$ sudo -E LSAN_OPTIONS=suppressions=/tmp/asan_suppression_file LD_PRELOAD='/usr/lib64/libasan.so.8 /home/vagrant/spdk_repo/spdk/build/fio/spdk_bdev' /usr/src/fio/fio --ioengine=spdk_bdev --iodepth=8 --bs=4k --runtime=10 /tmp/bdev.fio --verify_state_save=0 --spdk_json_conf=/tmp/bdev.json --spdk_mem=0
job_Ceph0: (g=0): rw=randwrite, bs=(R) 4096B-4096B, (W) 4096B-4096B, (T) 4096B-4096B, ioengine=spdk_bdev, iodepth=8
fio-3.28
Starting 1 thread
TELEMETRY: No legacy callbacks, legacy socket not created
EAL: pthread_setaffinity_np failed
Jobs: 1 (f=1): [w(1)][2.9%][r=4096KiB/s,w=2752KiB/s][r=1024,w=688 IOPS][eta 06m:09s]  
job_Ceph0: (groupid=0, jobs=1): err= 0: pid=48103: Thu Mar 16 08:18:17 2023
  write: IOPS=762, BW=3049KiB/s (3122kB/s)(29.8MiB/10012msec); 0 zone resets
    slat (usec): min=12, max=776, avg=48.97, stdev=65.10
    clat (msec): min=2, max=178, avg= 6.89, stdev= 2.40
     lat (msec): min=2, max=178, avg= 6.93, stdev= 2.40
    clat percentiles (msec):
     | 50.000th=[    7], 99.000th=[   13], 99.900th=[   17], 99.990th=[  180],
     | 99.999th=[  180]
   bw (  KiB/s): min=  672, max= 5205, per=100.00%, avg=3049.05, stdev=1475.68, samples=20
   iops        : min=  168, max= 1301, avg=762.25, stdev=368.90, samples=20
  lat (usec)   : 250=0.10%, 500=3.95%, 750=7.72%, 1000=14.71%
  lat (msec)   : 2=20.61%, 4=0.36%, 10=50.19%, 20=1.45%, 50=0.22%
  lat (msec)   : 100=0.20%, 250=0.33%, 500=0.17%
  cpu          : usr=94.98%, sys=1.23%, ctx=13722, majf=0, minf=18570
  IO depths    : 1=0.1%, 2=0.1%, 4=14.3%, 8=85.6%, 16=0.0%, 32=0.0%, >=64=0.0%
     submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     complete  : 0=0.0%, 4=99.8%, 8=0.2%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
     issued rwts: total=7168,7632,0,0 short=0,0,0,0 dropped=0,0,0,0
     latency   : target=0, window=0, percentile=100.00%, depth=8

Run status group 0 (all jobs):
  WRITE: bw=3049KiB/s (3122kB/s), 3049KiB/s-3049KiB/s (3122kB/s-3122kB/s), io=29.8MiB (31.3MB), run=10012-10012msec

=================================================================
==48080==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 904 byte(s) in 1 object(s) allocated from:
    #0 0x7fc0dc2ba6af in __interceptor_malloc (/usr/lib64/libasan.so.8+0xba6af)
    #1 0x7fc0d9faf14c in CRYPTO_zalloc (/usr/lib64/libcrypto.so.3+0x1af14c)

-----------------------------------------------------
Suppressions used:
  count      bytes template
      2         12 /usr/src/fio/parse.c
    450      39600 /usr/src/fio/iolog.c
      1          8 libtcmalloc_minimal.so
-----------------------------------------------------

SUMMARY: AddressSanitizer: 904 byte(s) leaked in 1 allocation(s).
```

## Comment 1472020593

other (CONTRIBUTOR) · ksztyber · 2023-03-16T13:56:03Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1472020593

I caught this allocation under gdb:
```
#0  CRYPTO_zalloc (num=904, file=0x7ffff592bab0 "crypto/err/err.c", line=691) at crypto/mem.c:194                     
#1  0x00007ffff576c048 in ossl_err_get_state_int () at crypto/err/err.c:691                                           
#2  0x00007ffff576c79d in ERR_set_mark () at crypto/err/err.c:882                                                     
#3  0x00007ffff57146b2 in CONF_modules_load_file_ex (libctx=0x0, filename=0x0, appname=0x0, flags=50)                 
    at crypto/conf/conf_mod.c:195                                                                                     
#4  0x00007ffff57b6360 in ossl_config_int (settings=0x0) at crypto/conf/conf_sap.c:68                                 
#5  ossl_config_int (settings=0x0) at crypto/conf/conf_sap.c:44                                                       
#6  ossl_init_config () at crypto/init.c:249                                                                          
#7  ossl_init_config_ossl_ () at crypto/init.c:247                                                                    
#8  0x00007ffff6ab3087 in __pthread_once_slow () from /usr/lib64/libc.so.6                                            
#9  0x00007ffff57bb87d in CRYPTO_THREAD_run_once (once=<optimized out>, init=<optimized out>)                         
    at crypto/threads_pthread.c:156                                                                                   
#10 0x00007ffff57b6c2e in OPENSSL_init_crypto (opts=64, settings=0x0) at crypto/init.c:588                            
#11 0x00007ffff5887a7e in ossl_engine_table_select.constprop.0 (table=0x7ffff5a277f8 <cipher_table>, nid=895,         
    l=<optimized out>, f=<optimized out>) at crypto/engine/eng_table.c:205                                            
#12 0x00007ffff578e009 in evp_cipher_init_internal (ctx=0x610000018040, cipher=0x7ffff59ddf40 <aesni_128_gcm>,        
    impl=0x0, key=0x0, iv=0x0, enc=<optimized out>, params=0x0) at crypto/evp/evp_enc.c:128                           
#13 0x00007ffff578e90f in EVP_CipherInit_ex (ctx=<optimized out>, cipher=<optimized out>, impl=<optimized out>,       
    key=<optimized out>, iv=<optimized out>, enc=<optimized out>) at crypto/evp/evp_enc.c:412                         
#14 0x00007ffff601b104 in ceph::crypto::onwire::AES128GCM_OnWireRxHandler::AES128GCM_OnWireRxHandler (                
    cct=<optimized out>, new_nonce_format=true, nonce=..., key=..., this=0x60400006c310)                              
    at /usr/src/debug/ceph-17.2.5-1.fc37.x86_64/src/msg/async/crypto_onwire.cc:180                                    
#15 std::make_unique<ceph::crypto::onwire::AES128GCM_OnWireRxHandler, ceph::common::CephContext*&, std::array<unsigned
 char, 16ul>&, ceph::crypto::onwire::nonce_t&, bool&> () at /usr/include/c++/12/bits/unique_ptr.h:1065                
#16 ceph::crypto::onwire::rxtx_t::create_handler_pair (cct=0x62800002c100, auth_meta=...,                             
    new_nonce_format=<optimized out>, crossed=<optimized out>)                                                        
    at /usr/src/debug/ceph-17.2.5-1.fc37.x86_64/src/msg/async/crypto_onwire.cc:299                                    
#17 0x00007ffff6004e8d in ProtocolV2::handle_auth_done (this=0x61a000011a80, payload=...)                             
    at /usr/include/c++/12/bits/shared_ptr_base.h:1349                                                                
#18 0x00007ffff5ff8899 in ProtocolV2::run_continuation (this=0x61a000011a80, continuation=...)                        
    at /usr/src/debug/ceph-17.2.5-1.fc37.x86_64/src/msg/async/ProtocolV2.cc:49                                        
#19 0x00007ffff5fd07dc in std::function<void (char*, long)>::operator()(char*, long) const (__args#1=0,               
    __args#0=<optimized out>, this=0x619000023418) at /usr/include/c++/12/bits/std_function.h:591                     
#20 AsyncConnection::process (this=0x619000023080)                                                                    
    at /usr/src/debug/ceph-17.2.5-1.fc37.x86_64/src/msg/async/AsyncConnection.cc:454                                  
#21 0x00007ffff6019960 in EventCenter::process_events (this=this@entry=0x616000019000,                                
    timeout_microseconds=<optimized out>, timeout_microseconds@entry=30000000,                                        
    working_dur=working_dur@entry=0x7fffd90ad0b8)                                                                     
    at /usr/src/debug/ceph-17.2.5-1.fc37.x86_64/src/msg/async/Event.cc:422                                            
#22 0x00007ffff601a1f6 in operator() (__closure=<optimized out>)                                                      
    at /usr/src/debug/ceph-17.2.5-1.fc37.x86_64/src/msg/async/Stack.cc:50                                             
#23 std::__invoke_impl<void, NetworkStack::add_thread(Worker*)::<lambda()>&> (__f=...)                                
    at /usr/include/c++/12/bits/invoke.h:61                                                                           
#24 std::__invoke_r<void, NetworkStack::add_thread(Worker*)::<lambda()>&> (__fn=...)                                  
    at /usr/include/c++/12/bits/invoke.h:111                                                                          
#25 std::_Function_handler<void(), NetworkStack::add_thread(Worker*)::<lambda()> >::_M_invoke(const std::_Any_data &) 
    (__functor=...) at /usr/include/c++/12/bits/std_function.h:290                                                    
#26 0x00007ffff66dbc03 in execute_native_thread_routine () from /usr/lib64/libstdc++.so.6                             
#27 0x00007ffff6aae12d in start_thread () from /usr/lib64/libc.so.6                                                   
#28 0x00007ffff6b2fbc0 in clone3 () from /usr/lib64/libc.so.6                                                         
```
And it looks like some internal openssl's initialization of some thread-local variable. And it only happens on Fedora 37 (which has openssl 3.0.8), and doesn't reproduce on Fedora 35 (with openssl 1.1.1o), so I think it might be openssl problem. But I haven't been able to prove it yet and haven't found any matching issue on their tracker. So currently, the only thing that I can think of to prevent this is to completely disable reporting leaks from openssl (adding `leak:libcrypto.so` to asan suppression file), but I'm not sure if we want to do that, since it'd also hide issues in our code.


## Comment 1472572005

reporter (CONTRIBUTOR) · karlatec · 2023-03-16T18:49:49Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1472572005

> , the only thing that I can think of to prevent this is to completely disable reporting leaks from openssl (adding leak:libcrypto.so to asan suppression file), but I'm not sure if we want to do that, since it'd also hide issues in our code.

I assume that if you're right and this is caused by openssl then the only way to fix this is to upgrade it's version? If so, then I think that adding this rule to suppress file is the way to go, at least for now. That way we can filter out this one library instead of removing ASAN scans completely from at least two CI jobs (crypto-autotest and iscsi-vg-autotest which runs RBD tests too).
If we decide to do it we can keep the issue open and periodically try removing suppression rule any time we deploy new OS images in CI.

I've submitted a patch adding the rule here: https://review.spdk.io/gerrit/c/spdk/spdk/+/17217/1
If it works fine then we should see crypto job passing in https://ci.spdk.io/public_build/autotest-per-patch_100380.html 

## Comment 1473277649

other (CONTRIBUTOR) · ksztyber · 2023-03-17T07:09:42Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1473277649

> I assume that if you're right and this is caused by openssl then the only way to fix this is to upgrade it's version? If so, then I think that adding this rule to suppress file is the way to go, at least for now.

I'm not 100% sure that's it's openssl yet (could be that we're not doing some required cleanup properly), but it certainly looks like it.

> That way we can filter out this one library instead of removing ASAN scans completely from at least two CI jobs (crypto-autotest and iscsi-vg-autotest which runs RBD tests too).

Agreed.



## Comment 1475931031

reporter (CONTRIBUTOR) · karlatec · 2023-03-20T09:59:39Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1475931031

Build with all `--with` flags and modified asan suppression file: https://ci.spdk.io/public_build/autotest-per-patch_100449.html
Both crypto and iscsi jobs passing.

## Comment 1478012851

other (CONTRIBUTOR) · ksztyber · 2023-03-21T15:10:22Z · https://github.com/spdk/spdk/issues/2947#issuecomment-1478012851

[Bug scrub] Konrad will try to create a small example to reproduce this without SPDK and will file a GH issue against OpenSSL.
