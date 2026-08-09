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

- [ ] 阅读体验
- [ ] 推进节奏
- [ ] 场景
- [ ] 表达自然
- [ ] 重复
- [ ] 收尾

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
