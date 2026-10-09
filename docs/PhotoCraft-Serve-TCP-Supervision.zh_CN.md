# serve TCP共享会话回复监督

PC-TX-005／9.6增量：源dev.52／插件dev.67，固定原生craft.5。stdio与TCP接入同一serve请求及回复合同；固定发行／安装证据与候选分别记录，完整9.6继续开放。

TCP前端只绑定127.0.0.1，保留原生64位十六进制令牌、16连接、1 MiB请求行和30秒网络IO超时。显式令牌及令牌文件优先于各自环境变量；两种来源冲突拒绝。缺失令牌文件以O_EXCL和0600创建，已有文件读取并复用，不覆盖。默认新令牌和就绪地址沿用原生stderr格式，认证消息不进入编辑回执或errorData。

启动配置静态拒绝先于安装和目录创建。认证失败、超长请求和认证后的无效首请求均不安装运行时。首条合法请求才安装摘要核验后的固定CLI并启动一个共享原生stdio会话；所有连接共享文档，完整调用、回复核验及交付保持在同一互斥边界。保留合法无id／复合id、原生JSON-lines成功输出、文档及PNG图像输出；端口允许原生+号及任意前导零。

回复畸形、错配身份、内层语义错误、额外帧或交付丢失，保留原请求和已验证回执，返回稳定code／phase／outcome／retryable／recoveryAction及禁止重放标记。自有原生进程关闭，共享会话进入隔离状态；其他连接返回serve_session_quarantined及not_executed，不隐式重启或继续编辑。已保存工程和源文件保全，不声称回滚。交付丢失发生在原生成功验证后，记录reply_validated／unknown；不能把该请求改写为未执行。

```bash
python3 -I -B "$SKILL_DIR/scripts/cli.py" -- serve --port 0 --control-token-file "$TOKEN_FILE" --automation-read-root "$READ_ROOT" --automation-write-root "$WRITE_ROOT"
```

健康双连接操作、七类实际原生保存后故障、交付丢失跨连接竞态和自有进程退出分别测试；认证／令牌文件／连接上限／请求大小／真实空闲超时单独检查。批量内部逐步确认、完整启动参数／MCP输入矩阵及完整V1仍需各自证据。当前batch只有静态步骤预检和外层回复校验，不能据此证明聚合内部停止。
