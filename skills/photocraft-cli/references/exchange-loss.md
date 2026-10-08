# 交换损失报告

开发版本 dev.2 交付 `exchange-loss.json`，manifest.lossReport 及 files 表绑定其摘要。报告保留原生工程与重新打开得到的 native.json 摘要，每个导出记录路径、摘要、格式、导出警告和格式损失。

`lost` 表示导出格式不携带对应原生编辑能力；`observed` 仅表示实际文件或重开结构观察；`unknown` 表示跨工具字体、效果、蒙版、图层或视觉保真尚未验证。SVG 元素数量、PSD 图层数量相等都不能证明无损。

导出是用户请求的派生物，nativeSubstitute 固定 false，原生工程始终随包保留。PNG/视频不替代原生工程；不能把未知项改写为已验证或自动提升为创作批准。实际跨编辑器保真需要单独验收。旧版本历史交付没有报告时保持历史事实，不补造保真证据。

## PSD 必要功能门禁 / Required PSD features

新生成 PSD 默认阻止功能矩阵中已观察到的 `lost`／`degraded`。可选计划字段 `psdPolicy.requiredFeatures` 声明必要特性；必要项为 `unknown` 或没有观察数据时也拒绝交付。可用类别为 `structure/text/mask/blend/opacity/smartObject/smartSourceKind/smartTransform/adjustment/shape/effects/tree-size`，精确位置如 `0/0:text`；`*` 要求所有已观察项。位置来自实际 native／PSD 图层树，不凭图层名称猜测。未要求的 unknown 仍如实报告，不升级为保真。

```json
{"psdPolicy":{"requiredFeatures":["structure","text","mask","adjustment"]}}
```

保存并重开原生和 PSD 后生成 `psd-acceptance.json`；它绑定实际工程、导出、检查记录和计划摘要，`exchange-loss.json` 与成功 manifest 绑定该回执。状态为 `PASS`、`FAIL` 或 `ACCEPTED_LOSS`；`completeFidelity` 始终 false。矩阵 retained 仅证明报告属性相符，蒙版 presence、文本基础属性或 PSD 重开不证明全部蒙版像素、完整文本样式或外部编辑器保真。完整性入口会重算矩阵与门禁；`native_verify.py` 在新只读原生会话同时重开原生和 PSD，不能用包内摘要自洽代替真实文件检查。

失败先保留原暂存中的 `.pcraft`、PSD、交换报告及 gate，再返回 `psd_required_features_unaccepted`，不发布成功 manifest、不覆盖源、不重放。读取输出 failure.json 的 stage，并按本技能失败暂存合同先核对摘要、在新会话检查原工程；失败目录不能充作成功源包。

用户已明确接受某项实际损失时，`psdPolicy.acceptedLosses` 按精确位置填写 `{status, observationSha256, reason}`，摘要取自对应 gate 的 features；`acceptedForSourceSha256` 必须等于此次已核验源包的 `expectedProjectSha256`，运行需传 `--source`。接受只适用于同一源版本、同一状态与同一观察；旧摘要、错误源和多余接受拒绝。新建首次发现损失时，应先保留原生成功源版本，再基于该版本制作独立导出修订。不得自动把拒绝回执转换成用户接受，也不重复询问已涵盖同一源和损失范围的已有授权。

For new PSD deliveries, observed losses/degradations block publication. `requiredFeatures` also gates unknown or unobserved required properties. Explicit acceptance is scoped by exact feature selector, observed status/hash, reason and the verified source-project digest; it requires a source revision. Acceptance never changes the observed loss into retained fidelity. The gate binds actual project/PSD/inspection/plan digests. Failure retains the native stage without success or replay; the read-only verifier reopens both native and PSD. Historical packages without this policy/gate keep their original read-only compatibility and gain no new acceptance.
