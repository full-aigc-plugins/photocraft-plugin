# 首次安装的并发协调 / Concurrent first-use installation

同一 CLI 的安装或复用先取得用户运行时目录中的安装锁。竞争者以单调时钟最多等待 120 秒，取得锁后重新核验原子发布的二进制摘要和安装回执；不会重复下载已经有效的版本。等待超时返回 runtime_install_busy，保留已有安装和工程。操作系统在持锁进程退出时释放锁，不凭锁文件或旧 PID 判断活动进程。

CLI installation and reuse acquire the runtime-directory install lock. A competing process waits up to 120 seconds using a monotonic clock, then verifies the atomically published binary digest and receipt. Valid installed versions are reused without another download. Timeout returns runtime_install_busy and preserves the installation and projects; the OS releases the lock when its owner exits.

等待仅针对安装互斥。编辑、渲染和结果未知的任务不得因为此等待逻辑自动重放。不同工程仍遵循领域单写和原生能力范围。并行技术样本只能证明已测试的平台、负载与任务；不代表无限并发或生产容量保证。

Waiting applies only to dependency installation. It must not replay editing, rendering or unknown native outcomes. Native project ownership and supported capabilities still apply. Parallel fixture tests establish the tested platform/workload, not unlimited concurrency or production capacity.
