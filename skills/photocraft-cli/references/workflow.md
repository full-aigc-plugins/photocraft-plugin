# 原生分层工作流

使用技能自带 `scripts/workflow.py` 执行可复现的编辑计划。首次执行自动安装或复用锁定 CLI；Python 3.11+ 即可运行，无需 Pillow。Pillow 只用于开发者的像素回归测试。

```bash
python3 /mnt/skills/user/photocraft-cli/scripts/workflow.py \
  /mnt/skills/user/photocraft-cli/examples/poster-plan.json \
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

其他操作是白名单内原生命令：形状、文字、填充/调整图层、图层选择与命名、像素/矢量蒙版、选区和图像/画布尺寸。执行在同一 headless MCP 会话；读写能力根只覆盖本次暂存目录。

## 局部修改与尺寸变体

从源交付 `manifest.json` 读取 `files.project.pcraft`，将它放入修订计划的 `expectedProjectSha256`。修改文字使用：

```json
{"command":"type.edit","params":{"layer":{"$ref":"headline.layer"},"text":"NOVA PLUS"}}
```

执行修订时传入 `--source /absolute/project/poster-v1 --output /absolute/project/poster-v2`，不要设置 document。源工程和原素材保留不动，新目录保存独立工程、素材、导出和验收数据。封面变体使用 `image.canvasSize` 或 `image.imageSize`，明确裁切/留白和锚点。

字体检查使用 `type.resolveMissingFonts`，检测到缺失字体即阻止交付，不自动换字体。保存后重新打开原生工程检查图层；PSD 另行重开并记录图层树。PSD 的 ID 可以重新分配，比较名称、图层类型、文字、蒙版、混合模式与实际像素。

交付包含 `.pcraft`、平面导出、可选 PSD、登记素材、操作记录、原生/PSD 检查结果与文件摘要。PNG 的“图层被扁平化”是平面导出特性；原生工程必须保留独立图层。兼容警告原样保留，不能仅凭 PSD 写入成功宣称无损。

超时不自动重试有副作用的命令；失败不会发布目标目录。助手尚未代替插件级任务账本、跨插件恢复和宿主验收。
