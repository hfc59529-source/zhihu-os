# 知乎系统研发日志

## 系统研究目标

[Research Objective](RESEARCH_OBJECTIVE.md) 定义Question Value、Distribution、Monetization、Persistence及贯穿全程的Epistemology / Validation。其层级高于单个实验；研究反馈生产仍须验证、人工审核与限定推广。

## 研发原则

**任何系统升级，都必须先提出假设，再设计控制变量实验，最后依据内部观察与平台数据共同决定是否进入 Runtime。**

## 实验记录

- [EXP001 - 正文生成接口表达层优化](experiments/EXP001.md)
- [EXP002 - 平台表达变量与 AI 识别相关性实验](experiments/EXP002.md)
- [EXP007 - Interaction Compiler：稳定冲突题的候选机制工具](experiments/EXP007.md)
- [EXP008 - Distribution Model：高收益回答的播放差异验证](experiments/EXP008.md)

## Case Studies

- [2026-09-03 Reactivation Case Study：老实人二次放量](../reports/reactivation_case_study_20260903_laoshiren.md)
- [2026-09-10 Reactivation Time Series：老实人二次分发续证](../reports/reactivation_timeseries_20260910_laoshiren.md)
- [2026-09-10 Revenue Attribution Audit：第一次带团队](../reports/revenue_attribution_audit_20260910_first_team_lead.md)
- [2026-09-10 Measurement Evidence：第一次带团队 73 盐粒归因](../reports/measurement_evidence_20260910_first_team_lead.md)
- [2026-09-10 EXP008 Challenge Case：领导能力 Pairwise Difference v0](../reports/exp008_challenge_case_leadership_pairwise_20260910.md)
- [2026-10-08 EXP008 恢复研究：Distribution / Monetization 续证与反例审计](../reports/exp008_research_update_20261008.md)

## 待审核接口提案

- [Topic Investment / Production Entry Gate V1](proposals/TOPIC_INVESTMENT_ENTRY_GATE_V1.md)：历史草案；已由2026-10-09最小Production Reference通道修复方案替代，不实施额外强制INVEST流程。

当前人工选题参考见 [Production References](../data/production_reference.md)：只使用人工接受、范围明确的数据Finding，正式机制Promotion独立。
