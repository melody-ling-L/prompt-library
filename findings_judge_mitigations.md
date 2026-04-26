# Findings: LLM-as-Judge — Rubric、偏置与缓解（Day 8–9）

> **归档日期**：2026-04-26  
> **仓库**：prompt-learning / llm-playground 实验代码（`judge_v1.py`、`judge_v2.py`、`judge_bias_test*.py`）  
> **模型**：DeepSeek Chat，`temperature=0`（除非另有说明）

---

## 1. 我们在解决什么问题

用 LLM 给「B 端客户道歉邮件」打分时，需要同时满足：

1. **可解释**：先判一票否决（deal breaker），再打多维分，并给出理由。  
2. **可对齐事实**：`fabrication` 必须结合 **Input** 判断，否则会误杀「合理补救」或放过「捏造第三方」。  
3. **可审计偏置**：同一内容不同表述、顺序、长度，分数不应无理由漂移。

---

## 2. Judge v1：Rubric 与 Prompt 设计要点

### 2.1 与 `judge_rubric_apology.yaml` 对齐的四维

| 维度 | 权重 | 作用边界（避免维度重叠） |
|------|------|---------------------------|
| empathy | 0.25 | 对客户处境与情绪，不看格式 |
| transparency | 0.25 | 事故说明是否具体、是否推诿 |
| remediation | 0.30 | 补偿与下一步是否可执行、可验证 |
| professionalism | 0.20 | 结构、称谓、用语是否 B 端规范 |

### 2.2 Deal breakers

- **fabrication**：与 **事故/根因/外部协作** 相关、且无法在 Input 中溯源的实体或矛盾陈述；**不**把「发件方 Acme 署名、官方 @acme.com、合理补救承诺」一律算作编造。  
- **blame_shift**：把主责推给客户环境/操作，并否认平台侧责任。

### 2.3 Prompt 工程经验

- **单一 JSON**：禁止在 system 里堆多个 JSON 示例块，否则模型容易漏字段或结构错乱。  
- **先 deal_breaker 后打分**：与后处理逻辑（FAIL → `overall_score=null`）一致。  
- **CoT**：要求 `cot` + `deal_breaker_reasoning` + `dimension_reasoning`，便于复核与迭代。

### 2.4 校准用例（`judge_v1.py`）一次跑通结果

| Case | 预期 | 结果 |
|------|------|------|
| 高质量 | PASS | PASS，overall 5.0 |
| 低共情 | PASS | PASS，overall 偏低（约 1.x） |
| 编造李工 / ABC | FAIL | FAIL，`fabrication=true` |
| 甩锅客户 | FAIL | FAIL，`blame_shift=true` |

---

## 3. Day 9 偏置实验（v1：`judge_bias_test.py`）

### 3.1 Verbosity（短版 vs 灌水版，信息等价）

- **现象**：灌水版总体略低于短版（约 **-0.20** 分），主要在 `professionalism`（4 vs 5）。  
- **解读**：与「越长越高分」相反，属于**少见**方向，但仍说明 **长度/修辞会影响 judge**，不能假设信息等价则分数相等。

### 3.2 Position（pairwise 顺序）

- **现象**：两种顺序下 **6/6** 判定与「高质量应赢」一致。  
- **解读**：在该任务与模型组合下，**未观察到明显 position bias**（不能外推到所有 pairwise 场景）。

### 3.3 Stability（同一高质量 case，temp=0 连跑 5 次）

- **现象**：verdict 与 overall、各维分数 **完全一致**，σ=0。  
- **解读**：在 **temp=0 + 固定 prompt** 下，该 judge **可复现**；临界 case 另见 v2。

---

## 4. Judge v2：四项缓解（`judge_v2.py`）

针对 v1 / Day9 前期暴露的问题：

| ID | 措施 | 目的 |
|----|------|------|
| M1 | **风格中立条款**（Style Neutrality） | 降低「温暖型 vs 专业型」偏好 |
| M2 | **1–5 全锚点**（补全 2/4 分等） | 减少锚点稀疏导致的随机性 |
| M3 | **多次采样 + 中位数** | 降低单次判分的方差 |
| M4 | **needs_review 标记** | 对高方差维度触发人工复核 |

### 4.1 一次 `python3 judge_v2.py` 的观测

1. **风格对照（信息等价：温暖型 vs 专业型）**  
   - 温暖型 overall **5.0**，专业型 **4.75**，差约 **+0.25**。  
   - **结论**：M1 后仍有**残余风格偏好**（尤其 `empathy`），不能认为「写进 prompt 就完全消除」。

2. **临界质量 + 5 次采样**  
   - `professionalism` 在 3/4 间摆动，σ≈**0.55**，`needs_review=True`。  
   - **结论**：**M3+M4 生效**——系统能自动标出「不稳维度」，避免把单次分数当真理。

---

## 5. 可复用的工程清单（Portfolio 向）

1. **Rubric 与代码同源**：YAML 描述 + Python `RUBRIC` 双份时，改一处要同步另一处，或改为**运行时加载 YAML**。  
2. **后处理归一化**：`deal_breakers` 兼容字符串 `"true"`，避免解析抖动。  
3. **Bias 回归套件**：verbosity / position / stability 应作为 **CI 或发版前** 的固定回归（阈值可配置）。  
4. **v3 方向（未实现，供迭代）**  
   - 对「信息等价的风格对」做 **pairwise 强制 tie-break** 或 **分差上限**约束。  
   - 临界 case：**投票数↑** 或 **双 judge 模型** 再聚合。  
   - 将 **fabrication** 规则做成可配置策略（严格 / 宽松），适配不同合规要求。

---

## 6. 相关文件索引

| 文件 | 说明 |
|------|------|
| `judge_rubric_apology.yaml` | Rubric 规范（v1 对齐） |
| `judge_v1.py` | Judge v1 + 校准用例 |
| `judge_bias_test.py` | Verbosity / Position / Stability |
| `judge_v2.py` | M1–M4 缓解 + 中位与 needs_review |
| `judge_bias_test_v2.py` | 更刁钻的 bias 场景（v2 配套） |

---

**一句话**：LLM-as-Judge 要上线，**Rubric + deal breaker + JSON 契约** 只是基础；**偏置测试与方差监控** 才是把它从 demo 变成工程组件的分水岭。
