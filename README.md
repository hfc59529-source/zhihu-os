# 知乎盈利系统

## System 职责

知乎盈利系统负责知乎内容生产、平台样本学习、账号数据验证与收益反馈闭环。只有顶层整体称为 System（系统），内部功能单元统一称为 Module（模块）。

当前日常生产主链：

```text
选题包（Question Package）
↓
Top3 Context
↓
现实（Reality）
↓
主认知落差（Main Gap）
↓
认知转换（Transformation）
↓
语义冻结门（Semantic Freeze Gate）
↓
Analyzer
↓
Structure Matcher
↓
Router
↓
Reasoning Path（推理路径，Compiler 内部中间表示，非新增 Layer）
↓
Claude Writer
↓
QA
↓
User Review
↓
Release
↓
Publish
↓
Metrics
```

语义冻结门（Semantic Freeze Gate）：现实、主认知落差、认知转换三项冻结成功后，才能进入 Analyzer；否则禁止进入正文生产，返回【选题包需要退回语义分析】。

Semantic Freeze Gate 成功后，现实、主认知落差、认知转换成为本次 Production 的 Single Source of Truth（唯一事实来源）。Analyzer、Structure Matcher、Router、Writer、QA 不得修改；如发现 Semantic 错误，只能返回【退回语义分析】，不得自行修正。

详见 [`docs/内容架构总则.md`](docs/内容架构总则.md) 与 [`templates/Claude正文生产Prompt.md`](templates/Claude正文生产Prompt.md)。

Reasoning Path（推理路径）：Router 之后、Writer 之前，由 Runtime Assembly 内部生成，把已冻结的 Reality / Main Gap / Transformation 编译成正文推导顺序（读者原有认知 → 错误推论 → 认知动摇点 → 真正机制 → 新认知）。它是 Compiler 内部中间表示，不是新的 Layer、不是 Card，只负责推导顺序，不负责表达；Writer 必须按这个顺序展开正文，不得重新推导。详见 [`docs/知乎OS Compiler V1.md`](docs/知乎OS%20Compiler%20V1.md) 第 4.4 节。

Production Card 已退役，不恢复；本链不新增对象、不新增流程，只是把《内容架构总则》四层正式接入生产入口。

生产链原有的记录与维护动作仍然保留：Codex 记录参数调用日志，必要时维护参数 / Prompt / 调用规则。

核心原则：

```text
Reasoning First
Compiler First
决策层永远不讨论表达
表达层永远不修改决策
任何规则只有一个权威来源
系统只允许单向流动
```

Reasoning First 表示：任何自动化之前，先定义推导；任何字段设计之前，先定义思维。系统建设顺序必须是 Reasoning Grammar → Evidence Schema → Knowledge Engine → Parser → Automation。

详见 [`docs/知乎OS Compiler V1.md`](docs/知乎OS%20Compiler%20V1.md)。

内容语义架构（现实／认知落差／认知转换／平台表达）详见 [`docs/内容架构总则.md`](docs/内容架构总则.md)，它是 Compiler 的语义上游，不替代 Compiler。

系统设计边界详见 [`docs/00-设计原则.md`](docs/00-设计原则.md)。

当前系统进入第二阶段：

```text
平台高表现样本负责发现规律
↓
本账号发布数据负责验证规律
↓
ACTIVE规律库负责日常生产触发
```

自己的历史文章不再作为主要规律发现对象，只作为验证规律是否适合本账号的实验数据。

## 顶层导航

五个模块只是导航和归属，不是新建五套数据库，也不是五个独立子系统。

| Module | 主要承载内容 |
| --- | --- |
| 00｜首页 | 收益指标、当前实验、唯一生产入口、待办视图 |
| 01｜生产模块 | MASTER、内容路由、结构执行、生产协议、表达、QA、终检 |
| 02｜知识模块 | 结构库、ACTIVE规律库、参数库、案例库、平台规则 |
| 03｜运行模块 | 选题包、当前正文、生产状态、发布状态 |
| 04｜复盘模块 | 内容资产库、历史基线、代表样本、候选规律、收益数据 |
| 05｜治理模块 | 证据门槛、状态流转、权威归属、参数升级与降级 |

模块边界：

```text
知乎盈利系统
├── 生产模块
├── 知识模块
├── 运行模块
├── 复盘模块
└── 治理模块
```

复盘模块负责采集结果、建立历史基线、筛选代表样本、形成候选规律，并把验证结论反馈给知识模块和生产模块。

权威归属以 [`docs/知乎OS权威归属表.md`](docs/知乎OS权威归属表.md) 为准。

## 五句话原则

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

任何页面都必须回答：我属于哪一句。回答不了，说明放错地方。

## 唯一交接对象

选题包是当前日常生产主链的唯一交接对象。选题包来源允许两种：Codex 采集，或用户手动提供（User Manual），两者权威完全一致，都进入同一条生产主链。

Codex 生成选题包后停止；Claude 根据选题包调用参数、推理并生成正文；GPT / 人工审核参数和正文归因。

## 运行模式纪律

知乎OS默认分为两种模式，生产和系统研发必须分离。

模式一：日常生产（默认）

目标：最快速度产出高质量正文。

```text
问题
↓
主变量
↓
一句核心机制
↓
正文
↓
发布
↓
记录数据
```

日常生产过程中禁止修改协议、禁止新增参数、禁止优化 Prompt、禁止重构系统/知识资产。

模式二：系统升级（条件触发）

仅满足以下任一条件时启动：

1. 连续 3 篇出现同一种问题。
2. 数据验证证明某个规律失效。
3. 新发现跨题型通用规律。

除此之外，一律禁止修改系统。所有系统升级必须遵守：先验证，再抽象。

## 五层架构

L1 协议层（Git/MD）
回答：AI 应该怎么干。

L2 知识层（Git docs/templates 规则源 / runtime 执行快照）
回答：AI 依据什么干。

L3 执行层（Codex）
回答：今天具体干什么。

L4 平台层（知乎/头条）
回答：真实反馈是什么。

L5 学习层（Git 复盘资产：`data/`、`reports/`）
回答：下次如何优化。

## 三层数据源

L1｜平台样本
回答：知乎平台上什么变量正在高频生效。

L2｜账号实验
回答：这些平台变量证据在本账号是否有效。

L3｜ACTIVE变量
回答：哪些已验证变量允许 Claude 在正文生产中调用。

唯一内容变量权威源是 `production_variable_library.md`，显示名称为《知乎内容变量参数库》。日常生产只触发该库中 `当前状态=ACTIVE` 且 `触发资格=是` 的变量。L1 和 L2 只在系统升级、规律验证和周期复盘时回写同一变量记录。

## 工作流程

```text
截图
↓
Codex
↓
读取原问题
↓
检查方向与重复
↓
补充必要事实
↓
生成选题包
↓
停止，等待 Claude 接管
```

正文生产由 Claude 接管：

```text
选题包
↓
调用参数
↓
推理
↓
生成正文
↓
GPT / 人工审核
↓
参数调用日志
↓
本地记录
↓
周期复盘
↓
回写 Git 规则源（`docs/` / `templates/` / `production_variable_library.md`）并通过 `scripts/release_runtime.py` 发布下一版 runtime
```

## 账号画像

账号画像是长期低频数据层，用来指导选题和复盘，不直接改 Prompt，不新增正文执行字段。

```text
账号画像（长期）
↓
选题
↓
选题包
↓
正文
↓
收益数据
↓
L0-L3复盘
```

高频使用两项：

1. 转化内容排行：每月更新新增关注 TOP20，用于建立关注转化排行榜，异常样本进入 L3 深度事实包。
2. 兴趣分布：季度或半年更新，用于校准选题方向。

其它画像字段，包括性别、年龄、地域、关注来源和活跃分层，作为账号基线画像，不参与每篇正文复盘。

## Codex 职责定义

Codex 有两类职责：

1. 单篇生产前：只做选题采集与入库。
2. 长期系统层：维护参数库、知识库、样本库和参数调用日志。

Production Card 已退出日常生产主链。Codex 不生成 Production Card，不写正文，不调表达，不审正文，不修改正文，不做单篇阅读体验优化。

## Codex 选题采集完成定义

收到以下任一输入时，Codex 自动进入选题采集模式：

1. 一个知乎问题。
2. 一个或多个知乎问题截图。
3. 一个真实知乎问题链接。
4. 用户要求 Codex 自行去知乎采集、挑选或推荐今日可回答问题。

采集入口分为两类：

```text
用户输入型：用户发问题 / 截图 / 链接
系统自采型：Codex 从知乎入口采集候选并推荐一题
```

两个入口只影响选题来源。题目选定后，Codex 只生成选题包并保存候选池。

Codex 任务的默认完成标准是生成标准化选题包：

```text
问题识别
↓
读取原问题
↓
判断是否符合账号方向
↓
判断是否值得回答
↓
必要背景补充
↓
历史重复检查
↓
生成选题包
↓
保存到候选池
↓
停止，等待 Claude 接管
```

Codex 不生成 Production Card，不提炼核心观点，不设计正文结构，不生成正文。

## 模式路由

选题采集模式触发词或输入：

- 采集选题
- 推荐问题
- 找题
- 入库
- 用户发送知乎题目、题目截图或问题链接
- 用户要求 Codex 自行去知乎采集、挑选或推荐今日可回答问题

行为：自动生成标准选题包，保存到 `data/topic_candidates/YYYY-MM-DD/`，并更新 `data/Topic_Pool.md` 索引；不自动生成 Production Card 或正文。

后续生产模式：

选题包完成后，Claude 直接调用参数、推理并生成正文；GPT / 人工再按固定清单审核。

审计模式触发词：

- 检查流程
- 审计系统
- 检查参数调用
- 不写正文
- 检查参数调用

行为：只执行用户指定的审计范围，不自动调用 Claude 生成正文。

禁止因为输入是截图就默认进入审计模式。判断依据是用户意图，不是输入形式。

所有执行协议以 `/docs` 为准；Codex 选题采集以 `docs/Codex选题采集协议.md` 和 `templates/选题包模板.md` 为准。Git（`docs/` / `templates/` / `production_variable_library.md`）是管理权威，经治理批准后由 `scripts/release_runtime.py` 审批并发布下一版 runtime；Notion 已退出 Production Authority Chain，降级为 Reference / Archive，详见 `docs/知乎OS权威归属表.md`。

## 生产接口

选题包完成后，后续正文生产必须由 Claude 接管。

Codex 负责读取问题、筛选选题、检查重复并输出固定格式选题包。

Trigger 能力不新增系统、入口或生产步骤：它已内置于 `production_variable_library.md` 每条变量的“适用题型 / 触发条件 / 禁用边界”字段，由变量匹配规则本身完成。Trigger / Pattern / Evidence 三份文件保留为研究草稿，不进入 runtime，不进入 Skill006 固定读取。

Claude 负责根据选题包调用参数、推理并生成正文，不直接读取 runtime，不新增变量，不虚构案例。

GPT / Codex 不直接生产文案，不重写正文。Codex 默认只交付选题包。

## 参数调用日志

Codex 负责维护 `data/parameter_call_log.md`。

每篇文章记录：

- Production ID。
- 选题编号。
- Claude 声称调用参数。
- GPT / 人工确认实际生效参数。
- GPT / 人工审核归因。
- 发布后阅读、点赞、收藏、收益。
- 是否需要回写参数库。

参数调用日志以 GPT / 人工审核结果为准，不以 Claude 自报为准；只记录调用事实和结果，不反推正文写法，不替正文做表达优化。

## Claude 正文生成

Claude 根据选题包调用参数、推理并生成正文。

Claude 不生成 Production Card，不要求 Codex 补 Card，不直接读取 runtime，不新增参数。

## GPT 审核

GPT / 人工审核固定使用 [GPT审核清单.md](/Users/huangsheng/Documents/知乎系统/templates/GPT审核清单.md)。

审核只看两张清单：

- 参数审核。
- 正文审核。

最终只输出：

- PASS。
- 正文问题。
- 系统问题。

归因口径：

- Claude 没有执行已有参数、遗漏选题包事实、正文开头/节奏/表达/收尾未达标，属于正文问题，退回 Claude 修改正文。
- 参数库缺少必要规则、Claude Prompt 指令冲突、调用规则无法执行，才可能属于系统问题。
- 单篇执行问题不能直接升级为系统问题；连续 3 篇出现同类问题，且 GPT / 人工确认不是正文执行偏差后，才允许交给 Codex 修复系统。
