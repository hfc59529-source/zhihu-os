# Proposal B — Governance Decision → 拟修改文件清单 + 最小 Contract Diff

Status：APPROVED FOR APPLICATION（Final Contract Diff Review: PASS，已批准应用到权威文件；本文件记录 Diff 内容与应用结果，本文件本身不具备执行权威，权威以已修改的目标文件为准）

依据：`docs/governance/Proposal-B_Content_Variable_Activation_Contract.md` 已获 `APPROVED WITH SPECIFIED RESOLUTION`，裁决摘要：

```text
CV = Runtime Parameter Identity（Registry 固定）
↓ COMPILE Trigger
CV Run Instantiation = Execution IR.acceptance_criteria（COMPILE 生成）
↓ WRITE → Realization → AUDIT（按对应 AC 验证）

triggered_rule_ids 继续只服务真正的 Global Rule，不承载 CV ID。
不恢复独立 Parameter_Call 前置步骤，不新增第三个 Execution IR 字段，不设每 Run 的"分类权"。
```

本文件只列出：需要改哪些文件、每处改哪一段、改前/改后文字对照。不实际执行修改，不新增未经裁决授权的内容。

## 1. 拟修改文件清单

| 文件 | 修改类型 | 触及的裁决问题 |
|---|---|---|
| `production_variable_library.md` 第15条 | 措辞澄清（明确 CV 统一走 acceptance_criteria，不走 triggered_rule_ids） | 0, 2 |
| `docs/知乎OS Compiler Data Flow V1.md` 第4节 | Schema 字段说明新增两句 | 2 |
| `docs/知乎OS Compiler V1.md` 第5节 COMPILE | Forbidden 列表新增约束（Proposal B 新增禁止性约束，非对原条款的重新解释） | 2 |
| `docs/知乎OS Compiler V1.md` 第11节 SSP 表 | 新增两行，明确 CV Identity 与 CV Run Instantiation 的唯一权威分别归属 | 1, 3 |

不修改文件：`docs/知乎OS Compiler V1.md` 第9节 RELEASE 及以下节点、`templates/GPT审核清单.md`（AUDIT 载体不变，AUDIT 仍按 Execution IR.AcceptanceCriteria 核对，本裁决不改变 AUDIT 的核对方式，只改变 AC 的生成来源之一）、`runtime/ACTIVE_MANIFEST.md`（本裁决不涉及 Runtime 发布本身，是否需要重新发布由 Governance 另行决定，不在本 Diff 范围）。

## 2. 逐处 Diff

### 2.1 `production_variable_library.md` 第15条

改前（现状）：

> 5. Claude 正文生产默认只触发本库中 `当前状态=ACTIVE` 且 `触发资格=是` 的变量。触发（Trigger）指题目、样本特征或结构条件命中变量的适用题型与触发条件，使其进入本题触发矩阵；COMPILE 将命中变量写入 `Execution IR.triggered_rule_ids`（规则类变量）或 `Execution IR.acceptance_criteria`（本篇正文义务）是激活（Activation）；WRITE 按 Execution IR 生成正文是执行（Execution）；正文中实际体现该变量效果是实现（Realization）。四个环节按顺序发生，不得跳过。

改后（拟）：

> 5. Claude 正文生产默认只触发本库中 `当前状态=ACTIVE` 且 `触发资格=是` 的变量。触发（Trigger）指题目、样本特征或结构条件命中变量的适用题型与触发条件，使其进入本题触发矩阵；**COMPILE 将命中的内容变量（CV）统一编译为本 Run 的 Instantiation 义务，写入 `Execution IR.acceptance_criteria` 完成激活（Activation）——CV 的 Global Identity（定义、适用题型、触发条件、触发权重）始终只存在于本库，不进入 `Execution IR.triggered_rule_ids`；`triggered_rule_ids` 只承载按现行 Contract 定义的 Global Rule ID，不承载 CV**；WRITE 按 Execution IR 生成正文是执行（Execution）；正文中实际体现该变量效果是实现（Realization）。四个环节按顺序发生，不得跳过。

变更说明：原文"或"字造成的二选一/未定义归属被消解——明确 CV 类内容变量只走 `acceptance_criteria` 一条路径，`triggered_rule_ids` 不承载 CV。**不描述 `triggered_rule_ids` 中的规则类变量由 WRITE 如何解析执行——这属于 Proposal A（Triggered Rule Audit/Writer Binding）范围，Proposal B 的裁决只批准"CV 不进入 triggered_rule_ids"，未批准该字段本身的下游绑定方式，本次修改不代为回答。**

### 2.2 `docs/知乎OS Compiler Data Flow V1.md` 第4节

改前（现状，`triggered_rule_ids` 说明）：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。

改后（拟，新增一句）：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。**本字段不承载 `production_variable_library.md` 登记的内容变量（CV）——CV 的 Global 身份始终只存在于 Parameter Registry，不进入本字段。**（本字段中 Global Rule 本身如何被 WRITE / AUDIT 解析和执行，仍是 Proposal A 待决问题，本次修改不涉及、不预支。）

改前（现状，`expression_constraints`/`acceptance_criteria` 说明）：

> `expression_constraints` 与 `acceptance_criteria` 只能是本次 Run 特有条目，不得复制 Runtime.Writer Rules / Runtime.Audit Rules 中已存在的通用条款。

改后（拟，新增一句）：

> `expression_constraints` 与 `acceptance_criteria` 只能是本次 Run 特有条目，不得复制 Runtime.Writer Rules / Runtime.Audit Rules 中已存在的通用条款。**`acceptance_criteria` 还承载由 COMPILE 依据已 Trigger 的内容变量（CV）编译出的 Run-specific Realization Requirement（本篇必须具体实现什么，例如"本文必须具体呈现该事件造成的权力/利益/责任重新分配"），不承载"本题为何命中该 CV"这类触发判定证据（Trigger Basis）——AC 只保存可验收的义务，不保存触发理由。此外新增一条 Proposal B 引入的禁止性约束（原条款只约束 Runtime.Writer Rules / Runtime.Audit Rules，不涉及 Parameter Registry，此处是新增，不是对原条款的重新解释）：不得复制该 CV 在 Parameter Registry 中的通用定义、适用题型、触发条件或触发权重。**

### 2.3 `docs/知乎OS Compiler V1.md` 第5节 COMPILE（Forbidden 列表）

改前（现状，节选）：

> Forbidden:
>   不得修改 Decision 四字段本身
>   不得决定具体措辞句子（WRITE 的权限）
>   不得省略 Acceptance Criteria，直接把"怎么写"丢给 WRITE 自由发挥
>   Expression Constraints / Acceptance Criteria 只能是"本 Run 特有义务"，不得把
>     Runtime.Audit Rules 中已存在的通用检查项（Global Operational Checks）复制
>     进 Execution IR——通用规则永远只活在 Runtime Release 里，不允许被复制出第二份
>   Triggered Rule IDs 只能是 ID 引用，不得连带复制规则正文

改后（拟，新增一条）：

> Forbidden:
>   不得修改 Decision 四字段本身
>   不得决定具体措辞句子（WRITE 的权限）
>   不得省略 Acceptance Criteria，直接把"怎么写"丢给 WRITE 自由发挥
>   Expression Constraints / Acceptance Criteria 只能是"本 Run 特有义务"，不得把
>     Runtime.Audit Rules 中已存在的通用检查项（Global Operational Checks）复制
>     进 Execution IR——通用规则永远只活在 Runtime Release 里，不允许被复制出第二份
>   Triggered Rule IDs 只能是 ID 引用，不得连带复制规则正文，**且不得引用
>     `production_variable_library.md` 登记的内容变量（CV）**
>   **（Proposal B 新增禁止性约束，非对原条款的重新解释——原"不得复制通用条款"仅
>     约束 Runtime.Writer Rules / Runtime.Audit Rules，未涉及 Parameter Registry）：
>     由内容变量（CV）编译出的 Acceptance Criteria，只能写本 Run 的 Realization
>     Requirement（本篇必须具体实现什么），不得复制该 CV 在 Parameter Registry 中的
>     通用定义字段（变量定义、适用题型、触发条件、触发权重等），也不得把"本题为何
>     命中该 CV"这类 Trigger Basis 写进 Acceptance Criteria——AC 只保存可验收的义务，
>     不保存触发证据**

### 2.4 `docs/知乎OS Compiler V1.md` 第11节 SSP｜Single Source of Policy 表

改前（现状，节选）：

> | 规则 | 唯一权威 |
> | --- | --- |
> | 读者真实困惑 / 事实边界 | INPUT |
> | Reality / Main Gap / Transformation / Core Judgment | DECISION |
> | 正文路线、结构、素材边界、本篇特有验收标准 | COMPILE（写入 Execution IR） |
> | 人话表达、节奏、留白 | Runtime.Writer Rules |
> | 通用可判定表达检查（重复、参数显形等） | Runtime.Audit Rules |
> | 最终正文是否接受 | REVIEW（人工，唯一权威，不得由 AUDIT 或 RELEASE 代为判断） |
> | 发布前置条件 | Runtime.Release Rules |
> | 收益评估 | Learning Plane（不在本流水线内，见下） |

改后（拟，新增两行）：

> | 规则 | 唯一权威 |
> | --- | --- |
> | 读者真实困惑 / 事实边界 | INPUT |
> | Reality / Main Gap / Transformation / Core Judgment | DECISION |
> | 正文路线、结构、素材边界、本篇特有验收标准 | COMPILE（写入 Execution IR） |
> | **内容变量（CV）Identity：定义、适用题型、触发条件、触发权重** | **`production_variable_library.md`（Parameter Registry）** |
> | **内容变量（CV）本 Run Instantiation：本篇必须具体实现什么（Realization Requirement）** | **COMPILE（写入 Execution IR.acceptance_criteria）** |
> | 人话表达、节奏、留白 | Runtime.Writer Rules |
> | 通用可判定表达检查（重复、参数显形等） | Runtime.Audit Rules |
> | 最终正文是否接受 | REVIEW（人工，唯一权威，不得由 AUDIT 或 RELEASE 代为判断） |
> | 发布前置条件 | Runtime.Release Rules |
> | 收益评估 | Learning Plane（不在本流水线内，见下） |

## 3. 本 Diff 明确不处理的事项（避免与 Proposal A 或其它待决事项混淆）

- `triggered_rule_ids → AuditRule.<ID>` 加载链路断点（Proposal A 范围）：本 Diff 不涉及，且 2.1/2.2/2.3 的措辞澄清不依赖 A 的裁决即可独立成立——因为本裁决只是把 CV 排除出 `triggered_rule_ids`，不改变该字段本身对规则类变量仍然存在的 Audit Binding 缺口。
- `triggered_rule_ids` 中 Global Rule 本身如何被 WRITE 解析、执行（即"规则类变量的 Writer Binding"）：Proposal A 范围，本 Diff 不涉及、不预支、不描述任何具体绑定方式。
- `runtime/ACTIVE_MANIFEST.md` 是否需要因本次 Contract 措辞变更而重新发布：不在本 Diff 范围，由 Governance 另行决定。
- 是否需要给规则类变量（`知乎ACTIVE规律快照.md` 条目）分配正式 ID：Proposal A 范围，本 Diff 不涉及。

## 3a. 显式留白：Unresolved Schema Detail（本 Diff 不解决，如实记录）

**CV Trigger Basis（本题为何命中某条 CV）是否需要持久化，若需要，落在哪个 Schema 位置——本 Diff 未解决，不假装已解决。**

裁决只确定了 Realization Requirement（本篇必须实现什么）进 `acceptance_criteria`，Trigger Basis（为什么命中）被明确排除在 AC 之外（见 2.2、2.3）。但 Trigger Basis 本身是否还需要在别处记录（例如供未来复盘、供 COMPILE 决策可追溯），Data Contract 目前没有任何字段承载它——历史 `Parameter_Call-v1.md` 里"触发依据"这一层，在本次裁决后暂时没有对应的新 Schema 落点。这不阻塞 CV Realization Contract（AC 层面已经自洽），但是一个尚未回答的问题，留给后续 Governance 决定是否需要补一个字段，还是接受这层信息不再持久化。

## 4. 受影响但不在本次修改范围内的下游生产对象（如实记录，供参考）

- `productions/ZH-20260810-001/Execution_IR-v1.md`、`Execution_IR-v2.md` 第6节自造的"CV 变量触发判定"子表，若本裁决正式落权威文件，理论上应改写为标准 `acceptance_criteria` 条目（CV ID 从 triggered_rule_ids 一节移除，改为在 `acceptance_criteria` 里新增对应 `{id, requirement}` 条目，`requirement` 只写本 Run Instantiation，不写 Registry 定义）。是否现在改写、还是等 `ZH-20260810-001` 恢复生产时再改写，由用户决定，本 Diff 不代为执行。

## 5. 校验建议（供用户自行核对，不由 Claude 代为判断是否通过）

- `scripts/validate_runtime_consistency.py` 是否需要新增校验项（例如校验 Execution IR 的 `triggered_rule_ids` 中不出现 CV 编号格式），本 Diff 不评估，留待用户决定是否需要。
- 2.3 与 2.4 的新增内容是否与 `docs/知乎OS Compiler V1.md` 其余章节（尤其第4节 COMPILE 主体 Output 定义、第10节 Writer 可替换性）存在未预见的冲突，建议逐节复核一遍，本 Diff 未做跨章节穷举复核。
