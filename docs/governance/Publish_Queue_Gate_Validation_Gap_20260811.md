# Governance Observation：Publish Queue Gate Validation Gap

日期：2026-08-11

状态：SUPPORTED（Governance Observation）

关联对象：

- `docs/governance/Publish_Runtime_Consistency_Issue_20260811.md`
- `data/Publish_Queue.md`
- `data/production_article_map.csv`
- `data/production_ledger.md`
- `scripts/validate_runtime_consistency.py`
- `docs/生产状态机与交接规范.md`

## 结论

Publish Queue Gate 当前仍存在真实执行缺口。

`Publish_Runtime_Consistency_Issue_20260811.md` 已裁决：

```text
RELEASE_READY → Publish Queue 是当前生效 Gate。
历史 4 次人工直接发布属于 Gate Bypass。
不新增第二条人工直接发布合法路径。
```

但当前 `scripts/validate_runtime_consistency.py` 中没有任何针对 `data/production_article_map.csv`、`USER_APPROVED`、`Publish_Queue.md` 或 `production_ledger.md` 的交叉校验逻辑。

因此，同类绕过现在仍然可能再次发生：

```text
人工直接发布
↓
production_article_map.csv 记录 trace_status=COMPLETE
↓
但 Publish Queue / USER_APPROVED 证据缺失
↓
validate_runtime_consistency.py 不会拦截
```

## 为什么这不是纯文档回填

Proposal-B 头部状态矛盾、RR-03/RR-05 Wiring Gap 过期，主要是记录滞后：实际 Runtime 已大体按正确方向运转。

本条不同。

这里的风险仍在执行层存在：已裁决的 Gate 缺少机器校验或强制审计检查，导致同一种 Gate Bypass 可以复发。

## 已有证据

`Publish_Runtime_Consistency_Issue_20260811.md` 已记录：

- `data/Publish_Queue.md` 已被当前 TRIAL Runtime Manifest 纳入执行资产；
- `docs/生产状态机与交接规范.md` 定义 `RELEASE_READY` 是入队入口；
- 历史 4 篇已发布记录绕过了队列；
- 这些绕过只作为历史异常存档，不放宽当前 Gate。

该文件第4节待决问题 3 明确提出：

```text
是否需要 validate_runtime_consistency.py 新增校验：
data/production_article_map.csv 中 trace_status=COMPLETE 的记录，
必须能在 data/Publish_Queue.md 或 ledger 中找到 USER_APPROVED 证据。
```

当前脚本未实现该校验。

## 风险

1. 人工发布动作再次绕过 `USER_APPROVED → RELEASE_READY → Publish Queue`。
2. 发布后补账时才发现证据断裂，无法在事前阻断。
3. `data/production_article_map.csv` 与 `data/Publish_Queue.md` / `production_ledger.md` 长期分叉。
4. Runtime Manifest 校验通过，但实际发布台账已违反 Release Gate。

## 处理原则

本条不直接修改脚本。

后续治理评审需要决定是否新增最小校验：

```text
For each row in data/production_article_map.csv:
  if trace_status == COMPLETE:
    require evidence in data/Publish_Queue.md or data/production_ledger.md:
      USER_APPROVED
      RELEASE_READY or PUBLISHED
      matching Production ID or article_id / answer_url
```

同时必须处理历史例外：

- `LEGACY_RELEASE_COMPLETED` / Gate Bypass Log 中已登记的历史 4 篇，不应导致当前校验失败；
- 但后续新增 COMPLETE 记录不能再无证据通过。

## 后续验证

若实施脚本校验，应至少验证三类样本：

1. 合规发布：有 `USER_APPROVED` 和 Publish Queue / ledger 证据，应 PASS。
2. 历史绕过：已登记为 `LEGACY_RELEASE_COMPLETED`，应 PASS with legacy exception。
3. 新绕过：`trace_status=COMPLETE` 但无 `USER_APPROVED` / queue / ledger 证据，应 FAIL。

本条 Observation 不决定具体脚本实现，只确认当前 Gate 缺少执行层防复发机制。
