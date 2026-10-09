# serve stdio回复监督候选

本增量实施PC-TX-005／任务9.6的serve stdio部分，基于公开源dev.51及固定craft.5；尚未发布或验证新的固定插件安装。完整9.6继续开放。

公开cli.py serve在首条合法JSON-lines请求之后才安装并启动自有原生进程。严格JSON、方法、参数容器、已捕获命令参数和批量步骤静态预检；doc.open／save／render路径按原生workspace语法拒绝绝对路径、穿越、Windows前缀、空组件及保留设备名。原生目录能力仍决定实际授权，不扩展权限。

成功原样保留id／ok／result：无id与复合JSON id、session.list对象、doc.new完整file.new参数、PNG base64和渲染文件回执。回复身份、结构、内层错误及路径通过后才转发成功并读取下一请求。异常时errorData提供code／phase／outcome／retryable／recoveryAction、原请求、已验证回执及replayAllowed:false；合法原生错误字符串保留。不自动重放、不声称回滚，已有保存原样保留。

真实craft.5测试通过保存后重复键、非有限值、语义错误、错配ID、额外帧、损坏error及缺失ok七类注入，后续编辑未发送，源摘要不变、保存工程可重开。健康路径验证渲染图像与文件、复合id、无id、可空params及额外file.new参数。

```bash
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- serve --automation-read-root "$READ_ROOT" --automation-write-root "$WRITE_ROOT"
```

TCP／port、批量内部逐步监督及完整argv／动态权限输入矩阵仍需实施和固定安装验收。当前批量只预检全部步骤及核验外层回复，不能证明内部异常后停止。不得以本候选关闭9.6或完整V1。
