# Prompt Library

我的 Prompt 资产库 v0.1

## 目录

- `templates/`：按任务类型分类的可复用模板
- `best-practices/`：沉淀的 Prompt 心法和方法论
- `CHANGELOG.md`：版本记录

## 使用原则

1. 每个模板必须带 metadata（适用模型、版本、指标）
2. 每个模板必须带 test_cases（至少 5 条）
3. 修改模板必须升版本号并记 CHANGELOG

## 模板版本规范

语义化版本：`v主.次.补丁`
- 主：Prompt 结构大改
- 次：新增 few-shot 例子 / 微调指令
- 补丁：改错别字 / 格式微调
