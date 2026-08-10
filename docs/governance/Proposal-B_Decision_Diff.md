# Proposal B — Governance Decision → 拟修改文件清单 + 最小 Contract Diff

Status：DRAFT（仅为待审查的修改草案，未应用到任何权威文件；本文件本身也不具备执行权威）

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
| `docs/知乎OS Compiler V1.md` 第5节 COMPILE | Forbidden 列表新增一条澄清，避免与"不得复制 Runtime 通用条款"混淆 | 2 |
| `docs/知乎OS Compiler V1.md` 第11节 SSP 表 | 新增两行，明确 CV Identity 与 CV Run Instantiation 的唯一权威分别归属 | 1, 3 |

不修改文件：`docs/知乎OS Compiler V1.md` 第9节 RELEASE 及以下节点、`templates/GPT审核清单.md`（AUDIT 载体不变，AUDIT 仍按 Execution IR.AcceptanceCriteria 核对，本裁决不改变 AUDIT 的核对方式，只改变 AC 的生成来源之一）、`runtime/ACTIVE_MANIFEST.md`（本裁决不涉及 Runtime 发布本身，是否需要重新发布由 Governance 另行决定，不在本 Diff 范围）。

## 2. 逐处 Diff

### 2.1 `production_variable_library.md` 第15条

改前（现状）：

> 5. Claude 正文生产默认只触发本库中 `当前状态=ACTIVE` 且 `触发资格=是` 的变量。触发（Trigger）指题目、样本特征或结构条件命中变量的适用题型与触发条件，使其进入本题触发矩阵；COMPILE 将命中变量写入 `Execution IR.triggered_rule_ids`（规则类变量）或 `Execution IR.acceptance_criteria`（本篇正文义务）是激活（Activation）；WRITE 按 Execution IR 生成正文是执行（Execution）；正文中实际体现该变量效果是实现（Realization）。四个环节按顺序发生，不得跳过。

改后（拟）：

> 5. Claude 正文生产默认只触发本库中 `当前状态=ACTIVE` 且 `触发资格=是` 的变量。触发（Trigger）指题目、样本特征或结构条件命中变量的适用题型与触发条件，使其进入本题触发矩阵；**COMPILE 将命中的内容变量（CV）统一编译为本 Run 的 Instantiation 义务，写入 `Execution IR.acceptance_criteria` 完成激活（Activation）——CV 的 Global Identity（定义、适用题型、触发条件、触发权重）始终只存在于本库，不进入 `Execution IR.triggered_rule_ids`；`triggered_rule_ids` 只服务于 `runtime/知乎ACTIVE规律快照.md` 一类不需要 Run-specific 实例化、由 WRITE 直接依据 Runtime.Writer Rules 原文执行的规则类变量，两类对象不共用同一落点**；WRITE 按 Execution IR 生成正文是执行（Execution）；正文中实际体现该变量效果是实现（Realization）。四个环节按顺序发生，不得跳过。

变更说明：原文"或"字造成的二选一/未定义归属被消解——明确 CV 类内容变量只走 `acceptance_criteria` 一条路径，`triggered_rule_ids` 专属规则类变量（如 ACTIVE 规律快照条目），两者按对象类型分流，不是同一对象的两个可选落点。

### 2.2 `docs/知乎OS Compiler Data Flow V1.md` 第4节

改前（现状，`triggered_rule_ids` 说明）：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。

改后（拟，新增一句）：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。**本字段只承载规则类变量（如 `runtime/知乎ACTIVE规律快照.md` 条目），不承载 `production_variable_library.md` 登记的内容变量（CV）——CV 的 Global 身份始终只存在于 Parameter Registry，不进入本字段。**

改前（现状，`expression_constraints`/`acceptance_criteria` 说明）：

> `expression_constraints` 与 `acceptance_criteria` 只能是本次 Run 特有条目，不得复制 Runtime.Writer Rules / Runtime.Audit Rules 中已存在的通用条款。

改后（拟，新增一句）：

> `expression_constraints` 与 `acceptance_criteria` 只能是本次 Run 特有条目，不得复制 Runtime.Writer Rules / Runtime.Audit Rules 中已存在的通用条款。**`acceptance_criteria` 还承载由 COMPILE 依据已 Trigger 的内容变量（CV）编译出的 Run Instantiation 义务；每条此类条目只能写"本篇必须实现什么"，不得复制该 CV 在 Parameter Registry 中的通用定义、适用题型、触发条件或触发权重——这类复制仍然违反本条"不得复制通用条款"的禁止性规定，只是复制对象从 Runtime.Audit Rules 换成了 Parameter Registry，性质相同。**

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
>   Triggered Rule IDs 只能是 ID 引用，不得连带复制规则正文，**且只能引用规则类变量，
>     不得引用 `production_variable_library.md` 登记的内容变量（CV）**
>   **由内容变量（CV）编译出的 Acceptance Criteria，只能写本 Run 的 Instantiation 义务
>     （本篇怎么体现该变量），不得复制该 CV 在 Parameter Registry 中的通用定义字段
>     （变量定义、适用题型、触发条件、触发权重等）——这属于本条"不得复制通用条款"
>     禁止的一种具体情形，不是新增的独立规则**

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
> | **内容变量（CV）本 Run Instantiation：本篇为何命中、具体怎么体现** | **COMPILE（写入 Execution IR.acceptance_criteria）** |
> | 人话表达、节奏、留白 | Runtime.Writer Rules |
> | 通用可判定表达检查（重复、参数显形等） | Runtime.Audit Rules |
> | 最终正文是否接受 | REVIEW（人工，唯一权威，不得由 AUDIT 或 RELEASE 代为判断） |
> | 发布前置条件 | Runtime.Release Rules |
> | 收益评估 | Learning Plane（不在本流水线内，见下） |

## 3. 本 Diff 明确不处理的事项（避免与 Proposal A 或其它待决事项混淆）

- `triggered_rule_ids → AuditRule.<ID>` 加载链路断点（Proposal A 范围）：本 Diff 不涉及，且 2.1/2.2/2.3 的措辞澄清不依赖 A 的裁决即可独立成立——因为本裁决只是把 CV 排除出 `triggered_rule_ids`，不改变该字段本身对规则类变量仍然存在的 Audit Binding 缺口。
- `runtime/ACTIVE_MANIFEST.md` 是否需要因本次 Contract 措辞变更而重新发布：不在本 Diff 范围，由 Governance 另行决定。
- 是否需要给规则类变量（`知乎ACTIVE规律快照.md` 条目）分配正式 ID：Proposal A 范围，本 Diff 不涉及。

## 4. 受影响但不在本次修改范围内的下游生产对象（如实记录，供参考）

- `productions/ZH-20260810-001/Execution_IR-v1.md`、`Execution_IR-v2.md` 第6节自造的"CV 变量触发判定"子表，若本裁决正式落权威文件，理论上应改写为标准 `acceptance_criteria` 条目（CV ID 从 triggered_rule_ids 一节移除，改为在 `acceptance_criteria` 里新增对应 `{id, requirement}` 条目，`requirement` 只写本 Run Instantiation，不写 Registry 定义）。是否现在改写、还是等 `ZH-20260810-001` 恢复生产时再改写，由用户决定，本 Diff 不代为执行。

## 5. 校验建议（供用户自行核对，不由 Claude 代为判断是否通过）

- `scripts/validate_runtime_consistency.py` 是否需要新增校验项（例如校验 Execution IR 的 `triggered_rule_ids` 中不出现 CV 编号格式），本 Diff 不评估，留待用户决定是否需要。
- 2.3 与 2.4 的新增内容是否与 `docs/知乎OS Compiler V1.md` 其余章节（尤其第4节 COMPILE 主体 Output 定义、第10节 Writer 可替换性）存在未预见的冲突，建议逐节复核一遍，本 Diff 未做跨章节穷举复核。
