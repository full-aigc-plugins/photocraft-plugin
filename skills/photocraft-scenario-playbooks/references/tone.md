# PhotoCraft tone 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

## faded-gray-tones：褪色黑白照片灰阶恢复

输入：扫描保留灰阶层次；黑白点分布可检查。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 观察直方图后恢复中间调，黑白场不硬截断 | `layer.newAdjustmentLayer.levels` | `{"inBlack":5,"gamma":1.05,"inWhite":248}` |
| 3. 轻微抬升中间调而保留高光 | `layer.newAdjustmentLayer.curves` | `{"points":[[0,0],[64,60],[128,136],[192,198],[255,255]]}` |

检查：黑衣与头发仍有层次；纸面高光不变成纯白块。

边界：参数为低强度起点；需观察实际直方图，不能对所有旧照统一套黑白点。

## yellow-paper-neutralize：泛黄纸基色偏校正

输入：原图中存在可信中性参考，且用户希望减轻泛黄。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 先温和抵消偏黄色，再看肤色 | `layer.newAdjustmentLayer.colorBalance` | `{"midtones":[0,0,6],"preserveLuminosity":true}` |
| 3. 观察直方图后恢复中间调，黑白场不硬截断 | `layer.newAdjustmentLayer.levels` | `{"inBlack":5,"gamma":1.05,"inWhite":248}` |

检查：中性参考更接近灰；肤色与旧照片原有暖调不过分抹去。

边界：没有中性参考时保留年代色调，白衣不一定是纯白。

## red-cast-aging：老彩照偏红衰变校正

输入：红通道偏移可由中性物体和其他通道比较确认。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 用红通道曲线做小幅中间调校正 | `layer.newAdjustmentLayer.curves` | `{"red":[[0,0],[128,120],[255,255]]}` |

检查：白色与肤色更自然；绿色和蓝色区域没有异常变色。

边界：颜色衰变不等于缺失通道可完全恢复。

## bw-conversion-preserve：旧彩照转黑白并保留层次

输入：用户明确需要黑白版本；原彩色文件另留。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 使用可编辑黑白调整层而非破坏性去色 | `layer.newAdjustmentLayer.blackWhite` | `{"reds":40,"yellows":60,"greens":40,"cyans":60,"blues":20,"magentas":80}` |

检查：肤色与背景在灰度上可区分；红绿物体不会并成一块。

边界：不把转黑白当色偏修复；彩色原版继续保留。

## duotone-editorial：编辑插图双色映射

输入：明确属于风格化插图交付，不要求保留真实颜色。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 先用可编辑渐变映射建立双色 | `layer.newAdjustmentLayer.gradientMap` | `{"stops":[[0,"#1b2540"],[1,"#f1dab1"]],"dither":true}` |

检查：暗部与高光仍分离；标题叠加区域对比足够。

边界：双色版与真实色彩版分开命名，不覆盖原图。

## black-white-selective-channel：彩色人像黑白通道混合

输入：要求黑白艺术版，红色衣物与肤色需分离层次。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"B&W channel mix"}` |
| 2. 无选区时创建整体可编辑黑白调整层 | `layer.newAdjustmentLayer.blackWhite` | `{"reds":45,"yellows":65,"greens":40,"cyans":55,"blues":15,"magentas":65}` |

检查：RGB三个通道相等或接近；肤色与衣物灰阶可分；原彩色像素图层保留。

边界：这是有意黑白转换；不能把固定通道权重当成所有肤色的标准。

## selective-accent-color：保留指定物体彩色其余转黑白

输入：用户明确要求选择性色彩创作，主体颜色与背景区域均可定位。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原始像素，复制并激活工作层 | `layer.duplicate` | `{"name":"Selective color"}` |
| 2. 按实际目标轮廓定位；此处为256×192测试矩形 | `select.rect` | `{"x":88,"y":56,"width":80,"height":96,"mode":"replace","feather":1}` |
| 3. 反选到非主体区 | `select.inverse` | `{}` |
| 4. 以反选区蒙版创建黑白调整层 | `layer.newAdjustmentLayer.blackWhite` | `{}` |
| 5. 结束局部操作，清除活动选区 | `select.deselect` | `{}` |

检查：主体中心RGB保持；背景转为灰阶；边缘没有遗漏彩点。

边界：这属于风格化处理；主体轮廓按实图替换，矩形不能用于毛发边缘。

