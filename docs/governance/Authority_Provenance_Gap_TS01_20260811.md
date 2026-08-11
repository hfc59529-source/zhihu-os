# Governance Observation：TS01 Authority Provenance Gap

日期：2026-08-11

状态：SUPPORTED（Governance Observation）

关联对象：

- `runtime/知乎结构库快照.md`：`ACTIVE-TS01｜老师爆款机制推进结构`
- `docs/知乎OS Structure Evolution V1.md`：ACTIVE 结构升级门槛
- `reports/notion_retirement_migration_ledger.md`：Notion 退役与迁移台账
- `docs/governance/Observation_Content_Value_Gate_Missing_20260811.md`
- `productions/ZH-20260811-001/`

## 结论

TS01 当前的 ACTIVE 身份存在 Authority Provenance Gap。

仓库中未找到 TS01 满足 `docs/知乎OS Structure Evolution V1.md` §4 ACTIVE 升级门槛的完整记录：

- 多个知乎高表现样本共同结构；
- 同题或相似题低表现反例；
- 明确适用边界 / 触发条件 / 禁用边界；
- 至少一次本账号实验验证；
- 同题 / 同结构收入不低于可比中位数；
- 与现有 ACTIVE 结构不重复。

相反，`reports/notion_retirement_migration_ledger.md` 显示，TS01 的主要血统来自 Notion 旧结构资产，尤其是“结构01｜反常识—选择权”的大量吸收；相关旧结构走的是 `SKIP / ARCHIVE` 迁移路径，不是通过当前 Git Schema 下的 ACTIVE 升级门槛后正式晋升。其相邻旧结构“结构00｜通用解释六段式”还明确带有“验证次数 0 / 验证等级假设”性质。

因此，本条不判定“TS01 内容一定错误”，而是判定：

```text
TS01 的 Contract Authority 缺少当前 Schema 可接受的证据链。
```

## 与 FP-20260811-002 的区别

`FP-20260811-002` / `Observation_Content_Value_Gate_Missing_20260811.md` 记录的是：

```text
机器 Gate PASS，但人工认为成品不可发。
```

那是一条 Production Quality Observation，需要后续样本复现才能判断是否修改 DECISION / COMPILE / WRITE / AUDIT。

本条记录的是：

```text
一个 Runtime ACTIVE 结构的 ACTIVE 身份本身缺少 provenance。
```

这是 Authority Model / Migration Provenance 问题，不依赖三篇生产复现。只要当前仓库无法提供 ACTIVE 晋升证据，而迁移台账又显示其来自旧资产吸收，就足以成立为治理缺口。

## 证据

### 1. Runtime 中 TS01 拥有合同化执行路径

`runtime/知乎结构库快照.md` 原设计要求：

```text
选择一个 ACTIVE 结构
↓
读取该结构完整字段
↓
完成本题结构实例化
↓
生成 Execution IR.Structure（含 required_steps 与 step_obligations）
```

`docs/知乎OS Compiler V1.md` 第5节又要求 COMPILE 把结构实例化结果写入 `Execution IR.Structure.required_steps / step_obligations`，并交由 AUDIT 核对。

这意味着 TS01 一旦被选中，就不是“写作参考”，而是可以被编译为单篇正文合同。

### 2. TS01 血统来自旧 Notion 结构吸收

`reports/notion_retirement_migration_ledger.md` 记录旧 Notion 结构资产迁移时，对“结构01｜反常识—选择权”的处理不是 ACTIVE 晋升，而是历史归档 / 部分吸收；TS01 大量吸收其内容。该路径不等价于 `Structure Evolution V1` §4 所要求的当前 Git ACTIVE 升级流程。

该 ledger 还多次明确警告：旧复盘、旧规律、旧收益协议不得直接写成 SUPPORTED，不得自动推进 Parameter，不得绕过 Evidence Split / Observation candidate / 重新验证。

### 3. 仓库未找到 TS01 满足五条 ACTIVE 门槛的验证记录

当前可检索证据中，未找到一份记录 TS01 已完成：

```text
平台样本统计
↓
低表现反例对照
↓
本账号实验验证
↓
收益不低于可比中位数
↓
治理批准 ACTIVE
```

因此不能把“历史遗留结构存在”推定为“当前 Contract Authority 成立”。

## Root Cause

这是迁移期 Authority Escalation 缺陷：

```text
Legacy Notion Structure / Pattern
↓
部分吸收进 Git Runtime Snapshot
↓
标记为 ACTIVE
↓
COMPILE 编译为 required_steps / step_obligations
↓
WRITE 被迫履约
↓
AUDIT 按合同核对
```

缺失的环节是：

```text
Legacy asset
↓
Evidence Split
↓
Observation / Candidate Structure
↓
Structure Evolution V1 §4 验证
↓
ACTIVE Contract Authority
```

## 处理原则

本条不要求立即改写 TS01 内容，也不直接判断 TS01 应删除。

正确处置是先修 Authority Model：

1. 未补齐 provenance 的结构不得拥有完整 Contract Authority。
2. 旧 Notion 资产吸收不得自动继承为当前 ACTIVE。
3. 效果代理、经验结构、历史规律在未完成当前证据链前，只能作为 advisory / review 材料。
4. COMPILE 不得把 provenance 缺失对象自动写入 `required_steps` / `step_obligations` / `Acceptance Criteria`。

## 已执行处置

2026-08-11 已落地 Authority Provenance Patch：

- `docs/知乎OS Compiler V1.md` 新增 `Authority Provenance Check`。
- `runtime/知乎结构库快照.md` 将 TS01 / TS02 标记为 `PROVISIONAL_ADVISORY`。
- `runtime/知乎ACTIVE规律快照.md` 将来源为“存量ACTIVE，待平台样本统计复核”的规律降级为 `LEGACY_REVIEW / ADVISORY_ONLY`。
- `docs/知乎OS权威归属表.md` 同步执行权限说明。
- `runtime/ACTIVE_MANIFEST.md` 已重新发布 TRIAL，Based On Commit：`5d8c41e218db3e5172bef1564d8f003cee6d1711`。

## 后续验证

下一篇生产应检查 Execution IR：

- 若调用 TS01 / TS02，只能记录为 provisional advisory reference。
- `required_steps` 必须来自本题 Decision 的必要推导，不得搬运固定十步。
- AUDIT 不能因 Draft 未兑现 TS01 固定模板步骤而判 Execution Compliance 失败。

如果后续希望 TS01 恢复 `VERIFIED_CONTRACT`，必须单独补齐 Structure Evolution V1 §4 证据，不得用本条 Observation 反向追认。
