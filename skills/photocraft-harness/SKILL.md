---
name: photocraft-harness
description: 当 PhotoCraft 任务需要跨会话状态查询、结果未知后的核对、停止自有执行、提交独立评审回执、导出或检查可移动血缘包，或从已保存检查点显式恢复修订、按问题进行受限另存修订，以及显式查询、升级或回退运行时组合时使用。只查询命令或执行一次领域操作时由对应 PhotoCraft 技能负责。
---

# PhotoCraft 任务控制

从本技能实际加载目录定位插件根目录；读取 [执行合同](references/execution-contract.md)。需要 Node 24.15+（小于 25）和 Python 3。插件技能来源仍由 `skills.lock.json` 固定，插件本地技能不混入独立技能包。

## 调用

使用插件根目录的 `src/cli.ts`：

```bash
node "$PLUGIN_ROOT/src/cli.ts" --help
node "$PLUGIN_ROOT/src/cli.ts" create --state-dir "$STATE_DIR" --request "$REQUEST_JSON"
node "$PLUGIN_ROOT/src/cli.ts" run --state-dir "$STATE_DIR" --task "$TASK_ID"
node "$PLUGIN_ROOT/src/cli.ts" status --state-dir "$STATE_DIR" --task "$TASK_ID"
node "$PLUGIN_ROOT/src/cli.ts" reconcile --state-dir "$STATE_DIR" --task "$TASK_ID"
node "$PLUGIN_ROOT/src/cli.ts" stop --state-dir "$STATE_DIR" --task "$TASK_ID"
```

路径必须是规范化绝对路径，用户路径中的符号链接被拒绝。状态目录为本机私有持久数据，不提交仓库。`run` 先验证计划和输入，再记录意图并执行。相同幂等键只代表同一份请求；未知结果只核对，不换键重跑原编辑。

## 技术、评审和接受

`verify` 核对交付包并使用已安装的固定二进制在新会话重开，不安装。`judge` 生成绑定候选的请求；评审者读取实际工程和预览，以独立上下文或人工方式产生回执。执行器不能编造评审回执。`review-import`（别名 `import-judge`）只接收回执；`accept` 需要用户明确接受当前评审候选。

`revise` 只把有效问题映射到已授权对象和属性，创建另存任务并消耗累计预算。新任务仍需 `run`、技术核验和新的评审。拒绝无问题改动、基础版本冲突和跨对象编辑。

## 当前范围

未受管账本默认执行资源以当前 `skills.lock.json` 固定快照为准；显式受管账本沿用已核验、保留并绑定摘要的活动组合。开发验证可明确传入 `--skill-root` 指向其他单技能目录，其摘要写入任务；该路径的验证不能冒充固定发行验收。桌面可变工程写入未接通，明确拒绝；真实宿主模型派发、Windows/Linux 原生运行及创作接受未验收。

## 可移动血缘交付

`bundle-export --state-dir "$STATE_DIR" --task "$TASK_ID" --bundle "$NEW_BUNDLE"` 导出技术已核验候选、引用素材和绑定评估记录；原目录不覆盖。保留返回的 bundleSha256 作为外部版本锚点。

`bundle-check --bundle "$MOVED_BUNDLE" --expected-sha256 "$BUNDLE_SHA256"` 只读核对，无需任务账本或旧绝对路径。旧交付可检查文件摘要，但血缘保持 UNKNOWN。完整性不证明评估器身份真实性，也不把 NOT_RUN 创作状态变成通过。

局部调整修订当前仅支持已有 `BrightnessContrast` 调整层的 `brightness`／`contrast`。必须有绑定的失败评估、目标授权、已启用蒙版及蒙版瓦片摘要，并声明保护区域；另存后核验实际像素变化、蒙版保全及非目标像素。其他调整种类仍拒绝，不由此声明完整领域或创作验收。

PSD 导出按固定技能的必要特性门禁执行；受限返工继承 `psdPolicy`，旧源版本的损失接受不得自动授权不同源版本。

平面导出 `flatExport` 的颜色／ICC／透明要求随返工继承；素材来源回执由已核验源包继承，替换素材不沿用旧回执；本地编辑不产生新的云生成计量。

## 检查点恢复

`recover --state-dir "$STATE_DIR" --task "$TASK_ID" --proposal "$PROPOSAL_JSON"` 从已保存且原执行者已确认退出的检查点创建关联子任务，不重放原operations。提案绑定原检查点记录（failure或checkpoint.json）及工程摘要、已有授权、明确对象和新操作；重复同提案返回同一子任务，累计修订预算与截止时间保留。新任务仍需`run`及独立评审。

仅有PID消失、未知记录或旧暂存不能恢复写入权；原任务、工作令牌、原计划、资产或文件不匹配时拒绝。检查点不伪装成成功父artifact；公开固定dev.61在macOS arm64通过当前PC-TX-002全部9个规范场景；恢复支持已有文字和图层名称局部修复，创作／模型及其他V1门禁保持独立。

## 显式运行时组合

仅在用户要求升级、回退或核对运行时组合时使用`runtime-status`／`runtime-upgrade`／`runtime-rollback`，不因普通创作任务自动升级。三个入口使用既有`--state-dir`，切换另外提供`--request`提案。先核对代次、来源摘要、后端与stateSchema；任务和原执行者未排空时不得删除记录或重置epoch规避。完整合同在插件根目录`docs/PhotoCraft-Runtime-Transition.zh_CN.md`。

状态查询不安装、不编辑。切换保留旧版本及状态备份，分别核验实际版本、命令schema和原生工程，再原子更新组合。当前仅支持ledger schema1，不迁移未知状态；bridge选择不能静默派发headless任务，可变GUI编辑仍拒绝。不同二进制版本及完整升级验收保持开放，同二进制来源切换证据不能冒充不同版本通过。

## 连续操作的实例复用

独立连续原生命令任务交给 **`photocraft-cli`** 技能的任务级会话入口，在同一进程句柄逐阶段操作，不为检查、保存、重开和返工重复启动桌面。安装：`npx skills add full-aigc-skills/photocraft-skills --skill photocraft-cli`。已有 Harness 任务仍使用原账本核对、授权和累计预算；不要为了复用实例另开任务或绕过 unknown／取消门禁。
