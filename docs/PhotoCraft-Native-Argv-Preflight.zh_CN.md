# 原生 argv 预检与 Harness 候选补充

现有 PC-TX-005 与任务9.6继续作为事实源。本次未发布候选建立在技能源dev.39、插件dev.44之后，不改变既有不可变标签或插件管理快照。

原生 `run`、`batch`、`droplet`、`convert` 在安装前校验公开参数、严格JSON及登记命令参数。错误保持 `code`、`phase`、`outcome`、`retryable`、`recoveryAction`、`category` 和 `fieldPath`。13类错误预检零安装／零会话／零输出，13个独立技能的重复键拒绝均通过。批处理动作格式以固定维护版0.2.0-craft.1为准：对象数组或actions包装；droplet另支持元组和裸ID。较新research工作树的批处理扩展不冒充当前运行时支持。真实原生创建、另存修订、批处理、droplet及转换通过，原来的JSON行、文字和空stdout格式保留。

```mermaid
flowchart LR
    Args[原生 argv] --> Validate[离线严格解析与参数预检]
    Validate -->|拒绝| Error[结构化错误：零安装／零会话]
    Validate -->|通过| Native[原锁定CLI执行并保留stdout格式]
    Task[Harness planned任务] --> Temp[本次私有临时预检文件]
    Temp -->|拒绝| Keep[任务／事件／持久计划不变]
    Temp -->|通过| Intent[持久计划与执行意图]
```

Harness运行预检不再提前写入账本目录的计划或记录失败事件，私有临时预检文件在成功及异常路径均清理。真实CLI审计仍确认：create接收语义无效计划后先建立账本；run外层尚未传播完整结构化预检字段。修订预算预占、子进程回复、流式MCP／serve及原生多步骤回复停止仍需补齐，不能把本轮静态拒绝和健康原生场景升级成9.6完成。

候选证据、已发布固定证据与完整逐命令验收保持独立。完整候选回归13项检查通过：技能库234项、插件TypeScript29项及Python48项，零跳过，源码指纹保持一致；固定发行安装尚未执行。任务9.6未勾选，计划仍有28项开放。
