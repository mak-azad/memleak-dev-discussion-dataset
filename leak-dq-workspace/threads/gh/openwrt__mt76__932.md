# possible memleak detected by kmemleak

- URL: https://github.com/openwrt/mt76/issues/932
- Repo: openwrt/mt76 (language: C)
- State: open; created 2024-11-18T02:17:13Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ptpt52 · 2024-11-18T02:17:13Z · https://github.com/openwrt/mt76/issues/932

mt7915 (mt7981)
enable kernel options:
```diff
diff --git a/target/linux/mediatek/filogic/config-6.6 b/target/linux/mediatek/filogic/config-6.6
index 9fe080bbbbc..be27783ed1a 100644
--- a/target/linux/mediatek/filogic/config-6.6
+++ b/target/linux/mediatek/filogic/config-6.6
@@ -141,6 +141,10 @@ CONFIG_CRYPTO_SM4_ARM64_CE_GCM=y
 CONFIG_CRYPTO_ZSTD=y
 CONFIG_DCACHE_WORD_ACCESS=y
 CONFIG_DEBUG_INFO=y
+CONFIG_DEBUG_KMEMLEAK=y
+CONFIG_DEBUG_KMEMLEAK_AUTO_SCAN=y
+# CONFIG_DEBUG_KMEMLEAK_DEFAULT_OFF is not set
+CONFIG_DEBUG_KMEMLEAK_MEM_POOL_SIZE=16000
 CONFIG_DEBUG_MISC=y
 CONFIG_DIMLIB=y
 CONFIG_DMADEVICES=y
@@ -225,6 +229,7 @@ CONFIG_IRQ_TIME_ACCOUNTING=y
 CONFIG_IRQ_WORK=y
 CONFIG_JBD2=y
 CONFIG_JUMP_LABEL=y
+CONFIG_KALLSYMS=y
 CONFIG_LEDS_PWM=y
 CONFIG_LEDS_SMARTRG_LED=y
 CONFIG_LIBFDT=y
@@ -460,6 +465,9 @@ CONFIG_SPI_MT65XX=y
 # CONFIG_SPI_MTK_NOR is not set
 CONFIG_SPI_MTK_SNFI=y
 CONFIG_SQUASHFS_DECOMP_MULTI_PERCPU=y
+CONFIG_STACKDEPOT=y
+CONFIG_STACKDEPOT_ALWAYS_INIT=y
+CONFIG_STACKTRACE=y
 CONFIG_SWIOTLB=y
 CONFIG_SWPHY=y
 CONFIG_SYSCTL_EXCEPTION_TRACE=y
```
log:
```
unreferenced object 0xffffff800ab2e780 (size 128):
  comm "mt76-tx phy0", pid 1489, jiffies 4294981471 (age 1169.570s)
  hex dump (first 32 bytes):
    2c 05 00 12 08 84 00 d1 28 00 00 00 02 78 00 20  ,.......(....x. 
    00 00 00 00 02 00 00 00 00 00 00 00 00 04 28 00  ..............(.
  backtrace:
    [<00000000e8ddd2ed>] __kmem_cache_alloc_node+0x1c0/0x2c0
    [<00000000b1f94e8f>] __kmalloc+0x80/0xd0
    [<000000002345fba3>] mt76_dma_cleanup+0x608/0x8a4 [mt76]
    [<000000008e536771>] mt76_tx_check_agg_ssn+0xa0/0x114 [mt76]
    [<0000000005904cb2>] __mt76_tx_complete_skb+0x9a0/0xaf8 [mt76]
    [<0000000049793883>] mt76_tx_worker+0xb4/0x1dc [mt76]
    [<000000009a7fb220>] __mt76_worker_fn+0x8c/0xdc [mt76]
    [<00000000584182c8>] kthread+0xd8/0xdc
    [<0000000028c29abf>] ret_from_fork+0x10/0x20
unreferenced object 0xffffff800ab2e380 (size 128):
  comm "mt76-tx phy0", pid 1489, jiffies 4294981471 (age 1169.570s)
  hex dump (first 32 bytes):
    2c 05 00 12 08 84 00 d1 28 00 00 00 02 78 00 20  ,.......(....x. 
    00 00 00 00 02 00 00 00 00 00 00 00 00 04 28 00  ..............(.
  backtrace:
    [<00000000e8ddd2ed>] __kmem_cache_alloc_node+0x1c0/0x2c0
    [<00000000b1f94e8f>] __kmalloc+0x80/0xd0
    [<000000002345fba3>] mt76_dma_cleanup+0x608/0x8a4 [mt76]
    [<000000008e536771>] mt76_tx_check_agg_ssn+0xa0/0x114 [mt76]
    [<0000000005904cb2>] __mt76_tx_complete_skb+0x9a0/0xaf8 [mt76]
    [<0000000049793883>] mt76_tx_worker+0xb4/0x1dc [mt76]
    [<000000009a7fb220>] __mt76_worker_fn+0x8c/0xdc [mt76]
    [<00000000584182c8>] kthread+0xd8/0xdc
    [<0000000028c29abf>] ret_from_fork+0x10/0x20
```
