# L0 内容资产总账 / Historical Baseline

本目录保存知乎内容资产索引，并承担账号历史统计基线（Historical Baseline）职责。L0 不做正文分析、变量判断或深度复盘，但必须能回答“相对于账号历史分布，这篇表现处在什么位置”。

## L0职责

| 职责 | 说明 |
| --- | --- |
| 内容资产总账 | 记录每篇内容的稳定身份、平台结果、采集来源和数据完整度 |
| 历史统计基线 | 计算阅读、赞同、评论、收藏、收益等指标的分布、分位数和账号画像 |

L0 的判断边界是统计位置，不是内容归因。例如：L0 可以说“274 阅读处于历史 P90 附近”，不能说“因为某个变量导致 274 阅读”。

## 唯一产出

`l0_content_assets.csv`

派生报告：

- `reports/l0_asset_report.md`：L0 资产统计报告。
- `reports/historical_baseline_report.md`：账号历史基线与分布画像。

## 字段规则

| 字段 | 说明 |
| --- | --- |
| article_id | 稳定唯一ID；优先使用链接中的回答/内容ID，缺失时使用类型、标题和发布时间生成临时ID |
| title | 内容标题或首句标题 |
| content_type | 回答/想法/文章/视频/播客/专栏 |
| published_at | 发布时间；保留页面可见原文 |
| url | 内容链接；缺失时留空，不猜测 |
| views | 阅读/浏览/播放数；未知留空 |
| likes | 赞同数；未知留空 |
| comments | 评论数；未知留空 |
| favorites | 收藏数；未知留空 |
| earnings | 收益；未知留空，不用0代替 |
| earnings_per_1k_views | 千阅读收益；由收益/阅读*1000自动计算，缺少阅读或收益时留空 |
| historical_batch | 历史回填批次；每50篇一批，如HIST-01 |
| historical_source | 历史来源；默认沿用source |
| historical_completeness | 历史字段完整度，如结果完整/标签待补 |
| question_type | 题型；无法判断写UNKNOWN |
| structure_used | 使用结构；无法判断写UNKNOWN |
| primary_variable | 主变量；无法判断写UNKNOWN |
| first_screen_type | 首屏类型；无法判断写UNKNOWN |
| core_mechanism | 核心机制；无法判断写UNKNOWN |
| result_layer | 结果分层：A高收益，B高千阅读收益，C高阅读低收益，D低阅读低收益；可多层命中 |
| deep_review | 是否进入代表样本深度复盘；是/否 |
| historical_rule_status | 历史规律状态：未提取/候选规律/05.5验证中/已进入ACTIVE |
| evidence_level | 证据等级（对应 `production_variable_library.md` Parameter 生命周期）：RAW/CANDIDATE/REVIEW/ACTIVE |
| status | 当前状态，如已发布/草稿/删除/未知 |
| sample_level | 当前层级，L0/L1/L2/L3；L0试采默认L0 |
| upgrade_reason | 升级原因；L0默认留空 |
| source | 数据来源 |
| collected_at | 采集时间 |
| notes | 采集缺口或异常说明 |

## L0边界

全量采集默认仅建立内容资产索引；正文、评论、同题高赞等高成本数据，必须由L1/L2/L3升级流程触发，不允许自动采集。

## Baseline Profile

L0 必须周期性生成账号画像（Profile），用于后续复盘判断：

- 内容总数、回答/文章/想法比例。
- 阅读、赞同、评论、收藏、收益的 P50 / P75 / P90 / P95 / MAX。
- 阅读分布、收藏分布、收益分布。
- 收益覆盖率、折叠率（有折叠字段或快照证据时）。
- 最近生产样本相对历史分布的位置。

以后任何“高阅读 / 低阅读 / 高收藏 / 低收益”判断，必须优先引用 L0 Baseline，而不是凭感觉判断。

## 历史回填执行规则

04内容资产库是唯一总表，不再另建历史回填总表。历史数据按50篇一批增量回填，先补基础结果字段，再由脚本自动计算千阅读收益、结果分层和代表样本标记。题型、结构、变量、首屏、机制无法判断时统一写`UNKNOWN`，不阻塞分层和复盘。

证据升级路径固定为（与 `production_variable_library.md` Parameter 生命周期一致，RAW 对应尚未正式建档的原始证据，早于 DISCOVERED）：

`RAW -> CANDIDATE -> REVIEW -> ACTIVE`

历史样本只能先进入05.5验证库；只有经过新文章再次验证并满足证据门槛后，才能升级为ACTIVE。
