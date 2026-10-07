# 固定公共协议来源

四个领域插件消费由 ArtCraft 持有的 craft-task/v1 与 craft-artifact/v1。`contracts-reference.json` 固定发行 v0.1.0-dev.107、提交，以及两份规范和两份 schema 的 SHA-256。ArtCraft 保持唯一事实源；领域插件不维护 schema 副本。

文档门禁拒绝浮动身份、未知版本、缺失文件和不一致 URL。离线结构校验不能认证来源字节；维护者需另行对含固定标签的 ArtCraft 检出执行：

```bash
python3 -I -B scripts/contract_reference.py --authority /path/to/artcraft-plugin
```

该检查核对标签提交及四个 Git 对象摘要，不读取可变工作树文件。协议升级须显式选择已验证的新发行并重新生成引用。这份引用不锁定可执行运行时，也不代表完整任务协议、宿主或首次使用验收。既有不可变插件发行仍保留旧引用，须在新发行发布后才更新安装产物。

CI 同时检出固定所有者提交，核对标签身份及内容摘要，不跟随所有者 main 分支。
