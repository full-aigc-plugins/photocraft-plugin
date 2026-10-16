---
name: photocraft-scenario-playbooks
description: 用 PhotoCraft 执行老照片划痕折痕修复、扫描去尘、自然人像精修、商品清洁抠图、影调恢复和成片交付时使用；按具体问题选择带真实命令参数的场景手册。
license: Apache-2.0
---

# PhotoCraft 场景操作手册

先查看输入图片、用途和修改边界，在下面选择相关手册。每条流程给出操作顺序、真实 command ID、参数起点、观察结果和不可完成的边界。只读取相关场景，不加载全部目录。

- [restoration：10 条](references/restoration.md)：老照片保守修复全流程、扫描灰尘与细小白点、胶片细划痕局部修补、背景折痕分区修补、照片角部小块缺损修复、银镜反光区域保守校正、扫描印刷网点轻度抑制、旧 JPEG 方块伪影减轻、暗部彩色噪声抑制、小面积霉点取样修复。
- [tone：5 条](references/tone.md)：褪色黑白照片灰阶恢复、泛黄纸基色偏校正、老彩照偏红衰变校正、旧彩照转黑白并保留层次、编辑插图双色映射。
- [geometry：1 条](references/geometry.md)：扫描倾斜与边框整理。
- [delivery：3 条](references/delivery.md)：修复成片的最终锐化、老照片打印分辨率标记、网页展示图缩小。
- [portrait：4 条](references/portrait.md)：自然人像局部痘印修饰、人像眼下阴影轻度减淡、人像整体轻微白平衡、逆光人像暗部回调。
- [product：5 条](references/product.md)：商品中性白底基础校正、商品表面灰尘清理、白底抠图白边整理、深色旧底抠图黑边整理、商品主体蒙版分离。
- [layout：2 条](references/layout.md)：社交图片补画布留白、版式镜像副本制作。

## 同会话 MCP 路径

1. 读取宿主实际工具 schema。已打开内嵌编辑器时使用这一会话，`editor_status` 确认可编辑后再执行；不要另启 headless CLI 改另一个工程并声称画面同步。
2. `doc_open {"path":"input/scan.png"}` 后 `doc_inspect {}` 取得尺寸、当前文档和图层。路径相对本次 workspace；使用返回的图层 ID。
3. 对本场景命令先用 `command_list {"filter":"paint.healingBrush"}` 等确认参数与可用性；再调用 `command_run {"id":"paint.healingBrush","params":{"points":[[80,40,1],[84,42,1]],"source":[60,40],"size":6,"opacity":70,"sampleLayer":"current"},"wait":true}`。此坐标只是示例，必须根据输入定位与取样。
4. 每个局部操作后看实际画面与结果。长任务如返回 job，等待 jobs 状态完成再继续；核对实际工具是否支持 wait 参数。
5. `doc_save {"path":"output/restored.pcraft"}` 保存分层工程；`doc_export {"path":"output/restored.png"}` 另存成片。重新打开工程，检查层与修改仍存在。Save As 后文档名可变为目标文件名。

## 独立 CLI 路径

执行前查询 `photocraft-cli --version` 和 `photocraft-cli commands --json --filter paint.healingBrush`；下面使用官方0.9.0语法。旧技能安装器锁的维护版与此版本不同，不能把目录存在当运行时已安装。

通过 argv 调用，不手拼跨平台 shell 引号。一个编辑批次保持单进程；示例：

```text
["photocraft-cli","run","input/scan.png",
 "--cmd","layer.duplicate","--params","{\"name\":\"Restoration working copy\"}",
 "--cmd","paint.healingBrush","--params","{\"points\":[[80,40,1]],\"source\":[60,40],\"size\":6,\"opacity\":70}",
 "--out","output/restored.pcraft"]
```

再由新进程 `photocraft-cli info output/restored.pcraft` 核对图层；`photocraft-cli convert output/restored.pcraft output/restored.png` 导出并查看成片。调整层创建后不能直接把像素笔画画在调整层上：手册把局部修复安排在影调调整之前；局部返工时重新选择工作像素层。

## 参数与来源

- 参数的固定版本观察见 [命令证据](references/command-evidence.json)，结构化步骤见 [recipes.json](references/recipes.json)。证据说明方法确实存在，不证明任意照片已经修复成功。
- 创作流程参考和许可记录见 [sources.json](references/sources.json)。场景正文与例子为原创适配，没有复制外部脚本。输入素材须有本任务使用权。
- 例子是低强度起点，采样点、损伤轮廓、裁切和尺寸必须由图像决定。输出新工程、成片和同尺寸前后对比；无法恢复的细节与推测区域明确列出。
