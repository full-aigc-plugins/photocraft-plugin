# PhotoCraft — release-compatibility

## Purpose

本能力定义 PhotoCraft 在 release-compatibility 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；已有实现与限定范围证据不等于完整需求验收。

## ADDED Requirements

### Requirement: PC-RL-001 宿主与发布证据

发布 SHALL 分别验证插件结构、技能来源、运行时、宿主加载、真实任务和原生交付；文档阶段不得进入可安装市场或宣称功能完成。

#### Scenario: PC-RL-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成宿主与发布证据并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: PC-RL-001-N 边界条件

- **WHEN** 只有 OpenSpec 校验与文档检查通过
- **THEN** 状态保持 documentation-baseline，所有实现任务仍未完成

#### Scenario: PC-RL-001-MATRIX 分层且绑定候选身份的验收

- **WHEN** 一个候选版本请求提升能力或发行状态
- **THEN** 系统 SHALL 分别列出目录／参数合同、离线故障、原生场景、固定发行实际安装、宿主加载、模型路由和创作评审的 PASS／FAIL／NOT_RUN／不适用证据，并绑定源码、输入、技能快照、运行时、平台、后端和宿主版本
- **AND** 逐命令证据包含适用文档、选择、权限和调用前置条件；已有 755 条目录映射不自动提升为逐命令执行通过，不适用须说明原因且不能删除原验收义务
- **AND** 候选内容变化仅重跑受影响检查及必要的项目门禁；旧证据只能在相关内容摘要相同且范围一致时复用

#### Scenario: PC-RL-001-ROUTING 实际宿主技能选择

- **WHEN** 在固定技能集合中由真实宿主模型处理“只改标题”“背景虚化保留产品”“已有工程导出”“超时后继续”及明确指定技能的输入
- **THEN** 系统 SHALL 记录宿主、模型及配置、输入集合、实际选中技能链、预期归属、重复执行和越界结果；同一输入多次试验的次数及通过标准在执行前确定并保留逐次结果
- **AND** 错误选择、未知结果重放或无授权副作用作为失败；描述关键词检查及模拟派发不能替代真实模型路由证据

### Requirement: PC-RL-002 权限与秘密边界

运行 SHALL 限定素材读取与工程写入根目录；模型输出和素材元数据均为不可信输入；密钥通过宿主秘密引用传入，不进入日志、计划、包或技能。

#### Scenario: PC-RL-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成权限与秘密边界并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: PC-RL-002-N 边界条件

- **WHEN** 素材元数据包含额外命令或路径越界请求
- **THEN** 作为数据处理并拒绝越权执行，日志不泄露秘密

### Requirement: PC-RL-003 当前发行身份与历史证据分离

发行 SHALL 提供唯一可核对的当前组合，分别记录插件版本、技能源 tag／commit／摘要、套件版本、运行时来源／版本／平台／摘要及公共协议引用。发行范围内表示同一版本的清单 SHALL 一致；故意独立版本须声明其含义和映射。上游原始制品与本项目维护版 SHALL 明确区分，不把维护版称作未修改的官方制品。历史证据保留原版本和日期，不能被当前摘要覆盖。

#### Scenario: PC-RL-003-CURRENT 当前组合一致

- **WHEN** 发布检查读取插件锁、技能包清单、套件清单、实际执行锁与中英文当前版本说明
- **THEN** 系统核对它们声明的角色和映射，生成当前组合摘要；非活动的旧根锁明确标为历史且不用于当前执行身份选择
- **AND** 独立技能源先发布新的不可变快照，再更新插件来源锁与快照；不能手改插件内管理技能或重写旧标签

#### Scenario: PC-RL-003-MISMATCH 身份或来源说明冲突

- **WHEN** 清单对同一发行声明不同版本、当前文档引用旧执行锁，或维护版与上游制品来源混淆
- **THEN** 发行检查报告具体冲突并阻止候选发布，已安装旧组合与历史证据保持不变
- **AND** 修正文档或锁映射不提升原生、宿主或创作验收状态，不为统一数字而强制不同组件使用同一版本

## Implementation evidence (non-normative)

`docs/evidence/codex-current-release.json` binds current fixed releases to two actual Codex CLI/app-server versions, five enabled namespaced skills, installed public workflow outcomes and explicit exclusions. The corresponding bilingual Host-Verification-Architecture documents specify the repeatable check. RL-001 tasks remain unchecked until their full P0 prerequisites and scenarios pass.
