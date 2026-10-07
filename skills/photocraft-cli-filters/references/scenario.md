# 通用命令操作指南 / General command guide

<!-- COMPLETE_SCENARIO_COMMANDS_START -->

## 完整归属清单 / Complete assigned command list

本技能归属 122 条命令。下面按命令族分组；上述短表若存在，仅是示例。归属按最长前缀确定，实际任务可组合其他能力的命令。

Each command below has a parameter contract in this skill’s `command-reference.md`. Assignment uses the most specific prefix; a task can combine commands from multiple capabilities.

执行顺序：检查工程和选中对象 → `commands.py describe COMMAND_ID` → 根据参数说明构造计划 → `commands.py check PLAN.json` → `commands.py run PLAN.json --output NEW_DIRECTORY` → 保存并重开原生工程、核验目标修改和非目标内容。涉及 GUI 时按 `command-usage.md` 选择 bridge 模式。

Order: inspect project and selection, describe parameters, construct and check the plan, run it, save and reopen the native project, then verify requested and unaffected content. Follow `command-usage.md` for bridge mode.

这些是命令使用入口，不能把分类或计划校验当作实际执行成功；禁用项必须重新查询上下文，超时不得直接重放。 / Classification and preflight do not prove execution acceptance. Re-query disabled commands and reconcile timed-out operations before retry.

### `filter` — 122

| 命令 / Command | 用途 / Label | 参数入口 / Parameters |
| --- | --- | --- |
| `filter.blur.gaussianBlur` | Gaussian Blur… | `describe filter.blur.gaussianBlur` |
| `filter.blur.blur` | Blur | `describe filter.blur.blur` |
| `filter.blur.blurMore` | Blur More | `describe filter.blur.blurMore` |
| `filter.sharpen.sharpen` | Sharpen | `describe filter.sharpen.sharpen` |
| `filter.sharpen.sharpenMore` | Sharpen More | `describe filter.sharpen.sharpenMore` |
| `filter.sharpen.sharpenEdges` | Sharpen Edges | `describe filter.sharpen.sharpenEdges` |
| `filter.noise.despeckle` | Despeckle | `describe filter.noise.despeckle` |
| `filter.blur.boxBlur` | Box Blur… | `describe filter.blur.boxBlur` |
| `filter.blur.motionBlur` | Motion Blur… | `describe filter.blur.motionBlur` |
| `filter.blur.radialBlur` | Radial Blur… | `describe filter.blur.radialBlur` |
| `filter.blur.surfaceBlur` | Surface Blur… | `describe filter.blur.surfaceBlur` |
| `filter.sharpen.unsharpMask` | Unsharp Mask… | `describe filter.sharpen.unsharpMask` |
| `filter.sharpen.smartSharpen` | Smart Sharpen… | `describe filter.sharpen.smartSharpen` |
| `filter.noise.addNoise` | Add Noise… | `describe filter.noise.addNoise` |
| `filter.noise.median` | Median… | `describe filter.noise.median` |
| `filter.noise.dustAndScratches` | Dust & Scratches… | `describe filter.noise.dustAndScratches` |
| `filter.pixelate.mosaic` | Mosaic… | `describe filter.pixelate.mosaic` |
| `filter.stylize.emboss` | Emboss… | `describe filter.stylize.emboss` |
| `filter.stylize.findEdges` | Find Edges | `describe filter.stylize.findEdges` |
| `filter.stylize.solarize` | Solarize | `describe filter.stylize.solarize` |
| `filter.distort.twirl` | Twirl… | `describe filter.distort.twirl` |
| `filter.distort.pinch` | Pinch… | `describe filter.distort.pinch` |
| `filter.distort.spherize` | Spherize… | `describe filter.distort.spherize` |
| `filter.distort.wave` | Wave… | `describe filter.distort.wave` |
| `filter.distort.ripple` | Ripple… | `describe filter.distort.ripple` |
| `filter.distort.polarCoordinates` | Polar Coordinates… | `describe filter.distort.polarCoordinates` |
| `filter.other.highPass` | High Pass… | `describe filter.other.highPass` |
| `filter.other.minimum` | Minimum… | `describe filter.other.minimum` |
| `filter.other.maximum` | Maximum… | `describe filter.other.maximum` |
| `filter.other.offset` | Offset… | `describe filter.other.offset` |
| `filter.lastFilter` | Last Filter | `describe filter.lastFilter` |
| `filter.pixelate.colorHalftone` | Color Halftone… | `describe filter.pixelate.colorHalftone` |
| `filter.pixelate.crystallize` | Crystallize… | `describe filter.pixelate.crystallize` |
| `filter.pixelate.facet` | Facet | `describe filter.pixelate.facet` |
| `filter.pixelate.fragment` | Fragment | `describe filter.pixelate.fragment` |
| `filter.pixelate.mezzotint` | Mezzotint… | `describe filter.pixelate.mezzotint` |
| `filter.pixelate.pointillize` | Pointillize… | `describe filter.pixelate.pointillize` |
| `filter.stylize.diffuse` | Diffuse… | `describe filter.stylize.diffuse` |
| `filter.stylize.extrude` | Extrude… | `describe filter.stylize.extrude` |
| `filter.stylize.oilPaint` | Oil Paint… | `describe filter.stylize.oilPaint` |
| `filter.stylize.tiles` | Tiles… | `describe filter.stylize.tiles` |
| `filter.stylize.traceContour` | Trace Contour… | `describe filter.stylize.traceContour` |
| `filter.stylize.wind` | Wind… | `describe filter.stylize.wind` |
| `filter.distort.displace` | Displace… | `describe filter.distort.displace` |
| `filter.distort.shear` | Shear… | `describe filter.distort.shear` |
| `filter.distort.zigZag` | ZigZag… | `describe filter.distort.zigZag` |
| `filter.render.fibers` | Fibers… | `describe filter.render.fibers` |
| `filter.render.lensFlare` | Lens Flare… | `describe filter.render.lensFlare` |
| `filter.render.lightingEffects` | Lighting Effects… | `describe filter.render.lightingEffects` |
| `filter.noise.reduceNoise` | Reduce Noise… | `describe filter.noise.reduceNoise` |
| `filter.blur.smartBlur` | Smart Blur… | `describe filter.blur.smartBlur` |
| `filter.blur.lensBlur` | Lens Blur… | `describe filter.blur.lensBlur` |
| `filter.blur.shapeBlur` | Shape Blur… | `describe filter.blur.shapeBlur` |
| `filter.blurGallery.tiltShift` | Tilt-Shift… | `describe filter.blurGallery.tiltShift` |
| `filter.blurGallery.irisBlur` | Iris Blur… | `describe filter.blurGallery.irisBlur` |
| `filter.blurGallery.fieldBlur` | Field Blur… | `describe filter.blurGallery.fieldBlur` |
| `filter.blurGallery.spinBlur` | Spin Blur… | `describe filter.blurGallery.spinBlur` |
| `filter.blurGallery.pathBlur` | Path Blur… | `describe filter.blurGallery.pathBlur` |
| `filter.other.custom` | Custom… | `describe filter.other.custom` |
| `filter.other.hsbHsl` | HSB/HSL | `describe filter.other.hsbHsl` |
| `filter.video.deInterlace` | De-Interlace… | `describe filter.video.deInterlace` |
| `filter.video.ntscColors` | NTSC Colors | `describe filter.video.ntscColors` |
| `filter.filterGallery` | Filter Gallery… | `describe filter.filterGallery` |
| `filter.gallery.coloredPencil` | Colored Pencil | `describe filter.gallery.coloredPencil` |
| `filter.gallery.cutout` | Cutout | `describe filter.gallery.cutout` |
| `filter.gallery.dryBrush` | Dry Brush | `describe filter.gallery.dryBrush` |
| `filter.gallery.filmGrain` | Film Grain | `describe filter.gallery.filmGrain` |
| `filter.gallery.fresco` | Fresco | `describe filter.gallery.fresco` |
| `filter.gallery.neonGlow` | Neon Glow | `describe filter.gallery.neonGlow` |
| `filter.gallery.paintDaubs` | Paint Daubs | `describe filter.gallery.paintDaubs` |
| `filter.gallery.paletteKnife` | Palette Knife | `describe filter.gallery.paletteKnife` |
| `filter.gallery.plasticWrap` | Plastic Wrap | `describe filter.gallery.plasticWrap` |
| `filter.gallery.posterEdges` | Poster Edges | `describe filter.gallery.posterEdges` |
| `filter.gallery.roughPastels` | Rough Pastels | `describe filter.gallery.roughPastels` |
| `filter.gallery.smudgeStick` | Smudge Stick | `describe filter.gallery.smudgeStick` |
| `filter.gallery.sponge` | Sponge | `describe filter.gallery.sponge` |
| `filter.gallery.underpainting` | Underpainting | `describe filter.gallery.underpainting` |
| `filter.gallery.watercolor` | Watercolor | `describe filter.gallery.watercolor` |
| `filter.gallery.accentedEdges` | Accented Edges | `describe filter.gallery.accentedEdges` |
| `filter.gallery.angledStrokes` | Angled Strokes | `describe filter.gallery.angledStrokes` |
| `filter.gallery.crosshatch` | Crosshatch | `describe filter.gallery.crosshatch` |
| `filter.gallery.darkStrokes` | Dark Strokes | `describe filter.gallery.darkStrokes` |
| `filter.gallery.inkOutlines` | Ink Outlines | `describe filter.gallery.inkOutlines` |
| `filter.gallery.spatter` | Spatter | `describe filter.gallery.spatter` |
| `filter.gallery.sprayedStrokes` | Sprayed Strokes | `describe filter.gallery.sprayedStrokes` |
| `filter.gallery.sumiE` | Sumi-e | `describe filter.gallery.sumiE` |
| `filter.gallery.diffuseGlow` | Diffuse Glow | `describe filter.gallery.diffuseGlow` |
| `filter.gallery.glass` | Glass | `describe filter.gallery.glass` |
| `filter.gallery.oceanRipple` | Ocean Ripple | `describe filter.gallery.oceanRipple` |
| `filter.gallery.basRelief` | Bas Relief | `describe filter.gallery.basRelief` |
| `filter.gallery.chalkCharcoal` | Chalk & Charcoal | `describe filter.gallery.chalkCharcoal` |
| `filter.gallery.charcoal` | Charcoal | `describe filter.gallery.charcoal` |
| `filter.gallery.chrome` | Chrome | `describe filter.gallery.chrome` |
| `filter.gallery.conteCrayon` | Conté Crayon | `describe filter.gallery.conteCrayon` |
| `filter.gallery.graphicPen` | Graphic Pen | `describe filter.gallery.graphicPen` |
| `filter.gallery.halftonePattern` | Halftone Pattern | `describe filter.gallery.halftonePattern` |
| `filter.gallery.notePaper` | Note Paper | `describe filter.gallery.notePaper` |
| `filter.gallery.photocopy` | Photocopy | `describe filter.gallery.photocopy` |
| `filter.gallery.plaster` | Plaster | `describe filter.gallery.plaster` |
| `filter.gallery.reticulation` | Reticulation | `describe filter.gallery.reticulation` |
| `filter.gallery.stamp` | Stamp | `describe filter.gallery.stamp` |
| `filter.gallery.tornEdges` | Torn Edges | `describe filter.gallery.tornEdges` |
| `filter.gallery.waterPaper` | Water Paper | `describe filter.gallery.waterPaper` |
| `filter.gallery.glowingEdges` | Glowing Edges | `describe filter.gallery.glowingEdges` |
| `filter.gallery.craquelure` | Craquelure | `describe filter.gallery.craquelure` |
| `filter.gallery.grain` | Grain | `describe filter.gallery.grain` |
| `filter.gallery.mosaicTiles` | Mosaic Tiles | `describe filter.gallery.mosaicTiles` |
| `filter.gallery.patchwork` | Patchwork | `describe filter.gallery.patchwork` |
| `filter.gallery.stainedGlass` | Stained Glass | `describe filter.gallery.stainedGlass` |
| `filter.gallery.texturizer` | Texturizer | `describe filter.gallery.texturizer` |
| `filter.blur.average` | Average | `describe filter.blur.average` |
| `filter.render.clouds` | Clouds | `describe filter.render.clouds` |
| `filter.render.differenceClouds` | Difference Clouds | `describe filter.render.differenceClouds` |
| `filter.convertForSmartFilters` | Convert for Smart Filters | `describe filter.convertForSmartFilters` |
| `filter.lensCorrection` | Lens Correction… | `describe filter.lensCorrection` |
| `filter.adaptiveWideAngle` | Adaptive Wide Angle… | `describe filter.adaptiveWideAngle` |
| `filter.cameraRaw` | Camera Raw Filter… | `describe filter.cameraRaw` |
| `filter.vanishingPoint` | Vanishing Point… | `describe filter.vanishingPoint` |
| `filter.liquify` | Liquify… | `describe filter.liquify` |
| `filter.render.flame` | Flame… | `describe filter.render.flame` |
| `filter.render.pictureFrame` | Picture Frame… | `describe filter.render.pictureFrame` |
| `filter.render.tree` | Tree… | `describe filter.render.tree` |

<!-- COMPLETE_SCENARIO_COMMANDS_END -->
