# 知乎本地执行快照清单

执行版本：ZH-RUNTIME-V2.1

状态：ACTIVE

发布日期：2026-07-28

## 当前执行文件

- 总调度：docs/知乎OS执行协议.md
- 权威归属：docs/知乎OS权威归属表.md
- 设计原则：docs/00-设计原则.md
- Compiler内核：docs/知乎OS Compiler V1.md
- Compiler数据流：docs/知乎OS Compiler Data Flow V1.md
- Writer输入包Schema：docs/Writer Input Package Schema V1.md
- 结构进化协议：docs/知乎OS Structure Evolution V1.md
- 平台样本学习：docs/知乎平台样本学习协议.md
- Production Card 生成：skills/Skill006_知乎生产卡生成器.md
- 历史资产检索：skills/Skill000_历史资产检索器.md
- Production Card 模板：templates/Production Card模板.md
- Failure Pattern 模板：templates/Failure Pattern模板.md
- Claude 正文 Prompt：templates/Claude正文生产Prompt.md
- 正文推理协议：docs/知乎正文推理协议 V1.0.md
- 正文 QA：skills/Skill007_正文QA协议.md
- 内容质量参数：runtime/知乎内容质量参数快照.md
- 内容变量参数库：production_variable_library.md
- 生产变量运行时快照：runtime/production_variable_snapshot.md
- ACTIVE 规律：runtime/知乎ACTIVE规律快照.md
- ACTIVE 结构：runtime/知乎结构库快照.md
- 账号画像：runtime/知乎账号画像快照.md

## 必检脚本

- scripts/validate_production_card.py
- scripts/validate_reasoning.py
- scripts/validate_runtime_consistency.py
- scripts/assemble_writer_input_package.py
- scripts/match_structure.py
- scripts/validate_obligation_coverage.py
- scripts/search_historical_assets.py

## 生效原则

只有本清单列出的文件可以决定正式生产。

未列入清单的历史文件、草稿文件、归档文件不得进入生产调用。

Notion 是管理权威；runtime MD 是 Codex 日常生产的执行权威。

Notion 内容修改不自动生效，只有完成快照发布并更新本清单版本后才进入生产链。

Claude 正文 Prompt 内置 Generation Constraint，用于限制正文模型无来源数字、新一级概念、自动三点论、重复升华和情绪标签。该约束只作用于正文生成，不改变 Production Card 字段、不新增生产流程、不影响复盘数据库。

知乎OS Compiler V1 是当前内容生产内核。现有 `Production Card` 在 Compiler V1 中解释为 `Production Card IR`。Compiler V1 试运行至少 10 篇真实知乎生产前，不重构 Notion 首页、不新建六套数据库、不批量迁移历史数据。

## 第二阶段学习闭环

知乎OS第二阶段采用三层数据源：

```text
L1｜平台样本：发现变量
↓
L2｜账号实验：验证变量
↓
L3｜ACTIVE变量：生产调用
```

平台样本负责从问题、高表现回答、评论区和失败样本中统计候选变量，所有证据统一回写 `production_variable_library.md` 的同一变量记录。

平台样本采集以职场为唯一主赛道，占比 70% 至 80%。组织管理和商业认知只作为职场内容的辅助样本来源，占比 20% 至 30%。心理学不得作为独立采集赛道，只能作为解释职场行为、组织关系或决策问题的辅助证据。

平台样本采集入口优先级：

1. 创作中心 -> 创作权益 -> 近期热点。
2. 创作中心 -> 等你来答 -> 推荐问题。
3. 创作中心 -> 问题搜索 -> 知乎热词 / 知乎热题 / 全网热点。
4. 创作中心 -> 等你来答 -> 邀请回答。
5. 知乎热榜 `/billboard` 或首页热榜 `/hot`，只做全站热度校验。
6. 知乎站内搜索职场、组织管理、商业认知关键词，只做垂直样本兜底。

入口必须按任务分流：创作中心近期热点、推荐问题和邀请回答主要用于选题候选；爆款变量训练必须优先使用知乎站内职场核心关键词高赞回答、全站热榜中可迁移问题和知乎热题中的高表现回答。推荐问题只说明账号匹配，不说明平台爆款。

爆款变量训练最低门槛：单题 Top1 回答赞同数建议不低于 300；低于 100 默认不得作为爆款训练样本。Top5 中至少 3 条回答赞同数达到 100 以上，或该题具备明显高收藏、高评论、高热度信号。

变量提取报告必须参数化：每个候选变量必须包含变量定义、生效机制、证据统计、证据等级、适用题型、触发条件、禁用边界、Production Card调用方式、Claude Prompt调用方式和升级建议。描述型报告不得进入参数库或Prompt升级。

Codex 负责执行采集、清洗、拆解、固定格式报告、参数草案和同步；GPT 负责规律质疑、参数体系设计、升级取舍和阶段性复盘。GPT 只在异常、升级、新机制发现或20至50篇阶段复盘时介入。

外部搜索结果不得作为知乎平台样本来源。

账号历史数据不再承担“发现规律”的主要职责，只承担“验证平台变量是否适合本账号”的职责。

日常生产仍只读取本清单列出的 ACTIVE 快照和唯一内容变量参数库。平台样本、评论拆解、失败样本和未验证候选变量不得直接进入 Production Card。

禁止新增“平台变量库”“账号变量库”或任何第二套参数体系。

内容变量参数库是长期总库；Production Card 不直接全量读取总库。每次正式生产必须先生成或刷新生产变量运行时快照，只把本题命中的变量投影给 Production Card。

## 复盘升级门槛

知乎复盘不再以单篇爆文直接升级规则。

规则升级必须经过：

```text
L1 平台样本变量统计
↓
写入 production_variable_library.md 同一变量记录
↓
L2 账号实验验证
↓
收益结果卡
↓
更新账号证据字段
↓
状态升级或废止
```

存量 216 篇文章的主要用途是账号验证，不再作为主要规律发现来源。

旧本账号闭环仍可用于验证已经提出的变量：

```text
L2 正文变量标注
↓
收益结果卡
↓
变量验证卡
↓
证据等级
↓
ACTIVE / Prompt 升级
```

变量验证卡的核心裁判指标是千阅读收益，其次是 7 天收益、30 天长尾收益和单篇总盐粒。

日常待生产问题默认采集有效高表现回答 Top5：Top1 至 Top3 深度分析，Top4 至 Top5 交叉验证；高竞争或分歧明显题可扩展到 Top8 至 Top10。只采问题不构成完整平台样本；未完成每题有效 Top5 回答正文读取的问题只能标记为 `QUESTION_ONLY`，不得进入变量提取、变量统计、参数升级、Production Card 升级或 Prompt 升级。Top5 原文和逐篇拆解不进入 Production Card，只有问题级聚合结论可以进入生产前分析。

同题高表现回答、Top20 评论和低表现回答用于统计平台候选变量；它们不进入本人行为结果统计，也不得未经账号验证直接升级 ACTIVE。

## 正式生产完成定义

收到知乎问题、知乎问题截图，“生成卡”“生产卡”“按截图生成卡”“继续”等明确卡片生产指令，或用户要求 Codex 自行去知乎采集、挑选、推荐今日可回答问题时，执行器自动进入日常生产卡模式。

生产入口分为两类：

- 用户输入型：用户发问题、截图或链接。
- 系统自采型：Codex 从知乎首页、创作中心推荐问题、邀请回答、问题搜索、创作榜单等入口采集候选并推荐一题。

两个入口只影响选题来源；题目选定后，后续 Production Card 主链完全一致。

日常生产卡模式必须连续执行：问题识别 → 选题准入 → 读取本清单 → 执行历史资产检索 → 读取本清单指定的 ACTIVE 结构、ACTIVE 规律、内容质量参数、内容变量参数库和账号画像 → 内容路由 → ACTIVE 规律回流调用 → 生成生产变量运行时快照 → 读取运行时快照中的命中变量 → 26 维质量参数总审计 → 生成 Production Card → 冻结 L1 生产卡 → 执行生产卡校验脚本 → 交付可复制 Claude版 Production Card → 写入本地运行日志。

L1 生产卡冻结规则：

- Production Card 必须写明题型、结构版本号、冻结证据清单、唯一主变量、核心机制、CR 目标和禁止后改项。
- Production Card 校验通过后，L2 正文生产只拥有执行权，不拥有选择权。
- L2 不得重选题型、替换结构、改变量、换证据、改 CR 或新增一级机制。
- 如果正文生产阶段发现卡片不成立，只能退回 L1 重做 Production Card，不得在 L2 生产时边写边改。

ACTIVE 规律回流调用只读取：

- runtime/知乎ACTIVE规律快照.md

内容变量筛选只读取：

- production_variable_library.md 中 `当前状态=ACTIVE` 且 `是否允许生产调用=是` 的变量

Production Card 变量调用只读取：

- runtime/production_variable_snapshot.md

读取范围：本题命中的变量。

`HYPOTHESIS` 只允许作为指定单变量实验或回溯验证调用，不得指导日常正文生产。`EXPERIENCE` 只允许在 Production Card 中标注为实验性调用，不得覆盖 ACTIVE 变量。`DEPRECATED` 禁止生产调用。

L2 正文变量矩阵、05 单篇复盘库和 05.5 规律验证库属于复盘系统，不得直接进入日常生产；只有验证结果回写到 `production_variable_library.md` 并达到调用权限后，才允许影响 Production Card。

Production Card 是日常生产默认交付对象。校验通过后不得自动交给 Claude 正文生产节点，除非用户明确要求“生产正文”“写回答”“调用正文节点”或“按完整链路生产”。

日常生产默认向用户交付题目识别、结构调用、26 维参数总审计、本题命中参数、未调用参数与原因、可复制 Production Card 和校验结果。
