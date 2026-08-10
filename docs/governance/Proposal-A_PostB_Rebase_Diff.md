# Proposal A — Post-B Semantic Rebase Diff

Status：DRAFT（仅为待审查的 Rebase 草案，未应用到 `Proposal-A_Triggered_Rule_Audit_Binding.md`；本文件不修改任何 Compiler/Data Flow/Parameter Registry 权威文件）

目的：把 Proposal A 建立时的事实前提，从"B 裁决前的世界状态"更新到"B 裁决后的世界状态"。**只更新被 B 实际改变的事实（`triggered_rule_ids` 的 Contract 定义原文、CV/Global Rule 的边界归属），不重新定义 A 的问题、不新增待决策问题、不修改候选方案的实质内容、不预支 A 的裁决。**

## 核查结论：Proposal A 原文本身没有把 CV 当作 `triggered_rule_ids` 候选对象

逐节核对 `Proposal-A_Triggered_Rule_Audit_Binding.md` 现有文本，确认：

- §1 现状、§3 Contract Gap、§6 候选方案一/二/三，通篇讨论的对象都是 `runtime/知乎ACTIVE规律快照.md` 中的规则类变量（开头钩子、认知增量等），**未出现过"CV"或"内容变量"字样**，没有把 CV 当作候选来源。
- §2 证据第一条明确写"9 条规则类变量"（不是 13 条），已经把 `Realization_Audit.md` 里的 4 条 CV 行排除在外，证据引用范围本来就没有混入 CV。

所以 A **不需要"删除 CV 相关前提"**——因为原文里本来就没有把这套前提建立在 CV 之上。真正过期的是下面这一处：

## 唯一需要 Rebase 的一处：§1 引用的 Data Contract 原文已被 B 修改

Proposal A §1 引用的 `docs/知乎OS Compiler Data Flow V1.md` 第4节 `triggered_rule_ids` 定义，是 **B 落地前** 的版本：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。

B 落地后，该字段定义已变为（现行权威文本，`docs/知乎OS Compiler Data Flow V1.md` 第4节）：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。本字段不承载 `production_variable_library.md` 登记的内容变量（CV）——CV 的 Global 身份始终只存在于 Parameter Registry，不进入本字段。（本字段中 Global Rule 本身如何被 WRITE / AUDIT 解析和执行，仍是 Proposal A 待决问题，本次修改不涉及、不预支。）

## Rebase Diff（拟应用到 `Proposal-A_Triggered_Rule_Audit_Binding.md`）

### 1. §1 现状：更新引用文本 + 补一句范围确认

改前：

> `docs/知乎OS Compiler Data Flow V1.md` 第4节对 COMPILE 输出对象 `Execution IR` 的 `triggered_rule_ids` 字段定义如下（原文）：
>
> > `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。

改后（拟）：

> `docs/知乎OS Compiler Data Flow V1.md` 第4节对 COMPILE 输出对象 `Execution IR` 的 `triggered_rule_ids` 字段定义如下（原文，含 Proposal B 落地后的最新表述）：
>
> > `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。本字段不承载 `production_variable_library.md` 登记的内容变量（CV）——CV 的 Global 身份始终只存在于 Parameter Registry，不进入本字段。（本字段中 Global Rule 本身如何被 WRITE / AUDIT 解析和执行，仍是 Proposal A 待决问题，本次修改不涉及、不预支。）
>
> **Post-B 范围确认**：Proposal B 已明确将 CV 排除出 `triggered_rule_ids`，并将"本字段中 Global Rule 如何被 WRITE/AUDIT 解析执行"保留给 Proposal A。Proposal A 原有证据与问题陈述本来就只针对 `知乎ACTIVE规律快照.md` 中的 9 条规则类变量，不包含 CV；因此 B 不改变 A 的证据对象范围。本句仅确认 CV 不属于 A，**不预先确认上述规则类变量是否应被治理定义为 Data Contract 所称的 Global Rule，该问题仍由 A 的 Governance Review 判断**。

### 2. §2 证据：追加一条来源说明，不改变原有两条证据

在原有两条证据之后追加：

> - （Post-B 补充说明）`Realization_Audit.md` 原表中另有 4 条 CV 记录（CV001–CV004）。其中由 CV 字段归属、Activation Schema 与 Run-specific Realization Requirement 所暴露的 Contract 问题已由 Proposal B 单独处理并裁决；这些 CV 记录不属于 Proposal A 的证据范围。Proposal A 的证据范围维持原状，只包含前述 9 条规则类变量，不因 B 的裁决而扩大或缩小。

### 3. §3 Contract Gap、§4 影响范围、§5 待决策问题、§6 候选方案：不改动

逐条核对后确认：这四节的实质内容均未依赖任何后来被 B 改变的事实，`知乎ACTIVE规律快照.md` 的 Rule ID 缺口、`GPT审核清单.md` 的映射缺口、候选方案一/二/三的具体设计，都不涉及 CV 或 Parameter Registry，B 的裁决不影响这些内容的成立性。**不做任何修改，避免借 Rebase 之机改动 A 的问题定义或预支裁决。**

## Rebase 后 Proposal A 的状态

Rebase 只涉及 §1 一处引用文本更新 + §2 一条补充说明，§3–§6 保持不变。Rebase 完成后，Proposal A 才可以正式进入 Governance Review。

本文件只是 Diff，尚未应用到 `Proposal-A_Triggered_Rule_Audit_Binding.md`，等待逐句审查后再落地。
