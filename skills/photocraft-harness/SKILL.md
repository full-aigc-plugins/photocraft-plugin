---
name: photocraft-harness
description: PhotoCraft 内置执行 harness——所有 photocraft 领域技能（photocraft-use、photocraft-cli 及各场景技能）的统一执行通道。首次安装固定 CLI、查询或执行原生命令、workflow 编排、桌面桥接、连续任务会话、交付与进度核验时，经由本技能的入口脚本执行；领域技能只提供场景知识、计划与示例，不自带脚本。
license: Apache-2.0
---

# PhotoCraft Harness（内置执行通道）

本技能是 PhotoCraft 技能套件的**唯一执行实现**：首次安装、原生命令调用、workflow 编排、桌面桥接、连续任务会话与交付核验都收敛在本目录 `scripts/` 内。`photocraft-use`、`photocraft-cli` 及各领域技能是薄文档技能——它们提供场景指引、计划示例与参考契约，实际执行一律经由本技能的入口。**执行任何 PhotoCraft 脚本前，先把 `HARNESS_DIR` 设为本 `SKILL.md` 所在目录（宿主实际加载的绝对路径），不要假设当前工作目录就是技能目录。** 用户级安装可能位于 `~/.agents/skills/photocraft-harness`，项目级可能位于 `.agents/skills/photocraft-harness`，插件可能位于其 `skills/photocraft-harness` 或宿主缓存目录；以宿主实际加载路径为准。领域技能文档中的 `SKILL_DIR` 指领域技能自身目录（用于读取其 `examples/`、`references/`），与本 harness 是两个位置。

## 入口

| 入口 | 用途 |
|---|---|
| `scripts/bootstrap.py` | 首次使用安装器：仅用标准库安装锁定的官方 CLI（`runtime.lock.json` 固定版本与摘要），返回 JSON `executable`。 |
| `scripts/cli.py` | 公开 CLI 通道：按 argv 调用固定二进制；`--` 后放原生子命令，另有 `mcp` 与 `serve` 会话入口。 |
| `scripts/commands.py` | 原生命令单技能入口：`list` / `describe` / `check` / `run`，参数说明、实时前置检查、同会话调用及失败回执。 |
| `scripts/workflow.py` | 原生分层计划执行器：独立会话、限定读写目录和不可变修订交付。 |
| `scripts/desktop.py` | 桌面桥接：按固定官方 DMG 安装桌面应用并执行桌面计划；与 CLI 缓存分离。 |
| `scripts/task_session.py` | 连续任务会话：逐阶段调用原命令入口，复用一个所属实例，不重启或重放。 |
| `scripts/route.py` | 意图路由查询：`route.py INTENT` 返回最短技能链；只读合同查询，不代替宿主模型理解。 |
| `scripts/delivery.py` | 交付完整性：只读核对交付清单、依赖和交换身份；不安装运行时。 |
| `scripts/progress.py` | 进度观察：原子进度快照的只读查询，不安装、不启动会话、不授予重放或修订权限。 |
| `scripts/native_verify.py` | 交付核验：使用已安装固定二进制在新会话只读重开；不安装、不修改交付包。 |
| `scripts/native_workflow.py` | 工作流网关：完整反射命令接入受核验工作流；交付由原生保存、重开及依赖门禁决定。 |
| `scripts/checkpoint_verify.py` | 检查点核对：只读核对失败暂存并重开原工程；不将部分成功升级为交付通过。 |

其余 `scripts/` 文件是上述入口的内部依赖（协议、守卫与合同模块），不单独调用。

## 用法

场景指引、计划与示例文件取自对应领域技能目录（`SKILL_DIR/examples/`、`SKILL_DIR/references/`）；执行路径一律使用本目录 `HARNESS_DIR/scripts/`。

首次安装（无预装 CLI 时；安装范围是用户数据目录，不需要 sudo）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
```

原生命令直连与命令目录查询（cli.py 的原生子命令须放在 `--` 之后；commands.py 输出恒为 JSON）：

```bash
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- --version
python3 -I -B "$HARNESS_DIR/scripts/cli.py" -- commands --json
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter QUERY
python3 -I -B "$HARNESS_DIR/scripts/commands.py" describe COMMAND_ID
```

持续交互可使用 `cli.py -- mcp` 或 `cli.py serve`（stdio/TCP）；连续检查、编辑、保存、重开使用 `task_session.py`。桌面安装与 GUI 计划见领域技能的 [固定桌面安装] 参考，入口为 `scripts/desktop.py`。

## 领域技能与本 harness 的关系

- `photocraft-use`：完整任务路由与交付合同；执行仍走本 harness。
- `photocraft-cli` 与各场景技能（setup/project/layers/selection/masks/adjustments/retouch/text/resize/export/filters）：场景知识与参数契约；执行仍走本 harness。
- 领域技能文档引用脚本时一律写作 `$HARNESS_DIR/scripts/<入口>`；`references/` 中的执行契约 JSON（commands、command-coverage、native-command-snapshot、desktop-command-snapshot、routing-contract）在本技能内与 `photocraft-use` 保持字节一致，领域技能各自保留其场景参考。
- 交付、移动包或源工程返工前按领域技能的交付完整性参考执行 `scripts/delivery.py`；只读检查无需安装运行时。

## 当前范围

固定 CLI 的版本与制品摘要以本技能 `scripts/runtime.lock.json` 为准；技能包版本以对应发布标签为准。独立安装复验与全量逐命令验收分别记录，不以发布替代验收。目录覆盖与直接原生使用不等于所有指令、GUI、交付或 Art 编排已验收。
