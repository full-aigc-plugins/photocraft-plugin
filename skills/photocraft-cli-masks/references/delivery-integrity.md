# 交付包完整性检查 / Delivery integrity

每个独立技能自带只读校验入口，不安装运行时，不编辑工程：

```bash
python3 -I -B "$SKILL_DIR/scripts/delivery.py" /absolute/delivery
python3 -I -B "$SKILL_DIR/scripts/delivery.py" /absolute/moved-delivery --expected-manifest-sha256 RECORDED_SHA256
```

校验清单内每个文件、登记素材、原生与检查记录、导出及交换报告的身份。必须保留project.pcraft、native.json、plan.json、operations.json、exchange-loss.json；相对路径禁止逃逸和符号链接。清单重复键、同名文件替换、缺失依赖和报告身份不一致均非零退出，不能继续称原验收有效。PASS仅指完整性，不代替实际重开、PSD保真和创作接受。

源工程返工自动在安装运行时之前检查完整源包，并在发布新包前重查源包与新包。可选expectedManifestSha256将源清单绑定此前回执；默认仍保留expectedProjectSha256版本保护，并在同次调用中固定源清单摘要。移动包只要相对引用与文件未改变仍可检查及返工。先前不完整或被改动的包必须恢复原文件或经重新交付获取新清单，不能直接改写摘要绕过。

Read-only verification checks every listed file, registered asset and native/inspection/export/loss-report identity without installing a runtime. Source revisions verify the complete source before installation and both packages before publication. Optional expectedManifestSha256 binds a previously recorded manifest; the existing native-project revision remains required. Paths stay relative so intact packages remain movable. Hashes do not authenticate authorship: an attacker replacing the files and manifest together requires an independently recorded manifest digest to detect. PASS is integrity evidence, not native reopening or creative acceptance.
