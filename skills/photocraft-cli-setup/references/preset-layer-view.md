# 画笔预设组织与图层视图 / Brush organization and layer view

## 使用场景 / When to use

`photocraft-cli-retouch` 管理已有画笔预设名称、组和顺序；`photocraft-cli-layers` 管理图层组与效果列表的展开状态。七条命令均可经本技能的 `commands.py describe/check/run` 调用。原生参数原文位于 `command-reference.md`。

Use retouch for brush preset names, groups and ordering; use layers for group and effects disclosure state. Describe each command, preflight a plan, then run through this skill's own scripts.

## 画笔预设 / Brush presets

先 `brush.presets.list` 并使用实际存在的名称。`name` 查找忽略大小写，重命名不能与另一个名称冲突。`brush.presets.rename` 的 `newName` 必填。不要用示例名称覆盖现有预设。

List presets first and use returned names. Lookup is case-insensitive. A new name must not collide with another preset.

- `brush.presets.move`：`name` 必填；`group` 省略则保留原组，空字符串表示未分组；`before` 指定目标预设，或 `index` 指定组内非负整数位置，省略则放末尾。跨组移动前检查目标名称与组是否一致。
- `brush.presets.moveGroup`：`group` 必填；按 `before` 组或非负整数 `index` 整组移动，组内顺序保留。
- `brush.presets.renameGroup`：`group` 和 `newName` 必填，目标组名不得与已有组冲突。
- `brush.presets.deleteGroup`：删除组内全部预设，并非仅移除组标签；先导出或确认该组成员可删除，检查返回的 `deleted` 数量。

Move presets with an explicit destination group and either a preceding preset or a non-negative integer index. Move a group as a block. Rename a group to a non-conflicting name. Deleting a group removes its members; inspect the group and preserve needed presets first.

这些操作可能将修改的内置预设转为用户预设。它们属于工具预设，不是 `.pcraft` 中的可编辑图层，也不应以保存工程代替预设持久化验收。

Modified built-in presets can become user presets. Tool presets are distinct from document layers; saving a native project does not prove preset persistence.

## 图层视图 / Layer disclosure

`layer.setExpanded` 必须有工程和组图层；`layer.setEffectsExpanded` 必须有工程和包含效果的图层。`layer` 使用创建或检查返回的 ID；省略则使用当前图层。`expanded` 必须是布尔值，省略会翻转状态；`all:true` 操作所有组或所有带效果图层。自动计划优先显式传 `expanded`，避免重试翻转。

Use actual layer IDs. Group disclosure requires a group; effects disclosure requires effects. Pass explicit boolean state for repeatable intent; omission toggles. `all:true` affects every applicable layer.

两条命令不增加撤销步骤，也不会使干净工程变脏。组展开状态可随 `.pcraft`／PSD 保存；效果列表展开状态属于会话视图，不能承诺重开后保留。改变视图不会改变合成像素。

Neither operation adds an undo step or dirties a clean document. Group disclosure is document data saved in native/PSD output; effects disclosure is session view state. Verify document content and rendered pixels separately.

## 示例与验收 / Example and verification

[preset-layer-view-create.json](../examples/preset-layer-view-create.json) 创建专用示例预设并操作五条预设命令，随后删除仅该示例组；创建带效果的图层和组，设置两种视图，保存原生工程并导出 PNG。执行前查询并确认 `CraftExample*` 名称未占用，实际任务替换为独有名称。`deleteGroup` 只针对本计划创建的组。

The example uses dedicated disposable names, exercises the five preset commands and cleans up only its own groups. It creates native layers/effects and group disclosure state, saves the project and exports PNG. Check for name collisions and use unique task names before running.

验收：预设操作前后的非目标完整列表一致；重命名／移动／删除回执符合目标；保存并重开工程检查组状态；对比目标效果与 PNG。参数说明、分类和预检通过不代替原生执行或长期预设存储验收。

Verify unchanged non-target presets, mutation receipts, saved/reopened group state and rendered content. Classification and preflight do not prove execution or long-term preset storage.
