# 知乎OS Compiler Data Flow V1

Status：ACTIVE_SCHEMA

本文件定义知乎OS Compiler各层输入、输出和文件产物。

目标：让任何执行者在 5 分钟内知道每层吃什么、吐什么。

## 1. 数据流总览

```text
Question
↓
Analyzer.json
↓
Structure Match.json
↓
Router
↓
IR.json
↓
Runtime Assembly
↓
Writer Input Package.json
↓
Writer Prompt
↓
Draft.md
↓
QA Report
↓
Feedback.json
↓
Failure Pattern
```

## 2. L1 Analyzer

### 输入

```text
Question
Question URL
Platform signals
Historical asset match
Runtime ACTIVE snapshots
```

### 输出：Analyzer.json

```json
{
  "question": "",
  "question_url": "",
  "platform": "知乎",
  "problem_type": "",
  "user_intent": "",
  "hidden_constraints": [],
  "main_variable": "",
  "auxiliary_variables": [],
  "core_mechanism": "",
  "selection_reason": "",
  "risk_notes": []
}
```

### 禁止

- 不写正文。
- 不写开头、结尾、金句。
- 不评价 AI 味。
- 不维护表达规则。

## 3. L2 Production Card IR

### 输入

```text
Analyzer.json
Runtime variable snapshot
Runtime structure snapshot
Router result
Structure Match.json
```

### 输出：IR.json

```json
{
  "question": "",
  "question_url": "",
  "platform": "知乎",
  "core_judgment": "",
  "core_mechanism": "",
  "route": "",
  "outline": [],
  "ending_judgment": "",
  "forbidden": [],
  "publish_target": ""
}
```

### 禁止

- 不写表达风格。
- 不写 AI 味。
- 不写阅读节奏。
- 不写 PD / RR / RE / BT 参数。
- 不复制 Writer Prompt 或 QA 标准。

## 3.1 L1.5 Router

## 2.1 L1.2 Structure Matcher

### 输入

```text
Analyzer.json
Runtime structure snapshot
Historical asset match
Production variable snapshot
```

### 输出：Structure Match.json

中文字段为人审权威，英文字段只做脚本兼容。

```json
{
  "运行编号": "",
  "结构匹配": {
    "选中结构": "",
    "结构名称": "",
    "结构版本": "",
    "选择理由": [],
    "匹配证据": [],
    "未选结构": [],
    "置信度": "high | medium | low",
    "匹配分": 0,
    "来源": "runtime/知乎结构库快照.md"
  },
  "structure_match": {
    "selected_structure_id": "",
    "selected_structure_name": "",
    "structure_version": "",
    "confidence": "",
    "score": 0,
    "evidence": []
  }
}
```

### 禁止

- 不写正文。
- 不修改 Analyzer。
- 不修改 ACTIVE 结构库。
- 不读取 Research Layer 未发布候选结构。

## 3.1 L1.5 Router

### 输入

```text
Analyzer.json
Structure Match.json
Runtime ACTIVE snapshots
Historical asset match
Production variable snapshot
```

### 输出：Router result

```json
{
  "structure_id": "",
  "active_rules": [],
  "behavior_targets": [],
  "cr_target": "",
  "quality_parameters": [],
  "material_requirements": []
}
```

### 禁止

- 不写正文。
- 不修改 Analyzer。
- 不修改 IR 决策。
- 不复制 ACTIVE 资产全文。

## 3.2 L2.5 Runtime Assembly

### 输入

```text
IR.json
Router result
Structure Match.json
Runtime ACTIVE snapshots
Reasoning Protocol
Expression Protocol
Production Card / locked run constraints
```

### 输出：Writer Input Package.json

Schema：

```text
docs/Writer Input Package Schema V1.md
```

### 禁止

- 不修改 IR。
- 不新增结构、变量、事实或机制。
- 不复制全文协议。
- 不把 Package 当作第二规则权威。

## 4. L3 Writer Prompt

### 输入

```text
Writer Input Package.json
Fixed Writer Prompt version
```

### 输出

```text
Writer input package
```

### 规则

Writer Prompt 只维护表达编译规则：

- 人话转换。
- 参数隐写。
- 场景承接。
- 节奏和留白。
- 避免培训课、报告腔和管理学腔。

Writer Prompt 不输出业务判断，不修改 IR。

## 5. L4 Writer

### 输入

```text
Writer Input Package.json
Writer Prompt
```

### 输出：Draft.md

```markdown
正文全文
```

### 禁止

- 不修改 IR。
- 不新增主变量。
- 不新增事实。
- 不向上游反问。
- 不输出分析过程。

## 6. L5 QA

### 输入

```text
IR.json
Writer Input Package.json
Draft.md
```

### 输出：QA Report

```json
{
  "qa_a": {
    "follow_card": true,
    "core_judgment_preserved": true,
    "new_variable_added": false,
    "publish_blocker": false,
    "notes": []
  },
  "qa_b": {
    "ai_score": 0,
    "repeat_score": 0,
    "zhihu_feel_score": 0,
    "collection_value_score": 0,
    "parameter_visible": false,
    "notes": []
  },
  "obligation_coverage": [
    {
      "obligation": "",
      "source_contract": "",
      "result": "PASS | PARTIAL | WARNING | FAIL",
      "evidence": [],
      "problem": ""
    }
  ],
  "decision": "PASS | REVISE | BLOCK"
}
```

### 禁止

- QA 不重写正文。
- QA 不修改 IR。
- QA 不修改 Writer Input Package。
- QA 不修改 Writer Prompt。

## 7. L6 Feedback

### 输入

```text
Question
IR.json
Draft.md
QA Report
Publish data
Engineering metrics
```

### 输出：Feedback.json

```json
{
  "question": "",
  "question_url": "",
  "publish_url": "",
  "quality_metrics": {
    "qa_a_pass": false,
    "qa_b_pass": false,
    "ai_risk": "",
    "repeat_risk": "",
    "collection_point_done": false,
    "publishable": false
  },
  "engineering_metrics": {
    "ir_chars": 0,
    "writer_prompt_changed": false,
    "manual_edit_count": 0,
    "token_cost": 0,
    "elapsed_minutes": 0,
    "debug_difficulty": "low | medium | high"
  },
  "failure_patterns": []
}
```

## 8. Failure Pattern

失败模式只记录重复问题，不直接升级协议。

### 输出：Failure Pattern Record

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
  "upgrade_candidate": false
}
```

### 升级闸门

同一失败模式累计 3 次，才允许进入系统升级评审。

未满 3 次时：

- 只记录。
- 不改协议。
- 不改 Writer Prompt。
- 不改模板。

## 9. 版本策略

`Compiler` 作为架构名称保持稳定。

升级版本绑定到各层组件：

- Analyzer Schema
- IR Schema
- Writer Input Package Schema
- Writer Prompt
- QA Schema
- Feedback Schema

不要因为 Writer Prompt 升级就把整个 Compiler 改成 V2。
