# 知乎盈利系统权威归属表

本表用于回答：到底改哪个页面。

五个模块只是导航和归属，不是新建五套数据库，也不是五个独立子系统。Production Card 已退出日常生产主链，当前唯一前置产物是 Codex 选题包（Topic Package），后续由 Claude 依次执行 Compiler V1 七节点中的 INPUT/DECISION/COMPILE/WRITE，产出 Execution IR 与正文，权威定义见 `docs/知乎OS Compiler V1.md`。

## Module 原则

```text
00 首页
决定做什么
↓
01 生产模块
决定怎么做
↓
02 知识模块
提供能力
↓
03 运行模块
记录正在做什么
↓
04 复盘模块
决定以后怎么做得更好
```

```text
知乎盈利系统
├── 生产模块
├── 知识模块
├── 运行模块
├── 复盘模块
└── 治理模块
```

只有顶层整体称为 System（系统）；内部功能单元统一称为 Module（模块）。

复盘模块负责采集结果、建立历史基线、筛选代表样本、形成候选规律，并把验证结论反馈给知识模块和生产模块。

任何页面都必须回答：我属于哪一句。回答不了，说明放错地方。

## 权威归属表

| 名称 | Module | 是否权威 | 引用方 | 谁不能再维护它 |
| --- | --- | --- | --- | --- |
| `README.md`｜知乎盈利系统首页 | 00 首页 | 是，顶层入口权威 | 全部页面、协议、日常生产 | 生产模块、知识模块、运行模块、复盘模块、治理模块不得另建首页或第二入口 |
| 收益指标 / 当前实验 / 待办视图 | 00 首页 | 入口视图，数据以来源库为准 | 日常生产、复盘判断 | 首页只引用，不复制维护底层数据 |
| `docs/知乎OS权威归属表.md` | 00 首页 | 是，归属判断权威 | README、总控协议、生产协议 | 其它页面不得另起一套归属表 |
| `docs/知乎OS Compiler V1.md` | 01 生产模块 | 是，七节点流水线（INPUT/DECISION/COMPILE/WRITE/AUDIT/REVIEW/RELEASE）节点定义、Execution IR Schema 与 Architecture Routing Table 唯一权威；Status: DESIGN_FROZEN，已由 `runtime/ACTIVE_MANIFEST.md` 以 TRIAL 状态发布为受控试运行执行权威 | 执行协议、总AI执行中心、Claude正文生产Prompt、生产状态机与交接规范、GPT审核清单、Failure Pattern模板、Structure Evolution V1 | 其它文件不得另立九对象链（Analyzer/Structure Matcher/Router/Slim IR/Runtime Assembly/Writer Input Package）或另立节点定义 |
| `docs/知乎OS执行协议.md` | 01 生产模块 | 是，生产执行总协议权威 | README、总AI执行中心 | 知识库、复盘库不得维护稳定流程；节点定义以 Compiler V1 为准，本文件不得另立 |
| `docs/08_总AI执行中心.md` | 01 生产模块 | 是，AI调用协议权威 | 执行协议、QA | 变量库、质量参数库不得维护调度链路；节点定义以 Compiler V1 为准 |
| `docs/00-设计原则.md` | 05 治理模块 | 是，系统设计边界权威 | README、执行协议、权威归属表 | 单篇复盘、临时实验不得直接改设计原则 |
| Reasoning First 推导优先原则 | 05 治理模块 | 是，系统架构优先级权威；唯一出处为 `docs/00-设计原则.md` 原则0 | 平台样本学习、Evidence Schema、Knowledge Engine、Parser、Automation、Execution IR | 协议中心、Parser、自动化脚本不得越过 Reasoning Grammar 直接定义字段或生产知识 |
| 中文字段优先规则 | 05 治理模块 | 是，字段命名与运行产物可读性权威；唯一出处为 `docs/00-设计原则.md` 原则13 | 所有 schema、JSON、模板、QA 报告、结构匹配产物 | 任何脚本或模板不得只新增英文关键字段 |
| `docs/知乎平台样本学习协议.md` | 02 知识模块 | 是，平台样本采集、拆解、统计和账号验证链路权威 | README、执行协议、ACTIVE_MANIFEST、ACTIVE规律快照 | 日常生产不得直接读取平台样本或未验证平台变量证据 |
| `skills/Skill006_知乎生产卡生成器.md` | 01 生产模块 | 否，`LEGACY_RETIRED`：Production Card 已退出日常生产主链，本文件只作历史归档，不具备执行权威 | 不适用——不再是任何日常生产上游 | 不得被 Codex/Claude 单篇任务引用、执行或转写 |
| `skills/Skill007_正文QA协议.md` | 01 生产模块 | 否，`LEGACY_RETIRED`（文件自身已标注）：AUDIT 节点现行执行载体是 `templates/GPT审核清单.md` | 不适用 | 不得被引用为当前 AUDIT 执行入口 |
| `templates/知乎OS总控提示词.md` | 01 生产模块 | 是，Codex 选题采集侧总控提示词权威（INPUT Boundary 之前） | Codex日常生产、执行协议 | 正文、复盘库不得维护总控提示词；不得越过 INPUT Boundary 定义 DECISION/COMPILE/WRITE 规则 |
| `templates/Claude正文生产Prompt.md` | 01 生产模块 | 是，Orchestrator + Writer Rules 权威：Claude 作为单一 Actor 顺序执行 INPUT/DECISION/COMPILE/WRITE 四节点，但本文件只完整拥有并维护 WRITE 的 Runtime.Writer Rules；INPUT/DECISION/COMPILE 三步只引用 `docs/Codex选题采集协议.md`§1.1、`docs/内容架构总则.md`、`docs/知乎OS Structure Evolution V1.md`§5、`production_variable_library.md` + `docs/知乎内容质量参数库_V2.md`§0 QT-QI（仅 QT-00/QI-01～QI-06 六项识别字段，2026-08-11 Migration Fix，见 Compiler V1 第4节），不得复制维护这四份 + 一节的规则正文 | Claude正文 | 知识库、复盘库不得维护正文Prompt；不得重新引入 Production Card 作为 IR；不得把 INPUT/DECISION/COMPILE 的判定规则正文复制进本文件（SSP） |
| `templates/Production Card模板.md` | 01 生产模块 | 否，`LEGACY_RETIRED`：Production Card 对象已随九对象链废弃，Execution IR 唯一权威见 Compiler V1 第5节 | 不适用 | 不得作为当前正文生产的 IR 载体 |
| Explanation Target（一致解释目标）字段定义 | 01 生产模块 | 是，跨节点字段，各字段权威分属不同节点，不归单一文件：`读者真实困惑`（DECISION，非 INPUT——Compiler V1 明确禁止 INPUT 写入带解释性质的字段，选题包「3. 读者视角校准」节和 `docs/Codex选题采集协议.md`§1.1 只负责采集/交接，判定权威在 DECISION）、`唯一核心判断`/Core Judgment（DECISION，来源 `docs/内容架构总则.md`）、`Reasoning Path`（COMPILE，来源 `docs/知乎OS Compiler V1.md`第5节）；`templates/Claude正文生产Prompt.md` 只在对应步骤消费这些字段，不持有其定义权威 | Claude正文生产Prompt、GPT审核清单 | 不得新增独立 Skill、Engine、流程节点、知识库或平行字段体系；不得把 DECISION/COMPILE 字段的定义权威归给 INPUT 或 WRITE 侧的 Claude正文生产Prompt |
| `templates/单次任务模板.md` | 01 生产模块 | 是，单次任务输入格式权威 | Codex日常任务 | 复盘库不得维护任务模板 |
| `docs/知乎OS Structure Evolution V1.md` | 02 知识模块 | 是，Research / Governance Authority：结构 Research Layer（Structure Lab、候选结构、ACTIVE 升级门槛）权威，以及 COMPILE 结构选择能力的边界定义（第5节，规定"能读什么、不能读什么"）；不是 Runtime Compile Rules 内容本身，不持有当前 TRIAL 实际调用的结构规则数据 | 结构库快照、COMPILE 结构选择能力 | 不得因 Structure Matcher 节点废弃而整篇废弃；Research Layer 判断不受 Production 节点变化影响；不得反向声称持有 Runtime Execution Authority |
| `docs/Writer Input Package Schema V1.md` | 01 生产模块 | 否，`DEPRECATED`：定义的 Writer Input Package 对象已被 Execution IR 取代，只作历史参考 | 不适用 | 不得重写为 Execution IR V2，避免形成第二个 Execution IR Schema 权威 |
| `templates/GPT审核清单.md` | 01 生产模块 | 是，AUDIT 节点执行载体权威，AuditResult（Expected Source/Expected/Actual/Violation Source/Return Stage）格式以本文件为准 | 生产状态机与交接规范、Claude正文生产Prompt Patch 规则 | 不得回退为"正文问题/系统问题"二分 |
| `docs/生产状态机与交接规范.md` | 01 生产模块 | 是，状态机与交接权威，同时是 `Runtime.Release Rules` 唯一权威（USER_APPROVED 前置条件） | Publish_Queue、README、执行协议 | `data/Publish_Queue.md` 不得重复维护 Release Gate 规则 |
| `templates/Failure Pattern模板.md` | 01 生产模块 | 是，失败模式记录格式权威，`violation_source`/`return_stage` 取值以 Compiler V1 Architecture Routing Table 为准 | 系统升级评审 | 不得回退为 Analyzer/IR/Writer Prompt/Writer/QA/Feedback 旧层枚举 |
| `docs/知乎内容质量参数库_V2.md` | 02 知识模块 | 是，质量参数权威（§0 QT-QI 另见下条 Migration Fix 说明） | 总AI执行中心、GPT审核清单、DECISION（仅§0 QT-QI 六项识别字段，2026-08-11 起） | 生产协议只触发参数，不复制维护参数 |
| `docs/知乎内容质量参数库_V2.md`§0 QT-QI（Migration Fix，2026-08-11） | 01 生产模块 | 是，DECISION 强制输入（Compiler V1 第4节）：Production Card 退役、职责迁入 Compiler V1 时，QT-QI 问题理解识别域未被任何现行节点正式继承，DECISION 曾直接从 Input Package 跳到 Main Gap，未核对用户真实提问类型；本条目补上这一遗漏，仅授权 QT-00/QI-01～QI-06 六项识别字段进入 DECISION，该文件其余 PD/RR/RE/BT/CR 等正文质量参数消费者不变（仍是 COMPILE/WRITE/AUDIT），不因本次修复扩大范围 | DECISION（Reality/Main Gap/Transformation/Core Judgment 锁定前必须先完成） | 不得把 QT-QI 之外的参数域一并授权给 DECISION；不得反向声称本条目扩大了`docs/知乎内容质量参数库_V2.md`对 DECISION 的整体授权 |
| `runtime/ACTIVE_MANIFEST.md` | 02 知识模块 | 是，Codex日常执行快照清单权威 | Codex日常生产、校验脚本 | Git docs/templates 修改未经 `scripts/release_runtime.py` 发布前不得直接影响生产 |
| `runtime/知乎内容质量参数快照.md` | 02 知识模块 | 是，Codex日常参数执行权威 | GPT审核清单 | 未标记ACTIVE的参数不得进入生产触发 |
| `runtime/知乎ACTIVE规律快照.md` | 02 知识模块 | 是，Codex日常规律执行权威（内容混装 COMPILE/Writer/Audit 职责，SPLIT REQUIRED，见迁移审计） | 爆款规律提取 | 单篇复盘不得直接覆盖runtime规律 |
| `runtime/知乎结构库快照.md` | 02 知识模块 | 是，Runtime Execution Authority：当前 TRIAL/ACTIVE 版本真正可调用的 Compile Rules 结构数据，COMPILE 执行时唯一读取的结构规则内容 | 内容路由、COMPILE（受 Structure Evolution V1 第5节边界约束） | 未发布的结构草稿不得直接进入生产；不得反向声称持有 Research/Governance Authority（升级门槛判断仍在 Structure Evolution V1） |
| `runtime/知乎账号画像快照.md` | 02 知识模块 | 是，账号画像执行快照权威 | 选题准入、选题扩展、案例选择、复盘样本优先级 | 不得新增 Execution IR 字段，不得直接修改 Prompt |
| `production_variable_library.md`｜知乎内容变量参数库 | 02 知识模块 | 是，唯一内容变量权威库 | Claude正文生产Prompt、正文生产、平台样本学习、账号验证 | 不得新建平台变量库、账号变量库或第二套参数体系 |
| `l2_variable_records.md` | 02 知识模块 | 变量标注材料，不是生产权威 | 知乎内容变量参数库、L2.5变量验证 | 不得作为第二套账号变量库 |
| `l2_variable_validation.md` | 02 知识模块 | 变量验证材料，不是生产权威 | 知乎内容变量参数库、复盘模块 | 不得作为第二套账号变量库，不得把单次验证升级为稳定协议 |
| 结构库 / ACTIVE规律库 / 参数库 / 案例库 / 平台规则（Notion） | 02 知识模块 | 否，已退出 Production Authority Chain（2026-08-09 治理变更），降级为 Reference / Archive，不拥有管理、审批或执行权威 | 不适用——不再是任何 runtime 发布或日常生产的上游 | 生产系统权威链收缩为 Git docs/templates → production_variable_library.md → runtime 执行快照 → ACTIVE_MANIFEST，不再经过 Notion；Notion 内容如需重新参与生产，须先以 Git 文件形式提出 Change Proposal，不得直接引用 Notion 页面作为依据 |
Execution IR（本次 Run 由 COMPILE 产出，不持久化为独立文件，随 Run 生命周期存在） | 03 运行模块 | 是，单篇执行对象权威（原 Skill006 输出的 Production Card 已 `LEGACY_RETIRED`） | Claude正文（WRITE）、GPT审核清单（AUDIT）、发布终检、复盘 | 不得新建第二套Run数据库或任务系统 |
| 当前正文 | 03 运行模块 | 单篇运行产物，以本次 Execution IR 为准 | GPT审核清单、发布状态、单篇复盘 | 正文不得反向修改 Execution IR |
| 生产状态 / 发布状态 | 03 运行模块 | 运行状态权威，以 `docs/生产状态机与交接规范.md` 状态表记录为准 | 首页待办视图、复盘模块 | 复盘库不得替代运行状态 |
| `data/L0_README.md` | 04 复盘模块 | 是，L0内容资产口径权威 | L0内容资产总账、报告、复盘 | 生产模块不得维护L0字段口径 |
| `data/l0_content_assets.csv` | 04 复盘模块 | 数据来源，内容资产总账权威 | L1样本、L2验证、收益报告、单篇复盘 | 首页和生产卡只引用，不复制维护 |
| `data/l1_sample_list.csv` | 04 复盘模块 | 是，L1分层样本权威 | L2变量验证、实验复盘 | L0总账不得直接形成规律结论 |
| `data/production_article_map.csv` | 04 复盘模块 | 是，Production ID 与 article_id 映射权威 | 参数调用日志、L0内容资产总账、单篇复盘 | 不得在报告里另建长期映射表 |
| `data/review_data_snapshots.csv` | 04 复盘模块 | 是，发布后复盘窗口主快照，合并互动数据与收益字段 | 参数调用日志、单篇复盘、周期复盘 | 不得另建日常收益快照表；不得用临时截图说明替代结构化快照 |
| `docs/单篇复盘执行协议.md` | 04 复盘模块 | 是，单篇复盘执行口径权威 | 参数调用日志、Observation、周期复盘 | 临时报告不得替代日常复盘协议 |
| `reports/l0_asset_report.md` | 04 复盘模块 | 报告，不替代数据源 | L0检查、收益回看 | 不得反向修改L0口径 |
| `reports/historical_baseline_report.md` | 04 复盘模块 | 报告，账号历史基线与分布画像 | 单篇复盘、L1样本入口、候选规律验证 | 不得替代L0内容资产总账；不得直接形成ACTIVE参数 |
| `reports/l1_sample_report.md` | 04 复盘模块 | 报告，不替代数据源 | L1样本检查、L2验证 | 不得替代L1样本清单 |
| `reports/earnings_backfill_report.md` | 04 复盘模块 | 报告，不替代数据源 | 收益数据回填、复盘判断 | 不得替代内容资产总账 |
| `reports/production_experiment_001.md` | 04 复盘模块 | 单次实验记录 | 复盘模块、后续规律验证 | 不得升级为稳定生产协议 |
| `知乎TOP10事实包_V1_给GPT复盘.md` | 04 复盘模块 | 复盘事实包 | 单篇复盘、规律验证、知识更新 | 不得替代 `docs/` 下的治理与协议权威文件 |
| `docs/系统治理原则.md` | 05 治理模块 | 是，证据门槛、状态流转和系统修改条件权威 | 参数库、Observation、复盘模块、生产模块 | 各模块不得另建治理原则 |
| `scripts/validate_production_card.py` | 01 生产模块 | 否，`LEGACY_RETIRED`：随 Production Card 对象退役，只作历史工具归档 | 不适用 | 不得成为当前 Execution IR 的校验入口 |
| `scripts/validate_l0_assets.py` | 04 复盘模块 | 工具，L0数据校验权威 | L0内容资产总账、L0报告 | 不得修改L0字段口径 |
| `scripts/generate_l1_sample_list.py` | 04 复盘模块 | 工具，L1样本生成权威 | L0内容资产总账、L1样本清单 | 不得直接生成规律结论 |
| `scripts/generate_l0_report.py` | 04 复盘模块 | 工具，L0报告生成权威 | L0内容资产总账、L0报告 | 不得替代数据源 |
| `CHANGELOG.md` | 00 首页 | 变更记录 | 全部模块 | 不得维护业务知识或执行协议 |

## 禁止事项

- 不复制数据库。
- 不新建第二套任务系统。
- 不为了目录整齐去删除、合并历史数据。
- 不把单篇经验直接升级为稳定协议。
- 不让正文、复盘或报告反向修改 Execution IR 或 Decision。
