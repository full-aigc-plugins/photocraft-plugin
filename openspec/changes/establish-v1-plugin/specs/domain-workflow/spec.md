# PhotoCraft — domain-workflow

## Purpose

本能力定义 PhotoCraft 在 domain-workflow 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范，尚未实现。

## ADDED Requirements

### Requirement: PC-DM-001 分层文档与编辑身份

PhotoCraft SHALL 明确文字、产品和背景图层，保留名称、ID、顺序、混合模式与可见性；禁止为通过验收而整体扁平化。

#### Scenario: PC-DM-001-P 正常交付

- **WHEN** 输入素材、运行时能力、授权与工程版本有效，用户请求分层文档与编辑身份
- **THEN** 明确文字、产品和背景图层，保留名称、ID、顺序、混合模式与可见性；禁止为通过验收而整体扁平化。
- **AND** 输出可检查的操作结果、工程版本和验收证据

#### Scenario: PC-DM-001-N 异常或不保真

- **WHEN** 输出只有单一扁平图层
- **THEN** 可编辑性门禁失败，即使平面预览正确

#### Scenario: PC-DM-001-SMART 登记智能对象替换与嵌入交付

- **WHEN** 已登记图像经公开素材别名放置为智能对象，或在原工程中替换／重新链接内容
- **THEN** 系统必须拒绝任意路径、未知字段和非法图层引用；保持非目标图层、蒙版与既有变换，并收集登记素材摘要
- **AND** 重新链接的内容在最终交付前转换为嵌入，另存原生工程并重新打开核验；移动包和删除原素材后仍能修订，原交付与技能目录不变
- **AND** 此场景不证明持久外部链接、所有智能滤镜、外部 PSD 编辑器或创作接受

### Requirement: PC-DM-002 蒙版与局部调整

PhotoCraft SHALL 将蒙版绑定至目标图层并记录作用区域；局部调整前后检查保护区域，确保未授权区域保持不变。

#### Scenario: PC-DM-002-P 正常交付

- **WHEN** 输入素材、运行时能力、授权与工程版本有效，用户请求蒙版与局部调整
- **THEN** 将蒙版绑定至目标图层并记录作用区域；局部调整前后检查保护区域，确保未授权区域保持不变。
- **AND** 输出可检查的操作结果、工程版本和验收证据

#### Scenario: PC-DM-002-N 异常或不保真

- **WHEN** 局部蒙版操作改变保护区域
- **THEN** 记录区域差异并拒绝当前修订

#### Scenario: PC-DM-002-GUARD 源工程局部修改保护区域

- **WHEN** 用户对源工程局部修改并在计划中声明非目标矩形保护区域
- **THEN** 公开工作流从实际打开的源工程和实际重开的新工程导出对照 PNG，核对相同画幅和保护区域 RGBA 样本，保存区域摘要与零差异结果
- **AND** 保护区域变化、无效区域、无法核验的 PNG 或尺寸变化均阻止发布新交付，源文件保持不变；该像素检查不替代视觉和创作验收

#### Scenario: PC-DM-002-RETOUCH 修图工作流另存与保护

- **WHEN** 单独安装修图技能后，通过公开源工程工作流选择像素图层并执行笔刷、仿制图章或修复笔刷
- **THEN** 工作流执行真实原生命令，保存并重开独立 `.pcraft`，导出 PNG、适用的 PSD，并记录笔触结果与输入工程摘要
- **AND** 声明的非目标区域保持零像素变化；笔触侵入保护区域时拒绝发布，源交付的所有文件保持不变

### Requirement: PC-DM-003 文字排版与字体依赖

PhotoCraft SHALL 保存文本内容、字体、尺寸、行距和布局；缺少字体时阻止需要精确排版的交付或显式接受替代。

#### Scenario: PC-DM-003-P 正常交付

- **WHEN** 输入素材、运行时能力、授权与工程版本有效，用户请求文字排版与字体依赖
- **THEN** 保存文本内容、字体、尺寸、行距和布局；缺少字体时阻止需要精确排版的交付或显式接受替代。
- **AND** 输出可检查的操作结果、工程版本和验收证据

#### Scenario: PC-DM-003-N 异常或不保真

- **WHEN** 字体替代改变排版但没有接受记录
- **THEN** 阻止精确排版交付并保留原文档

#### Scenario: PC-DM-003-CJK 单文字技能中文标题修订

- **WHEN** 实际安装的单个文字技能从全新缓存创建使用明确已有字体的中文标题，再用源摘要和目标图层另存修改标题
- **THEN** 保留标题图层身份、字体和字号，非目标图层、保护区域像素与源交付不变，原生与适用 PSD 保留中文可编辑 Type 内容
- **AND** 未知图层和缺失字体不得产生成功交付；示例字体和少量字形通过不提升完整中文排版或人工接受状态

#### Scenario: PC-DM-003-NO-TEXT 纯图片工程的字体前置条件

- **WHEN** 单独安装的技能首次创建不含文字层的图片合成，或另存修订该工程
- **THEN** 工作流检查原生图层树，确认没有文字层后不调用仅适用于文字文档的缺失字体命令，保存并重开 `.pcraft`，导出 PNG 与适用 PSD
- **AND** 组内文字仍参与字体检查；未知检查结构或含文字工程的字体检查错误不得被当作无文字跳过；源工程、素材与技能目录保持不变

### Requirement: PC-DM-004 海报封面尺寸变体

PhotoCraft SHALL 从源工程创建独立画幅变体，记录裁切、留白和安全区；尺寸变化不覆盖源工程。

#### Scenario: PC-DM-004-P 正常交付

- **WHEN** 输入素材、运行时能力、授权与工程版本有效，用户请求海报封面尺寸变体
- **THEN** 从源工程创建独立画幅变体，记录裁切、留白和安全区；尺寸变化不覆盖源工程。
- **AND** 输出可检查的操作结果、工程版本和验收证据

#### Scenario: PC-DM-004-N 异常或不保真

- **WHEN** 新尺寸覆盖了源文档
- **THEN** 变体验收失败，使用源检查点恢复

尺寸变体工作流 SHALL bind a requested size variant to its reopened native project, record native canvas offsets or resampling scales, verify distinct preserved background/product/text layer identities, and reject text or product bounds outside the declared safe area before publishing the variant directory.

#### Scenario: Native canvas variant retains editable identities
- **WHEN** a source-bound resize plan declares target dimensions, three layer roles and a safe area
- **THEN** the delivery includes a hashed layout-variant.json with actual geometry operations and reopened layer bounds while retaining the original source files

#### Scenario: Unsafe or inconsistent variant is rejected
- **WHEN** saved dimensions differ or a declared editable role changes identity/type or exceeds the safe area
- **THEN** no variant delivery directory is published and the source remains unchanged

### Requirement: PC-DM-005 原生与 PSD 保真

PhotoCraft SHALL 将 .pcraft 作为原生事实源；PSD 交付逐项验证所用图层功能并记录兼容损失；不宣称所有 PSD 无损兼容。

#### Scenario: PC-DM-005-P 正常交付

- **WHEN** 输入素材、运行时能力、授权与工程版本有效，用户请求原生与 PSD 保真
- **THEN** 将 .pcraft 作为原生事实源；PSD 交付逐项验证所用图层功能并记录兼容损失；不宣称所有 PSD 无损兼容。
- **AND** 输出可检查的操作结果、工程版本和验收证据

#### Scenario: PC-DM-005-N 异常或不保真

- **WHEN** PSD 无法保留所用图层特性
- **THEN** 报告兼容损失并保留 .pcraft，不称为无损

### Requirement: PC-DM-006 平面导出与来源

PhotoCraft SHALL 输出绑定源文档版本、ICC 或颜色空间与透明要求；外部生成素材保留来源回执，生成服务与图层编辑分开计量。

#### Scenario: PC-DM-006-P 正常交付

- **WHEN** 输入素材、运行时能力、授权与工程版本有效，用户请求平面导出与来源
- **THEN** 输出绑定源文档版本、ICC 或颜色空间与透明要求；外部生成素材保留来源回执，生成服务与图层编辑分开计量。
- **AND** 输出可检查的操作结果、工程版本和验收证据

#### Scenario: PC-DM-006-N 异常或不保真

- **WHEN** 输出被更换为同名文件
- **THEN** 摘要不符使先前导出与验收失效

### Requirement: PC-CM-001 完整反射命令使用与执行边界

Photocraft SHALL 为锁定反射目录每条命令保留完整参数原文、场景技能路由、空会话状态、真实同会话调用入口与验收状态；不以有限创作工作流白名单限制直接原生命令使用。原生调用 SHALL 检查当前注册表及可执行状态，保留真实返回值引用、失败回执和不自动重放的超时语义。GUI 连接、工程与素材前置条件 SHALL 明确记录；目录覆盖不等于逐命令原生或创作通过。

#### Scenario: PC-CM-001-P 完整目录与连续调用

- **WHEN** 用户指定锁定目录中的命令及有效原生上下文和参数
- **THEN** 技能 SHALL 给出参数原文和负责技能，在同一原生会话检查并调用命令，连续操作使用真实返回值引用，保存逐步回执
- **AND** 独立安装任何该领域技能仍可查询完整命令说明与使用入口，不能依赖兄弟技能目录

#### Scenario: PC-CM-001-N 错误、禁用与不明结果

- **WHEN** 命令未知、后续计划非法、当前命令禁用、原生返回语义错误或超时
- **THEN** 技能 SHALL 在可确定的最早阶段拒绝，报告命令、前置原因及已执行步骤；超时标为 unknown 且不自动重试
- **AND** 不发布成功回执，不把已收录或仅查询到的命令标为逐命令原生通过，不移除原生禁用或路径守卫

#### Scenario: PC-CM-001-WIRE 已发送请求的协议故障

- **WHEN** 已发送的原生编辑请求返回畸形或非有限 JSON、非对象响应、缺少结果、同时包含结果和错误、畸形工具内容，或写入通道失败使提交状态无法确认
- **THEN** 客户端 SHALL 保留逐步回执并标记 outcome_unknown／unknown，不把协议故障当作编辑未发生，不留下只有 running 的未解释回执
- **AND** 不启动替代会话、不重放请求、不执行后续编辑；已成功写出的原生文件保留，恢复先在新会话检查原文件与原请求身份

#### Scenario: [PC-CM-001-WORKFLOW-REPLY] 原生创作工作流的工具结构检查
- **GIVEN** 公开workflow使用Session.request调用tools/call，原生操作可能已提交
- **WHEN** 结果非对象，isError非布尔，content非数组，内容项非对象，或text类型字段缺失／非字符串
- **THEN** 协议客户端统一抛出outcome_unknown，公开工作流返回结构化错误而非未捕获类型异常，不重放调用。


#### Scenario: [PC-CM-001-INNER-JSON] 内层响应的数值与键不明确

- **WHEN** 已提交请求的工具 text JSON 包含 NaN／Infinity、数值溢出或重复对象键
- **THEN** 完整命令入口 SHALL 在记录成功或绑定返回值前标记 outcome_unknown／unknown，保留原调用及原文件，停止后续编辑且不重放
- **AND** 普通文字与图片工具保持原公开合同；单纯目录和单元测试不能代替固定安装与原生保存重开验收
