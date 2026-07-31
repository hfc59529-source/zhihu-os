# Failure Pattern 模板

```json
{
  "pattern_id": "",
  "layer": "Analyzer | IR | Writer Prompt | Writer | QA | Feedback",
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

## 使用规则

- 单次问题只记录，不升级。
- 同一失败模式累计 3 次，才允许进入系统升级评审。
- 未满 3 次不得修改协议、模板、Writer Prompt 或 QA 标准。
- 失败模式必须归属到唯一层。
- 如果无法归层，先记录为 `layer=Unknown`，不得升级。
