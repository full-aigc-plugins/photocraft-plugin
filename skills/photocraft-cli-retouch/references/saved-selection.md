# 持久选区、通道与局部蒙版 / Saved selections, channels and local masks

## 首次使用与前置状态 / First use and state

SKILL_DIR 必须指向宿主实际加载的本 SKILL.md 目录。本技能自带固定 CLI 安装器与 commands.py 查询／计划校验／同会话执行入口，不需要兄弟技能。输入为文档、区域、图层、颜色模式、允许修改对象与新输出目录；真实工程先读取摘要及当前图层和 channel.list。

选区是覆盖灰度，不是图层。当前固定原生 .pcraft 可以保存活动选区，并需重开核验；通道目标与可见性是视图状态。使用 select.saveSelection 将覆盖另存为命名 alpha 通道，可独立备份与复用多个区域，select.deselect 不会删除已保存通道。通道索引从真实返回值获得；名称也须确认唯一。选区 rect 使用 [x,y,width,height]，transformSelection.rect 使用 [x0,y0,x1,y1]，不能混用。

## 命令分类与场景 / Families and tasks

| 场景 | 命令 | 使用与核验 |
| --- | --- | --- |
| 范围建立与复用 | select.all、select.inverse、select.reselect、select.lasso | 同时核对 select.rect 和 select.deselect 参数；几何区域、antiAlias 与 feather 根据素材调整。反选及重选只影响当前会话，不代替持久保存 |
| 颜色与邻域选择 | select.magicWand、select.colorRange、select.grow、select.similar | 明确当前图层或 sampleAllLayers、tolerance/fuzziness、连续区域与增减模式。采样点用文档像素；输出覆盖和实际像素分别检查 |
| 主体与特征选择 | select.quick、select.object、select.subject、select.focusArea、select.sky | 给真实图像与区域，按当前 CLI 参数选择 mode 和采样来源；不能仅凭目录名称声称 AI 模型或语义分割验收。检测漂移、遗漏和错误背景 |
| 边界修改 | select.modify.border、select.modify.smooth、select.modify.expand、select.modify.contract、select.modify.feather、select.refineEdge | radius 用像素，feather 保留部分覆盖。refineEdge 的 output 可修改图层或蒙版；执行前明确授权和新图层范围，不能默认 destructive |
| 空间调整与矢量交接 | select.transformSelection、select.toWorkPath、select.convertToShape | transformSelection 只移动覆盖，不移动图像；非可逆变换拒绝。转换路径的 tolerance 是像素，检查轮廓误差与实际可编辑对象 |
| 图层面板筛选 | select.isolateLayers、select.allLayers、select.findLayers | 面板隔离与选区不同，findLayers 是名称子串，不把多匹配当作唯一目标；读取当前图层后选定真实 ID |
| 持久存取与快速蒙版 | select.saveSelection、select.loadSelection、select.editInQuickMaskMode | 保存返回 channel/document，new 与 replace/add/subtract/intersect 是不同写入范围。loadSelection 中 operation=invert 不存在，反相用 invert=true。快速蒙版需要进出模式核对目标 |
| 通道建立与管理 | channel.new、channel.newSpot、channel.duplicate、channel.delete、channel.rename、channel.move、channel.list | 新通道会改变编辑目标，返回合成前显式 channel.target.composite。duplicate 到新文档返回实际 document；索引随 move/delete 改变，禁止沿用旧编号 |
| 通道目标与显示 | channel.target、channel.target.composite、channel.setVisible、channel.options | target 决定像素／滤镜写入位置；可见性和覆盖数值分别检查。options 包括叠加颜色、opacity、indicates；spot 和普通 alpha 不同 |
| 通道快捷目标 | channel.target.slot3、channel.target.slot4、channel.target.slot5、channel.target.slot6、channel.target.slot7、channel.target.slot8、channel.target.slot9 | 快捷槽含义取决于颜色模式与已有通道。先 channel.list；不存在槽失败不能解释为安装失败，不猜 RGB、CMYK 与 Lab 的一致映射 |
| 专色与文档拆合 | channel.mergeSpot、channel.split、channel.merge | 这些操作可改变文档、像素和专色保真；先保存原生检查点。核对尺寸、模式和文档列表，打印专色、印刷分色与交换格式单独验收 |

Every owned selection/channel command is classified here. Use commands.py describe for exact parameters. Selection coverage, layer identity, edit target and channel visibility are separate state. The current native .pcraft format can preserve active selection. Named alpha channels separately retain reusable coverage after deselection. Smart-selection names do not establish AI segmentation acceptance. Split/merge and spot channels require separate fidelity checks.

## 自包含实例 / Self-contained workflow

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe select.saveSelection
python3 -I -B "$SKILL_DIR/scripts/commands.py" check "$SKILL_DIR/examples/saved-selection-create.json"
python3 -I -B "$SKILL_DIR/scripts/commands.py" run "$SKILL_DIR/examples/saved-selection-create.json" --output /absolute/new-selection-create
python3 -I -B "$SKILL_DIR/scripts/commands.py" run "$SKILL_DIR/examples/saved-selection-reopen.json" --input project=/absolute/new-selection-create/project.pcraft --output /absolute/new-selection-reopen
python3 -I -B "$SKILL_DIR/scripts/commands.py" run "$SKILL_DIR/examples/saved-selection-revise.json" --input project=/absolute/new-selection-create/project.pcraft --output /absolute/new-selection-revision
```

创建计划建立 128×80 RGB 8-bit 文档、灰色 Product 图形、绿色 Control 和可编辑亮度调整层。区域 [16,24,24,32] 羽化 2 像素，保存 Product Local alpha 通道并保留 Protected region 备份。恢复主通道覆盖、显式 channel.target.composite 后，为亮度 30 调整层建立蒙版。输出原生 project.pcraft、保留活动选区的 active-selection.pcraft 检查点、preview.png、selection-plane.png 和逐步回执。

selection-plane.png 通过 channel.duplicate 的 document=new 创建独立灰度文档并按返回 document 导出，不是通道面板截图。它用于检查羽化部分覆盖及重开一致。源工程先保存，再生成证明文档，避免把灰度文档当作原生交付工程。

重开计划先导出原画面，再恢复命名主通道。修订仅将覆盖右移 16 像素，replace 主通道并重建同一调整层蒙版，另存新工程；备份和图层内容保留。before.layers.0.id 只适用于本实例固定的最上方 Local brightness 调整层。真实任务须先核对目标 ID 与图层布局，不能将数组位置当作通用身份契约。输入材料、几何区域和亮度按实际任务调整。

The fixture saves feathered coverage into an alpha channel and keeps an untouched backup. It applies a masked editable brightness layer, saves the original native project, then exports the channel as a separate grayscale proof document. Reopen verifies pixels and channel coverage. Revision translates only the saved region and adjustment mask by 16 px. The fixture's top-layer index is not a general identity contract: observe actual targets for real projects.

## 核验、错误与交付 / Verification, failures and delivery

验收原生 manifest 的图层与通道内容、对应 tile 数据、灰度覆盖与复合像素；不能只看通道名称和 hasMask。无文档、未知通道、非法保存 operation 停止后续保存并保全输入；未知结果检查原回执，禁止自动重放修改。

本实例覆盖几何选区、羽化、通道存取及蒙版返工，不证明全部颜色模式／位深、智能选择、专色印刷、PSD通道保真、GUI和创作质量。固定发行与实际安装副本的首次使用验收单独记录。
