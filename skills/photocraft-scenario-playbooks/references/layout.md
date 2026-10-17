# PhotoCraft layout 场景

每条流程从新打开的栅格原图开始（无选区、无活动路径）。复用会话时先选择原像素层；仅在确有活动选区时取消选区，`select.deselect` 在无选区时会被拒绝。坐标以256×192为例，必须按当前输入重算。

## social-canvas-padding：社交图片补画布留白

输入：已经确认目标比例，主体像素不能拉伸。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 以透明或统一背景扩画布，保持居中 | `image.canvasSize` | `{"width":320,"height":240,"anchor":"center","extensionColor":"white"}` |

检查：主体比例未改变；新边界留白一致。

边界：输入大于目标时会裁内容，先读尺寸；需要完整保留时目标不得小于输入。

## photo-mirror-layout：版式镜像副本制作

输入：用户明确需要镜像图用于构图，文字和标识需核对。

| 顺序与目的 | Craft 命令 | 参数示例 |
| --- | --- | --- |
| 1. 保留原图层，复制到修复工作层 | `layer.duplicate` | `{"name":"Restoration working copy"}` |
| 2. 只镜像副本，保存原始方向 | `edit.transform.flipHorizontal` | `{"target":"pixels"}` |

检查：人物或物体方向符合用途；文字、品牌标识没有反写进入交付。

边界：含文字图像镜像可能不可用，不能把反写标识交付为真实照片。


镜像副本应使用选中图层的edit.transform.flipHorizontal；flipCanvasHorizontal会改变所有图层。保存后隐藏工作副本导出，核对底层原图方向，不能只看最终合成图。
