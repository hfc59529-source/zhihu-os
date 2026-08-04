# Trigger Engine 架构审查

术语状态：INACTIVE_PROPOSAL — 本文件术语（`OBSERVED`/`HYPOTHESIS`/`EXPERIENCE`、"调用"）已过时，不随 GOVERNANCE-PRINCIPLE-V1.6 / production_variable_library V3 同步更新。当前权威状态链和术语见 `production_variable_library.md`。

状态：PROPOSAL REVIEW
日期：2026-08-01

## 背景

今天发现一个系统性倾向：参数越多，默认调用越重，Production Card 负担越大。Trigger Engine 的方向是从“有什么规律”转向“什么时候触发这条规律”。

本审查只评估架构方向，不让新架构参与当前生产。

## 1. 方向是否正确

方向正确。

它试图解决：

- 参数全量调用过重。
- 规则缺少适用条件。
- Production Card 负担过大。
- 不同题型被同一组参数强行处理。

但方向正确不等于可以立即 ACTIVE。

## 2. 与现有系统的冲突点

最大冲突是 `production_variable_library.md` 的唯一权威地位。

目前有三种可能关系：

| 关系 | 含义 | 风险 |
|---|---|---|
| 替代 | Trigger Engine 取代现有参数库 | 风险最高，会破坏唯一权威入口 |
| 上层路由 | 参数库保留，Trigger 只决定调用哪些参数 | 风险较低，迁移可控 |
| 并行体系 | 两套入口同时存在 | 容易形成双权威和冲突调用 |

最终判定：以上三种关系都不成立，因为不需要建立 Trigger 这个外部对象。

`production_variable_library.md` 中每条变量本身已经带有“适用题型 / 触发条件 / 禁用边界 / 当前状态 / 是否允许生产调用 / 调用权重”六个字段，这就是 Trigger 能力本身，只是分散在每条变量记录里，没有被当成匹配规则完整写出来。

```text
题目
↓
production_variable_library.md 依据自身字段完成匹配
↓
Production Card
```

## 3. 最小落地方式

不新增触发器对象。真正需要落地的只是把参数库现有的"生产前必须先匹配题型，再调用变量"这句粗规则，展开成可执行的六层匹配顺序（生产权限 → 禁用边界 → 适用题型 → 触发条件 → 去重冲突 → 权重排序），并在运行时快照中补充"命中依据 / 禁用边界检查 / 本题用途 / 是否实际调用"四个字段。

已落地于 [`production_variable_library.md`](../production_variable_library.md) 的"调用原则"与"运行时快照"章节。

原候选实验 TR-WC-01（职场利益冲突型，证据 Observation-03，作用：决定是否调用"先接情绪、再解释机制"）不再作为独立 Trigger 申请 EXPERIMENT，而是转化为对 CV002 / CV004 等既有变量触发条件的补充证据，按现有变量生命周期回写。

## 4. 暂时不该落地的部分

当前不应：

- 把参数库整体改名。
- 建立正式 Trigger / Pattern / Evidence 三库并投入生产调用。
- 批量迁移 CV001-CV006 到新字段结构。
- 修改 README 正式入口。
- 让 Production Card 默认依赖任何独立 Trigger 对象。
- 在 Skill006 主流程中新增 Trigger 步骤。

## 5. 归属判定

任何新增能力，先回答四选一：

```text
□ 新系统
□ 新模块
□ 现有模块能力增强
☑ 参数优化 / 流程细化
```

只有满足以下三个条件时，才允许升级为独立系统：

1. 有独立生命周期；
2. 能被多个模块独立调用；
3. 可以脱离 Production Card Generator 单独运行。

Trigger 判断三个条件都不满足。更进一步：它甚至不需要作为 Generator 的独立步骤存在，因为参数库的"适用题型 / 触发条件 / 禁用边界"字段本身就是 Trigger。

因此结论是：**Trigger 不是新系统、不是新入口、也不是 Generator 的新步骤，而是 `production_variable_library.md` 现有"变量匹配"规则的精确化。**

Trigger / Pattern / Evidence 三份文件保留为研究草稿，不进入 runtime，不进入 Skill006 固定读取。

## 6. 建议状态

- 参数库匹配规则精确化（六层匹配顺序 + 快照命中字段）：已落地为 ACTIVE 规则的一部分，见 `production_variable_library.md`。
- Trigger / Pattern / Evidence Library：保留为研究草稿，不进入生产。
- 现有生产模块：继续 ACTIVE，主流程不变。

## 固定原则

任何涉及唯一权威入口、库结构或生产调用链的变更，必须先经过架构审查，不能由单次 Observation 直接触发正式落地。

默认不新增系统、不新增入口、不新增生产步骤；优先检查能否通过精确化现有规则解决问题。

## 当前结论

不建立 Trigger Engine，也不在 Skill006 中新增 Trigger 步骤。

Trigger 真正的价值——参数不能因为 ACTIVE 就全量调用，必须判断"什么时候适用"——已通过精确化 `production_variable_library.md` 的调用原则实现，不新增系统、入口或生产流程，不影响 ZH-20260801-011 / 012 当前流程。
