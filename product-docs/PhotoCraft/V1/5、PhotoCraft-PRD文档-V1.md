# PhotoCraft V1 — PRD文档

> **文档说明**：V1 实施阅读视图；规范事实源为 OpenSpec。
>
> **版本**：1.0.0
> **最后更新**：2026-10-05
> **状态**：目标设计；尚未实现。事实依据与验收结果单独标注。

关联文档：[品牌边界](../1%E3%80%81PhotoCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](../5%E3%80%81PhotoCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](../../../docs/PhotoCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../../../openspec/changes/establish-v1-plugin/proposal.md) · [证据](../../../docs/evidence/runtime-baseline.json)

## 1. 版本目标与非目标

用产品图制作海报与封面；重开 .pcraft 后文字、产品、背景仍可独立编辑；适用时输出经验证的 PSD。

本 PRD 是规范阅读视图；行为事实源是链接的 OpenSpec。未实现功能保持 planned。V1 不建设全新编辑器或多租户云平台。

## 2. 功能需求

| ID | 需求 | 行为摘要 | Priority | Authority |
| :--- | :--- | :--- | :--- | :--- |
| PC-SK-001 | 独立技能事实源 | 技能 SHALL 在独立技能仓库维护；插件仅同步固定 tag、commit 和 SHA-256 的发布副本；不得使用 latest、分支浮动引用或包外符号链接。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| PC-SK-002 | 独立安装与依赖声明 | 专业技能 SHALL 通过公开 CLI 接口运行；单独安装时不得依赖插件私有路径；ArtCraft 技能 SHALL 明确声明编排运行时依赖。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/skills-distribution/spec.md) |
| PC-RT-001 | 运行时来源与完整性 | 运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| PC-RT-002 | 运行能力与隔离升级 | 适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/runtime-distribution/spec.md) |
| PC-TX-001 | 版本绑定与单写 | 执行 SHALL 绑定 planHash、inputHashes、projectRevision、runtimeIdentity 和有效授权范围；同一工程只有一个写入者，冲突不得覆盖用户修改。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| PC-TX-002 | 幂等与不明确结果恢复 | 任务 SHALL 在副作用前登记幂等键；超时且执行结果未知时进入 reconciling；核对原任务或产物前不得重新提交。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| PC-TX-003 | 取消与预算边界 | 任务 SHALL 区分 cancel_requested 与 cancelled；父子调用共享预算和截止时间；只允许一个层级负责同一副作用的重试。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/task-execution/spec.md) |
| PC-AR-001 | 产物血缘与包完整性 | 产物 SHALL 登记逻辑 ID、不可变版本、内容摘要、来源任务、原生工程和依赖；交付前重新校验文件，移动后可按清单重关联。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| PC-AR-002 | 原生工程与交换损失 | 交付 SHALL 同时保留约定的原生工程与导出；工程需重新打开检查，交换中的扁平化、栅格化、字体和效果损失必须显式记录。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md) |
| PC-QA-001 | 技术与创作证据分离 | 质量结果 SHALL 分别记录工程、技术、创作和接受状态；证据绑定文件摘要及运行身份，NOT_RUN 不得当作 PASS，视觉评分不得覆盖技术失败。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| PC-QA-002 | 受限局部修订 | 质量循环 SHALL 将问题绑定对象、帧或区域及责任插件；设置最大轮数、预算与停滞规则；目标变化使旧验收与授权失效。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/quality-review/spec.md) |
| PC-RL-001 | 宿主与发布证据 | 发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| PC-RL-002 | 权限与秘密边界 | 运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md) |
| PC-DM-001 | 分层文档与编辑身份 | PhotoCraft SHALL 明确文字、产品和背景图层，保留名称、ID、顺序、混合模式与可见性；禁止为通过验收而整体扁平化。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-002 | 蒙版与局部调整 | PhotoCraft SHALL 将蒙版绑定至目标图层并记录作用区域；局部调整前后检查保护区域，确保未授权区域保持不变。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-003 | 文字排版与字体依赖 | PhotoCraft SHALL 保存文本内容、字体、尺寸、行距和布局；缺少字体时阻止需要精确排版的交付或显式接受替代。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-004 | 海报封面尺寸变体 | PhotoCraft SHALL 从源工程创建独立画幅变体，记录裁切、留白和安全区；尺寸变化不覆盖源工程。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-005 | 原生与 PSD 保真 | PhotoCraft SHALL 将 .pcraft 作为原生事实源；PSD 交付逐项验证所用图层功能并记录兼容损失；不宣称所有 PSD 无损兼容。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |
| PC-DM-006 | 平面导出与来源 | PhotoCraft SHALL 输出绑定源文档版本、ICC 或颜色空间与透明要求；外部生成素材保留来源回执，生成服务与图层编辑分开计量。 | P0 | [OpenSpec](../../../openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md) |


## 3. 非功能要求

工程单写；幂等重复不得增加副作用；秘密不得进入回执；所有验收绑定真实产物哈希；计划变化和 GUI 修改必须检测。初始修订上限 3 轮、单项目渲染并发 1 是待验证默认值，不是性能测量。

## 4. 端到端验收步骤

1. 从干净环境安装锁定运行时与技能。
2. 登记 fixture 素材与预期输出。
3. 执行计划，验证工程与导出。
4. 关闭并重开原生工程，检查对象可编辑性。
5. 执行代表性局部修改，比较不变对象。
6. 注入中断并恢复，核对没有重复副作用。
7. 在目标宿主重新执行并记录宿主版本。

## 5. 发布门禁

每个 P0 需求至少有成功与失败证据；未执行项标为 NOT_RUN。技术失败、原生损坏、摘要漂移或重复提交均阻断发布。



---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。
