# 知乎OS Structure Evolution V1

状态：ACTIVE_SCHEMA

本文件定义知乎OS的结构进化机制。

它不属于日常生产链，不直接决定单篇文章怎么写。它属于 Research Layer，负责把知乎爆款样本拆成候选结构，经过验证后发布为 ACTIVE 结构，再由生产链调用。

## 1. 总链路

```text
Research Layer
爆款样本
↓
案例分析
↓
传播规律
↓
候选结构
↓
规律验证
↓
ACTIVE结构
═══════════════
Production Layer
Question
↓
Analyzer
↓
Structure Matcher
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
QA
↓
Feedback
═══════════════
Learning Layer
收益
↓
复盘
↓
规律验证
↓
Research
```

## 2. Research Layer

Research Layer 只负责发现和验证结构，不直接进入生产。

输入：

- 知乎站内爆款样本。
- Top 回答结构路径。
- 评论触发点。
- 收藏点。
- 低表现回答反例。
- 本账号发布收益复盘。

输出：

- 候选结构。
- 传播规律。
- 结构验证记录。
- ACTIVE 结构升级建议。

Research Layer 禁止：

- 直接修改 Runtime Assembly。
- 直接修改单篇 IR。
- 直接影响 Writer。
- 未经验证把候选结构写入 `runtime/知乎结构库快照.md`。

## 3. Structure Lab

Structure Lab 是 Research Layer 内的结构实验室。

它把旧系统中的“爆款案例分析”和“传播规律提炼”重新归位为结构进化流程，而不是日常知识升级。

```text
爆款样本
↓
拆首屏
↓
拆正文推进
↓
拆认知奖励
↓
拆互动触发
↓
形成候选结构
↓
进入验证
```

候选结构必须记录：

| 中文字段 | 说明 |
| --- | --- |
| 结构编号 | 例如 CANDIDATE-08 |
| 结构名称 | 结构的人类可读名称 |
| 来源样本 | 来自哪些问题和回答 |
| 适用题型 | 适合哪些问题类型 |
| 触发条件 | 什么题应该用 |
| 禁用条件 | 什么题不能用 |
| 正文骨架 | 正文推进步骤 |
| 行为目标 | 服务停留、看完、收藏、评论或转发中的哪些 |
| 传播规律 | 为什么读者会继续读、收藏或评论 |
| 反例 | 该结构在哪些样本失败 |
| 验证状态 | DISCOVERED / CANDIDATE / REVIEW / ACTIVE / DEPRECATED / ARCHIVED |

## 4. ACTIVE 升级门槛

候选结构进入 ACTIVE 必须满足：

- 来自多个知乎高表现样本，不是单篇灵感。
- 有同题或相邻题型低表现反例对照。
- 能明确说明适用题型、触发条件和禁用条件。
- 至少经过本账号实验验证。
- 收益不低于同题型或同结构可比中位数。
- 不与现有 ACTIVE 结构同义重复。

未满足前，只能保留在 Research Layer，不得进入 Production Layer。

## 5. 生产触发边界

Production Layer 永远只触发 ACTIVE 结构。

Structure Matcher 只能读取：

- `runtime/知乎结构库快照.md`
- `production_variable_library.md` 中触发资格=是的 ACTIVE 变量
- 当前 Analyzer 输出
- 历史资产检索摘要
- 账号画像执行快照

Structure Matcher 不得读取未发布的候选结构、单篇爆款拆解原文或未验证研究结论。

## 6. 中文字段原则

日常运行产物优先使用中文字段。为脚本兼容可以保留英文别名，但中文字段必须存在。

例如：

```json
{
  "结构匹配": {
    "选中结构": "ACTIVE-01",
    "结构名称": "职场组织型回答结构",
    "选择理由": [],
    "匹配证据": [],
    "未选结构": [],
    "置信度": "high"
  },
  "structure_match": {
    "selected_structure_id": "ACTIVE-01"
  }
}
```

中文字段面向人审计，英文字段只服务脚本兼容。
