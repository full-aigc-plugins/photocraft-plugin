---
name: photocraft-harness
description: 当 PhotoCraft 任务需要跨会话状态查询、结果未知后的核对、停止自有执行、提交独立评审回执、导出或检查可移动血缘包，或按问题进行受限另存修订时使用。只查询命令或执行一次领域操作时由对应 PhotoCraft 技能负责。
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

开发版 dev.41 的默认执行资源来自固定 dev.37 快照。开发验证可明确传入 `--skill-root` 指向其他单技能目录，其摘要写入任务；该路径的验证不能冒充固定发行验收。桌面可变工程写入未接通，明确拒绝；真实宿主模型派发、Windows/Linux 原生运行及创作接受未验收。

## 可移动血缘交付

`bundle-export --state-dir "$STATE_DIR" --task "$TASK_ID" --bundle "$NEW_BUNDLE"` 导出技术已核验候选、引用素材和绑定评估记录；原目录不覆盖。保留返回的 bundleSha256 作为外部版本锚点。

`bundle-check --bundle "$MOVED_BUNDLE" --expected-sha256 "$BUNDLE_SHA256"` 只读核对，无需任务账本或旧绝对路径。旧交付可检查文件摘要，但血缘保持 UNKNOWN。完整性不证明评估器身份真实性，也不把 NOT_RUN 创作状态变成通过。

局部调整修订当前仅支持已有 `BrightnessContrast` 调整层的 `brightness`／`contrast`。必须有绑定的失败评估、目标授权、已启用蒙版及蒙版瓦片摘要，并声明保护区域；另存后核验实际像素变化、蒙版保全及非目标像素。其他调整种类仍拒绝，不由此声明完整领域或创作验收。

PSD 导出按固定技能的必要特性门禁执行；受限返工继承 `psdPolicy`，旧源版本的损失接受不得自动授权不同源版本。

平面导出 `flatExport` 的颜色／ICC／透明要求随返工继承；素材来源回执由已核验源包继承，替换素材不沿用旧回执；本地编辑不产生新的云生成计量。
