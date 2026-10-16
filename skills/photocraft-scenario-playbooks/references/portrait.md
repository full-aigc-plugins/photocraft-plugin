# PhotoCraft portrait 场景

以下参数是256×192示例坐标/低强度起点。先检查当前输入、对象和命令参数；按实际损伤重算坐标，不得直接套用。

## portrait-small-blemish：自然人像局部痘印修饰

输入：明确要修饰临时痘印，保留痣和身份特征。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 只对临时痘印做单点近邻修复 | `paint.spotHealing` | `{"points":[[100,72,1]],"size":4,"type":"proximityMatch"}` |

检查：皮肤纹理连续；原有身份特征保留。

边界：示例点不是人脸检测坐标；没有可靠人脸定位时先看图手动确定。

## portrait-eye-shadow：人像眼下阴影轻度减淡

输入：确认阴影而非真实轮廓；采样仍位于同一肤色区。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 低透明度修复局部阴影而非抹平眼袋结构 | `paint.healingBrush` | `{"points":[[100,72,1],[104,72,1]],"source":[100,82],"size":5,"opacity":25,"hardness":20,"sampleLayer":"current"}` |

检查：眼下与颧骨过渡自然；眼睛边缘未改变。

边界：保留年龄特征和眼部结构，用户未要求时不消除全部阴影。

## portrait-white-balance：人像整体轻微白平衡

输入：可信中性参考、肤色与背景颜色可比较。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 仅从小幅色彩平衡起步 | `layer.newAdjustmentLayer.colorBalance` | `{"midtones":[0,-2,3],"preserveLuminosity":true}` |

检查：脸和颈部一致；白衣与中性背景无异常色偏。

边界：暖光场景不必强制中性；调整方向应由输入测量决定。

## portrait-backlit：逆光人像暗部回调

输入：高光未完全剪切，脸部有可用暗部层次。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 温和提升阴影并限制半径 | `image.adjustments.shadowsHighlights` | `{"shadowAmount":15,"shadowTone":40,"shadowRadius":12,"highlightAmount":5,"highlightTone":50,"highlightRadius":12}` |

检查：发丝轮廓无光晕；脸部噪点不明显放大。

边界：此命令直接处理像素，先用副本；不能恢复全黑无数据的区域。

