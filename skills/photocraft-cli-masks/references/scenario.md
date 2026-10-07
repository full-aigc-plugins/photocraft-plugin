# 蒙版与剪贴操作指南

## 目标与前置

建立图层蒙版、矢量蒙版与剪贴合成。核对蒙版反相、坐标和非目标像素；将抠图结果与原图独立保留。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `layer.createClippingMask` | Create Clipping Mask |
| `layer.releaseClippingMask` | Release Clipping Mask |
| `layer.layerMask.revealAll` | Reveal All |
| `layer.layerMask.hideAll` | Hide All |
| `layer.layerMask.revealSelection` | Reveal Selection |
| `layer.layerMask.delete` | Delete |
| `layer.vectorMask.add` | Add Vector Mask |
| `layer.vectorMask.fromPath` | Vector Mask from Current Path |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 20 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `layer` — 20

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `layer.createClippingMask` | Create Clipping Mask | `describe layer.createClippingMask` |
| `layer.releaseClippingMask` | Release Clipping Mask | `describe layer.releaseClippingMask` |
| `layer.layerMask.revealAll` | Reveal All | `describe layer.layerMask.revealAll` |
| `layer.layerMask.hideAll` | Hide All | `describe layer.layerMask.hideAll` |
| `layer.layerMask.delete` | Delete | `describe layer.layerMask.delete` |
| `layer.vectorMask.add` | Add Vector Mask | `describe layer.vectorMask.add` |
| `layer.vectorMask.fromPath` | Vector Mask from Current Path | `describe layer.vectorMask.fromPath` |
| `layer.vectorMask.edit` | Edit Vector Mask | `describe layer.vectorMask.edit` |
| `layer.vectorMask.delete` | Delete Vector Mask | `describe layer.vectorMask.delete` |
| `layer.vectorMask.revealAll` | Vector Mask: Reveal All | `describe layer.vectorMask.revealAll` |
| `layer.vectorMask.hideAll` | Vector Mask: Hide All | `describe layer.vectorMask.hideAll` |
| `layer.vectorMask.currentPath` | Vector Mask: Current Path | `describe layer.vectorMask.currentPath` |
| `layer.vectorMask.enabled` | Enable Vector Mask | `describe layer.vectorMask.enabled` |
| `layer.vectorMask.linked` | Link Vector Mask | `describe layer.vectorMask.linked` |
| `layer.vectorMask.info` | Vector Mask Info | `describe layer.vectorMask.info` |
| `layer.layerMask.enabled` | Disable Layer Mask | `describe layer.layerMask.enabled` |
| `layer.layerMask.linked` | Unlink Layer Mask | `describe layer.layerMask.linked` |
| `layer.layerMask.apply` | Apply | `describe layer.layerMask.apply` |
| `layer.layerMask.fromTransparency` | From Transparency | `describe layer.layerMask.fromTransparency` |
| `layer.layerMask.hideSelection` | Hide Selection | `describe layer.layerMask.hideSelection` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
