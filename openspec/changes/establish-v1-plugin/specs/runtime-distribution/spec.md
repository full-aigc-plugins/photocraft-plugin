# PhotoCraft — runtime-distribution

## Purpose

本能力定义 PhotoCraft 在 runtime-distribution 范围内对用户、宿主与下游系统承诺的可观察行为、失败语义和验收证据，确保规划、执行与实际交付之间保持可验证的边界。当前为目标规范，尚未实现。

## ADDED Requirements

### Requirement: PC-RT-001 运行时来源与完整性

运行时安装 SHALL 固定制品来源、版本、平台及摘要；在暂存区验证后原子安装，保留许可与安装回执；不执行未经验证的下载内容。

#### Scenario: PC-RT-001-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行时来源与完整性并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: PC-RT-001-N 边界条件

- **WHEN** 下载内容与锁定摘要不符
- **THEN** 拒绝安装且现有运行时仍可使用

#### Scenario: 并行首次安装与复用
- **WHEN** 两个进程同时安装或复用同一锁定 CLI
- **THEN** 安装互斥等待最多 120 秒，取得锁后核验并复用已原子发布的版本；不存在重复下载或部分安装被运行
- **AND** 超时返回 runtime_install_busy，保留已有安装，不自动重放任何编辑或渲染

### Requirement: PC-RT-002 运行能力与隔离升级

适配器 SHALL 核对运行时版本和实际命令 schema，区分 headless 与 desktop bridge；升级必须排空任务、保留回退版本，禁止回退到不兼容状态 schema。

#### Scenario: PC-RT-002-P 合同条件满足

- **WHEN** 请求满足本需求的来源、输入、状态和证据条件
- **THEN** 系统按本需求完成运行能力与隔离升级并返回可核对的结果
- **AND** 结果绑定当前版本与执行身份，不提升未验证能力状态

#### Scenario: PC-RT-002-N 边界条件

- **WHEN** 新运行时缺少计划要求的能力
- **THEN** 执行前报 capability_missing，禁止静默替换工具
