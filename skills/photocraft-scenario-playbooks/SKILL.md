---
name: photocraft-scenario-playbooks
description: 用 PhotoCraft 执行老照片划痕折痕修复、扫描去尘、自然人像精修、商品清洁抠图、影调恢复和成片交付时使用；按具体问题选择带真实命令参数的场景手册。
license: Apache-2.0
---

# PhotoCraft 场景操作手册

每条流程默认从新打开的栅格原图开始，无选区和活动路径。复用会话时重新选择原像素层，只有存在选区时才取消选区；无选区时 `select.deselect` 会拒绝执行。先查看输入图片、用途和修改边界，在下面选择相关手册。每条流程给出操作顺序、真实 command ID、参数起点、观察结果和不可完成的边界。只读取相关场景，不加载全部目录。

- [restoration：12 条](references/restoration.md)：老照片保守修复全流程、扫描灰尘与细小白点、胶片细划痕局部修补、背景折痕分区修补、照片角部小块缺损修复、银镜反光区域保守校正、扫描印刷网点轻度抑制、旧 JPEG 方块伪影减轻、暗部彩色噪声抑制、小面积霉点取样修复、靠近人物边界的划痕定区修复、平坦背景块状污点修补。
- [tone：7 条](references/tone.md)：褪色黑白照片灰阶恢复、泛黄纸基色偏校正、老彩照偏红衰变校正、旧彩照转黑白并保留层次、编辑插图双色映射、彩色人像黑白通道混合、保留指定物体彩色其余转黑白。
- [geometry：2 条](references/geometry.md)：扫描倾斜与边框整理、扫描件四边污边裁去。
- [delivery：4 条](references/delivery.md)：修复成片的最终锐化、老照片打印分辨率标记、网页展示图缩小、透明四边扩画布交付。
- [portrait：7 条](references/portrait.md)：自然人像局部痘印修饰、人像眼下阴影轻度减淡、人像整体轻微白平衡、逆光人像暗部回调、保留皮肤纹理减弱局部油光、纯色背景杂发整理、牙齿自然去黄。
- [product：8 条](references/product.md)：商品中性白底基础校正、商品表面灰尘清理、白底抠图白边整理、深色旧底抠图黑边整理、商品主体蒙版分离、商品小面积反光点缓和、商品标签定区锐化、商品配色局部试样。
- [layout：2 条](references/layout.md)：社交图片补画布留白、版式镜像副本制作。
- [mask-local：8 条](references/mask-local.md)：室内窗景局部压高光、人物面部局部提亮、保留商品颜色并弱化背景色、主体外背景柔化、服装定向改色并保持肤色、白色包装局部去黄、天空与地面渐变曝光平衡、柔和暗角突出画面中心。

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

## 技能商店场景经验

遇到修复与推测分开交付、保留身份特征的人像修饰、代表样片后再批量调色时，读取[商店工作流适配](references/market-workflows.md)，使用对应的Craft方法和实际结果检查。上游技能不作为运行依赖。

镜像任务使用选中图层的翻转方法，原图保留检查见layout手册；画布翻转会改变所有图层，不能用它实现“仅翻转副本”。

执行取样修补、去尘、油光或杂发修整时，先读[修复检查方法](references/repair-checks.md)，确认供体、工作层与保护区；以保存后的实际局部结果验收，不用测试样例评分替代真实照片判断。

透明边缘与去背景配方中的`$ref:originalLayer`是手册记号：先inspect取得真实原图层ID并替换为整数。工作副本复制后保留但隐藏原图层，验证PNG的实际Alpha；可见原图会重新叠回背景或加重半透明边缘。

逆光恢复使用本技能中已验证的可编辑曲线适配；不能仅根据shadowsHighlights同名方法推断它实现了Photoshop的阴影／高光恢复行为。
