# Artifact State 模板 V1

Status：DRAFT（未接入 Production Prompt，未接入生产链，仅供审阅）

## 目的

解决单一问题：正文的迭代优化能不能在保留已确认优点的基础上累积，而不是每次修改都对全文重新抽奖。

本对象只负责 Artifact Memory（产物状态记忆），不涉及 Reader Simulation、Writer Authority 或任何写作风格实验；不与 Judgment Formation Gate、Semantic Freeze Gate 的语义权威冲突，只记录"这一篇具体哪些内容已经被人工确认"。

## 核心对象

```text
Artifact Baseline
= 当前被认可的基线版本正文

Assets
= 已确认有效、后续默认冻结的内容

Issues
= 当前明确允许修改的问题
```

## 修改语义

默认动作：PATCH。

```text
PATCH
= Baseline + Issues
→ 只改 Issues 标注的部分
→ Assets 原样继承，不得因为"顺手一起改"而改动
→ 生成新 Baseline，Revision 号 +1

REGENERATE
= 放弃当前 Baseline
→ 重新进入 Judgment Formation / Structure / Draft
→ 只在下列情况允许触发：
  - Judgment 不成立
  - Explanation Target 判断错误
  - 文章结构整体无法承载 Judgment（结构级重建）
→ 仅"这段解释太多""不像我的表达""结尾弱"等局部反馈，一律 PATCH，不得触发 REGENERATE
```

Revision_Mode 必须显式写明选择的是 PATCH 还是 REGENERATE，以及触发 REGENERATE 时对应的上游对象（Judgment / Explanation Target / Structure）。

## 模板

```markdown
# Artifact State

Production_ID:
Baseline: （对应正文文件名/版本号）
Revision_Mode: PATCH

## Locked Assets
- Judgment:
- Paragraph 1:
- Paragraph 2:

## Editable Issues
- Paragraph 3:
  - Issue:
  - Allowed change:

## Change Log
- Patch-001:
  - Changed:
  - Preserved:
  - Reason:
```

## 使用边界（V1）

- 不引入状态机、权重、评分或自动判断；PATCH / REGENERATE 由人工在反馈时显式选择。
- 不记录审计术语、参数名、后台字段以外的正文表达细节。
- 本模板生效前提是人工审阅通过；审阅后再决定是否成为每个 Production 的持久化对象，以及是否在 `templates/Claude正文生产Prompt.md` 中增加"任何 Patch 必须读取当前 STATE.md"的硬性要求。
