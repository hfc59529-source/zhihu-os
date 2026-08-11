# GPT 审核清单

执行版本：GPT-AUDIT-CHECKLIST-V2.0

本清单是 AUDIT 节点的执行载体，权威定义见 [`docs/知乎OS Compiler V1.md`](../docs/知乎OS%20Compiler%20V1.md) 第7节。AUDIT 核对两类合同：A. Execution Compliance（Execution IR 的 Run-specific Acceptance Criteria 是否兑现）；B. Operational Quality Checks（Runtime.Audit Rules 中已具备明确操作定义的通用表达约束）。

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

以下规则来自已发布 Runtime 的 `runtime/知乎内容质量参数快照.md` 中 ACTIVE 的 RR 阅读体验参数；本清单只收录具备明确操作定义、能给出 PASS / REVISE / BLOCK 的条目，作为 AUDIT 可引用的 `AuditRule.<ID>`。

- [ ] `AuditRule.RR-02-02` 抽象句比例：每连续 3 段中，至少 1 段包含具体对象或现实动作。
- [ ] `AuditRule.RR-02-03` 句子负荷：一句话超过 60 字进入检查，超过 80 字默认标记长句负荷过高。
- [ ] `AuditRule.RR-02-04` 解释冗余：同一观点最多允许 1 次提出、1 次解释、1 次场景证明、1 次总结；相邻 3-5 段不得换词重复解释同一个观点。
- [ ] `AuditRule.RR-04-02` 段落长度变化：全文应有 1-2 行短段、3-5 行中段和少量 5-8 行长段；禁止全文同长度，禁止全文一句一段。
- [ ] `AuditRule.RR-04-04` 解释切断点：连续抽象解释达到 3 段、300 字、2 个机制或 3 次因果连接时，必须用场景、对话、动作、例子或短判断切断。
- [ ] `AuditRule.RR-04-SEVERITY` 阅读节奏严重级别：连续 5 段以上抽象解释为 BLOCK；连续 3 段解释为 REVISE。
- [ ] `AuditRule.RR-07-01` 连续抽象疲劳：连续 3 段没有人物、动作、场景或具体对象，标记高风险。
- [ ] `AuditRule.RR-07-02` 连续解释疲劳：连续 3 段均以因果解释为主，标记高风险。
- [ ] `AuditRule.RR-07-04` 场景不足：1500 字以上正文少于 2 个现实场景，标记中风险。
- [ ] `AuditRule.RR-07-05` 人物语言不足：现实题全文没有人物语言或交流片段，标记中风险。
- [ ] `AuditRule.RR-07-06` 长句疲劳：超过 60 字句子多于 5 句，或超过 80 字句子多于 2 句，标记中风险。
- [ ] `AuditRule.RR-07-07` 段落机械化：70% 以上段落长度高度接近、大量一句一段或每节同构，标记中风险。
- [ ] `AuditRule.RR-07-09` 抽象名词堆积：连续 150 字内出现 6 个以上抽象概念，标记高风险。
- [ ] `AuditRule.RR-07-10` 结尾过载：结尾 20% 篇幅仍在新增机制、变量或理论，标记高风险。

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
