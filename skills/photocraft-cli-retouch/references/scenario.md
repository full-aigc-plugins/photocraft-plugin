# 修图与绘画操作指南

## 目标与前置

对已授权图像做修复、克隆、画笔和局部修饰。笔触坐标与采样来源需显式指定；局部修图保持未修改区域，算法输出需视觉检查。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `paint.stroke` | Brush Stroke |
| `paint.pencil` | Pencil |
| `paint.mixerBrush` | Mixer Brush |
| `paint.colorReplacement` | Color Replacement |
| `brush.presets.list` | List Brush Presets |
| `brush.presets.save` | Save Brush Preset |
| `brush.presets.delete` | Delete Brush Preset |
| `brush.defineFromSelection` | Define Brush Preset… |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

## 已验证的笔触、克隆与修复（CLI 0.2.0）

先通过 `info` 取得真实目标像素图层 ID，再在同一 `run` 内执行 `layer.select` 和笔触。`paint.stroke` 的 `hardness`、`opacity`、`flow` 使用 0..1；`paint.cloneStamp` 与 `paint.healingBrush` 的 `hardness` 使用 0..100，`opacity`、`flow` 使用 1..100。不要把两个工具的数值范围混用。

```bash
: "${SKILL_DIR:?本技能实际加载目录}" "${SOURCE_PROJECT:?原生工程绝对路径}" "${OUTPUT_PROJECT:?新工程绝对路径}" "${LAYER_ID:?从 info 取得的整数图层 ID}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- run "$SOURCE_PROJECT" \
  --cmd layer.select --params "{\"layer\":$LAYER_ID}" \
  --cmd paint.cloneStamp --params '{"points":[[130,180],[135,180]],"source":[140,200],"size":16,"hardness":100,"opacity":100,"flow":100}' \
  --out "$OUTPUT_PROJECT"
```

`source` 是第一个笔触点对应的源采样位置，坐标按真实图像替换；克隆与修复均应返回非空 `damage`。已测样本包含蓝色笔触、从邻近原色区克隆和修复，修改区回到源色，保护区域和文字图层保持不变。这是有界技术样本，不证明任意复杂纹理的修复质量。

## 公开工作流修图

需要保护指定区域并另存完整交付时，使用本技能 `scripts/workflow.py`。计划中先 `layer.select`，再执行 `paint.stroke`、`paint.cloneStamp` 或 `paint.healingBrush`；原生参数和坐标沿用上例。添加 expectedProjectSha256、protectedRegions、exports，并传入源交付目录。工作流保存并重开 `.pcraft`，保留素材和操作记录；保护区变化时不发布目标目录。直接原生 `run` 不包含此保护门禁。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 37 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `brush` — 12

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `brush.presets.list` | List Brush Presets | `describe brush.presets.list` |
| `brush.presets.save` | Save Brush Preset | `describe brush.presets.save` |
| `brush.presets.delete` | Delete Brush Preset | `describe brush.presets.delete` |
| `brush.defineFromSelection` | Define Brush Preset… | `describe brush.defineFromSelection` |
| `brush.get` | Get Brush | `describe brush.get` |
| `brush.presets.importAbr` | Import Brushes… | `describe brush.presets.importAbr` |
| `brush.texturePattern` | Brush Texture Pattern | `describe brush.texturePattern` |
| `brush.presets.rename` | Rename Brush | `describe brush.presets.rename` |
| `brush.presets.move` | Move Brush | `describe brush.presets.move` |
| `brush.presets.moveGroup` | Move Brush Group | `describe brush.presets.moveGroup` |
| `brush.presets.renameGroup` | Rename Brush Group | `describe brush.presets.renameGroup` |
| `brush.presets.deleteGroup` | Delete Brush Group | `describe brush.presets.deleteGroup` |

### `cloneSource` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `cloneSource.list` | Clone Sources | `describe cloneSource.list` |
| `cloneSource.select` | Select Clone Source | `describe cloneSource.select` |
| `cloneSource.set` | Set Clone Source | `describe cloneSource.set` |
| `cloneSource.resetTransform` | Reset Transform | `describe cloneSource.resetTransform` |
| `cloneSource.overlay` | Clone Source Overlay | `describe cloneSource.overlay` |

### `layer` — 2

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `layer.select` | Select Layer | `describe layer.select` |
| `layer.selectLinkedLayers` | Select Linked Layers | `describe layer.selectLinkedLayers` |

### `paint` — 18

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `paint.stroke` | Brush Stroke | `describe paint.stroke` |
| `paint.pencil` | Pencil | `describe paint.pencil` |
| `paint.mixerBrush` | Mixer Brush | `describe paint.mixerBrush` |
| `paint.colorReplacement` | Color Replacement | `describe paint.colorReplacement` |
| `paint.magicEraser` | Magic Eraser | `describe paint.magicEraser` |
| `paint.backgroundEraser` | Background Eraser | `describe paint.backgroundEraser` |
| `paint.cloneStamp` | Clone Stamp | `describe paint.cloneStamp` |
| `paint.healingBrush` | Healing Brush | `describe paint.healingBrush` |
| `paint.spotHealing` | Spot Healing Brush | `describe paint.spotHealing` |
| `paint.dodge` | Dodge | `describe paint.dodge` |
| `paint.burn` | Burn | `describe paint.burn` |
| `paint.sponge` | Sponge | `describe paint.sponge` |
| `paint.blur` | Blur | `describe paint.blur` |
| `paint.sharpen` | Sharpen | `describe paint.sharpen` |
| `paint.smudge` | Smudge | `describe paint.smudge` |
| `paint.historyBrush` | History Brush | `describe paint.historyBrush` |
| `paint.bucket` | Paint Bucket | `describe paint.bucket` |
| `paint.gradient` | Gradient | `describe paint.gradient` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
