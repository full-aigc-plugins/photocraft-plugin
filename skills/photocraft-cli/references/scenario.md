# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 194 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `color` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `color.profileMismatch` | Embedded Profile Mismatch | `describe color.profileMismatch` |

### `command` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `command.list` | List Commands | `describe command.list` |

### `count` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `count.add` | Add Count | `describe count.add` |
| `count.remove` | Remove Count | `describe count.remove` |
| `count.move` | Move Count | `describe count.move` |
| `count.clear` | Clear Count | `describe count.clear` |
| `count.newGroup` | New Count Group | `describe count.newGroup` |
| `count.deleteGroup` | Delete Count Group | `describe count.deleteGroup` |
| `count.setGroup` | Count Group Options | `describe count.setGroup` |

### `edit` — 70

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `edit.undo` | Undo | `describe edit.undo` |
| `edit.redo` | Redo | `describe edit.redo` |
| `edit.fill` | Fill… | `describe edit.fill` |
| `edit.clear` | Clear | `describe edit.clear` |
| `edit.transform` | Free Transform | `describe edit.transform` |
| `edit.cut` | Cut | `describe edit.cut` |
| `edit.copy` | Copy | `describe edit.copy` |
| `edit.copyMerged` | Copy Merged | `describe edit.copyMerged` |
| `edit.paste` | Paste | `describe edit.paste` |
| `edit.pasteSpecial.pasteInPlace` | Paste in Place | `describe edit.pasteSpecial.pasteInPlace` |
| `edit.toggleLastState` | Toggle Last State | `describe edit.toggleLastState` |
| `edit.transform.again` | Again | `describe edit.transform.again` |
| `edit.assignProfile` | Assign Profile… | `describe edit.assignProfile` |
| `edit.convertToProfile` | Convert to Profile… | `describe edit.convertToProfile` |
| `edit.colorSettings` | Color Settings… | `describe edit.colorSettings` |
| `edit.profileInfo` | Profile Info | `describe edit.profileInfo` |
| `edit.stroke` | Stroke… | `describe edit.stroke` |
| `edit.transform.rotate180` | Rotate 180° | `describe edit.transform.rotate180` |
| `edit.transform.rotate90Cw` | Rotate 90° Clockwise | `describe edit.transform.rotate90Cw` |
| `edit.transform.rotate90Ccw` | Rotate 90° Counter Clockwise | `describe edit.transform.rotate90Ccw` |
| `edit.transform.flipHorizontal` | Flip Horizontal | `describe edit.transform.flipHorizontal` |
| `edit.transform.flipVertical` | Flip Vertical | `describe edit.transform.flipVertical` |
| `edit.pasteSpecial.pasteInto` | Paste Into | `describe edit.pasteSpecial.pasteInto` |
| `edit.pasteSpecial.pasteOutside` | Paste Outside | `describe edit.pasteSpecial.pasteOutside` |
| `edit.checkSpelling` | Check Spelling… | `describe edit.checkSpelling` |
| `edit.preferences.general` | General… | `describe edit.preferences.general` |
| `edit.preferences.interface` | Interface… | `describe edit.preferences.interface` |
| `edit.preferences.workspace` | Workspace… | `describe edit.preferences.workspace` |
| `edit.preferences.tools` | Tools… | `describe edit.preferences.tools` |
| `edit.preferences.historyLog` | History Log… | `describe edit.preferences.historyLog` |
| `edit.preferences.fileHandling` | File Handling… | `describe edit.preferences.fileHandling` |
| `edit.preferences.export` | Export… | `describe edit.preferences.export` |
| `edit.preferences.performance` | Performance… | `describe edit.preferences.performance` |
| `edit.preferences.scratchDisks` | Scratch Disks… | `describe edit.preferences.scratchDisks` |
| `edit.preferences.cursors` | Cursors… | `describe edit.preferences.cursors` |
| `edit.preferences.transparencyAndGamut` | Transparency & Gamut… | `describe edit.preferences.transparencyAndGamut` |
| `edit.preferences.unitsAndRulers` | Units & Rulers… | `describe edit.preferences.unitsAndRulers` |
| `edit.preferences.guidesGridAndSlices` | Guides, Grid & Slices… | `describe edit.preferences.guidesGridAndSlices` |
| `edit.preferences.plugIns` | Plug-ins… | `describe edit.preferences.plugIns` |
| `edit.preferences.type` | Type… | `describe edit.preferences.type` |
| `edit.preferences.enhancedControls` | Enhanced Controls… | `describe edit.preferences.enhancedControls` |
| `edit.preferences.rawDefaults` | Camera Raw… | `describe edit.preferences.rawDefaults` |
| `edit.preferences.integrations` | Integrations… | `describe edit.preferences.integrations` |
| `edit.keyboardShortcuts` | Keyboard Shortcuts… | `describe edit.keyboardShortcuts` |
| `edit.menus` | Menus… | `describe edit.menus` |
| `edit.toolbar` | Toolbar… | `describe edit.toolbar` |
| `edit.fade` | Fade… | `describe edit.fade` |
| `edit.purge.undo` | Undo | `describe edit.purge.undo` |
| `edit.purge.clipboard` | Clipboard | `describe edit.purge.clipboard` |
| `edit.purge.histories` | Histories | `describe edit.purge.histories` |
| `edit.purge.videoCache` | Video Cache | `describe edit.purge.videoCache` |
| `edit.purge.all` | All | `describe edit.purge.all` |
| `edit.contentAwareFill` | Content-Aware Fill… | `describe edit.contentAwareFill` |
| `edit.contentAwareScale` | Content-Aware Scale | `describe edit.contentAwareScale` |
| `edit.defineBrushPreset` | Define Brush Preset… | `describe edit.defineBrushPreset` |
| `edit.defineCustomShape` | Define Custom Shape… | `describe edit.defineCustomShape` |
| `edit.findAndReplaceText` | Find and Replace Text… | `describe edit.findAndReplaceText` |
| `edit.presets.presetManager` | Preset Manager… | `describe edit.presets.presetManager` |
| `edit.presets.exportImportPresets` | Export/Import Presets… | `describe edit.presets.exportImportPresets` |
| `edit.autoAlignLayers` | Auto-Align Layers… | `describe edit.autoAlignLayers` |
| `edit.autoBlendLayers` | Auto-Blend Layers… | `describe edit.autoBlendLayers` |
| `edit.definePattern` | Define Pattern… | `describe edit.definePattern` |
| `edit.transform.warp` | Warp | `describe edit.transform.warp` |
| `edit.transform.splitWarpCrosswise` | Split Warp Crosswise | `describe edit.transform.splitWarpCrosswise` |
| `edit.transform.splitWarpHorizontally` | Split Warp Horizontally | `describe edit.transform.splitWarpHorizontally` |
| `edit.transform.splitWarpVertically` | Split Warp Vertically | `describe edit.transform.splitWarpVertically` |
| `edit.transform.removeWarpSplit` | Remove Warp Split | `describe edit.transform.removeWarpSplit` |
| `edit.puppetWarp` | Puppet Warp | `describe edit.puppetWarp` |
| `edit.perspectiveWarp` | Perspective Warp | `describe edit.perspectiveWarp` |
| `edit.presets.migratePresets` | Migrate Presets | `describe edit.presets.migratePresets` |

### `gradient` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `gradient.presets.importGrd` | Import Gradients… | `describe gradient.presets.importGrd` |
| `gradient.presets.list` | Gradient Presets | `describe gradient.presets.list` |
| `gradient.presets.select` | Select Gradient | `describe gradient.presets.select` |
| `gradient.presets.apply` | New Gradient Fill Layer from Preset | `describe gradient.presets.apply` |
| `gradient.presets.new` | New Gradient Preset | `describe gradient.presets.new` |
| `gradient.presets.edit` | Edit Gradient Presets | `describe gradient.presets.edit` |
| `gradient.presets.reset` | Restore Default Gradients | `describe gradient.presets.reset` |

### `image` — 14

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `image.applyImage` | Apply Image… | `describe image.applyImage` |
| `image.calculations` | Calculations… | `describe image.calculations` |
| `image.analysis.setMeasurementScale` | Set Measurement Scale… | `describe image.analysis.setMeasurementScale` |
| `image.analysis.selectDataPoints` | Select Data Points… | `describe image.analysis.selectDataPoints` |
| `image.analysis.recordMeasurements` | Record Measurements | `describe image.analysis.recordMeasurements` |
| `image.analysis.rulerTool` | Ruler Tool | `describe image.analysis.rulerTool` |
| `image.analysis.countTool` | Count Tool | `describe image.analysis.countTool` |
| `image.analysis.placeScaleMarker` | Place Scale Marker… | `describe image.analysis.placeScaleMarker` |
| `image.analysis.straightenLayer` | Straighten Layer | `describe image.analysis.straightenLayer` |
| `image.analysis.info` | Analysis Info | `describe image.analysis.info` |
| `image.trap` | Trap… | `describe image.trap` |
| `image.variables.define` | Define… | `describe image.variables.define` |
| `image.variables.dataSets` | Data Sets… | `describe image.variables.dataSets` |
| `image.applyDataSet` | Apply Data Set… | `describe image.applyDataSet` |

### `measurementLog` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `measurementLog.list` | Measurement Log | `describe measurementLog.list` |
| `measurementLog.delete` | Delete Measurements | `describe measurementLog.delete` |
| `measurementLog.export` | Export Measurements… | `describe measurementLog.export` |

### `notes` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `notes.add` | New Note | `describe notes.add` |
| `notes.set` | Edit Note | `describe notes.set` |
| `notes.delete` | Delete Note | `describe notes.delete` |
| `notes.list` | Notes | `describe notes.list` |

### `path` — 8

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `path.list` | List Paths | `describe path.list` |
| `path.info` | Path Info | `describe path.info` |
| `path.set` | Set Path | `describe path.set` |
| `path.delete` | Delete Path | `describe path.delete` |
| `path.rename` | Rename Path | `describe path.rename` |
| `path.toSelection` | Make Selection from Path | `describe path.toSelection` |
| `path.fill` | Fill Path | `describe path.fill` |
| `path.stroke` | Stroke Path | `describe path.stroke` |

### `pattern` — 10

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `pattern.list` | Patterns | `describe pattern.list` |
| `pattern.rename` | Rename Pattern | `describe pattern.rename` |
| `pattern.delete` | Delete Pattern | `describe pattern.delete` |
| `pattern.import` | Import Patterns… | `describe pattern.import` |
| `pattern.export` | Export Patterns… | `describe pattern.export` |
| `pattern.presets.list` | Pattern Presets | `describe pattern.presets.list` |
| `pattern.presets.select` | Select Pattern | `describe pattern.presets.select` |
| `pattern.presets.apply` | New Pattern Fill Layer from Preset | `describe pattern.presets.apply` |
| `pattern.presets.new` | New Pattern Preset | `describe pattern.presets.new` |
| `pattern.presets.edit` | Edit Pattern Presets | `describe pattern.presets.edit` |

### `plugin` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `plugin.list` | List Plug-ins | `describe plugin.list` |
| `plugin.install` | Install Plug-in… | `describe plugin.install` |
| `plugin.remove` | Remove Plug-in | `describe plugin.remove` |
| `plugin.reload` | Reload Plug-ins | `describe plugin.reload` |
| `plugin.run` | Run Plug-in | `describe plugin.run` |

### `prefs` — 3

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `prefs.get` | Get Preferences | `describe prefs.get` |
| `prefs.set` | Set Preferences | `describe prefs.set` |
| `prefs.reset` | Reset Preferences | `describe prefs.reset` |

### `session` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `session.inspect` | Inspect Session | `describe session.inspect` |

### `shape` — 9

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `shape.create` | New Shape Layer | `describe shape.create` |
| `shape.edit` | Edit Shape | `describe shape.edit` |
| `shape.info` | Shape Layer Info | `describe shape.info` |
| `shape.rasterize` | Rasterize Shape | `describe shape.rasterize` |
| `shape.presets.list` | Shape Presets | `describe shape.presets.list` |
| `shape.presets.place` | Place Custom Shape | `describe shape.presets.place` |
| `shape.presets.new` | New Shape Preset | `describe shape.presets.new` |
| `shape.presets.edit` | Edit Shape Presets | `describe shape.presets.edit` |
| `shape.presets.reset` | Restore Default Shapes | `describe shape.presets.reset` |

### `slice` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `slice.new` | Slice Tool | `describe slice.new` |
| `slice.fromGuides` | Slices From Guides | `describe slice.fromGuides` |
| `slice.set` | Slice Options… | `describe slice.set` |
| `slice.promote` | Promote | `describe slice.promote` |
| `slice.delete` | Delete Slice | `describe slice.delete` |
| `slice.divide` | Divide Slice… | `describe slice.divide` |
| `slice.list` | List Slices | `describe slice.list` |

### `style` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `style.presets.list` | Style Presets | `describe style.presets.list` |
| `style.presets.apply` | Apply Style | `describe style.presets.apply` |
| `style.presets.new` | New Style… | `describe style.presets.new` |
| `style.presets.edit` | Edit Style Presets | `describe style.presets.edit` |
| `style.presets.reset` | Restore Default Styles | `describe style.presets.reset` |

### `timeline` — 7

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `timeline.create` | Create Video Timeline | `describe timeline.create` |
| `timeline.delete` | Delete Timeline | `describe timeline.delete` |
| `timeline.setFrame` | Go to Frame | `describe timeline.setFrame` |
| `timeline.nextFrame` | Next Frame | `describe timeline.nextFrame` |
| `timeline.previousFrame` | Previous Frame | `describe timeline.previousFrame` |
| `timeline.setProps` | Timeline Settings | `describe timeline.setProps` |
| `timeline.info` | Timeline Info | `describe timeline.info` |

### `tool` — 5

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `tool.presets.list` | Tool Presets | `describe tool.presets.list` |
| `tool.presets.new` | New Tool Preset… | `describe tool.presets.new` |
| `tool.presets.select` | Select Tool Preset | `describe tool.presets.select` |
| `tool.presets.edit` | Edit Tool Presets | `describe tool.presets.edit` |
| `tool.presets.reset` | Reset Tool Presets | `describe tool.presets.reset` |

### `tools` — 4

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `tools.setColors` | Set Colors | `describe tools.setColors` |
| `tools.swapColors` | Switch Foreground and Background Colors | `describe tools.swapColors` |
| `tools.defaultColors` | Default Foreground and Background Colors | `describe tools.defaultColors` |
| `tools.setBrush` | Set Brush | `describe tools.setBrush` |

### `variables` — 1

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `variables.list` | List Variables | `describe variables.list` |

### `view` — 22

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `view.newGuide` | New Guide… | `describe view.newGuide` |
| `view.moveGuide` | Move Guide | `describe view.moveGuide` |
| `view.deleteGuide` | Delete Guide | `describe view.deleteGuide` |
| `view.clearGuides` | Clear Guides | `describe view.clearGuides` |
| `view.proofSetup` | Proof Setup… | `describe view.proofSetup` |
| `view.proofColors` | Proof Colors | `describe view.proofColors` |
| `view.gamutWarning` | Gamut Warning | `describe view.gamutWarning` |
| `view.newGuideLayout` | New Guide Layout… | `describe view.newGuideLayout` |
| `view.newGuidesFromShape` | New Guides From Shape | `describe view.newGuidesFromShape` |
| `view.clearCanvasGuides` | Clear Canvas Guides | `describe view.clearCanvasGuides` |
| `view.clearSelectedArtboardGuides` | Clear Selected Artboard Guides | `describe view.clearSelectedArtboardGuides` |
| `view.proofSetup.workingCyanPlate` | Working Cyan Plate | `describe view.proofSetup.workingCyanPlate` |
| `view.proofSetup.workingMagentaPlate` | Working Magenta Plate | `describe view.proofSetup.workingMagentaPlate` |
| `view.proofSetup.workingYellowPlate` | Working Yellow Plate | `describe view.proofSetup.workingYellowPlate` |
| `view.proofSetup.workingBlackPlate` | Working Black Plate | `describe view.proofSetup.workingBlackPlate` |
| `view.proofSetup.workingCmyPlate` | Working CMY Plate | `describe view.proofSetup.workingCmyPlate` |
| `view.proofSetup.legacyMacintoshRgb` | Legacy Macintosh RGB | `describe view.proofSetup.legacyMacintoshRgb` |
| `view.proofSetup.colorBlindnessProtanopia` | Color Blindness — Protanopia-type | `describe view.proofSetup.colorBlindnessProtanopia` |
| `view.proofSetup.colorBlindnessDeuteranopia` | Color Blindness — Deuteranopia-type | `describe view.proofSetup.colorBlindnessDeuteranopia` |
| `view.thirtyTwoBitPreviewOptions` | 32-bit Preview Options… | `describe view.thirtyTwoBitPreviewOptions` |
| `view.lockSlices` | Lock Slices | `describe view.lockSlices` |
| `view.clearSlices` | Clear Slices | `describe view.clearSlices` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
