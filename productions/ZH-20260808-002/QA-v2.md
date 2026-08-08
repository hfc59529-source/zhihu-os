Production ID: ZH-20260808-002

# QA v2

## Target

Draft-v2: `productions/ZH-20260808-002/Draft-v2.md`

## Patch Scope

Draft-v1 第 23–29 行使用"处理时可以按这个顺序来。第一…第二…第三…"的显性编号模板，违反 `Claude正文生产Prompt.md` 输出规则第 4 条（不使用"第一、第二、第三"等显性模板，除非题目天然需要清单式回答）。本题不属于清单类题目，不构成例外。

改写为自然推进的连续段落，内容和先后顺序不变（不当场拦 → 事后补同步 → 交付后复盘），Semantic Freeze 冻结的核心判断"指令可以越级，信息和责任不能断链"及其余段落未改动。

## Checks

### Reasoning

Command:

```text
python3 scripts/validate_reasoning.py productions/ZH-20260808-002/Draft-v2.md
```

Result: PASS

### Reading Experience

Command:

```text
python3 scripts/validate_reading_experience.py productions/ZH-20260808-002/Draft-v2.md
```

Result: PASS

```text
training_expression_hits: 0
abstract_dense_windows: 0
max_explanation_streak: 2
risks: none
```

## Decision

Draft-v2 PASS，QA-v1 标注的中风险（训练式表达）已消除，无新增风险。可交付进入 User Review。
