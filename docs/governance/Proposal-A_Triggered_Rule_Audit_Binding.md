# Governance Change Proposal A：Triggered Rule Audit Binding

Status：DRAFT（Governance Plane 待审，不具备执行权威，不修改任何已发布权威文件）

Proposed By：Claude（起草），发现来源：`ZH-20260810-001` 生产过程中的端到端 Realization 审计（见 `productions/ZH-20260810-001/Realization_Audit.md`）

## 1. 现状

`docs/知乎OS Compiler Data Flow V1.md` 第4节对 COMPILE 输出对象 `Execution IR` 的 `triggered_rule_ids` 字段定义如下（原文）：

> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文），AUDIT 据此判断本 Run 应加载哪些条件触发的 Audit Rule。

`docs/知乎OS Compiler V1.md` 第7节 AUDIT 定义中，Operational Quality Checks 的权威来源是：

> Runtime.Audit Rules 中已具备明确操作定义、能给出 PASS/FAIL 的通用表达约束

`templates/GPT审核清单.md` 是 AUDIT 节点的执行载体，其 B 组 Operational Quality Checks 目前列出的是 6 个笼统类目：阅读体验、推进节奏、场景、表达自然、重复、收尾，不含任何 ID，也未标注这些类目与 `runtime/知乎ACTIVE规律快照.md` 中具体规则（如"开头钩子""认知增量"）的对应关系。

`runtime/知乎ACTIVE规律快照.md` 中记录的规则（开头钩子、情绪入口、认知增量、结构节奏、观点锋利度、收藏价值，以及职场组织题规律：组织机制优先、责任转移优先、反道德化）均只有名称，没有分配正式 Rule ID。

## 2. 证据

- `Execution_IR-v1.md`、`Execution_IR-v2.md`（`ZH-20260810-001`）的 `Triggered Rule IDs` 一节，均记录了"该快照无正式 ID，只能以名称定位，不构成合法 ID 引用"。
- `Realization_Audit.md`（`ZH-20260810-001`）对该 Run 中被 Activate 的 9 条规则类变量逐条核对，Audit 可验证一栏全部为"否"——即在这一个受控 Run 内，找不到任何一条能被 AUDIT 合法引用的 `AuditRule.<ID>`。
- 该发现范围限定为 `ZH-20260810-001` 单一样本，尚未扩大到历史生产验证。

## 3. Contract Gap

Data Contract（`知乎OS Compiler Data Flow V1.md`）明确规定了"`triggered_rule_ids` → AUDIT 据此加载对应 Audit Rule"这一条链路，但支撑这条链路的两个前提目前都不成立：

1. `triggered_rule_ids` 的候选来源（`知乎ACTIVE规律快照.md`）没有正式 ID 编号体系，无法产出合法的 `AuditRule.<ID>`。
2. `templates/GPT审核清单.md` 的 Operational Quality Checks 是与具体规则脱钩的笼统类目，即使①被补齐，也没有现成的映射结构把某个 Rule ID 关联到某条可执行的 PASS/FAIL 检查定义。

Compiler V1 第11节 SSP 规定"通用可判定表达检查（重复、参数显形等）"的唯一权威是 `Runtime.Audit Rules`；但 `Runtime.Audit Rules` 作为一个具备 ID 体系、可被 `triggered_rule_ids` 引用的正式对象，目前并不存在——存在的只是 `GPT审核清单.md` 里的类目清单和 `知乎ACTIVE规律快照.md` 里的规则原文，两者未被打通。

## 4. 影响范围

- 直接影响：任何 Run 只要在 COMPILE 阶段命中 `知乎ACTIVE规律快照.md` 中的规则，其 `triggered_rule_ids` 字段就无法达到 Data Contract 要求的"只存 ID"标准，也无法被 AUDIT 用来加载对应检查项。
- 间接影响：AUDIT 阶段对"Operational Quality Checks"这一类问题（区别于 Execution Compliance）事实上处于不可判定状态——不是没有问题，是没有合法 Expected Source 可以判定，导致相关 Issue 无法合法生成，只能记录为 Observation。
- 已知范围：本 Proposal 的证据来自单一 Run（`ZH-20260810-001`），不代表已验证为系统全局现象；是否是长期存在、跨生产的普遍缺口，需要额外样本验证（不在本 Proposal 范围内）。

## 5. 待决策问题

1. Global Rule 的正式 ID 编号方案由谁拥有、如何分配（例如是否复用 `production_variable_library.md` 已有的 `PD-09` / `RR-02` / `CR-01` 编码风格，还是另立体系）？
2. `知乎ACTIVE规律快照.md` 中的规则，是否全部需要升级为可被 AUDIT 引用的 `Runtime.Audit Rules`，还是只有部分适合（该快照自身声明"只作为结构实例化后的内容补充与风险提醒"，可能不是所有条目都适合作为可判定的 PASS/FAIL 标准）？
3. `templates/GPT审核清单.md` 的 Operational Quality Checks 与具体 Rule ID 之间的映射结构应该是什么形式（清单内嵌 ID、还是引用独立的 Audit Rule 注册表）？
4. Runtime 发布（`runtime/ACTIVE_MANIFEST.md`）在纳入新的 Audit Rule ID 体系时，如何保证完整性校验（例如 `scripts/validate_runtime_consistency.py` 是否需要新增校验项，校验"每个 triggered_rule_ids 候选来源都有对应可加载的 Audit Rule"）？
5. 在方案落地前，AUDIT 对已知无法验证的 Operational Quality 类问题，应如何处理（继续按现状记录为 Observation 不进 AuditResult；还是临时降级为不触发 Triggered Rule IDs，只保留 Execution Compliance 检查）？

## 6. 候选方案（未评估，未决策，仅供 Governance Plane 参考）

- 方案一：为 `知乎ACTIVE规律快照.md` 中每条规则分配正式 ID（如 `GR-001` 开头），并在 `GPT审核清单.md` B组逐条替换为可挂载 ID 的检查项。
- 方案二：不改造 `知乎ACTIVE规律快照.md`，改为新建一份独立的 `Runtime.Audit Rules` 注册表，专门收录"具备明确操作定义、能给出 PASS/FAIL"的条目并分配 ID，`知乎ACTIVE规律快照.md` 保持"内容补充/风险提醒"定位不变，二者不必一一对应。
- 方案三：承认 `triggered_rule_ids → Audit Rule 加载` 这条链路当前不适用于 `知乎ACTIVE规律快照.md` 类的规则，修改 Data Contract 措辞，明确该字段只服务于未来会出现的、真正具备 ID 体系的 Global Rule，`知乎ACTIVE规律快照.md` 类内容改走 COMPILE 内部消化路径（不进入 triggered_rule_ids）。

本 Proposal 不推荐上述任一方案，候选方案的取舍、组合或另拟新方案，由 Governance Plane 决定。
