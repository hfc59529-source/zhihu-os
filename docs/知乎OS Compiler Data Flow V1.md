# 知乎OS Compiler Data Flow V1

Status：DATA_CONTRACT（不解释节点职责、七节点缘由、Governance 或 Runtime 发布逻辑，这些以 `docs/知乎OS Compiler V1.md` 为唯一权威；本文件不具备执行权威，执行权威只来自 `runtime/ACTIVE_MANIFEST.md` 中 `Status: ACTIVE` 的 Manifest）

本文件只回答：每个节点吃什么对象、吐什么对象、对象最小 Schema 是什么、对象由谁拥有、下一节点是谁。

## 1. 数据流总览

```text
Raw Input
↓
Input Package        （owner: INPUT）
↓
Decision              （owner: DECISION）
↓
Execution IR          （owner: COMPILE）
↓
Draft                 （owner: WRITE）
↓
AuditResult            （owner: AUDIT）
↓
Approval                （owner: REVIEW）
↓
Release                （owner: RELEASE）
```

WRITE 有重入分支，不新增节点：

```text
Execution IR + Current Draft + Approved Issues → Draft-vN   （owner: WRITE）
```

AUDIT 的退回不新增节点，由 `AuditResult.Issues[].Return Stage` 直接路由回 INPUT / DECISION / COMPILE / WRITE 中的一个。

## 2. INPUT

输入：

```text
Raw Input
  question
  question_url
  question_description
  platform_signals
  benchmark_answers[]   # 同题 Top3 高赞回答原文
```

输出：`Input Package`

```json
{
  "source_facts": {
    "question": "",
    "question_url": "",
    "question_description": "",
    "necessary_background": [],
    "platform_signals": {}
  },
  "benchmark_context": {
    "answers": [
      {"rank": 0, "author": "", "summary": "", "url": ""}
    ]
  },
  "duplicate_check": {
    "is_duplicate": false,
    "matched_history_id": ""
  }
}
```

下一节点：DECISION。

## 3. DECISION

输入：`Input Package`

输出：`Decision`

```json
{
  "reality": "",
  "main_gap": "",
  "transformation": "",
  "core_judgment": "",
  "frozen": true
}
```

`frozen: true` 后本对象不得被任何下游节点改写；退回重做只能整体退回 INPUT/DECISION，产生新的 `Decision` 对象，不得原地修改。

下一节点：COMPILE。

## 4. COMPILE

输入：`Decision`

输出：`Execution IR`

```json
{
  "reasoning_path": {
    "reader_mental_model": "",
    "false_inference": "",
    "breaking_point": "",
    "mechanism": "",
    "transformation": ""
  },
  "structure": {
    "selected_structure_id": "",
    "match_evidence": []
  },
  "material_boundary": {
    "allowed": [],
    "forbidden": []
  },
  "expression_constraints": [],
  "acceptance_criteria": [
    {"id": "", "requirement": ""}
  ]
}
```

`expression_constraints` 与 `acceptance_criteria` 只能是本次 Run 特有条目，不得复制 Runtime.Writer Rules / Runtime.Audit Rules 中已存在的通用条款。

下一节点：WRITE。

## 5. WRITE

输入（首次执行）：

```text
Execution IR
```

输入（修复重入）：

```text
Execution IR
Current Draft
Approved Issues            # AuditResult.Issues 中被判定需要修改的子集
```

输出：`Draft`

```json
{
  "run_id": "",
  "version": "v1",
  "body": "",
  "based_on_execution_ir": true
}
```

下一节点：AUDIT。

## 6. AUDIT

输入：

```text
Execution IR
Draft
```

输出：`AuditResult`

```json
{
  "result": "PASS | ISSUES",
  "issues": [
    {
      "expected_source": "ExecutionIR.AcceptanceCriteria.<id> | AuditRule.<id>",
      "expected": "",
      "actual": "",
      "violation_source": "ExpressionConstraints | AcceptanceCriteria | Structure | MaterialBoundary | Reality | MainGap | Transformation | SourceFacts",
      "return_stage": "WRITE | COMPILE | DECISION | INPUT"
    }
  ]
}
```

`return_stage` 由 `violation_source` 查 Architecture Routing Table 机械映射得出（映射表定义见 `知乎OS Compiler V1.md` 第7节；这张表是流水线级共享路由规则，不属于 Runtime.Audit Rules，AUDIT 和 REVIEW 都只是调用方），不是 AUDIT 自行判断的自由字段。

`result: PASS` 时下一节点：REVIEW。
`result: ISSUES` 时按每条 `return_stage` 分别退回对应节点，产生该节点的新版本对象。

## 7. REVIEW

输入：

```text
Draft
AuditResult（result: PASS）
```

输出：`Approval`

```json
{
  "run_id": "",
  "decision": "USER_APPROVED | USER_REJECTED",
  "rejected_issues": [
    {
      "user_feedback": "",
      "violation_source": "ExpressionConstraints | AcceptanceCriteria | Structure | MaterialBoundary | Reality | MainGap | Transformation | SourceFacts",
      "return_stage": "WRITE | COMPILE | DECISION | INPUT"
    }
  ]
}
```

`rejected_issues[]` 只做 Issue Type Classification（`user_feedback` + `violation_source` → 查 Architecture Routing Table 得出 `return_stage`），不复用 `AuditResult.issues` 的 `expected/actual/expected_source` 字段——用户拒绝的理由可能不对应任何一条已声明的 Acceptance Criteria 或 Audit Rule（例如"核心判断我不认"），不得为了凑 Schema 伪造一条合同违规。

`decision: USER_APPROVED` 时下一节点：RELEASE。
`decision: USER_REJECTED` 时按每条 `return_stage` 分别退回 INPUT / DECISION / COMPILE / WRITE，不一律退回 WRITE；退回节点产生新版本对象后重新沿流水线向下，最终重新进入 AUDIT，不直接跳回 REVIEW。

未经 AUDIT `result: PASS` 的 Draft 不得进入本节点。

下一节点：RELEASE（仅 `decision: USER_APPROVED` 时）。

## 8. RELEASE

输入：

```text
Approval（decision: USER_APPROVED）
Draft
Runtime Version
```

输出：`Release`

```json
{
  "run_id": "",
  "runtime_version": "",
  "released_at": "",
  "status": "RELEASED"
}
```

无下一节点（终点）；`Release` 对象是本次 Run 的终态记录。

## 9. 对象归属总表

| 对象 | 唯一拥有者 | 下一节点 |
| --- | --- | --- |
| Input Package | INPUT | DECISION |
| Decision | DECISION | COMPILE |
| Execution IR | COMPILE | WRITE |
| Draft | WRITE | AUDIT |
| AuditResult | AUDIT | REVIEW（PASS）或退回（ISSUES，按 return_stage） |
| Approval | REVIEW | RELEASE（USER_APPROVED）或退回 WRITE（USER_REJECTED） |
| Release | RELEASE | 无（终态） |

任何节点不得读取、缓存或复制不属于自己上一个节点交付的对象；跨节点取数只能通过上一节点的正式输出。
