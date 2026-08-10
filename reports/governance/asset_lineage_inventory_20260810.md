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

当前 `production_variable_library.md` 已经吸收了部分 L2/L2.5 统计结果，例如：

| Parameter | Registry 已吸收内容 | 缺失内容 |
|---|---|---|
| CV001｜认知校正 | 账号样本数 16、命中数 16、收益表现“全组高频” | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV002｜利益重分配 | 账号样本数 16、命中数 16 | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV003｜组织视角 | 账号样本数 16、命中数 15 | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV004｜风险传导 | 账号样本数 16、命中数 14、阅读差异 +40pp | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV005｜身份代入 | 账号样本数 16、命中数 14、阅读差异 +40pp | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |
| CV006｜结尾动作 | 账号样本数 16、命中数 13 | 证据引用待补录；平台样本字段 UNKNOWN；成功数/成功率 UNKNOWN |

这说明旧 L2 不是完全丢失；但它只被摘要式搬运，没有完整证据血缘。

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

断链性质：证据存在，但没有按 Parameter 记录建立 Evidence References。

Runtime 影响：COMPILE 能看到 CV 当前状态和触发资格，但看不到每个状态来自哪些样本、哪些反例、哪些统计。

### 2. Observation → Parameter Registry

`data/Milestone_Observations.md` 已定义 Observation 与 Parameter 的隔离关系，并要求：

```text
每次参数修改必须在 Parameter 记录的"证据引用"字段关联 Observation ID
```

但当前 CV001-CV010 的 `证据引用` 多为“待补录”。

断链性质：治理层已经定义血缘规则，但历史迁移没有执行完。

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
| 变量标注 | `l2_variable_records.md` | Evidence Asset | 应接回 Registry 的证据引用 |
| 变量验证 | `l2_variable_validation.md` | Evidence Asset | 应接回 Registry 的账号字段和反例字段 |
| 治理观察 | `data/Milestone_Observations.md` | Governance Asset | 应建立 Observation ID → Parameter Evidence References |
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
L1/L2 只能通过治理迁移进入 Parameter Registry 或 refreshed Runtime Snapshot 后，才影响生产。
```

## Recommended Next Action

不要重采全部历史数据。先做一次最小迁移试点：

1. 选择 CV001-CV006 六个 ACTIVE 参数。
2. 对每个参数补齐 `Evidence References`，引用：
   - `l2_variable_records.md`
   - `l2_variable_validation.md`
   - 必要时引用 `reports/l1_sample_report.md`
3. 只迁移已经存在的事实，不新增状态，不改变触发资格。
4. 保持平台字段为 UNKNOWN，除非存在可归属平台样本统计。
5. 保持账号成功数 / 成功率为 UNKNOWN，除非 Evidence Gate 放行对应 Production 结果。
6. 迁移完成后重新 release TRIAL Runtime。

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
