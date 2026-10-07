# 可编辑蒙版与局部亮度调整 / Editable mask and local brightness

本技能自带成对计划，单独安装即可运行；当前为源候选，固定安装验收尚未完成。

设置 SKILL_DIR 为本 SKILL.md 的实际目录。用公开 workflow.py 调用 examples/adjustment-mask-create.json，另存新 output。首次调用会使用本技能安装器下载固定原生运行时；无需兄弟技能目录。

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" "$SKILL_DIR/examples/adjustment-mask-create.json" --output /absolute/new-delivery
```

128×64 示例包含独立 Product、Control 与 brightnessContrast 调整层。先创建调整层并绑定真实 layer 返回值，再建立矩形选区、revealSelection 蒙版、取消选区。蒙版只覆盖产品左半部分；调整层不烘焙到产品像素。select.rect 的 x/y/width/height 单位为像素；brightness 范围 -150..150、contrast -50..100，示例明确给出 legacy=false。蒙版命令需要当前工程与有效图层；不能以猜测 ID 代替返回值。

返工时复制 examples/adjustment-mask-revise.json 到工作目录，将 expectedProjectSha256 设置为源 manifest.json 中 files["project.pcraft"] 的真实摘要。使用 --source 指向原交付目录并给出不同 --output。重开工程后先 layer.select 选择 adjustment，再 layer.setAdjustment；它的参数不得省略默认保持假设，示例明确给出 brightness/contrast/legacy。$ref 使用源 manifest 的真实绑定。不要覆盖原交付。

```bash
python3 -I -B "$SKILL_DIR/scripts/workflow.py" /absolute/revision-plan.json --source /absolute/new-delivery --output /absolute/revised-delivery
```

验收包含原生保存重开、蒙版与调整层信息、PNG 实际像素、修改区域及控制区域比对、源交付摘要保护。错误层类型或源摘要不匹配必须拒绝，不能在失败后盲目重放。此样例不证明全部748条指令、PSD 保真、GUI 或完整V1。

The paired plans preserve a native adjustment layer and a selection mask. Bind actual returned layer IDs, reopen the saved .pcraft, select the adjustment before revision, set the real source hash and use a new output directory. Verify rendered pixels inside and outside the mask, unchanged control layers and original delivery hashes. Source-candidate evidence is separate from fixed installed acceptance.
