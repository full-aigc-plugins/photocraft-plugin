# PhotoCraft — release-compatibility

## Purpose

本能力定义 PhotoCraft 在 release-compatibility 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范；已有实现与限定范围证据不等于完整需求验收。

## ADDED Requirements

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

`docs/evidence/codex-current-release.json` binds current fixed releases to two actual Codex CLI/app-server versions, five enabled namespaced skills, installed public workflow outcomes and explicit exclusions. The corresponding bilingual Host-Verification-Architecture documents specify the repeatable check.
