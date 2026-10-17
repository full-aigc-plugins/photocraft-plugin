# main候选：复用JPEG交付参数

适用于需要反复交付同尺寸、质量和元数据策略的网页JPEG。仅用于main `5f65579ecb44047c2a619036c18ff273202e1389`或实际暴露这些方法的更新候选；稳定版0.9.0的版本字符串不足以证明存在。四个新预设方法已通过真实Codex宿主调用，并在其内置浏览器同一编辑器中执行；原生工程保存重开与320×240 JPEG交付实际核对。具体观察见[方法证据](main-export-presets.json)。跨重启持久化还需单独检查。

## 从母版到固定交付尺寸

1. `editor_status`确认当前会话已连接；`doc_inspect`读取母版尺寸和当前图层。本例母版640×480；真实照片需按比例和用途决定尺寸，不能强行改成4:3。先用`doc_save {"path":"output/master.pcraft"}`保存分层母版。
2. `command_list {"filter":"file.export.presets"}`确认新方法存在。用`command_run {"id":"file.export.presets.list","params":{}}`检查同名预设；保存同名会替换，使用本任务的新名字或明确按用户要求更新。
3. 保存参数模板：

```json
{"id":"file.export.presets.save","params":{"name":"Web JPEG 320","settings":{"format":"jpg","quality":80,"sizing":"pixels","width":320,"height":240,"lockAspect":true,"metadata":"none","profile":"srgb","embedProfile":false}}}
```

这是`command_run`的参数对象。可省略的其余字段由引擎补默认值；`scale`单位是百分比，不是0–1倍率。尺寸应与母版比例一致，非等比例交付先明确裁切/留白策略。

4. `command_run {"id":"file.export.presets.get","params":{"name":"Web JPEG 320"}}`读取实际返回的`preset.settings`，确认尺寸、quality、metadata、profile。**get只返回参数，不会导出或改图。**
5. 将这个JPEG子集明确映射到已有的实际导出方法：

```json
{"id":"file.export.saveForWebLegacy","params":{"format":"jpeg","quality":80,"width":320,"height":240,"metadata":"none","convertToSrgb":true,"embedIcc":false,"path":"output/web-320.jpg"}}
```

先用`command_list`核对该方法在当前会话可用；上述值来自第4步返回值。本方法的格式拼法为`jpeg`，预设里是`jpg`；不能直接把整个settings对象原样传过去。这个映射只覆盖上述JPEG设置，不宣称所有预设格式自动适配。

6. 核对宿主确实写出了文件，读取实际JPEG像素尺寸，并查看压缩与边缘；再`doc_inspect`确认母版仍为640×480，重开`.pcraft`检查图层。PNG/JPEG均会扁平化，保留格式损失警告，不替代可编辑母版。

## 接口边界

- 本候选的`doc_export`只接受当前schema声明的格式/质量等字段，没有width/height/metadata/profile；不要给它塞不支持的参数，也不要假设存在未发现的`file.exportAs`命令。
- JPEG无透明通道。输入有透明边缘时先确认背景策略，不能将预设的transparency开关当JPEG透明能力。颜色转换需另外用真实色彩样本检查，本例不代表印刷色彩认证。
- `file.export.presets.delete {name}`删除命名模板；只删除本任务创建且确定不再需要的测试项，不自动清空用户品牌预设。
- 预设可以独立列出和保存，但当前浏览器资源缺失或版本过旧时先恢复运行时；不能用另一个CLI进程创建预设就声称界面已同步。跨重启恢复与本会话CRUD是两个验证层。
- 此流程是新增能力指导，不把原有50条场景映射虚增为51条；中文标题字体问题单独修复和验收。
