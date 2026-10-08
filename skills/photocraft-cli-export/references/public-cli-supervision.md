# 公开 CLI 逐步监督

对应 PC-TX-005 / 任务 9.6 的增量；开发版本，不关闭完整任务。

`cli.py` 的 run、batch、convert、droplet 在安装与摘要校验后，先核对原生监督元数据和锁定版本，再按逐步确认协议调用固定 craft.5。其他只读入口沿用原调用方式。

每个事件核对严格 JSON、序号、工具、实参及工具回复；打开与保存核对路径，batch 绑定输入和输出顺序。仅验证成功才发送 continue。合法调用保留原有可见输出。

回复损坏、语义错误或未知结果立即停止继续确认并收束本次子进程。失败输出保留 code、phase、outcome、retryable、recoveryAction、receipts、lastAttempt 和运行时摘要；replayAllowed 为 false。已有文件保留，不声称回滚已执行操作。

15 个真实原生保存后故障场景覆盖四入口：测试仅在原生回复传输层注入错误，核对后续编辑停止、原工程摘要不变、保存文件可重新打开及未自动重放。安装副本验收与源码回归分别记录。

流式 mcp/serve、TCP/port 和嵌套聚合回复尚未接入此监督；本合同不代替工作流的 protectedRegions、像素保全或完整首版验收。
