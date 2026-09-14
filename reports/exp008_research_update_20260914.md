# EXP008 Research Update｜2026-09-14

Status：RESEARCH LAYER UPDATE / NO ACTIVE RULE CHANGE

Sources：

- `research/experiments/EXP008.md`
- `reports/daily_review_20260910_zhihu_capture_recap.md`
- `reports/revenue_attribution_audit_20260910_first_team_lead.md`
- `reports/reactivation_timeseries_20260910_laoshiren.md`
- `reports/exp008_challenge_case_leadership_pairwise_20260910.md`
- `reports/daily_review_20260914_zhihu_capture_recap.md`
- `data/raw_exports/zhihu_knowledge_income_detail_20260914_recent30_browser.csv`

## 0. Boundary

2026-09-14 数据不修改 ACTIVE Production Rule，不升级正文协议，不把异常样本直接写成生产规则。

继续遵守 2026-09-10 锁定链路：

```text
Observation
-> Case
-> Hypothesis
-> Evidence
-> Validation
-> Rule
```

本轮只更新三个既有 Case，并新增一个 Question Cluster Observation。所有新增判断停留在 Research Layer。

## 1. Existing Case Updates

### Case 1：第一次带团队

```text
Title：第一次带团队，总感觉下属不听话怎么办？
Article ID：answer_2079600004604354925
Case：Revenue Attribution Measurement
Priority：P0
```

| 时间 | 内容管理阅读 | 收益表本期阅读 | 本期收益 | 累计收益 |
|---|---:|---:|---:|---:|
| 2026-09-10 | 103 | 57 | 73 | 73 |
| 2026-09-14 | 112 | 70 | 73 | 73 |
| Delta | +9 | +13 | +0 | +0 |

Update：

```text
OBSERVED：新增阅读出现，但未产生新增盐粒。
SUPPORTED：2026-09-10 的 Revenue Attribution Audit 必要性增强。
NOT PROVEN：该样本具有稳定高 RPM。
```

Interpretation：

9/10 不能把 `57 阅读 / 73 盐粒` 简化为稳定 RPM；9/14 进一步说明收益并非随着后续阅读均匀线性增长。当前更合理的问题是：

```text
知乎致知收益是否按所有“本期阅读”均匀产生？
```

Gate Status：

```text
CASE_OPEN
Priority：P0
Gate：Measurement Gate unresolved
Audience Composition：Candidate Variable only
```

在排除 Measurement / Attribution 口径错位之前，不建立 High Revenue Density Rule，不把 Audience Composition 写成解释变量。

### Case 2：老实人

```text
Title：体制内，为什么领导一眼就能看出你是老实人？
Article ID：answer_2073162526121107666
Case：Reactivation / Long-tail Persistence
Priority：P1
```

| 时间 | 窗口 | 窗口阅读 | 窗口收益 | 累计阅读 | 累计收益 |
|---|---|---:|---:|---:|---:|
| 2026-09-10 | 近 7 天 | 6673 | 710 | 20911 | 1483 |
| 2026-09-14 | 近 30 天 | 22843 | 1644 | 22843 | 1644 |

Update：

```text
SUPPORTED：该样本不是单次爆发后自然归零。
SUPPORTED：存在 Reactivation 后的 Long-tail Persistence。
OPEN：触发入口、分发来源、受众构成仍未知。
```

EXP008 当前 Distribution Model 得到进一步支持：

```text
Question Context
-> Entry
-> Initial Distribution
-> Consumption / Engagement
-> Further Distribution
-> Reactivation
-> Long-tail Persistence
```

Boundary：

不能把老实人的表现直接解释为某个正文变量造成。当前只确认生命周期现象，不确认触发机制。

### Case 3：领导能力 Challenge Pair

```text
New：如何判断一个人是否有领导能力？
Article ID：answer_2079612017883856957
Old：怎么看一个人有没有领导力？
Article ID：answer_2072695242105660190
Case：Challenge Pair / Pairwise Difference
Priority：P2
```

| 样本 | 2026-09-10 阅读 | 2026-09-14 阅读 | 赞同 | 收藏 | 收益 |
|---|---:|---:|---:|---:|---:|
| 旧答 | 375 | 375 | 2 | 0 | UNKNOWN |
| 新答 | 806 | 981 | 9 | 12 | 87 |

Pairwise Signal：

```text
2026-09-10：806 / 375 = 2.15x
2026-09-14：981 / 375 = 2.62x
```

Update：

```text
SUPPORTED：Challenge Signal 增强。
SUPPORTED：收藏从旧答 0 到新答 12，Costly Signal 增强。
NOT PROVEN：新解释框架导致 2.62x 播放。
```

Case Status：

```text
EXP008_STRONG_CONTROL_CANDIDATE
First result：PASS
Text difference：PARTIAL
```

仍需补旧答正文、发布时问题状态、旧答收益/收藏口径，才能进入更强的 pairwise validation。

## 2. New Observation：Leadership / Organizational Judgment Cluster

Observation Name：

```text
Leadership / Organizational Judgment Cluster
领导与组织判断需求簇
```

Definition v0：

读者需求不是泛泛的“职场”，而是围绕组织权力、人际判断、上下级关系和晋升筛选展开：

```text
领导怎么看人？
谁能当领导？
为什么升不上去？
什么人会成为心腹？
为什么领导留不住人？
谁会被提拔？
```

Keyword Coding v0：

```text
领导 / 心腹 / 提拔 / 晋升 / 中层 / 经理 / 总监 / 老板 / 管理 /
职场 / 下属 / 上级 / 部门 / 人才 / 骨干 / 老实人 / 组织 / 权力
```

2026-09-14 最近 30 天收益明细：

| 口径 | 全部 | Cluster | Cluster Share |
|---|---:|---:|---:|
| 内容数 | 62 | 40 | 64.52% |
| 本期阅读 | 54454 | 49451 | 90.81% |
| 本期收益 | 6466 | 6056 | 93.66% |
| 收益 Top 8 命中 | 8 | 8 | 100.00% |

Top Evidence：

| 内容 | 发布时间 | 本期阅读 | 本期收益 |
|---|---:|---:|---:|
| 什么性格的人适合当领导？ | 2026-08-18 | 7615 | 1774 |
| 体制内，为什么领导一眼就能看出你是老实人？ | 2026-08-18 | 22843 | 1644 |
| 为什么很多人，做到经理或总监，就再也上不去了？ | 2026-07-22 | 5635 | 1040 |
| 什么事情是你当了老板才知道的？ | 2026-06-24 | 2236 | 442 |
| 为什么有的领导身边能吸引很多人才，而有的领导却留不住核心骨干？ | 2026-08-17 | 1682 | 189 |
| 为什么领导的心腹很少有异性？ | 2026-08-25 | 1253 | 100 |
| 既为心腹，为什么反而会被领导批得最多、最狠？ | 2026-08-23 | 584 | 99 |
| 为什么职场上会出现提拔一批，躺平一批？ | 2026-08-18 | 1353 | 92 |

Hypothesis v0：

```text
某类 Question Context 本身可能具有更强的持续分发能力：
领导 / 识人 / 晋升 / 权力关系 / 组织关系。
```

Boundary：

这不是生产规则，只是 Question Context 层 Observation。当前不能推出：

```text
以后都写领导题。
该簇必然高收益。
某个正文结构导致该簇放量。
```

Next Validation：

1. 给 2026-08-16..2026-09-14 的 62 条内容做人工复核标签，避免关键词误分。
2. 与非 Cluster 内容比较收益/阅读中位数、Top 占比、发布时间分布。
3. 把 `什么性格的人适合当领导？` 与 `老实人` 建立双样本 Reactivation 对照。
4. 回查 8/18 同日发布内容是否共享相同问题池、入口、初始分发或二次分发机制。

## 3. Updated Research Priority

```text
P0  Revenue Attribution Measurement
    Case：第一次带团队
    Reason：新增阅读未新增盐粒，Measurement Gate 继续卡住 Monetization Model。

P1  Question Cluster
    Case：Leadership / Organizational Judgment Cluster
    Reason：最近30天收益 93.66% 集中于领导/组织判断需求簇，值得正式验证。

P1  Reactivation
    Case：什么性格适合当领导 + 老实人
    Reason：单 Case 已升级为双样本比较线索，重点研究 Question Context 与 Long-tail Persistence。

P2  Challenge Pair
    Case：领导能力新旧回答
    Reason：2.15x -> 2.62x，信号增强，但旧答正文缺失、平台环境不同，不能进因果结论。
```

## 4. Research Tree After 2026-09-14

```text
                    Distribution
                         |
          +--------------+--------------+
          |              |              |
   Question Context     Entry      Content Treatment
          |
          v
   Question Cluster
          |
          v
领导 / 识人 / 晋升 / 权力关系 / 组织关系
          |
          v
 Initial Distribution
          |
          v
 Further Distribution
          |
     +----+----+
     |         |
    Die    Reactivation
               |
               v
        Long-tail Persistence
```

Monetization 单独保留：

```text
Monetization Model
        |
        v
Revenue Attribution
        |
第一次带团队
        |
Measurement Gate
```

## 5. Final Judgment

2026-09-14 的增量不是“多了 62 条数据”，而是系统第一次同时看到四个层级：

```text
Question Cluster
-> Distribution Lifecycle
-> Content Treatment Difference
-> Monetization Measurement Anomaly
```

当前全部停留在 Research Layer，不进入 ACTIVE Production Rule。
