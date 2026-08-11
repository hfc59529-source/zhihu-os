# Governance Issue：Publish Runtime Consistency（发布节点协议状态矛盾）

Status：**DECIDED**（Governance Decision，2026-08-11）——`data/Publish_Queue.md` 是当前 TRIAL Runtime 已生效的强制执行资产，"唯一入口"规则现在就在约束生产行为；`ZH-20260808-001/002/003`、`ZH-20260809-001` 四次人工直接发布判定为 **Gate Bypass（治理异常）**，作为历史事实记录存档，不据此新增第二条发布路径，不据此放宽《生产状态机与交接规范》的"唯一入口"表述。

Proposed By：Claude（起草，基于用户核对 `main` 权威文件后的裁决方向），发现来源：`data/production_ledger.md` 2026-08-11 补账过程中，核对 `data/production_article_map.csv` 发现 4 篇已发布记录在 `data/Publish_Queue.md` 中无入队记录。

## 1. 现状：三处权威文件同时成立但相互矛盾

1. `docs/生产状态机与交接规范.md`：`RELEASE_READY` 是进入 `data/Publish_Queue.md` 的唯一生产状态入口；已存在 `Release-v1.md` 不能单独作为入队依据；未获得 `USER_APPROVED` 前不得作为当前入队依据。
2. `runtime/ACTIVE_MANIFEST.md`（TRIAL，2026-08-10 12:52:59 UTC 发布）：`data/Publish_Queue.md` 被列入 `Node Execution Assets` 分区，与 `templates/GPT审核清单.md`、`docs/生产状态机与交接规范.md` 同级——即被当前已发布的 Runtime 正式声明为生效执行资产。
3. `data/Publish_Queue.md` 自身：`## 发布闭环（后续单独验证，当前不执行）`，其下的流程图从 `USER_APPROVED` 一路画到 `数据回流`，字面上把整条链路（含 Publish Queue 节点本身）都框进"当前不执行"。

三者同时读，得到互斥结论：Runtime 说这是已生效资产，状态机说这是唯一入口，队列文件自己说不执行——但 `data/production_article_map.csv` 显示 4 篇文章已经绕开这一切，人工发布并已产生 `answer_url`（`answer_2069522411372933416` / `answer_2069533843439235799` / `answer_2069537531780129888` / `answer_2069838524929594559`，均 `trace_status: COMPLETE`）。

## 2. 裁决

采纳"已启用"解释：`data/Publish_Queue.md` 中"当前不执行"一句，裁定其效力范围仅限于该节标题下方流程图里 Publish Queue **之后**的自动化/脚本化执行步骤（写入知乎草稿箱、最终检查、正式发布动作本身、24h/72h/7天数据回流的自动采集），这些确实目前只能人工手动做；**不包括** "只有 `RELEASE_READY` 才能入队"这条 Gate 规则本身——这条规则的权威定义在《生产状态机与交接规范》，且已被 Runtime Manifest 纳入生效资产，现在就应当被遵守。

理由：
- 若采纳"未启用"解释，等于承认过去一周的 4 次人工发布是合规的，但 4 篇里只有 808-002 留有实质性用户审阅文字记录，808-001 完全没有、809-001 连 `Production_Decision.md` 都不存在——追认这类发布为合规，会实质性瓦解 `USER_APPROVED` 门禁的意义。
- Runtime Manifest 是当前系统对"什么已生效"的唯一正式声明；`Publish_Queue.md` 文件内部的松散措辞不应凌驾于 Manifest 的正式收录之上。

## 3. 处置

- `ZH-20260808-001/002/003`、`ZH-20260809-001` 四条记录在 `data/production_ledger.md` 中标注为 `LEGACY_RELEASE_COMPLETED` 并附带专门说明（2026-08-11 已补），明确其不代表符合当前 Release Gate 规则。
- 本文件视为该异常的正式治理记录；`data/Publish_Queue.md` 补充一节 `## Gate Bypass Log`，逐条登记这 4 次绕过，作为审计留痕（见本次同步修改）。
- **不修改**《生产状态机与交接规范》的"唯一入口"表述，**不新增**第二种"人工直接发布"合法路径。
- **不追溯处罚**已发布内容（不会要求下架/撤回），处置仅针对台账记录层面。

## 4. 待决策问题（留给后续 Governance Review，本次不处理）

1. `data/Publish_Queue.md` 措辞本身存在歧义（"当前不执行"字面覆盖了整条链路，包括 Gate 本身），是否需要重写该节标题和流程图注释，明确区分"Gate 规则（现在生效）"与"下游自动化步骤（现在不生效）"？
2. 为什么这 4 次绕过没有在事发时被任何审计流程拦截？是否需要在 WRITE→AUDIT→REVIEW 链路之外，为"人工在系统外直接发布"这个动作本身增加一个强制记录点（例如发布前必须先在 Publish_Queue.md 登记，哪怕是人工发布）？
3. 是否需要 `scripts/validate_runtime_consistency.py` 新增一项校验：`data/production_article_map.csv` 中每条 `trace_status=COMPLETE` 的记录，都必须能在 `data/Publish_Queue.md` 或 ledger 中找到对应的 `USER_APPROVED` 证据，否则校验失败？

本 Issue 不预支上述三题的答案，留待下一次 Governance Review 处理。
