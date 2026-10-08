# 已保存检查点的显式修订候选

失败后先核对原任务、原进程和保存工程，不重放未知操作，不换目录或幂等键绕过占用。插件任务通过`recover`创建关联子任务，必须有原监督退出证明、原任务／工作令牌绑定、已核验检查点、对象授权及剩余预算。独立技能的低层入口不替代这些任务门禁。

本技能工作流支持`--checkpoint <原失败输出> --write-root <已有授权根>`，与`--source`互斥。新计划必须声明`expectedCheckpointSha256`、`expectedCheckpointPlanSha256`、`expectedProjectSha256`，使用核验后的绑定或明确图层ID，并为局部变更声明`preserveObjects`。原工程另存副本后只执行新计划，不重放原operations。

失败暂存必须有受failure文件清单保护的`recovery-context.json`，记录原计划、运行时／能力、登记资产及已验证绑定。旧记录缺少上下文时只读核对，不能补造成功manifest获得恢复权。原文件保留，新的`checkpoint-origin.json`记录来源摘要；技术通过仍需独立创作评审及用户接受。

当前为候选实现；固定安装及完整重启矩阵完成前不宣称完整PC-TX-002或V1通过。
