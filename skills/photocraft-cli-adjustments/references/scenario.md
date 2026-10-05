# 非破坏调整操作指南

## 目标与前置

使用调整图层或指定局部颜色调整。优先调整图层保持原图；模式、深度和颜色管理约束以实际结果为准。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `layer.setAdjustment` | Adjustment Properties |
| `image.adjustments.desaturate` | Desaturate |
| `layer.newAdjustmentLayer.brightnessContrast` | Brightness/Contrast… |
| `image.adjustments.brightnessContrast` | Brightness/Contrast… |
| `layer.newAdjustmentLayer.levels` | Levels… |
| `image.adjustments.levels` | Levels… |
| `layer.newAdjustmentLayer.curves` | Curves… |
| `image.adjustments.curves` | Curves… |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

## 已验证的局部调整操作链（CLI 0.2.0）

创建调整图层本身不会把当前选区转换为蒙版；只创建亮度图层会影响其下方的全部像素。局部调整必须依次选择目标图层、创建选区、创建调整图层、在该新图层上执行 `layer.layerMask.revealSelection`、取消选区并保存。保持同一 `run` 会话，新建调整图层就是蒙版目标；分批操作时从真实回执取得新图层 ID 并显式指定。

```bash
: "${SKILL_DIR:?本技能实际加载目录}" "${SOURCE_PROJECT:?原生工程绝对路径}" "${OUTPUT_PROJECT:?新工程绝对路径}" "${LAYER_ID:?从 info 取得的整数图层 ID}"
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- run "$SOURCE_PROJECT" \
  --cmd layer.select --params "{\"layer\":$LAYER_ID}" \
  --cmd select.rect --params '{"x":110,"y":150,"width":20,"height":20}' \
  --cmd layer.newAdjustmentLayer.brightnessContrast --params '{"brightness":40,"contrast":0}' \
  --cmd layer.layerMask.revealSelection --params '{}' \
  --cmd select.deselect --params '{}' --out "$OUTPUT_PROJECT"
```

矩形是已测样本，按真实工程坐标替换。重开后应仍为 `Adjustment` 图层、`hasMask=true`；原像素图层保持可编辑，区域内像素变化、区域外像素不变。保持调整层与蒙版，不用破坏性扁平化替代局部调整。
