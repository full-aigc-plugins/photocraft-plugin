# PhotoCraft delivery 场景

以下参数是256×192示例坐标/低强度起点。先检查当前输入、对象和命令参数；按实际损伤重算坐标，不得直接套用。

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

