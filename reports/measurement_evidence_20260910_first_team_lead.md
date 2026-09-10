# Measurement Evidence｜第一次带团队 73 盐粒归因

Status：INSUFFICIENT_EVIDENCE

Created：2026-09-10

## Question

```text
「第一次带团队」的 73 盐粒，到底对应哪一段阅读？
```

本文件只处理 Measurement，不解释内容机制。

## Source Pull

### revenue_observations.csv

| observation_time | revenue_window | period_reads | period_revenue | cumulative_reads | cumulative_revenue | source_file |
|---|---|---:|---:|---:|---:|---|
| 2026-09-10T15:48:00+03:00 | 2026-09-03..2026-09-09 | 57 | 73 | 98 | 73 | zhihu_knowledge_income_detail_20260910_recent7_browser |

### review_data_snapshots.csv

| collected_at | published_display | views | likes | comments | favorites | earnings_window | earnings_match_status |
|---|---|---:|---:|---:|---:|---|---|
| 2026-09-10T15:48:00+03:00 | 发布于 09-05 | 103 | 2 | 0 | 7 | 2026-09-03..2026-09-09 | TITLE_MATCH |

## Evidence Table

| Window | Views Start | Views End | Delta Views | Salt / Revenue | 口径状态 |
|---|---:|---:|---:|---:|---|
| 2026-09-05 -> 2026-09-06 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| 2026-09-06 -> 2026-09-07 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| 2026-09-07 -> 2026-09-08 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| 2026-09-08 -> 2026-09-09 | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| 2026-09-09 -> 2026-09-10 | UNKNOWN | 103 | UNKNOWN | UNKNOWN | UNKNOWN |
| 2026-09-03 -> 2026-09-09 | UNKNOWN | UNKNOWN | 57 | 73 | REVENUE_PERIOD_ONLY |
| publish -> 2026-09-10 15:48 | UNKNOWN | 103 | UNKNOWN | UNKNOWN | CONTENT_SNAPSHOT_ONLY |
| publish -> revenue cumulative | UNKNOWN | 98 | UNKNOWN | 73 | REVENUE_CUMULATIVE_ONLY |

## Direct Alignment

当前唯一能直接对齐的是同一观察时间点的三个累计/窗口读数：

```text
内容管理累计阅读：103
收益明细累计阅读：98
收益明细本期阅读：57
收益明细累计收益：73
收益明细本期收益：73
```

可确认：

```text
73 盐粒在收益明细中同时表现为本期收益和累计收益。
收益明细声称本期收益 73 对应本期阅读 57。
收益明细累计阅读为 98，不等于本期阅读 57。
内容管理累计阅读为 103，接近但不等于收益明细累计阅读 98。
```

不可确认：

```text
73 盐粒对应 2026-09-05 -> 2026-09-06 哪一天的阅读。
73 盐粒是否只由 57 本期阅读产生。
收益明细本期阅读 57 与内容管理累计阅读 103 的日级关系。
```

## Gate Result

```text
INSUFFICIENT_EVIDENCE
```

理由：

```text
现有快照粒度不足，无法判断 73 盐粒到底对应哪一段日级阅读。
当前不能确认 MEASUREMENT_MISMATCH_CONFIRMED。
当前也不能确认 MONETIZATION_ANOMALY_SUPPORTED。
```

## Next Collection Requirement

保持 `CASE_OPEN`。后续必须按固定时间点采集：

```text
1. 内容管理累计阅读、赞同、评论、收藏。
2. 致知计划内容收益明细的本期阅读、本期收益、累计阅读、累计收益。
3. 若页面支持，采集日级收益趋势或指定日期窗口。
4. 每次采集后只计算相邻快照 Delta Views 与 Delta Salt，不先解释机制。
```
