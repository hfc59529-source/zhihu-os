# Execution IR v1

Production ID：ZH-20260811-002

Input：`Semantic_Freeze-v1.md`

Runtime：TRIAL Runtime，Authority Provenance Patch 已生效。

Status：EXECUTION_IR_READY

## 1. Reasoning Path

Reader Mental Model：

```text
形式动作没帮助干活
↓
所以它应该被取消
↓
但它越来越多
↓
说明领导/组织很荒唐
```

False Inference：

读者把“对业务结果有没有帮助”当成唯一存废标准，因此解释不了为什么无效动作反而稳定增加。

Breaking Point：

组织里很多动作不是为了让一线工作变顺，而是为了让责任在事后可展示、可转移、可证明。

Mechanism：

形式动作的直接产物不是结果，而是痕迹。痕迹在正常工作时可能没人看，但在检查、汇报、复盘、追责时会变成证据。因为保留一份证据的个人成本低，而取消一份证据的个人责任风险高，所以形式动作容易只增不减。

Transformation：

读者以后判断一个形式动作，不先问“它烦不烦、有没有用”，而先问三件事：

```text
谁会打开？
什么时候打开？
打开以后会改变谁的责任？
```

## 2. Structure

Structure Reference：ACTIVE-TS01｜老师爆款机制推进结构

authority_status：PROVISIONAL_ADVISORY

provenance_gap：TS01 缺少当前 Schema 下 VERIFIED_CONTRACT 证据链，不得完整合同化。

COMPILE 处理：

- 本 Run 不搬运 TS01 固定 10 步。
- 本 Run 只保留 Decision 必要推导：现象困惑 → 判断标准切换 → 责任证据机制 → 三问工具 → 边界收束。
- AUDIT 不得因 Draft 未兑现 TS01 固定模板步骤而判 Execution Compliance 失败。

Run Required Steps：

1. 从读者熟悉的形式动作进入，承认其消耗感。
2. 明确指出“有没有帮助干活”不是唯一存废标准。
3. 解释形式动作产出的痕迹如何在检查、汇报、复盘、追责时变成证据。
4. 给出三问判断工具：谁打开、什么时候打开、改变谁的责任。
5. 区分真实管理工具与免责证据，避免把所有流程都写成无效。
6. 结尾回到题目，说明为什么这类动作容易增加而不容易减少。

## 3. Material Boundary

Allowed：

- Topic Package 中的原问题、题主列举动作、页面可见信号。
- Benchmark Context 的摘要层结论：Top1 已覆盖组织控制/留痕免责；Top2 已覆盖故事化流程膨胀；Top3 已覆盖业务失控/中层存在感。
- 普通职场可见动作：日报、打卡、拍照、会议纪要、工作群、审批表、复盘材料、签字留痕。

Forbidden：

- 不引用周雪光理论名词或复述 Top1 框架。
- 不使用流水席故事。
- 不虚构具体公司、人物、项目或事故。
- 不做宏观政治表态。
- 不把所有流程都判为形式主义。

## 4. Expression Constraints

- 正文长度控制在 900-1200 字。
- 不使用后台字段名、参数名、审计术语。
- 不写成管理学教材。
- 不使用“首先、其次、最后”式讲义结构。
- 保留可读性：每段只承担一个主要任务，连续解释后必须有现实动作承接。

## 5. Acceptance Criteria

CV authority_status：LEGACY_ACTIVE_PROVENANCE_PENDING

说明：CV001-CV006 当前存在 Evidence References 待补录问题。本 Run 如使用 CV，只能写本题必要 Realization Requirement，不复制 CV 通用定义、触发条件或权重。

1. 【CV001 Realization】首屏内完成认知校正：读者原本按“对业务有没有用”判断形式动作，正文需切换到“痕迹会不会在责任场景中被打开”。
2. 【CV003 Realization】正文须把形式动作放回组织检查、汇报、复盘、追责关系中解释，不归因为领导个人闲、蠢或坏。
3. 【CV004 Realization】正文须具体说明痕迹如何改变责任归属：谁能证明自己做过、提醒过、检查过，谁因此少承担解释压力。
4. 【Gate B Experiment Realization】正文必须自然形成一个可复用判断工具，但不得把“Save Value”写成口号、模型名或系统术语；工具以普通读者能记住并复用的问句呈现。

## 6. Triggered Rule IDs

[]

适用依据：Triggered Rule IDs compatibility rule。当前 Runtime 未发布 ID-bearing conditional Audit Rules 候选集合，`[]` 视为字段如实完成，不阻断 WRITE。Global Operational Checks 由 AUDIT 执行载体直接加载，不依赖本字段。

## COMPILE Result

PASS。Execution IR 六项输出完成，可进入 WRITE。
