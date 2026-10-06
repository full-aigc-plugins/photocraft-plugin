# 完整命令网关（源候选） / Complete native gateway (source candidate)

固定发行版尚未包含此候选扩展。安装后的能力以版本及文件摘要为准；旧固定标签不会随main变化。

受核验的workflow.py计划新增显式native.command操作；params恰好包含command（完整固定目录ID）和params（原生参数对象）。外层as可绑定真实返回值；内层$ref使用此前真实对象／已登记素材。目录覆盖不等于当前工程上下文可执行，更不等于2639条全部通过验收。

```json
{"command":"native.command","params":{"command":"ACTUAL_NATIVE_ID","params":{}},"as":"actualResult"}
```

上面是结构示意。实际可执行创建样例见examples/native-workflow.json；Film样例必须以--asset still=/absolute/input.png登记32×32图片。通过当前技能的公开workflow.py执行样例，输出目录必须不存在。创建计划会调用正常的原生保存、素材收集、重开、导出和交换损失流程；不能把success.json当作DAG交付manifest。

进入网关前检查固定目录的原生程序摘要与runtime.lock；同会话实时查询完整原生目录和enabled状态。工程重开后选择状态可能消失：Film返工需timeline.select，Effect需layer.select。仅提供目标ID不代表native enabled为true。禁用时报告原因并停止；不自动选择、改参数或改用另一个会话。

回复采用完整命令入口的严格JSON解析，拒绝重复键、非有限值、错误结果和未知回复。网关记录真实nativeCommand、参数与回执；原有preserved_stage保留未知执行的原暂存工程并拒绝原目录重放。保存、依赖、交换报告或导出核验失败时不生成就绪交付。

Art调用时必须锁定native_workflow.py、commands.py和command-coverage.json；安装器生成文件摘要，调度前后沿用launcherIdentity核验。不得从模型计划选择执行器或脚本。当前网关使用既有工作流的headless模式，GUI命令使用commands.py的明确bridge流程单独验收。

Native gateway operations retain the existing workflow delivery contract: collected dependencies, native save/reopen, actual export and exchange-loss report. The gateway validates pinned membership and live enabled state, records actual results, preserves unknown attempts and never replays edits. Art locks the helper, parser and catalog. Candidate cold native samples are distinct from fixed installed-release, full DAG and exhaustive command acceptance.
