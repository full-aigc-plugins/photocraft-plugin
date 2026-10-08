# PhotoCraft 转换监督候选

插件dev.48锁定技能源dev.42，打包内部run／batch／convert监督候选。公开cli.py及维护版craft.1运行时不变，craft.4单独构建，未自动启用。

只读能力元数据门禁在编辑请求前拒绝不支持的运行时。转换保留原生打开／保存语义，每条回复严格核验，序号1确认后才保存，序号2确认后才成功。保存后未知回复保留真实产物及unknown回执，不重放。能力元数据不能替代二进制来源与摘要核验。

[候选证据](evidence/optimization/supervised-convert/candidate.json)记录30项定向与58项Rust测试；[完整源回归](evidence/optimization/supervised-convert/source-validation.json)：270项通过、零跳过，执行源码指纹未变。覆盖旧运行时零编辑拒绝、四种转换格式、六种真实保存后故障。发布不代表候选固定安装、流式、droplet或完整PC-TX-005验收。9.6继续开放，129/157完成、28开放；旧dev.47固定安装证据保留历史范围，不用于证明本版验收。

[源设计](https://github.com/full-aigc-skills/photocraft-skills/blob/v0.1.0-dev.42/docs/PhotoCraft-Supervised-Convert-Candidate.zh_CN.md)。
