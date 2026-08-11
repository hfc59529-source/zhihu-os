# 知乎OS Compiler V1

Status：DESIGN_FROZEN（架构规格已冻结，尚未进入 Runtime Release，本文件本身不具备执行权威；执行权威只来自已发布的 Runtime Manifest：`Status: TRIAL` = 受控试运行执行权威，`Status: ACTIVE` = 正式生产执行权威，`DRAFT` / `DEPRECATED` = 不具备执行权威，见 `runtime/ACTIVE_MANIFEST.md` 与 `scripts/validate_runtime_consistency.py`）

本文件定义知乎OS的内容编译流水线。V1 首版（Analyzer / Structure Matcher / Router / Slim IR / Runtime Assembly / Writer Input Package / Writer / QA-A/QA-B / Feedback 九对象链）已废弃，替换为下面的七节点流水线。废弃原因：九对象链是同一批职责在工程实现层被反复升级为独立对象的结果（Compiler 自己同时维护 Production Card IR、Runtime Assembly、Writer Input Package、Reasoning Path 四个相邻中间对象），与 README、执行协议、总AI执行中心各自维护的生产链文本互相不一致，2026-08-09 治理评审已将该不一致记录为 Observation-03（REJECTED → CLOSED，结论：不构成有效权威冲突，因为唯一发布过的 Runtime 是 07-31 Card-based 版本，本次废弃的九对象链描述本身也从未取得过 Runtime 权威）。

Compiler 的语义上游仍是 [内容架构总则](内容架构总则.md)：现实、认知落差、认知转换、平台表达是语义层描述，本文件的七节点是工程实现。Compiler 不重新定义这几个语义概念，只负责把它们编译成正文。

知乎OS不再被视为 Prompt 系统，而是内容编译器：

```text
业务语言
↓
中间表示
↓
自然语言
↓
平台反馈
```

## 1. Compiler First

任何新需求、规则、参数或优化，不允许第一反应是"加 Prompt"。

必须先回答：

```text
它属于哪一个节点？
它的唯一权威在哪里？
它是否破坏单向流？
它是否增加维护成本？
```

如果无法归节点，默认拒绝新增。

## 2. 七节点流水线

```text
INPUT
↓
DECISION
↓
COMPILE
↓
WRITE
↓
AUDIT
↓
REVIEW
↓
RELEASE
```

每个节点只有一个职责，接口定义为 Input / Decision Right / Output / Forbidden 四项，互不重叠。Structure Matcher、Router、Reasoning Path、参数触发等原九对象链中的能力，不再各自升级为独立节点，全部降级为 COMPILE 节点内部能力。REVIEW 独立于 RELEASE：AUDIT PASS 只代表审核条件满足，不代表用户已经看过正文；是否接受最终正文是一个不可压缩的独立 Decision Right（人工验收），不得压进 RELEASE 变成一个布尔前置条件——这是对齐现有 `docs/生产审计决策流程.md`、`docs/生产状态机与交接规范.md`、`data/Publish_Queue.md` 三份文件共同确认的纪律：即使 Audit Clean Pass，也不能从 AUDIT_PASS 直接跳到 RELEASE_READY。

## 3. INPUT

```text
Input:
  数据对象：
    Source Facts —— 原问题、问题描述、问题链接、必要事实、平台可见信号
    Benchmark Context —— 同题 Top3 高赞回答原文
  规则引用：
    Runtime Release → Input Rules 分区（去重判定标准、完整性判定标准）

Decision Right:
  判断信息是否完整
  判断是否与历史选题重复

Output:
  Input Package = Source Facts + Benchmark Context + 重复检查结果

Forbidden:
  不得判断"这题该不该答""这题该怎么答"（含"推荐级别"一类预判字段）
  不得写入任何已经带解释性质的字段（读者困惑、核心矛盾等属于 DECISION）
  下游节点（尤其 DECISION）不得把 Benchmark Context 中的观点、结论、判断当作
    Source Facts 使用；Benchmark Context 只能提供"读者已有认知是什么"这一事实层
```

## 4. DECISION

```text
Input:
  数据对象：Input Package
  规则引用：Runtime Release → Decision Rules 分区
    + `docs/知乎内容质量参数库_V2.md`§0 QT-QI｜问题理解系统
      （仅 QT-00 题型判断 + QI-01 提问动机 / QI-02 真实问题 / QI-03 当前认知 /
        QI-04 认知缺口 / QI-05 认知目标 / QI-06 阅读奖励 六项识别字段，
        不含该文件其余 PD / RR / RE / BT / CR 等正文质量参数——那些参数的
        消费者仍是 COMPILE/WRITE/AUDIT，不因本次修复扩大到 DECISION）

  Migration Fix（2026-08-11，TRIAL Runtime）：
    Production Card 退役、职责迁入 Compiler V1 时，QT-QI 问题理解识别域未被
    任何现行节点正式继承，DECISION 此前直接从 Input Package 跳到 Main Gap，
    未核对用户表层问题背后的真实提问类型。本修复把 QT-QI 六项识别字段列为
    DECISION 的强制输入，不改变 QT-QI 定义本身，不把该文件其余质量参数域
    授权给 DECISION。

Decision Right:
  先完成 QT-QI 识别（QT-00 题型 + QI-01～QI-06），再锁定
  Reality / Main Gap / Transformation / Core Judgment，一次性冻结
  （对应《内容架构总则》的语义冻结门）

Output:
  Decision（Reality / Main Gap / Transformation / Core Judgment 四个字段
    + QT-QI 识别记录：QT-00 题型判断、QI-01～QI-06 六项识别结果）

Forbidden:
  不涉及"怎么写"（结构、开头、句式属于 COMPILE / WRITE）
  不得引入 Input Package 之外的事实
  冻结后不得自行修改；发现问题只能整体退回 INPUT/DECISION 重做，不能局部改
  Main Gap / Transformation 不得在未说明理由的情况下，把 QI-02 识别出的
    真实问题类型替换为另一种类型（如把"求解释"换成"求判断"）；如确有理由
    认为 Benchmark Context 已使原始问题类型不再构成有效增量，必须在 Main Gap
    段落中显式写出这次类型替换的理由和证据，不得只靠"高赞已讲透"一句带过


## 5. COMPILE

```text
Input:
  数据对象：Decision（已冻结）
  规则引用：Runtime Release → Compile Rules 分区
    （含结构库快照、ACTIVE 变量快照——原 Structure Matcher / Router 的匹配能力，
      降级为本节点内部逻辑，不再是独立节点）

Decision Right:
  把 Decision 编译成：
    Reasoning Path（Reader Mental Model → False Inference → Breaking Point →
                    Mechanism → Transformation）
    Structure（本题调用哪个 ACTIVE 结构、匹配依据，以及该结构对本 Run
      实例化后的具体执行义务：required_steps 本 Run 必须完成的结构步骤，
      逐条对应该 ACTIVE 结构定义的步骤；step_obligations 每一步在本 Run 里
      具体要求做到什么——这两项不是复制整个结构库，只保存本 Run 已实例化
      后的义务，因此不违反 SSP；没有它们 AUDIT 就没有 Expected 可核对
      "Structure 义务有没有缺失"）
    Material Boundary（哪些事实/案例可用，哪些禁用）
    Expression Constraints（本篇特有的表达约束）
    Acceptance Criteria（本篇特有的、AUDIT 要核对的具体义务）
    Triggered Rule IDs（本 Run 按 Runtime.Compile Rules 的条件触发规则，
      从 Runtime.Audit Rules 的固定候选集合中，实际命中了哪些 Global Rule
      ID——只存 ID，不存规则正文，规则正文唯一权威仍在 Runtime Release；
      没有这个字段，AUDIT 就不知道本 Run 该加载哪些条件触发的 Audit Rule）

  TRIAL Runtime compatibility rule（2026-08-11）：
    Triggered Rule IDs 仅在当前 Runtime Release 已发布正式 ID-bearing
    conditional Audit Rules 固定候选集合时生成；若当前 Runtime Release
    尚未发布此类候选集合，Triggered Rule IDs 必须填为 `[]`，并视为本字段
    已如实完成，不视为 Execution IR 不完整，不阻断 COMPILE → WRITE。
    `[]` 只表示当前 Runtime 没有可供本字段引用的 ID-bearing conditional
    Audit Rules，不表示 Global Operational Checks 停止执行。Global Operational
    Checks 继续由 Runtime 的 AUDIT 执行载体直接加载，不依赖 Triggered Rule IDs。
    不得复制规则正文、不得自造 Rule ID、不得影响 Execution Compliance /
    Acceptance Criteria / REVIEW / RELEASE，也不得推出通用 AuditResult 降级模型。

Output:
  Execution IR
  （Decision 与 WRITE 之间只允许这一个正式中间对象；原 Production Card IR、
    Runtime Assembly、Writer Input Package 三个相邻对象在此合并）

Forbidden:
  不得修改 Decision 四字段本身
  不得决定具体措辞句子（WRITE 的权限）
  不得省略 Acceptance Criteria，直接把"怎么写"丢给 WRITE 自由发挥
  Expression Constraints / Acceptance Criteria 只能是"本 Run 特有义务"，不得把
    Runtime.Audit Rules 中已存在的通用检查项（Global Operational Checks）复制
    进 Execution IR——通用规则永远只活在 Runtime Release 里，不允许被复制出第二份
  Triggered Rule IDs 只能是 ID 引用，不得连带复制规则正文，且不得引用
    `production_variable_library.md` 登记的内容变量（CV）
  （Proposal B 新增禁止性约束，非对原条款的重新解释——原"不得复制通用条款"仅
    约束 Runtime.Writer Rules / Runtime.Audit Rules，未涉及 Parameter Registry）：
    由内容变量（CV）编译出的 Acceptance Criteria，只能写本 Run 的 Realization
    Requirement（本篇必须具体实现什么），不得复制该 CV 在 Parameter Registry 中的
    通用定义字段（变量定义、适用题型、触发条件、触发权重等），也不得把"本题为何
    命中该 CV"这类 Trigger Basis 写进 Acceptance Criteria——AC 只保存可验收的义务，
    不保存触发证据
```

## 6. WRITE

```text
Input（首次执行）:
  数据对象：Execution IR
  规则引用：Runtime Release → Writer Rules 分区
  Output: Draft-v1

Input（修复重入 / Patch）:
  数据对象：Execution IR + Current Draft + Approved Issues
            （AUDIT 输出中被判定需要修改的部分）
  规则引用：Runtime Release → Writer Rules 分区
  Output: Draft-vN

Decision Right:
  具体措辞、段落衔接、节奏、开头收尾——"这句话怎么说"（局部推理权）

Output 运行元数据（每次执行都必须记录，不只是首次）：
  writer_model（本次实际执行 WRITE 的模型：Claude / Codex / GPT / 其它——
    第10节"Writer 可替换性"的 A/B 归因依赖这个字段，缺了它就无法验证
    模型差异，这不是"怎么写"的决策，只是执行者身份记录，不占用 Decision Right）

Forbidden:
  不得重新推导 Reality / Main Gap / Transformation / Core Judgment / Reasoning Path
  不得引入 Execution IR 之外的案例、数据、人物、公司
  不得暴露参数名、字段名、系统术语
  Patch 模式下，Execution IR 未标记为 Approved Issues 对应位置的内容，逐字保留，
    不得因"顺手一起改"变动
```

## 7. AUDIT

```text
Input:
  数据对象：Execution IR + Draft
  规则引用：Runtime Release → Audit Rules 分区（Global Operational Checks）

Decision Right:
  核对 Draft 是否兑现两类合同：
    A. Execution Compliance —— Execution IR 的 Run-specific Acceptance Criteria
       是否兑现（Reasoning Path 有没有漏步骤、Material Boundary 有没有越界、
       指定机制有没有兑现、Structure 义务有没有缺失）
    B. Operational Quality Checks —— Runtime.Audit Rules 中已具备明确操作定义、
       能给出 PASS/FAIL 的通用表达约束（例：短距离重复、禁止参数名显形、
       禁止引入未授权案例）

Output:
  AuditResult：PASS，或 Issues[]，每条包含：
    Expected Source: Execution IR.AcceptanceCriteria.<N> 或 AuditRule.<ID>
    Expected
    Actual
    Violation Source（违反的是 Execution IR 的哪个字段，还是哪条 Audit Rule；
      取值见 Architecture Routing Table，AUDIT 不拥有这张表，只是第一个使用者）
    Return Stage（由 Violation Source 查 Architecture Routing Table 得出，
      AUDIT 不裁量，这张表不属于 Runtime.Audit Rules，是全流水线共享的路由规则，
      定义见本节末尾）

Forbidden:
  不得使用 Expected Source（Execution IR 或已发布 Audit Rule）之外的任何标准；
    "觉得应该更好""更有阅读价值"一类临时想到的标准不得进入审核
  不得重写正文、不得提供替代文案
  不得质疑或重新推导 Decision / Execution IR 本身——发现问题只能按 Return Stage
    整体退回，不能自己纠正
  SUPPORTED 的历史 Observation 不能被直接引用为 Expected Source；必须先经
    Governance 提交为正式 Runtime.Audit Rule，才能成为合法引用对象（区分
    Detectability 可判定性与 Effect Validity 效果有效性：Observation 验证的是
    后者，能否进入 AUDIT 取决于前者是否已经形成可发布的操作定义）
```

**Architecture Routing Table（violation_source → return_stage）**：这张表是流水线级的路由规则，不属于 Runtime.Audit Rules，不由 AUDIT 拥有；AUDIT 和 REVIEW 都只是调用方，不得各自维护一份副本。

```text
Expression Constraints / Acceptance Criteria 未兑现但 IR 本身没错 → WRITE
Structure / Material Boundary 与 Decision 对不上（COMPILE 编译错了）→ COMPILE
Reality / Main Gap / Transformation 本身站不住 → DECISION
支撑 Decision 的事实本身不存在或错误 → INPUT
```

## 8. REVIEW

```text
Input:
  数据对象：Draft + AuditResult（result: PASS）
  规则引用：Architecture Routing Table（仅用于 violation_source → return_stage
    的机械映射；不引用 Runtime.Audit Rules——REVIEW 不核对合同条款，AUDIT 已核对完）

Decision Right:
  人（User）判断最终正文是否接受，唯一、不可压缩的验收权
  （对应现有 `READY_FOR_USER_REVIEW` → `USER_APPROVED` / `USER_REJECTED` 状态转移）。
  若判断为 USER_REJECTED，把每条 user_feedback 定位到 violation_source
  是同一个 Decision Right 的组成部分，不是脱离验收权的第二次判断——一个人说
  "这段我不信"时，"不接受"和"为什么不接受、问题出在哪一层"是同一次判断，
  不是先后两次。violation_source 的分类权唯一属于 User；系统/Claude/GPT
  可以草拟建议分类供参考，但不得替 User 做出最终分类，草拟建议必须经 User
  确认才能写入 Approval。violation_source 确定后，映射到 return_stage
  才是机械查表，不再需要判断。

Output:
  Approval：USER_APPROVED，或 USER_REJECTED（附 rejected_issues[]，每条：
    user_feedback（User 的原始理由，判断权归 User）
    violation_source（User 判断/确认的分类，不是查表得出）
    return_stage（violation_source 查 Architecture Routing Table 机械得出）
    不要求填 Expected/Actual/Expected Source：用户拒绝的可能是
    "核心判断我就不认"，此时并不存在被违反的 AcceptanceCriteria 或 AuditRule，
    强行填 Expected Source 等于伪造一条合同违规）

Forbidden:
  不得直接修改正文（发现问题只能标注，由 return_stage 指向的节点处理）
  不得修改 Decision / Execution IR
  不得跳过：AUDIT 未 PASS 的 Draft 不得进入 REVIEW
  Claude / GPT / Codex 不得替 User 最终确定 violation_source，只能提供草拟建议
  不得把 return_stage 当成可裁量字段——它是对已确定 violation_source 的机械映射
```

USER_REJECTED 的退回路径：按每条 `rejected_issues[].return_stage` 分别退回 INPUT / DECISION / COMPILE / WRITE 对应节点，不一律退回 WRITE。退回 WRITE 时，`Current Draft + 该条 user_feedback` 作为 Approved Issues 输入；退回 INPUT/DECISION/COMPILE 时，产生该节点的新版本对象，重新沿流水线向下走，最终重新进入 AUDIT，不直接跳回 REVIEW（必须重新确认审核条件满足）。Codex 不得借用户拒绝直接改写正文。

## 9. RELEASE

```text
Input:
  数据对象：Approval（USER_APPROVED） + Draft + Runtime Version
  规则引用：Runtime Release → Release Rules 分区（发布前置条件）

Decision Right:
  无内容判断权，仅状态转换：READY_FOR_RELEASE → RELEASED，
    记录 Run ID + Runtime Version + 时间戳

Output:
  Release（发布记录，绑定生产该内容时使用的 Runtime Version）

Forbidden:
  不做任何内容判断
  没有 USER_APPROVED，不得转换状态，无例外（Audit PASS 不能替代 USER_APPROVED）
```

## 10. Writer 可替换性

Writer（对应 WRITE 节点执行者）是可替换模型，可选执行模型包括 Claude、Codex、GPT 及后续其它模型。

A/B 测试时，唯一变量必须是 Writer 模型本身。禁止同时改变 Execution IR、Writer Rules、Audit Rules，否则无法判断模型差异。

## 11. SSP｜Single Source of Policy

任何规则只有一个权威来源。其它节点只能引用，不得复制维护。

| 规则 | 唯一权威 |
| --- | --- |
| 读者真实困惑 / 事实边界 | INPUT |
| Reality / Main Gap / Transformation / Core Judgment | DECISION |
| 正文路线、结构、素材边界、本篇特有验收标准 | COMPILE（写入 Execution IR） |
| 内容变量（CV）Identity：定义、适用题型、触发条件、触发权重 | `production_variable_library.md`（Parameter Registry） |
| 内容变量（CV）本 Run Instantiation：本篇必须具体实现什么（Realization Requirement） | COMPILE（写入 Execution IR.acceptance_criteria） |
| 人话表达、节奏、留白 | Runtime.Writer Rules |
| 通用可判定表达检查（重复、参数显形等） | Runtime.Audit Rules |
| 最终正文是否接受 | REVIEW（人工，唯一权威，不得由 AUDIT 或 RELEASE 代为判断） |
| 发布前置条件 | Runtime.Release Rules |
| 收益评估 | Learning Plane（不在本流水线内，见下） |

如果同一规则出现在多处，必须删除重复项，只保留唯一权威。

## 12. 单向流与 Learning Plane 回路

```text
Governance Plane（治理：提出变更 → 批准 → Runtime Release）
     ↓ 发布
Runtime Plane（当前唯一允许执行的规则与知识快照）
     ↓ 供给
INPUT → DECISION → COMPILE → WRITE → AUDIT → REVIEW → RELEASE
                                                    ↓ 结果
                                                 Metrics
                                                    ↓
                                            Learning Plane（数据 → 证据 → 假设 → 验证）
                                                    ↓ change proposal
                                              回到 Governance Plane
```

禁止反向修改：

- COMPILE 不得修改 Decision。
- WRITE 不得修改 Execution IR，不得重新推导 Decision。
- AUDIT 不得修改 Draft、Execution IR、Decision。
- REVIEW 不得修改正文、Execution IR、Decision。
- Learning Plane 不得直接改 Runtime；只能形成 Change Proposal 交回 Governance Plane。

## 13. 失败模式升级闸门

任何 Runtime Rules（Input/Decision/Compile/Writer/Audit/Release Rules）的升级，必须先进入 Failure Pattern 记录。

升级条件：

```text
同一失败模式
↓
累计 3 次
↓
归属节点明确（由 AUDIT 的 Return Stage 或人工审核确定）
↓
证据可复查
↓
进入 Governance Plane 变更评审
```

未满 3 次时：只记录，不改 Runtime Rules。

## 14. 试运行门槛

七节点流水线进入正式生产前，需完成至少 10 篇真实知乎生产验证，且满足：

- Execution IR 持续保持精简。
- Writer Rules 基本不需要单题改动。
- AUDIT 能通过 Violation Source 快速定位问题所属节点。
- 人工修改次数下降。
- 正文质量不低于旧链路。
- 工程成本没有显著上升。

10 篇前禁止：批量迁移历史数据、删除旧资产、重构 Notion 首页或数据库结构。

## 15. 待处理事项（本次未处理，如实记录）

- `runtime/ACTIVE_MANIFEST.md` 的 Partitions 仍沿用旧资产分类，未按本文件的七节点重新组织；本文件本身也未进入任何 Runtime Release，Status 为 DESIGN_FROZEN，不具备执行权威。
- Manifest Contract 的 Status 枚举已扩展为 `DRAFT | TRIAL | ACTIVE | DEPRECATED`（`scripts/validate_runtime_consistency.py` 的 `VALID_STATUS`、`scripts/release_runtime.py` 的 `--status` 参数化均已完成并测试），但尚未实际执行过一次 TRIAL 发布——`runtime/ACTIVE_MANIFEST.md` 仍是 `Status: DRAFT`。
- Production Card、Skill006、Writer Input Package Schema 等旧对象的具体退场方式（删除 / 归档 / 内容迁入 Execution IR 载体）尚未落地，仅在设计层完成了职责判断（见对话记录中"现有系统哪些东西保留，哪些降级"一节）。
- `data/parameter_call_log.md` 的记录表列结构已扩展（Trigger Matrix Trace 字段：Experiment ID / 推荐变量 / 实际激活变量 / 未激活变量 / 预期结果），但截至本次修改仍是空表——尚未有任何 TRIAL Run 产生过一条新结构的记录。
