# 产品局部滤镜与输出锐化 / Local product filters and output sharpening

适用于产品海报中背景虚化、指定区域锐化和统一颗粒质感。先确认目标图层、蒙版、选区和最终输出尺寸；文字、产品与背景需要独立编辑时，不以合并整张海报替代原生交付。

Use for background blur, local sharpening and grain in a layered product design. Establish the target layer and mask before filtering; preserve independent text, product and background editing.

## 选择命令 / Choose a command

| 场景 / Scene | 原生命令 / Native command | 参数与决策 / Parameters and decisions |
| --- | --- | --- |
| 背景虚化 | `filter.blur.gaussianBlur` | `radius` 0.1–1000；根据实际像素尺寸选择，不将目录默认值当作设计值 |
| 方向性运动质感 | `filter.blur.motionBlur` | `angle` -360–360；`distance` 1–2000；先确认方向及产品轮廓是否应保留 |
| 局部细节锐化 | `filter.sharpen.unsharpMask` | `amount` 1–500、`radius` 0.1–1000、`threshold` 0–255；检查边缘光晕与噪声 |
| 输出尺寸的锐化 | `filter.sharpen.smartSharpen` | `amount` 1–500、`radius` 0.1–64、`reduceNoise` 0–100；在尺寸适配后检查实际结果 |
| 颗粒统一 | `filter.noise.addNoise` | 核对 `distribution`、`monochromatic`、`seed`；记录种子以便比较修订 |
| 智能滤镜前置 | `filter.convertForSmartFilters` | 查询当前图层是否适用，执行后检查真实图层结构；不能仅凭命令名称承诺非破坏编辑 |

这些范围来自固定版本的原生参数说明。其他 `filter.*` 按 `scenario.md` 分类查询；不将滤镜名称当作所有图层类型、色彩模式或位深都支持的证明。

These ranges come from the pinned native parameter contract. Query other filters by family. A command name does not establish support for every layer type, color mode or bit depth.

## 执行与局部返工 / Execution and revision

1. 读取工程、实际图层 ID、选区和蒙版，保存原始检查点；确认滤镜应作用于背景、产品还是整个目标图层。
2. 查询当前命令参数和 enabled。需要可调整滤镜时先检查智能对象/滤镜能力；否则保留原图层，通过独立工作副本处理并明确结果是否烘焙。
3. 按 `command-usage.md` 的计划合同构造命令，运行 `commands.py check` 后执行 `run`。选择、滤镜与保存需要保持正确原生会话上下文。
4. 保存新 `.pcraft`，重开检查图层、蒙版和实际滤镜状态。另行导出目标尺寸的 PNG/JPEG，并比较处理区域与不应变化区域。
5. 修改滤镜参数时从可编辑状态或原始副本开始；不要反复在已烘焙结果上叠加锐化。保留旧交付和参数记录。

Inspect the actual selection and layer IDs, use the command gateway contract, and save/reopen the native project. Distinguish editable filters from baked pixels. Revisions start from editable state or the preserved original rather than repeatedly sharpening a flattened result.

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" list --filter filter.
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.convertForSmartFilters
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe filter.sharpen.smartSharpen
```

## 交付验收 / Delivery acceptance

交付原生工程、依赖素材、参数记录与平面导出。核验文字仍可编辑，产品与背景保持独立，目标区域发生预期像素变化，非目标区域按任务约束保持不变。技术检查与视觉审核分别记录；本手册不代表 122 个滤镜命令已逐一执行验收。

Deliver the native project, dependencies, parameter records and raster exports. Verify editable text, independent product/background layers and requested pixel changes. Full per-filter native execution acceptance remains open.

## 已执行代表实例 / Executed representative example

本技能 `examples/filter-smart-create.json` 建立 96×64 测试工程，转换图形为智能对象并应用 radius=2 的高斯模糊，保存工程与 PNG。使用 `commands.py run`；输出目录必须是新目录。`examples/filter-smart-reopen.json` 通过 `--input project=/absolute/project.pcraft` 重开并再次导出。该例已核验智能滤镜参数保留与两次导出像素一致；不是用户海报规格，也不证明全部滤镜已验收。

Use the create fixture through the public command gateway and the reopen fixture with an explicit project input. This bounded example preserves the smart-filter contract and exported pixels; adapt it to the real design before use.
