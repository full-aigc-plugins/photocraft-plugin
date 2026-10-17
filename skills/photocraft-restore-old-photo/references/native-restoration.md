# 老照片修复：具体CLI与MCP操作

## 先确认输入和能力

原图只读保留，确认是否保持黑白、输出尺寸及修复范围。先看原分辨率的损伤；脸、手、文字、纹理边界单独保护。损伤穿越轮廓应分两侧短笔触，不能用大刷跨过五官。大面积缺失没有可靠参照时保留，不以生成结果冒充历史还原。

[独立操作计划](restoration-plan.json)完整内含两个阶段，复用既有old-photo-conservative流程，不增加场景计数，也不依赖其他技能文件。参数表是256×192合成输入的例子，所有点坐标、取样点、笔刷直径都必须针对真实输入重新确认。不能把示例缩放到脸上自动涂抹。

| 顺序与目的 | 命令 | 参数例子 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name": "Restoration working copy"}` |
| 2. 只点选已确认的灰尘，不覆盖眼睛、文字和胶片颗粒 | `paint.spotHealing` | `{"points": [[40, 30, 1], [44, 32, 1]], "size": 5, "type": "proximityMatch"}` |
| 3. 从同材质邻近完好位置采样，沿损伤做短笔触 | `paint.healingBrush` | `{"points": [[80, 40, 1], [84, 42, 1]], "source": [60, 40], "size": 6, "hardness": 40, "sampleLayer": "current", "opacity": 70}` |
| 4. 轻度降噪，保留可识别纹理和胶片颗粒 | `filter.noise.reduceNoise` | `{"strength": 2, "preserveDetails": 85, "reduceColorNoise": 20, "sharpenDetails": 0}` |
| 5. 观察直方图后恢复中间调，黑白场不硬截断 | `layer.newAdjustmentLayer.levels` | `{"inBlack": 5, "gamma": 1.05, "inWhite": 248}` |

## 分阶段操作

第一阶段只执行前三步：复制原层、局部点修、从邻近同材质采样的短笔触修复。复制后通过doc_inspect或CLI info确认当前工作层，不在原层执行画笔。MCP可按真实返回ID给两种画笔补充layer字段。保护区内不应改变像素；跨轮廓、文字或五官时停下改用更小范围，不以模糊掩盖损伤。

另存local-repair.pcraft并导出local-repair.png，与原图同尺寸比较，检查局部糊斑、重复纹理、硬边及越界。无真实无损参考时不能计算“还原率”；只记录观察到的变化和待确认区域。第一阶段未通过时不要用后续全局调色掩盖问题。

第二阶段在第一阶段工程继续操作：可选轻度降噪，再建立可编辑色阶。strength=2、preserveDetails=85、reduceColorNoise=20和gamma=1.05只是技术样例；真实胶片颗粒已细时跳过降噪，黑白场已贴边时保持0/255，不照抄5/248。原生0.9.0命令目录没有histogram命令，不虚构API：用实际编辑器直方图或对导出图作只读像素统计，再决定黑白点。高光已经缺失时不能宣称恢复细节。

第二阶段会改变全图影调，不能再要求“最终图未修区域逐像素不变”。改为检查原层仍完整保留、色阶可编辑、尺寸/构图未变及人脸字形未被改造，比较前后是否自然。

## 原生CLI路径

下面只负责按计划传递原生命令。先把plan中的input、project、preview和坐标改成本次任务值；使用新输出文件名，不覆盖输入。每阶段在同一个run进程内顺序执行全部步骤；第二阶段显式打开第一阶段已保存工程：

```python
import json, subprocess
from pathlib import Path
plan = json.loads(Path("<本技能目录>/references/restoration-plan.json").read_text(encoding="utf-8"))
cli = "<已验证photocraft-cli的实际路径>"
phase = plan["phases"][0]  # 先做local-repair；检查通过后再显式选择第二阶段
argv = [cli, "run", phase["input"]]
for item in phase["steps"]:
    argv += ["--cmd", item["command"], "--params", json.dumps(item["params"], ensure_ascii=False)]
subprocess.run(argv + ["--out", phase["project"]], check=True)
subprocess.run([cli, "convert", phase["project"], phase["preview"]], check=True)
```

Agent分开调用两个阶段，自行查看结果后决定继续，无需机械要求用户重复确认。`photocraft-cli info restored.pcraft`检查层树；原图、工作层和Adjustment应存在。不要通过恢复默认demo或新建空文档来“重开”。

## 同一编辑器MCP路径

1. 先调用open_browser_editor或open_editor并传任务workspace，用宿主浏览器呈现返回URL，等待editor_status报告attached/ready。仅返回URL或queued都不算就绪。不要先调用编辑命令再切工作区；已有实例拒绝切换时保留它，使用独立任务实例，不强停用户实例。
2. `doc_open {"path":"input.png"}`；若未返回index，调用`session_list {}`并读取active/documents中的实际index；工具结果可能在content文本内，需要先解析JSON，再用`doc_inspect {"index":实际index}`确认文档和当前层，读取command_list当前参数。
3. 逐条`command_run {"id":"layer.duplicate","params":{"name":"Restoration working copy"}}`，然后两种修复画笔分别使用表中参数，按实际工作层ID补layer。每条检查结果；禁用、未就绪或超时先核对状态，不盲重放。
4. `doc_save {"path":"local-repair.pcraft","index":实际index}`和`doc_export {"path":"local-repair.png","format":"png","index":实际index}`；检查图像后在同一文档继续后两条command_run。若使用另一个进程，须先显式保存并重开该检查点。
5. 另存restored.pcraft、导出restored.png，检查保存警告；重开新工程检查层与最终图像。CLI独立进程不会自动更改这个Web文档。

工具字段来自[实际观察](native-command-evidence.json)，业务效果、界面附着与画面同步分别验收；Web与CLI版本不同，缺少命令时明确报告，不能只凭相近标签调用。

## 保存和源层检查

交付分层工程、同尺寸前后图、阶段PNG和简短修改记录。可在另一个仅用于核验的副本中，按info/doc_inspect真实返回ID删除工作层与色阶，导出只剩原层的PNG，与输入解码像素比较；只处理核验副本，不删最终交付工程的层。只有经过实际比较才能声称原层未变。真实人像需100%看五官、文字及损伤边界，不能用合成点状污点的误差数值代替。

取样与色阶流程的[固定GitHub来源](workflow-sources.json)记录阅读路径和许可；未复制手册正文或代码。

## 本次真实宿主观察

Codex内置浏览器加载后，同一原生MCP实例完成五条业务命令，画布白点与层列表同步变化，保存并重开有三层的工程。这里只验证256×192合成夹具。局部修补导出与原生CLI解码像素相同；整体调色导出并非逐像素相同：该夹具最大通道差1/255，平均约0.051/255，两个范围均69–162。保留这个差异，不把Web与CLI视为位级相同，不据此推断全部真实照片表现。
