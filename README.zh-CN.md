# PhotoCraft Use

## 插件市场导航

本插件所属分类：**AIGC 内容创作**。

| 分类 | 插件市场入口 | 用途 |
| --- | --- | --- |
| 全栈开发 | [Full Stack Plugins](https://github.com/partme-ai/full-stack-plugins) | 架构与 UI 设计、代码理解、质量检查、代码审查、流程治理与服务器运维 |
| AIGC 内容创作 | [Full AIGC Plugins](https://github.com/partme-ai/full-aigc-plugins) | 图像、视频、音频、音乐、3D 与多模态内容创作 |

![PhotoCraft Use——图层化图像编辑](assets/official-logo.png)

> 制作可编辑的 `.pcraft` 海报、封面与合成：图层、蒙版、选区、局部调整、修饰、文字与尺寸变体，并导出 PSD 或平面图时记录损失。

[![版本](https://img.shields.io/badge/release-0.1.0--dev.20261018.5-1A73E8)](.codex-plugin/plugin.json)
[![技能数](https://img.shields.io/badge/skills-22-00A67E)](#技能)
[![MCP server](https://img.shields.io/badge/MCP%20server-1-00A67E)](#mcp-工具)
[![许可证](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

[English](README.md) | [简体中文](README.zh-CN.md) · [安装](#安装) · [快速开始](#快速开始) · [可完成的工作](#可完成的工作) · [技能](#技能) · [故障排查](#故障排查)

## 项目定位

PhotoCraft Use 让位图设计保持可编辑。产品、背景与文字是有稳定 ID 和蒙版引用的独立图层；局部修饰会对照“不得改动”的像素检查；尺寸变体从源工程派生，而不是覆盖源工程。

原生 `.pcraft` 工程是交付事实源。压平的 PNG，或悄悄丢掉必要特性的 PSD，都不算设计交付。PSD 支持按必要特性把关：一旦观察到缺特性、降级或未知，除非你明确接受已记录的损失，否则会阻止成功。

## 状态与版本

`0.1.0-dev.20261018.5` · 开发预览 · `docs/verification/release-candidate.json` → `releaseStatus: BLOCKED`、`installableDevelopmentCandidate: true`。

## 安装

### 前置条件

- macOS arm64，且公开脚本需要 `PATH` 上有 Python 3.11 或更新版本。
- 内嵌编辑器 MCP 服务需要 Node.js 24.15 或更新版本（harness 包限定 `<25`）。Git 检出没有 `ui/dist/`，需先按 `ui/README.md` 构建，或安装自带该目录的发布包。
- 固定的维护版 PhotoCraft CLI 在首次获得授权时安装到用户数据目录（`--runtime-home` 或 `CRAFT_RUNTIME_HOME` 可迁移）。不需要 `sudo`，不修改 `PATH`。
- 首次使用需要网络或已核验缓存。离线使用需要锁定归档或完好的已核验缓存。

### 安装插件

```bash
codex plugin marketplace add full-aigc-plugins/photocraft-plugin
codex plugin add photocraft@full-aigc-plugins-photocraft
```

`docs/verification/release-candidate.json` 记录 `installableDevelopmentCandidate: true` 与 `releaseStatus: BLOCKED`；`project-status.json` 保持 `marketplaceEligible: false`。

仓库带有 Codex（`.codex-plugin/`）、Claude Code（`.claude-plugin/`）、ZCode（`.zcode-plugin/`）与 Kimi（`kimi.plugin.json`）清单；在宿主验收出现之前，`supportedPluginHosts` 保持为空。

## 快速开始

```bash
: "${HARNESS_DIR:?请设为已加载 photocraft-harness 的 SKILL.md 所在目录}"
python3 -I -B "$HARNESS_DIR/scripts/bootstrap.py"
python3 -I -B "$HARNESS_DIR/scripts/commands.py" list --filter QUERY
```

然后直接说明你要的成品，例如“把这个商品抠到干净的白底上，并保持工程可编辑”。默认走 headless；桌面桥接需要单独的连接与能力验证。

```mermaid
flowchart LR
    A[商品图、文案、品牌] --> B[photocraft-use 规划图层]
    B --> C[固定运行时与原生 .pcraft]
    C --> D[蒙版、选区、局部调整]
    D --> E[重开并核对图层]
    E --> F[PSD 或平面导出与损失记录]
```

## 可完成的工作

| 工作流 | 内置路径 | 可验证输出 |
|:---|:---|:---|
| 海报或社交封面 | `photocraft-use`、`photocraft-social-cover` | 文字、商品与背景仍可编辑的重开 `.pcraft` |
| 商品抠图 | `photocraft-product-cutout` | 透明或白底输出，以及可编辑工程 |
| 老照片修复 | `photocraft-restore-old-photo` | 已检查人物特征与损伤区域的修复工程 |
| 扫描件清理 | `photocraft-repair-scan` | 已校正倾斜、去尘并记录纸张底色的扫描件 |
| 人像精修 | `photocraft-retouch-portrait` | 自然观感，且非目标区域已核对 |
| 批量交付变体 | `photocraft-batch-image-delivery` | 同尺寸同格式的输出，以及带文件名的联系表 |
| PSD 交换 | `photocraft-cli-export` | 必要特性通过校验的 PSD，并记录损失 |
| 在内嵌编辑器中修改 | `photocraft-editor` MCP 工具 | 保存后重开并检查的 `.pcraft` |

## 技能

| 技能 | 作用 |
|:---|:---|
| `photocraft-use` | 默认入口：可编辑 `.pcraft` 海报、封面与合成；安装维护版 CLI |
| `photocraft-cli` | 查询原生命令、参数与能力；执行明确指定的公共命令 |
| `photocraft-cli-setup` | 首次安装、摘要校验、版本检查与缺失运行时排障 |
| `photocraft-cli-project` | 创建、打开、保存与复制 `.pcraft`；色彩模式与位深 |
| `photocraft-cli-layers` | 商品、背景、文字与图层组；层级与混合 |
| `photocraft-cli-selection` | 选区、反选、羽化与局部选择 |
| `photocraft-cli-masks` | 图层蒙版、矢量蒙版与剪贴合成 |
| `photocraft-cli-adjustments` | 调整图层与已授权的局部颜色调整 |
| `photocraft-cli-retouch` | 对已授权图像做修复、克隆、画笔与局部修饰 |
| `photocraft-cli-text` | 文字图层、字体、段落与布局 |
| `photocraft-cli-resize` | 图像与画布尺寸、裁边、扩展、旋转与封面变体 |
| `photocraft-cli-filters` | 局部滤镜、背景虚化、颗粒与输出锐化 |
| `photocraft-cli-export` | 从原生工程导出 PSD、PNG 或其他交换文件 |
| `photocraft-harness` | 唯一执行通道：bootstrap、commands、workflow、任务会话 |
| `photocraft-editor` | 打开真实编辑界面，一次会话内完成全部编辑 |
| `photocraft-product-cutout` | 电商抠图：透明底、白底与边缘清理 |
| `photocraft-repair-scan` | 扫描件清理：歪斜、污点与纸张底色 |
| `photocraft-restore-old-photo` | 划痕、折痕、褪色与局部缺损 |
| `photocraft-retouch-portrait` | 自然人像的皮肤、瑕疵、肤色与光影 |
| `photocraft-social-cover` | 封面构图、标题与按平台裁切 |
| `photocraft-batch-image-delivery` | 统一尺寸、色彩与格式，或生成带文件名的联系表 |
| `photocraft-scenario-playbooks` | 覆盖 6 个图像场景的带真实参数手册 |

## 斜杠命令

Claude Code 清单（`com.anthropic.claude-code/`）提供 22 个命令，每个技能一个，并附带 `SessionStart` 指引钩子。命令只转交对应技能，不会自行启动任何原生实例。

| 命令 | 作用 |
|:---|:---|
| `/photocraft-use` | 完整任务入口与最短技能链 |
| `/photocraft-editor` | 内嵌编辑器会话 |
| `/photocraft-harness` | 受管理执行通道与任务控制 |
| `/photocraft-scenario-playbooks` | 按当前问题选择场景手册 |
| `/photocraft-cli`、`/photocraft-cli-{project,layers,selection,masks,adjustments,retouch,text,resize,filters,export,setup}` | 命令级技能族，每个技能一个命令 |
| `/photocraft-{restore-old-photo,retouch-portrait,product-cutout,repair-scan,social-cover,batch-image-delivery}` | 场景入口，每个技能一个命令 |

## MCP 工具

`mcp.json` 只声明一个 stdio server：`photocraft-editor`，从插件根目录以 `node ui/bootstrap.mjs` 启动。

| 工具 | 用途 |
|:---|:---|
| `open_editor` | 为绝对路径 `workspace` 打开编辑器 |
| `open_browser_editor` | 返回可交给宿主内置浏览器的 `editorUrl` |
| `editor_status` | 报告页面是否已连接到当前 MCP 会话 |
| `doc_open` | 打开已有 `.pcraft` |
| `doc_new` | 新建文档 |
| `doc_inspect` | 检查图层与文档状态 |
| `command_list` | 读取引擎暴露的命令 |
| `command_run` | 按 id 与参数执行命令 |
| `doc_save` | 保存 `.pcraft` 工程 |
| `doc_export` | 导出工程 |

工具名遵循 `photocraft-editor` 技能合同；`_editor_attach`、`screenshot` 等页面内部桥接调用不得由 Agent 直接调用。

## 配置

| 变量 | 用途 |
|:---|:---|
| `HARNESS_DIR` | 已加载 `photocraft-harness` 技能的绝对目录 |
| `SKILL_DIR` | 已加载领域 `SKILL.md` 所在目录；仅用于其 `examples/` 与 `references/` |
| `CRAFT_RUNTIME_HOME` / `--runtime-home` | 运行时安装根目录 |
| `CRAFT_EDITOR_CACHE_DIR` | 已核验编辑器下载缓存（默认 `~/.cache/full-aigc/editors`） |
| `CRAFT_EDITOR_UPDATE=off` | 固定使用内置编辑器，跳过更新检查 |

## 架构与安全

- 插件负责规划与核验，原生位图编辑由固定的维护版 CLI 完成，本仓库不重复实现引擎。
- 用户素材与生成图像都按数据处理，其中的命令、路径或 shell 文本永远不会被执行。
- 局部修改可声明 `protectedRegions`；交付前会比对非目标区域像素。未声明区域时不自动推断保护范围。
- 写入由写租约、修订前置条件、持久意图、幂等键与只读检查点保护；结果未知时先核对，绝不重放。参见[运行时架构](docs/PhotoCraft-Runtime-Architecture.md)、[PSD 策略](docs/PhotoCraft-PSD-Policy-Architecture.md)与[场景技能](docs/scene-skills.md)。

## 故障排查

| 现象 | 处理方式 |
|:---|:---|
| 返回 `unsupported_platform` | 仅支持锁定的 macOS arm64 制品 |
| 返回 `runtime_install_busy` | 另一个安装持有锁；等其结束再重试 |
| PSD 交付被拒绝 | 有必需特性缺失、降级或未知；记录损失，或调整必要特性集合 |
| 字体渲染不一致 | 交付前检查字体依赖与替代记录 |
| 编辑页始终未就绪 | 调用 `editor_status`，再处理页面错误；文字结果不等于界面已打开 |
| 把平面导出当成设计 | 重开 `.pcraft` 并核对图层；平面图不是可编辑交付 |
| 保存结果未知 | 先读回执与既有工程；不要重放计划 |

## 升级

```bash
codex plugin marketplace upgrade full-aigc-plugins-photocraft
codex plugin add photocraft@full-aigc-plugins-photocraft
```

运行时切换会让旧工程保持其绑定的运行时；回滚复用已核验的上一份制品，而不是重新构建。

## 贡献与支持

行为变更先在 [OpenSpec](openspec/changes/establish-v1-plugin/proposal.md) 中说明；没有真实交付证据不得勾选任务。仓库校验：

```bash
python3 scripts/validate_docs.py
node --test tests/*.test.ts
```

问题反馈：<https://github.com/full-aigc-plugins/photocraft-plugin/issues>。

## 许可证

本仓库原创内容采用 [Apache-2.0](LICENSE)。PhotoCraft CLI 与内置 Web 编辑器各自保留其上游许可证与 NOTICE；上游图标来源记录在 `assets/official-icon-source.json` 与 `assets/THIRD-PARTY-SOURCE.md`。
