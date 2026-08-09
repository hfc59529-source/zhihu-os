# Failure Pattern 模板

```json
{
  "pattern_id": "",
  "violation_source": "INPUT | DECISION | COMPILE | WRITE | Unknown",
  "return_stage": "INPUT | DECISION | COMPILE | WRITE",
  "symptom": "",
  "root_cause": "",
  "evidence": [],
  "occurrence_count": 1,
  "first_seen": "",
  "last_seen": "",
  "upgrade_candidate": false,
  "notes": ""
}
```

`violation_source` / `return_stage` 的取值和对应关系由 `docs/知乎OS Compiler V1.md` 第7节 Architecture Routing Table 唯一权威定义，本模板不重复维护映射规则：

```text
Expression Constraints / Acceptance Criteria 未兑现但 IR 本身没错 → WRITE
Structure / Material Boundary 与 Decision 对不上 → COMPILE
Reality / Main Gap / Transformation 本身站不住 → DECISION
支撑 Decision 的事实本身不存在或错误 → INPUT
```

REVIEW / AUDIT / RELEASE 本身不是 Failure Pattern 的归属层：AUDIT 只是发现问题、查表得出 return_stage 的角色；REVIEW 是 User 验收权，不产生独立失败模式；RELEASE 无内容判断权。所有失败模式最终必须归属到 INPUT / DECISION / COMPILE / WRITE 四个节点之一。

## 使用规则

- 单次问题只记录，不升级。
- 同一失败模式累计 3 次，且归属节点明确（由 AUDIT 的 Return Stage 或人工审核确定），才允许进入 Governance Plane 变更评审。
- 未满 3 次不得修改 Runtime Rules（Input/Decision/Compile/Writer/Audit/Release Rules）。
- 失败模式必须归属到唯一节点。
- 如果无法归属，先记录为 `violation_source=Unknown`，不得升级。
