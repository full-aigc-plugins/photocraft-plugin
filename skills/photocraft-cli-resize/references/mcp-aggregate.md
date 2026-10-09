# MCP与命令计划聚合逐步确认

PC-TX-005／9.6增量：源dev.54／插件dev.69，固定craft.5。公开MCP与craft-command-plan/v1的command_batch统一拆为同会话command_run，每步核验回复后才执行下一步。完整静态参数校验和原生256步上限先于安装／目录创建；stop_on_error:false不绕过失败停止及unknown核对合同。

健康结果保留原生completed／failed／results、合法文字结果、原客户端ID与元数据。命令计划保留批次别名及嵌套结果引用，每个已确认子步骤在下一调用前写入原journal。动态能力、参数schema及enabled前置条件在子步骤前复核；不能借批量绕过后端或当前文档条件。整批截止时间不重置；累计结果沿用原生8MiB限额和包络预留。

原生明确错误停止；重复键、非有限值、错配ID、缺失协议标识、畸形错误或当前已到达的额外回复转unknown。保留原批次、当前子请求、stepIndex、confirmedSteps和已验证子回执；未确认结果不绑定别名，不自动重放。命令计划会话在成功前排空合法通知，拒绝当前挂起的额外回复；此证据不声称能够预测尚未到达的未来帧。

原生测试分别观察真实会话中的图层、原文件和已保存检查点，并以新会话重开检查点；测试只读观察不算恢复编辑。覆盖两类入口各七类回复故障、中间错误、累计限额、健康批量、别名引用及合法通知。候选和公开固定安装证据分别绑定源码与制品。真实桌面聚合、完整启动／MCP输入矩阵、完整9.6及V1仍待各自验收，本增量不关闭任务。

## Owned desktop deadline

The desktop wrapper forwards the remaining batch timeout to the actual stdio MCP session and restores it afterwards. Signed GUI aggregate failure/healthy evidence is separate from headless evidence. Original checkpoints and prior receipts remain preserved; no implicit replay or attachment to a user GUI. Full public input acceptance remains a separate gate.
