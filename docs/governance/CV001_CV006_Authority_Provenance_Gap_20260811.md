# Governance Observation：CV001-CV006 Authority Provenance Gap

日期：2026-08-11

状态：SUPPORTED（Governance Observation）

关联对象：

- `production_variable_library.md`：CV001-CV006
- `docs/governance/Proposal-B_Content_Variable_Activation_Contract.md`
- `docs/governance/Proposal-B_Decision_Diff.md`
- `docs/知乎OS Compiler V1.md`
- `runtime/ACTIVE_MANIFEST.md`

## 结论

CV001-CV006 当前存在 Authority Provenance Gap。

这六条内容变量在 `production_variable_library.md` 中均为：

```text
当前状态：ACTIVE
触发资格（Trigger Eligibility）：是
证据引用（Evidence References）：待补录
```

其中多个字段仍为 `UNKNOWN` 或“待补充”，例如平台样本数、平台命中率、账号成功数、账号成功率等。

因此，本条不判定 CV001-CV006 内容一定错误，也不判定它们一定应该降级；本条只判定：

```text
CV001-CV006 拥有生产执行权限，但当前仓库无法通过 Evidence References 追溯其 ACTIVE 身份的完整证据链。
```

## 为什么这不是普通文档问题

Proposal B 已经裁决并基本落地：

```text
CV = Runtime Parameter Identity（固定在 production_variable_library.md）
↓ COMPILE Trigger
CV Run Instantiation = Execution IR.acceptance_criteria
↓ WRITE → Realization → AUDIT
```

这意味着 CV001-CV006 一旦命中，不只是“参考知识”，而是会被 COMPILE 编译成本 Run 的 `Acceptance Criteria`，再由 AUDIT 按 Execution Compliance 核对。

所以这组缺口比普通记录不完整更严重：

```text
ACTIVE CV with missing evidence references
↓
COMPILE writes Run Instantiation into Acceptance Criteria
↓
WRITE must realize it
↓
AUDIT enforces it
```

也就是说，CV001-CV006 当前拥有真实生产执行权。

## 与 TS01 Authority Provenance Gap 的关系

TS01 缺口属于 Structure Contract Authority：

```text
Structure → required_steps / step_obligations
```

CV001-CV006 缺口属于 Parameter Contract Authority：

```text
Content Variable → acceptance_criteria
```

二者不是同一个对象，但问题同构：都涉及缺少当前 Schema 可接受的 provenance，却已经拥有或曾经拥有生产合同化路径。

## 风险

1. 后续生产可能继续把证据链未补齐的 CV 编译成 Acceptance Criteria。
2. 如果某篇文章因 CV Realization 失败被 AUDIT 退回，Expected Source 本身的权威证据可能无法追溯。
3. 如果 CV 实际造成文章漂移，系统会难以判断是 WRITE 执行问题，还是 CV 自身不该具备当前执行权限。
4. 后续收益实验得到新信号时，可能继续叠加到这些 legacy ACTIVE CV 上，而不是替换、降权或重新验证。

## 处理原则

本条不直接修改 `production_variable_library.md`。

后续治理评审需要在至少三种处置中选择一种：

1. 补链：为 CV001-CV006 补齐 Evidence References，证明其满足当前 ACTIVE 门槛。
2. 降权：在证据补齐前，把相关 CV 改为 `PROVISIONAL_ADVISORY` / 单变量实验触发，不允许默认进入日常生产 AC。
3. 分层：保留部分基础 CV 为低风险 production invariant，降权其中更偏效果代理或传播假设的 CV。

在裁决前，下一篇生产如继续调用 CV001-CV006，应在 Execution IR 中显式记录：

```text
CV authority_status: LEGACY_ACTIVE_PROVENANCE_PENDING
```

并避免把 CV 通用定义、触发条件或权重复制为正文施工要求。

## 后续验证

下一步不应先讨论“CV 内容对不对”，而应先做 CV provenance audit：

- 每条 CV 的原始证据在哪里；
- 是否有账号发布结果验证；
- 是否有收益 / 阅读 / 收藏 / 评论等结果字段；
- 是否存在反例；
- 是否满足当前 Parameter 生命周期中 `REVIEW → ACTIVE` 的门槛；
- 若不满足，应降到什么权限层。

本条 Observation 不能反向追认 CV001-CV006 已经合格；它只记录当前缺口。
