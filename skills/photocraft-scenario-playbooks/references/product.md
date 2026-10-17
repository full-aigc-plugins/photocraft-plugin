# PhotoCraft product 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

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
| 2. 保留原图层用于恢复，但从成片合成中隐藏它，避免重新叠回背景/半透明边缘 | `layer.setProps` | `{"layer":{"$ref":"originalLayer"},"visible":false}` |
| 3. 仅去除白色杂边，保留alpha形状 | `layer.matting.removeWhiteMatte` | `{}` |

检查：深底下边缘无白边；浅色主体细边没有变黑。

边界：先确认alpha存在；全白主体边缘不可用此命令盲处理。

执行前先用当前inspect取得待处理原像素层的真实ID，记为originalLayer；$ref仅是手册记号，替换整个对象为实际整数后再调用原生CLI/MCP。复制工作层后隐藏原图层，不删除它；仍以工作副本为活动层。复杂工程还须检查其余可见底图，不无条件隐藏其他用户图层。

## product-dark-matte：深色旧底抠图黑边整理

输入：透明图层边缘有来自旧黑底的污染。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 保留原图层用于恢复，但从成片合成中隐藏它，避免重新叠回背景/半透明边缘 | `layer.setProps` | `{"layer":{"$ref":"originalLayer"},"visible":false}` |
| 3. 去黑底污染，保持alpha轮廓 | `layer.matting.removeBlackMatte` | `{}` |

检查：浅底下没有黑边；头发与半透明材质过渡自然。

边界：玻璃和烟雾不应按不透明硬边处理。

执行前先用当前inspect取得待处理原像素层的真实ID，记为originalLayer；$ref仅是手册记号，替换整个对象为实际整数后再调用原生CLI/MCP。复制工作层后隐藏原图层，不删除它；仍以工作副本为活动层。复杂工程还须检查其余可见底图，不无条件隐藏其他用户图层。

## product-background-mask：商品主体蒙版分离

输入：单一清晰主体，底图与主体边缘对比足够。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 保留原图层用于恢复，但从成片合成中隐藏它，避免重新叠回背景/半透明边缘 | `layer.setProps` | `{"layer":{"$ref":"originalLayer"},"visible":false}` |
| 3. 先用主体选择建立可编辑蒙版 | `layer.removeBackground` | `{"refine":true,"sampleAllLayers":false}` |

检查：蒙版保留细边；原图像素仍可恢复；输出透明图无锯齿。

边界：这是当前命令的主体选择能力，不保证发丝、玻璃和重叠商品完美。

执行前先用当前inspect取得待处理原像素层的真实ID，记为originalLayer；$ref仅是手册记号，替换整个对象为实际整数后再调用原生CLI/MCP。复制工作层后隐藏原图层，不删除它；仍以工作副本为活动层。复杂工程还须检查其余可见底图，不无条件隐藏其他用户图层。

## product-reflection-spot：商品小面积反光点缓和

输入：高光周围有同曲率、同材质可采样区；仅处理不承载商标的小点。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Reflection cleanup"}` |
| 2. 同材质取样以低透明度恢复局部过渡 | `paint.healingBrush` | `{"points":[[156,88,1]],"source":[144,88],"size":8,"hardness":30,"opacity":35,"sampleLayer":"current"}` |
| 3. 减弱修饰层，仍保留材质光泽 | `layer.setProps` | `{"opacity":0.75}` |

检查：高光未完全抹平；曲面光线连续；商标文字与产品形状保持。

边界：大面积镜面高光没有可信纹理时不修补；不得编造产品表面信息。

## product-label-edge-sharpen：商品标签定区锐化

输入：标签文字本来可辨，需提高缩图前局部清晰度。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Label detail"}` |
| 2. 按实际目标轮廓定位；此处为256×192测试矩形 | `select.rect` | `{"x":80,"y":64,"width":96,"height":56,"mode":"replace","feather":1}` |
| 3. 只对标签像素轻度锐化 | `filter.sharpen.unsharpMask` | `{"amount":45,"radius":0.6,"threshold":3}` |
| 4. 结束局部操作，清除活动选区 | `select.deselect` | `{}` |

检查：标签外背景噪声不变；细字没有白边；没有产生不存在的笔画。

边界：模糊到不可读的文字不能凭锐化恢复；确认缩图最终尺寸再调强度。

## product-color-proof-area：商品配色局部试样

输入：客户要求比较已有产品区域的替代配色，输出标明效果预览。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Color proof"}` |
| 2. 按实际目标轮廓定位；此处为256×192测试矩形 | `select.rect` | `{"x":64,"y":64,"width":96,"height":80,"mode":"replace","feather":1}` |
| 3. 在局部蒙版调整色相与饱和度 | `layer.newAdjustmentLayer.hueSaturation` | `{"hue":-35,"saturation":12}` |
| 4. 结束局部操作，清除活动选区 | `select.deselect` | `{}` |

检查：背景与商标排除区保持；反光阴影仍保留；文件名注明配色预览。

边界：示例矩形需要减去商标和不可改色区；此图不是实物颜色证明。

