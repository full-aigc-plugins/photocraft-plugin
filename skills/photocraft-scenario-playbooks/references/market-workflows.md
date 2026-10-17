# 从技能商店适配的场景方法

以下内容是基于已阅读技能的原创 Craft 指导。沿用现有配方的实际命令；这里补充任务判断和结果检查，不将同一配方再计为新增场景。商店提供发现入口，原技能使用的软件、服务和依赖不会随本插件安装。

示例步骤是参数模板，不能直接作为通用执行脚本。先取当前会话的文档、图层、片段或故事ID，解析所有引用，再按实际工具schema执行；尺寸、坐标、路径和文本按本次任务调整。已打开编辑器时使用同一个MCP会话；独立CLI文件编辑不能证明界面同步。

## 修复与推测分开交付

参考：[eachlabs/skills/photo-restoration](https://github.com/eachlabs/skills/blob/a881258627b81b6bb53812491edaa5917479687e/skills/photo-restoration/SKILL.md)；[skillhub:aihive-en-photo-restoration-studio](https://api.skillhub.cn/api/v1/download?slug=aihive-en-photo-restoration-studio)。

先标出划痕、缺损、褪色和不可判断的内容；先做局部修补，再处理整体影调。人物五官和历史文字逐区比对。上色或补造不存在的细节属于另一个选择，不能混入保真修复。

原配方：`old-photo-conservative`。输入与边界：有扫描图与可辨认的局部损伤；确认是否保持黑白。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2 | `paint.spotHealing` | `{"points":[[40,30,1],[44,32,1]],"size":5,"type":"proximityMatch"}` |
| 3 | `paint.healingBrush` | `{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"hardness":40,"sampleLayer":"current","opacity":70}` |
| 4 | `filter.noise.reduceNoise` | `{"strength":2,"preserveDetails":85,"reduceColorNoise":20,"sharpenDetails":0}` |
| 5 | `layer.newAdjustmentLayer.levels` | `{"inBlack":5,"gamma":1.05,"inWhite":248}` |

检查：保留原扫描；同尺寸检查人物和字迹，列出无法恢复的区域。

能力边界：Craft的取样修补不等于生成模型的人脸重建或自动上色。

原配方结果检查：["修复层与原图均保留", "人物边缘与字形未被改造", "前后图同尺寸比较，未修区纹理一致"]

原配方限制：大面积缺失和无法辨识的人脸不推测重建；逐分区采样，不把例子坐标用于整张照片。

## 保留身份特征的人像修饰

参考：[qzfcoder/photo-retouch-pro/photo-retouch-pro](https://github.com/qzfcoder/photo-retouch-pro/blob/bd963066b15f9dda1f46b10e63427f1046b57acc/SKILL.md)；[calesthio/generative-media-skills/still-image-retouching-finishing](https://github.com/calesthio/generative-media-skills/blob/8c85352d5d75d4dcbe58480bd138e37b9742bab1/skills/production/post-production/still-image-retouching-finishing/SKILL.md)。

先看缩略图判断主体，再在原尺寸区分暂时性痘印与痣、皱纹、轮廓等身份特征。只对获准区域取样，先少量修，再比较纹理，不能全脸同强度涂抹。

原配方：`portrait-small-blemish`。输入与边界：明确要修饰临时痘印，保留痣和身份特征。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2 | `paint.spotHealing` | `{"points":[[100,72,1]],"size":4,"type":"proximityMatch"}` |

检查：保护区与原图对照；痘印减弱而毛孔和轮廓仍在。

能力边界：不移植外部生成式换脸或自动美颜调用；坐标由本次照片决定。

原配方结果检查：["皮肤纹理连续", "原有身份特征保留"]

原配方限制：示例点不是人脸检测坐标；没有可靠人脸定位时先看图手动确定。

## 代表样片后再批量调色

参考：[adobe/skills/adobe-retouch-portraits](https://github.com/adobe/skills/blob/e9692ed98504e8a8658b99daeb698f81498dfc9b/plugins/creative-cloud/adobe-for-creativity/skills/adobe-retouch-portraits/SKILL.md)。

按光照和色偏分组，各组选一张代表图先修；把白平衡与肤色看清再决定其余照片的起点。预览尺寸可以缩小，最终从原尺寸输入重新处理，不能放大预览充当成片。

原配方：`portrait-white-balance`。输入与边界：可信中性参考、肤色与背景颜色可比较。

| 顺序 | Craft 实际方法 | 参数模板 |
| --- | --- | --- |
| 1 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2 | `layer.newAdjustmentLayer.colorBalance` | `{"midtones":[0,-2,3],"preserveLuminosity":true}` |

检查：逐组检查肤色、白衣和高光，异常曝光单张处理。

能力边界：不同照明不共用一套白平衡；不依赖Adobe账户、预设服务或外部初始化工具。

原配方结果检查：["脸和颈部一致", "白衣与中性背景无异常色偏"]

原配方限制：暖光场景不必强制中性；调整方向应由输入测量决定。

## 版本与执行

执行包装沿用本技能主文件。局部修补先选可写的像素层；取样位置、保护区域和强度从实际照片确定。预览与最终输出分别从合适分辨率的原图处理。 保存到未占用路径并重开，按实际产物检查；本轮文档适配未新增宿主或真实媒体验收。

本技能内的[商店来源与参数记录](market-adaptations.json)记录版本、内容哈希和观察方法；没有分发第三方脚本或正文。
