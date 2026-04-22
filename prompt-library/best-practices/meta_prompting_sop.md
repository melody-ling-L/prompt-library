# Meta-Prompting SOP

## 标准流程

1. 用 Meta-Prompt 生成初版（从 0 到 1）。
2. 手动诊断可执行性和约束冲突。
3. 增加 System/User 分层与 Action Trigger。
4. 跑固定 Eval 集（至少 10 条）。
5. 根据失败样例迭代，更新版本与 CHANGELOG。

## 禁止直接上线

- 未实测的 Meta-Prompt 输出禁止直接用于生产。
- 未给出失败样例分析禁止升级主版本。

## 产出要求

- 每次迭代至少记录：输入、输出、失败类型、修正措施。
- 模板升级需同步更新 `metadata.yaml` 与 `CHANGELOG.md`。
