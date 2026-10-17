---
name: photocraft-editor
description: 当需要在支持 MCP Apps 或内置浏览器的宿主内打开 photocraft 的真实编辑界面，连接当前工作区，或让 Agent 的操作显示在同一页面时使用。
license: Apache-2.0
---

# photocraft 内嵌编辑器

1. 从当前已加载插件的工具列表找到 `photocraft-editor` 服务。使用本任务工作区绝对路径调用 `open_editor`，首次调用传入 `workspace`；相对文件路径可在编辑器就绪后交给具体打开工具。
2. 宿主支持原生 MCP Apps 时呈现 `ui://photocraft/panel.html`。只有工具文字结果不代表界面已打开。
3. Codex 未自动呈现面板时调用 `open_browser_editor`，把返回的 `editorUrl` 交给宿主的内置浏览器打开能力。Codex Desktop 可调用 `open_in_codex`，target 为 browser，url 为实际返回值。不要把本地页面路径猜成固定端口。
4. 同一实例只打开一个编辑页。调用 `editor_status`，待 `attached` 或 `ready` 为 true 再执行；加载失败先处理页面错误。
5. 本轮所有编辑使用同一服务。原生 CLI 与 Web 编辑器不是同一个内存文档，切换前必须先保存并显式重开。

用 doc_open/doc_new 打开或新建，doc_inspect 查看图层；command_list 查询实际命令，command_run 执行；doc_save 保存 .pcraft，doc_export 导出。

如果宿主仅支持 MCP，工具调用能力与内嵌 UI 是两件事。可在外部浏览器使用同一个 editorUrl，但必须明确告知这不是宿主内嵌验收。

开发候选缺少 `ui/dist/adapter.mjs` 时需要先按插件 `ui/README.md` 构建。不要从任意缓存猜测路径，不要绕过校验。该技能独立安装不附带编辑器服务；需要安装配套插件或配置它的 MCP 后端。

工具未注册时，可在得到插件实际目录后用项目终端运行 `node ui/dist/adapter.mjs --serve`，通过环境变量 `CRAFT_WORKSPACE_ROOT` 指定本任务工作区。保持该进程存活；此模式可展示 UI，自动化仍须连接对应 MCP 实例，不能另开一个后端声称共享会话。

完成后保存工程并重开检查；读取实际导出文件。浏览器存储、预览截图和已提交渲染任务不等于工作区交付。
