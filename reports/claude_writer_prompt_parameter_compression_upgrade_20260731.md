# Claude Writer Prompt 参数隐写升级记录｜2026-07-31

## 触发问题

用户指出：当前 Production Card 作为决策层基本合格，但直接喂给 Claude 后，Claude 会把卡中的 PD / RR / RE / BT 参数逐项展开，导致正文像系统报告，而不像知乎真人回答。

核心问题不是 Production Card，而是缺少一层 Writer Prompt 翻译层：

```text
Production Card（决策）
↓
Writer Prompt（表达转换）
↓
Claude 正文
```

原链路的问题：

```text
Production Card
↓
Claude 正文
```

Claude 会忠实执行所有参数，形成“一个参数一段”的正文结构。

## 本次判断

本次属于正文 Prompt 表达转换层升级，不修改：

- Production Card 字段结构
- 内容变量库
- ACTIVE 结构库
- ACTIVE 规律库
- 质量参数库

## 已执行修改

### 1. 新增 GC-13｜参数隐写规则

文件：

- `templates/Claude正文生产Prompt.md`

新增模块：

```text
GC-13｜参数隐写规则（Parameter Compression）
```

核心规则：

- Production Card 是决策文档，不是正文提纲。
- 所有 PD / RR / RE / BT 参数属于后台推理和质量控制。
- 正文禁止按参数逐项展开。
- 多个参数必须融合成一个自然判断。
- 一个自然段最多表达一个判断。
- 一个判断最多解释一次。
- 禁止一个参数写一段。
- 禁止按 PD-03、PD-04、PD-05、PD-06、PD-08 的顺序展开正文。
- 读者只能看到场景、动作、判断和边界，不应该看到参数、模型、层级和后台术语。

### 2. 明确后台层级不得显性写出

文件：

- `templates/Claude正文生产Prompt.md`

将“机制层、利益关系层、人性博弈层、认知升级层”明确标注为内部推理，不得作为正文标题、段落顺序或显性表达。

### 3. 增加正文校验

文件：

- `scripts/validate_reasoning.py`

新增检测：

- 后台术语显形检测。
- 参数式小标题 / 分段检测。
- 三方心理分析模式检测。

会拦截的典型问题：

- 正文出现 `过程控制权`、`利益结构`、`风险传导`、`博弈关系`、`权力资源`、`认知升级` 等后台词。
- 正文按 `PD-03 / PD-04 / PD-05` 或 `机制层 / 利益关系层 / 人性博弈层` 展开。
- 正文连续写“领导为什么、同事为什么、你为什么”等三方心理分析。

## 边界

本次升级只解决：

- 参数显形。
- 系统语言直出。
- 一个参数一段。
- 管理学术语替代人话。

不解决：

- 单题选题质量。
- Production Card 变量选择。
- 平台样本不足。
- 正文事实来源不足。
- Claude 未遵守卡片时的二次修正。

## 当前验证

已确认：

- `templates/Claude正文生产Prompt.md` 包含 `GC-13｜参数隐写规则（Parameter Compression）`。
- `scripts/validate_reasoning.py` 包含后台术语和参数式分段检测。

旧正文测试：

- `reports/production_20260731_senior_leader_not_fired_expression_v1.txt` 仍会因既有绝对化、伪反常识和概念预算问题被拦截。
- 新增后台术语规则未对该旧文产生额外误伤。

## 后续观察

后续 3 篇正文重点观察：

- Claude 是否仍按参数拆段。
- 正文是否仍出现后台术语。
- 建议型回答是否能把机制压缩成自然判断后再给动作。
- 读者是否能看到“故事和判断”，而不是看到“系统参数”。
