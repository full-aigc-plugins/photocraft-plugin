# PhotoCraft delivery 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

## restore-final-sharpen：修复成片的最终锐化

输入：修复与尺寸处理已经完成；确认最终展示尺寸。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 确认交付尺寸后轻度锐化，避开明显损伤 | `filter.sharpen.unsharpMask` | `{"amount":35,"radius":0.6,"threshold":3}` |

检查：100%下没有双边和白边；字形与颗粒不过锐。

边界：不以锐化弥补失焦，打印和屏幕版分别调整强度。

## print-resolution-tag：老照片打印分辨率标记

输入：确认像素尺寸足够且打印需求只需修改ppi元数据。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 仅改分辨率，不重采样像素 | `image.imageSize` | `{"resolution":300,"resample":"none"}` |

检查：导出像素数不变；打印尺寸由像素/300ppi得到。

边界：不能把改ppi标记说成提高真实分辨率。

## web-image-downsample：网页展示图缩小

输入：确认目标为256×192示例尺寸；保持同一长宽比。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 先缩小到目标像素尺寸 | `image.imageSize` | `{"width":256,"height":192,"resample":"bicubicSharper"}` |

检查：比例不变；文字边缘清晰；没有反复放大再缩小。

边界：非4:3输入必须按比例计算另一边，例子尺寸不能直接套用。

## transparent-canvas-padding：透明四边扩画布交付

输入：输出用于叠加排版；原图不需要生成新背景。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Transparent padding"}` |
| 2. 居中增加四边透明画布，示例每边16像素 | `image.canvasSize` | `{"width":288,"height":224,"anchor":"center","extensionColor":"transparent"}` |

检查：输出为288×224；PNG四角alpha为0；原图内容居中且未缩放。

边界：JPEG不保存透明；保留.pcraft工程并用PNG交付，不能以白底预览判断透明。

