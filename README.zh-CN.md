# PhotoCraft Agent Plugin

独立技能驱动的保留图层的图像编辑与平面设计.

[English](README.md) | [简体中文](README.zh-CN.md)

## 当前版本与可复现宿主验证

此前完成宿主验证的插件/技能源版本：`0.1.0-dev.3`。Codex 0.147.0 与 0.153.4 均安装五个固定公开发布，发现全部 58 项启用的命名空间技能，加载错误为零，来源摘要一致。五项代表流程已通过 0.147.0 安装后的场景技能入口验证，包括原生工程、局部修订和 ArtCraft 在线混合流程。模型自动派发、桌面 GUI、创作最终评审和完整交换保真尚未验证。

[宿主验证设计](docs/PhotoCraft-Host-Verification-Architecture.zh_CN.md) · [绑定版本的证据](docs/evidence/codex-skill-suite.json)。历史里程碑保留原证据范围；当前版本身份以 manifest 和锁文件为准。

> 开发版已通过固定标签的 Codex 安装、技能发现和原生代表工作流；完整产品与创作验收仍未完成。

独立技能包已进入实施，单技能隔离安装已在 macOS arm64 实测；完整创作流程与插件宿主验收仍未完成。[证据](docs/evidence/bootstrap-tests.json)

独立技能已实测原生分层编辑、蒙版、局部改字和尺寸变体；合成样例通过 PSD 图层语义与像素往返检查。[工作流证据](docs/evidence/photo-workflow-tests.json)

## 定位

用产品图制作海报与封面；重开 .pcraft 后文字、产品、背景仍可独立编辑；适用时输出经验证的 PSD。

面向需要原生可编辑工程、反复修改和可靠自动化的创作者。

## 一眼了解

```text
Intent + assets
  -> independent Skills (pinned development release)
  -> public skill workflow / ArtCraft adapter
  -> verified runtime / child adapter
  -> native project + preview + export + evidence
```
| Property | Value |
| :--- | :--- |
| Plugin ID | photocraft |
| Metadata version | 0.1.0-dev.11 |
| Stage | implementation-in-progress |
| Skills source | photocraft-skills / v0.1.0-dev.10 |
| Execution | 上游 CLI；ArtCraft 使用子适配器 |
| Host compatibility | Codex development install/discovery pass; GUI and other hosts pending |
| License | Apache-2.0 (original repository content) |


## 能力与边界

| 能力 | 行为边界 | 状态 |
| :--- | :--- | :--- |
| 分层文档与编辑身份 | 明确文字、产品和背景图层，保留名称、ID、顺序、混合模式与可见性；禁止为通过验收而整体扁平化。 | 待完整验收 |
| 蒙版与局部调整 | 将蒙版绑定至目标图层并记录作用区域；局部调整前后检查保护区域，确保未授权区域保持不变。 | 待完整验收 |
| 文字排版与字体依赖 | 保存文本内容、字体、尺寸、行距和布局；缺少字体时阻止需要精确排版的交付或显式接受替代。 | 待完整验收 |
| 海报封面尺寸变体 | 从源工程创建独立画幅变体，记录裁切、留白和安全区；尺寸变化不覆盖源工程。 | 待完整验收 |
| 原生与 PSD 保真 | 将 .pcraft 作为原生事实源；PSD 交付逐项验证所用图层功能并记录兼容损失；不宣称所有 PSD 无损兼容。 | 待完整验收 |
| 平面导出与来源 | 输出绑定源文档版本、ICC 或颜色空间与透明要求；外部生成素材保留来源回执，生成服务与图层编辑分开计量。 | 待完整验收 |

不重写上游编辑引擎，不暗中改变原生交付格式，不宣称 GUI 或跨平台验收完成。

## 架构与文档

- [完整运行时架构](docs/PhotoCraft-Runtime-Architecture.zh_CN.md)
- [技术方案与路线](product-docs/PhotoCraft/5%E3%80%81PhotoCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md)
- [V1 PRD 与需求映射](product-docs/PhotoCraft/V1/5%E3%80%81PhotoCraft-PRD%E6%96%87%E6%A1%A3-V1.md)
- [完整文档导航](docs/README.zh-CN.md)
- [OpenSpec proposal](openspec/changes/establish-v1-plugin/proposal.md)
- [OpenSpec tasks](openspec/changes/establish-v1-plugin/tasks.md)

- [专业领域技术设计](docs/PhotoCraft-Domain-Design.zh_CN.md)

## 当前可执行的快速开始

```bash
python3 scripts/validate_docs.py
openspec validate establish-v1-plugin --strict --no-interactive
```
以上校验文档和规范，不运行产品工作流。OpenSpec 校验使用 1.13.1；本仓不自动安装工具。

已安装官方 CLI 后可执行基础检查：

```bash
photocraft-cli --version
```

本次记录结果为 0.2.0。独立技能的 bootstrap 与 workflow 是当前开发版入口；插件安装与技能发现已有证据；完整宿主验收仍待完成。

## 配置与运行时

目标配置包含 CLI 路径、允许读写根目录、运行模式、预算、超时与输出目录；配置 schema 尚待实现。技能锁文件固定已发布的独立技能源提交与内容摘要。运行时锁文件中的摘要来自真实官方制品，只证明已记录平台的基础运行。

## 可靠性与安全

规划要求：单工程写入锁、版本前置条件、持久化意图、幂等键、不明确结果核对、原生工程检查点、产物摘要及受限修订。密钥只通过宿主秘密引用传递；素材元数据不作为执行指令。

## 验证与成熟度

[脱敏 CLI 证据](docs/evidence/runtime-baseline.json)

| 层面 | 状态 |
| :--- | :--- |
| 上游 CLI 与只读 MCP | 已观察，仅 macOS arm64 |
| 独立技能与适配器 | 技术工作流已验证；完整 Harness 待完成 |
| 原生工程与创作验收 | 原生技术用例通过；创作质量待验收 |
| 目标宿主安装 | Codex 受控安装与发现通过；完整宿主验收待完成 |


## 路线与贡献

| 阶段 | 交付 | 进入下一阶段条件 |
| :--- | :--- | :--- |
| D0 | 双语文档与 OpenSpec 基线 | 文档、链接、规范校验通过；实现任务仍未完成 |
| M1 | 独立技能与运行时适配 | 清洁环境安装、摘要检查、真实 MCP 调用 |
| M2 | 专业领域完整闭环 | 代表任务、工程重开、输出解码、局部修改 |
| M3 | ArtCraft 跨插件协作 | 版本传播、局部失效、断线恢复与幂等 |
| M4 | 宿主与发布验收 | 宿主实装与多平台证据；市场清单一致 |

先更新 OpenSpec 再实现行为；每项任务通过实际验收后才能勾选。中英文文档同时维护。参考 CONTRIBUTING.md 与 AGENTS.md。

## 许可与上游

原创内容遵循 [Apache-2.0](LICENSE)。这是第三方集成规划，不代表上游背书。四款应用的代码许可与 ArtCraft/Services 的受限许可分别处理；不复制上游 ArtCraft/Services 代码或品牌资产。

[Upstream PhotoCraft](https://github.com/storytold/photocraft) · [Issues](https://github.com/full-aigc-plugins/photocraft-plugin/issues)

独立技能现已绑定当前已发布开发标签 `v0.1.0-dev.4`，`skills.lock.json` 固定来源提交与整个技能摘要。使用 `python3 scripts/vendor/skill_vendor.py check` 核对。技能源快照发布不代表宿主验收或生产完成。

## 开发版独立技能安装与使用

安装独立技能：`npx skills add full-aigc-skills/photocraft-skills --skill photocraft-use`。安装技能后，从其真实目录运行公开入口；插件快照也包含相同技能。

```bash
python3 -I -B skills/photocraft-use/scripts/bootstrap.py
python3 -I -B skills/photocraft-use/scripts/workflow.py --help
```

首次入口会安装锁定官方 CLI 到用户数据目录；要求 macOS arm64 与 Python 3.11+。使用技能内示例计划并提供真实素材；交付与修订合同见技能的 SKILL.md。[来源与校验证据](docs/evidence/skill-publication.json)。

## Codex 开发版宿主验证

五个插件已在隔离 Codex 配置中从公开标签安装，app-server 发现带命名空间的技能且无加载错误；安装缓存中的 ArtCraft 入口已交付四种原生工程。[宿主证据](docs/evidence/codex-installation.json)。此为受控开发验收，不代表桌面 GUI、其他宿主、完整创作或正式市场发布通过。

开发版本 `0.1.0-dev.1` 同步独立技能的安装锁等待修复；并行安装和复用按有界互斥协调，原生任务不自动重放。

当前开发里程碑为原生交付增加摘要绑定的交换损失报告，区分 lost、observed、unknown；派生导出不替代原生工程。跨编辑器字体、效果和蒙版保真尚未验证，完整交换验收任务保持未完成。

## CLI 与场景技能体系

技能源包含 12 项可独立安装的技能，分为安装、CLI 公共操作与场景任务。[架构与清单](docs/PhotoCraft-Skill-Suite-Architecture.zh_CN.md)。运行时与插件版本分别维护；旧宿主证据保持原版本范围。

当前插件版本：`0.1.0-dev.5`；技能源版本：`0.1.0-dev.4`。命令示例以宿主实际加载的 `SKILL.md` 所在目录调用脚本。全部技能在用户、项目与插件三种含空格布局中通过隔离入口检查。[路径证据](docs/evidence/installed-skill-paths.json)。此前宿主验证仍对应其记录版本，既有安装需更新。

插件 `0.1.0-dev.5` 从固定公开标签重新取快照并修正整个技能摘要，未带入本地 Python 缓存。插件标签 `v0.1.0-dev.4` 的摘要误包含被忽略的开发缓存，已被替代，不可安装该标签。

当前插件 `0.1.0-dev.6` 固定技能源 `0.1.0-dev.5`。九类独立场景技能通过冷安装及真实原生编辑，验证局部调整蒙版、修图数值范围和保护区域；完整回归 36 项、零跳过。[证据](docs/evidence/task-skill-first-use.json)。完整创作、GUI 与模型派发验收仍未完成。

当前固定发布的宿主核验（2026-10-06）：Codex 0.153.4 安装五个当前固定插件，加载全部 58 技能并逐项核对内容身份。本插件代表性原生工作流从实际安装路径调用，在新的原生运行时中完成创建、重开和修订检查；五工作流调用后，全部 58 个技能摘要保持不变。[证据](docs/evidence/codex-current-release-20261006.json)。显式标签生成器由 ArtCraft 统一持有。模型派发等待授权，GUI、创作与完整宿主验收仍未完成；本次 QA 维护不改变已发布技能/运行时内容或标签。

当前固定发布矩阵（FilmCraft dev.6、EffectCraft dev.7、PhotoCraft dev.6、VectorCraft dev.6、ArtCraft dev.17）在隔离 Codex 安装后通过 58 技能发现及原生代表工作流；执行后所有技能摘要保持不变。[宿主安装内容的原生验证](docs/evidence/codex-release17-native-20261006.json)。此证据不代表模型调度、GUI 或完整创作验收。

固定插件 dev.6／技能 dev.5 的实际安装单文字技能中文海报冷启动与标题修订通过（1 项，5.927 秒）。源文件和保护区域不变，PSD 保留文字且解码像素与 PNG 一致；未知图层和缺失字体被拒绝。人工接受仍为 NOT_RUN。[架构](docs/PhotoCraft-Chinese-Text-Architecture.zh_CN.md)、[证据](docs/evidence/chinese-text-first-use.json)。

候选插件 dev.7 同步固定技能 dev.6，新增源工程局部修改像素保护。原生 CLI 保持 0.2.0。源仓全量原生测试 44 项通过、0 跳过；实际宿主安装复验尚待完成。[架构](docs/PhotoCraft-Protected-Region-Architecture.zh_CN.md)、[证据](docs/evidence/protected-regions-first-use.json)。

固定 PhotoCraft 插件 dev.7／技能 dev.6 与 ArtCraft 插件 dev.30／技能 dev.26 的实际安装原生保护／交接复验通过；五插件全部 58 个技能摘要不变。只完成对应保护任务，整体实现和创作接受仍未完成。[证据](docs/evidence/codex-release30-protected-native-20261006.json)。

候选插件 dev.8 固定 PhotoCraft 技能源 dev.7，接通有界修图工作流。源码 45 项原生回归通过；实际安装后的插件复验仍待完成。[证据](docs/evidence/retouch-workflow-first-use.json)。

固定 PhotoCraft 插件 dev.8／技能源 dev.7 与 ArtCraft 插件 dev.31／技能源 dev.27 通过安装后的原生修图和交接测试（13.260 秒／23.264 秒）。58 个安装后技能摘要全部保持不变。仅完成有界修图任务；完整目标仍未完成。[证据](docs/evidence/codex-release31-retouch-native-20261006.json)。

尺寸变体 / Layout variants: [English architecture](docs/PhotoCraft-Layout-Variant-Architecture.md) · [中文架构](docs/PhotoCraft-Layout-Variant-Architecture.zh_CN.md) · [cold native evidence](docs/evidence/layout-variant-first-use.json). Plugin development version 0.1.0-dev.9 pins independent skills v0.1.0-dev.8; native runtime remains 0.2.0. Installed-plugin cold repetition passed; [version-bound evidence](docs/evidence/codex-photo9-layout-first-use-20261006.json). Full creative acceptance remains open.

固定已安装插件 dev.9／技能源 dev.8 的补充首次使用验收验证分层蒙版海报、改字与封面，并用 Pillow 独立核对三份不透明 PSD 合成图与 PNG 全部 RGB 像素；这与原生图层检查分开，不代表 Photoshop 实际编辑验收。[验收记录](docs/PhotoCraft-Independent-PSD-Acceptance.zh_CN.md)。

纯图片工作流字体前置条件：[架构](docs/PhotoCraft-Font-Preconditions-Architecture.zh_CN.md)。技能源 dev.9 候选通过公开冷启动原生创建／修订与独立 PNG／PSD 检查；固定插件实际安装复验仍待完成。

固定插件 dev.10／技能源 dev.9 通过实际 Codex 0.153.4 安装及单技能纯图片冷启动原生验收（5.601 秒）；58 个已发现安装技能摘要全部不变。升级后的 ArtCraft 固定混合验收单独执行。[证据](docs/evidence/codex-photo10-fontless-first-use-20261006.json)。

固定已安装矩阵 Film9／Effect8／Photo10／Vector11／Art61 通过登记 PNG／JPEG 的 Vector→Photo 替换复用（1 项）、四领域原生首用／恢复／打包（3 项），以及更新的 Photo／Art 全部 22 技能独立空缓存 CLI 检查（190.051 秒）；58 个安装技能摘要保持不变。SVG 混合输入、动态透明序列与完整创作验收仍开放。[证据](docs/evidence/codex-release61-vector-photo-first-use-20261006.json)。

当前固定发行领域场景矩阵：FilmCraft dev.10、EffectCraft dev.9、PhotoCraft dev.10、VectorCraft dev.11 共 37 个原生场景及 6 项合同检查通过，零跳过。每个场景仅复制对应安装技能，从空运行时目录使用默认公开附件安装原生 CLI；核验原生工程、实际像素／音频及局部修改保持，全部 58 项安装身份保持一致。[版本绑定证据](docs/evidence/codex-current-domain-task-matrix-20261006.json)。完整首版、通用 Skills CLI 安装、模型派发、GUI 与创作验收仍开放。

当前插件 `0.1.0-dev.11` 固定独立技能源 `0.1.0-dev.10` 与维护版 CLI `0.2.0-craft.1`，支持登记的可编辑智能对象内容。单技能公开源冷首用通过；实际固定插件安装及 Art 混合验收待执行。[证据](docs/evidence/smart-public-source-first-use-20261006.json)。

固定 Photo 插件 dev.11／技能源 dev.10／维护版 CLI 0.2.0-craft.1 已通过安装副本单技能智能对象放置／替换／重新链接收集与移动修订（4.633 秒）、PSD 独立解码及纯图片回归两项、十二项独立冷启动（51.647 秒）、全部 58 安装摘要、公开附件及四项标签 CI。默认维护版安装与旧官方 0.2.0 并存，旧二进制不变。[版本证据](docs/evidence/codex-photocraft11-smart-first-use-20261006.json)。Art 混合升级及完整首版仍开放。
