# 已保存检查点的显式修订候选

失败后先核对原任务、原进程和保存工程，不重放未知操作，不换目录或幂等键绕过占用。插件任务通过`recover`创建关联子任务，必须有原监督退出证明、原任务／工作令牌绑定、已核验检查点、对象授权及剩余预算。独立技能的低层入口不替代这些任务门禁。

本技能工作流支持`--checkpoint <原失败输出> --write-root <已有授权根>`，与`--source`互斥。新计划必须声明`expectedCheckpointSha256`、`expectedCheckpointPlanSha256`、`expectedProjectSha256`，使用核验后的绑定或明确图层ID，并为局部变更声明`preserveObjects`。原工程另存副本后只执行新计划，不重放原operations。

失败暂存必须有受failure文件清单保护的`recovery-context.json`，记录原计划、运行时／能力、登记资产及已验证绑定。旧记录缺少上下文时只读核对，不能补造成功manifest获得恢复权。原文件保留，新的`checkpoint-origin.json`记录来源摘要；技术通过仍需独立创作评审及用户接受。

当前为候选实现；固定安装及完整重启矩阵完成前不宣称完整PC-TX-002或V1通过。

## 硬中断后的持久进度

每次原生调用前持久化 submitted，回复严格确认后持久化 reply_validated；原计划、绑定、资产、能力和暂存目录身份同存于独立原子进度文件。只读查询：`python3 -I -B "$SKILL_DIR/scripts/progress.py" OUTPUT --write-root AUTHORIZED_ROOT`。读取不安装或启动会话，不修改原认领、工程和进度记录。返回 PASS 仅表示进度观察记录有效，不能替代原工作进程组停止证明、工程重开或检查点修订许可。缺少失败记录的保存工程仍须显式恢复流程，不能补造 failure.json。


独立中断检查点：原监督退出回执及两个进程组确认结束后，`reconcile` 可在授权根中创建新的 `checkpoint.json` 旁车。它绑定原进度、原计划／令牌、暂存 inode、落盘工程与全部依赖、原启动和退出摘要；只读重开前后重新核对。原暂存、进度、认领和未知请求不改写，不补造 `failure.json`。缺少工程、活跃执行者、输入冲突或文件变化保持 reconciling。显式 `recover` 仅创建原授权及累计预算内的新副本，不重放原计划。检查点回执的 `origin.schema=photocraft-checkpoint-context-origin/v2` 直接比较绑定及能力内容，完整原记录／上下文仍由文件 SHA-256 保护，避免 Python／JavaScript 的 `100.0` 与 `100` 摘要分歧。旧失败记录仍可读取；新的核验回执须与当前执行器版本配套。

新执行的 `executionIdentity.planHashAlgorithm` 为 `photocraft-json-f64/v2`：所有有限 JSON 数值按原生 binary64 大端位编码，零与负零统一；JSON 值使用类型标签，键按 UTF-16 排序，字符串使用 ASCII UTF-16 转义后计算 SHA-256。这样小数／科学计数／整数形式和 Unicode 在 Python／JavaScript 中一致；未知算法、非有限数值拒绝。历史记录无算法字段时仍按旧格式核对，不改写旧身份；跨技能源版本的原任务仍受执行器摘要围栏约束。
