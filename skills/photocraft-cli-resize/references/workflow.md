# 原生分层工作流

使用技能自带 `scripts/workflow.py` 执行可复现的编辑计划。首次执行自动安装或复用锁定 CLI；Python 3.11+ 即可运行，无需 Pillow。Pillow 只用于开发者的像素回归测试。

以下 `SKILL_DIR` 沿用本技能 `SKILL.md` 的实际加载目录，脚本和示例均来自同一技能。

```bash
python3 "$SKILL_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/poster-plan.json" \
  --asset product=/absolute/input/product.png \
  --output /absolute/project/poster-v1
```

技能根替换为实际安装目录。示例为 320×400 功能验证版式；正式设计前按需求调整尺寸、排版、素材位置和蒙版。CLI 会计算指定素材摘要并加入计划，不需要用户手工填摘要。

## 计划字段

| 字段 | 含义 |
| --- | --- |
| document | 新建文档的 name、width、height、background、mode、depth |
| assets | 命名素材的 `{path, sha256}`；也可由 `--asset NAME=PATH` 填充 |
| operations | 顺序执行 `{command, params, as?}`；允许范围见脚本 ALLOWED |
| as | 保存上游真实结果，后续通过 `{"$ref":"headline.layer"}` 引用 |
| minimumLayers | 重开后最低图层数门禁；无法替代图层语义检查 |
| exports | `[{"format":"png"},{"format":"psd"}]`；同时支持 jpg、tif、webp |
| expectedProjectSha256 | 修订时必须与源工程及源 manifest 摘要一致 |

`asset.place` 是本助手操作，不是上游命令。它使用限定读取根内的 `doc_open`，把素材复制到目标文档的独立像素图层，支持 `asset`、`center`、`name` 参数。它不创建链接图层或智能对象，不执行 MCP 明确禁止的带外文件命令。

其他操作是白名单内原生命令：形状、文字、填充/调整图层、图层选择与命名、像素/矢量蒙版、选区和图像/画布尺寸，以及 `paint.stroke`、`paint.cloneStamp`、`paint.healingBrush`。执行在同一 headless MCP 会话；读写能力根只覆盖本次暂存目录。

## 局部修改与尺寸变体

从源交付 `manifest.json` 读取 `files.project.pcraft`，将它放入修订计划的 `expectedProjectSha256`。修改文字使用：

```json
{"command":"type.edit","params":{"layer":{"$ref":"headline.layer"},"text":"NOVA PLUS"}}
```

执行修订时传入 `--source /absolute/project/poster-v1 --output /absolute/project/poster-v2`，不要设置 document。源工程和原素材保留不动，新目录保存独立工程、素材、导出和验收数据。封面变体使用 `image.canvasSize` 或 `image.imageSize`，明确裁切/留白和锚点。

字体检查使用 `type.resolveMissingFonts`，检测到缺失字体即阻止交付，不自动换字体。保存后重新打开原生工程检查图层；PSD 另行重开并记录图层树。PSD 的 ID 可以重新分配，比较名称、图层类型、文字、蒙版、混合模式与实际像素。

交付包含 `.pcraft`、平面导出、可选 PSD、登记素材、操作记录、原生/PSD 检查结果与文件摘要。PNG 的“图层被扁平化”是平面导出特性；原生工程必须保留独立图层。兼容警告原样保留，不能仅凭 PSD 写入成功宣称无损。

超时不自动重试有副作用的命令；失败不会发布目标目录。助手尚未代替插件级任务账本、跨插件恢复和宿主验收。

## 修图另存与保护区域

修图计划先执行 `layer.select`，用 `{"$ref":"product.layer"}` 或已核验的图层 ID 选择像素图层，再执行上述三个笔触命令。笔刷 hardness/opacity/flow 为 0..1；仿制图章和修复笔刷 hardness 为 0..100，opacity/flow 为 1..100，并显式提供 source 或 offset。不要混用单位。

通过 workflow.py 的 `--source` 另存修订，可同时声明 `protectedRegions` 并请求 PNG/PSD；实际保存重开后才发布交付。直接调用原生 cli.py run 不会执行 Python 工作流保护区域门禁。更多绘画命令虽可被原生 CLI 列出，但不因此进入此工作流白名单。

## 可核验的尺寸变体

另存计划可增加 `variant`；它要求 `--source` 和已核验的 `expectedProjectSha256`。例如：

```json
{"variant":{"width":360,"height":440,"safeArea":[8,8,344,424],"roles":{"background":2,"product":{"$ref":"product.layer"},"text":{"$ref":"headline.layer"}}}}
```

background 的数字 ID 必须读取源 `native.json` 的真实 Background 图层，不能照抄示例。roles 的三个 ID 必须互不相同并来自源工程；文字必须保持原生 Type 图层，所有角色必须可见，产品和文字的实际边界必须完整位于安全区。安全区 `[x,y,width,height]` 使用最终画布坐标。它是几何门禁，不表示视觉审美、品牌或印刷验收。

操作必须包含 `image.canvasSize` 或 `image.imageSize`。工作流记录每次操作前的实际尺寸和 CLI 返回结果；画布调整使用原生 offset 计算四边裁切与留白，图像重采样记录横纵比例。保存并重开 `.pcraft` 后核验目标尺寸和角色，再写入 `layout-variant.json` 并在 manifest 中绑定 SHA-256。尺寸不符、图层身份或类型变化、隐藏、文字/产品越出安全区都会拒绝发布目标目录，源交付保留。`protectedRegions` 为同尺寸像素保护，不能用原画幅坐标替代尺寸变体的安全区。

完整变体示例见本技能 `examples/resize-variant-plan.json`；先替换源工程摘要、背景 ID 和所需目标尺寸。

## 登记智能对象工作流 / Registered smart content

`asset.placeSmart` 使用 `{asset, center?, fit?, scale?}`；`layer.smartObjects.convertToSmartObject` 和 `layer.smartObjects.convertToEmbedded` 使用显式 `{layer}`。替换与重新链接使用 `{layer, asset}`，asset 必须是已登记图像别名；禁止直接传 path。维护版通过授权目录读取字节，收集交付中的重新链接转换为嵌入，保持原变换与蒙版。持续外部链接交付不由本映射证明。修订需提供 expectedProjectSha256 与 --source，另存旧包。

Smart placement accepts registered asset aliases with optional center/fit/scale. Conversion requires an explicit layer; replacement/relink requires `{layer, asset}` and rejects direct paths. The maintained runtime reads through directory capabilities. Collected relink content is embedded while preserving transform and masks; persistent external linked delivery is not claimed. Revisions bind the expected project digest, use --source, and preserve old packages.
