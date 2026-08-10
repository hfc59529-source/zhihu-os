# Governance Change Proposal B：Content Variable Activation Contract

Status：DRAFT（Governance Plane 待审，不具备执行权威，不修改任何已发布权威文件）

Proposed By：Claude（起草），发现来源：`ZH-20260810-001` 生产过程中的端到端 Realization 审计（见 `productions/ZH-20260810-001/Realization_Audit.md`）

## 1. 现状

`docs/知乎OS Compiler Data Flow V1.md` 第4节定义 `Execution IR` 只有两个与规则/变量相关的字段：

> `expression_constraints`、`acceptance_criteria`：只能是本次 Run 特有条目，不得复制 Runtime.Writer Rules / Runtime.Audit Rules 中已存在的通用条款。
> `triggered_rule_ids`：本 Run 按 Runtime.Compile Rules 条件触发的 Global Rule ID 列表（只存 ID，不存正文）。

`production_variable_library.md` 第15条定义了变量生命周期的四个环节：

> Trigger（命中）→ Activation（COMPILE 写入 `triggered_rule_ids`（规则类变量）或 `acceptance_criteria`（本篇正文义务）） → Execution（WRITE 按 Execution IR 生成正文） → Realization（正文实际体现）。四个环节按顺序发生，不得跳过。

该条把变量分成"规则类变量"（走 `triggered_rule_ids`）和"本篇正文义务"（走 `acceptance_criteria`）两类，但没有规定**具体某一条 CV 记录属于哪一类**，也没有规定判定归属的标准或归属权归谁。

## 2. 证据

- `production_variable_library.md` 中登记的 CV001（认知校正）、CV002（利益重分配）、CV003（组织视角）、CV004（风险传导）、CV005（身份代入）五条记录，字段里有"变量大类""适用题型""触发条件""触发权重"等，但没有任何字段标注该变量是"Global Rule"还是"Run-specific obligation"。
- `Execution_IR-v1.md`、`Execution_IR-v2.md`（`ZH-20260810-001`）在第6节"Triggered Rule IDs"标题下，自造了一个"CV 变量触发判定"子表，逐条给出触发资格判定（触发/不触发），但既没有写成合法的 `acceptance_criteria` 条目（未见 `{id, requirement}` 结构），也没有写成纯 ID 列表（附带了完整判定理由文字）。
- 这个自造子表本身证明 COMPILE 在缺少归属规则的情况下，只能自行发明一个第三落点，不代表这个落点具备权威性。

## 3. Contract Gap

`知乎OS Compiler Data Flow V1.md` 的 `Execution IR` Schema 只有 `triggered_rule_ids`（Global Rule ID 列表）与 `acceptance_criteria`（`{id, requirement}` 结构的 Run 特有条目）两个字段，二者互斥且用途不同：

- 进 `triggered_rule_ids`：意味着该变量的具体内容由 WRITE 自行去 `Runtime Release → Writer Rules 分区` 加载原文执行，Execution IR 里不展开。
- 进 `acceptance_criteria`：意味着该变量在本 Run 里被实例化为一条具体、可审的义务，Execution IR 里必须写清楚 `requirement`。

CV 变量本身兼具两种特征：它们既是"参数库"里登记的通用规则（有适用题型、触发条件，跨 Run 复用），又往往需要"本 Run 具体怎么体现"这类实例化描述（例如 CV002"利益重分配"命中后，需要说明本 Run 里利益重分配具体体现在哪个场景/哪句话）。Data Contract 没有回答：**这种"既通用又需要实例化"的变量，激活后到底该二选一，还是需要同时出现在两个字段（ID 进 triggered_rule_ids，实例化描述进 acceptance_criteria）？**

`production_variable_library.md` 第15条虽然提到了两个落点，但只是复述 Data Contract 已有的两个字段名，没有新增归属判定规则，也没有指定"谁有分类权"——是 COMPILE 每次自行判断，还是参数库记录本身应该有一个固定字段声明类型。

## 4. 影响范围

- 直接影响：任何生产 Run 只要触发 CV 变量，COMPILE 都需要自行决定落点，缺乏统一标准，不同 Run 可能产生不一致的 Schema 处理方式（本次即自造了第三个子表）。
- 间接影响：AUDIT 阶段无法用统一标准去核对 CV 变量是否被正确 Activation——因为连"正确的落点是什么"都没有定义，AUDIT 更无从判断"落点是否正确""内容是否符合该落点的 Schema 要求"。
- 已知范围：本 Proposal 的证据同样来自单一 Run（`ZH-20260810-001`），共 4 条实际触发的 CV 记录（CV001–CV004）。参数库中标记为 `当前状态=ACTIVE 且 触发资格=是` 的 CV 记录总数尚未清点，本 Proposal 不假设已核实全部记录都存在同样问题。

## 5. 待决策问题

1. CV 变量的类型归属（Global Rule / Run-specific obligation）应该在哪里声明——参数库记录本身新增一个字段，还是由 COMPILE 每次按题型/内容动态判断？
2. 如果允许"同时出现在两个字段"（ID 进 triggered_rule_ids，实例化描述进 acceptance_criteria），是否违反 Compiler V1 对 `acceptance_criteria` "不得复制 Runtime 通用条款"的禁止性规定？如果不违反，边界在哪里（ID 引用 ≠ 复制正文，但"实例化描述"和"复制正文"之间的界线由谁划定）？
3. 分类权归属：是 COMPILE 节点自行拥有判断权（类似 Structure 匹配的 Decision Right），还是这个分类应该在参数库治理阶段就确定好、COMPILE 只是读取，不做二次判断？
4. 历史已发布生产（如 `productions/ZH-20260808-002`、`ZH-20260808-003`）中出现的 `Parameter_Call-v1.md` 这类旧对象（Compiler V1 已将其合并入 Execution IR），是否隐含了一种历史上默认的 CV 落点约定，值得在制定新 Schema 时参考？

## 6. 候选方案（未评估，未决策，仅供 Governance Plane 参考）

- 方案一：在 `production_variable_library.md` 每条变量记录新增 `Activation Target` 字段，取值 `GlobalRule | RunSpecific`，由治理评审在变量定稿时一次性确定，COMPILE 只读取不判断。
- 方案二：不改参数库，改为在 `Execution IR` Schema 中新增第三个正式字段（例如 `activated_content_variables`），专门承载 CV 类型的激活记录，与 `triggered_rule_ids`（纯规则 ID）、`acceptance_criteria`（纯 Run 特有义务）三者并列，各自单一职责。
- 方案三：统一裁定 CV 变量一律按 `acceptance_criteria` 处理（因为 CV 天然需要"本 Run 如何体现"的实例化描述），`triggered_rule_ids` 只保留给不需要实例化、WRITE 直接照原文执行的规则（如 `知乎ACTIVE规律快照.md` 中的通用传播规律）。

本 Proposal 不推荐上述任一方案，候选方案的取舍、组合或另拟新方案，由 Governance Plane 决定。
