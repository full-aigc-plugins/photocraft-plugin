# 尺寸适配操作指南

## 目标与前置

调整画布和图像尺寸，制作海报封面变体。区分画布裁切与图像重采样；每种尺寸另存变体，文字和产品继续可编辑。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `image.imageRotation.flipCanvasHorizontal` | Flip Canvas Horizontal |
| `image.imageRotation.flipCanvasVertical` | Flip Canvas Vertical |
| `image.imageRotation.180` | 180° |
| `image.imageRotation.90cw` | 90° Clockwise |
| `image.imageRotation.90ccw` | 90° Counter Clockwise |
| `image.imageSize` | Image Size… |
| `image.canvasSize` | Canvas Size… |
| `image.crop` | Crop |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。
