# PhotoCraft 插件组件边界

根目录`plugin.json`是Agent Plugins 1.0.0可移植身份；`skills/`的14个直接子目录中有13个锁定技能源快照和1个插件本地任务控制技能。宿主专用命令与钩子位于`com.anthropic.claude-code/`，由`.claude-plugin/plugin.json`显式指向。命令按同名技能转交输入，钩子只在Claude Code会话启动／恢复时提示复用原实例；不安装、不启动、不关闭原生应用。缺少此宿主扩展时，技能仍按根目录固定位置独立发现。

原生操作由技能自带脚本调用锁定的PhotoCraft CLI；跨步骤任务复用所属会话，超时先核对同一请求。插件本地Harness仍为显式高级入口，其历史合同由OpenSpec保持，普通领域命令不默认调用它。`src/`是现有任务控制实现，`scripts/`包含开发验证与发布工具；两者均不是Agent Plugins 1.0.0新增的可移植组件。

`claude plugin validate . --strict`核验Claude专用manifest，但当前校验器的`contents`为空，不能据此证明宿主已发现14条命令或实际路由。包内测试逐项检查入口、同名技能、钩子仅SessionStart及不操作原生进程。固定安装、模型选择与真实原生交付按PC-RL-001另行验收。
