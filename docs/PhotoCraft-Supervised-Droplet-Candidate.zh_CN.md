# PhotoCraft Droplet 监督候选

技能源dev.43及插件dev.49打包内部craft.5 droplet监督模块；公开运行时仍使用craft.1，原生craft.5候选尚未接入。内部原生候选证据不代表固定安装、公开入口接入或完整首版验收。

原生补丁共用旧droplet计划准备，使用原引擎import、临时Session和save_doc，保留0–12 JPEG质量、输入顺序／重复输入及输出优先级。规范化计划、打开、动作与保存各自确认；计划包含质量值，预检后质量变化在打开／动作之前拒绝。原生失败或回复故障停止整个监督批次，普通droplet保留逐文件失败后继续。

[证据](evidence/optimization/supervised-droplet/candidate.json)绑定源码、补丁与二进制。真实保存后故障保留已保存工程并原样重开，输入摘要不变、后续文件调用为零、不重放；红灯记录区分原缺陷、fixture修正与独立磁盘构建失败。

流式、嵌套聚合动作内部、公开来源接入、持久恢复与候选固定安装仍开放；9.6不勾选，129/157完成、28开放。既有dev.48固定验收只适用于craft.1及字节一致的受管理技能。

[独立源设计](https://github.com/full-aigc-skills/photocraft-skills/blob/main/docs/PhotoCraft-Supervised-Droplet-Candidate.zh_CN.md)。
