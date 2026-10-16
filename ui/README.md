# photocraft 编辑器接入

本地开发候选。`dist/` 是可分发运行制品，已忽略，不提交 WASM 和用户素材。宿主运行需要 Node.js 24+，构建依赖只安装到本项目目录。

## 构建

可分发插件包已包含 `dist/`，运行不需要 Rust 或 node_modules。开发时先具备项目 JavaScript 依赖、Rust wasm32 target 与匹配 Cargo.lock 的 wasm-bindgen CLI；构建脚本不会自动安装工具。

在本目录构建一个全新的独立候选：

```bash
node build.mjs
python3 build-source.py --output /absolute/fresh-build --target-dir /absolute/cargo-target
```

`source.lock.json` 固定源码仓库及提交；脚本下载到新目录，在副本中应用 `runtime/` 补丁，通过 Cargo + wasm-bindgen 编译，提取真实工具目录并生成 `/absolute/fresh-build/packaged/editor`。`BUILD.json` 和许可证随制品保留。输出目录已存在时拒绝覆盖。

`prepare.mjs` 用于导入与 `editor.lock.json` 完全匹配的已验证制品；新的源码构建应先进行编辑、保存、重开回归，再生成对应锁文件并放入独立分发包。不要替换仍被活动会话使用的 `dist/editor`。当前交付包的位置与验证记录见目录仓 `docs/craft-source-integration.md`。

## 插件安装与界面

优先通过插件市场安装完整发布包，不需要手工填写每个 MCP 的绝对路径。开发仓必须先构建编辑器资源；仅克隆源码不等于已安装运行包。

| 入口 | 配置 | 路径基准 |
| --- | --- | --- |
| 标准 Agent Plugins | `plugin.json`、`mcp.json` | `${PLUGIN_ROOT}` 由支持该规范的宿主展开 |
| Codex | `.codex-plugin/plugin.json`、`.codex-plugin/mcp.json` | 相对 `cwd` 由宿主定位到插件根目录 |
| Claude Code | `.claude-plugin/plugin.json`、根 `.mcp.json` | `${CLAUDE_PLUGIN_ROOT}` 由宿主展开 |

连接后调用 `open_editor` 或 `open_browser_editor`，显式传入本次任务目录 `workspace`。这是用户文件的位置，不是插件安装位置，不写死在安装清单中。

支持 MCP Apps 的宿主可呈现工具关联的 UI 资源；支持内置浏览器的桌面宿主可打开 `open_browser_editor` 返回的地址。Claude Code 终端本身不提供浏览器面板。支持插件或 stdio MCP 并不自动意味着支持内嵌 UI；缺少 UI 能力时只能在浏览器打开同一会话，不能宣称宿主内嵌已通过。

stdio 负责 Agent 与插件通信，本地 HTTP 负责页面和同会话编辑桥接。Agent 指令作用于当前页面的编辑器状态；等待 `editor_status` 就绪后再执行编辑。保存源工程后重开检查，关闭 MCP 进程前先保存。

本轮优先验证标准插件入口、Codex 和 Claude Code 清单。仅支持 MCP 的工具不属于当前安装交付范围。

## 会话与文件

本地浏览器桥接只监听 127.0.0.1，随机令牌、Host/Origin 校验保护入口。工作区外路径被拒绝。浏览器手动导出保存到工作区 craft-exports，采用新文件名；工具指定的输出遵循对应工具契约。关闭 MCP 进程会结束当前编辑会话；先保存源工程。

必须重开保存的工程并检查实际内容，不能以浏览器存储或任务提交替代工作区交付。

## 验证范围

自动化浏览器检查、原生插件加载和宿主内嵌界面是不同验证层。当前状态见目录仓 docs/craft-editor-delivery.md；此文件不宣称所有宿主或所有场景已验收。新增场景位于 docs/scene-skills.md，原有锁定技能快照保持不变。

## 最新编辑器与内置回退

宿主与插件之间使用 **stdio MCP**；本地 HTTP 仅承载编辑器页面与页面桥接，不作为远程 MCP 服务。stdio 避免本地工具调用引入 HTTP MCP 服务，但整体编辑速度仍取决于引擎、素材和页面，不宣称未经测量的性能倍数。

首次调用 `open_editor` / `open_browser_editor` 时查询本插件 `full-aigc-plugins/*-plugin` 的最新稳定增强发行，下载并校验完整 WASM/JS 包。增强包由锁定的 fork 或上游源码构建，保留 同会话 UI 线程命令与文件桥接；原版 Web ZIP 不会替换增强运行时。不会下载 CLI 或升级宿主插件。

元数据请求超时 5 秒、归档下载超时 45 秒；HTTP 失败、缺少 SHA-256、摘要不符、异常 ZIP、工具输入契约变化或缓存损坏时使用内置版本。校验通过的下载缓存在 `~/.cache/full-aigc/editors`，可以用 `CRAFT_EDITOR_CACHE_DIR` 指定其他绝对目录。活动会话固定版本，重开页面不重新切换；缓存损坏会回退，不自动删除已有缓存。

`editor_status` 和打开工具结果中的 `runtime` 返回 `source`（download/cache/bundled）、`version`、下载摘要或 `reason`。`version` 是增强包版本，`upstream.version` 与 `upstream.commit` 标识引擎源码；旧运行时快照使用独立的来源标记。结构与工具 schema 校验不能保证未来上游版本的全部运行行为；升级后的实际编辑需按场景检查。

需要完全离线时，在现有 stdio MCP 配置的 env 中加 `"CRAFT_EDITOR_UPDATE": "off"`，直接使用内置包。更新不修改包内 `ui/dist/editor` 和原来的锁文件；内置版本始终保留。内置资源缺失仍是安装包错误，不能依赖网络掩盖。

## 插件安装与界面

优先通过插件市场安装完整发布包，不需要手工填写每个 MCP 的绝对路径。开发仓必须先构建编辑器资源；仅克隆源码不等于已安装运行包。

| 入口 | 配置 | 路径基准 |
| --- | --- | --- |
| 标准 Agent Plugins | `plugin.json`、`mcp.json` | `${PLUGIN_ROOT}` 由支持该规范的宿主展开 |
| Codex | `.codex-plugin/plugin.json`、`.codex-plugin/mcp.json` | 相对 `cwd` 由宿主定位到插件根目录 |
| Claude Code | `.claude-plugin/plugin.json`、根 `.mcp.json` | `${CLAUDE_PLUGIN_ROOT}` 由宿主展开 |

连接后调用 `open_editor` 或 `open_browser_editor`，显式传入本次任务目录 `workspace`。这是用户文件的位置，不是插件安装位置，不写死在安装清单中。

支持 MCP Apps 的宿主可呈现工具关联的 UI 资源；支持内置浏览器的桌面宿主可打开 `open_browser_editor` 返回的地址。Claude Code 终端本身不提供浏览器面板。支持插件或 stdio MCP 并不自动意味着支持内嵌 UI；缺少 UI 能力时只能在浏览器打开同一会话，不能宣称宿主内嵌已通过。

stdio 负责 Agent 与插件通信，本地 HTTP 负责页面和同会话编辑桥接。Agent 指令作用于当前页面的编辑器状态；等待 `editor_status` 就绪后再执行编辑。保存源工程后重开检查，关闭 MCP 进程前先保存。

本轮优先验证标准插件入口、Codex 和 Claude Code 清单。仅支持 MCP 的工具不属于当前安装交付范围。
