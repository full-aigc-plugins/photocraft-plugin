## Why

PhotoCraft 需要将“保留图层的图像编辑与平面设计”落为可独立安装、可追溯、可恢复的 Agent 插件。已安装的上游 CLI 仅证明运行时可用，不能替代技能、Harness 与原生交付验收。

## What Changes

- 建立独立 `photocraft-skills` 的发布与插件锁定引用规范；本变更不把技能源码改成插件私有内容。
- 定义运行时安装、能力探测、任务执行、工程与素材交付、质量修订和宿主发布门禁。
- 固化代表性验收：用产品图制作海报与封面；重开 .pcraft 后文字、产品、背景仍可独立编辑；适用时输出经验证的 PSD。
- 交付中英文产品文档、架构、技术方案与 README；实现按任务与证据逐项推进。

## Capabilities

### New Capabilities

- `skills-distribution`: 独立技能与不可变分发。
- `runtime-distribution`: 运行时安装、能力与回退。
- `task-execution`: 任务状态、幂等、授权与恢复。
- `artifact-delivery`: 原生工程、素材和产物证据。
- `quality-review`: 技术门禁与受限创作修订。
- `release-compatibility`: 宿主、权限与发布验收。
- `domain-workflow`: 保留图层的图像编辑与平面设计。

### Modified Capabilities

无。新仓库没有已实现行为或既有主规格。

## Impact

目标模块为未来的 `src/harness/`、`src/adapters/`、`runtime/`、`schemas/` 与独立技能仓库。四款上游应用保留各自工程格式；现有插件通过公开接口适配。ArtCraft Services 仅作为架构参考，不复制其受限许可代码。

## Non-goals

用户已授权进入五插件及独立技能实施；本阶段不分发 GUI 应用、不接入真实付费生成，未完成宿主与创作验收前不发布市场条目。协议内容属于目标设计，不能当作现有工具。
