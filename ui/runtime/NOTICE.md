基于 zcode-plugins craft-runtime，Apache-2.0。保留原项目许可。
本地改动：使用独立 fork 源码构建、适配新版本 API；不把增强 WASM 声称为上游原版发行物。

patches/ 保留来源参考；只应用 source.lock.json 明确列出的补丁，避免旧版本上下文或品牌修改自动进入新版。命令与文件桥接由 prepare-automation.py 按锁定版本应用。
