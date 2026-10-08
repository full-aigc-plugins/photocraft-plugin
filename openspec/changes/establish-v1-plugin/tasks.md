# V1 实施任务

已进入实施；仅在测试或真实验证有对应证据时勾选相应任务。每个需求按先失败测试、再最小实现、最后真实验证推进。通用依赖：M1 → M2 → M3 → M4。

## 1. skills-distribution

- [x] 1.1 [PC-SK-001] 编写能暴露“独立技能事实源”缺失的正向与失败测试并确认预期失败。责任：Skills owner；无前置实现；先读取本需求及公共协议。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 证据：`docs/evidence/vendor-self-contained-20261008.json`；固定来源、漂移拒绝、脏来源、链接及标签命名空间边界已逐项核验。
- [x] 1.2 [PC-SK-001] 在 独立 photocraft-skills 与技能同步校验 实现“独立技能事实源”的最小行为，不扩大支持范围。责任：Skills owner；前置：1.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 证据：`docs/evidence/vendor-self-contained-20261008.json`；固定来源、漂移拒绝、脏来源、链接及标签命名空间边界已逐项核验。
- [x] 1.3 [PC-SK-001] 完成“独立技能事实源”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：1.2。产物：evidence/pc-sk-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 证据：`docs/evidence/vendor-self-contained-20261008.json`；固定来源、漂移拒绝、脏来源、链接及标签命名空间边界已逐项核验。
- [x] 1.4 [PC-SK-002] 编写能暴露“独立安装与依赖声明”缺失的正向与失败测试并确认预期失败。责任：Skills owner；无前置实现；先读取本需求及公共协议。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 证据：`docs/evidence/craft-fixed-setup-boundary-20261008.json`。历史红灯为本轮重建；仅独立安装／依赖需求。
- [x] 1.5 [PC-SK-002] 在 独立 photocraft-skills 与技能同步校验 实现“独立安装与依赖声明”的最小行为，不扩大支持范围。责任：Skills owner；前置：1.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 证据：`docs/evidence/craft-fixed-setup-boundary-20261008.json`。历史红灯为本轮重建；仅独立安装／依赖需求。
- [x] 1.6 [PC-SK-002] 完成“独立安装与依赖声明”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：1.5。产物：evidence/pc-sk-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 证据：`docs/evidence/craft-fixed-setup-boundary-20261008.json`。历史红灯为本轮重建；仅独立安装／依赖需求。


- [x] 1.7 [PC-SK-003] 编写 CLI 子命令拒绝、单技能隔离执行与既有 use 回归测试，记录失败原因。责任：Skills owner；前置：上游 CodeGraph 调查与运行时目录取证；产物：tests/test_skill_suite.py、研究证据。
- [x] 1.8 [PC-SK-003] 实现 CLI/安装/领域场景技能和自包含公开调用入口；更新双语清单与插件来源锁。责任：Skills owner；前置：1.7；产物：独立技能源、固定标签与内置快照。
- [x] 1.9 [PC-SK-003] 验证每个单独技能的 CLI 发现与原生代表任务、旧入口回归及插件技能发现。责任：QA owner；前置：1.8；产物：docs/evidence/skill-suite.json；明确未执行的创作/GUI 场景。
- [x] 1.10 [PC-SK-003] 逐项执行九类场景技能的单独冷安装及原生操作，验证图层/蒙版/局部调整、克隆修复数值范围、保护区域和 PSD；完整回归 36 项、零跳过；产物：docs/evidence/task-skill-first-use.json、独立技能源 tests/test_task_skill_first_use.py。
- [x] 1.11 [PC-SK-003] 修正全部技能为真实加载目录调用，执行三种安装布局及含空格路径的隔离入口回归；产物：docs/evidence/installed-skill-paths.json、独立技能源 tests/test_installed_paths.py。此检查不替代完整创作验收。
- [x] 1.12 [PC-SK-001] 修复本地来源覆盖读取工作树而非固定标签的漂移，验证脏文件保留、缓存排除和公开来源摘要一致；产物：tests/test_skill_vendor.py、docs/evidence/installed-skill-paths.json。

## 2. runtime-distribution

- [x] 2.1 [PC-RT-001] 编写能暴露“运行时来源与完整性”缺失的正向与失败测试并确认预期失败。责任：Runtime owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。
- [x] 2.2 [PC-RT-001] 在 src/adapters/runtime、runtime/ 锁文件与安装器 实现“运行时来源与完整性”的最小行为，不扩大支持范围。责任：Runtime owner；前置：2.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 证据：`docs/evidence/craft-fixed-runtime-integrity-20261008.json`；固定当前安装、原制品保全、真实并发／超时及全部场景逐项核验，仅RT-001。
- [x] 2.3 [PC-RT-001] 完成“运行时来源与完整性”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：2.2。产物：evidence/pc-rt-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 证据：`docs/evidence/craft-fixed-runtime-integrity-20261008.json`；固定当前安装、原制品保全、真实并发／超时及全部场景逐项核验，仅RT-001。
- [ ] 2.4 [PC-RT-002] 编写能暴露“运行能力与隔离升级”缺失的正向与失败测试并确认预期失败。责任：Runtime owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。
- [ ] 2.5 [PC-RT-002] 在 src/adapters/runtime、runtime/ 锁文件与安装器 实现“运行能力与隔离升级”的最小行为，不扩大支持范围。责任：Runtime owner；前置：2.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。
- [ ] 2.6 [PC-RT-002] 完成“运行能力与隔离升级”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：2.5。产物：evidence/pc-rt-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。

- [x] 2.9 [PC-RT-002] 为首次原生下载的SSL EOF建立代表性红绿测试；独立技能源实现最多三次只读下载、丢弃半包并保留完整性边界，同步全部技能，候选回归通过。证据 `docs/evidence/photocraft-native-download-candidate-20261007.json`；仅候选子门禁。
- [x] 2.10 [PC-RT-002] 发布新的不可变技能源和插件，实际安装每个独立技能以空缓存公开安装并核对版本、目录及技能摘要；Art领域包另行升级。

## 3. task-execution

- [x] 3.1 [PC-TX-001] 编写能暴露“版本绑定与单写”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 3.2 [PC-TX-001] 在 src/harness/ 账本、租约与恢复 实现“版本绑定与单写”的最小行为，不扩大支持范围。责任：Harness owner；前置：3.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 3.3 [PC-TX-001] 完成“版本绑定与单写”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：3.2。产物：evidence/pc-tx-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。
- [x] 3.4 [PC-TX-002] 编写能暴露“幂等与不明确结果恢复”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 3.5 [PC-TX-002] 在 src/harness/ 账本、租约与恢复 实现“幂等与不明确结果恢复”的最小行为，不扩大支持范围。责任：Harness owner；前置：3.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 3.6 [PC-TX-002] 完成“幂等与不明确结果恢复”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：3.5。产物：evidence/pc-tx-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。
- [x] 3.7 [PC-TX-003] 编写能暴露“取消与预算边界”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 3.8 [PC-TX-003] 在 src/harness/ 账本、租约与恢复 实现“取消与预算边界”的最小行为，不扩大支持范围。责任：Harness owner；前置：3.7。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 3.9 [PC-TX-003] 完成“取消与预算边界”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：3.8。产物：evidence/pc-tx-003/；验证：规范所有场景有证据，且 README 能力状态与证据一致。

- [x] 3.10 [PC-TX-004] 真实保存后六类协议异常复现暂存工程删除，并建立目录竞争／成功清理／回执保全测试；确认失败为目标缺失。
- [x] 3.11 [PC-TX-004] 独立技能源保留失败暂存原路径、工程／依赖摘要、成功回执与未知状态；验证原生重开、不重放、成功交付及全部单技能资源。
- [x] 3.12 [PC-TX-004] 固定发布并验证实际安装副本首次使用与失败工程保留；Art 固定捆绑包另行验收，不以候选测试关闭发布子门禁。

- [x] 3.13 [PC-TX-001] 公开工作流在原生会话前登记同目标身份；覆盖竞争、SIGKILL后的未知记录、不同目标、异常及用户文件保全；验证全部独立技能同步与源冷原生创建／返工，不关闭完整任务合同。
- [x] 3.14 [PC-TX-001] 固定发布后验证安装副本、逐技能冷安装及原生创建／返工，保持全部技能摘要；Art固定领域包单独升级验收。

## 4. domain-workflow

- [x] 4.1 [PC-DM-001] 编写能暴露“分层文档与编辑身份”缺失的正向与失败测试并确认预期失败。责任：Domain owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 4.2 [PC-DM-001] 在 src/planning/、src/adapters/ 的领域计划与映射 实现“分层文档与编辑身份”的最小行为，不扩大支持范围。责任：Domain owner；前置：4.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 4.3 [PC-DM-001] 完成“分层文档与编辑身份”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：4.2。产物：evidence/pc-dm-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。
- [x] 4.4 [PC-DM-002] 编写能暴露“蒙版与局部调整”缺失的正向与失败测试并确认预期失败。责任：Domain owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 4.5 [PC-DM-002] 在 src/planning/、src/adapters/ 的领域计划与映射 实现“蒙版与局部调整”的最小行为，不扩大支持范围。责任：Domain owner；前置：4.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 4.6 [PC-DM-002] 完成“蒙版与局部调整”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：4.5。产物：evidence/pc-dm-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。
- [x] 4.7 [PC-DM-003] 编写能暴露“文字排版与字体依赖”缺失的正向与失败测试并确认预期失败。责任：Domain owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 4.8 [PC-DM-003] 在 src/planning/、src/adapters/ 的领域计划与映射 实现“文字排版与字体依赖”的最小行为，不扩大支持范围。责任：Domain owner；前置：4.7。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 4.9 [PC-DM-003] 完成“文字排版与字体依赖”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：4.8。产物：evidence/pc-dm-003/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。
- [x] 4.10 [PC-DM-004] 编写能暴露“海报封面尺寸变体”缺失的正向与失败测试并确认预期失败。责任：Domain owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 证据：`docs/evidence/photocraft-complete-variant-contract-20261008.json`；历史失败本轮重建，固定Photo38／源34尺寸技能原生三变体、重开、PSD图层、安全区／尺寸／覆盖拒绝与失败暂存保全通过，仅完整PC-DM-004。
- [x] 4.11 [PC-DM-004] 在 src/planning/、src/adapters/ 的领域计划与映射 实现“海报封面尺寸变体”的最小行为，不扩大支持范围。责任：Domain owner；前置：4.10。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 证据：`docs/evidence/photocraft-complete-variant-contract-20261008.json`；历史失败本轮重建，固定Photo38／源34尺寸技能原生三变体、重开、PSD图层、安全区／尺寸／覆盖拒绝与失败暂存保全通过，仅完整PC-DM-004。
- [x] 4.12 [PC-DM-004] 完成“海报封面尺寸变体”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：4.11。产物：evidence/pc-dm-004/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 证据：`docs/evidence/photocraft-complete-variant-contract-20261008.json`；历史失败本轮重建，固定Photo38／源34尺寸技能原生三变体、重开、PSD图层、安全区／尺寸／覆盖拒绝与失败暂存保全通过，仅完整PC-DM-004。
- [x] 4.13 [PC-DM-005] 编写能暴露“原生与 PSD 保真”缺失的正向与失败测试并确认预期失败。责任：Domain owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 4.14 [PC-DM-005] 在 src/planning/、src/adapters/ 的领域计划与映射 实现“原生与 PSD 保真”的最小行为，不扩大支持范围。责任：Domain owner；前置：4.13。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 4.15 [PC-DM-005] 完成“原生与 PSD 保真”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：4.14。产物：evidence/pc-dm-005/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 固定 dev.40／技能源 dev.36 场景验收：`docs/evidence/optimization/psd-acceptance-audit.json`；未验证外部编辑器及完整保真保持未知。
- [x] 4.16 [PC-DM-006] 编写能暴露“平面导出与来源”缺失的正向与失败测试并确认预期失败。责任：Domain owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 验收证据：`docs/evidence/optimization/flat-acceptance-audit.json`（固定 dev.41／技能源 dev.37，RGB8 与供应方回执夹具；真实生成及计费未验收）。
- [x] 4.17 [PC-DM-006] 在 src/planning/、src/adapters/ 的领域计划与映射 实现“平面导出与来源”的最小行为，不扩大支持范围。责任：Domain owner；前置：4.16。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 验收证据：`docs/evidence/optimization/flat-acceptance-audit.json`（固定 dev.41／技能源 dev.37，RGB8 与供应方回执夹具；真实生成及计费未验收）。
- [x] 4.18 [PC-DM-006] 完成“平面导出与来源”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：4.17。产物：evidence/pc-dm-006/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 验收证据：`docs/evidence/optimization/flat-acceptance-audit.json`（固定 dev.41／技能源 dev.37，RGB8 与供应方回执夹具；真实生成及计费未验收）。

- [x] 4.19 [PC-DM-003] 补充固定宿主安装单文字技能全新公开缓存中文海报创建和定点改字验收；核验原生/PSD Type 字体与内容、保护像素、原文件、PSD 解码、未知图层和缺失字体拒绝，登记有界证据。

- [x] 4.20 [PC-DM-002] 实现公开源工程工作流的显式保护区域检查，使用实际原生渲染并保持标准库首次使用；覆盖区域摘要、无效输入、变化拒绝、源保全、单技能冷安装与固定插件安装复验。
- [x] 4.21 [PC-DM-002] 接通修图工作流的笔刷、仿制图章和修复笔刷；验证独立技能冷安装、真实像素结果、原生/PSD 重开、保护区域拒绝与源交付保全，随后固定发布并在安装后的插件中复验。
- [x] 4.22 [PC-DM-004] 在独立尺寸技能工作流中记录实际裁切/留白、目标尺寸、安全区及文字/产品/背景图层身份；验证冷安装、原生与 PSD 重开、拒绝越界变体和源文件保全，再固定发布并在插件安装副本复验。

## 5. artifact-delivery

- [x] 5.1 [PC-AR-001] 编写能暴露“产物血缘与包完整性”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 5.2 [PC-AR-001] 在独立技能源 exchange_loss.py 与公开交付校验 实现“产物血缘与包完整性”的最小行为，不扩大支持范围。责任：Harness owner；前置：5.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选进展：独立只读包校验及返工前后完整源校验已实现，固定发行38已通过13技能冷安装与校验、原生海报移动／返工／篡改拒绝；完整血缘身份与全部场景仍开放，见docs/evidence/craft-photo-delivery-integrity-fixed-first-use-20261008.json。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [ ] 5.3 [PC-AR-001] 完成“产物血缘与包完整性”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：5.2。产物：evidence/pc-ar-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。
- [x] 5.4 [PC-AR-002] 编写能暴露“原生工程与交换损失”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。
- [x] 5.5 [PC-AR-002] 在独立技能源 exchange_loss.py 与公开交付校验 实现“原生工程与交换损失”的最小行为，不扩大支持范围。责任：Harness owner；前置：5.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。
- [x] 5.6 [PC-AR-002] 完成“原生工程与交换损失”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：5.5。产物：evidence/pc-ar-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 固定 dev.40／技能源 dev.36 场景验收：`docs/evidence/optimization/psd-acceptance-audit.json`；未验证外部编辑器及完整保真保持未知。

## 6. quality-review

- [x] 6.1 [PC-QA-001] 编写能暴露“技术与创作证据分离”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 6.2 [PC-QA-001] 在 src/evaluation/ 与修订协调 实现“技术与创作证据分离”的最小行为，不扩大支持范围。责任：Harness owner；前置：6.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 6.3 [PC-QA-001] 完成“技术与创作证据分离”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：6.2。产物：evidence/pc-qa-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。
- [x] 6.4 [PC-QA-002] 编写能暴露“受限局部修订”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 6.5 [PC-QA-002] 在 src/evaluation/ 与修订协调 实现“受限局部修订”的最小行为，不扩大支持范围。责任：Harness owner；前置：6.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 6.6 [PC-QA-002] 完成“受限局部修订”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：6.5。产物：evidence/pc-qa-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。

## 7. release-compatibility

- [ ] 7.1 [PC-RL-001] 编写能暴露“宿主与发布证据”缺失的正向与失败测试并确认预期失败。责任：Release owner；前置：所有 P0 实现、故障恢复与原生交付用例通过。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。
- [ ] 7.2 [PC-RL-001] 在 宿主清单、发布矩阵与权限适配 实现“宿主与发布证据”的最小行为，不扩大支持范围。责任：Release owner；前置：7.1。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。
- [ ] 7.3 [PC-RL-001] 完成“宿主与发布证据”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：7.2。产物：evidence/pc-rl-001/；验证：规范所有场景有证据，且 README 能力状态与证据一致。
- [ ] 7.4 [PC-RL-002] 编写能暴露“权限与秘密边界”缺失的正向与失败测试并确认预期失败。责任：Release owner；前置：所有 P0 实现、故障恢复与原生交付用例通过。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。
- [ ] 7.5 [PC-RL-002] 在 宿主清单、发布矩阵与权限适配 实现“权限与秘密边界”的最小行为，不扩大支持范围。责任：Release owner；前置：7.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。
- [ ] 7.6 [PC-RL-002] 完成“权限与秘密边界”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：7.5。产物：evidence/pc-rl-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。

## 当前宿主证据范围

- [x] 4.24 [PC-DM-003-NO-TEXT] 确认纯图片首用回归因无文字字体命令失败，再依据原生图层树修复字体前置条件；验证无文字 PNG／PSD 与另存修订、有文字缺失字体拒绝、组内文字检测、源素材和技能摘要不变。
- [x] 4.25 [PC-DM-003-NO-TEXT] 发布不可变技能源和插件快照，使用真实安装单技能、空缓存复验纯图片交付与 ArtCraft 混合流程，记录固定发行版本及未验证范围。

`docs/evidence/codex-current-release.json` 记录固定发布在 Codex 0.147.0 / 0.153.4 的安装、发现与公开入口执行；共享复现工具由 ArtCraft 持有。该证据未覆盖模型派发、桌面 GUI、完整 P0 与创作验收，release-compatibility 任务的前置条件尚未全部满足，不能据此勾选完整发布任务。

- [x] 4.23 [PC-DM-005] 重新隔离安装固定五插件，使用单导出技能空运行目录创建四图层蒙版海报、标题修订和封面；Pillow 独立解码三份不透明 PSD 合成图与 PNG 全像素比对，保留两个源交付和素材，核对全部 58 技能摘要。产物：docs/evidence/codex-photo9-independent-psd-first-use-20261006.json；不关闭完整 PSD／外部编辑器／创作验收任务。

## 智能对象公开工作流

- [x] 4.26 [PC-DM-001] 建立目标缺失的失败测试，实现登记智能对象放置、转换、替换、重新链接与嵌入交付的参数校验及映射。
- [x] 4.27 [PC-DM-001] 单技能空运行时验证原生保存重开、替换／重新链接、移动包、蒙版／变换／非目标保全及非法输入拒绝。
- [x] 4.28 [PC-DM-001] 发布固定独立技能源与插件，实际安装快照复验公开智能对象首次使用及 Art 混合交接，保全全部安装摘要。

- [x] 4.29 [PC-RT-002] 修复真实首用暴露的环境路径命令禁用缺口，建立目录能力字节输入的维护版补丁、边界回归、可复现构建与公开安装身份；不放开原环境路径守卫。

4.26／4.27／4.29 证据 `docs/evidence/smart-public-source-first-use-20261006.json`：源边界失败后修复，43 项源回归通过、19 门禁跳过，12 安装器测试通过；维护版原生自动化 46 项通过。公开空运行时单技能智能对象交付／修订一项通过（5.981 秒），变换／蒙版／移动包保全及非法路径拒绝；固定维护版归档、二进制与来源摘要通过。4.28 固定插件／Art 混合门禁仍开放。

4.28 固定 Photo 部分完成：插件 dev.11／源 dev.10／维护版 0.2.0-craft.1。安装后智能对象原生首用一项及 PSD／纯图片回归两项通过，十二项独立冷启动通过、58 安装摘要保全、公开附件及四项标签 CI 通过，默认新旧版本并存。证据 `docs/evidence/codex-photocraft11-smart-first-use-20261006.json`。Art 固定混合交接尚未完成，本任务保持开放。

2026-10-06 固定混合验收：4.28 完成。Art 插件 dev.70／源 dev.47／运行时 dev.68 与 Photo 插件 dev.11／源 dev.10／维护版 0.2.0-craft.1；安装后的智能对象混合原生测试 1 项通过（64.957 秒），十项 Art 独立冷启动通过，58 安装摘要保全，五固定包重建、公开归档及四项对应提交 CI 通过。证据 `docs/evidence/codex-artcraft70-smart-mixed-first-use-20261006.json`。完整首版及外部编辑器验收仍开放。

## 8. 完整命令覆盖

- [x] 8.1 [PC-CM-001] 建立全目录覆盖、后续非法命令、引用、嵌入错误及超时不重放的失败测试；记录目标缺失失败。
- [x] 8.2 [PC-CM-001] 在独立技能源实现完整命令参数说明、技能路由、同会话调用、实时状态检查及逐步回执；同步独立技能资源并验证固定目录覆盖。
- [ ] 8.3 [PC-CM-001] 完成逐命令适用上下文、GUI／原生输出与局部修订验收；固定发布及实际安装副本复验。仅目录和代表调用通过不得关闭此任务。

- [x] 8.4 [PC-CM-001] 固定技能源与插件公开发行后，真实隔离 Codex 安装／发现全部 58 项；本领域安装副本新入口公开冷安装、原生重开／渲染代表样例及全部技能独立冷启动通过，核对全部安装摘要。仅关闭固定首用子门禁，8.3 全量命令／GUI／修订验收保持开放。证据 `docs/evidence/codex-complete-command-first-use-20261007.json`。

- [x] 8.5 [PC-CM-001] 为每个独立技能补充配套创建／局部返工示例，明确重开后选择前置条件；从空运行时公开安装，直接执行文档计划，检查目标保存重开、非目标对象／像素及原交付／技能摘要。证据 `docs/evidence/complete-command-revision-first-use-20261007.json`；仅代表返工子门禁，8.3 保持开放。
- [x] 8.6 [PC-CM-001] 将返工示例固定发布到独立技能源并通过 vendor 同步插件；实际 Codex 固定安装副本执行新的文档返工计划，复核全部安装摘要，不以旧发行首用证据代替。

8.6 固定证据 `docs/evidence/codex-complete-command-revision-first-use-20261007.json`：真实隔离 Codex 0.153.4 安装五个固定公开标签，58 项技能发现零错误；四个安装领域技能独立空运行时公开安装后直接运行文档创建／返工计划，目标保存重开、非目标对象／像素、原交付／技能保全通过。执行后全部58项安装内容与元数据摘要不变；四个固定插件文档／实现CI均通过。全量2639条原生／GUI及模型派发门禁不关闭。

- [x] 8.7 [PC-CM-001] 用真实 stdio 子进程复现畸形／非对象／缺失／冲突／非有限响应与断管错误；客户端统一未知结果，完整命令入口保留 unknown 回执且不重放。通过锁定公开原生 CLI 的响应故障代理验证保存实际完成后仅执行一次、后续操作停止、原生重开和文件保全。
- [x] 8.8 [PC-CM-001] 固定发布协议故障修复的独立技能源和插件；实际安装副本冷运行故障代理与健康创建／返工，核对全技能摘要；Art 固定领域捆绑版本单独处理。

8.7 候选证据 `docs/evidence/protocol-fault-first-use-20261007.json`；不可变旧源失败日志 `docs/evidence/protocol-fault-red-baseline-20261007.json`。默认回归344项：254通过、90显式跳过。48个独立技能分别空运行时公开安装，共288个原生保存成功后故障案例通过；未知回执、不重放、后续停止、原生重开及交付／技能摘要保全均已检查。8.8固定安装副本通过，证据 `docs/evidence/codex-protocol-fault-first-use-20261007.json`；Art领域包升级独立保持开放。

- [x] 8.9 [PC-CM-001] 用真实stdio子进程复现公开工作流工具结构缺失检查；Session统一检查tools/call响应，同步独立技能并验证代表原生公开工作流故障与Art编排不重放，固定发布／实际安装单独验收。

8.9 固定安装子门禁证据 `docs/evidence/codex-public-workflow-session-first-use-20261007.json`：新领域源／插件标签，实际安装副本24个保存后异常、四个健康公开工作流，以及已发布 Art 引擎＋实际安装 Vector 公开工作流六类异常通过；全部58项身份保持不变。仅关闭本次共享 Session 检查与固定领域副本复验；全量8.3和Art内置领域分发升级不关闭。

3.10／3.11 候选原生保全证据 `docs/evidence/failed-stage-candidate-20261007.json`：六类真实保存后故障直接重开原暂存工程、文件摘要与已完成回执保全、不重放；八类生命周期及健康创作／局部返工回归通过。3.12 固定发行及实际安装副本仍开放，Art 捆绑包与完整 V1 不关闭。

3.12 固定验收证据 `docs/evidence/codex-failed-stage-first-use-20261007.json`：全部58技能独立CLI冷启动、24个保存后原暂存重开及四个健康返工，安装摘要与固定CI通过。仅关闭本领域固定首用子门禁；Art4.9、全量命令／GUI／模型和完整V1保持开放。

- [x] 8.10 [PC-CM-001] 修复完整命令工具内层JSON的非有限值／溢出／重复键歧义，保留unknown回执和原调用；单元红绿回归、同步全部独立技能及候选真实保存后的九类故障／原文件重开通过。证据 `docs/evidence/photocraft-inner-json-command-candidate-20261007.json`；仅候选子门禁。
- [x] 8.11 [PC-CM-001] 固定发布内层JSON修复的不可变技能源与插件，实际安装副本复验未知回执、真实保存与重开、健康命令及全技能摘要；Art捆绑包单独升级，全量8.3保持开放。


- [x] 8.12 [PC-CM-001] 完整目录原生命令接入公开工作流，保持素材收集、原生保存重开、导出及交换损失；核验实时状态、unknown保留和源工程局部返工。候选与固定安装证据分开，8.3保持开放。

- [x] 8.13 [PC-CM-001] 补齐十二个独立技能的调整层／选区蒙版成对原生计划及使用说明；验证原生保存重开、局部像素变化、控制图层与源交付保护、错误层类型拒绝。源候选证据独立记录；不得关闭全量8.3或完整PC-DM-002验收。
- [x] 8.14 [PC-CM-001] 固定发布后在十二个实际安装副本复验调整蒙版首次使用，核对公开下载、不可变摘要及控制区像素。
- [x] 8.15 [PC-CM-001] ArtCraft 锁定并分发新的 PhotoCraft 技能源，对实际安装的混合工作流及局部返工重新验收。

- [x] 8.16 [PC-DS-001] 实现每个独立技能的固定桌面安装、版本及制品身份校验、本地bridge启动与连接检查；错误摘要、平台或运行身份必须拒绝，不覆盖用户应用，不绕过系统安全控制。GUI工具与领域命令接口分别记录。
- [x] 8.17 [PC-DS-001] 在实际固定发布安装副本验证桌面首次使用、真实GUI编辑及原生保存重开，记录活动选择、控制地址、原生工程与输出身份；全量8.3继续保持独立验收。

- [x] 8.20 [PC-DS-001] 针对已观察到的桌面下载TLS握手35错误实现最多三次有限下载重试；清理本次私有下载残留、保持摘要及签名检查，其他失败不增加外层重试，安装重试不得重放编辑；确认失败测试、回归和公开首次安装结果。

2026-10-07 固定安装验收：8.17／8.20已完成，证据 `docs/evidence/craft-full-command-fixed-first-use-20261007.json`。仅关闭上述有界门禁：58独立技能冷启动、四领域进阶桌面原生保存重开及渲染、Art模式校验与GUI状态交接、品牌局部返工和包校验；全量逐命令、所有UI交互、通用Skills CLI、模型与完整V1门禁保持开放。


## 场景使用指引补齐 / Scenario usage guidance

- [x] [SC-001] 将完整命令归属清单与业务场景手册纳入独立技能源，验证每条命令唯一归属、参数参考和模板引用可在单技能内读取；四领域完整目录计数与生成漂移检查，Art 验证混合依赖和返工说明。
- [x] [SC-002] 同步固定插件快照并公开发布；在实际安装副本复验场景资料、首次安装和代表任务。目录检查不得替代逐命令执行、完整 GUI 和创作质量验收。

- [x] [FIRST-FAIL-001] 为首次安装失败补充当前技能自身安装路径与运行时目录的结构化诊断；确认缺失行为失败测试，再验证单技能安装边界及原生调用错误不误报为依赖失败。固定发行和安装副本复验单独记录。

- [x] [SC-004] 将固定原生快照新增的七条画笔预设／图层视图命令纳入反射、参数说明、分类场景和公开计划入口；增加目录集合一致性门禁、单技能资源检查与代表性原生执行证据，再执行固定发行和安装复验。

SC-004 固定安装证据：`docs/evidence/craft-photo30-art96-fixed-first-use-20261007.json`。仅关闭755目录增量与新增命令安装执行门禁；全量上下文、完整V1及通用Skills CLI保持开放。

- [x] [SC-005] 发布严格 JSON 命令计划解析的独立技能源并同步固定插件快照；执行实际安装入口的重复键拒绝与有效计划复验，核对技能摘要及未创建输出／缓存。保留已发布标签；源候选测试不替代安装后或完整首版验收。

2026-10-07 逐技能独立空运行时首用补证：`docs/evidence/craft-fixed64-every-skill-cold-first-use-20261007.json`。固定 Film／Effect／Vector 插件dev.30、Photo插件dev.31、Art插件dev.97，全部64技能各自单独复制至隔离项目 .agents/skills，经默认公开下载验证版本和命令发现（620.155秒）；每项结束移除本项运行时，后项不复用缓存，全部原安装摘要不变。本仓13项通过。仅补齐逐技能CLI冷启动范围；实际通用Skills CLI安装、全部命令执行上下文和完整V1仍开放。

2026-10-07 原首版代表任务固定安装复验：`docs/evidence/craft-fixed-v1-representative-native-baseline-20261007.json`。四领域当前固定安装副本分别从空运行时通过原生创作／重开／局部返工／导出，全部64安装摘要保持；Film字幕配音同步与素材移动、Effect改字保留动画、Photo图层蒙版PSD和尺寸变体、Vector多画板布尔改色与SVG/PDF/PNG均有实际测试。仅补充代表任务证据，不据此关闭所有领域、专项场景、全部命令或完整V1任务。

2026-10-07 固定安装专项首用补证：`docs/evidence/craft-fixed-installed-task-scenes-first-use-20261007.json`。38项真实原生测试通过，覆盖37个不同场景技能，各自从空运行时公开安装，目标修改、重开／导出与非目标保全有业务断言。Vector选择技能新增独立选择后移动图标并保留品牌画板测试；现有发布技能未改动。剩余五项领域专项、Art角色专项、实际Skills CLI和完整V1保持开放。

2026-10-07 专项补证：`docs/evidence/craft-fixed-additional-task-scenes-20261007.json`。新增多机位、时间文本转录、滤镜和Puppet四项固定安装原生验收通过，累计42项测试／41个领域场景技能；跟踪合成可渲染，但视频纹理未出现在预期像素且实际分析关键帧为0，未通过且保留失败回归。64个安装摘要保持。自动ASR、Art角色专项、实际Skills CLI及完整V1继续开放；未修改发行技能或原生运行时。

2026-10-07 跟踪根因与固定安装复验：`docs/evidence/craft-fixed-tracking-supported-input-20261007.json`。原输入使用原生不支持的lossless transform bypass；受支持H.264 High下独立冷安装、参考像素、12个实际关键帧、应用与重开及控制对象保全通过，累计43项／42个领域场景技能。每种编码、全部跟踪命令、Art角色、通用Skills CLI及完整V1仍开放；指南更新尚为技能源候选。

3.13源码候选证据：`docs/evidence/photocraft-output-execution-candidate-20261007.json`。公开入口红例、7项竞争／中断保护与冷原生创建／返工通过，固定安装3.14及完整TX合同仍开放。

3.14固定发行证据：`docs/evidence/craft-three-domain-output-guards-fixed-first-use-20261007.json`。全部领域技能独立空缓存、安装7项保护及实际原生创建／返工通过，全部64安装摘要保全；Art捆绑升级与完整TX合同保持单独门禁。

2026-10-08 独立技能事实源（PC-SK-001）完整合同验收：旧共享脚本的12项边界测试出现17个失败断言；修复链接拒绝、全部来源／旧目标预检、固定标签命名空间及完整锁检查。公开固定来源检出与当前64安装身份核对通过；当前Python回归18项（18通过／0条件跳过）。关闭本需求三项任务，不关闭实际Skills CLI、原生创作或完整V1。证据 `docs/evidence/vendor-self-contained-20261008.json`。

- [x] [PC-SK-003-PATH-SELF] 修正新增场景技能的自身安装目录例示，并在新固定插件安装副本上逐个独立冷启动、核对运行时与技能保全。源码路径检查与三布局帮助入口通过；完整SK-003及通用Skills CLI仍独立验收。

2026-10-08 固定安装复验完成：当前矩阵64技能零加载错误；六个有变更技能在自身目录与空缓存中使用固定公开原生CLI，通过准确版本、实时目录及自带参数查询，目录／用户文件保全。完整SK-003与通用Skills CLI不由此关闭。证据 `docs/evidence/craft-scenario-paths-fixed-first-use-20261008.json`。

- [x] [PC-CM-001-SAVED-SELECTION] 补齐羽化选区保存／重开恢复／蒙版局部返工实例、完整选区通道命令分类和真实首用测试；验证灰度覆盖、通道与对照保全、错误停止及固定发行单技能复验；不据此关闭全部选择、AI及印刷上下文。 证据：`docs/evidence/photocraft-saved-selection-fixed-first-use-20261008.json`。

## Optimization task policy — 2026-10-08

以下为 2026-10-08 分析阶段新增的可执行细化任务，创建时全部未完成。当时授权只写规范与任务；后续用户已授权完成计划任务，当前按逐项证据实施和勾选。发布／安装仍按对应授权执行，未满足验收前不执行 sync 或 archive。原第 1–8 节与历史完成项原样保留；新任务细化对应未完成总任务，不要求对同一未变化事实重复运行测试。总需求关闭必须覆盖新增场景，细化子项完成不能替代原总验收；PC-DM-004 等已关闭范围不被扩展任务借用。

通用验证合同：测试先因目标行为缺失失败，再最小实现与受影响回归；候选源码、固定发行和实际安装副本的证据分开。每份记录绑定需求／场景、源码提交、输入与产物摘要、技能来源、运行时、平台及实际宿主，报告 PASS／FAIL／NOT_RUN。发行、安装和外部调用仅在各自授权范围内执行，本任务表不自动触发这些操作。

## 9. P0：入口、路由与发行身份

- [x] 9.1 [PC-SK-004] 建立 cli／filters 触发冲突、明确指定技能、最短链、单技能隔离及生成副本漂移的正反例；检查每项输入／副作用／恢复／验收与拒绝示例。责任：Skills owner；前置：读取新增场景合同与原有 SK-003；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/routing-contract/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 9.2 [PC-SK-004] 在独立技能源调整 use／cli／setup／领域描述与路由，补齐场景参考和示例；从唯一维护来源生成公共资源，保留旧 use 与单技能自足入口。责任：Skills owner；前置：9.1；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 9.3 [PC-SK-004] 逐技能隔离安装并验证文档与资源完整、合法旧入口和代表任务；锁定发行后复验，模型派发证据交 13.4–13.6 单独验收。责任：QA owner；前置：9.2 及对应固定来源可用；产物：docs/evidence/optimization/routing-contract/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [x] 9.4 [PC-TX-005] 覆盖所有公开入口的重复键、NaN／Infinity／溢出、错误容器／未知字段、素材与引用依赖；用安装／会话调用计数确认提前拒绝，并复现普通工作流回复与网关语义差异。责任：Skills owner；前置：读取全入口合同与现有 JSON／MCP 故障回归；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/entry-contract/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 9.5 [PC-TX-005] 在独立技能源统一严格计划解析、静态预检、动态引用检查、工具回复与结构化错误；验证通过才写成功回执，保持文字／图片合法回复及失败保全兼容。责任：Skills owner；前置：9.4；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [ ] 9.6 [PC-TX-005] 验证有效创建／另存修订、真实保存后畸形及语义错误、后续编辑停止、unknown 不重放、原文件重开；候选和固定安装副本分别记录，预检失败零安装／零会话／零输出。责任：QA owner；前置：9.5 及对应固定来源可用；产物：docs/evidence/optimization/entry-contract/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [x] 9.7 [PC-RL-003] 建立同一版本声明冲突、活动锁误指历史锁、维护版误称上游官方、旧标签被替换等发行拒绝 fixture；合法独立版本映射通过。责任：Release owner；前置：读取当前插件、技能、套件、运行时与公共协议身份；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/release-identity/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 9.8 [PC-RL-003] 在各事实源增加当前组合一致性检查及生成说明，明确上游与维护版、套件版本语义和非活动根锁；同步双语当前说明，保留历史证据原值。责任：Release owner；前置：9.7；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [ ] 9.9 [PC-RL-003] 对候选及获授权的固定发行安装副本核对当前组合、来源摘要、旧版保全与发行拒绝；不因元数据一致提升宿主或创作状态。责任：QA owner；前置：9.8 及对应固定来源可用；产物：docs/evidence/optimization/release-identity/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

## 10. P1：能力快照与持久化控制

- [x] 10.1 [PC-RT-002] 建立同命令 ID 参数 schema 改变、后端切换、过期会话和 enabled／授权分离测试；先确认内容级能力漂移缺失。责任：Runtime owner；前置：9.5 的统一执行契约；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/capability-snapshot/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 10.2 [PC-RT-002] 在独立执行器和插件适配层绑定真实运行时／后端／会话及参数 schema 摘要；逐步检查动态文档与选择，漂移停止并保留旧组合。责任：Runtime owner；前置：10.1；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 10.3 [PC-RT-002] 分别验证支持的 headless 与 desktop 固定运行时正常探测及 schema 漂移拒绝；记录平台、后端与快照，不将该子门禁代替完整升级回退 2.6。责任：QA owner；前置：10.2 及对应固定来源可用；产物：docs/evidence/optimization/capability-snapshot/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。 验收证据：`docs/evidence/optimization/capability-acceptance-audit.json`（固定dev.42／技能源dev.38，macOS arm64双后端14例；2.6完整升级回退仍开放）。

- [x] 10.4 [PC-TX-001] 建立共享工程不同输出竞争、桌面未保存版本、过期 epoch 回执和独立不可变源副本的并发测试。责任：Harness owner；前置：9.5、10.2；关联原 3.1–3.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/project-ownership/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 10.5 [PC-TX-001] 在插件账本实现工程／会话写入权、版本前置条件和 epoch，关联已有输出登记；独立副本不被无理由串行化，未知 GUI 状态拒绝写入。责任：Harness owner；前置：10.4；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [ ] 10.6 [PC-TX-001] 在真实原生及声明支持的桌面边界验证竞争、迟到回执、用户改动保全和重启；旧 3.13／3.14 同目标证据只按其范围复用。责任：QA owner；前置：10.5 及对应固定来源可用；产物：docs/evidence/optimization/project-ownership/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [x] 10.7 [PC-TX-002] 建立提交前后崩溃、丢失回执、进程已退出但产物存在、损坏／旧账本、同键不同输入和查询无副作用的失败测试。责任：Harness owner；前置：10.5；关联原 3.4–3.6；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/task-recovery/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 10.8 [PC-TX-002] 实现插件本地 photocraft-harness 与持久化 status／reconcile，关联任务、意图、回执和检查点；保全旧记录，核清后按授权恢复为检查或关联新修订，不重放未知编辑。责任：Harness owner；前置：10.7；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 10.9 [PC-TX-002] 验证真实保存后中断、进程与文件核对、独立查询、损坏状态拒绝和可核验检查点恢复；记录重复编辑次数为零及证据不足时持续 reconciling。责任：QA owner；前置：10.8 及对应固定来源可用；产物：docs/evidence/optimization/task-recovery/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [x] 10.10 [PC-TX-003] 建立重启预算归零、父子重复重试、取消后迟到结果、非任务进程误终止及磁盘预留不足测试。责任：Harness owner；前置：10.8；关联原 3.7–3.9；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/task-budget-stop/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 10.11 [PC-TX-003] 实现持久时间／截止时间／并发／磁盘与修订计数、stop 对 cancel 合同的映射；只控制自有进程，未核清前保留占用并停止新操作。责任：Harness owner；前置：10.10；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [ ] 10.12 [PC-TX-003] 验证受控原生进程取消、中断重启、资源不足拒绝和迟到产物登记；证明 cancelled 需停止证据，本地流程无新增云登录／积分审批。责任：QA owner；前置：10.11 及对应固定来源可用；产物：docs/evidence/optimization/task-budget-stop/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

## 11. P2：质量、受限修订与血缘

- [x] 11.1 [PC-QA-001] 建立技术失败但视觉高分、旧请求／错误摘要、重复回执、评估缺失及生成者自评冒充独立评估的拒绝测试。责任：Harness owner；前置：10.8 与当前交付完整性；关联原 6.1–6.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/bound-review/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 11.2 [PC-QA-001] 实现 verify、judge／import-judge 协调与请求／回执校验，绑定需求、参考、工程、预览、量表和评估器；各验收状态独立，记录实际上下文隔离方式。责任：Harness owner；前置：11.1；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 11.3 [PC-QA-001] 以真实原生候选及宿主／外部／人工中实际声明支持的评估路径验证回执闭环；未支持路径保持 NOT_RUN，证明技术失败及旧候选不能 completed。责任：QA owner；前置：11.2 及对应固定来源可用；产物：docs/evidence/optimization/bound-review/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [x] 11.4 [PC-QA-002] 建立无问题改动、越界属性、基础版本冲突、保护对象变化、重复索取已有授权及无改善／预算耗尽的停止测试。责任：Harness owner；前置：11.2、10.11；关联原 6.4–6.6；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/bounded-revision/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 11.5 [PC-QA-002] 实现问题到图层／属性／区域的修订提案与白名单校验；绑定基础工程／清单及授权，另存执行并复查实际差异，禁止隐式无限循环。责任：Harness owner；前置：11.4；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [ ] 11.6 [PC-QA-002] 用真实改标题、局部调整和拒绝越界案例证明目标变化、非目标保全、版本冲突及有限轮停止；新候选重新评估，保留最佳已验证版本。责任：QA owner；前置：11.5 及对应固定来源可用；产物：docs/evidence/optimization/bounded-revision/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [x] 11.7 [PC-AR-001] 建立混合轮次预览／评估、父版本冲突、移动包和旧包缺少血缘字段的兼容与拒绝测试。责任：Harness owner；前置：11.5；关联原 5.1–5.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/artifact-lineage/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 11.8 [PC-AR-001] 实现本地交付到固定 craft-artifact/v1 的映射，关联逻辑资产、不可变版本、父版本、任务、计划、输入、能力及评估；公共字段需求回权威仓，不另造协议。责任：Harness owner；前置：11.7；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [ ] 11.9 [PC-AR-001] 验证真实创建、修订和移动包全链身份与旧包只读兼容；篡改及串用证据拒绝；安装副本复验，完整性与来源真实性／创作接受分开。责任：QA owner；前置：11.8 及对应固定来源可用；产物：docs/evidence/optimization/artifact-lineage/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

## 12. P2：领域结果与复杂场景验收

- [x] 12.1 [PC-DM-001] 建立嵌套组、空壳层、同名异类型、父子／顺序／可见性改变和整体扁平化的业务失败用例。责任：Domain owner；前置：9.5；关联原 4.1–4.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/recursive-layers/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 12.2 [PC-DM-001] 在独立技能源扩展递归对象身份与可编辑性断言，保留旧合法工程与角色映射；原生保存重开后核验对象关系和非目标对象。责任：Domain owner；前置：12.1；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 12.3 [PC-DM-001] 验证真实嵌套工程的定点修改、重开再编辑和负例拒绝，保存前后结构及原生摘要；固定安装验收不只统计图层数量。责任：QA owner；前置：12.2 及对应固定来源可用；产物：docs/evidence/optimization/recursive-layers/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。

- [x] 12.4 [PC-DM-002] 建立蒙版错绑／禁用、选择误当蒙版、保护区变化及不支持颜色模式／深度的拒绝用例。责任：Domain owner；前置：12.2；关联原 4.4–4.6；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/mask-protection/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 12.5 [PC-DM-002] 在独立技能源核验蒙版关系、局部作用和可编辑性，明确像素检查器支持边界；不可核验的保护约束不能静默跳过。责任：Domain owner；前置：12.4；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 12.6 [PC-DM-002] 在固定安装的真实工程上验证目标像素与蒙版、非目标区域和源包保全；额外格式单独记录未知或拒绝，不外推 RGBA8 证据。责任：QA owner；前置：12.5 及对应固定来源可用；产物：docs/evidence/optimization/mask-protection/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。

- [x] 12.7 [PC-DM-003] 建立文本溢出、缺字／替代、换行／字距变化和非目标文字改变用例，区分精确排版要求与能力未知。责任：Domain owner；前置：12.2；关联原 4.7–4.9；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/text-layout/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 12.8 [PC-DM-003] 扩展文字布局断言与替代接受记录，保留组内字体检查及无文字工程兼容；不可获取的布局指标保持 unknown。责任：Domain owner；前置：12.7；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；只关闭本项测试／最小实现，同组完整验收保持开放。
- [x] 12.9 [PC-DM-003] 以真实中文与混合文字定点修订验证内容、字体、布局及源工程保全；保存重开和适用交换结果分别记录，固定安装复验。责任：QA owner；前置：12.8 及对应固定来源可用；产物：docs/evidence/optimization/text-layout/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。

- [x] 12.10 [PC-DM-005] 建立 PSD 重开但文字／蒙版／效果丢失、图层数相同但属性降级的负例和真实使用功能矩阵。责任：Domain owner；前置：12.2、11.8；关联原 4.13–4.15 与 5.6；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/psd-feature-fidelity/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 12.11 [PC-DM-005] 按工程实际使用功能生成保留／降级／丢失／未知及绑定证据，兼容既有 exchange-loss 的 lost／observed／unknown，不把 observed 自动等同保真。责任：Domain owner；前置：12.10；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 12.12 [PC-DM-005] 验证原生与 PSD 功能矩阵及未接受有损替代拒绝；声明外部编辑器兼容时记录实际版本和独立复验，未运行项保持未知。责任：QA owner；前置：12.11 及对应固定来源可用；产物：docs/evidence/optimization/psd-feature-fidelity/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。 固定 dev.40／技能源 dev.36 场景验收：`docs/evidence/optimization/psd-acceptance-audit.json`；未验证外部编辑器及完整保真保持未知。

- [x] 12.13 [PC-DM-007] 建立嵌套角色变换／重复或歧义映射／安全区越界，以及背景滤镜侵入产品／烘焙伪称可编辑的失败用例。责任：Domain owner；前置：12.5、12.8；复用 PC-DM-004 原有合同；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/complex-layout-filters/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 12.14 [PC-DM-007] 实现递归布局角色变体与滤镜目标／选择／蒙版合同，明确可编辑和烘焙路径及支持能力，保持现有简单尺寸变体兼容。责任：Domain owner；前置：12.13；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。 候选实施证据：`docs/evidence/optimization/task-progress.json`；本项只关闭测试／最小实现，不关闭同组完整验收。
- [x] 12.15 [PC-DM-007] 在真实嵌套变体和背景虚化／颗粒／锐化任务中核验目标效果、可编辑性及保护范围；固定安装复验，新需求不能由 PC-DM-004 旧证据关闭。责任：QA owner；前置：12.14 及对应固定来源可用；产物：docs/evidence/optimization/complex-layout-filters/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。 固定安装场景证据：`docs/evidence/optimization/domain-acceptance-audit.json`；仅关闭当前锁定版本及声明边界，完整 V1 门禁不变。

## 13. 持续门禁：逐命令与真实宿主

- [x] 13.1 [PC-CM-001] 建立逐命令验收清单缺项、仅目录映射冒充 PASS、能力快照失效及上下文不适用的检查 fixture。责任：Skills owner；前置：9.5、10.2；细化原 8.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/command-acceptance/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选测试证据：`docs/evidence/optimization/task-progress.json`；六项索引／上下文／过期与绑定证据测试通过，13.2／13.3 仍开放。
- [ ] 13.2 [PC-CM-001] 维护每条命令所需文档／选择／素材／权限／后端、结果断言、原生保存与局部修订证据索引；接入候选测试及包内执行资源回归。责任：Skills owner；前置：13.1；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。
- [ ] 13.3 [PC-CM-001] 按固定目录在适用上下文逐项执行并核验真实结果，记录固定安装及源／输入／产物摘要；FAIL／NOT_RUN 保留，不适用说明理由且不减少 8.3 原验收范围。责任：QA owner；前置：13.2 及对应固定来源可用；产物：docs/evidence/optimization/command-acceptance/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

- [ ] 13.4 [PC-RL-001] 建立静态与模型路由分层的测试集及负例，覆盖改标题、背景虚化保留产品、已有工程导出、超时继续和显式技能；预先固定重复次数、通过标准及评估宿主／模型配置。责任：Release owner；前置：9.2 可开始路由；最终关闭依赖所有适用实现与原生门禁；关联原 7.1–7.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/host-evidence/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。
- [ ] 13.5 [PC-RL-001] 把目录、离线故障、原生、固定安装、宿主模型与创作评审接入分层证据流程；实现源码／输入／快照摘要关联与过期证据拒绝，状态页不由目录数推导可用性。责任：Release owner；前置：13.4；产物：对应仓库实现、用例与候选记录；验证：目标测试及受影响回归通过，不修改已发布快照充数。
- [ ] 13.6 [PC-RL-001] 在实际宿主和固定发行执行路由及任务验证，保留逐次选择链、越界／重复编辑次数和真实产物；完成必要跨仓消费复验，未执行平台、模型和真实服务明确 NOT_RUN。责任：QA owner；前置：13.5 及对应固定来源可用；产物：docs/evidence/optimization/host-evidence/ 验收记录；验证：本组全部规范场景有当前证据，不能以静态检查或候选通过代替固定安装／真实场景。

## Candidate implementation evidence — 2026-10-08

后续实施授权已生效；本轮已完成候选源码与本地回归。新增勾选仅覆盖有证据的测试／最小实现；同组真实全场景、固定发行安装、真实宿主与独立创作验收保持开放。[任务证据](../../../docs/evidence/optimization/task-progress.json) 逐组记录范围、未完成项与下一步；[完整候选回归](../../../docs/evidence/optimization/candidate-validation.json) 绑定源码、测试输入和原生结果。基线红灯重建单独标注，不伪称历史原始执行日志。

## Fixed domain acceptance — 2026-10-08

当前插件 dev.39／技能 dev.35 的 macOS arm64 固定安装已完成 PC-DM-001／002／003／007 的16个规范场景核对，新增关闭7项领域验收。累计120/157项完成、37项开放。真实首用、追加原生、蒙版像素与绑定证据及首轮失败记录见[逐场景审计](../../../docs/evidence/optimization/domain-acceptance-audit.json)；[复验方式与边界](../../../docs/PhotoCraft-Fixed-Domain-Acceptance.zh_CN.md)。PSD 必要功能损失、导出来源、运行时升级、宿主模型及完整命令等门禁保持开放，不同步／归档。
