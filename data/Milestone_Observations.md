# Milestone Observations

用途：记录进入 ZH-MILESTONE-010 统一复盘的观察项。这里不写入参数库，不修改协议，只保存待判断问题、平台验证过程和最终结论。

对象类型：Observation（观察）。与 `production_variable_library.md` 的 Parameter（参数）对象职责分离——Observation 只描述"观察到了什么、怎么验证、证据是否支持"，不描述"能不能进入生产"。Observation 状态和 Parameter 状态是两条独立状态链，不共用状态名，不发生对象类型变异（一条 Observation 不会自己变成一条 Parameter 记录）。

## Observation 生命周期

```text
OPEN
↓
VALIDATING
↓
SUPPORTED ──→ CLOSED
REJECTED ─────→ CLOSED
INCONCLUSIVE ─→ CLOSED
```

| 状态 | 定义 |
|---|---|
| OPEN | 刚从审核或生产中记录的问题，尚未开始验证 |
| VALIDATING | 正在收集平台样本或账号样本证据 |
| SUPPORTED | 证据支持该观察成立 |
| REJECTED | 证据不支持，观察不成立 |
| INCONCLUSIVE | 证据不足以下结论，且样本来源已穷尽或超出观察窗口 |
| CLOSED | 观察结束，不再更新（无论最终结论是 SUPPORTED / REJECTED / INCONCLUSIVE） |

`SUPPORTED` 不等于自动创建或修改 `production_variable_library.md` 中的 Parameter 记录——是否创建/推进 Parameter，是治理判断的下一步，由 [系统治理原则.md](../docs/系统治理原则.md) 的规则决定，两者靠 ID 引用连接。

参数缺口类 Observation 必须保留用户审核闭环。审核结果只允许四种：

| 审核结果 | 定义 | 后续动作 |
|---|---|---|
| 驳回 | 已有参数可以解释，或证据不足 | 关闭缺口，不进入参数库 |
| 合并 | 缺口本质属于已有参数 | 填写归入参数 ID，不新增参数 |
| 候选参数 | 用户批准进入候选参数前置流程 | 填写候选参数编号，进入 Candidate 前置验证 |
| 正式参数 | 用户明确批准且证据链充分 | 填写正式参数编号，极少使用，仍需记录证据引用 |

同类缺口必须累计重复次数，不得凭单篇高赞回答直接升级。

编号规则：

- 参数缺口：`Gap-001`
- 候选参数：`Candidate-001`
- 正式参数：`PD-09` / `RR-02` / `CR-01`

## Observation 治理边界

Observation 是审核问题和参数修改之间的隔离层。

固定闭环：

```text
生产
↓
审核
↓
Observation（OPEN）
↓
平台验证（VALIDATING）
↓
结论（SUPPORTED / REJECTED / INCONCLUSIVE → CLOSED）
↓
SUPPORTED 时，判断是否创建或推进 Parameter 记录
↓
更新参数库（如适用）
↓
记录变更
```

执行规则：

1. 审核发现问题，只写 Observation（状态 OPEN）。
2. 未完成平台验证（未进入或走完 VALIDATING），不改正式参数。
3. 结论为 REJECTED 或 INCONCLUSIVE，Observation 关闭（CLOSED），不进入参数库。
4. 结论为 SUPPORTED，才可能修改 `production_variable_library.md` 对应参数字段。
5. 每次参数修改必须在 Parameter 记录的"证据引用"字段关联 Observation ID。
6. 不新增独立 Trigger、Evidence、Change Log 系统。

标准字段：

```text
Observation ID：
Gap ID（如为参数缺口）：
Source（如为参数缺口）：高赞Top3 / 用户发布结果 / 人工审核 / 老师样本 / 历史数据库 / 评论区 / 数据复盘
对应内容 ID：
题目：
审核来源：
问题类型：
关联 Parameter ID（如已存在对应参数记录）：
问题描述：
初步修正意见：
生命周期状态：OPEN / VALIDATING / SUPPORTED / REJECTED / INCONCLUSIVE / CLOSED
缺口状态（如适用）：待审核 / 已审核
审核结果（如适用）：未审核 / 驳回 / 合并 / 候选参数 / 正式参数
审核说明：
归入参数 ID（审核结果为合并时必填）：
候选参数 ID（审核结果为候选参数时必填）：
正式参数 ID（审核结果为正式参数时必填）：
重复次数：
重复证据引用：
平台证据：
最终结论：
处理动作：
```

问题类型限定为：

- 结构问题
- 参数触发错误
- 触发条件错误
- 禁用边界缺失
- 表达问题
- 参数缺口

## 历史记录状态口径说明

以下两条 Observation 建立于本文件采用正式生命周期状态之前，沿用当时的"Open / Closed"二态记法。按新口径对照：旧记法的 `Open` 对应 `OPEN`（尚未完成验证）或 `VALIDATING`（已有部分证据但未终结），旧记法的 `Closed` 对应 `CLOSED`（终态），具体结论仍以原文叙述为准，不倒填 SUPPORTED / REJECTED / INCONCLUSIVE 标签。

## Observation-01：尾段重复压缩

状态：Closed（002-010 样本期结束，结论见下方"样本结束"部分）

证据等级：样本不足以支撑系统性模式判断，判定为局部巧合，不进入 Active。

定义：正文结尾已经通过分点或完整句完成信息传递后，又在短距离内用压缩句重复相同信息，且没有产生新的抽象或推进。

当前证据：

| Production ID | 是否出现 | 证据位置 | GPT Decision |
|---|---|---|---|
| ZH-20260801-006 | YES | 结尾 15 行内堆叠短判断，两对语义重复 | Approve |
| ZH-20260801-007 | YES | 结尾“三件事”分点后 6 行内再次压缩重复其中两点 | Approve |
| ZH-20260801-008 | NO | 结尾同样是"分点 + 总结"结构，但总结句为新抽象（"忠诚要换复利，跳槽要换台阶"未换词重复前文，而是用全文贯穿的核心隐喻做真正压缩），未构成 Issue | - |
| ZH-20260801-009 | NO | 结尾"四问"首次以设问形式出现，紧接的连接句是新判断而非重复；连续第二篇未复现 | - |
| ZH-20260801-010 | NO（另有一条不同性质的"首尾呼应"观察，已在 Audit_Report.md 中单独说明，不计入本观察项） | - | - |

**样本结束，Observation-01 最终统计（002-010，共 9 篇纳入新流程，其中结尾结构可比对的 5 篇：006/007/008/009/010）**：

| 结果 | 数量 |
|---|---|
| YES（复现） | 2（006、007） |
| NO（未复现） | 3（008、009、010） |

**010 复盘问题回答**：

- 这是否只是 006/007 局部巧合？**是**。5 篇可比对样本中仅前两篇（006、007）出现，此后连续 3 篇（008/009/010）均未复现，且 006/007 出现时是同一天连续生产（时间/上下文相邻），不排除是当时同一批生成上下文的局部现象，而非稳定的系统性模式。
- Production Card 是否隐含"分点之后必须再压缩总结"的施工倾向？**证据不支持**。008/009/010 的 Card 同样包含"结尾形成判断"类段落要求，但均未导致同类重复，说明问题不在 Card 模板本身。
- 治理结论：**不需要修改 Production Card 施工规范，不需要新增正文参数**。维持现状，作为已关闭的观察项存档，若未来样本中再次连续出现，重新开启观察而非假设已解决。

**状态更新：Observed → Closed（无需升级为参数或协议变更）**

## Observation-02：Card字段重叠

状态：Open

证据等级：待观察，未进入 Active。

定义：Production Card 中多个字段表达同一核心判断，导致 Draft 忠实执行 Card 后在首尾形成高度相似的判断表达。该现象不等同于 Draft 短距离重复，不直接构成正文 Issue。

当前证据：

| Production ID | 是否出现 | 证据位置 | GPT Decision |
|---|---|---|---|
| ZH-20260801-010 | YES | Card 的“唯一核心判断”与段落 7“具体内容”表达同一判断；Draft 首尾忠实落地，形成首尾呼应 | Clean / Final Validation PASS |

当前判断：

- 这是 Card 层观察，不是 Draft 层 Bug。
- 010 单篇证据不足，不修改 Card 模板或施工规范。
- 011/012/013 若继续出现，再判断是否进入治理。

## Observation-03：ACTIVE 权威文件间 Production Card 架构版本不一致

```text
Observation ID：Observation-03
Gap ID（如为参数缺口）：不适用
Source（如为参数缺口）：人工审核
对应内容 ID：TOPIC-20260809-002 / ZH-20260809-002（触发本次审核，非本观察的证据对象）
题目：不适用（本观察为系统一致性问题，非单篇正文问题）
审核来源：人工审核
问题类型：结构问题（当前问题类型限定表六项中无"跨文件权威/架构版本冲突"类别，暂归入结构问题，最贴近但不完全对应，需治理评审确认是否需要扩类型）
关联 Parameter ID（如已存在对应参数记录）：不适用
问题描述：
以下七个冲突点，涉及八个文件。这八个文件并非全部标注 ACTIVE——其中 Skill007 自身标注 `Status：LEGACY_RETIRED`，但仍被 `docs/知乎OS权威归属表.md` 列为"正文QA协议权威"并被其他文件引用。命题应精确为：当前系统中多个 ACTIVE 权威文件，及其仍被引用/声明为权威的 LEGACY_RETIRED 对象，对"Production Card 是否仍属于正式生产链"存在直接文本冲突，非推断：
1. `docs/知乎OS执行协议.md` 与 `docs/08_总AI执行中心.md`：明确 Production Card 已退出 Codex 日常生产主链。
2. `templates/Claude正文生产Prompt.md`（V5，ACTIVE）：唯一施工依据为选题包 + ACTIVE 变量，不生成 Production Card。
3. `skills/Skill007_正文QA协议.md`：自我标注 `Status：LEGACY_RETIRED`，声明"本协议不再作为日常正文审核入口"。
4. `docs/知乎OS权威归属表.md`：页首声明 Production Card 已退出主链，但表体第54/55/57/58/71/72行仍列 Skill006、Skill007、Production Card模板、"当前正文以生产卡为准"为现行权威。
5. `production_variable_library.md`（ACTIVE，唯一内容变量权威库）：第109-149行 Trigger Matrix 通用规则将"是否实际激活"定义为"写入 Card"，且每次生产必须记录 Experiment ID 等字段，Trigger 与 Activation 为连续同一条协议，非独立层级。
6. `docs/00-设计原则.md`：Compiler 主链仍含 Production Card 节点；原则九、十、十二仍将 Production Card IR 列入正式链路。
7. `docs/系统治理原则.md` 自身：变更日志 V1.5（第424行）仍写"Production Card 为正文阶段唯一内容权威"，说明治理原则文件本身也是冲突证据的一部分，而非冲突之外的裁判者。
初步修正意见：
暂不提出。待验证"上述七个冲突点涉及的八个文件是否确实同时构成当前有效权威，并且对同一生产对象给出互不兼容的规则"这一命题是否成立后，再进入治理判断；不预设 Precedence/Supersession Rule 或其他具体解法。
生命周期状态：REJECTED → CLOSED
缺口状态（如适用）：不适用
审核结果（如适用）：不适用
审核说明：
当前未发现该正文调用 Skill006、Skill007 或生成 Production Card 的证据；因此尚不能建立本观察与该正文结果之间的因果关系，也不能反向声称该正文"仅使用"了哪些具体机制——完整执行 Trace 未经证明（本条结论不受本次 REJECTED 影响，继续有效）。
归入参数 ID：不适用
候选参数 ID：不适用
正式参数 ID：不适用
重复次数：1（首次记录）
重复证据引用：不适用
平台证据：不适用（本观察不依赖平台/账号样本，依赖文件文本本身；验证方式为治理评审逐条核对七个冲突点涉及的八个文件原文，以及 `runtime/ACTIVE_MANIFEST.md`、`backups/20260731-130705/` 发布快照、`scripts/validate_runtime_consistency.py` 实测结果、git 提交历史（含 commit `78aa21f`）与治理批准记录检索结果）
治理评审结论（2026-08-09）：
验证命题——"上述七个冲突点涉及的八个文件是否确实同时构成当前有效权威，并对 Production Card 是否属于正式生产链给出互不兼容的规则"——不成立。逐条核对结果：
1. `docs/知乎OS执行协议.md`、`docs/08_总AI执行中心.md`：在 `ACTIVE_MANIFEST.md` 追踪清单内，当前 SHA256 与 manifest 记录失配（`validate_runtime_consistency.py` 实测 Fail）；`backups/20260731-130705/` 保存的、SHA 与 manifest 一致的发布版本原文仍为 Card-based（要求生成/校验/交付 Production Card）。当前"已退役"文本是未发布工作副本，不具备 Runtime 权威。
2. `templates/Claude正文生产Prompt.md`：不在 `ACTIVE_MANIFEST.md` 追踪清单内，其"Status：ACTIVE"为文件自我标注，未经治理批准或 runtime 发布程序确认，不构成有效权威。
3. `skills/Skill007_正文QA协议.md`：同样不在 manifest 追踪清单内，其 LEGACY_RETIRED 状态未经发布程序确认，但也不构成对已发布 runtime 的篡改。
4. `docs/知乎OS权威归属表.md`：不在 manifest 追踪清单内，页首与表体自相矛盾，属编辑遗留缺陷，不代表两个同时生效的权威。
5. `production_variable_library.md`：在 manifest 追踪清单内，SHA 已失配，同属未发布工作副本，不具备 Runtime 权威。
6. `docs/00-设计原则.md`：不在 manifest 追踪清单内；内容与唯一已发布 runtime（07-31 Card-based V3.0-TEACHER）一致，不构成冲突方。
7. `docs/系统治理原则.md`：V1.5 变更日志是 2026-08-01 的历史记录，与已发布 runtime 一致，是"尚未被后续未批准决策污染"的正确状态，不构成冲突方。
结论：截至审计时点，唯一有发布证据支持的有效 Runtime 是 2026-08-01 13:07:05 发布的 Card-based V3.0-TEACHER；七个冲突点中并非八个文件同时具有当前 Runtime 权威，"有效权威之间存在架构冲突"这一命题不成立。
最终结论：REJECTED（文本冲突客观存在，但冲突文件并非同时构成当前有效权威；原命题不成立）→ CLOSED。
处理动作：不修改任何正式协议或参数记录，不建立 Precedence/Supersession Rule（该需求随原命题一并解除）。本次审计过程中发现的另一个命题——"未经治理批准、未发布的设计工作副本被当作现行规则标注/使用，且 `validate_runtime_consistency.py` 这道 Runtime consistency gate 未能阻止这种情况被继续引用（含今日 TOPIC-20260809-002 / ZH-20260809-002 的生产实际引用了未发布版本的 `templates/Claude正文生产Prompt.md`）"——不属于本 Observation 范围，是否另立新 Observation 记录，留待下一步治理动作单独决定，不在本次收尾中一并处理。
```

## Observation-04：Governance Authority Registry 与 Runtime Publication Boundary 不一致

```text
Observation ID：Observation-04
Gap ID（如为参数缺口）：不适用
Source（如为参数缺口）：人工审核
对应内容 ID：不适用（本观察为系统一致性问题，非单篇正文问题；发现契机为 08-10 效果数据复盘讨论中途）
题目：不适用
审核来源：人工审核（用户 + 助手交叉核对 runtime/ACTIVE_MANIFEST.md 本地/远端与 docs/知乎OS权威归属表.md）
问题类型：结构问题（当前问题类型限定表六项中无"治理权威文件未纳入 Runtime 发布边界"类别，暂归入结构问题，最贴近但不完全对应，需治理评审确认是否需要扩类型；与 Observation-03 同源问题类型缺口）
关联 Parameter ID（如已存在对应参数记录）：不适用
问题描述：
Evidence A — Authority Registry：`docs/知乎OS权威归属表.md` 第92行明确声明 `docs/系统治理原则.md` 为"05 治理模块，是，证据门槛、状态流转和系统修改条件权威"，作用范围含"参数库、Observation、复盘模块、生产模块"。
Evidence B — Runtime Manifest：本地 `runtime/ACTIVE_MANIFEST.md`（`Status: TRIAL`）的六个 Partition（Compiler Authority / Protocol Docs / Node Execution Assets / Parameter & Knowledge Snapshots / Governance Infrastructure / Historical Asset Tools）均未列出 `docs/系统治理原则.md`，未被 sha256 锁定发布。
Evidence C — Manifest 落后 HEAD：该 TRIAL manifest 记录 `Published At: 2026-08-09 18:41:36 UTC`、`Based On Commit: 66b3ca5`，但当前分支 `compiler-v1-runtime-alignment` 的 HEAD 为 `77b7831`，中间另有 `dd156f2`、`02529cf`、`fd21879` 三次提交未被本次 TRIAL 覆盖。
Evidence D — 远端落差：`origin/main` 上的 `runtime/ACTIVE_MANIFEST.md` 为 `Status: DRAFT`，`Published At`/`Based On Commit` 均为空，所有 Partition 内 sha256 字段为空——与本地/`origin/compiler-v1-runtime-alignment` 分支上有内容的 TRIAL manifest 是两个不同状态，不可互相引用。
Impact：
由 Evidence A+B+C+D 共同构成的结果是——本次讨论中反复援引的"Observation/Parameter 生命周期规则"（OPEN→VALIDATING→SUPPORTED/REJECTED/INCONCLUSIVE→CLOSED 等）及 Compiler §12/§13 关于 Learning Plane 的约束，其 Runtime execution eligibility 目前无法唯一判定：Authority Registry 声称它是治理权威，但 Runtime Manifest 既未锁定该文件本身，其 Based On Commit 也已落后当前 HEAD，且远端唯一已知发布态是空 DRAFT。
初步修正意见：
暂不提出。本条不预设"治理规则是否必须进入 Manifest 锁定"这一架构问题的答案，留给治理评审通过 Q1/Q2 两问逐步回答：
Q1：`docs/系统治理原则.md` 是否属于 Runtime 必须锁定的执行依赖？若 YES，应补入 Manifest Partition 或另立被 Manifest 锁定的正式 Governance Runtime Asset；若 NO，需说明 Authority Registry 与 Runtime 权威判定标准为何允许分离，以及运行时实际引用哪个版本。
Q2：仅在 Q1 结论明确后，才判断当前 HEAD（`77b7831`）是否具备重新执行 `scripts/release_runtime.py`、将 TRIAL 对齐到 HEAD 的发布资格。
生命周期状态：OPEN
缺口状态（如适用）：不适用
审核结果（如适用）：未审核
审核说明：不适用（尚未进入审核）
归入参数 ID：不适用
候选参数 ID：不适用
正式参数 ID：不适用
重复次数：1（首次记录）
重复证据引用：不适用
平台证据：不适用（本观察依赖文件文本与 git 状态本身，不依赖平台/账号样本；验证方式为治理评审核对 `docs/知乎OS权威归属表.md`、`runtime/ACTIVE_MANIFEST.md`（本地/`origin/compiler-v1-runtime-alignment`/`origin/main` 三处）、`git log --oneline -- runtime/ACTIVE_MANIFEST.md`、`scripts/validate_runtime_consistency.py` 实测结果）
最终结论：待治理评审
处理动作：
本条 OPEN 期间禁止以下三项动作：
1. 不据此修改 Manifest Partition（不擅自把 `docs/系统治理原则.md` 加入或排除某个 Partition）；
2. 不直接执行 `scripts/release_runtime.py` 重新 release（避免隐含对 HEAD 发布资格和当前 Partition 边界正确性的未授权判断）；
3. 不据此修改 `docs/系统治理原则.md` 本身。
本 Observation 关闭前，08-10 效果数据（ZH-20260809-001 等）相关的 Observation/Hypothesis/Failure Pattern 状态判定同步搁置，不因本条 OPEN 而单独另开阻塞流程，两者并行但不相互提交对方结论。
```

## Observation-05：Paid/Costly Signal：低支付能力用户在获得深度干预后主动产生象征性付费

```text
Observation ID：Observation-05
Gap ID（如为参数缺口）：不适用
Source（如为参数缺口）：用户私信反馈 / 人工收入补记
对应内容 ID：不适用（私域互动与回答后的用户反馈，未绑定单篇公开内容 ID）
题目：不适用
审核来源：用户截图 + 人工判断
问题类型：参数缺口（当前问题类型限定表无"咨询价值验证信号/付费行为证据"类别，暂归入参数缺口，但本条不直接创建参数）
关联 Parameter ID（如已存在对应参数记录）：不适用
问题描述：
2026-08-23，知乎用户“刘利珠”在获得职场处境分析与个人边界建议后，通过微信发出 20 元红包，附言为“请您喝杯奶茶，交个朋友”，并继续表达“前辈”“谢谢您的理解”“等我慢慢恢复了，有足够才……”等关系维护与恢复后再补偿的意向。

该行为不适合被解释为标准咨询收入案例，金额过小，且用户主动将其包装为“喝杯奶茶/交个朋友”，而非等价咨询费。但它适合作为 Paid/Costly Signal：在疑似支付能力较弱的用户身上，仍发生了真实成本支出，说明此前回答并非仅获得情绪性认可，而是进入“被理解、被分析、被指导后愿意付出真实成本”的层级。

初步修正意见：
不将本条作为“知乎咨询已可规模化赚钱”的证据；应记录为咨询价值早期验证信号。后续若出现重复样本，可单独统计“深度干预后象征性付费/补偿/私域关系建立”的频率、金额、触发语境和对应回答结构。
生命周期状态：SUPPORTED
缺口状态（如适用）：待审核
审核结果（如适用）：未审核
审核说明：单例行为证据已发生，支持“存在咨询价值信号”；但不足以支持收入模型、定价模型或产品化咨询入口判断。
归入参数 ID：不适用
候选参数 ID（审核结果为候选参数时必填）：不适用
正式参数 ID（审核结果为正式参数时必填）：不适用
重复次数：1（首次记录）
重复证据引用：
- `data/revenue_observations.csv` 中 `manual_wechat_red_packet_rmb` 记录
- `reports/daily_review_20260823_zhihu_capture_recap.md` 的“人工收入补记 / 咨询价值信号”记录
平台证据：
- 微信红包截图显示：知乎用户“刘利珠”发出 20 元红包，留言“请您喝杯奶茶，交个朋友”，状态为已领取并存入零钱。
- 对话中用户使用“前辈”“谢谢您的理解”等表达，并说明“等我慢慢恢复了，有足够才……”，指向支付能力约束下的象征性感谢与关系建立。
最终结论：
SUPPORTED。该样本验证的是“深度职场干预可触发真实成本信号”，而非“咨询业务收入成立”。行为证据等级高于点赞、收藏、评论，低于稳定复购或明确标价咨询付费。
处理动作：
1. 保留 `data/revenue_observations.csv` 中 20 元人工收入记录，但不并入知乎盐粒收益判断。
2. 在 2026-08-23 复盘中将该样本标记为 Paid/Costly Signal。
3. 暂不修改正式参数库、收益目标参数映射或咨询产品化协议；等待重复样本后再评估是否形成候选参数或独立咨询信号表。
```

## Observation-06：Revenue Density：高 Self-Relevance 内容可能获得更高收益密度

```text
Observation ID：Observation-06
Gap ID（如为参数缺口）：不适用
Source（如为参数缺口）：数据复盘
对应内容 ID：answer_2074892737510380763 / answer_2074886991645241672 / answer_2074885270286217411 / answer_2074881863097884985 / answer_2074890614576105134
题目：2026-08-23 新增 5 篇回答的高意图阅读与收益密度分化
审核来源：用户基于 2026-08-25 Git 最新采集、`reports/daily_review_20260825_zhihu_capture_recap.md` 与 `data/revenue_observations.csv` 的复盘判断
问题类型：参数缺口（当前问题类型限定表无"收益密度假设/高意图阅读/内容价值分层"类别，暂归入参数缺口；本条不直接创建参数）
关联 Parameter ID（如已存在对应参数记录）：不适用
问题描述：
2026-08-23 新增 5 篇回答出现较明显的流量价值与收益价值分化。初步判断不应简化为"机制型内容一定高收益"，更可能是知乎收益在奖励高意图阅读：读者点进来时，不只是围观、站队或获得态度确认，而是在用回答诊断自己的处境、理解未来风险，并寻找可执行干预。

因此，当前底层变量从"题材是否职场/认知/管理"和"是否解释机制"下沉为：
读者是在看别人，还是在看自己；这篇回答是否把 Surface Question 转译成 Latent Question，并完成解释、诊断、预测和干预。

核心待验证 Hypothesis：
H1：高 Self-Relevance（自我相关性）的问题，更容易产生高 Revenue Density。
H2：在高 Self-Relevance 问题中，完成 Diagnosis -> Mechanism -> Prediction -> Intervention 的回答，更容易产生收藏、私信、Paid/Costly Signal 等高成本行为。

初步证据：
1. `认知水平高的人有什么特征？`：内容收益明细本期阅读 170，本期收益 36 盐粒，约 21.18 盐粒 / 100 阅读；内容管理累计阅读 204。
2. `为什么老一辈批判躺平，却对加班猝死视而不见？`：内容收益明细本期阅读 368，本期收益 8 盐粒，约 2.17 盐粒 / 100 阅读；内容管理累计阅读 378。
3. `既为心腹，为什么反而会被领导批得最多、最狠？`：内容收益明细本期阅读 322，本期收益 17 盐粒，约 5.28 盐粒 / 100 阅读；内容管理累计阅读 369。
4. `老板不敢放权，背后真正怕的是什么？`：内容收益明细本期阅读 173，本期收益 21 盐粒，约 12.14 盐粒 / 100 阅读；内容管理累计阅读 183。
5. `匿名举报同事后，整个部门被扣奖金并集体孤立我，我做错了吗？`：内容管理累计阅读 513、收藏 5，但当前收益明细可见列表未列出，暂不可判断收益密度；可先标记为 Traffic Winner / 高自我相关性待确认样本，不作为 Value Winner 证据。

解释修正：
`心腹为什么被骂得最狠？` 同样包含权力/关系机制，但收益密度不高，说明"写了机制"不是充分条件。该题可能混有猎奇、关系解释、职场八卦等低决策负荷阅读。相对更强的样本是"我为什么晋升不了""我怎样避免职业风险""我掉下去怎么办""我现在到底该怎么办""我和厉害的人差在哪里"这类 Self-Diagnosis Question。

历史支持线索：
08-23 收益窗口中，`为什么很多人，做到经理或总监，就再也上不去了？`、`和领导相处有哪些红线不能碰？`、`领导提拔你的最根本的原因是什么？`、`从国企离职后在私企越混越迷茫，未来的路该怎么走？`、`中年失业出路在哪？`、`管理的本质是决策还是协调？` 等老文章也表现出较强的自我诊断/个人利害信号。

DMPI 价值重解释：
D/M/P/I 不只是让文章显得更深，而是把知乎问题从内容消费变成个人决策工具：
D：Definition / Diagnosis，对应"我怎么了？"
M：Mechanism，对应"为什么？"
P：Prediction，对应"接下来会怎样？"
I：Intervention，对应"我怎么办？"

这与 Observation-05 的 20 元红包样本方向一致：深度职场干预触发真实成本行为，可能不是因为文笔，而是因为分析进入了"这就是我现在的问题，而且你告诉我该怎么理解和处理"这一层。

初步修正意见：
暂不新增生产规则，不修改协议，不将阅读高直接等同于题目好。后续 10-20 篇应在复盘层补两个验证标签：
- Self-Relevance：High / Medium / Low
- Intervention Depth：0 / 1 / 2

并同步观察：
- 阅读量
- 盐粒每 100 阅读
- 收藏率
- 私信咨询
- Paid/Costly Signal

生命周期状态：SUPPORTED
缺口状态（如适用）：待审核
审核结果（如适用）：正式参数
审核说明：用户明确批准本条不再停留于复盘观察，直接嵌入现有 QT-QI → DECISION → COMPILE 生产链路；落点不是新增平行模块，而是强化 QI-02、QI-04.1、QI-05、QI-06、QI-08 与 COMPILE Reasoning Path 的执行规则。样本量小、极小阅读样本的盐粒 / 100 阅读会剧烈波动、知乎致知计划收益算法未公开等限制仍保留，后续继续验证效果，不把当前相关性解释为因果定论。
归入参数 ID：不适用
候选参数 ID（审核结果为候选参数时必填）：不适用
正式参数 ID（审核结果为正式参数时必填）：QT-QI.1
重复次数：1（首次以 Self-Relevance / Revenue Density 分层方式记录）
重复证据引用：
- `reports/daily_review_20260825_zhihu_capture_recap.md`
- `data/revenue_observations.csv` 中 `zhihu_knowledge_income_detail_20260825_recent7_browser` 记录
- `data/review_data_snapshots.csv` 中 2026-08-25 新增 5 条 REVIEW_DAY 内容记录
平台证据：
知乎创作中心内容管理页与收益分析 -> 致知计划 -> 内容收益明细。收益单位为盐粒，页面说明 100 盐粒 = 1 元人民币；本轮收益窗口为 2026-08-19 至 2026-08-25。
最终结论：SUPPORTED。作为生产原则进入 QT-QI / DECISION / COMPILE；效果仍需后续 10-20 篇继续验证。
处理动作：
1. 已将生产原则写入 `docs/知乎内容质量参数库_V2.md` 的 QT-QI.1，并同步 `runtime/知乎内容质量参数快照.md`。
2. 已将 DECISION / COMPILE 执行边界写入 `docs/知乎OS Compiler V1.md`。
3. 已将选题阶段 Personal Stakes 字段写入 `docs/Codex选题采集协议.md` 与 `templates/选题包模板.md`。
4. 后续复盘中把题目结果拆分为 Traffic Winner、Value Winner 与 High-Intent Reader 样本观察。
5. 每篇新增 Self-Relevance 与 Intervention Depth 两个复盘标签，既服务生产执行，也服务后续效果验证。
6. 单篇判断不得仅按阅读量排序；至少并看阅读量、盐粒每 100 阅读、收藏率、私信咨询与 Paid/Costly Signal。
```

## Observation-07：Secondary Distribution / Reactivation：发布十几天后的二次放量

```text
Observation ID：Observation-07
Gap ID（如为参数缺口）：不适用
Source（如为参数缺口）：数据复盘
对应内容 ID：answer_2073162526121107666
题目：体制内，为什么领导一眼就能看出你是老实人？
审核来源：2026-09-03 收益复盘审计
问题类型：结构问题（分发模型阶段拆分；非正文结构问题，暂归入结构问题）
关联 Parameter ID（如已存在对应参数记录）：EXP008
问题描述：
2026-09-03 最近 7 天收益窗口中，`体制内，为什么领导一眼就能看出你是老实人？` 出现明显二次放量。该回答发布于 2026-08-18，并非发布当天一次性爆发；从 2026-08-30 至 2026-09-03 四天内，累计阅读由 3,711 增至 14,238，增加约 10,527。同期 2026-08-25 发布的新文样本反而出现第一轮后快速衰减：`为什么领导的心腹很少有异性？` 四天累计只增加约 102 阅读 / 8 盐粒；`劳务派遣以后是否会占据主流？` 四天累计只增加约 93 阅读 / 8 盐粒。

该现象提示：知乎分发不应只按一次性 Initial Distribution 理解，至少存在研究层需要显式追踪的 `Secondary Distribution / Reactivation` 阶段。原先用 `views_per_day = 最终播放 / 发布天数` 作为弱校正时，会把“稳定增长”和“前期停滞后突然二次放量”平均掉，无法识别不同分发机制。

初步修正意见：
EXP008 研究层增加生命周期阶段视角：
Question Context → Entry → Initial Distribution → Consumption / Engagement → Further Distribution → Reactivation → Long-tail Persistence。

但本条只有一个非常强的 reactivation case，不能升级为生产规则，不能据此改正文协议或选题协议。后续应优先画重点文章时间曲线，而不是继续盲目增加内容变量。

生命周期状态：SUPPORTED
缺口状态（如适用）：不适用
审核结果（如适用）：不适用
审核说明：
本条支持的是“存在二次放量现象，且 EXP008 研究框架需要显式记录该阶段”，不支持“已找到二次放量触发机制”，也不支持“某类内容可稳定复现二次激活”。因此只入研究库和 Observation，不入正式参数库。
归入参数 ID：不适用
候选参数 ID（审核结果为候选参数时必填）：不适用
正式参数 ID（审核结果为正式参数时必填）：不适用
重复次数：1（首次明确记录二次激活样本）
重复证据引用：
- `reports/daily_review_20260830_zhihu_capture_recap.md`
- `reports/daily_review_20260903_zhihu_capture_recap.md`
- `data/revenue_observations.csv` 中 `zhihu_knowledge_income_detail_20260830_recent7_browser` 与 `zhihu_knowledge_income_detail_20260903_recent7_browser` 记录
- `research/experiments/EXP008.md` 的 “2026-09-03 研究层修正：二次激活样本”
平台证据：
知乎创作中心内容管理页与收益分析 -> 致知计划 -> 内容收益明细。收益单位为盐粒，页面说明 100 盐粒 = 1 元人民币。关键窗口为 2026-08-23 至 2026-08-29、2026-08-27 至 2026-09-02 两个最近 7 天收益窗口；窗口存在重叠，因此窗口数据只用于解释结构变化，累计值差异用于确认 2026-08-30 至 2026-09-03 的实际增量。
最终结论：
SUPPORTED。知乎播放不是一次性分配过程；截至当前证据，EXP008 最值得新增追踪的未知变量是“什么条件触发二次放量”。该结论属于研究层模型修正，不属于生产规则。
处理动作：
1. 已在 `research/experiments/EXP008.md` 入库二次激活研究层修正。
2. 不修改 `production_variable_library.md`。
3. 不修改正文生产协议、选题采集协议或 Runtime。
4. 后续复盘优先补重点样本时间曲线：发布时间 → 第一轮增长 → 停滞 → 二次增长 → 长尾。
5. 对收益拆分采用 `Revenue = Distribution Volume × Monetization Efficiency × Persistence` 的观察口径，避免把高播放、高 RPM、长尾持续混成同一个变量。
6. 阶段性策略口径：当前不要继续把主要精力放在正文系统优化上；下一阶段优先破解 Distribution Gate，尤其是“为什么有些文章会获得第二轮放量”。
```
