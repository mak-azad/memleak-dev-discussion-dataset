# [Bug]SG2042 平台特定驱动内存泄露：mango_clk 与 cdns_pcie (openEuler 24.03 SP2)

- URL: https://github.com/RVCK-Project/rvck/issues/208
- Repo: RVCK-Project/rvck (language: C)
- State: open; created 2026-02-02T02:39:04Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ffkk722 · 2026-02-02T02:39:04Z · https://github.com/RVCK-Project/rvck/issues/208

一、Environment / 环境信息
- Hardware / 硬件: Milk-V Pioneer
- CPU: SOPHON SG2042 (RISC-V 64)
- OS / 操作系统: openEuler 24.03 LTS SP2
- Kernel / 内核: 6.6.0-98.0.0.103.oe2403sp2.riscv64
- Workload / 负载: Kubernetes Master Node (Running normally)

二、Symptom / 现象
  After enabling kmemleak on the SG2042 platform, we observed specific memory leaks in the initialization paths of mango_clk and cdns_pcie drivers. Although the leaked amount is small per occurrence, it indicates defects in the BSP driver code quality and memory management logic.
  在 SG2042 平台上开启 kmemleak 后，观测到 mango_clk 和 cdns_pcie 驱动在初始化路径中存在内存泄露。虽然单次泄露量不大，但这表明 BSP 驱动代码质量和内存管理逻辑存在缺陷。

三、Log Evidence / 日志证据
1. mango_clk Leak / mango_clk 泄露
Memory allocated in mango_clk_init is never freed.
mango_clk_init 中分配的内存从未被释放。

unreferenced object 0xffffffd900565100 (size 64):
  comm "swapper/0", pid 0
  backtrace:
    kmalloc_trace+0x26/0xba
    mango_clk_init+0x3c/0x38c
    __mango_clk_pll_of_clk_init_declare+0x10/0x34
    of_clk_init+0x19c/0x29a

2. cdns_pcie Leak / cdns_pcie 泄露
Interrupt resource requested in cdns_pcie_host_probe is leaked.
cdns_pcie_host_probe 中申请的中断资源发生泄露。

unreferenced object 0xffffffd90374f080 (size 128):
  comm "swapper/0", pid 1
  backtrace:
    kmalloc_trace+0x26/0xba
    request_threaded_irq+0x98/0x126
    devm_request_threaded_irq+0x60/0xb0
    cdns_pcie_host_probe+0x4aa/0x5d0

四、Code Analysis / 源码分析
1.Case 1: mango_clk (Logic Error / 逻辑错误)
In mango_clk_init, memory is allocated via kzalloc to clk_data. If dm_mango_register_mux_clks succeeds, the function returns directly without saving the clk_data pointer to any global structure or freeing it. This is a clear memory leak.
在 mango_clk_init 函数中，使用 kzalloc 分配了 clk_data。如果 dm_mango_register_mux_clks 执行成功，函数直接返回，既没有将 clk_data 指针保存到全局结构中，也没有释放它。这是明显的内存泄露。

/* Code Snippet from mango_clk */
clk_data = kzalloc(sizeof(*clk_data), GFP_KERNEL); // Allocation
// ...
ret = dm_mango_register_mux_clks(node, clk_data);
// ...
if (!ret)
    return; // <--- LEAK HERE! Memory is lost. / 泄露点！内存丢失。

no_match_data:
    kfree(clk_data); // Only freed on error path / 仅在错误路径释放

2.Case 2: cdns_pcie (Resource Management Issue / 资源管理问题)
In cdns_pcie_host_probe, specifically within the Sophgo-specific initialization logic (cdns_pcie_host_sophgo_init), devm_request_irq is called. The log shows the struct irqaction (size 128) is leaked. This suggests that the interrupt descriptor is not correctly managed or cleaned up, possibly due to improper handling in the probe error path or device reset sequence on SG2042.
在 cdns_pcie_host_probe 中，特别是涉及 Sophgo 特有的初始化逻辑 (cdns_pcie_host_sophgo_init) 时，调用了 devm_request_irq。日志显示 struct irqaction (大小 128) 发生泄露。这表明中断描述符未被正确管理或清理，可能是因为在 Probe 错误路径或 SG2042 设备复位序列中处理不当。

[log20260128.txt](https://github.com/user-attachments/files/24998823/log20260128.txt)

/* Code Snippet from cdns_pcie */
// Inside interrupt init logic
ret = devm_request_irq(dev, rc->msi_irq, cdns_pcie_irq_handler, ...);
if (ret) {
    goto err_init_irq; // Complex error handling might miss cleanup
}


## Comment 3834819252

maintainer (COLLABORATOR) · sterling-teng · 2026-02-02T12:25:22Z · https://github.com/RVCK-Project/rvck/issues/208#issuecomment-3834819252

麻烦算能的老师帮忙看下。

## Comment 5473163839

maintainer (COLLABORATOR) · unicornx · 2026-08-31T03:03:09Z · https://github.com/RVCK-Project/rvck/issues/208#issuecomment-5473163839

@ffkk722 你好，最近我在清理 rvck 这里的 issues。请问这个问题是否还继续存在？如无问题请关闭这个 issue。
