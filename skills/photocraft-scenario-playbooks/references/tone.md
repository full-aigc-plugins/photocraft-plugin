# PhotoCraft tone 场景

以下参数是256×192示例坐标/低强度起点。先检查当前输入、对象和命令参数；按实际损伤重算坐标，不得直接套用。

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

