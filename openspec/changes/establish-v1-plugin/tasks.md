# V1 实施任务

> 2026-10-12 过度设计裁剪：删除平台机制范围（PC-TX 任务执行/账本/租约/幂等/取消预算、PC-AR-001 产物血缘、PC-QA 评审闭环、PC-RT-002 隔离升级仪式、PC-RL 发布证据与宿主路由仪式、优化追踪 9.x–11.x 及 13.4–13.6）及其流水账段落；历史见 git 与 docs/evidence/。保留领域功能：技能源/安装、命令覆盖、桌面 GUI、PC-DM 领域工作流与复杂场景验收、PC-AR-002 原生交付。未完成任务收敛为实现导向单行。

> 本清单跟踪高级 V1 行为与完整验收；Agent Plugins 1.0.0 基础包按中央 `unify-craft-plugin-architecture` 变更独立核对。基础包通过不关闭下列开放任务，下列任务也不阻塞基础包结构结论。Harness 的必要性另行评审。

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

- [x] 2.9 [PC-RT-002] 为首次原生下载的SSL EOF建立代表性红绿测试；独立技能源实现最多三次只读下载、丢弃半包并保留完整性边界，同步全部技能，候选回归通过。证据 `docs/evidence/photocraft-native-download-candidate-20261007.json`；仅候选子门禁。
- [x] 2.10 [PC-RT-002] 发布新的不可变技能源和插件，实际安装每个独立技能以空缓存公开安装并核对版本、目录及技能摘要；Art领域包另行升级。

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

- [x] 5.4 [PC-AR-002] 编写能暴露“原生工程与交换损失”缺失的正向与失败测试并确认预期失败。责任：Harness owner；前置：技能/运行时合同已确定；业务调用依赖对应适配器。产物：fixture、断言及失败日志；验证：失败原因必须是目标行为缺失。
- [x] 5.5 [PC-AR-002] 在独立技能源 exchange_loss.py 与公开交付校验 实现“原生工程与交换损失”的最小行为，不扩大支持范围。责任：Harness owner；前置：5.4。产物：对应源码/独立技能源/锁定材料；验证：目标测试和受影响回归通过。
- [x] 5.6 [PC-AR-002] 完成“原生工程与交换损失”真实边界验收并记录版本、平台、输入输出摘要及未验证项。责任：QA owner；前置：5.5。产物：evidence/pc-ar-002/；验证：规范所有场景有证据，且 README 能力状态与证据一致。 固定 dev.40／技能源 dev.36 场景验收：`docs/evidence/optimization/psd-acceptance-audit.json`；未验证外部编辑器及完整保真保持未知。

## 4（续）领域补充验收

- [x] 4.24 [PC-DM-003-NO-TEXT] 确认纯图片首用回归因无文字字体命令失败，再依据原生图层树修复字体前置条件；验证无文字 PNG／PSD 与另存修订、有文字缺失字体拒绝、组内文字检测、源素材和技能摘要不变。
- [x] 4.25 [PC-DM-003-NO-TEXT] 发布不可变技能源和插件快照，使用真实安装单技能、空缓存复验纯图片交付与 ArtCraft 混合流程，记录固定发行版本及未验证范围。

- [x] 4.23 [PC-DM-005] 重新隔离安装固定五插件，使用单导出技能空运行目录创建四图层蒙版海报、标题修订和封面；Pillow 独立解码三份不透明 PSD 合成图与 PNG 全像素比对，保留两个源交付和素材，核对全部 58 技能摘要。产物：docs/evidence/codex-photo9-independent-psd-first-use-20261006.json；不关闭完整 PSD／外部编辑器／创作验收任务。

## 智能对象公开工作流

- [x] 4.26 [PC-DM-001] 建立目标缺失的失败测试，实现登记智能对象放置、转换、替换、重新链接与嵌入交付的参数校验及映射。
- [x] 4.27 [PC-DM-001] 单技能空运行时验证原生保存重开、替换／重新链接、移动包、蒙版／变换／非目标保全及非法输入拒绝。
- [x] 4.28 [PC-DM-001] 发布固定独立技能源与插件，实际安装快照复验公开智能对象首次使用及 Art 混合交接，保全全部安装摘要。

- [x] 4.29 [PC-RT-002] 修复真实首用暴露的环境路径命令禁用缺口，建立目录能力字节输入的维护版补丁、边界回归、可复现构建与公开安装身份；不放开原环境路径守卫。

## 8. 完整命令覆盖

- [x] 8.1 [PC-CM-001] 建立全目录覆盖、后续非法命令、引用、嵌入错误及超时不重放的失败测试；记录目标缺失失败。
- [x] 8.2 [PC-CM-001] 在独立技能源实现完整命令参数说明、技能路由、同会话调用、实时状态检查及逐步回执；同步独立技能资源并验证固定目录覆盖。

- [x] 8.4 [PC-CM-001] 固定技能源与插件公开发行后，真实隔离 Codex 安装／发现全部 58 项；本领域安装副本新入口公开冷安装、原生重开／渲染代表样例及全部技能独立冷启动通过，核对全部安装摘要。仅关闭固定首用子门禁，8.3 全量命令／GUI／修订验收保持开放。证据 `docs/evidence/codex-complete-command-first-use-20261007.json`。

- [x] 8.5 [PC-CM-001] 为每个独立技能补充配套创建／局部返工示例，明确重开后选择前置条件；从空运行时公开安装，直接执行文档计划，检查目标保存重开、非目标对象／像素及原交付／技能摘要。证据 `docs/evidence/complete-command-revision-first-use-20261007.json`；仅代表返工子门禁，8.3 保持开放。
- [x] 8.6 [PC-CM-001] 将返工示例固定发布到独立技能源并通过 vendor 同步插件；实际 Codex 固定安装副本执行新的文档返工计划，复核全部安装摘要，不以旧发行首用证据代替。

- [x] 8.7 [PC-CM-001] 用真实 stdio 子进程复现畸形／非对象／缺失／冲突／非有限响应与断管错误；客户端统一未知结果，完整命令入口保留 unknown 回执且不重放。通过锁定公开原生 CLI 的响应故障代理验证保存实际完成后仅执行一次、后续操作停止、原生重开和文件保全。
- [x] 8.8 [PC-CM-001] 固定发布协议故障修复的独立技能源和插件；实际安装副本冷运行故障代理与健康创建／返工，核对全技能摘要；Art 固定领域捆绑版本单独处理。

- [x] 8.9 [PC-CM-001] 用真实stdio子进程复现公开工作流工具结构缺失检查；Session统一检查tools/call响应，同步独立技能并验证代表原生公开工作流故障与Art编排不重放，固定发布／实际安装单独验收。

- [x] 8.10 [PC-CM-001] 修复完整命令工具内层JSON的非有限值／溢出／重复键歧义，保留unknown回执和原调用；单元红绿回归、同步全部独立技能及候选真实保存后的九类故障／原文件重开通过。证据 `docs/evidence/photocraft-inner-json-command-candidate-20261007.json`；仅候选子门禁。
- [x] 8.11 [PC-CM-001] 固定发布内层JSON修复的不可变技能源与插件，实际安装副本复验未知回执、真实保存与重开、健康命令及全技能摘要；Art捆绑包单独升级，全量8.3保持开放。

- [x] 8.12 [PC-CM-001] 完整目录原生命令接入公开工作流，保持素材收集、原生保存重开、导出及交换损失；核验实时状态、unknown保留和源工程局部返工。候选与固定安装证据分开，8.3保持开放。

- [x] 8.13 [PC-CM-001] 补齐十二个独立技能的调整层／选区蒙版成对原生计划及使用说明；验证原生保存重开、局部像素变化、控制图层与源交付保护、错误层类型拒绝。源候选证据独立记录；不得关闭全量8.3或完整PC-DM-002验收。
- [x] 8.14 [PC-CM-001] 固定发布后在十二个实际安装副本复验调整蒙版首次使用，核对公开下载、不可变摘要及控制区像素。
- [x] 8.15 [PC-CM-001] ArtCraft 锁定并分发新的 PhotoCraft 技能源，对实际安装的混合工作流及局部返工重新验收。

- [x] 8.16 [PC-DS-001] 实现每个独立技能的固定桌面安装、版本及制品身份校验、本地bridge启动与连接检查；错误摘要、平台或运行身份必须拒绝，不覆盖用户应用，不绕过系统安全控制。GUI工具与领域命令接口分别记录。
- [x] 8.17 [PC-DS-001] 在实际固定发布安装副本验证桌面首次使用、真实GUI编辑及原生保存重开，记录活动选择、控制地址、原生工程与输出身份；全量8.3继续保持独立验收。

- [x] 8.20 [PC-DS-001] 针对已观察到的桌面下载TLS握手35错误实现最多三次有限下载重试；清理本次私有下载残留、保持摘要及签名检查，其他失败不增加外层重试，安装重试不得重放编辑；确认失败测试、回归和公开首次安装结果。

## 场景使用指引

- [x] [SC-001] 将完整命令归属清单与业务场景手册纳入独立技能源，验证每条命令唯一归属、参数参考和模板引用可在单技能内读取；四领域完整目录计数与生成漂移检查，Art 验证混合依赖和返工说明。
- [x] [SC-002] 同步固定插件快照并公开发布；在实际安装副本复验场景资料、首次安装和代表任务。目录检查不得替代逐命令执行、完整 GUI 和创作质量验收。

- [x] [FIRST-FAIL-001] 为首次安装失败补充当前技能自身安装路径与运行时目录的结构化诊断；确认缺失行为失败测试，再验证单技能安装边界及原生调用错误不误报为依赖失败。固定发行和安装副本复验单独记录。

- [x] [SC-004] 将固定原生快照新增的七条画笔预设／图层视图命令纳入反射、参数说明、分类场景和公开计划入口；增加目录集合一致性门禁、单技能资源检查与代表性原生执行证据，再执行固定发行和安装复验。

- [x] [SC-005] 发布严格 JSON 命令计划解析的独立技能源并同步固定插件快照；执行实际安装入口的重复键拒绝与有效计划复验，核对技能摘要及未创建输出／缓存。保留已发布标签；源候选测试不替代安装后或完整首版验收。

- [x] [PC-SK-003-PATH-SELF] 修正新增场景技能的自身安装目录例示，并在新固定插件安装副本上逐个独立冷启动、核对运行时与技能保全。源码路径检查与三布局帮助入口通过；完整SK-003及通用Skills CLI仍独立验收。

- [x] [PC-CM-001-SAVED-SELECTION] 补齐羽化选区保存／重开恢复／蒙版局部返工实例、完整选区通道命令分类和真实首用测试；验证灰度覆盖、通道与对照保全、错误停止及固定发行单技能复验；不据此关闭全部选择、AI及印刷上下文。 证据：`docs/evidence/photocraft-saved-selection-fixed-first-use-20261008.json`。

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

## 13. 持续门禁：逐命令验收

- [x] 13.1 [PC-CM-001] 建立逐命令验收清单缺项、仅目录映射冒充 PASS、能力快照失效及上下文不适用的检查 fixture。责任：Skills owner；前置：9.5、10.2；细化原 8.3；产物：对应仓库失败测试／fixture 与 docs/evidence/optimization/command-acceptance/ 红灯记录；验证：失败来自目标行为缺失，环境故障另报。 候选测试证据：`docs/evidence/optimization/task-progress.json`；六项索引／上下文／过期与绑定证据测试通过，13.2／13.3 仍开放。
- [ ] 13.2 [PC-CM-001] 维护每条命令的文档／选择／素材／权限／后端前置、结果断言与原生保存／局部修订证据索引，含回归测试。
- [ ] 13.3 [PC-CM-001] 按固定目录在适用上下文逐项执行并核验真实结果，FAIL／NOT_RUN 保留，含回归测试。

## 14. 执行载荷收敛

- [x] 14.1 [PC-SK-003] 完成 13 份单技能运行资源的限定审计与可达性分析：带扩展名子串＋引号内无扩展模块名两遍法，自 12 个文档化入口闭包，42/42 执行文件可达、无真孤儿；确认不能仅凭文件名删除模块。结果与本迁移证据：`docs/evidence/photocraft-harness-convergence-20261013.json`。
- [x] 14.2 [PC-SK-003] 收敛重复执行实现（保留单技能独立安装、旧公开入口与防重放）。结果：技能源 v0.1.0-dev.60（本地 commit c267692，未 push）新增内置 photocraft-harness 技能承载唯一执行载荷（12 入口＋42 文件逐字节一致＋5 执行契约 JSON），13 个领域技能删除各自 scripts/ 并按名称路由（HARNESS_DIR）；插件已重 vendor 至该标签并通过 `skill_vendor.py check --offline` 与等价冒烟（cli/commands/route/bootstrap/delivery 入口）。上游全量回归 373 项通过（85 项显式 opt-in 跳过）；插件 unittest 66/68 通过，剩余 2 项失败为 2026-10-12 裁剪并行工作树的 132 条 spec/task 追溯预存错误（HEAD＋裁剪基线复现完全相同，与本迁移无关）。证据：`docs/evidence/photocraft-harness-convergence-20261013.json`。
