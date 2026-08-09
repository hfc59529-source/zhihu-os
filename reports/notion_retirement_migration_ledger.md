# Notion Zhihu OS Retirement Migration Ledger

日期：2026-08-09

状态：RETIREMENT COMPLETE

范围：

- 退役目标是整个 Notion：最终不再把 Notion 作为系统资产、生产入口或长期数据源。
- 与当前 Git 仓库 `/Users/huangsheng/Documents/知乎系统` 发生迁移比对关系的，只有 Notion 中“知乎项目OS / 知乎系统”子树。
- 本台账只记录“Notion 知乎系统子树 -> 当前 Git 知乎系统”的迁移差集，不审计、不迁移其他 Notion 系统到本仓库。
- 本轮不删除 Notion，不删除“知乎项目OS / 知乎系统”子树，不修改 Runtime Manifest，不发布 TRIAL / ACTIVE Runtime。
- Notion 中的 `ACTIVE`、`已验证`、`优先回答` 等状态只作为 Legacy Evidence，不继承为当前 Git Runtime 权威。
- 迁移前先判定 Schema 差集、记录覆盖差集和字段价值；Retirement Gate 通过后，不再逐页考古 Notion。剩余未逐条审核资产默认视为 Historical Evidence，只有同时满足 Salvage Gate（Git 不存在 / Notion 关闭会永久丢失 / 未来有实际用途）才重新开启迁移候选。

Retirement Gate 结论：

1. 当前 Git 生产不依赖 Notion；README 与 `docs/知乎OS权威归属表.md` 已确认 Notion 退出 Production Authority Chain。
2. 当前未发现已知的、Notion 独有且关闭后会造成实际生产损失的资产。
3. 剩余 Pending / Not Started 项均不构成 Source of Truth、Production Authority 或 Runtime Dependency；只可能作为 Historical Evidence 在需要时可选归档。
4. Notion 不再作为当前知乎系统的 Source of Truth、Production Authority 或 Runtime Dependency。

本仓库唯一迁移根节点：

```text
Notion Workspace
└── 黄升决策操作系统
    └── ...
        └── 知乎项目OS / 知乎系统
            ├── 02｜知乎选题库
            ├── 04｜知乎内容资产库
            ├── 05｜知乎单篇复盘库
            ├── 06｜知乎结构库
            ├── 08｜知乎协议中心
            ├── ACTIVE｜知乎规律库
            └── 其他知乎OS直属资产
```

OUT OF SCOPE：

- 知乎项目OS / 知乎系统子树之外的 Notion 页面、数据库和项目，不进入当前 Git 仓库迁移台账。
- 咖啡系统、商业系统、供应链系统或其他 Notion 资产，即使它们在 04 内容资产库的历史脏数据字段里出现。
- 整个 Notion Workspace 的删除、整理、归档或重构，不由本台账执行；本台账只负责证明当前 Git 知乎系统是否已覆盖 Notion 知乎系统资产。

执行规则（Retirement Gate 通过前的分类口径）：

```text
知乎项目OS 内
↓
Git 已有 → SKIP
Git 没有 + 对知乎仍有价值 → MIGRATE / MERGE 候选
只有历史证据价值 → ARCHIVE 到 Git
旧架构 / 重复 / 垃圾 → DROP

知乎项目OS 外（相对当前 Git 仓库）
↓
OUT OF SCOPE
不读取
不比较
不迁移
不写入本仓库
```

## Decision Key

注：`MIGRATE` / `MERGE` 是退役审计过程中的候选分类，不代表 Retirement Gate 通过后仍存在执行任务。当前结论以主表 `Migration Status` 和 `Retirement Closeout` 为准。

| Decision | Meaning |
|---|---|
| MIGRATE | Git 没有，Notion 内容仍有效，退役前可列为迁移候选 |
| MERGE | Git 已有等价对象，但 Notion 有有效增量，退役前可列为合并候选 |
| SKIP | Git 已覆盖，或已有更权威版本，不迁 |
| ARCHIVE | 不进入当前生产链，但有历史证据价值 |
| DROP | 过期、重复、旧架构或非当前知乎 OS 资产，不迁 |

## Migration Ledger

| Asset | Notion Source | Git Equivalent | Record / Field Scope | Delta | Evidence Value | Decision | Target Git Object | Migration Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 内容资产基础字段 | 04｜知乎内容资产库 | `data/l0_content_assets.csv`; `data/review_data_snapshots.csv`; `data/production_article_map.csv` | 问题、问题链接、回答链接、平台、发布时间、阅读、赞同、收藏、评论、收益、千阅读收益 | 大部分 6-7 月已发布内容在 L0 / L1 / review snapshot 已覆盖；04 中部分链接缺失或为空 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical source evidence | Retirement Gate Closed / no migration blocker | 不再作为迁移阻断；若未来需要证明历史来源，再按 article_id / answer_url 做可选归档，标题近似不能自动覆盖 |
| 内容资产收益回填证据 | 04｜知乎内容资产库 / 收益快照相关页 | `reports/earnings_backfill_report.md`; `data/l0_content_assets.csv` | 2026-07-22 收益快照、已回填收益、冲突收益 | Git 已有独立回填报告：新增匹配 24 条，冲突 3 条，来源存在但 L0 未命中为 0 | 高 | SKIP | `reports/earnings_backfill_report.md` | Covered | 已有报告足以证明该批收益迁移历史，不重复迁 |
| 内容资产人工复盘字段 | 04｜知乎内容资产库 | `data/Milestone_Observations.md` 或后续 Archive 文件 | 复盘结论、异常记录、核心结论、数据结果、当前实验变量、首屏检查、失败原因分类 | Git L0 多数只保留基础事实；Notion 有人工解释和导入备注，但这些字段混合了事实、观察、解释、因果判断、实验变量和失败归因 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical review evidence | Retirement Gate Closed / no migration blocker | 不直接 MERGE。复盘结论、核心结论、当前实验变量、失败原因分类不得直接写入 L0、Parameter、Prompt 或 runtime；未来若重新使用，必须从 Git 内发起 Evidence Split / Observation candidate |
| 内容资产旧商业字段 | 04｜知乎内容资产库 | 无当前等价对象 | 服务身份、旧服务身份、内容目的、引导动作、命中账本、体系分类、目标人群、用户类型、咖啡/商业主线字段 | 属于知乎系统内部混入的历史脏数据字段，不代表咖啡/商业系统进入本次审计范围 | 低 | DROP | None | Retirement Gate Closed | 不迁移；不得外扩审计咖啡、商业或供应链系统 |
| 2026-07 旧候选题事实 | 02｜知乎选题库 | `data/Topic_Pool.md`; `data/topic_candidates/` | 原问题、问题链接、来源、创建时间、最后更新、是否回答、状态、放弃原因 | Git 当前 Topic Pool 主要覆盖当前 Pre-Run；旧候选题仅具历史入口复盘价值 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical topic evidence | Retirement Gate Closed / no migration blocker | 不直接进入 Topic Pool 或当天生产；未来若需要历史题池证据，再按 Salvage Gate 单独发起 |
| 旧选题评分证据 | 02｜知乎选题库 | 无完整等价对象；部分理念已进入 `docs/知乎平台样本学习协议.md` | 评分证据V1、长期搜索价值V1、历史收益证据V1、认知优势匹配V1、推荐原因V1、评分置信度 | Notion 有旧评分过程；Git 当前 Pre-Run 已替代旧评分模型 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy decision evidence | Retirement Gate Closed / no migration blocker | 只可作为 Legacy Decision Evidence；不作为当前 DECISION 规则 |
| 旧选题生产决策字段 | 02｜知乎选题库 | 新架构 DECISION；`data/Topic_Pool.md` | 决策、主收益来源V1、内容机制V1、推荐主机制V1、推荐正文结构V1、选题总分、公式字段 | 属于旧生产逻辑和旧评分模型 | 低 / 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy decision evidence | Retirement Gate Closed / no migration blocker | 公式输出和旧路由不迁入 Runtime |
| 结构03｜事件驱动机制型 | 06｜知乎结构库 | `runtime/知乎结构库快照.md`; `docs/知乎OS Structure Evolution V1.md` | 反常识判断 -> 核心短概念 -> 真实事件 -> 机制拆解 -> 多事件验证 -> 规律升级 -> 回答原题 | Git 当前 ACTIVE-TS01 / TS02 未包含这个完整同构结构；但 Notion 记录状态为 ACTIVE / 已验证 / 结构规律只能作为 Legacy Evidence，不能继承为 Git 结构权威 | 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving candidate structure evidence | Retirement Gate Closed / no migration blocker | 不直接 MERGE。未来若要重启，只能从 Git Structure Lab 重新提出候选结构并补齐来源样本、反例、适用/禁用条件、本账号实验和收益对比；未发布前不得进入 runtime |
| 结构00｜通用解释六段式 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 直接结论 -> 现实场景 -> 核心机制 -> 适用边界 -> 可执行动作 -> 规则收束 | Git 已有 TS01/TS02；Notion 兜底结构验证次数 0，验证等级为假设 | 低 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving structure evolution evidence | Retirement Gate Closed / no migration blocker | 不迁入当前 Runtime |
| 结构01｜反常识—选择权 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 反常识 -> 情绪伤口 -> 利益关系 -> 组织规则 -> 选择权 | Git TS01 已吸收“反常识、情绪入口、机制终点、选择权”等能力 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving structure evolution evidence | Retirement Gate Closed / no migration blocker | 不独立迁为 Runtime 结构 |
| 结构02｜约束—决策 | 06｜知乎结构库 | `runtime/知乎结构库快照.md` | 错误认知 -> 真实约束 -> 关键变量 -> 决策方法 -> 风险边界 | Git TS02 已覆盖解决题/决策题场景、动作、边界、升级条件 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving structure evolution evidence | Retirement Gate Closed / no migration blocker | 不独立迁为 Runtime 结构 |
| 05 每日收益流水 | 05｜知乎单篇复盘库 | `reports/earnings_backfill_report.md`; `data/l0_content_assets.csv`; `data/review_data_snapshots.csv` | `知乎每日收益｜YYYY-MM-DD`、收益、记录时间、换算说明 | 多数只是收益流水，Git 已有收益回填报告和结构化快照承接收益事实 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving source evidence | Retirement Gate Closed / no migration blocker | 不重复迁每日流水；若需保留，只归档为收益来源证据 |
| 05 账号/选题纠偏复盘 | 05｜知乎单篇复盘库 | `data/Milestone_Observations.md`; `production_variable_library.md` | `知乎账号近期复盘记录｜选题跑偏与纠偏规则`、`近30天高商业价值问题复盘｜老板与管理身份题` | 有复盘文本、下一轮动作、边界条件和收益/阅读数据，但其中可能混有未经当前 Git 门槛验证的因果判断 | 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving review evidence | Retirement Gate Closed / no migration blocker | 不直接 MERGE。未来若重启，必须先拆 Evidence / Observation candidate；不得把旧复盘结论直接写成 SUPPORTED，不自动推进 Parameter，不直接改选题规则 |
| 05 规律迁移候选 | 05｜知乎单篇复盘库 | `data/Milestone_Observations.md`; `production_variable_library.md`; `docs/知乎内容质量参数库_V2.md` | 身份冲突机制模型、最强句前置、每篇实验只改一个变量、利益揭露提升停留、垂直度推荐稳定性等 | Notion 多数状态为 假设/经验，验证次数 0-7；有历史证据价值，但未达到当前 Git ACTIVE 门槛，且旧复盘判断可能混合 Evidence、Observation、Hypothesis 和 Parameter candidate | 中 / 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving rule-evolution evidence | Retirement Gate Closed / no migration blocker | 不直接 selective MERGE。未来若重启，只能触发证据补链审计，逐条拆为 Evidence -> Observation -> Hypothesis / Parameter Candidate -> 重新验证 |
| 05 旧协议影响字段 | 05｜知乎单篇复盘库 | `docs/系统治理原则.md`; `docs/生产审计决策流程.md` | 协议影响、升级规律、废弃规律、ACTIVE规律、下一轮动作 | 旧 Notion 复盘库曾承担协议升级建议，当前 Git 已要求证据驱动和人工治理 | 低 / 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy governance evidence | Retirement Gate Closed / no migration blocker | 旧协议影响不能自动改 Git 规则 |
| 08 规则优先级治理 | 08｜知乎协议中心 | `docs/系统治理原则.md`; `docs/知乎OS权威归属表.md`; `README.md`; `runtime/ACTIVE_MANIFEST.md` | `08-00｜知乎规则优先级 V1.0`、唯一 MASTER、L0-L7 协议优先级、协议状态 ACTIVE / TEST / ARCHIVE、低优先级不得覆盖高优先级、复盘不得直接改规则、协议升级验证、30 天冻结规则 | Git 已用 Evidence Driven、Single Source of Truth、Evidence Traceability、对象独立生命周期和 Authority Ownership 覆盖治理目的；L0-L7、唯一 MASTER、统一 ACTIVE / TEST / ARCHIVE 状态机和 30 天冻结规则属于旧实现，其中 30 天冻结已被后续 milestone 治理替代 | 中 | SKIP / ARCHIVE | `research/notion_archive/` only if preserving legacy governance evolution | Decision Checked / no migration required; legacy archive optional | 不存在需要 selective MERGE 的独有当前治理规则；Notion 08-00 只作为历史治理演化证据，不恢复唯一 MASTER / L0-L7，不迁统一协议状态机，不恢复 30 天冻结，不修改当前 Git Governance |
| 08 选题/输入协议 | 08｜知乎协议中心 | `docs/Codex选题采集协议.md`; `templates/选题包模板.md`; `docs/Input Rules V1.md` | 选题筛选四道门、题意识别卡、母题识别、高收益选题五维评分、六入口协议、旧 Skill001 等 | Git 当前 Pre-Run 已覆盖选题发现、入口校准、候选排序、读者视角、Benchmark、重复检查和 Topic Package；Input Rules V1 已明确题目选定后 INPUT 不再判断“该不该答 / 该怎么答”。Notion 的固定入口配额、职场比例、五维 100 分阈值、四道门和母题分类属于 Legacy Decision Logic | 中 | SKIP / ARCHIVE | `research/notion_archive/` only if preserving legacy topic-selection evolution | Decision Checked / no migration required; legacy archive optional | 未发现同时满足 Salvage Gate（Git 不存在 / 关闭 Notion 会永久丢失 / 未来有实际用途）的独有资产；不做 selective MERGE，不恢复六入口配额、固定日配额、职场 ≥60%、五维评分、80 分必答、十个母题或旧题意路由为当前 DECISION / Input 规则 |
| 08 生成/表达协议 | 08｜知乎协议中心 | `docs/知乎OS Compiler Data Flow V1.md`; `docs/知乎正文推理协议 V1.0.md`; `docs/知乎正文表达协议 V3.md`; `production_variable_library.md` | Skill005 正文生产、Skill006 表达转换、EGCR、利益揭露、选择权归还、高赞表达、商业翻译流、作者在场、机制解释补充卡 | Notion Skill005 / Skill006 属于旧节点架构；“冻结内容后生成正文”“表达不得改变事实/判断/结构/证据”“后台结构化、前台自然化”“推导深度”“现实画面/去模板化”等有效能力，已分别由当前 Execution IR / WRITE 数据契约、Reasoning Protocol、Expression Protocol V3 和 Parameter System 覆盖或升级 | 中 | SKIP / ARCHIVE | `research/notion_archive/` only if preserving legacy generation/expression evolution | Decision Checked / no migration required; legacy archive optional | 未发现通过 Salvage Gate 的独有当前能力；不做 selective MERGE，不恢复 Skill005 -> Skill006 节点模型，不恢复旧 Production Card / L2 / L3 生成模块，不把旧表达规则直接迁入 Parameter、Prompt 或 runtime |
| 08 发布前终检/评分协议 | 08｜知乎协议中心 | `docs/生产审计决策流程.md`; `docs/生产状态机与交接规范.md`; `docs/整体审核七项清单.md` | 回答价值评分、收益评分、发布前终检、边界/行动/跑题/表达硬检 | Git 已有 AUDIT / REVIEW / RELEASE 边界和用户验收规则；旧评分卡只可能作为历史审计对照 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy audit evidence | Retirement Gate Closed / no migration blocker | 不建立第二套评分发布门槛；如未来重启，必须先过 Salvage Gate |
| 08 数据复盘/收益优化协议 | 08｜知乎协议中心 | `docs/单篇复盘执行协议.md`; `data/review_data_snapshots.csv`; `data/Milestone_Observations.md` | 分阶段数据复盘、RPM 核心盈利指标、数据结构-因果判断-下一轮生产 | Git 有复盘数据表和复盘协议；Notion 有旧收益优化表达和 30 天实验约束 | 中 / 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy review evidence | Retirement Gate Closed / no migration blocker | 不让复盘直接覆盖生产规则；如未来重启，必须先过 Salvage Gate 和 Evidence Split |
| 08 旧 MASTER / Production Card 协议 | 08｜知乎协议中心 | `templates/Production Card模板.md`; `docs/知乎OS执行协议.md`; `docs/生产审计决策流程.md` | `知乎OS总调度 V2.16｜唯一MASTER｜Production Card`、旧 Answer Protocol、旧 Master Prompt | 当前 Git 已明确 Production Card 退出 Codex 日常主链，新架构以 Execution IR 为正式中间对象 | 低 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy architecture evidence | Retirement Gate Closed / no migration blocker | 不恢复旧 Master；只作为历史架构证据 |
| 00 知乎项目OS 首页 | 知乎项目OS 根页面 | `README.md`; `docs/知乎OS权威归属表.md` | 00-04 功能区、唯一入口、驾驶舱、当前启用数据库、运行规则、系统边界 | Git 已有 README 和权威归属表；Notion 首页包含旧 Production Card 唯一执行对象说法 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy IA evidence | Retirement Gate Closed / no migration blocker | 仅可选归档旧信息架构证据；不恢复“生产卡唯一执行对象” |
| Notion 版权威归属表 | 知乎OS权威归属表 | `docs/知乎OS权威归属表.md` | 页面归属、模块边界、Production Authority | Git 已有更新版，并已声明 Notion 退出 Production Authority Chain | 高 | SKIP | `docs/知乎OS权威归属表.md` | Checked | Git 版本更新，Notion 版只作为历史证据 |
| 03 高盐粒收益问题池 | 03｜知乎高收益问题池 | `data/Topic_Pool.md`; `data/topic_candidates/`; `data/l1_sample_list.csv` | 高收益问题、旧收益证据、候选题池 | 可能包含旧候选题，但当前生产已由 Git Pre-Run / Topic Pool 承接 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical topic evidence | Retirement Gate Closed / no migration blocker | 不直接并入当前 Topic Pool；未来若重启必须过 Salvage Gate |
| 05.5 规律验证库 | 知乎规律验证库 | `data/Milestone_Observations.md`; `production_variable_library.md` | Observation / Hypothesis / Experience / ACTIVE、Evidence、反例、连续验证、成功次数、成功率、下一步验证动作、是否允许升级协议 / MASTER | Notion 旧生命周期与 Git Observation / Parameter 生命周期相似但不等价；Schema 确认其承担旧治理职责 | 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical evidence | Retirement Gate Closed / no migration blocker | 不迁旧生命周期，不迁升级 MASTER / 协议权限；未来若重启只能抽独有历史 Evidence，不把旧 Hypothesis 重新激活成当前 OPEN Observation |
| 旧知乎规律库 | 知乎规律库（历史证据层） | `runtime/知乎ACTIVE规律快照.md`; `production_variable_library.md`; `data/Milestone_Observations.md` | 历史规律、经验、假设、失效记录 | 与 ACTIVE｜知乎规律库不同，可能有旧规律资产 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical rule evidence | Retirement Gate Closed / no migration blocker | Notion 状态不继承；未来若重启必须过 Salvage Gate |
| 旧知乎收益库 | 知乎收益库（历史证据层） | `data/l0_content_assets.csv`; `data/review_data_snapshots.csv`; `reports/earnings_backfill_report.md` | 收益快照、收益明细、历史收益记录 | Git 已有收益回填报告、L0 和 review snapshots 承接当前收益事实 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical earnings evidence | Retirement Gate Closed / no migration blocker | 未来若重启需按 answer_url / article_id 核对，不按标题近似覆盖 |
| 07 评论金矿库 | 07｜知乎评论金矿库 | `data/Milestone_Observations.md`; `docs/单篇复盘执行协议.md` | 高价值评论、评论诱因、读者反馈、需求信号 | 只可能有读者反馈证据价值，不构成当前生产依赖 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving reader-feedback evidence | Retirement Gate Closed / no migration blocker | 不直接生成生产规则；未来若重启必须过 Salvage Gate |
| 09 Skill Center | 09｜跨模型 Skill Center; Skill001/001B/005/006 等页面 | `skills/`; `docs/知乎OS执行协议.md`; `docs/知乎OS Compiler Data Flow V1.md` | 旧 Skill001-007 节点、输入输出、停止条件、错误代码 | Git skills 存在旧 Skill006/007；新架构已转向七节点对象流 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving legacy skill evidence | Retirement Gate Closed / no migration blocker | 不恢复旧 Skill 链；未来若重启只能作为历史架构证据 |
| 06 生产卡库 | 06｜知乎生产卡 | `productions/`; `templates/Production Card模板.md` | 历史 Production Card 实例、生产状态、发布状态 | 当前 Git 有 productions 目录，Production Card 已退出日常主链 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical production evidence | Retirement Gate Closed / no migration blocker | 只可选保留 Git 缺失且有追溯价值的实例；不恢复 Production Card 主链 |
| 07 正文 QA 库 | 07｜正文 QA | `productions/`; `docs/整体审核七项清单.md`; `docs/生产审计决策流程.md` | 历史 QA、终检、问题归因、发布前检查 | Git 部分 productions 下已有 QA/Audit/Release 文件 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical QA evidence | Retirement Gate Closed / no migration blocker | 不迁旧 QA 规则为新 AUDIT 权威；未来若重启需按 Production ID / 标题核对 |
| 平台爆款样本库 | 知乎平台爆款样本库｜职场 | `docs/知乎平台样本学习协议.md`; `data/Milestone_Observations.md` | 平台高赞样本、传播规律、样本证据 | Git 有平台样本学习协议；Notion 样本库不构成当前 Production Card / Execution IR 依赖 | 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving platform-sample evidence | Retirement Gate Closed / no migration blocker | 未来若重启需单独判定版权/引用边界；不得直接进入 Production Card / Execution IR |
| L2 正文变量矩阵 | L2｜正文变量矩阵 | `reports/zhihu_l2_variable_matrix_pilot_20260729.md`; `l2_variable_records.md`; `l2_variable_validation.md` | 2026-07-29 7 篇第一轮 L2 实验：唯一主变量、辅助变量、首屏、结构、信息价值、认知奖励、传播变量、收益数据；其中 5 篇有全文证据，2 篇只有摘录需复核 | Git 可证明覆盖 7 篇 pilot 报告的运行结论；Notion L2 全部行未完成 Query，但不构成当前生产依赖 | 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving L2 historical evidence | Retirement Gate Closed / no migration blocker | 不宣告全库 Covered；但不作为 Notion 退役阻断。未来若重启需恢复 Query 后做行级核验 |
| 知乎表达样本库 | 知乎表达样本库 | `docs/知乎正文表达协议 V3.md`; `data/Milestone_Observations.md`; `reports/` | 表达样本、AI味、可迁移等级、表达证据 | Git 有表达协议和 2026-07-31 表达证据报告 | 中 / 高 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving expression evidence | Retirement Gate Closed / no migration blocker | 不变成第二套 Writer Rules；未来若重启必须过 Salvage Gate |
| 7/25-7/31 数据快照页 | 根页面直属快照页 | `reports/`; `data/review_data_snapshots.csv`; `data/l0_content_assets.csv` | 近10篇回答、TOP10事实包、生产表现、收益明细、关注者画像、后台数据与同题样本 | Git 已有部分报告和数据表承接当前数据事实 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving historical snapshot evidence | Retirement Gate Closed / no migration blocker | 未来若重启需按页面逐条核对；优先保留可证明数据来源的快照 |
| Candidate v0.1｜内容变更分级与审批规则 | ACTIVE｜知乎规律库 | `docs/系统治理原则.md`; `data/Milestone_Observations.md`; `production_variable_library.md` | Level A 语言表达层、Level B 用户行为层、Level C 系统治理层；Level C 需人工审批 | Notion 状态为 REVIEW，证据样本数 1；Git 治理原则已明确“做信息隔离，不做对象膨胀”和参数/观察生命周期 | 中 | SKIP / legacy archive optional | `research/notion_archive/` only if preserving governance observation evidence | Retirement Gate Closed / no migration blocker | 不迁为 ACTIVE 规律；如保留，只作为治理观察证据 |
| ACTIVE 规律库行级资产 | ACTIVE｜知乎规律库 | `runtime/知乎ACTIVE规律快照.md`; `production_variable_library.md` | 当前 query 仅返回 1 条 REVIEW 候选，无正式 ACTIVE 行 | Notion 未发现可直接迁移的 ACTIVE 规律行 | 低 | SKIP | None | Checked | 暂不迁移；当前 Git runtime 规律快照仍是 DRAFT 过渡资产，后续由 release_runtime.py 控制发布 |

## Source Coverage Notes

### 04｜知乎内容资产库

已完成：Schema 差集、初步记录覆盖差集、字段价值分层。

结论：

- 基础内容事实大多已在 Git 数据层覆盖。
- Notion 独有价值集中在人工复盘、异常说明、旧收益导入备注、核心短概念和栏目/账号归属；Retirement Gate 后默认仅作 Historical Evidence。人工复盘字段不得把复盘结论、核心结论、当前实验变量或失败原因分类直接 MERGE 进当前知识体系。
- 非知乎经营字段、咖啡/商业旧体系字段默认 DROP；这不扩大本次范围，不继续审计知乎项目OS外部系统。

### 02｜知乎选题库

已完成：Schema 差集、初步记录覆盖差集、字段价值分层。

结论：

- 2026-07 旧候选题在 Git 当前 Topic Pool 中覆盖不足，但不构成当前生产依赖。
- 旧评分字段具有历史解释价值，但不能作为当前 DECISION Runtime 规则。
- Retirement Gate 后不再要求迁题目事实；未来若重启，只可按 Salvage Gate 抽取必要历史证据，不迁旧评分模型为生产权威。

### 06｜知乎结构库

已完成：行级差集。

行级结论：

| Notion Row | Git Coverage | Decision | Reason |
|---|---|---|---|
| 结构00｜通用解释六段式 | 部分被 TS01 / TS02 覆盖 | ARCHIVE / DROP | 兜底结构，验证次数 0，验证等级假设 |
| 结构01｜反常识—选择权 | 被 TS01 大量吸收 | SKIP / ARCHIVE | 旧结构演化证据，不独立入 Runtime |
| 结构02｜约束—决策 | 被 TS02 部分吸收 | SKIP / ARCHIVE | 可作为 TS02 对照，不独立入 Runtime |
| 结构03｜事件驱动机制型 | Git 缺完整同构结构，但缺少可继承的 Git 结构验证证据 | SKIP / legacy archive optional | Retirement Gate 后不构成迁移阻断；未来若重启，只能从 Git Structure Lab 重新提出候选结构并补来源样本、反例、适用/禁用条件、本账号实验和收益对比 |

### ACTIVE｜知乎规律库

已完成：行级差集。

结论：

- 当前可查询行只有 `Candidate v0.1｜内容变更分级与审批规则`。
- 状态是 REVIEW，证据样本数 1，不具备迁入 ACTIVE Runtime 资格。
- Git 治理原则已覆盖其核心意图的大部分。
- Retirement Gate 后不迁移；最多作为治理观察证据可选归档。

### 05｜知乎单篇复盘库

已完成：行级抽样与类别判定。

结论：

- `知乎每日收益｜YYYY-MM-DD` 类记录多为收益流水，和 Git 收益回填报告 / L0 / review snapshots 高度重叠，默认 SKIP；仅在需要证明来源时 ARCHIVE。
- `规律迁移｜...` 类记录多数是 假设 / 经验 状态，需先重分类为 Evidence、Observation candidate、Hypothesis 或 Parameter candidate；不得因 Git 参数缺证据引用而直接 selective MERGE，不允许直接进入 ACTIVE 规律或 Runtime。
- `知乎账号近期复盘记录｜选题跑偏与纠偏规则`、`近30天高商业价值问题复盘｜老板与管理身份题` 证据价值较高，但需先拆分 Evidence / Observation candidate；旧复盘中的因果判断不得直接作为 SUPPORTED Observation。
- `协议影响`、`升级规律`、`ACTIVE规律` 等旧字段只作为历史治理证据，不自动修改 Git 规则。

### 08｜知乎协议中心

已完成：行级抽样与类别判定。

结论：

- 08 是旧 L0-L7 协议中心，不作为当前 Git 生产入口恢复。
- 旧 Master / Production Card 调度协议默认 DROP / ARCHIVE，因为当前正式中间对象是 Execution IR。
- 规则优先级治理已由 Git 当前 Evidence Driven、Single Source of Truth、Evidence Traceability、对象独立生命周期和 Authority Ownership 覆盖，判定 SKIP / ARCHIVE。
- 选题/输入协议已由 Git 当前 Pre-Run 与 Input Rules 分工覆盖；Notion 六入口、固定配额、五维评分、四道门和母题分类属于 Legacy Decision Logic，判定 SKIP / ARCHIVE。
- 生成/表达协议已由当前 Execution IR / WRITE 数据契约、Reasoning Protocol、Expression Protocol V3 和 Parameter System 覆盖；Skill005 -> Skill006 属于旧节点架构，判定 SKIP / ARCHIVE。
- 结构执行、数据复盘、发布前终检等其他 08 子项仍需按各自行级证据单独审计。

### 其他知乎OS直属资产

已完成：根页面资产发现。

结论：

- 根页面确认还存在 03 高收益问题池、05.5 规律验证库、旧知乎规律库、旧知乎收益库、07 评论金矿库、09 Skill Center、06 生产卡库、07 正文 QA 库、平台爆款样本库、L2 正文变量矩阵、知乎表达样本库和多份 7/25-7/31 数据快照页。
- 这些资产属于“知乎项目OS / 知乎系统”子树，进入本台账；但多数尚未完成 Schema + row coverage。
- Retirement Gate 已关闭剩余直属资产的迁移阻断：未发现当前 Git 生产仍依赖 Notion，也未发现已知的 Notion 独有且关闭后会造成实际生产损失的资产。
- 05.5、L2、平台爆款样本库、生产卡库、正文 QA 库、03 高收益问题池等剩余项默认视为 Historical Evidence；未来只有同时满足 Salvage Gate 才重新开启迁移候选。
- 根页面本身和 Notion 版权威归属表已被 Git README / 权威归属表覆盖，只保留历史证据，不作为生产权威。

### Tooling Notes

- 尝试直接查询 L2 数据库全部行时，Notion Query Data Source 当前额度已用完；未重试。
- 该限制影响 L2 全库覆盖定案，但不构成 Retirement Gate 阻断：L2 不能宣告全库 Covered，也不能阻止 Notion 退出生产权威链。

## Retirement Closeout

1. 本台账不再要求逐页补审 Notion，也不进入实际迁移批处理。
2. 剩余未逐条核完的 Notion 资产默认降级为 Historical Evidence / legacy archive optional。
3. 后续任何 Notion 内容重新进入 Git，必须重新提出 Git Change Proposal，并同时通过 Salvage Gate：
   - Git 不存在；
   - Notion 关闭会永久丢失；
   - 未来有实际用途。
4. 即使通过 Salvage Gate，也不得继承 Notion 的 ACTIVE / 已验证 / 优先回答 / 升级 MASTER / 协议权限等旧状态。
5. 本次收尾不删除 Notion，不删除 Notion 子树，不修改 Runtime Manifest，不发布 TRIAL / ACTIVE Runtime。
