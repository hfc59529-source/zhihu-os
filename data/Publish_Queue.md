# Publish Queue

独立于生产 Ledger 的发布队列。生产闭环（Draft→Audit→Decision→Patch→Final Validation→Release）和发布闭环（Publish Queue→人工确认→草稿箱→最终检查→正式发布→数据回流）彻底分开，避免定位问题时混淆是文案问题还是发布问题。

| Production ID | 发布时间 | 状态 |
|---|---|---|
| ZH-20260801-002 | 待定 | Ready |
| ZH-20260801-003 | 待定 | Ready |

**状态取值**：Ready（Release-v1 已就绪，未排期）/ Scheduled（已排定发布时间）/ Draft Box（已写入知乎草稿箱，等人工最终检查）/ Published（已正式发布）

## 发布闭环（后续单独验证，当前不执行）

```
Release-v1
↓
Publish Queue（本文件）
↓
人工确认
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

1. 继续生产至 ZH-20260801-010（生产闭环优先，样本量不足以支撑复盘）
2. 本队列先积累 Ready 项，不自动写入知乎草稿箱
3. 等有一批 Ready 后，统一安排固定时间发布，控制发布时间变量
