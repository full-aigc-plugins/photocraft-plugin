# 源工程局部修改的保护区域

当用户要求只修改指定内容时，在源工程修订计划中填写非目标区域：

```json
{
  "expectedProjectSha256": "<源 project.pcraft 的 SHA256>",
  "operations": [],
  "exports": [{"format": "png"}],
  "protectedRegions": [
    {"id": "product-and-background", "rect": [0, 100, 320, 300]}
  ]
}
```

rect 为 `[x,y,width,height]`，以源工程画布左上角为原点，单位为像素整数；必须在画布范围内。保护区域须来自用户修改边界，不用避开错误的位置来让测试通过。没有声明保护区域时，工作流不会推断或声称区域已被保护。

使用本技能自带 workflow.py 和 --source。必须先有真实源工程。公开工作流从实际打开的源工程导出 protection-before.png，修改、保存并重开新原生工程后导出 protection-after.png。对照相同画幅、颜色配置块和保护区域 RGBA 样本；任何区域样本改变均拒绝新交付，源文件不变。

通过时 pixel-protection.json、两张对照 PNG 和各自摘要保存在交付清单中。失败时临时工程清理，不发布目标目录。未声明区域仍需单独审阅；本检查不等同于原生图层或创作接受。

当前解码只支持 8-bit 非交错 RGB/RGBA PNG，最大 64 MiB 文件和 RGBA 样本；最多 128 个矩形。其他编码、动画 PNG、无效 CRC、越界区域、颜色配置变化或画幅变化均拒绝核验。实现只使用 Python 标准库，不要求 Pillow、全局 Python 包或额外 CLI 安装。

能力状态以源包固定标签、插件锁和实际验收记录为准；原生 CLI 版本与技能发布版本分别登记。
