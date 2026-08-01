# Trigger 判断能力 V1（原 Trigger Engine，已并入 Skill006）

状态：PROPOSAL
日期：2026-08-01

是否生效：否

是否进入生产调用：否

是否替代唯一权威库：否

## 定位

Trigger 判断不是独立系统，是 Production Card Generator（Skill006）内部的一项候选能力，目标是未来可能优化”题目 → 参数库 → Production Card”中的参数调用层。

系统只有一个生产入口：Production Card Generator。Trigger 判断只是它内部多出的一步，不是新的中心节点。

不替换、不修改：

- Production Card
- Claude 审计
- QA
- 状态机
- Observation
- Comparison Report

## 提案意图

旧问题：

```text
有什么规律？
```

新问题：

```text
什么时候触发这条规律？
```

Trigger 判断的目标不是增加更多参数，而是减少默认调用，让每次进入 Production Card 的内容依据更明确。

本文件不代表当前运行事实，不得被日常生产自动调用。

## 三层对象

### 1. Trigger

回答：什么时候调用？

Trigger 是题目层识别器，只负责判断当前题目属于哪种触发场景。

示例：

- TR-WC-01｜职场利益冲突
- TR-ME-01｜机制解释型
- TR-EM-01｜情绪共鸣型
- TR-DE-01｜决策分析型

### 2. Pattern

回答：触发以后怎么写？

Pattern 是写作施工包，不是参数堆叠。

示例：

```text
入口：先接员工真实感受
正文：解释机制
结尾：迁移判断
禁止：直接讲理论
```

### 3. Evidence

回答：为什么能触发？

所有 Trigger 必须挂证据。证据来源只能是：

- 平台采集
- 历史爆款
- 人工审计
- 发布数据
- Comparison Report
- Observation

未挂证据的 Trigger 不允许进入正式生产。

## 生产调用链

Trigger 判断不作为独立链条存在，而是 Generator 内部步骤：

```text
题目
↓
Production Card Generator（Skill006）
├── 问题分类
├── Trigger 判断（本提案新增能力）
├── ACTIVE 结构选择
├── Pattern 选择
├── Evidence 调用
├── Parameter 调用
├── Observation 调用
└── Card 输出
↓
正文
```

## 证据链

Evidence / Trigger / Pattern 是 Generator 生产过程中读取的数据资源，与 Parameter Library、Observation 地位一致，不隶属于任何"Engine"：

```text
平台采集
历史爆款
人工审计
发布数据
Comparison Report
Observation
↓
Evidence Library
↓
Generator 内部 Trigger 判断步骤读取 Trigger Library / Pattern Library
↓
Production Card
```

## 与旧参数库的关系（待审查）

`production_variable_library.md` 暂不删除、不改名、不物理迁移。

提案倾向：Trigger 判断作为 Skill006 内部的选择性调用步骤，不是独立路由层：

```text
题目
↓
Production Card Generator（Skill006）内部 Trigger 判断步骤
↓
从 production_variable_library.md 选择性调用
↓
Production Card
```

在架构审查通过前：

1. 旧 CV 仍是当前生产系统的唯一权威内容变量入口。
2. Trigger 判断不替代 `production_variable_library.md`。
3. Trigger 判断不参与当前生产调用。
4. 新发现仍先进入 Observation。

## 禁止事项

1. 禁止因为单篇 Observation 新增正式 Trigger。
2. 禁止因为一个 Supports 结论升级协议。
3. 禁止把 Trigger 判断扩展成第二套 Production Card 或独立 Engine。
4. 禁止让 Trigger 直接决定正文段落；正文段落仍由 Production Card 承载。
5. 禁止把 Evidence 原文塞进 Claude 正文输入。

## 当前最小可用原则

每次生产只允许命中：

- 1 个主 Trigger
- 0-2 个辅助 Trigger
- 1 个主 Pattern

Production Card 只接收 Pattern 压缩后的施工要求，不接收完整证据链。

## 状态门槛

| 状态 | 含义 | 生产权限 |
|---|---|---|
| OBSERVED | 单篇或少量样本观察到触发现象 | 禁止正式调用 |
| SUPPORTED | 单问题 Top5 或多样本初步支持 | 仅可作为人工参考 |
| HYPOTHESIS | 多问题同赛道支持，具备扩样本价值 | 可申请进入实验生产 |
| ACTIVE | 跨样本、发布数据和 Comparison Report 稳定支持，且架构审查通过 | 可进入日常生产 |
| DEPRECATED | 失效、冲突或被更强 Trigger 替代 | 禁止调用 |

## 架构变更门槛

任何涉及唯一权威入口、库结构或生产调用链的变更，必须先经过架构审查，不能由单次 Observation 直接触发正式落地。
