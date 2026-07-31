# L0 内容资产总账

本目录只保存知乎内容资产索引，不做正文分析、变量判断或深度复盘。

## 唯一产出

`l0_content_assets.csv`

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
| evidence_level | 证据等级：RAW/HYPOTHESIS/EXPERIENCE/ACTIVE |
| status | 当前状态，如已发布/草稿/删除/未知 |
| sample_level | 当前层级，L0/L1/L2/L3；L0试采默认L0 |
| upgrade_reason | 升级原因；L0默认留空 |
| source | 数据来源 |
| collected_at | 采集时间 |
| notes | 采集缺口或异常说明 |

## L0边界

全量采集默认仅建立内容资产索引；正文、评论、同题高赞等高成本数据，必须由L1/L2/L3升级流程触发，不允许自动采集。

## 历史回填执行规则

04内容资产库是唯一总表，不再另建历史回填总表。历史数据按50篇一批增量回填，先补基础结果字段，再由脚本自动计算千阅读收益、结果分层和代表样本标记。题型、结构、变量、首屏、机制无法判断时统一写`UNKNOWN`，不阻塞分层和复盘。

证据升级路径固定为：

`RAW -> HYPOTHESIS -> EXPERIENCE -> ACTIVE`

历史样本只能先进入05.5验证库；只有经过新文章再次验证并满足证据门槛后，才能升级为ACTIVE。
