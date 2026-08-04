# Production Ledger

**生产闭环与发布闭环已分离**：本表的"生产状态"只反映生产链路（Draft → Audit → Decision → Patch → Patch Validation → User Review → Release Artifact）；发布相关状态见 **Release Status** 列，以及独立的 [Publish_Queue.md](Publish_Queue.md)。Release Artifact 完成 ≠ 已经发布。

**历史批次说明**：ZH-20260801-002 至 ZH-20260801-010 属于用户验收节点建立前的历史生产记录，保留原始事实，不补造 `USER_APPROVED`。从 ZH-20260801-011 起，必须严格执行：无 Issue 时 `AUDIT_PASS → READY_FOR_USER_REVIEW → USER_APPROVED → RELEASE_READY`；有 Patch 时 `PATCH_VALIDATED → READY_FOR_USER_REVIEW → USER_APPROVED → RELEASE_READY`。

| Production ID | 标题 | Top3 Source | Audit Result | Patch 数 | 生产状态 | Release Status | AI 创作提示 |
|---|---|---|---|---|---|---|---|
| ZH-20260801-001 | 职场中怎么改掉弱者气息？ | 未记录 | 未走本流程 | - | LEGACY_COMPLETED（旧流程，已发布，无 Release-v1 记录） | PUBLISHED | 有 |
| ZH-20260801-002 | 人过五十岁，单位领导班子年轻化，自己逐步被边缘化，如何渡过漫长的职场尾声？ | 未记录 | Issue（1） | 1 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-003 | 领导不声不响把你手里的任务拿走后，过了几个月，发现别人干不了，想还给你，你会怎么做呢？ | Mixed | Issue（1） | 1 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-004 | 作为领导，你是如何识别那些高潜力员工的？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Draft-v1 直接作为依据） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-005 | 被领导边缘化后，无事可做，工资不变，怎么办？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Draft-v1 直接作为依据） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-006 | 工作中发生紧急情况，领导正在午睡，要不要叫醒他？ | 未记录（见 Top3_Context.md） | Issue（1） | 1 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Patch-v1 已应用） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-007 | 如果领导很笨，又很有主见，我们该怎么办？ | 未记录（见 Top3_Context.md） | Issue（1） | 1 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Patch-v1 已应用） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-008 | 频繁跳槽和长期坚守一家公司，哪个更有前途？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Draft-v1 直接作为依据；未复现 006/007 模式） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-009 | 真正工作厉害的人，有哪些明显特征？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Draft-v1 直接作为依据；未复现 Observation-01） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-010 | 如何让领导知道你干了很多工作？ | 未记录（见 Top3_Context.md） | Clean Pass | 0 | LEGACY_RELEASE_COMPLETED（Final Validation PASSED，Release-v1 已生成；Draft-v1 直接作为依据；Observation-01 Closed，Observation-02 Open） | LEGACY_RELEASE_READY | 待观察 |
| ZH-20260801-011 | 你们知道为什么好多公司推行绩效考核失败吗？ | 快速语境总结（见 Top3_Context.md，降权使用） | Card Issue | 1 | CARD_REWORK_REQUIRED（Card_Audit_Report.md 判定 Card-v1 把原问题导向管理框架，当前正文不进入 Patch Validation / User Review；待重做 Production Card） | NOT_ENTERED | 待重做 Card |
| ZH-20260801-012 | 领导是如何看待不争不抢的员工？ | 快速语境总结（见 Top3_Context.md，降权使用） | 待人工审计 | 0 | READY_FOR_AUDIT（QA 前修正完成；validate_reasoning.py PASS；阅读体验 risks: none；未进入人工审计 / Patch Validation / Release） | NOT_ENTERED | 待人工审计 |
| ZH-20260801-013 | 未来20年什么是优质资产？ | 历史资产弱参考（见 Top3_Context.md） | QA Pass | 0 | READY_FOR_USER_REVIEW（未找到 USER_APPROVED 记录；Release-v1 已提前生成，标记为 INVALID_PREMATURE_ARTIFACT；runtime manifest 存在既有 SHA mismatch 待系统维护） | NOT_ENTERED | 待用户验收 |
| ZH-20260804-002 | 如果你是老板，被十几位员工联名要求罢免掉他们的直接上司，不然全辞职，你会怎么办? | 实拍 Top3（见 Top3_Context.md，Possible Current Gap 候选 A 已采用） | 待人工审计 | 0 | READY_FOR_AUDIT（Card-v1 / Draft-v1 已完成，读者视角三字段已从选题包直接消费；未进入人工审计 / Patch Validation / Release） | NOT_ENTERED | 待人工审计 |
| ZH-20260804-001 | 为什么现在越来越多的企业二代们普遍不愿意接班？ | 实拍 Top3（见 Top3_Context.md，Possible Current Gap 候选 A/B） | Topic Rejected（见 Production_Decision.md；此前 Card / Draft / Patch / Final Validation 作为作废产物保留） | 1 | REJECTED（作者缺乏足够一手知识或证据形成独立核心判断；不进入 User Review / Release；返回 Topic Pool 选择下一题） | NOT_ENTERED | 题级决策，非系统问题 |

**Production Status 取值**：DRAFT_READY / READY_FOR_AUDIT / CARD_REWORK_REQUIRED / PATCH_REQUIRED / PATCH_VALIDATION_REQUIRED / READY_FOR_USER_REVIEW / USER_APPROVED / RELEASE_COMPLETED；历史兼容值：LEGACY_COMPLETED / LEGACY_RELEASE_COMPLETED。

**Release Status 取值**：NOT_ENTERED / RELEASE_READY / QUEUED / DRAFT_BOX / PUBLISHED；历史兼容值：LEGACY_RELEASE_READY。

**Audit Result 统计口径（ZH-MILESTONE-010 触发）**：Pre-User-Gate Audit Batch（002-010，用户验收门禁前审计批次）共 9 篇，Clean Pass 5 篇（56%），Issue 4 篇（44%，全部已 Revise/Approve 通过），Final Validation 通过率 100%（9/9），Patch 后回退 0，误判 Issue 0。本统计截至 Final Validation，不包含 User Review 与 Release Gate。

**Observation-01 结论**：006/007 出现"结尾分点后压缩重述"，008/009/010 连续三篇未复现，5 篇可比对样本中 2 YES / 3 NO，判定为局部巧合而非系统性模式，Production Card 施工规范无需修改，状态 Closed（详见 [Milestone_Observations.md](Milestone_Observations.md)）。

**里程碑触发**：010 完成，样本量达到 ZH-MILESTONE-010 复盘门槛（[系统治理原则.md](../docs/系统治理原则.md) 定义的四项：参数治理、流程复盘、Top3 采样效果分析、生产质量趋势分析）。ZH-MILESTONE-010 复盘已启动。
