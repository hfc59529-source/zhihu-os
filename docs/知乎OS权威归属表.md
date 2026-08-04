# 知乎OS权威归属表

本表用于回答：到底改哪个页面。

五个功能区只是导航和归属，不是新建五套数据库。Production Card 已退出日常生产主链，当前唯一前置产物是 Codex 选题包，当前正文产物由 Claude 直接基于选题包、参数和推理生成。

## 功能区原则

```text
00 首页
决定做什么
↓
01 生产系统
决定怎么做
↓
02 知识系统
提供能力
↓
03 运行系统
记录正在做什么
↓
04 复盘系统
决定以后怎么做得更好
```

任何页面都必须回答：我属于哪一句。回答不了，说明放错地方。

## 权威归属表

| 名称 | 功能区 | 是否权威 | 引用方 | 谁不能再维护它 |
| --- | --- | --- | --- | --- |
| `README.md`｜知乎OS首页 | 00 首页 | 是，顶层入口权威 | 全部页面、协议、日常生产 | 生产系统、知识系统、运行系统、复盘系统不得另建首页或第二入口 |
| 收益指标 / 当前实验 / 待办视图 | 00 首页 | 入口视图，数据以来源库为准 | 日常生产、复盘判断 | 首页只引用，不复制维护底层数据 |
| `docs/知乎OS权威归属表.md` | 00 首页 | 是，归属判断权威 | README、总控协议、生产协议 | 其它页面不得另起一套归属表 |
| `docs/知乎OS执行协议.md` | 01 生产系统 | 是，生产执行总协议权威 | README、Skill006、Skill007、总AI执行中心 | 知识库、生产卡、复盘库不得维护稳定流程 |
| `docs/08_总AI执行中心.md` | 01 生产系统 | 是，AI调用协议权威 | Skill006、Production Card、QA | 变量库、质量参数库不得维护调度链路 |
| `docs/00-设计原则.md` | 01 生产系统 | 是，系统设计边界权威 | README、执行协议、权威归属表 | 单篇复盘、临时实验不得直接改设计原则 |
| Reasoning First 推导优先原则 | 01 生产系统 | 是，系统架构优先级权威；唯一出处为 `docs/00-设计原则.md` 原则0 | 平台样本学习、Evidence Schema、Knowledge Engine、Parser、Automation、Production Card | 协议中心、Parser、自动化脚本不得越过 Reasoning Grammar 直接定义字段或生产知识 |
| 中文字段优先规则 | 01 生产系统 | 是，字段命名与运行产物可读性权威；唯一出处为 `docs/00-设计原则.md` 原则13 | 所有 schema、JSON、模板、QA 报告、结构匹配产物 | 任何脚本或模板不得只新增英文关键字段 |
| `docs/知乎平台样本学习协议.md` | 02 知识系统 | 是，平台样本采集、拆解、统计和账号验证链路权威 | README、执行协议、ACTIVE_MANIFEST、ACTIVE规律快照 | 日常生产不得直接读取平台样本或未验证平台变量证据 |
| `skills/Skill006_知乎生产卡生成器.md` | 01 生产系统 | 是，生产卡生成协议权威 | README、总AI执行中心、Production Card模板 | Claude正文、复盘库不得维护生产卡生成规则 |
| `skills/Skill007_正文QA协议.md` | 01 生产系统 | 是，正文QA协议权威 | Production Card、Claude正文、发布终检 | 运行卡、复盘库不得改写QA标准 |
| `templates/知乎OS总控提示词.md` | 01 生产系统 | 是，总控提示词权威 | Codex日常生产、执行协议 | 生产卡、正文、复盘库不得维护总控提示词 |
| `templates/Claude正文生产Prompt.md` | 01 生产系统 | 是，Claude正文生产Prompt权威 | Production Card、Claude正文 | 知识库、复盘库不得维护正文Prompt |
| `templates/Production Card模板.md` | 01 生产系统 | 是，Production Card字段模板权威 | Skill006、Claude正文生产Prompt | 生产卡实例不得新增或删减模板字段 |
| Explanation Target（一致解释目标）字段定义 | 01 生产系统 | 是，归属现有 Production Card 字段：`读者真实困惑`、`因果追问链`、`因果追问终点`、`唯一核心判断`、`分段施工说明/推进关系` | Skill006、Claude正文生产Prompt、Skill007、Production Card 校验脚本 | 不得新增独立 Skill、Engine、流程节点、知识库或平行字段体系 |
| `templates/单次任务模板.md` | 01 生产系统 | 是，单次任务输入格式权威 | Codex日常任务、生产卡生成 | 生产卡、复盘库不得维护任务模板 |
| `docs/知乎内容质量参数库_V2.md` | 02 知识系统 | 是，质量参数权威 | 总AI执行中心、Skill006、QA | 生产协议只触发参数，不复制维护参数 |
| `runtime/ACTIVE_MANIFEST.md` | 02 知识系统 | 是，Codex日常执行快照清单权威 | Codex日常生产、Skill006、校验脚本 | Notion更新未发布到runtime前不得直接影响生产 |
| `runtime/知乎内容质量参数快照.md` | 02 知识系统 | 是，Codex日常参数执行权威 | Skill006、Production Card、QA | 未标记ACTIVE的Notion参数不得进入生产触发 |
| `runtime/知乎ACTIVE规律快照.md` | 02 知识系统 | 是，Codex日常规律执行权威 | Skill006、爆款规律提取 | 单篇复盘不得直接覆盖runtime规律 |
| `runtime/知乎结构库快照.md` | 02 知识系统 | 是，Codex日常结构执行权威 | 内容路由、Skill006、Production Card | Notion草稿结构不得直接进入生产 |
| `runtime/知乎账号画像快照.md` | 02 知识系统 | 是，账号画像执行快照权威 | 选题准入、选题扩展、案例选择、复盘样本优先级 | 不得新增 Production Card 字段，不得直接修改 Prompt |
| `production_variable_library.md`｜知乎内容变量参数库 | 02 知识系统 | 是，唯一内容变量权威库 | Skill006、Production Card、正文生产、平台样本学习、账号验证 | 不得新建平台变量库、账号变量库或第二套参数体系 |
| `l2_variable_records.md` | 02 知识系统 | 变量标注材料，不是生产权威 | 知乎内容变量参数库、L2.5变量验证 | 不得作为第二套账号变量库 |
| `l2_variable_validation.md` | 02 知识系统 | 变量验证材料，不是生产权威 | 知乎内容变量参数库、复盘系统 | 不得作为第二套账号变量库，不得把单次验证升级为稳定协议 |
| 结构库 / ACTIVE规律库 / 参数库 / 案例库 / 平台规则（Notion） | 02 知识系统 | 是，管理与审批权威 | runtime发布、周期复盘、版本升级 | Notion修改未发布到runtime前不得直接进入Codex日常生产 |
| `skills/Skill006_知乎生产卡生成器.md` 输出的 Production Card | 03 运行系统 | 是，单篇执行对象权威 | Claude正文、QA、发布终检、复盘 | 不得新建第二套Run数据库或任务系统 |
| 当前正文 | 03 运行系统 | 单篇运行产物，以生产卡为准 | QA、发布状态、单篇复盘 | 正文不得反向修改Production Card |
| 生产状态 / 发布状态 | 03 运行系统 | 运行状态权威，以生产卡记录为准 | 首页待办视图、复盘系统 | 复盘库不得替代运行状态 |
| `data/L0_README.md` | 04 复盘系统 | 是，L0内容资产口径权威 | L0内容资产总账、报告、复盘 | 生产系统不得维护L0字段口径 |
| `data/l0_content_assets.csv` | 04 复盘系统 | 数据来源，内容资产总账权威 | L1样本、L2验证、收益报告、单篇复盘 | 首页和生产卡只引用，不复制维护 |
| `data/l1_sample_list.csv` | 04 复盘系统 | 是，L1分层样本权威 | L2变量验证、实验复盘 | L0总账不得直接形成规律结论 |
| `data/production_article_map.csv` | 04 复盘系统 | 是，Production ID 与 article_id 映射权威 | 参数调用日志、L0内容资产总账、单篇复盘 | 不得在报告里另建长期映射表 |
| `docs/单篇复盘执行协议.md` | 04 复盘系统 | 是，单篇复盘执行口径权威 | 参数调用日志、Observation、周期复盘 | 临时报告不得替代日常复盘协议 |
| `reports/l0_asset_report.md` | 04 复盘系统 | 报告，不替代数据源 | L0检查、收益回看 | 不得反向修改L0口径 |
| `reports/l1_sample_report.md` | 04 复盘系统 | 报告，不替代数据源 | L1样本检查、L2验证 | 不得替代L1样本清单 |
| `reports/earnings_backfill_report.md` | 04 复盘系统 | 报告，不替代数据源 | 收益数据回填、复盘判断 | 不得替代内容资产总账 |
| `reports/production_experiment_001.md` | 04 复盘系统 | 单次实验记录 | 复盘系统、后续规律验证 | 不得升级为稳定生产协议 |
| `知乎TOP10事实包_V1_给GPT复盘.md` | 04 复盘系统 | 复盘事实包 | 单篇复盘、规律验证、知识更新 | 不得替代Notion知识层 |
| `scripts/validate_production_card.py` | 01 生产系统 | 工具，生产卡校验权威 | Skill006、生产卡模板 | 不得成为任务系统 |
| `scripts/validate_l0_assets.py` | 04 复盘系统 | 工具，L0数据校验权威 | L0内容资产总账、L0报告 | 不得修改L0字段口径 |
| `scripts/generate_l1_sample_list.py` | 04 复盘系统 | 工具，L1样本生成权威 | L0内容资产总账、L1样本清单 | 不得直接生成规律结论 |
| `scripts/generate_l0_report.py` | 04 复盘系统 | 工具，L0报告生成权威 | L0内容资产总账、L0报告 | 不得替代数据源 |
| `CHANGELOG.md` | 00 首页 | 变更记录 | 全部功能区 | 不得维护业务知识或执行协议 |

## 禁止事项

- 不复制数据库。
- 不新建第二套任务系统。
- 不为了目录整齐去删除、合并历史数据。
- 不把单篇经验直接升级为稳定协议。
- 不让正文、复盘或报告反向修改 Production Card。
