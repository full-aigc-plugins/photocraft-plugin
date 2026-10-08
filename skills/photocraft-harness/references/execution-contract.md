# 本地任务合同

请求包含 `idempotencyKey`、`brief`、`plan`、`output`、`authorization`、`budget`。`authorization` 提供已有授权的 `ref` 和已存在的 `writeRoot`，可选限制对象 ID；不新增云账户或积分审批。`budget` 包含毫秒时间戳 `deadline`、`maxRevisions` 和磁盘 `reserveBytes`。计划使用独立技能的工作流合同；预览评审必须导出 PNG。

`create` 只登记本地意图；`run` 执行独立副本。SQLite 用事务登记任务、资源租约、epoch 和事件，结果未知时租约保留。状态图见插件架构。`status` 只读，`reconcile` 可更新本地核对状态；两者不启动编辑或安装。缺少可靠结果时持续 `reconciling`。

停止只影响当前执行器实际持有的子进程，不按旧 PID 杀进程。停止请求与确认停止是不同状态，迟到产物保留用于核对。损坏或不支持版本的账本拒绝读取，不自动重建。

评审回执包含请求 ID、工程／预览／需求摘要、量表版本、评估器身份、版本 `evaluator.version` 及上下文隔离方式、PASS／FAIL 和问题列表。问题明确对象 `layer` 与属性 `property`。当前支持文字内容、白名单文字样式、图层命名，以及已有启用蒙版 BrightnessContrast 层的 brightness／contrast 另存修订。局部调整必须声明保护区域，并核验实际目标像素变化、蒙版瓦片及非目标像素保全。不得把通过技术核验或导入测试回执写成真实独立创作通过。

## PSD 必要特性

计划可携带 `psdPolicy.requiredFeatures`；实际丢失／降级以及必要未知项须按固定技能门禁拒绝或提供精确接受。返工继承必要特性，只保留与本次基础工程摘要完全相同的 `acceptedForSourceSha256` 接受记录；不同源版本必须重新评估。技术通过不表示独立创作通过。
