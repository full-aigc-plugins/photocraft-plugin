# 图像尺寸、模式与自动调整 / Image dimensions, modes and automatic adjustments

## 输入和保留策略 / Inputs and preservation

输入为目标pcraft工程、画幅、用途、模式/位深、输出要求及可修改对象。先doc_inspect，记录尺寸、图层、模式和位深，另存修订。图像重采样、画布变化、裁切和模式转换对内容的影响不同；保留原工程与素材。要求文字、产品、背景分别编辑时，不能将会合并图层的转换结果作为唯一原生交付。

Inspect native dimensions, mode, depth and layers before changing them. Keep the original project. Resampling, canvas changes, cropping and mode conversion are different operations. Preserve editable layers when required.

## 尺寸适配 / Dimension adaptation

由 **photocraft-cli-resize** 负责。安装：`npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-resize`。

| 任务 | 命令 | 步骤、参数和核验 |
| --- | --- | --- |
| 图像尺寸和重采样 | `image.imageSize` | width/height为像素，resolution为ppi；选择resample并核对图层、文字、蒙版和输出像素。resample:none不等于重新生成像素尺寸 |
| 留白或裁画布 | `image.canvasSize` | 明确relative、anchor与extensionColor；检查内容是否移动、裁切，扩展透明画布时不要误填背景色 |
| 裁去边缘 | `image.trim` | basedOn为transparent/topLeft/bottomRight，分别决定参照；四边开关独立。透明裁边按合成后的alpha检测，空内容会失败；检查尺寸、主体边界及保留图层 |
| 展开被画布遮住的内容 | `image.revealAll` | 先检查画布外对象，再执行并核对扩展边界；扩大画布不等于找回已经删除的像素 |
| 任意角旋转 | `image.rotation.arbitrary` | angle角度、direction为cw/ccw、interpolation重采样；检查新尺寸、透明角、文字和蒙版。与90度整数旋转、翻转分开处理 |
| 正交旋转和翻转 | `image.imageRotation.*` | 查询精确命令，核对旋转后的宽高、方向及每层位置；不要把预览视图旋转当作工程旋转 |

## 原生工程模式与副本 / Native modes and copies

由 **photocraft-cli-project** 负责。安装：`npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-project`。

| 任务 | 命令 | 步骤、参数和核验 |
| --- | --- | --- |
| 独立副本 | `image.duplicate` | 指定name，默认mergedOnly:false；mergedOnly:true是合成副本。核对活动文档和新文档身份，保存副本，不覆盖原工程 |
| 基础色彩模式 | `image.mode.rgb`、`image.mode.grayscale`、`image.mode.cmyk`、`image.mode.lab` | 明确目标用途，检查转换前后模式、profile及颜色；灰度会损失颜色，不把模式正确当作印刷色彩验收 |
| 位深 | `image.mode.bits8`、`image.mode.bits16`、`image.mode.bits32` | 核对当前和目标位深、动态范围与输出格式；提高位深不会恢复已丢失信息，降低位深需要检查渐变和高光 |
| 索引色及调色板 | `image.mode.indexedColor`、`image.mode.colorTable` | 明确palette、colors数量、transparency和dither；索引色会合并图层。colorTable的colors/entries/transparent指定表项，不是RGB图层配色 |
| 位图 | `image.mode.bitmap` | 明确method、frequency、angle与shape，frequency为线/英寸；该转换合并图层，需核对网点、尺寸和分辨率 |
| 专色与多通道 | `image.mode.duotone`、`image.mode.multichannel` | duotone明确type、inks名称/颜色/曲线；multichannel会合并图层，通道随来源模式变化。核对真实通道与交付，不能用通道存在推断印刷效果 |

## 自动像素调整 / Automatic pixel adjustments

由 **photocraft-cli-adjustments** 负责。安装：`npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli-adjustments`。

`image.autoTone`、`image.autoContrast`、`image.autoColor` 是自动像素调整，不能宣称它们自动创建了可编辑调整图层。明确目标图层、选区及修改范围，先保存副本，查询enabled后执行；核对直方图、颜色与非目标内容。要求可编辑参数时优先使用已有调整图层流程；自动调整结果需独立审核，不能以命令成功代替图像质量。

Auto adjustments change pixels; they do not prove an editable adjustment layer was created. Check the active layer/selection, preserve the source and inspect actual target and unaffected pixels.

## 公共执行步骤 / Public execution

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.trim
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe image.mode.indexedColor
python3 -I -B "$SKILL_DIR/scripts/commands.py" check /absolute/image-plan.json
python3 -I -B "$SKILL_DIR/scripts/commands.py" run /absolute/image-plan.json --output /absolute/new-image-result
```

使用本技能command-usage.md的计划合同；更改后同会话保存pcraft，重开后核对尺寸、模式、位深、图层及导出像素。参数说明、分类和计划校验不等于19条新增归属命令全部执行验收；不同转换的图层损失必须按实际结果记录。

Save and reopen the native document. Verify dimensions, mode, depth, layer preservation and exported pixels. The guide extends existing skills; complete per-command acceptance remains open.

## 已执行尺寸与位深实例 / Executed dimension and depth example

`examples/image-trim-depth-create.json` 无需外部素材，建立96×64透明RGB8工程与Product、Badge两个形状层，保存original.pcraft；透明裁边后转换为16位，另存variant.pcraft并导出PNG。`examples/image-trim-depth-reopen.json` 接收 `--input project=/absolute/variant.pcraft`，重开检查并导出；也可用于独立核对original.pcraft。均使用本技能commands.py run和新的输出目录。

已核验变体32×16、16位，图层ID/名称/类型保留，重开图层与导出像素一致；原工程独立重开仍为96×64、8位且图层未改。自动调整、任意角旋转、索引色/位图及全部19条命令仍需各自运行验收。

The bounded fixture preserves separate shape layers and the original project while trimming transparent margins and changing depth. It does not prove color fidelity or every newly routed operation.
