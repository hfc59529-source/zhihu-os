# Topic Investment / Production Entry Gate V1

日期：2026-10-09（Africa/Nairobi）
状态：PROPOSED / HUMAN_REVIEW_PENDING；不是已生效的生产入口。
来源：用户提出的八项Evidence-Informed Decision要求。
上层目标：[Research Objective](../RESEARCH_OBJECTIVE.md)。

## 审计结论与实施范围

现有Topic Package已经有“适合回答的原因”“历史重复检查”“风险提示”“推荐级别”，以及同题Answer_Benchmark_Top3；这些不是本账号历史Case-Control对照。缺口是：选题判断未统一保留历史结果、测量局限、反例及人工投资决定。

复用Topic Package，不新建独立Investment对象、总分、权重模型、Compiler节点或研究项目。准备在现有采集协议定义规则，选题包模板只新增记录槽位；历史Case与指标只引用原数据/报告。INVEST是上游选题授权，不等于正文USER_APPROVED或Runtime Release Approval。

本提案不使用EXP008候选解释作为选题门槛。第五问已有治理骨架，尚不意味着数据可靠性、机制验证或前瞻预测已经完成。

## 拟定入口规则

候选可以进入Topic Pool和进行采集；只有证据说明完成、且用户对当前版本作出INVEST决定后，才作为正式回答机会交给INPUT。DELAY保留待补证据/待时机；KILL结束本次机会，不宣布题目永远无价值。

完整性不是证据充分性：每项必须填写有来源的事实、明确假设或UNKNOWN，并说明检索/未知原因；不能用一串UNKNOWN冒充已检索。没有可比Case、指标缺失或尚无Validated Rule，均不自动KILL。用户可以以“明确的不确定性下有限探索”批准INVEST，但要记录投入边界和测量计划，不得宣称有稳定机制支持。

Codex负责整理证据、局限与可选建议；不得替用户填写Human Decision。用户手动提供的问题遵循同一记录和审核要求，不形成另一套入口。

## 选题包内的八项记录

### 1. Question Value

- 为什么值得占用一次回答机会：读者判断需求、现有答案覆盖与尚待澄清的问题。
- 本次机会成本/投入边界：时间或工作量约束；无法估计写UNKNOWN，不伪造ROI。
- 区分用户需求事实与研究者解释；不提前确定唯一核心判断、正文方向或结构。

### 2. Historical Evidence

- 对照Case ID/article_id、原报告或源表引用；可比条件及关键差异。
- 检索范围/方法；若找不到，记录NO_COMPARABLE_CASE及原因。
- 条件允许时同时寻找赢家与输家；不得只挑高播放、高收益的成功案例。
- 题材相近不等于机制相同；“最相似”必须说明具体相似维度及无法控制的差异。

### 3. Distribution Evidence

- 每个Case的阅读/播放数值、观察时间、实际内容年龄、指标来源和窗口。
- 是否存在曝光数据；阅读不能代替曝光事实。
- 证据状态、反例、可比性与UNKNOWN；不同时间/来源不得拼成当前赢家倍数。
- 高互动只能作为已观察的后置结果或待检验中介，不能直接倒推前置分发原因。

### 4. Monetization Evidence

- 收益值与单位、收益窗口、采集时间、身份匹配方法、证据引用。
- 阅读/收益有效窗口是否对齐；不对齐标MEASUREMENT_UNKNOWN / ATTRIBUTION_UNKNOWN。
- 缺失不等于0；盐粒/阅读仅可作明确口径的描述性比值，不称稳定RPM。
- 相似Case收益高不自动证明候选题会产生同类收益或具有相同受众。

### 5. Lifecycle Evidence

- 引用现有阶段观察：INITIAL_DISTRIBUTION / STAGNATION / REACTIVATION / LONG_TAIL / UNKNOWN。
- 阶段的时间区间、证据状态及人工审核状态；未经审核的解释标HYPOTHESIS。
- 允许重复、跳跃、重叠；没有日级/固定窗口证据不能断言“首轮死亡”。
- 确认某Case发生过再放量，不等于知道候选题为什么或是否会再激活。

### 6. Insight Duplication

- 最近相关历史内容/生产ID及已表达的认知，引用可读取原文/已冻结Decision；读取不到标UNKNOWN。
- 区分重复题材、重复问题与重复认知；检索范围明确，不武断声称“全库未重复”。
- 候选是否存在新的待回答问题，仅作为待DECISION检验的参考；不生成新回答的唯一核心判断。
- 复用现有“历史重复检查”，不复制另一张重复数据库。

### 7. Evidence Status

每条影响投资判断的陈述记录：claim、FACT/HYPOTHESIS/UNKNOWN、source_reference、measurement_limit、counterexample_or_failure_condition。

FACT只表达来源能够支持的观察，不把相关性标成因果事实；HYPOTHESIS不进入生产规则；UNKNOWN明确缺什么。纯粹价值取舍和投资理由由用户承担，不伪装成平台事实。

### 8. Human Decision

- decision：PENDING / INVEST / DELAY / KILL。
- decided_by、decided_at、reviewed_package_version、decision_reason、accepted_unknowns。
- INVEST另记录investment_scope和measurement_plan；DELAY记录待补条件；KILL记录本次停止原因。
- 默认PENDING；AI建议与人类决定分开。决定绑定实际审核的候选版本，关键内容变化后重新审核。

禁止加权总分、82分之类排名结论或把领导题/高互动/二次激活写为投资公式。

## 最小上线变更清单（待批准）

规则唯一权威仍为 `docs/Codex选题采集协议.md`：

1. 在§1与§2交接边界明确“Topic Package采集完成后，等待用户Investment Decision；INVEST后交给INPUT”，不改变Compiler节点。
2. 在采集完成标准附近增加本提案八项完整性要求及UNKNOWN/探索出口，保留现有账号方向、风险检查和合法性约束。
3. 规定Decision为PENDING/DELAY/KILL时不作为正式生产机会交接；不禁止继续候选采集。

`templates/选题包模板.md` 只增加对应字段：

1. §8复用Question Value记录；§10复用Insight Duplication记录。
2. 新增一个“Topic Investment Evidence”区块，容纳Historical/Distribution/Monetization/Lifecycle/Evidence Status与Human Decision；引用原数据，不复制研究正文。
3. §13交接状态区分“采集完成，待投资审核”与“用户INVEST，交给INPUT”。

不得修改Compiler内容逻辑、正文Prompt、ACTIVE变量或选题权重。本提案不处理既有9月14日选题簇加权与runtime漂移，不通过顺带改权威表或hash掩盖它。

## 验收与批准路径

上线前用真实或明确标为fixture的选题包进行最小合同验证：

| 情况 | 预期 |
|---|---|
| 证据齐全但Human Decision=PENDING | 可完成采集，不得正式交给INPUT |
| 无可比Case、检索已说明、用户明确INVEST有限探索 | 允许交接；UNKNOWN保持，不创造Validated Rule |
| 高阅读Case收益窗口不对齐 | 收益归因UNKNOWN，不推断高RPM |
| 缺日级窗口、只有旧累计端点 | 初始死亡/激活时点UNKNOWN |
| 用户DELAY/KILL | 不进入本次正式生产 |
| 有旧认知对照但无新Decision | 可以检查重复，不提前冻结新核心判断 |
| 审核后关键候选内容变化 | 原投资决定不自动沿用 |

以上验证证明接口合同是否成立，不证明分发、变现或长尾机制。Validation结果、反例检查与具体文件diff准备完毕后，才由用户审核Scoped Promotion Approval。概念认可不能冒充具体diff批准；不得填写虚构的PASSED或批准记录。

当前生产协议与模板尚未修改；本提案未生效，未宣称已建立强制执行门禁。无需新建基础设施，先审核此最小入口契约，再准备对应受控变更。
