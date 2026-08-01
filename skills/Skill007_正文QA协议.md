# Skill007｜正文 QA 协议 V2.0

Status：ACTIVE

## 目标

建立 Claude 正文生产后的自动审核闭环。

原则：QA 只审核，不修改正文；QA 只检查正文是否忠实执行 Production Card。

## 单一权威规则

正文 QA 阶段只有一个内容权威：Production Card。

QA 不得引用 Production Card 之外的历史参数体系、旧 Prompt 字段、旧协议字段或后台变量作为内容标准。包括但不限于：

- PD / RR / RE / BT / CR。
- 认知奖励。
- 机制层 / 利益关系层 / 人性博弈层 / 认知升级层。
- Reasoning Protocol / Expression Protocol。
- 任何 Production Card 未出现的变量、结构、案例、数据、判断或方法论。

如果正文质量问题无法在 Production Card 中找到对应约束，只能记录为 Observation，不得判定正文违反 QA。

## 执行流程

```text
Production Card
↓
Claude Draft
↓
QA
├── PASS
│   ↓
│   READY_FOR_AUDIT
└── FAIL
    ↓
    生成只基于 Production Card 的修正指令
    ↓
    Claude Patch
    ↓
    再次 QA
```

## QA 职责

QA 只检查以下事项：

1. 题目一致性：正文是否回答 Production Card 中的问题。
2. 核心判断一致性：正文是否兑现 Production Card 的唯一核心判断。
3. 结构一致性：正文是否按 Production Card 的结构实例化和分段施工说明推进。
4. 场景一致性：正文是否使用 Production Card 要求的现实场景或例子，且没有虚构 Card 未提供的真实事实。
5. 边界一致性：正文是否遵守 Production Card 的事实和安全边界。
6. 表达约束一致性：正文是否遵守 Production Card 的表达约束。
7. 收尾一致性：正文是否完成 Production Card 的结尾回收方式。
8. 后台痕迹检查：正文是否泄露参数名、审计术语、变量编码或系统施工痕迹。

## PASS 标准

同时满足以下条件，判定 PASS：

- 正文主线能回到 Production Card 的问题和唯一核心判断。
- Production Card 要求的段落职责、场景要求和推进关系均已兑现。
- 未新增 Production Card 没有提供的一级结构、核心概念、真实案例、数据或结论。
- 未违反 Production Card 的事实和安全边界。
- 未出现明显后台字段、参数名、审计术语或系统施工痕迹。
- 读者能从正文中获得 Production Card 规定的收尾判断。

## FAIL 标准

出现以下任一情况，判定 FAIL：

- 正文回答了另一个问题。
- 正文替换、稀释或反转 Production Card 的唯一核心判断。
- 正文绕开 Production Card 的分段施工说明，改成另一套论证结构。
- 正文遗漏 Production Card 明确要求的关键段落职责、现实场景或结尾回收。
- 正文新增 Production Card 未提供的理论框架、真实案例、数据、人物、公司、行业事实或核心判断。
- 正文违反 Production Card 的事实和安全边界。
- 正文出现后台参数名、审计术语、变量编码或系统施工痕迹。

## FAIL 分级

### MINOR FAIL

正文局部未兑现 Production Card，但未改变问题、核心判断和正文主结构。

典型情况：

- 某个段落场景不足。
- 某个推进关系表达不清。
- 结尾没有完全回收 Card 要求。
- 局部出现模板化表达或后台痕迹。

处理：只生成局部修正指令，交给 Claude 修正。

### MAJOR FAIL

正文已经偏离 Production Card 的内容权威。

典型情况：

- 问题回答偏移。
- 核心判断改变。
- 正文结构被替换。
- 新增 Card 外核心理论框架。
- 虚构 Card 外真实事实。

处理：退回 Claude 重新生成正文。

## QA 输出格式

必须严格输出：

```text
# QA Report
Production ID：
状态：PASS / MINOR FAIL / MAJOR FAIL

## Card 一致性检查
- 题目一致性：
- 核心判断一致性：
- 结构一致性：
- 场景一致性：
- 边界一致性：
- 表达约束一致性：
- 收尾一致性：
- 后台痕迹检查：

## 问题
1.
位置：
问题：
违反的 Card 字段：
修正责任：Claude

## 结论
PASS / 退回 Claude 局部修正 / 退回 Claude 重新生成
```

没有问题时，`## 问题` 写“无”。

不得输出 Production Card 之外的自由发挥建议。

## 修正指令规则

Codex 生成修正指令时，只能引用：

- Production Card 字段。
- 正文中违反该字段的具体位置。
- 需要 Claude 修正的局部任务。

禁止：

- 修改 Production Card。
- 增加 Production Card 没有的新观点。
- 增加 Production Card 没有的新变量、案例、数据或理论。
- 使用旧参数体系解释为什么要改。

## 停止条件

最大自动修复次数为 2 轮。达到最大修复次数仍 FAIL 时，停止并报告：

- 停止节点。
- 失败类型。
- 违反的 Production Card 字段。
- 需要补充的唯一信息。
