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
