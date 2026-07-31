# 知乎OS Compiler V1

Status：ACTIVE_KERNEL

本文件定义知乎OS的内容编译器内核。

知乎OS不再被视为 Prompt 系统，而是内容编译器：

```text
业务语言
↓
中间表示
↓
自然语言
↓
平台反馈
```

## 1. Compiler First

任何新需求、规则、参数或优化，不允许第一反应是“加 Prompt”。

必须先回答：

```text
它属于哪一层？
它的唯一权威在哪里？
它是否破坏单向流？
它是否增加维护成本？
```

如果无法归层，默认拒绝新增。

## 2. 六层架构

```text
L1 Analyzer（分析层）
↓
L1.2 Structure Matcher（结构匹配层）
↓
L1.5 Router（路由层）
↓
L2 Slim IR（中间表示）
↓
L2.5 Runtime Assembly（运行时装配）
↓
L3 Writer Input Package（执行合同）
↓
L4 Writer（模型执行）
↓
L5 QA-A / QA-B（质量审计）
↓
L6 Feedback（数据回写）
```

每层只有一个职责。

## 3. L1 Analyzer

Analyzer 只回答：

- 这个问题到底在问什么。
- 题型是什么。
- 用户真实意图是什么。
- 用户隐藏约束是什么。
- 唯一主变量是什么。
- 辅助变量是什么。
- 核心机制是什么。

Analyzer 禁止：

- 写正文。
- 讨论表达风格。
- 生成开头、结尾、金句或文案。
- 判断知乎感、AI味和收藏感。

## 4. L2 Production Card IR

Production Card IR 是 Slim IR（Intermediate Representation），不是 Prompt，也不是完整 Writer 输入。

它只回答：

- 这篇文章讲什么。
- 唯一判断是什么。
- 核心机制是什么。
- 正文路线是什么。
- 正文结构是什么。
- 禁止漂移是什么。
- 结尾判断是什么。
- 发布链接是什么。

Production Card IR 的目标长度：500 字左右，最多一页。

Production Card IR 禁止：

- 讨论怎么写得像真人。
- 维护 AI 味规则。
- 维护阅读节奏规则。
- 维护表达语气、留白、段落长度。
- 把 PD / RR / RE / BT 参数逐项暴露给 Writer。
- 复制 Writer Prompt 或 QA 的规则。

## 4.1 L1.5 Router

## 4.0 L1.2 Structure Matcher

Structure Matcher 只回答：

- 本题应该调用哪一个唯一 ACTIVE 结构。
- 为什么选它。
- 为什么没有选其它 ACTIVE 结构。
- 本次匹配证据是什么。
- 匹配置信度是什么。

Structure Matcher 读取：

- Analyzer 输出。
- runtime ACTIVE 结构快照。
- 历史资产检索摘要。
- 允许生产调用的 ACTIVE 变量。

Structure Matcher 禁止：

- 读取未验证候选结构。
- 修改结构库。
- 写正文。
- 修改 IR。
- 把爆款样本原文直接带入生产。

输出字段必须优先中文，允许保留英文兼容别名。

Structure Matcher 的长期上游是 Research Layer / Structure Lab。结构进化机制以 `docs/知乎OS Structure Evolution V1.md` 为准。

Router 只回答：

- 本题是否接受 Structure Matcher 选出的唯一 ACTIVE 结构。
- 本题调用哪些 ACTIVE 规律。
- 本题调用哪些行为目标和 CR 目标。
- 本题需要哪些质量参数进入运行时装配。

Router 禁止：

- 写正文。
- 修改 Analyzer。
- 扩写 IR 为长 Prompt。
- 复制结构库、参数库、推理协议或表达协议全文。

Router 的输出只能作为 Runtime Assembly 的输入引用。

## 4.2 L2.5 Runtime Assembly

Runtime Assembly 负责把 Slim IR 和 Router 结果装配成 Writer Input Package。

它读取：

- Slim IR。
- runtime ACTIVE 结构快照。
- runtime ACTIVE 规律快照。
- 内容质量参数快照。
- 正文推理协议。
- 正文表达协议。
- Production Card 中已经锁定的行为目标、CR 目标、重点执行和素材边界。

它输出：

- Writer Input Package。

Runtime Assembly 禁止：

- 修改 Slim IR 的核心判断、核心机制、路线、结尾和禁止项。
- 新增 ACTIVE 规则之外的结构、参数或表达协议。
- 把 IR 膨胀回完整 Production Card。
- 把全文协议复制进 Package。

## 4.3 L3 Writer Input Package

Writer Input Package 是本次运行的完整执行合同。

它必须包含：

- run_meta。
- decision_ir。
- structure_contract。
- behavior_contract。
- expression_contract。
- material_package。
- acceptance_contract。

Schema 权威为：

```text
docs/Writer Input Package Schema V1.md
```

Writer Input Package 保存本次实际调用的版本、引用和义务摘要。它是运行证据，不是第二规则权威。

## 5. L3 Writer Prompt

Writer Prompt 是编译规则。

它只回答：

- 怎么把 IR 翻译成知乎真人语言。
- 怎么避免培训课、报告腔和管理学腔。
- 怎么压缩系统参数。
- 怎么控制节奏、留白、场景和收尾。
- 怎么把后台词改成真实职场语言。

Writer Prompt 禁止：

- 修改唯一判断。
- 修改主变量。
- 新增机制。
- 新增事实。
- 改变 Production Card IR 的正文路线。

## 6. L4 Writer

Writer 是可替换模型。

可选执行模型包括：

- Claude
- Codex
- GPT
- 后续其它模型

Writer 只负责：

- 按同一份 Writer Prompt。
- 按同一份 Production Card IR。
- 生成正文。

A/B 测试时，唯一变量必须是 Writer 模型。

禁止同时改变：

- Production Card IR
- Writer Prompt
- QA 标准

否则无法判断模型差异。

## 7. L5 QA

QA 拆为两类。

### QA-A｜决策一致性审计

只检查：

- 是否跑题。
- 是否违反 Production Card IR。
- 是否修改唯一判断。
- 是否新增主变量或新机制。
- 是否完成结尾判断。
- 是否达到发布底线。

### QA-B｜表达质量审计

只检查：

- AI味。
- 阅读节奏。
- 知乎感。
- 重复解释。
- 参数显形。
- 收藏感。
- 是否像真人回答。

QA 禁止：

- 重写正文。
- 修改 Analyzer。
- 修改 Production Card IR。
- 修改 Writer Prompt。

QA 只能输出问题、等级和修正指令。

## 8. L6 Feedback

Feedback 只负责数据回写。

必须记录两类指标。

### 输出质量指标

- QA-A 是否通过。
- QA-B 是否通过。
- 是否符合 Production Card IR。
- AI味风险。
- 重复解释风险。
- 收藏点是否完成。
- 是否可发布。

### 工程成本指标

- Production Card IR 字数。
- Writer Prompt 是否改动。
- 人工修改次数。
- 总 Token 消耗。
- 完成耗时。
- 问题定位难度。

架构升级不能只看文章质量，也必须看复杂度、可维护性和可替换性。

## 9. SSP｜Single Source of Policy

任何规则只有一个权威来源。

其它层只能引用，不得复制维护。

| 规则 | 唯一权威 |
| --- | --- |
| 用户真实问题 | Analyzer |
| 主变量 | Analyzer |
| 唯一判断 | Production Card IR |
| 正文路线 | Production Card IR |
| 禁止漂移 | Production Card IR |
| 人话表达 | Writer Prompt |
| AI味标准 | QA-B |
| 发布标准 | QA-A |
| 收益评估 | Feedback |

如果同一规则出现在多个层，必须删除重复项，只保留唯一权威。

## 10. 单向流

知乎OS Compiler 只能单向流动：

```text
Analyzer
↓
Structure Matcher
↓
Router
↓
Slim IR
↓
Runtime Assembly
↓
Writer Input Package
↓
Writer
↓
QA
↓
Feedback
```

禁止反向修改：

- Runtime Assembly 不得修改 IR。
- Writer 不得修改 IR。
- Writer 不得修改 Analyzer。
- QA 不得修改 Writer Prompt。
- QA 不得修改 IR。
- QA 不得修改 Writer Input Package。
- Feedback 不得直接修改 Writer Prompt 或 IR。

允许的反馈路径只有：

```text
QA / Feedback
↓
下一轮 Analyzer 或系统升级评审
↓
重新生成
```

## 11. 十篇试运行门槛

Compiler V1 作为正式内核进入试运行，但不立即重构 Notion 页面和数据库。

必须完成至少 10 篇真实知乎生产，且满足以下条件，才允许重构 Notion 首页或数据库结构：

- IR 持续保持精简。
- Writer Prompt 基本不需要单题改动。
- QA 能快速定位问题。
- 人工修改次数下降。
- 正文质量不低于旧链路。
- 工程成本没有显著上升。

试运行必须同时维护：

- Compiler Data Flow 产物。
- QA 报告。
- Feedback 记录。
- Failure Pattern 记录。

10 篇前禁止：

- 重构 Notion 首页。
- 新建六套数据库替代旧系统。
- 删除旧 Production Card 流程。
- 批量迁移历史数据。

## 12. 当前兼容策略

现有 `Production Card` 名称暂时保留，但在 Compiler V1 中解释为：

```text
Production Card = Slim IR 的决策来源之一
```

Writer 正式输入以 Writer Input Package 为准。后续 Production Card 模板瘦身按 10 篇试运行结果推进，但不得删掉 Runtime Assembly 所需的运行时约束来源。

## 13. 失败模式升级闸门

任何协议、模板、Writer Prompt 或 QA 标准升级，必须先进入 Failure Pattern。

升级条件：

```text
同一失败模式
↓
累计 3 次
↓
归属层明确
↓
证据可复查
↓
进入系统升级评审
```

未满 3 次时：

- 只记录。
- 不改协议。
- 不改模板。
- 不改 Writer Prompt。
- 不改 QA 标准。

## 14. Data Flow Schema

Compiler 各层输入输出以 `docs/知乎OS Compiler Data Flow V1.md` 为准。

它定义：

- Analyzer.json
- IR.json
- Writer Input Package
- Draft.md
- QA Report
- Feedback.json
- Failure Pattern
