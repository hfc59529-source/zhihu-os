# Production Ledger

**生产闭环与发布闭环已分离**：本表的"状态"只反映生产链路（Draft → Audit → Decision → Patch → Patch Validation → User Review → Release）；发布相关状态见新增的 **Release Status** 列，以及独立的 [Publish_Queue.md](Publish_Queue.md)。Release 完成 ≠ 已经发布。

**历史批次说明**：ZH-20260801-002 至 ZH-20260801-010 属于用户验收节点建立前的历史生产记录，保留原始事实，不补造 `USER_APPROVED`。从 ZH-20260801-011 起，必须严格执行：无 Issue 时 `AUDIT_PASS → READY_FOR_USER_REVIEW → USER_APPROVED → RELEASE_READY`；有 Patch 时 `PATCH_VALIDATED → READY_FOR_USER_REVIEW → USER_APPROVED → RELEASE_READY`。

| Production ID | 标题 | Top3 Source | Audit Result | Patch 数 | 生产状态 | Release Status | AI 创作提示 |
|---|---|---|---|---|---|---|---|
| ZH-20260801-001 | 职场中怎么改掉弱者气息？ | 未记录 | 未走本流程 | - | 已发布（旧流程，无 Release-v1 记录） | Published | 有 |
| ZH-20260801-002 | 人过五十岁，单位领导班子年轻化，自己逐步被边缘化，如何渡过漫长的职场尾声？ | 未记录 | Issue（1） | 1 | Final Validation PASSED，Release-v1 已生成 | Ready | 待观察 |
| ZH-20260801-003 | 领导不声不响把你手里的任务拿走后，过了几个月，发现别人干不了，想还给你，你会怎么做呢？ | Mixed | Issue（1） | 1 | Final Validation PASSED，Release-v1 已生成 | Ready | 待观察 |
| ZH-20260801-004 | 作为领导，你是如何识别那些高潜力员工的？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | Final Validation PASSED，Release-v1 已生成（Draft-v1 直接作为依据） | Ready | 待观察 |
| ZH-20260801-005 | 被领导边缘化后，无事可做，工资不变，怎么办？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | Final Validation PASSED，Release-v1 已生成（Draft-v1 直接作为依据） | Ready | 待观察 |
| ZH-20260801-006 | 工作中发生紧急情况，领导正在午睡，要不要叫醒他？ | 未记录（见 Top3_Context.md） | Issue（1） | 1 | Final Validation PASSED，Release-v1 已生成（Patch-v1 已应用） | Ready | 待观察 |
| ZH-20260801-007 | 如果领导很笨，又很有主见，我们该怎么办？ | 未记录（见 Top3_Context.md） | Issue（1） | 1 | Final Validation PASSED，Release-v1 已生成（Patch-v1 已应用） | Ready | 待观察 |
| ZH-20260801-008 | 频繁跳槽和长期坚守一家公司，哪个更有前途？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | Final Validation PASSED，Release-v1 已生成（Draft-v1 直接作为依据；未复现 006/007 模式） | Ready | 待观察 |
| ZH-20260801-009 | 真正工作厉害的人，有哪些明显特征？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | Final Validation PASSED，Release-v1 已生成（Draft-v1 直接作为依据；未复现 Observation-01） | Ready | 待观察 |
| ZH-20260801-010 | 如何让领导知道你干了很多工作？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | Final Validation PASSED，Release-v1 已生成（Draft-v1 直接作为依据；Observation-01 Closed，Observation-02 Open） | Ready | 待观察 |
| ZH-20260801-011 | 你们知道为什么好多公司推行绩效考核失败吗？ | 快速语境总结（见 Top3_Context.md，降权使用） | Card Issue | 1 | Card_Audit_Report.md 判定 Card-v1 把原问题导向管理框架，当前正文不进入 Patch Validation / User Review；待重做 Production Card | CARD_REWORK_REQUIRED | 待重做 Card |
| ZH-20260801-012 | 领导是如何看待不争不抢的员工？ | 快速语境总结（见 Top3_Context.md，降权使用） | 待人工审计 | 0 | QA 前修正完成；validate_reasoning.py PASS；阅读体验 risks: none；未进入人工审计 / Patch Validation / Release | READY_FOR_AUDIT | 待人工审计 |
| ZH-20260801-013 | 未来20年什么是优质资产？ | 历史资产弱参考（见 Top3_Context.md） | QA Pass | 0 | 真实链接已补；Card PASS；validate_reasoning.py PASS_WITH_WARNING；Release-v1 已生成；runtime manifest 存在既有 SHA mismatch 待系统维护 | Ready | 待观察 |

| ZH-20260804-001 | 为什么现在越来越多的企业二代们普遍不愿意接班？ | 实拍 Top3（见 Top3_Context.md，Possible Current Gap 候选 A/B） | 待人工审计 | 0 | Card-v1 / Draft-v1 已完成，按 ACTIVE-TS01 生成；未进入人工审计 / Patch Validation / Release | READY_FOR_AUDIT | 待人工审计 |

**Release Status 取值**：READY_FOR_USER_REVIEW（Audit PASS 或 Patch Validation PASS，待用户验收）/ RELEASE_READY（用户已验收，Release-v1 已生成或确认）/ Queued（已进 Publish_Queue）/ Draft Box（已写入知乎草稿箱）/ Published（已正式发布）

**Audit Result 统计口径（ZH-MILESTONE-010 触发）**：新流程样本（002-010）共 9 篇，Clean Pass 5 篇（56%），Issue 4 篇（44%，全部已 Revise/Approve 通过），Final Validation 通过率 100%（9/9），Patch 后回退 0，误判 Issue 0。

**Observation-01 结论**：006/007 出现"结尾分点后压缩重述"，008/009/010 连续三篇未复现，5 篇可比对样本中 2 YES / 3 NO，判定为局部巧合而非系统性模式，Production Card 施工规范无需修改，状态 Closed（详见 [Milestone_Observations.md](Milestone_Observations.md)）。

**里程碑触发**：010 完成，样本量达到 ZH-MILESTONE-010 复盘门槛（[系统治理原则.md](../docs/系统治理原则.md) 定义的四项：参数治理、流程复盘、Top3 采样效果分析、生产质量趋势分析）。ZH-MILESTONE-010 复盘已启动。
