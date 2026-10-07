# 固定桌面安装 / Pinned desktop installation

仅在任务需要GUI时安装桌面；已有headless任务不需要此步骤。当前支持macOS arm64，官方桌面0.2.0与维护CLI分别锁定，不能用应用版本代替CLI版本。设置SKILL_DIR为当前技能真实加载目录。

```bash
python3 -I -B "$SKILL_DIR/scripts/desktop.py" install
```

返回真实.app路径、executable、version、binarySha256与reused。默认独立缓存为用户数据目录下的领域桌面版本目录；可用--runtime-home设置隔离目录。安装不会启动应用、覆盖/更新Applications内的用户应用或改变PATH。固定官方URL、DMG字节数和摘要、应用版本/ID、arm64架构、签名与完整安装树均核验；损坏安装拒绝而不是静默覆盖。文件下载只发生在私有临时目录，跨进程安装串行，失败不发布目标版本。可选--archive仍必须匹配固定制品，不能绕过校验。

桌面启动、真实GUI编辑及保存重开仍须独立验收。Film的live bridge读取已有候选证据；其他领域不能据此声称通过。commands.py --mode bridge仅连接明确的本地活动会话，不能自动回退headless。UI工具与领域命令接口不同：Film ui_inspect/ui_elements是MCP工具，不能使用exec ui.inspect替代。完整命令执行与GUI首用门禁仍开放。

English: install only when GUI is required. This standalone installer pins official DMG/archive/app/binary identities, architecture, signature and the complete installed tree. It uses a separate versioned user-data cache, never overwrites user Applications or modifies PATH, and does not launch the app. Corrupt existing installs fail. Local --archive inputs still require exact identity. Verify launch, selected live bridge and native GUI editing separately; do not treat installation as acceptance of all commands.

## 自动启动并运行 / Owned desktop workflow

设置 SKILL_DIR 为当前技能真实目录，PLAN 为完整 command-plan/v1 文件，OUTPUT 为尚不存在的输出目录。

```bash
python3 -I -B "$SKILL_DIR/scripts/desktop.py" run "$PLAN" --output "$OUTPUT"
```

可用 `--runtime-home` 指定独立缓存；`--input NAME=PATH` 显式导入素材。有效计划会安装已固定的桌面与 CLI，启动隔离应用，在同一桌面会话执行 `commands.py` 工作流，并保留原生工程、导出、journal、desktop.log 与 desktop-session.json。后者记录应用身份、监听端口归属及本次进程已退出。Photo 的 token 文件在退出时删除，GUI 与 CLI 使用同一输出根。只关闭本次拥有的进程，不连接其他用户会话。失败或未知编辑结果保留回执，不自动重放。安装平台仍为 macOS arm64。

English: `run` validates the full command plan, installs both pinned runtimes, starts an isolated owned desktop, verifies that its PID owns the loopback listener, executes the existing bridge gateway, and closes its own processes. Receipts/logs/creative outputs persist; private Photo authentication is removed. Invalid plans do not install or launch. Unknown edits are never retried. Complete per-command acceptance remains separate.
