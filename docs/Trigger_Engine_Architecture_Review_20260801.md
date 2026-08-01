# Trigger Engine 架构审查

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

当前最稳妥选择：上层路由。

```text
题目
↓
Trigger 路由
↓
从 production_variable_library.md 选择性调用
↓
Production Card
```

## 3. 最小落地方式

当前不落地正式架构，只保留 Proposal。

若进入实验，最小方式应是：

- 只做一个实验性触发器。
- 不建立正式三库。
- 不迁移全部 CV。
- 不改生产状态机。
- 不改变唯一权威库。
- 只在少量同类题目上测试。

候选实验：

```text
TR-WC-01｜职场利益冲突型
状态：EXPERIMENT（待申请）
证据：Observation-03
作用：决定是否调用“先接情绪、再解释机制”的已有规律
```

## 4. 暂时不该落地的部分

当前不应：

- 把参数库整体改名。
- 一次性建立正式 Trigger / Pattern / Evidence 三库。
- 批量迁移 CV001-CV006。
- 修改 README 正式入口。
- 让 Production Card 默认依赖 Trigger Engine。
- 宣布 Trigger Engine 为 ACTIVE。

## 5. 归属判定

任何新增能力，先回答四选一：

```text
□ 新系统
□ 新模块
☑ 现有模块能力增强
□ 参数优化
□ 流程优化
```

只有满足以下三个条件时，才允许升级为独立系统：

1. 有独立生命周期；
2. 能被多个模块独立调用；
3. 可以脱离 Production Card Generator 单独运行。

Trigger 判断三个条件都不满足：生命周期依赖 Generator；只服务 Production Card；无法单独运行。

因此结论是：**Trigger 是 Production Card Generator（Skill006）的内部能力（Internal Capability），不是新系统，不是新入口。**

不存在"Trigger Engine"这个独立组件；Trigger / Pattern / Evidence 三个库的地位与 Parameter Library、Observation 一致，都是 Generator 生产过程中读取的数据资源，不是某个 Engine 专属的资源。

## 6. 建议状态

建议三步：

```text
PROPOSAL
↓
EXPERIMENT
↓
ACTIVE
```

当前状态：

- Trigger 判断能力（Skill006 内部步骤）：PROPOSAL
- TR-WC-01：可申请进入 EXPERIMENT
- 现有生产系统：继续 ACTIVE

## 固定原则

任何涉及唯一权威入口、库结构或生产调用链的变更，必须先经过架构审查，不能由单次 Observation 直接触发正式落地。

默认不新增系统；系统只有一个生产入口：Production Card Generator（Skill006）。

## 当前结论

Trigger 判断保留为 Skill006 内部能力提案，状态 PROPOSAL。

当前不参与生产运行，不替代 `production_variable_library.md`，不修改 Production Card，不影响 ZH-20260801-011 / 012 当前流程，不作为独立入口或独立系统存在。

