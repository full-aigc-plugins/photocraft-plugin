# PhotoCraft geometry 场景

以下参数是256×192示例坐标/低强度起点。先检查当前输入、对象和命令参数；按实际损伤重算坐标，不得直接套用。

## scan-deskew-border：扫描倾斜与边框整理

输入：确认水平参考与最终需保留的纸边；例子画布至少256×192。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 按实测倾斜角纠偏 | `image.rotation.arbitrary` | `{"angle":1,"direction":"ccw","interpolation":"bicubic"}` |
| 3. 纠偏后重新量取裁切框 | `image.crop` | `{"x":8,"y":8,"width":240,"height":176,"deleteCroppedPixels":false}` |

检查：水平参考校正；裁切不切掉边缘文字或人物。

边界：旋转后的尺寸会变化，裁切参数必须重新计算。

