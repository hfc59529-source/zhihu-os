# 知乎OS Structure Evolution V1

状态：ACTIVE_SCHEMA（Research Layer：Structure Lab、候选结构、ACTIVE 升级门槛部分持续有效；Production Layer 接口已随 `docs/知乎OS Compiler V1.md` 七节点重写，见第1、5节）

本文件定义知乎OS的结构进化机制。Node（Structure Matcher 作为独立生产节点）已废弃，但 Capability（结构研究、候选结构验证、ACTIVE 升级）和 Research Protocol 均未失效——只是连接 Production Layer 的接口需要对齐 Compiler V1。

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
↓
Runtime Compile Rules（`runtime/知乎结构库快照.md`）
═══════════════
Production Layer（七节点，权威见 `docs/知乎OS Compiler V1.md`）
INPUT
↓
DECISION
↓
COMPILE（结构选择能力：读取 Runtime Compile Rules，产出 Execution IR.Structure）
↓
WRITE
↓
AUDIT
↓
REVIEW
↓
RELEASE
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

- 直接修改 Execution IR。
- 直接修改单篇 Decision。
- 直接影响 WRITE。
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

## 5. 生产触发边界（COMPILE 的结构选择能力）

Production Layer 永远只触发 ACTIVE 结构。原 Structure Matcher 节点已废弃，其结构匹配能力降级为 COMPILE 节点的内部能力（见 Compiler V1 第5节），不再是独立生产节点，不产生独立中间对象；匹配结果只写入 Execution IR 的 Structure 字段。

COMPILE 的结构选择能力只能读取：

- `runtime/知乎结构库快照.md`
- `production_variable_library.md` 中触发资格=是的 ACTIVE 变量
- 当前 DECISION 输出（Reality / Main Gap / Transformation / Core Judgment）
- 历史资产检索摘要
- 账号画像执行快照

COMPILE 不得读取未发布的候选结构、单篇爆款拆解原文或未验证研究结论。

本节定义的是 COMPILE 结构选择能力的边界（能读什么、不能读什么），属于 Research / Governance Authority；不是 Runtime Compile Rules 内容本身。当前 TRIAL/ACTIVE 版本真正被 COMPILE 调用的结构规则数据，唯一权威是 `runtime/知乎结构库快照.md`——两者不是竞争的"唯一权威"，而是治理层规则与执行层数据的分工：本文件决定能否升级、边界在哪，快照文件决定当前实际生效的内容是什么。

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
