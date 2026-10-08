# 平面导出与素材来源 / Flat export and provenance

请求 PNG、JPEG、TIFF、WebP 时可增加 `flatExport`，其 `colorSpace` 是实际重开后的 `Rgb/Grayscale/Cmyk/Lab`，不是 ICC 配置名称；`iccSha256` 是导出后实际嵌入 ICC 的字节摘要；`transparency` 为 `preserve/opaque/any`。RGB8 源的整幅归一化 RGBA8/alpha 与当前颜色配置用于核验，不是外部消费者、印刷或完整颜色感知验收。其他原生模式/位深使用此可选合同会在安装前明确拒绝；旧导出入口不增加此限制。

```json
{"flatExport":{"colorSpace":"Rgb","transparency":"preserve"}}
```

`flat-export.json` 绑定当前原生与源版本、导出和实际重开观察。`preserve` 要求整幅 alpha 摘要相同；有透明源导出 JPEG 会拒绝。用户明确要求 `opaque` 才接受不透明输出，不自动改写要求。ICC 预期不匹配、实际颜色模式/尺寸不符、观察文件丢失或输出被同名替换均拒绝。失败保留原生工程及观察暂存，不发布成功清单；新只读会话再次实际重开导出验证，不仅比较历史报告。仅以输出像素能重开不能宣称 ICC 正确。

`assetProvenance` 按已登记素材别名记录来源。普通提供的素材为 `{kind:"provided"}`；已有生成素材使用下列结构，替换摘要和路径为实际值。回执是已取得的原始供应方 JSON，不含凭据；本技能不发起生成请求或支付。回执最大1MiB，重复键与非有限数值拒绝。

```json
{"assetProvenance":{"product":{"kind":"generated","provider":"provider-name","model":"model-id","requestId":"existing-request-id","assetSha256":"ACTUAL_ASSET_SHA256","receipt":{"path":"/absolute/existing/provider-receipt.json","sha256":"ACTUAL_RECEIPT_SHA256"},"usage":{"quantity":1,"unit":"images"}}}}
```

单位允许 `images/credits/tokens/seconds`，不同单位不合并求和。声明必须绑定登记素材摘要；原回执字节按摘要复制为包内 `generation-<asset>.json` 并由清单登记。未替换素材在另存修订时继承原回执；替换素材不能继承旧来源。`asset-provenance.json` 的上游声明用量与本地 `executedPlanOperations`、`cloudGenerationCalls:0` 分开记录，修订不会把旧素材用量当作新生成收费。摘要完整性不证明供应方身份或真实账单，`sourceAuthenticity` 保持 `NOT_PROVEN`。

Plan `flatExport` checks actual reopened color mode, embedded ICC digest and full normalized alpha against the saved native version. Transparent JPEG fails `preserve`; opaque output must be requested explicitly. RGB8 normalization does not prove external print/color fidelity. Optional `assetProvenance` copies an existing provider receipt with asset/request/usage identity, preserves it only for unchanged assets, and separates recorded generation usage from local plan operations. No cloud generation or payment occurs, and receipt authenticity/billing remains unproven. Legacy deliveries without the new contracts retain their prior readonly compatibility.
