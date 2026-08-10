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

## 2a. 历史证据（用户补充核查，2026-08-10）

用户直接核对了两份历史生产对象 `productions/ZH-20260808-002/Parameter_Call-v1.md` 与 `productions/ZH-20260808-003/Parameter_Call-v1.md`（Compiler V1 已把 `Parameter_Call` 这类旧对象合并进 `Execution IR`，本节只作为历史 Schema 参考，不代表现行权威）。

`ZH-20260808-002/Parameter_Call-v1.md` 原文摘录：

> Rule：Writer 写 Draft-v1 前必须声明本题拟调用哪些 CV001-CV006 及触发依据。本文件为 Draft-v1 前置声明，不是发布后倒推。
>
> ### CV002｜利益重分配
> 触发依据：老板直接获得基层信息和控制感，基层获得曝光机会，中层失去指令入口但保留收尾责任。
> 调用方式：解释越级指挥后权力、信息、责任和风险如何重新分配。

可以看到历史对象里每条 CV 实际包含三层：**CV ID（跨 Run 通用变量身份）+ 触发依据（本题为何命中）+ 调用方式（本题具体怎么实现）**。`ZH-20260808-003` 同样是 CV ID + 本题触发依据，但未像 002 那样明确单列"调用方式"一栏，两份历史对象在这一点上不完全一致。

这项历史证据表明：旧 Schema 里 CV 天然存在两个层次——**Variable Identity**（CV002 本身是什么、适用什么题型，跨 Run 复用）与 **Run Instantiation**（这一篇里 CV002 具体体现为什么、体现在哪里）。这只能证明"旧 `Parameter_Call` 存在 CV Identity + Trigger Basis + Run-specific Invocation 三层，新 Schema 没有明确对应关系"，还不能证明本次 `ZH-20260810-001` 自造第三张表就是这一"迁移丢失"直接导致的——两者之间是一个**待验证的迁移假设**，不是已证明的根因：Compiler V1 合并 `Parameter_Call` 后，历史 Run-specific Invocation 语义可能没有获得明确的新 Schema 落点，本 Run 因此自行补了一张表来承载这层信息；这个假设是否成立，需要更多证据（例如更多历史 Run 的对比、或直接询问 Compiler V1 设计者当初的取舍），本 Proposal 不代为下结论。

第三项相关证据目前**未找到**：用户核查过程中没有找到对应的"历史 CV 调用后是否发生 Realization"的审核记录（例如 Parameter Compliance 或 CV Realization 审核对象）。可以确认的只是历史系统明确规定了"调用声明"这一步，但没有证据证明它同时建立了"调用后的 Realization 验证"这一步。这一点保持未知，不假设成立或不成立。

历史行为本身只能作为设计证据，不能自动升级为新 Contract——旧系统这样做过，不代表现在就应该照搬双层写法，这一点由 Governance Plane 判断。

## 3. Contract Gap

`知乎OS Compiler Data Flow V1.md` 的 `Execution IR` Schema 只有 `triggered_rule_ids`（Global Rule ID 列表）与 `acceptance_criteria`（`{id, requirement}` 结构的 Run 特有条目）两个字段，二者用途不同；但**当前 Contract 未明确同一 CV 的 Global Identity 与 Run-specific Instantiation 是否允许分别落入两个字段**（即 CV ID 进 `triggered_rule_ids`、同时该 CV 的本 Run 实例化描述进 `acceptance_criteria` 是否合法），这正是本节要交给 Governance Plane 判断的问题之一，不应预设"二者互斥"：

- 进 `triggered_rule_ids`：意味着该变量被声明为本 Run 触发的 Global Rule；但当前 Contract 尚未在本字段定义中明确 WRITE 如何由该 ID 获取对应 Writer Rule 并执行——`知乎OS Compiler V1.md` 第6节只规定 WRITE 的输入包含"规则引用：Runtime Release → Writer Rules 分区"，并未说明这个引用动作与 `triggered_rule_ids` 列表之间是否存在、以及应该是何种绑定关系；这正是 Proposal A 指出的同一个未闭合链路在 WRITE 侧的对应表现，不应在本 Proposal 中当作既定事实预支。
- 进 `acceptance_criteria`：意味着该变量在本 Run 里被实例化为一条具体、可审的义务，Execution IR 里必须写清楚 `requirement`。

CV 变量本身兼具两种特征：它们既是"参数库"里登记的通用规则（有适用题型、触发条件，跨 Run 复用），又往往需要"本 Run 具体怎么体现"这类实例化描述（例如 CV002"利益重分配"命中后，需要说明本 Run 里利益重分配具体体现在哪个场景/哪句话）。§2a 的历史证据显示，这不是本次生产才出现的特征——旧 `Parameter_Call` 对象里已经天然存在 Variable Identity 与 Run Instantiation 两层。Data Contract 没有回答：**这种"既通用又需要实例化"的变量，激活后到底该二选一，还是需要同时出现在两个字段（ID 进 triggered_rule_ids，实例化描述进 acceptance_criteria）？**（历史证据只说明旧系统曾经双层记录，不能自动推出"现在就应该双写"——这是候选方案要评估的问题，不是本节的结论。）

**核心问题的修正表述（基于 §2a 历史证据，比原表述更准确）**：Compiler V1 把 `Parameter_Call` 合并进 `Execution IR` 时，是否丢失了"CV Identity → Run-specific Instantiation"这一层语义？如果丢失了，这两层现在应该如何在新的 `Execution IR` Schema 中合法表达？这比单纯问"CV 该塞进哪个字段"更准确地定位了问题来源。

`production_variable_library.md` 第15条虽然提到了两个落点，但只是复述 Data Contract 已有的两个字段名，没有新增归属判定规则，也没有指定"谁有分类权"——是 COMPILE 每次自行判断，还是参数库记录本身应该有一个固定字段声明类型。

## 4. 影响范围

- 直接影响：任何生产 Run 只要触发 CV 变量，COMPILE 都需要自行决定落点，缺乏统一标准，不同 Run 可能产生不一致的 Schema 处理方式（本次即自造了第三个子表）。
- 间接影响：AUDIT 阶段无法用统一标准去核对 CV 变量是否被正确 Activation——因为连"正确的落点是什么"都没有定义，AUDIT 更无从判断"落点是否正确""内容是否符合该落点的 Schema 要求"。
- 已知范围：本 Proposal 的证据同样来自单一 Run（`ZH-20260810-001`），共 4 条实际触发的 CV 记录（CV001–CV004）。参数库中标记为 `当前状态=ACTIVE 且 触发资格=是` 的 CV 记录总数尚未清点，本 Proposal 不假设已核实全部记录都存在同样问题。

## 5. 待决策问题

0.（核心问题，基于 §2a 历史证据重新表述）Compiler V1 合并旧 `Parameter_Call` 时，是否丢失了 CV Identity → Run-specific Instantiation 这一层语义，以及这两层在新 `Execution IR` 中应该如何合法表达？
1. CV 变量的类型归属（Global Rule / Run-specific obligation，或历史证据显示的"两层并存"）应该在哪里声明——参数库记录本身新增字段，COMPILE 每次动态判断，还是恢复类似旧 `Parameter_Call` 的双层记录方式？
2. 如果允许"同时出现在两个字段"（ID 进 triggered_rule_ids，实例化描述进 acceptance_criteria），是否违反 Compiler V1 对 `acceptance_criteria` "不得复制 Runtime 通用条款"的禁止性规定？如果不违反，边界在哪里（ID 引用 ≠ 复制正文，但"实例化描述"和"复制正文"之间的界线由谁划定）？
3. 分类权归属：是 COMPILE 节点自行拥有判断权（类似 Structure 匹配的 Decision Right），还是这个分类应该在参数库治理阶段就确定好、COMPILE 只是读取，不做二次判断？
4. 历史 `Parameter_Call-v1.md` 的"调用声明"步骤（Rule：Writer 写 Draft 前必须声明拟调用 CV 及触发依据）是否也应该在新 Schema 中恢复为一个显式的前置声明步骤，还是应该被现有的 COMPILE→WRITE 流程隐式覆盖？
5.（未知项，需先补证据，不属于本次可决策范围）历史系统是否曾经建立过"CV 调用后的 Realization 验证"机制？目前未找到相关记录，这一未知本身是否影响 B 的决策，需要 Governance Plane 判断是否需要先补充这项历史检索，还是可以在缺少该证据的情况下继续决策。

## 6. 候选方案（未评估，未决策，仅供 Governance Plane 参考）

- 方案一：在 `production_variable_library.md` 每条变量记录新增 `Activation Target` 字段，取值 `GlobalRule | RunSpecific`，由治理评审在变量定稿时一次性确定，COMPILE 只读取不判断。
- 方案二：不改参数库，改为在 `Execution IR` Schema 中新增第三个正式字段（例如 `activated_content_variables`），专门承载 CV 类型的激活记录，与 `triggered_rule_ids`（纯规则 ID）、`acceptance_criteria`（纯 Run 特有义务）三者并列，各自单一职责。
- 方案三：统一裁定 CV 变量一律按 `acceptance_criteria` 处理（因为 CV 天然需要"本 Run 如何体现"的实例化描述），`triggered_rule_ids` 只保留给不需要实例化、WRITE 直接照原文执行的规则（如 `知乎ACTIVE规律快照.md` 中的通用传播规律）。
- 方案四（基于 §2a 历史证据）：在 `acceptance_criteria` 的 `{id, requirement}` 结构基础上，恢复历史 `Parameter_Call` 的双层记录方式——`requirement` 字段内部区分"触发依据"（为什么本题命中，对应历史"触发依据"）与"调用方式"（本题具体怎么体现，对应历史"调用方式"），CV ID 本身不再需要额外进入 `triggered_rule_ids`，因为 CV 的 Global 身份已经由 `production_variable_library.md` 的编号本身承载。

本 Proposal 不推荐上述任一方案，候选方案的取舍、组合或另拟新方案，由 Governance Plane 决定。
