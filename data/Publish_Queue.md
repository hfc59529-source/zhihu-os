# Publish Queue

独立于生产 Ledger 的发布队列。生产闭环（Draft→Audit→Decision→Patch→Patch Validation→User Review→Release）和发布闭环（Publish Queue→草稿箱→最终检查→正式发布→数据回流）彻底分开，避免定位问题时混淆是文案问题还是发布问题。

## 入队前置条件

当前有效入口只能是：

```text
USER_APPROVED
↓
Release-v1
↓
RELEASE_READY
↓
Publish Queue
```

Audit PASS 或 Patch Validation PASS 之后只能进入 `READY_FOR_USER_REVIEW`，不得生成或确认 Release，不得进入 Publish Queue；只有用户明确 `USER_APPROVED` 后，后续生产角色才能生成或确认 `Release-v1.md`，并将状态更新为 `RELEASE_READY`。

已存在 `Release-v1.md` 不能单独作为入队依据。

## 历史队列

以下 002-010 属于用户验收节点建立前的历史批次，保留原始记录事实，不补造 `USER_APPROVED`。

| Production ID | 发布时间 | 状态 |
|---|---|---|
| ZH-20260801-002 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-003 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-004 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-005 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-006 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-007 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-008 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-009 | 待定 | LEGACY_RELEASE_READY |
| ZH-20260801-010 | 待定 | LEGACY_RELEASE_READY |

**状态取值**：RELEASE_READY（用户已验收，Release-v1 已就绪，未排期）/ QUEUED（已进发布队列）/ DRAFT_BOX（已写入知乎草稿箱，等人工最终检查）/ PUBLISHED（已正式发布）/ LEGACY_RELEASE_READY（历史批次已完成当时版本 Release 文件，但未经过当前 User Review Gate）

## 发布闭环（后续单独验证，当前不执行）

```
USER_APPROVED
↓
Release-v1
↓
RELEASE_READY
↓
Publish Queue（本文件）
↓
写入知乎草稿箱
↓
人工最终检查
↓
正式发布
↓
24h / 72h / 7天 数据回流
```

## 当前优先级

1. 011 起，未经过 `USER_APPROVED` 的 Production 不得进入本队列。
2. 历史批次只保留事实，不回填用户验收。
3. 等有一批真正 `RELEASE_READY` 后，统一安排固定时间发布，控制发布时间变量。
