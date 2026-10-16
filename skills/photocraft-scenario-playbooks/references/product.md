# PhotoCraft product 场景

以下参数是256×192示例坐标/低强度起点。先检查当前输入、对象和命令参数；按实际损伤重算坐标，不得直接套用。

## product-neutral-packshot：商品中性白底基础校正

输入：真实商品图、准确材质颜色和白底参考。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 观察直方图后恢复中间调，黑白场不硬截断 | `layer.newAdjustmentLayer.levels` | `{"inBlack":5,"gamma":1.05,"inWhite":248}` |
| 3. 控制饱和度，避免偏离商品真实颜色 | `layer.newAdjustmentLayer.vibrance` | `{"vibrance":3,"saturation":0}` |

检查：包装文字清晰；商品颜色与原物相符。

边界：白底不等于主体可以过曝；反光应保留形体。

## product-surface-dust：商品表面灰尘清理

输入：拍摄灰尘与真实划伤、纹理、铭牌区分。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 只点选已确认的灰尘，不覆盖眼睛、文字和胶片颗粒 | `paint.spotHealing` | `{"points":[[40,30,1],[44,32,1]],"size":5,"type":"proximityMatch"}` |
| 3. 按边缘方向取样，以低透明度短笔触接续纹理 | `paint.cloneStamp` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":65,"opacity":60,"aligned":true,"sampleLayer":"current"}` |

检查：拍摄灰尘清除；真实材质与标签未修改。

边界：商业交付不得把真实商品缺陷无说明地抹成不同商品状态。

## product-edge-halo：白底抠图白边整理

输入：已有带透明度的像素图层；确认白色边缘来自旧底色。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 仅去除白色杂边，保留alpha形状 | `layer.matting.removeWhiteMatte` | `{}` |

检查：深底下边缘无白边；浅色主体细边没有变黑。

边界：先确认alpha存在；全白主体边缘不可用此命令盲处理。

## product-dark-matte：深色旧底抠图黑边整理

输入：透明图层边缘有来自旧黑底的污染。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 去黑底污染，保持alpha轮廓 | `layer.matting.removeBlackMatte` | `{}` |

检查：浅底下没有黑边；头发与半透明材质过渡自然。

边界：玻璃和烟雾不应按不透明硬边处理。

## product-background-mask：商品主体蒙版分离

输入：单一清晰主体，底图与主体边缘对比足够。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 先用主体选择建立可编辑蒙版 | `layer.removeBackground` | `{"refine":true,"sampleAllLayers":false}` |

检查：蒙版保留细边；原图像素仍可恢复；输出透明图无锯齿。

边界：这是当前命令的主体选择能力，不保证发丝、玻璃和重叠商品完美。

