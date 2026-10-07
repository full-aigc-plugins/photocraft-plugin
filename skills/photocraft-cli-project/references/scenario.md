# 图像工程与色彩模式操作指南

## 目标与前置

创建、打开和保存 pcraft，检查尺寸、深度和色彩模式。原生工程是分层事实源；另存后 info 重开，平面转换不代替工程。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `file.new` | New… |
| `file.close` | Close |
| `document.inspect` | Inspect Document |
| `document.activate` | Activate Document |
| `document.pixel` | Read Composite Pixel |
| `file.scripts.deleteAllEmptyLayers` | Delete All Empty Layers |
| `file.closeAll` | Close All |
| `file.closeOthers` | Close Others |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 52 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `document` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `document.inspect` | Inspect Document | `describe document.inspect` |
| `document.activate` | Activate Document | `describe document.activate` |
| `document.pixel` | Read Composite Pixel | `describe document.pixel` |

### `file` — 36

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `file.new` | New… | `describe file.new` |
| `file.close` | Close | `describe file.close` |
| `file.scripts.deleteAllEmptyLayers` | Delete All Empty Layers | `describe file.scripts.deleteAllEmptyLayers` |
| `file.closeAll` | Close All | `describe file.closeAll` |
| `file.closeOthers` | Close Others | `describe file.closeOthers` |
| `file.revert` | Revert | `describe file.revert` |
| `file.saveACopy` | Save a Copy… | `describe file.saveACopy` |
| `file.openAs` | Open As… | `describe file.openAs` |
| `file.placeEmbedded` | Place Embedded… | `describe file.placeEmbedded` |
| `file.placeLinked` | Place Linked… | `describe file.placeLinked` |
| `file.fileInfo` | File Info… | `describe file.fileInfo` |
| `file.automate.fitImage` | Fit Image… | `describe file.automate.fitImage` |
| `file.automate.conditionalModeChange` | Conditional Mode Change… | `describe file.automate.conditionalModeChange` |
| `file.automate.batch` | Batch… | `describe file.automate.batch` |
| `file.scripts.imageProcessor` | Image Processor… | `describe file.scripts.imageProcessor` |
| `file.scripts.loadFilesIntoStack` | Load Files into Stack… | `describe file.scripts.loadFilesIntoStack` |
| `file.scripts.flattenAllLayerEffects` | Flatten All Layer Effects | `describe file.scripts.flattenAllLayerEffects` |
| `file.scripts.flattenAllMasks` | Flatten All Masks | `describe file.scripts.flattenAllMasks` |
| `file.automate.photomerge` | Photomerge… | `describe file.automate.photomerge` |
| `file.automate.mergeToHdrPro` | Merge to HDR Pro… | `describe file.automate.mergeToHdrPro` |
| `file.automate.cropAndStraightenPhotos` | Crop and Straighten Photos | `describe file.automate.cropAndStraightenPhotos` |
| `file.automate.lensCorrection` | Lens Correction… | `describe file.automate.lensCorrection` |
| `file.import.notes` | Notes… | `describe file.import.notes` |
| `file.generate.imageAssets` | Image Assets | `describe file.generate.imageAssets` |
| `file.automate.contactSheetII` | Contact Sheet II… | `describe file.automate.contactSheetII` |
| `file.automate.createDroplet` | Create Droplet… | `describe file.automate.createDroplet` |
| `file.automate.runDroplet` | Run Droplet | `describe file.automate.runDroplet` |
| `file.scripts.statistics` | Statistics… | `describe file.scripts.statistics` |
| `file.scripts.browse` | Browse… | `describe file.scripts.browse` |
| `file.scripts.scriptEventsManager` | Script Events Manager… | `describe file.scripts.scriptEventsManager` |
| `file.print` | Print… | `describe file.print` |
| `file.printOneCopy` | Print One Copy | `describe file.printOneCopy` |
| `file.package` | Package… | `describe file.package` |
| `file.import.videoFramesToLayers` | Video Frames to Layers… | `describe file.import.videoFramesToLayers` |
| `file.import.wiaSupport` | WIA Support… | `describe file.import.wiaSupport` |
| `file.import.variableDataSets` | Variable Data Sets… | `describe file.import.variableDataSets` |

### `image` — 13

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `image.mode.rgb` | RGB Color | `describe image.mode.rgb` |
| `image.mode.grayscale` | Grayscale | `describe image.mode.grayscale` |
| `image.mode.cmyk` | CMYK Color | `describe image.mode.cmyk` |
| `image.mode.lab` | Lab Color | `describe image.mode.lab` |
| `image.mode.bits8` | 8 Bits/Channel | `describe image.mode.bits8` |
| `image.mode.bits16` | 16 Bits/Channel | `describe image.mode.bits16` |
| `image.mode.bits32` | 32 Bits/Channel | `describe image.mode.bits32` |
| `image.duplicate` | Duplicate… | `describe image.duplicate` |
| `image.mode.indexedColor` | Indexed Color… | `describe image.mode.indexedColor` |
| `image.mode.colorTable` | Color Table… | `describe image.mode.colorTable` |
| `image.mode.bitmap` | Bitmap… | `describe image.mode.bitmap` |
| `image.mode.duotone` | Duotone… | `describe image.mode.duotone` |
| `image.mode.multichannel` | Multichannel | `describe image.mode.multichannel` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
