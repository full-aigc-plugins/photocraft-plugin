# establish-v1-plugin

定义 photocraft 独立技能、运行时与插件 V1 规格及验收任务

## Optimization update — 2026-10-08

本变更继续作为 PhotoCraft 插件与独立技能源的唯一行为规格事实源。本次新增 4 项需求与 51 项待实施任务，原有 62 项已完成记录保持不变；共 95 项任务仍开放。以上为规划时点状态；后续候选实施进展见下节，不代表完整 V1 验收。

- [增量范围](proposal.md#optimization-scope--2026-10-08)
- [跨仓职责与兼容设计](design.md#optimization-ownership-and-compatibility)
- [分批任务与完成门禁](tasks.md#optimization-task-policy--2026-10-08)
- [机器可读需求映射](../../../docs/traceability.json)

## Candidate implementation — 2026-10-08

已新增完成 51 项测试／最小实现任务；当前 113/157 项勾选，44 项仍开放。技能 201 项完整本地回归含原生／桌面首用通过且零跳过；最近复验仅在技能源摘要及验证层完全相同时复用该记录，插件 TypeScript 27／Python 36 项重新执行通过且零跳过。13 项分层检查通过，原记录与复用摘要均保留。

- [逐组进展及剩余门禁](../../../docs/evidence/optimization/task-progress.json)
- [绑定发行源码的回归证据](../../../docs/evidence/optimization/release-candidate-validation.json)
- [候选架构与使用限制](../../../docs/PhotoCraft-Harness-Candidate.zh_CN.md)

已发布独立技能源 dev.35 与插件 dev.39，固定来源经 vendor 锁定。两条 CI、隔离安装14技能发现、13技能冷启动及安装副本原生执行通过；见[版本绑定证据](../../../docs/evidence/optimization/release-publication.json)。44项完整场景与其他未完成门禁保持开放，未执行 sync/archive。
