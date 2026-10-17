# PhotoCraft geometry 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

## scan-deskew-border：扫描倾斜与边框整理

输入：确认水平参考与最终需保留的纸边；例子画布至少256×192。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 按实测倾斜角纠偏 | `image.rotation.arbitrary` | `{"angle":1,"direction":"ccw","interpolation":"bicubic"}` |
| 3. 纠偏后重新量取裁切框 | `image.crop` | `{"x":8,"y":8,"width":240,"height":176,"deleteCroppedPixels":false}` |

检查：水平参考校正；裁切不切掉边缘文字或人物。

边界：旋转后的尺寸会变化，裁切参数必须重新计算。

## scan-four-side-crop：扫描件四边污边裁去

输入：边缘均为扫描台或污边；确认内容不触边，示例裁到240×176。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Clean scan crop"}` |
| 2. 按已确认的内容框裁切；保留外部像素供编辑回退 | `image.crop` | `{"x":8,"y":8,"width":240,"height":176,"deleteCroppedPixels":false}` |

检查：输出尺寸240×176；内容没有截断；保存后重开验证副本，执行 image.revealAll {} 并核对原始256×192边缘仍存在。

边界：不是透视矫正；输入尺寸与污边宽度变化后必须重算裁切框。

