# PhotoCraft — 命名与品牌说明

> **文档说明**：产品级边界与跨版本决策。
>
> **版本**：1.0.0
> **最后更新**：2026-10-05
> **状态**：目标设计；尚未实现。事实依据与验收结果单独标注。

关联文档：[品牌边界](1%E3%80%81PhotoCraft-%E5%91%BD%E5%90%8D%E4%B8%8E%E5%93%81%E7%89%8C%E8%AF%B4%E6%98%8E.md) · [技术方案](5%E3%80%81PhotoCraft-%E6%8A%80%E6%9C%AF%E6%96%B9%E6%A1%88%E4%B8%8E%E8%B7%AF%E7%BA%BF.md) · [详细架构](../../docs/PhotoCraft-Runtime-Architecture.zh_CN.md) · [OpenSpec](../../openspec/changes/establish-v1-plugin/proposal.md) · [证据](../../docs/evidence/runtime-baseline.json)

## 1. 产品定义与受众

PhotoCraft: 保留图层的图像编辑与平面设计.

面向需要保留编辑能力、反复修改和跨工具交付的创作者，以及构建可靠 Agent 工作流的工程团队。插件负责可执行流程与证据，专业知识由独立技能包维护。

## 2. 名称与发布身份

| Identity | Value |
| :--- | :--- |
| Product | PhotoCraft |
| Plugin ID | photocraft |
| Repository | full-aigc-plugins/photocraft-plugin |
| Skills source (planned) | full-aigc-skills/photocraft-skills |
| Native deliverable | .pcraft |
| Current stage | documentation-baseline |
| Metadata version | 0.1.0-dev.2 |


## 3. 品牌与版权边界

项目是第三方 Agent 集成规划，不表示获得上游官方背书。品牌名称用于描述兼容目标；不复制上游 Logo 或吉祥物。原创文档采用 Apache-2.0。四款应用与 ArtCraft/Services 的许可证分别核对；后者仅参考架构，不复制受限代码。公开发行前由维护者核对名称使用与制品再分发条件。

## 4. 范围与价值边界

用产品图制作海报与封面；重开 .pcraft 后文字、产品、背景仍可独立编辑；适用时输出经验证的 PSD。

不承诺完整复刻商业设计软件、不托管用户账户、不自动发布用户素材。功能支持以能力快照与真实验收为准。



---

**文档版本**：1.0.0
**创建日期**：2026-10-05
**最后更新**：2026-10-05
**文档状态**：待评审；实现以 OpenSpec 任务和证据为准。
