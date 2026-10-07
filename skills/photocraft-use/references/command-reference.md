# 完整原生命令参考 / Complete native command reference

本参考逐项保留锁定参数原文与技能路由。命令执行必须满足当前工程、选择对象、素材或 GUI 前置状态。
This reference preserves each pinned parameter contract and skill owner. Query live state before invocation.

使用方法见 [完整调用指南](command-usage.md)。全部参数均为原生语法说明，不把它们假装成 JSON Schema。
每项 NOT_RUN 指本轮完整逐命令验收；既有代表任务证据仍单独保留。

## file.new

New…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":u32=1920,"height":u32=1080,"mode":"rgb|gray|cmyk|lab"="rgb","depth":8|16|32=8,"background":"white|black|backgroundColor|transparent|#rrggbb"="white","resolution":ppi=72,"name":str}
```

## file.close

Close

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.close`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"document":index?}
```

## edit.undo

Undo

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.undo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.redo

Redo

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.redo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.fill

Fill…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.fill`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"contents":"color|pattern"="color","color":"#rrggbb|[r,g,b,a]"=foreground,"pattern":id|name (contents=pattern),"scale":%=100,"angle":deg,"opacity":%=100,"target":"pixels"|{"channel":i}|"quickMask"?}
```

## edit.clear

Clear

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.all

All

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.all`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.deselect

Deselect

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.deselect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

场景 / Recipes: [examples/adjustment-mask-create.json](../examples/adjustment-mask-create.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## select.inverse

Inverse

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.inverse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.rect

Rectangular Selection

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.rect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":i32,"y":i32,"width":u32,"height":u32,"mode":"replace|add|subtract|intersect"="replace","ellipse":bool=false,"antiAlias":bool=true,"feather":px=0}
```

场景 / Recipes: [examples/adjustment-mask-create.json](../examples/adjustment-mask-create.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## layer.new.layer

Layer…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.layer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?}
```

## layer.new.group

Group…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.group`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?}
```

## layer.groupLayers

Group Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.groupLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"name":str?} (no layer: every selected layer)
```

## layer.duplicate

Duplicate Layer…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} (no layer: every selected layer)
```

## layer.delete

Delete Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} (no layer: every selected layer)
```

## layer.select

Select Layer

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id,"mode":"replace|toggle|range|add"="replace"} (toggle = ⌘-click, range = ⇧-click)
```

场景 / Recipes: [examples/adjustment-mask-revise.json](../examples/adjustment-mask-revise.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## layer.setProps

Layer Properties

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.setProps`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"name":str?,"visible":bool?,"opacity":0..1?,"fill":0..1?,"blend":"Multiply|…"?,"clipped":bool?,"locked":bool?,"locks":{"transparency","pixels","position","artboard","all":bool}?,"channels":[bool,…]? (Advanced Blending: which colour channels blend, R G B / C M Y K / L a b)}
```

## layer.arrange.bringForward

Bring Forward

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.arrange.bringForward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.arrange.sendBackward

Send Backward

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.arrange.sendBackward`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.arrange.bringToFront

Bring to Front

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.arrange.bringToFront`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.arrange.sendToBack

Send to Back

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.arrange.sendToBack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.createClippingMask

Create Clipping Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.createClippingMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.releaseClippingMask

Release Clipping Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.releaseClippingMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerMask.revealAll

Reveal All

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.revealAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerMask.hideAll

Hide All

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.hideAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerMask.revealSelection

Reveal Selection

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.revealSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

场景 / Recipes: [examples/adjustment-mask-create.json](../examples/adjustment-mask-create.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## layer.layerMask.delete

Delete

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.mergeDown

Merge Down

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.mergeDown`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.flattenImage

Flatten Image

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.flattenImage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.newFillLayer.solidColor

Solid Color…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newFillLayer.solidColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb"=foreground}
```

## layer.newFillLayer.gradient

Gradient…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newFillLayer.gradient`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":"#rrggbb","to":"#rrggbb","angle":deg=90,"style":"linear|radial|angle|reflected|diamond","reverse":bool}
```

## layer.setAdjustment

Adjustment Properties

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.setAdjustment`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?, …params of that adjustment kind}
```

场景 / Recipes: [examples/adjustment-mask-revise.json](../examples/adjustment-mask-revise.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## layer.moveTo

Reorder Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.moveTo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"target":id,"position":"above|below|into"="above"}
```

## layer.translate

Move Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.translate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"dx":i32,"dy":i32} (no layer: every selected layer; linked layers follow)
```

## image.imageRotation.flipCanvasHorizontal

Flip Canvas Horizontal

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.imageRotation.flipCanvasHorizontal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.imageRotation.flipCanvasVertical

Flip Canvas Vertical

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.imageRotation.flipCanvasVertical`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.imageRotation.180

180°

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.imageRotation.180`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.imageRotation.90cw

90° Clockwise

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.imageRotation.90cw`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.imageRotation.90ccw

90° Counter Clockwise

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.imageRotation.90ccw`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.adjustments.desaturate

Desaturate

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.desaturate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## paint.stroke

Brush Stroke

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.stroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?,tiltX?,tiltY?,rotation?,timeMs?,wheel?],…],"brush":{…BrushSettings}?,"preset":name?,"size":px?,"hardness":0..1?,"opacity":0..1?,"flow":0..1?,"spacing":0..10?,"color":"#rrggbb"?=foreground,"mode":"normal|multiply|screen|…"="normal","erase":bool?,"smoothing":0..1?,"zoom":number=1,"seed":u64?,"target":"pixels"|"mask"|"quickMask"|{"channel":i}=Channels panel target}
```

## tools.setColors

Set Colors

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tools.setColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"foreground":"#rrggbb"?,"background":"#rrggbb"?}
```

## tools.swapColors

Switch Foreground and Background Colors

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tools.swapColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## tools.defaultColors

Default Foreground and Background Colors

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tools.defaultColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## session.inspect

Inspect Session

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe session.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## document.inspect

Inspect Document

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.inspect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"document":index?}
```

## document.activate

Activate Document

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.activate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"document":index}
```

## command.list

List Commands

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe command.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## document.pixel

Read Composite Pixel

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe document.pixel`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":i32,"y":i32}
```

## layer.newAdjustmentLayer.brightnessContrast

Brightness/Contrast…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.brightnessContrast`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brightness":-150..150=0,"contrast":-50..100=0,"legacy":bool=false}
```

场景 / Recipes: [examples/adjustment-mask-create.json](../examples/adjustment-mask-create.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## image.adjustments.brightnessContrast

Brightness/Contrast…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.brightnessContrast`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brightness":-150..150=0,"contrast":-50..100=0,"legacy":bool=false}
```

## layer.newAdjustmentLayer.levels

Levels…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.levels`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"inBlack":0..253=0,"gamma":0.01..9.99=1,"inWhite":2..255=255,"outBlack":0..255=0,"outWhite":0..255=255,"red":json,"green":json,"blue":json} (top level = composite; per channel {"inBlack","gamma","inWhite","outBlack","outWhite"} under red/green/blue, gray, cyan/magenta/yellow/black or lightness/a/b)
```

## image.adjustments.levels

Levels…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.levels`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"inBlack":0..253=0,"gamma":0.01..9.99=1,"inWhite":2..255=255,"outBlack":0..255=0,"outWhite":0..255=255,"red":json,"green":json,"blue":json} (top level = composite; per channel {"inBlack","gamma","inWhite","outBlack","outWhite"} under red/green/blue, gray, cyan/magenta/yellow/black or lightness/a/b)
```

## layer.newAdjustmentLayer.curves

Curves…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.curves`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":json,"red":json,"green":json,"blue":json} (curves as [[in,out],…] in 0..255, 2..19 points: points = composite; red/green/blue, gray, cyan/magenta/yellow/black or lightness/a/b per channel)
```

## image.adjustments.curves

Curves…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.curves`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":json,"red":json,"green":json,"blue":json} (curves as [[in,out],…] in 0..255, 2..19 points: points = composite; red/green/blue, gray, cyan/magenta/yellow/black or lightness/a/b per channel)
```

## layer.newAdjustmentLayer.exposure

Exposure…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.exposure`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"exposure":-20..20=0,"offset":-0.5..0.5=0,"gamma":0.01..9.99=1}
```

## image.adjustments.exposure

Exposure…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.exposure`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"exposure":-20..20=0,"offset":-0.5..0.5=0,"gamma":0.01..9.99=1}
```

## layer.newAdjustmentLayer.vibrance

Vibrance…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.vibrance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"vibrance":-100..100=0,"saturation":-100..100=0}
```

## image.adjustments.vibrance

Vibrance…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.vibrance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"vibrance":-100..100=0,"saturation":-100..100=0}
```

## layer.newAdjustmentLayer.hueSaturation

Hue/Saturation…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.hueSaturation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"hue":-180..180=0,"saturation":-100..100=0,"lightness":-100..100=0,"colorize":bool=false,"reds":json,"yellows":json,"greens":json,"cyans":json,"blues":json,"magentas":json} (per range {"hue","saturation","lightness","range":[4 hue degrees]}; colorize: hue 0..360, saturation 0..100)
```

## image.adjustments.hueSaturation

Hue/Saturation…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.hueSaturation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"hue":-180..180=0,"saturation":-100..100=0,"lightness":-100..100=0,"colorize":bool=false,"reds":json,"yellows":json,"greens":json,"cyans":json,"blues":json,"magentas":json} (per range {"hue","saturation","lightness","range":[4 hue degrees]}; colorize: hue 0..360, saturation 0..100)
```

## layer.newAdjustmentLayer.colorBalance

Color Balance…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.colorBalance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"shadows":json,"midtones":json,"highlights":json,"preserveLuminosity":bool=true} (each tone [cyan-red, magenta-green, yellow-blue] in -100..100)
```

## image.adjustments.colorBalance

Color Balance…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.colorBalance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"shadows":json,"midtones":json,"highlights":json,"preserveLuminosity":bool=true} (each tone [cyan-red, magenta-green, yellow-blue] in -100..100)
```

## layer.newAdjustmentLayer.blackWhite

Black & White…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.blackWhite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"reds":-200..300=40,"yellows":-200..300=60,"greens":-200..300=40,"cyans":-200..300=60,"blues":-200..300=20,"magentas":-200..300=80,"tint":bool=false,"tintColor":"#rrggbb"}
```

## image.adjustments.blackWhite

Black & White…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.blackWhite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"reds":-200..300=40,"yellows":-200..300=60,"greens":-200..300=40,"cyans":-200..300=60,"blues":-200..300=20,"magentas":-200..300=80,"tint":bool=false,"tintColor":"#rrggbb"}
```

## layer.newAdjustmentLayer.photoFilter

Photo Filter…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.photoFilter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"filter":"warming85|warmingLBA|warming81|cooling80|coolingLBB|cooling82|red|orange|yellow|green|cyan|blue|violet|magenta|sepia|deepRed|deepBlue|deepEmerald|deepYellow|underwater","color":"#rrggbb","density":0..100=25,"preserveLuminosity":bool=true}
```

## image.adjustments.photoFilter

Photo Filter…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.photoFilter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"filter":"warming85|warmingLBA|warming81|cooling80|coolingLBB|cooling82|red|orange|yellow|green|cyan|blue|violet|magenta|sepia|deepRed|deepBlue|deepEmerald|deepYellow|underwater","color":"#rrggbb","density":0..100=25,"preserveLuminosity":bool=true}
```

## layer.newAdjustmentLayer.channelMixer

Channel Mixer…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.channelMixer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"red":json,"green":json,"blue":json,"gray":json,"monochrome":bool=false} (per output channel [red %, green %, blue %, constant %] in -200..200; gray = the monochrome mix)
```

## image.adjustments.channelMixer

Channel Mixer…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.channelMixer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"red":json,"green":json,"blue":json,"gray":json,"monochrome":bool=false} (per output channel [red %, green %, blue %, constant %] in -200..200; gray = the monochrome mix)
```

## layer.newAdjustmentLayer.invert

Invert

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.invert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.adjustments.invert

Invert

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.invert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.newAdjustmentLayer.posterize

Posterize…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.posterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"levels":2..255=4}
```

## image.adjustments.posterize

Posterize…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.posterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"levels":2..255=4}
```

## layer.newAdjustmentLayer.threshold

Threshold…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.threshold`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"level":1..255=128}
```

## image.adjustments.threshold

Threshold…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.threshold`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"level":1..255=128}
```

## layer.newAdjustmentLayer.gradientMap

Gradient Map…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.gradientMap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"stops":json,"reverse":bool=false,"dither":bool=false} (stops [[location 0..1, "#rrggbb"], …], 2..64)
```

## image.adjustments.gradientMap

Gradient Map…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.gradientMap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"stops":json,"reverse":bool=false,"dither":bool=false} (stops [[location 0..1, "#rrggbb"], …], 2..64)
```

## layer.newAdjustmentLayer.selectiveColor

Selective Color…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.selectiveColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"relative|absolute"="relative","colors":"reds|yellows|greens|cyans|blues|magentas|whites|neutrals|blacks"="reds","cyan":-100..100=0,"magenta":-100..100=0,"yellow":-100..100=0,"black":-100..100=0,"reds":json} (per-range [c,m,y,k] arrays: reds yellows greens cyans blues magentas whites neutrals blacks)
```

## image.adjustments.selectiveColor

Selective Color…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.selectiveColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"relative|absolute"="relative","colors":"reds|yellows|greens|cyans|blues|magentas|whites|neutrals|blacks"="reds","cyan":-100..100=0,"magenta":-100..100=0,"yellow":-100..100=0,"black":-100..100=0,"reds":json} (per-range [c,m,y,k] arrays: reds yellows greens cyans blues magentas whites neutrals blacks)
```

## layer.newAdjustmentLayer.colorLookup

Color Lookup…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newAdjustmentLayer.colorLookup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"lut":"none|warm|cool|tealOrange|bleachBypass|fadedFilm|dayForNight|monoContrast|crossProcess"="none","file":text,"interpolation":"trilinear|tetrahedral"="trilinear","dither":bool=false,"data":json} (file: .cube/.3dl/.look path; data: file text + "fileName")
```

## image.adjustments.colorLookup

Color Lookup…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.colorLookup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"lut":"none|warm|cool|tealOrange|bleachBypass|fadedFilm|dayForNight|monoContrast|crossProcess"="none","file":text,"interpolation":"trilinear|tetrahedral"="trilinear","dither":bool=false,"data":json} (file: .cube/.3dl/.look path; data: file text + "fileName")
```

## layer.layerStyle.dropShadow

Drop Shadow…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.dropShadow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","opacity":0..100=75,"blend":str="multiply","angle":deg=120,"useGlobalLight":bool,"distance":px=5,"spread":0..100,"size":px=5,"knocksOut":bool,"add":bool,"layer":id}
```

## layer.layerStyle.innerShadow

Inner Shadow…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.innerShadow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","opacity":0..100=75,"blend":str,"angle":deg,"distance":px,"choke":0..100,"size":px,"add":bool}
```

## layer.layerStyle.outerGlow

Outer Glow…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.outerGlow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","opacity":0..100=75,"blend":str="screen","technique":"softer|precise","spread":0..100,"size":px,"range":0..100,"add":bool}
```

## layer.layerStyle.innerGlow

Inner Glow…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.innerGlow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","opacity":0..100=75,"blend":str="screen","technique":"softer|precise","source":"edge|center","choke":0..100,"size":px,"add":bool}
```

## layer.layerStyle.stroke

Stroke…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.stroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"size":px=3,"position":"outside|inside|center","color":"#rrggbb","from":"#rrggbb","to":"#rrggbb","style":str,"angle":deg,"opacity":0..100,"blend":str,"add":bool}
```

## layer.layerStyle.colorOverlay

Color Overlay…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.colorOverlay`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","opacity":0..100=100,"blend":str,"add":bool}
```

## layer.layerStyle.gradientOverlay

Gradient Overlay…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.gradientOverlay`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":"#rrggbb","to":"#rrggbb","style":"linear|radial|angle|reflected|diamond","angle":deg=90,"scale":10..150=100,"reverse":bool,"opacity":0..100,"blend":str,"add":bool}
```

## layer.layerStyle.patternOverlay

Pattern Overlay…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.patternOverlay`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name?=first library pattern,"opacity":0..100=100,"blend":str,"scale":1..1000=100,"angle":deg=0,"link":bool=true,"phaseX":px,"phaseY":px,"add":bool}
```

## layer.layerStyle.bevelEmboss

Bevel & Emboss…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.bevelEmboss`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"style":"inner|outer|emboss|pillow|stroke","technique":"smooth|chiselHard|chiselSoft","contour":bool,"contourRange":1..100=50,"texture":pattern id|name?,"textureScale":1..1000=100,"textureDepth":-1000..1000=100,"textureInvert":bool,"textureLink":bool=true,"depth":1..1000=100,"direction":"up|down","size":px=5,"soften":px,"angle":deg,"altitude":deg,"add":bool}
```

## layer.layerStyle.satin

Satin…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.satin`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":"#rrggbb","opacity":0..100=50,"blend":str,"angle":deg,"distance":px,"size":px,"invert":bool,"add":bool}
```

## layer.layerStyle.clear

Clear Layer Style

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id}
```

## filter.blur.gaussianBlur

Gaussian Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.gaussianBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0.1..1000=1}
```

## filter.blur.blur

Blur

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.blur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.blur.blurMore

Blur More

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.blurMore`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.sharpen.sharpen

Sharpen

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.sharpen.sharpen`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.sharpen.sharpenMore

Sharpen More

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.sharpen.sharpenMore`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.sharpen.sharpenEdges

Sharpen Edges

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.sharpen.sharpenEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.noise.despeckle

Despeckle

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.noise.despeckle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.blur.boxBlur

Box Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.boxBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..2000=1}
```

## filter.blur.motionBlur

Motion Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.motionBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"angle":-360..360=0,"distance":1..2000=10}
```

## filter.blur.radialBlur

Radial Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.radialBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":1..100=10,"method":"spin|zoom","centerX":0..1=0.5,"centerY":0..1=0.5}
```

## filter.blur.surfaceBlur

Surface Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.surfaceBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..100=5,"threshold":2..255=15}
```

## filter.sharpen.unsharpMask

Unsharp Mask…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.sharpen.unsharpMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":1..500=50,"radius":0.1..1000=1,"threshold":0..255=0}
```

## filter.sharpen.smartSharpen

Smart Sharpen…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.sharpen.smartSharpen`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":1..500=100,"radius":0.1..64=1,"reduceNoise":0..100=10}
```

## filter.noise.addNoise

Add Noise…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.noise.addNoise`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":0.1..400=12.5,"distribution":"uniform|gaussian","monochromatic":bool,"seed":u32=0}
```

## filter.noise.median

Median…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.noise.median`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..500=1}
```

## filter.noise.dustAndScratches

Dust & Scratches…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.noise.dustAndScratches`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..500=1,"threshold":0..255=0}
```

## filter.pixelate.mosaic

Mosaic…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.mosaic`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"cellSize":2..200=10}
```

## filter.stylize.emboss

Emboss…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.emboss`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"angle":-180..180=135,"height":1..100=3,"amount":1..500=100}
```

## filter.stylize.findEdges

Find Edges

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.findEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.stylize.solarize

Solarize

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.solarize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.distort.twirl

Twirl…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.twirl`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"angle":-999..999=50}
```

## filter.distort.pinch

Pinch…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.pinch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":-100..100=50}
```

## filter.distort.spherize

Spherize…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.spherize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":-100..100=100,"mode":"normal|horizontalOnly|verticalOnly"}
```

## filter.distort.wave

Wave…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.wave`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"generators":1..999=5,"wavelengthMin":1..998=10,"wavelengthMax":2..999=120,"amplitudeMin":1..998=5,"amplitudeMax":1..999=35,"type":"sine|triangle|square","undefinedAreas":"wrap|repeat","seed":u32=0}
```

## filter.distort.ripple

Ripple…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.ripple`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":-999..999=100,"size":"small|medium|large"}
```

## filter.distort.polarCoordinates

Polar Coordinates…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.polarCoordinates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"mode":"rectangularToPolar|polarToRectangular"}
```

## filter.other.highPass

High Pass…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.other.highPass`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0.1..1000=10}
```

## filter.other.minimum

Minimum…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.other.minimum`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0.2..500=1,"preserve":"squareness|roundness"}
```

## filter.other.maximum

Maximum…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.other.maximum`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0.2..500=1,"preserve":"squareness|roundness"}
```

## filter.other.offset

Offset…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.other.offset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"horizontal":px=0,"vertical":px=0,"undefinedAreas":"wrap|repeat|transparent"}
```

## filter.lastFilter

Last Filter

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.lastFilter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.pixelate.colorHalftone

Color Halftone…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.colorHalftone`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"maxRadius":4..127=8,"channel1":-360..360=108,"channel2":-360..360=162,"channel3":-360..360=90,"channel4":-360..360=45}
```

## filter.pixelate.crystallize

Crystallize…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.crystallize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"cellSize":3..300=10,"seed":u32=0}
```

## filter.pixelate.facet

Facet

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.facet`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.pixelate.fragment

Fragment

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.fragment`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.pixelate.mezzotint

Mezzotint…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.mezzotint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"type":"fineDots|mediumDots|grainyDots|coarseDots|shortLines|mediumLines|longLines|shortStrokes|mediumStrokes|longStrokes","seed":u32=0}
```

## filter.pixelate.pointillize

Pointillize…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.pixelate.pointillize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"cellSize":3..300=5,"seed":u32=0,"background":json}
```

## filter.stylize.diffuse

Diffuse…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.diffuse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"mode":"normal|darkenOnly|lightenOnly|anisotropic","seed":u32=0}
```

## filter.stylize.extrude

Extrude…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.extrude`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"type":"blocks|pyramids","size":2..255=30,"depth":1..255=30,"depthMode":"random|levelBased","solidFrontFaces":bool,"maskIncompleteBlocks":bool,"seed":u32=0}
```

## filter.stylize.oilPaint

Oil Paint…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.oilPaint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"stylization":0.1..10=4,"cleanliness":0..10=5,"scale":0.1..10=1,"bristleDetail":0..10=5,"lighting":bool=true,"angle":-180..180=-60,"shine":0..10=1}
```

## filter.stylize.tiles

Tiles…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.tiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"count":1..99=10,"maxOffset":1..99=10,"fill":"background|foreground|inverse|unaltered","seed":u32=0,"foreground":json,"background":json}
```

## filter.stylize.traceContour

Trace Contour…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.traceContour`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"level":0..255=128,"edge":"lower|upper"}
```

## filter.stylize.wind

Wind…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.stylize.wind`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"wind|blast|stagger","direction":"fromRight|fromLeft","seed":u32=0}
```

## filter.distort.displace

Displace…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.displace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"horizontal":-999..999=10,"vertical":-999..999=10,"fit":"stretch|tile","undefinedAreas":"repeat|wrap","mapDocument":doc,"mapPath":text,"mapLayer":json}
```

## filter.distort.shear

Shear…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.shear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":-100..100=0,"undefinedAreas":"wrap|repeat","points":json}
```

## filter.distort.zigZag

ZigZag…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.distort.zigZag`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":-100..100=10,"ridges":0..20=5,"style":"pondRipples|outFromCenter|aroundCenter"}
```

## filter.render.fibers

Fibers…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.fibers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"variance":1..64=16,"strength":1..64=4,"seed":u32=0,"foreground":json,"background":json}
```

## filter.render.lensFlare

Lens Flare…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.lensFlare`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brightness":10..300=100,"centerX":0..1=0.5,"centerY":0..1=0.5,"lens":"zoom|prime35|prime105|moviePrime"}
```

## filter.render.lightingEffects

Lighting Effects…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.lightingEffects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"lightType":"spot|point|infinite","intensity":-100..100=75,"lightX":0..1=0.25,"lightY":0..1=0.2,"lightZ":0..2=0.6,"targetX":0..1=0.5,"targetY":0..1=0.55,"cone":1..89=45,"hotspot":0..100=50,"angle":-180..180=135,"elevation":0..90=45,"gloss":-100..100=0,"metallic":-100..100=0,"exposure":-100..100=0,"ambience":-100..100=8,"texture":"none|red|green|blue|alpha|luminance","height":0..100=50,"whiteIsHigh":bool=true,"lights":json}
```

## filter.noise.reduceNoise

Reduce Noise…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.noise.reduceNoise`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strength":0..10=6,"preserveDetails":0..100=60,"reduceColorNoise":0..100=45,"sharpenDetails":0..100=25,"removeJpegArtifact":bool}
```

## filter.blur.smartBlur

Smart Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.smartBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0.1..100=3,"threshold":0.1..100=25,"quality":"high|medium|low","mode":"normal|edgeOnly|overlayEdge"}
```

## filter.blur.lensBlur

Lens Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.lensBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0..100=15,"shape":"hexagon|triangle|square|pentagon|heptagon|octagon","bladeCurvature":0..100=0,"rotation":0..360=0,"depthMap":"none|transparency|layerMask","focalDistance":0..255=0,"invert":bool,"brightness":0..100=0,"threshold":0..255=255,"noise":0..100=0,"distribution":"uniform|gaussian","monochromatic":bool,"seed":u32=0}
```

## filter.blur.shapeBlur

Shape Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.shapeBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":5..1000=10,"shape":"circle|ring|square|diamond|triangle|hexagon|star|heart|cross"}
```

## filter.blurGallery.tiltShift

Tilt-Shift…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blurGallery.tiltShift`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"blur":0..500=15,"centerX":0..1=0.5,"centerY":0..1=0.5,"angle":-90..90=0,"focus":0..1=0.1,"transition":0.01..1=0.15}
```

## filter.blurGallery.irisBlur

Iris Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blurGallery.irisBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"blur":0..500=15,"centerX":0..1=0.5,"centerY":0..1=0.5,"radiusX":0.01..1=0.35,"radiusY":0.01..1=0.25,"angle":-180..180=0,"roundness":0..100=0,"feather":0..0.99=0.5,"pins":json}
```

## filter.blurGallery.fieldBlur

Field Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blurGallery.fieldBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"blur":0..500=15,"centerX":0..1=0.5,"centerY":0..1=0.5,"pins":json}
```

## filter.blurGallery.spinBlur

Spin Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blurGallery.spinBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"blurAngle":0..360=15,"centerX":0..1=0.5,"centerY":0..1=0.5,"radiusX":0.01..1=0.3,"radiusY":0.01..1=0.3,"angle":-180..180=0,"pins":json}
```

## filter.blurGallery.pathBlur

Path Blur…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blurGallery.pathBlur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"speed":0..500=50,"taper":0..100=0,"startX":0..1=0.2,"startY":0..1=0.5,"endX":0..1=0.8,"endY":0..1=0.5,"paths":json}
```

## filter.other.custom

Custom…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.other.custom`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"kernel":int[25],"scale":1..9999=1,"offset":-9999..9999=0}
```

## filter.other.hsbHsl

HSB/HSL

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.other.hsbHsl`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"inputMode":"rgb|hsb|hsl","rowOrder":"hsb|hsl|rgb"}
```

## filter.video.deInterlace

De-Interlace…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.video.deInterlace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"eliminate":"oddFields|evenFields","createBy":"interpolation|duplication"}
```

## filter.video.ntscColors

NTSC Colors

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.video.ntscColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.filterGallery

Filter Gallery…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.filterGallery`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"effects":json,"foreground":json,"background":json,"list":bool}
```

## filter.gallery.coloredPencil

Colored Pencil

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.coloredPencil`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pencilWidth":1..24=4,"strokePressure":0..15=8,"paperBrightness":0..50=25}
```

## filter.gallery.cutout

Cutout

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.cutout`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"numberOfLevels":2..8=4,"edgeSimplicity":0..10=4,"edgeFidelity":1..3=2}
```

## filter.gallery.dryBrush

Dry Brush

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.dryBrush`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brushSize":0..10=2,"brushDetail":0..10=8,"texture":1..3=1}
```

## filter.gallery.filmGrain

Film Grain

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.filmGrain`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"grain":0..20=4,"highlightArea":0..20=0,"intensity":0..10=10}
```

## filter.gallery.fresco

Fresco

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.fresco`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brushSize":0..10=2,"brushDetail":0..10=8,"texture":1..3=1}
```

## filter.gallery.neonGlow

Neon Glow

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.neonGlow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"glowSize":-24..24=5,"glowBrightness":0..50=15,"glowColor":json}
```

## filter.gallery.paintDaubs

Paint Daubs

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.paintDaubs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brushSize":1..50=8,"sharpness":0..40=7,"brushType":"simple|lightRough|darkRough|wideSharp|wideBlurry|sparkle"}
```

## filter.gallery.paletteKnife

Palette Knife

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.paletteKnife`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeSize":1..50=25,"strokeDetail":1..3=3,"softness":0..10=0}
```

## filter.gallery.plasticWrap

Plastic Wrap

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.plasticWrap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"highlightStrength":0..20=15,"detail":1..15=9,"smoothness":1..15=7}
```

## filter.gallery.posterEdges

Poster Edges

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.posterEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"edgeThickness":0..10=2,"edgeIntensity":0..10=1,"posterization":0..6=2}
```

## filter.gallery.roughPastels

Rough Pastels

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.roughPastels`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeLength":0..40=6,"strokeDetail":1..20=4,"texture":"canvas|brick|burlap|sandstone","scaling":50..200=100,"relief":0..50=20,"light":"bottom|bottomLeft|left|topLeft|top|topRight|right|bottomRight","invert":bool}
```

## filter.gallery.smudgeStick

Smudge Stick

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.smudgeStick`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeLength":0..10=2,"highlightArea":0..20=0,"intensity":0..10=10}
```

## filter.gallery.sponge

Sponge

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.sponge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brushSize":0..10=2,"definition":0..25=12,"smoothness":1..15=5}
```

## filter.gallery.underpainting

Underpainting

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.underpainting`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brushSize":0..40=6,"textureCoverage":0..40=16,"texture":"canvas|brick|burlap|sandstone","scaling":50..200=100,"relief":0..50=4,"light":"top|topRight|right|bottomRight|bottom|bottomLeft|left|topLeft","invert":bool}
```

## filter.gallery.watercolor

Watercolor

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.watercolor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"brushDetail":1..14=9,"shadowIntensity":0..10=1,"texture":1..3=1}
```

## filter.gallery.accentedEdges

Accented Edges

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.accentedEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"edgeWidth":1..14=2,"edgeBrightness":0..50=38,"smoothness":1..15=5}
```

## filter.gallery.angledStrokes

Angled Strokes

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.angledStrokes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"directionBalance":0..100=50,"strokeLength":3..50=15,"sharpness":0..10=3}
```

## filter.gallery.crosshatch

Crosshatch

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.crosshatch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeLength":3..50=9,"sharpness":0..20=6,"strength":1..3=1}
```

## filter.gallery.darkStrokes

Dark Strokes

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.darkStrokes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"balance":0..10=5,"blackIntensity":0..10=6,"whiteIntensity":0..10=2}
```

## filter.gallery.inkOutlines

Ink Outlines

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.inkOutlines`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeLength":1..50=4,"darkIntensity":0..50=20,"lightIntensity":0..50=10}
```

## filter.gallery.spatter

Spatter

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.spatter`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"sprayRadius":0..25=10,"smoothness":1..15=5}
```

## filter.gallery.sprayedStrokes

Sprayed Strokes

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.sprayedStrokes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeLength":0..20=12,"sprayRadius":0..25=7,"strokeDirection":"rightDiagonal|horizontal|leftDiagonal|vertical"}
```

## filter.gallery.sumiE

Sumi-e

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.sumiE`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeWidth":3..15=10,"strokePressure":0..15=2,"contrast":0..40=16}
```

## filter.gallery.diffuseGlow

Diffuse Glow

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.diffuseGlow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"graininess":0..10=6,"glowAmount":0..20=10,"clearAmount":0..20=15,"background":json}
```

## filter.gallery.glass

Glass

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.glass`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"distortion":0..20=5,"smoothness":1..15=3,"texture":"frosted|blocks|canvas|tinyLens","scaling":50..200=100,"invert":bool}
```

## filter.gallery.oceanRipple

Ocean Ripple

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.oceanRipple`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"rippleSize":1..15=9,"rippleMagnitude":0..20=9}
```

## filter.gallery.basRelief

Bas Relief

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.basRelief`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"detail":1..15=13,"smoothness":1..15=3,"light":"bottom|bottomLeft|left|topLeft|top|topRight|right|bottomRight","foreground":json,"background":json}
```

## filter.gallery.chalkCharcoal

Chalk & Charcoal

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.chalkCharcoal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"charcoalArea":0..20=6,"chalkArea":0..20=6,"strokePressure":0..5=1,"foreground":json,"background":json}
```

## filter.gallery.charcoal

Charcoal

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.charcoal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"charcoalThickness":1..7=1,"detail":0..5=5,"lightDarkBalance":0..100=50,"foreground":json,"background":json}
```

## filter.gallery.chrome

Chrome

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.chrome`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"detail":0..10=4,"smoothness":0..10=7}
```

## filter.gallery.conteCrayon

Conté Crayon

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.conteCrayon`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"foregroundLevel":1..15=11,"backgroundLevel":1..15=7,"texture":"canvas|brick|burlap|sandstone","scaling":50..200=100,"relief":0..50=4,"light":"top|topRight|right|bottomRight|bottom|bottomLeft|left|topLeft","invert":bool,"foreground":json,"background":json}
```

## filter.gallery.graphicPen

Graphic Pen

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.graphicPen`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokeLength":1..15=15,"lightDarkBalance":0..100=50,"strokeDirection":"rightDiagonal|horizontal|leftDiagonal|vertical","foreground":json,"background":json}
```

## filter.gallery.halftonePattern

Halftone Pattern

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.halftonePattern`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"size":1..12=1,"contrast":0..50=5,"patternType":"dot|circle|line","foreground":json,"background":json}
```

## filter.gallery.notePaper

Note Paper

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.notePaper`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"imageBalance":0..50=25,"graininess":0..20=10,"relief":0..25=11,"foreground":json,"background":json}
```

## filter.gallery.photocopy

Photocopy

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.photocopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"detail":1..24=7,"darkness":1..50=8,"foreground":json,"background":json}
```

## filter.gallery.plaster

Plaster

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.plaster`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"imageBalance":0..50=20,"smoothness":1..15=2,"light":"top|topRight|right|bottomRight|bottom|bottomLeft|left|topLeft","foreground":json,"background":json}
```

## filter.gallery.reticulation

Reticulation

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.reticulation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"density":0..50=12,"foregroundLevel":0..50=40,"backgroundLevel":0..50=5,"foreground":json,"background":json}
```

## filter.gallery.stamp

Stamp

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.stamp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"lightDarkBalance":0..50=25,"smoothness":1..50=5,"foreground":json,"background":json}
```

## filter.gallery.tornEdges

Torn Edges

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.tornEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"imageBalance":0..50=25,"smoothness":1..15=11,"contrast":1..25=17,"foreground":json,"background":json}
```

## filter.gallery.waterPaper

Water Paper

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.waterPaper`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"fiberLength":3..50=15,"brightness":0..100=60,"contrast":0..100=80}
```

## filter.gallery.glowingEdges

Glowing Edges

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.glowingEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"edgeWidth":1..14=2,"edgeBrightness":0..20=6,"smoothness":1..15=5}
```

## filter.gallery.craquelure

Craquelure

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.craquelure`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"crackSpacing":2..100=15,"crackDepth":0..10=6,"crackBrightness":0..10=9}
```

## filter.gallery.grain

Grain

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.grain`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"intensity":0..100=40,"contrast":0..100=50,"grainType":"regular|soft|sprinkles|clumped|contrasty|enlarged|stippled|horizontal|vertical|speckle","foreground":json,"background":json}
```

## filter.gallery.mosaicTiles

Mosaic Tiles

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.mosaicTiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"tileSize":2..100=12,"groutWidth":1..15=3,"lightenGrout":0..10=9}
```

## filter.gallery.patchwork

Patchwork

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.patchwork`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"squareSize":0..10=4,"relief":0..25=8}
```

## filter.gallery.stainedGlass

Stained Glass

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.stainedGlass`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"cellSize":2..50=10,"borderThickness":1..20=4,"lightIntensity":0..10=3,"foreground":json}
```

## filter.gallery.texturizer

Texturizer

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.gallery.texturizer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"texture":"canvas|brick|burlap|sandstone","scaling":50..200=100,"relief":0..50=4,"light":"top|topRight|right|bottomRight|bottom|bottomLeft|left|topLeft","invert":bool}
```

## type.create

New Type Layer

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px (baseline anchor of point text),"text":str,"box":[x,y,w,h]? (paragraph text),"name":str?,"align":"left|center|right|justify…"?, …character keys: "font","size":pt=12,"color",…}
```

## type.edit

Edit Type

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"text":str? (replace all, styles kept),"replace":{"start":char,"end":char,"text":str}?,"runs":[{"start":char,"end":char,…character keys}]?,"box":[x,y,w,h]? (to paragraph text),"point":[x,y]? (to point text),"move":[dx,dy]?,"transform":[a,b,c,d,e,f]?,"antialias":"none|sharp|crisp|strong|smooth"?,"name":str?}
```

## type.setStyle

Set Type Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.setStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"range":[startChar,endChar]? (default all), "font":str,"fontStyle":str,"weight":100..900,"italic":bool,"size":pt,"color":"#rrggbb"|[r,g,b,a],"tracking":1/1000em,"leading":pt|"auto","baselineShift":pt,"horizontalScale":%,"verticalScale":%,"underline":bool,"strikethrough":bool,"fauxBold":bool,"fauxItalic":bool,"kerning":"metrics|optical|none","caps":"normal|small|all","ligatures":bool,"discretionaryLigatures":bool,"features":{"ss01":1},"variations":{"wght":650},"language":str, paragraph keys: "align":"left|center|right|justify|justifyCenter|justifyRight|justifyAll","firstLineIndent":pt,"startIndent":pt,"endIndent":pt,"spaceBefore":pt,"spaceAfter":pt,"autoLeading":%,"direction":"auto|ltr|rtl","hyphenate":bool}
```

## type.rasterize

Rasterize Type

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.rasterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.info

Type Layer Info

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} → text, runs/paragraphs (char offsets + styles), shape, transform, laid-out lines (text space px), bounds
```

## type.fonts

List Fonts

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.fonts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"family":str? (faces of one family)}
```

## edit.transform

Free Transform

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"rect":[x0,y0,x1,y1]? (source frame; default = layer content ∩ selection),"quad":[[x,y]×4]? (where the frame's corners go, clockwise from top-left),"matrix":[a,b,c,d,e,f]? (affine alternative),"interpolation":"bicubic|bilinear|nearest"="bicubic"}
```

## shape.create

New Shape Layer

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"kind":"rect|roundedRect|ellipse|polygon|star|line|path"="rect","rect":[x,y,w,h] (rect/roundedRect/ellipse/polygon/star),"radii":[tl,tr,br,bl]|r (roundedRect=10),"sides":3..100=5,"starRatio":0..1 (star=0.5),"from":[x,y],"to":[x,y],"weight":px=1 (line),"path":{…} (kind path),"fill":"#rrggbb"|[r,g,b,a]|{"gradient":{"stops":[[t,"#hex"]],"angle":deg,"scale":%,"style":"linear|radial|angle|reflected|diamond","reverse":bool}}|{"pattern":name}|null (no fill)=foreground,"stroke":{"width":px,"color":"#rrggbb"|fill,"opacity":0..100,"align":"inside|center|outside","cap":"butt|round|square","join":"miter|round|bevel","miterLimit":n,"dashes":[multiples of width],"dashOffset":n}|null=none,"name":str?,"addTo":layerId? + "op":"combine|subtract|intersect|exclude" (append to an existing shape layer)} → shape.info. path: {"subpaths":[{"closed":bool=true,"op":"combine|subtract|intersect|exclude","knots":[[x,y] | {"anchor":[x,y],"in":[x,y],"out":[x,y],"smooth":bool}]}],"fillRule":"nonzero|evenodd","inverted":bool}
```

场景 / Recipes: [examples/adjustment-mask-create.json](../examples/adjustment-mask-create.json)；前置条件见 [调整蒙版](adjustment-mask.md)。

## shape.edit

Edit Shape

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":{…}? (replaces; drops live shape),"kind":str?,"rect":[x,y,w,h]?,"radii":[tl,tr,br,bl]|r?,"sides":n?,"starRatio":r?,"from":[x,y]?,"to":[x,y]?,"weight":px? (live-shape params regenerate the path),"move":[dx,dy]?,"transform":[a,b,c,d,e,f]?,"op":"combine|…"? + "subpath":index? (default all but the first),"fillRule":"nonzero|evenodd"?,"fill":"#rrggbb"|[r,g,b,a]|{"gradient":{"stops":[[t,"#hex"]],"angle":deg,"scale":%,"style":"linear|radial|angle|reflected|diamond","reverse":bool}}|{"pattern":name}|null (no fill)?,"stroke":{"width":px,"color":"#rrggbb"|fill,"opacity":0..100,"align":"inside|center|outside","cap":"butt|round|square","join":"miter|round|bevel","miterLimit":n,"dashes":[multiples of width],"dashOffset":n}|null? (merged into the current stroke),"name":str?} → shape.info
```

## shape.info

Shape Layer Info

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} → {layer,name,kind,path,fill,stroke,live,bounds:[x,y,w,h]}
```

## shape.rasterize

Rasterize Shape

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.rasterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## path.list

List Paths

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {paths:[{name,knots,subpaths}],workPath,clippingPath,layerPath (active layer's shape path / vector mask)}
```

## path.info

Path Info

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"|"layer"="work"} → {name,path}
```

## path.set

Set Path

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"="work","path":{…},"op":"combine|subtract|intersect|exclude"? (append to the existing path with this op instead of replacing)}. path: {"subpaths":[{"closed":bool=true,"op":"combine|subtract|intersect|exclude","knots":[[x,y] | {"anchor":[x,y],"in":[x,y],"out":[x,y],"smooth":bool}]}],"fillRule":"nonzero|evenodd","inverted":bool}
```

## path.delete

Delete Path

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"="work"}
```

## path.rename

Rename Path

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"="work","to":str} (renaming the work path saves it)
```

## path.toSelection

Make Selection from Path

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.toSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"|"layer"="work","feather":px=0,"antiAlias":bool=true,"mode":"replace|add|subtract|intersect"="replace"}
```

## select.toWorkPath

Make Work Path

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.toWorkPath`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"tolerance":0.5..10 px=2} → {subpaths,knots}
```

## path.fill

Fill Path

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.fill`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"|"layer"="work","layer":id? (pixel layer, default active),"color":"#rrggbb"=foreground,"opacity":0..100=100,"mode":"normal|multiply|…"="normal","feather":px=0,"antiAlias":bool=true}
```

## path.stroke

Stroke Path

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe path.stroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str|"work"|"layer"="work","layer":id? (pixel layer),"tool":"brush|pencil|eraser"="brush","size":px?,"hardness":0..1?,"opacity":0..100?,"color":"#rrggbb"=foreground} (current brush settings otherwise)
```

## layer.vectorMask.add

Add Vector Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":{…}? | "name":str|"work"? (copy a document path),"hide":bool=false (Hide All = inverted)} → vector mask info. Without a path the mask reveals all.
```

## layer.vectorMask.fromPath

Vector Mask from Current Path

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.fromPath`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"name":str|"work"="work"}
```

## layer.vectorMask.edit

Edit Vector Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":{…}?,"enabled":bool?,"linked":bool?,"density":0..100?,"feather":px?,"invert":true?}. path: {"subpaths":[{"closed":bool=true,"op":"combine|subtract|intersect|exclude","knots":[[x,y] | {"anchor":[x,y],"in":[x,y],"out":[x,y],"smooth":bool}]}],"fillRule":"nonzero|evenodd","inverted":bool}
```

## layer.vectorMask.delete

Delete Vector Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.rasterize.vectorMask

Rasterize Vector Mask

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.vectorMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} (multiplied into the layer mask)
```

## layer.vectorMask.revealAll

Vector Mask: Reveal All

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.revealAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.vectorMask.hideAll

Vector Mask: Hide All

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.hideAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.vectorMask.currentPath

Vector Mask: Current Path

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.currentPath`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"name":str|"work"="work"}
```

## layer.vectorMask.enabled

Enable Vector Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.enabled`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"enabled":bool? (default: toggle)}
```

## layer.vectorMask.linked

Link Vector Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.linked`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"linked":bool? (default: toggle)}
```

## layer.rasterize.shape

Rasterize Shape

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.shape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.combineShapes.unite

Unite Shapes

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.combineShapes.unite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"subpath":index? (default all but the first)}
```

## layer.combineShapes.subtractFrontShape

Subtract Front Shape

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.combineShapes.subtractFrontShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"subpath":index?}
```

## layer.combineShapes.intersectShapeAreas

Intersect Shape Areas

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.combineShapes.intersectShapeAreas`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"subpath":index?}
```

## layer.combineShapes.excludeOverlappingShapes

Exclude Overlapping Shapes

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.combineShapes.excludeOverlappingShapes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"subpath":index?}
```

## layer.combineShapes.mergeShapeComponents

Merge Shape Components

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.combineShapes.mergeShapeComponents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"tolerance":px=0.1} (bakes the path operations into plain combined outlines, traced from the exact coverage)
```

## select.convertToShape

Convert Selection to Shape

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.convertToShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"tolerance":px=2,"fill":"#rrggbb"=foreground,"name":str?} → shape.info
```

## layer.vectorMask.info

Vector Mask Info

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.vectorMask.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} → {layer,path,enabled,linked,density,feather}
```

## select.quick

Quick Selection

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.quick`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y],…],"size":px=30,"mode":"add|subtract|replace"="add","sampleAllLayers":bool=false,"enhanceEdge":bool=false}
```

## select.object

Object Selection

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.object`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"rect":[x,y,w,h],"mode":"replace|add|subtract|intersect"="replace","sampleAllLayers":bool=false}
```

## select.subject

Subject

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.subject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"sampleAllLayers":bool=true,"mode":"replace|add|subtract|intersect"="replace"}
```

## select.refineEdge

Refine Edge

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.refineEdge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":px=0,"smartRadius":bool=false,"smooth":0..100=0,"feather":px=0,"contrast":0..100=0,"shiftEdge":-100..100=0,"decontaminate":bool=false,"amount":0..100=100,"output":"selection|layerMask|newLayer|newLayerWithMask"="selection","sampleAllLayers":bool=false}
```

## select.focusArea

Focus Area…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.focusArea`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"range":0..1=0.5,"noise":0..1=0,"sampleAllLayers":bool=true,"mode":"replace|add|subtract|intersect"="replace"}
```

## edit.cut

Cut

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.cut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.copy

Copy

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.copy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.copyMerged

Copy Merged

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.copyMerged`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.paste

Paste

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.paste`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"center":[x,y]? (view centre; default keeps the position when it overlaps the canvas)}
```

## edit.pasteSpecial.pasteInPlace

Paste in Place

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteSpecial.pasteInPlace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.new.layerViaCopy

Layer via Copy

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.layerViaCopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.new.layerViaCut

Layer via Cut

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.layerViaCut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.mergeVisible

Merge Visible

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.mergeVisible`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.autoTone

Auto Tone

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.autoTone`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.autoContrast

Auto Contrast

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.autoContrast`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.autoColor

Auto Color

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.autoColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.toggleLastState

Toggle Last State

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.toggleLastState`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.transform.again

Again

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.again`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## view.newGuide

New Guide…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.newGuide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"orientation":"horizontal|vertical","position":px}
```

## view.moveGuide

Move Guide

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.moveGuide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"orientation":"horizontal|vertical","index":n,"position":px}
```

## view.deleteGuide

Delete Guide

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.deleteGuide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"orientation":"horizontal|vertical","index":n}
```

## view.clearGuides

Clear Guides

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.clearGuides`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.assignProfile

Assign Profile…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.assignProfile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"working|srgb|display-p3|adobe-rgb-compat|prophoto-compat|linear-srgb|rec2020|gray-gamma-2.2|sgray|lab-d50|coated-cmyk|none" (or a path to an .icc file)}
```

## edit.convertToProfile

Convert to Profile…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.convertToProfile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"srgb|display-p3|adobe-rgb-compat|prophoto-compat|linear-srgb|rec2020|gray-gamma-2.2|sgray|lab-d50|coated-cmyk|working" (or a path to an .icc file),"intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true}
```

## edit.colorSettings

Color Settings…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.colorSettings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"workingRgb":"srgb|display-p3|adobe-rgb-compat|prophoto-compat|linear-srgb|rec2020","workingCmyk":"coated-cmyk","workingGray":"sgray|gray-gamma-2.2","policyRgb":"preserve|convert|off","policyCmyk":"preserve|convert|off","policyGray":"preserve|convert|off","askOnMismatch":bool=true,"askOnPaste":bool=true,"askOnMissing":bool=false,"intent":"relative|perceptual|saturation|absolute","blendTextGamma":1.0..2.2|bool=1.45,"bpc":bool=true,"dither":bool=true,"monitorProfile":"auto|srgb|display-p3|adobe-rgb-compat|prophoto-compat|rec2020","reset":bool=false} (working spaces and the monitor profile also accept .icc paths; monitor `auto` = the main display's profile when the platform provides it, else sRGB)
```

## color.profileMismatch

Embedded Profile Mismatch

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe color.profileMismatch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"preserve|convert|discard|assignWorking"}
```

## edit.profileInfo

Profile Info

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.profileInfo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"<builtin id>|document|/path/to/profile.icc"=document}
```

## view.proofSetup

Proof Setup…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"working-cmyk|srgb|display-p3|adobe-rgb-compat|prophoto-compat|linear-srgb|rec2020|gray-gamma-2.2|sgray|lab-d50|coated-cmyk" (or a path to an .icc file)="working-cmyk","intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true,"simulatePaper":bool=false}
```

## view.proofColors

Proof Colors

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofColors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool=toggle}
```

## view.gamutWarning

Gamut Warning

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.gamutWarning`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool=toggle,"threshold":deltaE=4,"profile":"<proof profile override>"}
```

## paint.pencil

Pencil

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.pencil`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?,tiltX?,tiltY?,rotation?,timeMs?,wheel?],…],"brush":{…}?,"preset":name?,"size":px?,"opacity":0..1?,"color":"#rrggbb"?=foreground,"mode":"normal|multiply|screen|…"="normal","erase":bool?,"autoErase":bool=false,"seed":u64?,"target":"pixels"|"mask"|"quickMask"|{"channel":i}=Channels panel target}
```

## paint.mixerBrush

Mixer Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.mixerBrush`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[…],"brush":{…}?,"preset":name?,"size":px?,"wet":0..100=brush.mixer.wet,"load":0..100=brush.mixer.load,"mix":0..100=brush.mixer.mix,"flow":0..100=brush.mixer.flow,"color":"#rrggbb"?=foreground,"sampleAllLayers":bool=brush.mixer.sampleAllLayers,"cleanAfterStroke":bool=true,"loadAfterStroke":bool=true,"seed":u64?}
```

## paint.colorReplacement

Color Replacement

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.colorReplacement`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[…],"brush":{…}?,"size":px?,"mode":"hue|saturation|color|luminosity"="color","sampling":"continuous|once|backgroundSwatch"="continuous","limits":"contiguous|discontiguous|findEdges"="contiguous","tolerance":0..100=30,"antiAlias":bool=true,"color":"#rrggbb"?=foreground,"seed":u64?}
```

## brush.presets.list

List Brush Presets

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"full":bool=false}
```

## brush.presets.save

Save Brush Preset

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.save`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":string,"brush":{…BrushSettings}?=current brush}
```

## brush.presets.delete

Delete Brush Preset

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":string}
```

## brush.defineFromSelection

Define Brush Preset…

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.defineFromSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":string}
```

## brush.get

Get Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## tools.setBrush

Set Brush

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tools.setBrush`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":name?,"reset":bool?,…BrushSettings fields (camelCase, deep-merged)}
```

## paint.magicEraser

Magic Eraser

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.magicEraser`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"tolerance":0..255=32,"antiAlias":bool=true,"contiguous":bool=true,"sampleAllLayers":bool=false,"opacity":1..100=100}
```

## paint.backgroundEraser

Background Eraser

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.backgroundEraser`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px?,"hardness":0..1?,"brush":{…}?,"preset":name?,"sampling":"continuous|once|backgroundSwatch"="continuous","limits":"discontiguous|contiguous|findEdges"="contiguous","tolerance":0..100=50,"protectForegroundColor":bool=false,"seed":u64?}
```

## brush.presets.importAbr

Import Brushes…

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.importAbr`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":".abr file"?,"data":base64 bytes?,"group":string?=file name,"replace":bool=true (replace a group of the same name),"select":bool=false (make the first imported preset current)}
```

## gradient.presets.importGrd

Import Gradients…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.importGrd`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":".grd file"?,"data":base64 bytes?,"group":string?=file name,"replace":bool=true (replace a group of the same name)}
```

## paint.cloneStamp

Clone Stamp

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.cloneStamp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"source":[sx,sy] (sampled under the first point) | "offset":[dx,dy],"aligned":bool=true,"sampleLayer":"current|currentAndBelow|all"="current","mode":"normal|multiply|…"="normal" → {"damage","offset","aligned","nextSource"}}
```

## paint.healingBrush

Healing Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.healingBrush`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"source":[sx,sy] | "offset":[dx,dy],"aligned":bool=true,"sampleLayer":"current|currentAndBelow|all"="current","mode":"normal|…"="normal" → {"damage","offset","aligned","nextSource"}}
```

## paint.spotHealing

Spot Healing Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.spotHealing`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"type":"contentAware|createTexture|proximityMatch"="contentAware"}
```

## paint.dodge

Dodge

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.dodge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"range":"shadows|midtones|highlights"="midtones","exposure":1..100=50,"protectTones":bool=true}
```

## paint.burn

Burn

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.burn`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"range":"shadows|midtones|highlights"="midtones","exposure":1..100=50,"protectTones":bool=true}
```

## paint.sponge

Sponge

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.sponge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"mode":"desaturate|saturate"="desaturate","vibrance":bool=true (flow = sponge strength)}
```

## paint.blur

Blur

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.blur`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"strength":1..100=50}
```

## paint.sharpen

Sharpen

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.sharpen`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"strength":1..100=50,"protectDetail":bool=true}
```

## paint.smudge

Smudge

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.smudge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"strength":1..100=50,"fingerPainting":bool=false (starts with the foreground colour)}
```

## paint.historyBrush

History Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.historyBrush`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y,pressure?],…],"size":px=tool size,"hardness":0..100=tool hardness,"opacity":1..100=100,"flow":1..100=100,"spacing":1..1000 (% of size)=25,"layer":id?=active,"state":index (into history.entries; default 0 = the oldest held state, normally the Open snapshot)}
```

## image.imageSize

Image Size…

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.imageSize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":px,"height":px,"resolution":ppi,"resample":"bicubic|bilinear|nearest|lanczos|preserveDetails|none"="bicubic"}
```

## image.canvasSize

Canvas Size…

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.canvasSize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":px,"height":px,"relative":bool=false,"anchor":"topLeft|top|topRight|left|center|right|bottomLeft|bottom|bottomRight"="center","extensionColor":"background|foreground|white|black|transparent|#rrggbb"="background"}
```

## image.crop

Crop

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.crop`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"width":px,"height":px,"deleteCroppedPixels":bool=true}
```

## image.trim

Trim…

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.trim`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"basedOn":"transparent|topLeft|bottomRight"="transparent","top":bool=true,"bottom":bool=true,"left":bool=true,"right":bool=true}
```

## image.mode.rgb

RGB Color

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.rgb`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"<builtin id>|working|/path/to/profile.icc"=working,"intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true}
```

## image.mode.grayscale

Grayscale

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.grayscale`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"<builtin id>|working|/path/to/profile.icc"=working,"intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true}
```

## image.mode.cmyk

CMYK Color

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.cmyk`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"<builtin id>|working|/path/to/profile.icc"=working,"intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true}
```

## image.mode.lab

Lab Color

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.lab`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"<builtin id>|working|/path/to/profile.icc"=working,"intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true}
```

## image.mode.bits8

8 Bits/Channel

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.bits8`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.mode.bits16

16 Bits/Channel

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.bits16`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.mode.bits32

32 Bits/Channel

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.bits32`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.duplicate

Duplicate…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str,"mergedOnly":bool=false}
```

## select.magicWand

Magic Wand

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.magicWand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"tolerance":0..255=32,"contiguous":bool=true,"antiAlias":bool=true,"sampleAllLayers":bool=false,"mode":"replace|add|subtract|intersect"="replace"}
```

## select.colorRange

Color Range…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.colorRange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"select":"sampledColors|reds|yellows|greens|cyans|blues|magentas|highlights|midtones|shadows|outOfGamut"="sampledColors","color":"#rrggbb"=foreground,"colors":["#rrggbb",…]?,"points":[[x,y],…]? (eyedropper samples),"subtractPoints":[[x,y],…]? (minus eyedropper),"fuzziness":0..200=40 (tones: 0..100 %=20),"localized":bool=false,"range":0..100=100 (% of the longer side),"tonalRange":level|[lo,hi] (shadows 65, highlights 190, midtones [105,150]),"invert":bool=false,"sampleAllLayers":bool=true,"mode":"replace|add|subtract|intersect"="replace"}
```

## select.modify.border

Border…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.modify.border`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..200=1}
```

## select.modify.smooth

Smooth…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.modify.smooth`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..500=1}
```

## select.modify.expand

Expand…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.modify.expand`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..500=1}
```

## select.modify.contract

Contract…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.modify.contract`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..500=1}
```

## select.modify.feather

Feather…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.modify.feather`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":0.1..1000=1}
```

## select.grow

Grow

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.grow`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"tolerance":0..255=32,"sampleAllLayers":bool=false}
```

## select.similar

Similar

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.similar`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"tolerance":0..255=32,"sampleAllLayers":bool=false}
```

## select.lasso

Lasso

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.lasso`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"points":[[x,y],…],"mode":"replace|add|subtract|intersect"="replace","antiAlias":bool=true,"feather":px=0}
```

## select.sky

Sky

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.sky`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"mode":"replace|add|subtract|intersect"="replace","sampleAllLayers":bool=true,"threshold":0..100=50 (higher = stricter),"softness":0..100=50 (edge softness)} → {selected, changed, coverage (0–1 of the canvas), bounds [x,y,w,h]}
```

## select.isolateLayers

Isolate Layers

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.isolateLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool? (default: toggle)} — Layers panel lists only the selected layers → {isolated, layers}
```

## select.transformSelection

Transform Selection

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.transformSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"rect":[x0,y0,x1,y1]? (frame; default = selection bounds),"quad"|"corners":[[x,y]×4]? (where the frame's corners go: distort/perspective),"matrix":[a,b,c,d,e,f]?,"scaleX":%=100,"scaleY":%=100,"rotate":deg=0,"skewX":deg=0,"skewY":deg=0,"dx":px=0,"dy":px=0,"reference":"center|topLeft|top|topRight|left|right|bottomLeft|bottom|bottomRight"|[x,y]="center","style"|"mesh"|"grid"|"warp":… (warp, as edit.transform.warp),"interpolation":"bilinear|bicubic|nearest"="bilinear"}
```

## paint.bucket

Paint Bucket

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.bucket`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"tolerance":0..255=32,"contiguous":bool=true,"antiAlias":bool=true,"contents":"foreground|pattern"="foreground","color":"#rrggbb"=foreground,"pattern":id|name (contents=pattern),"scale":%=100,"angle":deg,"opacity":1..100=100,"target":"pixels"|"mask"|"quickMask"|{"channel":i}=Channels panel target}
```

## paint.gradient

Gradient

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe paint.gradient`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":[x,y],"to":[x,y],"style":"linear|radial|angle|reflected|diamond"="linear","colors":["#rrggbb",…]? (evenly spaced),"gradient":preset name?,"stops":[[t,"#rrggbb"|"foreground"|"background"],…]?,"transparency":[[t,0..100],…]? (default: the current gradient, see gradient.presets.select),"reverse":bool=false,"dither":bool=true,"opacity":1..100=100,"mode":"normal|multiply|…"="normal","target":"pixels"|"mask"|"quickMask"|{"channel":i}=Channels panel target}
```

## edit.stroke

Stroke…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.stroke`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":1..250=1,"color":"#rrggbb|[r,g,b,a]"=foreground,"location":"inside|center|outside"="center","opacity":0..100=100}
```

## edit.transform.rotate180

Rotate 180°

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.rotate180`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.transform.rotate90Cw

Rotate 90° Clockwise

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.rotate90Cw`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.transform.rotate90Ccw

Rotate 90° Counter Clockwise

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.rotate90Ccw`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.transform.flipHorizontal

Flip Horizontal

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.flipHorizontal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.transform.flipVertical

Flip Vertical

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.flipVertical`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.pasteSpecial.pasteInto

Paste Into

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteSpecial.pasteInto`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"center":[x,y]?}
```

## edit.pasteSpecial.pasteOutside

Paste Outside

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.pasteSpecial.pasteOutside`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"center":[x,y]?}
```

## select.reselect

Reselect

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.reselect`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.adjustments.equalize

Equalize

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.equalize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.revealAll

Reveal All

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.revealAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.new.layerFromBackground

Layer From Background…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.layerFromBackground`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.layerStyle.copyLayerStyle

Copy Layer Style

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.copyLayerStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerStyle.pasteLayerStyle

Paste Layer Style

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.pasteLayerStyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerStyle.hideAllEffects

Hide All Effects

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.hideAllEffects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.layerStyle.showAllEffects

Show All Effects

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.showAllEffects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.layerMask.enabled

Disable Layer Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.enabled`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"enabled":bool? (default: toggle)}
```

## layer.layerMask.linked

Unlink Layer Mask

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.linked`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"linked":bool? (default: toggle)}
```

## layer.rasterize.layer

Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.layer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.rasterize.allLayers

All Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.allLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.rasterize.type

Type

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.type`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.rasterize.fillContent

Fill Content

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.fillContent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.rasterize.smartObject

Smart Object

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.smartObject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.delete.hiddenLayers

Hidden Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.delete.hiddenLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.scripts.deleteAllEmptyLayers

Delete All Empty Layers

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.deleteAllEmptyLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.ungroupLayers

Ungroup Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.ungroupLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.hideLayers

Hide Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.hideLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.showLayers

Show Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.showLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## filter.blur.average

Average

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.blur.average`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## filter.render.clouds

Clouds

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.clouds`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"seed":u32=0}
```

## filter.render.differenceClouds

Difference Clouds

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.differenceClouds`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"seed":u32=0}
```

## file.closeAll

Close All

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.closeAll`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.closeOthers

Close Others

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.closeOthers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"document":index? (the one to keep; default active)}
```

## file.revert

Revert

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.revert`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (reloads the saved file as one undoable step)
```

## file.saveACopy

Save a Copy…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.saveACopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str (format from the extension),"quality":0..12? (JPEG),"layers":bool=true}
```

## file.openAs

Open As…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.openAs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"as":"psd|png|jpg|tiff|…"? (decode as this format)}
```

## file.placeEmbedded

Place Embedded…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.placeEmbedded`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"scale":%? (default: fit when larger than the canvas),"fit":bool=true,"center":[x,y]?}
```

## file.placeLinked

Place Linked…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.placeLinked`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str,"scale":%?,"fit":bool=true,"center":[x,y]?}
```

## file.fileInfo

File Info…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.fileInfo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"title":str?,"author":str?,"authorTitle":str?,"description":str?,"keywords":[str]|"a; b"?,"copyright":str?,"copyrightStatus":"unknown|copyrighted|publicDomain"?,"copyrightUrl":str?} (no keys: read)
```

## file.automate.fitImage

Fit Image…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.fitImage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":px,"height":px,"dontEnlarge":bool=false,"resample":"bicubic|bilinear|nearest|lanczos|preserveDetails"="bicubic"}
```

## file.automate.conditionalModeChange

Conditional Mode Change…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.conditionalModeChange`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"from":["rgb","grayscale","cmyk","lab","indexed","bitmap",…]|"any"="any","to":"rgb|grayscale|cmyk|lab"}
```

## file.automate.batch

Batch…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.batch`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"steps":[[commandId,params]|{"command":id,"params":{}}…] (a recorded action),"input":folder|[paths],"output":folder,"format":"same|png|jpg|psd|tiff|…"="same","quality":0..12?} → {files, errors}
```

## file.scripts.imageProcessor

Image Processor…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.imageProcessor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"input":folder|[paths],"output":folder,"format":"jpg|png|psd|tiff|…"="jpg","quality":0..12=8,"width":px?,"height":px? (fit, never enlarge),"convertToSrgb":bool=false} → {files, errors}
```

## file.scripts.loadFilesIntoStack

Load Files into Stack…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.loadFilesIntoStack`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str]|folder,"createSmartObject":bool=false} → new document with one layer per file (inside one smart object with createSmartObject)
```

## file.scripts.flattenAllLayerEffects

Flatten All Layer Effects

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.flattenAllLayerEffects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## file.scripts.flattenAllMasks

Flatten All Masks

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.flattenAllMasks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (pixel layers; masks on other layer kinds are left)
```

## file.export.layersToFiles

Layers to Files…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.layersToFiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"dir":folder,"format":"png|jpg|psd|tiff|…"="png","prefix":str=document name,"visibleOnly":bool=true,"quality":0..12?} → {files}
```

## file.export.colorLookupTables

Color Lookup Tables…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.colorLookupTables`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str? (.cube; omit to return the text),"size":2..256=33,"title":str?}
```

## view.newGuideLayout

New Guide Layout…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.newGuideLayout`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"columns":n=0,"width":px?,"gutter":px=0,"rows":n=0,"height":px?,"rowGutter":px=gutter,"margin":px|[top,left,bottom,right]=0,"centerColumns":bool=false,"clearExisting":bool=false}
```

## view.newGuidesFromShape

New Guides From Shape

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.newGuidesFromShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## view.clearCanvasGuides

Clear Canvas Guides

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.clearCanvasGuides`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## type.antiAlias.none

None

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.none`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.antiAlias.sharp

Sharp

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.sharp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.antiAlias.crisp

Crisp

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.crisp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.antiAlias.strong

Strong

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.strong`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.antiAlias.smooth

Smooth

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.smooth`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.antiAlias.windowsLcd

Windows LCD

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.windowsLcd`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.antiAlias.windows

Windows

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.antiAlias.windows`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.orientation.horizontal

Horizontal

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.orientation.horizontal`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.orientation.vertical

Vertical

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.orientation.vertical`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} (stored and saved; rendered horizontally for now)
```

## type.openType.standardLigatures

Standard Ligatures

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.standardLigatures`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.contextualAlternates

Contextual Alternates

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.contextualAlternates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.discretionaryLigatures

Discretionary Ligatures

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.discretionaryLigatures`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.swash

Swash

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.swash`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.oldstyle

Oldstyle

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.oldstyle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.stylisticAlternates

Stylistic Alternates

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.stylisticAlternates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.titlingAlternates

Titling Alternates

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.titlingAlternates`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.ornaments

Ornaments

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.ornaments`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.ordinals

Ordinals

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.ordinals`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.openType.fractions

Fractions

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.openType.fractions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"on":bool? (default: toggle),"range":[startChar,endChar]? (default all)}
```

## type.createWorkPath

Create Work Path

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.createWorkPath`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.convertToShape

Convert to Shape

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.convertToShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.rasterizeTypeLayer

Rasterize Type Layer

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.rasterizeTypeLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.convertToParagraphText

Convert to Paragraph Text

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.convertToParagraphText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.convertToPointText

Convert to Point Text

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.convertToPointText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.warpText

Warp Text…

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.warpText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"style":"none|arc|arcLower|arcUpper|arch|bulge|shellLower|shellUpper|flag|wave|fish|rise|fisheye|inflate|squeeze|twist"="arc","bend":-100..100=50,"horizontalDistortion":-100..100=0,"verticalDistortion":-100..100=0,"orientation":"horizontal|vertical"="horizontal"}
```

## type.updateAllTextLayers

Update All Text Layers

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.updateAllTextLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## type.replaceAllMissingFonts

Replace All Missing Fonts

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.replaceAllMissingFonts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (with the default family)
```

## type.resolveMissingFonts

Resolve Missing Fonts…

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.resolveMissingFonts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"map":{"Missing Family":"Installed Family"}?} (no map: list the missing families)
```

## type.pasteLoremIpsum

Paste Lorem Ipsum

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.pasteLoremIpsum`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"at":char? (default end),"new":bool=false (new paragraph text layer)}
```

## type.saveDefaultTypeStyles

Save Default Type Styles

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.saveDefaultTypeStyles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (from the active type layer; new type layers start from them)
```

## type.loadDefaultTypeStyles

Load Default Type Styles

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.loadDefaultTypeStyles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## type.characterStyle.new

New Character Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"attrs":{model fields as in type.info ("size_pt":36,"font_family":"Inter","align":"Center",…) or Character/Paragraph panel keys as in type.setStyle ("size":36,"font":"Inter","color":"#rrggbb","align":"center",…)}?,"fromSelection":bool=true (start from the targeted text's formatting),"apply":bool=false,"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)} → {"id","name"}
```

## type.characterStyle.duplicate

Duplicate Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32}
```

## type.characterStyle.delete

Delete Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32} (text keeps its formatting as overrides)
```

## type.characterStyle.rename

Rename Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32,"name":str}
```

## type.characterStyle.set

Character Style Options

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32 (paragraph: 0 = Basic Paragraph),"name":str?,"attrs":{model fields as in type.info ("size_pt":36,"font_family":"Inter","align":"Center",…) or Character/Paragraph panel keys as in type.setStyle ("size":36,"font":"Inter","color":"#rrggbb","align":"center",…)},"replace":bool=false (drop attributes not given),"clear":[field]?} (text using the style updates, overrides kept)
```

## type.characterStyle.apply

Apply Character Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32|0|null (0/null: None / Basic Paragraph),"clearOverrides":bool=false (Alt-click),"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)}
```

## type.characterStyle.redefine

Redefine Character Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.redefine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32? (default: the targeted text's style),"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)} (the style takes the formatting of the start of the targeted text)
```

## type.characterStyle.clearOverride

Clear Override

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.clearOverride`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)}
```

## type.characterStyle.list

List Character Styles

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.characterStyle.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)} → {"styles":[{"id","name",attributes,"resolved"}],"current":{"character":id|null (mixed),"characterOverride":bool,"paragraph":id|null,"paragraphOverride":bool}}
```

## type.paragraphStyle.new

New Paragraph Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"attrs":{model fields as in type.info ("size_pt":36,"font_family":"Inter","align":"Center",…) or Character/Paragraph panel keys as in type.setStyle ("size":36,"font":"Inter","color":"#rrggbb","align":"center",…)}?,"fromSelection":bool=true (start from the targeted text's formatting),"apply":bool=false,"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)} → {"id","name"}
```

## type.paragraphStyle.duplicate

Duplicate Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32}
```

## type.paragraphStyle.delete

Delete Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32} (text keeps its formatting as overrides)
```

## type.paragraphStyle.rename

Rename Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32,"name":str}
```

## type.paragraphStyle.set

Paragraph Style Options

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32 (paragraph: 0 = Basic Paragraph),"name":str?,"attrs":{model fields as in type.info ("size_pt":36,"font_family":"Inter","align":"Center",…) or Character/Paragraph panel keys as in type.setStyle ("size":36,"font":"Inter","color":"#rrggbb","align":"center",…)},"replace":bool=false (drop attributes not given),"clear":[field]?} (text using the style updates, overrides kept)
```

## type.paragraphStyle.apply

Apply Paragraph Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32|0|null (0/null: None / Basic Paragraph),"clearOverrides":bool=false (Alt-click),"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)}
```

## type.paragraphStyle.redefine

Redefine Paragraph Style

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.redefine`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":u32? (default: the targeted text's style),"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)} (the style takes the formatting of the start of the targeted text)
```

## type.paragraphStyle.clearOverride

Clear Override

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.clearOverride`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)}
```

## type.paragraphStyle.list

List Paragraph Styles

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.paragraphStyle.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id? | "layers":[id]? (default: the selected type layers),"range":[startChar,endChar]? (one layer; default all text)} → {"styles":[{"id","name",attributes,"resolved"}],"current":{"character":id|null (mixed),"characterOverride":bool,"paragraph":id|null,"paragraphOverride":bool}}
```

## edit.checkSpelling

Check Spelling…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.checkSpelling`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"list|change|changeAll|addToDictionary|removeFromDictionary|suggest"="list","allLayers":bool=true,"layer":id? (check one layer),"ignore":[word]? (Ignore All for this check),"suggestions":n=5; change: "layer","start","end" (chars),"word"? (verified),"replace"; changeAll: "word","replace"; addToDictionary/removeFromDictionary/suggest: "word"} → list: {"misspellings":[{"layer","start","end","word","suggestions"}],"count"}
```

## type.insertText

Insert Glyph

- 技能 / Owner: `photocraft-cli-text`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-text`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe type.insertText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"text":str,"at":char? (default: end of text),"range":[startChar,endChar]? (replaced),"label":str?} → {"layer","caret"}
```

## layer.smartObjects.convertToSmartObject

Convert to Smart Object

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.convertToSmartObject`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## filter.convertForSmartFilters

Convert for Smart Filters

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.convertForSmartFilters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.newSmartObjectViaCopy

New Smart Object via Copy

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.newSmartObjectViaCopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.rasterize

Rasterize

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.rasterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.editContents

Edit Contents

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.editContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?} → opens the contents as a new document; saving (layer.smartObjects.saveContents) or closing it updates the smart object
```

## layer.smartObjects.saveContents

Save Contents

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.saveContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (in an Edit Contents document)
```

## layer.smartObjects.replaceContents

Replace Contents…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.replaceContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":str}
```

## layer.smartObjects.exportContents

Export Contents…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.exportContents`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":str}
```

## layer.smartObjects.relinkToFile

Relink to File…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.relinkToFile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":str}
```

## layer.smartObjects.updateModifiedContent

Update Modified Content

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.updateModifiedContent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.updateAllModifiedContent

Update All Modified Content

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.updateAllModifiedContent`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.smartObjects.convertToEmbedded

Convert to Embedded

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.convertToEmbedded`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.convertToLinked

Convert to Linked…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.convertToLinked`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":str} (writes the contents there)
```

## layer.smartFilter.disableSmartFilters

Disable Smart Filters

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.disableSmartFilters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"enabled":bool? (default: toggle)}
```

## layer.smartFilter.deleteFilterMask

Delete Filter Mask

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.deleteFilterMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartFilter.disableFilterMask

Disable Filter Mask

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.disableFilterMask`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"enabled":bool? (default: toggle)}
```

## layer.smartFilter.blendingOptions

Blending Options…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.blendingOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"index":u32? (0 = bottom; default top),"blend":str?,"opacity":0..1?}
```

## layer.smartFilter.clearSmartFilters

Clear Smart Filters

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.clearSmartFilters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartFilter.setVisible

Show/Hide Smart Filter

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.setVisible`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"index":u32?,"visible":bool? (default: toggle)}
```

## layer.smartFilter.setParams

Edit Smart Filter

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.setParams`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"index":u32?,"params":{…} (merged)}
```

## layer.smartFilter.delete

Delete Smart Filter

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"index":u32?}
```

## layer.smartFilter.move

Move Smart Filter

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartFilter.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"index":u32?,"to":u32}
```

## select.allLayers

All Layers

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.allLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.deselectLayers

Deselect Layers

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.deselectLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## select.findLayers

Find Layers

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.findLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str (case-insensitive substring)}
```

## layer.selectLinkedLayers

Select Linked Layers

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.selectLinkedLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.align.topEdges

Top Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.align.topEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"to":"auto|layers|selection|canvas"="auto"} (auto: the selection bounds with one layer and an active selection, else the selected layers' bounds)
```

## layer.align.verticalCenters

Vertical Centers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.align.verticalCenters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"to":"auto|layers|selection|canvas"="auto"} (auto: the selection bounds with one layer and an active selection, else the selected layers' bounds)
```

## layer.align.bottomEdges

Bottom Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.align.bottomEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"to":"auto|layers|selection|canvas"="auto"} (auto: the selection bounds with one layer and an active selection, else the selected layers' bounds)
```

## layer.align.leftEdges

Left Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.align.leftEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"to":"auto|layers|selection|canvas"="auto"} (auto: the selection bounds with one layer and an active selection, else the selected layers' bounds)
```

## layer.align.horizontalCenters

Horizontal Centers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.align.horizontalCenters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"to":"auto|layers|selection|canvas"="auto"} (auto: the selection bounds with one layer and an active selection, else the selected layers' bounds)
```

## layer.align.rightEdges

Right Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.align.rightEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"to":"auto|layers|selection|canvas"="auto"} (auto: the selection bounds with one layer and an active selection, else the selected layers' bounds)
```

## layer.distribute.topEdges

Top Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.topEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.distribute.verticalCenters

Vertical Centers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.verticalCenters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.distribute.bottomEdges

Bottom Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.bottomEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.distribute.leftEdges

Left Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.leftEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.distribute.horizontalCenters

Horizontal Centers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.horizontalCenters`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.distribute.rightEdges

Right Edges

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.rightEdges`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.distribute.horizontally

Horizontally

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.horizontally`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (equal horizontal gaps)
```

## layer.distribute.vertically

Vertically

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.distribute.vertically`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (equal vertical gaps)
```

## layer.linkLayers

Link Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.linkLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (toggles: unlinks when the selection is already one link group)
```

## layer.mergeLayers

Merge Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.mergeLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (one layer selected: Merge Down)
```

## layer.new.groupFromLayers

Group from Layers…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.groupFromLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?}
```

## layer.arrange.reverse

Reverse

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.arrange.reverse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.lockLayers

Lock Layers…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.lockLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"transparency":bool?,"pixels":bool?,"position":bool?,"artboard":bool?,"all":bool?} (none given: toggle lock all)
```

## layer.renameLayer

Rename Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.renameLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"name":str}
```

## prefs.get

Get Preferences

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.get`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":"section.key"?=everything (e.g. "performance.historyStates", "colorSettings.workingRgb")}
```

## prefs.set

Set Preferences

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":"section.key","value":json} or {"values":{"section.key":json,…}} (validated; all or nothing)
```

## prefs.reset

Reset Preferences

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe prefs.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":"section|section.key"?=everything}
```

## edit.preferences.general

General…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.general`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.interface

Interface…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.interface`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.workspace

Workspace…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.workspace`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.tools

Tools…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.tools`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.historyLog

History Log…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.historyLog`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.fileHandling

File Handling…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.fileHandling`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.export

Export…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.performance

Performance…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.performance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.scratchDisks

Scratch Disks…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.scratchDisks`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.cursors

Cursors…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.cursors`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.transparencyAndGamut

Transparency & Gamut…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.transparencyAndGamut`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.unitsAndRulers

Units & Rulers…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.unitsAndRulers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.guidesGridAndSlices

Guides, Grid & Slices…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.guidesGridAndSlices`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.plugIns

Plug-ins…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.plugIns`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.type

Type…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.type`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.enhancedControls

Enhanced Controls…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.enhancedControls`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.rawDefaults

Camera Raw…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.rawDefaults`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.preferences.integrations

Integrations…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.preferences.integrations`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.keyboardShortcuts

Keyboard Shortcuts…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.keyboardShortcuts`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"set":{"<command id>":"Cmd+Shift+X"|""(remove)|null(default)}?,"reset":true|["<id>",…]?,"removeConflicts":bool=true,"filter":str?,"list":bool=false}
```

## edit.menus

Menus…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.menus`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"hide":["<id>",…]?,"show":["<id>",…]?,"color":{"<id>":"red|orange|yellow|green|blue|violet|gray|none"}?,"reset":bool=false}
```

## edit.toolbar

Toolbar…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.toolbar`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"hidden":["<tool>",…]?,"order":["<tool>",…]?,"reset":bool=false}
```

## edit.fade

Fade…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.fade`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"opacity":0..100=100,"mode":"normal|multiply|screen|overlay|softLight|hardLight|darken|lighten|difference|color|luminosity"}
```

## edit.purge.undo

Undo

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.purge.undo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.purge.clipboard

Clipboard

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.purge.clipboard`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.purge.histories

Histories

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.purge.histories`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.purge.videoCache

Video Cache

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.purge.videoCache`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.purge.all

All

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.purge.all`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## edit.contentAwareFill

Content-Aware Fill…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.contentAwareFill`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"sampling":"auto|rectangular|custom","margin":px?,"area":[x,y,w,h]?,"channel":index|name?,"colorAdaptation":"default|none|high|veryHigh","rotationAdaptation":"none|low|medium|high|full","scale":bool=false,"mirror":bool=false,"output":"current|new|duplicate","seed":u64=1}
```

## edit.contentAwareScale

Content-Aware Scale

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.contentAwareScale`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":px?,"height":px?,"scaleX":1..400=100,"scaleY":1..400=100,"amount":0..100=100,"protect":"none"|channel index|name,"protectSkinTones":bool=false}
```

## edit.defineBrushPreset

Define Brush Preset…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.defineBrushPreset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":text}
```

## edit.defineCustomShape

Define Custom Shape…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.defineCustomShape`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":text,"path":"work|<saved path name>"?}
```

## edit.findAndReplaceText

Find and Replace Text…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.findAndReplaceText`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"find":text,"replace":text,"action":"changeAll|find|change|changeFind","caseSensitive":bool=false,"wholeWord":bool=false,"forward":bool=true,"allLayers":bool=true}
```

## edit.presets.presetManager

Preset Manager…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.presets.presetManager`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"list|rename|delete|move","kind":"brushes|customShapes|patterns","index":n?,"name":str?,"newName":str?,"to":n?}
```

## edit.presets.exportImportPresets

Export/Import Presets…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.presets.exportImportPresets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"export|import","kinds":["brushes","customShapes"]?,"data":json (import),"includeBuiltins":bool=false}
```

## edit.autoAlignLayers

Auto-Align Layers…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.autoAlignLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"projection":"auto|perspective|cylindrical|spherical|collage|reposition","reference":layer id?=bottom selected layer,"geometricCorrection":bool=false,"interpolation":"bicubic|bilinear|nearest"}
```

## edit.autoBlendLayers

Auto-Blend Layers…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.autoBlendLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"panorama|stack","seamlessTones":bool=true}
```

## file.automate.photomerge

Photomerge…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.photomerge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str]|folder,"useOpenDocuments":bool=false,"layout":"auto|perspective|cylindrical|spherical|collage|reposition","blend":bool=true,"vignetteRemoval":bool=false,"geometricCorrection":bool=false,"contentAwareFill":bool=false,"focalLength":mm=0 (35 mm equivalent; 0 = EXIF or estimated)} → new document, one masked layer per image
```

## file.automate.mergeToHdrPro

Merge to HDR Pro…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.mergeToHdrPro`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"paths":[str]|folder,"useOpenDocuments":bool=false,"exposures":[ev]? (default EXIF, else estimated),"align":bool=true,"removeGhosts":bool=false,"ghostBase":int?,"mode":"32|16|8","method":"localAdaptation|exposureGamma|highlightCompression|equalizeHistogram","radius":1..500=7,"strength":0.1..4=0.52,"gamma":0.1..2=1,"exposure":-5..5=0,"detail":-100..300=30,"shadow":-100..100=0,"highlight":-100..100=0,"vibrance":-100..100=0,"saturation":-100..100=20} → new document (32-bit linear, or tone-mapped 16/8-bit)
```

## file.automate.cropAndStraightenPhotos

Crop and Straighten Photos

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.cropAndStraightenPhotos`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → one new document per photo found on the scan
```

## filter.lensCorrection

Lens Correction…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.lensCorrection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"profile":"none|auto|generic","focalLength":mm=0,"correctDistortion":bool=true,"correctVignette":bool=true,"correctCA":bool=true,"autoScale":bool=false,"distortion":-100..100=0,"redCyan":-100..100=0,"blueYellow":-100..100=0,"vignetteAmount":-100..100=0,"vignetteMidpoint":0..100=50,"vertical":-100..100=0,"horizontal":-100..100=0,"angle":-180..180=0,"scale":50..150=100,"edge":"transparency|edgeExtension|black|white","straighten":[[x,y],[x,y]]?}
```

## filter.adaptiveWideAngle

Adaptive Wide Angle…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.adaptiveWideAngle`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"model":"auto|fisheye|perspective|fullSpherical","focalLength":0..200=0,"cropFactor":0.1..10=1,"scale":50..150=100,"constraints":[{"a":[x,y],"b":[x,y],"orientation":"free|horizontal|vertical"}]}
```

## filter.cameraRaw

Camera Raw Filter…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.cameraRaw`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"temperature":-100..100=0,"tint":-100..100=0,"exposure":-5..5=0,"contrast":-100..100=0,"highlights":-100..100=0,"shadows":-100..100=0,"whites":-100..100=0,"blacks":-100..100=0,"texture":-100..100=0,"clarity":-100..100=0,"dehaze":-100..100=0,"vibrance":-100..100=0,"saturation":-100..100=0,"curveHighlights":-100..100=0,"curveLights":-100..100=0,"curveDarks":-100..100=0,"curveShadows":-100..100=0,"curveSplits":[25,50,75],"pointCurve":[[in,out]],"pointCurveRed":[[in,out]],"pointCurveGreen":[[in,out]],"pointCurveBlue":[[in,out]],"hslHue":[8],"hslSat":[8],"hslLum":[8],"gradeShadows":{"hue":deg,"sat":0..100,"lum":-100..100},"gradeMidtones":{},"gradeHighlights":{},"gradeGlobal":{},"gradeBlending":0..100=50,"gradeBalance":-100..100=0,"sharpenAmount":0..150=0,"sharpenRadius":0.5..3=1,"sharpenDetail":0..100=25,"sharpenMasking":0..100=0,"noiseLuminance":0..100=0,"noiseLuminanceDetail":0..100=50,"noiseColor":0..100=0,"noiseColorDetail":0..100=50,"grainAmount":0..100=0,"grainSize":0..100=25,"grainRoughness":0..100=50,"vignetteAmount":-100..100=0,"vignetteMidpoint":0..100=50,"vignetteRoundness":-100..100=0,"vignetteFeather":0..100=50,"vignetteHighlights":0..100=0,"vignetteStyle":"highlightPriority|colorPriority|paintOverlay","seed":u32=0}
```

## file.automate.lensCorrection

Lens Correction…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.lensCorrection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"input":folder|[files],"output":folder,"format":"same|jpg|png|tif|psd","quality":0..12?, …Filter › Lens Correction params ("profile" defaults to "auto")}
```

## filter.vanishingPoint

Vanishing Point…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.vanishingPoint`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"planes":[{"corners":[[x,y]×4]} | {"from":plane,"edge":"top|right|bottom|left","angle":deg=90,"depth":1}],"focalLength":px=0,"paste":[{"plane":0,"layer":id? (else the clipboard),"at":[u,v]=[0.25,0.25],"width":0..1=0.5}],"clone":[{"source":[x,y],"points":[[x,y]],"size":px=40,"hardness":0..100=50,"opacity":0..100=100}],"newLayer":bool=false}
```

## select.saveSelection

Save Selection…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.saveSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"channel":"new"|index|name="new","document":index?,"operation":"new|replace|add|subtract|intersect"="new"}
```

## select.loadSelection

Load Selection…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.loadSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name|"composite"|"red|green|blue|…"|"transparency"|"mask"|"quickMask"|"selection","layer":id?,"document":index?,"invert":bool=false,"operation":"new|add|subtract|intersect"="new"}
```

## select.editInQuickMaskMode

Edit in Quick Mask Mode

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.editInQuickMaskMode`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool?=toggle}
```

## image.applyImage

Apply Image…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.applyImage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"source":{"document":index?,"layer":id|"merged"="merged","channel":"composite"|"red|…"|index|"selection"|"transparency"|"mask"="composite","invert":bool=false},"blending":"normal|multiply|screen|overlay|softLight|hardLight|colorDodge|colorBurn|darken|lighten|difference|exclusion|linearBurn|linearDodge|add|subtract|…"="multiply","opacity":0..100=100,"scale":1..2=1,"offset":-255..255=0,"preserveTransparency":bool=false,"mask":{"document","layer","channel","invert"}?,"sourceChannel|sourceDocument|sourceLayer|sourceInvert|maskChannel|…":flat form of source/mask?}
```

## image.calculations

Calculations…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.calculations`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"source1":{"document","layer","channel","invert"},"source2":{…},"blending":"multiply|…"="multiply","opacity":0..100=100,"scale":1..2=1,"offset":-255..255=0,"mask":{…}?,"result":"newChannel|newDocument|selection"="newChannel","name":str?}
```

## channel.new

New Channel…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"fill":"black|white|selection"="black","color":"#rrggbb"="#ff0000","opacity":0..100=50,"indicates":"masked|selected"="masked"}
```

## channel.newSpot

New Spot Channel…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.newSpot`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"color":"#rrggbb"="#ff0000","solidity":0..100=0,"fromSelection":bool=true}
```

## channel.duplicate

Duplicate Channel…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name|"red|…"|"composite"|"quickMask","name":str?,"document":index|"new"?=active,"invert":bool=false}
```

## channel.delete

Delete Channel

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name?=targeted}
```

## channel.rename

Rename Channel

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name,"name":str}
```

## channel.move

Reorder Channel

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name,"to":index}
```

## channel.target

Target Channel

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":"composite"|"red|green|blue|…"|index|name="composite"}
```

## channel.setVisible

Channel Visibility

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.setVisible`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":"composite"|"red|…"|index|name|"quickMask","visible":bool?=toggle}
```

## channel.options

Channel Options…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.options`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name|"quickMask","name":str?,"indicates":"masked|selected|spot"?,"color":"#rrggbb"?,"opacity":0..100?,"solidity":0..100?}
```

## channel.mergeSpot

Merge Spot Channel

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.mergeSpot`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"channel":index|name?=targeted or first spot}
```

## channel.split

Split Channels

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.split`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"closeOriginal":bool=true}
```

## channel.merge

Merge Channels…

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.merge`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"mode":"rgb|cmyk|lab"="rgb","documents":[index,…]?=open grayscale docs of the active size,"name":str?}
```

## channel.list

Channels

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.composite

Target Composite Channel

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.composite`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot3

Target Channel 3

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot3`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot4

Target Channel 4

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot4`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot5

Target Channel 5

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot5`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot6

Target Channel 6

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot6`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot7

Target Channel 7

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot7`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot8

Target Channel 8

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot8`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## channel.target.slot9

Target Channel 9

- 技能 / Owner: `photocraft-cli-selection`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-selection`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe channel.target.slot9`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## image.adjustments.shadowsHighlights

Shadows/Highlights…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.shadowsHighlights`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"shadowAmount":0..100=35,"shadowTone":0..100=50,"shadowRadius":0..2500=30,"highlightAmount":0..100=0,"highlightTone":0..100=50,"highlightRadius":0..2500=30,"color":-100..100=20,"midtone":-100..100=0,"blackClip":0..50=0.01,"whiteClip":0..50=0.01}
```

## image.adjustments.replaceColor

Replace Color…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.replaceColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"color":json,"fuzziness":0..200=40,"hue":-180..180=0,"saturation":-100..100=0,"lightness":-100..100=0} (color: "#rrggbb", default the foreground colour)
```

## image.adjustments.matchColor

Match Color…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.matchColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"source":doc,"sourceLayer":json,"luminance":1..200=100,"intensity":1..200=100,"fade":0..100=0,"neutralize":bool=false,"useSelectionInSource":bool=false,"useSelectionInTarget":bool=false} (source: document index; sourceLayer: layer id, default the merged image)
```

## image.adjustments.hdrToning

HDR Toning…

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.hdrToning`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"radius":1..500=30,"strength":0.1..4=0.5,"gamma":0.1..2=1,"exposure":-5..5=0,"detail":-100..300=30,"shadow":-100..100=0,"highlight":-100..100=0,"vibrance":-100..100=0,"saturation":-100..100=20,"curve":[[in,out],…] 0..255} (flattens the image)
```

## image.adjustments.colorLookup.list

List Color Lookup Looks

- 技能 / Owner: `photocraft-cli-adjustments`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.adjustments.colorLookup.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.layerMask.apply

Apply

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerMask.fromTransparency

From Transparency

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.fromTransparency`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerMask.hideSelection

Hide Selection

- 技能 / Owner: `photocraft-cli-masks`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-masks`。
- 当前工作流映射 / Workflow mapped: true。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerMask.hideSelection`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.maskAllObjects

Mask All Objects

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.maskAllObjects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.matting.defringe

Defringe…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.matting.defringe`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"width":1..200=1}
```

## layer.matting.removeBlackMatte

Remove Black Matte

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.matting.removeBlackMatte`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.matting.removeWhiteMatte

Remove White Matte

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.matting.removeWhiteMatte`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.matting.colorDecontaminate

Color Decontaminate…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.matting.colorDecontaminate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"amount":0..100=100,"radius":1..100=4}
```

## layer.smartObjects.stackMode.entropy

Entropy

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.entropy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.kurtosis

Kurtosis

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.kurtosis`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.maximum

Maximum

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.maximum`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.mean

Mean

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.mean`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.median

Median

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.median`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.minimum

Minimum

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.minimum`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.range

Range

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.range`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.skewness

Skewness

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.skewness`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.standardDeviation

Standard Deviation

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.standardDeviation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.summation

Summation

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.summation`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.variance

Variance

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.variance`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.stackMode.none

None

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.stackMode.none`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.smartObjects.revealInFinder

Reveal in Finder

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.revealInFinder`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"dryRun":bool=false}
```

## layer.layerStyle.blendingOptions

Blending Options…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.blendingOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"blend":"normal|multiply|…"?,"opacity":0..100?,"fillOpacity":0..100?,"blendIf":{"channel":"gray|red|green|blue|cyan|…"|index="gray","thisLayer":[black,white]|[blackLo,blackHi,whiteLo,whiteHi]?,"underlying":[…]?}|[{…},…]|null?} (Blend If values 0..255; split points fade; null resets)
```

## layer.layerStyle.globalLight

Global Light…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.globalLight`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"angle":-180..180=120,"altitude":0..90=30}
```

## layer.layerStyle.createLayer

Create Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.createLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?}
```

## layer.layerStyle.scaleEffects

Scale Effects…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerStyle.scaleEffects`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"scale":1..1000=100}
```

## layer.layerContentOptions

Layer Content Options…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.layerContentOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layer.quickExportAsPng

Quick Export as PNG

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.quickExportAsPng`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":text}
```

## layer.exportAs

Export As…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.exportAs`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"path":text,"scale":1..1000=100} (format from the path's extension)
```

## image.rotation.arbitrary

Arbitrary…

- 技能 / Owner: `photocraft-cli-resize`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.rotation.arbitrary`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"angle":-359.99..359.99=0,"direction":"cw|ccw"="cw","interpolation":"bicubic|bilinear|nearest"="bicubic"}
```

## image.mode.indexedColor

Indexed Color…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.indexedColor`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"palette":"selective|perceptual|adaptive|exact|systemMac|systemWindows|web|uniform"="selective","colors":2..256=256,"forced":"blackWhite|none|primaries|web"="blackWhite","transparency":bool=true,"dither":"diffusion|none|pattern|noise"="diffusion","amount":0..100=75} (flattens)
```

## image.mode.colorTable

Color Table…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.colorTable`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"table":"custom|blackBody|grayscale|spectrum|systemMac|systemWindows|web"="custom","colors":json,"entries":json,"transparent":json} (colors: ["#rrggbb", …]; entries: {"index": "#rrggbb"}; transparent: index|null)
```

## image.mode.bitmap

Bitmap…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.bitmap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"diffusion|threshold|pattern|halftone"="diffusion","frequency":1..999=53,"angle":-180..180=45,"shape":"round|ellipse|line|square|diamond|cross"="round"} (halftone frequency in lines/inch; flattens)
```

## image.mode.duotone

Duotone…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.duotone`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"type":"duotone|monotone|tritone|quadtone"="duotone","inks":json} (inks: [{"name","color":"#rrggbb","curve":[[in,out],…] in 0..100}, …])
```

## image.mode.multichannel

Multichannel

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.multichannel`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (flattens; RGB → Cyan/Magenta/Yellow, CMYK → Cyan/Magenta/Yellow/Black, Lab → Alpha 1–3, Grayscale → Black, Duotone → its inks)
```

## edit.definePattern

Define Pattern…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.definePattern`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"rect":[x0,y0,x1,y1]? (default: selection bounds, else the canvas)} → {"pattern":id} (added to the library; samples the visible composite)
```

## pattern.list

Patterns

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → [{id,name,width,height,mode,depth,inDocument,inLibrary}]
```

## pattern.rename

Rename Pattern

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name,"name":str}
```

## pattern.delete

Delete Pattern

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name} (library only; documents keep their copy)
```

## pattern.import

Import Patterns…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.import`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":".pat file"}
```

## pattern.export

Export Patterns…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":".pat file","patterns":[id|name]? (default: the whole library)}
```

## layer.newFillLayer.pattern

Pattern…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newFillLayer.pattern`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name?=first library pattern,"scale":1..1000=100,"angle":deg=0,"link":bool=true,"phase":[x,y]?}
```

## brush.texturePattern

Brush Texture Pattern

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.texturePattern`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name,"scale":1..1000?,"enabled":bool=true} (sets the session brush's Texture to that pattern)
```

## edit.transform.warp

Warp

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.warp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"rect":[x0,y0,x1,y1]? (warp box; default = layer content ∩ selection),"style":"custom|none|arc|arcLower|arcUpper|arch|bulge|shellLower|shellUpper|flag|wave|fish|rise|fisheye|inflate|squeeze|twist","bend":%=50,"hDistort":%,"vDistort":%,"vertical":bool,"mesh":{"us":[0,…,1],"vs":[0,…,1],"points":[[x,y]…]} ((3c+1)×(3r+1) control points, row-major, document px),"grid":[cols,rows]?,"warp":{full warp object}?,"interpolation":"bicubic|bilinear|nearest"}
```

## layer.smartObjects.warp

Warp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.warp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"rect":[x0,y0,x1,y1]? (warp box; default = layer content ∩ selection),"style":"custom|none|arc|arcLower|arcUpper|arch|bulge|shellLower|shellUpper|flag|wave|fish|rise|fisheye|inflate|squeeze|twist","bend":%=50,"hDistort":%,"vDistort":%,"vertical":bool,"mesh":{"us":[0,…,1],"vs":[0,…,1],"points":[[x,y]…]} ((3c+1)×(3r+1) control points, row-major, document px),"grid":[cols,rows]?,"warp":{full warp object}?,"interpolation":"bicubic|bilinear|nearest"}
```

## edit.transform.splitWarpCrosswise

Split Warp Crosswise

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.splitWarpCrosswise`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"warp":{…}? (the warp being edited; returned split),"rect":[x0,y0,x1,y1]?,"at":[x,y]? (document point; default = middle of the patch)} — without `warp`, edits the active smart object's warp
```

## edit.transform.splitWarpHorizontally

Split Warp Horizontally

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.splitWarpHorizontally`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"warp":{…}? (the warp being edited; returned split),"rect":[x0,y0,x1,y1]?,"at":[x,y]? (document point; default = middle of the patch)} — without `warp`, edits the active smart object's warp
```

## edit.transform.splitWarpVertically

Split Warp Vertically

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.splitWarpVertically`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"warp":{…}? (the warp being edited; returned split),"rect":[x0,y0,x1,y1]?,"at":[x,y]? (document point; default = middle of the patch)} — without `warp`, edits the active smart object's warp
```

## edit.transform.removeWarpSplit

Remove Warp Split

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.transform.removeWarpSplit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"warp":{…}? (the warp being edited; returned split),"rect":[x0,y0,x1,y1]?,"at":[x,y]? (document point; default = middle of the patch)} — without `warp`, edits the active smart object's warp
```

## layerComp.new

New Layer Comp…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str="Layer Comp N","comment":str="","visibility":bool=true,"position":bool=true,"appearance":bool=true} → {comp}
```

## layerComp.update

Update Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.update`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name|"*"? (default: last applied; "*" = all),"what":"all|visibility|position|appearance"="all"}
```

## layerComp.apply

Apply Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name? (default: last applied)} → {comp, missingLayers}
```

## layerComp.previous

Apply Previous Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.previous`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layerComp.next

Apply Next Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.next`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layerComp.delete

Delete Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name?}
```

## layerComp.duplicate

Duplicate Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.duplicate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name?} → {comp}
```

## layerComp.rename

Rename Layer Comp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name?,"name":str}
```

## layerComp.setComment

Layer Comp Comment

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.setComment`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name?,"comment":str}
```

## layerComp.setOptions

Layer Comp Options…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.setOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"comp":id|name?,"visibility":bool?,"position":bool?,"appearance":bool?,"name":str?,"comment":str?}
```

## layerComp.restoreLastDocumentState

Restore Last Document State

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.restoreLastDocumentState`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## layerComp.updateWarnings

Layer Comp Warnings

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.updateWarnings`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"clear":bool=false (drop states of deleted layers)} → {warnings:[{comp,name,missingLayers}],count}
```

## layerComp.list

List Layer Comps

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layerComp.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {comps:[{id,name,comment,visibility,position,appearance,layers,missingLayers}],lastApplied,hasLastDocumentState}
```

## file.export.layerCompsToFiles

Layer Comps to Files…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.layerCompsToFiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"dir":folder,"format":"png|jpg|psd|tiff|…"="png","prefix":str=document name,"selectedOnly":bool=false (only the last applied comp),"comps":[id]?,"quality":0..12?} → {files}
```

## layer.new.artboard

Artboard…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.artboard`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"rect":[x,y,w,h]? | "x","y","width","height"? (default: canvas size, right of the last board),"preset":"iPhone 14|Web 1920|A4|…"?,"name":str?,"background":"white|black|transparent|custom"="white","color":[r,g,b]|"#rrggbb"? (custom)} → {layer, rect}
```

## layer.new.artboardFromGroup

Artboard from Group…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.artboardFromGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id? (a top-level group; default active),"background":…?} → {layer, rect}
```

## layer.new.artboardFromLayers

Artboard from Layers…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.artboardFromLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"background":…?} (the selected layers) → {layer, rect}
```

## layer.artboard.set

Edit Artboard

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.artboard.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id? (default: the active artboard),"x","y","width","height"?|"rect":[x,y,w,h]?,"preset":str?,"background":"white|black|transparent|custom"?,"color":…?,"name":str?,"moveContents":bool=true} → {layer, rect}
```

## view.clearSelectedArtboardGuides

Clear Selected Artboard Guides

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.clearSelectedArtboardGuides`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (guides inside the active artboard)
```

## file.export.artboardsToFiles

Artboards to Files…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.artboardsToFiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"dir":folder,"format":"png|jpg|psd|tiff|…"="png","prefix":str=document name ("" = none),"artboards":[id]? (default all),"quality":0..12?} → {files}
```

## file.export.artboardsToPdf

Artboards to PDF…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.artboardsToPdf`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str (.pdf),"artboards":[id]?,"quality":0..12=10} → {path, pages} (one raster page per board)
```

## filter.liquify

Liquify…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.liquify`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"strokes":[{"tool":"forwardWarp|reconstruct|smooth|twirlCw|twirlCcw|pucker|bloat|pushLeft|freeze|thaw|reconstructAll","size":px=100,"density":0-100=50,"pressure":0-100=100,"rate":0-100=80,"points":[[x,y,pressure?]…],"amount":%? (reconstructAll)}…],"meshSize":px? (field resolution, px per node; default 2, or 4 above 4 MP),"layer":id?} — strokes replay in order on a fresh field; a selection limits the effect; on a smart object it becomes a smart filter
```

## edit.puppetWarp

Puppet Warp

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.puppetWarp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pins":[{"src":[x,y],"dst":[x,y],"rotate":deg?,"depth":n?}…],"mode":"rigid|normal|distort"="normal","density":"fewer|normal|more"="normal","expansion":px=2,"interpolation":"bicubic|bilinear|nearest","layer":id?} — mesh over the opaque region, as-rigid-as-possible; on a smart object it becomes a smart filter
```

## layer.smartObjects.puppetWarp

Puppet Warp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.puppetWarp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pins":[{"src":[x,y],"dst":[x,y],"rotate":deg?,"depth":n?}…],"mode":"rigid|normal|distort"="normal","density":"fewer|normal|more"="normal","expansion":px=2,"interpolation":"bicubic|bilinear|nearest","layer":id?} — mesh over the opaque region, as-rigid-as-possible; on a smart object it becomes a smart filter
```

## edit.perspectiveWarp

Perspective Warp

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.perspectiveWarp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"planes":[{"src":[[x,y]×4],"dst":[[x,y]×4]}…] (corners clockwise from top-left; corners that coincide in src are linked),"straighten":"horizontal|vertical|auto"?,"interpolation":"bicubic|bilinear|nearest","layer":id?}
```

## layer.smartObjects.perspectiveWarp

Perspective Warp

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.smartObjects.perspectiveWarp`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"planes":[{"src":[[x,y]×4],"dst":[[x,y]×4]}…] (corners clockwise from top-left; corners that coincide in src are linked),"straighten":"horizontal|vertical|auto"?,"interpolation":"bicubic|bilinear|nearest","layer":id?}
```

## image.analysis.setMeasurementScale

Set Measurement Scale…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.setMeasurementScale`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":"default|custom"="custom","pixelLength":px,"logicalLength":number,"units":str (e.g. "mm")} (no params: read the scale)
```

## image.analysis.selectDataPoints

Select Data Points…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.selectDataPoints`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"selection":[keys]|{key:bool}?,"ruler":[keys]|{key:bool}?,"count":[keys]|{key:bool}?,"reset":bool=false} (keys: label,dateTime,document,source,scale,scaleUnits,scaleFactor,count,area,perimeter,circularity,height,width,grayMin,grayMax,grayMean,grayMedian,integratedDensity,histogram,length,angle)
```

## image.analysis.recordMeasurements

Record Measurements

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.recordMeasurements`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"source":"auto|selection|ruler|count"="auto"} → appended Measurement Log rows (selection: summary + one row per feature)
```

## image.analysis.rulerTool

Ruler Tool

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.rulerTool`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"start":[x,y],"end":[x,y],"protractor":[x,y]|null?,"clear":bool=false} (no params: read) → X/Y/W/H/angle/L1/L2
```

## image.analysis.countTool

Count Tool

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.countTool`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → count groups and markers (edit with count.*)
```

## image.analysis.placeScaleMarker

Place Scale Marker…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.placeScaleMarker`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"length":logical units=nice ≈ width/5,"font":str?,"fontSize":pt=12,"displayText":bool=true,"textPosition":"top|bottom"="bottom","color":"black|white"="black"}
```

## image.analysis.straightenLayer

Straighten Layer

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.straightenLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"crop":bool=(active layer is the Background)} (rotates so the ruler line is level; crop = rotate the canvas and crop to the image)
```

## image.analysis.info

Analysis Info

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.analysis.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → scale, ruler readout, count groups, note and log counts
```

## count.add

Add Count

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"group":index?}
```

## count.remove

Remove Count

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":n,"group":index?} | {"x":px,"y":px,"radius":px=6}
```

## count.move

Move Count

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":n,"group":index?,"to":[x,y]} | {"x":px,"y":px,"to":[x,y]}
```

## count.clear

Clear Count

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.clear`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"group":index|"all"=active}
```

## count.newGroup

New Count Group

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.newGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"color":"#rrggbb"|[r,g,b]?}
```

## count.deleteGroup

Delete Count Group

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.deleteGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"group":index=active}
```

## count.setGroup

Count Group Options

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe count.setGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"group":index=active,"name":str?,"color":"#rrggbb"|[r,g,b]?,"markerSize":1..10?,"labelSize":8..72?,"visible":bool?,"active":bool?}
```

## measurementLog.list

Measurement Log

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe measurementLog.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → rows and columns
```

## measurementLog.delete

Delete Measurements

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe measurementLog.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"rows":[ids]}|{"all":true}
```

## measurementLog.export

Export Measurements…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe measurementLog.export`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str? (CSV file; omitted → returns the CSV text),"rows":[ids]?}
```

## notes.add

New Note

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe notes.add`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"text":str="","author":str="","color":"#rrggbb"|[r,g,b]=pale yellow,"open":bool=true}
```

## notes.set

Edit Note

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe notes.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":n,"text":str?,"author":str?,"color":"#rrggbb"|[r,g,b]?,"x":px?,"y":px?,"open":bool?}
```

## notes.delete

Delete Note

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe notes.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":n}|{"all":true}
```

## notes.list

Notes

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe notes.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → notes (index, author, text, colour, position, open, modified)
```

## file.import.notes

Notes…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.import.notes`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":".psd|.psb|.pcraft with notes"}
```

## view.proofSetup.workingCyanPlate

Working Cyan Plate

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.workingCyanPlate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.workingMagentaPlate

Working Magenta Plate

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.workingMagentaPlate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.workingYellowPlate

Working Yellow Plate

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.workingYellowPlate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.workingBlackPlate

Working Black Plate

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.workingBlackPlate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.workingCmyPlate

Working CMY Plate

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.workingCmyPlate`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.legacyMacintoshRgb

Legacy Macintosh RGB

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.legacyMacintoshRgb`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.colorBlindnessProtanopia

Color Blindness — Protanopia-type

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.colorBlindnessProtanopia`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.proofSetup.colorBlindnessDeuteranopia

Color Blindness — Deuteranopia-type

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.proofSetup.colorBlindnessDeuteranopia`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (sets the proof and turns Proof Colors on)
```

## view.thirtyTwoBitPreviewOptions

32-bit Preview Options…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.thirtyTwoBitPreviewOptions`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"method":"exposureGamma|highlightCompression"="exposureGamma","exposure":-20..20=0,"gamma":0.1..9.99=1}
```

## gradient.presets.list

Gradient Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {groups:[{name,presets:[{name,stops,transparency}]}],current}
```

## gradient.presets.select

Select Gradient

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":name|"stops":[[t 0..1,"#rrggbb"|"foreground"|"background"],…],"transparency":[[t,opacity 0..100],…]?,"group":name?,"applyToLayer":bool=true (also recolours a selected Gradient Fill layer)} → {current,layer?}. The Gradient tool paints with it.
```

## gradient.presets.apply

New Gradient Fill Layer from Preset

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":name?=current|"stops":[[t 0..1,"#rrggbb"|"foreground"|"background"],…],"transparency":[[t,opacity 0..100],…]?,"angle":deg=90,"style":"linear|radial|angle|reflected|diamond"="linear","scale":10..150=100,"reverse":bool} → {layer}
```

## gradient.presets.new

New Gradient Preset

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str="Custom","group":name?=first,"stops":[[t 0..1,"#rrggbb"|"foreground"|"background"],…],"transparency":[[t,opacity 0..100],…]? (default: the current gradient)}
```

## gradient.presets.edit

Edit Gradient Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"rename|delete|move|newGroup|renameGroup|deleteGroup","preset":name|[names] (rename/delete/move),"group":name? (narrows the lookup; the group for renameGroup/deleteGroup),"name":str (rename: new name; newGroup/renameGroup: group name),"to":group (move),"index":n? (move)}
```

## gradient.presets.reset

Restore Default Gradients

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe gradient.presets.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"append":bool=false}
```

## pattern.presets.list

Pattern Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {groups:[{name,patterns:[{id,name,width,height}]}],current}
```

## pattern.presets.select

Select Pattern

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.presets.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name,"applyToLayer":bool=true (also changes a selected Pattern Fill layer)} (Fill and new Pattern Fill layers default to it)
```

## pattern.presets.apply

New Pattern Fill Layer from Preset

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.presets.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"pattern":id|name?=selected,"scale":1..1000=100,"angle":deg=0} → {layer}
```

## pattern.presets.new

New Pattern Preset

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.presets.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?,"group":name?,"rect":[x0,y0,x1,y1]?} (Define Pattern from the selection/canvas into a group)
```

## pattern.presets.edit

Edit Pattern Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe pattern.presets.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"rename|delete|move|newGroup|renameGroup|deleteGroup","preset":name|[names] (rename/delete/move),"group":name? (narrows the lookup; the group for renameGroup/deleteGroup),"name":str (rename: new name; newGroup/renameGroup: group name),"to":group (move),"index":n? (move)}
```

## style.presets.list

Style Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe style.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {groups:[{name,presets:[{name,effects,blend,fillOpacity}]}]}
```

## style.presets.apply

Apply Style

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe style.presets.apply`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":name,"group":name?,"layers":[ids]?|"layer":id? (default: the selected layers),"add":bool=false (⇧-click: add to the existing effects)} → {layers,style}
```

## style.presets.new

New Style…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe style.presets.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str="Style","group":name?,"layer":id?,"includeEffects":bool=true,"includeBlending":bool=true} (from the layer's effects)
```

## style.presets.edit

Edit Style Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe style.presets.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"rename|delete|move|newGroup|renameGroup|deleteGroup","preset":name|[names] (rename/delete/move),"group":name? (narrows the lookup; the group for renameGroup/deleteGroup),"name":str (rename: new name; newGroup/renameGroup: group name),"to":group (move),"index":n? (move)}
```

## style.presets.reset

Restore Default Styles

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe style.presets.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"append":bool=false}
```

## shape.presets.list

Shape Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {groups:[{name,shapes:[{name,subpaths}]}]}
```

## shape.presets.place

Place Custom Shape

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.presets.place`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":name,"group":name?,"rect":[x,y,w,h]? (default: centred, half the canvas),"keepAspect":bool=true,"fill":…?=foreground,"stroke":…?,"name":str?,"addTo":layerId?,"op":"combine|subtract|intersect|exclude"?} → shape.info (Custom Shape tool / Shapes panel; fill and stroke as in shape.create)
```

## shape.presets.new

New Shape Preset

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.presets.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str="Shape","group":name?,"path":{…path}|"M x y L …" (preset path language)|"work"|saved path name? (default: work path, active shape layer or vector mask)}
```

## shape.presets.edit

Edit Shape Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.presets.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"rename|delete|move|newGroup|renameGroup|deleteGroup","preset":name|[names] (rename/delete/move),"group":name? (narrows the lookup; the group for renameGroup/deleteGroup),"name":str (rename: new name; newGroup/renameGroup: group name),"to":group (move),"index":n? (move)}
```

## shape.presets.reset

Restore Default Shapes

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe shape.presets.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"append":bool=false}
```

## tool.presets.list

Tool Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tool.presets.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"tool":name? (Current Tool Only)} → {presets:[{name,tool}]}
```

## tool.presets.new

New Tool Preset…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tool.presets.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?=tool,"tool":name,"options":{…}? (opaque; "brush" defaults to the current brush for painting tools),"includeColor":bool=false}
```

## tool.presets.select

Select Tool Preset

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tool.presets.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":name} → {name,tool,options} (applies "brush" and "foreground"; the shell switches tool and options)
```

## tool.presets.edit

Edit Tool Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tool.presets.edit`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"action":"rename|delete","preset":name|[names],"name":str (rename)}
```

## tool.presets.reset

Reset Tool Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe tool.presets.reset`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## cloneSource.list

Clone Sources

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe cloneSource.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {active,sources:[{index,source,anchor,offset,layer,width,height,rotation,flipH,flipV}],overlay}
```

## cloneSource.select

Select Clone Source

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe cloneSource.select`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":0..4}
```

## cloneSource.set

Set Clone Source

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe cloneSource.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":0..4?=active,"source":[x,y]? (⌥-click; re-pairs with the next stroke),"offset":[dx,dy]?,"width":%?,"height":%?|"scale":[w%,h%]?,"rotation":deg?,"flipH":bool?,"flipV":bool?,"layer":id?,"clear":bool?,"select":bool=true}
```

## cloneSource.resetTransform

Reset Transform

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe cloneSource.resetTransform`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"index":0..4?=active}
```

## cloneSource.overlay

Clone Source Overlay

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe cloneSource.overlay`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"show":bool?,"opacity":0..100?,"clipped":bool?,"autoHide":bool?,"invert":bool?,"blend":"normal|darken|lighten|difference"?}
```

## filter.render.flame

Flame…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.flame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"flameType":"oneFlameAlongPath|multipleFlamesAlongPath|multipleFlamesPathDirections|multipleFlamesVariousLength|candleLight|multipleFlamesOneDirection","length":1..1000=150,"randomizeLength":bool,"width":1..1000=40,"angle":-180..180=0,"interval":1..1000=60,"adjustIntervalForLoops":bool=true,"useCustomColor":bool,"color":color,"turbulent":0..100=25,"jag":0..100=25,"opacity":0..100=75,"flameLines":1..100=20,"flameBottomAlignment":0..100=20,"flameStyle":"normal|violent|flat","flameShape":"parallel|toCenter|spread|oval|pointed","randomizeShapes":bool,"seed":u32=0,"quality":"draft|low|medium|high|fine","path":text,"newLayer":bool} → {layer,newLayer,bounds,primitives,usedPath}
```

## filter.render.pictureFrame

Picture Frame…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.pictureFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"frame":"vineWithFlowers|vineWithLeaves|ivy|roses|daisies|berries|bamboo|waves|zigzag|dots|rope|scallops|doubleLine|snowflakes|stars|hearts","margin":0..30=4,"size":1..100=50,"arrangement":1..100=50,"lines":1..5=1,"thickness":1..100=30,"fade":0..100=0,"vineColor":color,"flowerColor":color,"leafColor":color,"seed":u32=0,"newLayer":bool} → {layer,newLayer,bounds,primitives,frame}
```

## filter.render.tree

Tree…

- 技能 / Owner: `photocraft-cli-filters`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-filters`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.render.tree`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"baseTreeType":1..34=1,"lightDirection":1..5=3,"leavesAmount":0..100=50,"leavesSize":0..200=100,"branchesHeight":50..300=100,"branchesThickness":50..200=100,"defaultLeaves":bool=true,"leavesColor":color,"customBranchColor":bool,"branchesColor":color,"flatShading":bool,"seed":u32=0,"x":0..1=0.5,"y":0..1=0.95,"size":0.05..2=0.8,"newLayer":bool} → {layer,newLayer,bounds,primitives,treeType}
```

## slice.new

Slice Tool

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.new`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"rect":[x,y,w,h] | "x","y","width","height", plus Slice Options ("name","kind":"image|noImage|table","url","target","message","alt","cellText","cellTextIsHtml","background":"none|#rrggbb")?} → {slice, number}
```

## slice.fromGuides

Slices From Guides

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.fromGuides`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (replaces every slice by the grid of the canvas guides) → {slices}
```

## slice.set

Slice Options…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.set`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slice":id | "number":n (an auto slice is promoted), "name"?,"kind":"image|noImage|table"?,"url"?,"target"?,"message"?,"alt"?,"cellText"?,"cellTextIsHtml"?,"horizontalAlign":0..4?,"verticalAlign":0..4?,"background":"none|#rrggbb"?,"outsets":[t,l,b,r]? (layer slices),"rect":[x,y,w,h]? (move/resize; a layer slice becomes a user slice)} → the slice
```

## slice.promote

Promote

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.promote`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slice":id | "number":n} (auto or layer-based → user slice) → {slice}
```

## slice.delete

Delete Slice

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slice":id | "number":n | "slices":[id…]} → {deleted}
```

## slice.divide

Divide Slice…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.divide`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"slice":id | "number":n,"horizontal":n=1 (slices down),"vertical":n=1 (slices across)} → {slices}
```

## slice.list

List Slices

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe slice.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {slices:[{number,id,origin:auto|layer|user,name,rect:[x,y,w,h],kind,layer,url,alt,…}], locked}
```

## layer.newLayerBasedSlice

New Layer Based Slice

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.newLayerBasedSlice`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"name":str?,"url":str?,"alt":str?} (follows the layer's bounds with effects) → {slice, rect}
```

## view.lockSlices

Lock Slices

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.lockSlices`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool? (default: toggle)} → {locked}
```

## view.clearSlices

Clear Slices

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe view.clearSlices`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (deletes every user and layer-based slice) → {cleared}
```

## file.export.saveForWebLegacy

Save for Web (Legacy)…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.saveForWebLegacy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"preset":"GIF 128 Dithered|JPEG High|PNG-24|…"?,"format":"gif|png8|png24|jpeg|wbmp"="png24","palette":"perceptual|selective|adaptive|restrictive|exact|systemMac|systemWindows|uniform"="selective","colors":2..256=256,"dither":"none|diffusion|pattern|noise"="diffusion","ditherAmount":0..100=88,"transparency":bool=true,"matte":"#rrggbb|none"="#ffffff","interlaced":bool=false,"webSnap":0..100=0,"quality":0..100=60,"progressive":bool=false,"optimized":bool=true,"embedIcc":bool=false,"metadata":"none|copyright|copyrightAndContact|all"="copyright","convertToSrgb":bool=true,"width"|"height"|"percent"? (image size),"resample":"bicubic|bilinear|nearest"?,"path":file? (whole image),"dir":folder? (one file per slice in images/),"html":bool=false,"slices":"all|user"="all","numbers":[n]?} → no path/dir: {bytes,width,height,colors} estimate; else {files, html, bytes}
```

## file.export.exportPreferences

Export Preferences…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.exportPreferences`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"quickExportFormat":"png|jpg|gif|webp"?,"quickExportLocation":"ask|sameFolder"?,"jpegQuality":1..100?,"metadata":"none|copyright|all"?,"convertToSrgb":bool?} → {values}
```

## file.export.quickExport

Quick Export

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.quickExport`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str? (required unless Export Preferences › Location is "sameFolder" and the document is saved)} → {path, format, bytes}
```

## file.generate.imageAssets

Image Assets

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.generate.imageAssets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"on":bool? (default: toggle),"dir":folder? (default <document>-assets next to the file)} → {enabled, files, errors}; layers named like "foo.png", "200% foo@2x.png", "48x48 icons/a.png8", "photo.jpg80%" are exported, now and after each save
```

## file.automate.contactSheetII

Contact Sheet II…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.contactSheetII`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"input":folder|[paths],"units":"inches|cm|mm|pixels"="inches","width":8,"height":10,"resolution":ppi=300,"mode":"rgb|gray|cmyk|lab"="rgb","depth":8|16=8,"columns":5,"rows":6,"placeAcrossFirst":bool=true,"autoSpacing":bool=true,"horizontal":units?,"vertical":units?,"rotateForBestFit":bool=false,"caption":bool=true (file name as caption),"font":family?,"fontSize":pt=12,"flatten":bool=false} → {documents, pages, images}
```

## file.automate.createDroplet

Create Droplet…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.createDroplet`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str (.pcdroplet),"steps":[[id,params]…] (the action),"name":str?,"output":folder?,"format":"same|png|jpg|…"?,"quality":0..12?,"shim":bool=true on Unix (writes <name>.command calling `photocraft-cli droplet`)} → {path, shim}
```

## file.automate.runDroplet

Run Droplet

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.automate.runDroplet`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"droplet":path,"input":[files or folders],"output":folder? (default: droplet's, else <input folder>/droplet-output)} → {files, errors}
```

## file.scripts.statistics

Statistics…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.statistics`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"mode":"mean|median|maximum|minimum|range|summation|variance|standardDeviation|skewness|kurtosis|entropy"="median","input":folder|[paths],"align":bool=false (Auto-Align first)} → new document with one stack-mode smart object
```

## file.scripts.browse

Browse…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.browse`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":script file | "script":text | "steps":[[id,params]…]} (JSON action, or one `command.id {json}` per line) → {steps, ok, results}
```

## file.scripts.scriptEventsManager

Script Events Manager…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.scripts.scriptEventsManager`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"enabled":bool?,"add":{"event":"startApplication|newDocument|openDocument|saveDocument|closeDocument|print|export|everything","script":path?|"steps":[…]?,"name":str?}?,"remove":index?,"removeAll":bool?} → {enabled, bindings, events}
```

## file.print

Print…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.print`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"printer":name? (default printer),"copies":1..999=1,"paper":"letter|legal|tabloid|a3|a4|a5|4x6|5x7"|[w,h] pt="letter","orientation":"portrait|landscape"="portrait","center":bool=true,"top":in?,"left":in?,"scale":%=100,"scaleToFit":bool=false,"colorHandling":"printerManages|photocraftManages|noColorManagement"="printerManages","printerProfile":profile? (photocraftManages),"intent":"perceptual|relative|saturation|absolute"="relative","bpc":bool=true,"cornerCropMarks":bool,"centerCropMarks":bool,"registrationMarks":bool,"description":bool,"labels":bool,"output":pdf path? (print to PDF; then "send" defaults to false),"send":bool?,"dryRun":bool=false (render the PDF, report the lp command, don't spool)} → {pdf, imageRect, command, sent}
```

## file.printOneCopy

Print One Copy

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.printOneCopy`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} (the last Print settings, one copy; any Print key overrides)
```

## file.package

Package…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.package`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"dir":folder,"format":"pcraft|psd|psb"="pcraft"} → {folder, document, links, missing} (copies the document and its linked files into <dir>/<name>/, relinked to Links/)
```

## file.export.pathsToIllustrator

Paths to Illustrator…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.pathsToIllustrator`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":str? (.ai; omit to return the text),"paths":"all|work|<path name>"="all"} → {path, paths}
```

## layer.pickAt

Auto-Select Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.pickAt`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"x":px,"y":px,"target":"layer|group"="layer","select":bool=true,"mode":"replace|toggle|add"="replace","list":bool=false (return every layer with pixels there, topmost first)} → {layer} | {layers}
```

## layer.new.frameFromLayers

Frame from Layers

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.new.frameFromLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":str?} → {layer, frame:[x,y,w,h]}: groups the selected layers and clips them to a frame rect
```

## edit.presets.migratePresets

Migrate Presets

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe edit.presets.migratePresets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path} → {migrated, added:{gradients,styles,shapes,patternGroups,toolPresets}}: merge a presets/preferences file into the library (appends groups by name)
```

## image.trap

Trap…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.trap`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{width:px>=1=1} → {trapped,width}: spread inks at colour edges (CMYK only)
```

## timeline.create

Create Video Timeline

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.create`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{duration?:30, fps?:30} → {timeline}
```

## timeline.delete

Delete Timeline

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.delete`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {timeline:null}
```

## timeline.setFrame

Go to Frame

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.setFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{frame} → {timeline}
```

## timeline.nextFrame

Next Frame

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.nextFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {timeline}
```

## timeline.previousFrame

Previous Frame

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.previousFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {timeline}
```

## timeline.setProps

Timeline Settings

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.setProps`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{fps?, duration?, workStart?, workEnd?} → {timeline}
```

## timeline.info

Timeline Info

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe timeline.info`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {timeline}
```

## layer.videoLayers.newBlankVideoLayer

New Blank Video Layer

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.newBlankVideoLayer`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.insertBlankFrame

Insert Blank Frame

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.insertBlankFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.duplicateFrame

Duplicate Frame

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.duplicateFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.deleteFrame

Delete Frame

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.deleteFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.restoreFrame

Restore Frame

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.restoreFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.restoreAllFrames

Restore All Frames

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.restoreAllFrames`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.showAlteredVideo

Show Altered Video

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.showAlteredVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.rasterize

Rasterize

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.rasterize`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.rasterize.video

Video

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.rasterize.video`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.newVideoLayerFromFile

New Video Layer from File…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.newVideoLayerFromFile`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.replaceFootage

Replace Footage…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.replaceFootage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.interpretFootage

Interpret Footage…

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.interpretFootage`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## layer.videoLayers.reloadFrame

Reload Frame

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.videoLayers.reloadFrame`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## file.import.videoFramesToLayers

Video Frames to Layers…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.import.videoFramesToLayers`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## file.export.renderVideo

Render Video…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.renderVideo`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {}
```

## file.import.wiaSupport

WIA Support…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.import.wiaSupport`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {available, devices, note}: acquire from a scanner/camera (Windows only)
```

## image.variables.define

Define…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.variables.define`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{defs:[{name, layer:id, type:visibility|textReplacement|pixelReplacement, method?:fit|fill|asIs|conform, align?, clip?}]} → {defs,dataSets,active}
```

## image.variables.dataSets

Data Sets…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.variables.dataSets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dataSets:[{name, values:[{variable, kind:visibility|text|pixels, value}]}], append?} → {defs,dataSets,active}
```

## image.applyDataSet

Apply Data Set…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.applyDataSet`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{name|index} → {applied, index}: sets layer visibility/text/pixels from the data set (one history step)
```

## file.import.variableDataSets

Variable Data Sets…

- 技能 / Owner: `photocraft-cli-project`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.import.variableDataSets`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{path, delimiter?} → {imported}: CSV header = variable names, each row a data set (first column may be the data-set name)
```

## file.export.dataSetsAsFiles

Data Sets as Files…

- 技能 / Owner: `photocraft-cli-export`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-export`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe file.export.dataSetsAsFiles`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{dir, format?:png, dataSets?[names], naming?:"{name}|{index}|{document}"} → {files,count}: apply each data set and export the flattened document
```

## variables.list

List Variables

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe variables.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{} → {defs,dataSets,active}
```

## plugin.list

List Plug-ins

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe plugin.list`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{}
```

## plugin.install

Install Plug-in…

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe plugin.install`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":text,"data":json,"replace":bool=true} (path: a .wasm file, native only; data: the module as base64)
```

## plugin.remove

Remove Plug-in

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe plugin.remove`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":text}
```

## plugin.reload

Reload Plug-ins

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe plugin.reload`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"path":text} (a folder of .wasm plug-ins; default: the Plug-ins preference folder)
```

## plugin.run

Run Plug-in

- 技能 / Owner: `photocraft-cli`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe plugin.run`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"id":text,"params":json} (plug-in parameters under "params" or at the top level; see plugin.list)
```

## brush.presets.rename

Rename Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.rename`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":string,"newName":string} → {name}
```

## brush.presets.move

Move Brush

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.move`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"name":string,"group":string?=its group ("" = ungrouped),"before":name? (preset to land before) | "index":n? (position in the group)=end} → {name, group, index}
```

## brush.presets.moveGroup

Move Brush Group

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.moveGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"group":string,"before":group? | "index":n? (group position)=end} → {group, index}
```

## brush.presets.renameGroup

Rename Brush Group

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.renameGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"group":string,"newName":string} → {group}
```

## brush.presets.deleteGroup

Delete Brush Group

- 技能 / Owner: `photocraft-cli-retouch`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-retouch`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: true；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe brush.presets.deleteGroup`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"group":string} → {deleted, count}
```

## layer.setExpanded

Expand/Collapse Group

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.setExpanded`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"expanded":bool?,"all":bool?} (no expanded: toggle; all: every group; not an undo step)
```

## layer.setEffectsExpanded

Expand/Collapse Effects

- 技能 / Owner: `photocraft-cli-layers`。
- 安装 / Install: `npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-layers`。
- 当前工作流映射 / Workflow mapped: false。
- 空会话观察 / Empty-session observation: false；禁用原因 / reason: 目录未提供具体原因；执行时重新查询 / query live state。
- 调用 / Invocation: `python3 -I -B "$SKILL_DIR/scripts/commands.py" describe layer.setEffectsExpanded`；按原生参数构造计划后执行 run。
- 完整逐命令验收 / Full command acceptance: NOT_RUN。

原生参数原文 / Verbatim native parameters:

```text
{"layer":id?,"expanded":bool?,"all":bool?} (no expanded: toggle; all: every layer with effects; view state, not an undo step)
```
