# PhotoCraft portrait 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

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

## skin-shine-burn：保留皮肤纹理减弱局部油光

输入：仅调整有纹理的额头/鼻梁高光，不处理纯白剪切区域。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Skin shine"}` |
| 2. 在油光区域以低曝光加深高光 | `paint.burn` | `{"points":[[112,60,1],[116,64,1]],"size":12,"hardness":0,"range":"highlights","exposure":6,"protectTones":true}` |
| 3. 减弱整个修饰层，避免灰斑 | `layer.setProps` | `{"opacity":0.65}` |

检查：皮肤毛孔仍可见；油光不再刺眼；没有灰色笔触边缘。

边界：采样坐标由当前人像确定；不要用加深重建被剪切纹理。

## hair-stray-cleanup：纯色背景杂发整理

输入：仅移除主体外孤立杂发，保留发际线与原发量。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Stray hair"}` |
| 2. 从同高度背景取样，以细硬笔短段修补 | `paint.cloneStamp` | `{"points":[[168,40,1],[172,44,1]],"source":[188,40],"size":3,"hardness":65,"opacity":90,"sampleLayer":"current"}` |
| 3. 降低修饰层强度，保留自然细发 | `layer.setProps` | `{"opacity":0.8}` |

检查：主体发量与轮廓未变；背景没有重复斑块；100%视图没有残余断发。

边界：复杂纹理背景需逐段重取样；例子不能自动识别所有杂发。

## portrait-teeth-local：牙齿自然去黄

输入：露齿区域有自然纹理；明确不修改牙形、不做纯白填充。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Teeth neutral"}` |
| 2. 沿牙齿区域勾选，避免嘴唇牙龈 | `select.lasso` | `{"points":[[100,102],[128,102],[126,112],[102,112]],"mode":"replace","feather":0.5}` |
| 3. 只降低黄色，保留冷暖与齿间阴影 | `layer.newAdjustmentLayer.hueSaturation` | `{"yellows":{"saturation":-25,"lightness":3}}` |
| 4. 结束局部操作，清除活动选区 | `select.deselect` | `{}` |

检查：唇色牙龈不变；牙齿未成白块；原有齿间纹理仍清晰。

边界：牙齿坐标须人工确认；不能把示例多边形套在任意人脸。

