# Asset Lineage Inventory｜2026-08-10

## Scope

本盘点只回答：历史 L0 / L1 / L2 / Observation / Parameter / 实验资产是否已经接入当前 Compiler V1 Runtime。

本文件不修改参数库，不新增 ACTIVE，不迁移证据，不恢复旧框架，不继续单篇生产。

当前 Runtime 状态：

```text
Development branch = compiler-v1-runtime-alignment
HEAD = f9cc59a
Published TRIAL Runtime = runtime/ACTIVE_MANIFEST.md
Based On Commit = 8b8d8d1
Runtime validity = PASS
```

## Runtime Consumption Map

| 资产层 | 代表文件 | 当前 Runtime 是否覆盖 | 当前生产节点是否直接消费 | 当前作用 |
|---|---|---:|---:|---|
| L0 内容资产总账 | `data/l0_content_assets.csv` | 否 | 否 | 历史基线与 L1 抽样来源 |
| Historical Baseline | `reports/historical_baseline_report.md` | 否 | 否 | 定义阅读/收益分位、L1 入口 |
| L1 样本清单 | `data/l1_sample_list.csv` | 否 | 否 | 代表样本入口 |
| L1 样本报告 | `reports/l1_sample_report.md` | 否 | 否 | 解释 L1 生成口径 |
| L2 变量记录 | `l2_variable_records.md` | 否 | 否 | 16 篇正文变量标注 |
| L2.5 验证报告 | `l2_variable_validation.md` | 否 | 否 | 变量出现率与高低组差异统计 |
| Observation | `data/Milestone_Observations.md` | 否 | 否 | 治理观察与参数修改隔离层 |
| Parameter Registry | `production_variable_library.md` | 是 | 是，经 COMPILE 消费 | 当前唯一内容变量权威库 |
| Runtime Snapshot | `runtime/production_variable_snapshot.md` | 是 | 是，但当前内容为旧测试快照 | 运行时变量快照，需刷新才可服务新 Run |
| Parameter Call Log | `data/parameter_call_log.md` | 否 | 否 | 发布后归因与结果记录 |
| Evidence Gate | `reports/evidence_gate_review_20260808.md` | 否 | 否 | 判断哪些新流程样本可进入变量效果判断 |
| VT-001 | `reports/VT-001_parameter_trigger_evidence_report_20260802.md` | 否 | 否 | 旧 Card 链下 Question → Card → Parameter match 证据 |

## Main Finding

历史资产不是没有价值，而是多数停在研究层或复盘层，没有形成当前 Runtime 可消费的血缘链。

当前 `production_variable_library.md` 已经吸收了部分 L2/L2.5 统计结果。这里的 16 篇不是平台其他作者样本，而是从本账号 `data/l0_content_assets.csv` 经 `data/l1_sample_list.csv` 分层抽样进入 L2 的账号历史样本。

| Parameter | Registry 已吸收内容 | 缺失内容 |
|---|---|---|
| CV001｜认知校正 | 账号样本数 16、命中数 16、收益表现“全组高频” | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV002｜利益重分配 | 账号样本数 16、命中数 16 | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV003｜组织视角 | 账号样本数 16、命中数 15 | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV004｜风险传导 | 账号样本数 16、命中数 14、阅读差异 +40pp | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV005｜身份代入 | 账号样本数 16、命中数 14、阅读差异 +40pp | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV006｜结尾动作 | 账号样本数 16、命中数 13 | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |

这说明旧 L2 不是完全丢失；但它只被摘要式搬运，尚未迁移成当前 Compiler V1 / Parameter Registry Schema 能完整解释的 provenance。更准确地说，这批证据能证明账号历史样本中的变量观察和初步相关性，但尚未回答 legacy ACTIVE Parameter 在当前 Runtime 下如何继承、复核或降级。

注意：当前 Observation → Parameter 规则是现行治理接口，不能直接倒推为历史 L2 当时必须遵守的流程，也不能据此证明 CV001-CV006 当初 ACTIVE 非法。当前问题是迁移语义未对齐，不是已证明的历史违规。

## Broken Links

### 1. L1 / L2 → Parameter Registry

`l2_variable_records.md` 和 `l2_variable_validation.md` 已经提供：

- 样本来源：`data/l1_sample_list.csv`
- 变量词表
- 16 篇正文变量标注
- Present / Absent / Unknown
- 高收益 / 低收益 / 高阅读 / 低阅读分组
- 差异统计

但 Registry 中对应字段仍为：

```text
平台样本数：UNKNOWN
平台证据强度：待补充
账号成功数：UNKNOWN
证据引用：待补录
```

断链性质：证据存在，但按当前 Schema 还没有被表达成可解释的 Parameter provenance。`production_variable_library.md` 当前要求 Parameter 的证据引用具备治理接口；但该要求不能溯及证明历史 L2 形成时漏做了 Observation。

Runtime 影响：COMPILE 能看到 CV 当前状态和触发资格，但看不到每个状态在当前 Schema 下如何解释：哪些来自历史账号样本观察，哪些来自受控实验，哪些属于 grandfathered / legacy ACTIVE 继承。

### 2. Observation → Parameter Registry

`data/Milestone_Observations.md` 已定义当前 Observation 与 Parameter 的隔离关系，并要求：

```text
每次参数修改必须在 Parameter 记录的"证据引用"字段关联 Observation ID
```

但同一文件也说明历史记录存在旧状态口径，后来才采用正式生命周期，历史记录不倒填新状态。因此当前 CV001-CV010 的 `证据引用` 多为“待补录”，只能证明当前 Schema 下 provenance 表达不足，不能证明历史形成过程违规。

断链性质：治理层已经定义新的血缘表达规则，但 legacy Parameter 如何接入该规则尚未被单独裁决。

Runtime 影响：后续无法判断某个参数状态来自 L2 统计、Observation 支撑、人工审核，还是旧系统遗留。

### 3. Parameter Registry → Runtime Snapshot

`runtime/production_variable_snapshot.md` 当前是：

```text
PARAM_CALL_TEST_ONLY
问题：未来20年什么是优质资产？
生成日期：2026-08-01
```

它不是当前 Compiler V1 每次生产可直接复用的通用快照。

断链性质：Registry 是 Runtime-covered 权威文件，但 Snapshot 仍像旧测试产物。

Runtime 影响：如果 COMPILE 直接消费该快照，会混入旧题上下文；如果 COMPILE 绕开它直接读 Registry，又违反“每次正式生产必须由 Claude 侧生成或刷新 snapshot”的口径。

### 4. Parameter Call Log → Result Validation

`data/parameter_call_log.md` 已记录若干 Production 的参数调用与结果，但分为两套状态：

- 历史旧列结构，不倒填新字段。
- 2026-08-09 起新字段结构，但尚未形成多篇新 Run 的完整记录。

断链性质：有调用事实和结果数据，但旧流程、新流程、Card 链、Compiler V1 链混在同一日志中，需要按 Production 世代分层。

Runtime 影响：不能直接用该日志推动 ACTIVE / REVIEW 状态，只能作为归因候选来源。

### 5. Evidence Gate → Parameter Effect

`reports/evidence_gate_review_20260808.md` 已明确很多新流程样本“不放行变量效果判断”，原因包括：

- 有收益样本缺 Production 映射和完整归因。
- 有 Production 映射的新流程样本缺收益匹配。
- 折叠样本不得归因为正文失败。
- REVIEW_DAY 补录不足以建立 Observation。

断链性质：它不是废资产，而是“禁止误用证据”的 Gate。

Runtime 影响：Registry 中 `账号成功数 / 成功率` 不能从这些样本直接倒推，必须等 Evidence Gate 放行。

## Asset Classification

| 类别 | 资产 | 分类 | 处理建议 |
|---|---|---|---|
| 原始数据 | `data/l0_content_assets.csv`、`data/review_data_snapshots.csv` | Evidence Asset | 保留；只做来源，不直接进 Runtime |
| 分层样本 | `data/l1_sample_list.csv`、`reports/l1_sample_report.md` | Evidence Asset | 保留；为 L2/复盘提供样本入口 |
| 变量标注 | `l2_variable_records.md` | Evidence Asset | 作为 legacy provenance 材料保留，等待迁移规则裁决 |
| 变量验证 | `l2_variable_validation.md` | Evidence Asset | 作为 observational association 证据保留，不能直接证明 Effect Validity |
| 治理观察 | `data/Milestone_Observations.md` | Governance Asset | 是当前治理接口，但是否用于承接 legacy ACTIVE 需另立迁移规则 |
| 旧 Card 匹配 | `reports/VT-001_parameter_trigger_evidence_report_20260802.md` | Research / Legacy Evidence | 保留研究价值；不能直接证明 Compiler V1 参数有效 |
| Evidence Gate | `reports/evidence_gate_review_20260808.md` | Gate Asset | 保留；用于阻止错误回写 |
| Runtime Snapshot | `runtime/production_variable_snapshot.md` | Runtime Asset, stale for current Run | 每次生产前刷新，不复用旧题测试快照 |
| 旧实验 Prompt / 实验稿 | `research/experiments/*`、部分 `productions/*experiment*` | Research Asset | 保留研究，不进入 Runtime，除非另行治理批准 |

## Immediate Runtime Implication

生产可以恢复，但不能假装 Registry 已经完整吸收历史证据。

当前可执行边界应写成：

```text
COMPILE 可以使用 production_variable_library.md 中已具备 ACTIVE + Trigger Eligibility 的 CV。
COMPILE 不得把 L1/L2 历史资产直接当作 Runtime 输入。
L1/L2 只能在治理规则明确后，通过合法迁移进入 Parameter Registry 或 refreshed Runtime Snapshot 后，才改变生产权重、状态或触发资格。
```

## Recommended Next Action

不要重采全部历史数据。也不要立刻补 Observation 或改 CV001-CV006。先补一条迁移规则：

1. 定义 grandfathered / legacy ACTIVE Parameter 在 Compiler V1 下的继承资格。
2. 明确哪些 legacy ACTIVE 可以临时保留触发资格，哪些需要 REVIEW / CANDIDATE / DEPRECATED。
3. 明确历史 L1/L2 observational association 是否可以作为 provenance material，而不是 Effect Validity 证明。
4. 明确是否允许新建“migration observation / migration record”来描述旧证据；若允许，必须标注为 2026-08-10 迁移记录，不得伪装成历史当时的 Observation。
5. 在迁移规则批准前，不补 CV001-CV006 的 Evidence References，不改状态、权重或触发资格。
6. 迁移规则批准并执行后，重新 release TRIAL Runtime。

## Corrected Evidence Level

`l2_variable_validation.md` 自身已经声明：

```text
本报告只做差异统计，不解释因果。
本轮不进入 L3。
```

因此这批历史资产的正确证据等级是：

- 可以证明哪些变量在账号历史内容里高频存在。
- 可以证明哪些变量与高/低阅读组存在初步差异提示。
- 可以证明哪些变量暂未显示区分度。
- 不能单独证明某变量造成高阅读、高收益或收藏。
- 不能单独满足当前 Parameter Lifecycle 中“指定单变量实验 → 连续3篇同向验证 → 累计10篇同向验证”的 Effect Validity 要求；但该当前要求不能自动溯及判定历史 ACTIVE 非法。

当前真正断点：

```text
Historical Account Samples
↓
L2 observational association
↓
摘要进入 Parameter Registry
↓
当前 Schema 下缺少清晰的 provenance / experiment lineage / success definition / controlled validation 说明
↓
legacy ACTIVE 在新 Runtime 下的继承资格尚未单独裁决
```

这不是样本来源错误，也不是已经证明历史 ACTIVE 非法，而是 Legacy → Current Governance Schema migration gap。

禁止事项：

- 禁止用当前 Observation 规则追溯判定历史 L2 当时违规。
- 禁止用 2026-08-10 新建 Observation 伪装成早期 ACTIVE 的原始血缘。
- 禁止在没有 legacy ACTIVE 迁移规则前，直接补 Evidence References 来制造闭环。

## Stop Condition

在完成上述迁移前，不应继续追问“为什么 CV001 是 P0”这类单点优先级问题。

正确问题是：

```text
CV001 的 P0 来自哪一组证据？
该证据是否已经有 Evidence Reference？
它证明的是高频稳定，还是成功区分度？
如果只是高频稳定，P0 是否表示默认触发优先级，而非效果强因果？
```

这四个问题只有完成 lineage 回填后才能被稳定回答。
