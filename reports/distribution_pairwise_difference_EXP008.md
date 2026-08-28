# EXP008 Pairwise Difference Report

Status：ANNOTATION_PENDING

本报告只做逐对差异，不做“10 个变量谁最重要”的总排序。分析顺序固定为：

```text
Question Context → Content Entry → Engagement → Distribution Interpretation
```

互动率属于 Post-distribution outcome / mediator，只能用来描述后置表现和提出反例，不得直接当作播放差异原因。

Text-derived annotation 必须先在 `data/distribution_text_annotations_blind.csv` 里盲标完成，再 join 回 matched-pair 数据。未盲标前，本报告不得填写内容处理变量差异。

若 blind 表中 `answer_text` 为空，相关样本不得填写 first sentence / first 100 chars 差异，只能保留为正文缺失。

## Priority Pairs

| Pair | Views Ratio | RPM Delta | Age Delta | Evidence Weight | Note |
|---|---:|---:|---:|---|---|
| PAIR-01 | 13.65x | 20.3% | 4d | HIGH | 极强播放差，发布时间接近 |
| PAIR-02 | 3.36x | 7.5% | 5d | HIGH | RPM 很接近 |
| PAIR-04 | 5.49x | 0.7% | 3d | CORE | 核心样本 |
| PAIR-05 | 2.19x | 8.3% | 1d | CORE | 很干净 |
| PAIR-09 | 3.23x | 9.9% | 0d | CORE | 同日发布 |
| PAIR-07 | 2.53x | 43.4% | 5d | LOW | RPM 差接近阈值上限 |
| PAIR-08 | 2.06x | 10.4% | 9d | MEDIUM_LOW | 日期差较大，降权 |

## Secondary Pairs

| Pair | Views Ratio | RPM Delta | Age Delta | Evidence Weight | Note |
|---|---:|---:|---:|---|---|
| PAIR-03 | 4.91x | 25.3% | 0d | SECONDARY | 同日发布，但 RPM 低于高收益主样本区间 |
| PAIR-06 | 3.55x | 12.1% | 1d | SECONDARY | 匹配干净，但低播放样本互动率更高，优先作为反例观察 |

## Initial Counter-Signal

当前未标注前，已有一个值得保留的反例信号：

```text
部分低播放样本的 like_rate / favorite_rate 高于对应高播放样本。
```

这削弱了“互动率高 → 必然继续放量”的单变量模型。第一轮应优先观察 Question Potential / Audience Scope / Competition，而不是先把互动率解释成原因。

## Pair Template

### PAIR-XX

A：
B：

Controlled Matching：

```text
RPM：
Exposure Age：
Views Ratio：
Evidence Weight：
```

Question Context：

```text
question_attention_level：
question_stage_at_publish：
existing_answer_count：
high_like_occupied：
audience_scope：
evidence_source：
```

Content Entry：

```text
conflict_strength：
emotional_charge：
first_sentence_judgment：
first_100_interest_conflict：
evidence_source：
```

Post Outcome / Mediator：

```text
like_rate：
comment_rate：
favorite_rate：
```

Distribution Interpretation：

```text
Primary difference：
Hypothesis supported：
Hypothesis weakened：
Unknown / confounder：
```
