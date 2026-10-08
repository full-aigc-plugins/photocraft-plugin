# 检查点来源与显式恢复修订

公开固定插件dev.61／源dev.48在macOS arm64通过全部9个PC-TX-002规范场景，3.6／10.9完成。六窗口包含监督丢失且无退出回执：即使进程组消失仍保持reconciling并拒绝修订。活动运行时仍为0.2.0-craft.1；创作／模型与完整V1门禁保持独立。[当前验收](evidence/optimization/task-recovery/acceptance-audit.json)。

失败暂存保留原位置的工程、素材、回执，并新增受failure文件清单摘要保护的`recovery-context.json`：原计划、执行身份、已验证绑定、登记资产及能力快照。缺少上下文的旧暂存仍可只读重开，但不能补造manifest获得恢复写入权。

```mermaid
flowchart LR
  A[原任务副作用前登记] --> B[原生保存后回复未知]
  B --> C[原位置保全工程和执行上下文]
  C --> D[确认原监督进程及原生组退出]
  D --> E[只读重开并核对原任务与文件摘要]
  E --> F[显式恢复提案和已有授权]
  F --> G[原子预留累计预算并创建关联子任务]
  G --> H[复制已保存工程并执行新操作]
  H --> I[技术门禁和检查点血缘]
  I --> J[独立创作评审及用户接受]
  E --> K[证据不足保持reconciling]
```

插件入口为`node src/cli.ts recover --state-dir <绝对状态目录> --task <原任务ID> --proposal <绝对提案路径>`。提案包含`baseProjectSha256`、`checkpointRecordSha256`、`authorizationRef`、`reason`和`operations`。当前恢复操作支持已有文字内容／样式及图层名称的局部修改；每项绑定明确图层ID，继承对象授权与原保护区域，非目标对象必须保持。新图层创建不是恢复旧未知操作的手段。

恢复前重新reconcile，要求原退出回执与任务、epoch、工作令牌、来源摘要匹配，原进程组已消失，原计划与保存工程一致。不能仅用PID消失或过期锁证明已停止。旧任务attempted和epoch不重置，保留unknown结果；同一显式提案返回同一子任务，修订计数与截止时间不重置。取消、耗尽预算、越权、无变化、源漂移或检查点变化均拒绝新增编辑。

独立工作流接受`--checkpoint <原失败输出> --write-root <已有授权根>`，与正常`--source`互斥。新计划还需三个摘要：`expectedCheckpointSha256`、`expectedCheckpointPlanSha256`、`expectedProjectSha256`。执行前只读重开，复制已保存工程及登记资产，不重放原operations；交付包含`checkpoint-origin.json`。此低层入口不替代插件持久预算和原进程退出门禁。

检查点不是technical PASS的父产物。新产物使用现有craft-artifact/v1的sourceRefs引用`photocraft-checkpoint:<原任务ID>`及工程摘要，并把来源证明列入evidenceRefs，不伪造父交付manifest或父artifact。新产物技术通过后creative和acceptance仍为NOT_RUN，须独立评审与接受。

验证：候选源测试`tests/test_checkpoint_source.py`涵盖保存回复丢失后修改现有标题、原文件保全、计划／记录／工程／资产身份拒绝；插件`tests/checkpoint-revision.test.ts`涵盖原退出证明、授权／预算／提案幂等与新产物血缘。开启插件原生测试时需`PHOTOCRAFT_NATIVE_TEST=1`、`PHOTOCRAFT_SKILL_ROOT`、`PHOTOCRAFT_SOURCE_ROOT`（包含不可变测试代理fixture的源仓快照）及`PHOTOCRAFT_PYTHON`。当前公开安装及全部PC-TX-002场景证据见上方验收；宿主模型、可变GUI写入权及完整V1仍另行验收。

## 完整交付生产者绑定

成功交付将监督器提供的 taskId、taskIdentity、epoch、workerToken、sourceSha256 写入摘要覆盖的 `task-binding.json` 和清单。Harness 核对原账本身份后才重开工程；旧无绑定交付仍可独立只读核验，但不能恢复当前任务接受状态。相同计划外来包与自洽篡改必须拒绝。公开固定dev.61／源dev.48已通过生产者和六窗口PC-TX-002审计；创作接受保持独立。

## 认领前中断

执行器在认领前固定并刷盘计划。只有账本仍为 planned／未尝试时，才复用与原请求字节完全一致的普通单链接文件；预算、幂等身份和原文件不变。截断、外来、链接或目录占位保全并拒绝。已登记意图的任务继续走 reconcile，不因计划可复用而重放。

```mermaid
flowchart LR
  A[原任务预检] --> B[固定计划并刷盘]
  B --> C[登记原执行意图]
  C --> D[监督工作进程]
  B -->|认领前中断| E[重启查询仍未尝试]
  E -->|精确原计划| C
  E -->|文件或身份冲突| F[保全并拒绝]
  D -->|结果未知| G[reconcile 禁止重放]
```

认领前窗口是当前9个规范场景之一；固定公开审计也覆盖工作进程硬中断持久进度及六个中断窗口。

## 原工作进程硬中断进度

status 只读关联原计划、输入、源版本、运行时、工作令牌及暂存 inode，拒绝外来或变化中的快照。监督回执及原进程组确认另外显示；观察本身不创建检查点或升级技术／创作状态。reconcile 可以返回 inspect_interrupted_stage，仍保留未知结果和原 epoch。缺少 failure.json 的暂存不能补造失败记录或直接 recover。


独立中断检查点：原监督退出回执及两个进程组确认结束后，`reconcile` 可在授权根中创建新的 `checkpoint.json` 旁车。它绑定原进度、原计划／令牌、暂存 inode、落盘工程与全部依赖、原启动和退出摘要；只读重开前后重新核对。原暂存、进度、认领和未知请求不改写，不补造 `failure.json`。缺少工程、活跃执行者、输入冲突或文件变化保持 reconciling。显式 `recover` 仅创建原授权及累计预算内的新副本，不重放原计划。检查点回执的 `origin.schema=photocraft-checkpoint-context-origin/v2` 直接比较绑定及能力内容，完整原记录／上下文仍由文件 SHA-256 保护，避免 Python／JavaScript 的 `100.0` 与 `100` 摘要分歧。旧失败记录仍可读取；新的核验回执须与当前执行器版本配套。

```mermaid
flowchart LR
  P[原持久进度] --> S{原监督与进程组均结束}
  S -->|否| R[保持 reconciling]
  S -->|是| C[独立 checkpoint.json]
  C --> V[摘要与依赖核对 / 只读重开]
  V -->|失败| R
  V -->|通过| E[显式 recover / 累计预算]
  E --> N[修订副本 / 重新技术与创作评估]
```

新执行的 `executionIdentity.planHashAlgorithm` 为 `photocraft-json-f64/v2`：所有有限 JSON 数值按原生 binary64 大端位编码，零与负零统一；JSON 值使用类型标签，键按 UTF-16 排序，字符串使用 ASCII UTF-16 转义后计算 SHA-256。这样小数／科学计数／整数形式和 Unicode 在 Python／JavaScript 中一致；未知算法、非有限数值拒绝。历史记录无算法字段时仍按旧格式核对，不改写旧身份；跨技能源版本的原任务仍受执行器摘要围栏约束。
