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
| flatExport | 平面导出的颜色／ICC／透明要求，见本技能 references/flat-export.md |
| assetProvenance | 登记素材对应的已有生成回执与上游声明用量，不发起生成请求 |
| psdPolicy | 必要 PSD 功能及与源版本／观察摘要绑定的明确损失接受；见本技能 exchange-loss.md |

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

通过 workflow.py 的 `--source` 另存修订，可同时声明 `protectedRegions` 并请求 PNG/PSD；实际保存重开后才发布交付。保护区域的精确像素比较只支持原生 `Rgb`、8 位源工程；16/32 位及其他模式在安装或编辑前拒绝，避免 PNG 转换掩盖原生差异。直接调用原生 cli.py run 不会执行 Python 工作流保护区域门禁。更多绘画命令虽可被原生 CLI 列出，但不因此进入此工作流白名单。

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

## 失败暂存的原生恢复

公开工作流已经进入暂存后失败时，保留输出 `failure.json` 指向的 `stage`、该原位置的工程与素材，以及 `recovery-operations.json`。核对 `files` 中全部摘要及 `lastAttempt`，未知请求可能已经执行；不能自动重跑计划、移动暂存或删除失败目录。输出已有时会拒绝再次运行，成功交付才清理未使用暂存。

先用本技能 `commands.py` 的新会话执行打开／检查计划，并显式登记恢复工程作为 `--input project=原暂存工程绝对路径`；按真实对象状态建立新的修改计划。`failure.json` 不是交付 manifest，不能把失败输出直接传给 `workflow.py --source`。成功保存、重开、依赖收集及派生输出检查后才形成新的交付。诊断写入权限不足时仍保留暂存并返回原异常，不能假定失败输出目录一定存在。

After staged failure, retain both the output recovery record and its original sibling stage. Verify all file hashes and the last submitted attempt; an unknown reply may follow a successful native operation. Open/inspect the retained project in a fresh commands.py session before an explicit new revision. Do not replay the original plan, move the stage or pass the failed directory as a successful workflow source package.

## 候选增强合同

`workflow.py PLAN --check [--source SOURCE]` 只检查计划、素材和源清单，不安装、不创建输出。正常运行仍使用 `--output NEW_DIRECTORY`。重复键、非有限数值、未知字段和引用依赖在安装前拒绝；执行中错误保留原暂存和回执。

可选 `assertions` 数组按 `layer`（ID 或已建立的 `$ref`）核对 `kind/name/visible/hasMask/text/bounds/within/parent/order`；`maskEnabled/maskLinked` 读取固定 v1 保存格式并绑定真实图层 ID；`lineCount/lineRanges/tracking/font/size/leading/orientation` 使用保存重开后的 type.info；native-facts.json 绑定工程摘要。`noOverflow/glyphCoverage` 当前缺少精确指标，要求这些断言会拒绝验证。`preserveObjects` 将对象 ID 字符串映射到允许变化的属性，如 `{"3":["text.text","bounds"]}`；父子、顺序、类型和其他对象保持不变，临时 selected 状态不属于内容保全。该合同只能用于已核验的源包另存。

`filterContract` 明确 `target/method/selection/mask/region`，例如 `{"target":2,"method":"raster","selection":false,"mask":false,"region":[0,0,32,32]}`。配合显式 layer.select 和 native.command 的 filter 命令；执行前核对上下文，执行后核验实际像素变化。raster 明确为烘焙；智能滤镜完整可编辑图当前无法核验，不能提升为可编辑通过。保护产品仍需声明 protectedRegions 或非目标对象保全。

`capabilities.json` 记录当前会话、后端、二进制、运行时版本／构建／平台、命令参数说明与 MCP 工具 schema 摘要；参数说明并非逐命令 JSON Schema。`native_verify.py DELIVERY` 使用已安装的固定二进制在新只读会话重开，验证结束后再次核对原包，不安装。PSD featureMatrix 的 retained/degraded/lost/unknown 只表示已报告属性比较，不等于完整保真或外部编辑器验收。

可选 `acceptedFontSubstitutions` 明确从缺失字体到已安装字体的映射。无接受映射时仍拒绝缺失字体；执行替换后再次只读查询当前缺失字体，font-substitutions.json 保留接受映射与原生前后回复。替代字体不会自动获得精确排版或外部 PSD 保真接受。

命令参数按固定公开说明做可确定的类型、范围及键检查；MCP 工具按固定实际 schema 检查。引用在解析后、下一副作用前再次检查。command_batch 的每一步同样校验；部分完成的批次保留子结果并转入核对，不登记成功别名或继续后续操作。重复 JSON 键及非有限数值携带字段路径；这些检查不等于全部命令的真实业务执行验收。

蒙版保全事实除绑定、启用、链接、密度和羽化外，还绑定保存格式中的 surface 描述与实际压缩瓦片 SHA-256。仅蒙版元数据相同不能通过保全；缺失瓦片或超过 64 MiB 的蒙版瓦片核验范围会明确拒绝。该摘要验证内容保全，不证明创作质量。

每次操作核对实际使用的命令／工具与发现工具，未使用合同变化不会阻止当前操作；完整发现摘要仍记录在 `capabilityChecks` 或 `capability-checks.json`。若以后使用已变化合同，按原会话基线拒绝，不把无关变化静默接受为新基线。
