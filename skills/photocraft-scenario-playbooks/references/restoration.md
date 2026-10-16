# PhotoCraft restoration 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

## old-photo-conservative：老照片保守修复全流程

输入：有扫描图与可辨认的局部损伤；确认是否保持黑白。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 只点选已确认的灰尘，不覆盖眼睛、文字和胶片颗粒 | `paint.spotHealing` | `{"points":[[40,30,1],[44,32,1]],"size":5,"type":"proximityMatch"}` |
| 3. 从同材质邻近完好位置采样，沿损伤做短笔触 | `paint.healingBrush` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":40,"sampleLayer":"current","opacity":70}` |
| 4. 轻度降噪，保留可识别纹理和胶片颗粒 | `filter.noise.reduceNoise` | `{"strength":2,"preserveDetails":85,"reduceColorNoise":20,"sharpenDetails":0}` |
| 5. 观察直方图后恢复中间调，黑白场不硬截断 | `layer.newAdjustmentLayer.levels` | `{"inBlack":5,"gamma":1.05,"inWhite":248}` |

检查：修复层与原图均保留；人物边缘与字形未被改造；前后图同尺寸比较，未修区纹理一致。

边界：大面积缺失和无法辨识的人脸不推测重建；逐分区采样，不把例子坐标用于整张照片。

## scan-dust-specks：扫描灰尘与细小白点

输入：灰尘位置可识别，并与真实高光、雀斑区分。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 只点选已确认的灰尘，不覆盖眼睛、文字和胶片颗粒 | `paint.spotHealing` | `{"points":[[40,30,1],[44,32,1]],"size":5,"type":"proximityMatch"}` |

检查：灰尘点消失而纹理继续；没有一片糊斑或重复纹理。

边界：高光反射、痣、衣服纹样不能按灰尘移除。

## hairline-scratch：胶片细划痕局部修补

输入：细划痕与邻近同材质采样位置。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 从同材质邻近完好位置采样，沿损伤做短笔触 | `paint.healingBrush` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":40,"sampleLayer":"current","opacity":70}` |

检查：划痕两侧亮度连续；笔画没有越过人物轮廓。

边界：划痕穿过五官时分段处理；不能从皮肤跨采样到背景。

## fold-line-background：背景折痕分区修补

输入：折痕分段位置、两侧对应材质、轮廓保护区。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 按边缘方向取样，以低透明度短笔触接续纹理 | `paint.cloneStamp` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":65,"opacity":60,"aligned":true,"sampleLayer":"current"}` |
| 3. 从同材质邻近完好位置采样，沿损伤做短笔触 | `paint.healingBrush` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":40,"sampleLayer":"current","opacity":70}` |

检查：折痕边界连续；没有重复图案；人物轮廓未移动。

边界：先克隆重建纹理，再修复亮度过渡；两次采样各自重新选择。

## torn-corner-texture：照片角部小块缺损修复

输入：缺损限于可由邻近背景推定的小角部。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 按边缘方向取样，以低透明度短笔触接续纹理 | `paint.cloneStamp` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":65,"opacity":60,"aligned":true,"sampleLayer":"current"}` |

检查：边框和背景接续方向一致；缺失处与原始留存区分明确。

边界：不补造缺失文字、身体、建筑结构；大缺角另存推测版。

## silver-mirror-local：银镜反光区域保守校正

输入：局部反光位置和相邻可靠纹理；仅能处理小面积扫描反光。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 按边缘方向取样，以低透明度短笔触接续纹理 | `paint.cloneStamp` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":65,"opacity":60,"aligned":true,"sampleLayer":"current"}` |

检查：高光变化局限于确认损伤；图案边界连续。

边界：广泛银镜反射优先重新布光扫描；命令不能恢复根本未采集到的细节。

## moire-small-radius：扫描印刷网点轻度抑制

输入：明显网点而非胶片颗粒；输出允许轻微细节损失。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 在副本尝试最小半径中值滤波 | `filter.noise.median` | `{"radius":1}` |

检查：网点减轻；发丝、纸纹未被完全磨平。

边界：单次小半径测试；网纹严重时重新扫描，不能靠强滤镜冒充修复。

## jpeg-block-reduction：旧 JPEG 方块伪影减轻

输入：有明显压缩网格的副本；原始文件不可得。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 对压缩伪影优先保留结构 | `filter.noise.reduceNoise` | `{"strength":2,"preserveDetails":90,"reduceColorNoise":25,"sharpenDetails":0,"removeJpegArtifact":true}` |

检查：块状网格减轻；小字没有糊成团。

边界：丢失的 JPEG 细节无法真实重建；不先锐化网格。

## gentle-color-noise：暗部彩色噪声抑制

输入：暗部有彩色斑点，与真实颜色边缘区分。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 优先减彩噪，少动亮度细节 | `filter.noise.reduceNoise` | `{"strength":1,"preserveDetails":90,"reduceColorNoise":35,"sharpenDetails":0}` |

检查：彩色斑点减轻；暗部纹理仍存在。

边界：显示器预览噪声不一定写入源文件，先以100%核对。

## small-stain-sampled：小面积霉点取样修复

输入：小霉点范围、同材质采样点、需要保留的斑纹。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 从同材质邻近完好位置采样，沿损伤做短笔触 | `paint.healingBrush` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":40,"sampleLayer":"current","opacity":70}` |
| 3. 按边缘方向取样，以低透明度短笔触接续纹理 | `paint.cloneStamp` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":65,"opacity":60,"aligned":true,"sampleLayer":"current"}` |

检查：霉点边界不突兀；没有残余取样十字纹。

边界：仅小面积；大霉斑涉及缺失图案时无法可靠复原。

## scratch-edge-protection：靠近人物边界的划痕定区修复

输入：划痕紧贴人物外缘，已知边界不应移动。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Protected scratch"}` |
| 2. 沿背景侧勾选修补区域，避开人物 | `select.lasso` | `{"points":[[28,30],[52,30],[52,70],[28,70]],"mode":"replace","feather":0.5}` |
| 3. 在选区中克隆邻近同材质背景 | `paint.cloneStamp` | `{"points":[[40,40,1],[40,60,1]],"source":[24,40],"size":5,"hardness":70,"opacity":85,"sampleLayer":"current"}` |
| 4. 结束局部操作，清除活动选区 | `select.deselect` | `{}` |

检查：边界内人物像素保持；划痕连续性打断；背景纹理方向连贯。

边界：例子采样点须有对应背景纹理；不能跨人脸、衣物或文字采样。

## large-stain-patch：平坦背景块状污点修补

输入：污点周围有足够同材质纹理，没有人物或文字被遮挡。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Patch stain"}` |
| 2. 按实际目标轮廓定位；此处为256×192测试矩形 | `select.rect` | `{"x":96,"y":72,"width":24,"height":20,"mode":"replace","feather":1}` |
| 3. 把选区拖向右侧干净纹理，源模式回填原污点区 | `paint.patch` | `{"offset":[40,0],"mode":"source","contentAware":false}` |
| 4. 结束局部操作，清除活动选区 | `select.deselect` | `{}` |

检查：原污点区被干净纹理替代；取样区没有同步破坏；接缝与邻域明暗接近。

边界：平铺纹理可能重复；移动offset前确保源区没有另一处损伤。

