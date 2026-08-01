# Production Ledger

**生产闭环与发布闭环已分离**：本表的"状态"只反映生产链路（Draft → Audit → Decision → Patch → Final Validation → Release）；发布相关状态见新增的 **Release Status** 列，以及独立的 [Publish_Queue.md](Publish_Queue.md)。Release 完成 ≠ 已经发布。

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

**Release Status 取值**：Ready（Release-v1 已生成，未进队列）/ Queued（已进 Publish_Queue）/ Draft Box（已写入知乎草稿箱）/ Published（已正式发布）

**Audit Result 统计口径**（供 ZH-MILESTONE-010 使用）：当前 7 篇纳入新流程（002-008），Clean Pass 3 篇（43%），Issue 4 篇（57%，全部 4 篇均已 Revise/Approve 通过），Final Validation 通过率 100%（7/7），Patch 后回退 0，误判 Issue 0。**观察更新**：006、007 出现"结尾分点后压缩重述"重复模式，008 未复现（结尾总结句为新抽象，非换词重复），已记入 [Milestone_Observations.md](Milestone_Observations.md) Observation-01，暂不构成系统性模式，继续观察至 010。
