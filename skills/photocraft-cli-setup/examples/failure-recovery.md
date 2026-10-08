# 保存回复未知后的处理

原生保存发出后发生断线或内层 JSON 歧义时，保留 failure.json、原暂存路径、原生工程、依赖和 recovery-operations.json。不要删除 `.photocraft-execution-*.json`，不要换目录再执行原计划。先核对原进程和文件摘要，再使用新会话检查已保存工程；进程退出不能证明编辑未执行。证据不足保持待核对，检查点与执行状态收敛后才能按授权发起关联的新修订。

```bash
python3 -I -B "$SKILL_DIR/scripts/route.py" edit_text --outcome unknown
```

该查询只返回 reconcile 动作，不重放编辑。没有完整交付清单的失败工程不能冒充已完成交付。
