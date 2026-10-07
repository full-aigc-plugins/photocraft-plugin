---
name: photocraft-cli-adjustments
description: 当需要使用调整图层或指定局部颜色调整时使用 PhotoCraft；本技能自带首次安装与公开 CLI 入口。
license: Apache-2.0
---

# PhotoCraft 非破坏调整

本技能负责使用调整图层或指定局部颜色调整。与同包技能按名称交接，单独安装即可使用，不读取兄弟目录。调用固定官方 photocraft-cli，保留原生编辑工程。

## 输入与交付

输入为用户已确认的任务、素材、工程或对象、输出目录与修改范围；需要现有工程时先核对摘要。返回实际 CLI 结果、保存后的原生工程、需要的派生输出与核验记录。安装成功、命令目录存在与创作任务完成分别报告。

## 首次使用与公共入口

定位当前 SKILL.md 的真实目录。当前支持 macOS arm64、Python 3.11+；固定 CLI 安装到用户数据目录。已有任务授权覆盖必要依赖时直接执行本技能安装器，不另造批准流程。

将 `SKILL_DIR` 设置为宿主实际加载的本 `SKILL.md` 所在目录（绝对路径）。用户级安装可能位于 `~/.agents/skills/photocraft-cli-adjustments`，项目级可能位于 `.agents/skills/photocraft-cli-adjustments`，插件可能位于其 `skills/photocraft-cli-adjustments` 或宿主缓存目录；以实际加载路径为准，不按当前工作目录猜测，也不搜索后随意选择重复版本。技能目录与 CLI 的用户数据安装目录是两个独立位置。

```bash
: "${SKILL_DIR:?请先设置为本 SKILL.md 的实际所在目录}"
python3 -I -B "$SKILL_DIR/scripts/bootstrap.py"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- --version
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- commands --json
```

CLI argv 在 `--` 后，原生子命令必须放首位。安装参数放分隔符前；`--runtime-home` 可隔离缓存。锁定制品摘要失败、损坏安装或不支持平台时停止；不改 PATH、不执行浮动升级。原生帮助入口是 `help`；launcher 自身 `--help` 只说明启动参数。

## 场景操作

核对本场景输入、原生工程、目标对象、版本和输出边界。按 [场景指南](references/scenario.md) 选择当前命令，保存独立检查点后执行；完成后重开原生工程并检查实际输出与非目标内容。

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

优先调整图层保持原图；模式、深度和颜色管理约束以实际结果为准。

原生组合与源工程修订使用本技能自带 `scripts/workflow.py`；读取 [工作流合同](references/workflow.md)，模板在本技能 examples 内。只修改授权对象，原生工程和依赖素材保留，派生格式损失读取 [交换报告](references/exchange-loss.md)。

## 核验与恢复

命令非零退出不算完成；需要查看真实保存工程、导出、尺寸及媒体解码。超时结果标 unknown，先检查原任务/工程，不能自动重放编辑。现有原生工作流支持另存修订；对应项目摘要不符时拒绝覆盖。

## 按需参考与交接

- [实际命令证据](references/commands.json)：固定版本观察，仅作为路由与参数参考；实时结果优先，禁用项不执行。
- [工作流合同](references/workflow.md)：组合操作、原生保存、依赖收集与修订。
- 安装/诊断需要时交给 **photocraft-cli-setup**，完整任务路由交给 **photocraft-use**；缺少技能时使用 `npx skills add full-aigc-skills/photocraft-skills --skill <skill-name>`。不通过相邻文件路径加载其他技能。

本技能不提供虚构的登录接口；本地 headless 不要求云账户。PhotoCraft bridge 的 control-token 是本地应用访问控制，与云登录不同。完整 GUI、跨编辑器保真与创作质量按实际证据陈述。

源工程局部修改可声明 `protectedRegions`，发布交付前检查非目标区域像素；参见本技能[保护区域合同](references/pixel-protection.md)。没有声明区域时不自动推断保护范围。

## 完整原生命令使用

当前技能自带完整目录的参数说明与同会话入口，不受创作模板白名单限制。读取 [完整使用指南](references/command-usage.md)，按需查询 [命令参考](references/command-reference.md)；每条指令有技能路由、前置观察及验收状态。

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" list --filter QUERY
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe COMMAND_ID
python3 -I -B "$SKILL_DIR/scripts/commands.py" run "$SKILL_DIR/examples/commands-advanced.json" --output /absolute/new-command-result
```

新入口执行前检查真实注册表与当前可执行状态，保留返回值引用和逐步回执；语义错误或超时不冒充成功。目录覆盖与直接原生使用不等于所有指令、GUI、交付或 Art 编排已验收。

完整工作流命令网关见 [使用说明](references/native-workflow.md)。领域分发固定版本为 0.1.0-dev.21；该版本的独立安装复验与全量逐命令验收分别记录，不以发布替代验收。

可编辑局部调整与源返工见 [蒙版调整使用说明](references/adjustment-mask.md)；成对计划在本技能 examples 中，源候选与固定安装证据分开。

GUI任务可先使用本技能自带的 [固定桌面安装](references/desktop-install.md)；安装、启动与实际GUI编辑分别核验。

完整归属命令按命令族列于 [分类使用清单](references/scenario.md)，每项可通过本技能的 `commands.py describe` 查看参数；通用 CLI 清单也保留未归入专项技能的全部命令。

业务任务从 [场景操作手册](references/business-scenes.md) 开始，按输入检查、模板适配、原生交付、局部返工和结果核验执行。

安装失败时读取 [首次使用诊断](references/first-use-failures.md)，按回执定位当前技能自身的 setup 入口；安装失败与原生调用失败分别处理。
