# 业务场景操作手册 / Business scenario playbook

## 产品海报与封面 / Product poster and cover

### 输入、参数与能力选择

核对产品素材、字体、文案、品牌色和海报/封面尺寸。示例为 320×400；产品、背景和文字应分别保留为可编辑图层。

从本技能的 `scenario.md` 与 `command-reference.md` 选择能力；模板 `operations` 可以包含公开工作流操作和原生命令。两者参数合同不同，不要把模板操作名当成反射命令 ID。对于完整原生命令，使用 `commands.py describe` 查看其真实参数，并按 `command-usage.md` 构造 `craft-command-plan/v1`；不要将下面的 workflow 模板直接传给 commands.py。

Choose capabilities using the local scenario and command references. Workflow operations and reflected native command IDs have different contracts. Do not pass the workflow fixture below to the full-command gateway.

### 从真实素材开始

复制本技能 `examples/poster-plan.json` 到工作目录，按用户需求修改其文档参数、操作和输出设置；保留技能安装副本。以下演示原模板，路径占位符必须替换为真实绝对路径，输出目录必须不存在。

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" \
  "$SKILL_DIR/examples/poster-plan.json" \
  --asset product=/absolute/input/product.png \
  --output /absolute/new-delivery
```

操作顺序：建立文档 → 放置产品 → 建立选区与蒙版 → 清除选择 → 创建标题及说明文字 → 保存重开 → 导出；封面适配参考 resize-variant-plan.json。

The fixture is an operation example, not the user's final specification. Copy and adapt it outside the installed skill; use real inputs and a fresh output directory. Installation and creation remain separate acceptance steps.

### 交付核验

`.pcraft`、平面导出和适用的 PSD；检查图层、蒙版和文字仍独立可编辑，PSD 交换损失按 exchange-loss.md 记录。

检查实际清单与文件摘要、重开后的对象结构和派生输出。预览、视频解码、像素与矢量结构核验各自只证明对应范围，视觉质量须单独审核。具体输出名称和修订合同见本技能 `workflow.md`。

### 局部返工与失败恢复

只调整目标文字、产品或背景；修改尺寸时检查裁切和文字边界，保留其他图层与原素材摘要。

使用 `command-usage.md` 中的配对 `commands-revision-create.json` / `commands-revision.json` 先理解原生返工合同；这些示例中的对象位置只适用于该示例，不得套用到真实用户工程。真实工程先检查 ID、当前选择、参数及摘要，再建立只修改目标的新计划。`workflow.py --source` 的输入合同以 `workflow.md` 为准。

超时或断开先读取 journal 与保存工程，结果未知时禁止自动重放。保留原交付和失败诊断，用新输出目录进行已确认的修订。

Inspect actual object IDs and hashes before revising. Fixture indices are not identifiers for an arbitrary user project. Preserve the original delivery, reconcile unknown results and avoid replaying mutations.

## 证据范围

本手册把已有代表模板与分类命令连接起来；不是全部命令、全部素材、全部 GUI 或创作质量的验收报告。最新固定版本证据在仓库 `docs/evidence/`，其版本不能替代当前工作树修改的安装复验。
