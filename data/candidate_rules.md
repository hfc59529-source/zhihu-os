# Candidate Rules

用途：记录 Blind Review 后形成的候选规律，供后续生产参考。

边界：本文件不属于 ACTIVE Parameter，不修改 Prompt，不修改生产协议，不修改治理原则，不建立 Observation。

## CAND-20260804-ORG-01｜组织题首屏认知升级

状态：CANDIDATE

证据来源：

- 2026-07-29 三篇组织题 Blind Review
- `data/l1_sample_list.csv` L1 样本对照
- `reports/historical_baseline_report.md` Historical Baseline

样本事实：

| Production ID | article_id | 标题摘要 | 阅读 | 赞同 | 收藏 | 对照位置 |
|---|---|---|---:|---:|---:|---|
| zhihu-20260729-middle-manager-promotion-001 | answer_2065829100695113964 | 明知中层缺乏管理能力，为什么还提拔 | 20 | 0 | 0 | 同题材低表现 |
| zhihu-20260729-fuzzy-responsibility-boundary-001 | answer_2065858842207032462 | 领导故意模糊责任界限，如何处理 | 61 | 1 | 0 | 同题材中间样本 |
| zhihu-20260729-senior-leader-not-fired-001 | answer_2065823788911048364 | 高层明明不行，大老板为什么不裁 | 242 | 4 | 2 | 同题材相对高表现 |

Candidate 01：

在本次三篇组织题样本中，首屏先完成“能力问题→风险问题”认知升级、覆盖面更广的问题，获得了更好的初始阅读表现。

Candidate 02：

首屏优先完成：

读者原理解
↓
更高层判断
↓
告诉读者本文真正解释什么

说明：这里记录的是首屏任务，不记录固定句式。

Candidate 03：

正文优先使用：

现象
↓
为什么暂时不处理
↓
不处理保护了什么
↓
什么情况下会处理
↓
普通人如何判断

适用范围：

- 职场组织题
- 老板视角题
- 高层任免题
- 明显不合理现象的解释型回答

使用限制：

- 只可作为下一篇 Production Card 的参考信息。
- 不作为 ACTIVE 参数触发。
- 不作为固定句式套用。
- 不回写 Prompt、生产协议或治理原则。

下一次验证：

- 后续同类新文章按 T24 / T72 / T7D 采集结果。
- 只有新文章验证后，才可讨论是否进入 Observation 或参数治理。
