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
| 候选参数 | 用户批准进入候选参数前置流程 | 进入 Candidate 前置验证 |
| 正式参数 | 用户明确批准且证据链充分 | 极少使用，仍需记录证据引用 |

同类缺口必须累计重复次数，不得凭单篇高赞回答直接升级。

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
