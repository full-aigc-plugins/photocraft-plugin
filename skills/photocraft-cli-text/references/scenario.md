# 海报文字排版操作指南

## 目标与前置

创建和修改文字图层、字体、段落和布局。文字保持独立图层；核对字体、换行、溢出与字形，缺失字体报告替代。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `type.create` | New Type Layer |
| `type.edit` | Edit Type |
| `type.setStyle` | Set Type Style |
| `type.rasterize` | Rasterize Type |
| `type.info` | Type Layer Info |
| `type.fonts` | List Fonts |
| `type.antiAlias.none` | None |
| `type.antiAlias.sharp` | Sharp |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 56 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `type` — 56

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `type.create` | New Type Layer | `describe type.create` |
| `type.edit` | Edit Type | `describe type.edit` |
| `type.setStyle` | Set Type Style | `describe type.setStyle` |
| `type.rasterize` | Rasterize Type | `describe type.rasterize` |
| `type.info` | Type Layer Info | `describe type.info` |
| `type.fonts` | List Fonts | `describe type.fonts` |
| `type.antiAlias.none` | None | `describe type.antiAlias.none` |
| `type.antiAlias.sharp` | Sharp | `describe type.antiAlias.sharp` |
| `type.antiAlias.crisp` | Crisp | `describe type.antiAlias.crisp` |
| `type.antiAlias.strong` | Strong | `describe type.antiAlias.strong` |
| `type.antiAlias.smooth` | Smooth | `describe type.antiAlias.smooth` |
| `type.antiAlias.windowsLcd` | Windows LCD | `describe type.antiAlias.windowsLcd` |
| `type.antiAlias.windows` | Windows | `describe type.antiAlias.windows` |
| `type.orientation.horizontal` | Horizontal | `describe type.orientation.horizontal` |
| `type.orientation.vertical` | Vertical | `describe type.orientation.vertical` |
| `type.openType.standardLigatures` | Standard Ligatures | `describe type.openType.standardLigatures` |
| `type.openType.contextualAlternates` | Contextual Alternates | `describe type.openType.contextualAlternates` |
| `type.openType.discretionaryLigatures` | Discretionary Ligatures | `describe type.openType.discretionaryLigatures` |
| `type.openType.swash` | Swash | `describe type.openType.swash` |
| `type.openType.oldstyle` | Oldstyle | `describe type.openType.oldstyle` |
| `type.openType.stylisticAlternates` | Stylistic Alternates | `describe type.openType.stylisticAlternates` |
| `type.openType.titlingAlternates` | Titling Alternates | `describe type.openType.titlingAlternates` |
| `type.openType.ornaments` | Ornaments | `describe type.openType.ornaments` |
| `type.openType.ordinals` | Ordinals | `describe type.openType.ordinals` |
| `type.openType.fractions` | Fractions | `describe type.openType.fractions` |
| `type.createWorkPath` | Create Work Path | `describe type.createWorkPath` |
| `type.convertToShape` | Convert to Shape | `describe type.convertToShape` |
| `type.rasterizeTypeLayer` | Rasterize Type Layer | `describe type.rasterizeTypeLayer` |
| `type.convertToParagraphText` | Convert to Paragraph Text | `describe type.convertToParagraphText` |
| `type.convertToPointText` | Convert to Point Text | `describe type.convertToPointText` |
| `type.warpText` | Warp Text… | `describe type.warpText` |
| `type.updateAllTextLayers` | Update All Text Layers | `describe type.updateAllTextLayers` |
| `type.replaceAllMissingFonts` | Replace All Missing Fonts | `describe type.replaceAllMissingFonts` |
| `type.resolveMissingFonts` | Resolve Missing Fonts… | `describe type.resolveMissingFonts` |
| `type.pasteLoremIpsum` | Paste Lorem Ipsum | `describe type.pasteLoremIpsum` |
| `type.saveDefaultTypeStyles` | Save Default Type Styles | `describe type.saveDefaultTypeStyles` |
| `type.loadDefaultTypeStyles` | Load Default Type Styles | `describe type.loadDefaultTypeStyles` |
| `type.characterStyle.new` | New Character Style | `describe type.characterStyle.new` |
| `type.characterStyle.duplicate` | Duplicate Style | `describe type.characterStyle.duplicate` |
| `type.characterStyle.delete` | Delete Style | `describe type.characterStyle.delete` |
| `type.characterStyle.rename` | Rename Style | `describe type.characterStyle.rename` |
| `type.characterStyle.set` | Character Style Options | `describe type.characterStyle.set` |
| `type.characterStyle.apply` | Apply Character Style | `describe type.characterStyle.apply` |
| `type.characterStyle.redefine` | Redefine Character Style | `describe type.characterStyle.redefine` |
| `type.characterStyle.clearOverride` | Clear Override | `describe type.characterStyle.clearOverride` |
| `type.characterStyle.list` | List Character Styles | `describe type.characterStyle.list` |
| `type.paragraphStyle.new` | New Paragraph Style | `describe type.paragraphStyle.new` |
| `type.paragraphStyle.duplicate` | Duplicate Style | `describe type.paragraphStyle.duplicate` |
| `type.paragraphStyle.delete` | Delete Style | `describe type.paragraphStyle.delete` |
| `type.paragraphStyle.rename` | Rename Style | `describe type.paragraphStyle.rename` |
| `type.paragraphStyle.set` | Paragraph Style Options | `describe type.paragraphStyle.set` |
| `type.paragraphStyle.apply` | Apply Paragraph Style | `describe type.paragraphStyle.apply` |
| `type.paragraphStyle.redefine` | Redefine Paragraph Style | `describe type.paragraphStyle.redefine` |
| `type.paragraphStyle.clearOverride` | Clear Override | `describe type.paragraphStyle.clearOverride` |
| `type.paragraphStyle.list` | List Paragraph Styles | `describe type.paragraphStyle.list` |
| `type.insertText` | Insert Glyph | `describe type.insertText` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
