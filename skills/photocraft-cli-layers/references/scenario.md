# 图层合成操作指南

## 目标与前置

组织产品、背景、文本与图层组，调整混合和层级。保持产品、文本、背景可分开编辑；不要为了导出提前 flatten 原工程。

先检查需求中的工程格式、目标对象、素材摘要、字体与输出约束。输入不完整时继续只读调查，但不猜测依赖它的参数。

## 当前版本命令入口

从 `commands --json --filter <关键词>` 读取 params；`run <工程> --cmd <id> --params <JSON> ... --out <新工程.pcraft>`，每个 --params 属于前一个 --cmd；serve/MCP 可保持单会话。

| 命令 ID | 目录标签 |
| :--- | :--- |
| `layer.new.layer` | Layer… |
| `layer.new.group` | Group… |
| `layer.groupLayers` | Group Layers |
| `layer.duplicate` | Duplicate Layer… |
| `layer.delete` | Delete Layer |
| `layer.select` | Select Layer |
| `layer.setProps` | Layer Properties |
| `layer.arrange.bringForward` | Bring Forward |

完整候选参数见本技能 commands.json；enabled 是空会话观察，打开目标工程后必须重查。命令参数 schema 存在不证明它在全部素材与平台有效。

## 执行与验收

1. 保存原生检查点、读取对象 ID 和参数值；已有素材先核验引用。
2. 构造当前版本命令参数；一次只改变请求的属性或对象。连续创建 ID 使用实际回执或同一会话。
3. 保存新原生工程、重新打开，比较目标参数和未修改对象。需要输出时检查帧、像素、音频或矢量结构。
4. 原生工程、素材清单、预览/导出及交换报告交付；技术核验和视觉审核分开记录。

首次组合实例采用本技能 examples 与 references/workflow.md。此实例验证组合能力，不替代所有候选命令的逐项验收。失败保留检查点，不将无损原生交付替换成扁平结果。

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 152 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `layer` — 139

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `layer.new.layer` | Layer… | `describe layer.new.layer` |
| `layer.new.group` | Group… | `describe layer.new.group` |
| `layer.groupLayers` | Group Layers | `describe layer.groupLayers` |
| `layer.duplicate` | Duplicate Layer… | `describe layer.duplicate` |
| `layer.delete` | Delete Layer | `describe layer.delete` |
| `layer.setProps` | Layer Properties | `describe layer.setProps` |
| `layer.arrange.bringForward` | Bring Forward | `describe layer.arrange.bringForward` |
| `layer.arrange.sendBackward` | Send Backward | `describe layer.arrange.sendBackward` |
| `layer.arrange.bringToFront` | Bring to Front | `describe layer.arrange.bringToFront` |
| `layer.arrange.sendToBack` | Send to Back | `describe layer.arrange.sendToBack` |
| `layer.mergeDown` | Merge Down | `describe layer.mergeDown` |
| `layer.flattenImage` | Flatten Image | `describe layer.flattenImage` |
| `layer.newFillLayer.solidColor` | Solid Color… | `describe layer.newFillLayer.solidColor` |
| `layer.newFillLayer.gradient` | Gradient… | `describe layer.newFillLayer.gradient` |
| `layer.moveTo` | Reorder Layer | `describe layer.moveTo` |
| `layer.translate` | Move Layer | `describe layer.translate` |
| `layer.layerStyle.dropShadow` | Drop Shadow… | `describe layer.layerStyle.dropShadow` |
| `layer.layerStyle.innerShadow` | Inner Shadow… | `describe layer.layerStyle.innerShadow` |
| `layer.layerStyle.outerGlow` | Outer Glow… | `describe layer.layerStyle.outerGlow` |
| `layer.layerStyle.innerGlow` | Inner Glow… | `describe layer.layerStyle.innerGlow` |
| `layer.layerStyle.stroke` | Stroke… | `describe layer.layerStyle.stroke` |
| `layer.layerStyle.colorOverlay` | Color Overlay… | `describe layer.layerStyle.colorOverlay` |
| `layer.layerStyle.gradientOverlay` | Gradient Overlay… | `describe layer.layerStyle.gradientOverlay` |
| `layer.layerStyle.patternOverlay` | Pattern Overlay… | `describe layer.layerStyle.patternOverlay` |
| `layer.layerStyle.bevelEmboss` | Bevel & Emboss… | `describe layer.layerStyle.bevelEmboss` |
| `layer.layerStyle.satin` | Satin… | `describe layer.layerStyle.satin` |
| `layer.layerStyle.clear` | Clear Layer Style | `describe layer.layerStyle.clear` |
| `layer.rasterize.vectorMask` | Rasterize Vector Mask | `describe layer.rasterize.vectorMask` |
| `layer.rasterize.shape` | Rasterize Shape | `describe layer.rasterize.shape` |
| `layer.combineShapes.unite` | Unite Shapes | `describe layer.combineShapes.unite` |
| `layer.combineShapes.subtractFrontShape` | Subtract Front Shape | `describe layer.combineShapes.subtractFrontShape` |
| `layer.combineShapes.intersectShapeAreas` | Intersect Shape Areas | `describe layer.combineShapes.intersectShapeAreas` |
| `layer.combineShapes.excludeOverlappingShapes` | Exclude Overlapping Shapes | `describe layer.combineShapes.excludeOverlappingShapes` |
| `layer.combineShapes.mergeShapeComponents` | Merge Shape Components | `describe layer.combineShapes.mergeShapeComponents` |
| `layer.new.layerViaCopy` | Layer via Copy | `describe layer.new.layerViaCopy` |
| `layer.new.layerViaCut` | Layer via Cut | `describe layer.new.layerViaCut` |
| `layer.mergeVisible` | Merge Visible | `describe layer.mergeVisible` |
| `layer.new.layerFromBackground` | Layer From Background… | `describe layer.new.layerFromBackground` |
| `layer.layerStyle.copyLayerStyle` | Copy Layer Style | `describe layer.layerStyle.copyLayerStyle` |
| `layer.layerStyle.pasteLayerStyle` | Paste Layer Style | `describe layer.layerStyle.pasteLayerStyle` |
| `layer.layerStyle.hideAllEffects` | Hide All Effects | `describe layer.layerStyle.hideAllEffects` |
| `layer.layerStyle.showAllEffects` | Show All Effects | `describe layer.layerStyle.showAllEffects` |
| `layer.rasterize.layer` | Layer | `describe layer.rasterize.layer` |
| `layer.rasterize.allLayers` | All Layers | `describe layer.rasterize.allLayers` |
| `layer.rasterize.type` | Type | `describe layer.rasterize.type` |
| `layer.rasterize.fillContent` | Fill Content | `describe layer.rasterize.fillContent` |
| `layer.rasterize.smartObject` | Smart Object | `describe layer.rasterize.smartObject` |
| `layer.delete.hiddenLayers` | Hidden Layers | `describe layer.delete.hiddenLayers` |
| `layer.ungroupLayers` | Ungroup Layers | `describe layer.ungroupLayers` |
| `layer.hideLayers` | Hide Layers | `describe layer.hideLayers` |
| `layer.showLayers` | Show Layers | `describe layer.showLayers` |
| `layer.smartObjects.convertToSmartObject` | Convert to Smart Object | `describe layer.smartObjects.convertToSmartObject` |
| `layer.smartObjects.newSmartObjectViaCopy` | New Smart Object via Copy | `describe layer.smartObjects.newSmartObjectViaCopy` |
| `layer.smartObjects.rasterize` | Rasterize | `describe layer.smartObjects.rasterize` |
| `layer.smartObjects.editContents` | Edit Contents | `describe layer.smartObjects.editContents` |
| `layer.smartObjects.saveContents` | Save Contents | `describe layer.smartObjects.saveContents` |
| `layer.smartObjects.replaceContents` | Replace Contents… | `describe layer.smartObjects.replaceContents` |
| `layer.smartObjects.exportContents` | Export Contents… | `describe layer.smartObjects.exportContents` |
| `layer.smartObjects.relinkToFile` | Relink to File… | `describe layer.smartObjects.relinkToFile` |
| `layer.smartObjects.updateModifiedContent` | Update Modified Content | `describe layer.smartObjects.updateModifiedContent` |
| `layer.smartObjects.updateAllModifiedContent` | Update All Modified Content | `describe layer.smartObjects.updateAllModifiedContent` |
| `layer.smartObjects.convertToEmbedded` | Convert to Embedded | `describe layer.smartObjects.convertToEmbedded` |
| `layer.smartObjects.convertToLinked` | Convert to Linked… | `describe layer.smartObjects.convertToLinked` |
| `layer.smartFilter.disableSmartFilters` | Disable Smart Filters | `describe layer.smartFilter.disableSmartFilters` |
| `layer.smartFilter.deleteFilterMask` | Delete Filter Mask | `describe layer.smartFilter.deleteFilterMask` |
| `layer.smartFilter.disableFilterMask` | Disable Filter Mask | `describe layer.smartFilter.disableFilterMask` |
| `layer.smartFilter.blendingOptions` | Blending Options… | `describe layer.smartFilter.blendingOptions` |
| `layer.smartFilter.clearSmartFilters` | Clear Smart Filters | `describe layer.smartFilter.clearSmartFilters` |
| `layer.smartFilter.setVisible` | Show/Hide Smart Filter | `describe layer.smartFilter.setVisible` |
| `layer.smartFilter.setParams` | Edit Smart Filter | `describe layer.smartFilter.setParams` |
| `layer.smartFilter.delete` | Delete Smart Filter | `describe layer.smartFilter.delete` |
| `layer.smartFilter.move` | Move Smart Filter | `describe layer.smartFilter.move` |
| `layer.align.topEdges` | Top Edges | `describe layer.align.topEdges` |
| `layer.align.verticalCenters` | Vertical Centers | `describe layer.align.verticalCenters` |
| `layer.align.bottomEdges` | Bottom Edges | `describe layer.align.bottomEdges` |
| `layer.align.leftEdges` | Left Edges | `describe layer.align.leftEdges` |
| `layer.align.horizontalCenters` | Horizontal Centers | `describe layer.align.horizontalCenters` |
| `layer.align.rightEdges` | Right Edges | `describe layer.align.rightEdges` |
| `layer.distribute.topEdges` | Top Edges | `describe layer.distribute.topEdges` |
| `layer.distribute.verticalCenters` | Vertical Centers | `describe layer.distribute.verticalCenters` |
| `layer.distribute.bottomEdges` | Bottom Edges | `describe layer.distribute.bottomEdges` |
| `layer.distribute.leftEdges` | Left Edges | `describe layer.distribute.leftEdges` |
| `layer.distribute.horizontalCenters` | Horizontal Centers | `describe layer.distribute.horizontalCenters` |
| `layer.distribute.rightEdges` | Right Edges | `describe layer.distribute.rightEdges` |
| `layer.distribute.horizontally` | Horizontally | `describe layer.distribute.horizontally` |
| `layer.distribute.vertically` | Vertically | `describe layer.distribute.vertically` |
| `layer.linkLayers` | Link Layers | `describe layer.linkLayers` |
| `layer.mergeLayers` | Merge Layers | `describe layer.mergeLayers` |
| `layer.new.groupFromLayers` | Group from Layers… | `describe layer.new.groupFromLayers` |
| `layer.arrange.reverse` | Reverse | `describe layer.arrange.reverse` |
| `layer.lockLayers` | Lock Layers… | `describe layer.lockLayers` |
| `layer.renameLayer` | Rename Layer | `describe layer.renameLayer` |
| `layer.maskAllObjects` | Mask All Objects | `describe layer.maskAllObjects` |
| `layer.matting.defringe` | Defringe… | `describe layer.matting.defringe` |
| `layer.matting.removeBlackMatte` | Remove Black Matte | `describe layer.matting.removeBlackMatte` |
| `layer.matting.removeWhiteMatte` | Remove White Matte | `describe layer.matting.removeWhiteMatte` |
| `layer.matting.colorDecontaminate` | Color Decontaminate… | `describe layer.matting.colorDecontaminate` |
| `layer.smartObjects.stackMode.entropy` | Entropy | `describe layer.smartObjects.stackMode.entropy` |
| `layer.smartObjects.stackMode.kurtosis` | Kurtosis | `describe layer.smartObjects.stackMode.kurtosis` |
| `layer.smartObjects.stackMode.maximum` | Maximum | `describe layer.smartObjects.stackMode.maximum` |
| `layer.smartObjects.stackMode.mean` | Mean | `describe layer.smartObjects.stackMode.mean` |
| `layer.smartObjects.stackMode.median` | Median | `describe layer.smartObjects.stackMode.median` |
| `layer.smartObjects.stackMode.minimum` | Minimum | `describe layer.smartObjects.stackMode.minimum` |
| `layer.smartObjects.stackMode.range` | Range | `describe layer.smartObjects.stackMode.range` |
| `layer.smartObjects.stackMode.skewness` | Skewness | `describe layer.smartObjects.stackMode.skewness` |
| `layer.smartObjects.stackMode.standardDeviation` | Standard Deviation | `describe layer.smartObjects.stackMode.standardDeviation` |
| `layer.smartObjects.stackMode.summation` | Summation | `describe layer.smartObjects.stackMode.summation` |
| `layer.smartObjects.stackMode.variance` | Variance | `describe layer.smartObjects.stackMode.variance` |
| `layer.smartObjects.stackMode.none` | None | `describe layer.smartObjects.stackMode.none` |
| `layer.smartObjects.revealInFinder` | Reveal in Finder | `describe layer.smartObjects.revealInFinder` |
| `layer.layerStyle.blendingOptions` | Blending Options… | `describe layer.layerStyle.blendingOptions` |
| `layer.layerStyle.globalLight` | Global Light… | `describe layer.layerStyle.globalLight` |
| `layer.layerStyle.createLayer` | Create Layer | `describe layer.layerStyle.createLayer` |
| `layer.layerStyle.scaleEffects` | Scale Effects… | `describe layer.layerStyle.scaleEffects` |
| `layer.layerContentOptions` | Layer Content Options… | `describe layer.layerContentOptions` |
| `layer.newFillLayer.pattern` | Pattern… | `describe layer.newFillLayer.pattern` |
| `layer.smartObjects.warp` | Warp | `describe layer.smartObjects.warp` |
| `layer.new.artboard` | Artboard… | `describe layer.new.artboard` |
| `layer.new.artboardFromGroup` | Artboard from Group… | `describe layer.new.artboardFromGroup` |
| `layer.new.artboardFromLayers` | Artboard from Layers… | `describe layer.new.artboardFromLayers` |
| `layer.artboard.set` | Edit Artboard | `describe layer.artboard.set` |
| `layer.smartObjects.puppetWarp` | Puppet Warp | `describe layer.smartObjects.puppetWarp` |
| `layer.smartObjects.perspectiveWarp` | Perspective Warp | `describe layer.smartObjects.perspectiveWarp` |
| `layer.newLayerBasedSlice` | New Layer Based Slice | `describe layer.newLayerBasedSlice` |
| `layer.pickAt` | Auto-Select Layer | `describe layer.pickAt` |
| `layer.new.frameFromLayers` | Frame from Layers | `describe layer.new.frameFromLayers` |
| `layer.videoLayers.newBlankVideoLayer` | New Blank Video Layer | `describe layer.videoLayers.newBlankVideoLayer` |
| `layer.videoLayers.insertBlankFrame` | Insert Blank Frame | `describe layer.videoLayers.insertBlankFrame` |
| `layer.videoLayers.duplicateFrame` | Duplicate Frame | `describe layer.videoLayers.duplicateFrame` |
| `layer.videoLayers.deleteFrame` | Delete Frame | `describe layer.videoLayers.deleteFrame` |
| `layer.videoLayers.restoreFrame` | Restore Frame | `describe layer.videoLayers.restoreFrame` |
| `layer.videoLayers.restoreAllFrames` | Restore All Frames | `describe layer.videoLayers.restoreAllFrames` |
| `layer.videoLayers.showAlteredVideo` | Show Altered Video | `describe layer.videoLayers.showAlteredVideo` |
| `layer.videoLayers.rasterize` | Rasterize | `describe layer.videoLayers.rasterize` |
| `layer.rasterize.video` | Video | `describe layer.rasterize.video` |
| `layer.videoLayers.newVideoLayerFromFile` | New Video Layer from File… | `describe layer.videoLayers.newVideoLayerFromFile` |
| `layer.videoLayers.replaceFootage` | Replace Footage… | `describe layer.videoLayers.replaceFootage` |
| `layer.videoLayers.interpretFootage` | Interpret Footage… | `describe layer.videoLayers.interpretFootage` |
| `layer.videoLayers.reloadFrame` | Reload Frame | `describe layer.videoLayers.reloadFrame` |

### `layerComp` — 13

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `layerComp.new` | New Layer Comp… | `describe layerComp.new` |
| `layerComp.update` | Update Layer Comp | `describe layerComp.update` |
| `layerComp.apply` | Apply Layer Comp | `describe layerComp.apply` |
| `layerComp.previous` | Apply Previous Layer Comp | `describe layerComp.previous` |
| `layerComp.next` | Apply Next Layer Comp | `describe layerComp.next` |
| `layerComp.delete` | Delete Layer Comp | `describe layerComp.delete` |
| `layerComp.duplicate` | Duplicate Layer Comp | `describe layerComp.duplicate` |
| `layerComp.rename` | Rename Layer Comp | `describe layerComp.rename` |
| `layerComp.setComment` | Layer Comp Comment | `describe layerComp.setComment` |
| `layerComp.setOptions` | Layer Comp Options… | `describe layerComp.setOptions` |
| `layerComp.restoreLastDocumentState` | Restore Last Document State | `describe layerComp.restoreLastDocumentState` |
| `layerComp.updateWarnings` | Layer Comp Warnings | `describe layerComp.updateWarnings` |
| `layerComp.list` | List Layer Comps | `describe layerComp.list` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
