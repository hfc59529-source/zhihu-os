# 截图文章 Traceability / Outcome Linking 记录

日期：2026-08-02

数据来源：用户提供的知乎创作中心截图。

执行边界：

- 不重抓文章。
- 不重新建立样本。
- 不补造 Production Card、QA、审计或发布记录。
- 只把截图中的平台结果与本地生产链路做可追溯关联。

## 1. 截图文章与 Production ID 对照

| 序号 | 截图标题 | Production ID | 匹配证据 | Trace 状态 |
|---:|---|---|---|---|
| 1 | 提拔你当了部门负责人，第一件事该干啥？ | ZH-20260802-001 | `data/Topic_Pool.md` 与 `productions/ZH-20260802-001/Card-v1.md` 标题一致 | PARTIAL |
| 2 | 职场中怎么改掉弱者气息？ | ZH-20260801-001 | `data/production_ledger.md` 与 `productions/ZH-20260801-001/Card-v1.md` 标题一致 | COMPLETE |
| 3 | 为什么老板明知你摸鱼却不拆穿？ | ZH-20260731-unknown_mofish | 仅找到 `draft_mofish.md` 与 `reports/review_ZH-20260731-unknown_mofish_v1.md`；未找到正式 Production ID | BROKEN |
| 4 | 领导不声不响把你手里的任务拿走后，过了几个月，发现别人干不了，想还给你，你会怎么做呢？ | ZH-20260801-003 | `data/production_ledger.md` 与 `productions/ZH-20260801-003/Card-v1.md` 标题一致 | COMPLETE |
| 5 | 领导布置任务故意模糊责任界限，作为底层员工，如何在谁都不得罪的前提下，保护好自己？ | zhihu-20260729-fuzzy-responsibility-boundary-001 | `runtime/logs/production_runs.jsonl` 与 `reports/production_20260729_fuzzy_responsibility_boundary_card.txt` 标题一致 | LEGACY_RUN |
| 6 | 为什么工作中，很多高层领导明知道某位中层领导缺乏管理能力，但还是提拔了他当中层？ | zhihu-20260729-middle-manager-promotion-001 | `runtime/logs/production_runs.jsonl` 与 `reports/production_20260729_middle_manager_promotion_card.txt` 标题一致 | LEGACY_RUN |
| 7 | 公司高层明明不行，大老板为什么还不裁掉他们？ | zhihu-20260729-senior-leader-not-fired-001 | `runtime/logs/production_runs.jsonl` 与 `reports/production_20260729_senior_leader_not_fired_card.txt` 标题一致 | LEGACY_RUN |

## 2. 当前平台数据补录

已同步追加到 `runtime/logs/publish_results.csv`，本表保留人工可读口径。

| Production ID | 平台状态 | 阅读 | 赞同 | 评论 | 收藏 | 喜欢 | 发布时间显示 | 备注 |
|---|---|---:|---:|---:|---:|---:|---|---|
| ZH-20260802-001 | 已发布 | 13 | 1 | 0 | 0 | 0 | 发布于 8 小时前 | 未显示收益 |
| ZH-20260801-001 | 已发布 / 被折叠 | 6 | 0 | 0 | 0 | 0 | 发布于 23 小时前 | 截图显示“被折叠” |
| ZH-20260731-unknown_mofish | 已发布 | 5 | 0 | 0 | 0 | 0 | 发布于 07-31 | 未找到 Production ID |
| ZH-20260801-003 | 已发布 | 24 | 0 | 0 | 0 | 0 | 发布于 07-31 | 未显示收益 |
| zhihu-20260729-fuzzy-responsibility-boundary-001 | 已发布 | 60 | 1 | 0 | 0 | 0 | 发布于 07-29 | 2026-07-31 旧抓取为 59 阅读 / 4 盐粒 |
| zhihu-20260729-middle-manager-promotion-001 | 已发布 | 20 | 0 | 0 | 0 | 0 | 发布于 07-29 | 2026-07-31 旧抓取为 19 阅读 / 0 盐粒 |
| zhihu-20260729-senior-leader-not-fired-001 | 已发布 | 223 | 4 | 0 | 2 | 0 | 发布于 07-29 | 2026-07-31 旧抓取为 164 阅读 / 9 盐粒 |

## 3. 生产链材料索引

| Production ID | Production Card | 正文 / 发布稿 | QA | 审计 / 复盘 |
|---|---|---|---|---|
| ZH-20260802-001 | `productions/ZH-20260802-001/Card-v1.md` | `productions/ZH-20260802-001/Draft-v1.md` | 未找到正式 QA | 未找到正式审计 |
| ZH-20260801-001 | `productions/ZH-20260801-001/Card-v1.md` | `productions/ZH-20260801-001/Article-v1.md` | `productions/ZH-20260801-001/SemanticReview-v1.md` | `productions/ZH-20260801-001/Review-v1.md` |
| ZH-20260731-unknown_mofish | 未找到 | `draft_mofish.md` | 未找到 | `reports/review_ZH-20260731-unknown_mofish_v1.md` |
| ZH-20260801-003 | `productions/ZH-20260801-003/Card-v1.md` | `productions/ZH-20260801-003/Release-v1.md` | `productions/ZH-20260801-003/Final_Validation.md` | `productions/ZH-20260801-003/Audit_Report.md` / `productions/ZH-20260801-003/Comparison_Report.md` |
| zhihu-20260729-fuzzy-responsibility-boundary-001 | `reports/production_20260729_fuzzy_responsibility_boundary_card.txt` | 未找到对应正文文件 | 未找到 | `runtime/logs/production_runs.jsonl` 记录 `CARD_PASS` |
| zhihu-20260729-middle-manager-promotion-001 | `reports/production_20260729_middle_manager_promotion_card.txt` | 未找到对应正文文件 | `reports/production_20260729_middle_manager_promotion_parameter_audit.txt` | `runtime/logs/production_runs.jsonl` 记录 `PUBLISHED` |
| zhihu-20260729-senior-leader-not-fired-001 | `reports/production_20260729_senior_leader_not_fired_card.txt` / `reports/production_20260731_senior_leader_not_fired_card_v2.txt` | 未找到对应正文文件 | 未找到 | `runtime/logs/production_runs.jsonl` 记录 `PUBLISHED` |

## 4. 失败层归因初判

归因等级说明：

- HIGH：有直接证据。
- MEDIUM：有链路证据，但平台因果仍需后续数据验证。
- LOW：仅能排除或提示方向。

| Production ID | 选题层 | Question Parsing | 核心判断 | 结构调用 | 表达 | 平台折叠或分发 | 当前判定 |
|---|---|---|---|---|---|---|---|
| ZH-20260802-001 | LOW：题目明确且有 Top3/Topic Pool 记录 | LOW：Card 对“第一件事”改写为“先校准”，无明显偏题证据 | LOW：核心判断清楚 | LOW：ACTIVE-TS02 与解决题匹配 | LOW：正文可读，未见正式 QA | MEDIUM：8 小时阅读 13，样本仍早 | 暂不判定失败层，先观察 24h |
| ZH-20260801-001 | LOW：题目为宽泛成长题，非强情境题 | LOW：Card 直接回应“怎么改掉” | LOW：三信号判断清楚 | LOW：ACTIVE-TS01 匹配机制型回答 | LOW：SemanticReview PASS | HIGH：截图显示“被折叠”且阅读 6 | 首要失败点在平台折叠/分发；不优先归因生产链 |
| ZH-20260731-unknown_mofish | UNKNOWN：无 Production Card，无法回溯选题目标 | UNKNOWN：无问题解析记录 | UNKNOWN：正文有判断，但无卡片约束 | UNKNOWN：无结构调用记录 | LOW：正文存在但未审核 | MEDIUM：阅读 5，未显示折叠 | 首要问题是 Trace 断裂；不能可靠归因 |
| ZH-20260801-003 | LOW：题目情境明确 | LOW：Card 准确解析为责任边界 / 风险回流 | LOW：Final Validation PASS | LOW：ACTIVE-TS02 匹配解决题 | LOW：Audit Issue 已 Patch 并通过 | MEDIUM：07-31 至截图阅读 24，分发弱但未见折叠 | 更像分发弱或选题热度不足，生产链暂无直接失败证据 |
| zhihu-20260729-fuzzy-responsibility-boundary-001 | LOW：选题来自 2026-07-29 推荐候选，情境明确 | LOW：Card 聚焦责任界限保护，未见偏题证据 | LOW：核心变量为责任边界保护 | MEDIUM：旧结构 ACTIVE-01，缺新式结构审计 | UNKNOWN：未找到正文文件，无法判断表达 | MEDIUM：07-31 到截图仅 59 -> 60 阅读 | 分发增长停滞；正文表达层证据不足 |
| zhihu-20260729-middle-manager-promotion-001 | LOW：选题池关注/浏览较高 | LOW：Card 聚焦组织可控性，匹配问题 | LOW：核心变量为组织可控性 | MEDIUM：旧结构 ACTIVE-01，缺新式结构审计 | UNKNOWN：未找到正文文件，无法判断表达 | MEDIUM：07-31 到截图仅 19 -> 20 阅读 | 结果弱，但生产链缺正文/QA，不能可靠归因 |
| zhihu-20260729-senior-leader-not-fired-001 | LOW：选题池强适配，且旧抓取已有收益 | LOW：Card 聚焦组织风险押注，匹配问题 | LOW：核心变量为组织风险押注 | MEDIUM：旧结构 ACTIVE-01，缺新式结构审计 | UNKNOWN：未找到正文文件，无法判断表达 | LOW：阅读 164 -> 223，收藏 2，赞同 4 | 相对本批表现最好，暂不归入失败样本 |

## 5. 闭环结论

1. 本轮不是样本缺失，而是 Outcome 没有稳定挂回 Production。
2. `ZH-20260801-001` 和 `ZH-20260801-003` 已能完成结果到生产链的回溯。
3. `ZH-20260802-001` 已有 Card 和 Draft，但缺 QA / 审计 / Release 链路记录，属于发布后观察前的 Trace Partial。
4. “为什么老板明知你摸鱼却不拆穿？”没有正式 Production ID，是当前闭环最大断点；应保留为历史未知生产，不补造 ID。
5. 截图中唯一直接平台异常证据是 `ZH-20260801-001` 被折叠，因此该篇先归入“平台折叠或分发”层，而不是优先改生产参数。
6. 2026-07-29 三篇属于旧运行日志体系，能追到 run_id 和 Production Card，但大多缺正文、QA、审计与 Review 文件，Trace 状态应标 `LEGACY_RUN`，不能和新式 `ZH-...` 生产闭环混同。

## 6. 后续记录动作

建议后续每次发布后固定记录：

- Production ID。
- 知乎问题链接 / 回答链接。
- 发布时间。
- 24h / 72h / 7d 阅读、赞同、评论、收藏、喜欢、收益。
- 是否被折叠。
- Review 文件路径。

这样才能把“生产链”和“平台结果”稳定接起来。
