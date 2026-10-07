# 选区与局部区域操作指南

## 目标与前置

创建选区、反选、羽化和局部选择。选择来源与边界必须核验；subject/sky 等目录条目不自动等于已验收 AI 分割。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `select.all` | All |
| `select.deselect` | Deselect |
| `select.inverse` | Inverse |
| `select.rect` | Rectangular Selection |
| `select.toWorkPath` | Make Work Path |
| `select.convertToShape` | Convert Selection to Shape |
| `select.quick` | Quick Selection |
| `select.object` | Object Selection |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 49 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `channel` — 21

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `channel.new` | New Channel… | `describe channel.new` |
| `channel.newSpot` | New Spot Channel… | `describe channel.newSpot` |
| `channel.duplicate` | Duplicate Channel… | `describe channel.duplicate` |
| `channel.delete` | Delete Channel | `describe channel.delete` |
| `channel.rename` | Rename Channel | `describe channel.rename` |
| `channel.move` | Reorder Channel | `describe channel.move` |
| `channel.target` | Target Channel | `describe channel.target` |
| `channel.setVisible` | Channel Visibility | `describe channel.setVisible` |
| `channel.options` | Channel Options… | `describe channel.options` |
| `channel.mergeSpot` | Merge Spot Channel | `describe channel.mergeSpot` |
| `channel.split` | Split Channels | `describe channel.split` |
| `channel.merge` | Merge Channels… | `describe channel.merge` |
| `channel.list` | Channels | `describe channel.list` |
| `channel.target.composite` | Target Composite Channel | `describe channel.target.composite` |
| `channel.target.slot3` | Target Channel 3 | `describe channel.target.slot3` |
| `channel.target.slot4` | Target Channel 4 | `describe channel.target.slot4` |
| `channel.target.slot5` | Target Channel 5 | `describe channel.target.slot5` |
| `channel.target.slot6` | Target Channel 6 | `describe channel.target.slot6` |
| `channel.target.slot7` | Target Channel 7 | `describe channel.target.slot7` |
| `channel.target.slot8` | Target Channel 8 | `describe channel.target.slot8` |
| `channel.target.slot9` | Target Channel 9 | `describe channel.target.slot9` |

### `select` — 28

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `select.all` | All | `describe select.all` |
| `select.inverse` | Inverse | `describe select.inverse` |
| `select.toWorkPath` | Make Work Path | `describe select.toWorkPath` |
| `select.convertToShape` | Convert Selection to Shape | `describe select.convertToShape` |
| `select.quick` | Quick Selection | `describe select.quick` |
| `select.object` | Object Selection | `describe select.object` |
| `select.subject` | Subject | `describe select.subject` |
| `select.refineEdge` | Refine Edge | `describe select.refineEdge` |
| `select.focusArea` | Focus Area… | `describe select.focusArea` |
| `select.magicWand` | Magic Wand | `describe select.magicWand` |
| `select.colorRange` | Color Range… | `describe select.colorRange` |
| `select.modify.border` | Border… | `describe select.modify.border` |
| `select.modify.smooth` | Smooth… | `describe select.modify.smooth` |
| `select.modify.expand` | Expand… | `describe select.modify.expand` |
| `select.modify.contract` | Contract… | `describe select.modify.contract` |
| `select.modify.feather` | Feather… | `describe select.modify.feather` |
| `select.grow` | Grow | `describe select.grow` |
| `select.similar` | Similar | `describe select.similar` |
| `select.lasso` | Lasso | `describe select.lasso` |
| `select.sky` | Sky | `describe select.sky` |
| `select.isolateLayers` | Isolate Layers | `describe select.isolateLayers` |
| `select.transformSelection` | Transform Selection | `describe select.transformSelection` |
| `select.reselect` | Reselect | `describe select.reselect` |
| `select.allLayers` | All Layers | `describe select.allLayers` |
| `select.findLayers` | Find Layers | `describe select.findLayers` |
| `select.saveSelection` | Save Selection… | `describe select.saveSelection` |
| `select.loadSelection` | Load Selection… | `describe select.loadSelection` |
| `select.editInQuickMaskMode` | Edit in Quick Mask Mode | `describe select.editInQuickMaskMode` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
