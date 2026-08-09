# Writer Input Package Schema V1

Status: DEPRECATED

本文件定义的 Analyzer → Router → Slim IR → Runtime Assembly → Writer Input Package 装配链已被 `docs/知乎OS Compiler V1.md` 的七节点流水线取代：COMPILE 与 WRITE 之间只保留 Execution IR 一个正式中间对象，本文件定义的 Writer Input Package 对象不再存在。本文件定义的 required_steps、step_obligations、material、acceptance 等能力已并入 Execution IR（见 Compiler V1 第5节 COMPILE）。

本文件只作历史参考保留，不得被当前 Codex / Claude / GPT 单篇任务引用、执行或转写；不重写为 Execution IR V2，避免形成第二个 Execution IR Schema 权威。以下为原文，保留供历史查阅。

---

本文件定义 Writer 启动前的运行时装配产物。

Writer Input Package 不是第二套 Production Card，也不是新规则库。它只保存本次 Run 实际调用的 ACTIVE 资产引用、版本和执行义务，用于让 Writer 拿到完整合同，并让 QA 能回查 obligation coverage。

## 1. 位置

```text
Question
↓
Analyzer
↓
Router
↓
Slim IR
↓
Runtime Assembly
↓
Writer Input Package
↓
Writer
↓
QA-A / QA-B
↓
Feedback
```

## 2. 原则

- IR 保持精简，只保存本篇决策。
- IR 只保存规则引用，不复制规则全文。
- Runtime Assembly 读取 ACTIVE 快照和固定协议，装配 Writer Input Package。
- Writer Input Package 保存本次运行的版本、引用和义务摘要。
- Writer Input Package 不成为规则权威；规则权威仍在 Manifest 指定文件。
- QA 必须检查 Package 中的 obligation，而不只输出总分。

## 3. JSON Schema

运行产物优先保留中文字段。以下英文字段是兼容字段；中文审计字段必须同步存在，尤其是结构相关字段。

```json
{
  "schema_version": "writer_input_package_v1",
  "run_meta": {
    "run_id": "",
    "question": "",
    "question_url": "",
    "platform": "知乎",
    "writer_model": "",
    "created_at": ""
  },
  "decision_ir": {
    "core_judgment": "",
    "core_mechanism": "",
    "route": "",
    "ending": "",
    "forbidden": []
  },
  "structure_contract": {
    "结构编号": "",
    "结构名称": "",
    "结构版本": "",
    "结构步骤": [],
    "选择理由": [],
    "匹配证据": [],
    "未选结构": [],
    "置信度": "",
    "structure_id": "",
    "structure_version": "",
    "source": "runtime/知乎结构库快照.md",
    "required_steps": [],
    "step_obligations": [],
    "forbidden_reordering": true
  },
  "behavior_contract": {
    "primary_behavior": "",
    "secondary_behavior": "",
    "cr_target": {
      "primary": "",
      "primary_goal": "",
      "secondary": "",
      "secondary_goal": ""
    },
    "reading_progression": []
  },
  "expression_contract": {
    "reasoning_protocol": {
      "id": "知乎正文推理协议 V1.0",
      "source": "docs/知乎正文推理协议 V1.0.md",
      "status": "ACTIVE",
      "obligations": []
    },
    "expression_protocol": {
      "id": "知乎正文表达协议 V3",
      "source": "docs/知乎正文表达协议 V3.md",
      "status": "ACTIVE",
      "obligations": []
    },
    "rr_obligations": [],
    "re_obligations": []
  },
  "material_package": {
    "evidence": [],
    "reality_anchors": [],
    "author_observation": [],
    "available_examples": []
  },
  "acceptance_contract": {
    "qa_a_requirements": [],
    "qa_b_requirements": [],
    "publish_gate": []
  }
}
```

## 4. QA Obligation Coverage

QA Report 必须新增 `obligation_coverage`：

```json
{
  "obligation_coverage": [
    {
      "obligation": "",
      "source_contract": "structure_contract | behavior_contract | expression_contract | material_package | acceptance_contract",
      "result": "PASS | PARTIAL | WARNING | FAIL",
      "evidence": [],
      "problem": ""
    }
  ]
}
```

没有 evidence 的 PASS 不成立。

## 5. 禁止

- 禁止把整个 ACTIVE 结构库、推理协议、表达协议全文复制进 Package。
- 禁止让 Writer Input Package 修改 IR 决策。
- 禁止让 QA 反向修改 Package、IR 或 ACTIVE 协议。
- 禁止用 Package 替代 Production Card 模板或 runtime 快照。
