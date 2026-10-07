# 【Bug】 SG2042/openEuler 24.03 SP1和SP2 环境下 K8s 负载出现严重的 struct pid 内存泄露

- URL: https://github.com/RVCK-Project/rvck/issues/209
- Repo: RVCK-Project/rvck (language: C)
- State: open; created 2026-02-02T03:33:00Z; status ok; passes offcwe

## Issue body

reporter (NONE) · ffkk722 · 2026-02-02T03:33:00Z · https://github.com/RVCK-Project/rvck/issues/209

一、Environment / 环境信息
- Hardware / 硬件: Milk-V Pioneer (SG2042, RISC-V 64)
- OS / 操作系统: openEuler 24.03 LTS SP2
- Kernel / 内核: 6.6.0-98.0.0.103.oe2403sp2.riscv64
- Workload / 负载: Kubernetes (K8s) Cluster - Master Node

二、Symptom / 现象
   在 Kubernetes 集群运行期间，观测到内核内存占用持续上升，最终导致 OOM 和系统死机。通过 kmemleak 分析，确认 struct pid 对象（128字节）正在大量泄露。
  During the operation of the Kubernetes cluster, we observed a continuous increase in kernel memory usage, eventually leading to OOM and system hang. Using kmemleak, we identified that struct pid objects (128 bytes) are being leaked massively.

Key Observations / 关键观察:

- Frequency / 频率: The leak occurs linearly with the creation/destruction of containers (processes).
- Refcount / 引用计数: The hex dump shows the struct pid has a refcount of 1 (01 00 00 00), indicating some component is holding a reference but never releasing it (put_pid).
- Trace / 堆栈: The allocation backtrace points to the standard clone syscall (__riscv_sys_clone -> copy_process -> alloc_pid).

三、Log Evidence / 日志证据
kmemleak output (90+ similar entries found):

unreferenced object 0xffffffe00358bf00 (size 128):
  comm "kube-controller", pid 3789, jiffies 4295673747
  hex dump (first 32 bytes):
    01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00  <-- Refcount = 1
  backtrace:
    __create_object+0x20/0xa0
    kmemleak_alloc+0x40/0x78
    kmem_cache_alloc+0x22e/0x4b0
    alloc_pid+0x62/0x322
    copy_process+0x58c/0x1036
    kernel_clone+0x78/0x39a
    __se_sys_clone+0x6c/0x8a
    __riscv_sys_clone+0x18/0x20
    do_trap_ecall_u+0x72/0x14a
    ret_from_exception+0x0/0x64

Associated Leaks / 关联泄露:
   同时注意到 apparmor 安全上下文和 Socket 创建也存在泄露，这可能与 PID 泄露有关。 
  We also noticed leaks in apparmor security contexts and socket creations, which might be related to the PID leak.

unreferenced object 0xfffffff031485390 (size 16):
  comm "kube-apiserver"
  backtrace:
    kmalloc_trace
    apparmor_sk_alloc_security
    security_sk_alloc
    sk_alloc
    inet6_create

[long_text_1BBAFC73-6079-49A7-BA37-348EAAA4E722.txt](https://github.com/user-attachments/files/24999317/long_text_1BBAFC73-6079-49A7-BA37-348EAAA4E722.txt)

Request for Help / 诉求
  目前已将问题范围锁定在涉及 struct pid 的内核态泄露，但受限于专业调试工具的缺失以及对 SG2042 BSP 实现细节的了解不足，难以精确定位具体的责任模块。诚挚请求社区和厂商专家协助排查泄露源头。我可以配合提供更多日志或执行验证测试，共同解决这一关键的稳定性问题。
  We have narrowed down the issue to a kernel-space leak involving struct pid, but due to the lack of specialized debugging tools and deep knowledge of the SG2042 BSP implementation, we are unable to pinpoint the exact module responsible. We kindly request the support of community and vendor experts to help trace the leak source. We remain fully available to provide further logs or conduct testing to resolve this critical stability issue together.

## Comment 3834814443

maintainer (COLLABORATOR) · sterling-teng · 2026-02-02T12:24:24Z · https://github.com/RVCK-Project/rvck/issues/209#issuecomment-3834814443

你好，方便提供复现环境和步骤吗？

## Comment 3839301797

reporter (NONE) · ffkk722 · 2026-02-03T06:19:15Z · https://github.com/RVCK-Project/rvck/issues/209#issuecomment-3839301797

> 您好，方便提供详细的环境和步骤吗？
您好 @sterling-teng ，感谢您的快速回复。

关于复现环境：
环境是 Milk-V Pioneer 开发板 (SG2042)，运行 openEuler 24.03 LTS SP2。
负载是 单节点 Kubernetes Master 并在其上运行 Prometheus 监控。
由于 K8s 组件是我们团队针对该 RISC-V 开发板内部交叉编译的，依赖较多，打包完整的环境供您在本地复现会比较复杂且容易出错。

我可以提供远程桌面连接（例如通过 ToDesk, 或会议链接），通过我的电脑直接访问该开发板环境。

请告知我您的邮箱地址，以便安全地发送连接信息并协调合适的时间。


## Comment 5473161220

maintainer (COLLABORATOR) · unicornx · 2026-08-31T03:02:40Z · https://github.com/RVCK-Project/rvck/issues/209#issuecomment-5473161220

@ffkk722 你好，最近我在清理 rvck 这里的 issues。请问这个问题是否还继续存在？如无问题请关闭这个 issue。
