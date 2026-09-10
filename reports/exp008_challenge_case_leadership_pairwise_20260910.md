# EXP008 Challenge Case｜领导能力 Pairwise Difference v0

Status：OBSERVED / TEXT_BASELINE_PARTIAL

Production ID：ZH-20260905-001

## Case

新答：

```text
Question：如何判断一个人是否有领导能力？
Article ID：answer_2079612017883856957
发布时间：2026-09-05
```

旧答：

```text
Question：怎么看一个人有没有领导力？
Article ID：answer_2072695242105660190
发布时间：2026-08-17
```

## Result Signal

| 样本 | 阅读 | 赞同 | 评论 | 收藏 | 数据时间 |
|---|---:|---:|---:|---:|---|
| 旧答 | 375 | 2 | 0 | 0 | 2026-09-05 后台口径 |
| 新答 | 806 | 8 | 0 | 8 | 2026-09-10 内容管理页 |

```text
806 / 375 = 2.15x
```

结论：

```text
OBSERVED：同 Question Context 下，新版本当前播放达到旧版本约 2.15x，出现与实验假设一致的结果。
NOT PROVEN：不能写成新解释框架导致播放提升。
```

## Threshold

EXP008 Challenge Case 的第一道播放阈值：

```text
高播放 >= 低播放 2x
```

当前状态：

```text
PASS_FIRST_DISTRIBUTION_THRESHOLD
```

## Pairwise Difference v0

旧答原文当前本地缺失，因此本轮不能做完整逐字 Difference。以下只基于 `Challenge_Case-v1.md` 已锁定的旧框架失败归因和新框架生产记录。

| 维度 | 旧答框架 | 新答框架 | 当前判断 |
|---|---|---|---|
| 解释框架 | Trait Definition：领导力拆成抽象能力/人格特征 | Behavioral Diagnosis：组织失序场景里的行为链 | 新答提供更可观察的判断工具 |
| 首句 | 原文缺失 | 判断一个人有没有领导能力，别看开会。看出事。 | 新答首句判断更强，但旧答待补正文 |
| 冲突强度 | 抽象能力清单，冲突可能偏弱 | “平时看不出，出事才看得出”制造判断反差 | 新答冲突更集中 |
| 具体场景 | 可能围绕能力解释 | 项目失控、责任模糊、利益冲突、团队询问“你觉得怎么办” | 新答场景更可代入 |
| 前100字信息密度 | 原文缺失 | 直接否定开会/流程/职位制造的假信号，转向失控场景 | 新答前100字更快进入识别方法 |
| 读者角色 | 可能是旁观者学习领导力定义 | 读者可判断自己、上级、同事谁在混乱中被询问 | 新答读者任务更明确 |
| 机制类型 | 心理/能力标签 | 组织机制：制度失效时谁降低不确定性 | 新答机制更偏社会/组织现场 |
| 可代入性 | 待补正文 | 强：会议、项目失控、扯皮、责任不清 | 新答可代入性更强 |

## Evidence Boundary

当前可写入 EXP008：

```text
OBSERVED：新答在同 Question Context 下达到旧答 2.15x 播放，并且收藏从 0 到 8，出现 Costly Signal。
```

当前不能写入：

```text
新框架因果导致播放提升。
```

原因：

- 旧答正文未补齐，无法完成完整文本 Difference。
- 两次发布时间不同，平台环境和问题池状态可能不同。
- 新答仍处于发布早期，后续是否继续放量未知。

## Next Step

1. 回采旧答正文 `answer_2072695242105660190`。
2. 建立专门 Challenge Pair blind record，不混入原 EXP008 历史 matched-pair 盲标表。
3. 补新答 7d / 14d 阅读、收藏、收益变化。
4. 完整比较：首句、前100字、冲突强度、解释框架、具体场景、读者角色、心理机制/社会机制、可代入性。

## Case Status

```text
EXP008_STRONG_CONTROL_CANDIDATE
First result：PASS
Text difference：PARTIAL
```
