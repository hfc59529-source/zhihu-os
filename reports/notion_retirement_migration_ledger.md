# Notion Retirement Migration Ledger

日期：2026-08-09

状态：DRAFT

边界：

- 本台账只服务 Notion 退役迁移，不属于 Runtime 重构。
- 本轮不删除 Notion，不修改 Runtime Manifest，不发布 TRIAL / ACTIVE Runtime。
- Notion 中的 `ACTIVE`、`已验证`、`优先回答` 等状态只作为 Legacy Evidence，不继承为当前 Git Runtime 权威。
- 迁移前先判定 Schema 差集、记录覆盖差集和字段价值；只迁 `MIGRATE` / `MERGE`，其余只保留审计结论。

## Decision Key

| Decision | Meaning |
|---|---|
| MIGRATE | Git 没有，Notion 内容仍有效，需要迁入 Git |
| MERGE | Git 已有等价对象，但 Notion 有有效增量，需要合并 |
| SKIP | Git 已覆盖，或已有更权威版本，不迁 |
| ARCHIVE | 不进入当前生产链，但有历史证据价值 |
| DROP | 过期、重复、旧架构或非当前知乎 OS 资产，不迁 |

## Migration Ledger

| Asset | Notion Source | Git Equivalent | Record / Field Scope | Delta | Evidence Value | Decision | Target Git Object | Migration Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 内容资产基础字段 | 04｜知乎内容资产库 | `data/l0_content_assets.csv`; `data/review_data_snapshots.csv`; `data/production_article_map.csv` | 问题、问题链接、回答链接、平台、发布时间、阅读、赞同、收藏、评论、收益、千阅读收益 | 大部分 6-7 月已发布内容在 L0 / L1 / review snapshot 已覆盖；04 中部分链接缺失或为空 | 中 | SKIP / MERGE | `data/l0_content_assets.csv`; `data/review_data_snapshots.csv` | Pending | 先以 article_id / answer_url 为主键核对；标题近似不能自动覆盖 |
| 内容资产收益回填证据 | 04｜知乎内容资产库 / 收益快照相关页 | `reports/earnings_backfill_report.md`; `data/l0_content_assets.csv` | 2026-07-22 收益快照、已回填收益、冲突收益 | Git 已有独立回填报告：新增匹配 24 条，冲突 3 条，来源存在但 L0 未命中为 0 | 高 | SKIP | `reports/earnings_backfill_report.md` | Covered | 已有报告足以证明该批收益迁移历史，不重复迁 |
| 内容资产人工复盘字段 | 04｜知乎内容资产库 | `data/Milestone_Observations.md` 或后续 Archive 文件 | 复盘结论、异常记录、核心结论、数据结果、当前实验变量、首屏检查、失败原因分类 | Git L0 多数只保留基础事实，Notion 有人工解释和导入备注 | 中 | ARCHIVE / MERGE | `data/Milestone_Observations.md` 或 `research/notion_archive/` | Pending | 只迁有证据价值的复盘；不得升级成 Runtime 规则 |
| 内容资产旧商业字段 | 04｜知乎内容资产库 | 无当前等价对象 | 服务身份、旧服务身份、内容目的、引导动作、命中账本、体系分类、目标人群、用户类型、咖啡/商业主线字段 | 属于旧商业/咖啡体系或旧经营字段，当前知乎生产链不需要 | 低 | DROP | None | Pending | 除非单条能证明对知乎内容复盘有证据价值，否则不迁 |
| 2026-07 旧候选题事实 | 02｜知乎选题库 | `data/Topic_Pool.md`; `data/topic_candidates/` | 原问题、问题链接、来源、创建时间、最后更新、是否回答、状态、放弃原因 | Git 当前 Topic Pool 主要覆盖 2026-08-01 之后；02 有大量 2026-07 候选题未覆盖 | 中 | MIGRATE / ARCHIVE | `data/Topic_Pool.md` 或 `research/notion_archive/` | Pending | 只作为历史候选池和入口复盘，不直接进入当天生产 |
| 旧选题评分证据 | 02｜知乎选题库 | 无完整等价对象；部分理念已进入 `docs/知乎平台样本学习协议.md` | 评分证据V1、长期搜索价值V1、历史收益证据V1、认知优势匹配V1、推荐原因V1、评分置信度 | Notion 有旧评分过程；Git 没有逐题保留 | 中 | ARCHIVE | `research/notion_archive/` | Pending | 可保留为 Legacy Decision Evidence，不作为当前 DECISION 规则 |
| 旧选题生产决策字段 | 02｜知乎选题库 | 新架构 DECISION；`data/Topic_Pool.md` | 决策、主收益来源V1、内容机制V1、推荐主机制V1、推荐正文结构V1、选题总分、公式字段 | 属于旧生产逻辑和旧评分模型 | 低 / 中 | ARCHIVE / DROP | `research/notion_archive/` | Pending | 有证据解释价值则 Archive；公式输出和旧路由不迁入 Runtime |
| 结构03｜事件驱动机制型 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 反常识判断 -> 核心短概念 -> 真实事件 -> 机制拆解 -> 多事件验证 -> 规律升级 -> 回答原题 | Git 当前 ACTIVE-TS01 / TS02 未包含这个完整事件驱动结构；Notion 记录状态为 ACTIVE / 已验证 / 结构规律，但不能直接继承状态 | 高 | MERGE | 后续结构库源文件或结构演进审计；不是直接改 runtime | Pending | 强 MERGE 候选。需在 Git 源规则中重写为候选结构，再走 release_runtime.py |
| 结构00｜通用解释六段式 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 直接结论 -> 现实场景 -> 核心机制 -> 适用边界 -> 可执行动作 -> 规则收束 | Git 已有 TS01/TS02；Notion 兜底结构验证次数 0，验证等级为假设 | 低 | ARCHIVE / DROP | `research/notion_archive/` | Pending | 可作为旧兜底结构证据；不建议迁入当前 Runtime |
| 结构01｜反常识—选择权 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 反常识 -> 情绪伤口 -> 利益关系 -> 组织规则 -> 选择权 | Git TS01 已吸收“反常识、情绪入口、机制终点、选择权”等能力 | 中 | SKIP / ARCHIVE | `research/notion_archive/` | Pending | 不独立迁为 Runtime 结构；可保留旧结构演化证据 |
| 结构02｜约束—决策 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 错误认知 -> 真实约束 -> 关键变量 -> 决策方法 -> 风险边界 | Git TS02 已覆盖解决题/决策题场景、动作、边界、升级条件 | 中 | SKIP / ARCHIVE | `research/notion_archive/` | Pending | 不独立迁为 Runtime 结构；可用于判断 TS02 是否遗漏“关键变量/风险边界” |
| 单篇复盘证据 | 05｜知乎单篇复盘库 | `data/Milestone_Observations.md`; `data/review_data_snapshots.csv`; `reports/` | 复盘结论、因果判断、协议影响、下一轮动作、Top20 评论、前三高赞回答、窗口指标 | Schema 很大，混合事实、复盘、评论样本和旧协议影响判断 | 中 / 高 | ARCHIVE / selective MIGRATE | `data/Milestone_Observations.md` 或 `research/notion_archive/` | Pending | 只能迁有证据价值的复盘；不得按旧“协议影响”自动改规则 |
| 协议优先级治理 | 08｜知乎协议中心 | `docs/系统治理原则.md`; `docs/知乎OS权威归属表.md` | ACTIVE > verified evidence > review suggestions > raw data；review 不覆盖 production；低优先级不能覆盖高优先级 | Git 治理原则已覆盖大部分；Notion 有旧 L0-L7 表达 | 中 | SKIP / selective MERGE | `docs/系统治理原则.md` | Pending | 仅当发现 Git 缺明确治理句时再合并；不迁旧协议中心层级 |
| 旧协议模板/生产协议 | 08｜知乎协议中心 | `docs/`; `templates/`; `skills/` | Master Prompt、选题协议、生成协议、评分协议、复盘协议、评论协议 | 多数属于旧 Production Card / 旧 Skill 工作流 | 低 | DROP / ARCHIVE | `research/notion_archive/` | Pending | 不恢复 Notion 协议中心为生产入口 |
| Candidate v0.1｜内容变更分级与审批规则 | ACTIVE｜知乎规律库 | `docs/系统治理原则.md`; `data/Milestone_Observations.md`; `production_variable_library.md` | Level A 语言表达层、Level B 用户行为层、Level C 系统治理层；Level C 需人工审批 | Notion 状态为 REVIEW，证据样本数 1；Git 治理原则已明确“做信息隔离，不做对象膨胀”和参数/观察生命周期 | 中 | ARCHIVE / SKIP | `data/Milestone_Observations.md` 或 no-op | Pending | 不迁为 ACTIVE 规律；如保留，只作为治理观察证据 |
| ACTIVE 规律库行级资产 | ACTIVE｜知乎规律库 | `runtime/知乎ACTIVE规律快照.md`; `production_variable_library.md` | 当前 query 仅返回 1 条 REVIEW 候选，无正式 ACTIVE 行 | Notion 未发现可直接迁移的 ACTIVE 规律行 | 低 | SKIP | None | Checked | 暂不迁移；当前 Git runtime 规律快照仍是 DRAFT 过渡资产，后续由 release_runtime.py 控制发布 |

## Source Coverage Notes

### 04｜知乎内容资产库

已完成：Schema 差集、初步记录覆盖差集、字段价值分层。

结论：

- 基础内容事实大多已在 Git 数据层覆盖。
- Notion 独有价值集中在人工复盘、异常说明、旧收益导入备注、核心短概念和栏目/账号归属。
- 非知乎经营字段、咖啡/商业旧体系字段默认 DROP。

### 02｜知乎选题库

已完成：Schema 差集、初步记录覆盖差集、字段价值分层。

结论：

- 2026-07 旧候选题在 Git 当前 Topic Pool 中覆盖不足。
- 旧评分字段具有历史解释价值，但不能作为当前 DECISION Runtime 规则。
- 只迁题目事实和必要历史证据，不迁旧评分模型为生产权威。

### 06｜知乎结构库

已完成：行级差集。

行级结论：

| Notion Row | Git Coverage | Decision | Reason |
|---|---|---|---|
| 结构00｜通用解释六段式 | 部分被 TS01 / TS02 覆盖 | ARCHIVE / DROP | 兜底结构，验证次数 0，验证等级假设 |
| 结构01｜反常识—选择权 | 被 TS01 大量吸收 | SKIP / ARCHIVE | 旧结构演化证据，不独立入 Runtime |
| 结构02｜约束—决策 | 被 TS02 部分吸收 | SKIP / ARCHIVE | 可作为 TS02 对照，不独立入 Runtime |
| 结构03｜事件驱动机制型 | Git 缺完整同构结构 | MERGE | 强候选，但必须经 Git 源规则和 runtime release，不继承 Notion ACTIVE |

### ACTIVE｜知乎规律库

已完成：行级差集。

结论：

- 当前可查询行只有 `Candidate v0.1｜内容变更分级与审批规则`。
- 状态是 REVIEW，证据样本数 1，不具备迁入 ACTIVE Runtime 资格。
- Git 治理原则已覆盖其核心意图的大部分。
- 暂不迁移；最多作为治理观察证据归档。

## Remaining Work

1. 为 04 逐条确认需 MERGE 的人工复盘字段，避免把旧商业字段带回 Git。
2. 为 02 导出 2026-07 候选题事实清单，决定进入 `Topic_Pool.md` 历史段还是 `research/notion_archive/`。
3. 为 05 抽取高证据价值复盘记录，按 Observation 口径归档。
4. 对 08 做逐条治理句对照，只合并 Git 缺失且仍有效的治理规则。
5. 对 06 的结构03 开一条后续结构演进任务，不在本轮直接改 runtime。
