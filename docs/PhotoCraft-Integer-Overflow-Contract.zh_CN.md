# PhotoCraft 整数字面量溢出合同

插件dev.49锁定技能源dev.43，在安装前拒绝原生有限f64范围之外的整数字面量。先检查数值文本再构造Python整数，5000位字面量仍保留精确字段路径；合法有限大整数保留旧类型。

[定向证据](evidence/optimization/integer-overflow/candidate.json)覆盖解析器／MCP／工具回复，以及13个独立技能的52例公开拒绝观察。无效输入返回nonfinite_json_value、validation／not_executed、retryable=false和correct_plan。安装／会话次数为零，原文件、运行时缓存和输出目录不变；原红灯捕获安装尝试，超长字面量红灯捕获字段路径缺失。完整源回归和固定公开副本验收分别记录。

同版打包[Droplet候选](PhotoCraft-Supervised-Droplet-Candidate.zh_CN.md)，其craft.5原生运行时未启用；公开运行时仍为craft.1。9.6、流式、嵌套聚合内部、公开监督接入、持久raw恢复及完整首版仍开放。
