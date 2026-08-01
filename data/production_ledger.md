# Production Ledger

**生产闭环与发布闭环已分离**：本表的"状态"只反映生产链路（Draft → Audit → Decision → Patch → Final Validation → Release）；发布相关状态见新增的 **Release Status** 列，以及独立的 [Publish_Queue.md](Publish_Queue.md)。Release 完成 ≠ 已经发布。

| Production ID | 标题 | Top3 Source | 生产状态 | Release Status | AI 创作提示 |
|---|---|---|---|---|---|
| ZH-20260801-001 | 职场中怎么改掉弱者气息？ | 未记录 | 已发布（旧流程，无 Release-v1 记录） | Published | 有 |
| ZH-20260801-002 | 人过五十岁，单位领导班子年轻化，自己逐步被边缘化，如何渡过漫长的职场尾声？ | 未记录 | Final Validation PASSED，Release-v1 已生成 | Ready | 待观察 |
| ZH-20260801-003 | 领导不声不响把你手里的任务拿走后，过了几个月，发现别人干不了，想还给你，你会怎么做呢？ | Mixed | Final Validation PASSED，Release-v1 已生成 | Ready | 待观察 |
| ZH-20260801-004 | 作为领导，你是如何识别那些高潜力员工的？ | 未记录（见 Top3_Context.md） | Claude Audit 完成，CLEAN（无 Issue），待 GPT Final Validation | - | 待观察 |

**Release Status 取值**：Ready（Release-v1 已生成，未进队列）/ Queued（已进 Publish_Queue）/ Draft Box（已写入知乎草稿箱）/ Published（已正式发布）
