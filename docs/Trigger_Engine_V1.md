# Trigger Engine V1

状态：PROPOSAL
日期：2026-08-01

是否生效：否

是否进入生产调用：否

是否替代唯一权威库：否

## 定位

Trigger Engine 是待评审架构提案，目标是未来可能优化“题目 → 参数库 → Production Card”中的参数调用层。

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

Trigger Engine 的目标不是增加更多参数，而是减少默认调用，让每次进入 Production Card 的内容依据更明确。

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

```text
题目
↓
Trigger Engine
↓
Trigger
↓
Pattern
↓
Production Card
↓
正文
```

## 证据链

```text
平台采集
历史爆款
人工审计
发布数据
Comparison Report
Observation
↓
Evidence
↓
Trigger
↓
Pattern
↓
Production Card
```

## 与旧参数库的关系（待审查）

`production_variable_library.md` 暂不删除、不改名、不物理迁移。

提案倾向采用“上层路由”关系：

```text
题目
↓
Trigger 路由
↓
从 production_variable_library.md 选择性调用
↓
Production Card
```

在架构审查通过前：

1. 旧 CV 仍是当前生产系统的唯一权威内容变量入口。
2. Trigger Engine 不替代 `production_variable_library.md`。
3. Trigger Engine 不参与当前生产调用。
4. 新发现仍先进入 Observation。

## 禁止事项

1. 禁止因为单篇 Observation 新增正式 Trigger。
2. 禁止因为一个 Supports 结论升级协议。
3. 禁止把 Trigger Engine 扩展成第二套 Production Card。
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
