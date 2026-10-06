# PhotoCraft PSD 独立解码首次使用验收

固定插件 dev.9／技能源 dev.8。旧临时宿主目录不可用后，按 ArtCraft 的发行锁重新隔离安装五插件；Codex 0.153.4 发现全部 58 项技能且无加载错误。复制已安装 `photocraft-cli-export` 到单独 `.agents/skills/`，从空运行目录下载固定 CLI 0.2.0，完成海报、改字版与封面三个原生交付。

海报原生工程包含 Background、Product、Headline、Caption 四个分别可编辑的图层，产品蒙版隐藏指定区域以外的像素。标题另存为 NOVA PLUS 时产品、背景、注释层完全保留，标题之外的 PNG 区域不变。封面从改字工程另存 360×440，并保留图层 ID、类型、产品蒙版和标题内容。两个源交付目录的全部文件及产品输入摘要未改变。

每份 PSD 的合成图使用既有 Pillow 12.3.0 独立解码，与 PNG 的全部 RGB 像素一致。三个样本均为不透明画布，PNG alpha 为 255；这不证明透明 PSD 合成 alpha。可编辑图层、文字和蒙版语义由原生独立重开及 PhotoCraft 的 PSD 重开检查记录观察，不能把 Pillow 合成图核验说成另一编辑器的文字／蒙版编辑验收。

真实目标测试 1 项通过，5.640 秒。源码默认回归 53 项中 36 通过、17 项 opt-in 跳过；跳过不是验收通过。复验后 58 项已安装技能摘要仍与宿主回执一致。见 [PSD 证据](evidence/codex-photo9-independent-psd-first-use-20261006.json) 与 [重新安装发现证据](evidence/codex-five-plugin-reinstall-discovery-20261006.json)。

没有安装额外依赖，没有修改固定技能快照或原生 CLI。Photoshop 实际编辑、透明 PSD、所有效果／混合映射、模型派发、创作与生产市场验收仍不在这些样本的证明范围内。
