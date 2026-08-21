# GPT 审核清单

执行版本：GPT-AUDIT-CHECKLIST-V2.0

本清单是 AUDIT 节点的执行载体，权威定义见 [`docs/知乎OS Compiler V1.md`](../docs/知乎OS%20Compiler%20V1.md) 第7节。AUDIT 核对两类合同：A. Execution Compliance（Execution IR 的 Run-specific Acceptance Criteria 是否兑现）；B. Operational Quality Checks（Runtime.Audit Rules 中已具备明确操作定义的通用表达约束）。

## REVIEW Diagnosis 入口

AUDIT 完成后，如需要向用户说明成稿质量瓶颈或讨论 Revision 方向，可使用 [`docs/生产状态机与交接规范.md`](../docs/生产状态机与交接规范.md) 的 `REVIEW DIAGNOSIS：成稿诊断语言`。

边界：

1. REVIEW DIAGNOSIS 不属于本清单 A/B 检查项，不生成 `AuditRule.<ID>`。
2. REVIEW DIAGNOSIS 不得作为 AuditResult 的 Expected Source，不得改变 PASS / Issues[] 结论。
3. REVIEW DIAGNOSIS 只用于诊断成稿瓶颈和确定最小修改方向，不构成 WRITE 要求，不要求维度齐全，不因单项缺失自动补写。

## A. Execution Compliance 检查（对应 Execution IR Acceptance Criteria）

- [ ] 是否回应原问题
- [ ] ACTIVE 是否正确
- [ ] 核心判断是否正确
- [ ] 参数是否调用正确
- [ ] 参数是否遗漏
- [ ] 参数是否冲突
- [ ] Reasoning Path 是否漏步骤（Reader Mental Model / False Inference / Breaking Point / Mechanism / Transformation）
- [ ] Structure 义务是否缺失
- [ ] Material Boundary 是否越界（使用了未授权案例、数据或人物）

## B. Operational Quality Checks（对应 Runtime.Audit Rules 通用表达检查）

以下规则来自已发布 Runtime 的 `runtime/知乎内容质量参数快照.md` 中 ACTIVE 的 RR 阅读体验参数；本清单只收录具备明确操作定义、能给出 PASS / REVISE / BLOCK 的子规则，作为 AUDIT 可引用的 `AuditRule.<ID>`。不得把整组 RR 参数视为自动进入审核的规则正文；只有本节登记的子规则才是 Runtime.Audit Rules。

### Run Activation 执行闭环

AUDIT 不得把 B 组当作可选检查集合。每次审核必须先完成：

```text
Execution IR + Draft
↓
逐条计算 AuditRule Run Activation Condition
↓
形成 Activated AuditRule Set
↓
对 Activated AuditRule Set 逐条执行
↓
输出 PASS 或 Issues[]
```

执行要求：

1. 每条 AuditRule 必须记录 `Activated / Not Activated`。
2. `Activated` 的 AuditRule 必须逐条执行，不得抽查。
3. `Not Activated` 必须写明原因，例如正文未达 1500 字、题型不是现实组织题、正文没有行动建议。
4. 只有所有 A 组 Execution Compliance 和 Activated AuditRule Set 均无有效 Issue，最终结论才允许 PASS。
5. 未登记为 AuditRule 的质量知识，只能作为 Observation，不得写入 AuditResult。

### AuditRule Registry

- [ ] `AuditRule.RR-01-01` 核心判断数量。Run Activation Condition：所有知乎正文默认激活。Expected：全文核心判断建议 1-3 个，唯一主判断必须能用一句话表达，其他判断必须服务主判断；不得每节都创造新的底层规律。Failure：无法确定唯一主判断为 BLOCK；超过 5 个可单独成立的核心判断为 BLOCK；4-5 个核心判断且主线分散为 REVISE。
- [ ] `AuditRule.RR-01-02` 单段认知任务。Run Activation Condition：所有知乎正文默认激活。Expected：每个自然段只完成描述现象、展示场景、解释一个原因、推导一个机制、给出一个判断或提供一个行动建议中的一种主要任务。Failure：多个段落同时承载三种以上任务并影响理解为 REVISE。
- [ ] `AuditRule.RR-01-03` 连续认知上限。Run Activation Condition：正文存在多个判断、多个因果层或连续抽象推导时激活。Expected：连续出现 2 个新判断后，必须进入场景、对话、动作、现实观察、简短例子或总结停顿；禁止连续 3 个以上新判断。Failure：连续 3 个以上新判断为 REVISE。
- [ ] `AuditRule.RR-01-04` 因果链长度。Run Activation Condition：正文存在显性因果推导时激活。Expected：单次显性因果推导建议 2-4 层；超过 4 层必须拆成“现象→场景→原因→缓冲→机制→判断”。Failure：单次显性因果推导超过 4 层且未拆分缓冲为 REVISE。
- [ ] `AuditRule.RR-02-02` 抽象句比例：每连续 3 段中，至少 1 段包含具体对象或现实动作。
- [ ] `AuditRule.RR-02-03` 句子负荷：一句话超过 60 字进入检查，超过 80 字默认标记长句负荷过高。
- [ ] `AuditRule.RR-02-04` 解释冗余：同一观点最多允许 1 次提出、1 次解释、1 次场景证明、1 次总结；相邻 3-5 段不得换词重复解释同一个观点。
- [ ] `AuditRule.RR-03-01` 机制后缓冲承接。Run Activation Condition：正文完成一个核心机制解释、连续两个新判断或连续两段抽象分析后激活。Expected：机制后必须出现 30-120 字的场景、对话、动作、观察或停顿承接，且不展开新机制。Failure：核心机制后缺少缓冲为 REVISE；缓冲虚构具体事实为 BLOCK。
- [ ] `AuditRule.RR-03-02` 缓冲不新增机制。Run Activation Condition：正文使用场景、对话、动作、观察或停顿作为缓冲时激活。Expected：缓冲只帮助读者吸收上一层机制，不引入新的核心机制、变量或理论。Failure：缓冲段引入新机制导致主线分叉为 REVISE。
- [ ] `AuditRule.RR-04-02` 段落长度变化：全文应有 1-2 行短段、3-5 行中段和少量 5-8 行长段；禁止全文同长度，禁止全文一句一段。
- [ ] `AuditRule.RR-04-04` 解释切断点：连续抽象解释达到 3 段、300 字、2 个机制或 3 次因果连接时，必须用场景、对话、动作、例子或短判断切断。
- [ ] `AuditRule.RR-04-SEVERITY` 阅读节奏严重级别：连续 5 段以上抽象解释为 BLOCK；连续 3 段解释为 REVISE。
- [ ] `AuditRule.RR-05-01` 机制现实承接。Run Activation Condition：正文出现核心机制、抽象概念或行动建议时激活。Expected：每个核心机制至少绑定一个现实场景、具体对象、组织动作或可感知例子。Failure：核心机制无现实承接为 REVISE；以伪造真实案例完成承接为 BLOCK。
- [ ] `AuditRule.RR-05-02` 抽象词翻译。Run Activation Condition：正文首次出现权力、资源、责任、成本、收益、博弈、共识、风险、边界、结构、机制、传导、激励等抽象概念时激活。Expected：抽象概念首次出现后，用普通人语言翻译一次，或立刻接具体动作/场景使其可理解。Failure：连续使用未翻译抽象词并影响理解为 REVISE。
- [ ] `AuditRule.RR-05-03` 用户经历映射。Run Activation Condition：现实题、职场组织题、管理题默认激活。Expected：正文中至少出现一个读者可直接对照自身经历的节点，如会议、汇报、群消息、邮件、纪要、项目推进、责任追问。Failure：全文没有可对照经历节点为 REVISE。
- [ ] `AuditRule.RR-06-03` 判断奖励数量。Run Activation Condition：所有长文默认激活。Expected：全文保留 2-3 个可单独成立的判断句，不得超过 5 个，不得每节都制造判断句。Failure：判断句超过 5 个或每节都制造判断句导致主线分散为 REVISE；超过 5 个独立核心判断按 RR-07 汇总结论 BLOCK。
- [ ] `AuditRule.RR-06-04` 行动奖励数量。Run Activation Condition：正文提供行动建议、判断工具或处理边界时激活。Expected：行动建议保留 1-3 个动作。Failure：行动建议超过 3 个且造成主线分散为 REVISE。
- [ ] `AuditRule.RR-06-05` 结尾奖励。Run Activation Condition：所有知乎正文默认激活。Expected：结尾只收束主判断、给行动边界或留下迁移判断，不新增机制。Failure：结尾新增理论造成主轴漂移为 BLOCK；结尾只堆口号且无判断/边界/迁移价值为 REVISE。
- [ ] `AuditRule.RR-07-01` 连续抽象疲劳：连续 3 段没有人物、动作、场景或具体对象，标记高风险。
- [ ] `AuditRule.RR-07-02` 连续解释疲劳：连续 3 段均以因果解释为主，标记高风险。
- [ ] `AuditRule.RR-07-04` 场景不足：1500 字以上正文少于 2 个现实场景，标记中风险。
- [ ] `AuditRule.RR-07-05` 人物语言不足：现实题全文没有人物语言或交流片段，标记中风险。
- [ ] `AuditRule.RR-07-06` 长句疲劳：超过 60 字句子多于 5 句，或超过 80 字句子多于 2 句，标记中风险。
- [ ] `AuditRule.RR-07-07` 段落机械化：70% 以上段落长度高度接近、大量一句一段或每节同构，标记中风险。
- [ ] `AuditRule.RR-07-09` 抽象名词堆积：连续 150 字内出现 6 个以上抽象概念，标记高风险。
- [ ] `AuditRule.RR-07-10` 结尾过载：结尾 20% 篇幅仍在新增机制、变量或理论，标记高风险。
- [ ] `AuditRule.RR-08-01` 一句话复述。Run Activation Condition：所有长文 QA 默认激活。Expected：普通读者读完后，应能用一句话说出文章主要判断。Failure：一句话复述失败为 BLOCK。
- [ ] `AuditRule.RR-08-02` 三点复述。Run Activation Condition：所有长文 QA 默认激活。Expected：读者最多记住三个关键内容，通常是为什么会发生、真正风险是什么、应该怎么做。Failure：三点复述失败为 REVISE；需要记住五个以上步骤才能理解为 REVISE。
- [ ] `AuditRule.RR-08-03` 概念替换测试。Run Activation Condition：正文出现参数名、理论名、机制名或抽象概念时激活。Expected：删除参数名和理论名后，正文仍应能理解。Failure：删除术语后无法说明现实中发生了什么为 BLOCK。
- [ ] `AuditRule.RR-08-04` 普通读者测试。Run Activation Condition：所有长文 QA 默认激活。Expected：无管理学、组织行为或商业背景的读者，应能理解发生了什么、为什么、自己怎么办。Failure：普通读者测试失败为 BLOCK。
- [ ] `AuditRule.RR-08-05` 跳读测试。Run Activation Condition：正文含标题、加粗句、分节首段或结尾时激活。Expected：只看标题、加粗句、每节首段和结尾，仍应能理解文章主线。Failure：跳读无法理解主线为 REVISE。

RR-07 汇总结论：无高风险项且中风险项不超过 2 个为 PASS；1 个高风险或 3 个以上中风险为 REVISE；连续 5 段以上抽象解释、超过 5 个核心判断或普通读者测试失败为 BLOCK。

## 最终结论：AuditResult

最终结论只能是：

- PASS
- Issues[]：每条必须包含以下五项，缺一不得作为有效 Issue 写入：
  - Expected Source：`Execution IR.AcceptanceCriteria.<N>` 或 `AuditRule.<ID>`
  - Expected
  - Actual
  - Violation Source：违反的是 Execution IR 的哪个字段，还是哪条 Audit Rule
  - Return Stage：由 Violation Source 查 Architecture Routing Table 机械得出，AUDIT 不裁量

## 归因规则（Architecture Routing Table，权威见 Compiler V1 第7节）

不再使用"正文问题 / 系统问题"二分，Return Stage 只能是以下四种之一：

| Violation Source 情形 | Return Stage |
| --- | --- |
| Expression Constraints / Acceptance Criteria 未兑现，但 Execution IR 本身没错（如 A 组勾选项已满足，但 B 组表达检查未达标；或 Claude 遗漏已有参数、未执行已冻结的 Explanation Target） | WRITE |
| Structure / Material Boundary 与 Decision 对不上（COMPILE 编译错了，如结构选择错误、素材边界划定错误） | COMPILE |
| Reality / Main Gap / Transformation / Core Judgment 本身站不住 | DECISION |
| 支撑 Decision 的事实本身不存在或错误（选题包事实缺失或有误） | INPUT |

不得使用 Expected Source（Execution IR 或已发布 Audit Rule）之外的任何标准；"觉得应该更好""更有阅读价值"一类临时想到的标准不得进入审核，只能记录为 Observation，不写入 AuditResult。

处理动作：

- Return Stage = WRITE：退回 Claude 按 Execution IR 修改 Draft（Patch 模式）。
- Return Stage = COMPILE / DECISION / INPUT：退回对应节点重新生成新版本对象，重新沿流水线向下走，最终重新进入 AUDIT，不直接进入 WRITE 局部修补。
- 无法判断 Expected Source：记录 Observation，不写入 AuditResult，不修改系统。

单次问题按 Return Stage 退回对应节点即可，不需要单篇升级为系统规则；只有同一失败模式累计 3 次、且归属节点明确（见 `templates/Failure Pattern模板.md`），才进入 Governance Plane 变更评审。

## 参数调用日志写入规则

参数调用日志以 GPT / 人工审核结果为准，不以 Claude 自报为准。

记录时必须区分：

- Claude 声称调用的参数。
- GPT / 人工确认实际生效的参数。
- GPT / 人工确认未生效、误用或遗漏的参数。
