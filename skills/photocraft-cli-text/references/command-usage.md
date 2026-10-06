# 完整命令调用 / Complete command usage

本入口覆盖本技能内完整固定反射目录，不受创作交付 workflow.py 的操作白名单限制。每条命令的参数原文、技能路由、空会话观察及逐命令验收状态见 [完整命令参考](command-reference.md)，机器索引为 [覆盖目录](command-coverage.json)。原生工具及参数 schema 见 [实际 MCP 快照](native-command-snapshot.json)。

This entry routes every command in the pinned reflected registry. It does not broaden the acceptance claims of workflow.py. The reference preserves verbatim parameters, skill ownership, empty-session observations and per-command acceptance status.

## 1. 定位、查询与准备 / Locate, inspect and prepare

SKILL_DIR 必须是宿主实际加载本 SKILL.md 的目录；支持用户／项目 .agents/skills、插件 skills 和宿主缓存。任何本领域单技能均包含此入口、目录和示例，不读取兄弟目录。

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" list --filter layer
python3 -I -B "$SKILL_DIR/scripts/commands.py" describe COMMAND_ID
```

查询无需安装或下载。参数说明是原生语法文本，不能将其直接作为 JSON，也不能把它冒称为正式 JSON Schema。先核对目标对象、工程、选择状态、素材、范围、单位及当前版本。命令目录存在不证明默认空会话能执行。

Queries require no installation. Parameter documentation is native syntax, not executable JSON or a fabricated JSON Schema. Establish the project, object IDs, selection, assets, units and current context before editing.

## 2. 同会话计划 / Persistent-session plans

计划只包含 schema 和 operations，schema 为 craft-command-plan/v1；每步必须提供 params 对象，并且恰好有 command 或 tool。command 使用完整命令目录中的 ID；tool 使用实际 MCP 快照中的工具名，可创建／打开／检查／保存／导出文档。

```json
{
  "schema": "craft-command-plan/v1",
  "operations": [
    {"command": "ACTUAL_COMMAND_ID", "params": {}, "as": "created"},
    {"command": "NEXT_COMMAND_ID", "params": {"id": {"$ref": "created.id"}}}
  ]
}
```

上面的 ID 是结构说明，不是可执行实例。必须从 describe 取得真实命令和必填参数；使用本技能内已执行的 examples/commands-advanced.json 作为完整实例。as 保存真实回执；$ref 可读取对象／数组路径，禁止前向和重复引用。对象 ID 按整数保留，不经过浮点转换。引用字段必须对应实际返回值，不能照搬其他工具的 id／layer／item／clips 字段。

The illustrative IDs above are not executable examples. Use the tested commands-advanced.json instead. Bind actual receipts with as and resolve earlier object or array paths with $ref; never guess a returned ID. Integer IDs retain their original type.

$input 引用不作为额外语法；使用 --input NAME=FILE 登记普通文件后，以 {"$ref":"NAME.path"} 引用复制后的文件路径，以 NAME.sha256 读取输入摘要。输入文件复制到新输出的 inputs 内并复验源及副本摘要。链接工程仍须登记其依赖，不会凭原路径自动复制所有依赖。

输出文件用 {"$output":"project.EXT"}：它解析为本次新输出目录内的目标；PhotoCraft 使用自动化根内相对路径，其他工具使用绝对路径。不能使用 ../、绝对路径或日志保留文件名。直接字符串参数仍由原生路径与权限规则处理，此入口不宣称隔离任意原生命令的全部副作用。

Inputs are copied and hash-checked via --input NAME=FILE and referenced as NAME.path. Linked project dependencies must be supplied explicitly. $output resolves a new output-relative target; PhotoCraft receives root-relative paths. Native commands retain their own permission rules and side effects.

## 3. 预检与执行 / Check and execute

```bash
python3 -I -B "$SKILL_DIR/scripts/commands.py" check "$SKILL_DIR/examples/commands-advanced.json"
python3 -I -B "$SKILL_DIR/scripts/commands.py" run "$SKILL_DIR/examples/commands-advanced.json" --output /absolute/new-command-result
```

check 检查完整计划的命令／工具身份、字段、JSON 数值及引用，不安装、不编辑。run 首次自动安装并校验固定 CLI；输出目录必须不存在。它检查实际 tools/list、完整注册表及每条命令的当前 enabled 状态。禁用立即停止并报告 why；不移除原生守卫、不自动选中另一对象、不忽略参数错误。原生 MCP 错误和返回对象中的 error 都算失败，包括表达式保存后被禁用的情况。

check validates all operations before installation; it is not native parameter or execution acceptance. run bootstraps the pinned CLI, verifies live tools and registry membership, and queries enabled state before each command. Disabled commands report the native reason. Native errors and semantic error fields fail the run.

## 4. GUI 与真实工程状态 / GUI and real project state

默认显式 headless。依赖面板、指针、窗口或交互的命令可能要求运行中的应用；不得把 headless 禁用解释为命令永久不存在。先在应用打开授权工程并建立选择状态，再指定 --mode bridge --connect 127.0.0.1:PORT。此入口映射各工具实际 --bridge／--connect 参数，不偷偷回退到其他会话。PhotoCraft 本地控制访问需要时使用 --control-token-file FILE；令牌不放计划、参数或回执。

Default mode is explicitly headless. UI-dependent commands require the running application and its project/selection state. Use --mode bridge --connect 127.0.0.1:PORT. PhotoCraft can use --control-token-file. GUI execution acceptance remains separately recorded; do not silently fall back to headless.

## 5. 回执、保存与恢复 / Receipts, saving and recovery

每步执行前／后持久化 journal.json。成功产生 success.json，失败产生 failure.json；命令超时、断开或无法确认结果时记录 unknown，不自动重放。新输出目录不能复用；再次执行前读取 journal 与实际工程，确认上次是否执行，另建修订计划。

Save or export must be explicit operations in the plan. A successful command receipt alone does not prove a deliverable. Save a new native project, reopen it in a separate session, check target parameters and unrelated objects, and independently inspect rendered output. Keep original assets and projects. Media packaging and exchange-loss acceptance still use the established workflow.py contracts when applicable.

保存和导出必须是计划中的显式步骤。success.json 只证明指定命令返回成功，不证明工程可重开、完整交付或创作通过。另存原生工程、独立会话重开、检查目标与非目标对象，实际解码或查看输出；保留原文件。需要素材打包及交换损失报告时继续使用已验收的 workflow.py 合同，不能把直接调用扩大为 ArtCraft 自动编排支持。

## 6. 逐命令完成标准 / Per-command completion

每项完整验收须绑定运行时摘要、实际前置上下文、输入参数、原生返回值、保存重开、预期输出、失败／禁用场景和适用时的局部修订。目录覆盖、结构预检、命令返回成功、代表实例通过分别记录。native-command-snapshot 是只读目录证据；command-coverage 中 NOT_RUN 表示本轮完整逐命令验收尚未完成，不覆盖历史有界任务证据。

A complete command acceptance binds runtime identity, real prerequisites, inputs, receipts, saved-project reopening, expected output, failures and applicable local revisions. Documentation coverage and representative cases are distinct from complete per-command acceptance.
