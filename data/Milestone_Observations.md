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
暂不提出。待验证"这些 ACTIVE 文件是否确实同时构成当前有效权威，并且对同一生产对象给出互不兼容的规则"这一命题是否成立后，再进入治理判断；不预设 Precedence/Supersession Rule 或其他具体解法。
生命周期状态：OPEN
缺口状态（如适用）：不适用
审核结果（如适用）：不适用
审核说明：
当前未发现该正文调用 Skill006、Skill007 或生成 Production Card 的证据；因此尚不能建立本观察与该正文结果之间的因果关系，也不能反向声称该正文"仅使用"了哪些具体机制——完整执行 Trace 未经证明。
归入参数 ID：不适用
候选参数 ID：不适用
正式参数 ID：不适用
重复次数：1（首次记录）
重复证据引用：不适用
平台证据：不适用（本观察不依赖平台/账号样本，依赖文件文本本身，验证方式应为治理评审逐条核对上述七个冲突点涉及的八个文件原文，确认摘录准确，而非等待生产样本积累）
最终结论：待定（OPEN，未进入 VALIDATING）
处理动作：不修改任何正式协议或参数记录。下一步是验证本命题——"上述七个冲突点涉及的八个文件（含标注 ACTIVE 的权威文件，以及标注 LEGACY_RETIRED 但仍被其他权威文件引用/声明为权威的对象）是否确实同时构成当前有效权威，并对 Production Card 是否属于正式生产链给出互不兼容的规则"——是否成立：成立则 SUPPORTED，此后才讨论治理层如何处理（可能是建立 Precedence Rule，也可能是直接删除某一侧的旧语义，或其他方案，方案本身不属于本次验证目标）；不成立则 REJECTED 或 INCONCLUSIVE 并 CLOSED。
```
